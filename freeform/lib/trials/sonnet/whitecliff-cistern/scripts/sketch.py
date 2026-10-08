"""Whitecliff Cistern's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

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
COL = P.COLOURS
KC = {i: COL[k] for k, i in R.kinds.items() if k in COL}
WAY = {"cistern": (230, 170, 40), "garden": (120, 230, 130), "boatyard": (120, 200, 255)}

S = Sheet("Whitecliff Cistern - the plan")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=7, title="THE BOARD",
          legend="the town from above: white blocks, tan streets, the sunken court, the garden (green), the dock (blue), the quay; "
                 "gold squares: the three hills; S spawns; the mirrored half is paler", symmetry=P.SYM)
m.raster(R, COL, image_half=blue_half)
m.heights(R, kinds=["quay", "court", "garden", "dock", "hill"], size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=9)
m.objectives(O.markers())
m.callout(0, 0, "the Oculus: a drop of six onto the pad", dx=40, dz=-30)
m.callout(-34, 0, "the cellar stair: a slot in the street, 14 down", dx=-10, dz=26)

r = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=7, title="THE WAYS onto the three hills, from red's spawn",
          legend="gold onto the Cistern (stairwells, the oculus, the undercroft), green onto the Garden, blue onto the Boatyard",
          symmetry=P.SYM)
r.raster(R, COL, image_half=blue_half)
r.dim(0.55)
for name, pts in paths.items():
    key = name.split(":")[0]
    r.route(pts[::2] + pts[-1:], WAY[key], width=2)
r.objectives(O.markers())

a = SectionPanel(-60, 60, 40, 90, scale=7, title="ACROSS THE TOWN, z -1 (the Middle Way)",
                 legend="west to east: the quay, Harbour Street, the cellar stair's slot, the ring, the sunken court, the mirror")
a.raster(R, "x", -1, KC, depth=4)
b = SectionPanel(-50, 50, 40, 90, scale=7, title="DOWN THE AXIS, x -1 (the garden, the court, the dock)",
                 legend="north to south: the garden at 72, North Plaza at 70, the court at 62 over the vault at 56, South Plaza, the dock at 66")
b.raster(R, "z", -1, KC, depth=4)
S.add(a)
S.add(b)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan; a drop costs 1.5 a block past three")
S.save(sys.argv[1])
