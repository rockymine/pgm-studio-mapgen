"""An enormous lace-up hiking boot, toe to the south, cuff open to the sky; hide in the toe or down the shaft."""
from mc import B

NAME = "The Giant Hiking Boot"
KIND = "sculpture"

T = [12, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3]       # top block of the upper, by z


def build(c):
    LEATHER = (B.STAINED_CLAY, 12)
    # sole: black clay, with a tread of cobble, a thicker heel
    for x in range(1, 10):
        for z in range(0, 11):
            c.set(x, 0, z, B.STAINED_CLAY, 15) if (x + z) % 3 else c.set(x, 0, z, B.COAL_BLOCK)
    c.fill(1, 1, 0, 9, 1, 2, B.STAINED_CLAY, 7)       # heel block
    # the upper
    for z in range(0, 11):
        for x in range(2, 9):
            top = T[z]
            c.fill(x, 1, z, x, top - 1, z, *LEATHER)
    # cheeks up to the rim at the back
    for x in (2, 8):
        c.fill(x, 1, 0, x, 12, 3, *LEATHER)
    c.fill(2, 1, 0, 8, 12, 0, *LEATHER)
    # toe cap darker
    for z in (8, 9, 10):
        for x in range(2, 9):
            c.fill(x, 1, z, x, T[z] - 1, z, B.STAINED_CLAY, 7 if z == 10 else 12)
    # the tongue slope: spruce stairs rising north, between the cheeks, with white laces
    for z in range(4, 11):
        for x in range(3, 8):
            c.set(x, T[z], z, B.SPRUCE_STAIRS, 3)
        c.set(2, T[z], z, B.STAINED_CLAY, 12)
        c.set(8, T[z], z, B.STAINED_CLAY, 12)
    for z in (5, 7, 9):
        for x in range(3, 8):
            c.set(x, T[z], z, B.WOOL, 0)
        c.set(2, T[z] + 1, z, B.IRON_BARS)
        c.set(8, T[z] + 1, z, B.IRON_BARS)
    # the lace ends dangle
    # the interior: foot cavity and the shaft down the cuff
    for z in range(1, 10):
        top = T[z] if z <= 3 else T[z] - 1
        c.fill(3, 1, z, 7, top, z, B.AIR)
    # fleece collar round the cuff
    c.fill(2, 12, 0, 8, 12, 0, B.WOOL, 0)
    for x in (2, 8):
        c.fill(x, 12, 0, x, 12, 3, B.WOOL, 0)
    # doors: the toe's mouse hole and a side door on the east cheek
    c.fill(5, 1, 10, 5, 2, 10, B.AIR)
    c.fill(4, 1, 8, 6, 5, 8, *LEATHER)
    c.fill(6, 1, 9, 6, 2, 9, *LEATHER)
    # ladder up the heel wall to the collar
    for y in range(1, 13):
        c.set(3, y, 1, B.LADDER, 3)
    # a foot-sock inside for colour and a lantern
    c.fill(4, 1, 7, 6, 1, 8, B.CARPET, 14)
    c.set(7, 1, 2, B.CHEST, 4)
    # side stitching and mud
    for z in range(2, 10):
        c.set(2, 1 + (z % 3), z, B.STAINED_CLAY, 1) if z % 2 == 0 and T[z] > 3 else None
        c.set(8, 1 + ((z + 1) % 3), z, B.STAINED_CLAY, 1) if z % 2 == 1 and z != 6 and T[z] > 3 else None
    for (x, z) in ((3, 10), (6, 10), (7, 9), (2, 8)):
        c.set(x, 1, z, B.DIRT, 1) if (x, z) != (2, 8) else None
    # pebbles stuck in the tread
