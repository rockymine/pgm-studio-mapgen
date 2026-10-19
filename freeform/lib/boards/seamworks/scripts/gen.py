"""Build Seamworks: the ground in rock under an ash crust, the cuts carved to their depths with their floors worn and
their flights stepped along wandering edges, the steel panels voxelised as leaning quads that meet at clean joints,
plated seams over lava, spoil heaps, the works in banded concrete with their storeys over the crust, the drift
tunnels timbered, a market in each forecourt, and the objectives. What each part is made of is `look.py`'s.

    python3 gen.py <build-dir>
"""
import math
import sys

import numpy as np

import look as L
import plan as P
from pgmvox import B, World
from pgmvox.built import props
from pgmvox.core.orient import ladder, stair
from pgmvox.play.objectives import DYES

YS = P.YS
DIRS = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}

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


def grow(m, r):
    """A mask widened by r columns, by the chessboard."""
    out = m.copy()
    for _ in range(r):
        g = out.copy()
        g[1:, :] |= out[:-1, :]; g[:-1, :] |= out[1:, :]; g[:, 1:] |= out[:, :-1]; g[:, :-1] |= out[:, 1:]
        g[1:, 1:] |= out[:-1, :-1]; g[:-1, :-1] |= out[1:, 1:]; g[1:, :-1] |= out[:-1, 1:]; g[:-1, 1:] |= out[1:, :-1]
        out = g
    return out


def point_mask(points):
    m = np.zeros(X.shape, bool)
    for x, z in points:
        if 0 <= x - w.x0 < w.sx and 0 <= z - w.z0 < w.sz:
            m[x - w.x0, z - w.z0] = True
    return m


# ---- the ground: bedrock under rock, the ash crust on top, a rim of bedrock and barrier round the board -------------
board = (X >= 0) & (X < P.W) & (Z >= 0) & (Z < P.H)
w.ids[:, 0, :] = B.BEDROCK
for x, z in cells(board):
    top = P.ground(x, z) - 1
    w.column(x, z, 1, top - 1, B.STONE)
    w.set(x, top, z, *L.crust(x, z))
for x, z in cells(~board):
    w.column(x, z, 0, YS - 1, B.BEDROCK)
    w.column(x, z, YS, YS + 34, B.BARRIER)
L.paint_rock(w)

# ---- floor depths: each cut's own, then its zones; a flight's step edges wander with the noise ----------------------
depth = np.full(X.shape, np.nan)
ramp = np.zeros(X.shape, bool)
uphill = np.zeros(X.shape + (2,))
for k, cut in enumerate(P.CUTS):
    depth[mask([p for p, _ in cut])] = P.CUT_DEPTH[k]
floor_any = ~np.isnan(depth)
STEP = np.zeros(X.shape)
STEP[1:-1, 1:-1] = L.STEP
for z_ in P.ZONES:
    m = mask(z_[0]) & floor_any
    if len(z_) == 2:
        depth[m] = z_[1]
        ramp[m] = False
        continue
    (lp, ld), (hp, hd) = z_[1], z_[2]
    vx, vz = hp[0] - lp[0], hp[1] - lp[1]
    run = math.hypot(vx, vz)
    t = ((CX - lp[0]) * vx + (CZ - lp[1]) * vz) / (run * run) + STEP * 1.4 / run
    depth[m] = (ld + (hd - ld) * np.clip(t, 0, 1))[m]
    ramp[m] = True
    uphill[m] = (vx, vz)
for rock in P.ROCKS:
    depth[mask(rock)] = np.nan
D = np.where(np.isnan(depth), 0, np.floor(depth + 0.5)).astype(int)
floor = ~np.isnan(depth)

for x, z in cells(floor):
    d = D[x - w.x0, z - w.z0]
    w.column(x, z, YS + d - 1, P.ground(x, z) - 1, B.AIR)
    w.set(x, YS + d - 1, z, *L.cut_floor(x, z))


def feet(x, z):
    return YS + int(D[x - w.x0, z - w.z0])


# stairs on every one-block rise of a flight, facing the neighbour it climbs to that lies most nearly uphill
for x, z in cells(floor & ramp):
    i, k = x - w.x0, z - w.z0
    ux, uz = uphill[i, k]
    best = None
    for sx, sz in DIRS.values():
        j, l = i + sx, k + sz
        if 0 <= j < w.sx and 0 <= l < w.sz and floor[j, l] and D[j, l] == D[i, k] + 1:
            score = sx * ux + sz * uz
            if best is None or score > best[0]:
                best = (score, (sx, sz))
    if best:
        w.set(x, feet(x, z), z, B.STONEBRICK_STAIRS, stair(best[1]))

# ---- the works: each section its storeys, under the crust as deep as its cut and two or three over it ---------------
building_mask = np.zeros(X.shape, bool)
for name, poly, d, sections in P.BUILDINGS:
    m = mask(poly)
    building_mask |= m
    storeys = np.zeros(X.shape, int)
    for (x0, z0, x1, z1), n, _ in sections:
        storeys[(X >= x0) & (X < x1) & (Z >= z0) & (Z < z1) & m] = n + P.storeys_below(d)
    base = YS + d
    for x, z in cells(m):
        i, k = x - w.x0, z - w.z0
        n = storeys[i, k]
        roof = base + n * P.STOREY
        out = [storeys[i + a, k + b] for a, b in DIRS.values()]
        corner = (out[0] < n or out[1] < n) and (out[2] < n or out[3] < n)
        w.column(x, z, base - 1, roof, *(L.BAND if corner else L.WALL))
        w.set(x, base - 1, z, *L.built_floor(x, z))
        for level in range(n):
            floor_y = base + level * P.STOREY
            outside = min(out) == 0 or any(r <= level for r in out)
            if outside:
                if level > 0:
                    w.set(x, floor_y - 1, z, *L.BAND)
                if level > 0 and not corner and (x + z) % 4 == 0:
                    for a, b in DIRS.values():
                        if storeys[i + a, k + b] <= level and w.id(x + a, floor_y + 1, z + b) == B.AIR \
                                and w.id(x + a, floor_y + 2, z + b) == B.AIR:
                            w.column(x, z, floor_y + 1, floor_y + 2, *L.WINDOW)
                continue
            w.column(x, z, floor_y, floor_y + P.STOREY - 2, B.AIR)
            if level > 0:
                w.set(x, floor_y - 1, z, *L.built_floor(x, z))
            if (x * 3 + z) % 7 == 0:
                w.set(x, floor_y + P.STOREY - 1, z, *L.LIGHT)
        if min(out) == 0 or any(r < n for r in out):
            w.set(x, roof, z, *L.BAND)
            w.set(x, roof + 1, z, *L.BAND)                                      # the parapet
        else:
            w.set(x, roof, z, *(L.SKYLIGHT if name == "hall" and z % 5 == 0 else L.BAND))
    for _, n, ((lx, lz), side) in sections:
        n += P.storeys_below(d)
        a, b = DIRS[side]
        for y in range(base, base + (n - 1) * P.STOREY + 1):
            w.set(lx, y, lz, B.LADDER, ladder((a, b)))
        w.column(lx + a, lz + b, base, base + (n - 1) * P.STOREY + 1, *L.WALL)


def hazard_frame(line, bottom, height):
    """A doorway's frame in hazard stripes: a jamb past each end of the opening and a lintel over it."""
    (x0, z0), (x1, z1) = line[0], line[-1]
    dx, dz = (1, 0) if z0 == z1 else (0, 1)
    for jx, jz in ((x0 - dx, z0 - dz), (x1 + dx, z1 + dz)):
        for y in range(bottom, bottom + height + 1):
            w.set(jx, y, jz, *L.HAZARD[y % 2])
    for k, (x, z) in enumerate(line):
        w.set(x, bottom + height, z, *L.HAZARD[(k + 1) % 2])


for name, door in P.DOORS:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if n == name and any(P.pip((c[0] + .5, c[1] + .5), pg) for c in door))
    for x, z in door:
        w.column(x, z, YS + d, YS + d + 2, B.AIR)
    hazard_frame(door, YS + d, 3)
for name, (x0, z0, x1, z1), h in P.CHIMNEYS:
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            top = w.top(x, z)
            w.column(x, z, top + 1, top + h, *L.CHIMNEY)
for (x, z), facing in P.FURNACES:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if P.pip((x + .5, z + .5), pg))
    w.set(x, YS + d, z, B.FURNACE, {"e": 5, "w": 4}[facing])
for x, z in P.COAL:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if P.pip((x + .5, z + .5), pg))
    w.set(x, YS + d, z, B.COAL_BLOCK)
    if (x + z) % 3 == 0:
        w.set(x, YS + d + 1, z, B.COAL_BLOCK)

# ---- panels: a quad on the floor leaning back into the earth, two blocks thick, the wedge before it cleared. A block
# two panels both reach belongs to the one whose foot is nearer, so neighbours meet at a mitre rather than through
# each other; nothing is laid inside a building -------------------------------------------------------------------------
def seg_dist(px, pz, a, b):
    vx, vz = b[0] - a[0], b[1] - a[1]
    t = np.clip(((px - a[0]) * vx + (pz - a[1]) * vz) / (vx * vx + vz * vz), 0, 1)
    return np.hypot(px - a[0] - t * vx, pz - a[1] - t * vz)


claims, cleared = {}, set()
for idx, (a, b, n, (l0, l1), shade) in enumerate(P.panels()):
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    inside = (int(math.floor((a[0] + b[0]) / 2 - n[0] * .6)), int(math.floor((a[1] + b[1]) / 2 - n[1] * .6)))
    base = feet(*inside) if floor[inside[0] - w.x0, inside[1] - w.z0] else YS - 10
    behind = (int(math.floor((a[0] + b[0]) / 2 + n[0] * 4)), int(math.floor((a[1] + b[1]) / 2 + n[1] * 4)))
    rise = P.ground(*behind) + P.LIP - base
    for s in np.arange(0, 1.0001, 0.2 / max(length, 1)):
        bx, bz = a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s
        lean = math.tan(math.radians(l0 + (l1 - l0) * s))
        for t in np.arange(0, 1.0001, 0.2 / rise):
            y = math.floor(base + t * rise)
            back = lean * t * rise
            for o in np.arange(0, back, 0.4):
                cleared.add((math.floor(bx + n[0] * o), y, math.floor(bz + n[1] * o)))
            for k in np.arange(0, 2.0, 0.4):
                c = (math.floor(bx + n[0] * (back + k)), y, math.floor(bz + n[1] * (back + k)))
                near = float(seg_dist(c[0] + .5, c[2] + .5, a, b))
                if c not in claims or near < claims[c][0]:
                    claims[c] = (near, shade)
def on_board(c):
    return 0 <= c[0] < P.W and 0 <= c[2] < P.H


for c in cleared - claims.keys():
    if on_board(c) and c[1] < P.ground(c[0], c[2]) and not floor[c[0] - w.x0, c[2] - w.z0] \
            and not building_mask[c[0] - w.x0, c[2] - w.z0]:
        w.set(*c, B.AIR)
for c, (_, shade) in claims.items():
    if on_board(c) and not building_mask[c[0] - w.x0, c[2] - w.z0]:
        w.set(*c, *L.rust(*c, shade))

# ---- plated seams: plates over a trench to the lava, the missing ones open, the trench's rock scorched -------------
trench = set()


def seam_trench(x, z, top):
    w.column(x, z, P.SEAM_Y + 1, top, B.AIR)
    w.set(x, P.SEAM_Y, z, B.LAVA)
    w.column(x, z, P.SEAM_Y - 2, P.SEAM_Y - 1, *L.SEAM_ROCK)
    trench.add((x, z, top))


strip_mask = np.zeros(X.shape, bool)
for lo, hi, width, rows, missing in P.STRIPS:
    run = math.hypot(hi[0] - lo[0], hi[1] - lo[1])
    ax = ((hi[0] - lo[0]) / run, (hi[1] - lo[1]) / run)
    U = (CX - lo[0]) * ax[0] + (CZ - lo[1]) * ax[1]
    V = -(CX - lo[0]) * ax[1] + (CZ - lo[1]) * ax[0]
    strip = floor & (U >= 0) & (U <= sum(rows)) & (np.abs(V) <= width / 2)
    strip_mask |= strip
    edges = np.cumsum([0] + rows)
    for x, z in cells(strip):
        i, k = x - w.x0, z - w.z0
        row = int(np.searchsorted(edges, U[i, k], side="right") - 1)
        col = 0 if V[i, k] < 0 else 1
        top = feet(x, z) - 1
        if abs(V[i, k]) <= width / 2 - 1.2:
            seam_trench(x, z, top)
        if (min(row, len(rows) - 1), col) not in missing:
            w.set(x, top, z, *L.PLATE)

for boxes, turned in P.SUMP:
    for j, (bx, bz, bw, bd) in enumerate(boxes):
        for x in range(int(bx), int(bx + bw)):
            for z in range(int(bz), int(bz + bd)):
                if not floor[x - w.x0, z - w.z0]:
                    continue
                strip_mask[x - w.x0, z - w.z0] = True
                top = feet(x, z) - 1
                if bz + 1 <= z < bz + bd - 1:
                    seam_trench(x, z, top)
                if j not in P.SUMP_MISSING:
                    w.set(x, top, z, *L.PLATE)
open_cells = {(x, z) for x, z, _ in trench}
for x, z, top in trench:
    for a, b in DIRS.values():
        if (x + a, z + b) not in open_cells:
            for y in range(P.SEAM_Y, min(P.SEAM_Y + 4, top)):
                if w.id(x + a, y, z + b) != B.AIR:
                    w.set(x + a, y, z + b, *L.SEAM_ROCK)

# ---- spoil: heaped from the toe to the crest, the scar behind hollowed ---------------------------------------------
def poly_edge_dist(poly):
    return np.min([seg_dist(CX, CZ, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))], axis=0)


spoil_mask = np.zeros(X.shape, bool)
for sp in P.SPOILS:
    if sp["scar"]:
        for x, z in cells(mask(sp["scar"]) & ~floor):
            top = P.ground(x, z)
            w.column(x, z, top - 4, top - 1, B.AIR)
            w.set(x, top - 5, z, *L.SPOIL[(x + z) % 2])
    toe = mask(sp["toe"]) & floor
    spoil_mask |= toe
    to_toe = poly_edge_dist(sp["toe"])
    to_crest = np.min([seg_dist(CX, CZ, sp["crest"][i], sp["crest"][i + 1]) for i in range(len(sp["crest"]) - 1)],
                      axis=0)
    rise = sp["peak"] * (to_toe / (to_toe + to_crest + 1e-9)) ** 0.8
    for x, z in cells(toe):
        h = int(round(rise[x - w.x0, z - w.z0]))
        for y in range(feet(x, z), feet(x, z) + h):
            w.set(x, y, z, *L.SPOIL[(x * 3 + z + y) % 2])

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
        w.set(x, y, z, *L.rust(x, y, z, 0))

# ---- the drift tunnels: four wide, four high, timbered every six blocks, the shaft's ladder up to the crust -----------
tunnel_mouths = []


def bore(path, d0, d1):
    lengths = [math.hypot(path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]) for i in range(len(path) - 1)]
    total = sum(lengths)
    done = 0.0
    frames = []
    for i, seg in enumerate(lengths):
        a, b = path[i], path[i + 1]
        ux, uz = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg
        for s in np.arange(0, seg, 0.4):
            d = round(d0 + (d1 - d0) * (done + s) / total)
            px, pz = a[0] + ux * s, a[1] + uz * s
            for o in np.arange(-2, 2.01, 0.4):
                x, z = math.floor(px - uz * o), math.floor(pz + ux * o)
                if floor[x - w.x0, z - w.z0]:
                    continue
                w.column(x, z, YS + d, YS + d + 3, B.AIR)
                w.set(x, YS + d - 1, z, *L.cut_floor(x, z))
            if int(done + s) % 6 == 3 and (not frames or done + s - frames[-1] > 5):
                frames.append(done + s)
                for o in (-2.2, 2.2):
                    x, z = math.floor(px - uz * o), math.floor(pz + ux * o)
                    if not floor[x - w.x0, z - w.z0]:
                        w.column(x, z, YS + d, YS + d + 2, *L.TIMBER_POST)
                for o in np.arange(-2.2, 2.21, 0.4):
                    x, z = math.floor(px - uz * o), math.floor(pz + ux * o)
                    if not floor[x - w.x0, z - w.z0]:
                        w.set(x, YS + d + 3, z, *L.TIMBER_BEAM)
                x, z = math.floor(px), math.floor(pz)
                w.set(x, YS + d + 4, z, *L.LIGHT)
        done += seg


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
    w.column(sx + wall[0], sz, low - 1, top - 1, *L.rock(sx + wall[0], low, sz))
    for y in range(low, top):
        w.set(sx, y, sz, B.LADDER, ladder(wall))
# the tunnel mouths, kept clear of the floor's wear
for cut in P.CUTS[:2]:
    for i, (p, tag) in enumerate(cut):
        if tag == "T":
            q = cut[(i + 1) % len(cut)][0]
            tunnel_mouths += [(math.floor(p[0] + (q[0] - p[0]) * s), math.floor(p[1] + (q[1] - p[1]) * s))
                              for s in np.arange(0, 1.01, 0.1)]

# ---- ladders up the cut walls: a rock backing up to the crust, a gap in the panels' lip over it ----------------------
for (x, z), side in P.LADDERS:
    dx, dz = DIRS[side]
    bottom = feet(x, z)
    top = P.ground(x + dx, z + dz)
    w.column(x, z, bottom, top + 3, B.AIR)
    for y in range(bottom, top):
        w.set(x + dx, y, z + dz, *L.rock(x + dx, y, z + dz))
        w.set(x, y, z, B.LADDER, ladder((dx, dz)))
    for k in range(1, 7):
        for o in (-1, 0, 1):
            cx, cz = x + dx * k + (o if dx == 0 else 0), z + dz * k + (o if dz == 0 else 0)
            here = P.ground(cx, cz)
            w.column(cx, cz, here, here + 4, B.AIR)
            if k > 1 and w.id(cx, here - 1, cz) == B.AIR:
                w.set(cx, here - 1, cz, *L.crust(cx, cz))

# ---- the floor worn: half-block lumps of cobblestone, never more than half a block above a neighbour --------------
keep = ramp | grow(strip_mask, 2) | grow(building_mask, 2) | spoil_mask | grow(point_mask(
    [c for c, _ in P.LADDERS] + [c for c, _ in P.STALLS] + P.LAMPS + tunnel_mouths
    + [c for _, c, _ in P.FLAG_POSTS] + [(P.W - 1 - x, P.H - 1 - z) for _, (x, z), _ in P.FLAG_POSTS]), 2)
level = np.zeros(X.shape, int)
wear = np.zeros(X.shape)
wear[1:-1, 1:-1] = L.WEAR
same = floor.copy()
for a, b in DIRS.values():
    same &= np.roll(floor, (-a, -b), (0, 1)) & (np.roll(D, (-a, -b), (0, 1)) == D)
ok = floor & ~keep & same
level[ok & (wear > 0.66)] = 1
level[ok & (wear > 0.8)] = 2
for _ in range(3):
    low = np.ones(X.shape, int) * 2
    for a, b in DIRS.values():
        low = np.minimum(low, np.roll(level, (-a, -b), (0, 1)))
    level = np.minimum(level, low + 1)
for x, z in cells(level > 0):
    y = feet(x, z)
    if w.id(x, y, z) != B.AIR:
        continue
    w.set(x, y, z, *(L.LUMP if level[x - w.x0, z - w.z0] == 2 else L.LUMP_SLAB))

# ---- the market and the lamps ----------------------------------------------------------------------------------------
AWNINGS = [12, 8, 7]                       # brown, light grey and grey wool, white stripes
for k, ((x, z), facing) in enumerate(P.STALLS):
    props.stall(w, x, feet(x, z) - 1, z, facing, awning=AWNINGS[k % 3], stripe=0)
for x, z in P.LAMPS:
    props.lamp(w, x, feet(x, z) - 1, z, height=3, post=(B.NETHER_FENCE, 0), cap=(B.SLAB, 3))

# ---- the objectives: the flags' banners at their first posts, the monuments --------------------------------------------
from mapxml import OBJECTIVES  # noqa: E402

OBJECTIVES.stamp(w)
for team, (x, z), d in ((0, P.FLAG_POSTS[0][1], P.FLAG_POSTS[0][2]),
                        (1, (P.W - 1 - P.FLAG_POSTS[0][1][0], P.H - 1 - P.FLAG_POSTS[0][1][1]), P.FLAG_POSTS[0][2])):
    w.banner(x, YS + d, z, 15 - DYES["green" if team == 0 else "purple"], rot=12 if team == 0 else 4)

w.save(sys.argv[1], "Seamworks", (P.SPAWN_AT[0], YS - 8, P.SPAWN_AT[1]))
print("generated", int(floor.sum()), "floor columns,", len(claims), "panel blocks,", int((level > 0).sum()), "worn")
