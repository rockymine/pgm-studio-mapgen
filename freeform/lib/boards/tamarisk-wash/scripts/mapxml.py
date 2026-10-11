"""Write Tamarisk Wash's map.xml: the teams of sixteen, the spawns and the four monuments from the plan's objectives;
the kit; the fall past the board's rim; building anywhere but over the void, no higher than the build height.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map

M = Map("Tamarisk Wash", "0.1.0", "Destroy both of the enemy's monuments: the Obelisk on Table Rock and the "
        "Sunstone in the Souk.", "dtm",
        authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
            Item("wood", 4, 64, 4), Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6, 4),
            Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("iron chestplate", unbreakable=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.MAX_BUILD),
        kill=KillHeight(P.KILL_Y))
print(M.xml())
