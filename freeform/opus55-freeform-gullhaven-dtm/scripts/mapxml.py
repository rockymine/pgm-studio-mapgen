"""Write Gullhaven DTM's map.xml: two teams of sixteen, each with two gold monuments (one floating over the harbour,
one over the beach), a spawn square in each town's upper street kept to its team, building up to y 56 and nowhere
past the board's edge, the clock held.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

from pgmvox import B  # noqa: E402
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Bounds, Build, Effect, Item, Kit, Map, Match, Respawn  # noqa: E402

GOLD = dict(material=(B.GOLD_BLOCK, 0), materials="gold block")
O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)))
O.add(Observer((-19, 60, 57), yaw=0))
O.add(Spawn("red-team", (16, 37, -39), yaw=0, kit="spawn-kit", area=Box(10, 0, -40, 22, 255, -36)), mirror=False)
O.add(Spawn("blue-team", (-54, 37, 154), yaw=180, kit="spawn-kit", area=Box(-60, 0, 151, -48, 255, 155)),
      mirror=False)
for team, key, name, box in (("red-team", "red-harbour", "Red's Harbour Monument", Box(30, 22, 24, 32, 24, 26)),
                             ("red-team", "red-beach", "Red's Beach Monument", Box(-52, 25, 7, -50, 27, 9)),
                             ("blue-team", "blue-harbour", "Blue's Harbour Monument", Box(-70, 22, 89, -68, 24, 91)),
                             ("blue-team", "blue-beach", "Blue's Beach Monument", Box(12, 25, 106, 14, 27, 108))):
    O.add(Destroyable(key, name, team, box, **GOLD), mirror=False)
O.add(Bounds(Box(-96, 0, -56, 58, 255, 171), "The sea is too rough past here.", build=False))

M = Map("Gullhaven DTM", "0.1.0", "Destroy both of the other team's gold monuments: one floating over the harbour, "
        "one over the beach.", "dtm", authors=["Claude (freeform generator)"], includes=[],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
                Item("iron pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("wood", 4, 64), Item("golden apple", 5, 2), Item("cooked beef", 6, 16),
                Item("water bucket", 7), Item("arrow", 28, 32),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots"),
                clear=True, effects=[Effect("damage resistance", "5s", amplifier=5)],
                reward=[Item("arrow", amount=6), Item("golden apple")]),
        build=Build(max_height=56, void=False),
        match=Match(respawn=Respawn("5s"), time_of_day=5000))
print(M.xml())
