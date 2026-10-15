"""The Bandstand: an octagonal stage on a stone skirt, eight white columns, a railing, and a copper roof stepping up
to a gold finial. A golden tuba waits on its stand. Steps climb to the stage from the south; a trap in the stage
floor lets a hider down under it; a ladder up the east column reaches the eaves, and the roof steps to the top."""
from mc import B

NAME = "The Bandstand"
KIND = "structure"

C = 5
SKIRT, FLOOR = (B.STONEBRICK, 0), (B.PLANKS, 1)
COLUMN = (B.QUARTZ, 2)                                           # quartz pillar, upright
COPPER, COPPER_DARK, GOLD = (B.STAINED_CLAY, 9), (B.WOOL, 9), (B.GOLD_BLOCK, 0)
POSTS = [(2, 3), (2, 7), (8, 3), (8, 7), (3, 2), (7, 2), (3, 8), (7, 8)]


def m(x, z):
    """The octagon's radius of a cell."""
    dx, dz = abs(x - C), abs(z - C)
    return max(dx, dz, (dx + dz) / 1.41)


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for x in range(11):
        for z in range(11):
            r = m(x, z)
            if r <= 3.6:
                c.set(x, 2, z, *FLOOR)                           # the stage at y 2, hollow under it
                if r > 2.6:
                    c.set(x, 0, z, *SKIRT)                       # the skirt round the space under the stage
                    c.set(x, 1, z, *((B.STONEBRICK, 3) if (x + z) % 2 else SKIRT))   # carved panels
                    if r > 3.0 and (x, z) not in POSTS and not (4 <= x <= 6 and z == 8):
                        c.set(x, 3, z, B.FENCE)                  # the railing
            if 1.5 < r <= 4.6 and (x + z) % 3 == 0:
                c.set(x, -1, z, B.GRAVEL)                        # a gravel ring round it
    for y in range(0, 3):                                        # a trap in the stage floor, a ladder down under it
        c.set(3, y, 6, B.LADDER, 5)
    for x in range(4, 7):                                        # steps up from the south
        c.set(x, 0, 10, B.STONEBRICK_STAIRS, 3)
        c.set(x, 1, 9, B.STONEBRICK_STAIRS, 3)
        c.set(x, 0, 9, *SKIRT)
    for x, z in POSTS:                                           # the columns
        for y in range(3, 7):
            c.set(x, y, z, *COLUMN)
    # the copper roof: a stepped octagon, darker at each eave, a gold finial on top
    for y, rad in ((7, 4.0), (8, 3.0), (9, 2.0), (10, 1.0)):
        for x in range(11):
            for z in range(11):
                r = m(x, z)
                if r <= rad:
                    c.set(x, y, z, *(COPPER_DARK if r > rad - 1 else COPPER))
    c.set(C, 11, C, *GOLD)
    c.set(C, 12, C, B.FENCE)
    c.set(C, 13, C, B.GOLD_BLOCK)
    # the tuba on its stand at the back of the stage, and music stands
    c.set(5, 3, 4, B.FENCE)
    c.set(5, 4, 4, *GOLD)
    c.set(5, 5, 4, *GOLD)
    c.set(6, 5, 4, *GOLD)
    c.set(6, 6, 4, B.HOPPER if hasattr(B, "HOPPER") else B.GOLD_BLOCK)
    for x in (3, 7):
        c.set(x, 3, 5, B.FENCE)
        c.set(x, 4, 5, B.WOOD_SLAB, 5)
    # the ladder up the east column's outer face to the eaves
    for y in range(0, 8):
        c.set(9, y, 7, B.LADDER, 5)
    c.set(8, 0, 7, *SKIRT); c.set(8, 1, 7, *SKIRT); c.set(8, 2, 7, *FLOOR)
    # benches and lamps round the lawn
    for x, z in ((0, 0), (10, 0), (0, 10), (10, 10)):
        c.set(x, 0, z, B.FENCE)
        c.set(x, 1, z, B.FENCE)
        c.set(x, 2, z, B.GLOWSTONE)
    for x in (1, 2):
        c.set(x, 0, 5, B.WOOD_SLAB, 1)
    c.set(10, 0, 4, B.WOOD_SLAB, 1)
