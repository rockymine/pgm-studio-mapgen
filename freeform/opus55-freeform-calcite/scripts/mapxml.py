"""Write Calcite's map.xml from the plan's hills, pads, spawners and spawn: King of the Hill for two teams of sixteen,
the Middle paying double, the jump pads sparing their riders the fall, every part drawn for red and turned half way
round for blue; no building and no using a block.

    python3 mapxml.py > map.xml
"""
import math
import os
import sys
from dataclasses import replace

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

import plan as P  # noqa: E402
from pgmvox.plan.raster import Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Hill, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Effect, Item, JumpPad, Kit, Map, Match, Respawn, Spawner  # noqa: E402

block = lambda p: (math.floor(p[0]), int(p[1]), math.floor(p[2]))       # noqa: E731
S = Symmetry("half")

O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), S)
O.add(Observer((0, 32, 0), yaw=90))
O.add(Spawn("red-team", block(P.SPAWN_POINT), yaw=-90, kit="spawn-kit", area=Box(-49, 0, -6, -42, 255, 5)))
for h in P.HILLS:
    x0, x1, z0, z1 = h["box"]
    O.add(Hill(h["key"], h["name"], Box(x0, h["y"], z0, x1, h["y"], z1), points=h["points"]), mirror=False)
for p in P.PADS:                                       # each pad and its turn
    x0, x1, z0, z1, y = p["cells"]
    pad = JumpPad(f"pad-{p['key']}", Box(x0, y + 1, z0, x1, y + 2, z1), p["v"], safe=True)
    O.add(pad, mirror=False)
    O.add(replace(pad.turned(S), id=f"{pad.id}-turn"), mirror=False)
x, y, z = block(P.GAPPLE_AT)                           # the golden apples in the Spring under the Middle
O.add(Spawner("apples", (x, y, z), [("golden apple", 1)], reach=None, box=Box(x, y, z, x + 1, y, z + 1)),
      mirror=False)
for k, at in enumerate(P.ARROWS_AT):                   # arrows in two diagonal corners of the Ledge
    a = block(at)
    O.add(Spawner(f"arrows-{k}", a, [("arrow", 4)], delay="10s", max_entities=8, reach=None, box=Box(*a, *a)),
          mirror=False)

M = Map("Calcite", "0.1.0", "Hold the hills: the Middle pays double. First to 600 points.", "koth",
        authors=["Claude (freeform generator)"], includes=[],
        objectives=O,
        kit=Kit(Item("stone sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True), Item("golden apple", 2),
                Item("arrow", 8, 16),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("iron boots", unbreakable=True, wear="boots"),
                clear=True, effects=[Effect("resistance", "3s", 5)], reward=[Item("arrow", amount=6)]),
        build=Build(never=True, use=False),
        match=Match(score=600, time=15 * 60, respawn=Respawn("3s", auto=True)))
print(M.xml())
