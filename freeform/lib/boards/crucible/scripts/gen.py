"""Generate Crucible from the plan: the land laid for both halves, then red's foundry, its caves and what is made on
its surface, turned half round onto blue's, and the objectives stamped on both.

    python3 gen.py <build-dir>
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import bunker
import cave
import ground
import land
import plan as P
import surface
from pgmvox import B, World
from pgmvox.core.orient import turn_world
from pgmvox.play.rules import mark_ground

RECOLOUR = {(B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11), (B.STAINED_GLASS, 14): (B.STAINED_GLASS, 11),
            (B.WOOL, 14): (B.WOOL, 11), (B.CARPET, 14): (B.CARPET, 11)}


def generate():
    t0 = time.time()
    w = World(land.X0, land.Z0, land.NX, land.NZ, sy=128)
    H, deg = ground.lay(w)
    lip = ground.channel(w, H)
    print(f"ground {time.time() - t0:.0f}s", flush=True)
    C = bunker.build(w)
    cave.build(w, C)
    print(f"foundry {time.time() - t0:.0f}s", flush=True)
    surface.build(w, H, C, lip)
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)   # gravel over air would fall
    w.ids[:, 1:, :][loose] = B.STONE
    w.dat[:, 1:, :][loose] = 5
    void = np.broadcast_to(~land.inside()[:, None, :], w.ids.shape)
    w.ids[void] = B.AIR
    w.dat[void] = 0
    ins = land.inside()                                   # the lava sea walled in obsidian where it meets the void
    edge = np.zeros_like(ins)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        edge |= ins & ~np.roll(np.roll(ins, dx, 0), dz, 1)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    edge &= ins
    seal = edge[:, None, :] & np.isin(w.ids, [B.LAVA, B.LAVA_FLOW])
    w.ids[seal] = B.OBSIDIAN
    w.dat[seal] = 0
    X, Z = land.grid()
    turn_world(w, "half", land.red_mask(X, Z), recolour=RECOLOUR)
    P.objectives().stamp(w)
    mark_ground(w)
    print(f"done {time.time() - t0:.0f}s", flush=True)
    return w


if __name__ == "__main__":
    w = generate()
    w.save(sys.argv[1], "Crucible", (0, 92, -1))
    print("generated")
