"""Hoarfire's ground laid in the world: rock in beds under the whole board, a floating underside sheer along the
Rift, the top finished by its angle in three grounds (the snowfield, the frost band at the Thaw, autumn grass), the
glacier in packed ice and snow, the water, and the biome under every column.

    lay(w, R, rng)  ->  deg, zones      the ground of the whole board (it is symmetric; the dressing is drawn on Rowan's
                                        half and mirrored)
"""
import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.geom import noise, shapes
from pgmvox.surface import terrain as T

COLD_TAIGA, MESA, SAVANNA = 30, 37, 35
SNOW_LINE = 62                              # above it the first snow lies on autumn ground too


def zones():
    """winter: how far into the snow a column lies, in blocks from a ragged seam beside the Thaw (positive: snow);
    the frost band is the few blocks either side of it."""
    X, Z = P.X, P.Z
    d, _, side = shapes.polyline(X, Z, land.THAW, side=True)
    west = side * d                                  # the right hand walking the stream south is the west
    ragged = 3.2 * noise.fbm(X.shape, 10, 2, seed=61) + 1.5 * noise.fbm(X.shape, 4, 1, seed=62)
    wint = west - 4 + ragged
    wint = P.SYM.field(wint, keep=Z < 0)
    return wint


def strata():
    return T.Strata([((B.STONE, 0), 3, 5), ((B.STONE, 5), 2.5, 3), ((B.STONE, 1), 0.7, 2), ((B.STONE, 6), 0.6, 1),
                     ((B.COAL_ORE, 0), 0.12, 1)], seed=17, start=1)


def patches(cell, seed, share):
    """A mask of small patches over the board, `share` of it, features `cell` across (mirrored)."""
    f = noise.fbm(P.H.shape, cell, 2, seed=seed)
    f = P.SYM.field(f, keep=P.Z < 0)
    return f > np.quantile(f, 1 - share)


def lay(w, R, rng):
    H, LAND = P.H, P.LAND
    beds = strata()
    offset = T.bed_offset(H.shape, dip=(0.04, -0.02), fold=2.5, cell=22, seed=5, drape=(H, 0.6, 10))
    fill = T.beds(beds, offset, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.04), ((B.STONE, 5), (B.GRAVEL, 0), 0.03)], seed=6)
    # where the rock ends: sheer along the Rift, tapering elsewhere
    void = ~LAND
    rift = void & (np.abs(P.Z + 0.5) < 16)
    for (cx, cz), rx, rz, _, _ in land.ISLETS:
        rift &= ~((np.abs(P.X - cx) <= rx + 4) & (np.abs(P.Z - cz) <= rz + 4))
    rough = 3 * noise.fbm(H.shape, 7, 2, seed=71)
    pad = 12                                                  # the void beyond the world's edge counts as void
    bottom = T.island_bottom(np.pad(H, pad), np.pad(LAND, pad), np.pad(rift, pad), taper=(3, 0.55),
                             sheer_taper=(16, 0.6), rough=np.pad(rough, pad), floor=6)[pad:-pad, pad:-pad]
    deg = T.lay(w, H, mask=LAND, top=lambda d, h: (B.GRASS, 0), under=(B.DIRT, 0), bands=fill, from_y=2, bottom=bottom)
    wint = zones()
    ice = land.ground()["ice"] if False else P.G["ice"]
    glacier = LAND & (ice > 2)
    snowy = (wint > 0) | glacier
    stony = patches(3, 81, 0.45)
    litter = patches(4, 82, 0.4)
    X, Z = P.X, P.Z
    frost_r = rng.random(H.shape)
    tops = {}
    for i, k in np.argwhere(LAND):
        h = int(H[i, k])
        d = deg[i, k]
        top = w.ids[i, h, k]
        if glacier[i, k]:
            thick = int(min(ice[i, k], 22))
            for y in range(max(2, h - thick), h):
                band = (y + int(offset[i, k])) % 7
                w.ids[i, y, k], w.dat[i, y, k] = (B.SNOW, 0) if band == 0 else (B.PACKED_ICE, 0)
            blk = (B.SNOW, 0) if d < 42 else (B.PACKED_ICE, 0)
        elif snowy[i, k]:
            if d < 34:
                blk = (B.SNOW, 0)
            elif d < 50:
                blk = (B.SNOW, 0) if not stony[i, k] else ((B.STONE, 5) if (i + k) % 3 else (B.STONE, 0))
            else:
                blk = None                                   # rock, as laid
        else:
            if d < 32:
                blk = (B.GRASS, 0)
            elif d < 48:
                blk = (B.GRASS, 0) if not stony[i, k] else ((B.STONE, 0) if litter[i, k] else (B.STONE, 5))
            else:
                blk = None
        if blk is not None and top != 0:
            if blk == (B.SNOW, 0) and w.ids[i, h - 1, k] == B.DIRT:
                pass
            w.ids[i, h, k], w.dat[i, h, k] = blk
        # snow lying: the frost band's specks, and the first snow on the heights
        lie = False
        if not snowy[i, k] and w.ids[i, h, k] == B.GRASS:
            if wint[i, k] > -5 and frost_r[i, k] < 0.75 * np.clip((wint[i, k] + 5) / 5, 0, 1):
                lie = True
            if h >= SNOW_LINE and frost_r[i, k] < np.clip((h - SNOW_LINE + 1) / 3, 0, 1):
                lie = True
        if lie and w.ids[i, h + 1, k] == 0:
            w.ids[i, h + 1, k], w.dat[i, h + 1, k] = B.SNOW_LAYER, 0
        tops[(i, k)] = h
    # the biome: cold taiga under the snow, mesa under the autumn (its grass and leaves russet)
    w.biome[:, :] = np.where(wint > -2, COLD_TAIGA, MESA)
    return deg, wint


def water(w):
    """The Thaw and the spring in water over gravel and clay; the Rime Tarn frozen, ice over water; the spring's
    west half skinned with ice."""
    H = P.H
    g = P.G
    for wat, bed in ((g["thaw"], (B.GRAVEL, 0)), (g["spring"], (B.CLAY, 0))):
        T.fill_water(w, H, np.where(wat.mask, wat.surface, 0), bed)
    tarn = g["tarn"]
    T.fill_water(w, H, np.where(tarn.mask, tarn.surface, 0), (B.GRAVEL, 0))
    for i, k in np.argwhere(tarn.mask):
        w.ids[i, int(tarn.surface[i, k]), k] = B.ICE
    sp = g["spring"]
    for i, k in np.argwhere(sp.mask):
        if P.X[i, k] < -1:
            w.ids[i, int(sp.surface[i, k]), k] = B.ICE
