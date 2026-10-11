"""Write Lantern Karst's map.xml. The placements are the pgmvox port's (lib/ports/lantern-karst), which lays this
board's spawns, wools, monuments, rooms and the spawns' iron where this board has them: two teams of sixteen, two
wools each, a fall below y 40 fatal, building only over a marked column up to y 92.

    python3 mapxml.py > map.xml
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "lib", "ports", "lantern-karst", "scripts"))

import plan as P  # noqa: E402  (the port's plan, which puts the library on the path)
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map  # noqa: E402

M = Map("Lantern Karst", "0.1.0", "Capture the enemy's two wools: the Pillar Shrine's and the Tea Store's.", "ctw",
        authors=["Claude (freeform generator)"],
        objectives=P.objectives(),
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                Item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
                Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), Item("wood", 4, 64, damage=1),
                Item("stained clay", 5, 48, team_color=True), Item("golden apple", 6), Item("water bucket", 7),
                Item("cooked beef", 8, 16), Item("arrow", 28), Item("shears", 29, unbreakable=True),
                Item("wood", 31, 64, damage=1),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.MAX_BUILD), kill=KillHeight(P.KILL_Y))
print(M.xml())
