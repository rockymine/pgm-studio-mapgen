"""Abandoned Mine: a terraced rocky hill with a timber-framed adit, rails and ore carts running out of it, a winch
over a shaft that drops into an ore-studded cave (cut away on the west face), a miners' shack, crates, TNT and
boulders."""
import random

from kit import Chunk

ORES = ("16", "15", "14", "16", "73", "56", "21", "16", "15")
POST, BEAM, PLANK = "17:1", "17:5", "5:1"


def ore(rng):
    return rng.choice(ORES)


def adit(c, rng):
    """The tunnel into the hill, x 6..10, z 3..9, three wide inside its timber frames, rails down the middle."""
    c.lower(6, 3, 10, 9, 0)
    c.roof(6, 3, 10, 6, 4, 9)
    c.roof(6, 7, 10, 8, 4, 7)
    c.roof(6, 9, 10, 9, 4, 5)
    for z in (9, 7, 5, 3):
        for y in range(0, 3):
            c.set(6, y, z, POST); c.set(10, y, z, POST)
        for x in range(6, 11):
            c.set(x, 3, z, BEAM)
    for z in (8, 6, 4):                                 # planked lagging between the frames
        for y in range(0, 3):
            if rng.random() < .55:
                c.set(6, y, z, PLANK)
            if rng.random() < .55:
                c.set(10, y, z, PLANK)
    for z in (9, 5):                                    # cross braces
        c.set(7, 2, z, "126:9"); c.set(9, 2, z, "126:9")
    c.box(6, 4, 9, 10, 4, 9, "5:1")                     # the lintel board over the portal
    c.set(8, 4, 10, "68:3")
    c.set(5, 5, 9, "17:1"); c.set(11, 5, 9, "17:1")
    for z in (4, 6, 8):
        c.set(7, 2, z, "50:1"); c.set(9, 2, z, "50:2")
    c.set(6, 2, 10, "50:3"); c.set(10, 2, 10, "50:3")
    # ore on the walls and at the face
    for z in range(3, 10):
        for y in range(0, 4):
            if rng.random() < .22 and (5, z) != (5, 9):
                c.set(5, y, z, ore(rng)); c.set(11, y, z, ore(rng)) if rng.random() < .8 else None
    for x in range(6, 11):
        for y in range(0, 4):
            c.set(x, y, 2, ore(rng) if rng.random() < .5 else "1")
    c.set(8, 0, 3, "87")
    # rails out to the south edge, a bumper at the face
    for z in range(4, 16):
        c.set(8, 0, z, "66:0")
    c.set(8, 0, 3, "98:2"); c.set(8, 1, 3, "50:5")
    for x, z in ((7, 3), (9, 3)):
        c.set(x, 0, z, "13") ; c.set(x, 0, z, "16")
    # carts: a hopper under a heap of ore
    for z, load in ((6, "15"), (7, "173"), (12, "14"), (13, "16")):
        c.set(8, 0, z, "154:0"); c.set(8, 1, z, load)
    c.set(8, 1, 7, "173"); c.set(8, 2, 7, "173")
    # spilled ore and a fallen beam
    c.set(7, 0, 5, "16"); c.set(9, 0, 8, "15"); c.set(7, 0, 8, "13"); c.set(9, 0, 4, "13")
    c.set(9, 0, 6, "17:9"); c.set(10, 0, 6, "17:9")
    c.set(7, 0, 7, "30"); c.set(9, 0, 5, "30")
    for x, z in ((6, 4), (10, 8), (6, 8), (10, 4)):
        c.set(x, 3, z, "30")


def cave(c, rng):
    """The ore cave under the western flank, a shaft up to the surface and a winch over it."""
    c.lower(0, 5, 5, 14, -6)
    c.roof(0, 5, 5, 8, -2, 0)
    c.roof(0, 11, 5, 14, -2, 0)
    c.roof(0, 9, 1, 10, -2, 0)
    c.roof(4, 9, 5, 10, -2, 0)
    # ore studs in the walls, ceiling and the back of the cave
    for y in range(-6, -2):
        for z in range(5, 15):
            if rng.random() < .45:
                c.set(6, y, z, ore(rng))
        for x in range(0, 6):
            if rng.random() < .4:
                c.set(x, y, 4, ore(rng)); c.set(x, y, 15, ore(rng)) if rng.random() < .8 else None
    for x in range(0, 6):
        for z in range(5, 15):
            if rng.random() < .22 and not (2 <= x <= 3 and 9 <= z <= 10):
                c.set(x, -2, z, ore(rng))
    # timber frames on the cut face and midway
    for x in (0, 3):
        for z in (6, 13) if x == 0 else (6, 13):
            for y in range(-6, -2):
                c.set(x, y, z, POST)
        for z in range(6, 14):
            c.set(x, -3, z, BEAM.replace(":5", ":9")) if x == 0 else c.set(x, -3, z, "17:9")
    # floor: gravel and rails, a loaded cart
    for z in range(7, 13):
        for x in range(0, 6):
            if rng.random() < .35:
                c.set(x, -7, z, "13" if rng.random() < .6 else "3:1")
    for z in range(7, 13):
        c.set(4, -6, z, "66:0")
    c.set(4, -6, 10, "154:0"); c.set(4, -5, 10, "173")
    c.set(4, -6, 8, "154:0"); c.set(4, -5, 8, "15")
    # TNT and a chest, pickaxes on posts, lanterns on the beams
    c.box(1, -6, 12, 2, -6, 12, "46"); c.set(1, -5, 12, "46"); c.set(0, -6, 12, "5:1")
    c.set(2, -5, 12, "126:1")
    c.set(1, -6, 7, "54:3"); c.set(2, -6, 7, "58"); c.set(1, -6, 8, "170:0")
    c.set(1, -4, 6, "69:3"); c.set(1, -5, 6, "69:3")
    for x, z in ((0, 9), (3, 8), (3, 11), (0, 11)):
        c.set(x, -4, z, "85"); c.set(x, -5, z, "89")
    c.set(5, -6, 7, "89")
    c.set(5, -6, 12, "30"); c.set(0, -3, 6, "30"); c.set(0, -3, 13, "30")
    c.set(1, -6, 10, "13"); c.set(0, -6, 9, "56")
    # a puddle where the cave drips
    c.set(2, -7, 10, "9")
    # headframe over the shaft (cells x 2..3, z 9..10): two A-frames carrying a winch drum
    for x in (1, 4):
        for z in (8, 11):
            for y in range(0, 5):
                c.set(x, y, z, POST)
        for z in range(8, 12):
            c.set(x, 5, z, "17:9")
        c.set(x, 6, 9, "126:1"); c.set(x, 6, 10, "126:1")
    for x in (2, 3):
        c.set(x, 5, 9, "17:5")
    for y in range(-2, 5):
        c.set(2, y, 9, "101")
    c.set(2, -4, 9, "118:3")                            # the bucket on its chain
    c.set(0, 5, 9, "17:5")
    c.set(5, 5, 9, "85"); c.set(5, 4, 9, "85")
    c.set(1, 2, 7, "85"); c.set(1, 3, 7, "89")        # lantern on a post


def shack(c, rng):
    """A miners' shack east of the rails: spruce walls on log corners, a gabled stair roof with a chimney, and a
    bunk, stove, chest and bench inside."""
    x0, x1, z0, z1 = 11, 14, 10, 14
    for y in range(0, 3):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) and z in (z0, z1):
                    c.set(x, y, z, POST)
                elif x in (x0, x1) or z in (z0, z1):
                    c.set(x, y, z, PLANK)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.set(x, -1, z, "5:1")
    c.set(x0, 0, 12, "64:0"); c.set(x0, 1, 12, "64:8")
    for x, z in ((12, 14), (13, 14), (x1, 12), (12, 10), (13, 10)):
        c.set(x, 1, z, "102")
    # roof: ridge along z over x 12..13, slopes to the long walls
    for z in range(z0 - 1, z1 + 2):
        c.set(x0 - 1, 3, z, "134:0"); c.set(x1 + 1, 3, z, "134:1")
        c.set(x0, 4, z, "134:0"); c.set(x1, 4, z, "134:1")
        c.set(x0 + 1, 5, z, "134:0"); c.set(x1 - 1, 5, z, "134:1")
        c.set(x0, 3, z, PLANK); c.set(x1, 3, z, PLANK)
        c.set(x0 + 1, 4, z, "5:1")
    for z in range(z0, z1 + 1):
        c.set(12, 3, z, "5:1"); c.set(13, 3, z, "5:1")
        c.set(12, 4, z, "5:1"); c.set(13, 4, z, "5:1")
    for x in (12, 13):                                   # gable ends
        for z in (z0, z1):
            c.set(x, 3, z, "5:1"); c.set(x, 4, z, "5:1")
    c.box(13, 3, 13, 13, 7, 13, "4"); c.set(13, 8, 13, "44:4")
    # inside
    c.set(13, 0, 11, "26:0"); c.set(13, 0, 12, "26:8")
    c.set(12, 0, 11, "61:3"); c.set(12, 0, 13, "54:2"); c.set(13, 0, 13, "58")
    c.set(12, 2, 12, "89")
    # porch: lantern post, a bench and a crate
    c.set(10, 0, 10, "85"); c.set(10, 1, 10, "85"); c.set(10, 2, 10, "89")
    c.set(10, 0, 13, "126:1"); c.set(10, 0, 14, "126:1")
    c.set(9, 0, 12, "17:5")


def yard(c, rng):
    """Clutter on the terraces and round the portal."""
    # crates and barrels by the rails
    c.prop("barrels", 11, 0, 9)
    c.prop("crates", 5, 0, 11)
    c.box(11, 0, 5, 11, 0, 5, "46"); c.set(12, 0, 5, "46"); c.set(11, 1, 5, "46")
    c.set(13, 0, 5, "54:4"); c.set(12, 0, 6, "170:0")
    # ore heaps, stepped
    heap = [((4, 0, 12), "16"), ((5, 0, 12), "15"), ((4, 0, 13), "14"), ((5, 0, 13), "16"), ((4, 1, 12), "16"),
            ((5, 1, 13), "13"), ((6, 0, 13), "13"), ((6, 0, 12), "15"), ((3, 0, 13), "16"), ((4, 1, 13), "15")]
    # (x 0..5, z 6..13 is the cave roof; heaps stand on it at y 0)
    for (x, y, z), block in heap:
        c.set(x, y, z, block)
    c.set(6, 0, 11, "173")
    c.set(7, 0, 11, "44:3")
    # fenced shaft collar and a warning stack
    c.set(2, 0, 11, "85"); c.set(3, 0, 11, "85"); c.set(2, 0, 8, "85"); c.set(3, 0, 8, "85")
    # a lantern on the upper terrace
    c.set(11, 8, 3, "89")
    # lanterns: fence posts topped with glowstone
    for x, z in ((6, 10), (10, 10)):
        c.set(x, 0, z, "85"); c.set(x, 1, z, "85"); c.set(x, 2, z, "89")
    # a pick and shovel leaning against the shack
    c.set(9, 1, 12, "69:2")
    # dead scrub and stones on the hill
    for x, y, z in ((2, 5, 5), (13, 5, 4), (6, 11, 3), (9, 11, 4), (3, 8, 3), (12, 8, 6)):
        c.set(x, y, z, "32")
    for x, y, z in ((5, 11, 4), (10, 11, 5), (7, 11, 6)):
        c.set(x, y, z, "48"); c.set(x, y + 1, z, "139:1") if (x + z) % 2 else None
    c.set(8, 11, 5, "13")


def hill_top(x, z):
    """Local height of the hill's ground at a cell."""
    if 4 <= x <= 11 and 2 <= z <= 6:
        return 9
    if 3 <= x <= 12 and 2 <= z <= 8:
        return 7
    if 1 <= x <= 14 and 2 <= z <= 9:
        return 5
    return 0


def paint_hill(c, rng):
    """Patches of turf, coarse dirt, gravel and moss on the hill tops, so the rock is not one grey."""
    for x in range(1, 15):
        for z in range(2, 10):
            top = hill_top(x, z) - 1
            if top < 0 or (x, z) in {(6, 9)} or (6 <= x <= 10 and 3 <= z <= 9 and top <= 4):
                continue
            if (x, top, z) in c.blocks or (x < 6 and z >= 5):
                continue
            roll = rng.random()
            c.set(x, top, z, "2" if roll < .35 else "3:1" if roll < .5 else "13" if roll < .65
                  else "48" if roll < .75 else "3:2" if roll < .82 else "1")


def build():
    c = Chunk("mine", "Abandoned Mine", "rock",
              "A terraced hill with a timber-framed adit, ore carts on rails, a winch over a shaft and an "
              "ore-studded cave cut away on the west face.")
    rng = random.Random(11)
    c.raise_(1, 2, 14, 9, 5)
    c.raise_(3, 2, 12, 8, 7)
    c.raise_(4, 2, 11, 6, 9)
    adit(c, rng)
    cave(c, rng)
    shack(c, rng)
    yard(c, rng)
    paint_hill(c, rng)
    c.set(11, 8, 4, "2")
    c.tree(11, 4, "tiny-spruce-4")
    c.set(4, 8, 3, "2")
    c.tree(4, 3, "tiny-spruce-2")
    for x, z, y in ((13, 8, 4), (1, 3, 4), (12, 9, 4), (7, 2, 4)):           # hand-heaped scree
        c.set(x, y, z, "4"); c.set(x - 1, y, z, "48"); c.set(x, y, z - 1, "1") if x != 1 else None
        c.set(x, y + 1, z, "48" if x % 2 else "1")
    c.prop("wheelbarrow", 1, 0, 13, 0)
    c.cover([(0, 0), (16, 0), (16, 6), (0, 6)], coverage=0.35, fernShare=0.3, flowerShare=0.02)
    c.cover([(6, 10), (16, 10), (16, 16), (6, 16)], coverage=0.25, fernShare=0.3, deadBushShare=0.2)
    return c
