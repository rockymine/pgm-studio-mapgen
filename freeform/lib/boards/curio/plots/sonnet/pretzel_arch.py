"""A colossal pretzel lying flat on salt crystal huts: climb the quartz ramp, walk the dough ribbons, hide in the huts."""
import math
from mc import B

NAME = "The Pretzel Knot"
KIND = "sculpture"

R = 1.25                  # dough tube radius
Y0 = 5.6                  # height of the dough's centreline


def P(u, v):
    return (u, Y0, v)


def centreline():
    pts = []
    for cu in (3.7, 6.3):
        for i in range(0, 100):
            a = i * 2 * math.pi / 100
            pts.append(P(cu + 2.5 * math.cos(a), 3.4 + 2.5 * math.sin(a)))
    for (u0, v0, u1, v1) in ((8.4, 9.6, 4.6, 5.6), (1.6, 9.6, 5.4, 5.6)):
        for i in range(0, 50):
            t = i / 49
            pts.append(P(u0 + (u1 - u0) * t, v0 + (v1 - v0) * t))
    return pts


def build(c):
    # the dough
    cells = set()
    for (px, py, pz) in centreline():
        for x in range(int(px) - 2, int(px) + 4):
            for y in range(int(py) - 2, int(py) + 4):
                for z in range(int(pz) - 2, int(pz) + 4):
                    if 0 <= x <= 10 and 0 <= z <= 10 and 0 <= y <= 22:
                        if (x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 <= R * R:
                            cells.add((x, y, z))
    for (x, y, z) in cells:
        h = (x * 31 + y * 17 + z * 7) % 7
        c.set(x, y, z, B.STAINED_CLAY, 12 if h < 2 else 1)
    # salt on the top of the dough
    for (x, y, z) in sorted(cells):
        if (x * 5 + y * 11 + z * 3) % 5 == 0 and (x, y + 1, z) not in cells:
            c.set(x, y + 1, z, B.QUARTZ, 0) if c.get(x, y + 1, z)[0] == 0 else None
    # pillars of salt under the dough
    for (x, y, z) in sorted(cells):
        if y == 4 and (x * 3 + z * 5) % 7 == 0:
            for yy in range(0, 4):
                if c.get(x, yy, z)[0] == 0:
                    c.set(x, yy, z, B.QUARTZ, 0)
    # the quartz ramp up the east edge to the right lobe
    for k in range(0, 7):
        c.fill(10, 0, 10 - k, 10, k - 1, 10 - k, B.QUARTZ, 0) if k else None
        c.set(10, k, 10 - k, B.QUARTZ_STAIRS if hasattr(B, "QUARTZ_STAIRS") else 156, 3)
    # crystal hut north-west
    c.fill(0, 0, 0, 4, 3, 4, B.QUARTZ, 0)
    c.fill(1, 0, 1, 3, 2, 3, B.AIR)
    c.fill(2, 0, 4, 2, 1, 4, B.AIR)
    c.set(2, 2, 2, B.GLOWSTONE)
    # crystal hut south-west
    c.fill(0, 0, 6, 4, 3, 10, B.QUARTZ, 0)
    c.fill(1, 0, 7, 3, 2, 9, B.AIR)
    c.fill(4, 0, 8, 4, 1, 8, B.AIR)
    c.fill(0, 0, 8, 0, 1, 8, B.AIR)
    c.set(2, 2, 8, B.GLOWSTONE)
    # chiselled and pillar quartz on the hut faces for texture
    for (x, y, z) in ((0, 1, 1), (4, 1, 3), (4, 2, 0), (0, 2, 4), (0, 1, 7), (4, 2, 9), (2, 3, 0), (2, 3, 10)):
        c.set(x, y, z, B.QUARTZ, 1) if c.get(x, y, z)[0] == B.QUARTZ else None
    # salt crystals in the yard
    for (x, z, h) in ((6, 9, 2), (7, 10, 3), (8, 9, 1), (6, 7, 1), (9, 6, 2)):
        c.fill(x, 0, z, x, h - 1, z, B.QUARTZ, 0)
