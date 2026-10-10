"""Generate Abbeymoor from land.py and plan.py: red's half (z < 0) is built, then turned onto blue's (orient.turn_world "half",
(x, z) -> (-1 - x, -1 - z)) with the team colours swapped; the monuments are stamped on both halves from the plan's objects.

The ground is land.py's heights exactly: rock in tilted beds from y 2 to the surface, bedrock at y 1, soil by slope, the paint by place
(heather, podzol, coarse dirt, the bog's dark ground, roads, flagstones), water in the pools and the beck, then what stands on it
(dress.py) and what is cut under it (crypt.py).

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import crypt
import dress
import plan as P
from pgmvox import B, World, noise, rng
from pgmvox import forms
from pgmvox import terrain as T
from pgmvox.orient import turn_world
from pgmvox.shapes import edge_depth

SY = 128


def red_cols(w):
    _, Z = w.grid()
    return Z < 0


def strata():
    return T.Strata([((B.STONE, 0), 3, 4), ((B.STONE, 5), 2.5, 3), ((B.COBBLE, 0), 1, 2), ((B.STONE, 6), 1, 2),
                     ((B.COAL_ORE, 0), 0.15, 1), ((B.DIRT, 0), 0.4, 1)], seed=17, start=1)


def rock(w, r):
    """Rock in beds from y 2 to the ground's top, soil by slope, bedrock at y 1: the whole island, both halves at once (the
    ground is symmetric), then the rim cut back in ledges and mossed."""
    H, LAND = P.H, P.LAND
    beds = strata()
    offset = T.bed_offset(H.shape, dip=(0.05, -0.03), fold=3, cell=18, seed=5)
    fill = T.beds(beds, offset, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.05), ((B.STONE, 5), (B.STONE, 6), 0.05)], seed=6)
    deg = T.lay(w, H, mask=LAND, top=lambda d, h: (B.GRASS, 0), under=(B.DIRT, 0), bands=fill, from_y=2)
    w.ids[:, 1, :][LAND] = B.BEDROCK
    w.ids[:, 0, :][LAND] = 36                                   # block 36 at y 0: a player may build over the island
    return deg


def make():
    R = P.build()
    O = P.objectives()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    stats = {}
    r = rng(P.BOARD, "rock")
    deg = rock(w, r)
    stats["steep"] = int((deg > 45).sum())
    forms.skirt(w, P.LAND, P.H, lambda y: (B.STONE, 5 if y % 3 else 0), rng(P.BOARD, "skirt"), moss=0.12, grass=0.2)
    dress.surface(w, R, deg, rng(P.BOARD, "surface"), stats)
    dress.water(w, stats)
    crypt.carve_all(w, R, rng(P.BOARD, "crypt"), stats)
    dress.everything(w, R, deg, O, stats)
    turn_world(w, "half", red_cols(w),
               recolour={(B.CARPET, 14): (B.CARPET, 11), (B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11), (B.WOOL, 14): (B.WOOL, 11)},
               banners={1: 4})
    O.stamp(w)
    w.biome[:, :] = P.BIOME
    return w, stats


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Abbeymoor", P.OBSERVER_AT)
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}")
