"""Write Riftwater's map.xml: teams of sixteen, the spawns, the four monuments and the observer point from the
plan's objectives; the original board's kit; the rift as the only place to build over the void; a build limit.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.rules import Build, Item, Kit, Map

M = Map("Riftwater", "0.2.0", "Destroy both of the enemy's monuments: one in their market square, one on their "
        "village green.", "dtm",
        authors=["Claude (freeform generator, ported onto pgmvox)"],
        contributors=[("rockymine", "Built the oak and birch trees (tree showcase)")],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64),
            Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6, 1), Item("water bucket", 7),
            Item("cooked beef", 8, 16), Item("arrow", 28),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("iron chestplate", unbreakable=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(areas=[(-P.RIFT, P.Z_MIN, P.RIFT - 1, P.Z_MAX)], max_height=90,
                        message="You may only bridge over the rift!"))
print(M.xml())
