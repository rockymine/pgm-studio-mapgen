"""Generate Islets from the plan: grass islands with tapering undersides, the hill in sandstone, a cloud deck far
below the kill height, and mountains far out."""
import sys

import numpy as np

from plan import GROUND, KILL_Y, build
from pgmvox import B, World, rng, terrain

R = build()
w = World(-110, -110, 220, 220, sy=120)
X, Z = w.grid()
H = terrain.mountain_ring(X, Z, clear=70, rise=30, base=20, relief=25, crest=40, seed=4, edge=110)
terrain.lay(w, np.where(H > 2, KILL_Y - 6 + H, 0).astype(int), mask=H > 2, snow_above=75)
terrain.cloud_deck(w, 5, seed=9)                       # its billows stay under the kill height
land = np.zeros((w.sx, w.sz), bool)
for x in range(R.x_min, R.x_max + 1):
    for z in range(R.z_min, R.z_max + 1):
        h, kind = R.at(x, z)
        if kind == "void":
            continue
        top = {"hill": (B.SANDSTONE, 2), "stair": (B.SANDSTONE, 0), "spawn": (B.STONEBRICK, 0)}.get(kind, (B.GRASS, 0))
        w.column(x, z, GROUND - 2, h - 1, B.DIRT)
        w.set(x, h, z, *top)
        land[x - w.x0, z - w.z0] = True
terrain.underside(w, land, GROUND - 2, rng=rng("islets", "underside"),
                  paint=lambda k, x, z: (B.STONE, 5) if k % 3 else (B.STONE, 0))
w.save(sys.argv[1], "Islets", (0, 40, 20))
print("generated")
