"""Write Hollowstack's map.xml: the teams, spawns, observer and monuments come from objectives.py; the kit, building
over the void only in the chasm between the walls, the build height, breaking only what a player builds (and the
monuments), and no crafting table are stated here: the rock holds, so every way to a monument is a door.

    python3 mapxml.py > map.xml
"""
import layout as L
import objectives as P
from pgmvox.play.rules import Build, Crafting, Item, Kit, Map, terrain_of

M = Map("Hollowstack", "1.0.0", "Destroy the enemy's two monuments: the one over the shrine in the forest's cavern "
        "and the one in the vault at the back of the dungeon.", "dtm", terrain=terrain_of(__file__),
        authors=["Claude (freeform generator, on pgmvox)"],
        objectives=P.objectives(),
        kit=Kit(
            Item("stone sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
            Item("diamond pickaxe", 2, enchant=[("efficiency", 2)], unbreakable=True),
            Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64, 1),
            Item("glass", 5, 64), Item("golden apple", 6), Item("water bucket", 7), Item("ladder", 8, 32),
            Item("arrow", 28), Item("shears", 29, unbreakable=True), Item("wood", 31, 64, 1),
            Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
            Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
            Item("leather leggings", unbreakable=True, team_color=True, wear="leggings"),
            Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(areas=[(-L.FACE - 1, L.Z0, L.FACE, L.Z0 + L.SZ - 1)], max_height=P.MAX_BUILD,
                    break_only=("wood", "glass", "ladder", "obsidian")),
        parts=[Crafting()])
print(M.xml())
