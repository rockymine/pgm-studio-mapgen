"""Riftwater's sketch: the plan drawn and annotated before anything is built, with the checker's numbers on it.

    python3 sketch.py renders/00-plan-sketch.png
"""
import math
import sys

import numpy as np

import plan as P
import plan_check as C
from pgmvox.sketch import TEAM, SectionPanel, Sheet

m = C.measure()
R = m["R"]
L = P.land()
S = Sheet("Riftwater (pgmvox port) - the plan")

# 1. the board from above
mp = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="THE BOARD",
           legend="kinds lit by height; blue's half paler; numbers: built floors; S spawn, M monuments; "
                  "red line: red's walks to its monuments; dots: the build zone over the rift")
mp.raster(R, P.COLOURS, edges=False)
mp.heights(R, kinds=["square", "green", "inside", "door"], min_cells=4, size=10)
mp.zone(np.abs(np.arange(R.x_min, R.x_max + 1))[:, None].repeat(R.nz, 1) <= P.RIFT, (230, 200, 60), "dots", 6)
for r in L.routes:
    mp.line(r["line"], (90, 70, 50) if r["kind"] != "street" else (70, 70, 80), 1, both=True)
for key, path in m["paths"].items():
    mp.route(path, TEAM["red"], 3, both=True)
for name, (x, z) in P.PLACES:
    mp.place(x, z, name, size=11)
mp.objectives(P.objectives().markers())
g = m["crossings"]
mp.callout(-6, -44, f"Old Bridge stubs: {g['Old Bridge']} of air", dx=40, dz=-40)
mp.callout(-10, 0, f"the falls: {g['the falls']} across", dx=44, dz=26)
mp.callout(-14, 70, f"south fields: {g['the south fields']} across", dx=44, dz=30)
mp.callout(-50, 38, "sinkhole: one-block steps into the cave", dx=-30, dz=40)
mp.callout(-104, 5, "mine adit", dx=-20, dz=30)

# 2. under the ground: storey 1 over the dimmed board, the decks of storey 2
U, D = R.storey(1), R.storey(2)
ug = S.map(-120, -50, 0, 70, scale=5, title="UNDER THE GROUND (red's half)",
           legend="storey 1 over the dimmed board: grey the cave, brown the mine, slate the gaol cellar; "
                  "storey 2: bridge decks; black: the walk from the cave mouth to the sinkhole")
ug.raster(R, P.COLOURS, edges=False)
ug.dim(0.6)
ug.storey(U, P.COLOURS, alpha=0.9, label=False)
ug.storey(D, P.COLOURS, alpha=0.9, label=False)
ug.route([c[:2] for c in m["cave_path"]], (20, 20, 20), 2)
for name, (x, z) in P.UNDERGROUND:
    ug.place(x, z, name, size=11)
for x, y, z in P.MINE[::2]:
    ug.label(x, z - 2, str(y - 1), (250, 220, 160), 10)
for pts in P.CAVE.values():
    for x, y, z, _ in pts[::2]:
        ug.label(x, z - 2, str(y - 1), (230, 230, 240), 10)
ug.callout(*P.GAOL_LADDER, "ladder: gaol floor 52 to the cellar 42", dx=30, dz=-30)
ug.callout(*P.SHAFT, "shaft ladder under the headframe", dx=-40, dz=30)

# 3. sections: across the falls and the cave at z 3; down x -50 through the cellar, the cave and the sinkhole
a = SectionPanel(-120, 0, 25, 85, scale=5, title="ACROSS THE FALLS",
                 legend="along x at z 4, true scale: the ridge, the pond, the river, the cave under the bank")
a.raster(R, "x", 4, P.COLOURS)
a.level(P.RIVER_LEVEL, "the river, 45", (60, 108, 205))
a.callout(-11, 36, "cave mouth and ledge, 36", dx=-60, dy=30)
a.callout(-98, 60, "spawn terrace 59", dx=20, dy=-20)
b = SectionPanel(-40, 50, 25, 70, scale=5, title="DOWN X -50",
                 legend="along z at x -50: the gaol cellar, the cave under the river, the sinkhole")
b.raster(R, "z", -50, P.COLOURS)
b.callout(-34, 42, "cellar 42", dx=20, dy=-20)
b.callout(38, 38, "sinkhole floor 38", dx=20, dy=-30)
S.row(a, b)
path = m["paths"]["square"]
length = round(sum(math.dist(p, q) for p, q in zip(path, path[1:])))
c = SectionPanel(0, length, 40, 70, scale=5, title="RED'S WALK TO THE SQUARE",
                 legend="unrolled along the route, spawn at left")
c.along(R, [(x + 0.5, z + 0.5) for x, z in path], P.COLOURS)
c.callout(1, 60, "spawn hall, 59", dx=20, dy=-12, colour=TEAM["red"])
c.callout(length, 53, "the square, 52", dx=-20, dy=-12)
path2 = m["paths"]["green"]
length2 = round(sum(math.dist(p, q) for p, q in zip(path2, path2[1:])))
d = SectionPanel(0, length2, 40, 70, scale=5, title="RED'S WALK TO THE GREEN",
                 legend="unrolled along the route, spawn at left")
d.along(R, [(x + 0.5, z + 0.5) for x, z in path2], P.COLOURS)
d.callout(length2, 51, "the green, 50", dx=-20, dy=-12)
S.row(c, d)

S.table(C.rows(m), width=mp.img.width)
S.save(sys.argv[1])
