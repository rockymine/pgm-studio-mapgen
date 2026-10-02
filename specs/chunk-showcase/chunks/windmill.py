"""Windmill Farm: a tapering cobble-and-spruce windmill with four wool sails, wheat, carrot and potato plots
between water channels, a scarecrow, hay, a cart, a tool shed over a root cellar cut open on two faces, and an oak."""
from kit import Chunk

MILL_X, MILL_Z = 6, 7          # centre of the tower
HUB_Y = 10                      # sail hub height
SAIL_Z = MILL_Z + 4             # the plane the sails turn in, one block clear of the tower's south face
STONES = ("4", "98", "48", "98:2", "4")
WOOD, LOG, DARK, DARK_SLAB = "5:1", "17:1", "5:5", "126:5"
WHEAT, CARROT, POTATO = "59:7", "141:7", "142:7"


def hashed(x, y, z, options):
    return options[(x * 7 + y * 13 + z * 5) % len(options)]


def tower(c):
    mx, mz = MILL_X, MILL_Z
    for y in range(0, 4):                                                # octagonal stone drum
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                if abs(dx) == 3 and abs(dz) == 3:
                    continue
                if max(abs(dx), abs(dz)) == 3 or y == 3:
                    c.set(mx + dx, y, mz + dz, hashed(mx + dx, y, mz + dz, STONES))
    for y in range(4, 9):                                                # spruce body
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if max(abs(dx), abs(dz)) == 2:
                    c.set(mx + dx, y, mz + dz, LOG if abs(dx) == 2 and abs(dz) == 2 else WOOD)
    for dx in range(-2, 3):                                              # balcony rail on the drum's top
        c.set(mx + dx, 4, mz - 3, "85"); c.set(mx + dx, 4, mz + 3, "85")
    for dz in range(-2, 3):
        c.set(mx - 3, 4, mz + dz, "85"); c.set(mx + 3, 4, mz + dz, "85")
    c.set(mx, 0, mz + 3, "64:3"); c.set(mx, 1, mz + 3, "64:8")           # door and steps
    for dx in (-1, 0, 1):
        c.set(mx + dx, -1, mz + 4, "98")
    c.set(mx, 2, mz + 3, "102"); c.set(mx, 2, mz - 3, "102")
    for dx in (-1, 0, 1):
        c.set(mx + dx, 6, mz + 2, "102"); c.set(mx + dx, 6, mz - 2, "102")
    for dz in (-1, 0, 1):
        c.set(mx - 2, 6, mz + dz, "102"); c.set(mx + 2, 6, mz + dz, "102")
    for dx in (-1, 1):                                                   # shutters beside the door-side windows
        c.set(mx + dx, 2, mz + 3, "96:5") if False else None
    c.set(mx + 2, 0, mz + 4, "85"); c.set(mx + 2, 1, mz + 4, "85"); c.set(mx + 2, 2, mz + 4, "89")   # door lamp
    for y in (0, 1, 2):                                                  # ivy on the west and north stone
        c.set(mx - 4, y, mz, "106:8"); c.set(mx - 4, y, mz + 1, "106:8") if y else None
        c.set(mx - 1, y, mz - 4, "106:4") if y != 1 else None
    # cap: a stair pyramid with an overhang
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            c.set(mx + dx, 9, mz + dz, DARK)
    for half, y, fill in ((3, 9, False), (2, 10, False), (1, 11, True)):
        for dx in range(-half, half + 1):
            for dz in range(-half, half + 1):
                if max(abs(dx), abs(dz)) != half:
                    if fill:
                        c.set(mx + dx, y, mz + dz, DARK)
                    continue
                corner = abs(dx) == half and abs(dz) == half
                stair = "164:3" if dz == half else "164:2" if dz == -half else "164:1" if dx == half else "164:0"
                c.set(mx + dx, y, mz + dz, DARK_SLAB if corner else stair)
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            c.set(mx + dx, 10, mz + dz, DARK)
    c.set(mx, 12, mz, DARK_SLAB); c.set(mx, 13, mz, "85")
    c.set(mx + 3, 4, mz + 3, "89") if False else None


def sails(c):
    """Four log arms along the axes, each carrying two rows of wool on its trailing side."""
    x0, y0, z = MILL_X, HUB_Y, SAIL_Z
    for dz in (2, 3):
        c.set(x0, y0, MILL_Z + dz, "17:8")                               # axle through the cap
    c.set(x0, y0, z, "162:0")
    for k in range(1, 6):
        c.set(x0 + k, y0, z, "17:4"); c.set(x0 - k, y0, z, "17:4")
        c.set(x0, y0 + k, z, "17:0"); c.set(x0, y0 - k, z, "17:0")
    for k in range(2, 6):
        cloth = "35:0" if k % 2 == 0 else "35:8"
        for row in (1, 2):
            c.set(x0 + k, y0 + row, z, cloth)                            # right arm, cloth above
            c.set(x0 - k, y0 - row, z, cloth)                            # left arm, cloth below
            c.set(x0 - row, y0 + k, z, cloth)                            # up arm, cloth to the left
            c.set(x0 + row, y0 - k, z, cloth)                            # down arm, cloth to the right
    c.set(x0 + 5, y0 + 3, z, "85"); c.set(x0 - 5, y0 - 3, z, "85")      # outer rails
    c.set(x0 - 3, y0 + 5, z, "85"); c.set(x0 + 3, y0 - 5, z, "85")
    c.set(x0 + 1, y0 + 1, z, "35:14"); c.set(x0 - 1, y0 - 1, z, "35:14")


def plot_row(c, x0, x1, z, crop):
    for x in range(x0, x1 + 1):
        c.set(x, -1, z, "60:7"); c.set(x, 0, z, crop)


def channel_row(c, x0, x1, z):
    for x in range(x0, x1 + 1):
        c.set(x, -1, z, "9")


def fields(c):
    for z, crop in ((12, WHEAT), (13, WHEAT), (15, CARROT)):             # south-west plot
        plot_row(c, 0, 6, z, crop)
    channel_row(c, 0, 6, 14)
    for z, crop in ((12, POTATO), (13, CARROT), (15, WHEAT)):            # south-east plot
        plot_row(c, 10, 15, z, crop)
    channel_row(c, 10, 15, 14)
    for z in range(7, 11):                                               # east plot, by column
        for x, crop in ((11, WHEAT), (13, WHEAT), (14, CARROT), (15, POTATO)):
            c.set(x, -1, z, "60:7"); c.set(x, 0, z, crop)
        c.set(12, -1, z, "9")
    for x in range(10, 16):                                              # fence between the plots, a gate
        c.set(x, 0, 11, "107:0" if x == 12 else "85")
    for z in range(7, 11):
        c.set(10, 0, z, "85")
    for x in (0, 1, 2, 4, 5, 6):
        c.set(x, 0, 11, "85")
    for x in (7, 8, 9):                                                  # path to the mill door
        for z in range(11, 16):
            c.set(x, -1, z, "13" if (x + z) % 2 else "3:1")
    c.set(6, -1, 11, "13"); c.set(5, -1, 11, "3:1")
    # water-edge detail: a bucket-ish cauldron and a sack pile beside the path
    c.set(9, 0, 11, "118:3")
    c.set(10, 0, 11, "85")
    c.set(7, 0, 12, "35:12"); c.set(7, 0, 13, "35:0"); c.set(8, 0, 12, "35:12")


def shed_and_cellar(c):
    # cellar: a void under the shed, open on the west and north faces, reached by a ladder in the shed floor
    c.lower(0, 0, 4, 4, -5)
    for x0, z0, x1, z1 in ((0, 0, 4, 0), (0, 4, 4, 4), (0, 1, 0, 3), (2, 1, 4, 3), (1, 2, 1, 3)):
        c.roof(x0, z0, x1, z1, -2, 0)
    for y in range(-5, 0):
        c.set(1, y, 1, "65:5")
    c.box(3, -5, 1, 4, -4, 1, "17:0")                                    # log stack
    c.box(2, -5, 3, 4, -5, 3, "47"); c.box(4, -4, 3, 4, -3, 3, "47"); c.set(2, -4, 3, "47"); c.set(3, -4, 3, "47")
    c.box(0, -5, 2, 0, -4, 2, "170:0"); c.set(0, -5, 3, "170:0")         # hay
    c.set(2, -5, 2, "54:3"); c.set(3, -5, 2, "118:3"); c.set(4, -5, 2, "58")
    c.set(3, -3, 1, "89"); c.set(1, -5, 3, "30"); c.set(2, -3, 4, "30")
    c.set(0, -5, 4, "35:12"); c.set(1, -5, 4, "54:2")
    # shed above
    for x in range(0, 5):
        for z in range(0, 5):
            if (x, z) != (1, 1):
                c.set(x, -1, z, WOOD)
    for y in (0, 1, 2):
        for x in range(0, 5):
            c.set(x, y, 0, WOOD); c.set(x, y, 4, WOOD)
        for z in range(1, 4):
            c.set(0, y, z, WOOD); c.set(4, y, z, WOOD)
    for x, z in ((0, 0), (4, 0), (0, 4), (4, 4)):
        c.box(x, 0, z, x, 2, z, LOG)
    c.set(2, 0, 4, "64:3"); c.set(2, 1, 4, "64:8")
    c.set(1, 1, 4, "102"); c.set(3, 1, 4, "102"); c.set(4, 1, 2, "102"); c.set(1, 1, 0, "102"); c.set(3, 1, 0, "102")
    for x in range(0, 5):
        c.set(x, 3, 0, "134:2"); c.set(x, 4, 1, "134:2"); c.set(x, 5, 2, "126:1")
        c.set(x, 4, 3, "134:3"); c.set(x, 3, 4, "134:3")
    for x in range(1, 4):
        c.set(x, 3, 1, WOOD); c.set(x, 3, 3, WOOD)
    for x in (0, 4):
        c.set(x, 3, 1, WOOD); c.set(x, 3, 2, WOOD); c.set(x, 4, 2, WOOD); c.set(x, 3, 3, WOOD)
    # inside: a bench, tools, a lamp
    c.set(2, 0, 2, "58"); c.set(3, 0, 3, "54:2"); c.set(3, 2, 2, "85") if False else None
    c.set(2, 2, 2, "85"); c.set(2, 1, 2, "89") if False else None
    # outside: stacked hay, a barrel and a pitchfork rack on the shed's east wall
    c.set(5, 0, 1, "170:0"); c.set(5, 1, 1, "170:0"); c.set(5, 0, 2, "170:4") if False else None
    c.set(5, 0, 3, "17:0"); c.set(5, 1, 3, "17:0")
    c.set(6, 0, 1, "170:0"); c.set(5, 0, 4, "35:12")
    c.set(0, 0, 5, "85"); c.set(0, 1, 5, "85")


def yard(c):
    c.prop("hand-cart", 10, 0, 1)
    c.set(9, 0, 3, "170:4"); c.set(9, 1, 3, "170:4"); c.set(9, 0, 4, "170:0")
    c.prop("scarecrow", 13, 1, 8, 0)
    c.set(13, 0, 8, "85")
    c.set(14, 0, 5, "37"); c.set(15, 0, 5, "38:4"); c.set(14, 0, 4, "38:5")   # flower bed
    c.set(4, 0, 3, "37"); c.set(5, 0, 3, "38:5"); c.set(6, 0, 3, "175:0") if False else None
    # well near the tower's north side
    c.prop("well", 8, 0, 1)
    # stepping stones to the shed
    for x, z in ((5, 5), (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (1, 7)):
        c.set(x, -1, z, "3:1") if False else None


def build():
    c = Chunk("windmill", "Windmill Farm", "grass",
              "A tapering windmill with four wool sails over wheat, carrot and potato plots, a scarecrow, a cart and a root cellar.")
    tower(c)
    sails(c)
    fields(c)
    shed_and_cellar(c)
    yard(c)
    c.tree(12, 5, "tiny-oak-3")
    c.boulder(3, 9, 2, "round")
    c.cover([(0, 0), (16, 0), (16, 11), (0, 11)], coverage=0.45, fernShare=0.1, flowerShare=0.25, tallShare=0.3)
    return c
