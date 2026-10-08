"""Generate the Vale from land.py: the ground laid by slope as the studio reads it, rock in tilted beds, water,
the road, and the floating island."""
import sys

import numpy as np

from land import ISLAND, ROAD, SEA, ground
from pgmvox import B, World, terrain as T
from pgmvox.shapes import polyline

X, Z, H, river, sea, road = ground()
w = World(-100, -100, 200, 200, sy=128)
beds = T.Strata([((B.STONE, 0), 0.35, 4), ((B.STONE, 5), 0.2, 3), ((B.HARDENED_CLAY, 0), 0.15, 2),
                 ((B.STAINED_CLAY, 8), 0.12, 2), ((B.STAINED_CLAY, 1), 0.08, 1), ((B.STONE, 3), 0.1, 2)],
                seed=11, start=34)
offset = T.bed_offset(H.shape, dip=(0.04, -0.02), fold=3, seed=5)
top = T.by_angle([(30, (B.GRASS, 0)), (42, (B.DIRT, 1)), (55, (B.STONE, 5)), (90, (B.STONE, 0))])
deg = T.lay(w, H, top=top, bands=T.beds(beds, offset, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.04)], seed=6),
            dirt_depth=3, snow_above=92)
road_d, _ = polyline(X, Z, ROAD)
for i, k in np.argwhere(road_d <= 2):
    w.set(int(X[i, k]), int(H[i, k]), int(Z[i, k]), B.GRAVEL)
for water in (sea, river):
    for i, k in np.argwhere(water.mask):
        x, z = int(X[i, k]), int(Z[i, k])
        for y in range(int(H[i, k]) + 1, int(water.surface[i, k]) + 1):
            w.set(x, y, z, B.WATER)
        if water is sea or H[i, k] <= SEA:
            w.set(x, int(H[i, k]), z, B.SAND)
beach = (H <= SEA + 2) & (H > SEA) & ~sea.mask
for i, k in np.argwhere(beach):
    w.set(int(X[i, k]), int(H[i, k]), int(Z[i, k]), B.SAND)

(cx, cz), r, y = ISLAND
isl = np.hypot(X - cx, Z - cz) < r
T.lay(w, np.where(isl, y, 0), mask=isl, top=top, dirt_depth=2, from_y=y - 2)
T.underside(w, isl, y - 2, depth=T.root_depth(isl, cone=2.6, flutes=4, spires=12, seed=8),
            paint=lambda k, x, z: beds(y - k - int(offset[x + 100, z + 100])))
w.save(sys.argv[1], "Vale", (0, 80, 0))
print(f"generated; slope: {int((deg <= 30).sum())} grass-flat, {int((deg > 55).sum())} cliff columns; "
      f"{len(river.falls)} falls")
