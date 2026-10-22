"""Blastworks' every number. Blue holds the west and red is its image under the half turn, (x, z) -> (-1 - x, -1 - z).
Every rectangle is (x0, z0, x1, z1) inclusive, with the height of its top block.

**Blue's base is the author's concept, laid block for block.** `assets/concept.npz` is the concept world's built part
(without its signs, its redstone and the duck beside it), set down here moved by CONCEPT_AT. It holds the spawn block,
the stair up to the deck and the stair down from the spawn, the wool box with its two doors of end stone (its roof
and its east wall), the bridge over the void before the side door, and the east block with its stair down into that
void. What this board adds is what a generator adds round a spawn and a wool: the spawn's second way out, the hub where a
team's ways meet, its front and the middle, and the build zones with their redstone.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.plan.raster import Symmetry                                                # noqa: E402

SYM = Symmetry("half")
X0, Z0, SX, SZ, SY = -128, -64, 256, 128, 40
CONCEPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "concept.npz")
CONCEPT_AT = (-84, 0, 40)                        # the concept's own coordinates plus this are the board's
SPAWN_H, ISLE_H, DECK_H = 12, 14, 18
MAX_BUILD = 26

# ---- the concept's parts, in the board's coordinates (measured off the asset) ----------------------------------------
SPAWN_BLOCK = (-110, -15, -69, -2)
BOX = (-96, -43, -77, -30)
ROOF_DOOR = (-94, -41, -85, -32, 15, 17)         # x0, z0, x1, z1, y0, y1: end stone, three thick
SIDE_DOOR = (-80, -41, -78, -32, 2, 11)          # end stone in the box's east wall, on the void under the bridge
ROOM = (-95, -42, -81, -31, 2, 14)               # the room inside the box, its floor falling to the side door
BOX_WOOL = (-91, 5, -37)                         # where the concept's sign said the wool is
SPAWN = (-102, 13, -8)                           # where the concept's sign said the spawn is
SPAWN_AREA = (-110, -15, -95, -2)

# ---- what this board adds, in the concept's widths (a band fourteen, a lane seven): (name, box, top, fill) -----------
LAND = [
    ("spawn-exit", (-68, -9, -34, -3), SPAWN_H, "lanes"),     # the spawn's other way out, where the concept's sign said
    ("hub", (-40, -43, -27, -16), ISLE_H, "plates"),          # where a team's ways meet: the east block, the exit, the front
    ("front", (-21, -25, -8, -12), ISLE_H, "plates"),         # the team's front, before the middle
    ("mid", (-6, -6, 5, 5), ISLE_H, "hazard"),                # the middle, shared
]
# flights: (name, box, the top at its low end, at its high end, the side its high end is on)
FLIGHTS = [
    ("exit-corner", (-40, -15, -34, -10), SPAWN_H, ISLE_H, "n"),  # the exit turning the corner up into the hub
    ("hub-stair", (-40, -36, -37, -30), ISLE_H, DECK_H, "w"),     # from the hub up to the east block's deck
]
SLOT = (-87, 13, -10)                            # the monument for the wool blue takes, on the spawn block
ON_THE_BOX = (-96, -43, -84, -30, 15, 26)        # over the box, inside its bedrock edge: closed to the box's own team

# ---- where a player may build over the void: blue's, and their images are red's ---------------------------------------
ZONES = [
    (-76, -43, -60, -30),                        # the concept's: the void under the bridge, before the side door
    (-65, -29, -60, -22),                        # and its foot, past the bottom of the stair down from the spawn
    (-26, -27, -22, -12),                        # from the hub to the front
    (-12, -11, -1, -7),                          # from the front to the middle
]
MARKER_Y = 1
