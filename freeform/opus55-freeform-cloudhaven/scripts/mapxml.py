"""Write Cloudhaven's map.xml: two teams of sixteen, each with two monuments (one under the gazebo on Lantern Isle,
one in the sunken garden of the Hanging Gardens), the spawns kept to their team, building up to y 116. Red's half is
stated and blue's turned half way round.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

from pgmvox.plan.raster import Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of  # noqa: E402

O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), Symmetry("half"))
O.add(Observer((0, 100, 0), yaw=90))
O.add(Spawn("red-team", (-110, 94, 0), yaw=270, kit="spawn-kit", area=Box(-117, 0, -7, -103, 255, 7)))
O.add(Destroyable("red-lantern", "Lantern Isle", "red-team", Box(-72, 83, -60, -72, 84, -60)))
O.add(Destroyable("red-gardens", "Hanging Gardens", "red-team", Box(-71, 63, 59, -71, 64, 59)))

M = Map("Cloudhaven", "0.1.0", "Break both of the enemy's monuments: one under the gazebo on Lantern Isle, one in the "
        "sunken garden of the Hanging Gardens.", "dtm",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "Built the willow and dense oak trees (tree showcase)")],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("wood", 4, 64), Item("wool", 5, 64, team_color=True), Item("wood", 27, 64),
                Item("golden apple", 6), Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=116, void=False))
print(M.xml())
