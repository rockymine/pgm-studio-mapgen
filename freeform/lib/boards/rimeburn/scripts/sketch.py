"""Rimeburn's sketch: the plan drawn and annotated before anything is built, with the checker's numbers on it.

    python3 sketch.py renders/00-plan-sketch.png
"""
import json
import math
import os
import sys

import land as LD
import plan as P
from pgmvox.plan import graph as G
from pgmvox.play.objectives import Core, Destroyable, Spawn
from pgmvox.read import sketch as SK
from pgmvox.read.sketch import SectionPanel, Sheet

SK.TEAM["ember"] = (215, 110, 25)
SK.TEAM["frost"] = (40, 150, 200)
R = P.build()
E = G.graph(R, P.WALK, wall_kinds={"wall"}, rules=G.PlanRules(diagonals=True), bridge=R.mask("seam"),
            extra=P.vent_extra(R))
O = P.objectives()
spawns = {s.team: [(s.at[0], s.at[2])] for s in O.of(Spawn)}
goals = [g for g in O.items if isinstance(g, (Core, Destroyable))]

S = Sheet("Rimeburn - the plan: one land, two seasons")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=6, title="THE BOARD",
          legend="number: floor height; C a Hearth (core), M an Icestone (monument), S a spawn; Ember's half paler; "
                 "blue: water (ice in Frost's half); dark: the seam, all of it a build zone; brown: walls and houses",
          symmetry=R.symmetry)
m.raster(R, P.COLOURS, image_half=lambda x, z: z >= 0)
m.heights(R, kinds=["ground", "stair"], min_cells=40)
for name, (x, z) in P.PLACES.items():
    m.place(x, z, name)
m.objectives(O.markers())
m.callout(LD.VENT[0][0], LD.VENT[0][2], "the Vent's mouth in the cliff, floor 32", dx=40, dz=40)
m.callout(*LD.FALLS, "the Rime Falls", dx=-60, dz=-10)

r = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=6, title="THE ROUTES",
          legend="Frost's walks (blue) to its own goals and to Ember's, Ember's (orange) the same; the seam is bridged")
r.raster(R, P.COLOURS, image_half=lambda x, z: z >= 0)
r.dim(0.5)
for team, colour in (("frost-team", SK.TEAM["frost"]), ("ember-team", SK.TEAM["ember"])):
    D, prev = G.dijkstra(E, spawns[team])
    for g in goals:
        c, by, p = G.measure(D, prev, E, P.goal_cells(g.box))
        if p:
            r.route(p, colour, width=2 if g.team == team else 3)
r.objectives(O.markers())

along = SectionPanel(R.z_min, R.z_max, 0, 80, scale=3, title="ALONG THE BOARD",
                     legend=f"along z at x {LD.HEARTH[0]}, true scale: Frost's Hearth Hollow, the seam, Ember's land")
along.raster(R, "z", LD.HEARTH[0], P.COLOURS)
along.level(P.KILL_Y, f"kill below y {P.KILL_Y}")
along.callout(LD.HEARTH[1], LD.HOLLOW_FLOOR + 1, "Hearth Hollow, floor 34", dx=20, dy=-20)
across = SectionPanel(R.x_min, R.x_max, 0, 80, scale=3, title="ACROSS FROST'S HALF",
                      legend=f"along x at z {LD.SHELF[1]}: the hollow, the burn, the Rime Shelf at 45")
across.raster(R, "x", LD.SHELF[1], P.COLOURS)
across.level(P.KILL_Y, "kill")
across.callout(LD.SHELF[0], LD.SHELF_TOP + 1, "the Rime Shelf", dx=-30, dy=-16)
S.row(along, across)

path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "plan-check.json")
rows = []
if os.path.isfile(path):
    rows = [(v, w, t, o) for v, w, t, o in json.load(open(path))]
S.table(rows, width=m.img.width)
S.save(sys.argv[1])
