"""The Crooked House: three timber-framed storeys, each one block further east than the one under it, under a steep
gable roof. Ladders climb inside from floor to floor and on into the attic; a balcony on the top storey's east end
leads to a ladder up the gable to the ridge."""
from mc import B

NAME = "The Crooked House"
KIND = "house"

PLASTER = (B.WOOL, 0)
FRAME = (B.LOG2, 1)                                              # dark oak
FRAME_X, FRAME_Z = (B.LOG2, 1 | 4), (B.LOG2, 1 | 8)
FLOOR = (B.PLANKS, 5)
ROOF = B.BRICK_STAIRS
ROOF_FULL = (B.BRICK, 0)
Z0, Z1 = 2, 8


def storey(c, k):
    x0, x1 = 1 + k, 7 + k
    yb = 4 * k
    for x in range(x0, x1 + 1):
        for z in range(Z0, Z1 + 1):
            if k:
                c.set(x, yb - 1, z, *FLOOR)                      # this storey's floor
            edge_x, edge_z = x in (x0, x1), z in (Z0, Z1)
            for y in range(yb, yb + 3):
                if edge_x and edge_z:
                    c.set(x, y, z, *FRAME)                       # corner posts
                elif edge_x or edge_z:
                    window = y == yb + 1 and ((edge_z and (x - x0) % 3 == 2) or (edge_x and z in (4, 6)))
                    c.set(x, y, z, *((B.PANE, 0) if window else PLASTER))
            if (edge_x or edge_z) and not (edge_x and edge_z) and (x + z) % 4 == 0:
                c.set(x, yb + 1, z, *FRAME)                       # studs between the windows
    for x in range(x0, x1 + 1):                                  # a beam band under the next storey
        for z in (Z0, Z1):
            c.set(x, yb + 3, z, *FRAME_X)
    for z in range(Z0, Z1 + 1):
        for x in (x0, x1):
            c.set(x, yb + 3, z, *FRAME_Z)


def ladders(c):
    """Up through every floor on the north wall, set once the floors are down so none is covered."""
    for k in range(3):
        for y in range(4 * k, 4 * k + 4):
            c.set(4 + k, y, Z0 + 1, B.LADDER, 3)


def main_roof(c):
    x0, x1 = 3, 9
    base = 11
    for i in range(5):                                           # stairs rising from both eaves to the ridge
        for x in range(x0 - 1, x1 + 1):
            if 0 <= x <= 10:
                c.set(x, base + i, Z0 - 1 + i, ROOF, 2)
                c.set(x, base + i, Z1 + 1 - i, ROOF, 3)
    for x in range(x0 - 1, x1 + 1):
        c.set(x, base + 5, 5, *ROOF_FULL)                        # the ridge
    c.set(x1, base + 4, 5, *ROOF_FULL)                           # under the ridge's east end, for the ladder
    for i in range(4):                                           # the gable ends, plastered, a round window
        for z in range(Z0 + i, Z1 - i + 1):
            for x in (x0, x1):
                c.set(x, base + i, z, *PLASTER)
    c.set(x0, base + 1, 5, B.STAINED_PANE, 12)
    c.set(x1, base + 1, 5, B.STAINED_PANE, 12)


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for z in range(0, 11):                                       # a cobbled path to the door
        c.set(4, -1, z, B.COBBLE) if z > Z1 else None
    for k in range(3):
        storey(c, k)
    ladders(c)
    c.set(4, 0, Z1, B.AIR)                                       # the front doorway, south
    c.set(4, 1, Z1, B.AIR)
    c.set(2, 0, Z0, B.AIR)                                       # a back doorway, north
    c.set(2, 1, Z0, B.AIR)
    main_roof(c)
    # the top storey's floor runs out east as a balcony, with a rail; a ladder up the gable to the ridge
    for z in range(4, 7):
        c.set(10, 7, z, *FLOOR)
        c.set(10, 8, z, B.FENCE) if z == 4 else None
    c.set(9, 8, 6, B.AIR)
    c.set(9, 9, 6, B.AIR)                                        # a door out onto the balcony
    for y in range(8, 17):
        c.set(10, y, 5, B.LADDER, 5)
    # leaning props under the overhang: crates and a barrel to hide behind
    c.fill(9, 0, 3, 10, 1, 3, B.PLANKS, 1)
    c.set(10, 0, 7, B.HAY)
    c.set(9, 0, 7, B.CAULDRON)
    c.set(0, 0, 9, B.FENCE)
    c.set(0, 1, 9, B.TORCH, 5)
