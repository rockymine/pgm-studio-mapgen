"""Tidewell Canals' sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png      (after plan_check.py, whose routes and table it draws)
"""
import json
import os
import sys

import plan as P
from pgmvox.sketch import TEAM, SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
R = P.build()
O = P.objectives()

S = Sheet("Tidewell Canals - the plan (king of the hill)")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=5, title="THE BOARD",
          legend="kinds lit by height; blue's half (east) paler; A: hills (gold, the centre worth 2, the flanks 1); "
                 "S spawns; dark: walls and large cover; brown: small cover; the gallery (storey 1) drawn over the Campo",
          symmetry=R.symmetry)
m.raster(R, P.COLOURS, edges=True)
m.storey(R.storey(1), P.COLOURS, alpha=0.6, label=False)
m.heights(R, kinds=["street", "campo", "court", "market"], min_cells=40, size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
lx0, lz0, lx1, lz1 = P.LOGGIA
m.rect(lx0, lz0, lx1, lz1, outline=(120, 80, 40), width=2, both=True)
m.objectives(O.markers())
m.callout(-40, -3, "the column: no line from the Campo's pad to the spawn", dx=-10, dz=50)
m.callout(-8, -26, "the gallery stair, 41 to 45", dx=-60, dz=-20)
m.callout(-21, -29, "steps out of the water", dx=-40, dz=-20)
m.callout(0, -50, "the north pad under the loggia's roof at 46", dx=60, dz=-6)

r = S.map(R.x_min, R.z_min, 0, R.z_max, scale=5, title="RED'S WALKS TO THE THREE HILLS",
          legend="red's cheapest walk to the Campo (gold) and to each fish market (red); blue's are their images")
r.raster(R, P.COLOURS, edges=False)
r.dim(0.5)
r.route([c[:2] for c in paths["campo"]], (220, 170, 40), 3)
for h in ("north-market", "south-market"):
    r.route([c[:2] for c in paths[h]], TEAM["red"], 3)
r.objectives(O.markers())

a = SectionPanel(-80, 79, 32, 60, scale=3, title="SPAWN TO SPAWN",
                 legend="along x at z -1, true scale: the customs houses, the column, the bridges over both Grand Canals, the Campo")
a.raster(R, "x", -1, P.COLOURS)
a.level(P.WATER, "the water, 38", (60, 108, 205))
b = SectionPanel(-64, 63, 32, 60, scale=3, title="FLANK TO FLANK",
                 legend="along z at x 0: the loggia over the north pad, the Rio and its bridge, the Campo under the "
                        "gallery, the south market")
b.raster(R, "z", -8, P.COLOURS)
b.band(-24, -20, P.GALLERY, P.GALLERY + 1, fill=P.COLOURS["gallery"], text="")
b.band(P.LOGGIA[1], P.LOGGIA[3] + 1, P.LOGGIA_ROOF, P.LOGGIA_ROOF + 1, fill=(120, 80, 40))
S.row(a)
S.add(b)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan (a step up 1.2); sight from eyes 1.62 over each floor, roofs and the gallery solid")
S.save(sys.argv[1])
