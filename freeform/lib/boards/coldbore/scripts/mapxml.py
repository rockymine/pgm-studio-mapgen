"""Write Coldbore's map.xml: two teams of twenty, each with a reactor (the core) hanging over a pit in a hall inside
its mountain and an orange or cyan wool sealed in a vault deep in the mountain's other side. A reactor's leak
opens its vault: the trigger clears the core, the cradle round it and the pit, and the vault's blast door. The
vault's shell is kept from being dug through, and no player may place or scoop lava, since a bucket of it near a
core would leak it.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.logic import All, Any, Cause, Completed, Deny, Fill, Material, Message, Trigger  # noqa: E402
from pgmvox.play.objectives import Box  # noqa: E402
from pgmvox.play.rules import Build, Item, KillHeight, Kit, Map, Zone, terrain_of  # noqa: E402

O = P.objectives()
vault = next(s for s in P.SPACES if s.name == "vault")
SHELL = [Box(vault.x0 - 2, vault.feet - 6, vault.z0 - 2, vault.x1 + 2, vault.feet - 1, vault.z1 + 2),     # floor
         Box(vault.x0 - 2, vault.feet, vault.z0 - 2, vault.x0 - 1, vault.feet + vault.h + 1, vault.z1 + 2),
         Box(vault.x1 + 1, vault.feet, vault.z0 - 2, vault.x1 + 2, vault.feet + vault.h + 1, vault.z1 + 2),
         Box(vault.x0, vault.feet, vault.z0 - 2, vault.x1, vault.feet + vault.h + 1, vault.z0 - 1),
         Box(vault.x0, vault.feet, vault.z1 + 1, vault.x1, vault.feet + vault.h + 1, vault.z1 + 2),
         Box(vault.x0, vault.feet + vault.h, vault.z0, vault.x1, vault.feet + vault.h + 1, vault.z1)]   # ceiling
O.add(Zone("red-vault-shell", SHELL, place=False, break_=False, team="red-team",
           message="The vault's shell is blast-proof: leak the reactor above it."))
SPILL = Box(P.PIT.x0, P.L1, P.PIT.z0, P.PIT.x1, P.CORE.y1 + 1, P.PIT.z1)   # the cradle and the air round the core
OPEN = [P.CORE, SPILL, P.PIT]


def opened(team, colour, wool):
    boxes = OPEN if team == "red" else [b.image(P.SYM) for b in OPEN]
    door = P.VAULT_DOOR if team == "red" else P.VAULT_DOOR.image(P.SYM)
    name = "Red" if team == "red" else "Blue"
    return Trigger(Completed(f"{team}-core"),
                   [Fill(boxes, "air"), Fill([door], "air"),
                    Message(f"{name}'s reactor has leaked and its vault stands open: go and get the {wool} wool!")])


M = Map("Coldbore", "0.2.0", "Leak the enemy's reactor in the hall inside its mountain, then take the wool from "
        "the vault the leak opens across the station.", ["ctw", "dtc"],
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"],
        contributors=[("rockymine", "The idea: a bunker in a cliff, a fissure, a reactor and a vault apart")],
        objectives=O,
        kit=Kit(Item("iron sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
                Item("diamond pickaxe", 2, unbreakable=True), Item("iron axe", 3, unbreakable=True),
                Item("stained clay", 4, 64, team_color=True), Item("wood", 5, 48), Item("golden apple", 6),
                Item("water bucket", 7), Item("cooked beef", 8, 16), Item("arrow", 28, 48),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("iron chestplate", unbreakable=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots")),
        build=Build(max_height=P.BUILD_HEIGHT,                   # nobody pours or scoops lava: a bucket could leak a core
                    rule=Deny(All(Any(Material("lava"), Material("stationary lava")), Cause("player"))),
                    message="Lava may not be placed or taken."),
        kill=KillHeight(P.KILL_Y),
        rules=["A reactor's leak opens its vault's blast door: its wool cannot be reached before.",
               "The vault's shell is blast-proof."],
        parts=[opened("red", "red", "orange"), opened("blue", "blue", "cyan")])
print(M.xml())
