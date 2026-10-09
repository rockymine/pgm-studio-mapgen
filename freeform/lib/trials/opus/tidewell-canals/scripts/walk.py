"""Read Tidewell Canals back from the built world: each spawn to each hill on foot, the gallery reached by its
stair, a swimmer out of the canal by the steps, what the built pads see of a spawn court, every objective checked
and every block's footing.

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


def best(d, cells, y):
    vals = [walk.nearest(d, w.x0, w.z0, x, y, z, 0) for x, z in cells]
    vals = [v for v in vals if v is not None]
    return min(vals) if vals else "not reached"


bx, bz = P.SYM.point(P.SPAWN_AT[0], P.SPAWN_AT[2])
spawns = {"red": P.SPAWN_AT, "blue": (bx, P.SPAWN_AT[1], bz)}
reached = None
for team, sp in spawns.items():
    d = walk.walk(w.ids, [sp], w.x0, w.z0, foot)
    reached = (d >= 0) if reached is None else reached | (d >= 0)
    out.append(f"{team} spawn {sp}: {int((d >= 0).sum())} places on foot")
    for h in ("campo", "north-market", "south-market"):
        out.append(f"  to {h}'s pad: {best(d, P.pad_cells(h), P.STREET + 1)}")
    gx0, gz0, gx1, gz1 = P.GALLERY_SPAN
    gal = [(x, z) for x in range(gx0, gx1 + 1) for z in range(gz0, gz1 + 1)]
    if team == "blue":
        gal = [P.SYM.point(x, z) for x, z in gal]
    out.append(f"  onto the gallery: {best(d, gal, P.GALLERY + 1)}")
out.append(f"[{time.time() - t0:.0f}s]")
d = walk.walk(w.ids, [(-18, P.WATER, -40)], w.x0, w.z0, foot)
out.append(f"a swimmer in the Grand Canal at (-18, 38, -40): out onto the quay {best(d, [(-22, -40), (-14, -40)], P.STREET + 1)}"
           f", to the Campo's pad {best(d, P.pad_cells('campo'), P.STREET + 1)}")

op = sight.voxel_opaque(w)
x0, z0, x1, z1 = P.CUSTOMS
court = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, -1 - z0 + 1)]
court += [P.SYM.point(x, z) for x, z in court]
targets = [sight.target(x, P.STREET + 1, z) for x, z in court[::3]]
for h in ("campo", "north-market", "south-market"):
    eyes = [sight.eye(x, P.STREET + 1, z) for x, z in P.pad_cells(h)]
    hid = sight.hidden(targets, eyes, op)
    out.append(f"spawn courts seen from {h}'s built pad: {len(targets) - len(hid)} of {len(targets)}")
gal_eyes = []
for i, y, k in np.argwhere(reached):
    x, z = int(i + w.x0), int(k + w.z0)
    if y >= P.GALLERY + 1:
        gal_eyes.append(sight.eye(x, y, z))
pad_t = [sight.target(x, P.STREET + 1, z) for x, z in P.pad_cells("campo")]
out.append(f"reached places at or over the gallery's height: {len(gal_eyes)}; centre pad cells they see: "
           f"{len(pad_t) - len(sight.hidden(pad_t, gal_eyes, op))} of {len(pad_t)}")
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
X, Z = w.grid()
lagoon = np.vectorize(lambda x, z: R.kind(x, z) == "lagoon")(X, Z)
out.append(f"lagoon columns a player reaches from a spawn: {int((reached.any(axis=1) & lagoon).sum())}")
out.append(f"[{time.time() - t0:.0f}s]")
print("\n".join(out))
