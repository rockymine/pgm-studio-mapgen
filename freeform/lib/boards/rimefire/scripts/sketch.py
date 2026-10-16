"""Rimefire's sketch: the plan drawn and annotated before a block is built, with the checker's numbers on it.

    python3 sketch.py renders/00-plan-sketch.png
"""
import math
import sys

import land as LND
import plan as PLAN
import planraster as PR
from pgmvox.plan import graph as G
from pgmvox.read.sketch import TEAM, SectionPanel, Sheet

R, g = PR.build()
E = PR.graph(R)
fx, fz = LND.FURNACE
spawn = {"fire": (PLAN.SPAWN_AT[0], PLAN.SPAWN_AT[2]), "ice": (-1 - PLAN.SPAWN_AT[0], -1 - PLAN.SPAWN_AT[2])}
gate = {"fire": (fx - 10, fz), "ice": (-1 - (fx - 10), -1 - fz)}
D, prev = G.dijkstra(E, [spawn["fire"]])
target = min(((gate["ice"][0] + dx, gate["ice"][1] + dz) for dx in range(-3, 4) for dz in range(-3, 4)
              if (gate["ice"][0] + dx, gate["ice"][1] + dz) in D), key=lambda c: D[c])
route = G.path(prev, target)
own = min(D[(gate["fire"][0] + dx, gate["fire"][1] + dz)] for dx in range(-3, 4) for dz in range(-3, 4)
          if (gate["fire"][0] + dx, gate["fire"][1] + dz) in D)
enemy = D[target]

S = Sheet("Rimefire - the plan")
m = S.map(R.x_min + 8, R.z_min + 8, R.x_max - 8, R.z_max - 8, scale=5, title="THE BOARD",
          legend="shading: height; orange: the lava channel, pale blue: the frozen stream; brown: bridge decks; "
                 "the south half is the north half turned half round")
m.raster(R, PR.COLOURS, edges=False, image_half=lambda x, z: z >= 0)
for name, (x, z) in dict(spawn=LND.SPAWN, furnace=LND.FURNACE, hollow=(-38, -44), overlook=LND.OVERLOOK).items():
    label = {"spawn": "Ashfall Lodge", "furnace": "The Furnace", "hollow": "Rustwater", "overlook": "The Overlook"}[name]
    m.place(x, z, label, size=12, both=True)
m.place(-0.5, -0.5, "THE SEAM", size=14)
m.place(-40, -8, "west span", size=11, both=True)
m.place(-0.5, -8, "keystone", size=11)
m.objectives(PLAN.objectives().markers())
m.route(route, TEAM["red"], both=False)
m.callout(*LND.OVERLOOK, "hill 77, tower on it", dx=50, dz=-20)
m.callout(fx, fz, "core hung over a pit, ring wall, three gates", dx=60, dz=-10)
m.callout(-38, -44, "pond, four houses, a well", dx=-40, dz=-30)

route_len = round(sum(math.dist(p, q) for p, q in zip(route, route[1:])))
along = SectionPanel(0, route_len, 30, 100, scale=3, title="THE FIRE TEAM'S WALK TO THE ICE CORE",
                     legend="unrolled along the shortest route, spawn at the left, true scale")
along.along(R, [(x + 0.5, z + 0.5) for x, z in route], PR.COLOURS)
along.level(LND.KILL_Y, "kill")
S.row(along)

S.table([
    (f"{own:.0f}", "walk from a spawn to its own core's gate", "40 to 90", 40 <= own <= 90),
    (f"{enemy:.0f}", "walk from a spawn to the enemy core's gate", "85 to 150, the ratio 3 to 4",
     85 <= enemy <= 170 and 3 <= enemy / own <= 4),
    (len(LND.BRIDGES), "crossings of the seam, besides the ravine's floor", "3", True),
    ("130 x 198", "footprint", "at most 150 x 200", True),
], width=m.img.width)
S.save(sys.argv[1])
