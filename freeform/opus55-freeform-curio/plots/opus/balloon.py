"""The Hot-Air Balloon: a wicker basket moored to the grass on four ropes, its striped envelope swelling above. A
ladder climbs the burner's iron mast from the basket through the envelope's mouth to a platform inside it, a room
of coloured light where nobody on the street can see."""
import math

from mc import B

NAME = "The Hot-Air Balloon"
KIND = "structure"

C = 5
WICKER, RIM = (B.PLANKS, 1), (B.LOG, 1)
MAST = (B.IRON_BLOCK, 0)
STRIPES = [(B.WOOL, 14), (B.WOOL, 0), (B.WOOL, 4), (B.WOOL, 0)]
CY, RXZ, RY = 14.0, 5.2, 6.4                                    # the envelope: centre height and radii
FLOOR = 9


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    # the basket, two high, a rim of logs, a door in its south side
    for x in range(3, 8):
        for z in range(3, 8):
            edge = x in (3, 7) or z in (3, 7)
            c.set(x, -1, z, *WICKER)
            if edge:
                c.set(x, 0, z, *WICKER)
                c.set(x, 1, z, *RIM)
    c.set(5, 0, 7, B.AIR); c.set(5, 1, 7, B.AIR)
    # the burner's mast from the basket floor to the platform, and the ladder up its north face
    for y in range(0, FLOOR + 2):
        c.set(C, y, C, *MAST)
    for y in range(0, FLOOR + 2):
        c.set(C, y, C - 1, B.LADDER, 2)
    c.set(C, FLOOR + 2, C, B.GLOWSTONE)                          # the burner's flame
    # the envelope: an ellipsoid shell of vertical stripes, open in a mouth round the mast at its foot
    for x in range(11):
        for z in range(11):
            for y in range(FLOOR - 1, 23):
                d = math.sqrt(((x - C) / RXZ) ** 2 + ((z - C) / RXZ) ** 2 + ((y - CY) / RY) ** 2)
                inner = math.sqrt(((x - C) / (RXZ - 1.7)) ** 2 + ((z - C) / (RXZ - 1.7)) ** 2 + ((y - CY) / (RY - 1.7)) ** 2)
                if d <= 1.0 and inner > 1.0:
                    mouth = y <= FLOOR and math.hypot(x - C, z - C) <= 1.6
                    if not mouth:
                        k = int((math.atan2(z - C, x - C) + math.pi) / (2 * math.pi) * 12) % 4
                        c.set(x, y, z, *STRIPES[k])
    # the platform inside, round the mast, with a gap for the ladder
    for x in range(11):
        for z in range(11):
            if math.hypot(x - C, z - C) <= 4.6 and c.get(x, FLOOR, z)[0] in (0,):
                if (x, z) != (C, C - 1):
                    c.set(x, FLOOR, z, B.PLANKS, 0)
    # the mooring ropes from the basket's corners out to stakes, and sandbags
    for (bx, bz), (sx, sz) in (((3, 3), (0, 0)), ((7, 3), (10, 0)), ((3, 7), (0, 10)), ((7, 7), (10, 10))):
        c.set(sx, 0, sz, B.FENCE)
        for y in range(2, FLOOR - 1):
            c.set(bx, y, bz, B.FENCE)                            # the rigging up to the envelope
    for x, z in ((2, 5), (8, 5), (5, 2)):
        c.set(x, 0, z, B.WOOL, 12)
        c.set(x, 1, z, B.WOOL, 12) if x == 2 else None
