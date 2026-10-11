"""Write Hollow Mesa's map.xml: two teams of sixteen, each with a core floating over a well through their mesa by the
headframe over the Throat, the spawns kept to their team, no building over the void, building up to y 100. Red's half
is stated and blue's turned half way round.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

from pgmvox.plan.raster import Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Core, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of  # noqa: E402

O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), Symmetry("half"))
O.add(Observer((0, 95, 0), yaw=90))
O.add(Spawn("red-team", (-102, 76, 6), yaw=270, kit="spawn-kit", area=Box(-113, 0, -8, -97, 255, 16)))
O.add(Core("red-core", "The Throat", "red-team", Box(-67, 79, -26, -64, 82, -23)))

M = Map("Hollow Mesa", "0.2.0", "Leak the enemy's core: it floats over a well through their mesa, by the headframe "
        "over the Throat.", "dtc",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "Built the acacia and olive trees (tree showcase)")],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("wood", 4, 64), Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6),
                Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=100, message="You may not build over the void, nor plug the Throat!"))
print(M.xml())
