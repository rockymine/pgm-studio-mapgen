"""Write Lantern Karst's map.xml. The teams, their spawns with their iron, the observer point, the four wools
with their monuments, spawners and rooms (entry and block protection) come from the plan's objectives; the kit,
the fall, building only over a marked column and the build height are stated here.
"""
import plan  # noqa: F401  (puts the library on the path)
from plan import KILL_Y, MAX_BUILD, objectives
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map

O = objectives()

M = Map("Lantern Karst", "0.2.0", "Capture the enemy's two wools: the Pillar Shrine's and the Tea Store's.", "ctw",
        authors=["Claude (freeform generator, ported onto pgmvox)"],
        objectives=O,
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
            Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), Item("wood", 4, 64, 1),
            Item("stained clay", 5, 48, team_color=True), Item("golden apple", 6), Item("water bucket", 7),
            Item("cooked beef", 8, 16), Item("arrow", 28), Item("shears", 29, unbreakable=True), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=MAX_BUILD),
        kill=KillHeight(KILL_Y))
print(M.xml())
