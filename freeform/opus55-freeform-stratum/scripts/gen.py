"""Generate Stratum: the city on red's half, mirrored onto blue; then the land, the city's fragments in it,
the woods and the cloud sea over the whole board, with no symmetry: nobody plays on them.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from mc import World, B
from mirror import mirror_world
import terrain


def make(mirror=False):
    """The city on red's half, mirrored; then the land, the pylons, the fragments, the woods and the clouds over
    the whole board, unsymmetric. Without `mirror` (the audit), the city stays on red's half only."""
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=128)
    F = terrain.Field()
    F.fragment_at = []
    terrain.build(F)
    import dressing, buildings
    buildings.build(w, F)
    if mirror:
        mirror_world(w)
        for team_block in (B.WOOL, B.STAINED_CLAY):
            m = (w.ids == team_block) & (w.dat == 14) & (~F.red)[:, None, :]
            w.dat[m] = 11
    terrain.write(w, F)
    buildings.pylons(w, F)
    terrain.fragments(w, F)
    dressing.build(w, F)
    F.cloud_blocks = terrain.clouds(w, F)
    w.biome[:, :] = 1
    return w, F


def main(build):
    t0 = time.time()
    w, F = make(mirror=True)
    print(f"generated {time.time() - t0:.1f}s, {F.cloud_blocks} blocks of cloud over the board")
    w.save(build, "Stratum", (0, 100, 0))
    np.save(f"{build}/heights.npy", F.H)
    print(f"saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
