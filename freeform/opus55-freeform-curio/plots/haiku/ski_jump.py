"""A timber ski jump: a judges' tower on the west with a booth inside, a ramp sloping down to the east from the tower top
over the square, and a hollow under the ramp joined to the booth through the tower. A stair and a passage two blocks up
lead in from the west; a ladder climbs the tower's west face to the top."""
from mc import B

NAME = "The Ski Jump"
KIND = "structure"

TIMBER = (B.PLANKS, 1)          # spruce boards
LOG_POST = (B.LOG, 1)           # spruce logs for the posts
RAIL = (B.WOOL, 14)             # red flags on the ramp edge
RAMP_TOP = (B.STAINED_CLAY, 0)  # white landing mat

# the ramp's top at each station, one block a step down the slope
RAMP = {5: 9, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4}


def build(c):
    # the judges' tower: a solid timber tower, four blocks wide, ten high, with a booth hollowed inside
    c.fill(1, 0, 2, 4, 10, 8, *TIMBER)
    c.fill(2, 1, 3, 3, 3, 7, B.AIR)                  # the booth
    c.fill(2, 0, 3, 3, 0, 7, *LOG_POST)              # its floor, of logs
    # the passage from the west, two blocks up, and the passage east through the tower into the ramp's hollow
    c.fill(1, 2, 5, 1, 3, 5, B.AIR)
    c.fill(4, 2, 5, 4, 3, 5, B.AIR)
    c.set(0, 0, 5, B.SPRUCE_STAIRS, 0)
    c.fill(1, 0, 5, 1, 1, 5, *TIMBER)                # the step under the passage

    # the ramp: a slope of timber from the tower's east face down over the square, with a hollow under it
    for x, top in RAMP.items():
        c.fill(x, 0, 3, x, top, 7, *TIMBER)
    c.fill(5, 1, 4, 9, 3, 6, B.AIR)                  # the hollow under the ramp
    # the landing mat at the ramp's foot, and red flags along the edge
    for x in (5, 6, 7, 8, 9, 10):
        c.set(x, RAMP[x] + 1, 3, *RAIL)
    c.set(10, 5, 7, *RAMP_TOP)

    # a ladder up the tower's west face, from the grass to the top
    for y in range(0, 10):
        c.set(0, y, 3, B.LADDER, 4)
