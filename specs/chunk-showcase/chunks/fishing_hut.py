"""Fisherman's Pond: a stilted spruce hut over a deep pond with a pier, a rowboat, nets and a drying rack on the
bank, reed clumps, lily pads, a willow, and a sunken chest on the pond bed."""
from kit import Chunk

BED = -5            # top course of the pond bed
SPRUCE, SPRUCE_LOG, SPRUCE_SLAB, SPRUCE_STAIR = "5:1", "17:1", "126:1", "134"
NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def in_pond(x, z):
    return ((x - 7.5) / 8.6) ** 2 + ((z - 7.5) / 4.7) ** 2 <= 1.0


def shore(x, z):
    """A bank cell that touches the pond."""
    return not in_pond(x, z) and any(in_pond(x + dx, z + dz) for dx, dz in NEIGHBOURS)


def pond(c):
    """Cut the bed row by row, fill it with water, and line it with clay, gravel and mud."""
    for z in range(16):
        xs = [x for x in range(16) if in_pond(x, z)]
        if xs:
            c.lower(min(xs), z, max(xs), z, BED + 1)
    for x in range(16):
        for z in range(16):
            if not in_pond(x, z):
                continue
            c.box(x, BED + 1, z, x, -1, z, "9")
            pick = (x * 7 + z * 13) % 9
            c.set(x, BED, z, "82" if pick < 4 else "13" if pick < 7 else "3:1" if pick < 8 else "12")
            if any(not in_pond(x + dx, z + dz) for dx, dz in NEIGHBOURS):      # sandy shelf at the edge
                c.set(x, BED + 1, z, "12")
                c.set(x, BED + 2, z, "12")


def hut(c):
    for x, z in ((7, 3), (11, 3), (7, 7), (11, 7), (9, 3), (9, 7)):
        c.box(x, BED + 1, z, x, -1, z, SPRUCE_LOG)                      # stilts from the bed
    c.box(7, 0, 3, 11, 0, 7, SPRUCE)
    for x in range(6, 13):                                              # floor beams and a front deck
        c.set(x, 0, 8, SPRUCE_SLAB); c.set(x, 0, 2, SPRUCE_SLAB)
    for z in range(2, 9):
        c.set(6, 0, z, SPRUCE_SLAB); c.set(12, 0, z, SPRUCE_SLAB)
    for x in range(7, 12):
        c.set(x, -1, 3, "17:5"); c.set(x, -1, 7, "17:5")
    for z in range(3, 8):
        c.set(7, -1, z, "17:9"); c.set(11, -1, z, "17:9")
    for y in (1, 2, 3):                                                 # walls
        for x in range(7, 12):
            c.set(x, y, 3, SPRUCE); c.set(x, y, 7, SPRUCE)
        for z in range(4, 7):
            c.set(7, y, z, SPRUCE); c.set(11, y, z, SPRUCE)
    for x, z in ((7, 3), (11, 3), (7, 7), (11, 7)):
        c.box(x, 1, z, x, 3, z, SPRUCE_LOG)
    for x in (8, 10):                                                   # windows, shutters outside
        c.set(x, 2, 3, "102"); c.set(x, 2, 7, "102")
        c.set(x - 1 if x == 8 else x + 1, 2, 2, "96:12") if False else None
    c.set(9, 2, 3, "102"); c.set(9, 2, 7, "102")
    c.set(11, 2, 5, "102"); c.set(11, 1, 5, "102")
    for y in (2,):
        for x in (8, 10):
            c.set(x, y, 8, "96:13") if False else None
    c.set(7, 1, 5, "64:2"); c.set(7, 2, 5, "64:8")                      # door west, onto the pier
    # roof along x
    for x in range(6, 13):
        c.set(x, 3, 2, "134:2"); c.set(x, 3, 8, "134:3")
        c.set(x, 4, 3, "134:2"); c.set(x, 4, 7, "134:3")
        c.set(x, 5, 4, "134:2"); c.set(x, 5, 6, "134:3")
        c.set(x, 6, 5, SPRUCE_SLAB)
    for x in range(7, 12):
        c.set(x, 4, 4, SPRUCE); c.set(x, 4, 6, SPRUCE)
    for x in (7, 11):
        c.set(x, 4, 5, SPRUCE); c.set(x, 5, 5, SPRUCE)
    for z in (4, 5, 6):                                                 # log gable beams
        c.set(6, 4, z, None)
    c.set(5, 6, 5, "85")                                                # roof finial
    c.set(13, 6, 5, "85")
    # interior
    c.set(8, 1, 6, "26:2"); c.set(8, 1, 5, "26:10")
    c.set(10, 1, 6, "54:2"); c.set(10, 1, 4, "58"); c.set(9, 1, 4, "61:2")
    c.set(10, 1, 5, "118:3"); c.set(9, 1, 6, "17:0")
    c.set(9, 3, 5, "85"); c.set(9, 2, 5, "89")                          # glowstone lamp hung from the ridge
    c.set(9, 4, 5, "85")
    c.set(10, 2, 4, "140"); c.set(8, 2, 4, "47")
    # front deck: rail, lamp post, stacked gear
    for x in range(6, 13):
        if x not in (8, 9, 10):
            c.set(x, 1, 8, "85")
    c.set(6, 1, 2, "85"); c.set(12, 1, 2, "85")
    c.set(12, 2, 8, "85"); c.set(12, 3, 8, "89")
    c.set(6, 2, 8, "85"); c.set(6, 3, 8, "89")
    c.set(8, 1, 8, "118:3"); c.set(10, 1, 8, "54:3"); c.set(10, 2, 8, "17:0")
    c.set(9, 1, 8, "170:0")
    # east deck: rod rack
    for z in (3, 5, 7):
        c.box(12, 1, z, 12, 2, z, "85")
    c.box(12, 3, 3, 12, 3, 7, SPRUCE_SLAB) if False else None
    c.set(12, 1, 4, "35:6"); c.set(12, 1, 6, "35:1")
    c.set(12, 3, 4, "85"); c.set(12, 3, 5, "85") if False else None


def pier(c):
    for x in range(0, 6):
        c.set(x, 0, 5, SPRUCE)
        c.set(x, 0, 4, SPRUCE_SLAB if x % 2 else SPRUCE)
    for x in range(0, 6, 2):
        c.box(x, BED + 1, 4, x, -1, 4, SPRUCE_LOG)
        c.box(x, BED + 1, 6, x, -1, 6, SPRUCE_LOG) if False else None
    for x in (1, 3, 5):
        c.box(x, 1, 3, x, 1, 3, "85") if False else None
    c.box(1, 1, 3, 1, 2, 3, "85") if False else None
    for x in range(0, 6):                                               # rail on the south side only
        c.set(x, 1, 6, "85") if x % 2 == 0 else None
    for x in (0, 2, 4):
        c.set(x, 0, 6, SPRUCE_SLAB) if False else None
    c.set(0, 1, 4, "118:3"); c.set(1, 1, 4, "17:0"); c.set(1, 2, 4, "17:0")
    c.set(4, 1, 4, "54:3")
    c.set(2, 1, 6, "85"); c.set(2, 2, 6, "89")                          # lamp
    # walkway planks are one block wide at z 4..5; boat tied at the end


def bank(c):
    # drying rack with fish on the north-east bank
    for x in (10, 14):
        c.box(x, 0, 1, x, 3, 1, "85")
    c.box(10, 4, 1, 14, 4, 1, SPRUCE_SLAB)
    for x, colour in ((11, "35:1"), (12, "35:6"), (13, "35:1")):
        c.set(x, 3, 1, colour); c.set(x, 2, 1, "35:6" if x != 12 else "35:1")
    c.set(11, 1, 1, "35:6"); c.set(13, 1, 1, "35:6")
    c.set(12, 0, 2, "17:5") if False else None
    # net: cobweb between poles on the south-west bank
    for x in (1, 5):
        c.box(x, 0, 13, x, 4, 13, "85")
    for x in (2, 3, 4):
        for y in (1, 2, 3):
            c.set(x, y, 13, "30")
        c.set(x, 4, 13, SPRUCE_SLAB)
    # barrels, crates, a chest
    c.set(1, 0, 15, "17:0"); c.set(1, 1, 15, "17:0"); c.set(2, 0, 15, "17:0"); c.set(3, 0, 15, "170:0")
    c.set(3, 1, 15, "170:0"); c.set(4, 0, 15, "54:3"); c.set(5, 0, 15, "118:3")
    c.set(4, 0, 14, "17:9"); c.set(3, 0, 14, "17:9") if False else None
    # fire pit with log seats beside the path
    c.set(11, -1, 14, "87"); c.set(11, 0, 14, "51")
    for dx, dz in ((1, 0), (-1, 0), (0, -1)):
        c.set(11 + dx, 0, 14 + dz, "44:3")
    c.set(11, 0, 15, "17:9"); c.set(12, 0, 15, "17:9")
    c.set(11, 1, 14, "85") if False else None
    # stacked wood and a chopping block on the south-east bank
    c.box(13, 0, 13, 14, 1, 13, "17:5"); c.box(13, 0, 14, 14, 0, 14, "17:5")
    c.set(13, 2, 13, SPRUCE_SLAB); c.set(14, 2, 13, SPRUCE_SLAB)
    c.set(15, 0, 12, "17:0") if False else None
    c.set(14, 0, 15, "17:0"); c.set(14, 1, 15, "69:5")
    # gravel path in from the south
    for z in range(13, 16):
        for x in (7, 8, 9):
            c.set(x, -1, z, "13" if (x + z) % 2 else "3:1")
    c.set(6, 0, 14, "85"); c.set(6, 1, 14, "85"); c.set(6, 2, 14, "89")
    c.prop("lantern-post", 0, 0, 2)
    # north bank: log pile
    c.box(14, 0, 4, 15, 0, 4, "17:5") if False else None
    c.set(3, 0, 0, "17:0") if False else None
    c.set(8, 0, 1, "17:0") if False else None


def reeds_and_lilies(c):
    """Reed clumps on little silt islets in the shallows, sugar cane on the bank, lily pads on open water."""
    for x, z in ((2, 2), (1, 6), (13, 3), (14, 6), (13, 11), (3, 11), (6, 12), (11, 12), (12, 2), (4, 3)):
        if in_pond(x, z) and c.blocks.get((x, 0, z)) is None and c.blocks.get((x, -1, z)) == (9, 0):
            c.set(x, -2, z, "3:0"); c.set(x, -1, z, "3:0")
            for dy in range(0, 2 + (x + z) % 2):
                c.set(x, dy, z, "83")
    for x in range(16):
        for z in range(16):
            if shore(x, z) and (x * 5 + z * 3) % 3 == 0 and (x, 0, z) not in c.blocks:
                for dy in range(2 + (x + z) % 2):
                    c.set(x, dy, z, "83")
    for x, z in ((3, 7), (5, 9), (9, 10), (12, 8), (5, 5), (10, 4), (13, 5), (7, 11), (9, 12), (4, 8), (12, 6),
                 (10, 8), (8, 9), (6, 8), (4, 6), (11, 11), (3, 9)):
        if in_pond(x, z) and (x, 0, z) not in c.blocks and c.blocks.get((x, -1, z)) == (9, 0):
            c.set(x, 0, z, "111")


def boat(c):
    c.prop("rowboat", 9, -1, 10, 0)
    c.set(8, 0, 10, "85") if False else None
    c.set(13, 0, 9, "85"); c.set(13, -1, 9, "17:1"); c.set(13, -2, 9, "17:1")   # mooring post
    c.set(14, 0, 10, "50:5") if False else None


def rocks(c):
    """Mossy cobble piles on the bank, where a boulder does not fit the narrow ground."""
    for x, z in ((12, 12), (5, 12), (2, 3), (14, 3)):
        c.set(x, 0, z, "48"); c.set(x + 1 if x < 14 else x - 1, 0, z, "48:0")
        c.set(x, 1, z, "44:3") if (x + z) % 2 else None
    c.set(5, 0, 11, "44:3") if False else None


def sunken(c):
    c.set(5, BED + 1, 7, "54:2"); c.set(6, BED + 1, 7, "13"); c.set(5, BED + 1, 8, "13")
    c.set(10, BED + 1, 10, "17:4"); c.set(11, BED + 1, 10, "17:4")
    c.set(4, BED + 1, 9, "145:0"); c.set(8, BED + 1, 12, "169"); c.set(7, BED + 1, 5, "169")
    c.set(12, BED + 1, 9, "170:0") if False else None


def build():
    c = Chunk("fishing-hut", "Fisherman's Pond", "grass",
              "A stilted spruce hut over a deep pond with a pier, a rowboat, nets, a drying rack, reeds and a willow.")
    pond(c)
    pier(c)
    hut(c)
    bank(c)
    boat(c)
    rocks(c)
    sunken(c)
    reeds_and_lilies(c)
    c.tree(3, 3, "small-olive-3")
    c.cover([(0, 0), (16, 0), (16, 3), (0, 3)], coverage=0.5, fernShare=0.3, flowerShare=0.1, mushroomShare=0.1)
    c.cover([(0, 12), (16, 12), (16, 16), (0, 16)], coverage=0.5, fernShare=0.3, flowerShare=0.1, tallShare=0.3)
    return c
