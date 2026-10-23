"""Read Frostvault back from the built world: footing and water; what a spawn reaches on foot; each team's walk to
its own wool monuments, to its own seals and to the enemy's, bridging; with every seal blown and its screen opened,
the walk to the enemy's wool and home with it; the match's phases with a seal standing and blown.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import board
import layout as L
import objectives as P
from pgmvox import B, World
from pgmvox.plan.bunker import ROCK
from pgmvox.play.objectives import Spawn, Wool
from pgmvox.read import audit, late
from pgmvox.read.walk import MoveRules, nearest, walk

w = World.load(sys.argv[1])
got = board.laid()
O = P.objectives(got)
print(f"footing problems: {len(audit.footing(w))}; water against air: {len(audit.loose_water(w))}")
inside = np.zeros((w.sx, w.sz), bool)
i0, j0 = got.x0 - w.x0, got.z0 - w.z0
inside[i0:i0 + got.blocks.shape[0], j0:j0 + got.blocks.shape[1]] = got.blocks != ROCK
foot = MoveRules(max_drop=3, jumps=False, kill_y=L.H.floor)
built = MoveRules(max_drop=3, jumps=False, kill_y=L.H.floor, build=(inside, (L.H.top + 1, L.H.ceil)))
spawns = {o.team: o.at for o in O.of(Spawn)}
wools = O.of(Wool)
team_of = {k: L.TEAMS[k][0] for k in L.TEAMS}

for team, at in spawns.items():
    d0 = walk(w.ids, [at], w.x0, w.z0, foot)
    print(f"{team}: on foot from its spawn a player reaches {int((d0 >= 0).sum())} places")
    for o in wools:
        if o.team == team:
            print(f"  to its {o.color} monument, on foot: {nearest(d0, w.x0, w.z0, *o.slot, r=1)}")
    d1 = walk(w.ids, [at], w.x0, w.z0, built)
    for r in got.rooms:
        fx, fz = r["face_at"]
        n = nearest(d1, w.x0, w.z0, fx, L.H.room + 3, fz, r=2)
        whose = "its own" if team_of[r["k"]] == team else "the enemy's"
        print(f"  to {whose} {P.colour(got, r)} seal, bridging: {n}")

open_w = World.load(sys.argv[1])
for r in got.rooms:
    for p in r["seal"] + r["case"] + r["door"]:
        open_w.set(*p, B.AIR)
for team, at in spawns.items():
    d = walk(open_w.ids, [at], w.x0, w.z0, built)
    for o in wools:
        if o.team != team:
            continue
        there = nearest(d, w.x0, w.z0, *o.found, r=1)
        back = walk(open_w.ids, [(o.found[0], o.found[1] + 1, o.found[2])], w.x0, w.z0, built)
        print(f"{team}, every seal blown: spawn to the {o.color} wool {there}, the wool home to its monument "
              f"{nearest(back, w.x0, w.z0, *o.slot, r=1)}")

print("\nthe match's phases, blue's spawn to each red wool, the seal and its screen walled as the door:")
drifts = {B.SNOW, B.SNOW_LAYER, B.PACKED_ICE, B.ICE}
rows = []
for r in got.rooms:
    if r["k"] != 1:
        continue
    goal = (r["found"][0], r["found"][1] + 1, r["found"][2])
    door = r["seal"] + r["case"] + r["door"]
    rows.append((f"{P.colour(got, r)}, seal standing", late.phases(w, spawns["blue-team"], goal, inside, L.H.ceil,
                                                                  door=door, breakable=drifts, low=L.H.top + 1)))
    rows.append((f"{P.colour(got, r)}, seal blown", late.phases(open_w, spawns["blue-team"], goal, inside, L.H.ceil,
                                                               door=door, breakable=drifts, low=L.H.top + 1)))
print(late.table(rows))
