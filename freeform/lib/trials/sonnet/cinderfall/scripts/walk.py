"""Read Cinderfall back from the built world: each spawn walked to its own core's plinth and to the enemy's, the
ridge and its beacon (ladder to the top), the vent tube from the pit to the blowhole, how much of the island's land
is reached, every objective checked, every block's footing.

    python3 walk.py <build-dir>

The walk opens doors (pgmvox.walk's PASSABLE has none), takes a drop of at most three and no running jumps.
"""
import sys

import numpy as np

import plan as P
from pgmvox import World, audit, walk
from pgmvox import blocks as K

w = World.load(sys.argv[1])
ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0
rules = walk.MoveRules(max_drop=3, jumps=False)
O = P.objectives()
L = P.land()


def reach(d, x, y, z, r=2):
    n = walk.nearest(d, w.x0, w.z0, x, y, z, r)
    return "not reached" if n is None else f"{n}"


problems = O.check(w)
print(f"objectives with a problem (Objectives.check): {len(problems)}")
for p in problems:
    print("   ", p)
foot = audit.footing(w)
print(f"footing problems (audit.footing): {len(foot)}")
for f in foot[:8]:
    print("   ", f)
cx, cz = P.CORE_AT
red = P.SPAWN
blue = (int(P.SYM.point(red[0], red[2])[0]), red[1], int(P.SYM.point(red[0], red[2])[1]))
for team, start in (("red", red), ("blue", blue)):
    d = walk.walk(ids, [start], w.x0, w.z0, rules)
    own = (cx, cz) if team == "red" else tuple(int(v) for v in P.SYM.point(cx, cz))
    other = tuple(int(v) for v in P.SYM.point(*own))
    print(f"{team} spawn at {start}: {int((d >= 0).sum())} places reached")
    print(f"  to its own core's plinth, its edge: {reach(d, own[0] + (5 if team == 'blue' else -5), P.PLINTH_Y + 1, own[1], 2)}")
    print(f"  to the plinth's centre: {reach(d, own[0], P.PLINTH_Y + 1, own[1], 1)}")
    print(f"  to the enemy's plinth's centre: {reach(d, other[0], P.PLINTH_Y + 1, other[1], 1)}")
    bx0, bz0, bx1, bz1 = P.BEACON
    if team == "red":
        print(f"  to the beacon's door: {reach(d, (bx0 + bx1) // 2, P.BEACON_Y + 1, bz1 + 1, 1)}")
        print(f"  to the beacon's top (by its ladder): {reach(d, (bx0 + bx1) // 2, P.BEACON_Y + 13, (bz0 + bz1) // 2, 2)}")
    reached = (d.max(axis=1) >= 0) & L.land
    print(f"  land columns reached: {int(reached.sum())} of {int(L.land.sum())} "
          f"({reached.sum() / L.land.sum():.0%}; the rest: the lava, sheer faces, and the tube's ceiling)")
(px, pz), py, _ = P.PIT
d = walk.walk(ids, [(px, py + 1, pz)], w.x0, w.z0, rules)
(bx, bz), by, _ = P.BLOWHOLE
print(f"from the Cinder Pit's floor {(px, py + 1, pz)}:")
print(f"  to the blowhole's floor: {reach(d, bx, by + 1, bz, 1)}")
print(f"  out of the blowhole onto the plain: {reach(d, bx - 9, P.at(L, bx - 9, bz) + 1, bz, 2)}")
print(f"  to red's plinth through the tube: {reach(d, cx - 5, P.PLINTH_Y + 1, cz, 2)}")
