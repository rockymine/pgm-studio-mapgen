"""Lantern Karst's sketch: the plan drawn and annotated before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
"""
import json
import os
import sys

from plan import (KILL_Y, MIST_Y, PIECE, PLACES, SPAWN_AT, WALL, KIND_COLOURS, build, objectives, zone_mask)
from pgmvox.objectives import DYES, Wool
from pgmvox.sketch import TEAM, SectionPanel, Sheet
from pgmvox import blocks as K

HERE = os.path.dirname(os.path.abspath(__file__))
R, flights, walls = build()
O = objectives()
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
PIECE_KINDS = [p for p in PIECE]
blue_half = (lambda x, z: z >= 0)                      # the paler half; the library's default is x >= 0


def wool_colour(name):
    return tuple(int(v) for v in K.COLOURS[K.B.WOOL, DYES[name]])


S = Sheet("Lantern Karst - the plan, ported onto pgmvox")

# 1. the board
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
          legend="number on each piece: its floor (y); yellow dots: build zones over void; S spawns; "
                 "W monuments (team colour); squares: wool rooms (wool colour); black bar: the bedrock wall; "
                 "ticks: stairs, rising; blue's half (south) paler")
m.raster(R, KIND_COLOURS, image_half=blue_half)
m.zone(zone_mask(R), colour=(230, 200, 60), step=4)
m.heights(R, kinds=PIECE_KINDS, size=10)
for name, (x, z) in PLACES:
    m.place(x, z, name, size=11)
m.label(0, 60, "blue's half: red's turned half a circle", size=11)
for o in O.of(Wool):                                     # the rooms: Wool.marker() draws only the monument
    x, _, z = o.found
    m.rect(x - 1, z - 1, x + 1, z + 1, fill=wool_colour(o.color), outline=(20, 20, 20), width=2)
m.objectives(O.markers())
for x0, z0 in ((WALL["x0"], WALL["z0"]), R.symmetry.point(WALL["x1"], WALL["z1"])):
    m.rect(x0, z0, x0 + WALL["x1"] - WALL["x0"], z0 + 1, fill=(0, 0, 0))
m.callout(-72, -79, "the Ledges at 46: drop 20, water bucket", dx=-30, dz=40)
m.callout(56, -82, "bedrock wall, 13 before the room", dx=40, dz=-10)
m.callout(*SPAWN_AT[::2], "red spawn, Pool Terrace 72", dx=50, dz=-30)
m.callout(-2, -87, "two flights of stairs up from the exits", dx=-60, dz=10)

# 2. the routes onto red's wools
r = S.map(R.x_min, R.z_min, R.x_max, 0, scale=4, title="THE ROUTES onto red's two wools",
          legend="blue attacking from the band (blue), red defending from its spawn (red); a route crosses "
                 "a build zone by bridging it")
r.raster(R, KIND_COLOURS, image_half=blue_half)
r.dim(0.55)
r.zone(zone_mask(R), colour=(150, 130, 50), step=4)
r.route(paths["band_pillar"], TEAM["blue"], width=3)
r.route(paths["band_store"], TEAM["blue"], width=3)
r.route(paths["spawn_pillar"], TEAM["red"], width=2)
r.route(paths["spawn_store"], TEAM["red"], width=2)
r.callout(-62, -94, "the Pillar: bridge 16 from either Arm or the Terrace", dx=40, dz=-30)
r.callout(56, -104, "the Store: three ways onto one road", dx=-40, dz=-14)
r.callout(-56, -36, "the Mist Steps", dx=-40, dz=20)
r.callout(55, -24, "the Tea Steps", dx=40, dz=20)

# 3. sections: the Pillar's pit, the Store Road, and the attack on the Pillar unrolled
COL = {k: v for k, v in KIND_COLOURS.items()}
a = SectionPanel(-100, -25, 20, 92, scale=5, title="THE PILLAR'S PIT", legend="along x at z -93, true scale")
a.band(-100, -25, MIST_Y[0], MIST_Y[1], fill=(232, 234, 238))
a.raster(R, "x", -93, COL, depth=7)
for key in ("ledge-w", "ledge-e"):
    x0, _, x1, _ = PIECE[key][3]
    a.band(x0, x1 + 1, PIECE[key][4] - 6, PIECE[key][4], fill=(100, 120, 180), text="46")
a.level(KILL_Y, f"kill below y {KILL_Y}")
a.callout(-62, 75, "the shrine at 74: 16 off each Arm, 7 up", dx=20, dy=-20)
a.callout(-72, 46, "Ledges (behind, z -79): 20 down", dx=12, dy=-40)
a.callout(-88, 68, "Far Arm 67", dx=10, dy=-30)
a.callout(-37, 68, "Near Arm 67", dx=10, dy=-30)

b = SectionPanel(-114, -36, 50, 86, scale=5, title="ALONG THE STORE ROAD", legend="along z at x 56")
b.raster(R, "z", 56, COL, depth=7)
b.callout(-82, 73, "the wall: 3 bedrock, 1 web", dx=10, dy=-20)
b.callout(-104, 78, "the Store at 70, its walls", dx=10, dy=-14)
b.callout(-50, 67, "66 past the Rows, then 67, 68, 69", dx=-20, dy=-24)

pts = [(x + 0.5, z + 0.5) for x, z in paths["band_pillar"]]
import math  # noqa: E402
L = round(sum(math.dist(p, q) for p, q in zip(pts, pts[1:])))
c = SectionPanel(0, L, 40, 90, scale=5, title="BLUE'S ATTACK ON THE PILLAR", legend="unrolled from the band; where nothing is drawn the way is bridged")
c.along(R, pts, COL, depth=7)
c.level(KILL_Y, "kill")
c.callout(L, 75, "the shrine", dx=-30, dy=-16, colour=TEAM["blue"])
c.callout(2, 65, "the band's edge", dx=14, dy=-16, colour=TEAM["blue"])
S.row(a, b)
S.add(c)

# 4. the table
S.table([tuple(row) for row in check["rows"]], width=m.img.width,
        legend="walked octile over the plan (a step up 1.2), build zones bridged block for block")
S.save(sys.argv[1])
