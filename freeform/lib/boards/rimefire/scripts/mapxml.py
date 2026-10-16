"""Rimefire's map.xml: Destroy the Core, two teams of up to 24, building over the island only."""
from plan import KILL_Y, TEAMS, objectives
from pgmvox.play.rules import Build, Item, Kit, KillHeight, Map, Match, terrain_of

M = Map("Rimefire", "1.0.0", "Leak the enemy core: a Furnace in the fire half, a Cold Hearth in the ice.", "dtc",
        terrain=terrain_of(__file__),
        authors=["Claude (pgmvox)"],
        objectives=objectives(),
        kit=Kit(
            Item("stone sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64),
            Item("stained clay", 5, 32, team_color=True), Item("golden apple", 6), Item("cooked beef", 7, 16),
            Item("shears", 8, unbreakable=True), Item("arrow", 28),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("leather leggings", unbreakable=True, team_color=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=112),
        kill=KillHeight(KILL_Y),
        match=Match(time=2400))
print(M.xml())
