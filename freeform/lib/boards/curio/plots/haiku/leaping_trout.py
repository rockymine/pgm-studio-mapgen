"""A leaping trout: a stone basin of water on the grass, and a trout of orange clay rising out of it in an arc. The body
tapers from a forked tail on the west to a blunt head on the east, speckled with white, with an eye and fins. The back is
stepped, one block a station, so a hider can climb from the stair on the west to the peak."""
from mc import B

NAME = "The Leaping Trout"
KIND = "sculpture"

TROUT = (B.STAINED_CLAY, 1)     # orange flanks
SPOT = (B.WOOL, 0)              # white speckles
BASIN = (B.STONEBRICK, 0)
FIN = (B.STAINED_CLAY, 4)       # yellow fins
EYE = (B.WOOL, 15)
TAIL = (B.STAINED_CLAY, 1)

# the body at each station along the fish: (bottom, top) of the column, tail at 2 and head at 9
BODY = {2: (2, 2), 3: (2, 3), 4: (2, 4), 5: (2, 5), 6: (2, 6), 7: (2, 7), 8: (3, 8), 9: (3, 9), 10: (3, 8)}


def build(c):
    # the basin: a stone pool on the grass, its walls two blocks high, the water inside it
    c.fill(1, 0, 1, 9, 1, 9, *BASIN)
    c.fill(2, 1, 2, 8, 1, 8, B.WATER)
    # the body: a column of clay at each station, with the white speckles on its back
    for x, (bot, top) in BODY.items():
        c.fill(x, bot, 3, x, top, 7, *TROUT)
        for y in range(bot, top + 1):
            if (x * 3 + y * 5) % 4 == 0:
                c.set(x, y, 3, *SPOT)
                c.set(x, y, 7, *SPOT)
    # the forked tail, two fins spread from the body's tip on the west
    c.set(1, 1, 5, *TAIL)
    c.set(1, 1, 4, *TAIL)
    c.set(1, 1, 6, *TAIL)
    c.set(1, 2, 4, *TAIL)
    c.set(1, 2, 6, *TAIL)
    # the dorsal fin on the peak, and the pectoral fins by the head
    c.set(7, 8, 5, *FIN)
    c.set(5, 6, 2, *FIN)
    c.set(7, 2, 8, *FIN)
    # the eye, on the head, facing the street on both sides
    c.set(10, 7, 3, *EYE)
    c.set(10, 7, 7, *EYE)
    # the stair up the west side, to the passage round the tail
    c.set(0, 0, 5, B.STONEBRICK_STAIRS, 0)
