"""Wizard's Tower: a round stone tower with a stepped purple roof, a balcony and flag, windows onto a study, an
alchemy loft and an observatory, a herb garden, a pond and crystals at its foot, and a mushroom cellar cut away
under the garden."""
import math
import random

from kit import Chunk

CX, CZ = 9, 5          # tower centre
FLOOR_Y = (5, 11, 17)  # plank floors above the ground floor
TOP = 22               # last wall course


def wall_cells(radius=3.2, ring=1.0):
    """Cells of the tower's wall ring and its interior, as (dx, dz) offsets."""
    wall, inner = [], []
    for dx in range(-5, 6):
        for dz in range(-5, 6):
            dist = math.hypot(dx, dz)
            if dist <= radius + 0.3:
                (wall if dist > radius - ring + 0.3 else inner).append((dx, dz))
    return wall, inner


def tower(c, rng):
    wall, inner = wall_cells()
    wall_set = set(wall)
    # foundation ring and steps
    for dx in range(-6, 7):
        for dz in range(-6, 7):
            dist = math.hypot(dx, dz)
            if 3.4 < dist <= 4.3:
                c.set(CX + dx, -1, CZ + dz, "98:2" if rng.random() < .5 else "48")
    for y in range(0, TOP + 1):
        for dx, dz in wall:
            roll = rng.random()
            low = y < 5
            block = "98:1" if roll < (.4 if low else .15) else "98:2" if roll < .25 + (.1 if low else 0) else "98:0"
            if y in (5, 11, 17, 22):
                block = "98:3"
            c.set(CX + dx, y, CZ + dz, block)
    # ground floor flags, plank floors with a ladder hole
    for dx, dz in inner:
        c.set(CX + dx, -1, CZ + dz, "98:0" if (dx + dz) % 2 else "98:2")
        for floor in FLOOR_Y:
            c.set(CX + dx, floor, CZ + dz, "5:5" if (dx + dz) % 2 == 0 else "5:1")
    for y in range(0, 23):
        c.set(CX - 2, y, CZ - 1, "65:5")
    for floor in FLOOR_Y:
        c.set(CX - 2, floor, CZ - 1, "65:5")
    # door south with a stone surround and steps
    for y in (0, 1):
        c.set(CX, y, CZ + 3, "64:3" if y == 0 else "64:11")
    c.set(CX - 1, 0, CZ + 3, "98:3"); c.set(CX + 1, 0, CZ + 3, "98:3")
    c.set(CX, 2, CZ + 3, "98:3"); c.set(CX - 1, 1, CZ + 3, "109:7"); c.set(CX + 1, 1, CZ + 3, "109:6")
    c.set(CX, 0, CZ + 4, "109:3"); c.set(CX - 1, 0, CZ + 4, "44:5"); c.set(CX + 1, 0, CZ + 4, "44:5")
    # windows, two wide east, west and north, one wide south; the south of the balcony level is the door
    for base in (1, 7, 13, 19):
        for dx, dz, spans in ((3, 0, (0, 1)), (-3, 0, (0, 1)), (0, -3, (0, 1)), (0, 3, (0,))):
            if (dx, dz) == (0, 3) and base in (1, 13):
                continue
            pane = "160:10" if base in (7, 19) else "102"
            for span in spans:
                sx, sz = (0, span) if dx else (span, 0)
                for y in (base, base + 1):
                    c.set(CX + dx + sx, y, CZ + dz + sz, pane)
                c.set(CX + dx + sx, base - 1, CZ + dz + sz, "44:5") if base > 1 else None
                c.set(CX + dx + sx, base + 2, CZ + dz + sz, "98:3")
    # balcony on the south side at floor 11
    for dx in range(-5, 6):
        for dz in range(0, 6):
            dist = math.hypot(dx, dz - 0)
            if 3.2 < dist <= 4.9 and dz >= 1:
                c.set(CX + dx, 10, CZ + dz, "98:3" if dist > 4.4 else "98:2")
                c.set(CX + dx, 11, CZ + dz, "44:13" if dist <= 4.4 else "44:5")
                if dist > 4.3 and dz >= 1:
                    c.set(CX + dx, 12, CZ + dz, "85")
    for y in (12, 13):
        c.set(CX, y, CZ + 3, None)
        c.set(CX - 1, y, CZ + 3, "160:10"); c.set(CX + 1, y, CZ + 3, "160:10")
    c.set(CX, 11, CZ + 3, "5:1")
    # banner pole with a purple pennant, off the balcony rail
    for y in range(12, 19):
        c.set(CX + 4, y, CZ + 2, "85")
    for dx in range(1, 4):
        for y in (16, 17, 18):
            if dx < 3 or y == 17:
                c.set(CX + 4 + dx, y, CZ + 2, "35:10" if y != 17 else "35:4")
    # corner buttresses
    for sx, sz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        bx, bz = CX + 4 * sx, CZ + 3 * sz if abs(sz) else CZ
        bx, bz = CX + 3 * sx, CZ + 3 * sz
        for y in range(0, 9):
            c.set(bx, y, bz, "98:1" if y % 3 == 0 and rng.random() < .5 else "98:0")
        c.set(bx, 9, bz, "109:%d" % (2 if sz < 0 else 3))
        for y in range(0, 4):
            c.set(bx + sx, y, bz, "98:0") if y < 2 else None
        c.set(bx + sx, 2, bz, "109:%d" % (0 if sx > 0 else 1))
    # roof: stepped cone, purple clay with blue bands, a glowing tip
    radii = [4.6, 3.9, 3.4, 2.9, 2.5, 2.1, 1.7, 1.3, 0.9]
    for index, radius in enumerate(radii):
        y = TOP + 1 + index
        block = "35:10" if index % 3 != 1 else "35:11"
        c.disc(CX, CZ, radius, y, block, ring=1.1 if index < len(radii) - 1 else None)
    c.set(CX, TOP + len(radii), CZ, "89")
    # inside the tower
    inside(c, rng)


def ring_cells(inner, low, high):
    return [(dx, dz) for dx, dz in inner if low <= math.hypot(dx, dz) <= high]


def inside(c, rng):
    _, inner = wall_cells()
    # level 0: study — enchanting table and a ring of shelves
    c.set(CX, 0, CZ, "116")
    for dx, dz in ((-1, -2), (2, -1), (-1, 2), (1, 2)):
        c.set(CX + dx, 0, CZ + dz, "47"); c.set(CX + dx, 1, CZ + dz, "47")
    c.set(CX + 1, 0, CZ - 1, "47")
    c.set(CX, 4, CZ + 1, "89")
    # level 1: alchemy
    f = FLOOR_Y[0] + 1
    c.set(CX, f, CZ, "117"); c.set(CX - 1, f, CZ, "118:3"); c.set(CX + 1, f, CZ, "58")
    for dx, dz in ((2, -1), (1, 2), (-1, 2), (-1, -2)):
        c.set(CX + dx, f, CZ + dz, "47"); c.set(CX + dx, f + 1, CZ + dz, "47")
    c.set(CX + 1, f, CZ + 1, "140"); c.set(CX - 1, f, CZ + 1, "54:2")
    c.set(CX + 1, FLOOR_Y[1] - 1, CZ + 1, "89")
    # level 2: bedroom desk
    f = FLOOR_Y[1] + 1
    c.set(CX, f, CZ + 1, "26:3"); c.set(CX + 1, f, CZ + 1, "26:11")
    c.set(CX + 1, f, CZ - 1, "145:0"); c.set(CX - 1, f, CZ + 1, "47"); c.set(CX - 1, f + 1, CZ + 1, "47")
    c.set(CX + 2, f, CZ - 1, "47"); c.set(CX + 2, f + 1, CZ - 1, "47")
    c.set(CX, FLOOR_Y[2] - 1, CZ, "89")
    # level 3: observatory
    f = FLOOR_Y[2] + 1
    c.set(CX, f, CZ, "58")
    c.set(CX, f + 1, CZ, "140"); c.set(CX - 1, f, CZ, "47"); c.set(CX + 1, f, CZ, "47")


def vines(c, rng):
    """Vines on the tower's outer face, where a wall block stands behind the cell."""
    wall, _ = wall_cells()
    for y in range(1, 20):
        for dx, dz in wall:
            for sx, sz, bit in ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1)):
                x, z = CX + dx + sx, CZ + dz + sz
                if (x, y, z) in c.blocks or (dx + sx, dz + sz) in set(wall):
                    continue
                if abs(sx * dx + sz * dz) < 2:
                    continue
                if y < 11 and rng.random() < .13 or y >= 11 and rng.random() < .04:
                    c.set(x, y, z, f"106:{bit}")


def cellar(c, rng):
    """A mushroom cellar under the garden: the cut face shows shelves, a still, glowing mushrooms and roots."""
    c.lower(0, 6, 7, 13, -6)
    c.roof(0, 6, 7, 11, -2, 0)
    c.roof(0, 12, 2, 13, -2, 0)
    c.roof(5, 12, 7, 13, -2, 0)
    # floor of podzol and mycelium
    for x in range(0, 8):
        for z in range(6, 14):
            c.set(x, -7, z, "110" if rng.random() < .4 else "3:2")
    # lining of dark oak frames on the cut face and the back
    for z in (6, 13):
        for y in range(-6, -2):
            c.set(0, y, z, "17:1")
    for z in range(6, 14):
        c.set(0, -3, z, "17:9")
    for x in range(0, 8):
        c.set(x, -3, 7, "17:5") if x in (0, 7) else None
    # shelves and the still against the back wall (z 6)
    for x in range(1, 7):
        for y in (-6, -5):
            c.set(x, y, 7, "47") if x not in (3, 4) else None
    c.set(3, -6, 7, "118:3"); c.set(4, -6, 7, "117"); c.set(3, -5, 7, "140"); c.set(4, -5, 7, "58")
    for x in (1, 2, 5, 6):
        c.set(x, -4, 7, "47")
    c.set(1, -6, 8, "54:3"); c.set(6, -6, 8, "145:0"); c.set(1, -5, 8, "144:1")
    # mushroom trees
    for x, z, height in ((2, 11, 2), (5, 11, 1), (6, 12, 2)):
        for y in range(-6, -6 + height):
            c.set(x, y, z, "99:10")
        top = -6 + height
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                c.set(x + dx, top, z + dz, "100:14" if (x, z) != (5, 11) else "99:14")
        c.set(x, top + 1, z, "100:14" if (x, z) != (5, 11) else "99:14")
    # glowing crystals and roots
    for x, z in ((0, 12), (7, 8)):
        c.set(x, -6, z, "169"); c.set(x, -5, z, "95:3")
    c.set(7, -6, 12, "169"); c.set(7, -5, 12, "95:11"); c.set(6, -6, 13, "95:3")
    for x, z in ((1, 12), (4, 13), (3, 10), (6, 11), (2, 8), (5, 7)):
        c.set(x, -3, z, "17:12")
        for y in range(-4, -4 - rng.randint(0, 2), -1):
            c.set(x, y, z, "106:0")
    c.set(7, -3, 6, "30"); c.set(0, -3, 6, "30"); c.set(0, -3, 13, "30"); c.set(7, -3, 13, "30")
    # a small pool
    c.set(1, -7, 11, "9"); c.set(2, -7, 12, "9"); c.set(1, -7, 12, "9"); c.set(2, -7, 13, "9")
    # skulls, ore in the cut below
    c.set(5, -6, 13, "144:1"); c.set(6, -6, 11, "39")
    c.set(0, -10, 10, "56"); c.set(0, -11, 9, "21")
    # hatch down with a ladder, ringed by a low wall
    for y in range(-6, 0):
        c.set(3, y, 13, "65:2")
    for x, z in ((2, 12), (2, 13), (5, 12), (5, 13), (3, 11), (4, 11)):
        c.set(x, 0, z, "139:1")
    c.set(2, 1, 12, "50:5"); c.set(5, 1, 12, "50:5")


def garden(c, rng):
    # a path from the south bridge to the door
    for z in range(9, 16):
        for x in (8, 9):
            c.set(x, -1, z, "13" if (x + z) % 3 else "98:2") if x == 8 or z > 8 else None
        c.set(10, -1, z, "48") if z % 2 else None
    # herb beds west of the path above the cellar
    for x0, z0 in ((1, 9), (5, 9)):
        for x in range(x0, x0 + 3):
            for z in range(z0, z0 + 2):
                c.set(x, -1, z, "3:2" if rng.random() < .5 else "3:0")
                c.set(x, 0, z, rng.choice(("37", "38:1", "38:3", "38:7", "38:2", "39", "40", "38:0", "38:4")))
    # bed borders
    for x0, z0, x1, z1 in ((1, 9, 3, 10), (5, 9, 7, 10)):
        for x in range(x0 - 1, x1 + 2):
            for z in (z0 - 1, z1 + 1):
                c.set(x, 0, z, "126:9") if (x, z) not in {(3, 11), (4, 11)} else None
    # east herb beds and a stone bench
    for x in range(11, 15):
        for z in (9, 10):
            c.set(x, -1, z, "3:2")
            c.set(x, 0, z, rng.choice(("38:5", "37", "38:2", "39", "38:8", "40", "38:6")))
    c.set(10, 0, 9, "126:9"); c.set(10, 0, 10, "126:9")
    for x in range(11, 15):
        c.set(x, 0, 11, "126:9") if x != 11 else None
    # pond
    c.lower(10, 12, 13, 14, -2)
    for x in range(10, 14):
        for z in range(12, 15):
            for y in (-2, -1):
                c.set(x, y, z, "9")
    for x, z in ((10, 13), (12, 12), (13, 14)):
        c.set(x, 0, z, "111")
    for x, z in ((9, 13), (9, 12), (14, 13), (14, 14)):
        c.set(x, 0, z, "83")
        c.set(x, 1, z, "83") if (x + z) % 2 else None
    # crystal clusters
    cluster(c, 14, 4, 4)
    cluster(c, 2, 5, 3)
    # signpost and a lantern post
    c.set(7, 0, 14, "85"); c.set(7, 1, 14, "85"); c.set(7, 2, 14, "89")
    c.set(10, 0, 15, "85"); c.set(10, 1, 15, "85")


def cluster(c, x, z, height):
    """A crystal cluster: sea-lantern spires with glass tips, one tall."""
    for y in range(0, height):
        c.set(x, y, z, "169")
    c.set(x, height, z, "95:3"); c.set(x, height + 1, z, "95:11")
    for dx, dz, spire in ((1, 0, 2), (-1, 0, 1), (0, 1, 2), (0, -1, 1), (1, 1, 0)):
        for y in range(0, spire):
            c.set(x + dx, y, z + dz, "169")
        c.set(x + dx, spire, z + dz, "95:3" if spire else "168:1")
    c.set(x - 1, 0, z + 1, "168:2")


def build():
    c = Chunk("wizard-tower", "Wizard's Tower", "forest",
              "A round stone tower under a stepped purple roof, windows onto a study and an alchemy loft, a herb "
              "garden, a pond, crystals and a mushroom cellar cut away below.")
    rng = random.Random(23)
    tower(c, rng)
    vines(c, rng)
    cellar(c, rng)
    garden(c, rng)
    c.tree(3, 4, "birch-9")
    c.cover([(0, 0), (16, 0), (16, 16), (0, 16)], coverage=0.55, fernShare=0.3, flowerShare=0.12,
            tallShare=0.2, mushroomShare=0.08)
    return c
