"""Write Rimeburn's map.xml: Ember and Frost, twenty-four a side; each defends its Hearth (a core) and its
Icestone (a monument of packed ice); the seam between the lands is the only place a player builds over the void.

    python3 mapxml.py > map.xml
"""
import plan as P
from pgmvox.play.logic import Gamerules
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, Match, terrain_of

ARMOUR = [Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
          Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
          Item("chainmail leggings", unbreakable=True, wear="leggings"),
          Item("leather boots", unbreakable=True, team_color=True, wear="boots")]


def kit(kid, wood):
    """The loadout: a diamond pickaxe for the Hearth's obsidian, an axe, the team's planks and glass to bridge the
    seam with, and the usual fight."""
    return Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
               Item("diamond pickaxe", 2, enchant=[("efficiency", 2)], unbreakable=True),
               Item("iron axe", 3, enchant=[("efficiency", 1)], unbreakable=True),
               Item("wood", 4, 64, wood), Item("golden apple", 5, 2), Item("glass", 6, 32),
               Item("cooked beef", 7, 16), Item("wood", 8, 64, wood), Item("arrow", 28),
               *ARMOUR, id=kid)


M = Map("Rimeburn", "1.0.0",
        "Break the enemy's Hearth and shatter their Icestone. Frost keeps a fire in the snow, Ember keeps ice in the "
        "autumn; each must lose both.", "dtcm",
        terrain=terrain_of(__file__),
        authors=["Claude Opus 5.5 (freeform, on pgmvox)"],
        objectives=P.objectives(),
        kits=[kit("frost-kit", 1), kit("ember-kit", 4)],
        build=Build(areas=[P.SEAM], max_height=P.MAX_BUILD),
        kill=KillHeight(P.KILL_Y),
        match=Match(time="25m"),
        rules=["Destroy both of the enemy's objectives: their Hearth (leak its lava) and their Icestone.",
               "The two lands meet only across the void: bridge the seam, or take the Thaw in its middle.",
               "The Vent under each front comes up in that side's Hearth Hollow."],
        parts=[Gamerules({"doFireTick": False})])
print(M.xml())
