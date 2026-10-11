"""The Sleeping St Bernard: a dog as big as a cottage lying asleep, white with red-brown patches, its head on its
paws and the rescue barrel on its collar. Its body rises a block at a time from every side, so it can be climbed
anywhere; a hole between the shoulder blades drops into a den inside, and its chin leaves a gap over its paws."""
import math

from mc import B

NAME = "The Sleeping St Bernard"
KIND = "sculpture"

WHITE, BROWN, DARK = (B.WOOL, 0), (B.WOOL, 12), (B.WOOL, 15)
TAN = (B.HARDENED_CLAY, 0)
BARREL, HOOP = (B.PLANKS, 1), (B.GOLD_BLOCK, 0)


def body_h(x, z):
    """The body: a stepped ellipse, a block higher for every block in from its edge, five at most."""
    e = ((x - 4.0) / 4.4) ** 2 + ((z - 5.0) / 3.6) ** 2
    if e > 1:
        return -1
    inset = (1 - math.sqrt(e)) * 4.0
    return min(5, int(inset * 1.6))


def head_h(x, z):
    e = ((x - 8.3) / 2.4) ** 2 + ((z - 5.0) / 2.6) ** 2
    if e > 1:
        return -1
    return min(7, 3 + int((1 - math.sqrt(e)) * 5))


def coat(x, y, z):
    if (x - 3) ** 2 + (z - 3) ** 2 < 5 or (x - 2) ** 2 + (z - 7) ** 2 < 4 or (x - 5) ** 2 + (y - 5) ** 2 < 3:
        return BROWN
    return WHITE


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    heights = {}
    for x in range(11):
        for z in range(11):
            h = max(body_h(x, z), head_h(x, z))
            if h < 0:
                continue
            heights[(x, z)] = h
            base = 2 if head_h(x, z) >= 0 and body_h(x, z) < 0 else 0      # the chin is off the ground
            for y in range(base, h + 1):
                c.set(x, y, z, *(BROWN if head_h(x, z) >= 0 and (z in (3, 7) or y == h and z in (4, 6)) else coat(x, y, z)))
    # the face: a dark nose and closed eyes, ears hanging brown
    c.set(10, 4, 5, *DARK)
    c.set(9, 6, 4, *DARK); c.set(9, 6, 6, *DARK)
    for z in (2, 8):
        c.fill(8, 2, z, 9, 5, z, *BROWN)
    # the front paws out on the grass under the chin
    for z in (3, 4, 6, 7):
        c.fill(8, 0, z, 10, 0, z, *WHITE)
    c.fill(8, 1, 3, 10, 1, 7, B.AIR)
    # the collar and the barrel on it, under the chin
    c.fill(7, 2, 2, 7, 4, 8, B.WOOL, 14)
    c.fill(9, 1, 5, 10, 1, 5, *BARREL)
    c.set(9, 1, 4, *HOOP)
    # the tail curled round on the grass at the back
    for x, z in ((0, 8), (0, 9), (1, 9), (2, 9), (3, 9)):
        c.set(x, 0, z, *BROWN)
    # the den inside: hollowed where the body is three and more high, its way in a hole on the back
    for x in range(11):
        for z in range(11):
            walled = all(body_h(x + dx, z + dz) >= 1 or head_h(x + dx, z + dz) >= 0
                         for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)))
            if body_h(x, z) >= 2 and head_h(x, z) < 0 and walled:
                c.set(x, 0, z, B.AIR); c.set(x, 1, z, B.AIR)
                c.set(x, -1, z, B.WOOL, 14)                      # a red blanket
    hx, hz = 3, 5                                                # the hole, beside the back's highest course
    c.fill(hx + 1, 0, hz, hx + 1, 1, hz, *WHITE)                 # a pillar in the den, for the ladder
    for y in range(0, heights[(hx, hz)] + 1):
        c.set(hx, y, hz, B.LADDER, 4)
