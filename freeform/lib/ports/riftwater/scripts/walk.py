"""Read Riftwater back from the built world: each spawn walked to its own monuments and to the mine adit, the
enemy's monuments out of reach on foot, the cave walked from the ledge behind the falls to its three ways up,
every objective checked, and every block's footing.

    python3 walk.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from pgmvox import World, audit, walk
from pgmvox import blocks as K

t0 = time.time()
w = World.load(sys.argv[1])
# pgmvox's PASSABLE has no doors in it, so its walk stops at every door: walk a copy with the doors open
ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0
# jumps off: pgmvox.walk is a breadth-first search, and a jump costs more than one move, so with jumps on the
# distances depend on the queue's order (red and blue come out different on a mirrored board)
rules = walk.MoveRules(max_drop=3, jumps=False)


def reach(dist, x, y, z, r=2):
    n = walk.nearest(dist, w.x0, w.z0, x, y, z, r)
    return "not reached" if n is None else f"{n}"


red = P.SPAWN
blue = (P.SYM.point(red[0], red[2])[0], red[1], red[2])
for team, start in (("red", red), ("blue", blue)):
    d = walk.walk(ids, [start], w.x0, w.z0, rules)
    print(f"{team} spawn at {start}:")
    for key, ((x, z), g, name) in P.MONUMENTS.items():
        own = (x, z) if team == "red" else P.SYM.point(x, z)
        other = P.SYM.point(*own)
        print(f"  to its own {key} monument: {reach(d, own[0], g + 1, own[1])}")
        print(f"  to the enemy's {key} monument, on foot: {reach(d, other[0], g + 1, other[1])}")
    ax, ay, az = P.MINE[0]
    adit = (ax, ay, az - 3) if team == "red" else (P.SYM.point(ax, az - 3)[0], ay, az - 3)
    print(f"  to the mine adit: {reach(d, *adit)}")
    sh = P.SHAFT if team == "red" else P.SYM.point(*P.SHAFT)
    print(f"  to the gallery under the headframe, down the shaft's ladder: {reach(d, sh[0], 45, sh[1])}")
print(f"[{time.time() - t0:.0f}s]")

d = walk.walk(ids, [(-11, 36, 6)], w.x0, w.z0, rules)
print("from the ledge behind red's falls (36):")
(sx, sz), floor, _ = P.SINKHOLE
print(f"  to the sinkhole floor: {reach(d, sx, floor + 1, sz)}")
print(f"  out of the sinkhole onto the field: {reach(d, sx - 10, P.at(P.land(), sx - 10, sz) + 1, sz, 1)}")
print(f"  to the gaol cellar: {reach(d, -52, P.CELLAR[1], -32)}")
print(f"  up the gaol ladder into the gaol: {reach(d, -52, 53, -34)}")
x, y, z = P.MINE[-1]
print(f"  to the mine breakthrough: {reach(d, x, y, z)}")
print(f"  to red's spawn, through the mine: {reach(d, *red)}")
sx_, sz_ = P.SHAFT
g = P.at(P.land(), sx_, sz_)
print(f"  up the shaft's ladder onto the headframe's collar: {reach(d, sx_, g + 1, sz_ + 3, 1)}")
print(f"[{time.time() - t0:.0f}s]")

jr = walk.MoveRules(max_drop=3, jumps=True)
sq = []
for start, mx in ((red, -66), (blue, 65)):
    dj = walk.walk(ids, [start], w.x0, w.z0, jr)
    sq.append(f"{reach(dj, mx, 53, -44)} / {reach(dj, mx, 51, 48)}")
print(f"with running jumps on, square / green: red {sq[0]}, blue {sq[1]} (the same board mirrored)")
print(f"[{time.time() - t0:.0f}s]")

problems = P.objectives().check(w)
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
f = audit.footing(w)
print("footing problems:", len(f))
kinds = {}
for x, y, z, why in f:
    kinds.setdefault(why, []).append((x, y, z))
for why, cells in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
    print(f"   {len(cells):4d}  {why}  e.g. {cells[:3]}")
