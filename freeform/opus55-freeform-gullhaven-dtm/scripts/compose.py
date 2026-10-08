"""Gullhaven DTM — Gullhaven turned into a destroy-the-monument board by putting two of it together.

The free-for-all island is built as it is, with two monuments of gold added: one floating over the water between
the harbour's two piers, one floating over a pad on the Cove's beach: cubes of gold three on a side with bedrock
at their hearts. Then the whole island is copied and turned half a
circle about the Skerry, (x, z) -> (-38 - x, 115 - z), so that the Skerry falls on itself and becomes the islet
between the two islands, each joined to it by its own bridge. Red holds the first island, blue the turned one.
Each team spawns in its own town's upper street, and wins by breaking both of the other's monuments.

    python3 compose.py <build-dir>
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "opus55-freeform-gullhaven", "scripts"))

import gen  # noqa: E402  (the free-for-all island's generator)
import plan as P  # noqa: E402
from mc import World, B  # noqa: E402

sys.path.insert(0, HERE)
from rotate import data_table  # noqa: E402

AX, BZ = -38, 115                       # the half-turn: (x, z) -> (AX - x, BZ - z)
SEA_FLOOR = gen.SEA_FLOOR
GOLD = (B.GOLD_BLOCK, 0)
RED, BLUE = 14, 11

# the monuments, on the first (red) island; blue's are their turned images
def cube(cx, y0, cz):
    """A monument: a three-block cube of gold, bedrock at its heart."""
    return [(cx + dx, y0 + dy, cz + dz) for dx in (-1, 0, 1) for dy in (0, 1, 2) for dz in (-1, 0, 1)]


# the monuments, on the first (red) island; blue's are their turned images. Each floats with three blocks of
# air under it: the harbour's over the water between the piers, the beach's over its pad.
MONUMENTS = [
    dict(key="harbour", name="the Harbour Monument", centre=(31, 25), y0=P.SEA + 4),
    dict(key="beach", name="the Beach Monument", centre=(-51, 8), y0=21 + 4, pad_y=21),
]
for m in MONUMENTS:
    m["blocks"] = cube(m["centre"][0], m["y0"], m["centre"][1])
SPAWN = dict(at=(16.5, 37, -38.5), yaw=0, box=(10, 22, -40, -36))     # the upper street, facing the harbour


def turn(x, z):
    return AX - x, BZ - z


def monuments(w):
    """Each monument a cube of gold three on a side with a block of bedrock at its centre, floating: the
    harbour's over the basin between the two piers, three blocks of air over the water; the beach's over a pad
    of mossy cobble ringed in the team's wool, three blocks of air over the pad."""
    for m in MONUMENTS:
        cx, cz = m["centre"]
        for x, y, z in m["blocks"]:
            centre = (x, z) == (cx, cz) and y == m["y0"] + 1
            w.set(x, y, z, *((B.BEDROCK, 0) if centre else GOLD))
        for x in range(cx - 1, cx + 2):                  # three blocks of air under it
            for z in range(cz - 1, cz + 2):
                for y in range(m["y0"] - 3, m["y0"]):
                    if y > P.SEA:
                        w.set(x, y, z, B.AIR)
    cx, cz = MONUMENTS[1]["centre"]
    py = MONUMENTS[1]["pad_y"]
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(cx + dx, py, cz + dz, *((B.WOOL, RED) if (dx, dz) != (0, 0) else (B.MOSSY, 0)))
            for y in range(18, py):
                w.set(cx + dx, y, cz + dz, B.MOSSY, 0)


def spawn_square(w):
    """The upper street round the spawn point in the team's wool and quartz, so a player knows where they are."""
    x0, x1, z0, z1 = SPAWN["box"]
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if w.id(x, 36, z) in (B.STONEBRICK, B.COBBLE, B.STONE, B.GRAVEL):
                w.set(x, 36, z, *((B.WOOL, RED) if (x + z) % 2 == 0 else (B.QUARTZ, 0)))


def compose():
    w1 = gen.make()
    monuments(w1)
    spawn_square(w1)
    # the combined box: both islands' boxes and the sea round them
    xa, xb = min(P.X_MIN, AX - P.X_MAX), max(P.X_MAX, AX - P.X_MIN)
    za, zb = min(P.Z_MIN, BZ - P.Z_MAX), max(P.Z_MAX, BZ - P.Z_MIN)
    W = World(xa, za, xb - xa + 1, zb - za + 1, sy=w1.sy)
    W.fill(xa, gen.BASE_Y, za, xb, SEA_FLOOR - 1, zb, B.STONE, 0)
    W.fill(xa, SEA_FLOOR, za, xb, SEA_FLOOR, zb, B.SAND, 0)
    W.fill(xa, SEA_FLOOR + 1, za, xb, P.SEA, zb, B.WATER, 0)
    # the first island
    i0, k0 = w1.x0 - xa, w1.z0 - za
    W.ids[i0:i0 + w1.sx, :, k0:k0 + w1.sz] = w1.ids
    W.dat[i0:i0 + w1.sx, :, k0:k0 + w1.sz] = w1.dat
    # the turned copy: arrays reversed in x and z, facing blocks turned, red wool made blue
    t = data_table()
    ids2 = w1.ids[::-1, :, ::-1].copy()
    dat2 = t[ids2, w1.dat[::-1, :, ::-1]]
    wool = ids2 == B.WOOL
    dat2[wool & (dat2 == RED)] = BLUE
    x2a = AX - (w1.x0 + w1.sx - 1)
    z2a = BZ - (w1.z0 + w1.sz - 1)
    i2, k2 = x2a - xa, z2a - za
    cur_i = W.ids[i2:i2 + w1.sx, :, k2:k2 + w1.sz]
    cur_d = W.dat[i2:i2 + w1.sx, :, k2:k2 + w1.sz]
    soft = np.isin(cur_i, [B.AIR, B.WATER, B.WATER_FLOW])
    hard2 = ~np.isin(ids2, [B.AIR, B.WATER, B.WATER_FLOW])
    take = soft & hard2 | ~np.isin(ids2, [B.AIR]) & soft     # where the first island has nothing, the copy wins
    W.ids[i2:i2 + w1.sx, :, k2:k2 + w1.sz] = np.where(take, ids2, cur_i)
    W.dat[i2:i2 + w1.sx, :, k2:k2 + w1.sz] = np.where(take, dat2, cur_d)
    W.biome[:, :] = 1
    return W


def main(build):
    t0 = time.time()
    W = compose()
    W.save(build, "Gullhaven DTM", (-19, 60, 57))
    print(f"composed and saved {time.time() - t0:.1f}s: {W.sx} x {W.sz}, x {W.x0}..{W.x0 + W.sx - 1}, "
          f"z {W.z0}..{W.z0 + W.sz - 1}")


if __name__ == "__main__":
    main(sys.argv[1])
