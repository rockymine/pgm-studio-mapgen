"""Write Stratum's map.xml: two teams of sixteen, each with a core hung in its Reactor and a monument on its Obelisk's
balcony, the spawns kept to their team, a fall below y 58 fatal, building up to y 122. Red's half is stated and
blue's mirrored across the middle.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

from pgmvox.plan.raster import Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Core, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, terrain_of  # noqa: E402

O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), Symmetry("mirror_x"))
O.add(Observer((0, 100, 0), yaw=90))
O.add(Spawn("red-team", (-80, 81, 0), yaw=270, kit="spawn-kit", area=Box(-93, 0, -13, -67, 255, 13)))
O.add(Core("red-core", "the Reactor", "red-team", Box(-57, 81, 47, -55, 83, 49), leak=10))
O.add(Destroyable("red-obelisk", "the Obelisk", "red-team", Box(-55, 100, -50, -55, 101, -50)))

M = Map("Stratum", "0.1.0", "Leak the core hung in the enemy's Reactor, and break the monument on their Obelisk's "
        "balcony.", ["dtm", "dtc"],
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "Built the oak and birch trees (tree showcase)")],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("wood", 4, 64), Item("wool", 5, 64, team_color=True), Item("golden apple", 6),
                Item("shears", 7, unbreakable=True), Item("cooked beef", 8, 16), Item("wood", 27, 64),
                Item("arrow", 28),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=122, void=False), kill=KillHeight(58))
print(M.xml())
