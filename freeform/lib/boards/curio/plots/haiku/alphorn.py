"""An alphorn, long and thin: a tall tube of pale wood with green bands, rising from a stone mouthpiece on the grass to a big
flared brass bell at the top. The mouthpiece is hollow and entered from the east by a passage two blocks up from a stair;
a ladder climbs the west side of the foot and the tube to the bell."""
from mc import B

NAME = "The Alphorn"
KIND = "sculpture"

WOOD = (B.HARDENED_CLAY, 4)      # the tube, pale bark
BAND = (B.STAINED_CLAY, 13)      # green wrapping
BRASS = (B.GOLD_BLOCK, 0)        # the bell
STONE = (B.STONEBRICK, 0)


def disc(c, y, r, bid, d=0, cx=4, cz=5):
    for x in range(11):
        for z in range(11):
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.5:
                c.set(x, y, z, bid, d)


def build(c):
    # the mouthpiece: a stone block on the grass, with a hollow inside
    c.fill(1, 0, 3, 6, 2, 7, *STONE)
    c.fill(2, 0, 4, 5, 1, 6, B.AIR)                 # the hollow
    c.fill(5, 2, 5, 6, 3, 5, B.AIR)                 # the passage from the east, two blocks up
    c.set(7, 0, 5, B.OAK_STAIRS, 1)                 # the stair up to the passage

    # the tube: two blocks wide and thin, rising from the mouthpiece to the bell
    c.fill(2, 4, 4, 3, 19, 6, *WOOD)
    for y in range(7, 19, 4):
        c.fill(2, y, 4, 3, y + 1, 6, *BAND)         # green wrappings round the tube
    # the ladder: up the west side of the foot, then up the tube's west side
    for y in range(0, 3):
        c.set(0, y, 5, B.LADDER, 4)
    for y in range(4, 20):
        c.set(1, y, 5, B.LADDER, 4)

    # the bell: a big brass flare at the top, widening upward, joined to the tube by a neck
    c.set(3, 20, 5, *BRASS)
    disc(c, 21, 1, *BRASS)
    disc(c, 22, 2, *BRASS)
    disc(c, 23, 3, *BRASS)
