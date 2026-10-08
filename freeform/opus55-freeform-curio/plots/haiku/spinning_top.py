"""A giant striped spinning top: a stem of stripes, a hollow inside entered by a passage two blocks up from a stair on the
west, a ladder up the stem's west side, and a flat head with a walk round it and a small spire on top."""
from mc import B

NAME = "The Spinning Top"
KIND = "sculpture"

STRIPES = [(B.WOOL, 14), (B.WOOL, 0), (B.WOOL, 11), (B.WOOL, 4), (B.WOOL, 0)]
SPIRE = (B.GOLD_BLOCK, 0)


def disc(c, y, r, bid, d=0, cx=5, cz=5):
    for x in range(11):
        for z in range(11):
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.5:
                c.set(x, y, z, bid, d)


def build(c):
    # the stem: a drum of stripes, four blocks round, one colour a layer
    for y in range(0, 5):
        bid, d = STRIPES[y % len(STRIPES)]
        disc(c, y, 4, bid, d)
    # the hollow inside the stem, entered by a passage two blocks up from the west
    c.fill(3, 1, 4, 7, 3, 6, B.AIR)
    c.fill(1, 0, 4, 1, 1, 4, B.WOOL, 0)               # the step under the passage
    c.fill(1, 2, 4, 2, 3, 4, B.AIR)
    c.fill(2, 2, 4, 2, 3, 4, B.AIR)
    c.set(0, 0, 4, B.STONEBRICK_STAIRS, 0)
    # the head: a plate of stripes one block high, its top a walk
    disc(c, 5, 3, B.WOOL, 14)
    # the spire on the head: a small cone, tipped with a gold block
    disc(c, 6, 2, B.WOOL, 4)
    c.set(5, 7, 5, *SPIRE)
    # a ladder up the stem's west side, to the walk round the head
    for y in range(0, 5):
        c.set(0, y, 5, B.LADDER, 4)
