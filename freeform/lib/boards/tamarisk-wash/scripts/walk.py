"""Read Tamarisk Wash back from the built world: each spawn walked to its own two monuments and the enemy's, the
mine's ladder to Table Rock's top, the qanat from the wash to the well, the aqueduct's gap, the caravanserai's roof,
every objective checked, every block's footing.

    python3 walk.py <build-dir>

The walk opens doors (pgmvox.walk's PASSABLE has none), takes a drop of at most three and no running jump.
"""
import sys

import numpy as np

import plan as P
from pgmvox import World, audit, walk
from pgmvox import blocks as K

w = World.load(sys.argv[1])
ids = w.ids.copy()
ids[np.isin(ids, sorted(K.DOORS))] = 0
rules = walk.MoveRules(max_drop=3, jumps=False)
O = P.objectives()
L = P.land()


def reach(d, x, y, z, r=2):
    n = walk.nearest(d, w.x0, w.z0, x, y, z, r)
    return "not reached" if n is None else f"{n}"


problems = O.check(w)
print(f"objectives with a problem (Objectives.check): {len(problems)}")
for p in problems:
    print("   ", p)
foot = audit.footing(w)
print(f"footing problems (audit.footing): {len(foot)}")
for f in foot[:8]:
    print("   ", f)
red = P.SPAWN
blue = (int(P.SYM.point(red[0], red[2])[0]), red[1], int(P.SYM.point(red[0], red[2])[1]))
ox, oz = P.OBELISK_AT
sx, sz = P.STONE_AT
for team, start in (("red", red), ("blue", blue)):
    d = walk.walk(ids, [start], w.x0, w.z0, rules)
    m = (lambda x, z: (x, z)) if team == "red" else (lambda x, z: tuple(int(v) for v in P.SYM.point(x, z)))
    own_o, own_s = m(ox, oz), m(sx, sz)
    en_o, en_s = P.SYM.point(*own_o), P.SYM.point(*own_s)
    sg = 1 if team == "red" else -1                              # the offsets mirror with the team
    print(f"{team} spawn at {start}: {int((d >= 0).sum())} places reached")
    print(f"  to its own Obelisk's dais (the top of Table Rock): {reach(d, own_o[0] + 2 * sg, P.TABLE_TOP + 1, own_o[1], 2)}")
    print(f"  to its own Sunstone's carpet: {reach(d, own_s[0] + 2 * sg, P.PLATEAU + 1, own_s[1], 2)}")
    print(f"  to the enemy's Obelisk's dais: {reach(d, int(en_o[0]) - 2 * sg, P.TABLE_TOP + 1, int(en_o[1]), 2)}")
    print(f"  to the enemy's Sunstone's carpet: {reach(d, int(en_s[0]) - 2 * sg, P.PLATEAU + 1, int(en_s[1]), 2)}")
    if team == "red":
        sx0, sz0, sx1, sz1 = P.SERAI
        print(f"  to the caravanserai's roof: {reach(d, sx0 + 12, P.PLATEAU + P.SERAI_WALL + 1, sz0 + 1, 1)}")
        print(f"  to the mine's adit: {reach(d, P.MINE[0][0], P.MINE[0][1] + 1, P.MINE[0][2], 1)}")
    reached = (d.max(axis=1) >= 0)
    print(f"  columns reached: {int(reached.sum())} of {reached.size}")
# the mine, the qanat, the arch, the aqueduct
mx, my, mz = P.MINE[0]
d = walk.walk(ids, [(mx, my, mz)], w.x0, w.z0, rules)
print(f"from the mine's adit {(mx, my, mz)}:")
print(f"  up the ladder onto Table Rock's top: {reach(d, P.MINE_SHAFT[0] + 3, P.TABLE_TOP + 1, P.MINE_SHAFT[1], 2)}")
qx, qy, qz, _ = P.QANAT[0]
d = walk.walk(ids, [(qx, qy, qz)], w.x0, w.z0, rules)
print(f"from the qanat's mouth in the wash {(qx, qy, qz)}:")
print(f"  to the cistern's floor: {reach(d, P.CISTERN[0] + 2, P.CISTERN[1], P.CISTERN[2], 2)}")
print(f"  up the well's ladder to the souk: {reach(d, P.WELL[0] + 3, P.PLATEAU + 1, P.WELL[1], 1)}")
ax, az = P.ARCH[0]
d = walk.walk(ids, [(ax, P.ZIGG_TOP + 1, az)], w.x0, w.z0, rules)
print(f"from the stepped rock's top, the arch's start {(ax, P.ZIGG_TOP + 1, az)}:")
print(f"  across the arch to Table Rock's top: {reach(d, P.ARCH[-1][0] - 2, P.TABLE_TOP + 1, P.ARCH[-1][1], 2)}")
ax0, az0, ax1, az1 = P.ARCADE
d = walk.walk(ids, [(ax0, P.DECK_Y + 1, az0 + 1)], w.x0, w.z0, rules)
print(f"from the aqueduct's anchor {(ax0, P.DECK_Y + 1, az0 + 1)}:")
print(f"  along the deck to its broken end: {reach(d, ax1 - 1, P.DECK_Y + 1, az0 + 1, 2)}")
print(f"  across to blue's half of the deck (the gap is {2 * (-1 - ax1)} blocks of air): "
      f"{reach(d, -1 - ax1, P.DECK_Y + 1, az0 + 1, 1)}")

# the well's foot: from the cistern's floor level through the opening in the ring to the shaft's floor and its ladder
cx_, cy_, cz_ = P.CISTERN
d = walk.walk(ids, [(cx_ + 2, cy_, cz_)], w.x0, w.z0, rules)
wx, wz = P.WELL
print(f"from the cistern's floor {(cx_ + 2, cy_, cz_)}:")
print(f"  into the well's shaft, its floor under the ladder: {reach(d, wx - 1, cy_, wz, 1)}")
print(f"  the opening in the ring: {sum(1 for dz in (-1, 0, 1) for y in range(cy_, cy_ + 3) if w.get(wx + 2, y, wz + dz)[0] == 0)} of 9 cells open, "
      f"floor under it: {[w.get(wx + 2, cy_ - 1, wz + dz)[0] != 0 for dz in (-1, 0, 1)]}")

# the ghats: stairs counted, and every step between neighbouring cells of the band in half blocks (a slab counts a half)
import gen as G  # noqa: E402
from pgmvox import shapes  # noqa: E402

X_, Z_ = w.grid()
earlier = np.zeros(X_.shape, bool)
SLABS = {44, 126}
LEAVES = {18, 161}


def surface(i, k):
    col = w.ids[i, :, k]
    ys = np.nonzero((col != 0) & ~np.isin(col, list(LEAVES)))[0]
    y = int(ys.max())
    return y + (0.5 if col[y] in SLABS and w.dat[i, y, k] < 8 else 1.0)


for rt in L.routes:
    if rt["name"] in G.GHATS:
        band, lvl, joined = G.ghat_levels(L, rt, X_, Z_, earlier)
        cells = {tuple(c): surface(*c) for c in np.argwhere(band)}
        step = max(abs(h - cells[(i + a, k + b)]) for (i, k), h in cells.items() for a, b in ((1, 0), (0, 1)) if (i + a, k + b) in cells)
        stairs = sum(1 for (i, k) in cells for y in range(40, 80) if w.ids[i, y, k] in (53, 67, 108, 109, 114, 128, 156, 163, 164))
        slabs = sum(1 for h in cells.values() if h % 1 == 0.5)
        head = min(min(int((np.nonzero(w.ids[i, int(np.ceil(h)):, k] != 0)[0].tolist() + [9])[0]), 9) for (i, k), h in cells.items())
        print(f"{rt['name']}: {len(cells)} cells from {min(cells.values()):.1f} to {max(cells.values()):.1f}, "
              f"largest step between neighbours {step} block, {stairs} stairs, {slabs} slab cells, "
              f"least headroom {head} blocks")
    earlier |= shapes.polyline(X_, Z_, rt["line"])[0] <= rt["width"] / 2
