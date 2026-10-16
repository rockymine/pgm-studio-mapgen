"""Rimeglow Rift's objectives, drawn once for the north half (Rime) and carried by the half turn to the south half
(Ember): a spawn in the court of each hall and a core held over a pit on each butte."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.play.objectives import Box, Core, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Item, Kit  # noqa: E402
from pgmvox.plan.raster import Symmetry  # noqa: E402

KILL_Y = 10
FLOOR = 71
CORE_BOX = Box(45, 74, -49, 47, 76, -47)


def objectives():
    O = Objectives(Teams(("rime-team", "Rime", "aqua", 24), ("ember-team", "Ember", "gold", 24)), Symmetry("half"))
    O.add(Spawn("rime-team", (13, FLOOR + 1, -68), yaw=0, area=Box(-3, FLOOR, -92, 29, FLOOR + 14, -63),
                spread=[Box(1, FLOOR + 1, -76, 8, FLOOR + 1, -66), Box(18, FLOOR + 1, -76, 25, FLOOR + 1, -66)]))
    O.add(Core("rime-core", "Rimewatch Core", "rime-team", CORE_BOX, leak=6))
    O.add(Observer((0, 92, 0), yaw=0), mirror=False)
    return O


def kit():
    return Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
               Item("diamond pickaxe", 2, enchant=[("efficiency", 2)], unbreakable=True),
               Item("iron axe", 3, unbreakable=True), Item("wood", 4, 64), Item("stained clay", 5, 48, team_color=True),
               Item("golden apple", 6, 2), Item("cooked beef", 7, 16), Item("arrow", 28),
               Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
               Item("iron chestplate", unbreakable=True, wear="chestplate"),
               Item("chainmail leggings", unbreakable=True, wear="leggings"),
               Item("leather boots", unbreakable=True, team_color=True, wear="boots"))


# the named places, north half (x, z); each has its half turn in the south, under the other half's name
PLACES = {
    "Rime Hall": (13, -83), "Hearth Court": (13, -70), "Rimewatch": (46, -48), "Frostmere": (-8, -42),
    "Hoarwood": (-50, -66), "Woodcutters' Rest": (-40, -60), "Glacier Tongue": (-26, -74),
    "Meltgate": (0, -24), "Hoarspan": (-38, -22), "Kindlespan": (38, -22),
}
SOUTH_NAMES = {
    "Rime Hall": "Ember Hall", "Rimewatch": "Emberwatch", "Frostmere": "Cinder Mere", "Hoarwood": "Amberwood",
    "Woodcutters' Rest": "Orchard Keeper's", "Glacier Tongue": "Cooled Flow", "Hearth Court": "Hearth Court",
    "Meltgate": "Meltgate", "Hoarspan": "Kindlespan", "Kindlespan": "Hoarspan",
}
