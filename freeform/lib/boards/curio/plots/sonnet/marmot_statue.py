"""A whistling marmot statue standing on a terraced rock; hollow belly, a burrow below, fur steps winding up its flank."""
import math
from mc import B

NAME = "The Standing Marmot"
KIND = "sculpture"


def ell(x, y, z, cx, cy, cz, rx, ry, rz):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2 <= 1.0


def fur(x, y, z):
    h = (x * 7 + y * 13 + z * 5) % 9
    return 7 if h == 0 else 1 if h < 3 else 12


def build(c):
    # rock terraces: stone, cobble and moss
    for k, (x0, x1, z0, z1) in enumerate(((0, 10, 0, 10), (1, 9, 1, 9), (2, 8, 2, 8), (3, 7, 3, 7))):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                v = (x * 5 + z * 3 + k) % 4
                c.set(x, k, z, B.COBBLE if v else B.MOSSY)
                if k and not (x0 < x < x1 and z0 < z < z1):
                    pass
    # body parts, as a set of cells so the ledge can find the surface
    solid = {}
    def add(fn, col=None):
        for x in range(0, 11):
            for y in range(3, 23):
                for z in range(0, 11):
                    if fn(x, y, z):
                        solid[(x, y, z)] = col
    add(lambda x, y, z: ell(x, y, z, 5, 9.2, 5, 3.6, 5.4, 3.3))                      # body
    add(lambda x, y, z: ell(x, y, z, 2.6, 6.0, 4.6, 1.8, 2.6, 2.4))                  # west haunch
    add(lambda x, y, z: ell(x, y, z, 7.4, 6.0, 4.6, 1.8, 2.6, 2.4))                  # east haunch
    add(lambda x, y, z: ell(x, y, z, 5, 16.0, 5.8, 2.5, 2.6, 2.6))                   # head
    add(lambda x, y, z: ell(x, y, z, 3.1, 10.0, 7.4, 1.1, 2.3, 1.3))                 # west arm
    add(lambda x, y, z: ell(x, y, z, 6.9, 10.0, 7.4, 1.1, 2.3, 1.3))                 # east arm
    add(lambda x, y, z: ell(x, y, z, 5, 14.6, 8.6, 1.5, 1.2, 1.5))                   # snout
    add(lambda x, y, z: ell(x, y, z, 5, 4.8, 8.5, 2.2, 1.3, 1.4))                    # feet
    for (x, y, z) in solid:
        belly = z >= 7 and 4 <= x <= 6 and y < 14 or (y >= 14 and z >= 8)
        c.set(x, y, z, B.STAINED_CLAY, 0 if belly else fur(x, y, z))
    # ears, eyes, nose, teeth, whiskers
    for x in (3, 7):
        c.fill(x, 18, 5, x, 19, 5, B.STAINED_CLAY, 12)
        c.set(x, 19, 5, B.STAINED_CLAY, 6)
    c.set(4, 16, 8, B.COAL_BLOCK)
    c.set(6, 16, 8, B.COAL_BLOCK)
    c.set(5, 15, 10, B.COAL_BLOCK)
    c.set(5, 13, 9, B.QUARTZ)
    for x in (2, 3, 7, 8):
        c.set(x, 14, 9, B.IRON_BARS)
        c.set(x, 15, 9, B.IRON_BARS)
    # hollow belly: inner ellipsoid, floor at y4
    for x in range(0, 11):
        for y in range(5, 14):
            for z in range(0, 11):
                if ell(x, y, z, 5, 9.2, 5, 2.6, 4.4, 2.3):
                    c.set(x, y, z, B.AIR)
    # belly door and a back door
    c.fill(4, 5, 6, 6, 6, 9, B.AIR)
    c.fill(5, 5, 2, 5, 6, 3, B.AIR)
    # the burrow under the rock, with a ladder shaft up into the belly
    c.fill(3, 0, 3, 7, 2, 7, B.AIR)
    c.set(5, 3, 4, B.AIR)
    c.fill(5, 0, 8, 5, 1, 9, B.AIR)
    c.fill(2, 0, 5, 3, 1, 5, B.AIR)
    for y in range(0, 5):
        c.set(5, y, 4, B.LADDER, 3)
    c.fill(5, 0, 3, 5, 4, 3, B.COBBLE)
    c.set(5, 4, 4, B.LADDER, 3)
    c.set(6, 0, 6, B.HAY)
    # fur steps winding up the flank: east -> north -> west
    prev = None
    ledge = set()
    n = 40
    for i in range(0, n + 1):
        a = -math.pi * i / n
        y = 1 + int(10 * i / n + 0.5)
        found = None
        for r10 in range(80, 10, -1):
            r = r10 / 10.0
            x = int(round(5 + r * math.cos(a)))
            z = int(round(5 + r * math.sin(a)))
            if 0 <= x <= 10 and 0 <= z <= 10 and (x, y, z) in solid:
                break
            if 0 <= x <= 10 and 0 <= z <= 10 and all((x, y + k, z) not in solid and (x, y + k, z) not in ledge for k in (1, 2, 3)):
                found = (x, y, z)
        if found is None:
            found = (int(round(5 + 4 * math.cos(a))), y, int(round(5 + 4 * math.sin(a))))
        x, y, z = found
        if prev and (prev[0] != x and prev[2] != z):
            c.set(prev[0], prev[1], z, B.WOOL, 12)
            for k in (1, 2, 3):
                c.set(prev[0], prev[1] + k, z, B.AIR)
            for yy in range(0, prev[1]):
                if c.get(prev[0], yy, z)[0] == 0:
                    c.set(prev[0], yy, z, B.COBBLE)
        if prev != found:
            ledge.add(found)
            c.set(x, y, z, B.WOOL, 1 if i % 2 else 12)
            for k in (1, 2, 3):
                c.set(x, y + k, z, B.AIR)
            for yy in range(0, y):
                if c.get(x, yy, z)[0] == 0:
                    c.set(x, yy, z, B.COBBLE)
        prev = found
    # the head's wide-open whistle: a hole through the snout
    c.set(5, 14, 9, B.AIR)
    c.set(5, 14, 8, B.AIR)
