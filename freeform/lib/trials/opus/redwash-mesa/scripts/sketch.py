"""Redwash Mesa's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png      (after plan_check.py, whose routes and table it draws)
"""
import json
import math
import os
import sys

import plan as P
from pgmvox.sketch import TEAM, SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
R = P.build()
L = P.land()
O = P.objectives()
WAYS = [(30, 70, 220), (100, 170, 250), (40, 160, 90), (230, 130, 30), (150, 60, 200), (220, 60, 140)]

S = Sheet("Redwash Mesa - the plan (destroy the monument)")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="kinds lit by height; blue's half (east) paler; numbers: floors; S spawn, M monuments; dots: the "
                 "build zone over the seam; red: red's walks to its monuments; dark lines: trails",
          symmetry=R.symmetry)
m.raster(R, P.COLOURS, edges=False)
m.heights(R, kinds=["table", "shelf", "wash", "plaza"], min_cells=60, size=10)
m.zone(P.zone(R), (230, 200, 60), "dots", 5)
for r in L.routes:
    m.line(r["line"], (90, 50, 30), 1, both=True)
for key in P.MONUMENTS:
    m.route([c[:2] for c in paths[f"own {key}"]], TEAM["red"], 3, both=True)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
for b in P.houses().values():
    xs = [c[0] for c in b["cells"]]; zs = [c[1] for c in b["cells"]]
    m.rect(min(xs), min(zs), max(xs), max(zs), outline=(90, 60, 30), both=True)
m.objectives(O.markers())
m.callout(-70, 2, "the Ladder: 10 steps cut up the cliff, 52 to 62", dx=-20, dz=-60)
m.callout(-76, 18, "the Head stair: 9 down to the Wash", dx=-30, dz=50)
m.callout(-38, 36, "the Bench stair: 11 up", dx=40, dz=40)
m.callout(*P.SHAFT, "the Silver Drift's shaft onto the Table", dx=30, dz=-40)

w = S.map(-96, -64, 4, 63, scale=5, title="THE WAYS ONTO RED'S MONUMENTS",
          legend="blue's cheapest walk by each way onto the table monument (north) and the wash monument (south); "
                 "the gallery (storey 1) drawn over the ground")
w.raster(R, P.COLOURS, edges=False)
w.dim(0.5)
w.storey(R.storey(1), P.COLOURS, alpha=0.9, label=False)
names = [k for k in paths if " | " in k]
for col, name in zip(WAYS * 2, names):
    w.route([c[:2] for c in paths[name]], col, 3)
for key in P.MONUMENTS:
    w.route([c[:2] for c in paths[f"own {key}"]], TEAM["red"], 3)
w.objectives(O.markers())
for name, (x, z) in P.PLACES:
    w.place(x, z, name, size=11)

a = SectionPanel(-64, 63, 34, 74, scale=4, title="ACROSS THE CANYON",
                 legend="along z at x -47, true scale: the Table and the drift's shaft, the Shelf, the town and its "
                        "monument, the Bench and its stair")
a.raster(R, "z", -47, P.COLOURS)
for key, ((x, z), _) in P.MONUMENTS.items():
    if key == "wash":
        g = P.at(L, x, z)
        a.band(z, z + 1, g + 2, g + 4, fill=(20, 10, 30), text="")
a.callout(15, 53, "the Shelf 52: 11 over the town", dx=-20, dy=-24)
a.callout(28, 43, "wash monument, floor 40", dx=20, dy=-30)
b = SectionPanel(-96, 0, 34, 74, scale=4, title="DOWN THE WASH",
                 legend="along x at z 24: the head stair, the Wash stepping down 43 to 40 toward the seam (the Gate)")
b.raster(R, "x", 24, P.COLOURS)
b.callout(-8, 41, "the Gate: 18 to bridge at 40", dx=-40, dy=-20)
S.row(a, b)
c = SectionPanel(-96, 0, 34, 74, scale=4, title="ACROSS THE TABLE",
                 legend="along x at z -24: the cliff house's cliff, the table monument, the rock pool at 58, the rim")
c.raster(R, "x", -24, P.COLOURS)
mx, mz = P.MONUMENTS["table"][0]
c.band(mx, mx + 1, P.TABLE + 2, P.TABLE + 4, fill=(20, 10, 30))
c.callout(mx, P.TABLE + 4, "table monument, two over 62", dx=20, dy=-12)
c.callout(-30, 58, "the rock pool", dx=10, dy=-20)
pts = [(x + 0.5, z + 0.5) for x, z in [p[:2] for p in paths["own wash"]]]
ln = round(sum(math.dist(p, q) for p, q in zip(pts, pts[1:])))
d = SectionPanel(0, ln, 34, 74, scale=4, title="RED'S WALK TO ITS WASH MONUMENT",
                 legend="unrolled from the ledge: down the head stair, along the floor")
d.along(R, pts, P.COLOURS)
d.callout(1, 53, "spawn 52", dx=20, dy=-14, colour=TEAM["red"])
S.row(c, d)
S.table([tuple(r) for r in check["rows"]], width=m.img.width)
S.save(sys.argv[1])
