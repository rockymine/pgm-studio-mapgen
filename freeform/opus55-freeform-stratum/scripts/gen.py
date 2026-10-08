"""Generate Stratum: the land, the city's fragments in it, the cloud sea, the city, all on red's half, then the
mirror onto blue.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from mc import World, B
from mirror import mirror_world
import terrain


def make():
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=128)
    F = terrain.Field()
    F.fragment_at = []
    terrain.build(F)
    terrain.write(w, F)
    terrain.fragments(w, F)
    import dressing, buildings
    dressing.build(w, F)
    buildings.build(w, F)
    F.cloud_blocks = terrain.clouds(w, F)
    w.biome[:, :] = 1
    return w, F


def main(build):
    t0 = time.time()
    w, F = make()
    print(f"generated {time.time() - t0:.1f}s, {F.cloud_blocks} blocks of cloud on red's half")
    mirror_world(w)
    for team_block in (B.WOOL, B.STAINED_CLAY):
        m = (w.ids == team_block) & (w.dat == 14) & (~F.red)[:, None, :]
        w.dat[m] = 11
    w.save(build, "Stratum", (0, 100, 0))
    np.save(f"{build}/heights.npy", F.H)
    print(f"saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
