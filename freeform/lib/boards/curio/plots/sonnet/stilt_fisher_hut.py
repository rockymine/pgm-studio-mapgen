"""A fisherman's hut on tall piles over a pond, with a jetty, a rowing boat and a net loft in the gable."""
from mc import B

NAME = "The Stilt Fisher Hut"
KIND = "house"


def build(c):
    # the pond: clay bed, one block of still water, stone rim, grass shore south
    c.fill(0, -1, 0, 10, -1, 9, B.CLAY)
    c.fill(0, 0, 0, 10, 0, 9, B.WATER)
    for x in range(0, 11):
        c.set(x, 0, 0, B.COBBLE) if x % 2 == 0 else c.set(x, 0, 0, B.MOSSY)
    for z in range(0, 10):
        c.set(0, 0, z, B.COBBLE if z % 2 == 0 else B.MOSSY)
        c.set(10, 0, z, B.COBBLE if z % 2 == 0 else B.MOSSY)
    # reeds and lilies
    for (x, z) in ((1, 2), (1, 5), (9, 1), (9, 6), (2, 8)):
        c.set(x, 0, z, B.WATER)
    # the platform: dark oak planks on piles
    c.fill(2, 4, 1, 10, 4, 8, B.PLANKS, 5)
    for x in (2, 6, 10):
        for z in (1, 4, 8):
            c.fill(x, 0, z, x, 3, z, B.LOG, 1)
    # cross bracing (fence) between the piles
    for x in (4, 8):
        for z in (1, 8):
            c.fill(x, 1, z, x, 3, z, B.FENCE)
    # platform rail on the south edge and sides
    for x in range(2, 11):
        c.set(x, 5, 8, B.FENCE) if x not in (6,) else None
    for z in range(1, 9):
        c.set(2, 5, z, B.FENCE) if z not in (4,) else None
        c.set(10, 5, z, B.FENCE) if z not in (4,) else None
    # the hut: spruce plank walls with log posts, hollow
    c.fill(3, 5, 2, 9, 8, 7, B.PLANKS, 1)
    c.fill(4, 5, 3, 8, 7, 6, B.AIR)
    for x in (3, 9):
        for z in (2, 7):
            c.fill(x, 5, z, x, 8, z, B.LOG, 1)
    # attic floor and ladder up through a hole
    c.fill(4, 8, 3, 8, 8, 6, B.PLANKS, 1)
    c.set(5, 8, 5, B.AIR)
    # ladder attached on the south wall interior at (5, y, 6): wall at (5, y, 7)
    for y in range(5, 9):
        c.set(5, y, 6, B.LADDER, 2)
    c.set(5, 8, 6, B.LADDER, 2)
    # roof: ridge along z, gables north and south; wall top y8, roof from y8
    for x, y in ((2, 8), (3, 9), (4, 10), (5, 11)):
        c.fill(x, y, 1, x, y, 8, B.SPRUCE_STAIRS, 0)
        c.fill(12 - x, y, 1, 12 - x, y, 8, B.SPRUCE_STAIRS, 1)
    c.fill(6, 12, 1, 6, 12, 8, B.WOOD_SLAB, 1)
    for z in (2, 7):
        c.fill(4, 9, z, 8, 9, z, B.PLANKS, 2)
        c.fill(5, 10, z, 7, 10, z, B.PLANKS, 2)
        c.set(6, 11, z, B.PLANKS, 2)
    # hide the tops: fill so the attic is a room (y9..11)
    # north gable door onto the net balcony
    c.fill(6, 9, 2, 6, 10, 2, B.AIR)
    c.fill(5, 8, 1, 7, 8, 1, B.WOOD_SLAB, 1)
    for x in (5, 7):
        c.set(x, 9, 1, B.FENCE)
    # the south door and windows
    c.fill(6, 5, 7, 6, 6, 7, B.AIR)
    for (x, z) in ((4, 7), (8, 7), (3, 4), (9, 5)):
        c.set(x, 6, z, B.PANE)
    c.fill(3, 6, 4, 3, 6, 5, B.PANE)
    c.fill(9, 6, 4, 9, 6, 5, B.PANE)
    # inside: bunk, table, lamp
    c.set(8, 5, 3, B.WOOL, 14)
    c.set(8, 5, 4, B.WOOL, 0)
    c.set(4, 5, 4, B.CRAFTING)
    c.set(4, 5, 5, B.CHEST, 5)
    c.set(8, 5, 6, B.CAULDRON)
    c.set(8, 7, 4, B.TORCH, 2)
    # attic: net drying frames and a hammock-like carpet
    c.fill(5, 9, 5, 5, 9, 5, B.AIR)
    c.set(7, 9, 4, B.HAY)
    c.set(7, 9, 5, B.HAY)
    # nets hung on the east side of the hut: iron bars
    for y in range(5, 9):
        c.set(10, y, 3, B.IRON_BARS)
        c.set(10, y, 5, B.IRON_BARS)
    # the jetty: slabs on the water from the shore to the south pile ladder
    for z in range(6, 10):
        c.set(6, 0, z, B.PLANKS, 1)
        c.set(7, 0, z, B.PLANKS, 1)
    c.fill(5, 0, 9, 5, 0, 9, B.WOOD_SLAB, 1)
    c.set(5, 1, 9, B.FENCE)
    c.set(8, 1, 9, B.FENCE)
    # the ladder up the south pile of the platform (pile at (6, y, 8))
    for y in range(0, 5):
        c.set(6, y, 9, B.LADDER, 3)
    c.set(6, 5, 9, B.AIR)
    # a rowing boat east of the jetty
    c.set(8, 0, 6, B.SPRUCE_STAIRS, 2)
    c.set(8, 0, 7, B.PLANKS, 5)
    c.set(8, 0, 8, B.PLANKS, 5)
    c.set(9, 0, 7, B.PLANKS, 5)
    c.set(9, 0, 8, B.PLANKS, 5)
    c.set(8, 0, 9, B.SPRUCE_STAIRS, 3)
    c.set(9, 0, 6, B.SPRUCE_STAIRS, 2)
    c.set(9, 0, 9, B.SPRUCE_STAIRS, 3)
    # stepping stones to the west pile and a stair of crates
    c.set(3, 0, 6, B.COBBLE)
    c.set(2, 0, 6, B.COBBLE)
    c.set(3, 1, 8, B.HAY)
    c.set(2, 1, 8, B.PLANKS, 1)
    c.set(2, 2, 8, B.WOOD_SLAB, 1)
    # lantern pole
    c.set(10, 5, 8, B.FENCE)
    c.set(10, 6, 8, B.FENCE)
    c.set(10, 7, 8, B.GLOWSTONE)
    # weathervane
    c.set(6, 13, 4, B.FENCE)
    c.set(6, 14, 4, B.FENCE)
    c.set(6, 14, 5, B.WOOL, 14)
