"""Generate Spark from the plan: the Claude spark as a single floor of terracotta wool hung in the sky, its rim a
shade darker, a tapering underside of clay under it; the blocks of cream stone on it; and far out and far below, a
cream sea of cloud and a ring of snow peaks.

    python3 gen.py <build-dir>

Nothing stands above the kill height within seventy blocks of the spark's floor: a knockback-ten hit carries a
player forty-three blocks, and anything they landed on would let them wait out the match.
"""
import math
import random
import sys
import time

import numpy as np
from scipy.ndimage import gaussian_filter

import noise
import plan as P
from mc import World, B

X0, X1, Z0, Z1 = -200, 199, -200, 199
SY = 200
CLEAR = 48 + 72                                                  # no scenery above the kill height inside this radius
rng = random.Random(41)

TERRACOTTA = (B.WOOL, 1)                                         # the floor: the logo's terracotta
RIM = (B.STAINED_CLAY, 1)                                        # its edge, a shade darker
UNDER = [(B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 14), (B.HARDENED_CLAY, 0)]
CREAM, CREAM_TOP = (B.SANDSTONE, 2), (B.SANDSTONE, 1)            # smooth and chiseled sandstone
CLOUD = [(B.WOOL, 0), (B.SNOW, 0), (B.QUARTZ, 0)]


def edge_dist():
    """For every cell of the spark, how far it lies inside its edge: a breadth-first walk in from the rim."""
    R = 52
    d = {}
    frontier = []
    for x in range(-R, R + 1):
        for z in range(-R, R + 1):
            if P.is_floor(x, z) and any(not P.is_floor(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                d[(x, z)] = 0
                frontier.append((x, z))
    while frontier:
        nxt = []
        for x, z in frontier:
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c = (x + dx, z + dz)
                if c not in d and P.is_floor(*c):
                    d[c] = d[(x, z)] + 1
                    nxt.append(c)
        frontier = nxt
    return d


def spark(w):
    y = P.FLOOR_Y
    dist = edge_dist()
    for (x, z), d in dist.items():
        w.set(x, y, z, *(RIM if d == 0 else TERRACOTTA))
        depth = 1 + int(1.6 * min(d, 7) ** 0.9) + rng.randint(0, 1) + (2 if math.hypot(x, z) < P.HUB_R + 2 else 0)
        for k in range(1, depth + 1):                            # a tapering underside, banded like fired clay
            w.set(x, y - k, z, *UNDER[(k + (x * 3 + z) // 11) % len(UNDER)])
    for x0, x1, z0, z1, h in P.CRATES:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for k in range(h):
                    w.set(x, y + 1 + k, z, *(CREAM_TOP if k == h - 1 and h == 2 else CREAM))


def clouds(w):
    """The cream cloud sea far below: a deck of white with billows rising out of it."""
    n = noise.fbm((X1 - X0 + 1, Z1 - Z0 + 1), 14, 4, seed=7)
    m = noise.fbm((X1 - X0 + 1, Z1 - Z0 + 1), 5, 2, seed=8)
    for i in range(X1 - X0 + 1):
        for j in range(Z1 - Z0 + 1):
            v = n[i, j]
            if v < -0.25:
                continue                                         # a break in the deck, the sky below showing
            top = P.CLOUD_Y + int(max(0.0, v) * 9 + m[i, j] * 1.5)
            bot = P.CLOUD_Y - 1 - int(max(0.0, v) * 3)
            mat = CLOUD[0] if m[i, j] > -0.2 else CLOUD[1]
            air = w.ids[i, bot:top + 1, j] == 0                    # round the mountains' feet, never into them
            w.ids[i, bot:top + 1, j][air] = mat[0]
            w.dat[i, bot:top + 1, j][air] = mat[1]


def peaks(w):
    """A ring of snow mountains round the horizon: a ridged heightfield that rises from the clouds outside CLEAR,
    crests and saddles and spurs, rock banded in andesite, snow on every top over 112."""
    sx, sz = X1 - X0 + 1, Z1 - Z0 + 1
    xs, zs = np.meshgrid(np.arange(X0, X1 + 1), np.arange(Z0, Z1 + 1), indexing="ij")
    r = np.hypot(xs, zs)
    t = np.clip((r - CLEAR - 8) / 45.0, 0, 1)
    ring = t * t * (3 - 2 * t)                                   # smoothstep: nothing inside CLEAR
    big = noise.fbm((sx, sz), 46, 3, seed=21)
    mass = np.clip((noise.fbm((sx, sz), 40, 2, seed=24) + 0.3) * 1.3, 0, 1) ** 1.5   # massifs, clouds between
    ridge = 1.0 - np.abs(noise.fbm((sx, sz), 20, 4, seed=22))   # crests where the noise crosses zero
    fine = noise.fbm((sx, sz), 6, 2, seed=23)
    edge = np.clip((200 - np.maximum(np.abs(xs), np.abs(zs))) / 30.0, 0, 1)
    h = ring * edge * (mass * (45 + 45 * (big + 0.5)) + mass ** 2 * 80 * ridge ** 2)
    h = gaussian_filter(h, 2.5) + 3 * fine * (h > 10)          # slopes, not walls; a little roughness on them
    h = np.clip(h, 0, SY - 3).astype(int)
    h[r < CLEAR] = np.minimum(h[r < CLEAR], P.KILL_Y - 2)
    ids, dat = w.ids, w.dat
    for i in range(sx):
        for j in range(sz):
            tp = h[i, j]
            if tp <= P.CLOUD_Y - 3:
                continue
            ids[i, 1:tp + 1, j] = B.STONE
            band = ((np.arange(1, tp + 1) + int(4 * fine[i, j])) // 7) % 5
            dat[i, 1:tp + 1, j] = np.where(band == 1, 5, np.where(band == 3, 6, 0))
            if tp > 112 or (tp > 98 and fine[i, j] > 0.15):
                ids[i, tp - 1:tp + 1, j] = B.SNOW
                dat[i, tp - 1:tp + 1, j] = 0
                ids[i, tp + 1, j], dat[i, tp + 1, j] = B.SNOW_LAYER, 1
            elif tp > 84 and fine[i, j] > 0.3:
                ids[i, tp + 1, j], dat[i, tp + 1, j] = B.SNOW_LAYER, 0
            elif tp < 60 and fine[i, j] > -0.1:
                ids[i, tp, j], dat[i, tp, j] = B.GRASS, 0


def make():
    w = World(X0, Z0, X1 - X0 + 1, Z1 - Z0 + 1, sy=SY)
    peaks(w)
    clouds(w)
    spark(w)
    w.biome[:, :] = 3                                                # extreme hills
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Spark", (0, P.FLOOR_Y + 2, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
