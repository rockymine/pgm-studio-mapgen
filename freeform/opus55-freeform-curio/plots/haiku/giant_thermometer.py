"""A giant thermometer: a red bulb at the foot, a hollow in the bulb entered by a passage two blocks up from a stair on the
west, a ladder up the bulb's west side to its top, and a glass tube rising out of the bulb with red mercury and scale marks."""
from mc import B

NAME = "The Thermometer"
KIND = "structure"

RED = (B.HARDENED_CLAY, 14)
GLASS_TUBE = (B.GLASS, 0)
MERCURY = (B.WOOL, 14)
MARK = (B.QUARTZ, 0)                                # quartz ticks on the scale


def disc(c, y, r, bid, d=0, cx=5, cz=5):
    for x in range(11):
        for z in range(11):
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.5:
                c.set(x, y, z, bid, d)


def build(c):
    # the bulb: a red drum, three blocks round, from the grass to its top
    for y in range(0, 6):
        disc(c, y, 3.6, *RED)
    # the hollow in the bulb, its passage from the west two blocks up
    c.fill(3, 1, 4, 7, 3, 6, B.AIR)
    c.fill(1, 0, 4, 1, 1, 4, *RED)                    # the step under the passage
    c.fill(2, 0, 4, 2, 1, 4, *RED)                    # the bulb's round corners, closed
    c.fill(2, 4, 4, 2, 5, 4, *RED)
    c.fill(2, 0, 6, 2, 5, 6, *RED)
    c.fill(1, 2, 4, 2, 3, 4, B.AIR)
    c.set(0, 0, 4, B.STONEBRICK_STAIRS, 0)
    # the tube: glass walls rising from the bulb's top, with mercury inside
    c.fill(4, 6, 4, 6, 17, 6, *GLASS_TUBE)
    c.fill(5, 6, 5, 5, 16, 5, *MERCURY)
    c.fill(4, 17, 4, 6, 17, 6, *RED)
    # scale marks: slabs on the west side of the tube
    for y in (7, 9, 11, 13, 15):
        c.set(3, y, 5, *MARK)
        c.set(7, y, 5, *MARK)
    c.set(5, 17, 5, *RED)
    # a ladder up the bulb's west side, from the grass to its top
    for y in range(0, 6):
        c.set(1, y, 5, B.LADDER, 4)
