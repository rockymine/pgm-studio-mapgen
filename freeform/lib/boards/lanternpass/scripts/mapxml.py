"""Write Lantern Pass's map.xml from the plan: the bell's region, the shrine, the side-swap rows, the warm-up gate
and the spawns are the plan's own numbers. Runners have one life and win by holding the bell for two seconds;
shooters cross between the walkways on the yellow rows and win at the clock.

    python3 mapxml.py > map.xml
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.logic import After, ControlPoint, Fill, MatchStarted, Named, Trigger  # noqa: E402
from pgmvox.play.objectives import Box, Objectives, Observer, Portal, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Blitz, Build, Effect, Item, Kit, Map, Match, Zone, terrain_of  # noqa: E402

lx0, lx1 = P.LANE
bx0, bx1, bz0, bz1 = P.BELL["box"]
hx0, hx1, hz0, hz1 = P.HEAL["box"]
left, right = P.WALKS["left"], P.WALKS["right"]
ledge = int(P.walkway_heights(P.build())[P.iz(-6)]) + 1          # the shooters' ledges, over the boathouse


def leather(colour, boots, *rest):
    return [Item(f"leather {part}", color=boots if part == "boots" else colour, wear=part)
            for part in ("helmet", "chestplate", "leggings", "boots")] + list(rest)


O = Objectives(Teams(("runners", "Runners", "light purple", 25, {"max_overfill": 30, "plural": True}),
                     ("shooters", "Shooters", "dark blue", 4, {"plural": True})))
O.add(Observer((0, 70, -21)))
O.add(Spawn("runners", kit="runner-kit", spread=Box(lx0 + 4, 21, -8, lx1 - 4, 21, 2)))
O.add(Spawn("shooters", kit="shooter-kit", spread=[Box(left[0] + 1, ledge, -8, left[1], ledge, -5),
                                                   Box(right[0], ledge, -8, right[1] - 1, ledge, -5)]))
O.add(ControlPoint("the-bell", "The Bell", Box(bx0, P.BELL["y"], bz0, bx1, P.BELL["y"] + 2, bz1),
                   capture_time="2s", capture_filter="only-runners"))
O.add(Zone("shrine", [Box(hx0, 33, hz0, hx1, 35, hz1)], kit="heal"))
O.add(Zone("boathouse", [Box(lx0 + 3, 20, -9, lx1 - 3, 27, 3)], enter="never",
           enter_message="You may not go back into the boathouse!"))
for side, x in (("left", left[0]), ("right", right[1])):          # the outer row of each walkway swaps sides
    O.add(Portal(f"swap-{side}", Box(x, 0, P.Z_MIN + 2, x, 255, P.Z_MAX - 2), by=(P.SWAP_DX[side], 0, 0)))

FED = Kit(id="fed", food=20)
M = Map("Lantern Pass", "1.0.0", "Runners: reach the temple and hold the bell for two seconds. Shooters: stop every "
        "runner before the clock runs out.", ["arcade", "blitz"], terrain=terrain_of(__file__), includes=[],
        rules=["Fall damage is off. Runners have one life.",
               "Shooters: step on the yellow row to cross to the other walkway."],
        objectives=O,
        kits=[FED,
              Kit(*leather("E07AAE", "FFFFFF"), id="runner-kit", parents=[FED], clear=True,
                  effects=[Effect("speed", "oo")]),
              Kit(*leather("1D2A5C", "111111", Item("bow", 0, unbreakable=True,
                                                    enchant=[("power", 3), ("punch", 1), ("infinity", 1)]),
                           Item("arrow", 28)),
                  id="shooter-kit", parents=[FED], clear=True, effects=[Effect("speed", "oo", 2)]),
              Kit(id="heal", health=20)],
        parts=[Named("warmup-over", After(P.WARMUP, MatchStarted())),
               Trigger("warmup-over", [Fill([Box(*b) for b in P.GATE_REGIONS["warmup"]])])],
        build=Build(never=True, use=False),
        match=Match(time=P.TIME, result="shooters", blitz=Blitz(1, "only-runners", broadcast=True),
                    fall_damage=False))
print(M.xml())
