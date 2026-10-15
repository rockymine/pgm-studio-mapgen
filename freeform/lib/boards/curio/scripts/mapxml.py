"""Write Curio Square's map.xml from the plan, after the community's Hide n' Seek maps: hiders and seekers, the
seekers blinded in a glass cage over the fountain for twenty-five seconds, six plots vanishing every minute in one
of four random orders, the hiders winning if any is alive at seven minutes.

    python3 mapxml.py > map.xml
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
import sketch  # noqa: E402
from gen import CAGE, Y  # noqa: E402
from pgmvox.play.logic import (Act, Action, After, All, Any, Area, Cause, Compass, Deny, Fill, Gamerules,  # noqa: E402
                               Give, Message, Named, Ref, SetVar, Team, Time, Trigger, Variable)
from pgmvox.play.objectives import Box, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.play.rules import Blitz, Bounds, Build, Effect, Item, Kit, Map, Match, terrain_of  # noqa: E402

ORDERS = 4
POTION = Item("potion", name="`rPotion of Invisibility `7(15s)", effects=[Effect("invisibility", "15s")])
LOCKED = dict(unbreakable=True, locked=True)

plots = [(f"plot-{i}-{j}", row["name"] if row else "a plot", *P.origin(i, j))
         for (i, j), (builder, row) in sorted(sketch.layout().items())]
names = {rid: name for rid, name, _, _ in plots}
orders = []
for k in range(ORDERS):
    ids = [p[0] for p in plots]
    random.Random(100 + k).shuffle(ids)
    orders.append(ids)

O = Objectives(Teams(("hiders", "Hiders", "green", 50, {"show_name_tags": False, "plural": True}),
                     ("seekers", "Seekers", "dark aqua", 3, {"max_overfill": 3, "plural": True})))
O.add(Spawn("hiders", kit="hider", safe=True, spread=[Box(x0, Y, z0, x1, Y, z1) for x0, z0, x1, z1 in
                                                     ((-8, -8, 8, -7), (-8, 7, 8, 8), (-8, -6, -7, 6), (7, -6, 8, 6))]))
O.add(Spawn("seekers", (P.CENTRE_X, CAGE[1] + 1, P.CENTRE_Z), kit="seeker-blind", filter="not(seekers-released)"))
O.add(Spawn("seekers", (P.CENTRE_X, Y, P.CENTRE_Z + 7), kit="seeker", filter="seekers-released"))
O.add(Observer((P.CENTRE_X, Y + 30, P.CENTRE_Z + 60), yaw=180, pitch=35))
O.add(Bounds(Box(-P.HALF, 0, -P.HALF, P.HALF, 255, P.HALF), message="The fair is inside the walls!"))


def vanish(k):
    """The k-th round: one of the four orders, drawn at the start, says which six plots go."""
    rounds = [Act([a for rid in ids[k * P.PER_ROUND:(k + 1) * P.PER_ROUND]
                   for a in (Fill(rid), Message(f"`7- {names[rid]}"))], filter=f"order={n}")
              for n, ids in enumerate(orders)]
    return Act([Message(f"`6`l{P.PER_ROUND} curiosities have vanished!")] + rounds, id=f"vanish-{k + 1}",
               scope="match")


LOGIC = ([Area("seeker-cage", [Box(*CAGE)])] +
         [Area(rid, [Box(x0, Y, z0, x0 + P.PLOT - 1, Y + 23, z0 + P.PLOT - 1)]) for rid, _, x0, z0 in plots] +
         [Named("seekers-released", After(f"{P.RELEASE}s", "match-started",
                                          message="`3`lSeekers`r will be released in {0}")),
          Named("seekers-out", All(Ref("seekers-released"), Team("seekers")))] +
         [Named(f"round-{k + 1}", Time(f"{t}s")) for k, t in enumerate(P.ROUNDS)] +
         [Named(f"potion-{r}", All(Time(f"{P.ROUNDS[r - 1]}s"), Team("hiders"))) for r in (1, 3, 5)] +
         [Give("hider-potion", f"potion-{r}") for r in (1, 3, 5)] +
         [Give("seeker", "seekers-out"),
          Variable("order"),
          Action("cage-clearer", [Fill("seeker-cage")]),
          Trigger("seekers-released", "cage-clearer"),
          Trigger("always", [SetVar("order", f"floor(random() * {ORDERS})")])] +
         [Trigger(f"round-{k + 1}", vanish(k)) for k in range(len(P.ROUNDS))] +
         [Compass("only-seekers", name="`3Closest Seeker"), Gamerules({"doTileDrops": False})])

M = Map("Curio Square", "1.0.0", "Hide from the seekers until the time runs out!", "arcade",
        terrain=terrain_of(__file__), includes=[],
        rules=["Fall damage is disabled.", "Hiders' name tags are hidden.",
               "Every minute six of the fair's curiosities vanish."],
        objectives=O, parts=LOGIC,
        kits=[Kit(id="seeker-blind", effects=[Effect("blindness")], game_mode="adventure"),
              Kit(Item("iron sword", 0, **LOCKED), Item("diamond helmet", wear="helmet", **LOCKED),
                  Item("diamond chestplate", wear="chestplate", **LOCKED),
                  Item("diamond leggings", wear="leggings", **LOCKED), Item("diamond boots", wear="boots", **LOCKED),
                  id="seeker", force=True, clear="effects", effects=[Effect("speed")], game_mode="adventure"),
              Kit(Item("compass", 0, locked=True), POTION, id="hider", game_mode="adventure",
                  remove=["glass bottle"]),
              Kit(POTION, id="hider-potion", deduct_items=False)],
        build=Build(rule=Deny(Any(Cause("player"), Cause("explosion")))),
        match=Match(time=P.TIME, result="hiders", blitz=Blitz(1, "only-hiders"), fall_damage=False,
                    time_of_day=6000,
                    broadcasts=[("alert", P.RELEASE, "Seekers have been released!"),
                                ("tip", P.RELEASE + 10, "Every minute, six of the curiosities will vanish!")] +
                               [("alert", t - 10, "Six curiosities vanish in 10 seconds!") for t in P.ROUNDS] +
                               [("tip", 5, "Your name tag is hidden from the seekers.", "only-hiders")]))
print(M.xml())
