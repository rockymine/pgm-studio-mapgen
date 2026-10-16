"""Generate Emberfrost: the ground (ground.py), then red's half dressed (dress.py), turned onto blue's across z = -0.5, the cores stamped
on both from the plan's objects and the island's ground marked for the void rule.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
import ground
from pgmvox import World
from pgmvox.core.orient import turn_world
from pgmvox.play.rules import mark_ground

SY = 128


def make():
    O = P.objectives()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    stats = {}
    deg, ice, fire, bottom = ground.lay_land(w, stats)
    ground.thaw(w, ice, fire, stats)
    ground.mirror_lake(w, stats)
    try:
        import dress
        dress.everything(w, deg, ice, fire, bottom, O, stats)
    except ImportError:
        pass
    turn_world(w, "mirror_z", w.grid()[1] < 0, recolour={(P.B.WOOL, 14): (P.B.WOOL, 11), (P.B.CARPET, 14): (P.B.CARPET, 11),
                                                       (P.B.STAINED_CLAY, 14): (P.B.STAINED_CLAY, 11)}, banners={1: 4})
    O.stamp(w)
    mark_ground(w)
    w.biome[:, :] = P.BIOME
    return w, stats


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Emberfrost", P.OBSERVER_AT)
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}")
