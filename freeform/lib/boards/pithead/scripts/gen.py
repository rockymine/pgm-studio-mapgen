"""Build Pithead from the plan through Seamworks' asset functions in Seamworks' look: each half a body of ground on the
bedrock with its cuts dug down through the orange to their levels and stepped between them, panels and bare rock for
their walls, a ladder up each wool's ledge, plated strips over the seam in the hub under a headframe, the works over
the spawn and the wool rooms, the defence walls, the two islands of the middle, and the objectives.

    python3 gen.py <build-dir>
"""
import math
import sys

import numpy as np
from scipy.ndimage import distance_transform_edt

import plan as P  # noqa: I001  (plan puts the library on the path, and is the `plan` Seamworks' look reads)
from pgmvox import B, World
from pgmvox.built import props
from pgmvox.geom.noise import fbm
from pgmvox.play.objectives import DYES

A = P.seamworks("assets", "seamworks_assets")
L = P.seamworks("look", "seamworks_look")
YS = P.YS
LOOK = L.LOOK
DIRS = A.DIRS

w = World(0, 0, P.W, P.H, sy=YS + 36)
X, Z = w.grid()
CX, CZ = X + 0.5, Z + 0.5


def mask(poly):
    """The columns whose centres lie inside a polygon."""
    xs = np.array([p[0] for p in poly]); zs = np.array([p[1] for p in poly])
    inside = np.zeros(X.shape, bool)
    j = len(poly) - 1
    for i in range(len(poly)):
        crosses = (zs[i] > CZ) != (zs[j] > CZ)
        inside ^= crosses & (CX < (xs[j] - xs[i]) * (CZ - zs[i]) / (zs[j] - zs[i] + 1e-12) + xs[i])
        j = i
    return inside


def turned_mask(m):
    return m | m[::-1, ::-1]


def both(poly):
    """A red polygon's columns and its half turn's."""
    return turned_mask(mask(poly))


def cells(m):
    for i, k in zip(*np.nonzero(m)):
        yield int(i + w.x0), int(k + w.z0)


def turned(c):
    return P.RC(c)


def turn_side(side):
    return {"w": "e", "e": "w", "n": "s", "s": "n"}[side]


def around(points, r):
    out = set()
    for x, z in points:
        out |= {(x + a, z + b) for a in range(-r, r + 1) for b in range(-r, r + 1)}
    return out


def smooth(seed, cell, octaves=3):
    f = fbm(X.shape, cell, octaves, seed=seed)
    f = (f + f[::-1, ::-1]) / 2
    return (f - f.min()) / (f.max() - f.min())


# ---- the land: each half's ground runs a few blocks past its cuts, and stops flush with the frontline's open edge;
# the middle's islands are their own -----------------------------------------------------------------------------------
red_cuts = np.zeros(X.shape, bool)
for poly, _ in P.CUTS.values():
    red_cuts |= mask(poly)
margin = P.MARGIN[0] + smooth(96, 9) * (P.MARGIN[1] - P.MARGIN[0])
red_land = ((distance_transform_edt(~red_cuts) <= margin) & (Z >= P.FRONT_EDGE)) | red_cuts
islands = both(P.ISLAND[0])
land = turned_mask(red_land) | islands
cut = turned_mask(red_cuts) | islands

# ---- the floors' levels: each cut's own, then the flights between them -----------------------------------------------
level = np.full(X.shape, np.nan)
for poly, v in list(P.CUTS.values()) + [P.ISLAND]:
    level[both(poly)] = v
flight = np.zeros(X.shape, bool)
uphill = np.zeros(X.shape + (2,))
for poly, (lp, lv), (hp, hv) in P.FLIGHTS:
    for pg, lo, hi in ((poly, lp, hp), ([P.R(p) for p in poly], P.R(lp), P.R(hp))):
        m = mask(pg) & cut
        vx, vz = hi[0] - lo[0], hi[1] - lo[1]
        run = math.hypot(vx, vz)
        t = ((CX - lo[0]) * vx + (CZ - lo[1]) * vz) / (run * run) + L.STEP[X % P.W, Z % P.H] * 1.4 / run
        level[m] = (lv + (hv - lv) * np.clip(t, 0, 1))[m]
        flight |= m
        uphill[m] = (vx, vz)
D = np.where(np.isnan(level), 0, np.floor(level + 0.5)).astype(int)
floor = cut.copy()


def on_board(x, z):
    return 0 <= x < P.W and 0 <= z < P.H


def is_floor(x, z):
    return on_board(x, z) and bool(floor[x, z])


def feet(x, z):
    return YS + int(D[x, z])


def ground(x, z):
    """Where a column's top is walked or would be: a floor's level, the surface's, or nothing off the land."""
    if not on_board(x, z) or not land[x, z]:
        return 0
    return feet(x, z) if cut[x, z] else P.GROUND


# ---- the ground: banded stone on the bedrock, the orange and its crust over it where nothing was dug; level round the
# works and the ledges -------------------------------------------------------------------------------------------------
works_cells = set()
for poly in [P.HALL[0]] + [wk[0] for wk in P.WORKS]:
    works_cells |= set(A.poly_cells(poly)) | set(A.poly_cells([P.R(p) for p in poly]))
ledge_cells = {c for (c, _, _) in P.LEDGES} | {turned(c) for (c, _, _) in P.LEDGES}
P.set_apron(around(works_cells | ledge_cells, 3))
for x, z in cells(land):
    w.set(x, 0, z, B.BEDROCK)
    w.column(x, z, 1, ground(x, z) - 1, B.STONE)
L.paint_rock(w)
for x, z in cells(floor):
    w.set(x, feet(x, z) - 1, z, *LOOK.cut_floor(x, z))
for x, z in cells(land & ~cut):
    A.lay_crust(w, x, z, ground, LOOK)
A.stairs(w, list(cells(floor & flight)), feet, is_floor, lambda x, z: tuple(uphill[x, z]), LOOK)

# ---- the rock left standing: a boss on each frontline, an outcrop on each island -------------------------------------
crag = smooth(98, 3, 2)
outcrop = np.zeros(X.shape, bool)
for poly, rise in ((P.ISLAND_ROCK, P.ISLAND_ROCK_RISE), (P.FRONT_ROCK, P.FRONT_ROCK_RISE)):
    m = both(poly) & land
    edge_in = distance_transform_edt(m)
    for x, z in cells(m):
        height = min(rise, 1 + int(edge_in[x, z] * 1.6 + crag[x, z] * 2))
        w.column(x, z, feet(x, z) - 1, feet(x, z) + height - 1, B.STONE)
    outcrop |= m
L.paint_rock(w)
floor &= ~outcrop

# ---- the hub's plated strips over the seam, hazard stripes round them, and the headframe over the middle one ---------
plated = set()
strip_cells = []
for lo, hi, width, rows, missing in P.STRIPS:
    for a, b in ((lo, hi), (P.R(lo), P.R(hi))):
        covered = A.plated_strip(w, a, b, width, rows, missing, feet, is_floor, P.SEAM_Y, LOOK)
        plated |= covered
        strip_cells.append(covered)
striped = 0
for covered in strip_cells:
    for x, z in around(covered, 1) - covered:
        if is_floor(x, z) and not flight[x, z]:
            black = ((x + z) // 2) % 2
            w.set(x, feet(x, z) - 1, z, B.STAINED_CLAY, 15 if black else 4)
            striped += 1


def headframe(box, base):
    """A tower of four legs standing round a plated strip and leaning in as they rise, ringed in iron bars twice, a
    deck on their heads and two sheave wheels upright on the deck, their axles across the board."""
    x0, z0, x1, z1 = box
    top = base + P.HEADFRAME
    taper = P.HEADFRAME_TAPER
    legs = set()

    def inset(y):
        return int(round((y - base) / P.HEADFRAME * taper))
    for y in range(base, top + 1):
        k = inset(y)
        for x, z in ((x0 + k, z0 + k), (x1 - k, z0 + k), (x0 + k, z1 - k), (x1 - k, z1 - k)):
            w.set(x, y, z, *((B.PRISMARINE, 2) if (y - base) % 6 == 5 else (B.STONE, 6)))
            if y == base:
                legs.add((x, z))
            if y > base and inset(y - 1) != k:              # the leg steps in: join the course below
                w.set(x, y - 1, z, B.STONE, 6)
    for y in (base + 6, base + 12):
        k = inset(y)
        for x in range(x0 + k + 1, x1 - k):
            for z in (z0 + k, z1 - k):
                w.set(x, y, z, B.IRON_BARS)
        for z in range(z0 + k + 1, z1 - k):
            for x in (x0 + k, x1 - k):
                w.set(x, y, z, B.IRON_BARS)
    k = inset(top)
    for x in range(x0 + k, x1 - k + 1):
        for z in range(z0 + k, z1 - k + 1):
            if x in (x0 + k, x1 - k) or z in (z0 + k, z1 - k):
                corner = x in (x0 + k, x1 - k) and z in (z0 + k, z1 - k)
                w.set(x, top, z, *((B.STONE, 6) if corner else (B.PRISMARINE, 2)))
                w.set(x, top + 1, z, B.SLAB, 6)
    cx = (x0 + x1 + 1) / 2
    r = 3.2
    for wz in (math.floor((z0 + z1) / 2) - 1, math.floor((z0 + z1) / 2) + 1):
        for x in range(math.floor(cx - r - 1), math.ceil(cx + r + 1)):
            for y in range(top + 1, top + 10):
                d = math.hypot(x + .5 - cx, y + .5 - (top + 1.5 + r))
                if abs(d - r) < 0.6:
                    w.set(x, y, wz, B.STONE, 6)
                elif d < r - 0.5 and (abs(x + .5 - cx) < 0.6 or abs(y + .5 - (top + 1.5 + r)) < 0.6):
                    w.set(x, y, wz, B.IRON_BARS)
    for z in range(z0 + k + 1, z1 - k):
        w.set(math.floor(cx), top + 1, z, B.PRISMARINE, 2)        # the axle beam across the deck
    return legs


def box_of(covered):
    xs = [x for x, _ in covered]; zs = [z for _, z in covered]
    return (min(xs) - 1, min(zs) - 1, max(xs) + 1, max(zs) + 1)


frame_cells = headframe(box_of(strip_cells[0]), YS) | headframe(box_of(strip_cells[1]), YS)

# ---- the panels on the cut walls and against each ledge, red's laid out and turned onto blue's -----------------------
quads = []


def facing_ground(a, b):
    """The unit normal of a wall's foot a -> b pointing to its higher side: into the ground, or up onto a ledge."""
    dx, dz = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dz)
    n = (dz / length, -dx / length)
    mx, mz = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    ahead = ground(math.floor(mx + n[0] * 1.5), math.floor(mz + n[1] * 1.5))
    back = ground(math.floor(mx - n[0] * 1.5), math.floor(mz - n[1] * 1.5))
    return n if ahead > back else (-n[0], -n[1])


def wall_of(a, b, rng, shade0=0):
    n = facing_ground(a, b)
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    ux, uz = (b[0] - a[0]) / length, (b[1] - a[1]) / length
    for j, (s0, s1) in enumerate(P.SP.panel_runs(a, b, rng)):
        lean = 11 + rng.uniform(-1.5, 1.5)
        quads.append(((a[0] + ux * s0, a[1] + uz * s0), (a[0] + ux * s1, a[1] + uz * s1), n,
                      (lean, lean + rng.uniform(-1.5, 1.5)), (shade0 + j) % 2))


import random  # noqa: E402

for k, (a, b) in enumerate(P.PANELS + [panel for _, _, panel in P.LEDGES]):
    wall_of(a, b, random.Random(41 + k), k)
quads += [(P.R(a), P.R(b), (-n[0], -n[1]), lean, shade) for a, b, n, lean, shade in quads]


def base_of(a, b, n):
    return feet(math.floor((a[0] + b[0]) / 2 - n[0] * .6), math.floor((a[1] + b[1]) / 2 - n[1] * .6))


def rise_of(a, b, n, base):
    return ground(math.floor((a[0] + b[0]) / 2 + n[0] * 4), math.floor((a[1] + b[1]) / 2 + n[1] * 4)) + P.LIP - base


claims, dropped = A.panels(w, quads, base_of, rise_of, is_floor,
                           lambda x, z: not on_board(x, z) or not land[x, z] or (x, z) in works_cells, ground, LOOK)
panel_cells = {(x, z) for x, _, z in claims}
for x, y, z in claims:                               # a floor a panel stands on is no longer walked
    if is_floor(x, z) and y >= feet(x, z):
        floor[x, z] = False

# ---- a ladder up each wool's ledge, against bare rock ----------------------------------------------------------------
ladders = []
for (x, z), side, _ in P.LEDGES:
    for c, s in (((x, z), side), (turned((x, z)), turn_side(side))):
        A.ladder_bay(w, c[0], c[1], s, feet(*c), ground, LOOK)
        ladders.append(c)

# ---- the works: the hall over the spawn room, the works over the wool rooms ------------------------------------------
building_cells = set()


def works(poly, storeys, ladder, base, door, skylights=False):
    global building_cells
    for image in (False, True):
        pg = [P.R(p) for p in poly] if image else poly
        lad = (turned(ladder[0]), turn_side(ladder[1])) if image else ladder
        cs = A.poly_cells(pg)
        building_cells |= A.building(w, pg, base, [(set(cs), storeys, lad)], LOOK, skylights=skylights)
        A.door(w, [turned(c) for c in door][::-1] if image else door, base, LOOK)


hall_poly, hall_storeys, hall_ladder = P.HALL
works(hall_poly, hall_storeys, hall_ladder, YS + 2, P.HALL_DOOR, skylights=True)
for poly, storeys, ladder, door in P.WORKS:
    works(poly, storeys, ladder, feet(*door[1]), door)
(a, b), (c, d) = turned(P.HALL_CHIMNEY[:2]), turned(P.HALL_CHIMNEY[2:])
A.chimney(w, P.HALL_CHIMNEY, 7, LOOK, drift=(1, 0))
A.chimney(w, (min(a, c), min(b, d), max(a, c), max(b, d)), 7, LOOK, drift=(-1, 0))
equipment = 0
for poly in [P.HALL[0]] + [wk[0] for wk in P.WORKS]:
    roof = A.flat_roof(w, A.poly_cells(poly))
    lit = A.flat_roof(w, A.poly_cells(poly), skylights=True)
    for kit in (A.roof_kit(roof, around=lit), A.roof_kit(roof, mirror=turned, around=lit)):
        A.lay_roof_kit(w, kit, LOOK)
        equipment += len(kit)

# ---- each wool corridor's defence wall, its chests, and the redstone line across each room's entry row ---------------
wall_cells = set()
for (a, b), ((cx, cz), facing) in zip(P.WALLS, P.CHESTS[::2]):
    wx = a[0] if facing == "+x" else a[0] - 1             # the wall stands on the cell beside its chests
    wall_cells |= {(wx, z) for z in range(a[1], b[1])}
wall_cells |= {turned(c) for c in wall_cells}
for x, z in wall_cells:
    for y in range(feet(x, z) - 1, feet(x, z) + P.WALL_COURSES):
        w.set(x, y, z, B.BEDROCK)
for (x, z), facing in P.CHESTS:
    way = {"+x": "e", "-x": "w"}[facing]
    props.defence_chests(w, [(x, z)], feet(x, z), way)
    tx, tz = turned((x, z))
    props.defence_chests(w, [(tx, tz)], feet(tx, tz), turn_side(way))
for (ax, az), (bx, bz) in P.LINES:
    for line in ([(x, az) for x in range(ax + 1, bx)], [turned((x, az)) for x in range(ax + 1, bx)]):
        for k, (x, z) in enumerate(line):
            end = k in (0, len(line) - 1)
            w.set(x, feet(x, z), z, B.REDSTONE_TORCH if end else B.REDSTONE_WIRE, 5 if end else 0)

# ---- the hut against the hub's west wall, the islands' daises --------------------------------------------------------
length, depth_, facing, (hx, hz) = P.HUT
hut_cells = A.hut(w, hx, hz, length, depth_, facing, feet(hx, hz), LOOK)
lx, lz = (length, depth_) if facing in ("n", "s") else (depth_, length)
tx, tz = turned((hx + lx - 1, hz + lz - 1))
hut_cells |= A.hut(w, tx, tz, length, depth_, turn_side(facing), feet(tx, tz), LOOK)
dais_cells = set()
dx, dz, size = P.DAIS
for x0, z0 in ((dx, dz), turned((dx + size - 1, dz + size - 1))):
    A.dais(w, x0, z0, size, feet(x0 + size // 2, z0 + size // 2), LOOK)
    dais_cells |= {(x, z) for x in range(x0, x0 + size) for z in range(z0, z0 + size)}

# ---- the bare rock walls: overhanging and undercut, never climbed ----------------------------------------------------
doors = {c for _, _, _, door in P.WORKS for c in door} | set(P.HALL_DOOR)
doors |= {turned(c) for c in doors}
spared = (around(set(ladders), 3) | around(building_cells | hut_cells | wall_cells | frame_cells, 2)
          | around(panel_cells, 2) | around(plated, 1) | set(cells(flight)) | around(doors, 3)
          | around({c for c, _ in P.CHESTS} | {turned(c) for c, _ in P.CHESTS}, 2))
jutted, hollowed = A.rock_faces(w, list(cells(floor)), feet, lambda x, z: not on_board(x, z) or (x, z) in spared,
                                lambda x, z: L._at(L.ROCK_B, x * 2 + 7, z), lambda x, z: L._at(L.WEAR, x + 11, z * 2),
                                LOOK)

# ---- the floor worn, clear of everything a player has to find or stand at --------------------------------------------
busy = around(plated | building_cells | wall_cells | hut_cells | dais_cells | frame_cells | set(ladders), 2) | \
    around({c for c, _ in P.CHESTS} | {turned(c) for c, _ in P.CHESTS}, 3) | around(doors, 2)
eligible = [(x, z) for x, z in cells(floor & ~flight) if (x, z) not in busy
            and all(is_floor(x + a, z + b) and feet(x + a, z + b) == feet(x, z) for a, b in DIRS.values())]
worn = A.wear(w, eligible, feet, lambda x, z: 2 if L._at(L.WEAR, x, z) > 0.8 else 1 if L._at(L.WEAR, x, z) > 0.66
              else 0, LOOK)

# ---- what the floors carry: the team's rim where a floor meets a wall, chevrons, and each hub's emblem ---------------
floor_y = {c: feet(*c) for c in cells(floor)}
floor_y.update(hollowed)


def side_of(x, z):
    return 0 if z >= P.H / 2 else 1


rimmed = A.rim(w, floor_y, side_of, LOOK, skip=plated)


def takes_mark(x, z):
    return ((x, z) not in plated and not flight[x, z] and (x, z) not in hut_cells and (x, z) not in building_cells
            and (x, z) not in dais_cells and w.id(x, floor_y[(x, z)], z) == B.AIR)


chevroned = 0
for tip, way in P.CHEVRONS:
    chevroned += A.chevrons(w, tip, way, floor_y, takes_mark, LOOK, 0, count=2, size=3, gap=4)
    chevroned += A.chevrons(w, (P.W - tip[0], P.H - tip[1]), (-way[0], -way[1]), floor_y, takes_mark, LOOK, 1,
                            count=2, size=3, gap=4)
(ex, ez), reach = P.EMBLEM
for team, (cx, cz) in ((0, (ex, ez)), (1, turned((ex, ez)))):
    for x in range(cx - reach, cx + reach + 1):
        for z in range(cz - reach, cz + reach + 1):
            d = abs(x - cx) + abs(z - cz)
            if (d == reach or d == 0 or (d == reach - 2 and (x == cx or z == cz))) and (x, z) in floor_y \
                    and takes_mark(x, z):
                w.set(x, floor_y[(x, z)] - 1, z, *LOOK.rim(team))

# ---- dead ground on the surface: slabs on the orange's steps, dead leaves, bare olives, mesa and swamp ---------------
ORANGE = {(B.SAND, 1), (B.RED_SANDSTONE, 0), (B.STAINED_CLAY, 1)}
SOOTY = {(B.STAINED_CLAY, 15), (B.PLANKS, 5), (B.DIRT, 1), (B.DIRT, 2)}
crust_top = {}
for x, z in cells(land & ~cut):
    t = w.top(x, z)
    if P.GROUND - 4 <= t < P.GROUND and w.get(x, t, z) in ORANGE | SOOTY:
        crust_top[(x, z)] = t
slabbed = 0
for (x, z), t in crust_top.items():
    if w.get(x, t, z) not in ORANGE or w.id(x, t + 1, z) != B.AIR:
        continue
    if any(crust_top.get((x + a, z + b)) == t + 1 and w.get(x + a, t + 1, z + b) in ORANGE for a, b in DIRS.values()):
        w.set(x, t + 1, z, 182, 0)                     # a red sandstone slab halves the step
        slabbed += 1
near_cut = around(set(cells(cut)), 2) | around(building_cells | set(ladders), 3)
LEAF = L._field(5, 91)
leafed = 0
for (x, z), t in crust_top.items():
    if (x, z) in near_cut or w.id(x, t + 1, z) != B.AIR:
        continue
    if L._at(LEAF, x, z) > 0.74 and L._hash(x, 7, z) < 0.45:
        w.set(x, t + 1, z, B.LEAVES, 4)                # oak leaves that never decay, browned by the biome
        leafed += 1
from dataclasses import replace as _replace  # noqa: E402
from pgmvox.scenery import trees as T  # noqa: E402

library = T.library()
bare = [_replace(library[n], blocks=tuple(b for b in library[n].blocks if b[3] not in T.LEAVES)) for n in P.OLIVES]
GIVES = T.GIVES_WAY | {B.SAND, B.RED_SANDSTONE, B.STAINED_CLAY, B.DIRT, B.PLANKS, B.LEAVES, 182}
far = around(near_cut, 2)
sites = sorted((c for c in crust_top if c[1] >= P.H / 2 and c not in far
                and all((c[0] + a, c[1] + b) in crust_top for a in range(-2, 3) for b in range(-2, 3))),
               key=lambda c: L._hash(c[0], 3, c[1]))
planted = []
for x, z in sites:
    if len(planted) == P.TREES_PER_SIDE:
        break
    if any(abs(x - a) + abs(z - b) < 16 for a, b in planted):
        continue
    tree = bare[len(planted) % len(bare)]
    tx, tz = turned((x, z))
    if T.plant(w, x, z, tree, 0, gives_way=GIVES) and T.plant(w, tx, tz, tree, 2, gives_way=GIVES):
        planted.append((x, z))
w.biome[:, :] = P.BIOME_MESA
for (x, z) in crust_top:
    if LOOK.patch(x, z):
        w.biome[x, z] = P.BIOME_SWAMP

# ---- no orange showing at a panel's ends and no sand on a face: a block of the orange beside a panel and open to a cut
# is rock, and red sand open at its side is red sandstone --------------------------------------------------------------
sealed = 0
for x, y, z in claims:
    for a, b in DIRS.values():
        for k in (1, 2):
            px, pz = x + a * k, z + b * k
            if (px, y, pz) in claims or not on_board(px, pz) or w.get(px, y, pz) not in ORANGE | SOOTY:
                continue
            if any(w.id(px + c, y, pz + d) == B.AIR for c, d in DIRS.values()):
                w.set(px, y, pz, *LOOK.rock(px, y, pz))
                sealed += 1
sand = np.argwhere((w.ids == B.SAND) & (w.dat == 1))
for i, y, k in sand:
    x, z = int(i + w.x0), int(k + w.z0)
    if any(on_board(x + a, z + b) and w.id(x + a, y, z + b) == B.AIR for a, b in DIRS.values()):
        w.set(x, y, z, B.RED_SANDSTONE, 0)
        sealed += 1

# ---- nothing that falls stands over air ------------------------------------------------------------------------------
for falls, holds in (((B.GRAVEL, 0), (B.STONE, 5)), ((B.SAND, 1), (B.RED_SANDSTONE, 0))):
    loose = (w.ids[:, 1:, :] == falls[0]) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose] = holds[0]
    w.dat[:, 1:, :][loose] = holds[1]

# ---- the objectives: the wools in their rooms, the monuments on each spawn yard ringed in their wool's colour --------
from mapxml import OBJECTIVES  # noqa: E402
from pgmvox.play.objectives import Wool  # noqa: E402

OBJECTIVES.stamp(w)
for wool in OBJECTIVES.of(Wool):
    sx, sy, sz = wool.slot
    for x in range(sx - 1, sx + 2):
        for z in range(sz - 1, sz + 2):
            if (x, z) != (sx, sz):
                w.set(x, sy - 1, z, B.STAINED_CLAY, DYES[wool.color])

w.save(sys.argv[1], "Pithead", (P.SPAWN_AT[0], YS + 2, P.SPAWN_AT[1]))
print("generated", int(land.sum()), "columns of land,", int(floor.sum()), "of floor,", len(claims), "panel blocks,",
      worn, "worn,", len(jutted), "jutting,", len(hollowed), "hollowed,", rimmed, "rim blocks,", chevroned,
      "chevron blocks,", striped, "hazard stripes,", equipment, "pieces on the roofs,", slabbed, "slabs on the orange,",
      leafed, "leaves,", sealed, "orange blocks sealed, olives at", planted)
for i in dropped:
    a, b = quads[i][0], quads[i][1]
    print(f"  panel left out at ({(a[0] + b[0]) / 2:.0f}, {(a[1] + b[1]) / 2:.0f})")
