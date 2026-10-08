"""Generate Cloudhaven: the islands for red's half, everything built on them, then the half-turn onto blue.

    python3 gen.py <build-dir> [--stage terrain|all]
"""
import argparse
import time

import numpy as np

import plan as P
from mc import World, B
from rotate import rotate_world
import terrain


def make(stage="all"):
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=128)
    F = terrain.Field()
    terrain.build(F)
    terrain.write(w, F)
    terrain.paint_biomes(w, F)
    if stage == "all":
        import buildings, dressing
        buildings.build(w, F)
        dressing.build(w, F)
    return w, F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build")
    ap.add_argument("--stage", default="all")
    a = ap.parse_args()
    t0 = time.time()
    w, F = make(a.stage)
    print(f"generated {time.time() - t0:.1f}s")
    rotate_world(w, F.red)
    # blue flies blue
    mask = (w.ids == B.WOOL) & (w.dat == 14) & (~F.red)[:, None, :]
    w.dat[mask] = 11
    w.save(a.build, "Cloudhaven", (0, 100, 0))
    np.save(f"{a.build}/heights.npy", F.H)
    print(f"saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
