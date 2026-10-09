"""Read Brittlebush KotH back from the built world: the objectives check clean, every block has its footing, no
water stands against air, building is allowed only over the board, and each team walks to the hills as the plan
said, the same for every team.

    python3 walk.py <build-dir>

The voxel walk (pgmvox.walk, running jumps, a drop of six at most) walks the blocks; for the golden apples it may
also build, the board's gaps standing in for blocks placed, filled with water a player swims through.
"""
import sys

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk
from pgmvox.objectives import Spawn

w = World.load(sys.argv[1])
O = P.objectives()
out = []
problems = O.check(w)
out.append(f"objectives with a problem (Objectives.check): {len(problems)}")
out += [f"   {p}" for p in problems]
foot = audit.footing(w)
out.append(f"footing problems (audit.footing): {len(foot)}")
out += [f"   {f}" for f in foot[:10]]
loose = audit.loose_water(w)                    # the ponds' water at y 1 meets the void unkerbed: PGM holds it still
out.append(f"water standing against air (audit.loose_water), the ponds' floor aside: "
           f"{sum(1 for p in loose if p[1] != 1)}; at the ponds' floor, held by PGM: {sum(1 for p in loose if p[1] == 1)}")
R = P.plan()
land = ~np.isin(R.K, [R.kinds["void"]])
marked = w.ids[:, 0, :] == 36
out.append(f"columns of board without block 36 at y 0: {int((land & ~marked).sum())}")
out.append(f"block 36 under plain void: {int((marked & ~land).sum())}")

rules = walk.MoveRules(max_drop=6)
wb = World(w.x0, w.z0, w.sx, w.sz, w.sy)
wb.ids, wb.dat = w.ids.copy(), w.dat.copy()
for i, k in np.argwhere(R.mask("gap") | R.mask("water")):
    col = wb.ids[i, 2:P.MAX_BUILD + 1, k]
    col[col == B.AIR] = B.WATER


def hill_cells(box):
    x0, z0, x1, z1 = box
    return [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]


def reach(d, cells, y):
    got = [walk.nearest(d, w.x0, w.z0, x, y, z, r=0) for x, z in cells]
    got = [g for g in got if g is not None]
    return min(got) if got else None


def around(p):
    """The two blocks by two either side of a point between blocks: the same under every quarter turn."""
    xs = {int(np.floor(p[0])), int(np.ceil(p[0]))}
    zs = {int(np.floor(p[1])), int(np.ceil(p[1]))}
    return [(x, z) for x in xs for z in zs]


order = ["north", "east", "south", "west"]
rows = []
for i, sp in enumerate(O.of(Spawn)):
    d = walk.walk(w.ids, [sp.at], w.x0, w.z0, rules)
    hills = {hid: reach(d, hill_cells(box), hy + 1) for hid, _, box, _, hy in P.HILLS}
    near = sorted([hills[order[i]], hills[order[(i + 3) % 4]]], key=lambda v: v if v is not None else 1e9)
    far = sorted([hills[order[(i + 1) % 4]], hills[order[(i + 2) % 4]]], key=lambda v: v if v is not None else 1e9)
    db = walk.walk(wb.ids, [sp.at], wb.x0, wb.z0, rules)
    apples = reach(db, [c for p in P.APPLES for c in around(p)], P.LEVEL[2] + 1)
    arrows = reach(d, [c for p in P.ARROWS for c in around(p)], P.LEVEL[0] + 1)
    row = (hills["centre"], tuple(near), tuple(far), apples, arrows)
    rows.append(row)
    out.append(f"from {sp.team}'s spawn: the Dais {row[0]}, the border hills beside it {near}, beyond {far}; "
               f"golden apples, building {apples}; arrows {arrows}")
out.append(f"every team the same: {'yes' if all(r == rows[0] for r in rows) else 'NO'}")
print("\n".join(out))
