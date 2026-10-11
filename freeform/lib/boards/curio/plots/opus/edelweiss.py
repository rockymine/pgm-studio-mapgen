"""The Edelweiss: one alpine flower as tall as a house. Woolly grey-green leaves wind up round the stalk as steps to
a star of white felted petals with a yellow heart; at the stalk's foot the lowest leaves arch into a bower, its way
in bent round the stalk, where nobody on the street can see."""
import math

from mc import B

NAME = "The Edelweiss"
KIND = "sculpture"

C = 5
STALK = (B.WOOL, 13)
LEAF, LEAF_PALE = (B.WOOL, 5), (B.WOOL, 8)
PETAL, PETAL_EDGE = (B.WOOL, 0), (B.SNOW, 0)
HEART = (B.WOOL, 4)
PETALS_Y = 11
RING = [(6, 5), (6, 6), (5, 6), (4, 6), (4, 5), (4, 4), (5, 4), (6, 4)]


def petal_r(theta):
    """A star of eight felted petals, pointed."""
    return 2.2 + 2.9 * abs(math.cos(4 * theta)) ** 1.6


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for y in range(0, PETALS_Y + 1):
        c.set(C, y, C, *STALK)
    # the bower: a leafy mound round the stalk's foot, hollow inside, its door bent so no line from the street
    # reaches the chamber
    for x in range(11):
        for z in range(11):
            d = math.hypot(x - C, z - C)
            if 1.5 <= d <= 4.6:
                h = int(3.6 * math.sqrt(max(0.0, 1 - (d / 4.7) ** 2)))
                for y in range(0, h + 1):
                    c.set(x, y, z, B.LEAVES, 0 | 4)
    for x in range(11):
        for z in range(11):
            d = math.hypot(x - C, z - C)
            if 0.9 <= d <= 3.1:
                c.set(x, 0, z, B.AIR); c.set(x, 1, z, B.AIR)      # the chamber round the stalk
                c.set(x, -1, z, B.DIRT, 2)
    for y in range(0, 4):                                        # no door: in by the open ring round the stalk,
        c.set(4, y, 5, B.LADDER, 4)                              # out by a ladder on the stalk
    # the leaf stair: round the stalk, a block higher at each step, felted leaves sticking out between
    k = 0
    for y in range(2, PETALS_Y):
        x, z = RING[k % len(RING)]
        c.set(x, y, z, *(LEAF if k % 2 else LEAF_PALE))
        k += 1
    for (x, z), (dx, dz) in (((7, 5), (1, 0)), ((3, 6), (-1, 0)), ((5, 7), (0, 1))):
        for i in range(2):
            c.set(x + dx * i, 4 + 3 * ((x + z) % 3) - i, z + dz * i, *LEAF)
    # the star of petals, felted white, its tips turned up, and a heart of little yellow florets
    last = RING[(PETALS_Y - 3) % len(RING)]
    for x in range(11):
        for z in range(11):
            d = math.hypot(x - C, z - C)
            th = math.atan2(z - C, x - C)
            r = petal_r(th)
            if d <= r and (x, z) not in (last, RING[(PETALS_Y - 4) % len(RING)], RING[(PETALS_Y - 5) % len(RING)]):
                c.set(x, PETALS_Y, z, *(PETAL_EDGE if d > r - 0.8 else PETAL))
                if d > r - 0.8 and d > 3.5:
                    c.set(x, PETALS_Y + 1, z, *PETAL_EDGE)
    for x in range(C - 1, C + 2):
        for z in range(C - 1, C + 2):
            if (x, z) not in (last, RING[(PETALS_Y - 4) % len(RING)]):     # the stair comes up through here
                c.set(x, PETALS_Y + 1, z, *HEART)
    c.set(C, PETALS_Y + 2, C, *HEART)
    # little edelweiss and stones round the foot
    for x, z in ((0, 0), (10, 10), (0, 10), (1, 8)):
        c.set(x, 0, z, B.FLOWER, 3)
    for x, z in ((10, 6), (0, 4)):
        c.set(x, 0, z, B.COBBLE)
