"""The Gingerbread House: walls of brown gingerbread, white icing along every edge and dripping off the eaves, a
roof of chocolate tiles studded with sweets, a candy-cane porch, and a chimney of stacked sweets. A ladder of
icing climbs the west gable to the ridge."""
from mc import B

NAME = "The Gingerbread House"
KIND = "house"

GINGER = (B.HARDENED_CLAY, 0)
DARK = (B.HARDENED_CLAY, 0)
ICING = (B.WOOL, 0)
ROOF = B.DARK_OAK_STAIRS
SWEETS = [(B.WOOL, 14), (B.WOOL, 5), (B.WOOL, 4), (B.WOOL, 6), (B.WOOL, 3), (B.WOOL, 1)]
X0, X1, Z0, Z1 = 1, 9, 2, 8
TOP = 4


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            ex, ez = x in (X0, X1), z in (Z0, Z1)
            if not (ex or ez):
                c.set(x, -1, z, B.PLANKS, 1)                     # a wooden floor inside
                continue
            for y in range(0, TOP + 1):
                corner = ex and ez
                window = y in (1, 2) and ((ez and x in (3, 7)) or (ex and z == 5))
                c.set(x, y, z, *(ICING if corner or y == TOP else (B.STAINED_PANE, 4) if window else GINGER))
    for x in (3, 7):                                             # icing round the windows
        for z in (Z0, Z1):
            c.set(x, 3, z, *ICING)
    for x in (5,):                                               # the front door, south, and a back door north
        c.set(x, 0, Z1, B.AIR); c.set(x, 1, Z1, B.AIR)
        c.set(x, 0, Z0, B.AIR); c.set(x, 1, Z0, B.AIR)
    c.set(5, 2, Z1, *ICING)
    # the roof: chocolate tiles from both eaves up to an iced ridge, overhanging the walls by one
    for i in range(4):
        for x in range(X0 - 1, X1 + 2):
            c.set(x, TOP + 1 + i, Z0 - 1 + i, ROOF, 2)
            c.set(x, TOP + 1 + i, Z1 + 1 - i, ROOF, 3)
    for x in range(X0 - 1, X1 + 2):
        c.set(x, TOP + 5, 5, *ICING)                             # the iced ridge
        c.set(x, TOP + 4, 5, *GINGER)
        c.set(x, TOP, Z0 - 1, *ICING) if x % 2 else None         # icing dripping off the eaves
        c.set(x, TOP, Z1 + 1, *ICING) if x % 2 == 0 else None
    for i in range(4):                                           # the gable ends, gingerbread with an iced edge
        for z in range(Z0 + i, Z1 - i + 1):
            for x in (X0, X1):
                c.set(x, TOP + 1 + i, z, *(ICING if z in (Z0 + i, Z1 - i) else GINGER))
    for k, (x, z) in enumerate([(2, 3), (4, 7), (6, 3), (8, 7), (3, 6), (7, 4)]):   # sweets on the tiles
        y = TOP + 1 + min(z - (Z0 - 1), (Z1 + 1) - z)
        c.set(x, y, z, *SWEETS[k % len(SWEETS)])
    # the chimney of stacked sweets on the north slope
    for k, y in enumerate(range(TOP + 3, TOP + 8)):
        c.set(7, y, 4, *SWEETS[k % len(SWEETS)])
    # the ladder of icing up the west gable to the ridge
    for y in range(0, TOP + 6):
        c.set(X0 - 1, y, 5, B.LADDER, 4)
    for y in range(TOP + 1, TOP + 6):
        c.set(X0, y, 5, *ICING)
    # the candy-cane porch: red and white posts holding a slab roof over the front door
    for x in (3, 7):
        for y in range(0, 3):
            c.set(x, y, 10, *(SWEETS[0] if y % 2 else ICING))
    for x in range(3, 8):
        c.set(x, 3, 9, B.WOOD_SLAB, 5)
        c.set(x, 3, 10, B.WOOD_SLAB, 5)
    # the attic: a floor across the top of the walls, a ladder up to it inside the back wall, a sweet-jar store
    for x in range(X0 + 1, X1):
        for z in range(Z0 + 1, Z1):
            if (x, z) != (3, Z0 + 1):
                c.set(x, TOP, z, B.PLANKS, 1)
    for y in range(0, TOP + 1):
        c.set(3, y, Z0 + 1, B.LADDER, 3)
    c.set(7, TOP + 1, 5, B.CHEST)
    c.set(2, TOP + 1, 5, *SWEETS[1])
    # gumdrops and a lollipop in the garden
    for k, (x, z) in enumerate([(0, 1), (10, 1), (10, 9), (0, 10)]):
        c.set(x, 0, z, *SWEETS[(k + 2) % len(SWEETS)])
    c.set(10, 0, 5, B.FENCE)
    c.set(10, 1, 5, B.FENCE)
    c.set(10, 2, 5, *SWEETS[3])
