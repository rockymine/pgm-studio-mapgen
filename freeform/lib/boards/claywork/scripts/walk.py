"""Read Claywork back from the built world: the objectives check clean, every block has its footing, no water
stands against air, and each team's walks come out as the plan's did.

    python3 walk.py <build-dir>

Two walks from each spawn, pgmvox.walk's voxel walk with running jumps:

    on foot     the world as built: its own monuments, the Walks and the wall, and that nothing reaches an enemy
                Kiln without building
    building    the same world with every build zone's void, from y 10 to the build height, and the bedrock walls,
                filled with water: a stand-in for "a player may build here", since the walk swims up and across
                water as a player climbs a tower or a bridge they build
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk
from pgmvox.objectives import DYES, Spawn, Wool

w = World.load(sys.argv[1])
R = P.plan()
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
loose = audit.loose_water(w)
out.append(f"water standing against air (audit.loose_water): {len(loose)}")
X, Z = w.grid()
land = R.piece != R.kinds["void"]
marked = (w.ids[:, 0, :] == 36)
out.append(f"columns of land or build zone without block 36 at y 0: {int(((land | P.band_mask(R)) & ~marked).sum())}")
out.append(f"block 36 under void that is no build zone: {int((marked & ~land & ~P.band_mask(R)).sum())}")
wall = R.mask("barrier")
holes = 0
for i, k in np.argwhere(wall):
    top = int(R.floor[i, k]) + P.WALL["height"]
    col = w.ids[i, 1:top + 1, k]
    holes += int(np.sum(~np.isin(col, [B.BEDROCK, B.CHEST, B.AIR]))) + int(col[0] != B.BEDROCK)
out.append(f"blocks of a wall's columns, y 1 to its top, that are not bedrock (a chest and its lid aside): {holes}")
cid = np.argwhere(w.ids == B.CHEST)
at_wall = sum(1 for i, y, k in cid if wall[i, k])
in_kiln = sum(1 for i, y, k in cid if R.piece[i, k] == R.kinds["kiln"])
out.append(f"defence chests set into the walls: {at_wall}; chests of gear in the Kilns: {in_kiln}")
iron = np.argwhere(w.ids == B.IRON_BLOCK)
inside = 0
for o in O.of(Spawn):
    a = o.area
    inside += sum(1 for i, y, k in iron if a.x0 <= i + w.x0 <= a.x1 and a.z0 <= k + w.z0 <= a.z1)
out.append(f"iron blocks: {len(iron)}, of them inside a spawn's area (mined there, and grown back): {inside}")

# the building stand-in
wb = World(w.x0, w.z0, w.sx, w.sz, w.sy)
wb.ids, wb.dat = w.ids.copy(), w.dat.copy()
for i, k in np.argwhere(P.band_mask(R)):
    col = wb.ids[i, 10:P.MAX_BUILD + 1, k]
    col[col == B.AIR] = B.WATER
for i, k in np.argwhere(R.mask("barrier")):
    col = wb.ids[i, 10:P.MAX_BUILD + 1, k]
    col[np.isin(col, [B.AIR, B.BEDROCK])] = B.WATER

rules = walk.MoveRules(max_drop=4)
for team, at in spawns.items():
    short = O.teams.short(team)
    d = walk.walk(w.ids, [at], w.x0, w.z0, rules)
    out.append(f"from {short}'s spawn {at}: {int((d >= 0).sum())} places reached on foot")
    for o in wools:
        if o.team == team:
            v = walk.nearest(d, w.x0, w.z0, *o.slot, r=1)
            out.append(f"  on foot to its own {o.color} monument: {v if v is not None else 'NOT REACHED'}")
    for o in wools:
        if o.team != team:
            v = walk.nearest(d, w.x0, w.z0, *o.found, r=2)
            out.append(f"  on foot, into its own {o.color} Kiln: {v if v is not None else 'NOT REACHED'}")
    for o in wools:
        if o.team == team:
            v = walk.nearest(d, w.x0, w.z0, *o.found, r=2)
            out.append(f"  on foot to the enemy's {o.color} Kiln: {v if v is not None else 'not reached (built to)'}")
    db = walk.walk(wb.ids, [at], wb.x0, wb.z0, rules)
    for o in wools:
        if o.team == team:
            v = walk.nearest(db, w.x0, w.z0, *o.found, r=2)
            out.append(f"  building, to the enemy's {o.color} Kiln: {v if v is not None else 'NOT REACHED'}")

# the Undercroft and the stepping stones, on red's west side; the drop into the well lands in its pool
well = walk.MoveRules(max_drop=P.HUB - P.UNDER)
d = walk.walk(w.ids, [(0, P.HUB + 1, -45)], w.x0, w.z0, well)
v = walk.nearest(d, w.x0, w.z0, 0, P.UNDER + 1, -56, r=2)
out.append(f"from the Court into the well's pool (a drop of {P.HUB - P.UNDER}): {v if v is not None else 'NOT REACHED'}")
lx, lz = P.LADDER
v = walk.nearest(d, w.x0, w.z0, lx - 1, P.HUB + 1, lz, r=1)
out.append(f"  and on, by the Undercroft and the ladder, onto the West Walk: {v if v is not None else 'NOT REACHED'}")
d = walk.walk(w.ids, [(0, P.UNDER + 1, -56)], w.x0, w.z0, well)
v = walk.nearest(d, w.x0, w.z0, 0, P.HUB + 1, -45, r=1)
out.append(f"from the well's floor back up into the Court, without the ladders: "
           f"{'reached (it should not be)' if v is not None and v < 20 else 'only round by a ladder' if v else 'no'}")
first, last = P.STONES[0][0], P.STONES[-1][0]
d = walk.walk(w.ids, [(first[0], P.STONES[0][1] + 1, first[1])], w.x0, w.z0, rules)
v = walk.nearest(d, w.x0, w.z0, last[0], P.STONES[-1][1] + 1, last[3], r=1)
out.append(f"the stepping stones, first to last: {v if v is not None else 'NOT REACHED'}")
d = walk.walk(w.ids, [(last[0], P.STONES[-1][1] + 1, last[3])], w.x0, w.z0, rules)
v = walk.nearest(d, w.x0, w.z0, first[0], P.HUB + 1, P.PIECE["wing"][2][3], r=1)
out.append(f"  and back up, last stone onto the Arcade: {v if v is not None else 'NOT REACHED'}")
print("\n".join(out))
