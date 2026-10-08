"""Cinder Reach's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png      (after plan_check.py, whose routes and table it draws)
"""
import json
import math
import os
import sys

import numpy as np

import plan as P
from pgmvox.sketch import TEAM, SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
R = P.build()
L = P.land()
O = P.objectives()
WAY = {"around the pond, north": (40, 90, 230), "around the pond, south": (90, 170, 250),
       "over the Spine's crag": (150, 60, 200), "up the lava tube": (230, 120, 30), "through Pumice Row": (30, 160, 150)}

S = Sheet("Cinder Reach - the plan (destroy the core)")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="kinds lit by height; blue's half (east) paler; numbers: floors of made ground; S spawn, C core; "
                 "dots: the build zone over the fissure; red: red's walk to its core; black lines: roads and paths",
          symmetry=R.symmetry)
m.raster(R, P.COLOURS, edges=False)
m.heights(R, kinds=["terrace", "bowl", "door"], min_cells=4, size=10)
m.zone(P.zone(R), (230, 200, 60), "dots", 5)
for r in L.routes:
    m.line(r["line"], (60, 40, 30), 1, both=True)
m.route([c[:2] for c in paths["own"]], TEAM["red"], 3, both=True)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
for key, b in P.houses().items():
    xs = [c[0] for c in b["cells"]]; zs = [c[1] for c in b["cells"]]
    m.rect(min(xs), min(zs), max(xs), max(zs), outline=(255, 240, 220), both=True)
m.objectives(O.markers())
cx, cz = P.CORE
m.callout(cx + 2, cz - 2, f"core over a vent: casing {P.CORE_Y}-{P.CORE_Y + 4}, bowl {P.BOWL_Y}, rim {P.RIM_Y}",
          dx=-60, dz=-70)
m.callout(*P.SPINE[-1], f"the crag, {P.SPINE_TOP}: 8 over the casing", dx=-40, dz=40)
x, _, z, _ = P.TUBE[0]
m.callout(x - 4, z, "tube mouth in the fissure face, floor 44", dx=40, dz=-50)
m.callout(*P.SPAWN[::2], "spawn terrace 57 under the Caldera Wall", dx=30, dz=40)
g = [int(r[0].split("-")[0]) for r in check["rows"] if r[1].startswith("the fissure")]
m.label(0, -66, "the fissure: build zone |x| <= 24", (20, 20, 20), 11)

# 2. the ways onto red's core
w = S.map(-100, -40, 30, 64, scale=5, title="THE WAYS ONTO RED'S CORE",
          legend="blue's cheapest walk by each way (colours as the table: N shore blue, S shore pale blue, crag "
                 "purple, tube orange, hamlet teal); red's walk to its core red; tube storey drawn over the ground")
w.raster(R, P.COLOURS, edges=False)
w.dim(0.5)
w.storey(R.storey(1), P.COLOURS, alpha=0.9, label=False)
for name, col in WAY.items():
    w.route([c[:2] for c in paths[name]], col, 3)
w.route([c[:2] for c in paths["own"]], TEAM["red"], 3)
for name, (x, z) in P.PLACES:
    if -100 <= x <= 30 and -40 <= z <= 64:
        w.place(x, z, name, size=11)
w.objectives(O.markers())
w.callout(-36, 6, "sinkhole: rings a block apart from the tube floor 43 to the wood 51", dx=-40, dz=-40)
w.callout(-60, 14, "west breach: a ramp, the defenders' door", dx=-60, dz=30)
w.callout(-40, 24, "east breach: the pond's side", dx=10, dz=-50)

# 3. sections
a = SectionPanel(-104, 30, 38, 76, scale=4, title="ACROSS THE CORE",
                 legend="along x at z 24, true scale: the wall, the hamlet, the bowl and the casing, the pond, the fissure")
a.raster(R, "x", 24, P.COLOURS)
a.band(cx - 2, cx + 3, P.CORE_Y, P.CORE_Y + 5, fill=(40, 20, 20), text="core")
a.band(cx - 2, cx + 3, P.VENT_BOTTOM, P.BOWL_Y + 1, fill=(20, 20, 24), text="vent")
a.level(P.CORE_Y - P.LEAK, f"leaks below {P.CORE_Y - P.LEAK}", (220, 110, 20), dash=True)
a.callout(cx + 9, P.RIM_Y + 1, "rim 56: a drop of 6 in", dx=20, dy=-20)
a.callout(-23, 51, "Steam Pond, 50", dx=10, dy=-24)
b = SectionPanel(-30, 64, 38, 76, scale=4, title="DOWN THE CORE",
                 legend="along z at x -51: Pumice Row's road, the bowl, the crag of the Spine at the south edge")
b.raster(R, "z", -51, P.COLOURS)
b.band(cz - 2, cz + 3, P.CORE_Y, P.CORE_Y + 5, fill=(40, 20, 20), text="core")
b.callout(47, P.SPINE_TOP + 1, "the crag 64", dx=-30, dy=-14)
S.row(a, b)
c = SectionPanel(-50, 30, 30, 70, scale=4, title="ALONG THE TUBE",
                 legend="along x at z 5: the sinkhole, the tube under the wood (storey 1), the fissure face")
c.raster(R, "x", 5, P.COLOURS)
for (x, z), y in sorted(P.tube_cells().items()):
    if z == 5 and R.storey(1).kind(x, z) == "tube":
        c.band(x, x + 1, y - 1, y + 1, fill=P.COLOURS["tube"])
c.callout(-12, 45, "mouth, 44: bridge down 7 to it", dx=20, dy=-20)
pts = [(x + 0.5, z + 0.5) for x, z in [p[:2] for p in paths["around the pond, north"]]]
ln = round(sum(math.dist(p, q) for p, q in zip(pts, pts[1:])))
d = SectionPanel(0, ln, 30, 80, scale=3, title="BLUE'S SHORTEST ATTACK",
                 legend="unrolled from blue's spawn round the pond's north shore; flat where it is bridged")
d.along(R, pts, P.COLOURS)
d.callout(1, 58, "blue spawn 57", dx=20, dy=-14, colour=TEAM["blue"])
d.callout(ln, 51, "red's bowl, 50", dx=-30, dy=-20)
S.row(c, d)
S.table([tuple(r) for r in check["rows"]], width=m.img.width)
S.save(sys.argv[1])
