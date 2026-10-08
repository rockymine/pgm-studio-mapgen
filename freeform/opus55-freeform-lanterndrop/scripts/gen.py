"""Generate Lantern Drop from the plan: every piece of the course as a fragment of Lantern Pass hanging in the void,
its top flat and walkable in the pass's materials, rock tapering away under it and hung with roots; the cisterns,
paddies and the harbour; the hills' borders; the bell court; and round the course, far out and well below it, the
snowy peaks and the sea of cloud.

    python3 gen.py <build-dir>

A piece's top is kept clear from edge to edge in the direction of the run, so nothing on it trips a player or
blocks a landing: what dresses a piece hangs under it or stands on its back corners.
"""
import math
import random
import sys
import time

import numpy as np

import noise
import plan as P
from mc import World, B

X0, X1, Z0, Z1 = -72, 71, -48, 344
SY = 256
rng = random.Random(29)

STONE, ANDESITE, MOSSY, COBBLE = (B.STONE, 0), (B.STONE, 5), (B.MOSSY, 0), (B.COBBLE, 0)
SBRICK, SB_MOSSY, POL_ANDESITE, QUARTZ = (B.STONEBRICK, 0), (B.STONEBRICK, 1), (B.STONE, 6), (B.QUARTZ, 0)
GRASS, DIRT, GRAVEL = (B.GRASS, 0), (B.DIRT, 0), (B.GRAVEL, 0)
SPRUCE, DARK_OAK, SPRUCE_LOG, DARK_LOG, JUNGLE_LEAVES = (B.PLANKS, 1), (B.PLANKS, 5), (B.LOG, 1), (B.LOG2, 1), (B.LEAVES, 3 | 4)
RED, BLACK, WHITE, GREEN, LIME = ((B.STAINED_CLAY, 14), (B.STAINED_CLAY, 15), (B.STAINED_CLAY, 0), (B.STAINED_CLAY, 13),
                                  (B.STAINED_CLAY, 5))
RED_WOOL, WHITE_WOOL = (B.WOOL, 14), (B.WOOL, 0)
HILL_CLAY = (B.STAINED_CLAY, 0)


def rock(y):
    band = (y // 6) % 7
    return ANDESITE if band == 2 else (B.STONE, 1) if band == 5 else STONE


def hill_box(p):
    """A hill's footprint on its piece: five by five on the piece's middle, or the piece's width where narrower."""
    i, name, theme, x0, x1, z0, z1, y, ex, sd = p
    cx, cz = (x0 + x1) / 2.0, (z0 + z1) / 2.0
    hx0, hx1 = max(x0, int(math.floor(cx - 2))), min(x1, int(math.floor(cx - 2)) + 4)
    hz0, hz1 = max(z0, int(math.floor(cz - 2))), min(z1, int(math.floor(cz - 2)) + 4)
    return hx0, hx1, hz0, hz1


# ---- a piece: its rock, its top ----------------------------------------------------------------------------
def underside(w, p, depth_k=1.8, mat=None):
    """Rock under a piece, deep at its middle and thin at its rim, ragged, mossy and hung with roots."""
    i, name, theme, x0, x1, z0, z1, y, ex, sd = p
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            d = min(x - x0, x1 - x, z - z0, z1 - z)
            depth = int(2 + depth_k * d) + rng.randint(0, 2) + (rng.randint(0, 4) if d >= 2 else 0)
            for yy in range(y - depth, y):
                w.set(x, yy, z, *(mat or (MOSSY if yy < y - depth + 2 and rng.random() < 0.5 else rock(yy))))
    for x in range(x0, x1 + 1):                                   # roots hanging from under it, never past its rim:
        for z in range(z0, z1 + 1):                               # anything beside a piece would catch a faller
            if rng.random() < 0.06:
                bot = y - 1
                while bot > 0 and w.id(x, bot, z) != 0:
                    bot -= 1
                for yy in range(bot, bot - rng.randint(2, 6), -1):
                    w.set(x, yy, z, *DARK_LOG)


def lantern(w, x, y, z, drop=1):
    for k in range(drop):
        w.set(x, y - k, z, B.FENCE)
    w.set(x, y - drop, z, *RED_WOOL)
    w.set(x, y - drop - 1, z, B.GLOWSTONE)


def top_layer(w, p, pick):
    i, name, theme, x0, x1, z0, z1, y, ex, sd = p
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, y, z, *pick(x, z))


def tiles(x0, x1):
    """A tiled roof's top: black tiles with a red ridge down the middle, along the run."""
    mid = (x0 + x1) // 2
    return lambda x, z: RED if x == mid else BLACK


def piece(w, p):
    i, name, theme, x0, x1, z0, z1, y, ex, sd = p
    if theme == "rope":
        for z in range(z0, z1 + 1):
            for x in range(x0, x1 + 1):
                w.set(x, y, z, *(SPRUCE if x in (x0, x1) or z % 4 else DARK_OAK))
            for x in (x0, x1):
                if z % 3 == 0:
                    w.set(x, y - 1, z, B.FENCE)                    # the ropes, under the planks
        for z in (z0, z1):
            for x in (x0, x1):
                for yy in range(y - 12, y):
                    w.set(x, yy, z, *SPRUCE_LOG)                   # anchors, hanging into the void
        return
    if theme == "pillar":
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for yy in range(y - 30 - rng.randint(0, 8), y):
                    w.set(x, yy, z, *rng.choice([STONE, ANDESITE, MOSSY, COBBLE]))
                w.set(x, y, z, *SB_MOSSY)
        return
    if theme == "nest":
        cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
        for yy in range(y - 18, y):
            w.set(cx, yy, cz, *SPRUCE_LOG)                         # the mast
        for yy in range(y - 14, y - 6):
            for dx in range(-1, 2):
                w.set(cx + dx, yy, cz + 1, *WHITE_WOOL)             # the furled sail, no wider than the nest
        top_layer(w, p, lambda x, z: SPRUCE)
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    w.set(x, y - 1, z, *DARK_OAK)
        return
    if theme == "bamboo":
        underside(w, p, 1.2)
        top_layer(w, p, lambda x, z: JUNGLE_LEAVES)
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if rng.random() < 0.35:
                    for yy in range(y - 14 - rng.randint(0, 8), y - 2):
                        if w.id(x, yy, z) == 0:
                            w.set(x, yy, z, *(LIME if yy % 3 == 0 else GREEN))
        return
    if theme == "beam":
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                w.set(x, y, z, *(DARK_LOG if x != (x0 + x1) // 2 else (B.LOG2, 1 | 8)))
                w.set(x, y - 1, z, *SPRUCE)
        for z in range(z0 + 1, z1, 3):
            lantern(w, x0 if z % 2 else x1, y - 2, z, drop=1)
        return
    if theme == "torii":
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                w.set(x, y, z, *(BLACK if z in (z0, z1) else RED))
                w.set(x, y - 1, z, *RED)
        for x in (x0 + 1, x1 - 1):                                 # its two posts, broken, hanging
            for yy in range(y - 2 - rng.randint(6, 12), y - 1):
                w.set(x, yy, (z0 + z1) // 2, *RED)
        return
    if theme == "awning":
        underside(w, p, 0.8, mat=SPRUCE)
        stripes = [(B.WOOL, 14), (B.WOOL, 1), (B.WOOL, 11), (B.WOOL, 4)]
        col = stripes[(i + (1 if sd == "right" else 0)) % len(stripes)]
        top_layer(w, p, lambda x, z: col if (z - z0) % 2 == 0 else WHITE_WOOL)
        return
    # the rest stand on rock
    underside(w, p)
    if theme == "court":
        top_layer(w, p, lambda x, z: QUARTZ if (x + z) % 2 else POL_ANDESITE)
        for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
            w.set(x, y + 1, z, B.COBBLE_WALL)
            w.set(x, y + 2, z, B.GLOWSTONE)
            w.set(x, y + 3, z, B.SLAB, 5)
        bell_tower(w, (x0 + x1) // 2, y, z0 + 2)
    elif theme in ("roof", "pagoda", "boathouse"):
        top_layer(w, p, tiles(x0, x1))
        for x, z in ((x0, z1), (x1, z1)):                            # upturned corners, at the far end only:
            w.set(x, y + 1, z, *BLACK)                               # nobody lands there
        for x in range(x0, x1 + 1, 3):                              # the eaves hung with lanterns
            for z in (z0, z1):
                lantern(w, x, y - 2, z, drop=1)
    elif theme == "gallery":
        top_layer(w, p, tiles(x0, x1))
        for x in range(x0, x1 + 1):                                 # its red walls, white panels, under the roof
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    for yy in range(y - 4, y):
                        w.set(x, yy, z, *(RED if (z - z0) % 4 == 0 or yy == y - 4 else WHITE))
    elif theme == "terrace":
        top_layer(w, p, lambda x, z: GRASS)
    elif theme == "arcade":
        top_layer(w, p, lambda x, z: DARK_LOG if (z - z0) % 6 == 0 else DARK_OAK)
        for x in range(x0, x1 + 1, 4):
            for z in (z0, z1):
                lantern(w, x, y - 2, z, drop=0)
    elif theme == "barge":
        barge(w, p)
    if "water" in ex:
        a0, a1, b0, b1 = ex["water"]
        deep = 1 if theme == "terrace" else 3
        for x in range(a0, a1 + 1):
            for z in range(b0, b1 + 1):
                if theme == "terrace" and ((x - a0) % 5 == 0 or (z - b0) % 5 == 0 or x == a1 or z == b1):
                    continue                                        # the bunds between the paddies
                for yy in range(y - deep + 1, y + 1):
                    w.set(x, yy, z, B.WATER)
                w.set(x, y - deep, z, *(DIRT if theme == "terrace" else SBRICK))
                if theme == "terrace" and rng.random() < 0.06:
                    w.set(x, y + 1, z, B.LILY)


def bell_tower(w, cx, y, z0):
    """The bell tower at the court's back: four red posts, a black roof, the gold bell."""
    for x in (cx - 3, cx + 3):
        for z in (z0 - 1, z0 + 3):
            for yy in range(y + 1, y + 8):
                w.set(x, yy, z, *RED)
    for x in range(cx - 4, cx + 5):
        for z in range(z0 - 2, z0 + 5):
            w.set(x, y + 8, z, *BLACK)
        w.set(x, y + 9, z0 + 1, *RED)
    for dx in (0, 1):
        for dz in (0, 1):
            for yy in (y + 5, y + 6):
                w.set(cx - 1 + dx, yy, z0 + dz, B.GOLD_BLOCK)
    w.set(cx, y + 7, z0, B.FENCE)


def barge(w, p):
    i, name, theme, x0, x1, z0, z1, y, ex, sd = p
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for yy in range(P.HARBOUR["y"] - 4, y + 1):
                w.set(x, yy, z, *(SPRUCE if yy == y else DARK_OAK))
    for x in range(x0, x1 + 1):                                  # a rail at the stern; the bow is where players land
        if (x + z1) % 2 == 0:
            w.set(x, y + 1, z1, B.DARK_OAK_FENCE)
    cx = (x0 + x1) // 2
    for yy in range(y + 1, y + 12):
        w.set(cx, yy, z1 - 1, *SPRUCE_LOG)                          # the mast at the stern, clear of the run's middle
    for yy in range(y + 5, y + 11):
        for dx in range(-3, 4):
            w.set(cx + dx, yy, z1, *(RED_WOOL if yy % 2 else WHITE_WOOL))


def harbour(w):
    """The harbour: a round floating basin of water, its rock bowl ragged underneath, a quay round it and the slipway."""
    h = P.HARBOUR
    (hx0, hx1), (hz0, hz1), hy = h["x"], h["z"], h["y"]
    cx, cz = (hx0 + hx1) / 2.0, (hz0 + hz1) / 2.0
    rx, rz = (hx1 - hx0) / 2.0 + 0.5, (hz1 - hz0) / 2.0 + 0.5

    def e(x, z):
        return ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2
    for x in range(hx0 - 2, hx1 + 3):
        for z in range(hz0 - 2, hz1 + 3):
            v = e(x, z)
            rim = 1.0 < v <= 1.0 + 2.6 / min(rx, rz)
            if v > 1.0 and not rim:
                continue
            depth = 8 + int(10 * max(0.0, 1 - v)) + rng.randint(0, 3)
            for yy in range(hy - depth, hy + (2 if rim else -5)):
                w.set(x, yy, z, *rock(yy))
            if rim:
                w.set(x, hy + 1, z, *SBRICK)
                if (x + z) % 7 == 0:
                    w.set(x, hy + 2, z, B.COBBLE_WALL)
                    w.set(x, hy + 3, z, B.GLOWSTONE)
            else:
                w.set(x, hy - 6, z, *GRAVEL)
                for yy in range(hy - 5, hy + 1):
                    w.set(x, yy, z, B.WATER)
    s = P.SLIPWAY
    for x in range(s["x"][0], s["x"][1] + 1):
        for z in range(s["z"][0], s["z"][1] + 2):
            k = z - s["z"][0]
            w.set(x, hy - 3 + min(k, 4), z, *POL_ANDESITE)            # a ramp of stone up out of the water
    for x in s["x"]:
        for yy in range(hy + 1, hy + 6):
            w.set(x, yy, s["z"][0], *RED)                            # a red gate over the slipway
    for x in range(s["x"][0], s["x"][1] + 1):
        w.set(x, hy + 6, s["z"][0], *BLACK)


def hills(w):
    for p in P.pieces():
        if not p[8].get("hill"):
            continue
        y = p[7]
        hx0, hx1, hz0, hz1 = hill_box(p)
        for x in range(hx0, hx1 + 1):
            for z in range(hz0, hz1 + 1):
                if (x in (hx0, hx1) or z in (hz0, hz1)) and w.id(x, y, z) not in (B.WATER, 0):
                    w.set(x, y, z, *HILL_CLAY)


# ---- far off: the peaks and the cloud sea ------------------------------------------------------------------
def scenery(w):
    r2 = random.Random(5)
    peaks = []
    for _ in range(24):
        side = r2.choice((-1, 1))
        peaks.append((side * r2.randint(52, 70), r2.randint(-40, 340), r2.randint(90, 230), r2.uniform(2.2, 3.4)))
    peaks += [(0, -46, 250, 2.6), (-30, -44, 200, 2.8), (32, -44, 210, 2.8)]
    ids = w.ids
    for px, pz, ph, slope in peaks:
        R0 = int(ph / slope * 0.6) + 2
        for x in range(px - R0, px + R0 + 1):
            for z in range(pz - R0, pz + R0 + 1):
                if not (X0 <= x <= X1 and Z0 <= z <= Z1):
                    continue
                if abs(x) < 38 and -22 <= z <= 324:
                    continue                                        # nothing near the course or under it
                d = math.hypot(x - px, z - pz)
                tp = int(ph - d * slope * (1.4 + 0.5 * math.sin(math.atan2(z - pz, x - px) * 3 + px)))
                if tp < 1:
                    continue
                col = ids[x - X0, :, z - Z0]
                band = (np.arange(1, tp + 1) // 6) % 7
                vals = np.where(band == 2, B.STONE, B.STONE)
                col[1:tp + 1] = np.where(col[1:tp + 1] == 0, vals, col[1:tp + 1])
                w.dat[x - X0, 1:tp + 1, z - Z0] = np.where(band == 2, 5, 0)
                if tp > 150:
                    w.set(x, tp, z, B.SNOW, 0)
                    w.set(x, tp + 1, z, B.SNOW_LAYER, 2)
                elif tp < 110 and d > 3:
                    w.set(x, tp, z, *GRASS)
    cl = noise.fbm((X1 - X0 + 1, Z1 - Z0 + 1), 9, 3, seed=12)
    for i in range(X1 - X0 + 1):
        for j in range(Z1 - Z0 + 1):
            x, z = i + X0, j + Z0
            if abs(x) < 40 and -24 <= z <= 326:
                continue
            if cl[i, j] > 0.15 and w.id(x, 8, z) == 0:
                w.set(x, 8, z, *WHITE_WOOL)
                if cl[i, j] > 0.35 and w.id(x, 9, z) == 0:
                    w.set(x, 9, z, *WHITE_WOOL)


def make():
    w = World(X0, Z0, X1 - X0 + 1, Z1 - Z0 + 1, sy=SY)
    harbour(w)
    for p in P.pieces():
        piece(w, p)
    hills(w)
    scenery(w)
    w.biome[:, :] = 3                                                # extreme hills
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Lantern Drop", (0, 245, 8))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
