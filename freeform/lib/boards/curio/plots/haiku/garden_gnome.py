"""A garden gnome: a blue robe with a hollow inside, entered by a passage two blocks up from a stair on the west; a pink
face with a nose and black eyes; a big white beard down the front; a tall red pointed hat with a brim; and a ladder
up the back of the robe."""
from mc import B

NAME = "The Garden Gnome"
KIND = "sculpture"

ROBE = (B.WOOL, 11)
SKIN = (B.WOOL, 6)
BEARD = (B.WOOL, 0)
HAT = (B.WOOL, 14)
EYE = (B.WOOL, 15)
BOOT = (B.STONE, 0)
BELT = (B.HARDENED_CLAY, 12)


def disc(c, y, r, bid, d=0, cx=5, cz=5):
    for x in range(11):
        for z in range(11):
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.5:
                c.set(x, y, z, bid, d)


def build(c):
    # the boots and the robe: blue, a little wider than the head, with a hollow inside
    c.fill(1, 0, 2, 9, 0, 8, *BOOT)
    c.fill(1, 1, 2, 9, 7, 8, *ROBE)
    c.fill(3, 1, 3, 7, 4, 7, B.AIR)
    c.fill(2, 2, 5, 3, 3, 5, B.AIR)                  # the passage from the west, two blocks up
    c.fill(1, 2, 5, 1, 3, 5, B.AIR)
    c.set(0, 0, 5, B.OAK_STAIRS, 0)
    c.fill(1, 4, 2, 9, 4, 2, *BELT)                  # the belt, with a gold buckle
    c.set(5, 4, 2, B.GOLD_BLOCK)

    # the beard: a white skirt round the top of the robe, all four sides, and a white band under the face
    for x in range(1, 10):
        for z in range(2, 9):
            if x in (1, 9) or z in (2, 8):
                c.fill(x, 5, z, x, 7, z, *BEARD)
    c.fill(2, 8, 3, 8, 8, 7, *BEARD)

    # the head: a pink face, with black eyes and a nose on every side
    c.fill(2, 9, 3, 8, 11, 7, *SKIN)
    for x, z in ((3, 3), (7, 3), (3, 7), (7, 7)):
        c.set(x, 10, z, *EYE)
    c.set(5, 9, 2, *SKIN)
    c.set(5, 9, 8, *SKIN)
    c.set(1, 9, 5, *SKIN)
    c.set(9, 9, 5, *SKIN)

    # the hat: a tall red cone on a brim, pointing into the sky
    disc(c, 12, 4, *HAT)
    disc(c, 13, 3, *HAT)
    disc(c, 14, 3, *HAT)
    disc(c, 15, 2, *HAT)
    disc(c, 16, 2, *HAT)
    disc(c, 17, 1, *HAT)
    disc(c, 18, 1, *HAT)
    c.set(5, 19, 5, *HAT)
    c.set(5, 20, 5, *HAT)

    # a ladder up the back of the robe, to the shoulder
    for y in range(0, 8):
        c.set(10, y, 5, B.LADDER, 5)
