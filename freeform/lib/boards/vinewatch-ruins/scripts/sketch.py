"""Vinewatch Ruins' sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

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
blue_half = (lambda x, z: z >= 0)
LANE_COL = {"the Causeway": (40, 90, 230), "the Plaza and the Ziggurat": (200, 40, 40),
            "the Sunken Court": (230, 130, 30), "the Cistern": (150, 60, 200)}

S = Sheet("Vinewatch Ruins - the plan (team deathmatch)")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=7, title="THE BOARD",
          legend="number on each piece: its floor; dark: walls and large cover; brown: small cover (3 high); "
                 "grey dots: pillars; S spawns; blue's half (south) paler; the cistern (storey 1) drawn over the middle")
m.raster(R, P.COLOURS, image_half=blue_half)
m.storey(R.storey(1), P.COLOURS, alpha=0.55, label=False)
m.heights(R, kinds=["plaza", "causeway", "court", "spawn", "tier1", "tier2", "tier3", "marsh", "jungle"],
          min_cells=8, size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=12)
m.objectives(O.markers())
m.callout(0, -33, "the screen, 8 high: the south gate's way out turns", dx=60, dz=-20)
m.callout(-15, -46, "baffle: the side gate is seen only from behind it", dx=-50, dz=-30)
m.callout(0, 0, "top tier 46 under a lid at 51", dx=70, dz=26)
m.callout(-38, 0, "the cistern's stairwell up into the marsh", dx=-20, dz=50)

r = S.map(R.x_min, R.z_min, R.x_max, 4, scale=7, title="THE LANES: red's quickest way to the middle by each",
          legend="blue: by the Causeway; red: by the Plaza and the Ziggurat; orange: by the Sunken Court; purple: by "
                 "the Cistern (under the plaza)")
r.raster(R, P.COLOURS, image_half=blue_half)
r.dim(0.5)
r.storey(R.storey(1), P.COLOURS, alpha=0.6, label=False)
for name, col in LANE_COL.items():
    r.route([c[:2] for c in paths[name]], col, 3)
r.objectives(O.markers())

a = SectionPanel(-56, 55, 30, 62, scale=5, title="DOWN THE MIDDLE",
                 legend="along z at x 0, true scale: red's gate-court, the screen, the ziggurat and its lid, blue's")
a.raster(R, "z", 0, P.COLOURS)
a.band(-6, 6, P.SHRINE_ROOF, P.SHRINE_ROOF + 1, fill=(120, 120, 110), text="")
a.band(-7, 7, P.CISTERN_Y, P.CISTERN_Y + 4, fill=(90, 110, 140), text="cistern")
a.callout(-45, P.SPAWN_Y + 1, "spawn 44", dx=10, dy=-20, colour=TEAM["red"])
b = SectionPanel(-48, 47, 30, 62, scale=5, title="ACROSS THE LANES",
                 legend="along x at z -10: the marsh and the causeway, the plaza's broken wall, the ziggurat, the court")
b.raster(R, "x", -10, P.COLOURS)
b.band(-38, 25, P.CISTERN_Y, P.CISTERN_Y + 4, fill=(90, 110, 140), text="cistern (z -3 to 2)")
S.row(a, b)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan (a step up 1.2), jumps included; sight from eyes 1.62 over each floor")
S.save(sys.argv[1])
