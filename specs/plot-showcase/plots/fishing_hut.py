"""Fisherman's Pond, as a plot: a stilted spruce hut over a deep pond sunk in a dell, a pier from the west bank,
a rowboat on a mooring, a drying rack on a knoll, nets and stores on a south-west rise, a fire pit on a
south-east rise, reed islets, lily pads, an olive on the north-west knoll and a chest on the pond bed."""
import math

from kit import Chunk

SPRUCE, SPRUCE_LOG, SPRUCE_SLAB, SPRUCE_STAIR = "5:1", "17:1", "126:1", "134"
POND_X, POND_Z, POND_RX, POND_RZ = 16.0, 15.0, 11.0, 8.0
WATER_TOP = -4                  # top course of the water
NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))
HILLS = ((6, 6, 7, 3), (25, 6, 6, 4), (5, 28, 7, 3), (26, 26, 6, 3))        # cx, cz, r, h as handed to c.hill
DELL = ((15.0, -2), (13.0, -3))                                              # radius, top course


def pond_q(x, z):
    return ((x - POND_X) / POND_RX) ** 2 + ((z - POND_Z) / POND_RZ) ** 2


def in_pond(x, z):
    return pond_q(x, z) <= 1.0


def bed_of(x, z):
    """Top course of the pond bed under a pond cell: a shelf at the rim, deeper toward the middle."""
    q = pond_q(x, z)
    return -6 if q > 0.72 else -7 if q > 0.4 else -8


def ground(x, z):
    """Top course of the terrain at a cell, as the ground shapes below lay it."""
    top = -1
    for cx, cz, radius, height in HILLS:
        for course in range(1, height + 1):
            ring = radius * (1 - (course - 1) / height * 0.7)
            if ring >= 0.8 and math.hypot(x - cx, z - cz) <= ring:
                top = max(top, course - 1)
    dist = math.hypot(x - POND_X, z - POND_Z)
    for radius, course_top in DELL:
        if dist <= radius:
            top = course_top
    return top


def floor_of(x, z):
    """Top course of whatever carries a thing standing at (x, z): the pond bed or the ground."""
    return bed_of(x, z) if in_pond(x, z) else ground(x, z)


def base(x, z):
    return floor_of(x, z) + 1


def put(c, x, z, dy, block):
    """A block `dy` courses above the first air course over the ground at (x, z)."""
    c.set(x, base(x, z) + dy, z, block)


def skin(c, x, z, block):
    """Replace the surface block of the ground at (x, z)."""
    c.set(x, ground(x, z), z, block)


def cut_top(x, z):
    """Top course a lowered cell is cut to — the dell's steps and the pond bed — or None for uncut ground."""
    if in_pond(x, z):
        return bed_of(x, z)
    dist = math.hypot(x - POND_X, z - POND_Z)
    for radius, course_top in DELL:
        if dist <= radius:
            return course_top
    return None


def landform(c):
    """Hills raised, then the dell and pond cut in non-overlapping runs (overlapping cuts do not stack)."""
    for cx, cz, radius, height in HILLS:
        c.hill(cx, cz, radius, height)
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
    """Fill the cut with water to WATER_TOP, line the bed, and sand the bank."""
    for x in range(32):
        for z in range(32):
            if not in_pond(x, z):
                continue
            bed = bed_of(x, z)
            c.box(x, bed + 1, z, x, WATER_TOP, z, "9")
            pick = (x * 7 + z * 13) % 9
            c.set(x, bed, z, "82" if pick < 4 else "13" if pick < 7 else "3:1" if pick < 8 else "12")
    for x in range(32):
        for z in range(32):
            if not in_pond(x, z) and any(in_pond(x + dx, z + dz) for dx, dz in NEIGHBOURS):
                skin(c, x, z, "12")
                if (x + z) % 3 == 0:
                    skin(c, x, z, "13")


HUT_X0, HUT_X1, HUT_Z0, HUT_Z1 = 13, 19, 12, 18
RIDGE_Z = 15


def hut(c):
    x0, x1, z0, z1 = HUT_X0, HUT_X1, HUT_Z0, HUT_Z1
    for x in (13, 16, 19):                                              # stilts from the bed
        for z in (12, 15, 18):
            c.box(x, -9, z, x, -1, z, SPRUCE_LOG)
    c.box(x0, 0, z0, x1, 0, z1, SPRUCE)
    for x in range(x0 - 1, x1 + 2):                                     # slab deck ring
        c.set(x, 0, z0 - 1, SPRUCE_SLAB); c.set(x, 0, z1 + 1, SPRUCE_SLAB)
    for z in range(z0 - 1, z1 + 2):
        c.set(x0 - 1, 0, z, SPRUCE_SLAB); c.set(x1 + 1, 0, z, SPRUCE_SLAB)
    for x in range(x0, x1 + 1):                                         # floor beams
        c.set(x, -1, z0, "17:5"); c.set(x, -1, z1, "17:5")
    for z in range(z0, z1 + 1):
        c.set(x0, -1, z, "17:9"); c.set(x1, -1, z, "17:9")
    for y in (1, 2, 3):                                                 # walls
        for x in range(x0, x1 + 1):
            c.set(x, y, z0, SPRUCE); c.set(x, y, z1, SPRUCE)
        for z in range(z0, z1 + 1):
            c.set(x0, y, z, SPRUCE); c.set(x1, y, z, SPRUCE)
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        c.box(x, 1, z, x, 3, z, SPRUCE_LOG)
    for x in (15, 16, 17):                                              # windows north and south
        c.set(x, 2, z0, "102"); c.set(x, 2, z1, "102")
    for z in (14, 16):
        c.set(x1, 2, z, "102")
    c.set(x1, 1, 15, "102"); c.set(x1, 2, 15, "102")
    c.set(x0, 1, 15, "64:2"); c.set(x0, 2, 15, "64:8")                  # door west, onto the pier
    for x in range(x0 - 1, x1 + 2):                                     # roof: stairs up to a slab ridge
        c.set(x, 3, z0 - 1, "134:2"); c.set(x, 4, z0, "134:2"); c.set(x, 5, z0 + 1, "134:2"); c.set(x, 6, z0 + 2, "134:2")
        c.set(x, 3, z1 + 1, "134:3"); c.set(x, 4, z1, "134:3"); c.set(x, 5, z1 - 1, "134:3"); c.set(x, 6, z1 - 2, "134:3")
        c.set(x, 7, RIDGE_Z, "126:9")
    for x in range(x0 + 1, x1):                                         # ceiling
        for z in range(z0 + 1, z1):
            c.set(x, 4, z, SPRUCE)
    for x in (x0, x1):                                                  # gable fills
        for z, top in ((13, 4), (14, 5), (15, 6), (16, 5), (17, 4)):
            for y in range(4, top + 1):
                c.set(x, y, z, SPRUCE)
    c.set(x0 - 1, 8, RIDGE_Z, "85") if False else None
    c.set(x0, 8, RIDGE_Z, "85"); c.set(x1, 8, RIDGE_Z, "85")           # ridge finials
    # interior
    c.set(14, 1, 17, "26:2"); c.set(14, 1, 16, "26:10")                 # bed, head to the north
    c.set(18, 1, 17, "54:2"); c.set(18, 1, 13, "58"); c.set(17, 1, 13, "61:2")
    c.set(18, 2, 13, "140"); c.set(18, 1, 15, "118:3"); c.set(16, 1, 17, "17:0")
    c.set(15, 1, 13, "47"); c.set(15, 2, 13, "47"); c.set(14, 1, 13, "47")
    c.set(16, 3, 15, "85"); c.set(16, 2, 15, "89")                      # lamp hung from the ceiling
    for x in (15, 16, 17):
        c.set(x, 1, 15, "171:14") if x != 16 else c.set(x, 1, 15, "171:14")
    # deck rail, lamp posts, stacked gear
    for x in range(x0 - 1, x1 + 2):
        c.set(x, 1, z0 - 1, "85")
        if x not in (15, 16, 17):
            c.set(x, 1, z1 + 1, "85")
    for z in range(z0, z1 + 1):
        if z not in (15, 16):
            c.set(x0 - 1, 1, z, "85")
    for x, z in ((x0 - 1, z0 - 1), (x1 + 1, z0 - 1), (x0 - 1, z1 + 1), (x1 + 1, z1 + 1)):
        c.set(x, 2, z, "85"); c.set(x, 3, z, "89")
    c.set(14, 1, 19, "118:3"); c.set(18, 1, 19, "54:3"); c.set(18, 2, 19, "17:0"); c.set(16, 1, 19, "170:0")
    for z in (13, 15, 17):                                              # east deck: rod rack
        c.box(x1 + 1, 1, z, x1 + 1, 2, z, "85")
    c.set(x1 + 1, 1, 14, "35:6"); c.set(x1 + 1, 1, 16, "35:1")
    c.set(x1 + 1, 3, 13, "85") if False else None


def pier(c):
    for x in range(0, 13):
        c.set(x, 0, 15, SPRUCE)
        c.set(x, 0, 16, SPRUCE if x % 2 == 0 else SPRUCE_SLAB)
    for x in range(1, 12, 2):
        c.box(x, floor_of(x, 16), 16, x, -1, 16, SPRUCE_LOG)
        c.box(x, floor_of(x, 14), 14, x, -1, 14, SPRUCE_LOG)
    for x in range(4, 12, 2):                                           # rail on the north side
        c.set(x, 1, 14, "85")
    for x in range(3, 12):
        c.set(x, 1, 17, "85") if x % 2 == 0 else None
    for x in (3, 9):
        c.box(x, 1, 17, x, 2, 17, "85"); c.set(x, 3, 17, "89")
    c.set(4, 1, 15, "118:3"); c.set(5, 1, 15, "17:0"); c.set(5, 2, 15, "17:0")
    c.set(8, 1, 15, "54:3"); c.set(10, 1, 15, "170:0")


def reeds_and_lilies(c):
    for x, z in ((8, 12), (7, 17), (24, 11), (25, 18), (13, 21), (20, 9), (11, 10), (22, 21), (9, 20), (26, 14)):
        if in_pond(x, z) and 0.5 < pond_q(x, z) < 0.95 and (x, 0, z) not in c.blocks:
            bed = bed_of(x, z)
            c.box(x, bed, z, x, WATER_TOP, z, "3:0")
            for dy in range(1, 3 + (x + z) % 2):
                c.set(x, WATER_TOP + dy, z, "83")
    for x in range(32):
        for z in range(32):
            if not in_pond(x, z) and any(in_pond(x + dx, z + dz) for dx, dz in NEIGHBOURS) \
                    and (x * 5 + z * 3) % 3 == 0 and (x, base(x, z), z) not in c.blocks \
                    and not (14 <= x <= 18):
                for dy in range(2 + (x + z) % 2):
                    put(c, x, z, dy, "83")
    for x, z in ((9, 15), (12, 20), (21, 20), (24, 13), (10, 18), (13, 9), (19, 10), (22, 11), (8, 14), (11, 12),
                 (25, 16), (14, 21), (18, 21), (9, 11), (23, 19), (21, 8)):
        if in_pond(x, z) and (x, WATER_TOP + 1, z) not in c.blocks and (x, 0, z) not in c.blocks:
            c.set(x, WATER_TOP + 1, z, "111")


def boat(c):
    c.prop("rowboat", 14, WATER_TOP, 21)
    c.box(19, -9, 21, 19, 0, 21, SPRUCE_LOG)                            # mooring post
    c.set(19, 1, 21, "85")


def sunken(c):
    c.set(11, bed_of(11, 13) + 1, 13, "54:2"); c.set(12, bed_of(12, 13) + 1, 13, "13")
    c.set(11, bed_of(11, 14) + 1, 14, "13")
    c.set(22, bed_of(22, 16) + 1, 16, "17:4"); c.set(23, bed_of(23, 16) + 1, 16, "17:4")
    c.set(10, bed_of(10, 16) + 1, 16, "145:0")
    for x, z in ((14, 12), (18, 18), (23, 15)):
        c.set(x, bed_of(x, z), z, "169")


def drying_rack(c):
    """On the north-east knoll: two posts and a beam hung with fish."""
    for x in (23, 27):
        c.box(x, base(x, 6), 6, x, base(x, 6) + 3, 6, "85")
    b = base(25, 6)
    for x in range(23, 28):
        c.set(x, b + 4, 6, SPRUCE_SLAB)
    for x, colour in ((24, "35:1"), (25, "35:6"), (26, "35:1")):
        c.set(x, b + 3, 6, colour); c.set(x, b + 2, 6, "35:6" if x != 25 else "35:1")
    c.set(24, b + 1, 6, "35:6"); c.set(26, b + 1, 6, "35:6")
    put(c, 25, 8, 0, "17:5"); put(c, 26, 8, 0, "17:9")
    c.set(23, b, 8, "44:3") if False else None


def net_and_stores(c):
    """On the south-west rise: a cobweb net between poles, barrels, crates and a chest."""
    for x in (2, 8):
        c.box(x, base(x, 29), 29, x, base(x, 29) + 4, 29, "85")
    b = base(5, 29)
    for x in (3, 4, 5, 6, 7):
        for y in (1, 2, 3):
            c.set(x, b + y, 29, "30")
        c.set(x, b + 4, 29, SPRUCE_SLAB)
    put(c, 3, 25, 0, "17:0"); put(c, 3, 25, 1, "17:0"); put(c, 4, 25, 0, "17:0"); put(c, 5, 25, 0, "170:0")
    put(c, 5, 25, 1, "170:0"); put(c, 6, 25, 0, "54:3"); put(c, 7, 25, 0, "118:3"); put(c, 4, 26, 0, "17:9")
    put(c, 6, 31, 0, "17:0") if False else None


def firepit_and_wood(c):
    """On the south-east rise: a fire pit ringed by log seats, a wood stack and a chopping block."""
    px, pz = 24, 27
    c.set(px, ground(px, pz), pz, "87")
    put(c, px, pz, 0, "51")
    for dx, dz in ((1, 0), (-1, 0), (0, -1)):
        put(c, px + dx, pz + dz, 0, "44:3")
    put(c, 24, 29, 0, "17:9"); put(c, 25, 29, 0, "17:9"); put(c, 22, 28, 0, "17:8") if False else None
    for dx in (0, 1):
        for dz in (0, 1):
            for dy in (0, 1):
                put(c, 28 + dx, 24 + dz, dy, "17:5")
    put(c, 28, 24, 2, SPRUCE_SLAB); put(c, 29, 24, 2, SPRUCE_SLAB)
    put(c, 29, 28, 0, "17:0"); put(c, 29, 28, 1, "69:5") if False else None
    put(c, 27, 29, 0, "17:0")


def paths_and_lamps(c):
    for z in range(24, 32):                                             # gravel in from the south
        for x in (15, 16, 17):
            skin(c, x, z, "13" if (x + z) % 2 else "3:1")
    for x in range(18, 24):                                             # branch to the fire pit
        skin(c, x, 27, "13" if x % 2 else "3:1")
    for z in range(0, 8):                                               # and in from the north
        for x in (15, 16, 17):
            skin(c, x, z, "13" if (x + z) % 2 else "3:1")
    c.prop("lantern-post", 14, base(14, 25), 25)
    c.prop("lantern-post", 18, base(18, 6), 6)
    put(c, 19, 3, 0, "17:8"); put(c, 20, 3, 0, "17:8") if False else None   # a log bench beside the north path


def rocks(c):
    for x, z in ((3, 21), (29, 19), (11, 3), (21, 2)):
        put(c, x, z, 0, "48"); put(c, x + 1, z, 0, "48")
        put(c, x, z + 1, 0, "44:3")


def build():
    c = Chunk("fishing-hut", "Fisherman's Pond", "grass",
              "A stilted spruce hut over a deep pond in a dell, with a pier, a rowboat, nets, a drying rack, "
              "reeds and an olive on its knoll.", size=32)
    landform(c)
    pond(c)
    pier(c)
    hut(c)
    boat(c)
    sunken(c)
    drying_rack(c)
    net_and_stores(c)
    firepit_and_wood(c)
    paths_and_lamps(c)
    rocks(c)
    reeds_and_lilies(c)
    c.tree(6, 6, "small-olive-1")
    c.cover([(0, 0), (32, 0), (32, 32), (0, 32)], coverage=0.32, fernShare=0.3, flowerShare=0.2,
            tallShare=0.15, mushroomShare=0.05)
    return c
