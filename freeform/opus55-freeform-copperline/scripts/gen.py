"""Generate Copperline from the plan: every column built to the height the checker walked, its top and its body by
kind; the mountains round the valley, rising from the valley's edge so nothing on the board looks out over an
edge; the gorge with its broken walls, the river, a waterfall in and a cave out; the slag heap fanned out from
the old upper adit with its tramway; the track, rail by rail, with its bumpers; the trestle and the footbridge;
the town, the station, the spawn rooms; the gantry and the headframe; the adit under the mine yard; the mine
hall carved into the mountain; the cover and the dressing.

    python3 gen.py <build-dir>

Every gate is a block the match's triggers fill with air when its stage falls: iron bars across a spawn room's
door. `GATE_REGIONS` lists their boxes for map.xml.
"""
import math
import random
import sys
import time

import numpy as np
from scipy import ndimage

import house
import noise
import plan as P
from mc import World, B

R = P.build()
KN = P.KN
NX, NZ = P.NX, P.NZ
BASE_Y = 4
SY = 100
RIVER_BED, WATER_TOP = 12, 14
rng = random.Random(23)

STONE, ANDESITE, GRANITE, DIORITE = (B.STONE, 0), (B.STONE, 5), (B.STONE, 1), (B.STONE, 3)
POL_ANDESITE = (B.STONE, 6)
COBBLE, MOSSY, GRAVEL, DIRT, COARSE, PODZOL = (B.COBBLE, 0), (B.MOSSY, 0), (B.GRAVEL, 0), (B.DIRT, 0), (B.DIRT, 1), (B.DIRT, 2)
GRASS, SAND, CLAY = (B.GRASS, 0), (B.SAND, 0), (B.CLAY, 0)
SBRICK, SB_MOSSY, SB_CRACKED = (B.STONEBRICK, 0), (B.STONEBRICK, 1), (B.STONEBRICK, 2)
SPRUCE, DARK_OAK, OAK = (B.PLANKS, 1), (B.PLANKS, 5), (B.PLANKS, 0)
SPRUCE_LOG, OAK_LOG, DARK_LOG = (B.LOG, 1), (B.LOG, 0), (B.LOG2, 1)
BRICK, COAL_BLOCK = (B.BRICK, 0), (B.COAL_BLOCK, 0)
BLACK_CLAY, GREY_CLAY, BROWN_CLAY = (B.STAINED_CLAY, 15), (B.STAINED_CLAY, 7), (B.STAINED_CLAY, 12)
STAIR_DATA = {"+x": 0, "-x": 1, "+z": 2, "-z": 3}
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
RED, BLUE = 14, 11
WALKABLE = set(P.WALK) | {"gate"}


def kind(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < NX and 0 <= j < NZ):
        return "rock"
    return KN[R.K[i, j]]


def h(x, z):
    return int(R.H[P.ix(x), P.iz(z)])


def pick(choices, weights):
    return rng.choices(choices, weights)[0]


def in_box(x, z, box, m=0):
    x0, x1, z0, z1 = box
    return x0 - m <= x <= x1 + m and z0 - m <= z <= z1 + m


MOUNTAIN_ROOMS = ("mine-hall", "lamp-room")


def in_mountain_room(x, z, m=0):
    return any(in_box(x, z, P.BUILDINGS[n]["box"], m) for n in MOUNTAIN_ROOMS)


# ---- fields ------------------------------------------------------------------------------------------------
X, Z = np.meshgrid(np.arange(P.X_MIN, P.X_MAX + 1), np.arange(P.Z_MIN, P.Z_MAX + 1), indexing="ij")
N1 = noise.fbm((NX, NZ), 18, 4, seed=3)
N2 = noise.fbm((NX, NZ), 7, 3, seed=5)
N3D = noise.fbm((NX, 48, NZ), 6, 3, seed=8)                    # the gorge walls' face, y from 4 up


def shape_heap():
    """The tip is not a box: where its flat foot runs into the mountain, the mountain comes down to meet it along
    a broken line, so the spoil reads as poured out of the old adit into a corner of the valley. Only the heap's
    flat foot, away from the town, the rail yard and the office's yard, is given to the mountain."""
    heap = R.K == P.KINDS["heap"]
    other = np.isin(R.K, [P.KINDS[k] for k in ("street", "yard", "ground", "track", "bed")])
    near_other = ndimage.distance_transform_edt(~other) < 5
    n = noise.fbm((NX, NZ), 6, 3, seed=17)
    flat = heap & (R.H <= 27)
    for i, j in zip(*np.nonzero(flat & ~near_other)):
        x, z = i + P.X_MIN, j + P.Z_MIN
        dz = abs(z - P.HEAP["c"][1])
        if n[i, j] + (dz - 13) * 0.25 > 0.05:
            R.K[i, j] = P.KINDS["rock"]
            R.H[i, j] = P.ROCK


shape_heap()
HEAP_NEAR = ndimage.distance_transform_edt(R.K != P.KINDS["heap"])     # how far each column is from the tip


def ground_map():
    """What each column stands on: a walkable column its own height; a house, a cover or a wall the floor
    round it."""
    G = R.H.copy()
    walk = np.isin(R.K, [P.KINDS[k] for k in WALKABLE if k in P.KINDS])
    hw = np.where(walk, R.H, 999)
    low = ndimage.minimum_filter(hw, size=7, mode="nearest")
    for name, b in P.BUILDINGS.items():
        x0, x1, z0, z1 = b["box"]
        G[P.ix(x0):P.ix(x1) + 1, P.iz(z0):P.iz(z1) + 1] = b["floor"]
    for k in ("house", "cover"):
        m = R.K == P.KINDS[k]
        G[m] = np.where(low[m] < 999, low[m], R.H[m])
    return G


GROUND = ground_map()


def mountain_map():
    """The mountains: every rock column (and the rooms carved into the mountain) rises from the valley's edge.
    The first ring stands at least four over the highest ground beside it, so nothing walks out of the valley,
    then it climbs two to three a block, broken by noise, to a crest."""
    rock = (R.K == P.KINDS["rock"])
    for n in MOUNTAIN_ROOMS:
        x0, x1, z0, z1 = P.BUILDINGS[n]["box"]
        rock[P.ix(x0):P.ix(x1) + 1, P.iz(z0):P.iz(z1) + 1] = True
    d, (ni, nj) = ndimage.distance_transform_edt(rock, return_indices=True)
    valley = np.where(~rock, GROUND, 0)
    gmax = np.maximum(ndimage.maximum_filter(valley, size=17, mode="nearest"), valley[ni, nj])
    edge = np.minimum.reduce([X - P.X_MIN, P.X_MAX - X, Z - P.Z_MIN, P.Z_MAX - Z]).astype(float)
    rise = 3.4 * (d - 1) + 8 * N1 + 3 * N2 + 14 * np.clip(1 - edge / 10.0, 0, 1)
    Hm = gmax + 5 + np.maximum(1.5 * d, rise)
    Hm = np.minimum(Hm, 90 + 4 * N2)
    Hm[d >= 1] = np.maximum(Hm[d >= 1], gmax[d >= 1] + 4)
    # the mountain over the mine stands well over its rooms; the upper adit's face stands over the heap
    room = np.zeros_like(rock)
    for n in MOUNTAIN_ROOMS:
        x0, x1, z0, z1 = P.BUILDINGS[n]["box"]
        room[P.ix(x0 - 3):P.ix(x1 + 3) + 1, P.iz(z0 - 3):P.iz(z1) + 1] = True
    Hm[room] = np.maximum(Hm[room], 52)
    Hm[P.ix(50):, P.iz(-18):P.iz(-2) + 1] = np.maximum(Hm[P.ix(50):, P.iz(-18):P.iz(-2) + 1], 50)   # over the falls
    x1 = P.HEAP["box"][1]
    Hm[P.ix(x1 + 1):, P.iz(P.HEAP["c"][1] - 6):P.iz(P.HEAP["c"][1] + 6) + 1] = np.maximum(
        Hm[P.ix(x1 + 1):, P.iz(P.HEAP["c"][1] - 6):P.iz(P.HEAP["c"][1] + 6) + 1], 46)
    return np.where(rock, np.round(Hm).astype(int), -1), d


MOUNT, MDIST = mountain_map()


# ---- the ground ------------------------------------------------------------------------------------------
def rock_mat(y, x, z):
    """The mountain's body: grey stone with bands of andesite and granite, and ore here and there."""
    band = (y + int(3 * N2[P.ix(x), P.iz(z)])) % 11
    r = rng.random()
    if r < 0.012:
        return (B.COAL_ORE, 0)
    if r < 0.016:
        return (B.IRON_ORE, 0)
    if band in (3, 4):
        return ANDESITE
    if band == 8:
        return GRANITE
    return STONE


def top_mat(k, x, z):
    n = N2[P.ix(x), P.iz(z)]
    if k == "yard":
        if z > 0:   # the rail yard: cinders and gravel
            return pick([GRAVEL, COARSE, COBBLE, ANDESITE, BLACK_CLAY], [35, 25, 15, 15, 10])
        return pick([GRAVEL, COARSE, COBBLE, STONE, DIRT], [30, 30, 15, 15, 10])           # the mine yard
    if k == "street":
        return pick([COBBLE, ANDESITE, GRAVEL, STONE, MOSSY], [40, 25, 15, 10, 10])
    if k == "ground":
        if n > 0.35:
            return COARSE
        if n < -0.45:
            return PODZOL
        return GRASS
    if k in ("track", "bed"):
        return pick([GRAVEL, GRAVEL, ANDESITE, COBBLE], [50, 20, 20, 10])
    if k == "heap":
        return pick([COAL_BLOCK, BLACK_CLAY, GREY_CLAY, GRAVEL, COBBLE], [15, 35, 25, 15, 10])
    if k == "platform":
        return POL_ANDESITE
    if k in ("floor", "gate"):
        return SPRUCE
    if k == "river":
        return pick([GRAVEL, SAND, CLAY, GRAVEL], [40, 30, 15, 15])
    return STONE


def body_mat(k, y, x, z):
    if k == "heap":
        return pick([BLACK_CLAY, GREY_CLAY, GRAVEL, COAL_BLOCK], [40, 30, 20, 10])
    if k in ("track", "bed") and y > 26:
        return pick([COBBLE, SBRICK, SB_MOSSY, SB_CRACKED], [40, 30, 15, 15])        # the shelf's embankment
    if k == "ground" and y >= h(x, z) - 2:
        return DIRT
    return rock_mat(y, x, z)


def columns(w):
    for i in range(NX):
        for j in range(NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, hh = KN[R.K[i, j]], int(R.H[i, j])
            if MOUNT[i, j] >= 0:
                top = MOUNT[i, j]
                for y in range(BASE_Y, top + 1):
                    w.set(x, y, z, *rock_mat(y, x, z))
                if HEAP_NEAR[i, j] <= 4 + 3 * N2[i, j] and top < 44:     # spoil poured over the mountain's foot
                    for y in range(top - 2, top + 1):
                        w.set(x, y, z, *top_mat("heap", x, z))
                    continue
                steep = MDIST[i, j] < 3 or abs(N2[i, j]) > 0.5
                if top > 80:
                    w.set(x, top + 1, z, B.SNOW_LAYER, 1)
                elif not steep and top < 76:
                    w.set(x, top, z, *GRASS)
                    w.set(x, top - 1, z, *DIRT)
                continue
            if k == "river":
                for y in range(BASE_Y, RIVER_BED):
                    w.set(x, y, z, *rock_mat(y, x, z))
                w.set(x, RIVER_BED, z, *top_mat(k, x, z))
                for y in range(RIVER_BED + 1, WATER_TOP + 1):
                    w.set(x, y, z, B.WATER)
                continue
            if k == "stair":
                for y in range(BASE_Y, hh):
                    w.set(x, y, z, *(rock_mat(y, x, z) if y < hh - 2 else COBBLE))
                w.set(x, hh, z, B.COBBLE_STAIRS, STAIR_DATA[R.stair[(x, z)]])
                if hh < WATER_TOP:
                    for y in range(hh + 1, WATER_TOP + 1):
                        w.set(x, y, z, B.WATER)
                continue
            g = int(GROUND[i, j])
            for y in range(BASE_Y, g):
                w.set(x, y, z, *body_mat(k, y, x, z))
            if k in ("house", "cover", "wall", "bumper"):
                w.set(x, g, z, *(top_mat("street", x, z) if g == 26 else GRAVEL))
            else:
                w.set(x, g, z, *top_mat(k, x, z))
            if k == "heap" and rng.random() < 0.06:
                w.set(x, g + 1, z, B.DEADBUSH)
            if k == "ground" and w.id(x, g, z) == B.GRASS:
                r = rng.random()
                if r < 0.22:
                    w.set(x, g + 1, z, B.TALLGRASS, 1 if r < 0.17 else 2)
                elif r < 0.235:
                    w.set(x, g + 1, z, B.FLOWER, pick([0, 3, 8], [1, 1, 1]))


# ---- the gorge -----------------------------------------------------------------------------------------
KEEP_GORGE = [(-1, 5), (-19, -2), (10, 22), (-29, -22)]          # x ranges kept straight: ladder, stair, bridges


def gorge(w):
    """Break the gorge's walls: alcoves cut into the face and bulges out of it, scree at the foot, all below the
    top two courses so the bank a player stands on is as planned; a waterfall at its east end, a cave at its west."""
    for i in range(NX):
        x = i + P.X_MIN
        if any(a <= x <= b for a, b in KEEP_GORGE):
            continue
        for z0, side in ((-4, 1), (-20, -1)):                        # the river's edge rows, and which way is bank
            bank_z = z0 + side
            if kind(x, bank_z) == "rock" or kind(x, z0) != "river":
                continue
            top = h(x, bank_z)
            for y in range(RIVER_BED + 1, top - 1):
                n = N3D[i, y - BASE_Y, P.iz(z0)]
                if n > 0.32:                                          # an alcove into the bank
                    w.set(x, y, bank_z, *(B.WATER, 0) if y <= WATER_TOP else (B.AIR, 0))
                    if n > 0.5:
                        w.set(x, y, bank_z + side, *(B.WATER, 0) if y <= WATER_TOP else (B.AIR, 0))
                elif n < -0.3:                                        # a bulge out of it
                    w.set(x, y, z0, *rock_mat(y, x, z0))
                    if n < -0.48 and y > WATER_TOP + 2:
                        w.set(x, y, z0 - side, *rock_mat(y, x, z0))
            if N2[i, P.iz(bank_z)] > 0.3:                              # a bite out of the lip, to the top
                deep = 1 + int(N2[i, P.iz(bank_z)] > 0.5)
                for k in range(deep):
                    zz = bank_z + side * k
                    for y in range(RIVER_BED + 1, top + 3):
                        w.set(x, y, zz, *(B.WATER, 0) if y <= WATER_TOP else (B.AIR, 0))
            for dz in (0, 1):                                         # scree at the foot
                zz = z0 - side * dz
                tall = int(max(0, 3.5 * N2[i, P.iz(zz)] + 1.5 - 1.5 * dz))
                for y in range(RIVER_BED + 1, RIVER_BED + 1 + tall):
                    w.set(x, y, zz, *pick([COBBLE, GRAVEL, STONE, MOSSY], [30, 30, 25, 15]))
    # the waterfall at the east end: a notch in the cliff, a fall of water into the river
    top = 42                                                       # a slot in the cliff, roofed: no way out up it
    for y in range(RIVER_BED + 1, top + 1):
        for z in (-13, -12, -11):
            w.set(52, y, z, B.AIR)
            w.set(53, y, z, B.AIR)
        w.set(52, y, -12, B.WATER_FLOW, 8)
    for z in (-13, -12, -11):
        w.set(53, top, z, B.WATER)
        w.set(53, top - 1, z, B.STONE)
    w.set(52, top, -12, B.WATER)
    # the cave at the west end: the river runs into the mountain under a low arch
    for x in range(-55, -50):
        for z in range(-15, -8):
            for y in range(RIVER_BED + 1, RIVER_BED + 5):
                w.set(x, y, z, B.WATER if y <= WATER_TOP else B.AIR)
    for z in range(-15, -8):
        for y in range(RIVER_BED + 1, RIVER_BED + 5):
            w.set(-53, y, z, B.IRON_BARS)


# ---- the slag heap and the old upper adit ----------------------------------------------------------------
def upper_adit(w):
    """The heap's source: an adit mouth in the mountain at the heap's back, timbered, with the tramway that tipped
    the spoil running out of it along the heap's crest to a buffer and a tub on its side."""
    cz, top = P.HEAP["c"][1], 34
    x_face = P.HEAP["box"][1] + 1
    for x in range(x_face, x_face + 4):
        for z in range(cz - 1, cz + 2):
            for y in range(top + 1, top + 4):
                w.set(x, y, z, B.AIR)
            w.set(x, top, z, *GRAVEL)
        w.set(x, top + 1, cz, B.RAIL, 1)
    for z in (cz - 2, cz + 2):
        for y in range(top + 1, top + 5):
            w.set(x_face, y, z, *SPRUCE_LOG)
    for z in range(cz - 2, cz + 3):
        w.set(x_face, top + 4, z, B.LOG, 1 | 8)
    for z in range(cz - 1, cz + 2):
        for y in range(top + 1, top + 4):
            w.set(x_face + 4, y, z, B.IRON_BARS)
    w.set(x_face + 1, top + 3, cz - 1, B.COBWEB)
    w.set(x_face + 2, top + 3, cz + 1, B.COBWEB)
    w.set(x_face - 1, top + 3, cz - 2, B.TORCH, 4)
    # the tramway: rails out along the crest, on sleepers, to a buffer at the tip's edge
    x_end = P.HEAP["c"][0] - 4
    for x in range(x_end + 1, x_face):
        y = w.top(x, cz)
        w.set(x, y, cz, *SPRUCE)
        w.set(x, y + 1, cz, B.RAIL, 1)
    y = w.top(x_end, cz)
    w.set(x_end, y + 1, cz, *SPRUCE_LOG)
    w.set(x_end, y + 2, cz, B.FENCE)
    w.set(x_end + 1, w.top(x_end + 1, cz + 1) + 1, cz + 1, B.CAULDRON)        # a tub, tipped off the rails
    # spoil spilled down the heap's face from the tip
    for _ in range(40):
        x = rng.randint(P.HEAP["c"][0] - 12, x_end)
        z = cz + rng.randint(-3, 3)
        y = w.top(x, z)
        if kind(x, z) == "heap" and w.id(x, y + 1, z) == 0:
            w.set(x, y + 1, z, B.CARPET, 15)


# ---- the track -------------------------------------------------------------------------------------------
def track(w):
    for leg in P.LEGS:
        for x, z, hh, d in P.lay(leg):
            if R.U[P.ix(x), P.iz(z)] < 0:
                w.set(x, hh, z, *pick([GRAVEL, GRAVEL, COBBLE], [3, 1, 1]))
            w.set(x, hh + 1, z, B.RAIL, d)
            for y in range(hh + 2, hh + 5):
                if w.id(x, y, z) not in (0, B.RAIL):
                    w.set(x, y, z, B.AIR)
    stops = list(P.BUMPERS)
    a = P.lay(P.LEGS[0])[0]
    stops.append((a[0], a[1] + 1, a[2]))                           # behind the line's start
    c = P.lay(P.LEGS[-1])[-1]
    stops.append((c[0], c[1] - 1, c[2]))                           # past its end, in the mine hall
    for x, z, hh in stops:
        w.set(x, hh, z, *GRAVEL)
        w.set(x, hh + 1, z, *SPRUCE_LOG)                           # a buffer stop: a timber beam on posts
        w.set(x, hh + 2, z, B.WOOL, RED)


def trestle(w):
    t = P.TRESTLE
    y = t["h"]
    for x in range(t["x0"], t["x1"] + 1):
        for z in range(t["z0"], t["z1"] + 1):
            w.set(x, y, z, *SPRUCE)
    for z in range(t["z0"], t["z1"] + 1):
        w.set(t["x0"], y + 1, z, B.SPRUCE_FENCE)
        w.set(t["x1"], y + 1, z, B.SPRUCE_FENCE)
        for x in (t["x0"] + 1, t["x1"] - 1):
            w.set(x, y - 1, z, B.LOG, 1 | 8)                       # stringers under the deck
    for z in range(t["z0"] + 2, t["z1"] - 1, 4):                   # the bents: posts from the river bed
        for x in (t["x0"], (t["x0"] + t["x1"]) // 2, t["x1"]):
            for yy in range(RIVER_BED + 1, y):
                w.set(x, yy, z, *SPRUCE_LOG)
        for x in range(t["x0"], t["x1"] + 1):
            w.set(x, y - 1, z, B.LOG, 1 | 4)                       # the cap
            w.set(x, y - 6, z, B.LOG, 1 | 4)                       # a waling well above the water
        for k in range(1, 5):                                      # cross braces between the posts
            for x in (t["x0"] + k, t["x1"] - k):
                w.set(x, y - 1 - k, z, B.SPRUCE_FENCE)
    f = P.FOOTBRIDGE
    for z in range(f["z0"], f["z1"] + 1):
        for x in range(f["x0"] - 1, f["x1"] + 2):
            w.set(x, f["h"], z, *(SPRUCE if f["x0"] <= x <= f["x1"] else DARK_OAK))
        w.set(f["x0"] - 1, f["h"] + 1, z, B.FENCE)
        w.set(f["x1"] + 1, f["h"] + 1, z, B.FENCE)
    zc = (f["z0"] + f["z1"]) // 2
    for x in range(f["x0"] - 1, f["x1"] + 2):
        for z in (zc, zc + 1):
            for yy in range(RIVER_BED + 1, f["h"]):
                w.set(x, yy, z, *pick([COBBLE, STONE, MOSSY], [4, 4, 2]))


def north_ladder(w):
    (x, za), (_, zb) = P.CONNECTORS[0][2], P.CONNECTORS[0][3]
    top = h(x, zb)
    for y in range(RIVER_BED + 1, top + 1):
        w.set(x, y, za - 1, *rock_mat(y, x, za - 1))               # the cliff behind it, solid
        w.set(x, y, za, B.LADDER, 3)
    w.set(x - 1, top + 1, zb, B.FENCE)
    w.set(x + 1, top + 1, zb, B.FENCE)
    w.set(x - 1, top + 2, zb, B.TORCH, 5)


# ---- buildings -----------------------------------------------------------------------------------------
GATE_REGIONS = {}                                                # stage -> boxes (x0, y0, z0, x1, y1, z1)
for _b in P.BUILDINGS.values():
    for _dx0, _dx1, _dz0, _dz1, _st in _b["doors"]:
        if _st:
            GATE_REGIONS.setdefault(_st, []).append((_dx0, _b["floor"] + 1, _dz0, _dx1, _b["floor"] + 4, _dz1))
STYLE = {"engine-shed": (BRICK, DARK_OAK), "station": (BRICK, DARK_OAK), "depot": (SPRUCE, DARK_OAK),
         "office": (SBRICK, DARK_OAK), "bunkhouse": (SPRUCE, DARK_OAK)}


def building(w, name, b):
    x0, x1, z0, z1 = b["box"]
    f = b["floor"]
    wall, roof = STYLE[name]
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            w.set(x, f, z, *(SBRICK if ring else (SPRUCE if (x + z) % 5 else DARK_OAK)))
            for y in range(f + 1, f + 9):
                w.set(x, y, z, B.AIR)
            if ring:
                corner = x in (x0, x1) and z in (z0, z1)
                post = corner or (wall == SPRUCE and ((x - x0) % 4 == 0 if z in (z0, z1) else (z - z0) % 4 == 0))
                for y in range(f + 1, f + 8):
                    blk = SPRUCE_LOG if post else (DARK_LOG if y == f + 7 and wall == SPRUCE else wall)
                    run = (x - x0) if z in (z0, z1) else (z - z0)
                    if not corner and y in (f + 3, f + 4) and run % 3 == 1 and not post:
                        blk = (B.PANE, 0)
                    w.set(x, y, z, *blk)
    # the roof: a gable along the long side, dark planks stepped up a block a block, the gable ends in the wall
    along_x = (x1 - x0) >= (z1 - z0)
    half = ((z1 - z0) if along_x else (x1 - x0)) / 2.0
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            v = abs((z - (z0 + z1) / 2.0) if along_x else (x - (x0 + x1) / 2.0))
            y = f + 8 + int(max(0, half + 1 - v) * 0.7)
            end = (x in (x0, x1)) if along_x else (z in (z0, z1))
            inside_end = x0 <= x <= x1 and z0 <= z <= z1
            w.set(x, y, z, *roof)
            if end and inside_end:
                for yy in range(f + 8, y):
                    w.set(x, yy, z, *wall)
    # doors: the plan's door cells, opened four high; a gate's opening is barred until its stage
    for dx0, dx1, dz0, dz1, st in b["doors"]:
        for x in range(dx0, dx1 + 1):
            for z in range(dz0, dz1 + 1):
                w.set(x, f, z, *SPRUCE)
                for y in range(f + 1, f + 5):
                    w.set(x, y, z, *((B.IRON_BARS, 0) if st else (B.AIR, 0)))
        lx0, lx1, lz0, lz1 = dx0 - (dx0 == dx1 and 0), dx1, dz0, dz1
        for x in range(lx0, lx1 + 1):
            for z in range(lz0, lz1 + 1):
                w.set(x, f + 5, z, B.LOG, 1 | (8 if dx0 == dx1 else 4))   # a lintel over the opening


def buildings(w):
    for name, b in P.BUILDINGS.items():
        if name not in MOUNTAIN_ROOMS:
            building(w, name, b)
    # the engine in the shed: a locomotive on its own short road, cab to the west
    x0, x1, z0, z1 = P.BUILDINGS["engine-shed"]["box"]
    zc = (z0 + z1) // 2 + 2
    f = 24
    for x in range(x0 + 2, x1 - 1):
        w.set(x, f + 1, zc, B.RAIL, 1)
    for x in range(x0 + 4, x0 + 15):
        for z in (zc - 1, zc, zc + 1):
            w.set(x, f + 2, z, *COAL_BLOCK)
        if x < x0 + 8:
            for z in (zc - 1, zc + 1):
                for y in (f + 3, f + 4):
                    w.set(x, y, z, *COAL_BLOCK if y == f + 3 else (B.PANE, 0))
            for z in (zc - 1, zc, zc + 1):
                w.set(x, f + 5, z, B.WOOL, 15)
        else:
            for z in (zc - 1, zc, zc + 1):
                w.set(x, f + 3, z, B.WOOL, 15 if z != zc else 14)
                w.set(x, f + 4, z, *(COAL_BLOCK if z == zc else (B.AIR, 0)))
    w.set(x0 + 13, f + 5, zc, B.COBBLE_WALL)
    w.set(x0 + 13, f + 6, zc, B.COBBLE_WALL)
    w.set(x0 + 14, f + 3, zc, *(B.IRON_BLOCK, 0))
    for x in (x0 + 5, x0 + 9, x0 + 12):
        for z in (zc - 2, zc + 2):
            w.set(x, f + 1, z, *COAL_BLOCK)                         # the wheels
    # the spawn rooms' floors in the team's colour
    for name, team in (("engine-shed", RED), ("station", RED), ("depot", RED), ("office", BLUE), ("bunkhouse", BLUE),
                       ("lamp-room", BLUE)):
        bx0, bx1, bz0, bz1 = P.BUILDINGS[name]["box"]
        fl = P.BUILDINGS[name]["floor"]
        for x in range(bx0 + 2, bx1 - 1):
            for z in range(bz0 + 2, bz1 - 1):
                if (x + z) % 3 == 0 and w.id(x, fl + 1, z) == 0:
                    w.set(x, fl + 1, z, B.CARPET, team)


def houses(w):
    for n, (x0, x1, z0, z1) in enumerate(P.HOUSES):
        f = int(GROUND[P.ix(x0), P.iz(z0)])
        spec = dict(cx=(x0 + x1 + 1) / 2, cz=(z0 + z1 + 1) / 2, heading=0 if (x1 - x0) >= (z1 - z0) else 90,
                    L=max(x1 - x0, z1 - z0) + 1, W=min(x1 - x0, z1 - z0) + 1, floor=f,
                    storeys=2, style=["town", "plaster", "brick"][n % 3], door=1 if n % 2 else -1)
        house.build(w, spec, ground_at=lambda x, z: f, rng=np.random.default_rng(n + 31))


def station(w):
    """The platforms' edges, and a canopy on posts over both and the line between them."""
    for x0, x1 in ((-18, -16), (-8, -6)):
        for z in range(12, 30):
            for x in range(x0, x1 + 1):
                w.set(x, 27, z, *(POL_ANDESITE if x in (-16, -8) else (B.STONE, 4)))
    for z in (13, 18, 23, 28):
        for x in (-17, -7):
            for y in range(28, 32):
                w.set(x, y, z, B.FENCE if y < 31 else B.DARK_OAK_FENCE)
    for x in range(-19, -4):
        for z in range(11, 31):
            w.set(x, 32, z, B.WOOD_SLAB, 5 if (x + 19) % 7 else 1)
    for z in (15, 21, 26):
        w.set(-17, 31, z, B.GLOWSTONE)
        w.set(-7, 31, z, B.GLOWSTONE)
    w.sign(-17, 28, 20, ["", "COPPERLINE", "station", ""], rot=4)


# ---- the gantry, the headframe ----------------------------------------------------------------------------
GANTRY_Y = 42


def gantry(w):
    """A timber tower on the north bank, a ladder up its middle, a walkway on trestles over the shelf, and the
    headframe in the mine yard with its sheave wheel and a ladder down."""
    y = GANTRY_Y
    (ax, az), (bx, bz) = P.CONNECTORS[1][2], P.CONNECTORS[1][3]
    # the tower
    for x in (2, 6):
        for z in (-32, az):
            for yy in range(29, y):
                w.set(x, yy, z, *SPRUCE_LOG)
    for x in range(2, 7):
        for z in range(-32, az + 1):
            w.set(x, y, z, *SPRUCE)
    for yy in range(29, y + 2):
        w.set(ax, yy, az - 1, *SPRUCE_LOG)                         # the ladder's back
    for yy in range(29, y + 2):
        w.set(ax, yy, az, B.LADDER, 3)
    for k in range(29, y, 4):                                      # braces round the tower
        for x in range(2, 7):
            w.set(x, k + 2, -32, B.SPRUCE_FENCE)
        for z in range(-32, az + 1):
            w.set(2, k + 2, z, B.SPRUCE_FENCE)
            w.set(6, k + 2, z, B.SPRUCE_FENCE)
    # the walkway
    for z in range(-49, -32):
        for x in range(3, 6):
            w.set(x, y, z, *SPRUCE)
        w.set(2, y, z, *DARK_OAK)
        w.set(6, y, z, *DARK_OAK)
        w.set(2, y + 1, z, B.SPRUCE_FENCE)
        w.set(6, y + 1, z, B.SPRUCE_FENCE)
    for z in (-35, -42):
        for x in (2, 6):
            g = w.top(x, z)
            for yy in range(g + 1, y):
                w.set(x, yy, z, *SPRUCE_LOG)
    # the headframe
    hx0, hx1, hz0, hz1 = 1, 7, -57, -50
    for x in (hx0, hx1):
        for z in (hz0, hz1):
            for yy in range(37, 53):
                w.set(x, yy, z, *SPRUCE_LOG)
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            w.set(x, y, z, *SPRUCE)
        for z in (hz0, hz1):
            w.set(x, 53, z, B.LOG, 1 | 4)
    for z in range(hz0, hz1 + 1):
        for x in (hx0, hx1):
            w.set(x, 53, z, B.LOG, 1 | 8)
            if z not in (hz0, hz1) and z != bz:
                w.set(x, y + 1, z, B.SPRUCE_FENCE)
    for x in range(hx0 + 1, hx1):
        w.set(x, y + 1, hz0, B.SPRUCE_FENCE)
    w.set(bx, y, bz, B.AIR)                                        # the hole the ladder comes up through
    for yy in range(37, y + 2):
        w.set(bx, yy, bz - 1, *SPRUCE_LOG)
        w.set(bx, yy, bz, B.LADDER, 3)
    cx, cy, cz = 4, 57, -53                                        # the sheave wheel, in the x-y plane
    for a in range(0, 360, 8):
        t = math.radians(a)
        w.set(cx + int(round(3.4 * math.cos(t))), cy + int(round(3.4 * math.sin(t))), cz, *DARK_LOG)
    for yy in range(53, cy + 1):
        w.set(cx, yy, cz, B.DARK_OAK_FENCE)
    w.set(cx, cy, cz, *(B.IRON_BLOCK, 0))
    for yy in range(37, cy - 3):                                   # the cable down the shaft
        w.set(cx, yy, cz, B.FENCE)
    for x in range(cx - 1, cx + 2):                                # the shaft's collar, fenced
        for z in range(cz - 1, cz + 2):
            if (x, z) != (cx, cz):
                w.set(x, 37, z, B.FENCE)
            w.set(x, 36, z, *SBRICK)


# ---- the adit and the mine ----------------------------------------------------------------------------------
ADIT = [(-16, -36, 28), (-16, -50, 28), (-30, -50, 28), (-30, -58, 32), (-30, -63, 36)]


def adit_cells():
    """The drift's centre line, a cell at a time, with its floor: flat, then climbing one in two under the yard,
    one a cell into the mountain, up into the mine hall's floor."""
    out = []
    for (x0, z0, f0), (x1, z1, f1) in zip(ADIT, ADIT[1:]):
        n = abs(x1 - x0) + abs(z1 - z0)
        for k in range(n):
            t = k / n
            out.append((x0 + round((x1 - x0) * t), z0 + round((z1 - z0) * t), int(round(f0 + (f1 - f0) * t))))
    out.append(ADIT[-1])
    return out


def adit(w):
    cells = adit_cells()
    for n, (x, z, f) in enumerate(cells):
        prev = cells[max(0, n - 1)]
        nxt = cells[min(len(cells) - 1, n + 1)]
        along_x = abs(nxt[0] - prev[0]) > abs(nxt[1] - prev[1])
        for o in range(-2, 3):
            px, pz = (x, z + o) if along_x else (x + o, z)
            w.set(px, f, pz, *GRAVEL)
            for y in range(f + 1, f + 5):
                if w.id(px, y, pz) != B.RAIL:
                    w.set(px, y, pz, B.AIR)
        if n % 4 == 0:                                             # a timber set: two legs and a cap
            for o in (-2, 2):
                px, pz = (x, z + o) if along_x else (x + o, z)
                for y in range(f + 1, f + 4):
                    w.set(px, y, pz, *SPRUCE_LOG)
            for o in range(-2, 3):
                px, pz = (x, z + o) if along_x else (x + o, z)
                w.set(px, f + 4, pz, B.LOG, 1 | (8 if along_x else 4))
            if n % 8 == 0:                                         # a lamp in every other cap
                w.set(x, f + 4, z, B.GLOWSTONE)
        # an old line down the drift's middle, broken here and there
        if rng.random() > 0.15 and f == cells[min(len(cells) - 1, n + 1)][2] == prev[2]:
            w.set(x, f + 1, z, B.RAIL, 1 if along_x else 0)
    # the portal in the shelf's face: a timber frame and a sign
    x, z, f = ADIT[0]
    for o in (-2, 2):
        for y in range(f + 1, f + 5):
            w.set(x + o, y, z, *SPRUCE_LOG)
    for o in range(-3, 4):
        w.set(x + o, f + 5, z, B.LOG, 1 | 4)
    w.sign(x + 3, f + 1, z + 1, ["", "No. 3 ADIT", "keep out", ""], rot=0)


def mine(w):
    """The mine hall and the lamp room, carved into the mountain; timber sets down the hall; ore in its walls; the
    portal over the line's end; the lamp room's door to the yard."""
    for name in MOUNTAIN_ROOMS:
        x0, x1, z0, z1 = P.BUILDINGS[name]["box"]
        f = P.BUILDINGS[name]["floor"]
        for x in range(x0 + 1, x1):
            for z in range(z0 + 1, z1):
                w.set(x, f, z, *pick([GRAVEL, STONE, COBBLE, ANDESITE], [35, 30, 20, 15]))
                ceil = f + 7 + int(1.6 * (N2[P.ix(x), P.iz(z)] + 0.6))
                for y in range(f + 1, ceil + 1):
                    w.set(x, y, z, B.AIR)
        for x in range(x0, x1 + 1):                                # ore showing in the walls
            for z in range(z0, z1 + 1):
                if x0 < x < x1 and z0 < z < z1:
                    continue
                for y in range(f + 1, f + 9):
                    r = rng.random()
                    if r < 0.06:
                        w.set(x, y, z, B.COAL_ORE)
                    elif r < 0.09:
                        w.set(x, y, z, B.IRON_ORE)
                    elif r < 0.1:
                        w.set(x, y, z, B.GOLD_ORE)
        for zz in range(z0 + 2, z1 - 1, 4):                        # timber sets across the room
            for x in (x0 + 1, x1 - 1):
                for y in range(f + 1, f + 7):
                    w.set(x, y, zz, *SPRUCE_LOG)
            for x in range(x0 + 1, x1):
                w.set(x, f + 7, zz, B.LOG, 1 | 4)
            for x in range(x0 + 4, x1 - 3, 6):
                w.set(x, f + 6, zz, B.FENCE)
                w.set(x, f + 5, zz, B.GLOWSTONE)
        for dx0, dx1, dz0, dz1, st in P.BUILDINGS[name]["doors"]:  # the portals
            for x in range(dx0, dx1 + 1):
                for z in range(dz0 - 1, dz1 + 2):
                    for y in range(f + 1, f + 6):
                        w.set(x, y, z, B.AIR)
                    w.set(x, f, z, *GRAVEL)
            for x in (dx0 - 1, dx1 + 1):
                for y in range(f + 1, f + 7):
                    w.set(x, y, dz0, *SPRUCE_LOG)
            for x in range(dx0 - 2, dx1 + 3):
                w.set(x, f + 6, dz0, B.LOG, 1 | 4)
                w.set(x, f + 7, dz0, *SPRUCE)
    w.sign(-17, 38, -58, ["", "COPPERLINE", "MINING CO.", "No. 1 level"], rot=0)
    w.sign(5, 38, -58, ["", "LAMP ROOM", "", ""], rot=0)
    # the tubs waiting at the end of the line, and ore heaped by the wall
    for x, z in ((-16, -64), (-16, -68), (-24, -66)):
        w.set(x, 37, z, B.CAULDRON)
    for x in range(-30, -22):
        for z in range(-70, -68):
            if rng.random() < 0.6:
                w.set(x, 37, z, *pick([(B.COAL_ORE, 0), (B.IRON_ORE, 0), GRAVEL], [3, 2, 2]))


# ---- cover, dressing --------------------------------------------------------------------------------------
def wagon(w, x0, x1, z0, z1, g):
    along_x = (x1 - x0) >= (z1 - z0)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            end = (x in (x0, x1)) if along_x else (z in (z0, z1))
            w.set(x, g + 1, z, *(COAL_BLOCK if end else (B.FENCE, 0)))
            w.set(x, g + 2, z, *(SPRUCE if (x + z) % 2 else DARK_OAK))
            if rng.random() < 0.6:
                w.set(x, g + 3, z, *COAL_BLOCK)


def crates(w, x0, x1, z0, z1, g, tall):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(g + 1, g + 1 + tall):
                if y == g + tall and rng.random() < 0.35:
                    continue
                w.set(x, y, z, *pick([SPRUCE, SPRUCE_LOG, OAK, (B.HAY, 0)], [4, 2, 2, 1]))


def coal_stack(w, x0, x1, z0, z1, g, tall):
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            edge = not (x0 <= x <= x1 and z0 <= z <= z1)
            if edge and rng.random() < 0.5:
                continue
            t = 1 if edge else tall
            gg = w.top(x, z)
            if kind(x, z) not in WALKABLE | {"cover"} or kind(x, z) in ("track", "bed"):
                continue
            for y in range(gg + 1, gg + 1 + t):
                w.set(x, y, z, *pick([COAL_BLOCK, COAL_BLOCK, (B.COAL_ORE, 0)], [3, 2, 1]))


def boulder(w, x0, x1, z0, z1, g, tall):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(g + 1, g + 1 + tall):
                w.set(x, y, z, *pick([STONE, COBBLE, MOSSY, ANDESITE], [4, 3, 1, 2]))


def ore_bin(w, x0, x1, z0, z1, g, tall):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            for y in range(g + 1, g + 1 + tall):
                w.set(x, y, z, *(SPRUCE_LOG if edge and (x in (x0, x1) and z in (z0, z1)) else
                                 SPRUCE if edge else pick([(B.IRON_ORE, 0), (B.COAL_ORE, 0), GRAVEL], [2, 2, 1])))


def cover(w):
    for x0, x1, z0, z1, tall in P.COVER:
        g = int(GROUND[P.ix(x0), P.iz(z0)])
        if z0 >= 54:
            wagon(w, x0, x1, z0, z1, g)
        elif z0 >= 8:
            crates(w, x0, x1, z0, z1, g, tall)
        elif z0 >= -3:
            coal_stack(w, x0, x1, z0, z1, g, tall)
        elif z0 >= -36:
            crates(w, x0, x1, z0, z1, g, tall)
        elif tall >= 3:
            ore_bin(w, x0, x1, z0, z1, g, tall)
        else:
            boulder(w, x0, x1, z0, z1, g, tall)
    # the water tower on the north bank
    x, z = P.WATER_TOWER
    for dx in (-1, 1):
        for dz in (-1, 1):
            for y in range(29, 35):
                w.set(x + dx, y, z + dz, *SPRUCE_LOG)
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) == 2 and abs(dz) == 2:
                continue
            w.set(x + dx, 35, z + dz, *SPRUCE)
            for y in range(36, 40):
                rim = abs(dx) == 2 or abs(dz) == 2
                w.set(x + dx, y, z + dz, *(SPRUCE if rim else (B.WATER, 0)))
                if rim and y in (37, 39):
                    w.set(x + dx, y, z + dz, B.LOG, 1 | (4 if abs(dz) == 2 else 8))
            w.set(x + dx, 40, z + dz, B.WOOD_SLAB, 5)
    w.set(x, 41, z, B.WOOD_SLAB, 5)
    for y in range(31, 35):
        w.set(x + 2, y, z, B.DARK_OAK_FENCE)                        # the spout


def lamps(w):
    """Lamp posts down Main Street and Station Road and along the brow, clear of the line."""
    spots = [(5, z) for z in range(37, 53, 5)] + [(11, z) for z in range(39, 53, 5)] + \
            [(x, 31) for x in range(-30, 12, 7)] + [(x, 9) for x in (-30, -20, 0, 20)] + [(x, -1) for x in (-40, -20, 10, 30)]
    for x, z in spots:
        if kind(x, z) not in ("street", "ground") or w.id(x, h(x, z) + 1, z) != 0:
            continue
        g = h(x, z)
        for y in range(g + 1, g + 4):
            w.set(x, y, z, B.DARK_OAK_FENCE)
        w.set(x, g + 4, z, B.GLOWSTONE)
        w.set(x, g + 5, z, B.WOOD_SLAB, 5)


def keep_mask():
    """Where nothing grows: the track and two either side, the buildings and a margin, the connectors' ends, the
    stairs, the bridges' ends."""
    m = np.isin(R.K, [P.KINDS[k] for k in ("track", "bed", "house", "wall", "floor", "gate", "stair", "platform",
                                           "cover", "bumper")])
    m = ndimage.binary_dilation(m, iterations=3)
    for name, way, a, b, L in P.CONNECTORS:
        for x, z in (a, b):
            m[max(0, P.ix(x) - 4):P.ix(x) + 5, max(0, P.iz(z) - 4):P.iz(z) + 5] = True
    for b in (P.TRESTLE, P.FOOTBRIDGE):
        m[P.ix(b["x0"]) - 4:P.ix(b["x1"]) + 5, P.iz(b["z0"]) - 6:P.iz(b["z1"]) + 7] = True
    m[P.ix(-34) - 2:P.ix(-32) + 3, :] |= False
    return m


def spruce(w, x, g, z, tall):
    for y in range(g + 1, g + tall + 1):
        w.set(x, y, z, *SPRUCE_LOG)
    for k, y in enumerate(range(g + tall, g + 2, -1)):
        r = 1 + (k % 2) + k // 3
        r = min(r, 3)
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) <= r + (0 if r < 2 else 1) and (dx or dz) and w.id(x + dx, y, z + dz) == 0:
                    w.set(x + dx, y, z + dz, B.LEAVES, 1 | 4)
    w.set(x, g + tall + 1, z, B.LEAVES, 1 | 4)
    w.set(x, g + tall + 2, z, B.LEAVES, 1 | 4)


def trees(w):
    keep = keep_mask()
    placed = []
    cands = [(i, j) for i in range(NX) for j in range(NZ) if KN[R.K[i, j]] == "ground" and not keep[i, j]]
    rng.shuffle(cands)
    for i, j in cands:
        if len(placed) >= 26:
            break
        x, z = i + P.X_MIN, j + P.Z_MIN
        if any(abs(x - a) + abs(z - b) < 9 for a, b in placed):
            continue
        if -36 <= z <= -21 and -35 <= x <= -30:                     # the foot of the west steps
            continue
        placed.append((x, z))
        spruce(w, x, h(x, z), z, rng.randint(6, 9))
    # and on the mountains, where the slope is gentle enough to hold one
    n = 0
    for _ in range(3000):
        i, j = rng.randrange(NX), rng.randrange(NZ)
        if MOUNT[i, j] < 0 or MDIST[i, j] < 3 or MOUNT[i, j] > 74:
            continue
        x, z = i + P.X_MIN, j + P.Z_MIN
        g = w.top(x, z)
        if w.id(x, g, z) != B.GRASS:
            continue
        spruce(w, x, g, z, rng.randint(5, 8))
        n += 1
        if n > 70:
            break


def make():
    w = World(P.X_MIN, P.Z_MIN, NX, NZ, sy=SY)
    columns(w)
    gorge(w)
    upper_adit(w)
    buildings(w)
    houses(w)
    station(w)
    trestle(w)
    north_ladder(w)
    mine(w)
    adit(w)
    gantry(w)
    cover(w)
    lamps(w)
    trees(w)
    track(w)
    w.biome[:, :] = 4                                                # forest
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Copperline", (0, 60, 0))
    print(f"generated and saved {time.time() - t0:.1f}s; gates: {GATE_REGIONS}")


if __name__ == "__main__":
    main(sys.argv[1])


ADIT_XZ = [(x, z) for x, z, f in adit_cells()]
