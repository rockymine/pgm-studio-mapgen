"""The grown ground of the red half: rock in beds that follow the surface, soil, the paint by slope, the river
and the pond, the falls into the rift, the island's underside, the biomes.

pgmvox.terrain.lay lays the columns with the rock in beds (Strata, beds), paints the top by slope and place
(Paint layers: patches of andesite and coarse dirt on a mid slope, a sandy lip by the river) and leaves nothing
under each column's own underside; fill_water lays the beds and the water. The falls are done here.
"""
import numpy as np

import plan as P
from pgmvox import B, rng
from pgmvox.noise import fbm
from pgmvox.terrain import Paint, Strata, beds, by_angle, fill_water, lay


def world_grid(w, a, fill=0):
    """A red-half array as a world-shaped one (the world's x0 is the board's)."""
    out = np.full((w.sx, w.sz), fill, dtype=np.asarray(a).dtype)
    out[:a.shape[0], :] = a
    return out


def lay_ground(w, L):
    H = world_grid(w, L.H, -1)
    mask = world_grid(w, L.land, False)
    rock = Strata([((B.STONE, 0), 3, 6), ((B.STONE, 5), 1.4, 3)], length=60, seed=7, start=-300)
    r = rng(P.BOARD, "ground")
    sh = (w.sx, w.sz)
    patch, patch2, cell = fbm(sh, 5, 2, seed=61), fbm(sh, 4, 2, seed=62), r.random(sh)
    water = world_grid(w, L.water, 0)
    X = w.x0 + np.arange(w.sx)[:, None] + np.zeros(sh, int)
    lip = (world_grid(w, L.d_river, 99.0) < 5.2) & (X > -75) & (H <= P.RIVER_LEVEL + 2)
    paint = [
        Paint((B.SAND, 0), slope=(None, 37), where=lip, values=[(patch2, -0.1, None)]),   # a sandy lip by the river
        Paint((B.GRAVEL, 0), slope=(None, 37), where=lip),
        Paint((B.DIRT, 1), slope=(33, 38), values=[(patch, 0.35, None)]),     # worn edge where the ground turns steep
        Paint((B.STONE, 5), slope=(38, 55), values=[(patch, -0.25, 0.15), (cell, None, 0.5)]),   # mid-slope patches
        Paint((B.STONE, 0), slope=(38, 55), values=[(patch, -0.25, 0.15)]),
        Paint((B.DIRT, 1), slope=(38, 55), values=[(patch, None, -0.25)]),
        Paint((B.STONE, 0), slope=(55, None), values=[(cell, None, 0.45)]),   # cliffs: stone, andesite, cobble
        Paint((B.STONE, 5), slope=(55, None), values=[(cell, None, 0.8)]),
        Paint((B.COBBLE, 0), slope=(55, None)),
    ]
    # beds follow the ground: a column's beds are counted down from its own surface (offset = its height)
    deg = lay(w, H, mask, top=by_angle([(38, (B.GRASS, 0)), (55, (B.GRASS, 0)), (90, (B.STONE, 0))]),
              bands=beds(rock, H, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.04)], seed=3), from_y=3,
              paint=paint, bottom=world_grid(w, L.bottom, 0))
    still = (X < -74) | (water == P.POND_LEVEL)
    fill_water(w, H, water, mask=mask, bed=[
        Paint((B.CLAY, 0), where=still, values=[(cell, None, 0.3)]),         # the pond and the mill race: clay, sand, dirt
        Paint((B.SAND, 0), where=still, values=[(cell, None, 0.6)]),
        Paint((B.DIRT, 0), where=still),
        Paint((B.GRAVEL, 0), values=[(cell, None, 0.55)]),                   # the river: gravel, sand, andesite
        Paint((B.SAND, 0), values=[(cell, None, 0.8)]),
        Paint((B.STONE, 5)),
    ])
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
