"""Cinderfall's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
"""
import json
import math
import os
import sys

import plan as P
from pgmvox.sketch import TEAM, SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
R = P.build()
L = P.land()
O = P.objectives()
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
blue_half = (lambda x, z: x >= 0)
COL = {k: P.COLOURS[k] for k in P.KINDS}
KC = {i: COL[k] for k, i in R.kinds.items()}
ways_col = {"around": (230, 170, 40), "above": (120, 200, 255), "below": (200, 90, 220), "through": (120, 230, 130),
            "unseen": (240, 240, 240)}

S = Sheet("Cinderfall - the plan")

m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=5, title="THE BOARD",
          legend="shade is height (lighter is higher); orange: lava; roads tan, tracks brown; red/blue discs: spawns S "
                 "and cores C; the dashed ring is the 4-block clearance round a core; the half-turn image is paler",
          symmetry=P.SYM)
m.raster(R, COL, image_half=blue_half)
m.heights(R, kinds=["house", "inside", "plinth", "pit"], size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(O.markers())
cx, cz = P.CORE_AT
m.poly([(cx + 7.5 * math.cos(t / 20 * 2 * math.pi), cz + 7.5 * math.sin(t / 20 * 2 * math.pi)) for t in range(21)],
       outline=(255, 255, 255), both=True)
m.callout(-58, -2, "blowhole: the tube's mouth", dx=-30, dz=30)
m.callout(-22, 17, "the Cinder Pit: the tube's other mouth", dx=30, dz=34)
m.callout(-48, -33, "the ridge face: 16 sheer over the plinth's apron", dx=40, dz=-6)
m.callout(-4, -24, "the ravine: lava at 47, rim 58 to 70", dx=-30, dz=-10)
m.callout(-8, -1, "the Slag Bridge on its keystone", dx=14, dz=-26)

# the five ways onto red's core, from blue's spawn
r = S.map(R.x_min, R.z_min, 0, R.z_max, scale=7, title="THE FIVE WAYS ONTO RED'S CORE",
          legend="each from blue's spawn: gold around, blue above, violet below, green through, white unseen",
          symmetry=P.SYM)
r.raster(R, COL, image_half=blue_half)
r.dim(0.5)
for name, pts in paths.items():
    key = name.split(" ")[0]
    r.route(pts[::2] + pts[-1:], ways_col[key], width=3)
r.objectives([mk for mk in O.markers() if mk[0] < 0])
for name, (x, z) in P.PLACES:
    if x < 0:
        r.place(x, z, name, size=10)

# sections, true scale
a = SectionPanel(-90, 90, 0, 90, scale=5, title="ALONG THE AXIS, z -1", legend="west to east through the ravine: "
                 "the hold, the road, the bridge on its keystone; the kill height under the island's root")
a.raster(R, "x", -1, KC, depth=None)
a.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
a.level(P.LAVA_Y, "lava 47", colour=(230, 110, 30), dash=True)
b = SectionPanel(-62, 28, 40, 90, scale=7, title="ACROSS THE CORE, x -48",
                 legend="north to south: the ridge face, the plinth, the road, the foundry; the core's casing floats 7 over the plinth")
b.raster(R, "z", -48, KC, depth=None)
b.band(P.CORE_BOX.z0, P.CORE_BOX.z1 + 1, P.CORE_BOX.y0, P.CORE_BOX.y1 + 1, fill=(40, 20, 30), text="core")
b.callout(-40, 74, "ridge top 74", dx=20, dy=-12)
S.row(a, b)

S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan, the vent tube joined at both mouths")
S.save(sys.argv[1])
