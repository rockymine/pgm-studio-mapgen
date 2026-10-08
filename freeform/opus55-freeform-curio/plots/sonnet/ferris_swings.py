"""A frozen chain-swing carousel: striped canopy, hollow mast with a ladder, a scaffold stair around it, swinging seats."""
import math
from mc import B

NAME = "The Chain Swing Carousel"
KIND = "structure"

CX, CZ = 5, 5


def stripe(x, z):
    a = math.atan2(z - CZ, x - CX)
    return 14 if int((a + math.pi) / (math.pi / 6)) % 2 == 0 else 0


def build(c):
    # the paving: a round floor of stone brick and quartz
    for x in range(0, 11):
        for z in range(0, 11):
            d = math.hypot(x - CX, z - CZ)
            if d <= 5.2:
                c.set(x, -1, z, B.QUARTZ if int(d) % 2 == 0 else B.STONEBRICK, 0)
    # the house at the foot of the mast: two low rooms, a ladder through the floors
    c.fill(3, 0, 3, 7, 5, 7, B.STAINED_CLAY, 14)
    for x in (3, 7):
        for z in (3, 7):
            c.fill(x, 0, z, x, 5, z, B.LOG2, 1)
    c.fill(4, 0, 4, 6, 1, 6, B.AIR)
    c.fill(4, 3, 4, 6, 4, 6, B.AIR)
    c.fill(5, 0, 6, 5, 4, 6, B.PLANKS, 5)             # an inner post for the ladder
    c.fill(4, 5, 4, 6, 5, 6, B.AIR)
    c.set(5, 5, 6, B.PLANKS, 5)
    c.fill(5, 0, 3, 5, 1, 3, B.AIR)                  # north door
    c.set(4, 0, 4, B.CHEST, 3)
    c.set(6, 0, 4, B.CRAFTING)
    c.set(4, 3, 4, B.BOOKSHELF)
    c.set(6, 3, 6, B.BOOKSHELF)
    c.set(6, 4, 4, B.GLOWSTONE)
    # the mast: a hollow 3x3 shaft with a ladder in it, y6..14
    c.fill(4, 6, 4, 6, 14, 6, B.LOG2, 1)
    c.fill(5, 6, 5, 5, 14, 5, B.AIR)
    c.fill(6, 13, 5, 6, 14, 5, B.AIR)                # the door onto the canopy
    for y in range(0, 14):
        c.set(5, y, 5, B.LADDER, 2)
    c.set(5, 2, 5, B.LADDER, 2)
    c.set(5, 5, 5, B.LADDER, 2)
    # the canopy: a striped disc, y12, radius 5
    for x in range(0, 11):
        for z in range(0, 11):
            d = math.hypot(x - CX, z - CZ)
            if d <= 5.0:
                c.set(x, 12, z, B.WOOL, stripe(x, z))
                if d > 4.0:
                    c.set(x, 13, z, B.FENCE) if (x + z) % 2 == 0 else None
    # restore the mast through the canopy
    c.fill(4, 12, 4, 6, 12, 6, B.LOG2, 1)
    c.fill(6, 13, 5, 6, 14, 5, B.AIR)
    c.set(5, 12, 5, B.AIR)
    # the hat and spire
    c.fill(4, 15, 4, 6, 15, 6, B.WOOL, 14)
    c.fill(4, 15, 5, 6, 15, 5, B.WOOL, 14)
    c.fill(5, 16, 4, 5, 16, 6, B.WOOL, 0)
    c.fill(4, 16, 5, 6, 16, 5, B.WOOL, 0)
    c.fill(5, 17, 5, 5, 19, 5, B.FENCE)
    c.set(5, 20, 5, B.GOLD_BLOCK)
    c.set(6, 19, 5, B.WOOL, 14)
    c.set(7, 19, 5, B.WOOL, 14)
    # the scaffold stair around the house: 24 cells, two to a level
    ring = [(x, 8) for x in range(2, 9)] + [(8, z) for z in range(7, 1, -1)] + [(x, 2) for x in range(7, 1, -1)] \
        + [(2, z) for z in range(3, 8)]
    for k, (x, z) in enumerate(ring):
        y = k // 2
        nx, nz = ring[(k + 1) % len(ring)]
        d = 0 if nx > x else 1 if nx < x else 2 if nz > z else 3
        if k % 2 == 0:
            c.set(x, y, z, B.PLANKS, 1)
        else:
            c.set(x, y, z, B.SPRUCE_STAIRS, d)
        if (x, z) != (5, 2) and (x, z) != (5, 8):
            for yy in range(0, y):
                c.set(x, yy, z, B.FENCE)
        if k >= 17:
            c.set(x, 12, z, B.AIR)
            c.set(x, 13, z, B.AIR)
    # seats on chains, frozen mid-spin
    seats = [((9, 5), 4, 0), ((1, 5), 7, 1), ((5, 1), 6, 3), ((5, 9), 3, 2),
             ((9, 3), 8, 0), ((3, 1), 5, 3), ((9, 7), 6, 0), ((1, 7), 8, 1)]
    for (x, z), y, d in seats:
        c.set(x, y, z, B.OAK_STAIRS, d)
        c.fill(x, y + 1, z, x, 11, z, B.FENCE)
        c.set(x, 12, z, B.WOOL, stripe(x, z))
