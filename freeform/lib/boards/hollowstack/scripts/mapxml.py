"""Write Hollowstack's map.xml: the teams, spawns, observer and wools come from objectives.py; the kit, building
over the void only in the chasm between the walls, and the build height are stated here.

    python3 mapxml.py > map.xml
"""
import layout as L
import objectives as P
from pgmvox.play.rules import Build, Item, Kit, Map, terrain_of

M = Map("Hollowstack", "1.0.0", "Capture the enemy's two wools, from the forest in its cavern and the vault in its "
        "dungeon, and carry them up to your keep.", "ctw", terrain=terrain_of(__file__),
        authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("stone sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
            Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64, 1),
            Item("glass", 5, 64), Item("golden apple", 6), Item("water bucket", 7), Item("ladder", 8, 32),
            Item("arrow", 28), Item("shears", 29, unbreakable=True), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("leather leggings", unbreakable=True, team_color=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(areas=[(-L.FACE - 1, L.Z0, L.FACE, L.Z0 + L.SZ - 1)], max_height=P.MAX_BUILD))
print(M.xml())
