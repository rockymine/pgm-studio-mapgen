"""A chapel and its churchyard: a mossy stone nave under a dark-oak roof, a bell tower with a spire, a fenced
graveyard of mixed headstones, one grave freshly dug, a dead oak, pumpkins, and the coffins under the graves
cut open on the east face."""
from kit import Chunk

WALL = ("98", "98", "98:1", "98:2", "98", "4", "98:1")
ROOF_N, ROOF_S = "164:3", "164:2"          # unused names kept short below


def stone(x, y, z):
    return WALL[(x * 5 + y * 3 + z * 7) % len(WALL)]


def nave(c):
    x0, x1, z0, z1 = 1, 7, 1, 8
    for y in range(0, 5):
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                c.set(x, y, z, stone(x, y, z))
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                c.set(x, y, z, stone(x, y, z))
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            c.set(x, -1, z, "98" if (x + z) % 2 else "1:6")
    # buttresses and tall windows down both long sides
    for z in (2, 5, 7):
        c.set(0, 0, z, "109:1"); c.set(8, 0, z, "109:0")
    for z in (3, 4, 6):
        c.box(x0, 1, z, x0, 3, z, "160:5" if z == 4 else "102")
        c.box(x1, 1, z, x1, 3, z, "160:11" if z == 4 else "102")
    # roof along z: dark oak, ridge at x 4
    for step in range(4):
        y = 5 + step
        for z in range(z0 - 1, z1 + 1):
            c.set(x0 - 1 + step, y, z, "164:0")
            c.set(x1 + 1 - step, y, z, "164:1")
        for z in (z0, z1):
            for x in range(x0 + step, x1 - step + 1):
                c.set(x, y - 1 if step else 4, z, stone(x, y, z))
    for z in range(z0 - 1, z1 + 1):
        c.set(4, 8, z, "126:5")
    for z in (z0,):
        c.box(2, 5, z, 6, 5, z, "98"); c.box(3, 6, z, 5, 6, z, "98"); c.set(4, 7, z, "98:3")
    # inside: pews, an altar, candles of glowstone
    for z in (3, 4, 5, 6):
        c.set(2, 0, z, "134:3"); c.set(3, 0, z, "134:3"); c.set(5, 0, z, "134:3"); c.set(6, 0, z, "134:3")
    c.box(3, 0, 2, 5, 0, 2, "155:2"); c.set(4, 1, 2, "140")
    c.set(2, 1, 2, "89"); c.set(6, 1, 2, "89")


def tower(c):
    """A 3 x 3 bell tower at the front, an open belfry, and a dark-oak spire with a cross."""
    x0, x1, z0, z1 = 3, 5, 8, 10
    top = 13
    for y in range(0, top + 1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = x in (x0, x1) or z in (z0, z1)
                corner = x in (x0, x1) and z in (z0, z1)
                if not edge:
                    continue
                if 10 <= y <= 11 and not corner:
                    continue
                c.set(x, y, z, stone(x, y, z))
    c.set(4, 0, 10, "193:1"); c.set(4, 1, 10, "193:8")         # spruce door facing south
    c.set(4, 0, 8, None); c.set(4, 1, 8, None)
    c.set(4, 3, 10, "160:14"); c.set(4, 4, 10, "68:3")
    c.set(4, 6, 10, "102"); c.set(4, 6, 8, "102"); c.set(3, 6, 9, "102"); c.set(5, 6, 9, "102")
    c.set(4, 11, 9, "188"); c.set(4, 10, 9, "41")              # the bell
    c.box(x0 - 1, 12, z0 - 1, x1 + 1, 12, z1 + 1, "44:13")
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.set(x, 12, z, "98"); c.set(x, 13, z, "98:3" if (x + z) % 2 else "98")
    y = top + 1
    for z in range(z0, z1 + 1):
        c.set(3, y, z, "164:0"); c.set(5, y, z, "164:1")
    c.set(4, y, 8, "164:3"); c.set(4, y, 10, "164:2")
    for dy in range(1, 5):
        c.set(4, y + dy - 1, 9, "5:5")
    c.set(4, y + 1, 8, "164:7"); c.set(4, y + 1, 10, "164:6"); c.set(3, y + 1, 9, "164:4"); c.set(5, y + 1, 9, "164:5")
    c.set(4, y + 4, 9, "139"); c.set(4, y + 5, 9, "139"); c.set(4, y + 6, 9, "139")
    c.set(4, y + 5, 8, "77:4"); c.set(4, y + 5, 10, "77:3")


def headstone(c, x, z, kind):
    """A grave at (x, z): a stone at its head (north) and a mound running south."""
    c.set(x, -1, z + 1, "3:2"); c.set(x, -1, z + 2, "3:1")
    if kind == 0:
        c.set(x, 0, z, "139"); c.set(x, 1, z, "44:0")
    elif kind == 1:
        c.set(x, 0, z, "109:3")
    elif kind == 2:
        c.set(x, 0, z, "98:1"); c.set(x, 0, z + 1, "68:3")
    elif kind == 3:
        c.set(x, 0, z, "139:1"); c.set(x, 1, z, "139:1")
        c.set(x, 1, z - 0, "139:1")
    else:
        c.set(x, 0, z, "44:5"); c.set(x, 0, z + 1, "140")
    # the coffin under it
    c.box(x, -4, z, x, -4, z + 2, "5:5")
    c.set(x, -3, z + 1, "144:1")


def build():
    c = Chunk("graveyard", "Chapel and Churchyard", "grass",
              "A mossy chapel with a bell tower and spire, a fenced churchyard, an open grave, a dead oak, and "
              "the coffins beneath cut open on the east face.")
    nave(c)
    tower(c)

    # churchyard fence of nether brick with a gate on the path
    for x in range(9, 16):
        c.set(x, 0, 0 + 1, "113")
        c.set(x, 0, 13, "113")
    for z in range(1, 14):
        c.set(9, 0, z, "113")
    c.set(9, 0, 8, "107:1")
    for z in range(1, 14):
        c.set(15, 0, z, "113")
    c.set(15, 0, 8, "107:3")
    for x in (9, 15):
        for z in (1, 13):
            c.set(x, 0, z, "139:1"); c.set(x, 1, z, "89" if (x, z) == (9, 13) else "50:5")

    kinds = [0, 1, 2, 3, 4, 2, 1, 0]
    spots = [(11, 2), (13, 2), (11, 6), (13, 6), (11, 9), (13, 9), (12, 4), (14, 4)]
    for index, (x, z) in enumerate(spots[:6]):
        headstone(c, x, z, kinds[index])
    # a freshly dug grave with its spoil heap and a shovel
    c.set(14, -1, 10, None); c.set(14, -1, 11, None)
    c.lower(14, 10, 14, 11, -1)
    c.set(14, 0, 9, "109:3")
    c.set(13, 0, 11, "3:1"); c.set(13, 0, 12, "3:1"); c.set(13, 1, 12, "78:3")
    c.set(12, 0, 12, "17:0"); c.set(12, 1, 12, "69:5")

    # the dead oak: a bare trunk with crooked limbs
    for y in range(0, 6):
        c.set(10, y, 11, "17:12")
    for x, y, z in ((11, 4, 11), (12, 5, 11), (12, 6, 10), (9, 5, 11), (8, 6, 12), (10, 6, 10), (10, 7, 9),
                    (11, 6, 12), (9, 3, 12)):
        c.set(x, y, z, "17:12")
    c.set(12, 4, 11, "106:2"); c.set(8, 5, 12, "30")

    # pumpkins, lanterns, a bench, cobwebs
    c.set(6, 0, 11, "86:0"); c.set(7, 0, 12, "91:0"); c.set(2, 0, 11, "86:1")
    c.set(1, 0, 13, "85"); c.set(1, 1, 13, "85"); c.set(1, 2, 13, "89")
    c.prop("park-bench", 2, 0, 12)
    c.set(1, 4, 1, "30"); c.set(7, 4, 8, "30"); c.set(5, 7, 10, "30")

    # path from the south bridge to the tower door and the churchyard gate
    for z in range(11, 16):
        for x in (7, 8):
            c.set(x, -1, z, "13" if (x + z) % 3 else "4")
    for x in range(4, 9):
        c.set(x, -1, 11, "13" if x % 2 else "4")
    for z in range(8, 11):
        c.set(8, -1, z, "4"); c.set(7, -1, z, "13")

    # the burial gallery under the graves, open on the east face
    c.lower(13, 2, 15, 12, -6)
    c.roof(13, 2, 15, 12, -3, 0)
    c.box(13, -7, 2, 15, -7, 12, "98:1")
    for z in range(2, 13, 2):
        c.set(14, -6, z, "144:1")
    c.set(14, -6, 3, "5:5"); c.set(14, -6, 5, "5:5"); c.set(15, -6, 7, "54:4"); c.set(14, -4, 7, "89")
    c.set(13, -6, 9, "30"); c.set(15, -4, 4, "30"); c.set(14, -6, 11, "48")

    c.tree(4, 13, "small-olive-3")
    c.boulder(12, 14, 2, "cairn")
    c.cover([(0, 9), (3, 9), (3, 16), (0, 16)], coverage=0.4, flowerShare=0.1)
    c.cover([(10, 2), (15, 2), (15, 13), (10, 13)], coverage=0.3, flowerShare=0.15, deadBushShare=0.2)
    return c
