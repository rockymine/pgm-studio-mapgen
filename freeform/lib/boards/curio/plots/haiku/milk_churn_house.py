"""A tall milk churn: a steel drum with red bands, a flared foot, an overhanging lid with a dome and a gold knob.
A ladder up the west side climbs past the drum to a step onto the lid's well, which is open under the overhang."""
from mc import B

NAME = "The Milk Churn"
KIND = "house"

STEEL = (B.IRON_BLOCK, 0)
RED = (B.STAINED_CLAY, 14)
DARK = (B.PLANKS, 5)
FOOT = (B.STONEBRICK, 0)


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
    # the foot: a flared stone ring, then the steel drum
    disc(c, 0, 4, *FOOT)
    for x in range(11):                                 # the foot's corners, filled so no gap shows
        for z in range(11):
            if 16.5 < (x - 5) ** 2 + (z - 5) ** 2 <= 20:
                c.set(x, 0, z, *FOOT)
                c.set(x, 1, z, *STEEL)
    disc(c, 1, 3, *STEEL)
    for y in range(2, 9):
        disc(c, y, 3, *STEEL)
    # the red bands, one low and one high
    for y in (2, 7):
        ring(c, y, 2.5, 3, *RED)
    # the lid's overhang, a ring of dark oak that sticks out past the drum; its well is open inside
    ring(c, 9, 3, 4, *DARK)
    # the dome of the lid, and its gold knob
    disc(c, 10, 2, *DARK)
    disc(c, 11, 1, B.WOOD_SLAB, 5)
    c.set(5, 12, 5, B.GOLD_BLOCK)

    # the ladder up the west side, past the drum, to the top of the drum
    for y in range(0, 9):
        c.set(1, y, 5, B.LADDER, 4)
    # a stair at the top of the ladder, leading onto the lid's well
    c.set(2, 8, 5, B.DARK_OAK_STAIRS, 1)
    # a stair up the east side to a doorway into the drum, two blocks up, hollowed inside
    c.set(9, 0, 5, B.COBBLE_STAIRS, 1)
    for y in range(0, 8):
        disc(c, y, 2, B.AIR)                          # the hollow inside the drum, under the stair's doorway
    c.fill(7, 2, 5, 8, 3, 5, B.AIR)                   # the doorway from the stair
    # the well in the lid: a ladder-side window of glass, and a flower on the drum's shoulder
    c.set(6, 9, 4, B.FLOWER_POT, 0)
    c.set(4, 9, 6, B.FLOWER, 0)
