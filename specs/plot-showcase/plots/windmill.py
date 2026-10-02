"""Windmill Farm, as a plot: a round cobble-and-spruce windmill with four wool sails on a low rise above its fields,
wheat, carrot and potato plots between water channels, a scarecrow, a well, a hay cart, a tool shed over a root
cellar cut open on two faces, an oak on its own mound and a boulder on the ridge behind."""
import math

from kit import Chunk

MILL_X, MILL_Z = 16, 12
BASE_Y = 3                       # first air course on the mill's plateau
HUB_Y = 13
SAIL_Z = MILL_Z + 5              # the plane the sails turn in, one block clear of the drum
ARM = 7
STONES = ("4", "98", "48", "98:2", "4")
WOOD, LOG, DARK, DARK_SLAB = "5:1", "17:1", "5:5", "126:5"
WHEAT, CARROT, POTATO = "59:7", "141:7", "142:7"
HILLS = ((16, 12, 9, 3), (26, 3, 6, 3), (27, 13, 4, 2))      # cx, cz, r, h as handed to c.hill


def hashed(x, y, z, options):
    return options[(x * 7 + y * 13 + z * 5) % len(options)]


def ground(x, z):
    """Top course of the terrain at a cell, as the hills below lay it."""
    top = -1
    for cx, cz, radius, height in HILLS:
        for course in range(1, height + 1):
            ring = radius * (1 - (course - 1) / height * 0.7)
            if ring >= 0.8 and math.hypot(x - cx, z - cz) <= ring:
                top = max(top, course - 1)
    return top


def base(x, z):
    return ground(x, z) + 1


def put(c, x, z, dy, block):
    c.set(x, base(x, z) + dy, z, block)


def skin(c, x, z, block):
    c.set(x, ground(x, z), z, block)


def ring(c, cx, cz, radius, y, pick, thickness=1.2):
    """A round wall course: every cell whose centre lies within `thickness` inside `radius`."""
    for x in range(int(cx - radius - 1), int(cx + radius + 2)):
        for z in range(int(cz - radius - 1), int(cz + radius + 2)):
            dist = math.hypot(x - cx, z - cz)
            if radius + 0.4 - thickness < dist <= radius + 0.4:
                c.set(x, y, z, pick(x, z))


def tower(c):
    mx, mz, b = MILL_X, MILL_Z, BASE_Y
    for dx in range(-3, 4):                                              # plank floor inside the drum
        for dz in range(-3, 4):
            if math.hypot(dx, dz) <= 3.2:
                c.set(mx + dx, b - 1, mz + dz, WOOD)
    for y in range(b, b + 4):                                            # round stone drum
        ring(c, mx, mz, 4, y, lambda x, z, y=y: hashed(x, y, z, STONES), 1.4)
    c.disc(mx, mz, 4, b + 4, "4")                                        # ledge and upper floor
    for y in range(b + 5, b + 9):                                        # spruce body
        ring(c, mx, mz, 3, y, lambda x, z: LOG if (x - mx) % 3 == 0 and (z - mz) % 3 == 0 else WOOD, 1.2)
    for y in range(b + 9, b + 12):
        ring(c, mx, mz, 2.5, y, lambda x, z: WOOD, 1.2)
    ring(c, mx, mz, 3, b + 7, lambda x, z: "17:1", 1.2)                  # belt course
    ring(c, mx, mz, 4, b + 5, lambda x, z: "85", 0.9)                    # balcony rail on the ledge
    for dx in (-1, 0, 1):
        c.set(mx + dx, b + 5, mz + 4, "85")
    c.set(mx, b, mz + 4, "64:3"); c.set(mx, b + 1, mz + 4, "64:8")      # door and steps
    for dx in (-1, 0, 1):
        skin(c, mx + dx, mz + 5, "98")
        skin(c, mx + dx, mz + 6, "98")
    for dx in (-4, 4):
        c.set(mx + dx, b + 2, mz, "102")
    c.set(mx, b + 2, mz - 4, "102")
    c.set(mx - 2, b + 2, mz + 3, "102"); c.set(mx + 2, b + 2, mz + 3, "102")
    for dx, dz in ((-3, 0), (3, 0), (0, -3), (-2, 2), (2, 2), (-2, -2), (2, -2)):
        c.set(mx + dx, b + 7, mz + dz, "102")
    for dx in (-2, 2):                                                   # door lamps
        c.set(mx + dx, b, mz + 5, "85"); c.set(mx + dx, b + 1, mz + 5, "85"); c.set(mx + dx, b + 2, mz + 5, "89")
    for y in (b, b + 1, b + 2):                                          # ivy on the north-west stone
        c.set(mx - 5, y, mz - 1, "106:8") if y else None
        c.set(mx - 2, y, mz - 5, "106:4") if y != b + 1 else None
    for lift, radius in enumerate((4.6, 3.6, 2.6, 1.6)):                 # dark cap, stepped discs
        c.disc(mx, mz, radius, b + 12 + lift, DARK)
    c.disc(mx, mz, 4.6, b + 12, DARK_SLAB, ring=0.9)
    c.set(mx, b + 16, mz, DARK_SLAB); c.set(mx, b + 17, mz, "85"); c.set(mx, b + 18, mz, "89")
    for dz in (2, 3, 4):                                                 # axle through the wall
        c.set(mx, HUB_Y, mz + dz, "17:8")
    # inside: sacks, a millstone and a lamp
    c.set(mx - 2, b, mz - 1, "35:12"); c.set(mx - 2, b, mz, "35:0"); c.set(mx - 2, b + 1, mz, "35:12")
    c.set(mx + 1, b, mz - 1, "145:0"); c.set(mx + 2, b, mz + 1, "170:0")
    c.set(mx, b + 3, mz, "85"); c.set(mx, b + 2, mz, "89")
    c.set(mx + 1, b + 5, mz + 1, "54:2"); c.set(mx - 1, b + 5, mz - 1, "58"); c.set(mx - 1, b + 5, mz + 1, "118:3")


def sails(c):
    """Four log arms along the axes, each carrying two rows of wool on its trailing side."""
    x0, y0, z = MILL_X, HUB_Y, SAIL_Z
    c.set(x0, y0, z, "162:0")
    for k in range(1, ARM + 1):
        c.set(x0 + k, y0, z, "17:4"); c.set(x0 - k, y0, z, "17:4")
        c.set(x0, y0 + k, z, "17:0"); c.set(x0, y0 - k, z, "17:0")
    for k in range(2, ARM + 1):
        cloth = "35:0" if k % 2 == 0 else "35:8"
        for row in (1, 2, 3):
            c.set(x0 + k, y0 + row, z, cloth)
            c.set(x0 - k, y0 - row, z, cloth)
            c.set(x0 - row, y0 + k, z, cloth)
            c.set(x0 + row, y0 - k, z, cloth)
    for tip in ((ARM, 4), (-ARM, -4), (-4, ARM), (4, -ARM)):
        c.set(x0 + tip[0], y0 + tip[1], z, "85")
    c.set(x0 + 1, y0 + 1, z, "35:14"); c.set(x0 - 1, y0 - 1, z, "35:14")


def field(c, x0, x1, z0, z1, tokens, along_x=True):
    """Crop rows (or columns) between water channels; `~` is a channel."""
    crops = {"W": WHEAT, "C": CARROT, "P": POTATO}
    for index, token in enumerate(tokens):
        cells = [(x, z0 + index) for x in range(x0, x1 + 1)] if along_x else [(x0 + index, z) for z in range(z0, z1 + 1)]
        for x, z in cells:
            if token == "~":
                c.set(x, -1, z, "9")
            else:
                c.set(x, -1, z, "60:7"); c.set(x, 0, z, crops[token])


def fence_rect(c, x0, z0, x1, z1, gates=()):
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            c.set(x, 0, z, "107:0" if (x, z) in gates else "85")
    for z in range(z0 + 1, z1):
        for x in (x0, x1):
            c.set(x, 0, z, "107:1" if (x, z) in gates else "85")


def fields(c):
    field(c, 2, 11, 23, 29, ["W", "W", "~", "C", "C", "~", "P"])
    fence_rect(c, 1, 22, 12, 30, gates=((12, 26),))
    field(c, 20, 29, 23, 29, ["W", "W", "~", "P", "P", "~", "C", "C", "~", "W"][:10], along_x=False)
    fence_rect(c, 19, 22, 30, 30, gates=((19, 26),))
    field(c, 2, 5, 15, 20, ["C", "W", "~", "P"], along_x=False)
    fence_rect(c, 1, 14, 6, 21, gates=((6, 17),))
    for z in range(23, 32):                                              # path up to the mill door
        for x in (14, 15, 16, 17, 18):
            if 15 <= x <= 17 or z >= 29:
                skin(c, x, z, "13" if (x + z) % 2 else "3:1")
    for z in range(17, 23):
        for x in (15, 16, 17):
            skin(c, x, z, "13" if (x + z) % 2 else "3:1")
    for x in range(13, 15):                                              # side path to the west plot's gate
        skin(c, x, 17, "3:1")
    for x in range(8, 14):
        skin(c, x, 17, "13" if x % 2 else "3:1")
    put(c, 14, 31, 0, "118:3") if False else None
    # sacks and a cauldron by the gate, a flower border along the path
    put(c, 13, 24, 0, "118:3"); put(c, 13, 25, 0, "35:12"); put(c, 13, 28, 0, "35:0"); put(c, 13, 28, 1, "35:12")
    for z in range(23, 29):
        if z % 2 == 0:
            put(c, 14, z, 0, "37" if z % 4 == 0 else "38:4")
            put(c, 18, z, 0, "38:5" if z % 4 == 0 else "37")


def shed_and_cellar(c):
    floor = -6
    c.lower(0, 0, 8, 7, floor)
    for x0, z0, x1, z1 in ((0, 0, 8, 0), (0, 7, 8, 7), (0, 1, 0, 6), (2, 1, 8, 6), (1, 2, 1, 6)):
        c.roof(x0, z0, x1, z1, -2, 0)
    for x in range(0, 9):                                                # paved cellar floor
        for z in range(0, 8):
            c.set(x, floor - 1, z, ("48", "4", "13", "3:1")[(x * 3 + z * 5) % 4])
    for y in range(floor, 0):
        c.set(1, y, 1, "65:5")
    c.box(5, floor, 1, 7, floor + 1, 1, "17:0")                          # log stack
    c.box(3, floor, 5, 7, floor, 5, "47"); c.box(7, floor + 1, 5, 7, floor + 2, 5, "47")
    c.box(5, floor + 1, 5, 6, floor + 1, 5, "47")
    c.box(0, floor, 3, 0, floor + 1, 3, "170:0"); c.box(0, floor, 4, 0, floor, 4, "170:0")
    c.set(3, floor, 3, "54:3"); c.set(4, floor, 3, "118:3"); c.set(5, floor, 3, "58"); c.set(6, floor, 3, "61:2")
    c.set(4, floor + 2, 1, "89"); c.set(2, floor + 2, 6, "30"); c.set(1, floor, 5, "30")
    c.set(7, floor, 4, "35:12"); c.set(2, floor, 5, "54:2"); c.set(8, floor, 2, "35:12"); c.set(8, floor, 3, "35:0")
    c.set(6, floor + 2, 1, "50:5") if False else None
    for x, z in ((8, 6), (0, 6)):
        c.set(x, floor + 1, z, "30")
    # shed above
    for x in range(0, 9):
        for z in range(0, 8):
            if (x, z) != (1, 1):
                c.set(x, -1, z, WOOD)
    for y in (0, 1, 2):
        for x in range(0, 9):
            c.set(x, y, 0, WOOD); c.set(x, y, 7, WOOD)
        for z in range(1, 7):
            c.set(0, y, z, WOOD); c.set(8, y, z, WOOD)
    for x, z in ((0, 0), (8, 0), (0, 7), (8, 7), (4, 0), (4, 7)):
        c.box(x, 0, z, x, 2, z, LOG)
    c.set(2, 0, 7, "64:3"); c.set(2, 1, 7, "64:8")
    for x in (1, 3, 6):
        c.set(x, 1, 7, "102")
    for x in (2, 3, 6, 7):
        c.set(x, 1, 0, "102")
    for z in (2, 5):
        c.set(8, 1, z, "102")
    c.set(0, 1, 3, "102")
    for x in range(0, 9):                                                # roof, ridge along x
        c.set(x, 3, 0, "134:2"); c.set(x, 4, 1, "134:2"); c.set(x, 5, 2, "134:2"); c.set(x, 6, 3, "134:2")
        c.set(x, 6, 4, "134:3"); c.set(x, 5, 5, "134:3"); c.set(x, 4, 6, "134:3"); c.set(x, 3, 7, "134:3")
    for x in range(1, 8):
        c.set(x, 3, 1, WOOD); c.set(x, 3, 6, WOOD); c.set(x, 4, 2, WOOD); c.set(x, 4, 5, WOOD)
        c.set(x, 5, 3, WOOD); c.set(x, 5, 4, WOOD)
    for x in (0, 8):
        for z, top in ((1, 3), (2, 4), (3, 5), (4, 5), (5, 4), (6, 3)):
            for y in range(3, top + 1):
                c.set(x, y, z, WOOD)
    # inside: bench, chest, lamp; outside: hay, barrels, rack
    c.set(3, 0, 2, "58"); c.set(7, 0, 5, "54:2"); c.set(6, 0, 2, "17:0"); c.set(4, 2, 4, "85"); c.set(4, 1, 4, "89")
    for dz in (1, 2):
        c.set(9, 0, dz, "170:0")
    c.set(9, 1, 1, "170:0")
    c.set(9, 0, 4, "17:0"); c.set(9, 1, 4, "17:0"); c.set(9, 0, 5, "35:12"); c.set(10, 0, 1, "170:0")
    c.set(1, 0, 8, "85"); c.set(1, 1, 8, "85"); c.set(0, 0, 8, "85"); c.set(0, 1, 8, "85"); c.set(0, 2, 8, SPRUCE_SLAB if False else "126:1")
    c.set(4, -1, 8, "98"); c.set(3, -1, 8, "98"); c.set(2, -1, 8, "98") if False else None
    for z in (8, 9, 10):                                                 # stepping stones to the well and the path
        c.set(2, ground(2, z), z, "3:1") if z > 8 else None


def yard(c):
    c.prop("hand-cart", 25, base(25, 17), 17)
    put(c, 24, 20, 0, "170:4"); put(c, 24, 20, 1, "170:4"); put(c, 25, 21, 0, "170:0"); put(c, 23, 20, 0, "170:0")
    c.prop("scarecrow", 3, 1, 17, 0)
    c.set(3, 0, 17, "85")
    c.prop("well", 4, base(4, 11), 11)
    for x, z, block in ((21, 15, "37"), (22, 15, "38:5"), (21, 14, "38:4"), (22, 16, "37"), (20, 16, "38:5")):
        put(c, x, z, 0, block)
    for x, z in ((6, 8), (7, 9), (8, 9), (9, 10), (10, 10)):                      # stepping stones from the shed
        skin(c, x, z, "4" if (x + z) % 2 else "98:2")


def build():
    c = Chunk("windmill", "Windmill Farm", "grass",
              "A round windmill with four wool sails on a low rise above wheat, carrot and potato plots, "
              "a scarecrow, a well, a cart and a root cellar.", size=32)
    for cx, cz, radius, height in HILLS:
        c.hill(cx, cz, radius, height)
    tower(c)
    sails(c)
    fields(c)
    shed_and_cellar(c)
    yard(c)
    c.tree(27, 13, "tiny-oak-3")
    c.boulder(26, 3, 3, "round")
    c.cover([(0, 0), (32, 0), (32, 22), (0, 22)], coverage=0.4, fernShare=0.1, flowerShare=0.25, tallShare=0.25)
    c.cover([(0, 22), (32, 22), (32, 32), (0, 32)], coverage=0.2, flowerShare=0.3, tallShare=0.2)
    return c
