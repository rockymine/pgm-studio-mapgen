"""Build Seamworks from the plan through the asset functions (`assets.py`) in the board's look (`look.py`): the ground in
rock under its ash, the cuts carved to their depths with their floors worn and their flights stepped along wandering
edges, the steel panels, the plated seams, the spoil, the works with their storeys over the crust, the drift tunnels,
the market and the objectives.

    python3 gen.py <build-dir>
"""
import math
import sys

import numpy as np

import plan as P  # noqa: I001  (plan puts the library on the path)
import assets as A
import look as L
from pgmvox import B, World
from pgmvox.built import props
from pgmvox.core.orient import ladder
from pgmvox.play.objectives import DYES

YS = P.YS
LOOK = L.LOOK
DIRS = A.DIRS

w = World(-P.MARGIN, -P.MARGIN, P.W + 2 * P.MARGIN, P.H + 2 * P.MARGIN, sy=YS + 40)
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


def on_board(x, z):
    return 0 <= x < P.W and 0 <= z < P.H


# ---- the ground: bedrock under stone, the orange overburden and its crust over it, the rock left standing bare -------
w.ids[:, 0, :] = B.BEDROCK
for x, z in cells(np.ones(X.shape, bool)):
    w.column(x, z, 1, P.ground(x, z) - 1, B.STONE)
L.paint_rock(w)
standing = np.zeros(X.shape, bool)
for rock in P.STANDING:
    standing |= mask(rock)
for x, z in cells(~standing):
    A.lay_crust(w, x, z, P.ground, LOOK)

# ---- floor depths: each cut's own, then its zones; a flight's step edges wander with the noise ----------------------
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
    run = math.hypot(vx, vz)
    t = ((CX - lp[0]) * vx + (CZ - lp[1]) * vz) / (run * run) + L.STEP[np.clip(X, 0, P.W - 1), np.clip(Z, 0, P.H - 1)] * 1.4 / run
    depth[m] = (ld + (hd - ld) * np.clip(t, 0, 1))[m]
    ramp[m] = True
    uphill[m] = (vx, vz)
for rock in P.ROCKS:
    depth[mask(rock)] = np.nan
D = np.where(np.isnan(depth), 0, np.floor(depth + 0.5)).astype(int)
floor = ~np.isnan(depth)

# ---- the outline: the land pushed out past the rectangle and pulled in from it, kept clear of what was dug and built ---
from scipy.ndimage import binary_dilation  # noqa: E402
from pgmvox.geom.noise import fbm  # noqa: E402

edge = np.minimum.reduce([CX, P.W - CX, CZ, P.H - CZ])
wobble = fbm(X.shape, 26, 3, seed=81)
wobble = (wobble + wobble[::-1, ::-1]) / 2
wobble = (wobble - wobble.min()) / (wobble.max() - wobble.min()) * 2 - 1
built = floor.copy()
for _, poly, _, _ in P.BUILDINGS:
    built |= mask(poly)
land = (edge + wobble * P.OUTLINE > 0) | binary_dilation(built, iterations=P.OUTLINE_KEEP)
w.ids.transpose(0, 2, 1)[~land] = B.AIR
w.dat.transpose(0, 2, 1)[~land] = 0


def is_floor(x, z):
    return on_board(x, z) and bool(floor[x - w.x0, z - w.z0])


def feet(x, z):
    return YS + int(D[x - w.x0, z - w.z0])


def ground(x, z):
    return P.ground(x, z)


for x, z in cells(floor):
    w.column(x, z, feet(x, z) - 1, ground(x, z) - 1, B.AIR)
    w.set(x, feet(x, z) - 1, z, *LOOK.cut_floor(x, z))
A.stairs(w, list(cells(floor & ramp)), feet, is_floor, lambda x, z: tuple(uphill[x - w.x0, z - w.z0]), LOOK)

# ---- the works --------------------------------------------------------------------------------------------------------
building_cells = set()
for name, poly, d, sections in P.BUILDINGS:
    below = P.storeys_below(d)
    secs = [({(x, z) for x in range(x0, x1) for z in range(z0, z1)}, n + below, lad)
            for (x0, z0, x1, z1), n, lad in sections]
    building_cells |= A.building(w, poly, YS + d, secs, LOOK, skylights=name == "hall")
# a building's base carried down to the floor wherever the floor beside its wall lies lower
for name, poly, d, sections in P.BUILDINGS:
    cells_ = A.poly_cells(poly)
    for x, z in cells_:
        lows = [feet(x + a, z + b) for a, b in DIRS.values() if (x + a, z + b) not in cells_ and is_floor(x + a, z + b)]
        if lows and min(lows) < YS + d:
            for y in range(min(lows) - 1, YS + d - 1):
                w.set(x, y, z, *LOOK.building(x, y, z, "base"))
for name, line in P.DOORS:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if n == name and any(A.pip((c[0] + .5, c[1] + .5), pg) for c in line))
    A.door(w, line, YS + d, LOOK)
for name, box, h in P.CHIMNEYS:
    A.chimney(w, box, h, LOOK, drift=(1, 0) if box[0] < P.W / 2 else (-1, 0))     # one wind, turned with the board
# what stands on the roofs: placed on red's works and turned onto blue's, so the two halves match
half = len(P.BUILDINGS) // 2
equipment = 0
for name, poly, d, sections in P.BUILDINGS[:half]:
    roof = A.flat_roof(w, A.poly_cells(poly))
    lit = A.flat_roof(w, A.poly_cells(poly), skylights=True)
    for kit in (A.roof_kit(roof, around=lit),
                A.roof_kit(roof, mirror=lambda c: (P.W - 1 - c[0], P.H - 1 - c[1]), around=lit)):
        A.lay_roof_kit(w, kit, LOOK)
        equipment += len(kit)
for (x, z), facing in P.FURNACES:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if A.pip((x + .5, z + .5), pg))
    w.set(x, YS + d, z, B.FURNACE, {"e": 5, "w": 4}[facing])
for x, z in P.COAL:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if A.pip((x + .5, z + .5), pg))
    w.set(x, YS + d, z, B.COAL_BLOCK)
    if (x + z) % 3 == 0:
        w.set(x, YS + d + 1, z, B.COAL_BLOCK)

# ---- the panels -------------------------------------------------------------------------------------------------------
def base_of(a, b, n):
    inside = (math.floor((a[0] + b[0]) / 2 - n[0] * .6), math.floor((a[1] + b[1]) / 2 - n[1] * .6))
    return feet(*inside) if is_floor(*inside) else YS - 10


def rise_of(a, b, n, base):
    behind = (math.floor((a[0] + b[0]) / 2 + n[0] * 4), math.floor((a[1] + b[1]) / 2 + n[1] * 4))
    return ground(*behind) + P.LIP - base


quads = P.panels()
claims, dropped = A.panels(w, quads, base_of, rise_of, is_floor,
                  lambda x, z: not on_board(x, z) or (x, z) in building_cells, ground, LOOK)

# ---- the plated seams and the sump ----------------------------------------------------------------------------------------
plated = set()
for lo, hi, width, rows, missing in P.STRIPS:
    plated |= A.plated_strip(w, lo, hi, width, rows, missing, feet, is_floor, P.SEAM_Y, LOOK)
for boxes, turned in P.SUMP:
    xs = [bx for bx, _, bw, _ in boxes] + [bx + bw for bx, _, bw, _ in boxes]
    zc = boxes[0][1] + boxes[0][3] / 2
    lo, hi = ((min(xs), zc), (max(xs), zc)) if not turned else ((max(xs), zc), (min(xs), zc))
    rows = [bw for _, _, bw, _ in boxes]
    gone = {(j, c) for j in P.SUMP_MISSING for c in (0, 1)}
    plated |= A.plated_strip(w, lo, hi, boxes[0][3], rows, gone, feet, is_floor, P.SEAM_Y, LOOK)

# ---- spoil, and the panel that fell -------------------------------------------------------------------------------------
heaped = set()
for sp in P.SPOILS:
    if sp["scar"]:
        A.crust_hollow(w, [c for c in A.poly_cells(sp["scar"]) if on_board(*c) and not is_floor(*c)
                           and not P.on_apron(*c) and c not in building_cells], ground, LOOK)
    heaped |= A.spoil(w, sp["toe"], sp["crest"], sp["peak"], feet, is_floor, LOOK)
for a, b, reach, turn, h0, h1, is_turned in P.FALLEN:
    cut = [p for p, _ in (P.CUTS[1] if is_turned else P.CUTS[0])]
    n = P.outward(a, b, cut)
    n = (-n[0], -n[1])
    r = math.radians(turn)
    n = (math.cos(r) * n[0] - math.sin(r) * n[1], math.sin(r) * n[0] + math.cos(r) * n[1])
    floor_y = feet(math.floor((a[0] + b[0]) / 2 + n[0] * 2), math.floor((a[1] + b[1]) / 2 + n[1] * 2))
    A.fallen_panel(w, a, b, n, reach, h0, h1, floor_y, is_floor, LOOK)

# ---- the drift tunnels, the unfinished branch and its shaft --------------------------------------------------------------
branch_depth = -8 - 2 * 10.2 / 46.5          # the main tunnel's depth where the branch leaves it
for turned in (False, True):
    T = (lambda p: P.R(p)) if turned else (lambda p: p)
    A.bore(w, [T(p) for p in P.TUNNEL], YS - 8, YS - 10, is_floor, LOOK)
    A.bore(w, [T(p) for p in P.BRANCH], YS + round(branch_depth), YS + round(branch_depth), is_floor, LOOK)
    sx, sz = (P.W - 1 - P.SHAFT[0], P.H - 1 - P.SHAFT[1]) if turned else P.SHAFT
    wall = (1, 0) if turned else (-1, 0)
    low = YS + round(branch_depth)
    top = ground(sx, sz)
    w.column(sx, sz, low, top - 1, B.AIR)
    for y in range(low - 1, top):
        w.set(sx + wall[0], y, sz, *LOOK.rock(sx + wall[0], y, sz))
    for y in range(low, top):
        w.set(sx, y, sz, B.LADDER, ladder(wall))
mouths = set()
for cut in P.CUTS[:2]:
    for i, (p, tag) in enumerate(cut):
        if tag == "T":
            q = cut[(i + 1) % len(cut)][0]
            mouths |= {(math.floor(p[0] + (q[0] - p[0]) * s), math.floor(p[1] + (q[1] - p[1]) * s))
                       for s in np.arange(0, 1.01, 0.1)}

# ---- ladders up the cut walls --------------------------------------------------------------------------------------------
for (x, z), side in P.LADDERS:
    A.ladder_bay(w, x, z, side, feet(x, z), ground, LOOK)

# ---- the bare rock faces: overhanging, undercut at the foot, nothing to climb --------------------------------------------
def around(points, r):
    out = set()
    for x, z in points:
        out |= {(x + a, z + b) for a in range(-r, r + 1) for b in range(-r, r + 1)}
    return out


flag_cells = {c for _, c, _ in P.FLAG_POSTS} | {(P.W - 1 - x, P.H - 1 - z) for _, (x, z), _ in P.FLAG_POSTS}
spared = (around({c for c, _ in P.LADDERS} | mouths | flag_cells | {c for c, _ in P.STALLS}, 3)
          | around(building_cells | heaped, 2) | around(plated, 1)
          | around({(x, z) for x, _, z in claims}, 2) | {c for c in cells(ramp)}
          | {c for _, line in P.DOORS for c in around(set(line), 3)})
jutted, hollowed = A.rock_faces(w, list(cells(floor)), feet, lambda x, z: not on_board(x, z) or (x, z) in spared,
                                lambda x, z: L._at(L.ROCK_B, x * 2 + 7, z), lambda x, z: L._at(L.WEAR, x + 11, z * 2),
                                LOOK)

# ---- the floor worn, clear of everything a player has to find or stand at --------------------------------------------------
near = around({c for c, _ in P.LADDERS} | {c for c, _ in P.STALLS} | mouths | plated | building_cells
              | flag_cells, 2)
eligible = [(x, z) for x, z in cells(floor & ~ramp) if (x, z) not in near and (x, z) not in heaped
            and all(is_floor(x + a, z + b) and feet(x + a, z + b) == feet(x, z) for a, b in DIRS.values())]
worn = A.wear(w, eligible, feet, lambda x, z: 2 if L._at(L.WEAR, x, z) > 0.8 else 1 if L._at(L.WEAR, x, z) > 0.66
              else 0, LOOK)

# ---- the team's rim: the floor's edge against every wall, red on red's half and blue on blue's -----------------------
floor_y = {c: feet(*c) for c in cells(floor)}
floor_y.update(hollowed)
rimmed = A.rim(w, floor_y, lambda x, z: 0 if x < P.W / 2 else 1, LOOK, skip=plated)

# ---- huts, the spawner's dais, and the chevrons -------------------------------------------------------------------------
hut_cells = set()
for (length, depth_, facing, (hx, hz)), team in P.HUTS:
    hut_cells |= A.hut(w, hx, hz, length, depth_, facing, feet(hx, hz), LOOK)
dx, dz, size = P.DAIS
A.dais(w, dx, dz, size, feet(dx + size // 2, dz + size // 2), LOOK)
dais_cells = {(x, z) for x in range(dx, dx + size) for z in range(dz, dz + size)}
ramps = set(cells(ramp))


def takes_chevron(x, z):
    return ((x, z) not in plated and (x, z) not in ramps and (x, z) not in hut_cells and (x, z) not in dais_cells
            and (x, z) not in building_cells and w.id(x, floor_y[(x, z)], z) == B.AIR)


chevroned = sum(A.chevrons(w, tip, way, floor_y, takes_chevron, LOOK, team, count=2, size=3, gap=4)
                for tip, way, team in P.CHEVRONS)

# ---- the market ----------------------------------------------------------------------------------------
AWNINGS = [12, 8, 7]                       # brown, light grey and grey wool, white stripes
for k, ((x, z), facing) in enumerate(P.STALLS):
    props.stall(w, x, feet(x, z) - 1, z, facing, awning=AWNINGS[k % 3], stripe=0)

# ---- nothing that falls stands over air ----------------------------------------------------------------------------------
for falls, holds in (((B.GRAVEL, 0), (B.STONE, 5)), ((B.SAND, 1), (B.RED_SANDSTONE, 0))):
    loose = (w.ids[:, 1:, :] == falls[0]) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose] = holds[0]
    w.dat[:, 1:, :][loose] = holds[1]

# ---- the objectives: the flags' banners at their first posts, the monuments --------------------------------------------
from mapxml import OBJECTIVES  # noqa: E402

OBJECTIVES.stamp(w)
for team, (x, z), d in ((0, P.FLAG_POSTS[0][1], P.FLAG_POSTS[0][2]),
                        (1, (P.W - 1 - P.FLAG_POSTS[0][1][0], P.H - 1 - P.FLAG_POSTS[0][1][1]), P.FLAG_POSTS[0][2])):
    w.banner(x, YS + d, z, 15 - DYES["red" if team == 0 else "blue"], rot=12 if team == 0 else 4)

w.save(sys.argv[1], "Seamworks", (P.SPAWN_AT[0], YS - 8, P.SPAWN_AT[1]))
print("generated", int(floor.sum()), "floor columns,", len(claims), "panel blocks,", worn, "worn,", len(jutted),
      "jutting over the floor,", len(hollowed), "hollowed at a face's foot,", rimmed, "rim blocks,", chevroned, "chevron blocks,", int(land.sum()), "columns of land,", equipment, "pieces on the roofs")
print("panels left out where two walls met, by the middle of their foot:")
for i in dropped:
    a, b = quads[i][0], quads[i][1]
    print(f"  ({(a[0] + b[0]) / 2:.0f}, {(a[1] + b[1]) / 2:.0f}), {math.hypot(b[0] - a[0], b[1] - a[1]):.0f} long")
