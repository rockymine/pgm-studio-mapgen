"""Riftwater's renders, framed as the original board's were so the two can be laid side by side: the board from
the south-east and the north-west, the town, Ironhollow, the river and mill, the falls, the underground in
x-ray, true-scale cutaways, and the plan's names over the built top-down.

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


iso("30-iso-board-se.png", 2, "se")
iso("31-iso-board-nw.png", 2, "sw")
iso("33-iso-town.png", 4, "se", (-80, -88, -8, -10), 30)
iso("34-iso-village.png", 4, "se", (-112, 34, -64, 87), 30)
iso("35-iso-river-mill.png", 4, "se", (-92, -14, -26, 30), 30)
iso("38-iso-rift-falls.png", 4, "se", (-40, -20, 39, 24), 20)
iso("40-xray-underground.png", 3, "se", (-120, -50, -1, 70), 20, 62, True)
render.cutaway(w, os.path.join(out, "10-section-falls-cave-z3.png"), [(-120, 3), (119, 3)], 20, 90, 4,
               title="along x at z 3: the ridge, the pond, the mill race, the cave under the bank, the falls, the rift")
render.cutaway(w, os.path.join(out, "12-section-cellar-gaol-x-52.png"), [(-52, -50), (-52, 50)], 20, 80, 4,
               title="along z at x -52: the gaol and its cellar, the cave under the river, the sinkhole")
render.cutaway(w, os.path.join(out, "13-section-mine-shaft-z56.png"), [(-120, 56), (-40, 56)], 20, 90, 4,
               title="along x at z 56: the headframe over the shaft, the gallery")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "52-elev-rift-face-red-from-rift.png"),
                 (-20, -88, -8, 87), 0, 90, look="west", scale=4)

# the plan's names and markers over what was built, to show it landed where the plan said
R = P.build()
S = Sheet("Riftwater (pgmvox port) - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks; the plan's names, objectives and building footprints over them",
          symmetry=R.symmetry)
m.built(w)
for b in P.houses().values():
    x0 = min(c[0] for c in b["cells"]); x1 = max(c[0] for c in b["cells"])
    z0 = min(c[1] for c in b["cells"]); z1 = max(c[1] for c in b["cells"])
    m.rect(x0, z0, x1, z1, outline=(255, 255, 255), both=True)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
