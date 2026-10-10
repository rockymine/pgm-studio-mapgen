"""Abbeymoor's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
"""
import json
import os
import sys

import plan as P
from pgmvox.sketch import TEAM, SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
R = P.build()
O = P.objectives()
try:
    with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
        check = json.load(f)
except FileNotFoundError:
    check = dict(rows=[], paths={})
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
blue_half = (lambda x, z: z >= 0)
COL = P.COLOURS
KC = {i: COL[k] for k, i in R.kinds.items() if k in COL}

S = Sheet("Abbeymoor - the plan")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="shaded by height (the abbey hill at 80, the moor at 66, the bog at 61); olive: the green and the orchards; sand: roads; "
                 "brown: the peat; dark blue: water; M the monuments in team colour; S spawns; blue's half (south) paler", symmetry=P.SYM)
m.raster(R, COL, image_half=blue_half)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=9)
m.objectives(O.markers())
m.callout(-40, -72, "Monument A, over a dais, in the open nave", dx=-34, dz=-16)
m.callout(30, -70, "Monument B, on the green", dx=30, dz=-16)
m.callout(-1, -12, "the Standing Stones in the bog", dx=36, dz=18)
m.callout(14, -60, "the cellar stair: the crypt passage comes up here", dx=40, dz=22)

r = S.map(R.x_min, R.z_min, R.x_max, 0, scale=4, title="THE WAYS onto red's two monuments",
          legend="blue's spawn to each monument over the ground, by the shortest walk; the dashed ways below are on the next panel", symmetry=P.SYM)
r.raster(R, COL, image_half=blue_half)
r.dim(0.55)
if "A" in paths:
    r.route(paths["A"], TEAM["blue"], width=3)
    r.route(paths["B"], TEAM["blue"], width=3)
r.callout(-40, -72, "A: over the hill, up the Monks' Way", dx=-20, dz=-24)
r.callout(30, -70, "B: across the green", dx=22, dz=-10)

u = S.map(-70, -100, 40, -40, scale=7, title="UNDER THE ABBEY: the crypt, the Night Stair and the passage (storey 1)",
          legend="the crypt hall at 70 under the nave, the Night Stair up to the chancel (east), the passage south and east under the hill and the valley to the "
                 "Tithe Barn's cellar stair; the nave and the barn faint over it", symmetry=None)
u.raster(R, COL, image_half=lambda x, z: False)
u.dim(0.5)
u.storey(R.storeys[1], COL)
u.callout(-48, -72, "the crypt: 70", dx=-10, dz=-18)
u.callout(-36, -69, "the Night Stair, 10 up", dx=10, dz=-20)
u.callout(-20, -61, "the passage: 60 blocks, 59 at its lowest", dx=0, dz=16)
u.callout(15, -61, "the cellar stair, 7 up", dx=0, dz=18)

a = SectionPanel(-100, 0, 40, 100, scale=4, title="ACROSS THE ABBEY HILL, z -72", legend="west to east: the moor, the hill, the plateau, the village valley, true scale")
a.raster(R, "x", -72, KC, depth=4)
a.level(P.KILL_Y + 40, "")
b = SectionPanel(-132, 0, 40, 100, scale=4, title="DOWN THE AXIS, x -42 (red's half)", legend="north to south through the ridge, Hall Farm, the abbey hill and the moor down into the bog")
b.raster(R, "z", -42, KC, depth=4)
S.row(a, b)
S.table([tuple(row) for row in check["rows"]], width=m.img.width, legend="walked octile over the plan, the storeys joined by their stairs")
S.save(sys.argv[1])
