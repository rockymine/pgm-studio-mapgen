"""Overgrowth's renders: the valley from two corners, red's half, the court, the ziggurat, a tunnel and the chamber in
x-ray, the north gorge and its bridges, a watchtower; three cuts; an elevation of the ziggurat; and the plan's names
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


iso("30-iso-board-se.png", 3, "se", ymin=50)
iso("31-iso-board-sw.png", 3, "sw", ymin=50)
iso("32-iso-red-half.png", 4, "se", (-64, -48, -1, 47), 52)
iso("33-iso-court.png", 7, "se", (-64, -14, -40, 14), 58)
iso("34-iso-ziggurat.png", 6, "se", (-24, -22, 24, 22), 56)
iso("35-iso-north-gorge-and-bridges.png", 6, "se", (-64, -48, -2, -22), 50)
iso("36-iso-watchtower.png", 8, "sw", (-42, -48, -26, -34), 58)
render.cutaway(w, os.path.join(out, "10-section-z-8-the-tunnel.png"), [(-64, -7.5), (63, -7.5)], 50, 90, 6,
               title="along x at z -8: the court, the valley, the tunnel under the tiers, the mirror")
render.cutaway(w, os.path.join(out, "11-section-z-1-the-heart.png"), [(-24, -0.5), (24, -0.5)], 50, 90, 9,
               title="along x at z -1: the four tiers, the heart ladders, the chamber")
render.cutaway(w, os.path.join(out, "12-section-x-30-the-gorges.png"), [(-30.5, -48), (-30.5, 47)], 50, 90, 6,
               title="along z at x -31: the terraces, the gorges' streams, the valley between")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-ziggurat-from-the-court.png"),
                 (-24, -22, -6, 22), 56, 86, look="east", scale=8)

R = P.build()
S = Sheet("Overgrowth - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=7, title="FROM ABOVE",
          legend="the built world's top blocks, the plan's names and objectives over them", symmetry=R.symmetry)
m.built(w, ymin=40)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=10)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
