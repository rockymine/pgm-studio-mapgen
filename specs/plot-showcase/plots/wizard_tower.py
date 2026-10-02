"""Wizard's Tower as a 32 x 32 plot: a round stone tower on a stepped knoll under a purple roof, a ridge behind it,
a herb garden over a mushroom cellar cut away on the west face, a round pond in a dell and crystal clusters."""
import math
import random

from kit import Chunk

class At:
    """A chunk seen through an offset: every call lands `dx`, `dz` cells further along the plot."""

    def __init__(self, chunk, dx=0, dz=0, dy=0):
        self.chunk, self.dx, self.dz, self.dy = chunk, dx, dz, dy
        self.blocks = _Blocks(self)

    def set(self, x, y, z, block):
        self.chunk.set(x + self.dx, y + self.dy, z + self.dz, block)

    def box(self, x0, y0, z0, x1, y1, z1, block, hollow=False):
        self.chunk.box(x0 + self.dx, y0 + self.dy, z0 + self.dz, x1 + self.dx, y1 + self.dy, z1 + self.dz,
                       block, hollow)

    def walls(self, x0, y0, z0, x1, y1, z1, block):
        self.chunk.walls(x0 + self.dx, y0 + self.dy, z0 + self.dz, x1 + self.dx, y1 + self.dy, z1 + self.dz, block)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.box(x0, y0, z0, x1, y1, z1, None)

    def disc(self, cx, cz, r, y, block, ring=None):
        self.chunk.disc(cx + self.dx, cz + self.dz, r, y + self.dy, block, ring)

    def ascii(self, x, y, z, legend, *layers):
        self.chunk.ascii(x + self.dx, y + self.dy, z + self.dz, legend, *layers)

    def prop(self, name, x, y, z, turns=0):
        self.chunk.prop(name, x + self.dx, y + self.dy, z + self.dz, turns)

    def raise_(self, x0, z0, x1, z1, h, theme=None):
        self.chunk.raise_(x0 + self.dx, z0 + self.dz, x1 + self.dx, z1 + self.dz, h, theme)

    def lower(self, x0, z0, x1, z1, h, theme=None):
        self.chunk.lower(x0 + self.dx, z0 + self.dz, x1 + self.dx, z1 + self.dz, h, theme)

    def roof(self, x0, z0, x1, z1, floor, top, theme=None):
        self.chunk.roof(x0 + self.dx, z0 + self.dz, x1 + self.dx, z1 + self.dz, floor, top, theme)

    def mound(self, cx, cz, r, h, theme=None):
        self.chunk.mound(cx + self.dx, cz + self.dz, r, h, theme)

    def hill(self, cx, cz, r, h, theme=None, squash=1.0):
        self.chunk.hill(cx + self.dx, cz + self.dz, r, h, theme, squash)

    def basin(self, cx, cz, r, h, theme=None):
        self.chunk.basin(cx + self.dx, cz + self.dz, r, h, theme)

    def tree(self, x, z, style):
        self.chunk.tree(x + self.dx, z + self.dz, style)

    def boulder(self, x, z, size=2, form="round", mossy=True):
        self.chunk.boulder(x + self.dx, z + self.dz, size, form, mossy)

    def cover(self, points, **spec):
        self.chunk.cover([(x + self.dx, z + self.dz) for x, z in points], **spec)


class _Blocks:
    def __init__(self, view):
        self.view = view

    def __contains__(self, key):
        x, y, z = key
        return (x + self.view.dx, y + self.view.dy, z + self.view.dz) in self.view.chunk.blocks


TX, TZ = 17, 9         # tower centre
R = 4                  # tower radius in whole cells (wall ring at 3.5 < d <= 4.5)
KNOLL = 2              # courses of ground the tower stands on
FLOOR_Y = (5, 10, 15)  # plank floors above the ground floor, relative to the knoll top
TOP = 20               # last wall course
CX, CZ = 0, 0          # the tower functions work in tower-relative cells; `At` carries them to TX, TZ

MOUNDS = [(TX, TZ, 9.5, 1), (TX, TZ, 7.2, 2)]     # the knoll's two steps, for placing things on it
CLEARANCE = 4.5


def ground_top(x, z):
    """Top course of the ground at a cell, over the knoll steps and the ridge."""
    top = -1
    for cx, cz, radius, height in MOUNDS:
        if math.hypot(x - cx, z - cz) <= radius:
            top = max(top, height - 1)
    return top


def wall_cells(radius=R + 0.2, ring=1.0):
    """Cells of the tower's wall ring and its interior, as (dx, dz) offsets."""
    wall, inner = [], []
    for dx in range(-6, 7):
        for dz in range(-6, 7):
            dist = math.hypot(dx, dz)
            if dist <= radius + 0.3:
                (wall if dist > radius - ring + 0.3 else inner).append((dx, dz))
    return wall, inner


def tower(c, rng):
    """The round tower, in tower-relative cells with y 0 the ground floor's first course."""
    wall, inner = wall_cells()
    for dx in range(-7, 8):                              # foundation ring
        for dz in range(-7, 8):
            dist = math.hypot(dx, dz)
            if R + 0.4 < dist <= R + 1.3:
                c.set(dx, -1, dz, "98:2" if rng.random() < .5 else "48")
    for y in range(0, TOP + 1):
        for dx, dz in wall:
            roll = rng.random()
            low = y < 5
            block = "98:1" if roll < (.4 if low else .15) else "98:2" if roll < .25 + (.1 if low else 0) else "98:0"
            if y in (*FLOOR_Y, TOP):
                block = "98:3"
            c.set(dx, y, dz, block)
    for dx, dz in inner:                                 # ground floor flags, plank floors
        c.set(dx, -1, dz, "98:0" if (dx + dz) % 2 else "98:2")
        for floor in FLOOR_Y:
            c.set(dx, floor, dz, "5:5" if (dx + dz) % 2 == 0 else "5:1")
    for y in range(0, TOP + 1):                          # the ladder, with holes in each floor
        c.set(-R + 1, y, -1, "65:5")
    for floor in FLOOR_Y:
        c.set(-R + 1, floor, -1, "65:5")
    for y in (0, 1):                                     # door south with a stone surround and steps
        c.set(0, y, R, "64:3" if y == 0 else "64:11")
    c.set(-1, 0, R, "98:3"); c.set(1, 0, R, "98:3")
    c.set(0, 2, R, "98:3"); c.set(-1, 1, R, "109:7"); c.set(1, 1, R, "109:6")
    c.set(0, 0, R + 1, "109:3"); c.set(-1, 0, R + 1, "44:5"); c.set(1, 0, R + 1, "44:5")
    bases = (1, 7, 12, 17)
    for base in bases:                                   # windows: two wide E, W, N; one wide S
        for dx, dz, spans in ((R, 0, (0, 1)), (-R, 0, (0, 1)), (0, -R, (0, 1)), (0, R, (0,))):
            if (dx, dz) == (0, R) and base in (1, FLOOR_Y[1] + 2):
                continue
            pane = "160:10" if base in (7, 17) else "102"
            for span in spans:
                sx, sz = (0, span) if dx else (span, 0)
                for y in (base, base + 1):
                    c.set(dx + sx, y, dz + sz, pane)
                c.set(dx + sx, base - 1, dz + sz, "44:5") if base > 1 else None
                c.set(dx + sx, base + 2, dz + sz, "98:3")
    balcony = FLOOR_Y[1]                                 # balcony on the south side
    for dx in range(-7, 8):
        for dz in range(1, 8):
            dist = math.hypot(dx, dz)
            if R + 0.2 < dist <= R + 1.9:
                c.set(dx, balcony - 1, dz, "98:3" if dist > R + 1.4 else "98:2")
                c.set(dx, balcony, dz, "44:13" if dist <= R + 1.4 else "44:5")
                if dist > R + 1.3:
                    c.set(dx, balcony + 1, dz, "85")
    for y in (balcony + 1, balcony + 2):
        c.set(0, y, R, None)
        c.set(-1, y, R, "160:10"); c.set(1, y, R, "160:10")
    c.set(0, balcony, R, "5:1")
    for y in range(balcony + 1, balcony + 8):            # banner pole with a purple pennant
        c.set(R + 1, y, 2, "85")
    for dx in range(1, 4):
        for y in (balcony + 5, balcony + 6, balcony + 7):
            if dx < 3 or y == balcony + 6:
                c.set(R + 1 + dx, y, 2, "35:10" if y != balcony + 6 else "35:4")
    for sx, sz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):  # corner buttresses
        bx, bz = R * sx, R * sz
        for y in range(0, 9):
            c.set(bx, y, bz, "98:1" if y % 3 == 0 and rng.random() < .5 else "98:0")
        c.set(bx, 9, bz, "109:%d" % (2 if sz < 0 else 3))
        for y in range(0, 2):
            c.set(bx + sx, y, bz, "98:0")
        c.set(bx + sx, 2, bz, "109:%d" % (0 if sx > 0 else 1))
    radii = [5.8, 5.0, 4.3, 3.7, 3.1, 2.5, 1.9, 1.4, 0.9]     # stepped cone, purple clay with blue bands
    for index, radius in enumerate(radii):
        block = "35:10" if index % 3 != 1 else "35:11"
        c.disc(0, 0, radius, TOP + 1 + index, block, ring=1.1 if index < len(radii) - 1 else None)
    c.set(0, TOP + len(radii), 0, "89")
    inside(c, rng)


def inside(c, rng):
    """Study, alchemy loft, bedroom and observatory, one a level."""
    c.set(0, 0, 0, "116")                                # level 0: study, an enchanting table and a ring of shelves
    for dx, dz in ((-1, -2), (2, -1), (-1, 2), (1, 2), (-3, 0), (3, 1), (2, -2)):
        c.set(dx, 0, dz, "47"); c.set(dx, 1, dz, "47")
    c.set(1, 0, -1, "47")
    c.set(0, 4, 1, "89")
    f = FLOOR_Y[0] + 1                                   # level 1: alchemy
    c.set(0, f, 0, "117"); c.set(-1, f, 0, "118:3"); c.set(1, f, 0, "58")
    for dx, dz in ((2, -1), (1, 2), (-1, 2), (-1, -2), (-3, 1), (3, 0)):
        c.set(dx, f, dz, "47"); c.set(dx, f + 1, dz, "47")
    c.set(1, f, 1, "140"); c.set(-1, f, 1, "54:2")
    c.set(1, FLOOR_Y[1] - 1, 1, "89")
    f = FLOOR_Y[1] + 1                                   # level 2: bedroom desk
    c.set(0, f, 1, "26:3"); c.set(1, f, 1, "26:11")
    c.set(1, f, -1, "145:0"); c.set(-1, f, 1, "47"); c.set(-1, f + 1, 1, "47")
    c.set(2, f, -1, "47"); c.set(2, f + 1, -1, "47"); c.set(-3, f, 1, "54:5")
    c.set(0, FLOOR_Y[2] - 1, 0, "89")
    f = FLOOR_Y[2] + 1                                   # level 3: observatory
    c.set(0, f, 0, "58")
    c.set(0, f + 1, 0, "140"); c.set(-1, f, 0, "47"); c.set(1, f, 0, "47")
    c.set(0, FLOOR_Y[2] + 4, 0, "89")


def vines(c, rng):
    """Vines on the tower's outer face, where a wall block stands behind the cell."""
    wall, _ = wall_cells()
    wall_set = set(wall)
    for y in range(1, 17):
        for dx, dz in wall:
            for sx, sz, bit in ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1)):
                x, z = dx + sx, dz + sz
                if (x, y, z) in c.blocks or (x, z) in wall_set:
                    continue
                if abs(sx * dx + sz * dz) < 2:
                    continue
                if y < 8 and rng.random() < .13 or y >= 8 and rng.random() < .04:
                    c.set(x, y, z, f"106:{bit}")


def cellar(c, rng):
    """A mushroom cellar: the cut face shows shelves, a still, glowing mushrooms and roots (chunk coordinates)."""
    c.lower(0, 6, 7, 13, -6)
    c.roof(0, 6, 7, 11, -2, 0)
    c.roof(0, 12, 2, 13, -2, 0)
    c.roof(5, 12, 7, 13, -2, 0)
    for x in range(0, 8):
        for z in range(6, 14):
            c.set(x, -7, z, "110" if rng.random() < .4 else "3:2")
    for z in (6, 13):
        for y in range(-6, -2):
            c.set(0, y, z, "17:1")
    for z in range(6, 14):
        c.set(0, -3, z, "17:9")
    for x in range(0, 8):
        c.set(x, -3, 7, "17:5") if x in (0, 7) else None
    for x in range(1, 7):
        for y in (-6, -5):
            c.set(x, y, 7, "47") if x not in (3, 4) else None
    c.set(3, -6, 7, "118:3"); c.set(4, -6, 7, "117"); c.set(3, -5, 7, "140"); c.set(4, -5, 7, "58")
    for x in (1, 2, 5, 6):
        c.set(x, -4, 7, "47")
    c.set(1, -6, 8, "54:3"); c.set(6, -6, 8, "145:0"); c.set(1, -5, 8, "144:1")
    for x, z, height in ((2, 11, 2), (5, 11, 1), (6, 12, 2)):     # mushroom trees
        for y in range(-6, -6 + height):
            c.set(x, y, z, "99:10")
        top = -6 + height
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                c.set(x + dx, top, z + dz, "100:14" if (x, z) != (5, 11) else "99:14")
        c.set(x, top + 1, z, "100:14" if (x, z) != (5, 11) else "99:14")
    for x, z in ((0, 12), (7, 8)):
        c.set(x, -6, z, "169"); c.set(x, -5, z, "95:3")
    c.set(7, -6, 12, "169"); c.set(7, -5, 12, "95:11"); c.set(6, -6, 13, "95:3")
    for x, z in ((1, 12), (4, 13), (3, 10), (6, 11), (2, 8), (5, 7)):
        c.set(x, -3, z, "17:12")
        for y in range(-4, -4 - rng.randint(0, 2), -1):
            c.set(x, y, z, "106:0")
    c.set(7, -3, 6, "30"); c.set(0, -3, 6, "30"); c.set(0, -3, 13, "30"); c.set(7, -3, 13, "30")
    c.set(1, -7, 11, "9"); c.set(2, -7, 12, "9"); c.set(1, -7, 12, "9"); c.set(2, -7, 13, "9")
    c.set(5, -6, 13, "144:1"); c.set(6, -6, 11, "39")
    c.set(0, -10, 10, "56"); c.set(0, -11, 9, "21")
    for y in range(-6, 0):                               # hatch down with a ladder, ringed by a low wall
        c.set(3, y, 13, "65:2")
    for x, z in ((2, 12), (2, 13), (5, 12), (5, 13), (3, 11), (4, 11)):
        c.set(x, 0, z, "139:1")
    c.set(2, 1, 12, "50:5"); c.set(5, 1, 12, "50:5")


def herb_beds(c, rng):
    """Two raised herb beds over the cellar, bordered with slabs (chunk coordinates, above the cellar)."""
    for x0, z0 in ((1, 9), (5, 9)):
        for x in range(x0, x0 + 3):
            for z in range(z0, z0 + 2):
                c.set(x, -1, z, "3:2" if rng.random() < .5 else "3:0")
                c.set(x, 0, z, rng.choice(("37", "38:1", "38:3", "38:7", "38:2", "39", "40", "38:0", "38:4")))
    for x0, z0, x1, z1 in ((1, 9, 3, 10), (5, 9, 7, 10)):
        for x in range(x0 - 1, x1 + 2):
            for z in (z0 - 1, z1 + 1):
                c.set(x, 0, z, "126:9") if (x, z) not in {(3, 11), (4, 11)} else None


def pond(c, rng):
    """A round dell with a pond, lily pads and sugar cane round it."""
    cx, cz, radius = 25, 25, 4.3
    c.basin(cx, cz, radius, -2)
    for x in range(int(cx - radius) - 1, int(cx + radius) + 2):
        for z in range(int(cz - radius) - 1, int(cz + radius) + 2):
            if math.hypot(x - cx, z - cz) <= radius - 0.4:
                for y in (-2, -1):
                    c.set(x, y, z, "9")
    for x, z in ((23, 24), (26, 23), (25, 27), (27, 26), (24, 26)):
        c.set(x, 0, z, "111")
    for x, z in ((20, 24), (21, 28), (29, 24), (28, 29), (21, 22), (29, 28)):
        c.set(x, 0, z, "83")
        c.set(x, 1, z, "83") if (x + z) % 2 else None


def east_beds(c, rng):
    """A long bed of flowers and mushrooms with a fence and a stone bench, south-east of the tower."""
    for x in range(21, 27):
        for z in (17, 18):
            c.set(x, -1, z, "3:2")
            c.set(x, 0, z, rng.choice(("38:5", "37", "38:2", "39", "38:8", "40", "38:6")))
    for x in range(20, 28):
        c.set(x, 0, 16, "126:9"); c.set(x, 0, 19, "126:9")
    for z in (17, 18):
        c.set(20, 0, z, "126:9"); c.set(27, 0, z, "126:9")
    for x in range(22, 26):                              # the bench
        c.set(x, 0, 14, "126:1")
    c.set(22, 1, 14, "50:5"); c.set(25, 1, 14, "50:5")


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


def path(c, rng, points, width=2):
    """Flagstones and gravel along a poly-line, flush with the ground wherever it runs."""
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        steps = max(abs(x1 - x0), abs(z1 - z0))
        for step in range(steps + 1):
            x = round(x0 + (x1 - x0) * step / steps)
            z = round(z0 + (z1 - z0) * step / steps)
            for dx in range(width):
                top = ground_top(x + dx, z)
                if (x + dx, top + 1, z) not in c.blocks and (x + dx, top, z) not in c.blocks:
                    c.set(x + dx, top, z, rng.choice(("13", "98:2", "48", "13")))


def build():
    c = Chunk("wizard-tower", "Wizard's Tower", "forest",
              "A round stone tower on its knoll under a stepped purple roof, windows onto a study and an alchemy "
              "loft, a herb garden, a pond, crystals and a mushroom cellar cut away below.", size=32)
    rng = random.Random(23)
    c.mound(TX, TZ, 9.5, 1)                              # the knoll, two steps
    c.mound(TX, TZ, 7.2, 2)
    c.raise_poly([(0, 0), (11, 0), (12, 4), (9, 9), (0, 11)], 4)    # the ridge behind, NW
    c.mound(5, 4, 4.2, 6)
    c.mound(28, 9, 3.2, 3)                               # crystal knoll
    c.mound(9, 14, 2.8, 2)
    base = At(c, TX, TZ, KNOLL)
    tower(base, rng)
    vines(base, rng)
    cellar(At(c, 0, 15), rng)
    herb_beds(At(c, 0, 15), rng)
    pond(c, rng)
    east_beds(c, rng)
    cluster(At(c, 0, 0, 5), 28, 9, 4)
    cluster(At(c, 0, 0, 1), 9, 14, 3)
    path(c, rng, [(17, 31), (17, 26), (15, 21), (17, 16)], 2)
    for x, z in ((14, 28), (20, 29)):                    # a signpost and a lantern post on the path
        c.set(x, -1 + 0, z, "85"); c.set(x, 0, z, "85"); c.set(x, 1, z, "85")
    c.set(14, 2, 28, "89"); c.set(20, 2, 29, "89")
    c.set(12, 0, 22, "85"); c.set(12, 1, 22, "85"); c.set(12, 2, 22, "89")
    c.tree(5, 4, "birch-9")
    c.cover([(0, 0), (32, 0), (32, 32), (0, 32)], coverage=0.55, fernShare=0.3, flowerShare=0.12,
            tallShare=0.2, mushroomShare=0.08)
    return c
