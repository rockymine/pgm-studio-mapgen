"""The Igloo Inn: three snow domes, the biggest the inn's hall, joined by low tunnels, with blue-ice windows, a
packed-ice stair up the smallest dome and across to the top of the hall, and the inn's sign on a pole."""
import math

from mc import B

NAME = "The Igloo Inn"
KIND = "house"

SNOW = (B.SNOW, 0)
ICE = (B.PACKED_ICE, 0)
DOMES = [  # cx, cz, radius, height
    (4.5, 6.0, 4.6, 6),
    (8.5, 1.8, 2.4, 3),
    (1.6, 1.6, 2.0, 3),
]


def dome_top(d, r, h):
    return h * math.sqrt(max(0.0, 1 - (d / r) ** 2))


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.SNOW)
    for cx, cz, r, h in DOMES:
        for x in range(11):
            for z in range(11):
                d = math.hypot(x - cx, z - cz)
                if d > r:
                    continue
                t = int(round(dome_top(d, r, h)))
                ti = int(round(dome_top(d, r - 1.6, h - 1))) if d <= r - 1.6 else -1
                for y in range(0, t + 1):
                    hollow = y < ti
                    if hollow:
                        c.set(x, y, z, B.AIR)
                    elif c.get(x, y, z)[0] == 0:
                        c.set(x, y, z, *SNOW)
                if ti >= 0:
                    c.set(x, -1, z, B.WOOL, 12 if (x + z) % 2 else 14)   # rugs on the floor
    # tunnels: the hall to each small dome, two blocks high, and doors out to the street
    for x, z in [(6, 3), (7, 3), (7, 2), (3, 3), (2, 3), (2, 2)]:
        c.set(x, 0, z, B.AIR); c.set(x, 1, z, B.AIR)
    for x, z in [(10, 2)]:                                       # a back door out of the east dome
        c.set(x, 0, z, B.AIR); c.set(x, 1, z, B.AIR)
    # the hall's entrance: a snow porch with a bend, so the street never sees in
    for x in range(6, 10):
        for z in range(8, 11):
            for y in range(0, 3):
                c.set(x, y, z, *SNOW)
    for x, z in [(5, 9), (6, 9), (7, 9), (8, 9), (8, 10)]:
        c.set(x, 0, z, B.AIR); c.set(x, 1, z, B.AIR)
    for x, y, z in [(0, 2, 6), (9, 2, 6), (4, 2, 10), (4, 3, 2)]:    # blue-ice windows
        if c.get(x, y, z)[0] == B.SNOW:
            c.set(x, y, z, B.ICE)
    # the packed-ice stair: up the small north-east dome, then across a ridge of ice to the hall's crown
    for x, y, z in [(10, 0, 4), (10, 1, 3), (9, 2, 4), (8, 3, 4), (8, 4, 5), (7, 5, 5), (6, 6, 5)]:
        c.set(x, y, z, *ICE)
        c.set(x, y + 1, z, B.AIR) if c.get(x, y + 1, z)[0] == B.SNOW else None
    c.set(4, 7, 6, B.SNOW_LAYER, 0)
    # the inn's sign on a pole by the door, and lanterns
    c.fill(9, 3, 10, 9, 4, 10, B.FENCE)                           # the sign pole on the porch
    c.set(9, 5, 10, B.WOOL, 14)
    c.set(9, 5, 9, B.WOOL, 4)
    c.set(2, 0, 9, B.FENCE)
    c.set(2, 1, 9, B.GLOWSTONE)
    # sledges and a woodpile
    c.fill(0, 0, 8, 0, 0, 10, B.WOOD_SLAB, 1)
    c.fill(9, 0, 6, 10, 1, 7, B.LOG, 1 | 4)
