"""Build Pithead from the plan through Seamworks' asset functions in Seamworks' look: the composed pieces as islands of
banded rock over the void, their floors at their levels and stepped between them, the banks of orange ground at the
hub's back with their panels, the shaft and its headframe, the works over the spawn and the wool rooms, the defence
walls, and the objectives.

    python3 gen.py <build-dir>
"""
import math
import random
import sys

import numpy as np
from scipy.ndimage import binary_dilation, distance_transform_edt

import plan as P  # noqa: I001  (plan puts the library on the path, and is the `plan` Seamworks' look reads)
from pgmvox import B, World
from pgmvox.built import props
from pgmvox.geom.noise import fbm

A = P.seamworks("assets", "seamworks_assets")
L = P.seamworks("look", "seamworks_look")
YS = P.YS
LOOK = L.LOOK
DIRS = A.DIRS

w = World(0, 0, P.W, P.H, sy=YS + 44)
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


def both(poly):
    """A red polygon's columns and its half turn's."""
    return mask(poly) | mask([P.R(p) for p in poly])


def cells(m):
    for i, k in zip(*np.nonzero(m)):
        yield int(i + w.x0), int(k + w.z0)


def turned(c):
    return P.RC(c)


def around(points, r):
    out = set()
    for x, z in points:
        out |= {(x + a, z + b) for a in range(-r, r + 1) for b in range(-r, r + 1)}
    return out


# ---- the land: the composed pieces less the shaft, pushed out at the void edge where nothing is kept clear ----------
pieces = np.zeros(X.shape, bool)
for poly in P.PIECES.values():
    pieces |= both(poly)
shaft = both(P.HOLE)
pieces &= ~shaft
x0, z0, x1, z1 = P.BUILD
build_zone = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
wall_cells = set()
for (a, b, _), ((cx, cz), facing) in zip(P.WALLS, P.CHESTS[::2]):
    wx = a[0] if facing == "+x" else a[0] - 1             # the wall stands on the cell beside its chests
    wall_cells |= {(wx, z) for z in range(a[1], b[1])}
wall_cells |= {turned(c) for c in wall_cells}
kept_clear = binary_dilation(build_zone & ~pieces, iterations=1) | binary_dilation(shaft, iterations=2)
for x, z in around(wall_cells, 5):
    if 0 <= x < P.W and 0 <= z < P.H:
        kept_clear[x, z] = True
wobble = fbm(X.shape, 7, 3, seed=96)
wobble = (wobble + wobble[::-1, ::-1]) / 2
wobble = (wobble - wobble.min()) / (wobble.max() - wobble.min())
reach = distance_transform_edt(~pieces)
land = pieces | ((reach <= wobble * (P.OUTLINE + 0.99)) & ~kept_clear & ~shaft)

# ---- the floor's levels: each piece's own, the surface's, then the flights cut between them --------------------------
level = np.zeros(X.shape)
for poly, v in P.LEVELS:
    level[both(poly)] = v
surface = np.zeros(X.shape, bool)
for poly in P.SURFACE:
    surface |= both(poly)
level[surface] = P.SURFACE_RISE
flight = np.zeros(X.shape, bool)
uphill = np.zeros(X.shape + (2,))
for poly, (lp, lv), (hp, hv) in P.FLIGHTS:
    for pg, lo, hi in ((poly, lp, hp), ([P.R(p) for p in poly], P.R(lp), P.R(hp))):
        m = mask(pg) & land
        vx, vz = hi[0] - lo[0], hi[1] - lo[1]
        run = math.hypot(vx, vz)
        t = ((CX - lo[0]) * vx + (CZ - lo[1]) * vz) / (run * run) + L.STEP[X % P.W, Z % P.H] * 1.4 / run
        level[m] = (lv + (hv - lv) * np.clip(t, 0, 1))[m]
        flight |= m
        uphill[m] = (vx, vz)
surface &= ~flight
# the land pushed out past a piece takes the level and the ground of the piece it was pushed from
idx = distance_transform_edt(~pieces, return_distances=False, return_indices=True)
pushed = land & ~pieces
level[pushed] = level[idx[0], idx[1]][pushed]
surface[pushed] = surface[idx[0], idx[1]][pushed]
flight[pushed] = False
D = np.floor(level + 0.5).astype(int)
banks = np.zeros(X.shape, bool)
for poly in P.BANKS:
    banks |= both(poly)
banks &= land
floor = land & ~banks & ~surface                 # the stone a player walks on


def on_board(x, z):
    return 0 <= x < P.W and 0 <= z < P.H


def is_floor(x, z):
    return on_board(x, z) and bool(floor[x, z])


def feet(x, z):
    return YS + int(D[x, z])


def ground(x, z):
    """The surface's level before its soot patches sink it: the banks', the walked surface's, or a floor's."""
    if not on_board(x, z) or not land[x, z]:
        return 0
    return YS + P.BANK_RISE if banks[x, z] else feet(x, z)


# ---- the rock: banded stone under every floor, thickest where the land is widest, ragged underneath; the orange
# ground and its crust on the surface and the banks, level round the works ---------------------------------------------
inland = distance_transform_edt(land)
rag = fbm(X.shape, 5, 3, seed=97)
rag = (rag - rag.min()) / (rag.max() - rag.min())
depth = 3 + np.sqrt(inland) * 4.2 + rag * 4
for x, z in cells(land):
    top = min(feet(x, z), YS) - 1
    w.column(x, z, max(top - int(depth[x, z]), P.KILL_Y + 4), ground(x, z) - 1, B.STONE)
L.paint_rock(w)
for x, z in cells(floor):
    w.set(x, feet(x, z) - 1, z, *LOOK.cut_floor(x, z))
works_cells = set()
for poly in [P.HALL[0]] + [wk[0] for wk in P.WORKS]:
    works_cells |= set(A.poly_cells(poly)) | set(A.poly_cells([P.R(p) for p in poly]))
P.set_apron(around(works_cells, 2) | around({c for c in cells(flight)}, 1))
for x, z in cells(banks | surface):
    A.lay_crust(w, x, z, ground, LOOK)
A.stairs(w, list(cells(floor & flight)), feet, is_floor, lambda x, z: tuple(uphill[x, z]), LOOK)

# ---- the rock left standing: the mid stone's two outcrops over the middle's floor, and a boss on each frontline ------
crag = fbm(X.shape, 3, 2, seed=98)
crag = (crag + crag[::-1, ::-1]) / 2
crag = (crag - crag.min()) / (crag.max() - crag.min())
outcrop = np.zeros(X.shape, bool)
for poly, rise in ((P.MID_ROCK, P.MID_ROCK_RISE), (P.FRONT_ROCK, P.FRONT_ROCK_RISE)):
    m = both(poly) & land
    edge_in = distance_transform_edt(m)
    for x, z in cells(m):
        foot = feet(x, z) if floor[x, z] else w.top(x, z) + 1
        height = min(rise, 1 + int(edge_in[x, z] * 1.6 + crag[x, z] * 2))
        w.column(x, z, min(foot, feet(x, z)) - 2, foot + height - 1, B.STONE)
    outcrop |= m
L.paint_rock(w)
floor &= ~outcrop
surface &= ~outcrop

# ---- the shaft's collar of iron plates and smooth stone, and the headframe over it -----------------------------------
lip = binary_dilation(shaft, iterations=1) & floor
plated = set(cells(lip))
for x, z in plated:
    y = feet(x, z) - 1
    w.set(x, y, z, *(LOOK.plate(x, y, z, "plate") if L._hash(x // 3, 5, z // 3) < 0.4 else (B.DSLAB, 0)))
hx0, hz0 = min(p[0] for p in P.HOLE), min(p[1] for p in P.HOLE)
hx1, hz1 = max(p[0] for p in P.HOLE) - 1, max(p[1] for p in P.HOLE) - 1


def headframe(box, base):
    """A tower of four legs standing on the shaft's collar and leaning in as they rise, ringed in iron bars twice, a
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


collar = (hx0 - 1, hz0 - 1, hx1 + 1, hz1 + 1)
frame_cells = headframe(collar, YS)
(a, b), (c, d) = turned(collar[:2]), turned(collar[2:])
frame_cells |= headframe((min(a, c), min(b, d), max(a, c), max(b, d)), YS)

# ---- the panels: on the surface's faces over the stone and the banks' toward the hub, red's laid out and turned onto
# blue's ---------------------------------------------------------------------------------------------------------------
quads = []


def wall_of(a, b, n, rng, shade0=0):
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    ux, uz = (b[0] - a[0]) / length, (b[1] - a[1]) / length
    for j, (s0, s1) in enumerate(P.SP.panel_runs(a, b, rng)):
        lean = 11 + rng.uniform(-1.5, 1.5)
        quads.append(((a[0] + ux * s0, a[1] + uz * s0), (a[0] + ux * s1, a[1] + uz * s1), n,
                      (lean, lean + rng.uniform(-1.5, 1.5)), (shade0 + j) % 2))


for k, (a, b, n) in enumerate(P.FACES):
    wall_of(a, b, n, random.Random(41 + k), k)
quads += [(P.R(a), P.R(b), (-n[0], -n[1]), lean, shade) for a, b, n, lean, shade in quads]


def base_of(a, b, n):
    inside = (math.floor((a[0] + b[0]) / 2 - n[0] * .6), math.floor((a[1] + b[1]) / 2 - n[1] * .6))
    return feet(*inside) if is_floor(*inside) else YS


def rise_of(a, b, n, base):
    behind = (math.floor((a[0] + b[0]) / 2 + n[0] * 4), math.floor((a[1] + b[1]) / 2 + n[1] * 4))
    return ground(*behind) + P.LIP - base


claims, dropped = A.panels(w, quads, base_of, rise_of, is_floor, lambda x, z: not on_board(x, z) or not land[x, z],
                           ground, LOOK)

# ---- the works: the hall over the spawn room, the works over the wool rooms ------------------------------------------
building_cells = set()


def works(poly, storeys, ladder, base, door, skylights=False):
    global building_cells
    for image in (False, True):
        pg = [P.R(p) for p in poly] if image else poly
        lad = (turned(ladder[0]), {"w": "e", "e": "w", "n": "s", "s": "n"}[ladder[1]]) if image else ladder
        cs = A.poly_cells(pg)
        building_cells |= A.building(w, pg, base, [(set(cs), storeys, lad)], LOOK, skylights=skylights)
        A.door(w, [turned(c) for c in door][::-1] if image else door, base, LOOK)


hall_poly, hall_storeys, hall_ladder = P.HALL
works(hall_poly, hall_storeys, hall_ladder, YS + 2, P.HALL_DOOR, skylights=True)
for poly, storeys, ladder, door in P.WORKS:
    works(poly, storeys, ladder, YS + P.SURFACE_RISE, door)
x0_, z0_, x1_, z1_ = P.HALL_CHIMNEY
A.chimney(w, P.HALL_CHIMNEY, 7, LOOK, drift=(1, 0))
(a, b), (c, d) = turned((x0_, z0_)), turned((x1_, z1_))
A.chimney(w, (min(a, c), min(b, d), max(a, c), max(b, d)), 7, LOOK, drift=(-1, 0))
equipment = 0
for poly in [P.HALL[0]] + [wk[0] for wk in P.WORKS]:
    roof = A.flat_roof(w, A.poly_cells(poly))
    lit = A.flat_roof(w, A.poly_cells(poly), skylights=True)
    for kit in (A.roof_kit(roof, around=lit), A.roof_kit(roof, mirror=turned, around=lit)):
        A.lay_roof_kit(w, kit, LOOK)
        equipment += len(kit)

# ---- each wool approach's defence wall, its chests, and the redstone line across each room's entry row ---------------
for x, z in wall_cells:
    for y in range(feet(x, z) - 1, feet(x, z) + 3):     # three courses over the floor
        w.set(x, y, z, B.BEDROCK)
for (x, z), facing in P.CHESTS:
    way = {"+x": "e", "-x": "w"}[facing]
    props.defence_chests(w, [(x, z)], feet(x, z), way)
    tx, tz = turned((x, z))
    props.defence_chests(w, [(tx, tz)], feet(tx, tz), {"e": "w", "w": "e"}[way])
for (ax, az), (bx, bz) in P.LINES:
    for line in ([(x, az) for x in range(ax + 1, bx)], [turned((x, az)) for x in range(ax + 1, bx)]):
        for k, (x, z) in enumerate(line):
            end = k in (0, len(line) - 1)
            w.set(x, feet(x, z), z, B.REDSTONE_TORCH if end else B.REDSTONE_WIRE, 5 if end else 0)

# ---- the hub's hut and spoil, the middle's dais ----------------------------------------------------------------------
length, depth_, facing, (hx, hz) = P.HUT
hut_cells = A.hut(w, hx, hz, length, depth_, facing, feet(hx, hz), LOOK)
lx, lz = (length, depth_) if facing in ("n", "s") else (depth_, length)
tx, tz = turned((hx + lx - 1, hz + lz - 1))
hut_cells |= A.hut(w, tx, tz, length, depth_, {"w": "e", "e": "w", "n": "s", "s": "n"}[facing], feet(tx, tz), LOOK)
toe, crest, peak = P.SPOIL
heaped = A.spoil(w, toe, crest, peak, feet, is_floor, LOOK)
heaped |= A.spoil(w, [P.R(p) for p in toe], [P.R(p) for p in crest], peak, feet, is_floor, LOOK)
dx, dz, size = P.DAIS
A.dais(w, dx, dz, size, feet(dx + size // 2, dz + size // 2), LOOK)
dais_cells = {(x, z) for x in range(dx, dx + size) for z in range(dz, dz + size)}

# ---- the floor worn, clear of everything a player has to find or stand at --------------------------------------------
busy = around(plated | building_cells | wall_cells | hut_cells | dais_cells | frame_cells | heaped, 2) | \
    around({c for c, _ in P.CHESTS} | {turned(c) for c, _ in P.CHESTS}, 3)
eligible = [(x, z) for x, z in cells(floor & ~flight) if (x, z) not in busy
            and all(is_floor(x + a, z + b) and feet(x + a, z + b) == feet(x, z) for a, b in DIRS.values())]
worn = A.wear(w, eligible, feet, lambda x, z: 2 if L._at(L.WEAR, x, z) > 0.8 else 1 if L._at(L.WEAR, x, z) > 0.66
              else 0, LOOK)

# ---- the team's rim where the floor meets a wall, and the chevrons ---------------------------------------------------
floor_y = {c: feet(*c) for c in cells(floor)}
rimmed = A.rim(w, floor_y, lambda x, z: 0 if z >= P.H / 2 else 1, LOOK, skip=plated)


def takes_chevron(x, z):
    return ((x, z) not in plated and not flight[x, z] and (x, z) not in hut_cells and (x, z) not in building_cells
            and w.id(x, floor_y[(x, z)], z) == B.AIR)


chevroned = 0
for tip, way in P.CHEVRONS:
    chevroned += A.chevrons(w, tip, way, floor_y, takes_chevron, LOOK, 0, count=2, size=3, gap=4)
    chevroned += A.chevrons(w, (P.W - tip[0], P.H - tip[1]), (-way[0], -way[1]), floor_y, takes_chevron, LOOK, 1,
                            count=2, size=3, gap=4)

# ---- dead ground on the surface and the banks: slabs on the orange's steps, dead leaves, bare olives, mesa and swamp -
ORANGE = {(B.SAND, 1), (B.RED_SANDSTONE, 0), (B.STAINED_CLAY, 1)}
crust_top = {}
for x, z in cells(banks | surface):
    t = w.top(x, z)
    if ground(x, z) - 4 <= t < ground(x, z):
        crust_top[(x, z)] = t
slabbed = 0
for (x, z), t in crust_top.items():
    if w.get(x, t, z) not in ORANGE or w.id(x, t + 1, z) != B.AIR:
        continue
    if any(crust_top.get((x + a, z + b)) == t + 1 and w.get(x + a, t + 1, z + b) in ORANGE for a, b in DIRS.values()):
        w.set(x, t + 1, z, 182, 0)                     # a red sandstone slab halves the step
        slabbed += 1
paths = around(works_cells | set(cells(flight)) | {c for _, wk in enumerate(P.WORKS) for c in wk[3]}, 3)
paths |= {turned(c) for c in paths}
LEAF = L._field(5, 91)
leafed = 0
for (x, z), t in crust_top.items():
    if (x, z) in paths or w.id(x, t + 1, z) != B.AIR:
        continue
    if L._at(LEAF, x, z) > (0.7 if banks[x, z] else 0.8) and L._hash(x, 7, z) < 0.45:
        w.set(x, t + 1, z, B.LEAVES, 4)                # oak leaves that never decay, browned by the biome
        leafed += 1
from dataclasses import replace as _replace  # noqa: E402
from pgmvox.scenery import trees as T  # noqa: E402

library = T.library()
bare = [_replace(library[n], blocks=tuple(b for b in library[n].blocks if b[3] not in T.LEAVES)) for n in P.OLIVES]
GIVES = T.GIVES_WAY | {B.SAND, B.RED_SANDSTONE, B.STAINED_CLAY, B.DIRT, B.PLANKS, B.LEAVES, 182}
planted = []
sites = []
for poly in P.BANKS:
    inner = [c for c in A.poly_cells(poly) if all((c[0] + a, c[1] + b) in crust_top for a in range(-2, 3)
                                                  for b in range(-2, 3))]
    sites.append(sorted(inner, key=lambda c: L._hash(c[0], 3, c[1])))
sites += [[c] for c in P.SURFACE_OLIVES]
for k, options in enumerate(sites):
    for x, z in options:
        tree = bare[k % len(bare)]
        tx, tz = turned((x, z))
        if T.plant(w, x, z, tree, k % 4, gives_way=GIVES) and T.plant(w, tx, tz, tree, (k + 2) % 4, gives_way=GIVES):
            planted.append((x, z))
            break
w.biome[:, :] = P.BIOME_MESA
for (x, z) in crust_top:
    if LOOK.patch(x, z):
        w.biome[x, z] = P.BIOME_SWAMP

# ---- nothing that falls stands over air ------------------------------------------------------------------------------
for falls, holds in (((B.GRAVEL, 0), (B.STONE, 5)), ((B.SAND, 1), (B.RED_SANDSTONE, 0))):
    loose = (w.ids[:, 1:, :] == falls[0]) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose] = holds[0]
    w.dat[:, 1:, :][loose] = holds[1]

# ---- the objectives: the wools in their rooms, the monuments on each spawn yard, a plinth under each -----------------
from mapxml import OBJECTIVES  # noqa: E402
from pgmvox.play.objectives import Wool  # noqa: E402

OBJECTIVES.stamp(w)
for wool in OBJECTIVES.of(Wool):
    sx, sy, sz = wool.slot
    for x in range(sx - 1, sx + 2):
        for z in range(sz - 1, sz + 2):
            if (x, z) != (sx, sz):
                w.set(x, sy - 1, z, B.STONE, 6)

w.save(sys.argv[1], "Pithead", (P.SPAWN_AT[0], YS + 2, P.SPAWN_AT[1]))
print("generated", int(land.sum()), "columns of land,", int(floor.sum()), "of floor,", len(claims), "panel blocks,",
      worn, "worn,", rimmed, "rim blocks,", chevroned, "chevron blocks,", equipment, "pieces on the roofs,", slabbed,
      "slabs on the orange,", leafed, "leaves, olives at", planted)
for i in dropped:
    a, b = quads[i][0], quads[i][1]
    print(f"  panel left out at ({(a[0] + b[0]) / 2:.0f}, {(a[1] + b[1]) / 2:.0f})")
