"""Write Crucible's map.xml: two teams of twenty-four, each with a crucible (the core) hung over the casting pit in
front of its foundry and a dye stock (the wool) in the cold store at the foundry's deepest level. A team wins by
leaking the other's crucible and placing the other's wool on its own monument; the two are separate goals, and
the crucible's casing turns to gold at fifteen minutes and to glass at twenty, so a held core still ends. The
cold store's shell is kept from being dug through, so its three ways in are the ways in, and no player may place
or scoop lava, since a bucket of it near a crucible would leak it.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.logic import All, Any, Cause, Deny, Material  # noqa: E402
from pgmvox.play.mapxml import E  # noqa: E402
from pgmvox.play.objectives import Box  # noqa: E402
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, Zone, terrain_of  # noqa: E402

O = P.objectives()
s = P.STORE
SHELL = [Box(s.x0 - 2, s.feet - 4, s.z0 - 2, s.x1 + 2, s.feet - 2, s.z1 + 2),                   # under the floor
         Box(s.x0 - 2, s.feet - 1, s.z1 + 1, s.x1 + 2, s.feet + s.h + 1, s.z1 + 2),             # the back wall
         Box(s.x1 + 1, s.feet - 1, s.z0 - 2, s.x1 + 2, s.feet + s.h + 1, s.z1),                 # the east wall
         Box(s.x0 - 2, s.feet + s.h, s.z0 - 2, s.x1 + 2, s.feet + s.h + 1, s.z1)]               # the roof
O.add(Zone("red-store-shell", SHELL, place=False, break_=False, team="red-team",
           message="The cold store's shell is blast-proof: come in by a door."))


class Modes:
    """The crucibles' casing through the match: gold at fifteen minutes, glass at twenty."""

    def write(self, doc):
        doc.add(E("modes", E("mode", after="15m", material="gold block", name="`6GOLD CRUCIBLE MODE"),
                  E("mode", after="20m", material="glass", name="`fGLASS CRUCIBLE MODE")))


M = Map("Crucible", "0.1.0", "Leak the enemy's crucible over its casting pit and carry its dye stock home from the "
        "cold store under its mountain.", ["ctw", "dtc"],
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "The brief: a bunker in rock, a core and a wool, ramps between its levels")],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("stained clay", 4, 64, team_color=True), Item("wood", 5, 48), Item("golden apple", 6),
                Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28, 48),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.BUILD_HEIGHT,
                    rule=Deny(All(Any(Material("lava"), Material("stationary lava")), Cause("player"))),
                    message="Lava may not be placed or taken."),
        kill=KillHeight(P.KILL_Y),
        rules=["Leak the enemy's crucible and capture its wool: both, to win.",
               "The crucibles turn to gold at 15 minutes and to glass at 20.",
               "The cold store's shell is blast-proof: its ways in are the doors and the flank cave."],
        parts=[Modes()])
print(M.xml())
