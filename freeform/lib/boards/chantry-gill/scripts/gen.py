"""Chantry Gill: build the board. At this stage the base terrain alone: the islands, the gill and the highlands.

    python3 gen.py <build-dir>
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import terrain as TR                                                                   # noqa: E402
import layout as L                                                                     # noqa: E402
import objectives as OB                                                                # noqa: E402
from pgmvox.play.rules import mark_ground                                              # noqa: E402
from pgmvox.document import layers                                                     # noqa: E402

grids = TR.arrays()
doc = TR.document(grids)
built = layers.build(doc, arrays=grids)
w = built.world
for s in built.steps:
    print(f"{s.stage:9} {s.id:10} {int(np.asarray(s.changed).sum()):6} columns  {s.note}")
H, land = built.H, built.land
print(f"\nland: {int(land.sum())} columns a team; heights {int(H[land].min())} to {int(H[land].max())}")
piece = grids["piece"]
for k, (_, _, r, name) in enumerate(L.SEEDS):
    m = (piece == k) & land
    if m.any():
        print(f"  {name:12} +{r:<3} {int(m.sum()):5} columns, top y {int(H[m].max())}, "
              f"{'scenery' if r > L.SCENERY_RISE else 'foothill'}")
x0, z0 = int(built.X[0, 0]), int(built.Z[0, 0])
for name, (x, z) in (("spawn", L.SPAWN), ("town monument", L.MONUMENTS[0]), ("scar monument", L.MONUMENTS[1])):
    print(f"  {name:14} ({x}, {z}) ground y {int(H[x - x0, z - z0])}")
gill = (grids['gill'] > 0.5) & land
print(f"  gill floor y {int(H[gill].min())}, rims to y {int(np.percentile(H[gill], 95))}, "
      f"{int(gill.sum())} columns")
bench = L.mask(L.BENCH, built.X, built.Z) & land
print(f"  scar bench y {int(np.median(H[bench]))} (median), plateau to y {int(H[L.mask(L.SIDE, built.X, built.Z) & land].max())}")
O = OB.objectives()
O.stamp(w)
print(f"\nmonuments stamped; ground marked under {mark_ground(w)} columns")
problems = O.check(w)
print(f"objectives with a problem: {len(problems)}")
for p in problems:
    print("   ", p)
w.save(sys.argv[1], "chantry-gill", (0.5, 80, 0.5))
print("generated")
