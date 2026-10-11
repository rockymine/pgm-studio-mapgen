"""Write Loomfall's map.xml from the plan: the spawn on the top carpet, the kill height, the wool that turns white
under a player's step and falls, and the clearing of falling wool before it lands on a carpet below.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.logic import (All, BlockDrop, Cause, Damage, Entity, Falling, KillEntities, Material,  # noqa: E402
                               MatchRunning, Named, Not, Pulse, Trigger)
from pgmvox.play.objectives import Box, Objectives, Observer, Spawn  # noqa: E402
from pgmvox.play.rules import Blitz, Build, Item, KillHeight, Kit, Map, Match, terrain_of  # noqa: E402

top = P.CARPETS[0][5] + 1
(sx0, sx1), (sz0, sz1) = P.SPAWN["x"], P.SPAWN["z"]

O = Objectives()
O.add(Spawn(None, kit="flyer", spread=Box(sx0, top, sz0, sx1, top, sz1), safe=True))
O.add(Observer((0, top + 19, -41), pitch=60))

M = Map("Loomfall", "1.0.0", "Keep running: the carpet falls away under every step. Be the last one flying.", "arcade",
        terrain=terrain_of(__file__),
        includes=[], players=(2, 40),
        rules=["Wool you step on turns white and falls.", "No fall damage, no fighting: only snowball grenades.",
               "Below the last carpet you are out."],
        objectives=O,
        kit=Kit(Item("snow ball", 0, 5, grenade=1), id="flyer", clear=True, game_mode="adventure", remove=["wool"]),
        parts=[BlockDrop(filter=Material("wool"), replacement="wool:0", trample=True),
               Falling(Material("wool:0"), delay=P.WOOL_DELAY),
               Named("running", MatchRunning()),
               Named("falling-wool", Entity("falling block")),
               Trigger(Pulse("0.25s", "0.5s", "running"), [KillEntities("falling-wool")]),
               Damage(allow=[Cause("void"), Cause("potion")], only=[Not(Cause("player"))])],
        build=Build(rule=Not(All(Cause("world"), Material("wool:0")))),
        kill=KillHeight(P.KILL_Y),
        match=Match(time=10 * 60, blitz=Blitz(1), fall_damage=False, time_of_day=18000))
print(M.xml())
