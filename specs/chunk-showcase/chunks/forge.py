"""A village blacksmith: an open timber-framed smithy under a spruce gable, a brick hearth with a lava bed and a
chimney through the roof, anvil, quench trough, furnaces, a tool wall, coal and ore deliveries, and a cellar of
stock cut open on the west face."""
from kit import Chunk

LOG = "17:1"            # spruce
BEAM_X, BEAM_Z = "17:5", "17:9"
PLANK = "5:1"


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
    if (z1 - z0 + 1) % 2:
        for x in range(x0, x1 + 1):
            c.set(x, y0 + rows, z0 + rows, "126:1")
    else:
        for x in range(x0, x1 + 1):
            c.set(x, y0 + rows - 1 + 1, z0 + rows - 1, "126:1")
            c.set(x, y0 + rows - 1 + 1, z0 + rows, "126:1")


def build():
    c = Chunk("forge", "The Smithy", "grass",
              "An open timber smithy with a lava hearth and chimney, anvil, quench trough, tool wall, coal "
              "deliveries and a stock cellar below.")

    # floor and frame: x 2..10, z 2..9
    for x in range(2, 11):
        for z in range(2, 10):
            c.set(x, -1, z, "4" if (x * 7 + z * 3) % 5 else "1:5")
    for x in (2, 6, 10):
        for z in (2, 9):
            c.box(x, 0, z, x, 3, z, LOG)
    c.box(2, 4, 2, 10, 4, 2, BEAM_X)
    c.box(2, 4, 9, 10, 4, 9, BEAM_X)
    for x in (2, 6, 10):
        c.box(x, 4, 3, x, 4, 8, BEAM_Z)
    # a low back wall of cobble with a window of bars, and a half wall to the west
    c.box(3, 0, 2, 9, 1, 2, "4")
    c.set(4, 1, 2, "98:1"); c.set(9, 0, 2, "48")
    c.box(3, 2, 2, 5, 2, 2, "101")
    c.box(2, 0, 3, 2, 0, 8, "4")
    c.set(2, 0, 5, "107:1")
    roof(c, 1, 11, 1, 10, 5)

    # hearth: a brick box with a lava bed, a hood and a chimney up through the ridge
    c.box(7, 0, 3, 9, 0, 5, "45")
    c.box(7, 1, 3, 9, 1, 5, "45")
    c.set(8, 1, 4, "11"); c.set(8, 1, 5, "108:2")
    c.set(7, 2, 4, "44:12"); c.set(9, 2, 4, "44:12"); c.set(8, 2, 5, "108:7")
    c.box(7, 2, 3, 9, 3, 3, "45")
    for y in range(4, 12):
        c.set(8, y, 3, "45")
    c.set(8, 12, 3, "139")
    c.set(7, 3, 3, "108:1"); c.set(9, 3, 3, "108:0")
    c.set(6, 0, 4, "35:12"); c.set(6, 1, 4, "126:9")             # bellows
    # anvil, quench, grinding stone, workbench
    c.set(5, 0, 6, "145:1")
    c.set(5, 0, 8, "118:3"); c.set(6, 0, 8, "118:3")
    c.set(3, 0, 5, "188"); c.set(3, 1, 5, "44:8")
    c.set(3, 0, 7, "58"); c.set(3, 1, 7, "148")
    c.set(3, 0, 3, "61:3"); c.set(4, 0, 3, "61:3")
    c.set(5, 0, 3, "54:3"); c.set(5, 1, 3, "147")
    # the tool wall: levers hung on the back wall
    for x in (6, 7):
        c.set(x, 1, 3, None)
    c.set(6, 1, 3, "69:3")
    # coal and ore heaps by the hearth
    c.set(9, 0, 7, "173"); c.set(10, 0, 7, "173"); c.set(9, 0, 8, "173"); c.set(9, 1, 7, "44:8")
    c.set(10, 0, 8, "15"); c.set(10, 1, 8, "15")
    # a hanging sign on the front post
    c.set(6, 2, 10, "68:3")
    c.set(6, 3, 10, "89")

    # the yard: a trough, a hitching rail, a cart with ore, a wheel leaning on the wall
    c.box(12, 0, 4, 14, 0, 4, "126:9")
    c.box(12, 0, 5, 14, 0, 5, "9")
    c.box(12, 0, 6, 14, 0, 6, "126:9")
    c.set(11, 0, 5, "126:9"); c.set(15, 0, 5, "126:9")
    c.box(12, 0, 8, 12, 1, 8, "85"); c.box(14, 0, 8, 14, 1, 8, "85"); c.box(12, 1, 8, 14, 1, 8, "85")
    c.prop("hand-cart", 10, 0, 11, 0)
    c.set(12, 1, 13, "15"); c.set(11, 1, 13, "16")
    c.set(1, 0, 9, "17:9"); c.set(1, 0, 8, "17:9")
    c.prop("barrels", 11, 0, 1, 0)
    c.prop("lantern-post", 4, 0, 11, 0)

    # a path in from the south bridge, and from the east
    for z in range(10, 16):
        for x in (7, 8, 9):
            c.set(x, -1, z, "13" if (x + z) % 4 else "4")
    for x in range(11, 16):
        c.set(x, -1, 7, "13" if x % 3 else "4")

    # the stock cellar: open on the west face, down a ladder from beside the cart
    c.lower(0, 11, 4, 14, -8)
    c.roof(0, 11, 4, 14, -3, 0)
    c.roof(0, 11, 0, 14, -3, 0)
    c.box(0, -9, 11, 4, -9, 14, "5:1")
    c.box(1, -8, 14, 1, -6, 14, "17:1")
    c.box(4, -8, 11, 4, -6, 11, "17:1")
    c.set(1, -8, 11, "42"); c.set(2, -8, 11, "42"); c.set(1, -7, 11, "42")
    c.set(3, -8, 11, "41")
    c.set(2, -8, 14, "54:2"); c.set(3, -8, 14, "54:2")
    c.set(4, -8, 13, "173"); c.set(4, -8, 12, "15"); c.set(4, -7, 13, "16")
    c.set(2, -4, 12, "89")

    c.tree(1, 1, "tiny-spruce-1")
    c.tree(14, 14, "small-olive-2")
    c.tree(5, 12, "small-olive-1")
    c.boulder(13, 2, 3, "angular")
    c.boulder(13, 10, 3)
    c.cover([(0, 10), (7, 10), (7, 16), (0, 16)], coverage=0.45, flowerShare=0.3)
    c.cover([(11, 9), (16, 9), (16, 16), (11, 16)], coverage=0.4, flowerShare=0.2)
    c.cover([(11, 0), (16, 0), (16, 4), (11, 4)], coverage=0.35)
    return c
