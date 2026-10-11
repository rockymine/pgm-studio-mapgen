"""Brassmoor Works' sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png      (after plan_check.py, whose routes and table it draws)
"""
import json
import math
import os
import sys

import plan as P
from pgmvox import blocks as K
from pgmvox.objectives import DYES, Wool
from pgmvox.sketch import TEAM, SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
R = P.build()
O = P.objectives()
blue_half = (lambda x, z: z >= 0)
COL = P.KIND_COLOURS


def wool_colour(name):
    return tuple(int(v) for v in K.COLOURS[K.B.WOOL, DYES[name]])


S = Sheet("Brassmoor Works - the plan (capture the wool)")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="number on each piece: its floor; yellow dots: build zones; S spawns; W monuments; squares: wool "
                 "rooms in their wool's colour; black bars: bedrock lines; brown: the rooms' walls; blue's half (south) paler")
m.raster(R, COL, image_half=blue_half)
m.zone(P.zone_mask(R), colour=(230, 200, 60), step=4)
m.heights(R, kinds=[p[0] for p in P.PIECES], size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
for o in O.of(Wool):
    x, _, z = o.found
    m.rect(x - 1, z - 1, x + 1, z + 1, fill=wool_colour(o.color), outline=(20, 20, 20), width=2)
m.objectives(O.markers())
m.callout(-58, -84, "bedrock line: 3 high and a web, 4 before the room", dx=20, dz=-14)
m.callout(-67, -73, "the south door: the second way in", dx=-10, dz=70)
m.callout(0, -71, "Turntable Pit: void in the Yard", dx=50, dz=30)
m.callout(*P.SPAWN_AT[::2], "spawn on the Gatehouse, 70; monuments on its front edge", dx=40, dz=8)

r = S.map(R.x_min, R.z_min, R.x_max, 0, scale=4, title="THE ROUTES onto red's wools",
          legend="from the band's edge on red's side: blue by the lane over the bedrock line (dark blue) and by the "
                 "flats (light blue); red from its spawn (red)")
r.raster(R, COL, image_half=blue_half)
r.dim(0.55)
r.zone(P.zone_mask(R), colour=(150, 130, 50), step=4)
for key in P.ROOMS:
    r.route(paths[f"lane {key}"], TEAM["blue"], 3)
    r.route(paths[f"flats {key}"], (110, 170, 240), 3)
    r.route(paths[f"own {key}"], TEAM["red"], 2)
r.objectives(O.markers())

a = SectionPanel(-88, 40, 20, 96, scale=4, title="ACROSS THE BOILER HOUSE",
                 legend="along x at z -78, true scale: the room, the bedrock line on the Gantry, the Yard, the Spur")
a.raster(R, "x", -78, COL, depth=6)
a.band(-88, 40, P.SMOG_Y[0], P.SMOG_Y[1], fill=(200, 200, 205), text="smog")
a.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
a.callout(-58, 70, "the line, 66 + 4", dx=10, dy=-24)
b = SectionPanel(-112, 0, 20, 96, scale=4, title="SPAWN TO THE BAND",
                 legend="along z at x -34: the Gantry, the Yard, the West Quay, the band")
b.raster(R, "z", -34, COL, depth=6)
b.level(P.KILL_Y, "kill")
b.band(-11, 0, 60, 64, fill=(230, 200, 60), text="build")
S.row(a, b)
pts = [(x + 0.5, z + 0.5) for x, z in [c[:2] for c in paths["flats boiler"]]]
ln = round(sum(math.dist(p, q) for p, q in zip(pts, pts[1:])))
c = SectionPanel(0, ln, 40, 90, scale=4, title="BLUE ONTO THE BOILER HOUSE BY THE FLATS",
                 legend="unrolled from the band's edge; where nothing is drawn the way is bridged")
c.along(R, pts, COL, depth=6)
c.level(P.KILL_Y, "kill")
S.add(c)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan (a step up 1.2), build zones and bedrock lines bridged block for block")
S.save(sys.argv[1])
