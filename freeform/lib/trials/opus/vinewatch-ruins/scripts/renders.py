"""Vinewatch Ruins' renders: the bowl from two corners, red's gate-court and its screen, the ziggurat and its lid,
the causeway and the court, the cistern in x-ray, cuts down the middle and across the lanes, and the plan's names
over the built top-down.

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


def iso(name, scale, corner, box=None, ymin=0, ymax=None, xray=False, ids=None):
    p = os.path.join(out, name)
    render.iso(w.ids if ids is None else ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax, xray)
    render.trim(p)


iso("30-iso-board-se.png", 3, "se", ymin=30)
iso("31-iso-board-nw.png", 3, "nw", ymin=30)
iso("32-iso-gate-court-se.png", 6, "se", (-20, -54, 20, -26), 36)
iso("33-iso-ziggurat-sw.png", 6, "sw", (-22, -22, 22, 22), 36)
iso("34-iso-causeway-and-marsh-se.png", 5, "se", (-46, -42, -18, 10), 33)
iso("35-iso-sunken-court-sw.png", 5, "sw", (20, -42, 46, 10), 33)
under = w.ids.copy()
under[:, P.CISTERN_Y + 7:, :] = 0                                # everything over the cistern's roof lifted off
iso("40-xray-cistern.png", 5, "se", (-46, -10, 34, 10), 30, 46, False, under)
render.cutaway(w, os.path.join(out, "10-section-middle-x0.png"), [(0.5, -56), (0.5, 55)], 30, 62, 5,
               title="along z at x 0: red's gate-court, the screen, the ziggurat and its lid over the cistern hall, blue's")
render.cutaway(w, os.path.join(out, "11-section-lanes-z-10.png"), [(-48, -9.5), (47, -9.5)], 30, 62, 5,
               title="along x at z -10: the marsh, the causeway, the broken wall, the ziggurat, the court")
render.cutaway(w, os.path.join(out, "12-section-cistern-z0.png"), [(-48, -0.5), (47, -0.5)], 30, 62, 5,
               title="along x at z 0: the stairwell in the marsh, the cistern, its hall, the stairwell into the court")

R = P.build()
S = Sheet("Vinewatch Ruins - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=6, title="FROM ABOVE",
          legend="the built world's top blocks; the plan's names and spawns over them", symmetry=R.symmetry)
m.built(w, ymin=30)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=12)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
