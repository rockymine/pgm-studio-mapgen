"""Generate Lantern Karst: red's half (z < 0) is built, then turned half a circle onto blue's; the mist
under the board is laid over both halves afterward, with no symmetry.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import buildings
import plan as P
import terrain as T
from mc import World, B
from rotate import rotate_world

# what each room holds and each monument waits for. Red's rooms hold lime and yellow; blue's, turned from red's,
# are recoloured magenta and orange. Red's monuments wait for blue's colours, blue's for red's.
RED_ROOMS = {"pillar": 5, "store": 4}
BLUE_ROOMS = {"pillar": 2, "store": 1}
RED_MONUMENTS = [2, 1]          # at P.MONUMENTS[0] (west) and [1] (east): blue's Pillar, blue's Store
BLUE_MONUMENTS = [5, 4]         # at their turns: red's Pillar, red's Store


def make():
    w = World(P.X_MIN, P.Z_MIN, T.NX, T.NZ, sy=128)
    F = T.Field()
    rng = np.random.default_rng(7)
    T.write(w, F)
    buildings.build(w, F, rng)
    T.joins(w, F)
    n_red = T.markers(w, F)
    n_vine = T.vines(w, F, rng)
    for k, (m, c) in enumerate(zip(P.MONUMENTS, RED_MONUMENTS)):
        w.set(int(np.floor(m["at"][0])), 70, int(np.floor(m["at"][1])), B.STAINED_CLAY, c)
    rotate_world(w, T.RED)
    blue = ~T.RED
    # recolour blue's half: banners, room wools, monument pedestals
    m = (w.ids == B.WOOL) & (w.dat == 14) & blue[:, None, :]
    w.dat[m] = 11
    for room, wl in zip(("pillar", "store"), P.WOOLS):
        x, z = P.rot(int(np.floor(wl["at"][0])), int(np.floor(wl["at"][1])))
        w.set(x, wl["y"], z, B.WOOL, BLUE_ROOMS[room])
    for mo, c in zip(P.MONUMENTS, BLUE_MONUMENTS):
        x, z = P.rot(int(np.floor(mo["at"][0])), int(np.floor(mo["at"][1])))
        w.set(x, 70, z, B.STAINED_CLAY, c)
    n_spires = T.spires(w, np.random.default_rng(31))
    n_mist = T.mist(w)
    w.biome[:, :] = 3                              # extreme hills: the cool green of a misty karst
    return w, F, dict(redstone=n_red, vines=n_vine, mist=n_mist, spires=n_spires)


def main(build):
    t0 = time.time()
    w, F, n = make()
    print(f"generated {time.time() - t0:.1f}s: {n}")
    w.save(build, "Lantern Karst", (0, 90, 0))
    print(f"saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
