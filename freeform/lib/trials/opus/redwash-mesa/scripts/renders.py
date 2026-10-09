"""Redwash Mesa's renders: the board from two corners, red's canyon town and its monument, the cliff house and the
cut stairs, the table monument and the rock pool, the drift in x-ray, cuts across the canyon and down the Wash,
and the plan's names over the built top-down.

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
iso("31-iso-board-sw.png", 2, "sw")
iso("32-iso-arroyo-town-se.png", 6, "se", (-72, 12, -30, 42), 30, 51)   # cut at 51: the walls off
iso("33-iso-cliff-house-se.png", 5, "se", (-96, -8, -62, 30), 34)
iso("34-iso-table-monument-sw.png", 5, "sw", (-70, -40, -14, -8), 50)
iso("35-iso-the-gate-se.png", 4, "se", (-30, 10, 29, 46), 30)
under = w.ids.copy()
L = P.land()
for i, k in np.argwhere(L.land):
    under[i, int(L.H[i, k]) - 1:, k] = 0
iso("40-xray-silver-drift.png", 6, "se", (-50, -10, -30, 26), 34, 64, True, under)
render.cutaway(w, os.path.join(out, "10-section-canyon-x-47.png"), [(-46.5, -64), (-46.5, 63)], 30, 76, 4,
               title="along z at x -47: the Table, the drift's shaft, the Shelf, Arroyo Town and its monument, the Bench")
render.cutaway(w, os.path.join(out, "11-section-wash-z24.png"), [(-96, 24.5), (95, 24.5)], 30, 76, 4,
               title="along x at z 24: the head stairs, the Wash stepping to the seam, the Gate, blue's Wash")
render.cutaway(w, os.path.join(out, "12-section-table-z-24.png"), [(-96, -23.5), (95, -23.5)], 30, 76, 4,
               title="along x at z -24: the Table, both table monuments, both rock pools, the seam")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-cliff-house-from-the-wash.png"),
                 (-96, -2, -66, 24), 38, 72, look="north", scale=7)

R = P.build()
S = Sheet("Redwash Mesa - as built")
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
