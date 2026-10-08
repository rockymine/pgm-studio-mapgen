"""Islets' sketch: the plan drawn and annotated before anything is built, with the checker's numbers on it.

    python3 sketch.py renders/00-plan-sketch.png
"""
import math
import sys

from plan import COLOURS, GROUND, HILL, KILL_Y, WALK, build
from pgmvox import plangraph as G
from pgmvox.sketch import TEAM, SectionPanel, Sheet

R = build()
E = G.graph(R, WALK)
J = G.jumps(R, WALK)
SPAWNS = {"red": [(-24, 0)], "blue": [(23, -1)]}
HILL_CELLS = [(x, z) for x in range(-2, 2) for z in range(-4, 4)]
a = G.arrivals(E, SPAWNS, {"the hill": HILL_CELLS})["the hill"]
D, prev = G.dijkstra(E, SPAWNS["red"])
red = G.path(prev, min((c for c in HILL_CELLS if c in D), key=D.get))
widest = max((g for *_, g in J), default=0)

S = Sheet("Islets - the plan")

m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=12, title="THE BOARD",
          legend="number on each piece: its floor height; A the hill; S spawns; blue's half drawn paler")
m.raster(R, COLOURS)
m.heights(R)
m.place(-20, -7, "Red's island")
m.place(*R.symmetry.point(-20, -7), "Blue's island")
m.jumps(J, R=R)
m.route(red, TEAM["red"], both=True)
m.marker(-24, 0, "S", TEAM["red"], both=True)
m.marker(-1, 2, "A", TEAM["neutral"])
m.callout(-7, -6, "stepping stone, a jump off the causeway", dx=-40, dz=-34)
m.callout(-3, -1, f"two steps, {GROUND} to {HILL}", dx=-10, dz=60)
m.callout(-24, 12, f"void: kill below y {KILL_Y}", dx=30, dz=20)

along_x = SectionPanel(R.x_min, R.x_max, KILL_Y - 2, 38, scale=8, title="ACROSS",
                       legend="along x at z 0, true scale")
along_x.raster(R, "x", 0, COLOURS)
along_x.level(KILL_Y, f"kill below y {KILL_Y}")
along_x.callout(-1, HILL + 1, f"the hill, floor {HILL}", dx=20, dy=-14)
along_x.callout(-20, GROUND + 1, f"islands, floor {GROUND}", dx=16, dy=-16)

route_len = round(sum(math.dist(p, q) for p, q in zip(red, red[1:])))
along_r = SectionPanel(0, route_len, KILL_Y - 2, 38, scale=8, title="RED'S WALK",
                       legend="unrolled along the route, spawn at left")
along_r.along(R, [(x + 0.5, z + 0.5) for x, z in red], COLOURS)
along_r.level(KILL_Y, "kill")
along_r.callout(1, GROUND + 1, "spawn", dx=12, dy=-14, colour=TEAM["red"])
along_r.callout(route_len, HILL + 1, "the hill", dx=-12, dy=-14)
S.row(along_x, along_r)

S.table([
    (f"{a['red']:.1f}", "red's walk to the hill", "equal to blue's", abs(a["red"] - a["blue"]) < 0.01),
    (f"{a['blue']:.1f}", "blue's walk to the hill", "at most 30", a["blue"] <= 30),
    (len(J), "jumps the plan allows", "", None),
    (widest, "the widest jump", "at most 3", widest <= 3),
], width=m.img.width)
S.save(sys.argv[1])
