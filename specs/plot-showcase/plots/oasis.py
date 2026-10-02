"""Desert Oasis, as a plot: a clear pool in a hollow ringed with palms and an olive, a ruined sandstone arch on a
raised terrace, a trader's striped tent, a pack camel, a half-buried ribcage, cacti and dead bushes between round
dunes, and a tomb cut open on two faces under the north-west dune."""
import math

from kit import Chunk

POOL_X, POOL_Z, POOL_RX, POOL_RZ = 9.0, 21.0, 5.5, 4.0
HOLLOW = ((8.0, -2), (6.5, -3))            # radius, top course of the hollow's steps
WATER_TOP = -4
POOL_BED = -7
LEAF = "18:7"
SMOOTH, CHISEL, PLAIN = "24:2", "24:1", "24:0"
RED_SMOOTH, RED_CHISEL, RED = "179:2", "179:1", "179:0"
DUNES = ((5, 4, 10.5, 6), (30, 30, 6, 3), (4, 13, 4, 3))            # cx, cz, r, h as handed to c.hill
GRASS_PATCH = (14, 11, 3.5, 1)                                         # soil under the olive
TERRACE = (24, 6, 7.5, 2)                                            # cx, cz, r, h as handed to c.mound
TOMB_X1, TOMB_Z1, TOMB_FLOOR = 9, 8, -8
SHAFT = ((7, 1), (8, 1), (7, 2), (8, 2))
NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def dune_top(x, z):
    top = -1
    for cx, cz, radius, height in DUNES:
        for course in range(1, height + 1):
            ring = radius * (1 - (course - 1) / height * 0.7)
            if ring >= 0.8 and math.hypot(x - cx, z - cz) <= ring:
                top = max(top, course - 1)
    for cx, cz, radius, height in (TERRACE, GRASS_PATCH):
        if math.hypot(x - cx, z - cz) <= radius:
            top = max(top, height - 1)
    return top


def pool_q(x, z):
    return ((x - POOL_X) / POOL_RX) ** 2 + ((z - POOL_Z) / POOL_RZ) ** 2


def in_pool(x, z):
    return pool_q(x, z) <= 1.0


def pool_bed(x, z):
    return POOL_BED + 1 if pool_q(x, z) > 0.7 else POOL_BED


def cut_top(x, z):
    """Top course a lowered cell is cut to: the pool bed or a step of its hollow; None for uncut ground."""
    if in_pool(x, z):
        return pool_bed(x, z)
    dist = math.hypot(x - POOL_X, z - POOL_Z)
    for radius, course_top in HOLLOW:
        if dist <= radius:
            return course_top
    return None


def ground(x, z):
    cut = cut_top(x, z)
    return dune_top(x, z) if cut is None else cut


def base(x, z):
    return ground(x, z) + 1


def put(c, x, z, dy, block):
    c.set(x, base(x, z) + dy, z, block)


def flat(x0, z0, x1, z1, top=-1):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            assert ground(x, z) == top, f"ground at ({x}, {z}) is {ground(x, z)}, not {top}"


def landform(c):
    """Dunes raised, then the pool's hollow cut in non-overlapping runs (overlapping cuts do not stack)."""
    for cx, cz, radius, height in DUNES:
        c.hill(cx, cz, radius, height)
    c.mound(TERRACE[0], TERRACE[1], TERRACE[2], TERRACE[3])
    c.mound(GRASS_PATCH[0], GRASS_PATCH[1], GRASS_PATCH[2], GRASS_PATCH[3], theme="grass")
    for z in range(32):
        start = None
        for x in range(33):
            top = cut_top(x, z) if x < 32 else None
            if start is not None and top != cut_top(start, z):
                c.lower(start, z, x - 1, z, cut_top(start, z) + 1)
                start = None
            if top is not None and start is None:
                start = x


def pool(c):
    for x in range(32):
        for z in range(32):
            if in_pool(x, z):
                bed = pool_bed(x, z)
                c.box(x, bed + 1, z, x, WATER_TOP, z, "9")
                c.set(x, bed, z, "12" if (x + z) % 4 else "82")
    for x, z in ((7, 21), (8, 22), (10, 21), (11, 22)):                  # sunken clay
        if in_pool(x, z):
            c.set(x, pool_bed(x, z), z, "82")


def palm(c, x, z, lean, height):
    """A jungle-log trunk bending toward `lean`, crowned with drooping fronds."""
    lx, lz = lean
    foot = base(x, z)
    for i in range(height):
        tx = x + round(lx * (i / height) ** 2 * 3)
        tz = z + round(lz * (i / height) ** 2 * 3)
        c.set(tx, foot + i, tz, "17:3")
    top = foot + height
    c.set(tx, top, tz, LEAF)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        c.set(tx + dx, top, tz + dz, LEAF)
        if dx == 0 or dz == 0:
            c.set(tx + 2 * dx, top, tz + 2 * dz, LEAF)
            c.set(tx + 3 * dx, top - 1, tz + 3 * dz, LEAF)
            c.set(tx + 3 * dx, top - 2, tz + 3 * dz, LEAF)
        else:
            c.set(tx + 2 * dx, top - 1, tz + 2 * dz, LEAF)


def pillar(c, x, z, height, broken=False):
    b = base(x, z)
    c.set(x, b, z, CHISEL)
    for y in range(1, height):
        c.set(x, b + y, z, RED_SMOOTH if y == 3 else SMOOTH)
    c.set(x, b + height, z, "44:1" if broken else CHISEL)


def ruins(c):
    """On the terrace: an arch of two pillars, one broken, an altar, a fallen column, rubble and a forecourt."""
    flat(19, 3, 29, 9, 1)
    b = 2
    pillar(c, 20, 6, 7)
    pillar(c, 25, 6, 5, broken=True)
    c.set(21, b + 7, 6, "128:5"); c.set(21, b + 6, 6, SMOOTH)            # the arch springing from the tall pillar
    c.set(22, b + 7, 6, "44:9"); c.set(22, b + 6, 6, "128:5")
    c.set(23, b + 6, 6, "44:1"); c.set(23, b + 5, 6, "128:0")
    c.set(24, b + 4, 6, "44:1")
    pillar(c, 28, 10, 3, broken=True)                                    # stumps and a fallen column
    pillar(c, 22, 10, 2, broken=True)
    for x in range(23, 28):
        c.set(x, b, 8, SMOOTH)
    c.set(28, b, 8, "128:0"); c.set(28, b, 7, "128:3")
    for x, z, block in ((19, 4, "44:1"), (27, 4, "44:1"), (23, 4, "128:2"), (28, 5, RED_CHISEL), (21, 5, "44:1"),
                        (26, 10, "128:1"), (19, 8, "44:9"), (29, 8, "44:1"), (27, 11, RED), (23, 11, "44:1")):
        c.set(x, b, z, block)
    c.set(28, b + 1, 5, "44:1")
    for x in range(20, 26):                                              # paved forecourt, sand-drifted
        for z in (7, 8):
            if (x, z) not in c.blocks:
                c.set(x, b - 1, z, SMOOTH if (x + z) % 3 else RED_SMOOTH)
    c.set(22, b - 1, 6, RED_CHISEL); c.set(22, b - 1, 5, SMOOTH); c.set(23, b - 1, 6, SMOOTH)
    c.set(22, b, 4, CHISEL); c.set(22, b + 1, 4, "85"); c.set(22, b + 2, 4, "89")      # altar and brazier


def tent(c):
    x0, x1, z0, z1 = 20, 26, 15, 19
    flat(x0 - 1, z0 - 1, x1 + 2, z1 + 2)
    for x in range(x0, x1 + 1):
        stripe = "35:14" if (x - x0) % 2 == 0 else "35:0"
        for z in range(z0, z1 + 1):
            c.set(x, 3, z, stripe)
        c.set(x, 2, z1 + 1, stripe)                                      # front awning
        for y in (0, 1, 2):
            c.set(x, y, z0, "35:4" if y < 2 else stripe)                 # back wall
    for z in range(z0, z1 + 1):
        for y in (0, 1, 2):
            c.set(x1, y, z, "35:4")                                      # east wall
    for x, z in ((x0, z1), (x1, z1), (x0, z0 + 1), (x0 + 3, z1)):
        c.box(x, 0, z, x, 2, z, "85")
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            c.set(x, 0, z, "171:14" if (x + z) % 2 else "171:1")
    c.set(x0 + 1, 0, z0 + 1, "54:3"); c.set(x0 + 2, 0, z0 + 1, "54:3"); c.set(x0 + 3, 0, z0 + 1, "118:3")
    c.set(x1 - 1, 0, z0 + 1, "17:0"); c.set(x1 - 1, 1, z0 + 1, "17:0"); c.set(x1 - 1, 0, z0 + 2, "17:0")
    c.set(x1 - 1, 0, z0 + 3, "17:0")
    c.set(x0 + 1, 0, z1 - 1, "126:8"); c.set(x0 + 2, 0, z1 - 1, "126:8"); c.set(x0 + 3, 0, z1 - 1, "126:8")
    c.set(x0 + 1, 1, z1 - 1, "140"); c.set(x0 + 3, 1, z1 - 1, "140")
    c.set(x0 + 5, 0, z1 - 1, "145:0")
    c.set(x0 + 3, 2, z0 + 1, "89"); c.set(x0 + 3, 2, z0 + 2, "85") if False else None
    for dz in (1, 2):                                                    # sacks and crates beside the tent
        c.set(x1 + 1, 0, z0 + dz, "35:12")
    c.set(x1 + 1, 1, z0 + 1, "35:12"); c.set(x1 + 2, 0, z0 + 1, "170:0")


def camel(c):
    """A pack camel in coarse dirt: fence legs, a long body with a saddled hump, a lean neck and a head."""
    x, z = 21, 24
    flat(x - 4, z - 1, x + 5, z + 1)
    for dx, dz in ((0, 0), (0, 1), (4, 0), (4, 1)):
        c.box(x + dx, 0, z + dz, x + dx, 2, z + dz, "85")
    for dx in range(0, 5):
        for dz in (0, 1):
            c.set(x + dx, 3, z + dz, "3:1")
    for dx in (1, 2, 3):
        for dz in (0, 1):
            c.set(x + dx, 4, z + dz, "3:1")
    for dz in (0, 1):
        c.set(x + 1, 5, z + dz, "171:14"); c.set(x + 2, 5, z + dz, "171:0"); c.set(x + 3, 5, z + dz, "171:14")
    for dx, dy in ((-1, 4), (-1, 5), (-2, 5), (-2, 6), (-3, 6), (-3, 7)):
        c.set(x + dx, dy, z, "3:1")
    c.set(x + 5, 3, z + 1, "85"); c.set(x + 5, 2, z + 1, "85")           # tail


def bones(c):
    """A half-buried ribcage with a skull."""
    x0, z0 = 1, 30
    flat(x0 - 1, z0 - 1, x0 + 7, z0 + 1)
    for i in range(6):
        c.set(x0 + i, 0, z0, "44:7")
    c.set(x0 + 6, 0, z0, "144:1")
    for i in (1, 3, 4):
        for dz in (-1, 1):
            c.set(x0 + i, 0, z0 + dz, "44:7"); c.set(x0 + i, 1, z0 + dz, "44:7")


def tomb(c):
    """A void under the north-west dune, open on its west and north faces, reached by a ladder shaft."""
    f = TOMB_FLOOR
    c.lower(0, 0, TOMB_X1, TOMB_Z1, f)
    for z in range(TOMB_Z1 + 1):                                         # the dune's own surface roofs the void
        start = None
        for x in range(TOMB_X1 + 2):
            here = x <= TOMB_X1 and (x, z) not in SHAFT
            top = dune_top(x, z) + 1 if here else None
            if start is not None and top != dune_top(start, z) + 1:
                c.roof(start, z, x - 1, z, -2, dune_top(start, z) + 1)
                start = None
            if here and start is None:
                start = x
    for x in range(0, TOMB_X1 + 1):
        for z in range(0, TOMB_Z1 + 1):
            c.set(x, f - 1, z, SMOOTH)
    for z in range(0, TOMB_Z1 + 1):                                      # carved east wall
        for y in range(f, -2):
            c.set(TOMB_X1, y, z, RED_CHISEL if y == f + 2 else CHISEL if y == f + 3 else SMOOTH)
    for y in range(f, 5):
        c.set(8, y, 1, "65:4") if y <= dune_top(9, 1) else None          # ladder up the shaft
    for x, z in ((4, 0), (0, 8), (4, 8), (8, 8), (0, 0)):               # supporting columns
        c.box(x, f, z, x, -3, z, SMOOTH)
        c.set(x, f, z, CHISEL); c.set(x, -3, z, CHISEL)
    c.box(2, f, 4, 4, f, 5, CHISEL)                                      # sarcophagus with a slab lid
    c.box(2, f + 1, 4, 4, f + 1, 5, "44:1")
    c.set(3, f + 2, 4, "144:1")
    for x, z in ((0, 6), (0, 7), (1, 7)):                                # treasure
        c.set(x, f, z, "41")
    c.set(0, f + 1, 6, "41")
    c.set(7, f, 7, "54:2"); c.set(7, f, 6, "54:2"); c.set(6, f, 7, "41"); c.set(8, f, 5, "41")
    c.set(6, f, 3, "144:1"); c.set(3, f, 1, "144:1"); c.set(2, f, 2, "155:2") if False else None
    for x, z in ((1, 2), (6, 6), (7, 4), (1, 4)):                        # torches on stubs
        c.set(x, f, z, SMOOTH); c.set(x, f + 1, z, "50:5")
    for x, y, z in ((1, -3, 1), (0, -3, 4), (6, -3, 7), (8, -3, 4), (3, f + 2, 0), (5, -3, 3)):
        c.set(x, y, z, "30")
    c.set(7, f - 1, 3, "46"); c.set(7, f, 3, "70")                       # plate over buried TNT near the ladder


def plants(c):
    """Cacti, dead bushes and sugar cane on the open sand."""
    spots = ((15, 3, 3), (30, 13, 2), (2, 22, 2), (27, 16, 3), (8, 12, 1), (13, 1, 2), (1, 30, 1), (30, 21, 1),
             (13, 15, 1), (14, 29, 2))
    for x, z, height in spots:
        if (x, base(x, z), z) not in c.blocks and not in_pool(x, z) and cut_top(x, z) is None:
            for dy in range(height):
                put(c, x, z, dy, "81")
    for x, z in ((12, 14), (18, 12), (2, 18), (24, 22), (28, 13), (7, 30), (17, 7), (30, 24), (6, 11), (16, 22)):
        if (x, base(x, z), z) not in c.blocks and not in_pool(x, z) and cut_top(x, z) is None:
            put(c, x, z, 0, "32")
    for x in range(32):
        for z in range(32):
            near = any(in_pool(x + dx, z + dz) for dx, dz in NEIGHBOURS)
            if near and not in_pool(x, z) and (x * 3 + z) % 4 == 0 and (x, base(x, z), z) not in c.blocks:
                for dy in range(2 + (x % 2)):
                    put(c, x, z, dy, "83")


def build():
    c = Chunk("oasis", "Desert Oasis", "sand",
              "A clear pool in a hollow ringed with palms, a ruined sandstone arch on a terrace, a trader's tent, "
              "a camel and a buried tomb among round dunes.", size=32)
    landform(c)
    pool(c)
    tomb(c)
    ruins(c)
    tent(c)
    camel(c)
    bones(c)
    plants(c)
    palm(c, 4, 19, (2, 0), 8)
    palm(c, 14, 25, (-1, -1), 7)
    c.tree(14, 11, "olive-6")
    c.cover([(0, 0), (32, 0), (32, 32), (0, 32)], coverage=0.25, deadBushShare=0.5, cactusShare=0.35,
            tallShare=0.0, flowerShare=0.0, fernShare=0.0)
    return c
