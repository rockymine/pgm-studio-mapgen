"""The roads: a stroke through a few points, wandering between them, laid as three tones of one family. Warm granite with brick in
strips through the orchard and the fire lane, grey andesite and gravel on the ice lane, nether brick strips where a road enters the
Caldera. A road is a claim on the ground: trees and props keep off it."""
import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.geom.shapes import polyline
from util import claim_cells, wander

ROADS = {
    "Drove Road": [(0, -76), (2, -68), (-1, -58), (2, -49), (-4, -44), (-7, -37), (-5, -28), (-1, -20), (0, -15)],
    "Frost Road": [(-13, -79), (-23, -71), (-29, -62), (-29, -56)],
    "Frost Way": [(-35, -44), (-35, -36), (-37, -30), (-40, -23), (-41, -16)],
    "Ledger Lane": [(-2, -52), (-13, -52), (-22, -52), (-26, -50)],
    "Ember Road": [(13, -78), (14, -68), (18, -61), (24, -60), (27, -60)],
    "Cinder Road": [(5, -46), (16, -45), (28, -40), (38, -37), (41, -35), (41, -46)],
    "Brimstone Way": [(41, -35), (41, -26), (40, -17)],
}
WIDTH = {"Drove Road": 5, "Ember Road": 4, "Cinder Road": 4, "Brimstone Way": 4, "Frost Road": 4, "Frost Way": 4, "Ledger Lane": 3}


def lay(w, rng, stats):
    ice, fire = land.zones(P.X, P.Z)
    total = 0
    for name, pts in ROADS.items():
        pts = wander(pts, rng, step=7, amp=1.6) if name not in ("Brimstone Way",) else pts
        x0 = int(min(p[0] for p in pts)) - 4
        x1 = int(max(p[0] for p in pts)) + 4
        z0 = int(min(p[1] for p in pts)) - 4
        z1 = int(max(p[1] for p in pts)) + 4
        X, Z = np.meshgrid(np.arange(x0, x1 + 1), np.arange(z0, z1 + 1), indexing="ij")
        d, s = polyline(X.astype(float), Z.astype(float), pts)
        half = WIDTH[name] / 2
        cells = []
        for i, k in np.argwhere(d <= half + 0.6):
            x, z = int(X[i, k]), int(Z[i, k])
            gi, gk = x - P.X_MIN, z - P.Z_MIN
            if not (0 <= gi < P.H.shape[0] and 0 <= gk < P.H.shape[1]) or not P.LAND[gi, gk] or z >= -1:
                continue
            if d[i, k] > half and rng.random() < 0.5:
                continue
            y = int(P.H[gi, gk])
            if w.id(x, y, z) in (B.WATER, B.LAVA, B.ICE, B.AIR, B.OBSIDIAN):
                continue
            iz, fz = ice[gi, gk], fire[gi, gk]
            stripe = int(s[i, k] // 3) % 5 == 0
            u = rng.random()
            if iz > 0.4:
                blk = (B.GRAVEL, 0) if u < 0.4 else (B.STONE, 5) if u < 0.7 else (B.STONE, 6) if u < 0.88 else (B.COBBLE, 0)
            elif fz > 0.5:
                blk = (B.NETHER_BRICK, 0) if stripe else (B.STONE, 1) if u < 0.6 else (B.STONE, 2) if u < 0.85 else (B.HARDENED_CLAY, 0)
            else:
                blk = (B.BRICK, 0) if stripe else (B.STONE, 1) if u < 0.62 else (B.STONE, 2) if u < 0.88 else (B.DIRT, 1)
            w.set(x, y, z, *blk)
            if w.id(x, y + 1, z) in (B.TALLGRASS, B.DEADBUSH, B.FLOWER, B.SNOW_LAYER):
                w.set(x, y + 1, z, B.AIR)
            cells.append((x, z))
        claim_cells(cells, 0)
        total += len(cells)
    stats["road blocks"] = total
