"""Cinderfall's renders: the island from two corners, red's half, the spawn, the core and its plinth, the ridge, the
Foundry Row, the caldera, the underground in x-ray; three cuts; an elevation of the ridge face; and the plan's names
over the built top-down.

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


def iso(name, scale, corner, box=None, ymin=0, ymax=None, xray=False):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax, xray)
    render.trim(p)


iso("30-iso-board-se.png", 2, "se", ymin=12)
iso("31-iso-board-sw.png", 2, "sw", ymin=12)
iso("32-iso-red-half.png", 3, "se", (-90, -60, -1, 59), 30)
iso("33-iso-spawn-hold.png", 6, "se", (-90, 0, -64, 36), 52)
iso("34-iso-core-plinth.png", 6, "se", (-70, -26, -34, 6), 50)
iso("35-iso-slag-ridge.png", 5, "sw", (-86, -58, -22, -20), 50)
iso("36-iso-foundry-row.png", 6, "se", (-70, 0, -28, 32), 48)
iso("37-iso-caldera.png", 4, "se", (-34, -34, 34, 34), 30)
# the x-ray keeps every roofed void: clear everything over the plan's ground first, so only the tube is seen
L = P.land()
under = w.ids.copy()
for i, k in np.argwhere(L.land):
    under[i, int(L.H[i, k]) - 2:, k] = 0
p = os.path.join(out, "40-xray-vent-tube.png")
render.iso(under, w.dat, w.x0, w.z0, p, 5, "se", (-70, -12, -14, 24), 40, 60, True)
render.trim(p)
render.cutaway(w, os.path.join(out, "10-section-axis-z-1.png"), [(-90, -0.5), (89, -0.5)], 8, 90, 4,
               title="along x at z -1: the hold, the road, the rim, the lake, and back")
render.cutaway(w, os.path.join(out, "11-section-core-x-48.png"), [(-47.5, -58), (-47.5, 56)], 8, 90, 4,
               title="along z at x -48: the ridge, the core's casing over its plinth, the road, the foundry")
render.cutaway(w, os.path.join(out, "12-section-vent-tube.png"), [(-22.5, 17.5), (-34.5, 12.5), (-42.5, 7.5),
                                                                    (-50.5, 2.5), (-58.5, -2.5)], 36, 66, 8,
               title="the vent tube, from the Cinder Pit to the blowhole")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-ridge-face-from-the-plinth.png"),
                 (-84, -50, -26, -22), 50, 82, look="north", scale=6)

R = P.build()
S = Sheet("Cinderfall - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=5, title="FROM ABOVE",
          legend="the built world's top blocks over the kill height; the plan's names, objectives and buildings over them",
          symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for b in P.houses().values():
    xs = [c[0] for c in b["cells"]]
    zs = [c[1] for c in b["cells"]]
    m.rect(min(xs), min(zs), max(xs), max(zs), outline=(255, 255, 255), both=True)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
