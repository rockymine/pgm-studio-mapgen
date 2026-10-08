"""A cottage hung from a floating meadow slab, roof and chimney pointing at the ground."""
from mc import B

NAME = "The Upside-Down House"
KIND = "house"


def build(c):
    # the sky meadow: a plank slab, grassed on top, on four log pillars
    c.fill(0, 12, 0, 10, 12, 10, B.PLANKS, 1)
    c.fill(1, 13, 1, 9, 13, 9, B.GRASS)
    for x in (0, 10):
        for z in (0, 10):
            c.fill(x, 0, z, x, 12, z, B.LOG, 1)
            c.set(x, 13, z, B.LOG, 1)
    for t in range(1, 10):
        if t % 2 == 1:
            for (x, z) in ((t, 0), (t, 10), (0, t), (10, t)):
                c.set(x, 13, z, B.FENCE)
    # ladder up the west pillar to a hole in the meadow
    for y in range(0, 14):
        c.set(1, y, 0, B.LADDER, 5)
    c.set(1, 13, 0, B.LADDER, 5)
    c.set(1, 12, 0, B.LADDER, 5)
    # meadow furniture
    for x in (3, 4, 6, 7):
        c.set(x, 14, 3, B.FLOWER, (x % 4) + 4)
    c.fill(7, 13, 7, 8, 13, 8, B.DIRT, 1)
    c.set(7, 14, 7, B.RED_MUSHROOM)
    c.set(8, 14, 8, B.BROWN_MUSHROOM)
    c.set(3, 14, 7, B.FENCE)
    c.set(3, 15, 7, B.JACK, 0)
    c.set(4, 14, 7, B.STONEBRICK_STAIRS, 0)
    c.set(5, 14, 7, B.STONEBRICK_STAIRS, 1)
    # the hull: an upside-down brick roof, its tip toward the ground
    for z in range(2, 9):
        c.set(1, 4, z, B.BRICK_STAIRS, 4)
        c.set(9, 4, z, B.BRICK_STAIRS, 5)
        c.set(2, 3, z, B.BRICK_STAIRS, 4)
        c.set(8, 3, z, B.BRICK_STAIRS, 5)
        c.set(3, 2, z, B.BRICK_STAIRS, 4)
        c.set(7, 2, z, B.BRICK_STAIRS, 5)
        c.set(4, 1, z, B.BRICK_STAIRS, 4)
        c.set(6, 1, z, B.BRICK_STAIRS, 5)
        c.set(5, 1, z, B.BRICK)
        c.fill(3, 3, z, 7, 3, z, B.BRICK)
        c.fill(4, 2, z, 6, 2, z, B.BRICK)
        c.fill(2, 4, z, 8, 4, z, B.BRICK)
    # walls: white clay, dark oak beams; room y5..10, ceiling y11 (the house's "floor")
    c.fill(2, 4, 2, 8, 11, 8, B.STAINED_CLAY, 0)
    c.fill(3, 5, 3, 7, 10, 7, B.AIR)
    c.fill(3, 11, 3, 7, 11, 7, B.WOOL, 14)
    for x in (2, 8):
        for z in (2, 8):
            c.fill(x, 4, z, x, 11, z, B.LOG2, 1)
    for t in range(2, 9):
        for (x, z) in ((t, 2), (t, 8), (2, t), (8, t)):
            c.set(x, 7, z, B.PLANKS, 5)
            c.set(x, 11, z, B.PLANKS, 5)
    # windows
    for (x, z) in ((5, 2), (2, 5), (8, 6), (3, 8), (7, 8)):
        c.fill(x, 8, z, x, 9, z, B.PANE)
    c.fill(2, 8, 4, 2, 9, 4, B.PANE)
    # the front door, raised: y5..6 at (5, z=8)
    c.fill(5, 5, 8, 5, 6, 8, B.AIR)
    # upside-down furniture, hanging from the rug
    c.set(5, 10, 5, B.GLOWSTONE)
    c.set(4, 10, 5, B.FENCE)
    c.set(6, 10, 5, B.FENCE)
    c.set(4, 9, 5, B.FENCE)
    c.set(6, 9, 5, B.FENCE)
    c.fill(4, 8, 5, 6, 8, 5, B.WOOD_SLAB, 1)
    c.fill(3, 10, 3, 5, 10, 3, B.BOOKSHELF)
    c.set(3, 9, 3, B.BOOKSHELF)
    c.set(7, 10, 3, B.STAINED_CLAY, 1)
    c.set(3, 5, 6, B.CRAFTING)
    c.set(7, 5, 7, B.CHEST, 4)
    c.set(5, 5, 3, B.FURNACE, 3)
    # the chimney, pointing down: a hollow brick stack beneath the east wall
    c.fill(7, 0, 3, 9, 3, 5, B.BRICK)
    c.fill(8, 0, 4, 8, 3, 4, B.AIR)
    for y in range(0, 5):
        c.set(8, y, 4, B.LADDER, 4)
    c.fill(8, 0, 5, 8, 1, 5, B.AIR)
    c.set(7, 0, 4, B.IRON_BARS)
    c.set(8, 0, 3, B.IRON_BARS)
    c.set(9, 3, 5, B.COAL_BLOCK)
    c.set(7, 1, 3, B.COAL_BLOCK)
    c.set(8, 4, 4, B.LADDER, 4)
    # the porch run: stairs from the south-east pillar to the door landing
    for x, y in ((9, 0), (8, 1), (7, 2), (6, 3)):
        if y:
            c.fill(x, 0, 9, x, y - 1, 9, B.COBBLE)
        c.set(x, y, 9, B.STONEBRICK_STAIRS, 1)
    c.fill(5, 0, 9, 5, 3, 9, B.COBBLE)
    c.set(5, 4, 9, B.PLANKS, 5)
    c.set(4, 4, 9, B.WOOD_SLAB, 1)
    c.set(10, 0, 9, B.STONEBRICK_STAIRS, 1)
    # a lantern post at the door
    c.set(4, 5, 9, B.FENCE)
    c.set(4, 6, 9, B.TORCH, 5)
