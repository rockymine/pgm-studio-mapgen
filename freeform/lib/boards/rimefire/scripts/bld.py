"""Small builders every place uses."""
import numpy as np

from pgmvox import B
from pgmvox.core.orient import stair as stair_data

import land as LND


def ground_y(g, x, z):
    return int(g["H"][x - LND.X0, z - LND.Z0])


def level(w, g, x0, z0, x1, z1, y, top=(B.STONEBRICK, 0), under=(B.STONE, 0), clear=14, grow=None):
    """Level a rectangle: ground filled to y (the top block `top`) and everything above it cleared. `top` may be a
    function (x, z) -> block."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            gh = ground_y(g, x, z)
            if gh <= 0:
                continue
            for yy in range(min(gh, y) - 1, y):
                if w.id(x, yy, z) in (B.AIR, B.SNOW_LAYER, B.TALLGRASS):
                    w.set(x, yy, z, *under)
            blk = top(x, z) if callable(top) else top
            if blk is not None:
                w.set(x, y, z, *blk)
            for yy in range(y + 1, y + 1 + clear):
                if w.id(x, yy, z) != B.AIR:
                    w.set(x, yy, z, B.AIR)


def stair(w, x, y, z, block, rises, upside=False):
    w.set(x, y, z, block, stair_data(rises, upside))


def ring_cells(cx, cz, r0, r1):
    out = []
    for x in range(int(cx - r1) - 1, int(cx + r1) + 2):
        for z in range(int(cz - r1) - 1, int(cz + r1) + 2):
            d = np.hypot(x + 0.5 - cx, z + 0.5 - cz)
            if r0 <= d < r1:
                out.append((x, z))
    return out


def post(w, x, y, z, height, fence=B.DARK_OAK_FENCE, lamp=(B.JACK, 0)):
    for k in range(1, height + 1):
        w.set(x, y + k, z, fence)
    if lamp:
        w.set(x, y + height + 1, z, *lamp)
