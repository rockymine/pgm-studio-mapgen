"""Write Thawline's map.xml: the teams, spawns, observer, the two cores and the two monuments come from the plan's
objectives; the kit (a diamond pickaxe for the obsidian), building only over a marked column, the build height, the
fall into the rift, and fire held where it is laid (no spread) are stated here.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.logic import Gamerules
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, terrain_of

M = Map("Thawline", "1.0.0", "Leak the enemy's Heart and break their Lantern.", ["dtc", "dtm"],
        terrain=terrain_of(__file__),
        authors=["Claude Opus 5.5 (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("diamond pickaxe", 2, enchant=[("efficiency", 2)], unbreakable=True),
            Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), Item("wood", 4, 64, 1),
            Item("stained clay", 5, 64, team_color=True), Item("golden apple", 6), Item("water bucket", 7),
            Item("cooked beef", 8, 16), Item("arrow", 28), Item("shears", 29, unbreakable=True),
            Item("stained glass", 30, 32, team_color=True), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.MAX_BUILD),
        kill=KillHeight(P.KILL_Y),
        parts=[Gamerules({"doFireTick": False})])
print(M.xml())
