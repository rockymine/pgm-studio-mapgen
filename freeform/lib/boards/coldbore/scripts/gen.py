"""Generate Coldbore from the plan: red's half laid in order — the ground, the snowfield's dressing, the station
inside the mountain, the cave, the station on the plateau — then turned half round onto blue's, and the objectives
stamped on both.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import bunker
import cave
import ground
import land
import plan as P
import station
import surface
from pgmvox import B, World
from pgmvox.core.orient import turn_world
from pgmvox.play.rules import mark_ground

RECOLOUR = {(B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11), (B.STAINED_GLASS, 14): (B.STAINED_GLASS, 11),
            (B.WOOL, 14): (B.WOOL, 11)}


def generate():
    t0 = time.time()
    w = World(land.X0, land.Z0, land.NX, land.NZ, sy=128)
    top, deg, scorched = ground.lay(w)
    ground.crevasse_ice(w, top)
    print(f"ground {time.time() - t0:.0f}s", flush=True)
    surface.build(w, top)
    air = bunker.build(w, top)
    print(f"station {time.time() - t0:.0f}s", flush=True)
    cave.build(w, top, air)
    station.build(w)
    surface.pylons(w)
    print(f"cave and plateau {time.time() - t0:.0f}s", flush=True)
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)   # gravel over air would fall: andesite
    w.ids[:, 1:, :][loose] = B.STONE
    w.dat[:, 1:, :][loose] = 5
    X, Z = land.grid()
    turn_world(w, "half", land.red_mask(X, Z), recolour=RECOLOUR)
    P.objectives().stamp(w)
    mark_ground(w)
    print(f"done {time.time() - t0:.0f}s", flush=True)
    return w


if __name__ == "__main__":
    w = generate()
    w.save(sys.argv[1], "Coldbore", (0, 112, -1))
    print("generated")
