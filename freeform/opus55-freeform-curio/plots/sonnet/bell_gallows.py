"""A timber bell frame with three huge golden bells you can climb into, and a ringer's shed behind."""
from mc import B

NAME = "The Bell Frame"
KIND = "structure"


def build(c):
    # the two posts: thick dark oak, x0 and x10, z4..6, with a stone footing
    for x in (0, 10):
        c.fill(x, 0, 4, x, 16, 6, B.LOG2, 1)
        c.fill(x, 0, 4, x, 0, 6, B.STONEBRICK, 0)
        c.fill(x, 3, 4, x, 3, 6, B.PLANKS, 5)
        c.fill(x, 9, 4, x, 9, 6, B.PLANKS, 5)
    # the crossbeam, along x, z4..7, with a plank-capped walk on top
    c.fill(0, 16, 4, 10, 16, 7, B.LOG2, 5)
    c.fill(1, 17, 4, 9, 17, 4, B.FENCE)
    c.fill(1, 17, 7, 9, 17, 7, B.FENCE)
    # knee braces under the beam, stairs, upside down
    for z in (4, 6):
        for x, d in ((1, 5), (9, 4)):
            c.set(x, 15, z, B.DARK_OAK_STAIRS, d)
        for x, d in ((1, 5), (9, 4)):
            pass
    # the lower platform: planks, z5..7, x0..10
    c.fill(1, 8, 5, 9, 8, 7, B.PLANKS, 5)
    c.fill(1, 8, 7, 9, 8, 7, B.PLANKS, 1)
    # ladders on the south faces of the posts
    for x in (0, 10):
        for y in range(0, 17):
            c.set(x, y, 7, B.LADDER, 3)
        c.set(x, 16, 7, B.LADDER, 3)
    c.set(0, 8, 7, B.LADDER, 3)
    c.set(10, 8, 7, B.LADDER, 3)
    # three bells, centres x2, x5, x8, z5
    for cx in (2, 5, 8):
        # lip and body rings
        for y in range(9, 14):
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if dx == 0 and dz == 0:
                        continue
                    blk = (B.IRON_BLOCK, 0) if y <= 10 else (B.GOLD_BLOCK, 0)
                    c.set(cx + dx, y, 5 + dz, *blk)
        # rounded crown
        for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            c.set(cx + dx, 13, 5 + dz, B.AIR)
        c.fill(cx - 1, 14, 5, cx + 1, 14, 5, B.GOLD_BLOCK)
        c.fill(cx, 14, 4, cx, 14, 6, B.GOLD_BLOCK)
        c.set(cx, 15, 5, B.GOLD_BLOCK)
        # the doorway in the front and the clapper
        c.fill(cx, 9, 6, cx, 10, 6, B.AIR)
        c.set(cx, 12, 5, B.FENCE)
        c.set(cx, 11, 5, B.IRON_BLOCK)
        c.set(cx, 13, 5, B.AIR)
        c.set(cx, 12, 5, B.FENCE)
        c.set(cx, 13, 5, B.FENCE)
    # the ringer's shed, north
    c.fill(2, 0, 0, 8, 3, 3, B.PLANKS, 1)
    c.fill(3, 0, 1, 7, 2, 2, B.AIR)
    for x in (2, 8):
        for z in (0, 3):
            c.fill(x, 0, z, x, 3, z, B.LOG2, 1)
    c.fill(2, 3, 0, 8, 3, 3, B.PLANKS, 5)
    c.fill(3, 0, 3, 3, 1, 3, B.AIR)                # door
    c.fill(7, 0, 3, 7, 1, 3, B.AIR)                # second door
    # inside: partition, rope, barrel, bench
    c.fill(5, 0, 2, 5, 2, 2, B.PLANKS, 1)
    c.set(4, 0, 1, B.HAY)
    c.set(6, 0, 1, B.CAULDRON)
    c.set(7, 2, 1, B.GLOWSTONE)
    # shed roof: slabs with a lip, bell-rope hole omitted
    c.fill(1, 4, 0, 9, 4, 3, B.WOOD_SLAB, 5)
    # windows in the shed
    # lantern on a hook by the south ladder
    # steps from the street up to the platform: a stack of crates
    c.set(3, 0, 8, B.HAY)
    c.set(4, 0, 8, B.HAY)
    c.set(4, 1, 8, B.PLANKS, 1)
    # finial lantern posts on the beam
