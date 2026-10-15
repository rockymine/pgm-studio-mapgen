"""A copper kettle: a round copper drum with a verdigris band, a lid with a gold knob, an arched handle over it, a
spout on the east, a stair up to a doorway into the drum's hollow foot, and a ladder up the north side to the shoulder."""
import math

from mc import B

NAME = "The Copper Kettle"
KIND = "house"

CU = (B.HARDENED_CLAY, 1)        # copper: orange hardened clay
CU_DARK = (B.HARDENED_CLAY, 12)  # aged copper
VERDIGRIS = (B.STAINED_CLAY, 5)  # the green band
STONE = (B.STONEBRICK, 0)


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
    # the plinth: stone brick, a little wider than the drum
    disc(c, 0, 4, *STONE)
    # the drum: copper, with a hollow room in its foot
    for y in range(1, 6):
        disc(c, y, 4, *CU)
    for y in range(0, 4):
        disc(c, y, 2.5, B.AIR)                          # the room
    c.fill(1, 2, 5, 2, 3, 5, B.AIR)                     # its doorway, on the west, two blocks up
    c.fill(2, 2, 5, 2, 3, 5, B.AIR)
    ring(c, 5, 3.5, 4, *VERDIGRIS)                      # the verdigris band round the drum

    # the shoulder: a walkable ring at the top of the drum, stepped up to the lid
    disc(c, 6, 4, *CU_DARK)
    disc(c, 7, 3, *CU)
    disc(c, 8, 2, *CU_DARK)
    c.set(5, 9, 5, B.GOLD_BLOCK)                        # the knob

    # the handle: an arch of copper over the lid, from the west side to the east side
    for i in range(0, 121):
        t = math.pi * i / 120
        c.set(round(5 + 5 * math.cos(t)), round(7 + 5 * math.sin(t)), 5, B.IRON_BLOCK)

    # the spout: a stair sloping down from the east side of the drum
    c.set(10, 4, 5, B.BRICK_STAIRS, 1)
    c.set(10, 3, 5, B.BRICK_STAIRS, 1)

    # the stair up to the doorway on the west
    c.set(0, 0, 5, STONE[0], 0)
    # the ladder up the north side to the shoulder
    for y in range(0, 7):
        c.set(5, y, 0, B.LADDER, 2)
