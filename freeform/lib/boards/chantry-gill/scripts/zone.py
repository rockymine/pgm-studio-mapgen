"""Chantry Gill's build zone: the whole of the void between the two coasts that face each other, column by column,
so a player can bridge out from any block of the front coast and nowhere is it unclear where building stops.

    edges()       {x: z} the first land of blue's front coast in each column (red's is its half turn)
    columns()     {x: (z0, z1)} the zone in each column, inclusive: from red's coast to blue's, held within CAP
    rects()       the zone as rectangles (x0, z0, x1, z1), runs of columns with the same span merged
    mask(X, Z)    the zone on a grid

Past CAP blocks from the middle a coast has turned into an island's flank, and the zone stops there: the flanks are
not the front, and a zone reaching round them would let a team build round the board's sides.
"""
import functools

import numpy as np

CAP = 24


@functools.lru_cache(maxsize=1)
def edges():
    import terrain as TR
    import layout as L
    land = TR.arrays()["landmask"] > 0.5
    X, Z = L.grid(TR.X_RANGE, TR.Z_RANGE)
    out = {}
    for i in range(land.shape[0]):
        zs = Z[i][land[i] & (Z[i] >= 0)]
        if len(zs):
            out[int(X[i, 0])] = int(zs.min())
    return out


def columns():
    b = edges()
    out = {}
    for x in range(min(min(b), -1 - max(b)), max(max(b), -1 - min(b)) + 1):
        blue = min(b.get(x, CAP + 1), CAP + 1)
        red = -1 - min(b.get(-1 - x, CAP + 1), CAP + 1)                 # (x, z) -> (-1 - x, -1 - z)
        out[x] = (red + 1, blue - 1)
    return out


def rects():
    cols = sorted(columns().items())
    out, start, span = [], None, None
    for x, s in cols + [(None, None)]:
        if s != span:
            if span is not None:
                out.append((start, span[0], prev, span[1]))
            start, span = x, s
        prev = x
    return out


def mask(X, Z):
    m = np.zeros(X.shape, bool)
    for x0, z0, x1, z1 in rects():
        m |= (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
    return m
