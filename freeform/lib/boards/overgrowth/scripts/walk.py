"""Read Overgrowth back from the built world: each spawn walked to the enemy's, by the lanes the plan measured, the
tunnel and its heart ladders up to the chamber, the watchtowers' ladders, the bridges; every objective checked, every
block's footing.

    python3 walk.py <build-dir>

The walk opens doors, takes a drop of at most three and no running jump; its steps are four-way, so its numbers run
above the plan's octile ones.
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
problems = O.check(w)
print(f"objectives with a problem (Objectives.check): {len(problems)}")
for p in problems:
    print("   ", p)
foot = audit.footing(w)
print(f"footing problems (audit.footing): {len(foot)}")
for f in foot[:8]:
    print("   ", f)


def reach(d, x, y, z, r=2):
    n = walk.nearest(d, w.x0, w.z0, x, y, z, r)
    return "not reached" if n is None else f"{n}"


red = P.SPAWN_AT
blue = (int(P.SYM.point(red[0], red[2])[0]), red[1], int(P.SYM.point(red[0], red[2])[1]))
for team, start in (("red", red), ("blue", blue)):
    d = walk.walk(ids, [start], w.x0, w.z0, rules)
    other = blue if team == "red" else red
    print(f"{team} spawn {start}: {int((d >= 0).sum())} places reached")
    print(f"  to the enemy's spawn: {reach(d, other[0], other[1], other[2], 1)}")
    if team == "red":
        print(f"  to the ziggurat's top tier, the chamber's door: {reach(d, 2, 74, 0, 2)}")
        print(f"  to the tunnel's crossing (the H): {reach(d, 0, 62, -2, 2)}")
        print(f"  up the heart ladder into the chamber: {reach(d, 0, 74, 0, 1)}")
        for box in P.TOWERS:
            x0, z0, x1, z1 = box
            print(f"  up the tower at {(x0 + x1) // 2, (z0 + z1) // 2}: {reach(d, (x0 + x1) // 2, P.TOWER_TOP + 1, (z0 + z1) // 2, 1)}")
        print(f"  across the north bridge at x {P.BRIDGES_X[0]} to the terrace: {reach(d, P.BRIDGES_X[0], 65, -37, 1)}")
        print(f"  across the south bridge at x {P.BRIDGES_X[1]} to the terrace: {reach(d, P.BRIDGES_X[1], 65, 36, 1)}")
    for side, x0, z0, x1, z1 in P.GATES:
        cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
        if team == "red":
            print(f"  to the {side} gate: {reach(d, cx, P.COURT_Y + 1, cz, 1)}")
