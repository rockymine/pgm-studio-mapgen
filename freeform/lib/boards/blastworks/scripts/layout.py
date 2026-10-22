"""Blastworks' every number. Blue holds the west and red is its image under the half turn, (x, z) -> (-1 - x, -1 - z).
Every rectangle is (x0, z0, x1, z1) inclusive; a height is the top block's y.

The board finishes the author's second concept: a wool sealed in a box whose roof and east wall are doors of end
stone only TNT breaks, the roof under the deck a team walks on and the wall under the bridge. Its layout is the one
agreed in the author's review (plan 4 and the raised east block): blue's base runs z -21 to 20, even about the axis,
so the two sides stand in line.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.plan.raster import Symmetry                                                # noqa: E402

SYM = Symmetry("half")
X0, Z0, SX, SZ, SY = -128, -40, 256, 80, 48
SPAWN_H, FRONT_H, DECK_H, EAST_TOP = 12, 14, 18, 26
TUNNEL = (21, 25)                                # the east block's tunnel: its floor's y, its last air's y
MAX_BUILD = 32

# ---- nature: real ground, solid to the bottom ------------------------------------------------------------------------
SPAWN = (-110, 7, -69, 20)
FRONT = (-40, -21, -27, 20)

# ---- the grammar's pieces --------------------------------------------------------------------------------------------
BOX = (-96, -21, -77, -8)                        # the wool's box, its deck at 18
BRIDGE = (-76, -21, -60, -8)                     # the bridge, its deck at 18 and its underside at 12
DESCENT = (-59, -21, -41, -15)                   # the descent: 14 at its east end down to 5 at its west
EAST = (-59, -14, -41, -8)                       # the east block, raised to 26, the tunnel through its length
ARM = (-68, -14, -60, -8)                        # its arm over the bridge at 26, flush with the void's edge
TUNNEL_Z = (-12, -10)
EAST_STAIR = (-40, -12, -34, -10)                # from the front straight up into the tunnel, 14 to 21
UP_STAIR = (-82, -7, -77, 6)                     # the concept's stair up from the spawn to the deck
DOWN_STAIR = (-76, -1, -69, 6)                   # and its stair down, 12 to 6, toward the void under the bridge
EXIT = [(-68, 14, -59, 20), (-50, 14, -41, 20)]  # the spawn's second way out, its gap of eight between
STONE = (-11, -21, 2, -8)                        # the middle's stone, red's its image
TNT = (-2, -2, 1, 1)                             # the TNT spawner's pedestal at the very middle

# ---- the box, as the concept has it -----------------------------------------------------------------------------------
ROOF_DOOR = (-94, -19, -85, -10, 15, 17)         # x0, z0, x1, z1, y0, y1: end stone, three thick
SIDE_DOOR = (-80, -19, -78, -10, 2, 11)          # end stone in the east wall, onto the void under the bridge
ROOM = (-95, -20, -81, -9, 2, 14)
BOX_WOOL = (-91, 5, -15)

# ---- on the spawn -----------------------------------------------------------------------------------------------------
HOUSE = (-106, 10, -96, 17)
SPAWN_AT = (-101, 13, 18)                        # in front of the house's door
SPAWN_AREA = (-110, 7, -94, 20)
SLOT = (-87, 13, 12)

# ---- where a player may build over the void: blue's, and their images are red's ---------------------------------------
ZONES = [
    (-76, -21, -60, -8),                         # under the bridge, all of it
    (-76, -7, -69, -2),                          # in line with the stair down, from its foot to the bridge
    (-68, -1, -41, 13),                          # the hole, from the stair down's edge to the front
    (-58, 14, -51, 20),                          # the exit's gap
    (-26, -21, 25, 20),                          # the middle, front to front
]
MARKER_Y = 1
