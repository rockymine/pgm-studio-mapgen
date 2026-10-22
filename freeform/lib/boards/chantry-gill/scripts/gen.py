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
from pgmvox.document import layers                                                     # noqa: E402

doc, grids = TR.document(), TR.arrays()
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
gill = L.mask(L.GILL, built.X, built.Z) & land
print(f"  gill floor y {int(H[gill].min())}, rims to y {int(np.percentile(H[gill], 95))}")
w.save(sys.argv[1], "chantry-gill", (0.5, 70, 0.5))
print("generated")
