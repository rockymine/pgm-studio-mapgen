"""A chalet-shaped cuckoo clock with a pendulum, pine-cone weights and a cuckoo door."""
from mc import B

NAME = "The Cuckoo Clock"
KIND = "house"


def build(c):
    # plinth
    c.fill(1, -1, 1, 9, -1, 9, B.STONE, 6)
    # case: birch walls, dark oak corner posts
    c.fill(2, 0, 2, 8, 8, 8, B.PLANKS, 2)
    c.fill(3, 0, 3, 7, 7, 7, B.AIR)
    for x in (2, 8):
        for z in (2, 8):
            c.fill(x, 0, z, x, 8, z, B.LOG2, 1)
    # dark oak belts at floor levels, outside
    for y in (0, 4, 8):
        c.fill(2, y, 2, 8, y, 2, B.PLANKS, 5)
        c.fill(2, y, 8, 8, y, 8, B.PLANKS, 5)
        c.fill(2, y, 2, 2, y, 8, B.PLANKS, 5)
        c.fill(8, y, 2, 8, y, 8, B.PLANKS, 5)
    # floors
    c.fill(3, 4, 3, 7, 4, 7, B.PLANKS, 5)
    c.fill(3, 8, 3, 7, 8, 7, B.PLANKS, 5)
    c.set(3, 4, 7, B.AIR)
    c.set(7, 8, 7, B.AIR)
    for y in range(0, 5):
        c.set(3, y, 7, B.LADDER, 2)
    for y in range(5, 10):
        c.set(7, y, 7, B.LADDER, 2)
    # roof, ridge along z
    for x, y in ((1, 8), (2, 9), (3, 10), (4, 11), (5, 12)):
        if x < 5:
            c.fill(x, y, 1, x, y, 9, B.SPRUCE_STAIRS, 0)
            c.fill(10 - x, y, 1, 10 - x, y, 9, B.SPRUCE_STAIRS, 1)
        else:
            c.fill(x, y, 1, x, y, 9, B.PLANKS, 5)
    c.fill(5, 13, 1, 5, 13, 9, B.WOOD_SLAB, 5)
    # gable walls front and back, attic hollow
    for z in (2, 8):
        c.fill(3, 9, z, 7, 9, z, B.PLANKS, 2)
        c.fill(4, 10, z, 6, 10, z, B.PLANKS, 2)
        c.set(5, 11, z, B.PLANKS, 2)
    # gable trim
    for z in (1, 9):
        c.set(5, 13, z, B.LOG2, 1)
    # cuckoo door and balcony in the front gable
    c.fill(5, 9, 8, 5, 10, 8, B.AIR)
    c.set(5, 8, 9, B.WOOD_SLAB, 1)
    c.fill(4, 8, 9, 4, 8, 9, B.FENCE)
    c.fill(6, 8, 9, 6, 8, 9, B.FENCE)
    c.set(5, 9, 7, B.WOOL, 4)       # the bird, waiting
    c.set(5, 10, 7, B.WOOL, 14)
    c.set(5, 14, 5, B.FENCE)
    c.set(5, 15, 5, B.GOLD_BLOCK)
    # dial centred (5,5,9)
    cx, cy = 5, 5
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            d = dx * dx + dy * dy
            if d <= 10:
                c.set(cx + dx, cy + dy, 9, B.LOG2 if d >= 8 else B.QUARTZ, 1 if d >= 8 else 0)
    for dx, dy in ((0, 2), (0, -2), (2, 0), (-2, 0)):
        c.set(cx + dx, cy + dy, 9, B.COAL_BLOCK)
    c.fill(5, 5, 9, 5, 7, 9, B.COAL_BLOCK)
    c.fill(5, 5, 9, 6, 5, 9, B.COAL_BLOCK)
    c.set(5, 5, 9, B.GOLD_BLOCK)
    # pendulum alcove on the front wall below the dial
    c.fill(4, 0, 8, 6, 1, 8, B.AIR)
    c.fill(5, 2, 9, 5, 2, 9, B.FENCE)
    c.fill(4, 0, 9, 6, 1, 9, B.AIR)
    c.set(5, 1, 9, B.GOLD_BLOCK)
    c.set(5, 0, 9, B.GOLD_BLOCK)
    # small windows high on the sides
    for x in (2, 8):
        c.fill(x, 6, 4, x, 6, 6, B.GLASS)
    # side doorways (ground) and a back slot
    c.fill(2, 0, 5, 2, 1, 5, B.AIR)
    c.fill(5, 0, 2, 5, 1, 2, B.AIR)
    c.fill(8, 5, 5, 8, 6, 5, B.AIR)
    # inner pendulum, shelf, torch
    for y in range(1, 4):
        c.set(5, y, 4, B.FENCE)
    c.set(5, 0, 4, B.GOLD_BLOCK)
    c.fill(4, 5, 3, 6, 5, 3, B.WOOD_SLAB, 1)
    c.set(6, 6, 3, B.TORCH, 5)
    c.fill(3, 1, 3, 4, 1, 3, B.BOOKSHELF)
    # pine-cone weights hung from the eaves at x=1 and x=9
    for x in (1, 9):
        c.fill(x, 4, 5, x, 7, 5, B.FENCE)
        c.fill(x, 1, 5, x, 3, 5, B.STAINED_CLAY, 12)
        c.set(x, 0, 5, B.STAINED_CLAY, 12)
        c.set(x, 2, 4, B.WOOD_SLAB, 1)
        c.set(x, 2, 6, B.WOOD_SLAB, 1)
        c.set(x, 0, 4, B.STAINED_CLAY, 12)
        c.set(x, 0, 6, B.STAINED_CLAY, 12)
    # a stepped log pile up the east side, to the weight's chain and the eave
    c.set(9, 0, 8, B.PLANKS, 5)
    c.set(9, 0, 7, B.PLANKS, 5)
    c.set(9, 1, 7, B.WOOD_SLAB, 5)
    c.set(9, 1, 6, B.PLANKS, 5)
