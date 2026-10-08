"""Generate Tamarisk Wash from the plan: red's half (x < 0) is built, then mirrored across the wash (orient.turn_world,
x' = -1 - x); the monuments are stamped on both halves from their objects.

The ground is the plan's heightfield, exactly. Rock in the colours of a mesa (hardened clay and stained clay in
beds that dip a little), sand and red sand on top by slope, the wash's floor of gravel and dried mud, the oasis's
grass. On it: the roads, the kasbah and the Souk, the caravanserai, Table Rock's steps and ruins, the arch, the
aqueduct, the qanat and the cistern, the old mine, the palms and the dressing.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np
from scipy import ndimage

import desert as DS
import kit
import plan as P
from pgmvox import B, World, rng
from pgmvox import build as BLD
from pgmvox import facade as F
from pgmvox import props, route, shapes
from pgmvox import terrain as T
from pgmvox import under as U
from pgmvox.noise import fbm
from pgmvox.orient import door as door_data, stair as stair_data, turn_world

SY = 128


def red_cols(w):
    X, _ = w.grid()
    return X < 0


def lay_ground(w, L):
    X, Z = w.grid()
    H = L.H.copy()
    red = red_cols(w)
    rock = T.Strata([((B.STAINED_CLAY, 1), 2, 2), ((B.STAINED_CLAY, 14), 1.4, 2), ((B.STAINED_CLAY, 12), 1.6, 3),
                     ((B.HARDENED_CLAY, 0), 2, 3), ((B.STAINED_CLAY, 0), 1, 1), ((B.STAINED_CLAY, 4), 0.8, 1),
                     ((B.STAINED_CLAY, 8), 0.8, 1)], length=170, seed=9, start=0)
    offset = T.bed_offset((w.sx, w.sz), dip=(0.0, 0.03), fold=2.5, cell=30, seed=4)
    bed = T.beds(rock, offset, flecks=[((B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 12), 0.04)], seed=2)
    deg = T.lay(w, H, red, top=T.by_angle([(16, (B.SAND, 0)), (34, (B.SAND, 1)), (90, (B.SANDSTONE, 0))]),
                bands=bed, under=(B.SANDSTONE, 0), from_y=3, soil=((18, 3), (30, 1)))
    r = rng(P.BOARD, "ground")
    sh = (w.sx, w.sz)
    patch, cell = fbm(sh, 8, 2, seed=61), r.random(sh)
    for i, k in np.argwhere(red):
        top = int(H[i, k])
        a = int(deg[i, k])
        c, pv = cell[i, k], patch[i, k]
        if L.water[i, k] > 0:
            w.ids[i, top, k], w.dat[i, top, k] = (B.CLAY, 0) if c < 0.5 else (B.SAND, 0)
            w.ids[i, top + 1:int(L.water[i, k]) + 1, k] = B.WATER
            w.dat[i, top + 1:int(L.water[i, k]) + 1, k] = 0
            continue
        if L.wash[i, k] and top <= P.WASH_FLOOR + 4:
            blk = (B.GRAVEL, 0) if c < 0.3 else (B.DIRT, 1) if c < 0.55 else (B.STAINED_CLAY, 12) if pv > 0.1 else (B.SAND, 0)
            w.ids[i, top, k], w.dat[i, top, k] = blk
        elif a <= 16:
            blk = (B.SAND, 1) if pv > 0.28 else (B.SAND, 0)
            if c > 0.97:
                blk = (B.SANDSTONE, 0)
            elif c > 0.94:
                blk = (B.HARDENED_CLAY, 0)
            w.ids[i, top, k], w.dat[i, top, k] = blk
        elif a <= 34:
            w.ids[i, top, k], w.dat[i, top, k] = (B.SAND, 1) if c < 0.6 else (B.HARDENED_CLAY, 0) if c < 0.8 else (B.STAINED_CLAY, 1)
        else:                                                         # the bed shows where the ground is steep
            blk = bed(i, k, [top])[0]
            w.ids[i, top, k], w.dat[i, top, k] = blk
        if L.grove[i, k]:
            w.ids[i, top, k], w.dat[i, top, k] = (B.GRASS, 0) if c < 0.8 else (B.DIRT, 2)
            if rng(P.BOARD, "grass%d" % (i * 400 + k)).random() < 0.22 and w.id(w.x0 + i, top + 1, w.z0 + k) == B.AIR:
                w.set(w.x0 + i, top + 1, w.z0 + k, B.TALLGRASS, 1)
    w.biome[:, :] = 2
    w.biome[L.grove] = 1
    return deg


def roads(w, L):
    X, Z = w.grid()
    H = L.H.copy()
    for rt in L.routes:
        if rt["kind"] == "road":
            surf = ((B.SANDSTONE, 2), (B.DIRT, 1), (B.SAND, 1), (B.GRAVEL, 0))
            wts = (0.35, 0.3, 0.2, 0.15)
        else:
            surf = ((B.DIRT, 1), (B.SAND, 0), (B.GRAVEL, 0), (B.SANDSTONE, 0))
            wts = (0.4, 0.3, 0.2, 0.1)
        route.pave(w, np.where(L.water > 0, 0, H), X, Z, [tuple(p) for p in rt["line"]], width=rt["width"], surface=surf,
                   weights=wts, clear=3, seed=len(rt["name"]), keep=(X >= 0) | (L.water > 0))
        if rt["grade"] > 0.4:
            route.steps(w, H, X, Z, [tuple(p) for p in rt["line"]], block=B.SANDSTONE_STAIRS, width=min(rt["width"], 3))


def houses(w, L):
    r = rng(P.BOARD, "houses")
    ground_at = lambda x, z: P.at(L, x, z)                          # noqa: E731
    for key, b in P.houses().items():
        if key == "minaret":
            continue
        BLD.site(w, b["cells"], b["floor"], ground_at, margin=2, fill=(B.SANDSTONE, 0), top=(B.SAND, 0),
                 under=(B.SANDSTONE, 0), clear=14)
        res = BLD.house(w, b["house"], ground_at, r)
        st = b["spec"]["style"]
        if st in ("adobe", "kasbah"):
            BLD.parapet(w, b["cells"], res["eave"] + 1, (B.SANDSTONE, 2), crenel=(B.SANDSTONE, 1) if st == "kasbah" else None)
        if st == "tiled":                                            # the shop's hip roof in cyan clay
            pass
        # shutters: a stained pane band under the eave on the door side is the style's window; add an awning
        if st == "adobe":
            dx, dz = b["door"]
            for off in (-1, 0, 1):
                pass
    # the kasbah's four turrets, a course of battlement over the roof
    kb = P.houses()["kasbah"]
    xs = [c[0] for c in kb["cells"]]; zs = [c[1] for c in kb["cells"]]
    top = kb["house"].floor + 2 * 4 + 1
    for x0, z0 in ((min(xs), min(zs)), (max(xs) - 2, min(zs)), (min(xs), max(zs) - 2), (max(xs) - 2, max(zs) - 2)):
        for dx in range(3):
            for dz in range(3):
                for y in range(top, top + 4):
                    edge = dx in (0, 2) or dz in (0, 2)
                    w.set(x0 + dx, y, z0 + dz, *((B.SANDSTONE, 2) if edge else (B.AIR, 0)))
                w.set(x0 + dx, top + 4, z0 + dz, B.SANDSTONE, 1 if (dx + dz) % 2 == 0 else 2)
    # the kasbah's hall: a carpet runner, lanterns, two chests of the kit
    f = kb["floor"]
    cx, cz = (min(xs) + max(xs)) // 2, (min(zs) + max(zs)) // 2
    for x in range(min(xs) + 2, max(xs) - 1):
        for z in (cz - 1, cz, cz + 1):
            w.set(x, f + 1, z, B.CARPET, 14)
    for dx, dz in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        w.set(cx + dx, f + 4, cz + dz, B.SEA_LANTERN, 0)
    w.chest(min(xs) + 2, f + 1, min(zs) + 2, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:cooked_beef", 32, 0)], 3)
    w.chest(min(xs) + 2, f + 1, max(zs) - 2, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:arrow", 32, 0)], 3)


def minaret(w, L):
    x0, z0, x1, z1 = P.houses()["minaret"]["spec"]["rect"]
    kit.tower(w, x0, z0, x1, z1, P.PLATEAU, 14, wall=((B.SANDSTONE, 2), (B.SANDSTONE, 2), (B.SANDSTONE, 0)),
              corner=(B.SANDSTONE, 1), floor=(B.PLANKS, 4), slit=(B.STAINED_PANE, 3), door=B.ACACIA_DOOR,
              door_side="n", crown=(B.SANDSTONE, 1), crenel=(B.SANDSTONE, 2), light=(B.SEA_LANTERN, 0),
              rng=rng(P.BOARD, "minaret"), ladder_on="s")


def souk(w, L):
    """The square's floor in cyan and white, stalls on its edges, the sunstone's footing."""
    x0, z0, x1, z1 = P.SQUARE
    sx, sz = P.STONE_AT
    field = F.first_of(F.border(1, (B.STAINED_CLAY, 9)), F.border(0, (B.STAINED_CLAY, 0), at=2),
                       F.medallion(0.0, 0.16, (B.STAINED_CLAY, 4)), F.medallion(0.16, 0.30, (B.STAINED_CLAY, 3)),
                       F.corners(3, (B.STAINED_CLAY, 9)), default=(B.SANDSTONE, 2))
    F.carpet(w, x0, z0, x1, z1, P.PLATEAU, field)
    for y in range(P.PLATEAU + 1, P.PLATEAU + 6):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                w.set(x, y, z, B.AIR)
    props.stalls(w, [(x0 - 1, z) for z in range(z0 + 1, z1)], P.PLATEAU, "e", every=4)
    props.stalls(w, [(x1 + 2, z) for z in range(z0 + 1, z1)], P.PLATEAU, "w", every=4, stripe=11)
    for x, z in ((x0 - 1, z0 - 1), (x1 + 1, z0 - 1), (x0 - 1, z1 + 1), (x1 + 1, z1 + 1)):
        props.lamp(w, x, P.PLATEAU, z, height=3, post=(B.ACACIA_FENCE, 0), cap=None)


def serai(w, L):
    """The caravanserai: a ring of rooms with a flat walkable roof, gates east and west, a courtyard with a trough
    and hay, and a flight of steps up to the roof along the north wall."""
    ring, yard, gate = P.serai_cells()
    top = P.PLATEAU + P.SERAI_WALL
    r = rng(P.BOARD, "serai")
    base = lambda x, y, z: (B.SANDSTONE, 0) if (y - P.PLATEAU) % 3 == 0 else (B.SANDSTONE, 2)       # noqa: E731
    F.extrude(w, ring, P.PLATEAU, top, base=base, faces_=[F.windows(4, 2, 3, (B.STAINED_PANE, 3)), F.courses(3, (B.SANDSTONE, 0))],
              top="parapet-slotted", top_block=(B.SANDSTONE, 1))
    for x, z in gate:
        for y in range(P.PLATEAU + 1, top + 3):
            w.set(x, y, z, B.AIR)
        w.set(x, P.PLATEAU, z, B.SANDSTONE, 2)
    for x, z in yard:
        for y in range(P.PLATEAU + 1, top + 3):
            w.set(x, y, z, B.AIR)
    # the courtyard floor: sand tiles with a border of smooth sandstone
    x0, z0, x1, z1 = P.SERAI
    t = P.SERAI_WALL
    F.carpet(w, x0 + t, z0 + t, x1 - t, z1 - t, P.PLATEAU, F.first_of(F.border(1, (B.SANDSTONE, 2)), F.tiles(2, (B.SAND, 0), (B.SANDSTONE, 0)),
                                                                     default=(B.SAND, 0)))
    # the flight along the north wall, two wide, and the wall behind it kept
    sx = x0 + t + 1
    for k in range(4):
        for dz in (0, 1):
            x, z, y = sx + k, z0 + t + dz, P.PLATEAU + 1 + k
            for yy in range(P.PLATEAU, y):
                w.set(x, yy, z, B.SANDSTONE, 2)
            w.set(x, y, z, B.SANDSTONE_STAIRS, stair_data("e"))
            for yy in range(y + 1, y + 4):
                w.set(x, yy, z, B.AIR)
    # open the parapet where the flight meets the roof: a gap in its inner edge
    for k in range(4):
        w.set(sx + k, top + 1, z0 + t - 1, B.AIR)
    # a trough and hay for cover in the yard
    cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
    for dx in (-1, 0, 1):
        w.set(cx + dx, P.PLATEAU + 1, cz, B.SANDSTONE, 2)
        w.set(cx + dx, P.PLATEAU + 1, cz + 1, B.WATER, 0)
    for dx, dz in ((-6, -2), (-5, -2), (6, 2), (5, 2), (-3, 3), (4, -3)):
        w.set(cx + dx, P.PLATEAU + 1, cz + dz, B.HAY, 0)
        if (dx + dz) % 2:
            w.set(cx + dx, P.PLATEAU + 2, cz + dz, B.HAY, 0)


def table_rock(w, L):
    """Steps up the south face (cut into it), pillars round the top, a dais under the obelisk."""
    r = rng(P.BOARD, "table")
    ox, oz = P.OBELISK_AT
    top = P.TABLE_TOP
    # the steps: the plan's flight, drawn in the raster (both halves); lay red's
    R = P.build()
    cells = [(x, z) for x in range(P.TABLE[0] - 1, P.TABLE[0] + 2) for z in range(P.TABLE[1] - 1, P.TABLE[1] + 22)
             if R.kind(x, z) == "stair" and x < 0]
    for x, z in cells:
        y = R.h(x, z)
        for yy in range(L.H[x - w.x0, z - w.z0] - 0, y):
            w.set(x, yy, z, B.SANDSTONE, 2)
        for yy in range(y - 4, y):
            if w.id(x, yy, z) in (B.AIR, B.SAND):
                w.set(x, yy, z, B.SANDSTONE, 2)
        w.set(x, y, z, B.SANDSTONE_STAIRS, stair_data("n"))
        for yy in range(y + 1, y + 5):
            w.set(x, yy, z, B.AIR)
    # the dais under the obelisk, and six pillars round the top, three of them broken
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if max(abs(dx), abs(dz)) <= 1 or (abs(dx) + abs(dz) <= 2):
                w.set(ox + dx, top + 1, oz + dz, B.SANDSTONE, 2)
    w.set(ox, top + 1, oz, B.SANDSTONE, 1)
    for a in range(6):
        ang = a * np.pi / 3 + 0.3
        px, pz = int(round(ox + 6 * np.cos(ang))), int(round(oz + 6 * np.sin(ang)))
        if any((px, pz) == (c[0], c[1]) for c in cells):
            continue
        DS.broken_pillar(w, px, top, pz, r, h=int(r.integers(2, 6)) if a % 2 else 6)


def arch(w, L):
    """The natural arch: a three-wide deck from the stepped rock to Table Rock's top over a hollow of rock."""
    cells = P.arch_cells()
    line = shapes.spline if False else None
    from pgmvox.noise import spline
    pts = spline(P.ARCH, 0.5)
    X, Z = w.grid()
    arr = np.array(pts)
    total = float(np.sum(np.hypot(*np.diff(arr, axis=0).T)))
    r = rng(P.BOARD, "arch")
    for x, z in cells:
        d = np.hypot(arr[:, 0] - x, arr[:, 1] - z)
        j = int(np.argmin(d))
        s = j / max(1, len(arr) - 1)
        thick = 1 + int(round(5 * abs(2 * s - 1) ** 2))
        y = P.ZIGG_TOP
        w.set(x, y, z, B.SANDSTONE, 2)
        for k in range(1, thick + 1):
            if w.id(x, y - k, z) in (B.AIR, B.SAND, B.TALLGRASS):
                w.set(x, y - k, z, *((B.RED_SANDSTONE, 0) if r.random() < 0.7 else (B.SANDSTONE, 0)))
        for yy in range(y + 1, y + 5):
            if w.id(x, yy, z) not in (B.AIR,):
                w.set(x, yy, z, B.AIR)


def aqueduct(w, L):
    """The ruined aqueduct: red's half ends in a broken arch, rubble on the wash floor under it."""
    x0, z0, x1, z1 = P.ARCADE
    r = rng(P.BOARD, "arcade")
    ground = lambda x, z: int(L.H[x - w.x0, z - w.z0])              # noqa: E731
    DS.arcade(w, x0, x1, z0, z1, P.DECK_Y, ground, r, piers=[(-25, -24), (-19, -18), (-13, -12), (-7, -6)],
              ragged_end=x1)
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            if w.id(x, P.DECK_Y, z) != B.AIR and x < x1 - 1 and (x % 2 == 0):
                w.set(x, P.DECK_Y + 1, z, B.COBBLE_WALL, 0)
    for _ in range(14):
        x, z = int(r.integers(-14, -3)), int(r.integers(-4, 4))
        kit.rubble(w, x, ground(x, z), z, r, r=1.8, blocks=((B.SANDSTONE, 0), (B.SANDSTONE, 2), (B.SAND, 0)))


def underground(w, L):
    r = rng(P.BOARD, "under")
    keep = lambda x, y, z: x >= 0                                   # noqa: E731
    U.tunnel(w, P.QANAT, ground=None, keep=keep)
    cx, cy, cz = P.CISTERN
    U.chamber(w, cx, cy, cz, 5.2, 5.0, rz=5.2, ground=None, keep=keep)
    # tiles: cyan and sandstone in the cistern, a pillar at each quarter, lanterns in the roof
    for x in range(cx - 6, cx + 7):
        for z in range(cz - 6, cz + 7):
            if w.id(x, cy, z) == B.AIR and w.id(x, cy - 1, z) != B.AIR:
                w.set(x, cy - 1, z, *((B.STAINED_CLAY, 9) if (x + z) % 4 == 0 else (B.SANDSTONE, 2)))
    for dx, dz in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
        for y in range(cy, cy + 4):
            w.set(cx + dx, y, cz + dz, B.QUARTZ, 2)
        w.set(cx + dx, cy + 4, cz + dz, B.SEA_LANTERN, 0)
    # the qanat's floor: sandstone with a channel of water down one side
    for x, fy, z, rad in P.QANAT[:-1]:
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if w.id(x + dx, fy, z + dz) == B.AIR and w.id(x + dx, fy - 1, z + dz) != B.AIR:
                    w.set(x + dx, fy - 1, z + dz, *((B.SANDSTONE, 2) if r.random() < 0.7 else (B.SANDSTONE, 0)))
    U.dress_cave(w, (-66, -4, 24, 34, 44, 60), r, ground=None, keep=keep,
                 floors=((B.SANDSTONE, 2), (B.SANDSTONE, 0), (B.GRAVEL, 0)), weights=(0.4, 0.4, 0.2), mushrooms=0.0,
                 stalactites=0.02, ores=60, stalagmites=60, ore_blocks=((B.GOLD_ORE, 0.3), (B.LAPIS_ORE, 0.7)))
    # lights in the roof
    for x, fy, z, rad in P.QANAT[1:-1]:
        for y in range(fy + 1, fy + 6):
            if w.id(x, y, z) != B.AIR:
                w.set(x, y, z, B.GLOWSTONE, 0)
                break
    # the well house over the cistern's shaft
    wx, wz = P.WELL
    DS.well_house(w, wx, wz, P.PLATEAU, cy, r, door_side="e")
    # the old mine
    line = U.gallery_line(P.MINE)
    U.gallery(w, line, r, timber=(B.LOG2, 0), fence=(B.ACACIA_FENCE, 0), stair=B.SANDSTONE_STAIRS, every=4,
              rails=True, torches=10, floor=((B.SANDSTONE, 0), (B.STAINED_CLAY, 12), (B.HARDENED_CLAY, 0)), ore=None)
    sx, sz = P.MINE_SHAFT
    U.shaft(w, sx, sz, P.MINE[-1][1], P.TABLE_TOP, wall=(B.PLANKS, 4), post=(B.LOG2, 0), ladder_on="s")


def plants(w, L):
    """Palms and tamarisk round the oasis, tamarisk on the wash's rim, cacti and rubble on the plateau, a camp."""
    r = rng(P.BOARD, "plants")
    X, Z = w.grid()
    road = np.zeros(X.shape, bool)
    for m in L.road_on.values():
        road |= m
    road = ndimage.binary_dilation(road, iterations=2)
    hm = np.zeros(X.shape, bool)
    for b in P.houses().values():
        for x, z in b["cells"]:
            hm[x - w.x0, z - w.z0] = True
    ring, yard, gate = P.serai_cells()
    for x, z in ring | yard | gate:
        hm[x - w.x0, z - w.z0] = True
    hm[(X >= P.SQUARE[0] - 2) & (X <= P.SQUARE[2] + 2) & (Z >= P.SQUARE[1] - 2) & (Z <= P.SQUARE[3] + 2)] = True
    hm = ndimage.binary_dilation(hm, iterations=3)
    red = X < 0
    grove = L.grove & red & ~road & ~hm & (L.water == 0) & (L.slope < 25)
    palms = kit.scatter_points(grove, 40, 3.8, r, X, Z)
    for x, z in palms:
        DS.palm(w, x, int(L.H[x - w.x0, z - w.z0]), z, r)
    shrubs = kit.scatter_points(grove, 40, 2.6, r, X, Z, taken=palms)
    for x, z in shrubs:
        DS.tamarisk(w, x, int(L.H[x - w.x0, z - w.z0]), z, r)
    # reeds and lilies at the pond
    wet = ndimage.binary_dilation(L.water > 0, iterations=2) & (L.water == 0) & red
    for i, k in np.argwhere(wet):
        if r.random() < 0.3 and w.ids[i, int(L.H[i, k]) + 1, k] == 0:
            w.ids[i, int(L.H[i, k]) + 1, k] = B.REEDS
    for i, k in np.argwhere((L.water > 0) & red):
        if r.random() < 0.08:
            w.ids[i, int(L.water[i, k]) + 1, k] = B.LILY
    # the plateau: tamarisk on the wash's rim, cacti on the dunes, rubble, dead bushes
    free = red & ~road & ~hm & ~L.grove & (L.slope < 22) & (L.water == 0) & (L.H > P.PLATEAU - 3) & (L.H < P.PLATEAU + 7)
    free &= (np.hypot(X - P.OBELISK_AT[0], Z - P.OBELISK_AT[1]) > 12) & (np.hypot(X - P.STONE_AT[0], Z - P.STONE_AT[1]) > 12)
    rim = free & (np.abs(X + 0.5) < 30) & (np.abs(X + 0.5) > 22)
    for x, z in kit.scatter_points(rim, 12, 7, r, X, Z):
        DS.tamarisk(w, x, int(L.H[x - w.x0, z - w.z0]), z, r)
    n = 0
    for x, z in kit.scatter_points(free, 60, 6, r, X, Z):
        if DS.cactus(w, x, int(L.H[x - w.x0, z - w.z0]), z, r):
            n += 1
    for x, z in kit.scatter_points(free, 24, 8, r, X, Z):
        kit.rubble(w, x, int(L.H[x - w.x0, z - w.z0]), z, r, r=float(r.uniform(1.2, 2.2)),
                   blocks=((B.SANDSTONE, 0), (B.STAINED_CLAY, 1), (B.HARDENED_CLAY, 0), (B.SAND, 1)))
    for x, z in kit.scatter_points(free, 80, 3, r, X, Z):
        y = int(L.H[x - w.x0, z - w.z0])
        if w.id(x, y + 1, z) == B.AIR:
            w.set(x, y + 1, z, B.DEADBUSH, 0)
    # the wash's floor: boulders and dry shrubs
    wash = red & L.wash & (L.H <= P.WASH_FLOOR + 3) & ~road
    for x, z in kit.scatter_points(wash, 20, 9, r, X, Z):
        kit.rubble(w, x, int(L.H[x - w.x0, z - w.z0]), z, r, r=float(r.uniform(1.5, 2.6)),
                   blocks=((B.SANDSTONE, 0), (B.STONE, 5), (B.COBBLE, 0), (B.HARDENED_CLAY, 0)))
    # the camp at the north ghat's head: two tents and a fire pit of netherrack-free stones
    for tx, tz, along, col in ((-33, -14, "x", 3), (-30, -19, "z", 0)):
        DS.tent(w, tx, int(L.H[tx - w.x0, tz - w.z0]), tz, along, 5, col, 11)
    return len(palms), len(shrubs), n


def lamps(w, L):
    X, Z = w.grid()
    H = np.where(L.land if hasattr(L, "land") else True, L.H, 0)
    for rt in L.routes:
        if rt["kind"] == "road":
            kit.lamps(w, [tuple(p) for p in rt["line"]], H, X, Z, every=13, side=3.2, post=(B.ACACIA_FENCE, 0),
                      light=(B.SEA_LANTERN, 0))


def make():
    L = P.land()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    t0 = time.time()
    lay_ground(w, L)
    roads(w, L)
    houses(w, L)
    minaret(w, L)
    souk(w, L)
    serai(w, L)
    table_rock(w, L)
    arch(w, L)
    aqueduct(w, L)
    underground(w, L)
    n_palm, n_shrub, n_cactus = plants(w, L)
    lamps(w, L)
    turn_world(w, "mirror_x", red_cols(w), recolour={(B.CARPET, 14): (B.CARPET, 11)})
    P.objectives().stamp(w)
    w.ids[:, 0, :] = 36
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose], w.dat[:, 1:, :][loose] = B.STONE, 5
    print(f"generated in {time.time() - t0:.0f}s: {n_palm} palms, {n_shrub} tamarisk, {n_cactus} cacti")
    return w


if __name__ == "__main__":
    w = make()
    w.save(sys.argv[1], "Tamarisk Wash", (0, 100, 0))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}, {int(np.count_nonzero(w.ids))} blocks")
