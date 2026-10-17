"""Sixes and Sevens' sketch: the plan drawn and annotated before anything is built, with the checker's numbers on it.

    python3 sketch.py renders/00-plan-sketch.png
"""
import sys

import plan as P
from plan import COLOURS, WALK, WALLS, build, objectives
from plan_check import BLUE, RED, SITES, rows
from pgmvox.plan import graph as G
from pgmvox.read.sketch import TEAM, Sheet

R = build()
E = G.graph(R, WALK, WALLS, rules=G.PlanRules(diagonals=True))
D, prev = G.dijkstra(E, [RED])
to_blue_reactor = G.path(prev, SITES["blue reactor"])
to_blue_pump = G.path(prev, SITES["blue pump"])
sym = R.symmetry.point

S = Sheet("Sixes and Sevens - the plan")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=5, title="THE BOARD",
          legend="bunker 06 (Red) west, 07 (Blue) east, each the half turn of the other; Blue's half paler; "
                 "M monuments, S spawns; red lines Red's walks to Blue's monuments; orange the lava crevasses")
m.raster(R, COLOURS)
m.heights(R, kinds={"shelf", "cut"}, min_cells=40)
m.route(to_blue_reactor, TEAM["red"])
m.route(to_blue_pump, (230, 110, 110))
m.objectives(objectives().markers())

for name, (x, z) in {"tall hall": (-60, 12), "spawn hall": (-94, 34), "dark room": (-100, -6), "yard": (-58, 51),
                     "the Teeth": (-23, -12), "high shelf": (-8, 78), "north spur": (-40, -40),
                     "the cut": (-30, 56), "the Spine": (0, 0), "open snow": (-18, -64)}.items():
    m.place(x, z, name, both=name != "the Spine")
U = R.storey(1)
for box in P.GALLERY + [P.UPPER_CORRIDOR]:
    m.rect(box[0], box[2], box[1] + 1, box[3] + 1, outline=(240, 170, 40), width=2, both=True)
for (x, z), way, n in P.STAIR_FLIGHTS:
    dx = 1 if way == "e" else -1
    m.line([(x, z + 1), (x + dx * 3 * n, z + 1)], colour=(240, 170, 40), width=3, arrow=True, both=True)
m.callout(P.FACADE_X, 8, "06: the facade, 45 wide, door 18 x 16", dx=40, dz=-70)
m.callout(-70, 22, "upper floor at 48 (orange): gallery over the Reactor, corridor over the spawn tunnel", dx=-70, dz=60)
m.callout(-95, 18, "switchback stair, treads 3 deep, two flights of 4", dx=-40, dz=-60)
m.callout(-24, 52, "the cut: a trench six deep, a way to the Pump from below", dx=10, dz=60)
m.callout(-10, 60, "seam: crevasses to lava, irregular, a build zone over them", dx=70, dz=40)
m.callout(-8, 37, "snow bridge", dx=60, dz=-10)
m.callout(-28, -76, "a second crack across the open snow, one snow bridge", dx=-30, dz=-30)
m.callout(0, -2, "the Spine: rock over the seam, the middle crossing", dx=70, dz=-60)
m.callout(-29, 67, "lofted walls: the shelf and each spur", dx=-60, dz=30)
m.callout(20, 68, "wide steps up onto the shelf", dx=40, dz=20)
m.callout(-90, -60, "over the bunker: the snowfield again, the bunker sunk into it; out of play", dx=-20, dz=-40)

S.table(rows() + [("—", "the mountain above each bunker", "a roof to be decided", None),
                  (len(to_blue_reactor), "cells on Red's walk to Blue's Reactor", "", None)], width=m.img.width)
S.save(sys.argv[1])
