"""The Watermill: a stone mill house with a spruce gable roof and a great wooden wheel turning in a millrace along
its east side. The wheel's paddles step up to the eaves; inside, a ladder climbs to the grain loft and a hatch onto
the roof."""
import math

from mc import B

NAME = "The Watermill"
KIND = "house"

STONE, BRICK, MOSSY = (B.COBBLE, 0), (B.STONEBRICK, 0), (B.MOSSY, 0)
SPRUCE, SPRUCE_LOG = (B.PLANKS, 1), (B.LOG, 1)
ROOF = B.SPRUCE_STAIRS
X0, X1, Z0, Z1 = 0, 6, 1, 9
TOP = 5


def build(c):
    # the mill house, cobble below and stone brick above, spruce posts at its corners
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            ex, ez = x in (X0, X1), z in (Z0, Z1)
            if not (ex or ez):
                c.set(x, -1, z, *SPRUCE)
                continue
            for y in range(0, TOP + 1):
                if ex and ez:
                    blk = SPRUCE_LOG
                elif y in (2, 3) and ((ez and x in (2, 4)) or (ex and z in (3, 7))):
                    blk = (B.PANE, 0)
                else:
                    blk = STONE if y < 2 else (MOSSY if (x * 3 + z + y) % 7 == 0 else BRICK)
                c.set(x, y, z, *blk)
    c.set(3, 0, Z1, B.AIR); c.set(3, 1, Z1, B.AIR)                # the door, south
    c.set(0, 0, 5, B.AIR); c.set(0, 1, 5, B.AIR)                  # and west
    # the grain loft at y 3, and a ladder up to it and on to a hatch in the roof
    for x in range(X0 + 1, X1):
        for z in range(Z0 + 1, Z1):
            if not (x == 1 and z in (2, 3)):
                c.set(x, 3, z, *SPRUCE)
    for y in range(0, 4):
        c.set(1, y, 2, B.LADDER, 3)
    c.fill(4, 4, 6, 5, 5, 7, B.HAY)                              # sacks in the loft
    # the gable roof along x, ridge over z 5
    for i in range(5):
        for x in range(X0 - 0, X1 + 1):
            c.set(x, TOP + 1 + i, Z0 - 1 + i, ROOF, 2)
            c.set(x, TOP + 1 + i, Z1 + 1 - i, ROOF, 3)
    for x in range(X0, X1 + 1):
        c.set(x, TOP + 5, 5, *SPRUCE)
    for i in range(4):
        for z in range(Z0 + 1 + i, Z1 - i):
            for x in (X0, X1):
                c.set(x, TOP + 1 + i, z, *SPRUCE)
    # the millrace: a stone channel along the east wall, still water in it
    for z in range(0, 11):
        c.set(7, 0, z, *STONE)
        c.set(10, 0, z, *STONE)
        c.set(8, 0, z, B.WATER)
        c.set(9, 0, z, B.WATER)
    # the wheel: a ring of spruce in the plane x = 8, centre at y 4, its spokes, and paddles to climb
    cz, cy, r = 5.0, 4.0, 4.2
    for z in range(0, 11):
        for y in range(0, 10):
            d = math.hypot(z - cz, y - cy)
            if r - 0.7 <= d <= r + 0.5:
                c.set(8, y, z, B.PLANKS, 0)                      # the rim, pale oak against the stone
            elif d < r - 0.7 and (abs(z - cz) < 0.5 or abs(y - cy) < 0.5 or abs(abs(z - cz) - abs(y - cy)) < 0.5):
                c.set(8, y, z, B.FENCE)                          # eight spokes
    c.set(8, 4, 5, B.LOG, 0)                                     # the hub
    c.set(7, 4, 5, B.LOG, 0 | 4)                                 # the axle into the wall
    for z, y in [(9, 1), (8, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7)]:   # paddles round the rim, a stair up its east face
        c.set(9, y, z, B.WOOD_SLAB, 1 | 8)
    c.set(9, 0, 10, *STONE)
    # the wheel's top reaches the eaves: a plank to step across onto the roof
    c.set(7, 8, 5, *SPRUCE)
    c.set(7, 9, 5, *SPRUCE)
