"""Coldstore's every number. The board is one quarter drawn and mirrored twice: across v = -0.5 inside a team, and
across u = -0.5 between the teams. Blue holds the west (u < 0); the drawn quarter is blue's south one, u -92 to -1,
v 0 to 54. x is u and z is v; the world's middle is the corner where the four quarters meet.

The quarter is measured off the author's concept world: every rectangle below is one of its pieces, moved into this
frame (u = x - 42, v = z - 45). Heights are the concept's own.
"""

from pgmvox.plan.raster import Symmetry                                                # noqa: E402

SYM = Symmetry("mirror_x")                       # between the teams; inside a team the quarter is mirrored in z too

# ---- the box --------------------------------------------------------------------------------------------------------
X0, Z0, SX, SZ, SY = -128, -80, 256, 160, 100
MARGIN = 22                                      # the ice field runs this far past the bunker's walls, down its sides
INNER = (-92, -1, 0, 54)                         # the drawn quarter's inside, u0, u1, v0, v1
OUTER_U, OUTER_V = -104, 56                      # the bedrock box's outer faces in the quarter: u -104, v 56
FLOOR = 7                                        # an island's underside; below it, nothing but void to the world's floor
TOP = 17                                         # an island's top block: players stand at y 18
PLINTH = (9, 10)                                 # the stone plinth round every island, pillar and wall, a block proud
CEIL = 41                                        # the last block of air: the roof's bedrock is y 42 to 48
ROOF = (42, 48)
TRIM = 36                                        # the ceiling trim on the walls, y 36 to 41
TUNNEL = (27, 34)                                # a vent tunnel: floor y 27, air y 28 to 34

# ---- the walls that are the map's edge, as (u0, u1, v0, v1) of rock from floor to roof ----------------------------------
WALLS = [
    (-104, -91, 0, 56),                          # the west wall, two blocks of face over the spawn's rock
    (-104, -1, 45, 56),                          # the south wall
    (-104, -83, 27, 56),                         # the south-west bulk, behind the wool room
    (-92, -72, 25, 34),                          # the wool block: the room and the monument in front of it
    (-51, -42, 35, 56),                          # the buttress out of the south wall
]

# ---- the islands: where the concept has a floor, here a slab of rock with nothing under it ---------------------------
ISLANDS = [
    (-90, -62, 0, 4),                            # the hub's strip along the middle, joined to its image across v -0.5
    (-71, -62, 0, 14),                           # the hub's leg south
    (-31, -20, 25, 43),                          # the south-east island's arm
    (-20, -11, 34, 43),                          # its foot east
    (-24, -17, 44, 51),                          # the alcove of the great door, a step into the south wall
]

# ---- the pillars: the negatives of a void hole, bedrock from floor to roof ----------------------------------------------
PILLARS = [
    dict(box=(-51, -32, 5, 14), tunnel=dict(axis="v", at=(-39, -36))),   # the vent tunnel runs south to north through it
    dict(box=(-20, -11, 0, 4)),                                          # on the line between a team's quarters
    dict(box=(-10, -1, 15, 24), tunnel=dict(axis="u", at=(18, 21))),     # on the line between the teams: the crossing
]

# ---- the wool block -------------------------------------------------------------------------------------------------
ROOM = (-87, -85, 27, 32)                        # the wool room, floor y 27, air y 28 to 31
ROOM_FLOOR = 27
SCREEN_U = -84                                   # the pane wall between the room and the monument
DOOR_V = (29, 30)                                # its middle, two wide and four tall, opened when the monument goes
MONUMENT = (-82, -73, 27, 32, 25, 35)            # the end stone capsule, u0, u1, v0, v1, y0, y1, rounded
CASE_U = -72                                     # its glass case on the void, and in the faces north and south
WOOL_FOUND = (-86, 28, 30)                       # where the wool lies on its pad

# ---- the spawn, cut into the west wall --------------------------------------------------------------------------------
SPAWN_ROOM = (-101, -93, -5, 4)                  # floor y 17, air to y 23
SPAWN_EXIT = (-92, -91, -3, 2)                   # the opening onto the hub, y 18 to 21
SPAWN = (-97, 18, 0)
SLOT = (-87, 18, 2)                              # the monument for the wool taken from the enemy's south room

# ---- the roof fans and the vents --------------------------------------------------------------------------------------
FANS = [(-61, 25, 8)]                            # (u, v, r): a round hole in the roof over the void, a fan in it
SURFACE = 49                                     # the ice over the roof starts here
SHAFT = 3.2                                      # a fan's shaft up through the ice to the sky, this radius
POCKET = (-90, -73, 5, 24)                       # beside the spawn, between it and its wool block: its team builds nothing
ARROW_SQUARE = (-86, -84, 19, 21)                # the arrow's square of colour, u0, u1, y0, y1, in the face at v 26
