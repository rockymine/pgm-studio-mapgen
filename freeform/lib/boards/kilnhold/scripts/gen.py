"""Generate Kilnhold from the plan: red's half (z < 0) is built, then turned onto blue's with the half turn
(orient.turn_world "half", (x, z) -> (-1 - x, -1 - z)) with the team colours swapped, then the monuments are
stamped for both teams from the plan's objects.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import kit
import plan as P
import dress
import rooms
import terrain
import works
from pgmvox import B, World
from pgmvox.core.orient import turn_world
from pgmvox.play.rules import mark_ground


def make(verbose=True):
    t0 = time.time()
    L = terrain.land()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=P.SY)
    terrain.lay(w, L)
    stats = {}
    works.crater(w, L)
    works.facade(w)
    works.apron(w, L)
    works.tower(w, L)
    works.pit(w, L)
    stats["roads"] = works.crown_roads(w)
    works.deck(w, L)
    if verbose:
        print(f"ground and works {time.time() - t0:.1f}s")
    I, made = rooms.build(w)
    stats["interior"] = made
    if verbose:
        print(f"interior {time.time() - t0:.1f}s, {made['lined']} cells lined")
    dress.build(w, L, stats)
    if verbose:
        print(f"dressing {time.time() - t0:.1f}s: {stats['boulders']} boulders, {stats['trees']} bare trees")
    # the flag's banner, red's: the image gets blue's
    fx, fy, fz = P.FLAG_POST
    w.banner(fx, fy, fz, 1, rot=4)
    X, Z = w.grid()
    turn_world(w, "half", Z < 0, recolour=kit.RECOLOUR, banners={1: 4})
    O = P.objectives()
    O.stamp(w)
    mark_ground(w)
    if verbose:
        print(f"turned and stamped {time.time() - t0:.1f}s")
    return w, stats


if __name__ == "__main__":
    w, stats = make()
    w.save(sys.argv[1], "Kilnhold", (0, 90, 0))
    print(f"{int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
