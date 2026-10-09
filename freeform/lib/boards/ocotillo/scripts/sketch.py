"""Ocotillo's sketch: the blueprint drawn before anything is built, with the checker's table on it.

    python3 sketch.py renders/00-plan-sketch.png       (after plan_check.py, whose routes and table it draws)
"""
import json
import os
import sys

import plan as P
from pgmvox import blocks as K
from pgmvox.objectives import DYES
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


def wool_colour(name):
    return tuple(int(v) for v in K.COLOURS[K.B.WOOL, DYES[name]])


def cell_marks(m, only_red=False):
    """On every cell: its level, the keeps and towers in their team's colours, the water's waves."""
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
        x0, z0, x1, z1 = P.tower_box(i)
        m.rect(x0 + 1, z0 + 1, x1 - 1, z1 - 1, fill=wool_colour(P.WOOLS[team]), outline=TEAM_COLOUR[i], width=3)
        sx, sz = P.spawn_cell(i)
        m.marker(sx, sz, "S", TEAM_COLOUR[i])


S = Sheet("Ocotillo - four teams, one wool each, a blueprint of five-block cells, for review")

# 1. the board
m = MapPanel(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=4, title="THE BOARD",
          legend="every cell 5 by 5; the number: its floor (y), deck/underfloor on a stacked cell; sand yellow, "
                 "inlay green, decks brown, stairs grey with a tick toward the top; dotted: gaps to build over; "
                 "framed: a team's keep (S) and, in its wool's colour, its tower")
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
for name, (a, b), dx, dz in [("the Keep: spawn, 3x3 at 19", (1, 2), 0, 22), ("the Orchard, 16", (5, 0), 0, -4),
                             ("the terrace, 13", (9, 0), 0, -4), ("an island at 10, shared with blue", (12, 1), -30, 30),
                             ("the yard, 13", (4.5, 4.5), 0, -22), ("the Tower: the wool", (6.5, 6.5), -14, 20),
                             ("the Arbour: deck 13 over a covered walk at 10", (9, 4), -34, -20),
                             ("an island at 10 by the covered walk", (12, 6), -24, 26),
                             ("the inner court, 10", (9, 8.5), -30, -4),
                             ("a landing at 7, shared with blue", (12, 9.5), -36, -16),
                             ("the dais, 10x10 at 10, a quarter of it", (12, 12), -40, -6),
                             ("gaps: built over", (11, 2), -20, 22)]:
    x, z = quad(a, b)
    q.callout(x, z, name, dx=dx, dz=dz, size=11)

# 3. routes
r = MapPanel(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=4, title="RED'S ROUTES",
          legend="from red's spawn: its own wool (red), blue's and yellow's across a border gap, built (blue, "
                 "yellow), green's through the middle (green); grey: to the dais")
r.raster(R, P.COLOURS)
r.dim(0.55)
r.zone(R.mask("gap"), colour=(150, 140, 120), step=3)
r.route(paths["wool0"], TEAM["red"], width=3)
r.route(paths["wool1"], TEAM["blue"], width=3)
r.route(paths["wool2"], TEAM["green"], width=3)
r.route(paths["wool3"], TEAM["yellow"], width=3)
r.route(paths["dais"], (200, 200, 200), width=2)
S.row(m, r)
S.add(q)

# 4. a section along red's diagonal, from the keep's corner to the middle
COL = dict(P.COLOURS)
pts = [(P.X_MIN, P.Z_MIN), (0, 0)]
c = SectionPanel(0, 92, 0, 32, scale=7, title="ALONG RED'S DIAGONAL",
                 legend="the keep 19, the yard 13, the tower 13, the inner court 10, the dais 10; the levels 3 apart; "
                        "nothing under a floor but bedrock")
c.along(R, pts, COL, depth=8)
c.level(P.MAX_BUILD, f"build to y {P.MAX_BUILD}")
S.add(c)

S.table([tuple(row) for row in check["rows"]], width=1040,
        legend="walked octile over the plan (a step up 1.2), gaps built over block for block")
S.save(sys.argv[1])
