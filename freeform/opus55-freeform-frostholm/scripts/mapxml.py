"""Write Frostholm's map.xml: two teams of sixteen, each with a core by its lighthouse and a monument on its lake
knoll, the spawns kept to their team, building up to y 96. Red's half is stated and blue's turned half way round.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

from pgmvox.plan.raster import Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Core, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Build, Item, Kit, Map  # noqa: E402

O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), Symmetry("half"))
O.add(Observer((0, 80, 0), yaw=90))
O.add(Spawn("red-team", (-60, 57, -64), yaw=270, kit="spawn-kit", area=Box(-76, 0, -69, -52, 255, -59)))
O.add(Core("red-core", "The Beacon", "red-team", Box(-29, 59, -59, -27, 61, -57)))
O.add(Destroyable("red-holmstein", "Holmstein", "red-team", Box(-58, 63, -20, -58, 64, -20)))

M = Map("Frostholm", "0.1.0", "Leak the core standing by the enemy's lighthouse, and break the monument on their lake "
        "knoll.", ["dtm", "dtc"],
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "Built the pine and spruce trees (tree showcase)")],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("wood", 4, 64), Item("wool", 5, 32, team_color=True), Item("golden apple", 6),
                Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=96, void=False))
print(M.xml())
