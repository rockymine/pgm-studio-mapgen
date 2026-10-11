"""The Viaduct: two stone arches of a mountain railway carrying a little green steam engine and its tender, stopped
on the track. Rough stone steps climb the south face of the piers to the deck; the cab and the tender are the
places to hide, high over the street where no eye on the ground can see in."""
from mc import B

NAME = "The Viaduct"
KIND = "structure"

STONE, STONE2, CAP = (B.STONEBRICK, 0), (B.STONE, 5), (B.STONEBRICK, 3)
Z0, Z1 = 2, 8                                                    # the viaduct's width: parapets at 2 and 8
DECK = 7
GREEN, BLACK, BRASS, RED = (B.STAINED_CLAY, 13), (B.COAL_BLOCK, 0), (B.GOLD_BLOCK, 0), (B.STAINED_CLAY, 14)


def arch_top(x):
    """The underside of the arches: piers at x 0-1, 5 and 9-10, a round arch between each pair."""
    if x in (0, 1, 5, 9, 10):
        return 0
    span = (2, 4) if x < 5 else (6, 8)
    mid = (span[0] + span[1]) / 2
    return {0: 5, 1: 4}.get(abs(x - mid), 5) if abs(x - mid) < 1 else 4


def build(c):
    c.fill(0, -1, 0, 10, -1, 10, B.GRASS)
    for x in range(11):
        for z in range(Z0, Z1 + 1):
            under = arch_top(x)
            for y in range(under, DECK + 1):
                c.set(x, y, z, *(CAP if y == DECK else STONE2 if (x + y + z) % 5 == 0 else STONE))
    # a stream under the west arch, stones under the east
    for z in range(0, 11):
        for x in (2, 3, 4):
            if z < Z0 or z > Z1:
                c.set(x, -1, z, B.GRAVEL)
    c.fill(3, 0, 0, 3, 0, 10, B.WATER)
    c.fill(3, -1, 0, 3, -1, 10, B.GRAVEL)
    # the parapets, with a gap on the south side where the steps arrive
    for x in range(11):
        for z in (Z0, Z1):
            if not (z == Z0 and x == 7):
                c.set(x, DECK + 1, z, B.COBBLE_WALL)
    # rough stone steps up the south face, from the ground at the west end to the deck
    for k in range(DECK):
        c.set(k, k, Z0 - 1, *STONE2)
    c.set(DECK, DECK, Z0 - 1, *STONE2)
    c.set(DECK, DECK + 1, Z0, B.AIR)
    # the track: rails down the middle of the deck
    for x in range(11):
        c.set(x, DECK + 1, 5, B.RAIL, 1)
    # the engine: boiler east, smokestack, cab at the west end, red buffer beam
    for x in range(5, 10):
        for z in range(4, 7):
            for y in (DECK + 1, DECK + 2, DECK + 3):
                if y == DECK + 1 and z == 5:
                    continue
                c.set(x, y, z, *(BRASS if x == 7 and y == DECK + 2 else GREEN if y > DECK + 1 else BLACK))
    c.set(8, DECK + 4, 5, *BLACK)
    c.set(8, DECK + 5, 5, *BLACK)
    c.set(8, DECK + 6, 5, B.COBBLE_WALL)
    c.set(6, DECK + 4, 5, *BRASS)                                # the dome
    c.fill(10, DECK + 1, 4, 10, DECK + 1, 6, *RED)
    # the cab: green walls, a black roof, its door on the south side facing the steps
    for x in range(1, 5):
        for z in range(4, 7):
            edge = x in (1, 4) or z in (4, 6)
            for y in range(DECK + 1, DECK + 4):
                if edge:
                    window = y == DECK + 2 and (z in (4, 6) and x in (2, 3))
                    c.set(x, y, z, *((B.PANE, 0) if window else GREEN))
            c.set(x, DECK + 4, z, *BLACK)
    c.set(2, DECK + 1, 4, B.AIR); c.set(2, DECK + 2, 4, B.AIR)    # the cab's door
    c.set(3, DECK + 1, 5, B.FURNACE)                             # the firebox
    # the tender behind the cab, heaped with coal: a hollow to drop into
    for x in (0,):
        for z in range(4, 7):
            for y in range(DECK + 1, DECK + 3):
                c.set(x, y, z, *GREEN)
    # buttresses and ivy on the piers
    for x, z in ((5, 9), (0, 9), (10, 1), (10, 9)):
        for y in range(0, 4):
            c.set(x, y, z, *STONE2)
        c.set(x, 4, z, B.STONEBRICK_STAIRS, 3 if z == 1 else 2)
