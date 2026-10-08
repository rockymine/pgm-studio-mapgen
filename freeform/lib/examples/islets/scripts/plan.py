"""Islets — the library's worked example: a small King of the Hill board of two floating islands and a middle
hill, drawn once as a raster with its half turn in the plan, and read by the checker, the sketch and the generator.

    floors: 30 the islands, 33 the middle hill; the void below, the kill height at 20, cloud far under it
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.plan import Raster, Symmetry  # noqa: E402

KILL_Y = 20
GROUND = 30
HILL = 33
KINDS = ["void", "floor", "stair", "hill", "spawn"]
COLOURS = {"void": (34, 38, 52), "floor": (150, 175, 110), "stair": (170, 160, 130), "hill": (225, 205, 120),
           "spawn": (120, 150, 200)}
WALK = {"floor", "stair", "hill", "spawn"}


def build():
    R = Raster((-30, 29), (-16, 15), KINDS, base_h=0, base_kind="void", symmetry=Symmetry("half"))
    R.poly([(-28, -9), (-14, -12), (-11, -2), (-14, 9), (-26, 10)], GROUND)       # red's island and its image
    R.rect(-25, -22, -2, 1, GROUND, "spawn")
    R.rect(-2, 1, -4, 3, HILL, "hill", both=False)                                 # the middle hill, one only
    R.rect(-8, -3, -1, 0, GROUND)                                                  # a causeway out to it
    R.flight((-3, -1), "e", width=(0, 1), h0=GROUND + 1, n=2)                      # two steps up onto the hill
    R.rect(-8, -6, -6, -5, GROUND)                                                 # a stepping stone, a jump away
    return R
