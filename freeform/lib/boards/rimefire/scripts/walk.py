"""Rimefire read back from the built world: each spawn's walk to every core and to the enemy spawn, the walls and
the pit round a core, whether anything is standable over the void, and every block's footing."""
import sys

import numpy as np

import plan as PLAN
from pgmvox import World
from pgmvox.read import audit, walk

w = World.load(sys.argv[1])
O = PLAN.objectives()
rules = walk.MoveRules(max_drop=3, jumps=True, max_gap=3)
spawns = {s.team: s for s in O.of(__import__("pgmvox.play.objectives", fromlist=["Spawn"]).Spawn)}
cores = {c.team: c for c in O.of(__import__("pgmvox.play.objectives", fromlist=["Core"]).Core)}


def stand_near(box, r=6):
    """The nearest place a player stands within r of a box's middle at its floor."""
    x, z = (box.x0 + box.x1) // 2, (box.z0 + box.z1) // 2
    return x, z


dists = {}
for team, s in spawns.items():
    start = (s.at[0], s.at[1], s.at[2])
    dists[team] = walk.walk(w.ids, [start], w.x0, w.z0, rules)


def reach(team, x, y, z, r=3):
    return walk.nearest(dists[team], w.x0, w.z0, x, y, z, r)


for team, c in cores.items():
    b = c.box
    cx, cz = (b.x0 + b.x1) // 2, (b.z0 + b.z1) // 2
    # approach cells: the ledge round the pit and the pit floor beside the core
    ledge = (cx - 8, b.y0 - 4 if team == "fire-team" else b.y0 - 4, cz)
    for who in spawns:
        d_ledge = reach(who, cx + (-8 if team == "fire-team" else 8), b.y0 - 3, cz, 4)
        d_pit = reach(who, cx + (-4 if team == "fire-team" else 4), b.y0 - 3, cz, 3)
        print(f"{who} spawn -> {team} core: ledge {d_ledge}, pit floor {d_pit}")
for team, s in spawns.items():
    other = [t for t in spawns if t != team][0]
    o = spawns[other]
    print(f"{team} spawn -> {other} spawn: {reach(team, o.at[0], o.at[1], o.at[2], 3)}")
print("columns reached from fire spawn:", int((dists['fire-team'] >= 0).any(axis=1).sum()))
print("footing problems:", len(audit.footing(w)))
problems = O.check(w)
print("objectives with a problem:", len(problems))
for p in problems:
    print("  ", p)
