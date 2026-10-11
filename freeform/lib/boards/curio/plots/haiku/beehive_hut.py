"""A straw skep beehive hut: layers of straw that step in as they rise, banded with honeycomb, climbed by a stair of
straw up the west face to the comb cap. A room is hollowed in its foot, entered from the south under a low lip."""
from mc import B

NAME = "The Beehive Hut"
KIND = "house"

STRAW = (B.HAY, 0)
STRAW_SIDE = (B.HAY, 4)            # hay with the grain across the ring
COMB = (B.STAINED_CLAY, 4)         # honeycomb yellow
PLANK = (B.PLANKS, 2)              # birch shelves
STONE = (B.COBBLE, 0)


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
    # the skep: each layer one radius smaller than the one under it, so the outside is a stair to the top
    disc(c, 0, 5, *STONE)                                # the stone ring the skep stands on
    disc(c, 1, 4, *STRAW)
    disc(c, 2, 3, *STRAW)
    disc(c, 3, 2, *STRAW)
    disc(c, 4, 1, *STRAW)
    c.set(5, 5, 5, *COMB)                               # the comb cap, one block, to climb onto
    # the honeycomb showing through the straw: a scatter of comb cells in the first three layers
    for y in (1, 2, 3):
        for x in range(11):
            for z in range(11):
                if c.get(x, y, z)[0] == B.HAY and (x * 2 + z * 3 + y) % 7 == 0:
                    c.set(x, y, z, *COMB)
    # the bands: honeycomb round the second layer, grain across the first
    ring(c, 1, 3.5, 4, *STRAW_SIDE)
    ring(c, 2, 2.5, 3, *COMB)

    # the room: a hollow three blocks square in the heart of the skep, reached along a passage from the east
    # at the height of the second layer, up two blocks from the street. The passage is higher than a seeker's eye.
    c.fill(4, 1, 4, 6, 3, 6, B.AIR)
    c.fill(7, 2, 5, 8, 3, 5, B.AIR)
    c.fill(3, 1, 4, 3, 2, 6, B.AIR)
    # a flower and a pot by the door
    c.set(7, 1, 9, B.FLOWER_POT, 0)
    c.set(2, 1, 10, B.DANDELION)
    c.set(8, 1, 1, B.TALLGRASS, 1)
