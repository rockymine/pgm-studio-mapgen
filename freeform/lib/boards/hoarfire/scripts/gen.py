"""Generate Hoarfire from land.py and plan.py: the ground of the whole board, Rowan's dressing (z < 0) mirrored onto
Sloe's half with the team colours swapped, then the objectives stamped on both halves and the ground marked at y 0.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import ground
import plan as P
from pgmvox import B, World, rng
from pgmvox.core.orient import turn_world
from pgmvox.play.rules import mark_ground

SY = 100
TEAM_SWAP = {(B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11), (B.STAINED_GLASS, 14): (B.STAINED_GLASS, 11), (B.STAINED_PANE, 14): (B.STAINED_PANE, 11)}


def make():
    R = P.build()
    O = P.objectives()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    stats = {}
    deg, wint = ground.lay(w, R, rng(P.BOARD, "ground"))
    ground.water(w)
    try:
        import dress
        dress.everything(w, R, deg, wint, O, stats)
    except ImportError:
        pass
    turn_world(w, "mirror_z", P.Z < 0, recolour=TEAM_SWAP, banners={1: 4})
    O.stamp(w)
    stats["marked"] = mark_ground(w)
    return w, stats


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Hoarfire", P.OBSERVER_AT)
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
