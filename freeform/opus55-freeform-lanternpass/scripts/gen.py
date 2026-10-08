"""Generate Lantern Pass from the plan: the lane and the two walkways as ridges of rock tapering away under them over
the void; every section's floor and what stands on it — the boathouse, the harbour's boardwalk, piers and barges,
the market's stalls, awnings and arcade, the rice terraces, the bamboo and its shrine, the gorge's rope bridge,
pillars and gallery, the great stair and its torii, the temple court, the bell tower and the hall; the walkways'
paving, side-swap rows and outer wall; and far off, out of reach, peaks and a sea of cloud.

    python3 gen.py <build-dir>

Everything that hides a runner in the plan is built where the plan put it and as high: a stall three, an awning
or a roof one block at its height, a bamboo stalk nine, the grove's crown at forty.
"""
import math
import random
import sys
import time

import numpy as np
from scipy import ndimage

import noise
import plan as P
from mc import World, B

R = P.build()
KN = P.KN
HW = P.walkway_heights(R)
rng = random.Random(41)
X0, X1, Z0, Z1 = -64, 63, -44, 410                               # the volume, scenery included
SY = 90

STONE, ANDESITE, GRANITE, COBBLE, MOSSY = (B.STONE, 0), (B.STONE, 5), (B.STONE, 1), (B.COBBLE, 0), (B.MOSSY, 0)
POL_ANDESITE, SBRICK, SB_MOSSY, SB_CRACKED = (B.STONE, 6), (B.STONEBRICK, 0), (B.STONEBRICK, 1), (B.STONEBRICK, 2)
GRASS, DIRT, COARSE, PODZOL, GRAVEL = (B.GRASS, 0), (B.DIRT, 0), (B.DIRT, 1), (B.DIRT, 2), (B.GRAVEL, 0)
SPRUCE, DARK_OAK, BIRCH = (B.PLANKS, 1), (B.PLANKS, 5), (B.PLANKS, 2)
SPRUCE_LOG, DARK_LOG = (B.LOG, 1), (B.LOG2, 1)
RED_CLAY, BLACK_CLAY, WHITE_CLAY, LIME_CLAY, GREEN_CLAY = ((B.STAINED_CLAY, 14), (B.STAINED_CLAY, 15), (B.STAINED_CLAY, 0),
                                                           (B.STAINED_CLAY, 5), (B.STAINED_CLAY, 13))
RED_WOOL, WHITE_WOOL = (B.WOOL, 14), (B.WOOL, 0)
QUARTZ = (B.QUARTZ, 0)
N1 = noise.fbm((P.NX, P.NZ), 10, 3, seed=2)


def kind(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return "void"
    return KN[R.K[i, j]]


def h(x, z):
    return int(R.H[P.ix(x), P.iz(z)])


def top(x, z):
    return int(R.T[P.ix(x), P.iz(z)])


def pick(choices, weights):
    return rng.choices(choices, weights)[0]


def ridge_bottoms():
    """How deep the rock goes under each column: thin at a ridge's edge, deep at its spine, broken by noise, so
    from below the lane and the walkways read as ridges of a mountain rather than slabs."""
    solid = R.K != P.KINDS["void"]
    d = ndimage.distance_transform_edt(solid)
    n = noise.fbm((P.NX, P.NZ), 6, 3, seed=9)
    depth = 3 + 2.6 * d + 5 * n + 3 * np.abs(noise.fbm((P.NX, P.NZ), 3, 2, seed=4))
    floor = np.where(solid, R.H, 0)
    bottom = floor - np.maximum(3, depth)
    g, a = P.GORGE, P.ARCH
    for z in range(g["z0"], g["z1"] + 1):                        # the arch: thin at its crown, deep where it springs
        t = (z - g["z0"]) / (g["z1"] - g["z0"])
        bottom[P.ix(a["x0"] - 1):P.ix(a["x1"] + 1) + 1, P.iz(z)] = a["h"] - 2 - int(16 * (2 * t - 1) ** 2)
    for x, z, hh in P.PILLARS:                                    # the pillars stand on the gorge's far floor
        bottom[P.ix(x):P.ix(x) + 2, P.iz(z):P.iz(z) + 2] = 2
    return np.maximum(1, np.round(bottom)).astype(int)


BOTTOM = ridge_bottoms()


def rock(y):
    band = y % 9
    return ANDESITE if band in (2, 3) else GRANITE if band == 6 and rng.random() < 0.5 else STONE


# ---- the ground --------------------------------------------------------------------------------------------
def columns(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k = KN[R.K[i, j]]
            if k == "void":
                continue
            hh, b = int(R.H[i, j]), int(BOTTOM[i, j])
            if k == "bridge":                                       # a rope bridge is its planks and nothing under
                continue
            floor = hh if k not in ("cover", "house", "wall", "bamboo") else ground(x, z)
            if k == "wall" and kind(x, z) == "wall" and in_walkway_wall(x):
                floor = hh
            for y in range(b, floor):
                w.set(x, y, z, *rock(y))
            for y in range(b, min(b + 3, floor)):                  # the ridge's underside, mossy and hung with vines
                if rng.random() < 0.35:
                    w.set(x, y, z, *MOSSY)
            w.set(x, floor, z, *surface(k, x, z, floor))
            if k == "water":
                for y in (hh + 1, hh + 2):
                    w.set(x, y, z, B.WATER)
            if k == "paddy":
                w.set(x, hh + 1, z, B.WATER)
                if rng.random() < 0.08:
                    w.set(x, hh + 2, z, B.LILY)
            if k == "grass" and rng.random() < 0.25 and not in_box(x, z, P.HEAL["box"]):
                w.set(x, hh + 1, z, B.TALLGRASS, 1 if rng.random() < 0.8 else 2)
            if k == "stair" and (x, z) in R.stair:
                d = {"+z": 2, "-z": 3, "+x": 0, "-x": 1}[R.stair[(x, z)]]
                w.set(x, hh, z, B.STONEBRICK_STAIRS if hh >= 30 else B.OAK_STAIRS if hh < 23 else B.COBBLE_STAIRS, d)
    vines(w)


def in_walkway_wall(x):
    return x in (P.WALKS["left"][0] - 1, P.WALKS["right"][1] + 1)


def in_box(x, z, box, m=0):
    x0, x1, z0, z1 = box
    return x0 - m <= x <= x1 + m and z0 - m <= z <= z1 + m


def ground(x, z):
    """The floor under a thing standing on it: the floor of the cells round it."""
    hs = [h(x + dx, z + dz) for dx in range(-2, 3) for dz in range(-2, 3)
          if kind(x + dx, z + dz) in P.WALK and kind(x + dx, z + dz) != "water"]
    return min(hs) if hs else h(x, z)


def surface(k, x, z, y):
    if k == "plank":
        return SPRUCE if z not in range(8, 50) or x < 4 else DARK_OAK
    if k == "street":
        return pick([COBBLE, ANDESITE, POL_ANDESITE, GRAVEL], [35, 30, 20, 15])
    if k in ("grass", "bund"):
        return pick([GRASS, GRASS, PODZOL], [6, 3, 1]) if k == "grass" else GRASS
    if k == "paddy":
        return (B.FARMLAND, 7) if rng.random() < 0.5 else DIRT
    if k == "water":
        return pick([GRAVEL, (B.CLAY, 0), (B.SAND, 0)], [4, 3, 2])
    if k in ("stone", "pillar"):
        if 331 <= z:
            return pick([SBRICK, POL_ANDESITE, SB_CRACKED], [5, 3, 1])
        return pick([SBRICK, SB_MOSSY, COBBLE, ANDESITE], [4, 2, 2, 2])
    if k == "stair":
        return SBRICK
    if k == "bridge":
        return SPRUCE
    if k in ("walk",):
        return pick([SBRICK, SBRICK, SB_CRACKED, POL_ANDESITE], [5, 2, 1, 2])
    if k == "swap":
        return (B.STAINED_CLAY, 4)
    if k in ("floor", "gate"):
        return DARK_OAK if x % 2 else SPRUCE
    return STONE


def vines(w):
    """Vines hung from the ridges' undersides and their thin edges."""
    for _ in range(2500):
        x, z = rng.randint(P.X_MIN, P.X_MAX), rng.randint(P.Z_MIN, P.Z_MAX)
        i, j = P.ix(x), P.iz(z)
        if R.K[i, j] != P.KINDS["void"]:
            continue
        for dx, dz, d in ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1)):
            if kind(x + dx, z + dz) not in ("void",):
                y = int(BOTTOM[P.ix(x + dx), P.iz(z + dz)]) + rng.randint(1, 4)
                for yy in range(y, y - rng.randint(2, 7), -1):
                    if w.id(x, yy, z) == 0 and w.id(x + dx, yy, z + dz) not in (0, B.VINE):
                        w.set(x, yy, z, B.VINE, d)
                break


# ---- 0 the boathouse ---------------------------------------------------------------------------------------
GATE_REGIONS = {"warmup": [(P.SPAWN_GATE[0], 21, 4, P.SPAWN_GATE[1], 24, 4)]}


def boathouse(w):
    lx0, lx1 = P.LANE
    x0, x1, z0, z1 = lx0 + 2, lx1 - 2, -10, 4
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            if not ring:
                continue
            post = (x in (x0, x1) and (z - z0) % 4 == 0) or (z in (z0, z1) and (x - x0) % 4 == 0)
            for y in range(21, 28):
                blk = DARK_LOG if post else (RED_CLAY if y < 23 else WHITE_CLAY)
                if not post and y in (24, 25) and (x + z) % 3 == 0:
                    blk = (B.PANE, 0)
                w.set(x, y, z, *blk)
    roof(w, x0, x1, z0, z1, 28, along_x=False)
    for x in range(P.SPAWN_GATE[0], P.SPAWN_GATE[1] + 1):
        for y in range(21, 25):
            w.set(x, y, 4, B.SPRUCE_FENCE)
        w.set(x, 25, 4, *DARK_LOG)
    for x in (x0 + 2, x1 - 2):
        lantern_hang(w, x, 26, -3)
    for x in range(x0 + 2, x1 - 1, 3):                             # boats hauled up inside
        for z in (-8, -7):
            w.set(x, 21, z, *SPRUCE)


def roof(w, x0, x1, z0, z1, y, along_x=True, mat=BLACK_CLAY, eave=1):
    """A low roof with upturned corners: the ridge along x or z, black tiles, red ridge beam."""
    half = ((z1 - z0) if along_x else (x1 - x0)) / 2.0
    for x in range(x0 - eave, x1 + eave + 1):
        for z in range(z0 - eave, z1 + eave + 1):
            v = abs(z - (z0 + z1) / 2.0) if along_x else abs(x - (x0 + x1) / 2.0)
            yy = y + int(max(0, half + eave - v) * 0.5)
            w.set(x, yy, z, *mat)
            corner = (x in (x0 - eave, x1 + eave)) and (z in (z0 - eave, z1 + eave))
            if corner:
                w.set(x, yy + 1, z, *mat)
    if along_x:
        zc = (z0 + z1) // 2
        for x in range(x0 - eave, x1 + eave + 1):
            w.set(x, y + int((half + eave) * 0.5) + 1, zc, *RED_CLAY)
    else:
        xc = (x0 + x1) // 2
        for z in range(z0 - eave, z1 + eave + 1):
            w.set(xc, y + int((half + eave) * 0.5) + 1, z, *RED_CLAY)


def lantern_hang(w, x, y, z, drop=1):
    for k in range(drop):
        w.set(x, y - k, z, B.FENCE)
    w.set(x, y - drop, z, *RED_WOOL)
    w.set(x, y - drop - 1, z, B.GLOWSTONE)


def stone_lantern(w, x, y, z):
    w.set(x, y + 1, z, B.COBBLE_WALL)
    w.set(x, y + 2, z, B.GLOWSTONE)
    w.set(x, y + 3, z, B.SLAB, 5)


# ---- 1 the harbour -----------------------------------------------------------------------------------------
def harbour(w):
    for x0, x1, z0, z1 in P.BARGES:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                hull = x in (x0, x1) or z in (z0, z1)
                for y in (18, 19):
                    w.set(x, y, z, *DARK_OAK)
                if hull and (x + z) % 2 == 0:
                    w.set(x, 21, z, B.DARK_OAK_FENCE)
        w.set(x0 + 1, 21, z0 + 1, *SPRUCE_LOG)                     # a mast stump and a furled sail
        for y in range(21, 29):
            w.set((x0 + x1) // 2, y, (z0 + z1) // 2 + 2, *SPRUCE_LOG)
        for y in range(25, 28):
            w.set((x0 + x1) // 2, y, (z0 + z1) // 2 + 1, *WHITE_WOOL)
    for x0, x1, z0, z1 in P.CABINS:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(21, 24):
                    w.set(x, y, z, *(DARK_LOG if x in (x0, x1) and z in (z0, z1) else SPRUCE))
        roof(w, x0, x1, z0, z1, 24, along_x=False, eave=0)
    for x0, x1, z0, z1 in P.PIERS:                                  # piles at the piers' corners
        for x in (x0, x1):
            for z in (z0, z1):
                for y in range(21, 23):
                    w.set(x, y, z, *SPRUCE_LOG)
    for z in range(5, 61, 4):                                       # the boardwalk's rail posts and lanterns
        w.set(-12, 21, z, B.SPRUCE_FENCE)
        if z % 12 == 1:
            lantern_hang(w, -12, 23, z)
            w.set(-12, 22, z, B.SPRUCE_FENCE)
            w.set(-12, 23, z, B.SPRUCE_FENCE)
    for x0, x1, z0, z1, t in P.HARBOUR_COVER:
        crates(w, x0, x1, z0, z1, 20, t)
    for z in range(5, 61):
        if z % 3 == 0:
            w.set(11, 21, z, B.COBBLE_WALL)


def crates(w, x0, x1, z0, z1, g, t):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(g + 1, g + 1 + t):
                w.set(x, y, z, *pick([SPRUCE, SPRUCE_LOG, (B.HAY, 0), BIRCH], [4, 2, 1, 1]))


# ---- 2 the market ------------------------------------------------------------------------------------------
AWNING = [(B.WOOL, 14), (B.WOOL, 0), (B.WOOL, 1), (B.WOOL, 11), (B.WOOL, 4)]


def market(w):
    for n, (x0, x1) in enumerate(P.STALL_ROWS):
        for m, (z0, z1) in enumerate(P.STALLS_Z):
            col = AWNING[(n * 3 + m) % len(AWNING)]
            for x in range(x0, x1 + 1):
                for z in range(z0, z1 + 1):
                    edge = x in (x0, x1) or z in (z0, z1)
                    for y in (23, 24):
                        w.set(x, y, z, *(SPRUCE if edge else DARK_OAK))
                    w.set(x, 25, z, *((B.WOOD_SLAB, 1) if edge else pick([(B.MELON, 0), (B.PUMPKIN, 0), (B.HAY, 0),
                                                                      (B.WOOL, 14), (B.WOOL, 1), SPRUCE], [1] * 6)))
            for x in range(x0 - 1, x1 + 2):
                for z in range(z0, z1 + 1):
                    w.set(x, 26, z, *(col if (z - z0) % 2 == 0 else WHITE_WOOL))
    for z in range(63, 113):                                         # the arcade's roof, timber, with lanterns
        if z in (76, 77, 91, 92):
            continue
        for x in range(-8, 7):
            if w.id(x, 26, z) == 0:
                w.set(x, 26, z, *((B.WOOD_SLAB, 5 + 8) if (z % 6) else DARK_LOG))
        if z % 6 == 0:
            lantern_hang(w, -1, 25, z, drop=0)
    for z in range(61, 116, 6):                                     # lanterns strung over the open avenues
        for x in (-12, 11):
            for y in range(23, 27):
                w.set(x, y, z, *DARK_LOG)
            w.set(x, 27, z, *RED_WOOL)
            w.set(x, 28, z, B.GLOWSTONE)


# ---- 3 the terraces ----------------------------------------------------------------------------------------
def terraces(w):
    for z0, z1, hh in P.TERRACES:
        for x in range(P.LANE[0], P.LANE[1] + 1):
            if z0 > 116 and kind(x, z0 - 1) != "stair":
                pass
        # the riser's face: dry stone, mossy
        if z0 > 116:
            for x in range(P.LANE[0], P.LANE[1] + 1):
                for y in range(BOTTOM[P.ix(x), P.iz(z0)], hh):
                    if w.id(x, y, z0) in (B.STONE,):
                        w.set(x, y, z0, *pick([COBBLE, MOSSY], [3, 2]))
    for x0, x1, z0, z1 in P.HUTS:
        g = ground(x0, z0)
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                w.set(x, g, z, *DIRT)
                for y in range(g + 1, g + 4):
                    edge = x in (x0, x1) or z in (z0, z1)
                    w.set(x, y, z, *(SPRUCE_LOG if x in (x0, x1) and z in (z0, z1) else BIRCH if edge else SPRUCE))
        for x in range(x0 - 1, x1 + 2):
            for z in range(z0 - 1, z1 + 2):
                w.set(x, g + 4, z, B.HAY, 0)
        w.set((x0 + x1) // 2, g + 5, (z0 + z1) // 2, B.HAY, 0)
    for z0, z1, hh in P.TERRACES:                                   # scarecrows in the paddies' corners
        x, z = P.LANE[0] + 3, z0 + 3
        if kind(x, z) == "paddy":
            for y in (hh, hh + 1):
                w.set(x, y, z, B.FENCE)
            w.set(x, hh + 2, z, B.HAY, 4)
            w.set(x, hh + 3, z, B.PUMPKIN, 0)


# ---- 4 the bamboo ------------------------------------------------------------------------------------------
def bamboo(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            if not (171 <= z <= 225 and P.LANE[0] <= x <= P.LANE[1]):
                continue
            if R.K[i, j] == P.KINDS["bamboo"]:
                for y in range(33, 42):
                    w.set(x, y, z, *(LIME_CLAY if y % 3 == 0 else GREEN_CLAY))
            if R.C[i, j] == 40:
                w.set(x, 40, z, B.LEAVES, 3 | 4)
                if rng.random() < 0.5:
                    w.set(x, 41, z, B.LEAVES, 3 | 4)
    # the shrine: red posts, a black roof, a bell rope and an offering box
    x0, x1, z0, z1 = P.HEAL["box"]
    for x in (x0 - 1, x1 + 1):
        for z in (z0, z1):
            for y in range(33, 37):
                w.set(x, y, z, *RED_CLAY)
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0, z1 + 1):
            w.set(x, 37, z, *BLACK_CLAY)
    for x in range(x0 - 1, x1 + 2):
        w.set(x, 38, (z0 + z1) // 2, *RED_CLAY)
    w.set(0, 33, z1, *SPRUCE)
    w.set(0, 34, z1, B.WOOD_SLAB, 5)
    for y in (34, 35, 36):
        w.set(-1, y, z0 + 1, B.FENCE)
    w.set(-1, 33, z0 + 1, B.GOLD_BLOCK)


# ---- 5 the gorge -------------------------------------------------------------------------------------------
def gorge(w):
    g = P.GORGE
    # the rope bridge: planks on two ropes, posts at its ends, no rail
    for z in range(g["z0"], g["z1"] + 1):
        hh = h(P.ROPE["x0"], z)
        for x in (P.ROPE["x0"] - 1, P.ROPE["x1"] + 1):
            w.set(x, hh, z, B.FENCE)                                 # the ropes, level with the planks
        for x in range(P.ROPE["x0"], P.ROPE["x1"] + 1):
            w.set(x, hh, z, *(SPRUCE if z % 4 else DARK_OAK))
    for z in (g["z0"] - 1, g["z1"] + 1):
        for x in (P.ROPE["x0"] - 1, P.ROPE["x1"] + 1):
            for y in range(h(x, z) + 1, h(x, z) + 4):
                w.set(x, y, z, *SPRUCE_LOG)
    # the pillars: worn stone, from far below
    for x, z, hh in P.PILLARS:
        for dx in (0, 1):
            for dz in (0, 1):
                for y in range(2, hh):
                    w.set(x + dx, y, z + dz, *pick([STONE, ANDESITE, MOSSY, COBBLE], [5, 3, 2, 1]))
                w.set(x + dx, hh, z + dz, *pick([SB_MOSSY, SBRICK, MOSSY], [2, 2, 1]))
    # the arch: a stone arch under the gallery's deck, the gallery's red walls and black roof
    a = P.ARCH
    span = g["z1"] - g["z0"]
    for z in range(g["z0"], g["z1"] + 1):
        t = (z - g["z0"]) / span
        for x in range(a["x0"] - 1, a["x1"] + 2):                    # the arch's ring of dressed stone
            for y in range(int(BOTTOM[P.ix(x), P.iz(z)]), a["h"]):
                w.set(x, y, z, *(SBRICK if y > a["h"] - 3 or (x in (a["x0"] - 1, a["x1"] + 1)) else STONE))
        for x in (a["x0"] - 1, a["x1"] + 1):
            if kind(x, z) == "wall":
                for y in range(a["h"] + 1, a["h"] + 4):
                    post = (z - g["z0"]) % 7 == 0
                    w.set(x, y, z, *(DARK_LOG if post else RED_CLAY if y == a["h"] + 1 else WHITE_CLAY))
            else:
                w.set(x, a["h"] + 1, z, *RED_CLAY)                     # the window's sill
        for x in range(a["x0"] - 2, a["x1"] + 3):
            w.set(x, a["h"] + 4, z, *BLACK_CLAY)
        w.set(a["x0"] + 1, a["h"] + 5, z, *RED_CLAY)
        if (z - g["z0"]) % 6 == 3:
            lantern_hang(w, a["x0"] + 1, a["h"] + 3, z, drop=0)


# ---- 6 the stairs, 7 the temple ----------------------------------------------------------------------------
def stairs_and_temple(w):
    lx0, lx1 = P.LANE
    for z in P.TORII:
        hh = P.stair_h(z)
        for x in (lx0 + 5, lx1 - 5):
            for y in range(hh + 1, hh + 7):
                w.set(x, y, z, *RED_CLAY)
            w.set(x, hh + 1, z, *BLACK_CLAY)
        for x in range(lx0 + 3, lx1 - 2):
            w.set(x, hh + 6, z, *RED_CLAY)
            w.set(x, hh + 7, z, *BLACK_CLAY)
        w.set(lx0 + 2, hh + 7, z, *BLACK_CLAY)
        w.set(lx1 - 2, hh + 7, z, *BLACK_CLAY)
        w.set(-1, hh + 5, z, *RED_CLAY)
    for x, z in P.LANTERNS:
        stone_lantern(w, x, h(x, z), z)
    for x, z in P.PINES:
        pine(w, x, h(x, z), z)
    # the incense burner
    for x in range(-2, 2):
        for z in (340, 341):
            w.set(x, 51, z, B.CAULDRON) if (x + z) % 2 else w.set(x, 51, z, *COBBLE)
            w.set(x, 52, z, B.FENCE if (x + z) % 2 else B.COBBLE_WALL)
    # the bell tower: four red posts, a black roof, and the bronze bell hung high in it
    bx0, bx1, bz0, bz1 = P.BELL["box"]
    for x in (bx0 - 1, bx1 + 1):
        for z in (bz0 - 1, bz1 + 1):
            for y in range(51, 58):
                w.set(x, y, z, *RED_CLAY)
    for x in range(bx0 - 1, bx1 + 2):
        for z in (bz0 - 1, bz1 + 1):
            w.set(x, 56, z, *RED_CLAY)
    roof(w, bx0 - 1, bx1 + 1, bz0 - 1, bz1 + 1, 57, along_x=True, eave=1)
    cx, cz = (bx0 + bx1) // 2, (bz0 + bz1) // 2
    for y in (56,):
        w.set(cx, y, cz, B.FENCE)
    for dx in (0, 1):
        for dz in (0, 1):
            w.set(cx + dx - 0, 55, cz + dz, B.GOLD_BLOCK)
            w.set(cx + dx, 54, cz + dz, B.GOLD_BLOCK)
    w.set(cx, 53, cz, B.FENCE)                                      # the clapper rope
    for x in range(bx0, bx1 + 1):
        for z in range(bz0, bz1 + 1):
            w.set(x, 50, z, *(QUARTZ if (x + z) % 2 else POL_ANDESITE))
    # the temple hall: red pillars, white walls, a great black roof
    hx0, hx1, hz0, hz1 = P.LANE[0], P.LANE[1], 366, 372
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            ring = x in (hx0, hx1) or z in (hz0, hz1)
            for y in range(51, 62):
                if ring:
                    post = (x - hx0) % 4 == 0 if z in (hz0, hz1) else True
                    w.set(x, y, z, *(RED_CLAY if post else WHITE_CLAY if y > 52 else DARK_OAK))
                else:
                    w.set(x, y, z, *DARK_OAK)
    roof(w, hx0, hx1, hz0, hz1, 62, along_x=True, eave=2)
    for x in range(-2, 2):
        for y in (52, 53, 54):
            w.set(x, y, hz0, *DARK_LOG)                               # the hall's shut doors


def pine(w, x, g, z):
    for y in range(g + 1, g + 9):
        w.set(x, y, z, *SPRUCE_LOG)
    for k, y in enumerate(range(g + 8, g + 3, -1)):
        r = min(3, 1 + k // 2)
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) <= r and (dx or dz) and w.id(x + dx, y, z + dz) == 0:
                    w.set(x + dx, y, z + dz, B.LEAVES, 1 | 4)
    w.set(x, g + 9, z, B.LEAVES, 1 | 4)


# ---- the walkways ------------------------------------------------------------------------------------------
def walkways(w):
    for side, (x0, x1) in P.WALKS.items():
        outer = x0 if side == "left" else x1
        wall = outer - 1 if side == "left" else outer + 1
        for z in range(P.Z_MIN + 2, P.Z_MAX - 1):
            hh = int(HW[P.iz(z)])
            for y in range(hh + 1, hh + 5):
                post = z % 8 == 0
                w.set(wall, y, z, *(RED_CLAY if post else WHITE_CLAY if y < hh + 4 else BLACK_CLAY))
            w.set(wall, hh + 5, z, *BLACK_CLAY)
            prev = int(HW[P.iz(z - 1)])
            if hh == prev + 1:                                       # a step up the walkway: stairs
                for x in range(x0, x1 + 1):
                    if x != outer:
                        w.set(x, hh, z, B.STONEBRICK_STAIRS, 3)
            elif hh == prev - 1:
                for x in range(x0, x1 + 1):
                    if x != outer:
                        w.set(x, prev, z - 1, B.STONEBRICK_STAIRS, 2)
            if z % 16 == 4:
                lantern_hang(w, outer, hh + 4, z, drop=0)
        for z in (P.Z_MIN + 2, P.Z_MAX - 2):                         # the walkways' ends, walled
            for x in range(x0, x1 + 1):
                hh = int(HW[P.iz(z)])
                for y in range(hh + 1, hh + 5):
                    w.set(x, y, z, *WHITE_CLAY)


# ---- far off: peaks and a sea of cloud, none of it under the lane or within reach -------------------------
def scenery(w):
    peaks = []
    r2 = random.Random(5)
    for _ in range(26):
        side = r2.choice((-1, 1))
        x = side * r2.randint(44, 62)
        z = r2.randint(-40, 405)
        peaks.append((x, z, r2.randint(22, 52), r2.uniform(0.6, 1.0)))
    peaks += [(0, 400, 70, 0.55), (-24, 396, 58, 0.6), (26, 398, 62, 0.6), (-40, -30, 30, 0.8), (40, -34, 26, 0.8)]
    for px, pz, ph, slope in peaks:
        R0 = int(ph / slope) + 2
        for x in range(px - R0, px + R0 + 1):
            for z in range(pz - R0, pz + R0 + 1):
                if not (X0 <= x <= X1 and Z0 <= z <= Z1):
                    continue
                if P.X_MIN - 2 <= x <= P.X_MAX + 2 and P.Z_MIN - 2 <= z <= P.Z_MAX + 2:
                    continue                                          # nothing under the board
                d = math.hypot(x - px, z - pz)
                tp = int(ph - d * slope * (1.6 + 0.4 * math.sin(math.atan2(z - pz, x - px) * 3 + px)))
                if tp < 1:
                    continue
                for y in range(1, tp + 1):
                    if w.id(x, y, z) == 0:
                        w.set(x, y, z, *rock(y))
                if tp > 44:
                    w.set(x, tp + 1, z, B.SNOW_LAYER, 2)
                elif tp < 30 and w.id(x, tp, z) == B.STONE:
                    w.set(x, tp, z, *GRASS)
    # the cloud sea: low, far out, never under the lane or the gaps
    cl = noise.fbm((X1 - X0 + 1, Z1 - Z0 + 1), 9, 3, seed=12)
    for i in range(X1 - X0 + 1):
        for j in range(Z1 - Z0 + 1):
            x, z = i + X0, j + Z0
            if abs(x) < 38 and P.Z_MIN - 4 <= z <= P.Z_MAX + 4:
                continue
            if cl[i, j] > 0.15 and w.id(x, 6, z) == 0:
                w.set(x, 6, z, *WHITE_WOOL)
                if cl[i, j] > 0.35 and w.id(x, 7, z) == 0:
                    w.set(x, 7, z, *WHITE_WOOL)


def make():
    w = World(X0, Z0, X1 - X0 + 1, Z1 - Z0 + 1, sy=SY)
    columns(w)
    boathouse(w)
    harbour(w)
    market(w)
    terraces(w)
    bamboo(w)
    gorge(w)
    stairs_and_temple(w)
    walkways(w)
    scenery(w)
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Lantern Pass", (0, 70, -20))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
