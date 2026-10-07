"""Generate Riftwater: the land, the water, the underground, the buildings and the dressing, then mirror the
red half onto blue and write the volume for write_world.cs.

    python3 gen.py <build-dir> [--stage terrain|all]
"""
import argparse
import time

import numpy as np

import plan as P
from mc import World, B
from mirror import mirror_world
import terrain


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
    spawn = (0, 90, 0)
    w.save(a.build, "Riftwater", spawn)
    np.save(f"{a.build}/heights_red.npy", L.H)
    print(f"saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
