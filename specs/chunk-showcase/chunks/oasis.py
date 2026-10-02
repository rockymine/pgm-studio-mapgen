"""Desert Oasis: a clear pool with palms, a ruined sandstone arch and pillars, a trader's striped tent, a camel,
cacti and bones, and a buried tomb cut open on two faces under the north-west dune."""
from kit import Chunk

POOL_X, POOL_Z, POOL_RX, POOL_RZ = 5.5, 10.5, 3.9, 2.9
BED = -4                       # top course of the pool bed
LEAF = "18:7"                  # jungle leaves, permanent
SMOOTH, CHISEL, PLAIN = "24:2", "24:1", "24:0"
RED_SMOOTH, RED_CHISEL, RED = "179:2", "179:1", "179:0"


def in_pool(x, z):
    return ((x - POOL_X) / POOL_RX) ** 2 + ((z - POOL_Z) / POOL_RZ) ** 2 <= 1.0


def pool(c):
    for z in range(16):
        xs = [x for x in range(16) if in_pool(x, z)]
        if xs:
            c.lower(min(xs), z, max(xs), z, BED + 1)
    for x in range(16):
        for z in range(16):
            if in_pool(x, z):
                c.box(x, BED + 1, z, x, -1, z, "9")
                c.set(x, BED, z, "12" if (x + z) % 4 else "82")
    for x, z in ((4, 10), (5, 11), (6, 10), (7, 11)):                    # sunken clay and a lost jar
        c.set(x, BED, z, "82")
    c.set(6, BED + 1, 10, "140") if False else None


def palm(c, x, z, lean, height):
    """A jungle-log trunk bending toward `lean`, crowned with drooping fronds."""
    lx, lz = lean
    for i in range(height):
        tx = x + round(lx * (i / height) ** 2 * 3)
        tz = z + round(lz * (i / height) ** 2 * 3)
        c.set(tx, i, tz, "17:3")
    c.set(tx, height, tz, LEAF)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        straight = dx == 0 or dz == 0
        c.set(tx + dx, height, tz + dz, LEAF)
        if straight:
            c.set(tx + 2 * dx, height, tz + 2 * dz, LEAF)
            c.set(tx + 3 * dx, height - 1, tz + 3 * dz, LEAF)
            c.set(tx + 3 * dx, height - 2, tz + 3 * dz, LEAF)
        else:
            c.set(tx + 2 * dx, height - 1, tz + 2 * dz, LEAF)


def pillar(c, x, z, height, broken=False):
    c.set(x, 0, z, CHISEL)
    for y in range(1, height):
        c.set(x, y, z, RED_SMOOTH if y == 2 else SMOOTH)
    if broken:
        c.set(x, height, z, "44:1")
    else:
        c.set(x, height, z, CHISEL)
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.set(x + dx, height, z + dz, "128:" + str({(1, 0): 0, (-1, 0): 1, (0, 1): 2, (0, -1): 3}[(dx, dz)] + 4)) \
                if False else None


def ruins(c):
    # arch at z=3: left half complete, right half broken off
    pillar(c, 8, 3, 6)
    pillar(c, 12, 3, 4, broken=True)
    c.set(8, 6, 3, CHISEL)
    c.set(9, 6, 3, "128:5"); c.set(9, 5, 3, SMOOTH)
    c.set(10, 6, 3, "44:9"); c.set(10, 5, 3, "128:5") if False else None
    c.set(11, 4, 3, "128:4") if False else None
    c.set(11, 4, 3, "44:1"); c.set(11, 3, 3, "128:0")
    c.set(10, 6, 3, "44:9")
    c.set(9, 4, 3, None)
    # a second pillar stump and a fallen column
    pillar(c, 14, 6, 3, broken=True)
    pillar(c, 11, 6, 2, broken=True)
    for x in range(9, 13):
        c.set(x, 0, 5, "24:2" if False else "17:4" if False else SMOOTH)
    c.set(9, 0, 5, "24:2"); c.set(10, 0, 5, "24:2"); c.set(11, 0, 5, "24:2"); c.set(12, 0, 5, "24:2")
    c.set(13, 0, 5, "128:0"); c.set(13, 0, 4, "128:3")
    # rubble: cracked sandstone, slabs, red blocks, scattered
    for x, z, block in ((7, 1, "44:1"), (13, 1, "44:1"), (10, 1, "128:2"), (14, 2, RED_CHISEL), (9, 2, "44:1"),
                        (12, 6, "128:1"), (7, 4, "44:9"), (15, 4, "44:1"), (13, 7, RED), (10, 7, "44:1")):
        c.set(x, 0, z, block)
    c.set(14, 1, 2, "44:1")
    # a paved forecourt of smooth sandstone with sand drifted over it
    for x in range(8, 13):
        for z in (4,):
            c.set(x, -1, z, SMOOTH if (x + z) % 3 else RED_SMOOTH)
    c.set(10, -1, 3, RED_CHISEL); c.set(10, -1, 2, SMOOTH)
    # an altar under the arch with a lit brazier
    c.set(10, 0, 2, CHISEL); c.set(10, 1, 2, "85"); c.set(10, 2, 2, "89")


def tent(c):
    x0, x1, z0, z1 = 10, 14, 8, 11
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.set(x, 3, z, "35:14" if (x - x0) % 2 == 0 else "35:0")
        c.set(x, 2, z1 + 1, "35:14" if (x - x0) % 2 == 0 else "35:0")  # front awning
        for y in (0, 1, 2):
            c.set(x, y, z0, "35:4" if y < 2 else "35:14" if x % 2 == 0 else "35:0")        # back wall
    for z in range(z0, z1 + 1):
        for y in (0, 1, 2):
            c.set(x1, y, z, "35:4")                                      # east wall
    for x, z in ((x0, z0 + 1), (x0, z1), (x1 - 4 + 4 - 4 + 0, z1)):
        pass
    for x, z in ((x0, z1), (x1, z1), (x0, z0 + 1), (x0 + 2, z1), (x0 + 4, z1)):
        c.box(x, 0, z, x, 2, z, "85") if (x, z) != (x1, z1) or True else None
    c.box(x1, 0, z1, x1, 2, z1, "85")
    for x in range(x0, x1 + 1):                                          # carpets
        for z in range(z0 + 1, z1 + 1):
            c.set(x, -1, z, "172") if False else None
            if (x, z) not in ((x1, z1),):
                pass
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            c.set(x, 0, z, "171:14" if (x + z) % 2 else "171:1")
    # stock: chests, cauldron, a stack of barrels, pots on a slab shelf, an anvil
    c.set(x0 + 1, 0, z0 + 1, "54:3"); c.set(x0 + 2, 0, z0 + 1, "54:3"); c.set(x0 + 3, 0, z0 + 1, "118:3")
    c.set(x0 + 1, 1, z0 + 1, "17:0") if False else None
    c.set(x1 - 1, 0, z0 + 2, "17:0"); c.set(x1 - 1, 1, z0 + 2, "17:0"); c.set(x1 - 1, 0, z0 + 3, "17:0")
    c.set(x0 + 1, 0, z1 - 1, "126:8"); c.set(x0 + 2, 0, z1 - 1, "126:8")
    c.set(x0 + 1, 1, z1 - 1, "140"); c.set(x0 + 2, 1, z1 - 1, "140")
    c.set(x0 + 3, 0, z1 - 1, "145:0")
    c.set(x0 + 2, 1, z0 + 1, "140") if False else None
    c.set(x0 + 2, 2, z0 + 2, "85"); c.set(x0 + 2, 2, z0 + 3, "89") if False else None
    c.set(x0 + 2, 2, z0 + 1, "89")                                       # lamp hung at the back
    c.set(x0 - 1, 0, z1 + 1, "172") if False else None
    # sign in front
    c.set(x0 - 1, 0, z1, "85"); c.set(x0 - 1, 1, z1, "68:5") if False else None
    c.set(x0 + 1, 1, z1 + 1, "68:3") if False else None
    c.set(x0, 1, z1, "68:3") if False else None
    # sacks (brown wool) and crates (hay) beside the tent
    c.set(x1 + 1, 0, z0 + 1, "35:12"); c.set(x1 + 1, 0, z0 + 2, "35:12"); c.set(x1 + 1, 1, z0 + 1, "35:12")
    c.set(9, 0, 9, "170:0") if False else None


def camel(c):
    """A pack camel in coarse dirt: fence legs, a long body with a saddled hump, a lean neck and a head."""
    x, z = 8, 14
    for dx, dz in ((0, 0), (0, 1), (3, 0), (3, 1)):
        c.box(x + dx, 0, z + dz, x + dx, 1, z + dz, "85")
    for dx in range(0, 4):
        for dz in (0, 1):
            c.set(x + dx, 2, z + dz, "3:1")
    for dx in (1, 2):
        for dz in (0, 1):
            c.set(x + dx, 3, z + dz, "3:1")
    c.set(x + 1, 4, z, "171:14"); c.set(x + 1, 4, z + 1, "171:14")      # saddle blanket on the hump
    c.set(x + 2, 4, z, "171:0"); c.set(x + 2, 4, z + 1, "171:0")
    c.set(x - 1, 3, z, "3:1"); c.set(x - 1, 4, z, "3:1"); c.set(x - 2, 4, z, "3:1"); c.set(x - 2, 5, z, "3:1")
    c.set(x - 3, 5, z, "3:1"); c.set(x - 3, 6, z, "172") if False else None
    c.set(x - 2, 6, z, "44:3") if False else None
    c.set(x + 4, 2, z, "35:12") if False else None
    c.set(x + 4, 2, z + 1, "85"); c.set(x + 4, 1, z + 1, "85")           # tail
    c.set(x - 3, 4, z, "44:11") if False else None


def bones(c):
    """A half-buried ribcage with a skull."""
    x0, z0 = 2, 14
    for i in range(5):
        c.set(x0 + i, 0, z0, "155:3" if False else "44:7")
    c.set(x0 + 5, 0, z0, "144:1")
    for i in (1, 3):
        c.set(x0 + i, 0, z0 - 1, "156:3") if False else None
        c.set(x0 + i, 1, z0 - 1, "44:7"); c.set(x0 + i, 0, z0 - 1, "44:7")
        c.set(x0 + i, 1, z0 + 1, "44:7"); c.set(x0 + i, 0, z0 + 1, "44:7")
    c.set(x0 - 1, 0, z0, "155:2") if False else None


def tomb(c):
    """A void under the north-west dune, open on its west and north faces, reached by a ladder shaft."""
    f = -7                                                               # lowest air course of the chamber
    c.lower(0, 0, 6, 5, f)
    for x0, z0, x1, z1 in ((0, 0, 6, 0), (0, 3, 6, 5), (0, 1, 3, 2), (6, 1, 6, 2)):
        c.roof(x0, z0, x1, z1, -2, 0)
    c.box(0, f - 1, 0, 6, f - 1, 5, SMOOTH)
    for y in range(f, -2):
        c.set(6, y, 1, SMOOTH)
        c.set(5, y, 1, "65:4")                                           # ladder up the shaft
    for z in range(2, 6):                                                # carved east wall
        for y in range(f, -2):
            c.set(6, y, z, RED_CHISEL if y == f + 2 else CHISEL if y == f + 3 else SMOOTH)
    for x, z in ((3, 5), (0, 5), (3, 0)):                                # supporting columns
        c.box(x, f, z, x, -3, z, SMOOTH)
        c.set(x, f, z, CHISEL); c.set(x, -3, z, CHISEL)
    # sarcophagus with a slab lid
    c.box(1, f, 3, 2, f, 4, CHISEL)
    c.box(1, f + 1, 3, 2, f + 1, 4, "44:1")
    c.set(1, f + 2, 3, "144:1") if False else None
    # treasure
    c.set(0, f, 4, "41"); c.set(0, f, 3, "41"); c.set(0, f + 1, 4, "41")
    c.set(5, f, 5, "54:2"); c.set(5, f, 4, "54:2"); c.set(4, f, 5, "41")
    # bones and torches
    c.set(4, f, 3, "144:1"); c.set(2, f, 1, "144:1"); c.set(1, f, 2, "155:2")
    for x, z in ((1, 1), (4, 4), (5, 3)):
        c.set(x, f, z, SMOOTH); c.set(x, f + 1, z, "50:5")
    for x, y, z in ((1, -3, 1), (0, -3, 3), (4, -3, 5), (5, -3, 3), (2, f + 2, 0)):
        c.set(x, y, z, "30")
    # a plate over buried TNT at the foot of the ladder
    c.set(4, f - 1, 2, "46"); c.set(4, f, 2, "70")
    c.set(1, f, 0, "118:0") if False else None


def plants(c):
    """Cacti, dead bushes and sugar cane on the open sand."""
    for x, z, height in ((14, 4, 3), (15, 11, 2), (1, 12, 2), (13, 13, 3), (5, 6, 1), (12, 0, 2), (0, 15, 1),
                         (15, 7, 1), (7, 6, 1), (11, 15, 2)):
        if (x, 0, z) not in c.blocks and not in_pool(x, z):
            for dy in range(height):
                c.set(x, dy, z, "81")
    for x, z in ((6, 7), (10, 6), (1, 10), (12, 14), (14, 9), (4, 15), (9, 5), (15, 13), (3, 6), (11, 0)):
        if (x, 0, z) not in c.blocks and not in_pool(x, z):
            c.set(x, 0, z, "32")
    for x in range(16):
        for z in range(16):
            near = any(in_pool(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if near and not in_pool(x, z) and (x * 3 + z) % 5 == 0 and (x, 0, z) not in c.blocks:
                for dy in range(2 + (x % 2)):
                    c.set(x, dy, z, "83")


def build():
    c = Chunk("oasis", "Desert Oasis", "sand",
              "A clear pool ringed with palms, a ruined sandstone arch, a trader's striped tent, a camel and a buried tomb.")
    # low drifts heaped against the edges
    for cx, cz in ((1, 8), (14, 14), (14, 1)):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if 0 <= cx + dx <= 15 and 0 <= cz + dz <= 15:
                    c.set(cx + dx, 0, cz + dz, "12" if abs(dx) + abs(dz) < 2 else "44:1")
        c.set(cx, 1, cz, "44:1")
    for x in (4, 5):
        for z in (1, 2):
            c.set(x, -1, z, "96:8")
    pool(c)
    tomb(c)
    ruins(c)
    tent(c)
    camel(c)
    bones(c)
    plants(c)
    palm(c, 2, 8, (2, 0), 6)
    palm(c, 6, 14, (0, -2), 5)
    c.tree(9, 7, "olive-6")
    c.cover([(0, 0), (16, 0), (16, 16), (0, 16)], coverage=0.3, deadBushShare=0.5, cactusShare=0.35,
            tallShare=0.0, flowerShare=0.0, fernShare=0.0)
    return c
