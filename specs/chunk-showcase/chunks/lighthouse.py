"""Lighthouse Point: a rocky headland with a red-and-white striped lighthouse, a keeper's cottage, and a cove
inlet with a plank pier, a rowboat, buoys and nets; a smugglers' cave is cut away under the south-west."""
import math
import random

from kit import Chunk

LX, LZ = 5, 5            # lighthouse centre
RED, WHITE = "35:14", "35:0"


def body(c, rng):
    """The striped tower from a stone foundation up to the gallery, the lantern room and the cap."""
    c.disc(LX, LZ, 3.3, 2, "98:2")
    c.disc(LX, LZ, 3.3, 3, "98:0", ring=1.0)
    c.disc(LX, LZ, 2.3, 3, "98:0")                       # floor
    for y in range(4, 22):
        radius = 2.7 if y <= 10 else 2.3 if y <= 16 else 2.0
        stripe = RED if ((y - 4) // 3) % 2 == 0 else WHITE
        c.disc(LX, LZ, radius, y, stripe, ring=1.0)
    for y in (11, 17):                                    # ledges where the tower steps in
        c.disc(LX, LZ, 2.7 if y == 11 else 2.3, y, "98:0", ring=1.0)
    # door, steps and slit windows
    c.set(LX, 4, LZ + 3, "64:3"); c.set(LX, 5, LZ + 3, "64:11")
    c.set(LX - 1, 4, LZ + 3, "98:3"); c.set(LX + 1, 4, LZ + 3, "98:3"); c.set(LX, 6, LZ + 3, "98:3")
    c.set(LX, 3, LZ + 4, "109:3"); c.set(LX - 1, 3, LZ + 4, "44:5"); c.set(LX + 1, 3, LZ + 4, "44:5")
    for y, (dx, dz) in ((8, (0, -2)), (8, (2, 0)), (13, (-2, 0)), (13, (0, 2)), (18, (0, -2)), (18, (2, 0)),
                        (19, (-2, 0))):
        c.set(LX + dx, y, LZ + dz, "102"); c.set(LX + dx, y + 1, LZ + dz, "102")
    c.set(LX - 3, 7, LZ, "102"); c.set(LX - 3, 8, LZ, "102")
    # the ladder inside
    for y in range(4, 25):
        c.set(LX, y, LZ - 2, "98:0"); c.set(LX, y, LZ - 1, "65:3")
    # gallery with its rail, and the stone under it
    c.disc(LX, LZ, 2.9, 22, "98:2", ring=1.2)
    c.disc(LX, LZ, 3.4, 23, "98:0")
    c.disc(LX, LZ, 3.4, 24, "85", ring=0.8)
    c.set(LX, 23, LZ - 1, None)
    # lantern room
    for y in (24, 25, 26):
        c.disc(LX, LZ, 1.9, y, "20", ring=1.0)
        c.set(LX, y, LZ - 1, "65:3") if y < 26 else None
    for dx, dz in ((2, 0), (-2, 0), (0, -2), (0, 2)):     # mullion posts, a door to the gallery
        for y in (24, 25, 26):
            c.set(LX + dx, y, LZ + dz, "98:3" if y == 26 else "101")
    c.set(LX, 24, LZ + 2, None); c.set(LX, 25, LZ + 2, None)
    c.set(LX, 24, LZ, "89"); c.set(LX, 25, LZ, "169"); c.set(LX, 26, LZ, "89")
    # cap
    for y, radius in ((27, 2.9), (28, 2.2), (29, 1.4)):
        c.disc(LX, LZ, radius, y, "159:14")
    c.disc(LX, LZ, 0.5, 30, "159:14")
    c.set(LX, 31, LZ, "101")


def cottage(c, rng):
    """The keeper's cottage: whitewash on a stone footing, a red stair roof, a chimney and a lit window."""
    x0, x1, z0, z1 = 10, 14, 2, 6
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.set(x, 0, z, "98:0")
            c.set(x, 1, z, "98:0") if x in (x0, x1) or z in (z0, z1) else None
    for y in (2, 3):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) and z in (z0, z1):
                    c.set(x, y, z, "17:1")
                elif x in (x0, x1) or z in (z0, z1):
                    c.set(x, y, z, WHITE)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not (x in (x0, x1) or z in (z0, z1)):
                c.set(x, 0, z, "5:1")
    c.set(x0, 1, 4, None)
    c.set(x0, 2, 4, "64:0"); c.set(x0, 3, 4, "64:8")
    for x, z in ((12, 2), (12, 6), (14, 4), (11, 6), (13, 6)):
        c.set(x, 3, z, "102")
        c.set(x, 2, z, "102")
    # roof along x
    for x in range(x0 - 1, x1 + 2):
        c.set(x, 4, z0 - 1, "108:2"); c.set(x, 5, z0, "108:2"); c.set(x, 6, z0 + 1, "108:2")
        c.set(x, 4, z1 + 1, "108:3"); c.set(x, 5, z1, "108:3"); c.set(x, 6, z1 - 1, "108:3")
        c.set(x, 7, 4, "44:4")
        c.set(x, 4, z0, "98:0") if x in (x0, x1) else None
    for x in range(x0 - 1, x1 + 2):
        c.set(x, 6, 4, "4")
    for x in (x0, x1):
        for z in range(z0 + 1, z1):
            c.set(x, 4, z, WHITE); c.set(x, 5, z, WHITE) if z == 4 or True else None
    c.box(13, 4, 5, 13, 8, 5, "98:0"); c.set(13, 9, 5, "44:0")
    # inside
    c.set(13, 1, 3, "26:0"); c.set(13, 1, 4, "26:8")
    c.set(11, 1, 3, "54:3"); c.set(12, 1, 5, "58"); c.set(11, 1, 5, "61:2")
    c.set(12, 3, 4, "89")
    # porch: a bench, a lantern post, a flag pole with a red pennant
    c.set(9, 1, 3, "85"); c.set(9, 2, 3, "85"); c.set(9, 3, 3, "89")
    c.set(9, 1, 5, "126:1"); c.set(9, 1, 6, "126:1")


def cove(c, rng):
    c.lower(10, 10, 15, 15, -3)
    for x in range(10, 16):
        for z in range(10, 16):
            for y in (-3, -2, -1):
                c.set(x, y, z, "9")
    # shore walls of stone round the cove
    for z in range(10, 16):
        for y in (-3, -2, -1):
            c.set(9, y, z, "1" if y == -3 else "48" if rng.random() < .4 else "1")
    for x in range(10, 16):
        for y in (-3, -2, -1):
            c.set(x, y, 9, "48" if rng.random() < .35 else "1")
    # the pier: deck flush with the ground, posts into the water, a T head
    for x in range(9, 14):
        c.set(x, -1, 12, "5:1" if x % 2 else "126:9")
    for z in (11, 13):
        c.set(13, -1, z, "5:1")
    c.set(13, -1, 12, "5:1")
    for x in (10, 12, 13):
        for y in (-3, -2):
            c.set(x, y, 12, "17:1")
    for x, z in ((13, 11), (13, 13)):
        for y in (-3, -2):
            c.set(x, y, z, "17:1")
        c.set(x, 0, z, "85"); c.set(x, 1, z, "85"); c.set(x, 2, z, "50:5")
    # crates and a barrel stack on the pier
    c.set(11, 0, 11, "54:3"); c.set(10, 0, 11, "170:0")
    c.set(11, 0, 13, "118:0")
    # moored rowboat, buoys
    c.prop("rowboat", 10, -1, 14, 0)
    c.set(14, -1, 11, "35:14"); c.set(14, 0, 11, "35:0")
    c.set(15, -1, 13, "35:0"); c.set(15, 0, 13, "35:14")
    c.set(11, -1, 10, "35:14")
    c.set(13, -1, 14, "35:14")


def yard(c, rng):
    """Clutter: nets, pots, rope and driftwood between the pier and the lighthouse; a path of flags."""
    # nets drying on a pole frame
    for y in range(1, 4):
        c.set(7, y, 10, "85"); c.set(7, y, 13, "85")
    for z in range(10, 14):
        c.set(7, 3, z, "85")
        c.set(7, 2, z, "30") if z in (11, 12) else None
    c.set(7, 1, 11, "30")
    # lobster pots (cauldrons with a trapdoor lid look) and rope coils
    c.set(8, 0, 10, "118:0"); c.set(8, 0, 11, "118:0")
    c.set(6, 0, 14, "171:12"); c.set(7, 0, 14, "171:12"); c.set(6, 0, 15, "171:12")
    c.set(8, 0, 14, "145:0")
    c.set(5, 0, 12, "17:5"); c.set(4, 0, 12, "17:5"); c.set(3, 0, 13, "17:1")
    # beach and path
    for z in range(0, 16):
        c.set(8, -1, z, "13") if z in range(0, 3) else None
    for z in range(2, 16):
        for x in (8, 9):
            if (x + z) % 2:
                c.set(x, -1, z, "13")
    # headland stairs from the north bridge and the west bridge
    for x in (7, 8, 9):
        c.set(x, 0, 1, "67:2")
    for z in (7, 8, 9):
        c.set(1, 0, z, "67:0")
    # rock and tide-pool details on the cliff top
    for x, z in ((2, 9), (10, 8), (3, 2), (9, 2), (2, 3)):
        c.set(x, 1, z, "48"); c.set(x, 2, z, "44:3") if (x + z) % 2 else None
    # hanging lantern pole by the door
    c.set(LX + 2, 4, LZ + 4, "85"); c.set(LX + 2, 5, LZ + 4, "85"); c.set(LX + 2, 6, LZ + 4, "89")
    c.set(LX - 2, 4, LZ + 4, "85"); c.set(LX - 2, 5, LZ + 4, "85"); c.set(LX - 2, 6, LZ + 4, "89")


def smugglers_cave(c, rng):
    """A cave under the south-west corner: a hidden cache, a lantern and a stretch of tide."""
    c.lower(0, 9, 6, 14, -7)
    c.roof(0, 9, 6, 14, -2, 0)
    floor = -8
    for x in range(0, 7):
        for z in range(9, 15):
            c.set(x, floor, z, "13" if rng.random() < .5 else "12")
    for y in range(-7, -2):
        for z in range(9, 15):
            if rng.random() < .3:
                c.set(7, y, z, rng.choice(("16", "15", "1:5", "4", "14")))
    for z in (9, 14):
        for y in range(-7, -2):
            c.set(0, y, z, "17:1")
    for z in range(9, 15):
        c.set(0, -3, z, "17:9")
        c.set(3, -3, z, "17:9")
    for y in range(-7, -3):
        c.set(3, y, 9, "17:1"); c.set(3, y, 14, "17:1")
    c.set(1, -7, 10, "54:3"); c.set(2, -7, 10, "54:3")
    c.set(1, -7, 13, "118:3"); c.set(2, -7, 13, "170:0"); c.set(2, -6, 13, "170:0")
    c.set(4, -7, 10, "145:0"); c.set(5, -7, 11, "46"); c.set(5, -7, 12, "46"); c.set(5, -6, 11, "46")
    c.set(6, -7, 12, "89"); c.set(6, -6, 13, "89")
    c.set(3, -7, 11, "144:1"); c.set(0, -7, 12, "144:1")
    c.set(6, -3, 14, "30"); c.set(0, -3, 10, "30"); c.set(4, -3, 9, "30")
    for x, z in ((3, 12), (4, 12), (3, 13), (4, 13), (5, 13), (2, 12)):
        c.set(x, -8, z, "9"); c.set(x, -7, z, "9") if (x + z) % 2 else None
    # a stair-stepped passage up to the surface
    c.set(1, -4, 12, "85"); c.set(1, -5, 12, "85"); c.set(1, -6, 12, "89")


def rocks(c):
    """Hand-heaped rock piles on the cliff edges: cobble, mossy cobble and stone, stepped."""
    for x, y, z in ((9, 1, 8), (2, 1, 9), (10, 1, 3), (8, 1, 2), (12, 0, 8), (13, 0, 9), (2, 1, 2)):
        c.set(x, y, z, "48"); c.set(x + 1, y, z, "4"); c.set(x, y, z + 1, "1")
        c.set(x, y + 1, z, "4" if (x + z) % 2 else "48"); c.set(x - 1, y, z, "44:3") if x > 1 else None
        c.set(x + 1, y + 1, z, "44:3") if (x + z) % 3 == 0 else None


def shore(c, rng):
    """Sand along the cove, gravel and turf patches on the headland so the rock is not one grey."""
    for z in range(10, 16):
        c.set(8, -1, z, "12" if rng.random() < .7 else "13")
    for x in range(2, 11):
        for z in range(2, 10):
            top = 2 if (3 <= x <= 7 and 3 <= z <= 7) else 1
            if (x, top, z) in c.blocks or (x, top + 1, z) in c.blocks or math_hypot(x - LX, z - LZ) < 3.6:
                continue
            if rng.random() < .4:
                c.set(x, top, z, rng.choice(("2", "2", "3:1", "13", "48")))


def math_hypot(dx, dz):
    return math.hypot(dx, dz)


def build():
    c = Chunk("lighthouse", "Lighthouse Point", "rock",
              "A red-and-white lighthouse on a rocky headland, a keeper's cottage, and a cove with a pier, "
              "rowboat, nets and buoys above a cut-away smugglers' cave.")
    rng = random.Random(41)
    c.raise_(2, 2, 10, 9, 2)
    c.raise_(3, 3, 7, 7, 3)
    c.raise_(10, 2, 14, 6, 1)
    body(c, rng)
    cottage(c, rng)
    cove(c, rng)
    yard(c, rng)
    shore(c, rng)
    rocks(c)
    smugglers_cave(c, rng)
    c.cover([(0, 0), (16, 0), (16, 9), (0, 9)], coverage=0.15, fernShare=0.3, deadBushShare=0.2)
    return c
