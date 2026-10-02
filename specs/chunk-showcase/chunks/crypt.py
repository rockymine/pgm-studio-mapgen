"""The Forgotten Crypt: a ruined, overgrown chapel whose nave has collapsed into a stair trench, leading down to
a stone-brick vault with pillars, sarcophagi, an iron-bar cell, a lava well and a flooded corner. The vault is cut
away on the west side of the chunk."""
import random

from kit import Chunk

FLOOR = -9          # vault floor course
CEIL = -4           # last air course in the vault


def brick(rng, mossy=0.3, cracked=0.25):
    roll = rng.random()
    return "98:1" if roll < mossy else "98:2" if roll < mossy + cracked else "98:0"


def vault(c, rng):
    c.lower(0, 2, 8, 13, FLOOR + 1)
    c.roof(0, 2, 8, 13, -3, 0)
    c.lower(9, 6, 14, 9, FLOOR + 1)                     # the stair trench
    # floor, a chequer of dark and light bricks
    for x in range(0, 9):
        for z in range(2, 14):
            c.set(x, FLOOR, z, "98:0" if (x + z) % 2 else "98:2" if rng.random() < .5 else "98:1")
    # lining
    for y in range(FLOOR + 1, CEIL + 1):
        for x in range(0, 9):
            c.set(x, y, 2, brick(rng)); c.set(x, y, 13, brick(rng))
        for z in range(2, 14):
            if not 6 <= z <= 9:
                c.set(8, y, z, brick(rng))
        for x in range(9, 15):
            c.set(x, y, 5, brick(rng)); c.set(x, y, 10, brick(rng))
    for y in range(CEIL + 1, 0):
        for x in range(9, 15):
            c.set(x, y, 5, brick(rng, .45)); c.set(x, y, 10, brick(rng, .45))
        for z in range(6, 10):
            c.set(8, y, z, "98:1") if y < -1 else None
    # ceiling frieze of chiselled bricks every third course
    for x in range(0, 8):
        for z in range(3, 13):
            if z in (3, 12) or x % 3 == 1:
                c.set(x, CEIL, z, "98:3" if (x + z) % 2 == 0 else "98:2")
    # stairs down the trench, solid under each tread
    for step in range(8):
        x, y = 14 - step, -1 - step
        for z in (6, 7, 8, 9):
            c.set(x, y, z, "109:0" if step % 3 else "67:0")
            for under in range(FLOOR, y):
                c.set(x, under, z, brick(rng))
    # pillars with stair feet and chiselled caps
    for x, z in ((2, 5), (5, 5), (2, 10), (5, 10)):
        for y in range(FLOOR + 1, CEIL):
            c.set(x, y, z, "155:2" if y not in (FLOOR + 1,) else "155:1")
        c.set(x, CEIL, z, "98:3")
        for dx, dz, data in ((1, 0, 1), (-1, 0, 0), (0, 1, 3), (0, -1, 2)):
            c.set(x + dx, FLOOR + 1, z + dz, f"109:{data}") if rng.random() < .7 else None
    # sarcophagi on the north wall: stone base, slab lid, a skull at the head
    for x0, z0 in ((1, 3), (5, 3)):
        c.box(x0, FLOOR + 1, z0, x0 + 2, FLOOR + 1, z0 + 1, "98:0")
        c.box(x0, FLOOR + 2, z0, x0 + 2, FLOOR + 2, z0 + 1, "44:7")
        c.set(x0, FLOOR + 3, z0, "144:1")
    c.set(2, FLOOR + 2, 3, "155:0"); c.set(6, FLOOR + 2, 4, "44:13")
    # a lone sarcophagus across the room, open, with a chest at its foot
    c.box(1, FLOOR + 1, 7, 2, FLOOR + 1, 9, "98:2")
    c.box(1, FLOOR + 2, 7, 2, FLOOR + 2, 9, "44:5")
    c.set(1, FLOOR + 2, 8, "144:1"); c.set(2, FLOOR + 2, 7, "30")
    c.set(1, FLOOR + 1, 10, "54:2")
    # iron-bar cell in the south-east corner
    c.box(4, FLOOR + 1, 11, 4, FLOOR + 4, 12, "101")
    c.box(5, FLOOR + 4, 11, 7, FLOOR + 4, 12, "101")
    c.box(5, FLOOR + 1, 11, 7, FLOOR + 1, 11, "101")
    c.set(6, FLOOR + 1, 12, "54:2"); c.set(7, FLOOR + 1, 12, "144:1"); c.set(5, FLOOR + 1, 12, "30")
    c.set(7, FLOOR + 2, 12, "30"); c.set(4, FLOOR + 1, 10, "144:1")
    # lava well in the south-west
    c.box(0, FLOOR + 1, 11, 2, FLOOR + 1, 12, "98:0")
    c.box(1, FLOOR, 11, 1, FLOOR, 12, "11"); c.set(1, FLOOR + 1, 11, "11"); c.set(1, FLOOR + 1, 12, "11")
    c.set(0, FLOOR + 1, 11, "11"); c.set(0, FLOOR, 11, "11")
    c.set(2, FLOOR + 1, 11, "11"); c.set(2, FLOOR, 11, "11")
    # flooded corner with a fallen grate
    c.box(5, FLOOR, 3, 7, FLOOR, 4, "9"); c.box(6, FLOOR + 1, 3, 7, FLOOR + 1, 4, "9")
    c.set(5, FLOOR + 1, 3, "111"); c.set(7, FLOOR + 1, 3, "111")
    c.box(5, FLOOR + 1, 5, 7, FLOOR + 2, 5, "101")
    # light and rot
    for x, z in ((3, 3), (3, 12), (6, 7), (0, 6)):
        c.set(x, CEIL - 1, z, "89") if (x, z) == (6, 7) else None
    c.set(6, CEIL, 7, "169"); c.set(0, CEIL, 8, "89"); c.set(3, CEIL, 7, "89")
    for x, z in ((3, 3), (4, 12), (7, 3)):
        c.set(x, -6, z + 1 if z == 3 else z - 1, "50:3" if z == 3 else "50:4")
    for x, y, z in ((0, CEIL, 3), (7, CEIL, 3), (0, CEIL, 12), (7, CEIL, 12), (4, CEIL, 7), (8, CEIL, 5)):
        c.set(x, y, z, "30")
    for x, z in ((3, 7), (6, 8), (4, 9), (3, 12), (0, 5)):
        c.set(x, FLOOR + 1, z, "144:1") if (x + z) % 3 == 0 else c.set(x, FLOOR + 1, z, "30")
    # ore glint in the cut face under the floor and a buried chest
    c.set(0, FLOOR - 2, 7, "56"); c.set(0, FLOOR - 3, 8, "56"); c.set(0, FLOOR - 1, 4, "14")
    c.set(0, FLOOR - 4, 10, "21"); c.set(0, FLOOR - 2, 12, "129")


def chapel(c, rng):
    """Ruined walls round the trench, ragged at the top, with a broken portal over the stairs."""
    heights = {}
    for x in range(9, 16):
        heights[(x, 3)] = rng.choice((2, 3, 4, 3, 5)) if x < 15 else 2
        heights[(x, 12)] = rng.choice((2, 3, 4, 3)) if x < 15 else 2
    for (x, z), top in heights.items():
        for y in range(0, top + 1):
            c.set(x, y, z, brick(rng, .4, .3))
    for x in (9, 12, 15):                                  # buttress pillars, taller
        for z in (3, 12):
            for y in range(0, 7 if x != 15 else 3):
                c.set(x, y, z, "98:0" if y % 2 == 0 else "98:1")
            c.set(x, 7 if x != 15 else 3, z, "109:2" if z == 3 else "109:3")
    # west end wall: broken, a portal arch over the trench
    for z in range(3, 13):
        top = 6 if z in (3, 4, 11, 12) else 3
        if 6 <= z <= 9:
            continue
        for y in range(0, top + 1):
            c.set(9, y, z, brick(rng))
    c.box(9, 0, 5, 9, 5, 5, "98:0"); c.box(9, 0, 10, 9, 5, 10, "98:0")
    c.set(9, 5, 6, "109:7"); c.set(9, 5, 9, "109:6")
    c.box(9, 6, 5, 9, 6, 10, "98:3"); c.set(9, 6, 7, "98:2")
    c.set(9, 7, 7, "44:5"); c.set(9, 7, 8, "44:5")
    c.box(9, 3, 6, 9, 4, 6, "101"); c.box(9, 3, 9, 9, 4, 9, "101")      # gate stubs hanging from the arch
    c.set(9, 4, 7, "101"); c.set(9, 4, 8, "101")
    for y in range(0, 3):
        c.set(9, y, 7, "101") if y == 0 and False else None
    # side wall windows: knock out arched gaps
    for x in (10, 11, 13, 14):
        for z in (3, 12):
            c.set(x, 1, z, "101") if x in (11, 14) else None
    # nave floor either side of the trench: cracked flags and moss
    for x in range(10, 15):
        for z in (4, 11):
            c.set(x, -1, z, "98:2" if rng.random() < .5 else "48")
    # vines up the outer faces, cobwebs in the corners
    for x in range(9, 15):
        for y in range(0, 3):
            if rng.random() < .5 and (x, 3) in heights and y < heights[(x, 3)]:
                c.set(x, y, 2, "106:1")
            if x < 11 and rng.random() < .5 and (x, 12) in heights and y < heights[(x, 12)]:
                c.set(x, y, 13, "106:4")
    c.set(11, 3, 3, "30"); c.set(14, 2, 12, "30"); c.set(10, 3, 12, "30"); c.set(13, 2, 3, "30")


def graveyard(c, rng):
    stones = ((1, 4), (3, 6), (2, 9), (5, 8), (7, 12), (4, 12), (6, 4))
    for index, (x, z) in enumerate(stones):
        form = index % 3
        if form == 0:
            c.set(x, 0, z, "98:2"); c.set(x, 1, z, "44:3")
        elif form == 1:
            c.set(x, 0, z, "139:1"); c.set(x, 1, z, "139:1")
        else:
            c.set(x, 0, z, "109:2"); c.set(x, 1, z, "44:8")
        c.set(x, -1, z + 1, "3:1")                          # the mound
    # iron fence along the south, with a gate gap
    for x in range(0, 9):
        if x not in (4, 5):
            c.set(x, 0, 14, "101"); c.set(x, 1, 14, "101")
    for x in (0, 3, 6, 8):
        c.set(x, 0, 14, "98:1"); c.set(x, 1, 14, "98:2"); c.set(x, 2, 14, "44:5")
    c.set(3, 2, 14, "44:5")
    # a gnarled dead tree: log trunk, fence-post twigs
    c.box(6, 0, 7, 6, 3, 7, "17:1")
    for x, y, z in ((5, 3, 7), (4, 4, 7), (3, 5, 7), (3, 6, 7), (7, 3, 7), (8, 4, 7), (9, 5, 7), (6, 4, 7), (6, 5, 7),
                    (6, 6, 7), (6, 4, 6), (6, 5, 5), (6, 6, 5), (6, 4, 8), (6, 5, 9), (5, 6, 7), (4, 6, 7),
                    (7, 6, 7), (8, 6, 7), (6, 7, 6), (6, 7, 8), (2, 6, 7), (9, 6, 7)):
        c.set(x, y, z, "191")
    c.set(5, 2, 7, "17:5"); c.set(7, 2, 7, "17:5"); c.set(6, 4, 7, "17:1")
    for x, y, z in ((6, 3, 6), (4, 3, 7), (7, 4, 8)):
        c.set(x, y, z, "30")
    # statue of a weeping figure on a plinth
    c.set(3, 0, 3, "98:3"); c.set(3, 1, 3, "98:0"); c.set(3, 2, 3, "98:3")
    c.set(3, 3, 3, "98:1"); c.set(3, 4, 3, "98:0"); c.set(3, 5, 3, "144:0")
    c.set(2, 4, 3, "44:13"); c.set(4, 4, 3, "44:13"); c.set(2, 5, 3, "109:7") ; c.set(4, 5, 3, "109:6")
    c.set(4, 0, 13, "32"); c.set(1, 0, 3, "32"); c.set(7, 0, 9, "32"); c.set(8, 0, 4, "32")
    c.set(0, 0, 10, "32")


def build():
    c = Chunk("crypt", "The Forgotten Crypt", "grass",
              "A ruined chapel with a collapsed nave opens a stair down to a cobwebbed vault of pillars, "
              "sarcophagi, an iron-bar cell and a lava well.")
    rng = random.Random(7)
    c.raise_(10, 0, 15, 2, 1)
    c.raise_(12, 13, 15, 15, 2)
    vault(c, rng)
    chapel(c, rng)
    graveyard(c, rng)
    # a mossy cobble path in from the south bridge and east portal
    for z in range(9, 16):
        for x in (7, 8, 9):
            if z >= 13 or x == 9:
                c.set(x, -1, z, "48" if (x + z) % 2 else "13")
    c.tree(12, 13, "tiny-spruce-3")
    c.boulder(11, 2, 3, "angular")
    c.cover([(0, 2), (16, 2), (16, 16), (0, 16)], coverage=0.5, fernShare=0.4, flowerShare=0.04,
            deadBushShare=0.15, mushroomShare=0.1)
    return c
