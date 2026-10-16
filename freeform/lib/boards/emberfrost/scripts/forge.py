"""The Forge: the fire core on a plinth at 66 inside a lava moat in the Caldera, a ring of chimneys round it, two gates in the rim, and the
Slag Run, a lava tube up from the south slope to an undercroft whose roof is the plinth's floor.

The core is exposed on a bare plinth with the moat round it; the approaches differ: across a bridge from either gap, over the moat from
the north and east by building, down from the rim at 77 above, and up the Slag Run from below.
"""
import math

import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.volume import under
from util import disc, pick, stairs

FX, FZ = land.FORGE
Y = land.FORGE_LEVEL
MOAT = (9.7, 12.3)
BED = 61
LAVA_TOP = 64

WARM = [((B.NETHER_BRICK, 0), 5), ((B.RED_SANDSTONE, 2), 4), ((B.STAINED_CLAY, 12), 2), ((B.HARDENED_CLAY, 0), 2)]


def plinth(w, rng):
    for x, z, d in disc(FX, FZ, 9.4):
        h = P.g(x, z)
        for yy in range(min(h, Y) - 1, Y):
            w.set(x, yy, z, B.NETHER_BRICK, 0)
        for yy in range(Y + 1, max(h, Y) + 3):
            w.set(x, yy, z, B.AIR)
        m = max(abs(x - FX), abs(z - FZ))
        if m <= 2:
            blk = (B.NETHER_BRICK, 0) if (x + z) % 2 else (B.STAINED_CLAY, 15)
        elif m == 3:
            blk = (B.RED_SANDSTONE, 1)
        elif d < 6.6:
            blk = pick(rng, WARM)
        elif d < 7.4:
            blk = (B.RED_SANDSTONE, 0)
        else:
            blk = pick(rng, [((B.NETHER_BRICK, 0), 4), ((B.STAINED_CLAY, 15), 2), ((B.STONE, 6), 2)])
        w.set(x, Y, z, *blk)


def moat(w, rng):
    """A ring of lava three wide between the plinth and the crater floor, a block under both its banks."""
    for x, z, d in disc(FX, FZ, 13.6):
        if d < MOAT[0] - 0.5:
            continue
        h = P.g(x, z)
        if MOAT[0] <= d <= MOAT[1]:
            for yy in range(BED, LAVA_TOP + 1):
                w.set(x, yy, z, B.LAVA if yy > BED else B.STAINED_CLAY, 0 if yy > BED else 15)
            for yy in range(LAVA_TOP + 1, max(h, Y) + 3):
                w.set(x, yy, z, B.AIR)
            w.set(x, BED - 1, z, B.OBSIDIAN)
        elif MOAT[0] - 0.5 < d < MOAT[0]:
            for yy in range(BED, Y):
                w.set(x, yy, z, B.NETHER_BRICK, 0)
            w.set(x, Y, z, B.NETHER_BRICK, 0)
        elif MOAT[1] < d <= MOAT[1] + 0.9:
            top = max(h, LAVA_TOP + 2)
            for yy in range(BED, top):
                w.set(x, yy, z, B.NETHER_BRICK, 0)
            w.set(x, top, z, B.NETHER_BRICK, 0)


def bridge(w, dx, dz):
    """A bridge of three across the moat along (dx, dz), nether brick with a fence either side and a glow at its ends."""
    side = (-dz, dx)
    for r in range(8, 15):
        for j in (-1, 0, 1):
            x, z = FX + dx * r + side[0] * j, FZ + dz * r + side[1] * j
            top = Y
            if r >= 13:
                top = Y - (r - 12) // 2
            for yy in range(min(top, P.g(x, z)) - 1, top):
                w.set(x, yy, z, B.NETHER_BRICK, 0)
            w.set(x, top, z, B.NETHER_BRICK if (r + j) % 2 else B.STAINED_CLAY, 0 if (r + j) % 2 else 15)
            for yy in range(top + 1, top + 4):
                w.set(x, yy, z, B.AIR)
        if 9 <= r <= 13:
            for j in (-2, 2):
                x, z = FX + dx * r + side[0] * j, FZ + dz * r + side[1] * j
                w.set(x, Y + 1, z, B.NETHER_FENCE)
                if r in (9, 13):
                    w.set(x, Y + 2, z, B.NETHER_FENCE)
                    w.set(x, Y + 3, z, B.GLOWSTONE)
    for r in (13, 14):
        for j in (-1, 0, 1):
            x, z = FX + dx * r + side[0] * j, FZ + dz * r + side[1] * j
            top = Y - (r - 12) // 2
            if r == 14:
                w.set(x, top, z, *stairs(B.NETHER_STAIRS, (-dx, -dz)))


def chimney(w, x, z):
    base = P.g(x, z)
    for ddx in (-1, 0, 1):
        for ddz in (-1, 0, 1):
            for yy in range(base - 1, base + 13):
                band = (yy - base) in (3, 7)
                w.set(x + ddx, yy, z + ddz, *(((B.STONEBRICK, 0) if band else (B.NETHER_BRICK, 0))))
    for ddx in (-1, 0, 1):
        for ddz in (-1, 0, 1):
            ring = (ddx, ddz) != (0, 0)
            w.set(x + ddx, base + 13, z + ddz, *(((B.NETHER_BRICK, 0)) if ring else (B.NETHERRACK, 0)))
            if ring:
                w.set(x + ddx, base + 14, z + ddz, B.SLAB, 6)
    w.set(x, base + 14, z, B.FIRE)
    for yy in range(base + 4, base + 7):                       # a slit of glowing glass low in the stack
        w.set(x, yy, z + 2, B.AIR)
    w.set(x, base + 5, z - 2, B.AIR)


def pylon(w, x, z, h=10):
    base = P.g(x, z)
    for ddx in (-1, 0, 1):
        for ddz in (-1, 0, 1):
            for yy in range(base - 1, base + h):
                w.set(x + ddx, yy, z + ddz, *((B.NETHER_BRICK, 0) if (yy - base) % 4 else (B.STONEBRICK, 3)))
    w.set(x, base + h, z, B.NETHERRACK)
    w.set(x, base + h + 1, z, B.FIRE)
    return base + h


def gate(w, a, b, axis):
    """Two pylons and a lintel over a road through a gap in the rim: axis 'z' is a gate across z (a gap in a north-south line)."""
    ya = pylon(w, *a)
    yb = pylon(w, *b)
    top = max(ya, yb) - 3
    n = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
    for t in range(n + 1):
        x = a[0] + (b[0] - a[0]) * t // max(n, 1)
        z = a[1] + (b[1] - a[1]) * t // max(n, 1)
        for ddx, ddz in ((0, 0), (1, 0), (0, 1)) if axis == "z" else ((0, 0), (0, 1), (1, 0)):
            w.set(x + ddx * (1 if axis == "x" else 0), top, z + ddz * (1 if axis == "z" else 0), B.NETHER_BRICK, 0)
        w.set(x, top + 1, z, B.SLAB, 6)
        if t % 3 == 1:
            w.set(x, top - 1, z, B.IRON_BARS)
            w.set(x, top - 2, z, B.IRON_BARS)
    w.set((a[0] + b[0]) // 2, top - 1, (a[1] + b[1]) // 2, B.GLOWSTONE)


def slag_run(w, rng, stats):
    """The lava tube: a mouth in the south slope, a passage stepping down, a hall under the plinth with a lava pool; walls of black rock."""
    snap = w.ids.copy()
    n1, floor = under.tunnel(w, [(29, 65, -35, 2.9), (31, 62, -40, 2.8), (33, 58, -45, 2.8), (36, 54, -52, 3.0), (38, 54, -56, 3.2)], ground=None)
    n2 = under.chamber(w, FX, 54, FZ, 6.4, 3.3, rz=6.4, ground=None)
    carved = (snap != 0) & (w.ids == 0)
    for a, y, c in np.argwhere(carved):
        for da, dy, dc in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0)):
            na, ny, nc = a + da, y + dy, c + dc
            if 0 <= na < w.sx and 0 <= ny < w.sy and 0 <= nc < w.sz and w.ids[na, ny, nc] != 0 and not carved[na, ny, nc] \
                    and w.ids[na, ny, nc] not in (B.LAVA, B.WATER):
                if dy == 1 and rng.random() < 0.07:
                    w.ids[na, ny, nc], w.dat[na, ny, nc] = B.GLOWSTONE, 0
                elif dy == -1:
                    w.ids[na, ny, nc], w.dat[na, ny, nc] = pick(rng, [((B.STONE, 6), 3), ((B.COBBLE, 0), 2), ((B.STAINED_CLAY, 15), 3), ((B.NETHERRACK, 0), 2)])
                else:
                    w.ids[na, ny, nc], w.dat[na, ny, nc] = pick(rng, [((B.STAINED_CLAY, 15), 4), ((B.STONE, 6), 2), ((B.NETHERRACK, 0), 3), ((B.COAL_ORE, 0), 1), ((B.STAINED_CLAY, 12), 1)])
    for px, pz in ((FX - 5, FZ + 2), (FX + 4, FZ - 3), (FX + 1, FZ + 5)):        # lava pools sunk in the hall's floor
        for ddx in (0, 1):
            for ddz in (0, 1):
                if True:
                    w.set(px + ddx, 53, pz + ddz, B.LAVA)
                    w.set(px + ddx, 52, pz + ddz, B.STAINED_CLAY, 15)
    stats["slag run"] = n1 + n2


def build(w, rng, stats):
    slag_run(w, rng, stats)
    plinth(w, rng)
    moat(w, rng)
    bridge(w, -1, 0)
    bridge(w, 0, 1)
    for ang in (-0.75, 0.35, 2.6):
        chimney(w, FX + round(16.5 * math.cos(ang)), FZ + round(16.5 * math.sin(ang)))
