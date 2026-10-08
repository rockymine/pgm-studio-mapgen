"""A grassy hillock cellar with giant cheese wheels stacked on its crown, climbed wheel by wheel."""
import math
from mc import B

NAME = "The Cheese Wheel Cellar"
KIND = "structure"


def wheel(c, cx, cz, r, y0, y1):
    """A cheese wheel: yellow clay, orange rind round the rim, yellow wool top with dimples."""
    for x in range(0, 11):
        for z in range(0, 11):
            d = math.hypot(x - cx, z - cz)
            if d <= r:
                rim = d > r - 0.7
                for y in range(y0, y1 + 1):
                    c.set(x, y, z, B.STAINED_CLAY, 1 if rim else 4)
                c.set(x, y1, z, B.WOOL, 4)
                if rim:
                    c.set(x, y1, z, B.STAINED_CLAY, 1)
                elif (x * 7 + z * 3) % 5 == 0:
                    c.set(x, y1, z, B.STAINED_CLAY, 1)
                if rim and y0 < y1:
                    c.set(x, y0, z, B.STAINED_CLAY, 1)


def build(c):
    # the hillock: four terraces, front face flush at z=10
    for k in range(4):
        x0, x1, z0 = k, 10 - k, 2 + k
        c.fill(x0, 0, z0, x1, k, 10, B.DIRT, 0)
    for k in range(4):
        x0, x1, z0 = k, 10 - k, 2 + k
        c.fill(x0, k, z0, x1, k, 10, B.GRASS)
    # the front face is stone brick under the grass
    for k in range(4):
        c.fill(k, 0, 10, 10 - k, k, 10, B.STONEBRICK, 0)
    # sprinkle: mossy stones and flowers on the terraces
    c.set(1, 2, 8, B.FLOWER, 6)
    c.set(9, 2, 8, B.FLOWER, 4)
    c.set(2, 3, 5, B.FLOWER, 0)
    c.set(8, 3, 6, B.FLOWER, 7)
    # the cellar: x3..7, z5..9, y0..1
    c.fill(3, 0, 5, 7, 1, 9, B.AIR)
    c.fill(5, 0, 10, 5, 1, 10, B.AIR)                # south door
    c.fill(4, 0, 10, 4, 2, 10, B.LOG, 1)
    c.fill(6, 0, 10, 6, 2, 10, B.LOG, 1)
    c.fill(4, 2, 10, 6, 2, 10, B.LOG, 1)
    c.fill(0, 0, 7, 2, 1, 7, B.AIR)                  # west tunnel
    c.fill(2, 0, 7, 2, 1, 7, B.AIR)
    c.set(5, 2, 7, B.GLOWSTONE)
    c.fill(8, 0, 7, 8, 1, 9, B.AIR)
    # inside: a maze of cheese-wheel stacks
    blocked = [(4, 8), (5, 8), (6, 8), (4, 7), (4, 6), (6, 6), (7, 6)]
    for (x, z) in blocked:
        c.fill(x, 0, z, x, 1, z, B.STAINED_CLAY, 4)
        c.set(x, 1, z, B.WOOL, 4)
        if (x + z) % 3 == 0:
            c.set(x, 0, z, B.STAINED_CLAY, 1)
    c.set(3, 0, 5, B.CRAFTING)
    c.set(7, 0, 5, B.CHEST, 4)
    c.set(5, 2, 5, B.GLOWSTONE)
    c.set(3, 2, 7, B.GLOWSTONE)
    # the crown: wheels
    wheel(c, 5, 7, 2.6, 4, 5)
    wheel(c, 5, 7, 1.7, 6, 7)
    wheel(c, 5, 7, 0.8, 8, 9)
    # a wedge cut out of the bottom wheel's rim on the north-east, a nook behind the wheels
    for x in range(3, 8):
        for z in range(5, 10):
            ang = math.degrees(math.atan2(z - 7, x - 5))
            if 12 < abs(ang) < 70 and math.hypot(x - 5, z - 7) > 1.8 and x > 5 and z < 7:
                c.fill(x, 4, z, x, 5, z, B.AIR)
    # steps up: stairs on the mound crown and on each wheel ring
    c.set(5, 4, 10, B.SPRUCE_STAIRS, 3)
    c.set(3, 4, 9, B.SPRUCE_STAIRS, 0)
    c.set(5, 6, 9, B.SPRUCE_STAIRS, 3)
    c.set(3, 6, 7, B.SPRUCE_STAIRS, 0)
    c.set(4, 8, 7, B.SPRUCE_STAIRS, 0)
    c.set(6, 8, 7, B.SPRUCE_STAIRS, 1)
    # the crown's steps: a stair to the first wheel from the front terrace
    # pennant on the top wheel
    c.fill(5, 10, 7, 5, 12, 7, B.FENCE)
    c.set(6, 12, 7, B.WOOL, 14)
    c.set(7, 12, 7, B.WOOL, 14)
