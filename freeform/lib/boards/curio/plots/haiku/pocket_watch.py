"""A giant pocket watch stood on its edge: a round-cornered case of gold, a white face with black numerals on both sides,
a bow ring on top and a chain of iron links below. A cavity is hollowed in the case, entered by a passage two blocks up
from a stair on the west; a ladder climbs the west face to the top of the case."""
from mc import B

NAME = "The Pocket Watch"
KIND = "sculpture"

GOLD = (B.GOLD_BLOCK, 0)
FACE = (B.QUARTZ, 0)
NUMERAL = (B.WOOL, 15)

# the numerals of the dial, on the face's ring: (across, up)
DIAL = ((5, 11), (7, 10), (8, 8), (7, 6), (5, 5), (3, 6), (2, 8), (3, 10))


def face(c, z):
    c.fill(2, 3, z, 8, 11, z, *FACE)
    for a, y in DIAL:
        c.set(a, y, z, *NUMERAL)
    c.set(5, 8, z, *NUMERAL)
    c.set(5, 9, z, *NUMERAL)
    c.set(5, 10, z, *NUMERAL)


def build(c):
    # the case: a slab of gold standing on its edge, its east corners rounded off
    c.fill(1, 0, 3, 9, 13, 7, *GOLD)
    for y in (0, 1, 12, 13):
        c.set(9, y, 3, B.AIR)
        c.set(9, y, 7, B.AIR)
    c.set(8, 0, 3, B.AIR)
    c.set(8, 0, 7, B.AIR)
    # the faces, one each side of the case, with their numerals
    face(c, 7)
    face(c, 3)
    # the bow: a gold ring on top of the case
    c.set(4, 14, 5, *GOLD)
    c.set(5, 14, 5, *GOLD)
    c.set(6, 14, 5, *GOLD)
    c.set(4, 15, 5, *GOLD)
    c.set(6, 15, 5, *GOLD)
    c.set(5, 16, 5, *GOLD)

    # the cavity inside the case, its passage from the west at the height of the second block, and the stair
    c.fill(3, 1, 4, 7, 4, 6, B.AIR)
    c.fill(1, 2, 4, 2, 3, 4, B.AIR)
    c.fill(2, 2, 4, 3, 3, 4, B.AIR)
    c.set(0, 0, 4, B.OAK_STAIRS, 0)

    # a ladder up the west face, from the grass to the top of the case
    for y in range(0, 14):
        c.set(0, y, 5, B.LADDER, 4)
