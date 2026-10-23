"""Write Chantry Gill's map.xml: the teams, spawns, observer and the four monuments come from objectives.py; the kit
(a diamond pickaxe, which breaks obsidian), building over the void only in the build zone between the two coasts (zone.py), and
the build height are stated here.

    python3 mapxml.py > map.xml
"""
import objectives as P
import zone as ZN
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of

M = Map("Chantry Gill", "1.0.0", "Destroy the enemy's two monuments: the one in the town's square and the one on the Scar.",
        "dtm", terrain=terrain_of(__file__),
        authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("diamond pickaxe", 2, enchant=[("efficiency", 2)], unbreakable=True),
            Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), Item("wood", 4, 64, 1),
            Item("stained clay", 5, 64, team_color=True), Item("golden apple", 6), Item("water bucket", 7),
            Item("cooked beef", 8, 16), Item("arrow", 28), Item("shears", 29, unbreakable=True), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(areas=ZN.rects(), max_height=P.MAX_BUILD))
print(M.xml())
