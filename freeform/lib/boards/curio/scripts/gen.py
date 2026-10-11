"""Generate Curio Square: the paved square and its streets, every builder's plot drawn from its own module into its
place, the fountain in the middle with the seekers' cage over it, the town wall round the square, the alpine
market town round the wall, and the mountains round the town.

    python3 gen.py <build-dir>

A plot draws only into its own box, through the same canvas the plot kit checks it with, so what was checked alone
is what stands in the square.
"""
import math
import os
import random
import sys
import time

import numpy as np
from scipy.ndimage import gaussian_filter

import noise
import plan as P
import plotkit as K
import sketch
from mc import World, B

HERE = os.path.dirname(os.path.abspath(__file__))
X0, X1, Z0, Z1 = -140, 139, -140, 139                           # was -180..179: the outside is 22% narrower a side
SY = 200
Y = P.STREET_Y                                                   # a player on the street stands at y 64
G = Y - 1                                                        # the paving
rng = random.Random(17)

PAVE = [(B.STONEBRICK, 0), (B.STONE, 5), (B.STONE, 6), (B.STONEBRICK, 0), (B.COBBLE, 0)]
CAGE = (P.CENTRE_X - 2, Y + 14, P.CENTRE_Z - 2, P.CENTRE_X + 2, Y + 18, P.CENTRE_Z + 2)


def ground(w):
    """The valley floor round the town, rising into the mountains: grass on dirt on stone."""
    sx, sz = X1 - X0 + 1, Z1 - Z0 + 1
    xs, zs = np.meshgrid(np.arange(X0, X1 + 1), np.arange(Z0, Z1 + 1), indexing="ij")
    r = np.maximum(np.abs(xs), np.abs(zs)) * 0.6 + np.hypot(xs, zs) * 0.4
    t = np.clip((r - 105) / 37.0, 0, 1)                            # the mountains rise over 37 blocks, not 55
    ring = t * t * (3 - 2 * t)
    big = noise.fbm((sx, sz), 46, 3, seed=31)
    mass = np.clip((noise.fbm((sx, sz), 40, 2, seed=34) + 0.35) * 1.3, 0, 1) ** 1.3
    ridge = 1.0 - np.abs(noise.fbm((sx, sz), 20, 4, seed=32))
    fine = noise.fbm((sx, sz), 6, 2, seed=33)
    meadow = 2.5 * noise.fbm((sx, sz), 18, 2, seed=35) * np.clip((r - 62) / 20.0, 0, 1)
    h = G + meadow + ring * (mass * (35 + 40 * (big + 0.5)) + mass ** 2 * 70 * ridge ** 2)
    h = gaussian_filter(h, 2.0) + 2 * fine * ring
    h = np.clip(h, 1, SY - 4).astype(int)
    ids, dat = w.ids, w.dat
    for i in range(sx):
        for j in range(sz):
            tp = h[i, j]
            ids[i, 1:tp - 3, j] = B.STONE
            ids[i, tp - 3:tp, j] = B.DIRT
            ids[i, tp, j] = B.GRASS
            if tp > G + 30:                                      # rock and snow on the heights
                ids[i, tp - 3:tp + 1, j] = B.STONE
                dat[i, tp - 3:tp + 1, j] = 5 if fine[i, j] > 0 else 0
                if tp > G + 62 or (tp > G + 52 and fine[i, j] > 0.1):
                    ids[i, tp, j], dat[i, tp, j] = B.SNOW, 0
                    ids[i, tp + 1, j], dat[i, tp + 1, j] = B.SNOW_LAYER, 1
            elif tp > G + 4 and fine[i, j] > 0.45:
                ids[i, tp + 1, j], dat[i, tp + 1, j] = B.TALLGRASS, 1
    ids[:, 0, :] = B.BEDROCK
    return h


def square(w):
    """The paving: the whole square at y 63, a patterned stone with a border round every plot."""
    for x in range(-P.HALF, P.HALF + 1):
        for z in range(-P.HALF, P.HALF + 1):
            for y in range(G - 3, G):
                w.set(x, y, z, B.STONE)
            w.set(x, G, z, *PAVE[(x * 7 + z * 13 + (x * z) % 5) % len(PAVE)])
            for y in range(G + 1, SY):
                w.set(x, y, z, B.AIR)
    for i, j in P.plots():                                       # a kerb of smooth stone round every plot
        x0, z0 = P.origin(i, j)
        for k in range(-1, P.PLOT + 1):
            for x, z in ((x0 + k, z0 - 1), (x0 + k, z0 + P.PLOT), (x0 - 1, z0 + k), (x0 + P.PLOT, z0 + k)):
                w.set(x, G, z, B.DSLAB, 0)


def fountain(w):
    """The middle plot: a round basin and a column with a gilded figure; the seekers' glass cage hangs over it."""
    cx, cz = P.CENTRE_X, P.CENTRE_Z
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            d = math.hypot(x - cx, z - cz)
            w.set(x, G, z, *((B.QUARTZ, 0) if (x + z) % 2 else (B.STONE, 4)))
            if 3.6 <= d <= 4.6:
                w.set(x, Y, z, B.STONEBRICK, 0)
                w.set(x, Y + 1, z, B.SLAB, 5)
            elif d < 3.6:
                w.set(x, Y, z, B.WATER)
                w.set(x, G, z, B.STONE, 6)
    for y in range(Y, Y + 6):
        w.set(cx, y, cz, B.QUARTZ, 2)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        w.set(cx + dx, Y, cz + dz, B.QUARTZ, 1)
        w.set(cx + dx, Y + 4, cz + dz, B.SLAB, 7)
    w.set(cx, Y + 6, cz, B.GOLD_BLOCK)
    w.set(cx, Y + 7, cz, B.GOLD_BLOCK)
    w.set(cx, Y + 8, cz, B.FENCE)
    # the cage: glass on all six sides, cleared when the seekers are released
    x0, y0, z0, x1, y1, z1 = CAGE
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or y in (y0, y1) or z in (z0, z1):
                    w.set(x, y, z, B.GLASS)


def plots(w):
    out = []
    for (i, j), (builder, row) in sketch.layout().items():
        if row is None:
            out.append((i, j, builder, None, ["no plot"]))
            continue
        path = os.path.join(HERE, "..", "plots", builder, row["file"])
        x0, z0 = P.origin(i, j)
        if not os.path.exists(path):
            out.append((i, j, builder, row, ["the module is missing"]))
            continue
        m = K.load(path)
        c = K.draw(w, m, x0, z0, Y)
        out.append((i, j, builder, row, c.errors))
    return out


def wall(w):
    """The town wall round the square: eight high, crenellated, gates on each side shut with portcullises."""
    W = P.WALL
    for k in range(-W, W + 1):
        for x, z in ((k, -W), (k, W), (-W, k), (W, k)):
            for y in range(G, Y + 8):
                w.set(x, y, z, *((B.STONEBRICK, 2) if (x * 3 + y + z * 5) % 9 == 0 else (B.STONEBRICK, 0)))
            if k % 2 == 0:
                w.set(x, Y + 8, z, B.STONEBRICK, 0)
            for t in (1, 2):                                     # a walk behind the parapet, outside the square
                ox, oz = (0, -t) if z == -W else (0, t) if z == W else (-t, 0) if x == -W else (t, 0)
                if abs(x + ox) <= W + 2 and abs(z + oz) <= W + 2:
                    for y in range(G, Y + 7):
                        w.set(x + ox, y, z + oz, B.STONEBRICK, 0)
    for gx, gz, along in ((0, -W, "x"), (0, W, "x"), (-W, 0, "z"), (W, 0, "z")):
        for k in range(-2, 3):
            x, z = (gx + k, gz) if along == "x" else (gx, gz + k)
            for y in range(Y, Y + 5):
                w.set(x, y, z, B.IRON_BARS)
            for y in range(Y + 5, Y + 11):
                w.set(x, y, z, B.STONEBRICK, 0)
        for k in (-3, 3):                                        # gate towers
            x, z = (gx + k, gz) if along == "x" else (gx, gz + k)
            for y in range(G, Y + 13):
                w.set(x, y, z, B.STONEBRICK, 0)
            w.set(x, Y + 13, z, B.BRICK)


def chalet(w, x0, z0, wd, dp, floors, h, axis):
    """A town chalet: a stone ground floor, white upper floors, a dark timber gable with a balcony, a deep roof."""
    g = max(int(h[x0 - X0 + dx, z0 - Z0 + dz]) for dx in (0, wd - 1) for dz in (0, dp - 1))
    top = g + 1 + 4 * floors
    for x in range(x0, x0 + wd):
        for z in range(z0, z0 + dp):
            for y in range(int(h[x - X0, z - Z0]) - 1, g + 1):
                w.set(x, y, z, B.COBBLE)
            edge = x in (x0, x0 + wd - 1) or z in (z0, z0 + dp - 1)
            if not edge:
                continue
            for y in range(g + 1, top):
                upper = y >= g + 5
                window = (y - g) % 4 == 2 and (x + z) % 3 == 1
                blk = (B.PANE, 0) if window else (B.WOOL, 0) if upper else (B.COBBLE, 0)
                if upper and (x in (x0, x0 + wd - 1) and z in (z0, z0 + dp - 1)):
                    blk = (B.LOG2, 1)
                w.set(x, y, z, *blk)
    span = dp if axis == "x" else wd
    for i in range(span // 2 + 2):                               # the roof, overhanging by one
        y = top + i
        for a in range(-1, (wd if axis == "x" else dp) + 1):
            for b in (i - 1, span - i):
                x, z = (x0 + a, z0 + b) if axis == "x" else (x0 + b, z0 + a)
                if 0 <= b + 0 < span + 0 or True:
                    w.set(x, y, z, B.SPRUCE_STAIRS if b == i - 1 or b == span - i else B.PLANKS,
                          (2 if b == i - 1 else 3) if axis == "x" else (0 if b == i - 1 else 1))
        if span - i - (i - 1) <= 1:
            break
    for i in range(span // 2 + 1):                               # the gable ends in dark timber
        for b in range(i, span - i):
            for a in (0, (wd if axis == "x" else dp) - 1):
                x, z = (x0 + a, z0 + b) if axis == "x" else (x0 + b, z0 + a)
                w.set(x, top + i, z, B.PLANKS, 5)
    if axis == "x":                                              # a balcony across the front gable
        for b in range(1, dp - 1):
            w.set(x0 - 1, g + 5, z0 + b, B.WOOD_SLAB, 5)
            w.set(x0 - 2, g + 6, z0 + b, B.FENCE) if False else None
    for y in range(top - 2, top + span // 2 + 2):               # a chimney
        w.set(x0 + 1, y, z0 + 1, B.BRICK)


def town(w, h):
    """The market town round the wall: rows of chalets in streets, a church with a spire, an inn."""
    placed = []
    for ring_r in (62, 76, 90):
        n = int(2 * math.pi * ring_r / 15)
        for k in range(n):
            a = 2 * math.pi * k / n + rng.uniform(-0.05, 0.05) + ring_r * 0.01
            if any(abs(math.atan2(math.sin(a - g), math.cos(a - g))) < 0.07 for g in (0, math.pi / 2, math.pi, -math.pi / 2)):
                continue                                         # the roads out of the gates stay open
            cx, cz = int(ring_r * math.cos(a)), int(ring_r * math.sin(a))
            wd, dp = rng.randint(7, 10), rng.randint(7, 10)
            x0, z0 = cx - wd // 2, cz - dp // 2
            if max(abs(cx), abs(cz)) < P.WALL + 9 or rng.random() < 0.12:
                continue
            if any(abs(x0 - px) < 11 and abs(z0 - pz) < 11 for px, pz in placed):
                continue
            if h[x0 - X0, z0 - Z0] > G + 10:
                continue
            placed.append((x0, z0))
            chalet(w, x0, z0, wd, dp, rng.randint(2, 3), h, "x" if abs(cx) > abs(cz) else "z")
    # the church: a nave and a tall spire north-east of the square
    cx, cz = 78, -70
    g = int(h[cx - X0, cz - Z0])
    for x in range(cx - 8, cx + 9):
        for z in range(cz - 4, cz + 5):
            for y in range(g - 2, g + 1):
                w.set(x, y, z, B.COBBLE)
            if x in (cx - 8, cx + 8) or z in (cz - 4, cz + 4):
                for y in range(g + 1, g + 10):
                    w.set(x, y, z, *((B.PANE, 0) if (y - g) % 4 == 2 and x % 3 == 0 else (B.WOOL, 0)))
    for i in range(6):
        for x in range(cx - 9, cx + 10):
            w.set(x, g + 10 + i, cz - 5 + i, B.SPRUCE_STAIRS, 2)
            w.set(x, g + 10 + i, cz + 5 - i, B.SPRUCE_STAIRS, 3)
    for x in range(cx + 6, cx + 11):
        for z in range(cz - 2, cz + 3):
            for y in range(g + 1, g + 22):
                if x in (cx + 6, cx + 10) or z in (cz - 2, cz + 2):
                    w.set(x, y, z, B.WOOL, 0)
    for i in range(10):                                          # the spire, an onion of copper green
        r = [3, 3, 2.5, 2, 1.5, 1.2, 1, 1, 0.5, 0.5][i]
        for x in range(cx + 8 - 3, cx + 8 + 4):
            for z in range(cz - 3, cz + 4):
                if math.hypot(x - cx - 8, z - cz) <= r:
                    w.set(x, g + 22 + i, z, B.STAINED_CLAY, 9 if i < 6 else 13)
    w.set(cx + 8, g + 32, cz, B.GOLD_BLOCK)
    w.set(cx + 8, g + 33, cz, B.FENCE)


def make():
    w = World(X0, Z0, X1 - X0 + 1, Z1 - Z0 + 1, sy=SY)
    h = ground(w)
    town(w, h)
    square(w)
    wall(w)
    fountain(w)
    report = plots(w)
    w.biome[:, :] = 3
    return w, report


def main(build):
    t0 = time.time()
    w, report = make()
    bad = [r for r in report if r[4]]
    for i, j, builder, row, errs in bad:
        print(f"plot {i},{j} ({builder} {row['file'] if row else '-'}): {'; '.join(errs[:3])}")
    w.save(build, "Curio Square", (P.CENTRE_X, Y + 30, P.CENTRE_Z + 60))
    print(f"generated and saved {time.time() - t0:.1f}s; {len(report) - len(bad)} plots drawn clean, {len(bad)} not")


if __name__ == "__main__":
    main(sys.argv[1])
