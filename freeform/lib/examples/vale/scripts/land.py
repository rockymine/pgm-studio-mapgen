"""The Vale: the library's terrain example, every landform on one stretch of ground. The numbers are this board's.

    a coast all round an irregular outline, the sea at 30
    a scarp across the north, lifting the uplands 18; a butte and a spire on them
    a canyon cut down through the scarp, with ledges; a river from its mouth to the sea, in reaches and falls
    a road graded to 1 in 7 from the west shore up onto the uplands
    a hillside cut into terraces three blocks apart
    a floating island over the west with a fluted, spired underside
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import landform as L, noise  # noqa: E402

X0, Z0, N = -100, -100, 200
SEA = 30
OUTLINE = [(-92, -96), (-20, -98), (60, -94), (95, -70), (93, 10), (80, 70), (40, 92), (-30, 90), (-88, 70),
           (-96, 0)]
CANYON = [(-4, -78), (0, -62), (-8, -42)]
RIVER = [(-8, -42), (6, -10), (30, 20), (48, 55), (58, 95)]
ROAD = [(-86, 30), (-50, 12), (-20, -10), (20, -32), (60, -55)]
TERRACES = ((-45, 52), 20)
BUTTE = ((45, -74), 11, 82)
SPIRE = ((-55, -78), 7, 104)
ISLAND = ((-62, -20), 16, 96)


def ground():
    """Heights over the world, and what each landform left: the river's water, the sea, the road's level."""
    X, Z = np.meshgrid(np.arange(X0, X0 + N), np.arange(Z0, Z0 + N), indexing="ij")
    H = 44 + 14 * noise.fbm(X.shape, 48, 4, seed=3) + 6 * noise.ridged(X.shape, 24, 3, seed=4) - 0.08 * Z
    H = L.scarp(H, X, Z, [(-100, -52), (100, -40)], 18, side=-1, cliff=3, talus=8, reach=70)
    H = L.butte(H, X, Z, *BUTTE[:1], r=BUTTE[1], top=BUTTE[2], seed=1)
    H = L.spire(H, X, Z, SPIRE[0], r=SPIRE[1], top=SPIRE[2], seed=2)
    hill = np.hypot(X - TERRACES[0][0], Z - TERRACES[0][1]) < TERRACES[1]
    H = L.spire(H, X, Z, TERRACES[0], r=TERRACES[1], top=66, taper=0.8, jag=0.05, seed=3)   # a round hill
    H = L.terraces(H, hill, step=3)                                                         # cut into steps
    H, sea = L.coast(H, X, Z, SEA, outline=OUTLINE, shelf=24, depth=8)                      # the sea first
    H = L.canyon(H, X, Z, CANYON, width=22, depth=16, floor=0.3, wall=3, ledges=3, downhill=True, lowest=SEA + 2)
    H, road = L.grade(H, X, Z, ROAD, width=4, max_grade=1 / 7, shoulder=4)
    H, river = L.watercourse(H, X, Z, RIVER, width=6, depth=2, bank=4, fall_min=2, reach_min=12, lowest=SEA - 2)
    return X, Z, np.round(H).astype(int), river, sea, road
