"""Read Hoarfrost Reach back from the built world: the objectives check clean, every block has its footing, and each
team reaches its own monuments and rooms on foot, and the enemy's rooms by building.

    python3 walk.py <build-dir>

Two walks from each spawn, pgmvox.walk's voxel walk, a drop of at most three (doors opened, no running jump):

    on foot     the world as built: the own monuments and rooms, and how far the board goes before a build zone
    building    the same world with every build zone's void, from the kill height to the build height, filled with
                water: a stand-in for "a player may build anywhere here", since the walk swims up and across water
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk
from pgmvox import blocks as K
from pgmvox.objectives import DYES, Spawn, Wool

w = World.load(sys.argv[1])
R = P.build()
O = P.objectives()
spawns = {o.team: o.at for o in O.of(Spawn)}
wools = O.of(Wool)
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
missing = [o.color for o in wools if w.get(*o.found) != (B.WOOL, DYES[o.color])]
out.append(f"wools missing from their rooms: {len(missing)} {missing if missing else ''}")
foot = audit.footing(w)
out.append(f"footing problems (audit.footing): {len(foot)}")
out += [f"   {f}" for f in foot[:10]]

ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0                         # doors open: pgmvox.walk's PASSABLE has none
wb = World(w.x0, w.z0, w.sx, w.sz, w.sy)
wb.ids, wb.dat = ids.copy(), w.dat.copy()
zm = P.zone_mask(R)
for i, k in np.argwhere(zm):
    col = wb.ids[i, P.KILL_Y + 1:P.MAX_BUILD + 1, k]
    col[col == B.AIR] = B.WATER
foot_rules = walk.MoveRules(max_drop=3, jumps=False)
for team, at in spawns.items():
    short = O.teams.short(team)
    d = walk.walk(ids, [at], w.x0, w.z0, foot_rules)
    d[:, :P.KILL_Y + 1, :] = -1
    out.append(f"from {short}'s spawn {at}: {int((d >= 0).sum())} places reached on foot")
    for o in wools:
        if o.team == team:
            v = walk.nearest(d, w.x0, w.z0, o.slot[0], o.slot[1] + 0, o.slot[2], r=2)
            out.append(f"  on foot to its own {o.color} monument: {v if v is not None else 'NOT REACHED'}")
    for o in wools:
        if o.team != team:
            v = walk.nearest(d, w.x0, w.z0, *o.found, r=2)
            out.append(f"  on foot into its own {o.color} room (the keepers'): {v if v is not None else 'not reached'}")
    db = walk.walk(wb.ids, [at], wb.x0, wb.z0, foot_rules)
    db[:, :P.KILL_Y + 1, :] = -1
    for o in wools:
        if o.team == team:
            v = walk.nearest(db, w.x0, w.z0, *o.found, r=2)
            out.append(f"  building, to the enemy's {o.color} room: {v if v is not None else 'NOT REACHED'}")
# the keepers' own walks to their rooms: the other team's rooms' images by symmetry
for team, at in spawns.items():
    d = walk.walk(wb.ids, [at], wb.x0, wb.z0, foot_rules)
    d[:, :P.KILL_Y + 1, :] = -1
    for o in wools:
        if o.team != team:
            v = walk.nearest(d, w.x0, w.z0, *o.found, r=2)
            out.append(f"  {O.teams.short(team)}'s walk to its own {o.color} room, with the gap built: {v if v is not None else 'NOT REACHED'}")
print("\n".join(out))
