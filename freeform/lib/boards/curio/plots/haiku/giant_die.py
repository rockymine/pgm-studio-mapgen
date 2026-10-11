"""A giant die showing five pips on its top face, cut from quartz with black pips and a red edge. A cavity inside is
entered by a passage two blocks up from a stair on the west, and a ladder up the west face leads to the top."""
from mc import B

NAME = "The Giant Die"
KIND = "sculpture"

QUARTZ = (B.QUARTZ, 0)
PIP = (B.WOOL, 15)
EDGE = (B.WOOL, 14)


def build(c):
    # the cube: quartz, with a red edge along the bottom
    c.fill(1, 0, 1, 9, 7, 9, *QUARTZ)
    c.fill(1, 0, 1, 9, 0, 1, *EDGE)
    c.fill(1, 0, 9, 9, 0, 9, *EDGE)
    # the cavity inside, and its passage on the west face, two blocks up
    c.fill(3, 1, 3, 7, 5, 7, B.AIR)
    c.fill(1, 2, 4, 2, 3, 4, B.AIR)
    c.fill(2, 2, 4, 3, 3, 4, B.AIR)
    c.set(0, 0, 4, B.STONEBRICK_STAIRS, 0)
    # the pips: five on the top face and five on each side face, set flush into the quartz
    for x, z in ((3, 3), (7, 3), (5, 5), (3, 7), (7, 7)):
        c.set(x, 7, z, *PIP)
    for a, y in ((3, 2), (7, 2), (5, 4), (3, 6), (7, 6)):
        c.set(9, y, a, *PIP)                        # east face
        c.set(1, y, a, *PIP)                        # west face
        c.set(a, y, 9, *PIP)                        # south face
        c.set(a, y, 1, *PIP)                        # north face
    # a ladder up the west face to the top, climbed beside the passage
    for y in range(0, 8):
        c.set(0, y, 5, B.LADDER, 4)
