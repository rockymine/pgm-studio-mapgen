"""Write Riad's map.xml from the plan's posts and spawns: King of the Flag for two teams of sixteen, the flag on
three posts, its carrier slowed and armoured lighter, a team's dead waiting while one of their own holds it, no
building and no using a block, the clock held at noon.

    python3 mapxml.py > map.xml
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.objectives import Box, Flag, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import (Build, Effect, EnchantItem, ForEveryone, Item, Kit, Map, Match, Respawn,  # noqa: E402
                               terrain_of)

block = lambda p: (math.floor(p[0]), int(p[1]), math.floor(p[2]))       # noqa: E731

O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)))
O.add(Observer((0, 40, 0), yaw=90))
for team, z0 in (("red", -56), ("blue", 46)):                         # the terraces two over the back gardens
    x, y, z, yaw = P.SPAWNS[team]
    O.add(Spawn(f"{team}-team", block((x, y, z)), yaw=yaw, kit="spawn-kit", filter="flag-free",
                area=Box(-10, 22, z0, 10, 29, z0 + 10)), mirror=False)
flag = Flag("flag", "Flag", "purple", [(p["name"], block(p["at"]), p["yaw"]) for p in P.POSTS],
            pickup_kit="flag-kit", drop_kit="reset-health", proximity="none", show_respawn=False,
            hold_respawn=True, compass=True)
O.add(flag)

M = Map("Riad", "0.1.0", "Hold the flag for 200 seconds. While your team holds it, your dead wait.", "kotf",
        terrain=terrain_of(__file__),
        authors=["Claude (freeform generator)"], includes=[],
        objectives=O,
        kit=Kit(Item("stone sword", 0, unbreakable=True), Item("bow", 1, unbreakable=True),
                Item("golden apple", 2), Item("compass", 3), Item("arrow", 8, 12),
                Item("leather helmet", unbreakable=True, team_color=True, wear="helmet"),
                Item("leather chestplate", unbreakable=True, team_color=True, wear="chestplate"),
                Item("chainmail leggings", unbreakable=True, enchant=[("projectile_protection", 3)], wear="leggings"),
                Item("iron boots", unbreakable=True, wear="boots"),
                clear=True, effects=[Effect("resistance", "7.5s", 5)], game_mode="adventure",
                reward=[Item("arrow", amount=6)]),
        kits=[Kit(id="flag-kit", force=True, max_health=8,                # the carrier: four hearts, slowed
                  effects=[Effect("absorption", "3s", 2), Effect("slowness")],
                  actions=[EnchantItem("chainmail leggings", "projectile_protection", 2)]),
              Kit(id="reset-health", force=True, max_health=20,           # on the drop: health back, all regenerate
                  effects=[Effect("slowness", "0s", 0), Effect("regeneration", "2s", 10)],
                  actions=[EnchantItem("chainmail leggings", "projectile_protection", 3),
                           ForEveryone(f"all(alive,not({flag.carrier()}))",
                                       Kit(effects=[Effect("regeneration", "4s", 3)]))])],
        build=Build(never=True, use=False),
        match=Match(score=200, time_of_day=6000,
                    respawn=Respawn("3s", auto=True, spectate=True,
                                    message="death.respawn.confirmed.waiting.flagDropped")))
print(M.xml())
