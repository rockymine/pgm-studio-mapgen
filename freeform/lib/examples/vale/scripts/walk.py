"""Read the Vale back: from the harbour, every place the roads join reached on foot without jumping, the spire's
foot reached by the footpath, and how the walk would go without the roads."""
import sys

import numpy as np

from land import FOOTPATH, PLACES
from pgmvox import World, walk

w = World.load(sys.argv[1])
hx, hz = PLACES["harbour"]
start = (hx, w.top(hx, hz) + 1, hz)
d = walk.walk(w.ids, [start], w.x0, w.z0, walk.MoveRules(jumps=False, max_drop=3))


def reached(x, z):
    return walk.nearest(d, w.x0, w.z0, x, w.top(x, z) + 1, z, 3) is not None


for name, (x, z) in list(PLACES.items()) + [("the spire's foot", FOOTPATH[1])]:
    print(f"{name}: {'reached' if reached(x, z) else 'NOT reached'} on foot from the harbour, no jumps, no drop over 3")
print("columns reached:", int((d >= 0).any(axis=1).sum()))
