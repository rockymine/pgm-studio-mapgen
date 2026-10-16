"""Rimefire's two skins for one ground.

A column is warm (autumn: dry grass, podzol, coarse dirt, banded clay in the cliffs) or cold (snow, packed ice,
andesite and ice in the cliffs), and the cold factor says which. It rises toward the south and with altitude and is
broken up by a slow noise, so the fire half is cold on its peaks and the ice half is warm in its low hollows: each
half keeps a piece of the other. Across the line where the two meet, warm ground carries a dusting of snow layers.
"""
import numpy as np

from pgmvox import B
from pgmvox.geom import noise, shapes
from pgmvox.surface import terrain as T

import land as LND

# the banded rock under each skin: (block, data, thickness)
WARM_BEDS = [(B.STAINED_CLAY, 12, 3), (B.HARDENED_CLAY, 0, 2), (B.STAINED_CLAY, 1, 1), (B.HARDENED_CLAY, 0, 3),
             (B.RED_SANDSTONE, 0, 2), (B.STAINED_CLAY, 12, 2), (B.STAINED_CLAY, 4, 1), (B.HARDENED_CLAY, 0, 2)]
COLD_BEDS = [(B.STONE, 5, 3), (B.STONE, 0, 2), (B.PACKED_ICE, 0, 2), (B.STONE, 5, 2), (B.STONE, 6, 2),
             (B.PACKED_ICE, 0, 1), (B.STONE, 0, 3), (B.STONE, 5, 1)]


def _table(beds):
    ids, dat = [], []
    for bid, d, n in beds:
        ids += [bid] * n
        dat += [d] * n
    return np.array(ids, np.uint16), np.array(dat, np.uint8)


WARM_T, COLD_T = _table(WARM_BEDS), _table(COLD_BEDS)


def cold_factor(g):
    """0 fully autumn, 1 fully frozen. Rises south and with height; broken by a slow noise."""
    X, Z, H = g["X"], g["Z"], g["H"]
    shape = X.shape
    slow = noise.fbm(shape, 34, 3, seed=61)
    return 0.5 + (Z + 0.5) / 105.0 + (H - 66) / 26.0 + 0.34 * slow


def fields(g):
    shape = g["X"].shape
    f = dict(
        cold=cold_factor(g),
        grain=noise.fbm(shape, 6, 2, seed=71),
        patch=noise.fbm(shape, 16, 3, seed=72),
        edge=noise.fbm(shape, 5, 2, seed=73),
        offset=(noise.fbm(shape, 30, 2, seed=74) * 4).astype(int),
    )
    return f


def skin(f, i, k):
    """'warm', 'dust' (warm ground with snow over it) or 'cold' for a column."""
    c = f["cold"][i, k] + 0.10 * f["edge"][i, k]
    if c > 0.58:
        return "cold"
    if c > 0.47:
        return "dust"
    return "warm"


def top_block(kind, deg, f, i, k):
    u, p = f["grain"][i, k], f["patch"][i, k]
    if kind == "cold":
        if deg > 52:
            return (B.PACKED_ICE, 0) if u > 0.15 else (B.STONE, 5)
        if deg > 36:
            return (B.STONE, 5) if u > 0.0 else (B.GRAVEL, 0) if u > -0.3 else (B.SNOW, 0)
        if p > 0.42:
            return (B.PACKED_ICE, 0)
        if p < -0.5 and u > 0.1:
            return (B.STONE, 5)
        return (B.SNOW, 0)
    if deg > 54:
        return None
    if deg > 38:
        return (B.DIRT, 1) if u > -0.1 else (B.GRAVEL, 0)
    if p > 0.40:
        return (B.DIRT, 2)
    if p < -0.35:
        return (B.DIRT, 1)
    return (B.GRASS, 0) if u > -0.25 else (B.DIRT, 2)


def lay_ground(w, g, f, bottom):
    """Rock in banded beds, soil, then the top of each column, by its skin and slope. Returns the slope and the skin map
    (0 warm, 1 dust, 2 cold)."""
    H, land, X = g["H"], g["land"], g["X"]
    deg = T.slope_deg(H, land)
    deg = T.ledge_angle(H, deg, land)
    depth = T.soil_depth(deg)
    skins = np.zeros(H.shape, np.uint8)
    sx, sz = H.shape
    for i in range(sx):
        for k in range(sz):
            if not land[i, k]:
                continue
            h = int(H[i, k])
            kind = skin(f, i, k)
            if g["seam"][i, k]:
                kind = "cold" if g["south"][i, k] else "warm"
            skins[i, k] = {"warm": 0, "dust": 1, "cold": 2}[kind]
            tab = COLD_T if kind == "cold" else WARM_T
            n = len(tab[0])
            lo = max(1, int(bottom[i, k]))
            ys = np.arange(lo, h)
            idx = (ys + int(f["offset"][i, k])) % n
            dd = int(depth[i, k])
            if h - lo > 0:
                w.ids[i, lo:h, k] = tab[0][idx]
                w.dat[i, lo:h, k] = tab[1][idx]
            if dd > 0:
                w.ids[i, max(lo, h - dd):h, k] = B.DIRT
                w.dat[i, max(lo, h - dd):h, k] = 1 if kind != "cold" and f["patch"][i, k] < -0.1 else 0
            blk = top_block(kind, deg[i, k], f, i, k)
            if blk is None:
                blk = (tab[0][(h + int(f["offset"][i, k])) % n], tab[1][(h + int(f["offset"][i, k])) % n])
            w.ids[i, h, k], w.dat[i, h, k] = blk
            if kind == "dust" and deg[i, k] < 40 and h + 1 < w.sy and f["grain"][i, k] > -0.55:
                w.ids[i, h + 1, k], w.dat[i, h + 1, k] = B.SNOW_LAYER, 0
    return deg, skins
