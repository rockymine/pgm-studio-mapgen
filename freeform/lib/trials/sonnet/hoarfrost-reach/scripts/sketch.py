"""Hoarfrost Reach's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
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
R = P.build()
O = P.objectives()
try:
    with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
        check = json.load(f)
except FileNotFoundError:
    check = dict(rows=[], paths={})
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
blue_half = (lambda x, z: z >= 0)
COL = P.KIND_COLOURS
KC = {i: COL[k] for k, i in R.kinds.items() if k in COL}


def wool_colour(name):
    return tuple(int(v) for v in K.COLOURS[K.B.WOOL, DYES[name]])


S = Sheet("Hoarfrost Reach - the plan")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="number on each piece: its floor (y); yellow dots: build zones over void; S spawns; W monuments (team colour); "
                 "squares: wool rooms (wool colour); ticks: stairs, rising; blue's half (south) paler", symmetry=P.SYM)
m.raster(R, COL, image_half=blue_half)
m.zone(P.zone_mask(R), colour=(230, 200, 60), step=4)
m.heights(R, kinds=[p[0] for p in P.PIECES if p[4] is not None], size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=10)
for o in O.of(Wool):
    x, _, z = o.found
    m.rect(x - 1, z - 1, x + 1, z + 1, fill=wool_colour(o.color), outline=(20, 20, 20), width=2)
m.objectives(O.markers())
m.callout(-62, -55, "12 of air: a build zone", dx=-10, dz=30)
m.callout(62, -66, "Glacier Stair: 20 up, 9 wide", dx=40, dz=-20)
m.callout(0, -53, "frozen pond: a void, 13 across", dx=0, dz=26)

r = S.map(R.x_min, R.z_min, R.x_max, 0, scale=6, title="THE ROUTES onto red's two wool rooms",
          legend="the band's edge to each room (blue attacking) and red's spawn to each (red defending); a route crosses a build "
                 "zone by bridging it", symmetry=P.SYM)
r.raster(R, COL, image_half=blue_half)
r.dim(0.55)
r.zone(P.zone_mask(R), colour=(150, 130, 50), step=4)
if "a_lh" in paths:
    r.route(paths["a_lh"], TEAM["blue"], width=3)
    r.route(paths["a_hall"], TEAM["blue"], width=3)
    r.route(paths["s_lh"], TEAM["red"], width=2)
    r.route(paths["s_hall"], TEAM["red"], width=2)
r.callout(-78, -60, "the Lighthouse: ladder up the tower", dx=10, dz=-30)
r.callout(62, -84, "the Ice Hall", dx=-30, dz=-8)

a = SectionPanel(-88, 88, 40, 108, scale=5, title="ALONG THE CAUSEWAYS, z -55",
                 legend="west to east, true scale: the Lighthouse stack and its tower, the 12-block gap, the strand, the East Causeway, the shelf")
a.raster(R, "x", -55, KC, depth=4)
a.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
a.band(-82, -74, 72, 98, fill=(90, 100, 120), text="tower")
a.callout(-62, 74, "the gap: 12 of air", dx=10, dy=-24)
b = SectionPanel(-100, 0, 40, 108, scale=5, title="DOWN THE AXIS, x 0 (red's half)",
                 legend="the skald, the strand, the breakwater, the band: north to south")
b.raster(R, "z", 0, KC, depth=4)
b.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
S.row(a, b)
c = SectionPanel(-80, -44, 40, 108, scale=8, title="UP THE GLACIER STAIR, x 62",
                 legend="north to south: the Ice Hall at 92, the landing, twenty stairs down to the shelf at 72")
c.raster(R, "z", 62, KC, depth=4)
S.add(c)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan; a build zone is crossed by bridging it")
S.save(sys.argv[1])
