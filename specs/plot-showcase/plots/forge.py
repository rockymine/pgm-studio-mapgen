"""The village smithy, given room: the timber smithy stands on a low terrace under a wooded rise, its lava hearth
and chimney at the back, the yard with trough, hitching rail and ore cart opening east, steps down to the south
path, and the stock cellar cut into the west face."""
from kit import Chunk

LOG = "17:1"
BEAM_X, BEAM_Z = "17:5", "17:9"
PLANK = "5:1"
Y = 1                     # the terrace's floor course


def roof(c, x0, x1, z0, z1, y0):
    """A spruce gable running along x over z0..z1, eaves at y0, ridge slabs on top, gable ends boarded."""
    rows = (z1 - z0 + 1) // 2
    for step in range(rows):
        y = y0 + step
        for x in range(x0, x1 + 1):
            c.set(x, y, z0 + step, "134:2")
            c.set(x, y, z1 - step, "134:3")
        if step:
            for z in range(z0 + step, z1 - step + 1):
                c.set(x0 + 1, y - 1, z, PLANK)
                c.set(x1 - 1, y - 1, z, PLANK)
    for x in range(x0, x1 + 1):
        c.set(x, y0 + rows, z0 + rows, "126:1")
        if (z1 - z0 + 1) % 2 == 0:
            c.set(x, y0 + rows - 1, z0 + rows - 1, "134:2")


def smithy(c):
    x0, x1, z0, z1 = 6, 16, 5, 13
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.set(x, Y - 1, z, "4" if (x * 7 + z * 3) % 5 else "1:5")
    for x in (x0, 11, x1):
        for z in (z0, z1):
            c.box(x, Y, z, x, Y + 3, z, LOG)
    c.box(x0, Y + 4, z0, x1, Y + 4, z0, BEAM_X)
    c.box(x0, Y + 4, z1, x1, Y + 4, z1, BEAM_X)
    for x in (x0, 11, x1):
        c.box(x, Y + 4, z0 + 1, x, Y + 4, z1 - 1, BEAM_Z)
    # back wall with a barred window, a half wall and gate to the west
    c.box(x0 + 1, Y, z0, x1 - 1, Y + 1, z0, "4")
    c.set(8, Y + 1, z0, "98:1"); c.set(15, Y, z0, "48"); c.set(12, Y + 1, z0, "48")
    c.box(7, Y + 2, z0, 10, Y + 2, z0, "101")
    c.box(x0, Y, z0 + 1, x0, Y, z1 - 1, "4")
    c.set(x0, Y, 9, "107:1")
    roof(c, x0 - 1, x1 + 1, z0 - 1, z1 + 1, Y + 5)

    # hearth, hood and chimney
    c.box(12, Y, 6, 14, Y + 1, 8, "45")
    c.set(13, Y + 1, 7, "11"); c.set(13, Y + 1, 8, "108:2")
    c.set(12, Y + 2, 7, "44:12"); c.set(14, Y + 2, 7, "44:12"); c.set(13, Y + 2, 8, "108:7")
    c.box(12, Y + 2, 6, 14, Y + 3, 6, "45")
    c.set(12, Y + 3, 6, "108:1"); c.set(14, Y + 3, 6, "108:0")
    for y in range(Y + 4, Y + 14):
        c.set(13, y, 6, "45")
    c.set(13, Y + 14, 6, "139")
    c.set(11, Y, 7, "35:12"); c.set(11, Y + 1, 7, "126:9")
    # anvil, quench, grinding stone, workbench, furnaces, a chest of ingots, the tool wall
    c.set(9, Y, 9, "145:1")
    c.set(9, Y, 11, "118:3"); c.set(10, Y, 11, "118:3")
    c.set(7, Y, 8, "188"); c.set(7, Y + 1, 8, "44:8")
    c.set(7, Y, 11, "58"); c.set(7, Y + 1, 11, "148")
    c.set(7, Y, 6, "61:3"); c.set(8, Y, 6, "61:3")
    c.set(9, Y, 6, "54:3"); c.set(9, Y + 1, 6, "147")
    c.set(10, Y + 1, 6, "69:3")
    # coal and ore by the hearth
    c.set(14, Y, 10, "173"); c.set(15, Y, 10, "173"); c.set(14, Y, 11, "173"); c.set(14, Y + 1, 10, "44:8")
    c.set(15, Y, 12, "15"); c.set(15, Y + 1, 12, "15")
    # the hanging sign on the front post
    c.set(11, Y + 2, 14, "68:3"); c.set(11, Y + 3, 14, "89")


def build():
    c = Chunk("forge", "The Smithy", "grass",
              "An open timber smithy on a terrace under a wooded rise, a lava hearth and chimney, anvil and "
              "quench, a yard with trough and ore cart, and a stock cellar below.", size=32)
    # landform: the terrace, a wooded rise behind it, a gentle swell in the south-east
    c.raise_(4, 3, 19, 15, Y)
    c.hill(7, 2, 7, 3)
    c.hill(26, 26, 6, 2)
    smithy(c)
    # steps down from the terrace to the south path, and onto the east path
    for x in (15, 16, 17):
        c.set(x, 0, 16, "67:3")
    for z in (15, 16, 17):
        c.set(20, 0, z, "67:1")

    # the yard
    c.box(22, 0, 8, 25, 0, 8, "126:9")
    c.box(22, 0, 9, 25, 0, 9, "9")
    c.box(22, 0, 10, 25, 0, 10, "126:9")
    c.set(21, 0, 9, "126:9"); c.set(26, 0, 9, "126:9")
    c.box(22, 0, 12, 22, 1, 12, "85"); c.box(25, 0, 12, 25, 1, 12, "85"); c.box(22, 1, 12, 25, 1, 12, "85")
    c.prop("hand-cart", 22, 0, 19, 0)
    c.set(24, 1, 21, "15"); c.set(23, 1, 21, "16")
    c.set(21, 0, 5, "17:9"); c.set(21, 0, 6, "17:9")
    c.prop("barrels", 26, 0, 3, 0)
    c.prop("lantern-post", 13, 0, 20, 0)

    # paths: south from the bridge to the steps, east from the yard to the bridge
    for z in range(17, 32):
        for x in (15, 16, 17):
            c.set(x, -1, z, "13" if (x + z) % 4 else "4")
    for x in range(21, 32):
        for z in (15, 16, 17):
            c.set(x, -1, z, "13" if (x * 3 + z) % 5 else "4")

    # the stock cellar: open on the west face, down a hatch and ladder
    c.lower(0, 19, 6, 26, -8)
    c.roof(0, 19, 5, 26, -3, 0)
    c.roof(6, 20, 6, 26, -3, 0)
    for y in range(-8, -1):
        c.set(6, y, 19, "65:4")
    c.set(6, -1, 19, "96:8")
    c.box(0, -9, 19, 6, -9, 26, "5:1")
    for z in (19, 26):
        c.box(2, -8, z, 2, -4, z, "17:1"); c.box(5, -8, z, 5, -4, z, "17:1")
    c.set(1, -8, 20, "42"); c.set(2, -8, 20, "42"); c.set(1, -7, 20, "42")
    c.set(3, -8, 20, "41")
    c.set(3, -8, 26, "54:2"); c.set(4, -8, 26, "54:2")
    c.set(5, -8, 23, "173"); c.set(5, -8, 22, "15"); c.set(5, -7, 23, "16")
    c.set(3, -4, 23, "89")

    c.tree(3, 3, "tiny-spruce-1")
    c.tree(27, 26, "small-olive-2")
    c.tree(10, 25, "small-olive-1")
    c.boulder(27, 6, 3, "angular")
    c.boulder(24, 13, 3)
    c.cover([(0, 16), (14, 16), (14, 32), (0, 32)], coverage=0.45, flowerShare=0.3)
    c.cover([(19, 18), (32, 18), (32, 32), (19, 32)], coverage=0.4, flowerShare=0.2)
    c.cover([(0, 0), (19, 0), (19, 3), (4, 3), (4, 16), (0, 16)], coverage=0.4, fernShare=0.3)
    c.cover([(20, 0), (32, 0), (32, 14), (20, 14)], coverage=0.3)
    return c
