"""A covered timber bridge with a snow-capped roof over a dry gully; a hollow tunnel runs under the deck."""
from mc import B

NAME = "The Snow Shed Bridge"
KIND = "structure"

QUARTZ_STAIRS = 156


def build(c):
    # the dry gully floor, painted cobble and stone
    for x in range(2, 9):
        for z in range(0, 11):
            c.set(x, -1, z, B.COBBLE if (x * 3 + z) % 4 else B.MOSSY, 0)
    # the west embankment: a rocky ramp, x0 y0, x1 y0..1, x2 y0..2
    for x, h in ((0, 0), (1, 1), (2, 2)):
        c.fill(x, 0, 2, x, h, 8, B.STONE, 0)
        c.fill(x, h, 2, x, h, 8, B.COBBLE)
        c.set(x, h + 1, 2, B.SNOW_LAYER)
        c.set(x, h + 1, 8, B.SNOW_LAYER)
    # the east embankment: a sheer cliff, x9..10, y0..3
    c.fill(9, 0, 2, 10, 3, 8, B.STONE, 0)
    for z in range(2, 9):
        c.set(9, 3, z, B.PLANKS, 1)
        c.set(10, 3, z, B.PLANKS, 1)
        if z % 2:
            c.set(10, 1, z, B.COBBLE)
    c.fill(10, 0, 2, 10, 3, 2, B.MOSSY)
    c.fill(10, 2, 8, 10, 3, 8, B.MOSSY)
    # the deck, y3, z3..7, x3..8
    c.fill(3, 3, 3, 8, 3, 7, B.PLANKS, 1)
    # the tunnel under the deck: stone brick walls at z3 and z7, floor open
    c.fill(3, 0, 3, 8, 2, 3, B.STONEBRICK, 0)
    c.fill(3, 0, 7, 8, 2, 7, B.STONEBRICK, 0)
    c.fill(3, 0, 4, 8, 2, 6, B.AIR)
    c.fill(3, 0, 7, 3, 1, 7, B.AIR)                      # south doorway
    c.fill(7, 0, 3, 7, 1, 3, B.AIR)                      # north doorway
    c.fill(2, 0, 5, 2, 1, 5, B.AIR)                      # a manhole from the west bank
    # inside the tunnel: the pier with its ladder
    c.fill(5, 0, 5, 5, 2, 5, B.LOG, 1)
    for y in range(0, 4):
        c.set(5, y, 4, B.LADDER, 2)
    c.set(5, 3, 4, B.LADDER, 2)
    c.set(4, 0, 6, B.HAY)
    c.set(7, 0, 6, B.PLANKS, 1)
    c.set(7, 1, 6, B.PLANKS, 1)
    c.set(4, 2, 5, B.GLOWSTONE)
    c.set(7, 2, 5, B.GLOWSTONE)
    # the covered span: walls y4..7, log posts, small slit windows, x2..10
    for x in range(2, 11):
        for z in (3, 7):
            c.fill(x, 4, z, x, 7, z, B.PLANKS, 1)
        if x % 2 == 0:
            for z in (3, 7):
                c.fill(x, 4, z, x, 7, z, B.LOG, 1)
        else:
            for z in (3, 7):
                c.set(x, 6, z, B.AIR)
    # the roof: eaves at z2/z8, three courses and a ridge, snow on the upper ones
    for x in range(1, 11):
        c.set(x, 7, 2, B.SPRUCE_STAIRS, 2)
        c.set(x, 8, 3, B.SPRUCE_STAIRS, 2)
        c.set(x, 9, 4, QUARTZ_STAIRS, 2)
        c.set(x, 7, 8, B.SPRUCE_STAIRS, 3)
        c.set(x, 8, 7, B.SPRUCE_STAIRS, 3)
        c.set(x, 9, 6, QUARTZ_STAIRS, 3)
        c.set(x, 10, 5, B.SNOW)
        c.fill(x, 8, 4, x, 8, 6, B.AIR)
        c.set(x, 9, 5, B.AIR)
    c.fill(2, 8, 4, 2, 8, 6, B.PLANKS, 2)
    c.fill(10, 8, 4, 10, 8, 6, B.PLANKS, 2)
    c.set(2, 9, 5, B.PLANKS, 2)
    c.set(10, 9, 5, B.PLANKS, 2)
    # the rafter loft: a floor at y7 over the corridor, a post and ladder up from the deck
    c.fill(3, 7, 4, 9, 7, 6, B.PLANKS, 5)
    for x in (4, 6, 8):
        c.fill(x, 7, 4, x, 7, 6, B.LOG, 9)
    c.fill(3, 4, 6, 3, 7, 6, B.LOG, 1)
    for y in range(4, 8):
        c.set(3, y, 5, B.LADDER, 2)
    c.set(3, 7, 5, B.LADDER, 2)
    # the ends: open portals, x2 and x10, z4..6, y4..7 already open (walls only at z3, z7)
    # a pair of tall stone-and-snow outcrops on the north and south of the east cliff
    c.set(0, 1, 2, B.SNOW_LAYER)
    c.set(0, 1, 8, B.SNOW_LAYER)
    # a bench and crates on the deck
    c.set(6, 4, 4, B.WOOD_SLAB, 1)
    c.set(8, 4, 6, B.PLANKS, 1)
    # snow patches on the cliff top beyond the roof
    for z in range(2, 9):
        c.set(9, 4, z, B.AIR)
    c.fill(9, 4, 2, 9, 4, 2, B.SNOW_LAYER)
    # signpost at the west foot
    c.fill(0, 1, 4, 0, 2, 4, B.FENCE)
    c.set(0, 3, 4, B.WOOD_SLAB, 1)
