"""Whitecliff Cistern's renders: the stack from two corners, red's half, the quay, the court and the oculus, the garden,
the boatyard, the rooftop walk; the vault in x-ray; four cuts; an elevation of the court's face; and the plan's names
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


iso("30-iso-board-se.png", 3, "se", ymin=36)
iso("31-iso-board-sw.png", 3, "sw", ymin=36)
iso("32-iso-red-half.png", 4, "se", (-60, -50, -1, 49), 50)
iso("33-iso-quay.png", 7, "se", (-60, -16, -42, 14), 62)
iso("34-iso-cistern-court.png", 6, "se", (-22, -22, 22, 22), 56)
iso("35-iso-garden.png", 6, "se", (-22, -50, 22, -26), 62)
iso("36-iso-boatyard.png", 6, "sw", (-22, 26, 22, 50), 58)
iso("37-iso-rooftop-walk.png", 6, "se", (-46, -26, -16, 24), 66)
under = w.ids.copy()
under[:, P.COURT + 1:, :] = 0
p = os.path.join(out, "40-xray-vault-and-undercroft.png")
render.iso(under, w.dat, w.x0, w.z0, p, 6, "se", (-42, -14, 42, 14), 50, 63, True)
render.trim(p)
render.cutaway(w, os.path.join(out, "10-section-z-1-middle-way.png"), [(-60, -0.5), (59, -0.5)], 44, 90, 5,
               title="along x at z -1: the quay, the cellar stair, the undercroft, the vault, the court, the mirror")
render.cutaway(w, os.path.join(out, "11-section-x-1-the-axis.png"), [(-0.5, -50), (-0.5, 49)], 44, 90, 5,
               title="along z at x -1: the garden, the north plaza, the court over the vault, the south plaza, the dock")
render.cutaway(w, os.path.join(out, "12-section-x-33-sailmakers-row.png"), [(-33.5, -50), (-33.5, 49)], 60, 90, 5,
               title="along z at x -34: the blocks and their roofs, the plank walk across the Middle Way")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-court-west-face.png"),
                 (-20, -14, -8, 14), 54, 82, look="east", scale=8)

R = P.build()
S = Sheet("Whitecliff Cistern - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=7, title="FROM ABOVE",
          legend="the built world's top blocks, the plan's names and objectives over them", symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=9)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
