"""Read Whitecliff Cistern back from the built world: each spawn walked to each hill's pad, the ways onto the Cistern
(its stairwells, the oculus's drop, the undercroft), the garden's gates and steps, the boatyard's ramps, the roofs;
every objective checked, every block's footing.

    python3 walk.py <build-dir>

The walk opens doors, drops at most three (the oculus is walked from the court floor, a drop of six, with the limit
lifted) and takes no running jump; its steps are four-way, so its numbers run above the plan's octile ones.
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
    print(f"{team} spawn {start}: {int((d >= 0).sum())} places reached")
    for key, name, box, pts in P.HILLS:
        cx, cz = (box.x0 + box.x1) // 2, (box.z0 + box.z1) // 2
        print(f"  to {name}'s pad: {reach(d, cx, box.y0 + 1, cz, 1)}")
    if team == "red":
        print(f"  to the court's floor: {reach(d, 0, P.COURT + 1, 8, 1)}")
        print(f"  to the roofs, up Sailmakers' Row: {reach(d, -33, P.ROOF + 1, -13, 1)}")
        print(f"  across the plank walk to Net Lofts' roof: {reach(d, -33, P.ROOF + 1, 8, 1)}")
# the oculus: a drop of six from the court's floor onto the cistern's pad, walked with the limit lifted
d = walk.walk(ids, [(-4, P.COURT + 1, 0)], w.x0, w.z0, walk.MoveRules(max_drop=None, jumps=False))
print(f"from the court's floor beside the oculus, falling: the Cistern's pad {reach(d, 0, P.VAULT + 1, 0, 1)}")
d = walk.walk(ids, [(-6, P.COURT + 1, -10)], w.x0, w.z0, rules)
print(f"from the north-west stairwell's head: the Cistern's pad {reach(d, 0, P.VAULT + 1, 0, 1)}")
d = walk.walk(ids, [(-41, P.TOWN + 1, -1)], w.x0, w.z0, rules)
print(f"from Harbour Street at the cellar stair's head: the Cistern's pad {reach(d, 0, P.VAULT + 1, 0, 1)}")
