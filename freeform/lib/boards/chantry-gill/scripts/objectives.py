"""Chantry Gill's teams, spawns and monuments. Blue's are stated; red's are their images under the half turn.

    objectives()    pgmvox Objectives: two spawns, the observer, four monuments
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from layout import FLOOR                                                              # noqa: E402
from pgmvox import B                                                                   # noqa: E402
from pgmvox.plan.raster import Symmetry                                                # noqa: E402
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402

SYM = Symmetry("half")
SPAWN_AT = (4, FLOOR + 6, 95)                     # on the spawn knoll's foot, the hall behind, facing the front
SPAWN_AREA = Box(-3, FLOOR + 4, 90, 12, FLOOR + 20, 99)
TOWN = (-14, FLOOR + 2, 57)                         # the square's paving under it
SCAR = (54, FLOOR + 10, 82)                          # the bench under it
MAX_BUILD = FLOOR + 52


def monument(x, ground, z):
    return Box(x, ground + 4, z, x, ground + 6, z)


def objectives():
    O = Objectives(Teams(("blue-team", "Blue", "blue", 16), ("red-team", "Red", "red", 16)), SYM)
    O.add(Spawn("blue-team", SPAWN_AT, yaw=180, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Observer((0.5, FLOOR + 40, 0.5), yaw=90), mirror=False)
    O.add(Destroyable("blue-town", "Chantry Monument", "blue-team", monument(*TOWN), (B.OBSIDIAN, 0), "obsidian"))
    O.add(Destroyable("blue-scar", "Scar Monument", "blue-team", monument(*SCAR), (B.OBSIDIAN, 0), "obsidian"))
    return O
