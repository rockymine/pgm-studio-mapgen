"""Snowy Outpost, as a plot: a spruce watchtower on a knoll with a roofed lookout, a log cabin with a stone chimney on
a terrace, an igloo whose floor hatch drops into an ice cave cut open on two faces, a frozen pond in a dell, a
sled, a snowman, firewood, two firs, a spruce and two boulders."""
import math

from kit import Chunk

SPRUCE, SPRUCE_LOG, SLAB = "5:1", "17:1", "126:1"
POND_X, POND_Z, POND_RX, POND_RZ = 9.0, 23.0, 5.0, 3.8
HOLLOW_R, HOLLOW_TOP = 7.0, -2           # the dell round the pond; ice lies flush with its floor
POND_BED = -5
CAVE_FLOOR = -8
CAVE = (19, 0, 31, 10)                   # x0, z0, x1, z1 of the cave, open on the north and east faces
HATCH = (25, 5)
IGLOO_X, IGLOO_Z, IGLOO_R = 25, 5, 5.0
HILLS = ((24, 22, 8, 3),)                # cx, cz, r, h as handed to c.hill
TERRACES = ((7, 6, 6.5, 2),)             # cx, cz, r, h as handed to c.mound
SOIL_PATCH = (14, 13, 3, 1)              # forest soil under the spruce
NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def in_pond(x, z):
    return ((x - POND_X) / POND_RX) ** 2 + ((z - POND_Z) / POND_RZ) ** 2 <= 1.0


def in_cave(x, z):
    return CAVE[0] <= x <= CAVE[2] and CAVE[1] <= z <= CAVE[3]


def cut_top(x, z):
    if in_pond(x, z):
        return POND_BED
    if math.hypot(x - POND_X, z - POND_Z) <= HOLLOW_R:
        return HOLLOW_TOP
    return None


def ground(x, z):
    """Top course of the terrain at a cell: the hills and terraces, cut by the dell; the cave roof is flat."""
    cut = cut_top(x, z)
    if cut is not None:
        return cut
    top = -1
    for cx, cz, radius, height in HILLS:
        for course in range(1, height + 1):
            ring = radius * (1 - (course - 1) / height * 0.7)
            if ring >= 0.8 and math.hypot(x - cx, z - cz) <= ring:
                top = max(top, course - 1)
    for cx, cz, radius, height in TERRACES + (SOIL_PATCH,):
        if math.hypot(x - cx, z - cz) <= radius:
            top = max(top, height - 1)
    return top


def base(x, z):
    return ground(x, z) + 1


def put(c, x, z, dy, block):
    c.set(x, base(x, z) + dy, z, block)


def skin(c, x, z, block):
    c.set(x, ground(x, z), z, block)


def landform(c):
    for cx, cz, radius, height in HILLS:
        c.hill(cx, cz, radius, height)
    for cx, cz, radius, height in TERRACES:
        c.mound(cx, cz, radius, height)
    c.mound(SOIL_PATCH[0], SOIL_PATCH[1], SOIL_PATCH[2], SOIL_PATCH[3], theme="forest")
    for z in range(32):
        start = None
        for x in range(33):
            top = cut_top(x, z) if x < 32 else None
            if start is not None and top != cut_top(start, z):
                c.lower(start, z, x - 1, z, cut_top(start, z) + 1)
                start = None
            if top is not None and start is None:
                start = x


def pond(c):
    for x in range(32):
        for z in range(32):
            if in_pond(x, z):
                c.set(x, POND_BED, z, "13" if (x + z) % 3 else "3:1")
                c.box(x, POND_BED + 1, z, x, HOLLOW_TOP - 1, z, "9")
                c.set(x, HOLLOW_TOP, z, "174" if (x * 5 + z * 3) % 7 == 0 else "79")
            elif math.hypot(x - POND_X, z - POND_Z) <= HOLLOW_R and any(
                    in_pond(x + dx, z + dz) for dx, dz in NEIGHBOURS):
                skin(c, x, z, "174" if (x + z) % 2 else "80")


def cabin(c):
    b = 2                                                               # first air course on the terrace
    x0, x1, z0, z1 = 3, 10, 3, 9
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.set(x, b - 1, z, SPRUCE)                                  # plank floor
    for y in range(b, b + 4):
        for x in range(x0, x1 + 1):
            c.set(x, y, z0, SPRUCE); c.set(x, y, z1, SPRUCE)
        for z in range(z0, z1 + 1):
            c.set(x0, y, z, SPRUCE); c.set(x1, y, z, SPRUCE)
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        c.box(x, b, z, x, b + 3, z, SPRUCE_LOG)
    for x in range(x0 + 1, x1):                                         # log sill and plate
        if x != 7:
            c.set(x, b, z1, "17:5")
        c.set(x, b + 3, z0, "17:5"); c.set(x, b + 3, z1, "17:5")
    for z in range(z0 + 1, z1):
        c.set(x0, b + 3, z, "17:9"); c.set(x1, b + 3, z, "17:9")
    c.set(7, b, z1, "64:3"); c.set(7, b + 1, z1, "64:8")                # door, south wall
    for x in (4, 5, 9):
        c.set(x, b + 1, z1, "102"); c.set(x, b + 2, z1, "102")
    for x in (5, 8):
        c.set(x, b + 1, z0, "102"); c.set(x, b + 2, z0, "102")
    c.set(x0, b + 1, 6, "102"); c.set(x0, b + 2, 6, "102")
    for x in range(x0 - 1, x1 + 2):                                     # roof: ridge east-west, snow on top
        c.set(x, b + 3, z0 - 1, "134:2"); c.set(x, b + 4, z0, "134:2"); c.set(x, b + 5, z0 + 1, "134:2")
        c.set(x, b + 6, z0 + 2, "134:2")
        c.set(x, b + 3, z1 + 1, "134:3"); c.set(x, b + 4, z1, "134:3"); c.set(x, b + 5, z1 - 1, "134:3")
        c.set(x, b + 6, z1 - 2, "134:3")
        c.set(x, b + 7, 6, "80")
    for x in range(x0 + 1, x1):                                         # ceiling
        for z in range(z0 + 1, z1):
            c.set(x, b + 4, z, SPRUCE)
    for x in (x0, x1):                                                  # gable fills
        for z, top in ((4, 4), (5, 5), (6, 6), (7, 5), (8, 4)):
            for y in range(b + 4, b + top + 1):
                c.set(x, y, z, SPRUCE)
    for y in range(b, b + 10):                                          # stone chimney on the east gable
        c.set(x1 + 1, y, 6, "98" if y % 3 else "4")
    c.set(x1 + 1, b, 5, "4"); c.set(x1 + 1, b, 7, "4"); c.set(x1 + 1, b + 10, 6, "44:5")
    # inside: hearth, bed, table, chest, shelves, rug
    c.set(x1 - 1, b, 6, "61:4")
    c.set(4, b, 4, "26:1"); c.set(5, b, 4, "26:9")
    c.set(4, b, 8, "54:3"); c.set(5, b, 8, "58"); c.set(8, b, 4, "47"); c.set(8, b + 1, 4, "47")
    c.set(7, b, 4, "47"); c.set(9, b, 8, "140") if False else None
    for x in (5, 6, 7, 8):
        for z in (6, 7):
            c.set(x, b, z, "171:14")
    c.set(9, b, 7, "140")
    c.set(6, b + 3, 6, "85"); c.set(6, b + 2, 6, "89")                  # lamp hung from the ceiling beam
    # porch: steps, a log bench, a lamp
    for x in (6, 7, 8):
        c.set(x, b - 1, z1 + 1, "98")
    c.set(3, b, z1 + 1, "85"); c.set(3, b + 1, z1 + 1, "85"); c.set(3, b + 2, z1 + 1, "89")
    c.set(10, b, z1 + 1, "17:9"); c.set(10, b, z1 + 2, "17:9") if False else None
    # firewood against the north wall, a chopping block and axe
    for y in range(0, 2):
        c.box(x0 + 1, b + y, z0 - 1, x0 + 6 - y, b + y, z0 - 1, "17:5")
    c.set(x1, b, z0 - 1, "17:0"); c.set(x1, b + 1, z0 - 1, "69:5") if False else None
    c.set(x1 + 1, b, z0 - 1, "17:0")


def tower(c):
    """Four spruce legs on the knoll, ring beams, a ladder, a fenced platform and a four-ring stair roof."""
    legs = ((21, 19), (26, 19), (21, 24), (26, 24))
    platform = 14
    for x, z in legs:
        c.box(x, base(x, z), z, x, platform, z, SPRUCE_LOG)
    for y in (6, 9, 12):
        for x in range(21, 27):
            c.set(x, y, 19, "17:5"); c.set(x, y, 24, "17:5")
        for z in range(19, 25):
            c.set(21, y, z, "17:9"); c.set(26, y, z, "17:9")
    for y in (4, 5, 7, 8, 10, 11, 13):                      # lattice of fences between the beams
        for x in (22, 23, 24, 25):
            c.set(x, y, 24, "85") if (x + y) % 2 == 0 else None
            c.set(x, y, 19, "85") if (x + y) % 2 else None
        for z in (20, 21, 22, 23):
            c.set(26, y, z, "85") if (z + y) % 2 == 0 else None
            c.set(21, y, z, "85") if (z + y) % 2 else None
    for y in range(base(21, 18), platform):                             # ladder up the north-west leg
        c.set(21, y, 18, "65:2")
    for x in range(20, 28):
        for z in range(18, 26):
            c.set(x, platform, z, SPRUCE)
    c.set(21, platform, 18, None)                                       # hatch above the ladder
    for x in range(20, 28):
        for z in (18, 25):
            c.set(x, platform + 1, z, "85")
    for z in range(18, 26):
        for x in (20, 27):
            c.set(x, platform + 1, z, "85")
    c.set(21, platform + 1, 18, None)
    for x, z in ((20, 18), (27, 18), (20, 25), (27, 25)):
        c.box(x, platform + 1, z, x, platform + 4, z, SPRUCE_LOG)
    top = platform + 5                                                  # roof rings: 10x10, 8x8, 6x6
    for lo_x, hi_x, lo_z, hi_z, y in ((19, 28, 17, 26, top), (20, 27, 18, 25, top + 1), (21, 26, 19, 24, top + 2)):
        for x in range(lo_x, hi_x + 1):
            for z in range(lo_z, hi_z + 1):
                edge_x, edge_z = x in (lo_x, hi_x), z in (lo_z, hi_z)
                if edge_x or edge_z:
                    stair = "134:3" if z == hi_z else "134:2" if z == lo_z else "134:1" if x == hi_x else "134:0"
                    c.set(x, y, z, SLAB if edge_x and edge_z else stair)
                else:
                    c.set(x, y, z, SPRUCE)
    c.box(22, top + 3, 20, 25, top + 3, 23, SLAB)
    c.set(23, top + 4, 21, "85")
    c.set(24, platform + 1, 22, "54:2"); c.set(25, platform + 1, 20, "58"); c.set(22, platform + 1, 24, "171:14")
    c.set(24, platform + 4, 22, "85"); c.set(24, platform + 3, 22, "89")
    for x, z, block in ((23, 26, "17:0"), (24, 26, "170:0"), (28, 21, "17:0"), (28, 22, "118:3"), (28, 20, "54:4")):
        put(c, x, z, 0, block)


def igloo(c):
    cx, cz, radius = IGLOO_X, IGLOO_Z, IGLOO_R
    for x in range(cx - 6, cx + 7):
        for z in range(0, 11):
            if not 0 <= x <= 31:
                continue
            for y in range(0, 6):
                dist = math.sqrt((x - cx) ** 2 + (y + 0.5) ** 2 + (z - cz) ** 2)
                if radius - 1.2 <= dist <= radius:
                    c.set(x, y, z, "80")
    for y in (0, 1):                                                    # door and a short tunnel south
        c.set(cx, y, 10, None)
        for dx in (-1, 1):
            c.set(cx + dx, y, 11, "80"); c.set(cx + dx, y, 12, "80")
    for z in (11, 12):
        for dx in (-1, 0, 1):
            c.set(cx + dx, 2, z, "80")
    for dx in (-1, 1):
        c.set(cx + dx, 0, 10, "80")
    c.set(28, 0, 3, "26:2"); c.set(28, 0, 2, "26:10")
    c.set(22, 0, 6, "54:5"); c.set(22, 0, 4, "61:5")
    c.set(24, 0, 3, "171:14"); c.set(25, 0, 3, "171:14"); c.set(26, 0, 3, "171:14")
    c.set(25, 3, 4, "89") if False else None


def cave(c):
    f = CAVE_FLOOR
    x0, z0, x1, z1 = CAVE
    c.lower(x0, z0, x1, z1, f)
    for z in range(z0, z1 + 1):                                         # the roof, everywhere but the hatch
        if z == HATCH[1]:
            c.roof(x0, z, HATCH[0] - 1, z, -2, 0)
            c.roof(HATCH[0] + 1, z, x1, z, -2, 0)
        else:
            c.roof(x0, z, x1, z, -2, 0)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.set(x, f - 1, z, "174")
    for y in range(f, 0):
        c.set(HATCH[0], y, HATCH[1], "65:4")                            # ladder up the hatch
    for y in range(f, -2):
        c.set(HATCH[0] + 1, y, HATCH[1], "174")
    # stalagmites and stalactites of ice
    for x, z, rise, hang in ((21, 1, 4, 2), (29, 1, 3, 3), (21, 8, 3, 2), (29, 8, 4, 2), (25, 0, 2, 3),
                             (22, 10, 3, 1), (27, 3, 5, 1), (24, 8, 2, 3), (30, 5, 3, 2), (20, 4, 2, 2)):
        for dy in range(rise):
            c.set(x, f + dy, z, "79" if dy else "174")
        for dy in range(hang):
            c.set(x, -3 - dy, z, "79")
    # a frozen waterfall down the back wall and sea-lantern glow behind the ice
    for y in range(f, -2):
        for z in (6, 7, 8):
            c.set(x0, y, z, "79" if (y + z) % 2 else "174")
    c.set(x0, f + 1, 5, "169"); c.set(x1, f + 1, 8, "169")
    # loot: a chest and a frozen explorer
    c.set(29, f, 6, "54:4"); c.set(29, f, 5, "54:4"); c.set(28, f, 8, "144:1"); c.set(22, f, 3, "144:1")
    c.set(22, f, 1, "174"); c.set(22, f + 1, 1, "50:5")
    c.set(28, f, 1, "174"); c.set(28, f + 1, 1, "50:5")
    for x, z in ((20, 3), (30, 9), (25, 1), (21, 9)):
        c.set(x, f + 1, z, "30")
    for x, z in ((23, 7), (21, 5), (27, 5), (24, 2), (26, 9), (29, 3)):
        c.set(x, f, z, "78")


def yard(c):
    # snowman in front of the cabin
    for dy in (0, 1):
        put(c, 6, 12, dy, "80")
    put(c, 6, 12, 2, "86:0")
    put(c, 5, 12, 1, "85"); put(c, 7, 12, 1, "85")
    # sled
    for x in (2, 3, 4):
        put(c, x, 13, 0, "126:9"); put(c, x, 14, 0, "126:9")
    put(c, 1, 13, 0, "126:9"); put(c, 1, 14, 0, "126:9")
    put(c, 2, 13, 1, "96:0"); put(c, 3, 13, 1, "96:0"); put(c, 4, 13, 1, "96:0")
    # lamp post and signpost on the path, crates and barrels by the tower
    c.prop("lantern-post", 12, base(12, 14), 14)
    c.prop("signpost", 16, base(16, 17), 17)
    put(c, 14, 29, 0, "17:0"); put(c, 15, 29, 0, "170:0"); put(c, 14, 30, 0, "170:0")


def paths(c):
    for z in range(13, 32):                                             # gravel in from the south
        for x in (15, 16, 17):
            if cut_top(x, z) is None:
                skin(c, x, z, "13" if (x + z) % 2 else "174")
    for x in range(0, 16):                                              # and in from the west, to the cabin steps
        for z in (16, 17):
            if cut_top(x, z) is None:
                skin(c, x, z, "13" if (x + z) % 2 else "174")
    for z in range(10, 16):
        for x in (7, 8):
            if cut_top(x, z) is None:
                skin(c, x, z, "13" if (x + z) % 2 else "174")


def fir(c, x, z, height):
    """A small made spruce: a log trunk in tiers of spruce leaves."""
    foot = base(x, z)
    for y in range(height):
        c.set(x, foot + y, z, SPRUCE_LOG)
    for y in range(1, height + 1):
        radius = 2 if (height - y) % 2 == 1 and height - y > 1 else 1 if height - y > 0 else 0
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if abs(dx) + abs(dz) <= radius + (1 if radius == 2 else 0) and (dx or dz or y == height):
                    if (x + dx, foot + y, z + dz) not in c.blocks and 0 <= x + dx <= 31 and 0 <= z + dz <= 31:
                        c.set(x + dx, foot + y, z + dz, "18:5")


def dust(c):
    """Snow layers on bare ground and on full blocks with open sky over them."""
    full = {17, 5, 80, 4, 98, 79, 174, 170, 24, 1}
    for x in range(32):
        for z in range(32):
            if in_pond(x, z) or in_cave(x, z) and not (x, z) == (0, 0):
                continue
            column = [y for (px, y, pz) in c.blocks if px == x and pz == z]
            if not column:
                if (x * 7 + z * 11) % 3 == 0 and ground(x, z) >= -1 and (x, base(x, z), z) not in c.blocks \
                        and not (x in (7, 8) and 10 <= z <= 15) and not (15 <= x <= 17 and z >= 13) \
                        and not (z in (16, 17) and x <= 15):
                    put(c, x, z, 0, "78")
                continue
            top = max(column)
            block = c.blocks[(x, top, z)]
            if block[0] in full and top >= 0 and (x * 5 + z * 3 + top) % 3 != 0:
                c.set(x, top + 1, z, "78")


def build():
    c = Chunk("outpost", "Snowy Outpost", "snow",
              "A spruce watchtower on a knoll, a log cabin on its terrace, an igloo over an ice cave, a frozen "
              "pond in a dell and a snowman.", size=32)
    landform(c)
    pond(c)
    cave(c)
    cabin(c)
    tower(c)
    igloo(c)
    yard(c)
    paths(c)
    c.tree(14, 13, "tiny-spruce-4")
    c.boulder(20, 29, 3, "round", mossy=False)
    c.boulder(19, 13, 2, "angular", mossy=False)
    for x, z, height in ((3, 28, 6), (13, 20, 6)):
        fir(c, x, z, height)
    dust(c)
    return c
