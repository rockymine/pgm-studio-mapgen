"""A lost jungle shrine, given room: a broader stepped temple climbs in three tiers to the idol's house, a long
staircase runs down to a lily moat bridged in planks, jungle hummocks crowd the corners, and the treasure vault
lies under the temple's west flank, cut open on the west face."""
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
        c.set(x, y1, z0, "109:7"); c.set(x, y1, z1, "109:6")
    for z in range(z0 + 1, z1):
        c.set(x0, y1, z, "109:4"); c.set(x1, y1, z, "109:5")


def vine(c, x, y_top, z, bits, length):
    for y in range(y_top, y_top - length, -1):
        c.set(x, y, z, f"106:{bits}")


def bush(c, x, z, y=0, tall=False):
    for dx, dz in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)):
        c.set(x + dx, y, z + dz, "18:7")
    c.set(x, y + 1, z, "18:7")
    if tall:
        c.set(x + 1, y + 1, z, "18:7"); c.set(x, y + 2, z, "18:7")


def build():
    c = Chunk("jungle-shrine", "Lost Jungle Shrine", "forest",
              "A stepped temple of mossy stone climbing to a golden idol, braziers and vines, a lily moat and "
              "jungle hummocks, and a treasure vault cut open beneath it.", size=32)
    # landform: hummocks crowding the corners, a dell for the moat
    c.hill(4, 4, 6, 3)
    c.hill(28, 5, 5, 2)
    c.hill(27, 26, 6, 3)
    c.hill(3, 27, 4, 2)

    # the temple: three tiers and the idol's house
    tier(c, 9, 5, 22, 17, 0, 2)
    tier(c, 10, 6, 21, 14, 3, 5)
    tier(c, 11, 6, 20, 12, 6, 8)
    house = (13, 18, 6, 10)
    for y in range(9, 13):
        for x in range(house[0], house[1] + 1):
            for z in range(house[2], house[3] + 1):
                if x in house[:2] or z in house[2:]:
                    c.set(x, y, z, mossy(x, y, z))
    for x in house[:2]:
        for z in house[2:]:
            c.box(x, 9, z, x, 12, z, "98:3")
    c.box(12, 13, 5, 19, 13, 11, "44:5")
    c.box(13, 13, 6, 18, 13, 10, "98:3")
    c.box(14, 14, 7, 17, 14, 9, "44:5")
    c.box(15, 15, 8, 16, 15, 8, "98:3")
    for x in (15, 16):
        for y in (9, 10, 11):
            c.set(x, y, 10, None)
        c.set(x, 12, 10, "109:6")
    # the idol and its glow
    c.box(15, 9, 7, 16, 9, 7, "98:3"); c.box(15, 10, 7, 16, 11, 7, "41")
    c.set(15, 12, 7, "169"); c.set(16, 12, 7, "169")
    for z in (7, 8):
        c.set(13, 10, z, "160:5"); c.set(18, 10, z, "160:5")

    # the staircase down the south face, on a solid flight, with balustrades
    for step in range(9):
        z = 21 - step
        for x in (15, 16):
            for y in range(0, step):
                c.set(x, y, z, mossy(x, y, z))
            c.set(x, step, z, "109:3")
            for y in range(step + 1, 9):
                c.set(x, y, z, None)
        for x in (14, 17):
            for y in range(0, step):
                c.set(x, y, z, mossy(x, y, z))
            c.set(x, step, z, "139:1")
    for x in (14, 17):
        c.set(x, 1, 21, "89")
    # braziers on the tiers' corners and beside the landing
    for x, y, z in ((10, 3, 6), (21, 3, 6), (10, 3, 14), (21, 3, 14), (12, 9, 12), (19, 9, 12)):
        c.set(x, y, z, "87"); c.set(x, y + 1, z, "51")

    # vines down every tier
    for z in (6, 9, 12, 15):
        vine(c, 8, 2, z, 8, 2)
        vine(c, 23, 2, z, 2, 2)
    for z in (7, 10, 13):
        vine(c, 9, 5, z, 8, 2)
        vine(c, 22, 5, z, 2, 2)
    for z in (7, 9, 11):
        vine(c, 10, 8, z, 8, 3)
        vine(c, 21, 8, z, 2, 3)
    for x in (12, 18):
        vine(c, x, 11, 5, 1, 2)

    # jungle growth: leaf bushes, melons and a pumpkin at the temple's foot and on the hummocks
    for x, z, tall in ((6, 12, True), (25, 11, False), (7, 19, False), (24, 19, True), (12, 23, False),
                       (20, 23, False), (5, 6, False), (29, 15, True)):
        bush(c, x, z, tall=tall)
    c.set(8, 0, 9, "103"); c.set(24, 0, 15, "103"); c.set(23, 0, 8, "86:3")

    # the lily moat across the front, bridged in planks
    c.lower(4, 24, 27, 26, -1)
    c.basin(4, 25, 2, -1)
    c.basin(27, 25, 2, -1)
    for x in range(2, 30):
        for z in range(23, 28):
            near_end = (x < 4 and abs(z - 25) + (4 - x) <= 2) or (x > 27 and abs(z - 25) + (x - 27) <= 2)
            if (4 <= x <= 27 and 24 <= z <= 26) or near_end:
                c.set(x, -1, z, "9")
                if 15 <= x <= 17 and 24 <= z <= 26:
                    c.set(x, 0, z, "5:3")
                elif (x * 3 + z) % 4 == 0:
                    c.set(x, 0, z, "111")
    for x in (14, 18):
        for z in (24, 26):
            c.set(x, 0, z, "190")
        c.set(x, 1, 24, "50:5"); c.set(x, 1, 26, "50:5")
    for z in range(22, 24):
        for x in (15, 16, 17):
            c.set(x, -1, z, "4" if (x + z) % 2 else "48")
    for z in range(27, 32):
        for x in (15, 16, 17):
            c.set(x, -1, z, "3:1" if (x + z) % 2 else "13")

    # the vault beneath the temple's west flank, open on the west face
    c.lower(0, 8, 12, 14, -10)
    c.roof(0, 8, 12, 14, -4, 0)
    c.box(0, -11, 8, 12, -11, 14, "98:1")
    for x in (3, 7):
        c.box(x, -10, 8, x, -5, 8, "98:3"); c.box(x, -10, 14, x, -5, 14, "98:3")
    c.box(12, -10, 8, 12, -5, 14, "98:3")
    c.set(11, -10, 10, "41"); c.set(11, -10, 11, "41"); c.set(11, -9, 10, "41"); c.set(10, -10, 11, "57")
    c.set(11, -9, 11, "41")
    c.set(11, -10, 9, "54:4"); c.set(11, -10, 13, "54:4")
    c.set(5, -10, 9, "144:1"); c.set(2, -10, 13, "144:1"); c.set(8, -10, 12, "144:1")
    c.set(12, -7, 10, "23:4"); c.set(12, -7, 12, "23:4")
    c.set(6, -5, 11, "169"); c.set(10, -5, 11, "169")
    c.set(1, -5, 9, "30"); c.set(4, -10, 12, "30"); c.set(0, -7, 13, "30"); c.set(9, -6, 8, "30")
    c.set(6, -10, 11, "70"); c.set(8, -10, 10, "70")

    c.tree(27, 26, "jungle-4")
    c.boulder(9, 29, 3, "round")
    c.cover([(0, 0), (32, 0), (32, 5), (0, 5)], coverage=0.6, fernShare=0.6, tallShare=0.2, flowerShare=0.1)
    c.cover([(0, 5), (9, 5), (9, 23), (0, 23)], coverage=0.6, fernShare=0.6, tallShare=0.2)
    c.cover([(23, 5), (32, 5), (32, 23), (23, 23)], coverage=0.6, fernShare=0.6, tallShare=0.2)
    c.cover([(0, 27), (14, 27), (14, 32), (0, 32)], coverage=0.55, fernShare=0.5)
    c.cover([(18, 27), (32, 27), (32, 32), (18, 32)], coverage=0.55, fernShare=0.5)
    c.cover([(9, 18), (14, 18), (14, 23), (9, 23)], coverage=0.5, fernShare=0.5)
    c.cover([(18, 18), (23, 18), (23, 23), (18, 23)], coverage=0.5, fernShare=0.5)
    return c
