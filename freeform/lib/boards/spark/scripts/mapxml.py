"""Write Spark's map.xml from the plan, after Knockout Stick Fight's: a knockback stick that steps up on a clock,
three seconds' protection at the start, nothing that hurts but the void, one life each.

    python3 mapxml.py > map.xml
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

import plan as P  # noqa: E402
from pgmvox.play.logic import All, Give, Named, Participating, Time  # noqa: E402
from pgmvox.play.objectives import Objectives, Observer, Spawn  # noqa: E402
from pgmvox.play.rules import Blitz, Build, Effect, Item, KillHeight, Kit, Map, Match, terrain_of  # noqa: E402

NAMES = {1: "`r`lKnockback 1 Stick", 2: "`r`a`lKnockback 2 Stick", 3: "`r`e`lKnockback 3 Stick",
         10: "`r`c`lKnockback 10 Stick"}
y = P.FLOOR_Y + 1


def spawn_points():
    """One block at the foot of every ray, facing out along it, on the ring round the hub's eye: (x, y, z, yaw)."""
    pts = []
    for a, length, w0, w1 in P.RAYS:
        t = math.radians(a)
        bx, bz = math.floor(P.SPAWN_R * math.cos(t)), math.floor(P.SPAWN_R * math.sin(t))
        if P.crate_at(bx, bz) or not P.is_floor(bx, bz):
            continue
        yaw = (a - 90) % 360                                     # Minecraft yaw: 0 faces south, 90 west
        pts.append((bx, y, bz, round(yaw - 360 if yaw > 180 else yaw)))
    return pts


def stick(level, **kit):
    return Kit(Item("stick", 0, name=NAMES[level], enchant=[("knockback", None if level == 1 else level)]), **kit)


O = Objectives()
O.add(Spawn(None, kit="stick", points=spawn_points(), far=True, safe=True))
O.add(Observer((0, y + 24, -41), pitch=40))

later = P.LEVELS[1:]
M = Map("Spark", "1.0.0", "Knock the other players off the spark and be the last one standing!", "blitz",
        terrain=terrain_of(__file__),
        includes=[], players=(2, 64),
        rules=["Players can only die to the void.", "Your stick gets stronger at one, two and four minutes."],
        objectives=O,
        kit=stick(1, id="stick", effects=[Effect("damage resistance", "3s", 255), Effect("slowness", "1s", 255),
                                          Effect("regeneration")], knockback_reduction=0.9, game_mode="adventure"),
        kits=[stick(level, id=f"stick{level}", force=True) for _, level in later],
        parts=[Give(Kit(knockback_reduction=0, force=True), Time("3s"))] +
              [part for t, level in later for part in (Named(f"from-{t}", All(Time(f"{t}s"), Participating())),
                                                       Give(f"stick{level}", f"from-{t}"))],
        build=Build(never=True),
        kill=KillHeight(P.KILL_Y),
        match=Match(time=P.TIME, blitz=Blitz(1, broadcast=True), fall_damage=False, time_of_day=6000,
                    broadcasts=[("alert", f"{t // 60}m", f"Your sticks are now knockback {level}!")
                                for t, level in later]))
print(M.xml())
