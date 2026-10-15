"""Write Sandreach's map.xml: two teams, their spawns, each wool with its room, its entry rule and its spawner; the
kit; building only over the board and its zones.
"""
import plan as P
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of

O = P.objectives()

M = Map("Sandreach", "1.1.0", "Capture the other team's wool and destroy its emerald!", ["ctw", "dtm"],
        terrain=terrain_of(__file__),
        authors=["rockymine", "Claude (freeform generator, pgmvox)"],
        objectives=O,
        kit=Kit(
            Item("stone sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64),
            Item("stained clay", 5, 48, team_color=True), Item("golden apple", 6), Item("cooked beef", 7, 16),
            Item("shears", 8, unbreakable=True), Item("arrow", 28),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("leather leggings", unbreakable=True, team_color=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.MAX_BUILD))
print(M.xml())
