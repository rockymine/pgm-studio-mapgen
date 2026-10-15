"""An upturned rowboat, lived under: a hull of planks turned keel-up on the grass, its belly hollowed into a cabin,
a stair to its low doorway in the bow, a stern seat, oars resting along the keel and a fence rack for them."""
from mc import B

NAME = "The Upturned Rowboat"
KIND = "house"

OAK = (B.PLANKS, 0)
SPRUCE = (B.PLANKS, 1)
KEEL = (B.WOOD_SLAB, 5)              # dark oak, a ridge down the keel
CUSHION = (B.WOOL, 14)               # red seat cushion
FENCE = B.FENCE


def half_width(x):
    """How far the hull reaches out from the centre line at this station along the boat."""
    if x in (1, 9):
        return 2
    if x in (2, 8):
        return 3
    return 4


def inside_hull(x, y, z):
    return 1 <= x <= 9 and 0 <= y <= 3 and abs(z - 5) <= half_width(x) - y * 0.6


def build(c):
    # the hull, plank by plank, spruce and oak in strakes
    for x in range(1, 10):
        for y in range(0, 4):
            for z in range(0, 11):
                if inside_hull(x, y, z):
                    c.set(x, y, z, *(SPRUCE if (y + abs(z - 5)) % 2 == 0 else OAK))
    # the keel: a dark ridge running the length of the upturned hull, one block high
    for x in range(2, 9):
        c.set(x, 4, 5, *KEEL)
    # the cabin, hollowed out of the belly: two blocks high, its floor the hull's own bottom
    for x in range(3, 8):
        for z in range(4, 7):
            for y in (1, 2):
                c.set(x, y, z, B.AIR)
    # the low doorway in the bow, two blocks up, reached from a stair in the grass
    c.fill(1, 2, 5, 2, 3, 5, B.AIR)
    c.fill(2, 2, 5, 3, 3, 5, B.AIR)
    c.set(0, 0, 5, B.OAK_STAIRS, 0)
    # a thwart block on the keel for a deck to stand on, and a red cushion in the stern
    c.set(5, 5, 5, B.WOOD_SLAB, 5)
    c.set(9, 4, 5, *CUSHION)
    # the oars: two lying along the hull's flank on the grass, leaning on fence posts
    for y in range(0, 3):
        c.set(10, y, 1, FENCE)
    for x in range(2, 9):
        c.set(x, 0, 0, B.LOG, 4)                             # a log of driftwood, lying along x
    for y in range(0, 4):
        c.set(10, y, 9, FENCE)
    c.set(10, 3, 8, B.FENCE_GATE, 0)
