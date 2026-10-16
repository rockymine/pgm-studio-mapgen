"""Read Thawline back: each spawn walked over the built blocks (the rift crossed by building, nobody below the
kill height), every objective reached and checked, ground to stand on over the void, and every block's footing."""
import sys

import numpy as np

import plan as P
from pgmvox import World
from pgmvox.read import audit, walk

w = World.load(sys.argv[1])
X, Z = w.grid()
rift = P.RIFT
ember = P.SYM.point(P.SPAWN_AT[0], P.SPAWN_AT[2])
starts = {"frost": [P.SPAWN_AT], "ember": [(ember[0], P.SPAWN_AT[1], ember[1])]}
rules = walk.MoveRules(kill_y=P.KILL_Y, build=(rift, (P.land.LIP - 2, P.land.LIP + 4)))
O = P.objectives()
for team, st in starts.items():
    d = walk.walk(w.ids, st, w.x0, w.z0, rules)
    print(f"from {team}'s spawn: {int((d >= 0).sum())} places reached")
    for o in O.items:
        box = getattr(o, "box", None)
        if box is None:
            continue
        cx, cz = (int(v) for v in box.centre())
        feet = P.g(cx, cz) + 1
        hit = walk.nearest(d, w.x0, w.z0, cx, feet, cz, 3)
        print(f"   {o.name}: the ground under it {'reached in ' + str(hit) + ' moves' if hit is not None else 'NOT reached'}")
problems = O.check(w)
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
over = walk.no_stand_above(w, P.KILL_Y, np.hypot(X, Z) < 400, P.LAND | P.RIFT)
print("standable over the kill height off the land:", len(over))
f = audit.footing(w)
print("footing problems:", len(f))
for p in f[:12]:
    print("  ", p)
lw = audit.loose_water(w)
print("water standing against air:", len(lw))
