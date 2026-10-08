"""Read Islets back: the hill reached from both spawns, nothing standable over the kill height but the islands,
and every block's footing."""
import sys

import numpy as np

from plan import KILL_Y, build, objectives
from pgmvox import World, audit, walk

R = build()
w = World.load(sys.argv[1])
d = walk.walk(w.ids, [(-23, 31, 0), (22, 31, -1)], w.x0, w.z0)
print("the hill reached:", walk.nearest(d, w.x0, w.z0, 0, 34, 0, 1) is not None)
X, Z = w.grid()
islands = np.vectorize(lambda x, z: R.inside(x, z) and R.kind(x, z) != "void")(X, Z)
print("standable over the kill height beside the islands:", len(walk.no_stand_above(w, KILL_Y, np.hypot(X, Z) < 60,
                                                                                      islands)))
print("footing problems:", len(audit.footing(w)))
problems = objectives().check(w)
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
