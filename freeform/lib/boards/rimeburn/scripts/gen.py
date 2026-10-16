"""Generate Rimeburn: lay Frost's half as winter, build in it, carry it onto Ember's half re-seasoned, then plant
each season's trees, dress each half, stamp the objectives and mark the ground.

    python3 gen.py <build-dir>
"""
import sys

import numpy as np

import ground as GR
import land as LD
import plan as P
import season as SE
import works as WK
from pgmvox import World, rng
from pgmvox import B
from pgmvox.play.rules import mark_ground

X, Z, H, land, water, surface = LD.build()
ramps = LD.ramp_cells(X, Z)
w = World(LD.X0, LD.Z0, X.shape[0], X.shape[1], sy=96)
north = Z < 0

# ---- Frost's ground, and the Thaw's north half ----------------------------------------------------------------
deg, masks = GR.lay(w, X, Z, H, land & north, water, surface, P.PATHS, ramps)
snapshot = w.ids.copy(), w.dat.copy()

# ---- what was built ---------------------------------------------------------------------------------------------
r = rng("rimeburn", "works")
WK.hold(w, H)
WK.hearth(w, H)
WK.shrine(w, r)
WK.hamlet(w, H, r)
WK.bridges(w, H, water)
WK.thaw_deck(w, H)
WK.vent(w, H, r)
WK.march(w, H, r)
WK.boulders(w, H, r)
WK.jetty(w, H)
falls = WK.falls(w, H)
WK.steps(w, H, ramps)
made = (w.ids != snapshot[0]) | (w.dat != snapshot[1])

# ---- Ember's half: the same, re-seasoned ------------------------------------------------------------------------
SE.carry(w, made, masks["path"])

# ---- the trees, each season's own -------------------------------------------------------------------------------
keep_clear = set()
for box in (P.CORE, P.ICESTONE):
    for x in range(box.x0 - 10, box.x1 + 11):
        for z in range(box.z0 - 10, box.z1 + 11):
            keep_clear |= {(x, z), LD.SYM.point(x, z)}
pathm = masks["path"]


from pgmvox.geom.shapes import edge_depth  # noqa: E402
inland = edge_depth(land) >= 5


def ok(x, z):
    i, k = x - LD.X0, z - LD.Z0
    return inland[i, k] and not water[i, k] and not pathm[i, k] and (x, z) not in keep_clear


stood = SE.plant_trees(w, ok, rng("rimeburn", "trees"))
SE.dress_frost(w, made, masks["hollow"], H)
SE.thaw_line(w, made)
SE.croft_yard(w, rng("rimeburn", "croft"))
clear = keep_clear | {(x, z) for x in range(LD.X0, LD.X1 + 1) for z in range(LD.Z0, LD.Z1 + 1)
                      if pathm[x - LD.X0, z - LD.Z0]}
SE.dress_ember(w, clear, rng("rimeburn", "ember"))
SE.ember_falls(w, falls)

# ---- the objectives, the void's marks, the save ------------------------------------------------------------------
from pgmvox.read import audit  # noqa: E402
for x, y, z, why in audit.footing(w):
    if w.id(x, y, z) == B.SNOW_LAYER:
        w.set(x, y, z, B.AIR)
P.objectives().stamp(w)
marked = mark_ground(w)
w.save(sys.argv[1], "Rimeburn", (0, 62, 0))
print(f"land {int(land.sum())} columns, {len(stood)} trees, {marked} columns marked at y 0")
