"""Read Sandreach back from the built world: the objectives check clean, nothing falls or hangs on nothing, no
water stands against air, building is allowed over the board and its zones, and each team walks to its own wool's
door and its monument, reaches the meadow down its stair, and reaches the other team's wool building across the
middle, the same for both teams.

    python3 walk.py <build-dir>

The building walk stands in for blocks placed with water a player swims through: every build zone's column from
y 2 to the build height, and four blocks over every column of land.
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk
from pgmvox.brittle import CELL
from pgmvox.objectives import Spawn

w = World.load(sys.argv[1])
O = P.objectives()
cells, team = P.cells()
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
foot = audit.footing(w)
out.append(f"footing problems (audit.footing): {len(foot)}")
out += [f"   {f}" for f in foot[:10]]
out.append(f"water standing against air (audit.loose_water): {len(audit.loose_water(w))}")
zone = np.zeros((w.sx, w.sz), bool)
for (cx, cz), c in cells.items():
    if c.kind == "gap":
        zone[cx * CELL - w.x0:(cx + 1) * CELL - w.x0, cz * CELL - w.z0:(cz + 1) * CELL - w.z0] = True
X, Z = P.grid()                                    # land is what the plan says is land, made or grown: not
made = P.made_mask(X, Z, cells)                    # an eave or a crown hanging over the void
grown = P.meadow(X, Z, cells)[0] | (P.island(X, Z)[0] & ~made)
land = made | grown | grown[::-1, ::-1]
marked = w.ids[:, 0, :] == 36
out.append(f"columns of land without block 36 at y 0: {int((land & ~marked).sum())}")
out.append(f"block 36 under neither land nor a zone: {int((marked & ~land & ~zone).sum())}")

wb = World(w.x0, w.z0, w.sx, w.sz, w.sy)
wb.ids, wb.dat = w.ids.copy(), w.dat.copy()
for i, k in np.argwhere(zone & ~land):
    col = wb.ids[i, 2:P.MAX_BUILD + 1, k]
    col[np.isin(col, [B.AIR, B.COBWEB])] = B.WATER
for i, k in np.argwhere(land):
    solid = np.nonzero(w.ids[i, :, k])[0]
    top = int(solid[-1])
    col = wb.ids[i, top + 1:top + 5, k]
    col[col == B.AIR] = B.WATER
rules = walk.MoveRules(max_drop=6)
rows = []
sym = [lambda p: p, lambda p: (int(P.SYM.point(p[0], p[1])[0]), int(P.SYM.point(p[0], p[1])[1]))]
for k, sp in enumerate(O.of(Spawn)):
    d = walk.walk(w.ids, [sp.at], w.x0, w.z0, rules)
    db = walk.walk(wb.ids, [sp.at], wb.x0, wb.z0, rules)
    wx0, wz0, wx1, wz1 = P.WOOL_BOX
    door = sym[k]((wx0 + 7, wz1 + 1))
    own = walk.nearest(d, w.x0, w.z0, door[0], P.WOOL + 1, door[1], r=1)
    mon = sym[k]((P.MONUMENT[0], P.MONUMENT[2]))
    monument = walk.nearest(d, w.x0, w.z0, mon[0], P.MONUMENT[1], mon[1], r=1)
    foot = sym[k]((22, -58))
    meadow = walk.nearest(d, w.x0, w.z0, foot[0], P.LANE + 1, foot[1], r=2)
    other = sym[1 - k]((P.WOOL_AT[0], P.WOOL_AT[2]))
    enemy = walk.nearest(db, w.x0, w.z0, other[0], P.WOOL + 1, other[1], r=2)
    enemy_foot = walk.nearest(d, w.x0, w.z0, other[0], P.WOOL + 1, other[1], r=2)
    row = (int((d >= 0).sum()), own, monument, meadow, enemy, enemy_foot)
    rows.append(row)
    out.append(f"from {sp.team}'s spawn: {row[0]} places on foot; on foot to its own wool's door {own}, to its "
               f"monument {monument}, down the stair onto its meadow {meadow}; to the other wool on foot "
               f"{enemy_foot if enemy_foot is not None else 'NOT REACHED'}, building {enemy}")
out.append(f"both teams the same: {'yes' if rows[0] == rows[1] else 'NO'}")
print("\n".join(out))
