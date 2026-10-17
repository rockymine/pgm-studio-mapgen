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

for name, (x, z) in {"tall hall": (-60, 18), "spawn hall": (-94, 34), "dark room": (-100, -6), "yard": (-58, 51),
                     "the Teeth": (-23, -12), "high shelf": (-12, 72), "north spur": (-38, -38),
                     "the cut": (-30, 56), "the Spine": (0, 0)}.items():
    m.place(x, z, name, both=name != "the Spine")
m.callout(P.FACADE_X, 8, "06: the facade, 42 wide, door 18 x 16", dx=40, dz=-70)
m.callout(*P.VENT, "vent: the cliff top drops into the hall over the Reactor", dx=-60, dz=-110)
m.callout(-24, 52, "the cut: a trench six deep, a way to the Pump from below", dx=10, dz=60)
m.callout(-10, 60, "seam: crevasses 14 deep, lava at the foot, a build zone over them", dx=70, dz=40)
m.callout(-8, 37, "snow bridge", dx=60, dz=-10)
m.callout(0, -2, "the Spine: rock over the seam, the middle crossing", dx=70, dz=-60)
m.callout(-36, 61, "lofted wall holds the shelf; another holds each spur", dx=-60, dz=30)
m.callout(18, 65, "ramp up onto the shelf", dx=40, dz=20)
m.callout(-44, -40, "lofted wall, 06", dx=-80, dz=-20)

S.table(rows() + [("—", "the mountain above each bunker", "a roof to be decided", None),
                  (len(to_blue_reactor), "cells on Red's walk to Blue's Reactor", "", None)], width=m.img.width)
S.save(sys.argv[1])
