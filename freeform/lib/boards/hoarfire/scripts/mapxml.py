"""Write Hoarfire's map.xml: two teams of twenty, their spawns, a Rime Monument and an Ember Core each from the
plan's objectives; a kit whose diamond pickaxe breaks the obsidian and the packed ice; building over the void only
in the Rift; the kill height under the islands; fire and the random tick held, so the falls, the hearths and the snow
stay as they were built.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.logic import Gamerules
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, Match, terrain_of

M = Map("Hoarfire", "1.0.0", "Leak the enemy's Ember Core in the autumn wood and break their Rime Monument on the snow.",
        ["dtc", "dtm"],
        terrain=terrain_of(__file__),
        authors=["Claude Opus 5.5 (freeform, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("diamond pickaxe", 2, enchant=[("efficiency", 2)], unbreakable=True),
            Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True), Item("wood", 4, 64, 1),
            Item("stained clay", 5, 64, team_color=True), Item("golden apple", 6), Item("water bucket", 7),
            Item("cooked beef", 8, 16), Item("arrow", 28), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("chainmail leggings", unbreakable=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(areas=[P.BUILD_ZONE], max_height=P.MAX_BUILD),
        kill=KillHeight(P.KILL_Y),
        match=Match(time_of_day=10000),
        parts=[Gamerules({"doFireTick": False, "randomTickSpeed": 0})])
print(M.xml())
