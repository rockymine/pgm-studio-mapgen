"""The Ibex on its Crag: a pinnacle of banded grey rock, a ledge winding up round it twice to the top, where an ibex
stands with its horns swept back. Halfway up, the ledge passes the mouth of a cave in the rock."""
import math

from mc import B

NAME = "The Ibex on its Crag"
KIND = "sculpture"

C = 5.0
TOP = 13


def rock(x, y, z):
    k = (y + (x * 2 + z) // 5) % 6
    return (B.STONE, 5) if k in (1, 4) else (B.STONE, 0) if k != 3 else (B.COBBLE, 0)


def radius(theta, y):
    """The crag's radius at a height: wide at the foot, narrowing to the top, broken by the angle."""
    base = 4.8 - 2.9 * (y / TOP) ** 1.2
    return base + 0.5 * math.sin(3 * theta + y * 0.4) + 0.3 * math.sin(5 * theta)


def path():
    """The ledge: a 4-connected walk round the crag, one block higher at every step, twice round."""
    pts = []
    y = 0
    x, z = 9, 5
    pts.append((x, z, y))
    a = 0.0
    while y < TOP - 1:
        a += 0.52
        r = 4.3 - 2.2 * (y / TOP)
        tx, tz = int(round(C + r * math.cos(a))), int(round(C + r * math.sin(a)))
        while (x, z) != (tx, tz):
            if x != tx:
                x += 1 if tx > x else -1
            else:
                z += 1 if tz > z else -1
            y += 1
            pts.append((x, z, y))
            if y >= TOP - 1:
                break
    return pts


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for x in range(11):
        for z in range(11):
            th = math.atan2(z - C, x - C)
            d = math.hypot(x - C, z - C)
            for y in range(0, TOP):
                if d <= radius(th, y):
                    c.set(x, y, z, *rock(x, y, z))
    # the ledge: each step a rock block with two of air over it, cut into the crag
    pts = path()
    for x, z, y in pts:
        if 0 <= x <= 10 and 0 <= z <= 10:
            c.set(x, y, z, *rock(x, y, z))
            for k in (1, 2, 3):                                  # headroom to step up to the next
                c.set(x, y + k, z, B.AIR) if y + k <= 23 else None
    for x, z, y in pts:                                          # anything the cut took from a step beneath goes back
        c.set(x, y, z, *rock(x, y, z))
    # the cave: a chamber in the rock beside the ledge at about half height
    mid = [p for p in pts if p[2] == 6][0]
    cx, cz = int(round(C)), int(round(C))
    c.fill(cx - 2, 6, cz - 2, cx + 2, 7, cz + 1, B.AIR)
    c.fill(cx - 2, 5, cz - 2, cx + 2, 5, cz + 1, B.STONE, 0)
    x, z = mid[0], mid[1]
    while (x, z) != (cx, cz):                                    # a passage from the ledge in to the chamber
        if z != cz:
            z += 1 if cz > z else -1
        else:
            x += 1 if cx > x else -1
        c.set(x, 6, z, B.AIR); c.set(x, 7, z, B.AIR)
        c.set(x, 5, z, B.STONE, 0)
    for x, z, y in pts:                                          # the ledge's steps stay, whatever the cave cut
        if y not in (6, 7) or (x, z) == (mid[0], mid[1]):
            c.set(x, y, z, *rock(x, y, z))
    # the summit: a flat top, and the ibex on it
    for x in range(4, 7):
        for z in range(4, 7):
            c.set(x, TOP - 1, z, B.STONE, 6)
    ib = TOP
    for x in (4, 6):                                             # legs
        for z in (4, 6):
            c.set(x, ib, z, B.FENCE)
    c.fill(4, ib + 1, 4, 6, ib + 1, 6, B.HARDENED_CLAY, 0)       # the body
    c.set(5, ib + 1, 5, B.WOOL, 12)
    c.set(7, ib + 2, 5, B.HARDENED_CLAY, 0)                      # the neck and head
    c.set(7, ib + 3, 5, B.WOOL, 12)
    c.set(6, ib + 4, 4, B.LOG, 1 | 4); c.set(6, ib + 4, 6, B.LOG, 1 | 4)   # horns swept back
    c.set(5, ib + 4, 4, B.LOG, 1 | 4); c.set(5, ib + 4, 6, B.LOG, 1 | 4)
    c.set(7, ib + 4, 5, B.WOOL, 12)
    # scree and alpine flowers round the foot
    for x, z in ((0, 2), (1, 9), (9, 0), (10, 8), (0, 6)):
        c.set(x, 0, z, B.GRAVEL)
    for x, z in ((1, 1), (9, 9), (0, 9)):
        c.set(x, 0, z, B.FLOWER, 2)
