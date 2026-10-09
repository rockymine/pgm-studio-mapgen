"""Read Brittlebush III back from the built world: the objectives check clean, nothing falls or hangs on nothing,
no water stands against air, building is allowed over the board and its zones, and each team reaches its own wool
on foot and the others' building across the zones, the same for every team.

    python3 walk.py <build-dir>

Every piece of the plan is its own island, and every wool stands on a plateau three over the ground in front of it,
as Brittlebush raises its wool rooms: a player builds across the water and up. The building walk stands in for
blocks placed with water a player swims through: every zone's column from y 2 to the build height, and four blocks
over every other column of the board. A team's own room shuts it out, so its own wool is reached at its door.
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
loose = audit.loose_water(w)                    # the zones' water at y 1 meets the void unkerbed: PGM holds it still
out.append(f"water standing against air (audit.loose_water), the zones' floor aside: "
           f"{sum(1 for p in loose if p[1] != 1)}; at the zones' floor, held by PGM: {sum(1 for p in loose if p[1] == 1)}")
board = np.zeros((w.sx, w.sz), bool)
water = np.zeros((w.sx, w.sz), bool)
for (cx, cz), c in cells.items():
    sl = (slice(cx * CELL - w.x0, (cx + 1) * CELL - w.x0), slice(cz * CELL - w.z0, (cz + 1) * CELL - w.z0))
    board[sl] = True
    if c.kind in ("water", "gap"):
        water[sl] = True
marked = w.ids[:, 0, :] == 36
out.append(f"columns of board without block 36 at y 0: {int((board & ~marked).sum())}")
out.append(f"block 36 off the board: {int((marked & ~board).sum())}")

wb = World(w.x0, w.z0, w.sx, w.sz, w.sy)
wb.ids, wb.dat = w.ids.copy(), w.dat.copy()
for i, k in np.argwhere(water):
    col = wb.ids[i, 2:P.MAX_BUILD + 1, k]
    col[np.isin(col, [B.AIR, B.COBWEB])] = B.WATER
for i, k in np.argwhere(board & ~water):
    solid = np.nonzero(w.ids[i, :, k])[0]
    top = int(solid[-1]) if len(solid) else 0
    col = wb.ids[i, top + 1:top + 5, k]
    col[col == B.AIR] = B.WATER
rules = walk.MoveRules(max_drop=6)
rows = []
for k, sp in enumerate(O.of(Spawn)):
    d = walk.walk(w.ids, [sp.at], w.x0, w.z0, rules)
    db = walk.walk(wb.ids, [sp.at], wb.x0, wb.z0, rules)
    x0, z0, x1, z1 = P.turned_box(P.WOOL_BOX, k)
    door = [(x, z) for x in range(x0 - 2, x1 + 3) for z in range(z0 - 2, z1 + 3)
            if not (x0 <= x <= x1 and z0 <= z <= z1)]
    own = min([v for v in (walk.nearest(db, w.x0, w.z0, x, P.WOOL_Y + 1, z, r=0) for x, z in door)
               if v is not None], default=None)
    island = int((d >= 0).sum())
    got = []
    for j in range(4):
        if j == k:
            continue
        fx, fz = P.turned((P.WOOL_AT[0], P.WOOL_AT[2]), j)
        got.append(walk.nearest(db, w.x0, w.z0, fx, P.WOOL_Y + 1, fz, r=2))
    rows.append((own, tuple(sorted(v if v is not None else 10 ** 6 for v in got))))
    out.append(f"from {sp.team}'s spawn: {island} places on foot; building, to its own wool room's door {own}, to the "
               f"other wools "
               f"{[g if g is not None else 'NOT REACHED' for g in got]}")
    rows[-1] = rows[-1] + (island,)
out.append(f"every team the same: {'yes' if all(r == rows[0] for r in rows) else 'NO'}")
print("\n".join(out))
