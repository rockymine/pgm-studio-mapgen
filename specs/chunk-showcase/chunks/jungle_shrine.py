"""A lost jungle shrine: a stepped temple of mossy stone with a staircase to a golden idol, braziers, vines and
jungle growth, a lily moat crossed by a plank bridge, and the treasure vault beneath cut open on the west face."""
from kit import Chunk

BRICKS = ("98:1", "98", "98:1", "48", "98:2", "98:1", "4", "98:1")


def mossy(x, y, z):
    return BRICKS[(x * 7 + y * 5 + z * 3) % len(BRICKS)]


def tier(c, x0, z0, x1, z1, y0, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                c.set(x, y, z, mossy(x, y, z))
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            c.set(x, y1, z, "109:7" if z == z0 else "109:6")
    for z in range(z0 + 1, z1):
        c.set(x0, y1, z, "109:4"); c.set(x1, y1, z, "109:5")


def vine(c, x, y_top, z, bits, length):
    for y in range(y_top, y_top - length, -1):
        c.set(x, y, z, f"106:{bits}")


def build():
    c = Chunk("jungle-shrine", "Lost Jungle Shrine", "forest",
              "A stepped temple of mossy stone with a golden idol, braziers and vines, a lily moat and a "
              "treasure vault cut open beneath it.")
    # the temple: three tiers set back to the north and a shrine house on top
    tier(c, 3, 2, 12, 11, 0, 1)
    tier(c, 4, 3, 11, 9, 2, 3)
    tier(c, 5, 3, 10, 7, 4, 5)
    for y in range(6, 9):
        for x in range(6, 10):
            for z in range(3, 7):
                if x in (6, 9) or z in (3, 6):
                    c.set(x, y, z, mossy(x, y, z))
    for x in (6, 9):
        for z in (3, 6):
            c.box(x, 6, z, x, 8, z, "98:3")
    c.box(5, 9, 2, 10, 9, 7, "44:5")
    c.box(6, 9, 3, 9, 9, 6, "98:3")
    c.box(7, 10, 4, 8, 10, 5, "44:5")
    for x in (7, 8):
        c.set(x, 6, 6, None); c.set(x, 7, 6, None)
        c.set(x, 8, 6, "109:6")
    # the idol and its glow
    c.set(7, 6, 4, "98:3"); c.set(7, 7, 4, "41"); c.set(8, 6, 4, "98:3"); c.set(8, 7, 4, "41")
    c.set(7, 8, 4, "169"); c.set(8, 8, 4, "169")
    c.set(6, 7, 4, "160:5"); c.set(9, 7, 4, "160:5"); c.set(6, 7, 5, "160:5"); c.set(9, 7, 5, "160:5")
    # the staircase up the south face, on a solid flight
    for step in range(6):
        z = 12 - step
        for x in (7, 8):
            for y in range(0, step):
                c.set(x, y, z, mossy(x, y, z))
            c.set(x, step, z, "109:3")
            for y in range(step + 1, 6):
                c.set(x, y, z, None)
        c.set(6, step, z, "109:4" if step else "98:1"); c.set(9, step, z, "109:5" if step else "98:1")
        for y in range(0, step):
            c.set(6, y, z, mossy(6, y, z)); c.set(9, y, z, mossy(9, y, z))
    for x in (6, 9):
        c.set(x, 1, 12, "89")
    # braziers on the tiers' corners: netherrack burning
    for x, y, z in ((4, 4, 3), (11, 4, 3), (4, 4, 9), (11, 4, 9), (5, 6, 7), (10, 6, 7)):
        c.set(x, y - 1, z, "87"); c.set(x, y, z, "51")
    # vines down the sides
    for z in (3, 6, 9, 10):
        vine(c, 2, 1, z, 8, 2)
        vine(c, 13, 1, z, 2, 2)
    for z in (4, 7):
        vine(c, 3, 3, z, 8, 2)
        vine(c, 12, 3, z, 2, 2)
    for z in (4, 6):
        vine(c, 4, 5, z, 8, 2)
        vine(c, 11, 5, z, 2, 2)
    # jungle growth: leaf bushes and melons at the foot of the temple
    for x, y, z in ((1, 0, 1), (2, 0, 1), (1, 1, 1), (13, 0, 1), (14, 0, 1), (14, 0, 2), (14, 1, 1),
                    (2, 0, 12), (1, 0, 11), (13, 0, 11), (14, 0, 11), (14, 1, 11), (12, 2, 2), (3, 2, 11),
                    (4, 4, 10), (11, 4, 10), (12, 2, 11)):
        c.set(x, y, z, "18:7")
    c.set(1, 0, 4, "103"); c.set(14, 0, 6, "103"); c.set(14, 0, 8, "86:3")
    # a lily moat across the front, bridged in planks
    c.lower(1, 13, 14, 14, -1)
    for x in range(1, 15):
        for z in (13, 14):
            c.set(x, -1, z, "9")
            if x in (7, 8, 9):
                c.set(x, 0, z, "5:3")
            elif (x * 3 + z) % 4 == 0:
                c.set(x, 0, z, "111")
    for x in (6, 10):
        c.set(x, 0, 13, "190"); c.set(x, 0, 14, "190"); c.set(x, 1, 13, "50:5")
    for x in (7, 8, 9):
        c.set(x, -1, 15, "3:1" if x % 2 else "13")

    # the vault beneath, open on the west face: gold, chests, a dart trap, cobwebs, a sea-lantern glow
    c.lower(0, 4, 5, 9, -9)
    c.roof(0, 4, 5, 9, -4, 0)
    c.box(0, -10, 4, 5, -10, 9, "98:1")
    c.box(5, -9, 4, 5, -5, 9, "98:3")
    c.set(4, -9, 6, "41"); c.set(4, -9, 7, "41"); c.set(4, -8, 6, "41"); c.set(3, -9, 7, "57")
    c.set(4, -9, 5, "54:4"); c.set(4, -9, 8, "54:4")
    c.set(2, -9, 4, "144:1"); c.set(1, -9, 9, "144:1")
    c.set(5, -6, 6, "23:4"); c.set(5, -6, 7, "23:4")
    c.set(3, -5, 6, "169")
    c.set(1, -5, 5, "30"); c.set(2, -9, 8, "30"); c.set(0, -6, 8, "30")
    c.set(1, -9, 6, "70")

    c.tree(12, 12, "jungle-4")
    c.boulder(3, 12, 3, "round")
    c.cover([(0, 0), (16, 0), (16, 2), (0, 2)], coverage=0.6, fernShare=0.6, tallShare=0.2, flowerShare=0.1)
    c.cover([(0, 2), (3, 2), (3, 13), (0, 13)], coverage=0.6, fernShare=0.6, tallShare=0.2)
    c.cover([(13, 2), (16, 2), (16, 13), (13, 13)], coverage=0.6, fernShare=0.6, tallShare=0.2)
    c.cover([(3, 12), (13, 12), (13, 13), (3, 13)], coverage=0.5, fernShare=0.5)
    return c
