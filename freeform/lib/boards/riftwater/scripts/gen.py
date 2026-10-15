"""Generate Riftwater: the land, the water, the underground, the buildings and the dressing, then mirror the
red half onto blue, mark the ground at y 0 for the void rule, and write the volume for write_world.cs.

    python3 gen.py <build-dir> [--stage terrain|all]
"""
import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from mc import World, B  # noqa: E402
from mirror import mirror_world  # noqa: E402
from pgmvox.play.rules import mark_ground  # noqa: E402
import terrain  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build")
    ap.add_argument("--stage", default="all")
    a = ap.parse_args()
    t0 = time.time()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=128)
    L = terrain.Land()
    terrain.build_heights(L)
    terrain.build_underside(L)
    terrain.write_land(w, L)
    terrain.write_falls(w, L)
    terrain.paint_biomes(w, L)
    print(f"terrain {time.time() - t0:.1f}s")
    if a.stage != "terrain":
        import underground
        underground.build(w, L)
        print(f"underground {time.time() - t0:.1f}s")
    if a.stage == "all":
        import buildings, dressing
        buildings.build(w, L)
        print(f"buildings {time.time() - t0:.1f}s")
        dressing.build(w, L)
        print(f"dressing {time.time() - t0:.1f}s")
    mirror_world(w)
    # blue's spawn flies blue: recolour the team wool the mirror copied from red's tower
    sub = w.ids[84 - w.x0:111 - w.x0, 50:90, -16 - w.z0:3 - w.z0]
    dsub = w.dat[84 - w.x0:111 - w.x0, 50:90, -16 - w.z0:3 - w.z0]
    dsub[(sub == B.WOOL) & (dsub == 14)] = 11
    print(f"ground marked under {mark_ground(w)} columns")
    spawn = (0, 90, 0)
    w.save(a.build, "Riftwater", spawn)
    np.save(f"{a.build}/heights_red.npy", L.H)
    print(f"saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
