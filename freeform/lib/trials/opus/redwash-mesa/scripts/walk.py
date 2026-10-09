"""Read Redwash Mesa back from the built world: each spawn to its own two monuments on foot and to the enemy's by
bridging the seam, the cut stairs and the drift walked, every objective checked and every block's footing.

    python3 walk.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from pgmvox import World, audit, walk

t0 = time.time()
w = World.load(sys.argv[1])
R = P.build()
L = P.land()
X, Z = w.grid()
zone = np.abs(X + 0.5) <= P.SEAM + 0.5
foot = walk.MoveRules(max_drop=3)
drop = walk.MoveRules(max_drop=12)                               # a drop off the Shelf (eleven) is a choice
building = walk.MoveRules(max_drop=3, build=(zone, (36, P.MAX_BUILD)))
out = []


def reach(d, x, y, z, r=2):
    n = walk.nearest(d, w.x0, w.z0, x, y, z, r)
    return "not reached" if n is None else n


def mon(d, key, team):
    (x, z), _ = P.MONUMENTS[key]
    if team == "blue":
        x, z = P.SYM.point(x, z)
    return reach(d, x, P.at(L, *((x, z) if team == "red" else P.SYM.point(x, z))) + 1, z, 2)


bx, bz = P.SYM.point(P.SPAWN[0], P.SPAWN[2])
spawns = {"red": P.SPAWN, "blue": (bx, P.SPAWN[1], bz)}
for team, sp in spawns.items():
    other = "blue" if team == "red" else "red"
    d = walk.walk(w.ids, [sp], w.x0, w.z0, foot)
    db = walk.walk(w.ids, [sp], w.x0, w.z0, building)
    out.append(f"{team} spawn {sp}: {int((d >= 0).sum())} places on foot (drops of three at most)")
    for key in P.MONUMENTS:
        out.append(f"  to its own {key} monument, on foot: {mon(d, key, team)}")
        out.append(f"  to the enemy's {key} monument, on foot: {mon(d, key, other)}; bridging: {mon(db, key, other)}")
    x, y, z = P.mine_line()[-1]
    if team == "blue":
        x, z = P.SYM.point(x, z)
    out.append(f"  onto its own Table by the drift's shaft head: {reach(d, x, P.TABLE + 1, z, 3)}")
out.append(f"[{time.time() - t0:.0f}s]")

# the drift: from its portal on the canyon floor, along the gallery, up the shaft onto the Table
mx, my, mz = P.mine_line()[0]
d = walk.walk(w.ids, [(mx, my, mz)], w.x0, w.z0, foot)
ex, ey, ez = P.mine_line()[-1]
out.append(f"from the Silver Drift's portal ({mx}, {my}, {mz}): to the gallery's end {reach(d, ex, ey, ez, 1)}, "
           f"up the shaft onto the Table {reach(d, ex, P.TABLE + 1, ez, 3)}, "
           f"to the table monument {mon(d, 'table', 'red')}")
# off the Shelf onto the wash monument: the drop is taken
sh = (-47, P.SHELF + 1, 15)
d = walk.walk(w.ids, [sh], w.x0, w.z0, drop)
out.append(f"from the Shelf over the town {sh}, dropping: to the wash monument {mon(d, 'wash', 'red')}")
d = walk.walk(w.ids, [sh], w.x0, w.z0, foot)
out.append(f"from the Shelf, no drop past three: to the wash monument {mon(d, 'wash', 'red')}, "
           f"to the spawn {reach(d, *P.SPAWN)}")

problems = P.objectives().check(w)
out.append(f"objectives with a problem: {len(problems)}")
out += [f"   {p}" for p in problems]
f = audit.footing(w)
out.append(f"footing problems: {len(f)}")
kinds = {}
for x, y, z, why in f:
    kinds.setdefault(why, []).append((x, y, z))
for why, cells in sorted(kinds.items(), key=lambda kv: -len(kv[1])):
    out.append(f"   {len(cells):4d}  {why}  e.g. {cells[:3]}")
island = R.K != R.kinds["void"]
st = walk.no_stand_above(w, 0, np.ones(X.shape, bool), island)
out.append(f"standable columns off the land (over the void): {len(st)} {st[:5]}")
out.append(f"[{time.time() - t0:.0f}s]")
print("\n".join(out))
