"""Write Claywork's map.xml. The teams, their spawns, the observer point, the four wools with their monuments,
spawners and rooms (entry and block protection) come from the plan's objectives; the kit, building only over a marked column and the build
height are stated here, and what a player keeps and is rewarded with follows from the kit. The void below the
world is the kill.
"""
import plan  # noqa: F401  (puts the library on the path)
from plan import MAX_BUILD, objectives
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of

O = objectives()

M = Map("Claywork", "1.0.0", "Capture the enemy's two wools from the Kilns in their back corners.", "ctw",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator, pgmvox)"],
        objectives=O,
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
            Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), Item("wood", 4, 64, 1),
            Item("stained clay", 5, 64, team_color=True), Item("golden apple", 6), Item("water bucket", 7),
            Item("cooked beef", 8, 16), Item("arrow", 28), Item("shears", 29, unbreakable=True), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=MAX_BUILD))
print(M.xml())
