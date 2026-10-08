"""Drop — the library's worked course plan: a short water drop, run south and falling from 120 to 30, its left
and right ways mirror images across x = -0.5, meeting on the middle pieces. Plan phase only: the course, its
audit and its sketch.

    y is the top of a piece, the block a player stands on
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.pieces import Course, box  # noqa: E402
from pgmvox.plan import Symmetry  # noqa: E402

KILL_Y = 10
HEALTH = 20
COLOURS = {"void": (34, 38, 52), "floor": (150, 175, 110), "roof": (150, 90, 70), "beam": (170, 140, 100),
           "water": (70, 120, 200), "start": (120, 150, 200)}


def build():
    C = Course(Symmetry("mirror_x"))
    C.add("the start", box(-6, 5, 0, 8), 120, "start", spawn=True)
    C.add("the ledges", box(-12, -8, 12, 18), 112)
    C.add("the roofs", box(-11, -4, 23, 31), 100, "roof")
    C.add("the beam", box(-1, 0, 36, 50), 95, "beam")
    C.add("the pillars", box(-6, -5, 54, 55), 92, "beam")
    C.add("the galleries", box(-12, -6, 60, 70), 80, "roof")
    C.add("the terrace", box(-9, 8, 76, 86), 60, "water", water=box(-9, 8, 76, 86))    # a paddy, water to its edges
    C.add("the barge", box(-5, 4, 93, 105), 30, "water", water=box(-5, 4, 93, 105))
    return C
