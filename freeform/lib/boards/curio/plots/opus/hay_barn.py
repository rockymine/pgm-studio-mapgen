"""The Hay Barn: an open-sided barn on spruce posts under a long gable roof, piled with hay. The bales step up to a
hayloft along the east side and on to the tie-beams under the ridge; the stacks on the west side leave lanes
between them to crouch in."""
from mc import B

NAME = "The Hay Barn"
KIND = "structure"

POST, BEAM_X = (B.LOG, 1), (B.LOG, 1 | 4)
HAY = (B.HAY, 0)
LOFT = (B.PLANKS, 1)
ROOF = B.SPRUCE_STAIRS
EAVE_Y = 6


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for x in range(1, 10):
        for z in range(1, 10):
            c.set(x, -1, z, B.DIRT, 1)                           # a beaten earth floor
    # posts at the corners and the middles of the long sides, a beam round the top
    for x, z in [(1, 1), (5, 1), (9, 1), (1, 9), (5, 9), (9, 9), (1, 5), (9, 5)]:
        for y in range(0, EAVE_Y):
            c.set(x, y, z, *POST)
    for x in range(1, 10):
        c.set(x, EAVE_Y - 1, 1, *BEAM_X)
        c.set(x, EAVE_Y - 1, 9, *BEAM_X)
    # the roof: stairs from both eaves (north and south) up to a ridge along x over z 5
    for i in range(6):
        for x in range(0, 11):
            c.set(x, EAVE_Y + i, i, ROOF, 2) if i < 5 else None
            c.set(x, EAVE_Y + i, 10 - i, ROOF, 3) if i < 5 else None
    for x in range(0, 11):
        c.set(x, EAVE_Y + 5, 5, B.WOOD_SLAB, 1)
        c.set(x, EAVE_Y + 4, 5, *LOFT)
    for x in (0, 10):                                            # the gable ends boarded over the beam
        for i in range(1, 5):
            for z in range(i + 1, 10 - i):
                c.set(x, EAVE_Y + i - 1, z, *LOFT) if x == 0 or z != 5 else None
    # tie-beams across under the ridge, to walk on
    for x in range(1, 10):
        c.set(x, EAVE_Y, 5, *BEAM_X)
    # the hayloft along the east side, at y 4
    for x in range(6, 10):
        for z in range(2, 9):
            c.set(x, 3, z, *LOFT)
    for x in range(6, 10):                                       # bales walling the loft's ends, two high
        c.fill(x, 4, 2, x, 5, 2, *HAY)
        c.fill(x, 4, 8, x, 5, 8, *HAY)
    for z in range(3, 8):                                        # a knee wall of boards along the loft's open side
        if z not in (4, 5):
            c.set(6, 4, z, *LOFT)
    # the bale stair from the floor to the loft, and a bale on the loft up to the beams
    for k, (x, z, h) in enumerate([(5, 8, 1), (5, 7, 2), (5, 6, 3), (5, 5, 4)]):
        c.fill(x, 0, z, x, h - 1, z, *HAY)
    c.set(6, 4, 4, *HAY)                                         # one bale, then two, up to the tie-beams
    c.fill(7, 4, 4, 7, 5, 4, *HAY)
    # stacks on the west side with lanes between
    # a hay fort on the west side: a stack three high with a den inside, its only way in a hole in the top
    c.fill(1, 0, 2, 4, 2, 7, *HAY)
    c.fill(2, 0, 3, 3, 1, 6, B.AIR)                              # the den
    for y in range(0, 3):
        c.set(2, y, 3, B.LADDER, 3)                              # down through the hole, and back out
    c.fill(2, 0, 8, 3, 1, 8, *HAY)                               # a lower stack by the south posts
    # a cart, a pitchfork rack and a trough outside
    c.fill(0, 0, 2, 0, 0, 4, B.PLANKS, 1)
    c.set(0, 1, 2, B.FENCE); c.set(0, 1, 4, B.FENCE)
    c.set(0, 1, 3, *HAY)
    c.set(10, 0, 3, B.CAULDRON)
    c.set(10, 0, 7, B.FENCE); c.set(10, 1, 7, B.FENCE)
