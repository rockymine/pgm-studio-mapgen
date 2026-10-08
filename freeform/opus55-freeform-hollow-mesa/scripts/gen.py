"""Generate Hollow Mesa: the land, the underground, the buildings and the dressing on the red half, then turn
it onto blue and write the volume for write_world.cs.

    python3 gen.py <build-dir> [--stage terrain|under|all]
"""
import argparse
import time

import numpy as np

import plan as P
from mc import World, B
from rotate import rotate_world
import terrain


def green_mask(L):
    """Where the board is green: the creek's banks on the canyon floor, the groves, the acacia flat."""
    g = (np.abs(L.X - L.cx) < 8) & (L.d < L.floor_edge)
    for key in ("grove", "acacias", "rancho"):
        p = dict((q["key"], q) for q in P.PLACES)[key]
        (x, z), r = p["at"], p["r"]
        g |= np.hypot(L.X - x, L.Z - z) < r + 4
    return g


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
    terrain.sky_arch(w, L)
    L.green = green_mask(L)
    terrain.paint_biomes(w, L, L.green)
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
    rotate_world(w)
    # blue flies blue: recolour the team wool the half-turn copied from red's fort
    sx0, sz0 = P.rot(-90, 22)
    sx1, sz1 = P.rot(-130, -16)
    sub = w.ids[sx0 - w.x0:sx1 - w.x0 + 1, 60:110, sz0 - w.z0:sz1 - w.z0 + 1]
    dsub = w.dat[sx0 - w.x0:sx1 - w.x0 + 1, 60:110, sz0 - w.z0:sz1 - w.z0 + 1]
    dsub[(sub == B.WOOL) & (dsub == 14)] = 11
    w.save(a.build, "Hollow Mesa", (0, 100, 0))
    np.save(f"{a.build}/heights_red.npy", L.H)
    print(f"saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
