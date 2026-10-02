"""The Forgotten Crypt as a 32 x 32 plot: a long ruined chapel whose collapsed nave is a gentle stair trench down
to a stone-brick vault (pillars, sarcophagi, an iron-bar cell, a lava well, a flooded corner) cut away on the
west side; a graveyard with a weeping statue and a dead tree on the hill above it; a ridge, a knoll and a dell."""
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


FLOOR = -9          # vault floor course
CEIL = -4           # last air course in the vault
NAVE_END = 23       # east end of the stair trench and the chapel
SHIFT = 8           # the vault and chapel sit this far south in the plot


def brick(rng, mossy=0.3, cracked=0.25):
    roll = rng.random()
    return "98:1" if roll < mossy else "98:2" if roll < mossy + cracked else "98:0"


def vault(c, rng):
    """The vault, in its own coordinates (x 0..8, z 2..13) with the stair trench running east from its wall."""
    c.lower(0, 2, 8, 13, FLOOR + 1)
    c.roof(0, 2, 8, 13, -3, 0)
    c.lower(9, 6, NAVE_END, 9, FLOOR + 1)               # the stair trench
    for x in range(0, 9):
        for z in range(2, 14):
            c.set(x, FLOOR, z, "98:0" if (x + z) % 2 else "98:2" if rng.random() < .5 else "98:1")
    for y in range(FLOOR + 1, CEIL + 1):
        for x in range(0, 9):
            c.set(x, y, 2, brick(rng)); c.set(x, y, 13, brick(rng))
        for z in range(2, 14):
            if not 6 <= z <= 9:
                c.set(8, y, z, brick(rng))
        for x in range(9, NAVE_END + 1):
            c.set(x, y, 5, brick(rng)); c.set(x, y, 10, brick(rng))
    for y in range(CEIL + 1, 0):
        for x in range(9, NAVE_END + 1):
            c.set(x, y, 5, brick(rng, .45)); c.set(x, y, 10, brick(rng, .45))
        for z in range(6, 10):
            c.set(8, y, z, "98:1") if y < -1 else None
    for x in range(0, 8):                               # ceiling frieze of chiselled bricks
        for z in range(3, 13):
            if z in (3, 12) or x % 3 == 1:
                c.set(x, CEIL, z, "98:3" if (x + z) % 2 == 0 else "98:2")
    # a gentle stair, two treads to the course, solid under each
    for step in range(8):
        y = -1 - step
        for run in (0, 1):
            x = NAVE_END - 2 * step - run
            for z in (6, 7, 8, 9):
                c.set(x, y, z, "109:0" if step % 3 else "67:0")
                for under in range(FLOOR, y):
                    c.set(x, under, z, brick(rng))
    for x, z in ((2, 5), (5, 5), (2, 10), (5, 10)):     # pillars with stair feet and chiselled caps
        for y in range(FLOOR + 1, CEIL):
            c.set(x, y, z, "155:2" if y not in (FLOOR + 1,) else "155:1")
        c.set(x, CEIL, z, "98:3")
        for dx, dz, data in ((1, 0, 1), (-1, 0, 0), (0, 1, 3), (0, -1, 2)):
            c.set(x + dx, FLOOR + 1, z + dz, f"109:{data}") if rng.random() < .7 else None
    for x0, z0 in ((1, 3), (5, 3)):                     # sarcophagi on the north wall
        c.box(x0, FLOOR + 1, z0, x0 + 2, FLOOR + 1, z0 + 1, "98:0")
        c.box(x0, FLOOR + 2, z0, x0 + 2, FLOOR + 2, z0 + 1, "44:7")
        c.set(x0, FLOOR + 3, z0, "144:1")
    c.set(2, FLOOR + 2, 3, "155:0"); c.set(6, FLOOR + 2, 4, "44:13")
    c.box(1, FLOOR + 1, 7, 2, FLOOR + 1, 9, "98:2")     # a lone sarcophagus, open, a chest at its foot
    c.box(1, FLOOR + 2, 7, 2, FLOOR + 2, 9, "44:5")
    c.set(1, FLOOR + 2, 8, "144:1"); c.set(2, FLOOR + 2, 7, "30")
    c.set(1, FLOOR + 1, 10, "54:2")
    c.box(4, FLOOR + 1, 11, 4, FLOOR + 4, 12, "101")    # iron-bar cell in the south-east corner
    c.box(5, FLOOR + 4, 11, 7, FLOOR + 4, 12, "101")
    c.box(5, FLOOR + 1, 11, 7, FLOOR + 1, 11, "101")
    c.set(6, FLOOR + 1, 12, "54:2"); c.set(7, FLOOR + 1, 12, "144:1"); c.set(5, FLOOR + 1, 12, "30")
    c.set(7, FLOOR + 2, 12, "30"); c.set(4, FLOOR + 1, 10, "144:1")
    c.box(0, FLOOR + 1, 11, 2, FLOOR + 1, 12, "98:0")   # lava well in the south-west
    c.box(1, FLOOR, 11, 1, FLOOR, 12, "11"); c.set(1, FLOOR + 1, 11, "11"); c.set(1, FLOOR + 1, 12, "11")
    c.set(0, FLOOR + 1, 11, "11"); c.set(0, FLOOR, 11, "11")
    c.set(2, FLOOR + 1, 11, "11"); c.set(2, FLOOR, 11, "11")
    c.box(5, FLOOR, 3, 7, FLOOR, 4, "9"); c.box(6, FLOOR + 1, 3, 7, FLOOR + 1, 4, "9")   # flooded corner
    c.set(5, FLOOR + 1, 3, "111"); c.set(7, FLOOR + 1, 3, "111")
    c.box(5, FLOOR + 1, 5, 7, FLOOR + 2, 5, "101")
    c.set(6, CEIL, 7, "169"); c.set(0, CEIL, 8, "89"); c.set(3, CEIL, 7, "89"); c.set(6, CEIL - 1, 7, "89")
    for x, z in ((3, 3), (4, 12), (7, 3)):
        c.set(x, -6, z + 1 if z == 3 else z - 1, "50:3" if z == 3 else "50:4")
    for x, y, z in ((0, CEIL, 3), (7, CEIL, 3), (0, CEIL, 12), (7, CEIL, 12), (4, CEIL, 7), (8, CEIL, 5)):
        c.set(x, y, z, "30")
    for x, z in ((3, 7), (6, 8), (4, 9), (3, 12), (0, 5)):
        c.set(x, FLOOR + 1, z, "144:1") if (x + z) % 3 == 0 else c.set(x, FLOOR + 1, z, "30")
    c.set(0, FLOOR - 2, 7, "56"); c.set(0, FLOOR - 3, 8, "56"); c.set(0, FLOOR - 1, 4, "14")
    c.set(0, FLOOR - 4, 10, "21"); c.set(0, FLOOR - 2, 12, "129")


def chapel(c, rng):
    """Ruined walls round the long trench, ragged at the top, a broken portal over the stairs, an open east end."""
    heights = {}
    for x in range(9, NAVE_END + 1):
        edge = x == NAVE_END
        heights[(x, 3)] = 2 if edge else rng.choice((2, 3, 4, 3, 5))
        heights[(x, 12)] = 2 if edge else rng.choice((2, 3, 4, 3))
    for x in range(14, NAVE_END):                       # the far nave has fallen further
        heights[(x, 3)] = min(heights[(x, 3)], rng.choice((1, 2, 3)))
        heights[(x, 12)] = min(heights[(x, 12)], rng.choice((1, 2, 2)))
    for (x, z), top in heights.items():
        for y in range(0, top + 1):
            c.set(x, y, z, brick(rng, .4, .3))
    for x in (9, 12, 15, 18, 21, NAVE_END):             # buttress pillars, taller
        for z in (3, 12):
            top = 7 if x < 15 else 5 if x < 21 else 3
            for y in range(0, top):
                c.set(x, y, z, "98:0" if y % 2 == 0 else "98:1")
            c.set(x, top, z, "109:2" if z == 3 else "109:3")
    for z in range(3, 13):                              # west end wall, an arch over the trench
        top = 6 if z in (3, 4, 11, 12) else 3
        if 6 <= z <= 9:
            continue
        for y in range(0, top + 1):
            c.set(9, y, z, brick(rng))
    c.box(9, 0, 5, 9, 5, 5, "98:0"); c.box(9, 0, 10, 9, 5, 10, "98:0")
    c.set(9, 5, 6, "109:7"); c.set(9, 5, 9, "109:6")
    c.box(9, 6, 5, 9, 6, 10, "98:3"); c.set(9, 6, 7, "98:2")
    c.set(9, 7, 7, "44:5"); c.set(9, 7, 8, "44:5")
    c.box(9, 3, 6, 9, 4, 6, "101"); c.box(9, 3, 9, 9, 4, 9, "101")
    c.set(9, 4, 7, "101"); c.set(9, 4, 8, "101")
    for x in range(11, NAVE_END, 3):                    # barred windows
        for z in (3, 12):
            c.set(x, 1, z, "101")
    for x in range(10, NAVE_END):                       # cracked flags either side of the trench
        for z in (4, 11):
            c.set(x, -1, z, "98:2" if rng.random() < .5 else "48")
    for x in range(9, NAVE_END):                        # vines on the outer faces, cobwebs in the corners
        for y in range(0, 3):
            if rng.random() < .5 and y < heights[(x, 3)]:
                c.set(x, y, 2, "106:1")
            if rng.random() < .35 and y < heights[(x, 12)]:
                c.set(x, y, 13, "106:4")
    c.set(11, 3, 3, "30"); c.set(14, 2, 12, "30"); c.set(10, 3, 12, "30"); c.set(13, 2, 3, "30")


def graveyard(c, rng):
    """Stones over the vault on gentle mounds, a dead tree on a knoll, the weeping statue on a small hill."""
    stones = ((1, 14), (3, 17), (2, 20), (6, 15), (7, 19), (5, 21), (7, 13), (3, 12))
    for index, (x, z) in enumerate(stones):
        form = index % 3
        if form == 0:
            c.set(x, 0, z, "98:2"); c.set(x, 1, z, "44:3")
        elif form == 1:
            c.set(x, 0, z, "139:1"); c.set(x, 1, z, "139:1")
        else:
            c.set(x, 0, z, "109:2"); c.set(x, 1, z, "44:8")
        c.set(x, -1, z + 1, "3:1")
    for x in range(0, 9):                               # iron fence along the south, a gate gap
        if x not in (4, 5):
            c.set(x, 0, 23, "101"); c.set(x, 1, 23, "101")
    for x in (0, 3, 6, 8):
        c.set(x, 0, 23, "98:1"); c.set(x, 1, 23, "98:2"); c.set(x, 2, 23, "44:5")
    for x in (3, 6):
        c.set(x, 2, 23, "44:5")
    # the dead tree on its knoll (ground top course 1), trunk base at y 2
    tx, tz, base = 7, 6, 2
    c.hill(tx, tz, 4.2, 2)
    c.box(tx, base, tz, tx, base + 3, tz, "17:1")
    for dx, dy, dz in ((-1, 3, 0), (-2, 4, 0), (-3, 5, 0), (-3, 6, 0), (1, 3, 0), (2, 4, 0), (3, 5, 0), (0, 4, 0),
                       (0, 5, 0), (0, 6, 0), (0, 4, -1), (0, 5, -2), (0, 6, -2), (0, 4, 1), (0, 5, 2), (-1, 6, 0),
                       (-2, 6, 0), (1, 6, 0), (2, 6, 0), (0, 7, -1), (0, 7, 1), (-4, 6, 0), (3, 6, 0)):
        c.set(tx + dx, base + dy, tz + dz, "191")
    c.set(tx - 1, base, tz, "17:5"); c.set(tx + 1, base, tz, "17:5")
    for dx, dy, dz in ((0, 3, -1), (-2, 3, 0), (1, 4, 1)):
        c.set(tx + dx, base + dy, tz + dz, "30")
    # the weeping figure on a plinth atop a terraced hill
    sx, sz, top = 2, 5, 3
    c.hill(sx, sz, 4.5, top)
    for dy, block in enumerate(("98:3", "98:0", "98:3", "98:1", "98:0", "144:0")):
        c.set(sx, top + dy, sz, block)
    c.set(sx - 1, top + 3, sz, "44:13"); c.set(sx + 1, top + 3, sz, "44:13")
    c.set(sx - 1, top + 4, sz, "109:7"); c.set(sx + 1, top + 4, sz, "109:6")
    for x, z in ((4, 24), (1, 10), (7, 16), (8, 21), (0, 18)):
        c.set(x, 0, z, "32")


def path(c, rng, points, width=2):
    """A mossy cobble and gravel path along a poly-line, flush with the grass."""
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        steps = max(abs(x1 - x0), abs(z1 - z0))
        for step in range(steps + 1):
            x = round(x0 + (x1 - x0) * step / steps)
            z = round(z0 + (z1 - z0) * step / steps)
            for dx in range(width):
                for dz in range(width):
                    if (x + dx, 0, z + dz) not in c.blocks:
                        c.set(x + dx, -1, z + dz, rng.choice(("48", "13", "98:2", "13")))


def build():
    c = Chunk("crypt", "The Forgotten Crypt", "grass",
              "A ruined chapel with a long collapsed nave opens a stair down to a cobwebbed vault of pillars, "
              "sarcophagi, an iron-bar cell and a lava well, a graveyard on the hill above.", size=32)
    rng = random.Random(7)
    # relief: a ridge behind the chapel, a knoll for the spruce, a dell for the boulder
    c.raise_poly([(19, 0), (31, 0), (31, 8), (27, 9), (22, 8)], 3)
    c.hill(27, 4, 5, 6)
    c.hill(14, 3, 3.5, 2)
    c.hill(27, 24, 5, 3)
    c.basin(19, 26, 3.2, -1)
    vault(At(c, 0, SHIFT), rng)
    chapel(At(c, 0, SHIFT), rng)
    graveyard(c, rng)
    path(c, rng, [(16, 30), (16, 27), (11, 26), (4, 24)])
    path(c, rng, [(16, 27), (20, 23), (24, 18)])
    c.tree(27, 24, "tiny-spruce-4")
    c.boulder(13, 5, 4, "angular")
    c.cover([(0, 0), (32, 0), (32, 32), (0, 32)], coverage=0.5, fernShare=0.4, flowerShare=0.04,
            deadBushShare=0.15, mushroomShare=0.1)
    return c
