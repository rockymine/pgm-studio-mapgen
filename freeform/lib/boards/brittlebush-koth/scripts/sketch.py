"""Brittlebush KotH's sketch: the blueprint drawn before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
"""
import json
import os
import sys

import plan as P
from pgmvox.sketch import TEAM, MapPanel, SectionPanel, Sheet

HERE = os.path.dirname(os.path.abspath(__file__))
R = P.plan()
C = R.cells
with open(os.path.join(HERE, "..", "renders", "plan-check.json")) as f:
    check = json.load(f)
paths = {k: [tuple(c) for c in v] for k, v in check["paths"].items()}
TEAM_COLOUR = [TEAM["red"], TEAM["blue"], TEAM["green"], TEAM["yellow"]]
ARROW = {"<": "w", ">": "e", "^": "n", "v": "s"}
for (cx, cz), (k, lv, d, team) in C.items():                   # the stairs' ticks, one a cell, toward the top
    if k == "stair":
        R.stair[(cx * P.CELL + 2, cz * P.CELL + 2)] = ARROW[d]


def centre(cx, cz):
    return cx * P.CELL + 2, cz * P.CELL + 2


def quad(a, b):
    """A cell of red's quadrant (a, b) as block coordinates of its middle."""
    return centre(a - P.N, b - P.N)


def cell_marks(m, only_red=False):
    """On every cell: its level, the keeps in their team's colours, the water's waves."""
    for (cx, cz), (k, lv, d, team) in C.items():
        if only_red and not (cx < 0 and cz < 0):
            continue
        x, z = centre(cx, cz)
        if k in ("flat", "stacked", "keep", "tower"):
            m.label(x, z, f"{P.LEVEL[lv]}" + ("/" + str(P.LEVEL[lv - 1]) if k == "stacked" else ""),
                    size=9 if k == "stacked" else 10)
        elif k == "water":
            m.label(x, z, "~", colour=(230, 240, 255), size=12)
    for i, (team, name, colour) in enumerate(P.TEAMS):
        x0, z0, x1, z1 = P.keep_box(i)
        m.rect(x0, z0, x1, z1, outline=TEAM_COLOUR[i], width=3)
        sx, sz = P.spawn_cell(i)
        m.marker(sx, sz, "S", TEAM_COLOUR[i])
    for hid, name, (x0, z0, x1, z1), points, hy in P.HILLS:
        m.rect(x0, z0, x1, z1, outline=(250, 250, 250), width=3)
        m.marker((x0 + x1) / 2, (z0 + z1) / 2, "H", TEAM["neutral"])
    for x, z in P.APPLES:
        m.marker(x, z, "G", (230, 190, 40))
    for x, z in P.ARROWS:
        m.marker(x, z, "A", (150, 150, 160))


S = Sheet("Brittlebush KotH - king of the hill for four teams, five hills, a blueprint of five-block cells, for review")

# 1. the board
m = MapPanel(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=4, title="THE BOARD",
          legend="every cell 5 by 5; the number: its floor (y); sand yellow, "
                 "inlay green, decks brown, stairs grey with a tick toward the top; dotted: gaps to build over; "
                 "framed: a team's keep (S) and its house; white squares: the five hills (H); G golden apples, "
                 "A arrows")
m.raster(R, P.COLOURS)
m.zone(R.mask("gap"), colour=(200, 190, 170), step=3)
cell_marks(m)
m.label(-33, -67, "RED", TEAM["red"], 14)
m.label(32, -67, "BLUE", TEAM["blue"], 14)
m.label(32, 66, "GREEN", TEAM["green"], 14)
m.label(-33, 66, "YELLOW", TEAM["yellow"], 14)

# 2. red's quadrant, named
q = MapPanel(P.X_MIN, P.Z_MIN, -1, -1, scale=9, title="RED'S QUADRANT, THE BLUEPRINT",
          legend="each other quadrant is this one turned a quarter; it is its own mirror across its diagonal")
q.raster(R, P.COLOURS)
q.zone(R.mask("gap"), colour=(200, 190, 170), step=3)
cell_marks(q, only_red=True)
for name, (a, b), dx, dz in [(f"the Keep and its house: spawn, 3x3 at {P.LEVEL[5]}", (1, 2), 0, 22),
                             (f"the Orchard, {P.LEVEL[4]}", (5, 0), 0, -4), (f"the terrace, {P.LEVEL[3]}", (9, 0), 0, -4),
                             (f"the North Island hill, at {P.LEVEL[2]}, shared with blue", (12, 1), -30, 30),
                             (f"the yard, {P.LEVEL[3]}", (4.5, 4.5), 0, -22), ("the pond", (6.5, 6.5), -14, 20),
                             (f"the arbour, {P.LEVEL[2]}", (9, 4), -20, -20),
                             (f"an inner island at {P.LEVEL[2]}: golden apples", (12, 6), -24, 26),
                             (f"the inner court, {P.LEVEL[1]}", (9, 8.5), -30, -4),
                             (f"a landing at {P.LEVEL[0]}, shared with blue: arrows", (12, 9.5), -36, -16),
                             (f"the Dais, the middle hill, 10x10 at {P.LEVEL[1]}", (12, 12), -40, -6),
                             ("gaps: built over", (11, 5), -16, 30)]:
    x, z = quad(a, b)
    q.callout(x, z, name, dx=dx, dz=dz, size=11)

# 3. routes
r = MapPanel(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=4, title="RED'S ROUTES",
          legend="from red's spawn, on foot: the two border hills beside it (red), the middle hill (white), the two "
                 "beyond it (pale); to the golden apples, bridged (gold)")
r.raster(R, P.COLOURS)
r.dim(0.55)
r.zone(R.mask("gap"), colour=(150, 140, 120), step=3)
r.route(paths["near0"], TEAM["red"], width=3)
r.route(paths["near1"], TEAM["red"], width=3)
r.route(paths["centre"], (240, 240, 240), width=3)
r.route(paths["far0"], (230, 170, 170), width=2)
r.route(paths["far1"], (230, 170, 170), width=2)
r.route(paths["apples"], (230, 190, 40), width=2)
for hid, name, (x0, z0, x1, z1), points, hy in P.HILLS:
    r.rect(x0, z0, x1, z1, outline=(250, 250, 250), width=3)
S.row(m, r)
S.add(q)

# 4. a section along red's diagonal, from the keep's corner to the middle
COL = dict(P.COLOURS)
pts = [(P.X_MIN, P.Z_MIN), (0, 0)]
c = SectionPanel(0, 92, 0, 32, scale=7, title="ALONG RED'S DIAGONAL",
                 legend=f"the keep {P.LEVEL[5]}, the orchard {P.LEVEL[4]}, the yard {P.LEVEL[3]}, the pond, the inner court "
                        f"{P.LEVEL[1]}, the Dais {P.LEVEL[1]}; the levels 3 apart; under a floor, stone and bedrock")
c.along(R, pts, COL, depth=8)
c.level(P.MAX_BUILD, f"build to y {P.MAX_BUILD}")
S.add(c)

S.table([tuple(row) for row in check["rows"]], width=1040,
        legend="walked octile over the plan (a step up 1.2); 'on foot' crosses no gap, the apples are bridged to")
S.save(sys.argv[1])
