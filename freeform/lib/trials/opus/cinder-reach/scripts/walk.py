"""Read Cinder Reach back from the built world: each spawn to its own core on foot, the enemy's core by bridging
the fissure, the tube walked from its mouth to the sinkhole, the crag and the cone's breaches, the core's leak,
every objective checked and every block's footing.

    python3 walk.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from pgmvox import B, World, audit, walk

t0 = time.time()
w = World.load(sys.argv[1])
R = P.build()
X, Z = w.grid()
zone = (np.abs(X + 0.5) <= P.RENT + 0.5)
foot = walk.MoveRules(max_drop=6)                                # a drop of six into the bowl costs a heart and a half
building = walk.MoveRules(max_drop=6, build=(zone, (40, P.MAX_BUILD)))
out = []


def reach(d, x, y, z, r=2):
    n = walk.nearest(d, w.x0, w.z0, x, y, z, r)
    return "not reached" if n is None else n


def ring_best(d, team):
    cx, cz = P.CORE if team == "red" else P.SYM.point(*P.CORE)
    vals = [walk.nearest(d, w.x0, w.z0, x, P.BOWL_Y + 1, z, 0) for x, z in P.core_ring(team)]
    vals = [v for v in vals if v is not None]
    return min(vals) if vals else "not reached"


spawns = {"red": P.SPAWN, "blue": (*P.SYM.point(P.SPAWN[0], P.SPAWN[2])[:1], P.SPAWN[1],
                                   P.SYM.point(P.SPAWN[0], P.SPAWN[2])[1])}
for team, sp in spawns.items():
    other = "blue" if team == "red" else "red"
    d = walk.walk(w.ids, [sp], w.x0, w.z0, foot)
    db = walk.walk(w.ids, [sp], w.x0, w.z0, building)
    out.append(f"{team} spawn {sp}: {int((d >= 0).sum())} places on foot")
    out.append(f"  to its own core, on foot: {ring_best(d, team)}")
    out.append(f"  to the enemy's core, on foot: {ring_best(d, other)}  (the fissure is bridged)")
    out.append(f"  to the enemy's core, bridging: {ring_best(db, other)}")
    tx, ty, tz, _ = P.TUBE[2]
    if other == "blue":
        tx, tz = P.SYM.point(tx, tz)
    out.append(f"  into the enemy's lava tube, bridging to its mouth: {reach(db, tx, ty, tz)}")
    sx, sz = P.SPINE[-1]
    if other == "blue":
        sx, sz = P.SYM.point(sx, sz)
    out.append(f"  onto the enemy's crag: {reach(db, sx, P.SPINE_TOP + 1, sz, 3)}")
out.append(f"[{time.time() - t0:.0f}s]")

(kx, kz), _, kf = P.SINK
st, _ = walk.standing(w.ids)
x, z = -13, 4                                                    # the tube's last cell inside the fissure face
y = next(y for y in range(40, 50) if st[x - w.x0, y, z - w.z0])
d = walk.walk(w.ids, [(x, y, z)], w.x0, w.z0, foot)
out.append(f"from the tube's mouth ({x}, {y}, {z}), on foot:")
out.append(f"  to the sinkhole floor: {reach(d, kx, kf + 1, kz, 2)}")
out.append(f"  out of the sinkhole onto the wood: {reach(d, kx - 9, P.at(P.land(), kx - 9, kz) + 1, kz, 2)}")
out.append(f"  to red's core: {ring_best(d, 'red')}")
out.append(f"  standing room in the face at the mouth: {[(xx, yy) for xx in range(-12, -9) for yy in range(42, 49) if st[xx - w.x0, yy, z - w.z0]]}")

# the core leaks: the vent's floor under the casing, against the leak distance
cx, cz = P.CORE
open_ = [y for y in range(P.CORE_Y - 1, 0, -1) if w.id(cx, y, cz) != B.AIR]
out.append(f"red's core: the first block under the casing is {P.CORE_Y - open_[0]} down (leak {P.LEAK}): "
           f"{'leaks' if P.CORE_Y - open_[0] > P.LEAK else 'CANNOT LEAK'}")
out.append(f"red's core: a player beside it stands at {P.BOWL_Y + 1}, under the casing's {P.CORE_Y}: "
           f"{'the vent is shut to players' if P.CORE_Y - (P.BOWL_Y + 1) < 2 else 'a player can walk under it'}")

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
out.append(f"standable columns off the islands (over the void): {len(st)} {st[:5]}")
out.append(f"[{time.time() - t0:.0f}s]")
print("\n".join(out))
