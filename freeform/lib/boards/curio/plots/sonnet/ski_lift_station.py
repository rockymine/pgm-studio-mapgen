"""A ski-lift station: a timber pylon with a scaffold stair around it, a red gondola parked on the cable, a winch house."""
from mc import B

NAME = "The Ski Lift Station"
KIND = "structure"


def build(c):
    # pylon legs: dark oak logs at the corners of x6..8, z4..6, up past the top platform
    for x in (6, 8):
        for z in (4, 6):
            c.fill(x, 0, z, x, 17, z, B.LOG2, 1)
    # cross-bracing rings of iron bars between the legs
    for y in (3, 6, 9, 15):
        for t in (7,):
            c.set(t, y, 4, B.IRON_BARS)
            c.set(t, y, 6, B.IRON_BARS)
            c.set(6, y, 5, B.IRON_BARS)
            c.set(8, y, 5, B.IRON_BARS)
    # top platform, rails
    c.fill(6, 12, 4, 8, 12, 6, B.PLANKS, 1)
    for x in (7, 8):
        c.set(x, 13, 4, B.FENCE)
        c.set(x, 13, 6, B.FENCE)
    c.set(8, 13, 5, B.FENCE)
    c.set(7, 13, 5, B.AIR)
    # the crossbar and cable pulley at the top
    c.fill(6, 18, 5, 8, 18, 5, B.IRON_BLOCK)
    for z in (4, 6):
        c.fill(6, 18, z, 8, 18, z, B.PLANKS, 5)
    # the cable: iron bars along z=5 from the pylon to the end pole
    c.fill(1, 18, 5, 5, 18, 5, B.IRON_BARS)
    c.fill(0, 0, 5, 0, 18, 5, B.LOG2, 1)
    # scaffold stair around the pylon: a ring of stairs on fence posts, ccw from the south-west
    ring = [(5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (8, 3), (7, 3), (6, 3)]
    dirs = {}
    for i, (x, z) in enumerate(ring):
        nx, nz = ring[min(i + 1, len(ring) - 1)]
        if i == len(ring) - 1:
            nx, nz = 5, 3
        d = 0 if nx > x else (1 if nx < x else (2 if nz > z else 3))
        dirs[i] = d
        c.set(x, i, z, B.STONEBRICK_STAIRS, d)
        if i > 0:
            c.fill(x, 0, z, x, i - 1, z, B.FENCE)
    # landing platform at the end of the stair, level with the top platform edge
    # a ladder on the west side of the pylon
    for y in range(0, 13):
        c.set(5, y, 4, B.LADDER, 4)
    # the red gondola: floor y12, walls y13..14, roof y15, x1..4, z3..7
    c.fill(1, 12, 3, 4, 12, 7, B.PLANKS, 5)
    c.fill(1, 13, 3, 4, 14, 7, B.STAINED_CLAY, 14)
    c.fill(2, 13, 4, 3, 14, 6, B.AIR)
    c.fill(1, 15, 3, 4, 15, 7, B.QUARTZ)
    for x in (2, 3):
        c.fill(x, 16, 5, x, 17, 5, B.FENCE)
    # glass bands and the door
    for z in (4, 5, 6):
        c.set(1, 14, z, B.GLASS)
    for x in (2, 3):
        c.set(x, 14, 3, B.GLASS)
        c.set(x, 14, 7, B.GLASS)
    c.fill(4, 13, 5, 4, 14, 5, B.AIR)
    c.set(4, 14, 4, B.GLASS)
    c.set(4, 14, 6, B.GLASS)
    # benches inside the cabin
    c.set(2, 13, 4, B.WOOD_SLAB, 1)
    c.set(2, 13, 6, B.WOOD_SLAB, 1)
    c.set(3, 14, 5, B.AIR)
    # the cabin's stripe
    for z in range(3, 8):
        c.set(1, 13, z, B.STAINED_CLAY, 0) if z % 2 == 0 else None
        c.set(4, 13, z, B.STAINED_CLAY, 0) if z % 2 == 0 and z != 5 else None
    # the winch house at the foot of the line: two storeys, a ladder up through the floor to the roof hatch
    c.fill(0, 0, 6, 4, 4, 10, B.STONEBRICK, 0)
    c.fill(1, 0, 7, 3, 1, 9, B.AIR)
    c.fill(1, 3, 7, 3, 4, 9, B.AIR)
    c.fill(0, 5, 6, 4, 5, 10, B.PLANKS, 5)
    c.fill(2, 0, 10, 2, 1, 10, B.AIR)              # south door
    c.fill(4, 0, 9, 4, 1, 9, B.AIR)                # east door
    c.set(2, 2, 7, B.AIR)
    c.set(2, 5, 7, B.AIR)
    for y in range(0, 6):
        c.set(2, y, 7, B.LADDER, 3)
    c.fill(0, 2, 6, 4, 2, 6, B.LOG2, 1)
    c.fill(0, 2, 10, 4, 2, 10, B.LOG2, 1)
    # winch drum: iron and a coal band, on the roof; and a signpost
    c.fill(1, 6, 8, 3, 6, 8, B.IRON_BLOCK)
    c.set(2, 6, 8, B.COAL_BLOCK)
    c.set(1, 0, 7, B.FURNACE, 3)
    c.set(3, 0, 7, B.CRAFTING)
    c.set(1, 3, 9, B.CHEST, 3)
    c.set(3, 3, 8, B.BOOKSHELF)
    c.set(3, 3, 9, B.BOOKSHELF)
    # a ski rack by the pylon and a lantern post
    c.fill(10, 0, 9, 10, 3, 9, B.FENCE)
    c.set(10, 4, 9, B.GLOWSTONE)
    c.fill(9, 0, 10, 9, 2, 10, B.FENCE)
    c.fill(8, 0, 10, 8, 2, 10, B.FENCE)
