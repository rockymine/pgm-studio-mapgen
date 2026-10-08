"""A split tree stump, lived in: a bark drum with a cut top, a room hollowed in its foot with a raised doorway,
a stair up the west side, a ladder up the north side, a small window, a chimney and flower pots on the top."""
from mc import B

NAME = "The Hollow Stump"
KIND = "house"

BARK = (B.LOG, 12)               # upright bark
HEART = (B.LOG, 0)               # the cut rings of the top
MOSS = (B.MOSSY, 0)


def disc(c, y, r, bid, d=0, cx=5, cz=5):
    for x in range(11):
        for z in range(11):
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.5:
                c.set(x, y, z, bid, d)


def ring(c, y, r_in, r_out, bid, d=0):
    for x in range(11):
        for z in range(11):
            d2 = (x - 5) ** 2 + (z - 5) ** 2
            if r_in * r_in + 0.5 < d2 <= r_out * r_out + 0.5:
                c.set(x, y, z, bid, d)


def build(c):
    # the stump: bark on the outside, a ring of heartwood round the middle, cut flat at the top
    for y in range(0, 8):
        disc(c, y, 4, *BARK)
        disc(c, y, 2.5, *HEART)
    disc(c, 8, 4, *HEART)                              # the cut top, its rings in the logs' ends
    ring(c, 0, 4, 4, *MOSS)                             # moss on the base

    # the room: hollowed out of the heart, with a doorway on the west, two blocks up
    for y in range(0, 4):
        disc(c, y, 2, B.AIR)
    c.fill(1, 2, 5, 3, 3, 5, B.AIR)                    # the doorway and its passage
    c.set(3, 2, 4, B.AIR)
    c.set(3, 3, 4, B.AIR)

    # the stair up to the doorway, and the ladder up the north side to the cut top
    c.set(0, 0, 5, B.OAK_STAIRS, 0)
    for y in range(0, 9):
        c.set(5, y, 0, B.LADDER, 2)

    # a window of glass on the east face of the stump, and a chimney on the cut top
    c.set(9, 4, 5, B.GLASS)
    c.set(9, 5, 5, B.GLASS)
    c.set(7, 9, 7, B.COBBLE)
    c.set(7, 10, 7, B.COBBLE)
    c.set(7, 11, 7, B.COBBLE)
    c.set(6, 9, 3, B.FLOWER_POT, 0)
    c.set(4, 9, 8, B.FLOWER_POT, 0)
    c.set(3, 9, 3, B.DANDELION)
    c.set(4, 9, 3, B.TALLGRASS, 1)
