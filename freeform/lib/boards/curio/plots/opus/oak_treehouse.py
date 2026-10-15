"""The Treehouse: a great oak with a plank hut in its crown, a ladder up the trunk, and a walk of slabs and rope
rails climbing out along a branch to a crow's-nest lookout over the leaves."""
import math

from mc import B

NAME = "The Treehouse"
KIND = "house"

LOG, LOG_X, LOG_Z = (B.LOG, 0), (B.LOG, 4), (B.LOG, 8)
LEAVES = (B.LEAVES, 0 | 4)
PLANK, SPRUCE = (B.PLANKS, 0), (B.PLANKS, 1)


def build(c):
    # roots and the trunk, two by two, flared at the foot
    for x, z in ((4, 4), (5, 4), (4, 5), (5, 5)):
        c.fill(x, 0, z, x, 12, z, *LOG)
    for x, z in ((3, 4), (6, 5), (4, 6), (5, 3)):
        c.set(x, 0, z, *LOG)
    c.set(2, 0, 4, *LOG_X)
    c.set(7, 0, 5, *LOG_X)
    # the ladder up the trunk's south face, through the platform
    for y in range(0, 11):
        c.set(4, y, 6, B.LADDER, 3)
    # the platform round the trunk at y 9, and the hut on it
    for x in range(1, 10):
        for z in range(1, 10):
            if (x, z) in ((4, 6),):
                continue
            if abs(x - 4.5) + abs(z - 4.5) <= 7.5:
                c.set(x, 9, z, *SPRUCE)
    for x in range(2, 8):
        for z in range(2, 8):
            if not (2 < x < 7 and 2 < z < 7):
                for y in range(10, 13):
                    door = (z == 7 and x == 5 and y < 12) or (x == 2 and z == 4 and y < 12)
                    window = y == 11 and ((x == 7 and z in (3, 5)) or (z == 2 and x in (3, 6)))
                    if not door:
                        c.set(x, y, z, *((B.PANE, 0) if window else PLANK))
    for x in range(1, 9):                                        # the hut's roof, slabs over its eaves
        for z in range(1, 9):
            c.set(x, 13, z, B.WOOD_SLAB, 0)
    c.set(4, 13, 4, *LOG)                                         # the trunk runs up through the roof
    c.set(5, 13, 5, *LOG)
    for x, z in ((1, 1), (1, 8), (8, 1), (8, 8)):                # rails at the platform's corners
        c.set(x, 10, z, B.FENCE)
    # the branch out to the lookout: a log climbing north-east, slabs on it as steps
    for i, (x, y, z) in enumerate([(6, 13, 3), (7, 14, 3), (8, 15, 2), (8, 16, 1)]):
        c.set(x, y, z, *LOG_X)
    c.set(5, 14, 4, *LOG)
    for x in range(7, 11):                                       # the lookout floor
        for z in range(0, 3):
            c.set(x, 17, z, *SPRUCE)
    for x in range(7, 11):
        for z in range(0, 3):
            edge = x in (7, 10) or z in (0, 2)
            if edge and not (x == 7 and z == 1):
                c.set(x, 18, z, B.FENCE)
    c.set(8, 16, 2, *SPRUCE)                                     # the last step up into the nest
    # the crown: leaves in a broad ball round everything, never filling the hut, the platform or the climb
    keep = set()
    for x in range(1, 10):
        for z in range(1, 10):
            for y in range(10, 13):
                keep.add((x, y, z))
    for x in range(0, 11):
        for z in range(0, 11):
            for y in range(13, 23):
                d = math.sqrt(((x - 5) / 5.5) ** 2 + ((y - 15.5) / 4.5) ** 2 + ((z - 5) / 5.5) ** 2)
                if d > 1 or (x, y, z) in keep:
                    continue
                if 6 <= x <= 10 and z <= 4 and y <= 19:
                    continue                                     # the branch and the lookout stay open
                if y == 14 and 4 <= x <= 6 and 2 <= z <= 5:
                    continue                                     # headroom on the hut's roof
                if c.get(x, y, z)[0] == 0 and (x * 7 + y * 3 + z * 5) % 11:
                    c.set(x, y, z, *LEAVES)
    for x, z in ((1, 3), (8, 7), (2, 8)):                        # leaves hanging under the platform's rim
        c.set(x, 8, z, *LEAVES)
    c.set(8, 0, 8, B.HAY)
    c.set(1, 0, 1, B.HAY)
