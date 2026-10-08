"""Generate Riftwater from the plan: the red half's ground, underground, buildings and dressing, then blue's half
as its mirror image (pgmvox.orient.turn_world, with red's wool recoloured blue), then the objectives stamped
for both teams.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import dress
import ground
import plan as P
import under
import works
from pgmvox import B, World
from pgmvox.orient import turn_world

t0 = time.time()
L = P.land()
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=128)
ground.lay_ground(w, L)
ground.falls(w, L)
print(f"ground {time.time() - t0:.1f}s")
u = under.build(w, L)
print(f"underground {time.time() - t0:.1f}s: {u['carved']} blocks carved")
k = works.build(w, L, u["shaft_top"])
under.gaol_ladder(w)
print(f"buildings {time.time() - t0:.1f}s: {len(k['built'])} houses, headframe to {k['headframe_top']}")
d = dress.build(w, L)
print(f"dressing {time.time() - t0:.1f}s: {d['trees']} trees")
X, _ = w.grid()
turn_world(w, "mirror_x", X < 0, recolour={(B.WOOL, 14): (B.WOOL, 11)})
O = P.objectives()
O.stamp(w)
w.save(sys.argv[1], "Riftwater", (0, 90, 0))
print(f"saved {time.time() - t0:.1f}s; {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
