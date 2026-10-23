"""Frostvault's every number. The board is a layout the studio's generator composed, read as a bunker: the composed
board is `assets/composed.json`, written by

    dotnet run freeform/lib/pgmvox/data/compose_board.cs -- 24 mirror_z 11 assets/composed.json

and `pgmvox.plan.bunker.draw` turns it into rock, island, void and pillar. The teams split across z: blue holds the
south (z > 0), red the north, each the other's mirror.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.built.bunker import Heights                                                # noqa: E402

COMPOSED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "composed.json")
PLAYERS, SYMMETRY, SEED = 24, "mirror_z", 11
GAP = 2                        # cells of void an isolation cut and a seal's front take: ten blocks
MOAT = 2                       # cells of void between the shore and the bunker's walls
CUT = ("wool", "frontline")    # the generator's boxes cut from the rest of a team's land
H = Heights()                  # the concept's heights: floors y 17, the roof y 42 to 48
SY = 76
TEAMS = {0: ("blue-team", "Blue", "blue"), 1: ("red-team", "Red", "red")}
KEPT = {0: ("orange", "lime"), 1: ("purple", "yellow")}   # the wools each team keeps, its rooms west to east
