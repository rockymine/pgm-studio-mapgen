"""Write Penstock's map.xml: a team deathmatch with score boxes for two teams of sixteen, ten minutes, a kill a point
and a score box two; a scorer is sent home; diamonds on the Exciter buy from the Station Store, whose Quartermaster
stands in each spawn; kill streaks pay diamonds; only leaves may be placed; a fall down a tailrace shaft is fatal.
Red's half is stated and blue's mirrored across the middle.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

from pgmvox.plan.raster import Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Objectives, Observer, ScoreBox, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import (Build, Effect, Item, KillHeight, KillReward, Kit, Map, Match, Offer,  # noqa: E402
                               Respawn, Shop, Shopkeeper, Spawner, Zone, terrain_of)

O = Objectives(Teams(("red", "Red", "red", 16), ("blue", "Blue", "blue", 16)), Symmetry("mirror_x"))
O.add(Observer((0, 30, 0), yaw=90))
O.add(Spawn("red", (-64, 25, -1), yaw=-90, kit="base-kit", area=Box(-69, 0, -11, -56, 255, 10)))
for side, z0 in (("n", -36), ("s", 30)):              # in red's back wall: blue scores here and is sent home
    O.add(ScoreBox("blue", Box(-60, 22, z0, -58, 24, z0 + 5), points=2, home=(63, 25, -1), home_yaw=90))
O.add(Zone("red-scoreboxes", [Box(-60, 22, -36, -57, 24, -31), Box(-60, 22, 30, -57, 24, 35)], place=False,
           break_=False, message="You may not modify the score boxes!", team="red", enter="blue",
           enter_message="You may not enter your own score boxes!"))
O.add(Shopkeeper("store", "Quartermaster", (-68, 25, -7), yaw=-90, team="red"))
O.add(Spawner("diamond-spot", (-1, 23, -1), [("diamond", 1)], delay="25s", reach=None, box=Box(-1, 23, -1, 0, 23, 0)),
      mirror=False)                                   # diamonds on the Exciter in the middle of the hall
for key, z in (("arrows-north", -43), ("arrows-south", 41)):          # arrows in the two Pump Rooms
    O.add(Spawner(key, (-1, 21, z), [("arrow", 4)], delay="8s", max_entities=8, reach=None,
                  box=Box(-1, 21, z, 0, 21, z)), mirror=False)

STORE = Shop("store", "Station Store", [
    ("weapons", "iron sword", [Offer(Item("iron sword"), 3, "diamond"),
                               Offer(Item("bow", damage=374, enchant=[("power", 2)]), 2, "diamond"),
                               Offer(Item("arrow", amount=16), 1, "diamond")]),
    ("armour", "iron chestplate", [Offer(Item("iron chestplate"), 4, "diamond"),
                                   Offer(Item("iron leggings"), 3, "diamond"),
                                   Offer(Item("iron helmet"), 2, "diamond")]),
    ("supplies", "golden apple", [Offer(Item("golden apple"), 1, "diamond"),
                                  Offer(Item("leaves", amount=16), 1, "diamond")])])

M = Map("Penstock", "0.1.0", "Be the team with the most points after 10 minutes: a kill is a point, a score box two.",
        ["tdm", "scorebox"], terrain=terrain_of(__file__), authors=["Claude (freeform generator)"], includes=[],
        objectives=O, shops=[STORE],
        kit=Kit(Item("stone sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True), Item("golden apple", 2),
                Item("leaves", 3, 8), Item("arrow", 8, 16),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, wear="leggings"),
                Item("leather boots", unbreakable=True, team_color=True, wear="boots"),
                id="base-kit", clear=True, effects=[Effect("resistance", "4s", amplifier=5)],
                reward=[Item("arrow", amount=6), Item("leaves", amount=4),
                        KillReward([Item("diamond")], streak=2), KillReward([Item("diamond", amount=3)], streak=4),
                        KillReward([Item("diamond", amount=5)], streak=7)]),
        build=Build(only=("leaves",), max_height=34, message="Only leaves may be placed and broken!"),
        kill=KillHeight(8),
        match=Match(time=10 * 60, result="score", kills=1, respawn=Respawn("2s", auto=True)))
print(M.xml())
