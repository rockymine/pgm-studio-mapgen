"""Coldbore's ground laid in blocks: rock in beds under everything, snow on whatever is gentle enough to hold it,
the scorched band along the fissure where the snow has melted off to ash, the fissure's crust and its lava.

Three grounds, each a set of one tone: the snowfield (snow, with packed ice where the wind has scoured it), the
rock (stone and andesite, cobblestone under a third) on every slope too steep for snow, and the ash (grey stained
clay with black stained clay patches and gravel inset). The snow meets the ash raggedly, with a speckled band of
snow lying over ash a few blocks wide.
"""
import numpy as np

import land
from pgmvox import B
from pgmvox.geom import noise
from pgmvox.surface.terrain import slope_deg

ICE_PLAINS = 12
SNOW_SLOPE = 35                                # steeper than this holds no snow
SCORCH = 14.0                                  # the ash band's reach past the fissure's rim, before its ragged edge


def lay(w):
    """Lay the whole board's ground; returns (top, deg, scorched) over the world grid."""
    H, X, Z = land.heights()
    top = np.round(H).astype(int)
    deg = slope_deg(top)
    c, half = land.fissure_line()
    s = land.across(X, Z)
    hw = half[(X - land.X0).astype(int)]
    rim = np.abs(s) - hw                                         # under 0 inside the fissure
    edge = SCORCH + 4 * noise.fbm(X.shape, 9, 2, seed=40) + 2 * noise.fbm(X.shape, 3, 1, seed=41)
    scorched = rim < edge
    speckle = (rim >= edge) & (rim < edge + 5) & (noise.fbm(X.shape, 2, 1, seed=42) > 0.15 + 0.12 * (rim - edge))
    patch = noise.fbm(X.shape, 5, 2, seed=43)
    scour = noise.fbm(X.shape, 16, 2, seed=46)                   # where the wind has scoured the snow to ice
    fleck = noise.fbm(X.shape, 2, 1, seed=44)
    bed = noise.fbm(X.shape, 40, 2, seed=45) * 3

    sy = w.ids.shape[1]
    ys = np.arange(sy)
    for i in range(w.sx):
        for k in range(w.sz):
            h = int(top[i, k])
            col_ids = np.zeros(sy, np.uint16)
            col_dat = np.zeros(sy, np.uint8)
            # the rock in beds: andesite where the bed wave is high, cobblestone flecked through
            wave = np.sin((ys + bed[i, k]) / 2.6)
            col_ids[1:h + 1] = B.STONE
            col_dat[1:h + 1] = np.where(wave[1:h + 1] > 0.45, 5, 0)
            hot = rim[i, k] < 4 and h < 62                       # the fissure's throat: veins, crust, glow
            if hot:
                vein = np.sin(ys[1:h + 1] * 0.7 + bed[i, k] * 3 + (i + k) * 0.25) > 0.8
                col_ids[1:h + 1] = np.where(vein, B.NETHERRACK, col_ids[1:h + 1])
                glint = ((ys[1:h + 1] * 31 + i * 17 + k * 13) % 53 == 0) & (ys[1:h + 1] < 46)
                col_ids[1:h + 1] = np.where(glint, B.GLOWSTONE, col_ids[1:h + 1])
                deep = ys[1:h + 1] < 30
                col_ids[1:h + 1] = np.where(deep & (wave[1:h + 1] > 0.2), B.NETHERRACK, col_ids[1:h + 1])
                col_ids[1:h + 1] = np.where(ys[1:h + 1] < 24, B.OBSIDIAN, col_ids[1:h + 1])
                col_dat[1:h + 1] = np.where(col_ids[1:h + 1] == B.STONE, col_dat[1:h + 1], 0)
            g = deg[i, k]
            if h <= land.LAVA:                                     # the lava's floor: obsidian and netherrack
                col_ids[h] = B.OBSIDIAN if fleck[i, k] > 0 else B.NETHERRACK
                col_dat[h] = 0
                col_ids[h + 1:land.LAVA + 1] = B.LAVA
            elif rim[i, k] < 0 and g >= SNOW_SLOPE:              # the fissure's walls: bare rock, cooling crust low
                if h < 30:
                    col_ids[h], col_dat[h] = (B.OBSIDIAN, 0) if fleck[i, k] > 0.2 else (B.COBBLE, 0)
            elif g >= SNOW_SLOPE:                                 # rock too steep for snow
                if fleck[i, k] > 0.35:
                    col_ids[h], col_dat[h] = B.COBBLE, 0
            elif scorched[i, k]:                                  # the ash band
                blk = (B.STAINED_CLAY, 15) if patch[i, k] < -0.32 else (B.GRAVEL, 0) if patch[i, k] > 0.5 \
                    else (B.STAINED_CLAY, 7)
                col_ids[max(1, h - 2):h + 1] = B.STAINED_CLAY
                col_dat[max(1, h - 2):h + 1] = 7
                col_ids[h], col_dat[h] = blk
                if rim[i, k] < 1.5 and fleck[i, k] > 0.3:         # the lip: netherrack crust at the very edge
                    col_ids[h], col_dat[h] = B.NETHERRACK, 0
            else:                                                 # the snowfield
                col_ids[max(1, h - 2):h + 1] = B.SNOW
                col_dat[max(1, h - 2):h + 1] = 0
                if scour[i, k] > 0.62 and g < 10:
                    col_ids[h] = B.PACKED_ICE
            if speckle[i, k] and g < SNOW_SLOPE and h + 1 < sy and col_ids[h] in (B.STAINED_CLAY, B.GRAVEL):
                col_ids[h + 1] = B.SNOW_LAYER
            w.ids[i, :, k] = col_ids
            w.dat[i, :, k] = col_dat
    w.biome[:] = ICE_PLAINS
    return top, deg, scorched


def crevasse_ice(w, top):
    """The flank crevasses' walls in ice: every column within a few blocks of one is packed ice under its snow,
    deep enough that the crack's faces read as glacier ice rather than rock."""
    from pgmvox.geom.shapes import polyline
    X, Z = land.grid()
    for pts in [[(-71, 19), (-66, 24), (-60, 21), (-55, 26)], [(42, 36), (50, 33), (56, 38), (64, 35)]]:
        d = polyline(X, Z, pts)[0]
        for i, k in np.argwhere(d < 4.5):
            h = int(top[i, k])
            lo = max(1, h - 16)
            col = w.ids[i, lo:h - 1, k]
            w.ids[i, lo:h - 1, k] = np.where(col == B.STONE, B.PACKED_ICE, col)
            w.dat[i, lo:h - 1, k] = np.where(col == B.STONE, 0, w.dat[i, lo:h - 1, k])
