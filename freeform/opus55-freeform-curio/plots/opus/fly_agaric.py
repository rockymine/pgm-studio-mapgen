"""The Fairy Ring: a ring of fly agaric toadstools round a great one, each cap red with white spots. The ring's caps
climb a block at a time round the circle, the last beside a door in the great cap's dome: a red room up in the
mushroom, its floor the cap's underside, where nobody on the street can see."""
import math

from mc import B

NAME = "The Fairy Ring"
KIND = "sculpture"

C = 5
STEM = (100, 10)                                                 # mushroom stem
CAP = (100, 14)                                                  # red cap, all sides
SPOT = (B.WOOL, 0)
BIG_UNDER, BIG_R = 8, 3.6


def spot(x, y, z):
    return (x * 3 + z * 5 + y * 7) % 6 == 0


def toadstool(c, cx, cz, top, r):
    """A small toadstool: a stem up to its cap, a flat red cap with a domed middle."""
    for y in range(0, top):
        c.set(cx, y, cz, *STEM)
    for x in range(int(cx - r), int(cx + r) + 1):
        for z in range(int(cz - r), int(cz + r) + 1):
            if 0 <= x <= 10 and 0 <= z <= 10 and math.hypot(x - cx, z - cz) <= r:
                if c.get(x, top, z)[0] == 0:
                    c.set(x, top, z, *(SPOT if spot(x, top, z) else CAP))


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    # the great toadstool: a thick stem, a cap with a hollow dome over its underside
    for x in range(11):
        for z in range(11):
            d = math.hypot(x - C, z - C)
            if d <= 1.2:
                for y in range(0, BIG_UNDER):
                    c.set(x, y, z, *STEM)
            if d <= BIG_R:
                c.set(x, BIG_UNDER, z, *STEM)                    # the gills underneath, pale
                top = BIG_UNDER + 1 + int(round(2.6 * math.sqrt(max(0.0, 1 - (d / (BIG_R + 0.4)) ** 2))))
                for y in range(BIG_UNDER + 1, top + 1):
                    shell = d > BIG_R - 1.2 or y == top
                    if shell:
                        c.set(x, y, z, *(SPOT if spot(x, y, z) else CAP))
    # the ring: eight toadstools stepping up round the circle, a block higher each
    ring = []
    for k in range(8):
        a = math.radians(200 + k * 41)
        ring.append((C + 4.6 * math.cos(a), C + 4.6 * math.sin(a), k))
    for cx, cz, top in ring:
        toadstool(c, int(round(cx)), int(round(cz)), top, 1.3)
    # the door in the dome, beside the last cap
    lx, lz, lt = ring[-1]
    a = math.atan2(lz - C, lx - C)
    for rr in (2.0, 2.6, 3.0, 3.4):
        dx, dz = int(round(C + rr * math.cos(a))), int(round(C + rr * math.sin(a)))
        c.set(dx, BIG_UNDER + 1, dz, B.AIR)
        c.set(dx, BIG_UNDER + 2, dz, B.AIR)
    # little toadstools and grass in the ring
    for x, z in ((2, 5), (8, 6), (5, 8), (6, 2)):
        c.set(x, 0, z, B.RED_MUSHROOM)
    for x, z in ((3, 3), (7, 7), (3, 7), (7, 3)):
        c.set(x, 0, z, B.TALLGRASS, 1)
