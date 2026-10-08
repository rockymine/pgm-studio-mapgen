"""The grown ground of the red half: rock in beds that follow the surface, soil, the paint by slope, the river
and the pond, the falls into the rift, the island's underside, the biomes.

pgmvox.terrain.lay lays the columns and paints the top by slope (by_angle) with the rock in beds (Strata, beds).
What it cannot do is done here: a top that varies by place as well as slope (patches of andesite and coarse dirt
on a mid slope, a sandy lip by the river), a per-column underside (lay and underside both take one floor height),
the water, and the falls.
"""
import numpy as np

import plan as P
from pgmvox import B, rng
from pgmvox.noise import fbm
from pgmvox.terrain import Strata, beds, by_angle, lay


def world_grid(w, a, fill=0):
    """A red-half array as a world-shaped one (the world's x0 is the board's)."""
    out = np.full((w.sx, w.sz), fill, dtype=np.asarray(a).dtype)
    out[:a.shape[0], :] = a
    return out


def lay_ground(w, L):
    H = world_grid(w, L.H, -1)
    mask = world_grid(w, L.land, False)
    rock = Strata([((B.STONE, 0), 3, 6), ((B.STONE, 5), 1.4, 3)], length=60, seed=7, start=-300)
    # beds follow the ground: a column's beds are counted down from its own surface (offset = its height)
    deg = lay(w, H, mask, top=by_angle([(38, (B.GRASS, 0)), (55, (B.GRASS, 0)), (90, (B.STONE, 0))]),
              bands=beds(rock, H, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.04)], seed=3), dirt_depth=3, from_y=3)
    r = rng(P.BOARD, "ground")
    sh = (w.sx, w.sz)
    patch, patch2, cell = fbm(sh, 5, 2, seed=61), fbm(sh, 4, 2, seed=62), r.random(sh)
    bottom = world_grid(w, L.bottom, 0)
    water = world_grid(w, L.water, 0)
    d_river = world_grid(w, L.d_river, 99.0)
    for i, k in np.argwhere(mask):
        top = int(H[i, k])
        w.ids[i, :max(0, bottom[i, k]), k] = 0                  # the underside: nothing under the column's bottom
        w.dat[i, :max(0, bottom[i, k]), k] = 0
        a = deg[i, k]
        x = w.x0 + i
        if water[i, k] > 0:
            c = cell[i, k]
            still = x < -74 or water[i, k] == P.POND_LEVEL
            blk = ((B.CLAY, 0) if c < 0.3 else (B.SAND, 0) if c < 0.6 else (B.DIRT, 0)) if still else \
                  ((B.GRAVEL, 0) if c < 0.55 else (B.SAND, 0) if c < 0.8 else (B.STONE, 5))
            w.ids[i, top, k], w.dat[i, top, k] = blk
            w.ids[i, top + 1:water[i, k] + 1, k] = B.WATER
            w.dat[i, top + 1:water[i, k] + 1, k] = 0
            continue
        if 33 < a <= 38 and patch[i, k] > 0.35:                 # worn edge where the ground turns steep
            w.ids[i, top, k], w.dat[i, top, k] = B.DIRT, 1
        elif 38 < a <= 55:                                      # a mid slope: grass, rock or coarse dirt in patches
            pv = patch[i, k]
            if pv <= 0.15:
                w.ids[i, top, k], w.dat[i, top, k] = (B.STONE, 5 if cell[i, k] < 0.5 else 0) if pv > -0.25 else (B.DIRT, 1)
        elif a > 55:
            c = cell[i, k]
            w.ids[i, top, k], w.dat[i, top, k] = (B.STONE, 0) if c < 0.45 else (B.STONE, 5) if c < 0.8 else (B.COBBLE, 0)
        if d_river[i, k] < 5.2 and x > -75 and top <= P.RIVER_LEVEL + 2 and a < 38:
            w.ids[i, top, k], w.dat[i, top, k] = (B.SAND, 0) if patch2[i, k] > -0.1 else (B.GRAVEL, 0)
    # biomes: forest on the woods, river in the channel, plains elsewhere
    w.biome[:, :] = 1
    w.biome[world_grid(w, L.forest, False)] = 4
    w.biome[water > 0] = 7
    return deg


def falls(w, L):
    """The river spills over the lip: falling water down the rift face into the void."""
    for k in range(L.H.shape[1]):
        wet = np.nonzero(L.water[:, k] > 0)[0]
        if len(wet) == 0:
            continue
        i = wet.max()
        x, z = P.X_MIN + i, P.Z_MIN + k
        if x < -14:
            continue
        lvl = int(L.water[i, k])
        for xx in range(x + 1, -9):
            for y in range(8, lvl + 1):
                if w.id(xx, y, z) == 0:
                    w.set(xx, y, z, B.WATER_FLOW, 8)
