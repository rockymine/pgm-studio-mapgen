"""A chapel and its churchyard, given room: the mossy nave and its bell tower stand on a knoll to the west, the
fenced churchyard spreads east in two rows of graves with an open grave and a dead oak, the path climbs from the
south to the tower door, and the coffins lie in a burial gallery cut open on the east face."""
from kit import Chunk

WALL = ("98", "98", "98:1", "98:2", "98", "4", "98:1")
Y = 2                      # the knoll's floor course


def stone(x, y, z):
    return WALL[(x * 5 + y * 3 + z * 7) % len(WALL)]


def nave(c):
    x0, x1, z0, z1 = 4, 12, 5, 15
    top = Y + 5
    for y in range(Y, top + 1):
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                c.set(x, y, z, stone(x, y, z))
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                c.set(x, y, z, stone(x, y, z))
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            c.set(x, Y - 1, z, "98" if (x + z) % 2 else "1:6")
    for z in (6, 9, 12, 14):
        c.set(x0 - 1, Y, z, "109:1"); c.set(x0 - 1, Y + 1, z, "139:1")
        c.set(x1 + 1, Y, z, "109:0"); c.set(x1 + 1, Y + 1, z, "139:1")
    for z in (7, 8, 10, 11, 13):
        glass = "160:5" if z == 10 else "102"
        c.box(x0, Y + 1, z, x0, Y + 4, z, glass)
        c.box(x1, Y + 1, z, x1, Y + 4, z, "160:11" if z == 10 else "102")
    # roof along z, ridge over x 8
    for step in range(5):
        y = top + 1 + step
        for z in range(z0 - 1, z1 + 2):
            c.set(x0 - 1 + step, y, z, "164:0")
            c.set(x1 + 1 - step, y, z, "164:1")
        for x in range(x0 + step, x1 - step + 1):
            if step:
                c.set(x, y - 1, z0, stone(x, y, z0))
    for z in range(z0 - 1, z1 + 2):
        c.set(8, top + 6, z, "126:5")
    c.box(7, top + 1, z0, 9, top + 1, z0, "160:14"); c.set(8, top + 2, z0, "160:14")
    # inside: pews, an altar, lights
    for z in range(8, 14):
        for x in (5, 6, 7, 9, 10, 11):
            c.set(x, Y, z, "134:3")
    c.box(7, Y, 6, 9, Y, 6, "155:2"); c.set(8, Y + 1, 6, "140")
    c.set(5, Y + 1, 6, "89"); c.set(11, Y + 1, 6, "89")


def tower(c):
    x0, x1, z0, z1 = 7, 9, 15, 17
    top = Y + 15
    for y in range(Y, top + 1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = x in (x0, x1) or z in (z0, z1)
                corner = x in (x0, x1) and z in (z0, z1)
                if not edge or (top - 5 <= y <= top - 4 and not corner):
                    continue
                c.set(x, y, z, stone(x, y, z))
    c.set(8, Y, 17, "193:1"); c.set(8, Y + 1, 17, "193:8")
    c.set(8, Y, 15, None); c.set(8, Y + 1, 15, None)
    c.set(8, Y + 3, 17, "160:14"); c.set(8, Y + 4, 17, "68:3")
    for y in (Y + 7,):
        c.set(8, y, 17, "102"); c.set(7, y, 16, "102"); c.set(9, y, 16, "102")
    c.set(8, top - 4, 16, "188"); c.set(8, top - 5, 16, "41")
    c.box(x0 - 1, top - 3, z0 - 1, x1 + 1, top - 3, z1 + 1, "44:13")
    c.box(x0, top - 3, z0, x1, top, z1, "98")
    y = top + 1
    for z in range(z0, z1 + 1):
        c.set(7, y, z, "164:0"); c.set(9, y, z, "164:1")
    c.set(8, y, 15, "164:3"); c.set(8, y, 17, "164:2")
    for dy in range(4):
        c.set(8, y + dy, 16, "5:5")
    c.set(8, y + 1, 15, "164:7"); c.set(8, y + 1, 17, "164:6"); c.set(7, y + 1, 16, "164:4"); c.set(9, y + 1, 16, "164:5")
    for dy in (4, 5, 6):
        c.set(8, y + dy, 16, "139")
    c.set(8, y + 5, 15, "77:4"); c.set(8, y + 5, 17, "77:3")


def headstone(c, x, z, kind):
    c.set(x, -1, z + 1, "3:2"); c.set(x, -1, z + 2, "3:1")
    if kind == 0:
        c.set(x, 0, z, "139"); c.set(x, 1, z, "44:0")
    elif kind == 1:
        c.set(x, 0, z, "109:3")
    elif kind == 2:
        c.set(x, 0, z, "98:1"); c.set(x, 0, z + 1, "68:3")
    elif kind == 3:
        c.set(x, 0, z, "139:1"); c.set(x, 1, z, "139:1")
    else:
        c.set(x, 0, z, "44:5"); c.set(x, 0, z + 1, "140")
    c.box(x, -4, z, x, -4, z + 2, "5:5")
    c.set(x, -3, z + 1, "144:1")


def build():
    c = Chunk("graveyard", "Chapel and Churchyard", "grass",
              "A mossy chapel and bell tower on a knoll, a fenced churchyard of graves with an open grave and a "
              "dead oak, and the coffins beneath cut open on the east face.", size=32)
    # landform: the chapel's knoll with a flat top, a soft swell south of the churchyard
    c.hill(8, 12, 12, 2)
    c.raise_(2, 3, 14, 19, Y)
    c.hill(22, 29, 5, 1)
    nave(c)
    tower(c)
    # steps from the path up the knoll to the tower door
    c.set(8, 0, 20, "109:3"); c.set(8, 1, 19, "109:3")
    c.set(7, 0, 20, "109:3"); c.set(9, 0, 20, "109:3"); c.set(7, 1, 19, "109:3"); c.set(9, 1, 19, "109:3")

    # churchyard: x 18..29, z 4..24
    x0, x1, z0, z1 = 18, 29, 4, 24
    for x in range(x0, x1 + 1):
        c.set(x, 0, z0, "113"); c.set(x, 0, z1, "113")
    for z in range(z0, z1 + 1):
        c.set(x0, 0, z, "113"); c.set(x1, 0, z, "113")
    c.set(x0, 0, 12, "107:1"); c.set(23, 0, z1, "107:0")
    for x in (x0, x1):
        for z in (z0, z1):
            c.set(x, 0, z, "139:1"); c.set(x, 1, z, "89" if (x, z) == (x0, z1) else "50:5")
    kinds = [0, 1, 2, 3, 4, 2]
    for index, (x, z) in enumerate(((21, 6), (24, 6), (27, 6), (21, 13), (24, 13), (27, 13))):
        headstone(c, x, z, kinds[index])
    # the open grave, its spoil and a shovel
    c.lower(26, 19, 26, 20, -1)
    c.set(26, 0, 18, "109:3")
    c.set(25, 0, 20, "3:1"); c.set(25, 0, 21, "3:1"); c.set(25, 1, 21, "78:3")
    c.set(24, 0, 21, "17:0"); c.set(24, 1, 21, "69:5")
    # the dead oak
    for y in range(0, 7):
        c.set(21, y, 20, "17:12")
    for x, y, z in ((22, 5, 20), (23, 6, 20), (23, 7, 19), (20, 6, 20), (19, 7, 21), (21, 7, 19), (21, 8, 18),
                    (22, 7, 21), (20, 4, 21), (24, 7, 19)):
        c.set(x, y, z, "17:12")
    c.set(23, 5, 20, "106:2"); c.set(19, 6, 21, "30")

    # pumpkins, a lantern, a bench, cobwebs
    c.set(11, Y, 18, "86:0"); c.set(12, Y, 17, "91:0"); c.set(4, Y, 17, "86:1")
    c.set(14, 0, 22, "85"); c.set(14, 1, 22, "85"); c.set(14, 2, 22, "89")
    c.prop("park-bench", 10, 0, 23)
    c.set(5, Y + 4, 6, "30"); c.set(11, Y + 5, 14, "30"); c.set(9, Y + 10, 17, "30")

    # paths: from the south bridge to the tower steps and to the churchyard's south gate
    for z in range(21, 32):
        for x in (15, 16, 17):
            c.set(x, -1, z, "13" if (x + z) % 3 else "4")
    for x in range(7, 18):
        c.set(x, -1, 21, "13" if x % 2 else "4"); c.set(x, -1, 22, "4" if x % 3 else "13")
    for x in range(17, 24):
        c.set(x, -1, 25, "13" if x % 2 else "4"); c.set(x, -1, 26, "4" if x % 3 else "13")

    # the burial gallery under the graves, open on the east face
    c.lower(20, 5, 31, 16, -6)
    c.roof(20, 5, 31, 16, -3, 0)
    c.box(20, -7, 5, 31, -7, 16, "98:1")
    for x in range(21, 31, 3):
        c.box(x, -6, 10, x, -4, 10, "98:3")
    for x, z in ((22, 7), (25, 7), (28, 7), (22, 14), (25, 14), (28, 14)):
        c.set(x, -6, z, "144:1")
    c.set(23, -6, 6, "5:5"); c.set(26, -6, 15, "5:5"); c.set(31, -6, 12, "54:4"); c.set(26, -4, 10, "89")
    c.set(20, -6, 9, "30"); c.set(30, -4, 6, "30"); c.set(29, -6, 15, "48")

    c.tree(5, 26, "small-olive-3")
    c.boulder(12, 27, 2, "cairn")
    c.cover([(0, 20), (14, 20), (14, 32), (0, 32)], coverage=0.4, flowerShare=0.12)
    c.cover([(19, 5), (29, 5), (29, 24), (19, 24)], coverage=0.3, flowerShare=0.15, deadBushShare=0.2)
    c.cover([(0, 0), (32, 0), (32, 3), (0, 3)], coverage=0.35)
    c.cover([(24, 26), (32, 26), (32, 32), (24, 32)], coverage=0.35, flowerShare=0.2)
    return c
