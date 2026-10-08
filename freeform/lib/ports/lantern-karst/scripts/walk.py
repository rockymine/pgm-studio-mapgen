"""Read Lantern Karst back from the built world: the objectives check clean, every block has its footing, and
each team reaches its own monuments on foot and the enemy's wool rooms by building.

    python3 walk.py <build-dir>

Two walks from each spawn, pgmvox.walk's voxel walk, a drop of at most three:

    on foot     the world as built, no block placed: the own monuments, and how far the board goes before a
                build zone or the bedrock wall stops it
    building    the same world with every build zone's void, from the kill height to the build height, and
                the bedrock wall's cells, filled with water: a stand-in for "a player may build anywhere here",
                since the walk swims up and across water as a player climbs a bridge or a tower they build
"""
import sys

import numpy as np

import plan  # noqa: F401  (puts the library on the path)
from plan import KILL_Y, MAX_BUILD, WALL, build, objectives, zone_mask
from pgmvox import B, World, audit, walk
from pgmvox.objectives import DYES, Spawn, Wool

w = World.load(sys.argv[1])
R, _, _ = build()
O = objectives()
spawns = {o.team: o.at for o in O.of(Spawn)}
wools = O.of(Wool)
out = []

problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
missing = [o.color for o in wools if w.get(*o.found) != (B.WOOL, DYES[o.color])]
out.append(f"wools missing from their rooms: {len(missing)} {missing if missing else ''}")
foot = audit.footing(w)
outline = [f for f in foot if f[1] == 1 and w.id(f[0], 1, f[2]) == B.REDSTONE_WIRE]
out.append(f"footing problems (audit.footing): {len(foot)}, of which {len(outline)} are the build outline's "
           f"redstone at y 1 over the void, as the studio's ST5 stamper lays it")
out += [f"   {f}" for f in foot if f not in outline][:10]

X, Z = w.grid()
islands = ~R.mask("void")
stand = walk.no_stand_above(w, KILL_Y, np.ones(X.shape, bool), islands)
out.append(f"columns off the islands with ground over the kill height: {len(stand)} "
           f"(the karst towers' crowns and the islands' skirts; scenery nobody reaches without building)")

# the building stand-in: the zones and the wall flooded from the kill height to the build height
wb = World(w.x0, w.z0, w.sx, w.sz, w.sy)
wb.ids, wb.dat = w.ids.copy(), w.dat.copy()
zm = zone_mask(R)
for i, k in np.argwhere(zm):
    col = wb.ids[i, KILL_Y + 1:MAX_BUILD + 1, k]
    col[col == B.AIR] = B.WATER
for x0, z0 in ((WALL["x0"], WALL["z0"]), R.symmetry.point(WALL["x1"], WALL["z1"])):
    for x in range(x0, x0 + WALL["x1"] - WALL["x0"] + 1):
        for z in range(z0, z0 + WALL["z1"] - WALL["z0"] + 1):
            i, k = x - w.x0, z - w.z0
            col = wb.ids[i, KILL_Y + 1:MAX_BUILD + 1, k]
            col[np.isin(col, [B.AIR, B.BEDROCK, B.COBWEB])] = B.WATER
            wb.ids[i, :, k][wb.ids[i, :, k] == B.REDSTONE_WIRE] = B.REDSTONE_WIRE

foot_rules = walk.MoveRules(max_drop=3)
build_rules = walk.MoveRules(max_drop=3, jumps=False)
for team, at in spawns.items():
    short = O.teams.short(team)
    d = walk.walk(w.ids, [at], w.x0, w.z0, foot_rules)
    d[:, :KILL_Y + 1, :] = -1                                   # nothing under the kill height is ground
    out.append(f"from {short}'s spawn {at}: {int((d >= 0).sum())} places reached on foot")
    for o in wools:
        if o.team == team:
            v = walk.nearest(d, w.x0, w.z0, *o.slot, r=1)
            out.append(f"  on foot to its own {o.color} monument: {v if v is not None else 'NOT REACHED'}")
    for o in wools:
        if o.team == team:
            v = walk.nearest(d, w.x0, w.z0, *o.found, r=2)
            out.append(f"  on foot to the enemy's {o.color} room: {v if v is not None else 'not reached (built to)'}")
    db = walk.walk(wb.ids, [at], wb.x0, wb.z0, build_rules)
    db[:, :KILL_Y + 1, :] = -1
    for o in wools:
        if o.team == team:
            v = walk.nearest(db, w.x0, w.z0, *o.found, r=2)
            out.append(f"  building, to the enemy's {o.color} room: {v if v is not None else 'NOT REACHED'}")
    for o in wools:
        if o.team != team:
            v = walk.nearest(d, w.x0, w.z0, *o.found, r=2)
            out.append(f"  on foot, into its own {o.color} room: {v if v is not None else 'not reached'}")
print("\n".join(out))
