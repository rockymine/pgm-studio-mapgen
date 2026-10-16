"""Rimefire's plan: two teams, the same bones in two skins, a spawn each at the back of its half and a core each on
the east (fire) or the west (ice) of it, the seam between.

    fire (north): spawn at the back ridge, the core in the Furnace on the tor, the hamlet in the hollow
    ice (south):  the half turn of all of it
    the walk from a core to its own spawn is about a third of the walk to the enemy spawn, and the objective stands
    off to one side of the line between the spawns, in front of the spawn it belongs to
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.play.objectives import Box, Core, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan.raster import Symmetry  # noqa: E402

import land as LND  # noqa: E402

KILL_Y = LND.KILL_Y
SPAWN_AT = (-14, LND.LEVEL + 2, -73)
LODGE_AREA = (-29, LND.LEVEL + 1, -90, 1, LND.LEVEL + 9, -66)
CORE_BOX = LND.CORE_BOX
TEAMS = Teams(("fire-team", "Fire", "red", 24), ("ice-team", "Ice", "aqua", 24))


def objectives():
    O = Objectives(TEAMS, Symmetry("half"))
    O.add(Spawn("fire-team", SPAWN_AT, yaw=0, area=Box(*LODGE_AREA)))
    O.add(Core("fire-core", "the Furnace", "fire-team", Box(*CORE_BOX), leak=5), name="the Cold Hearth")
    O.add(Observer((0, 100, -1), yaw=0), mirror=False)
    return O
