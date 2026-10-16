"""Read Rimeglow Rift back from the built world: each spawn's walk to every objective and gate, the goal rules' ratio, how
much of the land is reached, footing, and each objective's own check."""
import sys

import numpy as np

import land as LD
from plan import KILL_Y, objectives
from pgmvox import World
from pgmvox.read import audit, walk

w = World.load(sys.argv[1])
O = objectives()
rules = walk.MoveRules(max_drop=4, jumps=True, max_gap=3, kill_y=KILL_Y + 2)


def feet(x, z):
    return (x, w.top(x, z) + 1, z)


starts = {"Rime": feet(13, -68), "Ember": feet(-14, 67)}
cores = {"Rime": (46, 74, -48), "Ember": (-47, 74, 47)}
dist = {team: walk.walk(w.ids, [pos], w.x0, w.z0, rules) for team, pos in starts.items()}


def to(d, x, y, z, r=4):
    return walk.nearest(d, w.x0, w.z0, x, y, z, r)


print("walks, in moves (four-way steps; a straight line is about three quarters of it)")
rows = {}
for team, d in dist.items():
    other = "Ember" if team == "Rime" else "Rime"
    own, foe = to(d, *cores[team]), to(d, *cores[other])
    spawn = to(d, *[(v if i != 1 else w.top(starts[other][0], starts[other][2]) + 1) for i, v in enumerate(starts[other])])
    rows[team] = (own, foe, spawn)
    print(f"  {team} spawn: own core {own}, enemy core {foe}, enemy spawn {spawn}")
own, foe = rows["Rime"][0], rows["Rime"][1]
print(f"  enemy core over own core: {foe / own:.2f}  (the goal rules ask 3 to 4)")
for name, (x, z) in {"west gate": (-38, -22), "centre gate": (0, -22), "east gate": (38, -22)}.items():
    print(f"  Rime spawn to the {name}: {to(dist['Rime'], x, 60, z)}")
for name, (x, z) in {"west bridge, far end": (-39, 17), "centre bridge, far end": (0, 17), "east bridge, far end": (38, 17)}.items():
    print(f"  Rime spawn to the {name}: {to(dist['Rime'], x, 60, z)}")
reached = (dist["Rime"] >= 0).any(axis=1)
X, Z = w.grid()
land = LD.land_mask(X, Z)
print(f"land columns reached from the Rime spawn: {int((reached & land).sum())} of {int(land.sum())}")
print("footing problems:", len(audit.footing(w)))
print("loose water:", len(audit.loose_water(w)))
problems = O.check(w)
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
