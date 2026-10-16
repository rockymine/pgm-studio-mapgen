"""Small things every dressing module needs: discs of columns, stairs and slabs by name, the ground as the plan states it, and a path laid
as a wandering stroke."""
import math

import numpy as np

import plan as P
from pgmvox import B
from pgmvox.core.orient import stair as stair_data

AIRY = (B.AIR, B.TALLGRASS, B.DEADBUSH, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT, B.SNOW_LAYER, B.VINE)


def disc(cx, cz, r):
    """(x, z, distance) of every block whose centre is within r of the block (cx, cz)."""
    R = int(math.ceil(r))
    for x in range(cx - R, cx + R + 1):
        for z in range(cz - R, cz + R + 1):
            d = math.hypot(x - cx, z - cz)
            if d <= r:
                yield x, z, d


def stairs(blk, rises, upside=False):
    return (blk, stair_data(rises, upside))


def clear_above(w, x, z, y0, y1=None):
    """Air from y0 up (to y1, or the world's top)."""
    w.column(x, z, y0, (w.sy - 1) if y1 is None else y1, B.AIR)


def pick(rng, table):
    total = sum(s for _, s in table)
    r = rng.random() * total
    acc = 0.0
    for blk, s in table:
        acc += s
        if r <= acc:
            return blk
    return table[-1][0]


def line_cells(a, b):
    """Block cells from a to b inclusive (a Bresenham line), each (x, z)."""
    (x0, z0), (x1, z1) = a, b
    dx, dz = abs(x1 - x0), abs(z1 - z0)
    sx, sz = (1 if x1 > x0 else -1), (1 if z1 > z0 else -1)
    err = dx - dz
    out = []
    while True:
        out.append((x0, z0))
        if (x0, z0) == (x1, z1):
            break
        e2 = 2 * err
        if e2 > -dz:
            err -= dz
            x0 += sx
        if e2 < dx:
            err += dx
            z0 += sz
    return out


def ground_top(w, x, z):
    """The y of the highest block in a column that is not air, a plant, a snow layer or a liquid."""
    for y in range(w.sy - 1, 0, -1):
        if w.id(x, y, z) not in AIRY + (B.WATER, B.LAVA, B.WATER_FLOW, B.LAVA_FLOW):
            return y
    return 0


def wander(points, rng, step=6.0, amp=2.2):
    """A route through `points` with each leg bent by smooth wobble, so a path is not a ruled line: returns a denser polyline."""
    out = [points[0]]
    for (ax, az), (bx, bz) in zip(points, points[1:]):
        length = math.hypot(bx - ax, bz - az)
        n = max(1, int(length // step))
        nx, nz = -(bz - az) / max(length, 1e-9), (bx - ax) / max(length, 1e-9)
        phase = rng.uniform(0, 6.28)
        for j in range(1, n + 1):
            t = j / n
            bend = amp * math.sin(math.pi * t) * math.sin(phase + 3.1 * t)
            out.append((ax + (bx - ax) * t + nx * bend, az + (bz - az) * t + nz * bend))
    return out


# ---- what is already spoken for: roads, buildings, plazas and the ground round an objective, kept clear of trees and props ------------
CLAIM = np.zeros(P.H.shape, bool)


def reset_claims():
    CLAIM[:] = False


def claim_cells(cells, pad=0):
    for x, z in cells:
        for dx in range(-pad, pad + 1):
            for dz in range(-pad, pad + 1):
                i, k = x + dx - P.X_MIN, z + dz - P.Z_MIN
                if 0 <= i < CLAIM.shape[0] and 0 <= k < CLAIM.shape[1]:
                    CLAIM[i, k] = True


def claim_disc(cx, cz, r):
    claim_cells([(x, z) for x, z, _ in disc(cx, cz, r)])


def claimed(x, z):
    i, k = x - P.X_MIN, z - P.Z_MIN
    return not (0 <= i < CLAIM.shape[0] and 0 <= k < CLAIM.shape[1]) or bool(CLAIM[i, k])
