"""The Palm House: a glass house on a white iron frame, its barrel vault rising to a lantern, two palms and a
thicket of ferns crowding the glass. A seeker sees through glass, so the hiding is in the fronds and the potting
shed at the back; a ladder up the frame's end rib reaches the vault and its lantern."""
import math

from mc import B

NAME = "The Palm House"
KIND = "structure"

FRAME = (B.QUARTZ, 0)
RIB = (B.QUARTZ, 2)
GLASS = (B.GLASS, 0)
X0, X1, Z0, Z1 = 5, 9, 2, 8
CZ = 5.0
R = 3.6                                                          # the vault's radius over the walls
WALL = 3


def vault_y(z):
    d = abs(z - CZ)
    return WALL + int(round(math.sqrt(max(0.0, R * R - d * d)))) if d <= R else None


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            c.set(x, -1, z, B.DIRT, 2)                           # podzol beds inside
    # the walls: glass between white ribs every other block, a quartz sill
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            ex, ez = x in (X0, X1), z in (Z0, Z1)
            if not (ex or ez):
                continue
            for y in range(0, WALL):
                rib = (ex and ez) or (ez and x % 2 == 1) or (ex and z % 3 == 2)
                c.set(x, y, z, *(FRAME if y == 0 else RIB if rib else GLASS))
    # the vault along x, glass with a rib every other block; the gable ends glazed too
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            top = vault_y(z)
            if top is None:
                continue
            rib = x % 2 == 1
            c.set(x, top, z, *(RIB if rib or x in (X0, X1) else GLASS))
            for y in range(WALL, top):                           # fill under the curve at the vault's edges
                if z in (Z0, Z1) or (z > Z0 and vault_y(z - 1) is not None and vault_y(z - 1) < y) or \
                        (z < Z1 and vault_y(z + 1) is not None and vault_y(z + 1) < y):
                    c.set(x, y, z, *(RIB if rib else GLASS))
            if x in (X0, X1):
                for y in range(WALL, top):
                    c.set(x, y, z, *(RIB if z % 3 == 2 else GLASS))
    # the lantern on the crown, its little roof and a gold ball
    ty = vault_y(5)
    for x in range(6, 9):
        for z in range(4, 7):
            c.set(x, ty + 1, z, *(RIB if (x + z) % 2 == 0 else GLASS))
            c.set(x, ty + 2, z, B.SLAB, 7)
    c.set(7, ty + 1, 5, B.AIR)
    c.set(7, ty + 3, 5, B.GOLD_BLOCK)
    # doors: south and north, through the glass
    c.set(7, 0, Z1, B.AIR); c.set(7, 1, Z1, B.AIR)
    c.set(5, 0, Z0, B.AIR); c.set(5, 1, Z0, B.AIR)
    # the palms: jungle trunks up to the vault, crowns of fronds pressing the glass; ferns below
    for px, pz, h in ((6, 4, 5), (8, 6, 6)):
        for y in range(0, h):
            c.set(px, y, pz, B.LOG, 3)
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (2, 0), (-2, 0), (0, 2), (0, -2)):
            x, z = px + dx, pz + dz
            if X0 < x < X1 and Z0 < z < Z1:
                y = h - (1 if abs(dx) + abs(dz) > 1 else 0)
                if c.get(x, y, z)[0] == 0:
                    c.set(x, y, z, B.LEAVES, 3 | 4)
        c.set(px, h, pz, B.LEAVES, 3 | 4)
    for x, z in ((6, 7), (7, 7), (7, 3), (8, 3), (6, 3), (8, 7), (6, 5)):
        c.set(x, 0, z, B.LEAVES, 3 | 4)                          # fern thickets, a hider's cover
        if (x + z) % 2:
            c.set(x, 1, z, B.LEAVES, 3 | 4)
    # the potting shed against the west end: a plank room with a slab roof, its only door from the glass house
    for x in range(0, X0):
        for z in range(Z0, Z1 + 1):
            edge = x in (0, X0 - 1) or z in (Z0, Z1)
            c.set(x, -1, z, B.PLANKS, 2)
            for y in range(0, 3):
                if edge:
                    c.set(x, y, z, B.PLANKS, 2 if y else 1)
            c.set(x, 3, z, B.WOOD_SLAB, 1)
    c.set(X0, 0, 3, B.AIR); c.set(X0, 1, 3, B.AIR)                # the door through from the glass, by the north wall
    c.set(X0 - 1, 0, 3, B.AIR); c.set(X0 - 1, 1, 3, B.AIR)
    c.set(1, 0, 7, B.CHEST)                                      # benches and pots inside
    c.set(3, 0, 7, B.CRAFTING)
    c.fill(2, 0, 4, 3, 1, 4, B.BOOKSHELF)                        # a shelf of seed packets across the room
    c.set(1, 0, 6, B.FLOWER_POT)
    # the ladder up the east end rib, to the vault and the lantern
    for y in range(0, vault_y(5) + 1):
        c.set(10, y, 5, B.LADDER, 5)
    c.set(X1, 0, 5, *FRAME)
    for y in range(1, vault_y(5) + 1):
        c.set(X1, y, 5, *RIB)
    # flower pots and a bench
    c.set(10, 0, 8, B.FLOWER_POT)
    c.set(0, 0, 9, B.WOOD_SLAB, 2)
    c.set(0, 0, 10, B.WOOD_SLAB, 2)
