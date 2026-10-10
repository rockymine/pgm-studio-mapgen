"""Slatefold's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
"""
import json
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
COL = P.COLOURS
KC = {i: COL[k] for k, i in R.kinds.items() if k in COL}


def wool_colour(name):
    return tuple(int(v) for v in K.COLOURS[K.B.WOOL, DYES[name]])


S = Sheet("Slatefold - the plan")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="number on each piece: its floor (y); yellow dots: build zones over void; S spawns; W monuments (team colour); "
                 "squares: wool rooms (wool colour); black: bedrock walls; ticks: stairs, rising; blue's half (south) paler",
          symmetry=P.SYM)
m.raster(R, COL, image_half=blue_half)
m.zone(P.zone_mask(R), colour=(230, 200, 60), step=4)
m.heights(R, kinds=["spawn", "row", "yard", "front", "quarry", "pit", "landing", "bench"], size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=9)
for o in O.of(Wool):
    x, _, z = o.found
    m.rect(x - 1, z - 1, x + 1, z + 1, fill=wool_colour(o.color), outline=(20, 20, 20), width=2)
m.objectives(O.markers())
m.callout(25, -57, "Cart Gantry: 2 flights, a wall", dx=14, dz=24)
m.callout(-60, -82, "Winding Path: 3 flights, a wall", dx=-12, dz=24)
m.callout(0, -7, "the band: 28 across, built over", dx=28, dz=0)

r = S.map(R.x_min, R.z_min, R.x_max, 0, scale=6, title="THE ROUTES onto red's two wool rooms",
          legend="the front line to each room (blue attacking) and red's spawn to each (red defending); both cross a bedrock wall "
                 "by building over it; a route crosses a build zone by bridging it", symmetry=P.SYM)
r.raster(R, COL, image_half=blue_half)
r.dim(0.55)
r.zone(P.zone_mask(R), colour=(150, 130, 50), step=4)
if "a_k" in paths:
    r.route(paths["a_k"], TEAM["blue"], width=3)
    r.route(paths["a_w"], TEAM["blue"], width=3)
    r.route(paths["s_k"], TEAM["red"], width=2)
    r.route(paths["s_w"], TEAM["red"], width=2)
r.callout(60, -68, "the Kiln", dx=-14, dz=-20)
r.callout(-75, -91, "the Winding House", dx=22, dz=-14)

a = SectionPanel(-80, 80, 30, 110, scale=5, title="ACROSS THE YARD AND THE GANTRY, z -58",
                 legend="west to east at z -58, true scale: the yard at 66, the Cart Gantry's flights and wall, the Quarry Floor and the Pit")
a.raster(R, "x", -58, KC, depth=4)
a.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
a.callout(25, 64, "the wall: 3 of bedrock", dx=0, dy=-26)
b = SectionPanel(-108, 0, 30, 110, scale=5, title="DOWN THE AXIS, x 0 (red's half)",
                 legend="north to south: the bank, the spawn at 74, the row at 70, the yard at 66, the Dressing Floor at 62, the band")
b.raster(R, "z", 0, KC, depth=4)
b.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
S.row(a, b)
c = SectionPanel(-80, -44, 30, 110, scale=7, title="THE WINDING PATH, west to east at z -81",
                 legend="the High Bench at 82, the flight, the second landing at 78 with its wall, the first at 74, the row at 70")
c.raster(R, "x", -81, KC, depth=4)
S.add(c)
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan; a build zone or a wall is crossed by building")
S.save(sys.argv[1])
