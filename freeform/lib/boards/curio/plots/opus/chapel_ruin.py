"""The Ruined Chapel: half a nave of broken stone with no roof, its east wall stepping up course by course to a
bell tower that still stands at the north-east corner. Inside the tower a ladder climbs to the bell chamber, open
on all four sides; the bell itself lies cracked in the nave where it fell."""
from mc import B

NAME = "The Ruined Chapel"
KIND = "structure"

BRICK, CRACKED, MOSSY = (B.STONEBRICK, 0), (B.STONEBRICK, 2), (B.STONEBRICK, 1)
COBBLE, MOSSCOB = (B.COBBLE, 0), (B.MOSSY, 0)
TX0, TX1, TZ0, TZ1 = 6, 9, 0, 4                                  # the tower
NAVE = (1, 9, 4, 10)                                             # x0, x1, z0, z1


def stone(x, y, z):
    k = (x * 7 + y * 13 + z * 5) % 11
    return MOSSY if k < 2 else CRACKED if k < 4 else MOSSCOB if k == 4 and y < 3 else BRICK


def build(c):
    x0, x1, z0, z1 = NAVE
    # the nave floor, cobbled and broken through to grass
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (x * 3 + z * 7) % 5:
                c.set(x, -1, z, *COBBLE)
    # the nave's walls, ruined to uneven heights; the east wall steps up toward the tower, one course at a time
    heights = {}
    for z in range(z0, z1 + 1):
        heights[(x1, z)] = 2 + (z1 - z)                          # 2 at the south end, 8 at the tower
        heights[(x0, z)] = [1, 3, 4, 2, 1, 2, 3][(z - z0) % 7]
    for x in range(x0, x1):
        heights[(x, z1)] = [1, 2, 1, 0, 0, 2, 3, 2][(x - x0) % 8]
    for (x, z), h in heights.items():
        for y in range(0, h):
            arch = (x == x0 and z in (6, 7) and y < 3) or (z == z1 and x in (4, 5) and y < 3)
            if not arch:
                c.set(x, y, z, *stone(x, y, z))
    c.set(x0, 3, 6, *BRICK) if heights[(x0, 6)] > 3 else None
    # the tower: four walls fourteen high, a door from the nave, the bell chamber's openings, broken crenels
    for x in range(TX0, TX1 + 1):
        for z in range(TZ0, TZ1 + 1):
            edge = x in (TX0, TX1) or z in (TZ0, TZ1)
            if not edge:
                continue
            top = 14 if (x + z) % 2 else 15
            for y in range(0, top):
                opening = 10 <= y <= 12 and ((x in (7, 8) and z in (TZ0, TZ1)) or (z in (2,) and x in (TX0, TX1)))
                door = z == TZ1 and x == 7 and y < 2
                gap = z == TZ1 and x in (8, 9) and 7 <= y <= 8 and False
                if not (opening or door or gap):
                    c.set(x, y, z, *stone(x, y, z))
    # the bell chamber's floor, and a ladder up the inside of the north wall to it
    for x in range(TX0 + 1, TX1):
        for z in range(TZ0 + 1, TZ1):
            if (x, z) != (7, 1):
                c.set(x, 9, z, B.PLANKS, 5)
    for y in range(0, 10):
        c.set(7, y, 1, B.LADDER, 3)
    c.set(8, 10, 3, B.FENCE)                                     # the empty bell frame
    c.set(8, 11, 3, B.FENCE)
    c.set(8, 12, 3, B.LOG, 1 | 4)
    # the tower's roof is gone: a ring of slabs inside the parapet to stand on, reached from the chamber
    for y in range(10, 14):
        c.set(7, y, 3, B.LADDER, 5)                              # hung on the west wall, between the openings
    for x in range(TX0 + 1, TX1):
        for z in range(TZ0 + 1, TZ1):
            if (x, z) != (7, 3):
                c.set(x, 13, z, B.STONEBRICK, 0)
    # the fallen bell, cracked, half sunk in the nave's grass, and rubble
    for x, y, z in [(3, 0, 7), (4, 0, 7), (5, 0, 7), (3, 0, 8), (4, 0, 8), (5, 0, 8), (3, 0, 6), (4, 0, 6), (5, 0, 6),
                    (4, 1, 7), (3, 1, 7), (4, 1, 6), (4, 1, 8), (4, 2, 7)]:
        c.set(x, y, z, B.GOLD_BLOCK if (x + y + z) % 3 else B.HARDENED_CLAY)
    for x, z in [(2, 9), (7, 9), (6, 5), (2, 5), (8, 8)]:
        c.set(x, 0, z, *(MOSSCOB if (x + z) % 2 else CRACKED))
    c.set(0, 0, 2, B.COBBLE_WALL)                                # a broken gatepost and the old graves
    c.set(0, 1, 2, B.COBBLE_WALL)
    for x in (1, 3):
        c.set(x, 0, 1, B.STONEBRICK, 3)
    c.set(5, 0, 1, B.COBBLE_WALL)
