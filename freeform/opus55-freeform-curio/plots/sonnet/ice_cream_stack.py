"""A waffle cone with three scoops and a cherry: a ladder up the cone into the hollow first scoop, a sprinkle ledge round the rest."""
import math
from mc import B

NAME = "The Cone of Scoops"
KIND = "sculpture"

CX, CZ = 5, 5
SPHERES = [(9.0, 4.5), (15.0, 3.6), (19.0, 2.6)]        # centre y, radius: pink, mint, chocolate
COLORS = [6, 5, 12]


def dist3(x, y, z, cy):
    return math.sqrt((x - CX) ** 2 + (y - cy) ** 2 + (z - CZ) ** 2)


def rprof(y):
    best = 0.0
    for cy, r in SPHERES:
        v = r * r - (y - cy) ** 2
        if v > 0:
            best = max(best, math.sqrt(v))
    return best


def build(c):
    # the cone: y0..7, radius 1.6 -> 3.4, waffle checks
    for y in range(0, 8):
        r = 1.6 + 0.26 * y
        for x in range(0, 11):
            for z in range(0, 11):
                d = math.hypot(x - CX, z - CZ)
                if d <= r:
                    col = 12 if (x + z + y) % 3 == 0 else 1
                    c.set(x, y, z, B.STAINED_CLAY, col)
    # rim ring at the top of the cone
    for x in range(0, 11):
        for z in range(0, 11):
            d = math.hypot(x - CX, z - CZ)
            if 3.0 < d <= 4.1:
                c.set(x, 7, z, B.STAINED_CLAY, 4)
    # the scoops
    for i, (cy, r) in enumerate(SPHERES):
        for x in range(0, 11):
            for z in range(0, 11):
                for y in range(0, 24):
                    if dist3(x, y, z, cy) <= r:
                        c.set(x, y, z, B.WOOL, COLORS[i])
    # drips: the pink scoop runs over the rim
    for (x, z) in ((2, 5), (8, 4), (5, 8), (4, 2)):
        c.set(x, 6, z, B.WOOL, 6)
        c.set(x, 5, z, B.WOOL, 6) if (x + z) % 2 else None
    # the cherry and stalk
    for (dx, dy, dz) in ((0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, -1, 0), (0, 1, 0)):
        c.set(CX + dx, 22 + dy, CZ + dz, B.WOOL, 14)
    # hollow first scoop: cavity r3.5, floor at y6
    cy, r = SPHERES[0]
    for x in range(0, 11):
        for z in range(0, 11):
            for y in range(7, 14):
                if dist3(x, y, z, cy) <= r - 1.0:
                    c.set(x, y, z, B.AIR)
    # hollow second scoop: a bowl with floor at y14
    cy, r = SPHERES[1]
    for x in range(0, 11):
        for z in range(0, 11):
            for y in range(14, 20):
                if dist3(x, y, z, cy) <= r - 1.0:
                    c.set(x, y, z, B.AIR)
    # the cone's shaft and ladder, and its door
    c.fill(5, 0, 5, 5, 6, 5, B.AIR)
    c.fill(5, 0, 6, 5, 1, 6, B.AIR)
    for y in range(0, 7):
        c.set(5, y, 5, B.LADDER, 3)
    # the sprinkle ledge, rising round the scoops
    cells = []
    i = 0
    while True:
        y = 6 + i * 0.3
        if y > 18.4:
            break
        a = i * 0.15
        rr = rprof(y) + 0.6
        rr = max(rr, 3.6)
        x = int(round(CX + rr * math.cos(a)))
        z = int(round(CZ + rr * math.sin(a)))
        yy = int(y)
        if cells and (cells[-1][0], cells[-1][2]) == (x, z):
            if yy > cells[-1][1]:
                cells[-1] = (x, yy, z)
            i += 1
            continue
        if cells and cells[-1][0] != x and cells[-1][2] != z:
            cells.append((cells[-1][0], cells[-1][1], z))
        cells.append((x, yy, z))
        i += 1
    for k, (x, y, z) in enumerate(cells):
        c.set(x, y, z, B.STAINED_CLAY, [14, 4, 3, 5, 10, 6][k % 6])
        # headroom
        for dy in (1, 2, 3):
            if c.get(x, y + dy, z)[0] == B.WOOL:
                c.set(x, y + dy, z, B.AIR)
    # the door from the first scoop's cavity to the ledge start
    x0, y0, z0 = cells[0]
    ang = 0.0
    for d in range(2, 6):
        xx = CX + d
        for yy in (7, 8):
            c.set(xx, yy, CZ, B.AIR)
        c.set(xx, 6, CZ, B.STAINED_CLAY, 4) if c.get(xx, 6, CZ)[0] == B.AIR else None
