"""Tamarisk Wash's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
"""
import json
import os
import sys

import plan as P
from pgmvox.sketch import SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
R = P.build()
O = P.objectives()
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
blue_half = (lambda x, z: x >= 0)
COL = {k: P.COLOURS[k] for k in P.KINDS}
KC = {i: COL[k] for k, i in R.kinds.items()}
WAY = {"steps": (230, 170, 40), "mine": (200, 90, 220), "arch": (120, 200, 255), "lanes": (230, 170, 40),
       "roofs": (120, 200, 255), "qanat": (200, 90, 220), "grove": (240, 240, 240)}

S = Sheet("Tamarisk Wash - the plan")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=5, title="THE BOARD",
          legend="shade is height; sand and clay by kind, blue is water, dark blue-grey the qanat; red/blue discs: spawns S "
                 "and monuments M; the mirrored half is paler; the wash runs down the middle", symmetry=P.SYM)
m.raster(R, COL, image_half=blue_half)
m.heights(R, kinds=["house", "inside", "square", "deck"], size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(O.markers())
m.callout(-14, 0, "the aqueduct: 8 blocks of air between its halves", dx=-40, dz=-30)
m.callout(P.WELL[0], P.WELL[1], "the well: ladder to the cistern", dx=-20, dz=30)
m.callout(-50, -36, "the old salt mine: gallery and ladder to the top", dx=-30, dz=-16)

r = S.map(R.x_min, R.z_min, 0, R.z_max, scale=7, title="THE WAYS ONTO RED'S TWO MONUMENTS",
          legend="each from blue's spawn: gold the direct way, violet below, blue above, white unseen", symmetry=P.SYM)
r.raster(R, COL, image_half=blue_half)
r.dim(0.5)
for name, pts in paths.items():
    key = name.split(":")[1].strip().split(" ")[0]
    r.route(pts[::2] + pts[-1:], WAY[key], width=3)
r.objectives([mk for mk in O.markers() if mk[0] < 0])
for name, (x, z) in P.PLACES:
    if x < 0:
        r.place(x, z, name, size=10)

a = SectionPanel(-100, 100, 30, 100, scale=5, title="ACROSS THE WASH, z -28 (the north ghats and Table Rock)",
                 legend="west to east, true scale: the kasbah's terrace, the plateau, Table Rock, the ghat, the wash floor, its mirror")
a.raster(R, "x", -28, KC, depth=None)
b = SectionPanel(-100, 100, 30, 100, scale=5, title="ACROSS THE WASH, z 24 (the south ghats, the serai, the souk)",
                 legend="west to east: the souk's square, the caravanserai, the ghat, the wash floor and the mirror")
b.raster(R, "x", 24, KC, depth=None)
S.add(a)
S.add(b)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan; the qanat, the well's ladder and the mine joined by links")
S.save(sys.argv[1])
