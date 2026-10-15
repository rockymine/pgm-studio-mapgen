"""The Chess Knight: a black knight on a chequered pedestal, its head turned east, its jaw open. A mane of steps
climbs its back to the ears; a hider can drop from the muzzle into the open jaw, or go down through a trap in the
pedestal to the vault inside it."""
from mc import B

NAME = "The Chess Knight"
KIND = "sculpture"

BLACK, SHINE = (B.WOOL, 15), (B.COAL_BLOCK, 0)
WHITE_SQ, BLACK_SQ = (B.QUARTZ, 0), (B.COAL_BLOCK, 0)
Z0, Z1 = 3, 7
BASE = 3                                                         # the pedestal is three high
# the knight's profile, rows from its foot up: (x from, x to)
PROFILE = [(2, 8), (2, 8), (3, 7), (3, 7), (3, 7), (3, 8), (3, 8), (2, 9), (2, 10), (2, 10), (3, 10), (3, 7),
           (4, 6), (4, 6)]


def build(c):
    # the pedestal, chequered, hollow inside: a vault two high on pillars
    for x in range(0, 11):
        for z in range(0, 11):
            c.set(x, -1, z, *(WHITE_SQ if (x + z) % 2 else (B.STONE, 6)))
            if not (1 <= x <= 9 and 1 <= z <= 8):
                continue
            sq = WHITE_SQ if (x // 2 + z // 2) % 2 else BLACK_SQ
            edge = x in (1, 9) or z in (1, 8)
            for y in range(0, BASE):
                if edge or y == BASE - 1 or (x % 4 == 1 and z % 4 == 1):
                    c.set(x, y, z, *sq)
    # the trap into the vault, beside the knight, and its ladder
    for y in range(0, BASE):
        c.set(2, y, 2, B.LADDER, 3)
    # steps up the pedestal's south face
    for x in range(4, 7):
        c.set(x, 0, 10, 156, 3)                                  # quartz stairs
        c.set(x, 0, 9, *WHITE_SQ)
        c.set(x, 1, 9, 156, 3)
    # the knight
    for i, (a, b) in enumerate(PROFILE):
        y = BASE + i
        for x in range(a, b + 1):
            for z in range(Z0, Z1 + 1):
                if i >= 11 and z in (Z0, Z1):
                    continue
                c.set(x, y, z, *(SHINE if (x + y) % 5 == 0 and z in (Z0, Z1) else BLACK))
    ears = BASE + len(PROFILE)
    for z in (4, 6):
        c.set(5, ears, z, *BLACK)
    # the open jaw: a cavity in the muzzle at rows 8 and 9, open at the front
    for x in range(7, 11):
        for z in range(4, 7):
            c.set(x, BASE + 8, z, B.AIR)
            c.set(x, BASE + 9, z, B.AIR)
    for x in range(8, 11):                                       # the muzzle's top, over the jaw
        for z in range(Z0, Z1 + 1):
            c.set(x, BASE + 10, z, *BLACK)
    c.set(9, BASE + 11, 4, B.WOOL, 0)                            # an eye
    c.set(9, BASE + 11, 6, B.WOOL, 0)
    # the mane: a stair of blocks up the knight's back, along z and back again, a block higher each step
    path = []
    seq = [(1, z) for z in range(Z0, Z1 + 1)] + [(0, z) for z in range(Z1, Z0 - 1, -1)]
    y = BASE
    k = 0
    while y < BASE + len(PROFILE) - 1:
        x, z = seq[k % len(seq)]
        path.append((x, y, z))
        y += 1
        k += 1
    for x, y, z in path:
        if x == 0:
            c.set(x, y, z, *BLACK)                               # the mane's outer tufts stand free of the neck
        else:
            for xx in range(x, PROFILE[y - BASE][0]):
                c.set(xx, y, z, *BLACK)
