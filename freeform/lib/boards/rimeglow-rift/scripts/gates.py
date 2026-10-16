"""The gates at the heads of the three crossings: twin towers over the causeway's road, a pair of lit pylons at each
side bridge, and the plazas they stand on."""
from pgmvox import B
from stamp import AIR

DECK = 59


def tower(S, H, x0, z0, doors_toward):
    """A 5x5 tower of stone: floored at the deck and again 7 above it, a ladder up the inside, arrow slits, a door to the
    road, and a crown on corbels that stands a block proud of the shaft with its crenels on the outer edge."""
    x1, z1 = x0 + 4, z0 + 4
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            S.foot(H, x, z, DECK, "rock")
    for y in range(DECK, DECK + 14):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = x in (x0, x1) or z in (z0, z1)
                corner = x in (x0, x1) and z in (z0, z1)
                if y == DECK:
                    S.set(x, y, z, "pave_c")
                elif edge:
                    band = y in (DECK + 7, DECK + 13)
                    S.set(x, y, z, "log" if corner else ("plinth" if band else "wall"))
                else:
                    S.set(x, y, z, "plank" if y == DECK + 7 else AIR)
    for y in (DECK + 3, DECK + 10):                          # arrow slits
        S.set(x0 + 2, y, z0, (B.IRON_BARS, 0)); S.set(x0 + 2, y, z1, (B.IRON_BARS, 0))
        S.set(x0, y, z0 + 2, (B.IRON_BARS, 0)); S.set(x1, y, z0 + 2, (B.IRON_BARS, 0))
    door_x = x1 if doors_toward == "e" else x0
    for y in (DECK + 1, DECK + 2):
        S.set(door_x, y, z0 + 2, AIR)
    lx = x0 + 1 if doors_toward == "e" else x1 - 1
    for y in range(DECK + 1, DECK + 14):
        S.ladder(lx, y, z1 - 1, "s")
    # the crown: a ring one block out on upside-down stairs, a floor, and crenels on its edge
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            outer = x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1)
            if outer:
                face = "w" if x == x0 - 1 else "e" if x == x1 + 1 else "n" if z == z0 - 1 else "s"
                toward = {"w": "e", "e": "w", "n": "s", "s": "n"}[face]
                S.stair(x, DECK + 13, z, "wall", toward, upside=True)
                S.set(x, DECK + 14, z, "plinth")
                if (x + z) % 2 == 0:
                    S.set(x, DECK + 15, z, "wall")
            elif x in (x0, x1) or z in (z0, z1):
                S.set(x, DECK + 14, z, "plinth")
            else:
                S.set(x, DECK + 14, z, "pave_c")
    S.ladder(lx, DECK + 14, z1 - 1, "s")                      # the ladder comes up through a hatch in the crown's floor
    S.set(x0 + 2, DECK + 15, z0 + 2, "wall")
    S.set(x0 + 2, DECK + 16, z0 + 2, "light")


def causeway_gate(S, H):
    tower(S, H, -9, -27, "e")
    tower(S, H, 4, -27, "w")
    # the lintel: an arch of stone across the road between the towers, at the first floor
    for x in range(-4, 4):
        for z in range(-27, -22):
            for y in range(DECK + 6, DECK + 9):
                S.set(x, y, z, "wall" if y != DECK + 6 else "plinth")
        for y in range(DECK + 1, DECK + 6):
            for z in range(-27, -22):
                S.set(x, y, z, AIR)
    for x in range(-4, 4):                                   # the arch's curve: stairs under the lintel's ends
        for z in (-27, -23):
            pass
    for z in range(-27, -22):
        S.stair(-4, DECK + 5, z, "wall", "e", upside=True) if False else None
        S.stair(-4, DECK + 5, z, "wall", "w", upside=True)
        S.stair(3, DECK + 5, z, "wall", "e", upside=True)
    # braziers on the plaza, either side of the road
    for x in (-6, 5):
        for z in (-19,):
            S.set(x, DECK + 1, z, (B.NETHERRACK, 0))
            S.set(x, DECK + 2, z, (B.FIRE, 0))
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                S.set(x + dx, DECK + 1, z + dz, "wall")


def pylons(S, H, xc):
    """Two stone pylons at the head of a side bridge, a lit cap on each and a banner between."""
    for x0 in (xc - 5, xc + 3):
        for x in range(x0, x0 + 3):
            for z in range(-22, -19):
                S.foot(H, x, z, DECK, "rock")
                for y in range(DECK, DECK + 9):
                    corner = x in (x0, x0 + 2) and z in (-22, -20)
                    S.set(x, y, z, ("wall" if y > DECK else "plinth") if not corner else "log")
        S.set(x0 + 1, DECK + 9, -21, "wall")
        S.set(x0 + 1, DECK + 10, -21, "light")
    for x in range(xc - 5, xc + 6):                          # a beam across the head of the bridge
        S.log(x, DECK + 8, -21, "x")
    for x in (xc - 1, xc, xc + 1):
        S.set(x, DECK + 7, -21, "fence")


def banner(S, x, y, z, rot=0):
    """A standing banner on a post, in the half's colour: light blue in the north, orange in the south."""
    S.set(x, y, z, "fence")
    S.set(x, y + 1, z, "fence")
    S.banner(x, y + 2, z, 6 if not S.south else 14, [("bs", 15 if not S.south else 11)], rot=rot)


def plaza(S, H, xc):
    """The paved head of a crossing: a border, four stones in cells, a pair of shield walls before the bridge so those
    who cross have somewhere to stop, braziers either side, and a banner on a post."""
    for x in range(xc - 10, xc + 11):
        for z in range(-28, -15):
            edge = x in (xc - 10, xc + 10) or z in (-28, -16)
            pick = ((x // 3) * 7 + (z // 3) * 13 + ((x * 3 + z * 5) % 7 == 0)) % 4
            if S.get(x, DECK, z)[0] not in (B.FENCE, B.LOG):
                S.set(x, DECK, z, "plinth" if edge else ("pave_a", "pave_b", "pave_c", "pave_d")[pick])
            for y in range(DECK + 1, DECK + 3):
                if S.get(x, y, z)[0] in (B.SNOW_LAYER, B.CARPET, B.TALLGRASS):
                    S.set(x, y, z, AIR)
    # shield walls before the bridge, stepped, with merlons
    for side in (-1, 1):
        for k in range(4):
            x = xc + side * (5 + k)
            z = -18 - (k == 3)
            for y in range(DECK + 1, DECK + 3):
                S.set(x, y, z, "wall")
            if k % 2 == 0:
                S.set(x, DECK + 3, z, "wall")
    # braziers
    for side in (-1, 1):
        x, z = xc + side * 9, -20
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            S.set(x + dx, DECK + 1, z + dz, "wall")
        S.set(x, DECK, z, (B.NETHERRACK, 0))
        S.set(x, DECK + 1, z, (B.FIRE, 0))
    banner(S, xc - 9, DECK + 1, -18)
    banner(S, xc + 9, DECK + 1, -18)
