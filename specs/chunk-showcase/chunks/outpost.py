"""Snowy Outpost: a spruce watchtower with a roofed lookout, a log cabin with a stone chimney, an igloo whose
floor hatch drops into an ice cave cut open on two faces, a frozen pond, a sled, a snowman and firewood."""
import math

from kit import Chunk

SPRUCE, SPRUCE_LOG, SLAB = "5:1", "17:1", "126:1"
POND_X, POND_Z, POND_RX, POND_RZ = 3.5, 11.5, 3.3, 2.8
CAVE_FLOOR = -7                          # lowest air course of the ice cave


def in_pond(x, z):
    return ((x - POND_X) / POND_RX) ** 2 + ((z - POND_Z) / POND_RZ) ** 2 <= 1.0


def pond(c):
    for z in range(16):
        xs = [x for x in range(16) if in_pond(x, z)]
        if xs:
            c.lower(min(xs), z, max(xs), z, -2)
    for x in range(16):
        for z in range(16):
            if in_pond(x, z):
                c.set(x, -3, z, "13" if (x + z) % 3 else "3:1")
                c.set(x, -2, z, "9")
                c.set(x, -1, z, "174" if (x * 5 + z * 3) % 7 == 0 else "79")
            elif any(in_pond(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                c.set(x, -1, z, "174" if (x + z) % 2 else "80")
    c.set(2, 0, 10, "83") if False else None
    c.set(0, -1, 14, "174") if False else None


def cabin(c):
    x0, x1, z0, z1 = 1, 6, 1, 5
    for y in range(0, 4):
        for x in range(x0, x1 + 1):
            c.set(x, y, z0, SPRUCE); c.set(x, y, z1, SPRUCE)
        for z in range(z0, z1 + 1):
            c.set(x0, y, z, SPRUCE); c.set(x1, y, z, SPRUCE)
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        c.box(x, 0, z, x, 3, z, SPRUCE_LOG)
    for x in range(x0, x1 + 1):                                         # log sill and plate
        c.set(x, 0, z1, "17:5") if x not in (x0, x1, 4) else None
        c.set(x, 3, z0, "17:5") if x not in (x0, x1) else None
        c.set(x, 3, z1, "17:5") if x not in (x0, x1) else None
    for z in range(z0 + 1, z1):
        c.set(x0, 3, z, "17:9"); c.set(x1, 3, z, "17:9")
    c.set(4, 0, z1, "64:3"); c.set(4, 1, z1, "64:8")                    # door, south wall
    for x in (2, 6 - 1):
        pass
    c.set(2, 1, z1, "102"); c.set(2, 2, z1, "102"); c.set(6 - 1, 1, z1, "102")
    c.set(3, 1, z0, "102"); c.set(3, 2, z0, "102"); c.set(5, 1, z0, "102")
    c.set(x0, 1, 3, "102"); c.set(x0, 2, 3, "102")
    # shutters beside the front windows
    c.set(1 + 0, 2, z1 + 1, "96:5") if False else None
    # roof, ridge east-west with eaves
    for x in range(0, 8):
        c.set(x, 3, 0, "134:2") if x in (0, 7) else None
        c.set(x, 4, 1, "134:2"); c.set(x, 5, 2, "134:2")
        c.set(x, 6, 3, "80")
        c.set(x, 5, 4, "134:3"); c.set(x, 4, 5, "134:3")
        c.set(x, 3, 6, "134:3")
    for x in range(1, 7):
        c.set(x, 3, 0, "134:2")
    for x in range(0, 8):
        c.set(x, 3, 6, "134:3")
    for x in (1, 6):                                                    # gable fills
        c.set(x, 4, 2, SPRUCE); c.set(x, 4, 3, SPRUCE); c.set(x, 5, 3, SPRUCE); c.set(x, 4, 4, SPRUCE)
    for x in range(2, 6):                                               # ceiling under the ridge
        c.set(x, 4, 2, SPRUCE); c.set(x, 4, 4, SPRUCE)
    # stone chimney on the east gable
    for y in range(0, 9):
        c.set(7, y, 3, "98" if y % 3 else "4")
    c.set(7, 0, 2, "4"); c.set(7, 0, 4, "4"); c.set(7, 1, 2, "4") if False else None
    c.set(7, 9, 3, "44:5"); c.set(7, 1, 4, "98") if False else None
    c.set(7, 0, 3, "4")
    # inside: hearth, bed, table, chest, shelves, rug
    c.set(6, 0, 3, "61:4"); c.set(6, 0, 2, "4") if False else None
    c.set(2, 0, 2, "26:1"); c.set(3, 0, 2, "26:9")
    c.set(2, 0, 4, "54:3"); c.set(3, 0, 4, "58"); c.set(5, 0, 2, "47"); c.set(5, 1, 2, "47"); c.set(4, 0, 2, "47")
    c.set(4, 2, 3, "85"); c.set(4, 1, 3, "89") if False else None
    c.set(4, 3, 3, "85") if False else None
    c.set(3, 0, 3, "171:14"); c.set(4, 0, 3, "171:14"); c.set(5, 0, 3, "171:14"); c.set(5, 0, 4, "140")
    c.set(4, 3, 3, "89")                                                # lamp in the ceiling beam
    # porch: step, bench and a lamp
    c.set(4, -1, z1 + 1, "98"); c.set(3, -1, z1 + 1, "98"); c.set(5, -1, z1 + 1, "98")
    c.set(2, 0, z1 + 1, "17:9") if False else None
    c.set(1, 0, z1 + 1, "85"); c.set(1, 1, z1 + 1, "85"); c.set(1, 2, z1 + 1, "89")
    # firewood against the north wall, a chopping block and axe
    for y in range(0, 2):
        c.box(1, y, 0, 5 - y, y, 0, "17:5")
    c.set(2, 2, 0, SLAB) if False else None
    c.set(6, 0, 0, "17:0"); c.set(6, 1, 0, "69:5") if False else None
    c.set(0, 0, 3, "17:9") if False else None
    c.set(0, 0, 2, "17:0") if False else None


def tower(c):
    """Four spruce legs 13 high, ring beams, a ladder, a fenced platform and a four-ring stair roof."""
    platform = 13
    for x, z in ((10, 10), (13, 10), (10, 13), (13, 13)):
        c.box(x, 0, z, x, platform, z, SPRUCE_LOG)
    for y in (3, 6, 9, 12):
        for x in range(10, 14):
            c.set(x, y, 10, "17:5"); c.set(x, y, 13, "17:5")
        for z in range(10, 14):
            c.set(10, y, z, "17:9"); c.set(13, y, z, "17:9")
    for y in (4, 5, 7, 8, 10, 11):                                      # lattice of fences between the beams
        for x in (11, 12):
            c.set(x, y, 13, "85") if (x + y) % 2 == 0 else None
            c.set(x, y, 10, "85") if (x + y) % 2 else None
        for z in (11, 12):
            c.set(13, y, z, "85") if (z + y) % 2 == 0 else None
            c.set(10, y, z, "85") if (z + y) % 2 else None
    for y in range(0, platform):                                        # ladder up the north-west leg
        c.set(10, y, 9, "65:2")
    for x in range(9, 15):
        for z in range(9, 15):
            c.set(x, platform, z, SPRUCE)
    c.set(10, platform, 9, None)                                        # hatch above the ladder
    for x in range(9, 15):
        for z in (9, 14):
            c.set(x, platform + 1, z, "85")
    for z in range(9, 15):
        for x in (9, 14):
            c.set(x, platform + 1, z, "85")
    c.set(10, platform + 1, 9, None)
    for x, z in ((9, 9), (14, 9), (9, 14), (14, 14)):
        c.box(x, platform + 1, z, x, platform + 4, z, SPRUCE_LOG)
    top = platform + 5                                                   # roof rings: 8x8, 6x6, 4x4
    for lo, hi, y in ((8, 15, top), (9, 14, top + 1), (10, 13, top + 2)):
        for x in range(lo, hi + 1):
            for z in range(lo, hi + 1):
                edge_x, edge_z = x in (lo, hi), z in (lo, hi)
                if edge_x or edge_z:
                    stair = "134:3" if z == hi else "134:2" if z == lo else "134:1" if x == hi else "134:0"
                    c.set(x, y, z, SLAB if edge_x and edge_z else stair)
                else:
                    c.set(x, y, z, SPRUCE)
    c.box(11, top + 3, 11, 12, top + 3, 12, SLAB)
    c.set(11, top + 4, 11, "85")
    # lookout furnishings
    c.set(12, platform + 1, 12, "54:2"); c.set(13, platform + 1, 11, "58"); c.set(11, platform + 1, 13, "171:14")
    c.set(12, platform + 4, 12, "85"); c.set(12, platform + 3, 12, "89")
    c.set(11, platform + 4, 10, "85") if False else None
    # supplies at the tower's foot
    c.set(11, 0, 14, "17:0"); c.set(12, 0, 14, "170:0"); c.set(14, 0, 11, "17:0"); c.set(14, 0, 12, "118:3")
    c.set(14, 0, 10, "54:4")


def igloo(c):
    cx, cz, radius = 11, 3, 3.4
    for x in range(7, 16):
        for z in range(0, 7):
            for y in range(0, 4):
                d = math.sqrt((x - cx) ** 2 + (y + 0.5) ** 2 + (z - cz) ** 2)
                if radius - 1.1 <= d <= radius:
                    c.set(x, y, z, "80")
    c.set(cx, 3, cz, "80") if False else None
    for y in (0, 1):                                                    # door and a short tunnel south
        c.set(11, y, 6, None)
        c.set(10, y, 7, "80"); c.set(12, y, 7, "80"); c.set(10, y, 8, "80"); c.set(12, y, 8, "80")
    for z in (7, 8):
        c.set(11, 2, z, "80"); c.set(10, 2, z, "80"); c.set(12, 2, z, "80")
    c.set(10, 0, 6, "80"); c.set(12, 0, 6, "80")
    for x, z in ((9, 3), (13, 3), (11, 1), (11, 5), (9, 2), (13, 4)):   # rugs and furniture inside
        pass
    c.set(13, 0, 2, "26:2") if False else None
    c.set(13, 0, 1, "26:2"); c.set(13, 0, 2, "26:10") if False else None
    c.set(9, 0, 4, "54:5"); c.set(9, 0, 2, "61:5")
    c.set(10, 0, 5, "171:14") if False else None
    for x, z in ((10, 3), (12, 3), (11, 2), (11, 4), (10, 2), (12, 4), (10, 4), (12, 2)):
        c.set(x, -1, z, "35:0") if False else None
    c.set(11, 2, 3, "89") if False else None
    c.set(11, 3, 3, "89") if False else None


def cave(c):
    floor = CAVE_FLOOR
    c.lower(8, 0, 15, 6, floor)
    for x0, z0, x1, z1 in ((8, 0, 15, 2), (8, 4, 15, 6), (8, 3, 10, 3), (12, 3, 15, 3)):
        c.roof(x0, z0, x1, z1, -2, 0)
    c.box(8, floor - 1, 0, 15, floor - 1, 6, "174")
    for y in range(floor, -1):
        c.set(11, y, 3, "65:4")                                         # ladder up the hatch
    for y in range(floor, -2):
        c.set(12, y, 3, "174")
    # stalagmites and stalactites of ice
    for x, z, rise, hang in ((9, 1, 3, 2), (14, 1, 2, 3), (9, 5, 2, 2), (14, 5, 3, 2), (12, 0, 1, 3), (10, 6, 2, 1),
                             (13, 2, 4, 1), (12, 5, 1, 3)):
        for dy in range(rise):
            c.set(x, floor + dy, z, "79" if dy else "174")
        for dy in range(hang):
            c.set(x, -3 - dy, z, "79")
    # a frozen waterfall down the back wall and sea-lantern glow behind the ice
    for y in range(floor, -2):
        c.set(8, y, 4, "79"); c.set(8, y, 5, "174" if y % 2 else "79")
    c.set(8, floor + 1, 3, "169"); c.set(15, floor + 1, 4, "169") if False else None
    # loot: a chest and a frozen explorer
    c.set(14, floor, 4, "54:4"); c.set(14, floor, 3, "54:4")
    c.set(13, floor, 5, "144:1"); c.set(9, floor, 2, "144:1")
    c.set(10, floor, 4, "50:5") if False else None
    c.set(10, floor, 1, "174"); c.set(10, floor + 1, 1, "50:5")
    c.set(13, floor, 1, "174"); c.set(13, floor + 1, 1, "50:5")
    c.set(14, floor, 6, "78") if False else None
    for x, z in ((9, 3), (15, 5), (12, 1), (9, 6)):
        c.set(x, floor + 1, z, "30")
    c.set(11, floor, 5, "78"); c.set(10, floor, 3, "78"); c.set(13, floor, 3, "78"); c.set(11, floor, 1, "78")


def yard(c):
    # snowman in front of the cabin
    c.set(5, 0, 7, "80"); c.set(5, 1, 7, "80"); c.set(5, 2, 7, "86:0")
    c.set(4, 1, 7, "85"); c.set(6, 1, 7, "85")
    # sled
    for z in range(7, 10):
        pass
    for x in (2, 3):
        c.set(x, 0, 7, SLAB.replace(":1", ":9")); c.set(x, 0, 8, SLAB.replace(":1", ":9"))
    c.set(1, 0, 7, "126:9"); c.set(1, 0, 8, "126:9")
    c.set(2, 1, 7, "96:11") if False else None
    c.set(3, 1, 8, "96:3") if False else None
    c.set(2, 1, 7, "96:0"); c.set(3, 1, 7, "96:0")
    c.set(0, 0, 7, "17:5") if False else None
    c.set(1, 1, 7, "85") if False else None
    # a lamp post by the path in from the west and a signpost
    c.prop("lantern-post", 6, 0, 9)
    c.prop("signpost", 8, 0, 11)
    # a stack of crates and barrels beside the tower
    c.set(9, 0, 13, "17:0"); c.set(8, 0, 14, "170:0"); c.set(8, 1, 14, "17:0") if False else None


def fir(c, x, z, height):
    """A small made spruce: a log trunk in tiers of spruce leaves."""
    for y in range(height):
        c.set(x, y, z, SPRUCE_LOG)
    for y in range(1, height + 1):
        radius = 2 if (height - y) % 2 == 1 and height - y > 1 else 1 if height - y > 0 else 0
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if abs(dx) + abs(dz) <= radius + (1 if radius == 2 else 0) and (dx or dz or y == height):
                    if (x + dx, y, z + dz) not in c.blocks and 0 <= x + dx <= 15 and 0 <= z + dz <= 15:
                        c.set(x + dx, y, z + dz, "18:5")
    c.set(x, height + 1, z, "78") if False else None


def dust(c):
    """Snow layers on the bare ground and on full blocks with open sky over them."""
    full = {17, 5, 80, 4, 98, 79, 174, 170, 24, 1}
    for x in range(16):
        for z in range(16):
            column = [y for (px, y, pz) in c.blocks if px == x and pz == z]
            if not column:
                if (x * 7 + z * 11) % 3 == 0 and not (7 <= x <= 9 and z >= 6):
                    if not in_pond(x, z) and (x, 0, z) not in c.blocks:
                        c.set(x, 0, z, "78")
                continue
            top = max(column)
            block = c.blocks[(x, top, z)]
            if block[0] in full and top >= 0 and (x * 5 + z * 3 + top) % 3 != 0:
                c.set(x, top + 1, z, "78")


def build():
    c = Chunk("outpost", "Snowy Outpost", "snow",
              "A spruce watchtower, a log cabin with a stone chimney, an igloo over an ice cave, a frozen pond and a snowman.")
    c.raise_(0, 14, 2, 15, 2); c.raise_(0, 15, 1, 15, 3)
    c.raise_(13, 0, 15, 1, 2) if False else None
    pond(c)
    cave(c)
    cabin(c)
    tower(c)
    igloo(c)
    yard(c)
    c.tree(8, 8, "tiny-spruce-4")
    c.boulder(6, 11, 3, "round", mossy=False)
    c.boulder(12, 13, 2, "angular", mossy=False)
    for x, z, height in ((14, 7, 5), (6, 14, 5)):
        fir(c, x, z, height)
    dust(c)
    return c
