"""Cinder Reach's renders: the board from two corners, red's cone and its ways in, the lodge and Pumice Row, the
tube in x-ray, true-scale cuts through the core and along the tube, and the plan's names over the built top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import numpy as np

import plan as P
from pgmvox import World, render
from pgmvox.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")


def iso(name, scale, corner, box=None, ymin=0, ymax=None, xray=False, ids=None):
    p = os.path.join(out, name)
    render.iso(w.ids if ids is None else ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax, xray)
    render.trim(p)


iso("30-iso-board-se.png", 2, "se")
iso("31-iso-board-nw.png", 2, "nw")
iso("32-iso-red-cone-se.png", 5, "se", (-76, 2, -8, 60), 30)
iso("33-iso-lodge-and-row-se.png", 5, "se", (-104, -30, -56, 26), 35)
iso("34-iso-north-flats-sw.png", 4, "sw", (-70, -72, 0, -10), 35)
under = w.ids.copy()                                            # the x-ray: only what is under red's ground
L = P.land()
for i, k in np.argwhere(L.land):
    under[i, int(L.H[i, k]) - 1:, k] = 0
iso("40-xray-tube.png", 6, "se", (-44, -6, -6, 16), 30, 56, True, under)
render.cutaway(w, os.path.join(out, "10-section-core-z24.png"), [(-104, 24.5), (103, 24.5)], 30, 80, 4,
               title="along x at z 24: the Caldera Wall, Pumice Row, red's cone and core, the pond, the fissure, blue's shelf")
render.cutaway(w, os.path.join(out, "11-section-core-x-51.png"), [(-50.5, -40), (-50.5, 66)], 30, 80, 4,
               title="along z at x -51: the knolls, the hamlet road, the cone over its vent, the Spine's crag")
render.cutaway(w, os.path.join(out, "12-section-tube-z5.png"), [(-50, 5.5), (10, 5.5)], 30, 70, 6,
               title="along x at z 5: the sinkhole, the lava tube, its mouth in the fissure face")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-cone-from-the-pond.png"),
                 (-68, 8, -40, 40), 40, 70, look="west", scale=8)

R = P.build()
S = Sheet("Cinder Reach - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks; the plan's names, objectives and building footprints over them",
          symmetry=R.symmetry)
m.built(w)
for b in P.houses().values():
    xs = [c[0] for c in b["cells"]]; zs = [c[1] for c in b["cells"]]
    m.rect(min(xs), min(zs), max(xs), max(zs), outline=(255, 255, 255), both=True)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
