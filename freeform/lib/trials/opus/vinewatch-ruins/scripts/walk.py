"""Read Vinewatch Ruins back from the built world: each spawn to the middle by each lane on foot, the cistern walked
end to end, what the built middle sees of a spawn court, every objective checked and every block's footing.

    python3 walk.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from pgmvox import World, audit, sight, walk

t0 = time.time()
w = World.load(sys.argv[1])
R = P.build()
foot = walk.MoveRules(max_drop=3)
out = []


def best(d, cells, y_lo, y_hi):
    vals = []
    for x, z in cells:
        for y in range(y_lo, y_hi + 1):
            v = walk.nearest(d, w.x0, w.z0, x, y, z, 0)
            if v is not None:
                vals.append(v)
    return min(vals) if vals else "not reached"


lanes = {"the Causeway": ([(x, -1) for x in range(-38, -27)], 43, 43),
         "the Plaza / Ziggurat": ([(x, -1) for x in range(-21, 21)], 41, 47),
         "the Sunken Court": ([(x, -1) for x in range(26, 41)], 37, 37),
         "the Cistern": ([(x, -1) for x in range(-30, 21)], P.CISTERN_Y + 1, P.CISTERN_Y + 1)}
bx, bz = P.SYM.point(P.SPAWN_AT[0], P.SPAWN_AT[2])
for team, sp in (("red", P.SPAWN_AT), ("blue", (bx, P.SPAWN_AT[1], bz))):
    d = walk.walk(w.ids, [sp], w.x0, w.z0, foot)
    out.append(f"{team} spawn {sp}: {int((d >= 0).sum())} places on foot")
    for name, (cells, lo, hi) in lanes.items():
        if team == "blue":
            cells = [(x, 0) for x, _ in cells]
        out.append(f"  to the middle by {name}: {best(d, cells, lo, hi)}")
out.append(f"[{time.time() - t0:.0f}s]")
d = walk.walk(w.ids, [(-43, 40, 0)], w.x0, w.z0, foot)
out.append(f"from the marsh's stairwell (-43, 40, 0): along the cistern to the court's stairwell "
           f"{best(d, [(28, 0)], 36, 38)}, into the hall {best(d, [(0, -6)], P.CISTERN_Y + 1, P.CISTERN_Y + 1)}")

# what the built middle sees of red's spawn court: eyes over every standing place with |z| <= 12, sampled
st, _ = walk.standing(w.ids)
op = sight.voxel_opaque(w)
eyes = []
reached = (walk.walk(w.ids, [P.SPAWN_AT, (bx, P.SPAWN_AT[1], bz)], w.x0, w.z0, walk.MoveRules(max_drop=None)) >= 0)
out.append(f"standing places a player cannot reach (wall, pillar and lid tops; no building here): "
           f"{int((st & ~reached).sum())}")
for i, y, k in np.argwhere(st & reached):
    x, z = int(i + w.x0), int(k + w.z0)
    if abs(z + 0.5) <= 12 and (x + z + y) % 3 == 0 and y > P.CISTERN_Y + 3:
        eyes.append(sight.eye(x, y, z))
targets = [sight.target(x, P.SPAWN_Y + 1, z) for x, z in P.spawn_cells("red")[::3]]
hid = sight.hidden(targets, eyes, op)
out.append(f"red's spawn court seen from the built middle: {len(targets) - len(hid)} of {len(targets)} sampled cells "
           f"({len(eyes)} eyes)")

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
reach = walk.walk(w.ids, [P.SPAWN_AT], w.x0, w.z0, walk.MoveRules(max_drop=None))
X, Z = w.grid()
rim = np.vectorize(lambda x, z: R.kind(x, z) == "rim")(X, Z)
escaped = int(((reach >= 0).any(axis=1) & rim).sum())
out.append(f"rim columns a player reaches (out of bounds): {escaped}")
out.append(f"[{time.time() - t0:.0f}s]")
print("\n".join(out))
