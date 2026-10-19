"""Build Seamworks as a gray map: the ground in stone under a yellow crust, the cuts carved to their depths with
stairs on every one-block rise of a ramp, panels voxelised as leaning quads, plated seams over lava, spoil heaps,
plain stone-brick buildings, the drift tunnels and the objectives.

    python3 gen.py <build-dir>
"""
import math
import sys

import numpy as np

import plan as P
from pgmvox import B, World
from pgmvox.core.orient import ladder, stair
from pgmvox.play.objectives import DYES

YS = P.YS
CRUST = (B.STAINED_CLAY, 4)
ROCK_TOP = (B.STONE, 0)
FLOOR = (B.STONE, 6)
PANEL = [(B.STAINED_CLAY, 8), (B.STAINED_CLAY, 7)]
PLATE = (B.IRON_BLOCK, 0)
SPOIL = (B.DIRT, 1)
WALL = (B.STONEBRICK, 0)
LIGHT = (B.GLOWSTONE, 0)

w = World(-1, -1, P.W + 2, P.H + 2, sy=YS + 40)
X, Z = w.grid()
CX, CZ = X + 0.5, Z + 0.5


def mask(poly):
    """The columns whose centres lie inside a polygon."""
    xs = np.array([p[0] for p in poly]); zs = np.array([p[1] for p in poly])
    inside = np.zeros(X.shape, bool)
    j = len(poly) - 1
    for i in range(len(poly)):
        cond = ((zs[i] > CZ) != (zs[j] > CZ)) & (CX < (xs[j] - xs[i]) * (CZ - zs[i]) / (zs[j] - zs[i] + 1e-12) + xs[i])
        inside ^= cond
        j = i
    return inside


def cells(m):
    for i, k in zip(*np.nonzero(m)):
        yield int(i + w.x0), int(k + w.z0)


# ---- the ground: bedrock under stone, the crust on top, a rim of bedrock and barrier round the board ------------------------------
board = (X >= 0) & (X < P.W) & (Z >= 0) & (Z < P.H)
w.ids[:, 0, :] = B.BEDROCK
for x, z in cells(board):
    top = P.ground(x, z) - 1
    w.column(x, z, 1, top - 1, B.STONE)
    w.set(x, top, z, *CRUST)
for x, z in cells(~board):
    w.column(x, z, 0, YS - 1, B.BEDROCK)
    w.column(x, z, YS, YS + 34, B.BARRIER)

# ---- floor depths -------------------------------------------------------------------------------------------------
depth = np.full(X.shape, np.nan)
ramp = np.zeros(X.shape, bool)
uphill = np.zeros(X.shape + (2,))
for k, cut in enumerate(P.CUTS):
    depth[mask([p for p, _ in cut])] = P.CUT_DEPTH[k]
floor_any = ~np.isnan(depth)
for z_ in P.ZONES:
    m = mask(z_[0]) & floor_any
    if len(z_) == 2:
        depth[m] = z_[1]
        ramp[m] = False
        continue
    (lp, ld), (hp, hd) = z_[1], z_[2]
    vx, vz = hp[0] - lp[0], hp[1] - lp[1]
    t = np.clip(((CX - lp[0]) * vx + (CZ - lp[1]) * vz) / (vx * vx + vz * vz), 0, 1)
    depth[m] = (ld + (hd - ld) * t)[m]
    ramp[m] = True
    uphill[m] = (vx, vz)
for rock in P.ROCKS:
    depth[mask(rock)] = np.nan
D = np.where(np.isnan(depth), 0, np.floor(depth + 0.5)).astype(int)
floor = ~np.isnan(depth)

for x, z in cells(floor):
    d = D[x - w.x0, z - w.z0]
    w.column(x, z, YS + d - 1, P.ground(x, z) - 1, B.AIR)
    w.set(x, YS + d - 1, z, *FLOOR)
for rock in P.ROCKS:
    for x, z in cells(mask(rock)):
        w.set(x, P.ground(x, z) - 1, z, *ROCK_TOP)


def feet(x, z):
    return YS + int(D[x - w.x0, z - w.z0])


# stairs on every one-block rise of a ramp, facing up it
for x, z in cells(floor & ramp):
    i, k = x - w.x0, z - w.z0
    ux, uz = uphill[i, k]
    sx, sz = (int(np.sign(ux)), 0) if abs(ux) >= abs(uz) else (0, int(np.sign(uz)))
    j, l = i + sx, k + sz
    if 0 <= j < w.sx and 0 <= l < w.sz and floor[j, l] and D[j, l] == D[i, k] + 1:
        w.set(x, feet(x, z), z, B.STONEBRICK_STAIRS, stair((sx, sz)))

# ---- buildings: each section its own storeys, a slab every storey with its ladder's hole, windows where the
# outside is open, a wall wherever a section stands over its neighbour ------------------------------------------------
DIRS = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}
for name, poly, d, sections in P.BUILDINGS:
    m = mask(poly)
    storeys = np.zeros(X.shape, int)
    for (x0, z0, x1, z1), n, _ in sections:
        storeys[(X >= x0) & (X < x1) & (Z >= z0) & (Z < z1) & m] = n + P.storeys_below(d)
    base = YS + d
    for x, z in cells(m):
        i, k = x - w.x0, z - w.z0
        n = storeys[i, k]
        roof = base + n * P.STOREY
        w.column(x, z, base - 1, roof, *WALL)
        rim = [storeys[i + a, k + b] for a, b in DIRS.values()]
        for level in range(n):
            floor_y = base + level * P.STOREY
            if min(rim) == 0 or any(r <= level for r in rim):
                # an outside wall at this storey: a window two high every fourth cell, where the outside is open air
                if level > 0 and (x + z) % 4 == 0:
                    for a, b in DIRS.values():
                        if storeys[i + a, k + b] <= level and w.id(x + a, floor_y + 1, z + b) == B.AIR \
                                and w.id(x + a, floor_y + 2, z + b) == B.AIR:
                            w.column(x, z, floor_y + 1, floor_y + 2, B.AIR)
                continue
            w.column(x, z, floor_y, floor_y + P.STOREY - 2, B.AIR)
            if (x * 3 + z) % 7 == 0:
                w.set(x, floor_y + P.STOREY - 1, z, *LIGHT)
    for _, n, ((lx, lz), side) in sections:
        n += P.storeys_below(d)
        a, b = DIRS[side]
        for y in range(base, base + (n - 1) * P.STOREY + 1):
            w.set(lx, y, lz, B.LADDER, ladder((a, b)))
        w.column(lx + a, lz + b, base, base + (n - 1) * P.STOREY + 1, *WALL)
for name, door in P.DOORS:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if n == name and any(P.pip((c[0] + .5, c[1] + .5), pg) for c in door))
    for x, z in door:
        w.column(x, z, YS + d, YS + d + 2, B.AIR)

# ---- panels: a quad on the floor leaning back into the earth, two blocks thick, the wedge before it cleared ---------
for a, b, n, (l0, l1), shade in P.panels():
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    inside = (int(math.floor((a[0] + b[0]) / 2 - n[0] * .6)), int(math.floor((a[1] + b[1]) / 2 - n[1] * .6)))
    base = feet(*inside) if floor[inside[0] - w.x0, inside[1] - w.z0] else YS - 10
    behind = (int(math.floor((a[0] + b[0]) / 2 + n[0] * 4)), int(math.floor((a[1] + b[1]) / 2 + n[1] * 4)))
    rise = P.ground(*behind) + P.LIP - base
    clear, solid = set(), set()
    for s in np.arange(0, 1.0001, 0.2 / max(length, 1)):
        bx, bz = a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s
        lean = math.tan(math.radians(l0 + (l1 - l0) * s))
        for t in np.arange(0, 1.0001, 0.2 / rise):
            y = base + t * rise
            back = lean * t * rise
            for o in np.arange(0, back, 0.4):
                clear.add((math.floor(bx + n[0] * o), math.floor(y), math.floor(bz + n[1] * o)))
            for k in np.arange(0, 2.0, 0.4):
                solid.add((math.floor(bx + n[0] * (back + k)), math.floor(y), math.floor(bz + n[1] * (back + k))))
    for c in clear - solid:
        if c[1] < P.ground(c[0], c[2]) and not floor[c[0] - w.x0, c[2] - w.z0]:
            w.set(*c, B.AIR)
    for c in solid:
        w.set(*c, *PANEL[shade])

# ---- plated seams: plates over a trench to the lava, the missing ones open -------------------------------------------
def seam_trench(x, z, top):
    w.column(x, z, P.SEAM_Y + 1, top, B.AIR)
    w.set(x, P.SEAM_Y, z, B.LAVA)
    w.column(x, z, P.SEAM_Y - 2, P.SEAM_Y - 1, B.STONE)


for lo, hi, width, rows, missing in P.STRIPS:
    L = math.hypot(hi[0] - lo[0], hi[1] - lo[1])
    ax = ((hi[0] - lo[0]) / L, (hi[1] - lo[1]) / L)
    U = (CX - lo[0]) * ax[0] + (CZ - lo[1]) * ax[1]
    V = -(CX - lo[0]) * ax[1] + (CZ - lo[1]) * ax[0]
    strip = floor & (U >= 0) & (U <= sum(rows)) & (np.abs(V) <= width / 2)
    edges = np.cumsum([0] + rows)
    for x, z in cells(strip):
        i, k = x - w.x0, z - w.z0
        row = int(np.searchsorted(edges, U[i, k], side="right") - 1)
        col = 0 if V[i, k] < 0 else 1
        top = feet(x, z) - 1
        if abs(V[i, k]) <= width / 2 - 1.2:
            seam_trench(x, z, top)
        if (min(row, len(rows) - 1), col) not in missing:
            w.set(x, top, z, *PLATE)

for boxes, turned in P.SUMP:
    for j, (bx, bz, bw, bd) in enumerate(boxes):
        for x in range(int(bx), int(bx + bw)):
            for z in range(int(bz), int(bz + bd)):
                if not floor[x - w.x0, z - w.z0]:
                    continue
                top = feet(x, z) - 1
                if bz + 1 <= z < bz + bd - 1:
                    seam_trench(x, z, top)
                if j not in P.SUMP_MISSING:
                    w.set(x, top, z, *PLATE)

# ---- spoil: heaped from the toe to the crest, the scar behind hollowed ---------------------------------------------
def seg_dist(px, pz, a, b):
    vx, vz = b[0] - a[0], b[1] - a[1]
    t = np.clip(((px - a[0]) * vx + (pz - a[1]) * vz) / (vx * vx + vz * vz), 0, 1)
    return np.hypot(px - a[0] - t * vx, pz - a[1] - t * vz)


def poly_edge_dist(poly):
    return np.min([seg_dist(CX, CZ, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))], axis=0)


for sp in P.SPOILS:
    if sp["scar"]:
        for x, z in cells(mask(sp["scar"]) & ~floor):
            top = P.ground(x, z)
            w.column(x, z, top - 4, top - 1, B.AIR)
            w.set(x, top - 5, z, *SPOIL)
    toe = mask(sp["toe"]) & floor
    to_toe = poly_edge_dist(sp["toe"])
    to_crest = np.min([seg_dist(CX, CZ, sp["crest"][i], sp["crest"][i + 1]) for i in range(len(sp["crest"]) - 1)],
                      axis=0)
    rise = sp["peak"] * (to_toe / (to_toe + to_crest + 1e-9)) ** 0.8
    for x, z in cells(toe):
        h = int(round(rise[x - w.x0, z - w.z0]))
        if h > 0:
            w.column(x, z, feet(x, z), feet(x, z) + h - 1, *SPOIL)

for a, b, reach, turn, h0, h1, is_turned in P.FALLEN:
    cut = [p for p, _ in (P.CUTS[1] if is_turned else P.CUTS[0])]
    n = P.outward(a, b, cut)
    n = (-n[0], -n[1])
    r = math.radians(turn)
    n = (math.cos(r) * n[0] - math.sin(r) * n[1], math.sin(r) * n[0] + math.cos(r) * n[1])
    floor_y = feet(math.floor((a[0] + b[0]) / 2 + n[0] * 2), math.floor((a[1] + b[1]) / 2 + n[1] * 2))
    laid = {}
    for s in np.arange(0, 1.0001, 0.05):
        for t in np.arange(0, 1.0001, 0.03):
            x = math.floor(a[0] + (b[0] - a[0]) * s + n[0] * reach * t)
            z = math.floor(a[1] + (b[1] - a[1]) * s + n[1] * reach * t)
            if floor[x - w.x0, z - w.z0]:
                laid[(x, z)] = round(floor_y + h0 + (h1 - h0) * t)
    for (x, z), y in laid.items():
        w.column(x, z, y, y + 6, B.AIR)                  # the spoil it fell on stays under it, never over it
        w.set(x, y, z, *PANEL[0])

# ---- the drift tunnels: four wide, four high, level along each leg's arc, the shaft's ladder up to the crust ---------
def bore(path, d0, d1, lights=True):
    lengths = [math.hypot(path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]) for i in range(len(path) - 1)]
    total = sum(lengths)
    run = 0.0
    for i, seg in enumerate(lengths):
        a, b = path[i], path[i + 1]
        ux, uz = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg
        for s in np.arange(0, seg, 0.4):
            d = round(d0 + (d1 - d0) * (run + s) / total)
            px, pz = a[0] + ux * s, a[1] + uz * s
            for o in np.arange(-2, 2.01, 0.4):
                x, z = math.floor(px - uz * o), math.floor(pz + ux * o)
                if floor[x - w.x0, z - w.z0]:
                    continue
                w.column(x, z, YS + d, YS + d + 3, B.AIR)
                w.set(x, YS + d - 1, z, *FLOOR)
                if lights and abs(o) < .2 and int(run + s) % 7 == 0:
                    w.set(x, YS + d + 4, z, *LIGHT)
        run += seg


branch_depth = -8 - 2 * 10.2 / 46.5          # the main tunnel's depth where the branch leaves it
for turned in (False, True):
    T = (lambda p: P.R(p)) if turned else (lambda p: p)
    bore([T(p) for p in P.TUNNEL], -8, -10)
    bore([T(p) for p in P.BRANCH], branch_depth, branch_depth)
    sx, sz = (P.W - 1 - P.SHAFT[0], P.H - 1 - P.SHAFT[1]) if turned else P.SHAFT
    wall = (1, 0) if turned else (-1, 0)
    low = YS + round(branch_depth)
    top = P.ground(sx, sz)
    w.column(sx, sz, low, top - 1, B.AIR)
    w.column(sx + wall[0], sz, low - 1, top - 1, B.STONE)
    for y in range(low, top):
        w.set(sx, y, sz, B.LADDER, ladder(wall))

# ---- ladders up the cut walls: a stone backing up to the crust, a gap in the panels' lip over it --------------------
for (x, z), side in P.LADDERS:
    dx, dz = DIRS[side]
    bottom = feet(x, z)
    top = P.ground(x + dx, z + dz)
    w.column(x, z, bottom, top + 3, B.AIR)
    w.column(x + dx, z + dz, bottom, top - 1, B.STONE)
    for y in range(bottom, top):
        w.set(x, y, z, B.LADDER, ladder((dx, dz)))
    for k in range(1, 7):
        for o in (-1, 0, 1):
            cx, cz = x + dx * k + (o if dx == 0 else 0), z + dz * k + (o if dz == 0 else 0)
            here = P.ground(cx, cz)
            w.column(cx, cz, here, here + 4, B.AIR)
            if k > 1 and w.id(cx, here - 1, cz) == B.AIR:
                w.set(cx, here - 1, cz, *CRUST)

# ---- the objectives: the flags' banners at their first posts, the monuments --------------------------------------------
from mapxml import OBJECTIVES  # noqa: E402

OBJECTIVES.stamp(w)
for team, (x, z), d in ((0, P.FLAG_POSTS[0][1], P.FLAG_POSTS[0][2]),
                        (1, (P.W - 1 - P.FLAG_POSTS[0][1][0], P.H - 1 - P.FLAG_POSTS[0][1][1]), P.FLAG_POSTS[0][2])):
    w.banner(x, YS + d, z, 15 - DYES["green" if team == 0 else "purple"], rot=12 if team == 0 else 4)

w.save(sys.argv[1], "Seamworks", (P.SPAWN_AT[0], YS - 8, P.SPAWN_AT[1]))
print("generated", int(floor.sum()), "floor columns")
