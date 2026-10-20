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

w = World(0, 0, P.W, P.H, sy=YS + 40)
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
    t = ((CX - lp[0]) * vx + (CZ - lp[1]) * vz) / (run * run) + L.STEP * 1.4 / run
    depth[m] = (ld + (hd - ld) * np.clip(t, 0, 1))[m]
    ramp[m] = True
    uphill[m] = (vx, vz)
for rock in P.ROCKS:
    depth[mask(rock)] = np.nan
D = np.where(np.isnan(depth), 0, np.floor(depth + 0.5)).astype(int)
floor = ~np.isnan(depth)


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
for name, line in P.DOORS:
    d = next(dd for n, pg, dd, _ in P.BUILDINGS if n == name and any(A.pip((c[0] + .5, c[1] + .5), pg) for c in line))
    A.door(w, line, YS + d, LOOK)
for name, box, h in P.CHIMNEYS:
    A.chimney(w, box, h, LOOK, drift=(1, 0) if box[0] < P.W / 2 else (-1, 0))     # one wind, turned with the board
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
        A.crust_hollow(w, [c for c in A.poly_cells(sp["scar"]) if on_board(*c) and not is_floor(*c)], ground, LOOK)
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
          | around(set(P.LAMPS) | building_cells | heaped, 2) | around(plated, 1)
          | around({(x, z) for x, _, z in claims}, 2) | {c for c in cells(ramp)}
          | {c for _, line in P.DOORS for c in around(set(line), 3)})
jutted, hollowed = A.rock_faces(w, list(cells(floor)), feet, lambda x, z: not on_board(x, z) or (x, z) in spared,
                                lambda x, z: L._at(L.ROCK_B, x * 2 + 7, z), lambda x, z: L._at(L.WEAR, x + 11, z * 2),
                                LOOK)

# ---- the floor worn, clear of everything a player has to find or stand at --------------------------------------------------
near = around({c for c, _ in P.LADDERS} | {c for c, _ in P.STALLS} | set(P.LAMPS) | mouths | plated | building_cells
              | flag_cells, 2)
eligible = [(x, z) for x, z in cells(floor & ~ramp) if (x, z) not in near and (x, z) not in heaped
            and all(is_floor(x + a, z + b) and feet(x + a, z + b) == feet(x, z) for a, b in DIRS.values())]
worn = A.wear(w, eligible, feet, lambda x, z: 2 if L._at(L.WEAR, x, z) > 0.8 else 1 if L._at(L.WEAR, x, z) > 0.66
              else 0, LOOK)

# ---- the team's rim: the floor's edge against every wall, red on red's half and blue on blue's -----------------------
floor_y = {c: feet(*c) for c in cells(floor)}
floor_y.update(hollowed)
rimmed = A.rim(w, floor_y, lambda x, z: 0 if x < P.W / 2 else 1, LOOK, skip=plated)

# ---- the market and the lamps ----------------------------------------------------------------------------------------
AWNINGS = [12, 8, 7]                       # brown, light grey and grey wool, white stripes
for k, ((x, z), facing) in enumerate(P.STALLS):
    props.stall(w, x, feet(x, z) - 1, z, facing, awning=AWNINGS[k % 3], stripe=0)
for x, z in P.LAMPS:
    props.lamp(w, x, feet(x, z) - 1, z, height=3, post=(B.NETHER_FENCE, 0), cap=(B.SLAB, 3))

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
      "jutting over the floor,", len(hollowed), "hollowed at a face's foot,", rimmed, "rim blocks")
print("panels left out where two walls met, by the middle of their foot:")
for i in dropped:
    a, b = quads[i][0], quads[i][1]
    print(f"  ({(a[0] + b[0]) / 2:.0f}, {(a[1] + b[1]) / 2:.0f}), {math.hypot(b[0] - a[0], b[1] - a[1]):.0f} long")
