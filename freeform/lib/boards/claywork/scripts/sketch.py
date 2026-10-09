"""Claywork's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

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
R = P.plan()
O = P.objectives()
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
blue_half = (lambda x, z: z >= 0)
PIECE_KINDS = ["front", "rostrum", "apron", "terrace", "steps", "hub", "wing", "walk", "neck", "spawn", "kiln"]


def wool_colour(name):
    return tuple(int(v) for v in K.COLOURS[K.B.WOOL, DYES[name]])


S = Sheet("Claywork - a standard capture-the-wool board, the layout for review")

# 1. the board
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="number on each piece: its floor (y); every piece stands on bedrock, 12 of ground under its "
                 "surface; yellow dots: the band, built over; S spawns; W monuments; squares: the wools; "
                 "black bars: bedrock walls; grey: arch legs; brown: the Undercroft at 19, under the Court and Arcades "
                 "and in the well; blue's half (south) paler")
m.raster(R, P.COLOURS, image_half=blue_half)
m.zone(P.band_mask(R), colour=(230, 200, 60), step=4)
m.heights(R, kinds=PIECE_KINDS, size=10)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.label(0, 60, "blue's half: red's in a mirror", size=11)
for o in O.of(Wool):
    x, _, z = o.found
    m.rect(x - 1, z - 1, x + 1, z + 1, fill=wool_colour(o.color), outline=(20, 20, 20), width=2)
m.objectives(O.markers())
m.callout(-66, -71, "bedrock wall across the Walk, 12 wide, 3 high", dx=-10, dz=44)
m.callout(22, -35, "a flight at each end of the Forecourt, the Rostrum between", dx=8, dz=22)
m.callout(-45, -63, "balcony under the Arcade, open to the north; ladder up at its end", dx=6, dz=-34)
m.callout(3, -73, "Spawn Steps between the terraces", dx=40, dz=14)
m.callout(-40, -22, "build zones between Forecourt and Apron", dx=8, dz=24)
m.callout(-66, -77, "the Walk climbs 23 to 26 into the Kiln", dx=28, dz=-28)

# 2. the routes onto red's west wool
r = S.map(R.x_min, R.z_min, R.x_max, 0, scale=4, title="THE ROUTES onto red's wools",
          legend="blue attacking from the band (blue), red defending from its spawn (red); dashed: over the wall")
r.raster(R, P.COLOURS, image_half=blue_half)
r.dim(0.55)
r.zone(P.band_mask(R), colour=(150, 130, 50), step=4)
r.route(paths["band_west"], TEAM["blue"], width=3)
r.route(paths["spawn_west"], TEAM["red"], width=2)
r.route(paths["spawn_east"], TEAM["red"], width=2)
r.route(paths["undercroft"], (120, 70, 30), width=2)
r.callout(-62, -22, "attackers land on the Apron and climb the Walk", dx=40, dz=-6)
r.callout(-46, -58, "defenders come round by the Arcade", dx=30, dz=-16)
r.callout(20, -63, "brown: Walk to Walk through the Undercroft", dx=10, dz=26)

# 3. sections
COL = dict(P.COLOURS)


def upper(panel, axis, at, s0, s1):
    """The first storey (the Court and the Arcades over the Undercroft): its floor block over each column."""
    U = R.storeys[1]
    for s in range(s0, s1 + 1):
        x, z = (s, at) if axis == "x" else (at, s)
        if U.inside(x, z) and U.kind(x, z) != "none":
            panel.band(s, s + 1, U.h(x, z), U.h(x, z) + 1, fill=P.COLOURS[U.kind(x, z)])
BEDROCK = (44, 44, 48)


def bedrock(panel, axis, at, s0, s1):
    """Bedrock from the world's floor up to each piece's ground, the twelve blocks of ground drawn over it."""
    for s in range(s0, s1 + 1):
        x, z = (s, at) if axis == "x" else (at, s)
        if not R.inside(x, z) or R.piece[R.ix(x), R.iz(z)] == R.kinds["void"]:
            continue
        top = int(R.floor[R.ix(x), R.iz(z)]) - P.GROUND
        panel.band(s, s + 1, 0, top + 1, fill=BEDROCK)

a = SectionPanel(-104, 0, 0, 40, scale=5, title="ALONG THE WEST WALK",
                 legend="along z at x -66, true scale: Apron 20, up to 23, the wall, up to the Kiln at 26; dark: bedrock to the floor")
bedrock(a, "z", -66, -104, 0)
a.raster(R, "z", -66, COL, depth=P.GROUND)
a.level(P.MAX_BUILD, f"build to y {P.MAX_BUILD}")
a.callout(-71, 27, "the wall", dx=10, dy=-14)
a.callout(-90, 33, "the West Kiln", dx=10, dy=-10)

b = SectionPanel(-104, 0, 0, 40, scale=5, title="THROUGH THE ROSTRUM",
                 legend="along z at x 10: Forecourt 20, the Rostrum at 23, the Court over the Undercroft, "
                        "a Statue Terrace at 27, the Gatehouse")
bedrock(b, "z", 10, -104, 0)
b.raster(R, "z", 10, COL, depth=P.GROUND)
b.level(P.MAX_BUILD, f"build to y {P.MAX_BUILD}")
b.callout(-72, 27, "the Statue Terrace, 4 over the Court", dx=10, dy=-14)
upper(b, "z", 10, -104, 0)
b.callout(-63, 20, "the Undercroft", dx=10, dy=-24)

c = SectionPanel(P.X_MIN, P.X_MAX, 0, 40, scale=4, title="ALONG THE UNDERCROFT",
                 legend="along x at z -63: Walk, the balcony under the Arcade, the passage under the Court, the "
                        "well, and out the other side; the floors at 23 drawn over it")
bedrock(c, "x", -63, P.X_MIN, P.X_MAX)
c.raster(R, "x", -63, COL, depth=P.GROUND)
upper(c, "x", -63, P.X_MIN, P.X_MAX)
c.callout(-60, 22, "the ladder up to the Walk", dx=10, dy=-20)
c.callout(0, 20, "the well, open to the sky", dx=12, dy=-26)
S.row(a, b)
S.add(c)

# 4. the table
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan (a step up 1.2), the band bridged block for block")
S.save(sys.argv[1])
