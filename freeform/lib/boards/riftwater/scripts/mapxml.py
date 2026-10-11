"""Write Riftwater's map.xml. The placements are the pgmvox port's (lib/boards/riftwater-pgmvox), which lays this board's
monuments, spawns and rift where this board has them: two teams of sixteen, two monuments each, the rift the only
place to bridge over the void, building up to y 90.

    python3 mapxml.py > map.xml
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "riftwater-pgmvox", "scripts"))

import plan as P  # noqa: E402  (the port's plan, which puts the library on the path)
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of  # noqa: E402

M = Map("Riftwater", "0.1.0", "Destroy both of the enemy's monuments: one in their market square, one on their "
        "village green.", "dtm",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "Built the oak and birch trees (tree showcase)")],
        objectives=P.objectives(),
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("wood", 4, 64), Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6),
                Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(areas=[(-P.RIFT, P.Z_MIN, P.RIFT - 1, P.Z_MAX)], max_height=90,
                    message="You may only bridge over the rift!"))
print(M.xml())
