"""Claywork's renders: the board from two corners, red's half, the Gatehouse and Court, a Kiln and its Walk, the
front, the Undercroft in x-ray; three cuts; an elevation of a face; and the plan's names over the built top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World, render
from pgmvox.sketch import Sheet

build_dir, root = sys.argv[1], sys.argv[2]
w = World.load(build_dir)
out = os.path.join(root, "renders")


def iso(name, scale, corner, box=None, ymin=0, ymax=None, xray=False):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax, xray=xray)
    render.trim(p)


iso("30-iso-board-se.png", 3, "se")
iso("31-iso-board-nw.png", 3, "nw")
iso("32-iso-red-half-se.png", 5, "se", (-72, -104, 71, -1))
iso("33-iso-gatehouse-and-court-se.png", 7, "se", (-36, -102, 35, -38), 10)
iso("34-iso-west-kiln-and-walk-se.png", 7, "se", (-72, -100, -40, -28), 10)
iso("35-iso-front-and-steps-sw.png", 6, "sw", (-72, -42, 71, 12), 6)
iso("36-iso-arcade-and-stones-se.png", 7, "se", (-64, -66, -24, -26), 6)
iso("37-iso-apron-and-walk-floors-se.png", 10, "se", (-72, -75, -40, -13), 15)
iso("38-iso-court-forecourt-and-well-se.png", 7, "se", (-36, -70, 35, -12), 15)
iso("40-xray-undercroft.png", 5, "se", (-72, -70, 71, -48), 15, P.HUB, xray=True)

render.cutaway(w, os.path.join(out, "10-section-west-walk-x-66.png"), [(-65.5, -103), (-65.5, 0)], 0, 46, 5,
               title="the West Walk, along z at x -66")
render.cutaway(w, os.path.join(out, "11-section-rostrum-x10.png"), [(10.5, -103), (10.5, 0)], 0, 46, 5,
               title="through the Rostrum and a Statue Terrace, along z at x 10")
render.cutaway(w, os.path.join(out, "12-section-undercroft-z-63.png"), [(-72, -62.5), (71, -62.5)], 0, 46, 4,
               title="along the Undercroft, along x at z -63")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-forecourt-face-from-the-band.png"),
                 (-40, -20, 39, -8), 0, 30, look="north", scale=6)

R = P.plan()
S = Sheet("Claywork - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks, the plan's names and objectives over them", symmetry=R.symmetry)
m.built(w, ymin=0)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
