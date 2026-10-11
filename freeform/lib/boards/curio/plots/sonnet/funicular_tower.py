"""A funicular: a stepped rail incline with a red car, climbing to a water-tower barrel on a timber platform."""
from mc import B

NAME = "The Water Tower Funicular"
KIND = "structure"


def build(c):
    # the incline: three-wide stair bed, y = 10 - z for z 10..1
    for z in range(1, 11):
        y = 10 - z
        c.set(2, y, z, B.STONEBRICK_STAIRS, 3)
        c.set(4, y, z, B.STONEBRICK_STAIRS, 3)
        c.set(3, y, z, B.DARK_OAK_STAIRS, 3)
        if z % 2 == 0 and y > 0:
            for x in (2, 4):
                c.fill(x, 0, z, x, y - 1, z, B.LOG, 1)
            c.set(3, y - 1, z, B.FENCE) if y > 1 else None
    # the car: z4..6, red with a white band, open at both ends
    for z in (4, 5, 6):
        y = 10 - z
        for x in (2, 4):
            c.fill(x, y + 1, z, x, y + 3, z, B.STAINED_CLAY, 14)
            c.set(x, y + 3, z, B.PANE) if z == 5 else None
        c.fill(2, y + 4, z, 4, y + 4, z, B.QUARTZ)
        c.fill(3, y + 1, z, 3, y + 3, z, B.AIR)
    # the tower platform at y9, x4..10, z0..5 (the stair bed ends level with it)
    c.fill(5, 9, 0, 10, 9, 5, B.PLANKS, 1)
    c.fill(4, 9, 0, 4, 9, 0, B.PLANKS, 1)
    for x in (5, 10):
        for z in (0, 5):
            c.fill(x, 0, z, x, 8, z, B.LOG, 1)
    # a ring of rail posts on the platform edge, with gaps
    for x in range(5, 11):
        c.set(x, 10, 5, B.FENCE) if x not in (7, 5) else None
    for z in range(0, 6):
        c.set(10, 10, z, B.FENCE) if z not in (2,) else None
    # the machine house at the foot of the tower
    c.fill(6, 0, 1, 9, 4, 5, B.STONEBRICK, 0)
    c.fill(7, 0, 2, 8, 3, 4, B.AIR)
    c.fill(6, 4, 1, 9, 4, 5, B.PLANKS, 5)
    c.fill(7, 0, 5, 7, 1, 5, B.AIR)                   # south door
    c.fill(6, 0, 3, 6, 1, 3, B.AIR)                   # west door onto the track side
    c.fill(5, 0, 3, 5, 1, 3, B.AIR)
    c.set(8, 0, 2, B.FURNACE, 3)
    c.set(8, 0, 4, B.CRAFTING)
    c.set(7, 4, 3, B.GLOWSTONE)
    c.set(7, 0, 2, B.IRON_BLOCK)
    # the barrel: an octagon, y10..15, interior x6..8, z1..3, water on the floor
    rows = {0: (6, 8), 1: (5, 9), 2: (5, 9), 3: (5, 9), 4: (6, 8)}
    for y in range(10, 16):
        for z, (xa, xb) in rows.items():
            c.fill(xa, y, z, xb, y, z, B.PLANKS, 1 if y not in (11, 14) else 5)
        c.fill(6, y, 1, 8, y, 3, B.AIR)
    c.fill(6, 10, 1, 8, 10, 3, B.WATER)
    c.set(7, 10, 4, B.HAY)                            # the sill
    c.fill(7, 11, 4, 7, 12, 4, B.AIR)
    # iron hoops
    for z, (xa, xb) in rows.items():
        for x in (xa, xb):
            c.set(x, 12, z, B.IRON_BLOCK) if z in (1, 3) and x in (5, 9) else None
    # a ladder up the barrel's south-west flank
    for y in range(10, 16):
        c.set(5, y, 4, B.LADDER, 4)
    # ledge inside the barrel: a catwalk of slabs on the north side
    c.fill(6, 12, 1, 8, 12, 1, B.WOOD_SLAB, 1)
    c.set(6, 13, 3, B.AIR)
    # rim lanterns and a flag pole on the north-east rim
    c.fill(9, 16, 1, 9, 19, 1, B.FENCE)
    c.fill(8, 19, 1, 8, 19, 1, B.WOOL, 14)
    c.set(7, 19, 1, B.WOOL, 14)
    c.set(5, 16, 2, B.GLOWSTONE)
    # sleepers and a buffer stop at the bottom of the incline
    c.set(3, 0, 10, B.DARK_OAK_STAIRS, 3)
