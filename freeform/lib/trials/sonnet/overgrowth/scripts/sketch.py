"""Overgrowth's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

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
LANE = {"centre, over the tiers": (230, 170, 40), "centre, through the tunnel": (200, 90, 220),
        "north terrace": (120, 200, 255), "south terrace": (120, 200, 255), "valley, north flank": (120, 230, 130),
        "valley, south flank": (120, 230, 130)}

S = Sheet("Overgrowth - the plan")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=7, title="THE BOARD",
          legend="number on each piece: its floor (y); green valley, blue ford, dark green terraces, tan courts and tiers, brown "
                 "bridges and platforms; S spawns; the mirrored half is paler", symmetry=P.SYM)
m.raster(R, COL, image_half=blue_half)
m.heights(R, kinds=["tier1", "tier2", "tier3", "tier4", "court", "tower", "chamber"], size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=10)
m.objectives(O.markers())
m.callout(-34, -41, "watchtower: ladder to a platform at 78", dx=-30, dz=-4)
m.callout(-30, -32, "gorge: a stream between banks", dx=0, dz=30)
m.callout(0, -8, "the tunnel: an H under the tiers", dx=40, dz=-4)

r = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=7, title="THE LANES between the spawns",
          legend="gold over the tiers, violet through the tunnel, blue the terraces, green the valley's flanks; each walked from red's spawn to blue's",
          symmetry=P.SYM)
r.raster(R, COL, image_half=blue_half)
r.dim(0.55)
for name, pts in paths.items():
    r.route(pts[::2] + pts[-1:], LANE[name], width=3)
r.objectives(O.markers())

a = SectionPanel(-64, 64, 40, 100, scale=7, title="ALONG THE AXIS, z -8 (through the tunnel)",
                 legend="west to east, true scale: the court on its platform, the valley, the four tiers of the ziggurat, the mirror")
a.raster(R, "x", -8, KC, depth=4)
b = SectionPanel(-64, 64, 40, 100, scale=7, title="ALONG THE GORGE, z -32",
                 legend="west to east: the stream's bed 55, the bridges over it, the watchtower's footing")
b.raster(R, "x", -32, KC, depth=4)
S.add(a)
S.add(b)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan; the H of tunnels and the towers' ladders joined by links")
S.save(sys.argv[1])
