"""Generate Loomfall from the plan: the five carpets, each a single sheet of wool in its pattern over nothing; the
desert city far below the kill height, its domes, minarets, flat roofs and lit windows; the dunes round it; and
paper lanterns floating high over the carpets and well clear of their edges.

    python3 gen.py <build-dir>

Nothing stands under a carpet, near or far, but the city below the kill height, and nothing stands within a
running jump of a carpet's edge: a block under the wool would hold it up when it should fall, and a block beside
a carpet would be a place to wait out the match.
"""
import math
import random
import sys
import time

import numpy as np

import noise
import plan as P
from mc import World, B

X0, X1, Z0, Z1 = -96, 95, -96, 95
SY = 230
rng = random.Random(31)
CITY_TOP = 100                                                   # every roof and minaret under this
SAND, SANDSTONE, SMOOTH, CHISELED = (B.SAND, 0), (B.SANDSTONE, 0), (B.SANDSTONE, 2), (B.SANDSTONE, 1)
QUARTZ, WHITE_CLAY, ORANGE_CLAY = (B.QUARTZ, 0), (B.STAINED_CLAY, 0), (B.STAINED_CLAY, 1)
CYAN_CLAY, BLUE_CLAY, GOLD = (B.STAINED_CLAY, 9), (B.STAINED_CLAY, 11), (B.GOLD_BLOCK, 0)
PALM_LOG, PALM_LEAVES = (B.LOG, 3), (B.LEAVES, 3 | 4)


def footprint():
    """Every column a carpet covers, widened by eight: the reach of a running jump and more."""
    m = np.zeros((X1 - X0 + 1, Z1 - Z0 + 1), bool)
    for c in P.CARPETS:
        name, x0, x1, z0, z1, y, holes = c
        m[x0 - 8 - X0:x1 + 9 - X0, z0 - 8 - Z0:z1 + 9 - Z0] = True
    return m


FOOT = footprint()


def carpets(w):
    for k, c in enumerate(P.CARPETS):
        y = c[5]
        for x, z in P.cells(c):
            w.set(x, y, z, B.WOOL, P.pattern(k, x, z))


# ---- the city, far below ---------------------------------------------------------------------------------
def dunes(w):
    n = noise.fbm((X1 - X0 + 1, Z1 - Z0 + 1), 24, 3, seed=4)
    for i in range(X1 - X0 + 1):
        for j in range(Z1 - Z0 + 1):
            h = int(22 + 6 * n[i, j])
            w.ids[i, 1:h, j] = B.SANDSTONE
            w.ids[i, h - 2:h + 1, j] = B.SAND
    return n


def ground(w, x, z):
    return w.top(x, z)


def house(w, x0, z0, wd, dp, hgt):
    g = min(ground(w, x, z) for x in (x0, x0 + wd - 1) for z in (z0, z0 + dp - 1))
    for x in range(x0, x0 + wd):
        for z in range(z0, z0 + dp):
            edge = x in (x0, x0 + wd - 1) or z in (z0, z0 + dp - 1)
            for y in range(g - 2, g + hgt):
                if edge or y < g + 1:
                    blk = SMOOTH if (y - g) % 4 else SANDSTONE
                    if edge and y > g and (y - g) % 4 == 2 and (x + z) % 3 == 0:
                        blk = (B.GLOWSTONE, 0) if rng.random() < 0.6 else (B.STAINED_PANE, 1)     # lit windows
                    w.set(x, y, z, *blk)
            w.set(x, g + hgt, z, *SANDSTONE)
            if edge and (x + z) % 2 == 0:
                w.set(x, g + hgt + 1, z, *SMOOTH)                     # the parapet's crenels
    return g + hgt


def dome(w, cx, cz, r, base, colour):
    for x in range(cx - r, cx + r + 1):
        for z in range(cz - r, cz + r + 1):
            d2 = (x - cx) ** 2 + (z - cz) ** 2
            if d2 > r * r:
                continue
            hh = int(math.sqrt(r * r - d2) * 1.2)
            for y in range(base, base + hh + 1):
                w.set(x, y, z, *colour)
    w.set(cx, base + int(r * 1.2) + 1, cz, *GOLD)
    w.set(cx, base + int(r * 1.2) + 2, cz, B.FENCE)


def minaret(w, x, z, h):
    g = ground(w, x, z)
    for y in range(g, g + h):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if abs(dx) + abs(dz) < 2 or y < g + 4:
                    w.set(x + dx, y, z + dz, *(SMOOTH if (y - g) % 7 else CHISELED))
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) + abs(dz) <= 3:
                w.set(x + dx, g + h, z + dz, *SANDSTONE)
                if abs(dx) == 2 or abs(dz) == 2:
                    w.set(x + dx, g + h + 1, z + dz, B.FENCE)
    w.set(x, g + h + 1, z, B.GLOWSTONE)
    for y in range(g + h + 2, g + h + 6):
        w.set(x, y, z, *(WHITE_CLAY if y < g + h + 5 else GOLD))


def palm(w, x, z):
    g = ground(w, x, z)
    h = rng.randint(6, 10)
    for y in range(g + 1, g + h):
        w.set(x, y, z, *PALM_LOG)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        for k in range(1, 4):
            w.set(x + dx * k, g + h - (1 if k == 3 else 0), z + dz * k, *PALM_LEAVES)
    w.set(x, g + h, z, *PALM_LEAVES)


def city(w):
    dunes(w)
    # the walled city on the plain beneath the carpets: streets of flat-roofed houses, a great mosque, minarets
    for bx in range(-70, 70, 11):
        for bz in range(-70, 70, 11):
            if math.hypot(bx, bz) > 72 or rng.random() < 0.18:
                continue
            if abs(bx) < 14 and abs(bz) < 14:
                continue
            house(w, bx + rng.randint(0, 2), bz + rng.randint(0, 2), rng.randint(5, 8), rng.randint(5, 8), rng.randint(5, 12))
    g = ground(w, 0, 0)
    for x in range(-13, 14):                                      # the mosque's court
        for z in range(-13, 14):
            w.set(x, g, z, *(QUARTZ if (x + z) % 2 else SMOOTH))
    house(w, -9, -9, 19, 19, 12)
    dome(w, 0, 0, 8, g + 12, CYAN_CLAY)
    for x, z in ((-12, -12), (12, -12), (-12, 12), (12, 12)):
        minaret(w, x, z, 30)
    for x, z in ((-45, 30), (40, -42), (52, 50), (-55, -40)):
        minaret(w, x, z, rng.randint(22, 32))
    for x, z in ((30, 30), (-30, -36)):
        dome(w, x, z, 5, ground(w, x, z) + 9, ORANGE_CLAY if x > 0 else BLUE_CLAY)
    for _ in range(50):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(74, 92)
        palm(w, int(r * math.cos(a)), int(r * math.sin(a)))
    # the city wall
    for a in range(0, 360, 1):
        t = math.radians(a)
        x, z = int(round(76 * math.cos(t))), int(round(76 * math.sin(t)))
        g = ground(w, x, z)
        for y in range(g, g + 8):
            w.set(x, y, z, *SANDSTONE)
        if a % 3 == 0:
            w.set(x, g + 8, z, *SMOOTH)
    top = int(np.nonzero(w.ids.any(axis=(0, 2)))[0].max())
    assert top < CITY_TOP, top


# ---- the lanterns, high and clear --------------------------------------------------------------------------
def lanterns(w):
    """Paper lanterns floating over the carpets, all six and more above the top one: a lantern anywhere lower, even
    far out, could be reached by a long fall from a carpet's edge and stood on, with no fall damage to stop it."""
    placed = 0
    top_y = P.CARPETS[0][5]
    while placed < 70:
        x, z = rng.randint(-60, 60), rng.randint(-60, 60)
        y = rng.randint(top_y + 6, SY - 6)
        w.set(x, y + 1, z, B.FENCE)
        w.set(x, y, z, B.WOOL, rng.choice([14, 1, 4]))
        w.set(x, y - 1, z, B.GLOWSTONE)
        placed += 1


def make():
    w = World(X0, Z0, X1 - X0 + 1, Z1 - Z0 + 1, sy=SY)
    city(w)
    lanterns(w)
    carpets(w)
    w.biome[:, :] = 2                                                # desert
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Loomfall", (0, 200, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
