"""Abandoned Mine as a 32 x 32 plot: a terraced rocky hill with a timber-framed adit cut into its south face and
rails and ore carts running out of it, a winch over a shaft that drops into an ore-studded cave (cut away on the
west face), a miners' shack on its own knoll, crates, TNT and ore heaps."""
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


ORES = ("16", "15", "14", "16", "73", "56", "21", "16", "15")
POST, BEAM, PLANK = "17:1", "17:5", "5:1"
HILL = (16, 11, 10.0, 8)          # centre x, centre z, foot radius, courses
CENTRE = 16                       # the rails and the adit run down this column
FACE, PORTAL = 9, 17              # z of the tunnel's working face and of its portal frame
CAVE_SHIFT = 12                   # the cave sits this far south of where the chunk drew it


def ore(rng):
    return rng.choice(ORES)


def hill_courses(x, z):
    """Courses of the terraced hill over a cell, matching `Chunk.hill`'s rings."""
    cx, cz, radius, courses = HILL
    count = 0
    for course in range(1, courses + 1):
        if math.hypot(x - cx, z - cz) <= radius * (1 - (course - 1) / courses * 0.7):
            count = course
    return count


def adit(c, rng):
    """The tunnel into the hill, three wide inside its timber frames, rails down the middle."""
    left, right = CENTRE - 2, CENTRE + 2
    c.lower(left, FACE, right, PORTAL, 0)
    for x in range(left, right + 1):                    # ceiling: the hill's own ground from y 4 up
        for z in range(FACE, PORTAL + 1):
            top = hill_courses(x, z)
            if top > 4:
                c.roof(x, z, x, z, 4, top)
    for z in range(FACE, PORTAL + 1, 2):                # timber frames
        for y in range(0, 3):
            c.set(left, y, z, POST); c.set(right, y, z, POST)
        for x in range(left, right + 1):
            c.set(x, 3, z, BEAM)
    for z in range(FACE + 1, PORTAL, 2):                # planked lagging between the frames
        for y in range(0, 3):
            if rng.random() < .55:
                c.set(left, y, z, PLANK)
            if rng.random() < .55:
                c.set(right, y, z, PLANK)
    for z in (PORTAL, PORTAL - 4, FACE + 2):            # cross braces
        c.set(left + 1, 2, z, "126:9"); c.set(right - 1, 2, z, "126:9")
    c.box(left, 4, PORTAL, right, 4, PORTAL, "5:1")     # the lintel board over the portal
    c.set(CENTRE, 4, PORTAL + 1, "68:3")
    c.set(left - 1, 5, PORTAL, "17:1"); c.set(right + 1, 5, PORTAL, "17:1")
    for z in range(FACE + 2, PORTAL, 2):
        c.set(left + 1, 2, z, "50:1"); c.set(right - 1, 2, z, "50:2")
    c.set(left, 2, PORTAL + 1, "50:3"); c.set(right, 2, PORTAL + 1, "50:3")
    for z in range(FACE - 1, PORTAL):                   # ore on the walls and at the face
        for y in range(0, 4):
            if rng.random() < .22:
                c.set(left - 1, y, z, ore(rng))
                c.set(right + 1, y, z, ore(rng)) if rng.random() < .8 else None
    for x in range(left, right + 1):
        for y in range(0, 4):
            c.set(x, y, FACE - 1, ore(rng) if rng.random() < .5 else "1")
    for z in range(FACE + 1, 32):                       # rails out to the south edge, a bumper at the face
        c.set(CENTRE, 0, z, "66:0")
    c.set(CENTRE, 0, FACE, "98:2"); c.set(CENTRE, 1, FACE, "50:5")
    c.set(CENTRE - 1, 0, FACE, "16"); c.set(CENTRE + 1, 0, FACE, "16")
    for z, load in ((13, "15"), (15, "173"), (23, "14"), (26, "16")):     # carts: a hopper under a heap of ore
        c.set(CENTRE, 0, z, "154:0"); c.set(CENTRE, 1, z, load)
    c.set(CENTRE, 1, 15, "173"); c.set(CENTRE, 2, 15, "173")
    c.set(CENTRE - 1, 0, 12, "16"); c.set(CENTRE + 1, 0, 14, "15"); c.set(CENTRE - 1, 0, 16, "13")
    c.set(CENTRE + 1, 0, 11, "13")
    c.set(CENTRE + 1, 0, 13, "17:9"); c.set(CENTRE + 2, 0, 13, "17:9")    # a fallen beam
    c.set(CENTRE - 1, 0, 15, "30"); c.set(CENTRE + 1, 0, 12, "30")
    for x, z in ((left, 12), (right, 16), (left, 16), (right, 12)):
        c.set(x, 3, z, "30")


def cave(c, rng):
    """The ore cave under the western flank, a shaft up to the surface and a winch over it (chunk coordinates)."""
    c.lower(0, 5, 5, 14, -6)
    c.roof(0, 5, 5, 8, -2, 0)
    c.roof(0, 11, 5, 14, -2, 0)
    c.roof(0, 9, 1, 10, -2, 0)
    c.roof(4, 9, 5, 10, -2, 0)
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
    for x in (0, 3):
        for z in (6, 13):
            for y in range(-6, -2):
                c.set(x, y, z, POST)
        for z in range(6, 14):
            c.set(x, -3, z, "17:9")
    for z in range(7, 13):
        for x in range(0, 6):
            if rng.random() < .35:
                c.set(x, -7, z, "13" if rng.random() < .6 else "3:1")
    for z in range(7, 13):
        c.set(4, -6, z, "66:0")
    c.set(4, -6, 10, "154:0"); c.set(4, -5, 10, "173")
    c.set(4, -6, 8, "154:0"); c.set(4, -5, 8, "15")
    c.box(1, -6, 12, 2, -6, 12, "46"); c.set(1, -5, 12, "46"); c.set(0, -6, 12, "5:1")
    c.set(2, -5, 12, "126:1")
    c.set(1, -6, 7, "54:3"); c.set(2, -6, 7, "58"); c.set(1, -6, 8, "170:0")
    c.set(1, -4, 6, "69:3"); c.set(1, -5, 6, "69:3")
    for x, z in ((0, 9), (3, 8), (3, 11), (0, 11)):
        c.set(x, -4, z, "85"); c.set(x, -5, z, "89")
    c.set(5, -6, 7, "89")
    c.set(5, -6, 12, "30"); c.set(0, -3, 6, "30"); c.set(0, -3, 13, "30")
    c.set(1, -6, 10, "13"); c.set(0, -6, 9, "56")
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
    c.set(2, -4, 9, "118:3")
    c.set(0, 5, 9, "17:5")
    c.set(5, 5, 9, "85"); c.set(5, 4, 9, "85")
    c.set(1, 2, 7, "85"); c.set(1, 3, 7, "89")
    # fenced shaft collar, ore heaps and a crate stack on the cave roof
    for x, z in ((2, 11), (3, 11), (2, 8), (3, 8)):
        c.set(x, 0, z, "85")
    heap = [((4, 0, 12), "16"), ((5, 0, 12), "15"), ((4, 0, 13), "14"), ((5, 0, 13), "16"), ((4, 1, 12), "16"),
            ((5, 1, 13), "13"), ((6, 0, 13), "13"), ((6, 0, 12), "15"), ((3, 0, 13), "16"), ((4, 1, 13), "15")]
    for (x, y, z), block in heap:
        c.set(x, y, z, block)
    c.prop("crates", 5, 0, 11)


def shack(c, rng, x0, z0):
    """A miners' shack: spruce walls on log corners, a gabled stair roof with a chimney, a bunk, a stove, a chest
    and a bench; five wide, six deep, its ridge along z, on the knoll's flat top (y 0 is its floor course + 1)."""
    x1, z1 = x0 + 4, z0 + 5
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
    c.set(x0, 0, z0 + 3, "64:0"); c.set(x0, 1, z0 + 3, "64:8")
    for x, z in ((x0 + 1, z1), (x0 + 3, z1), (x1, z0 + 2), (x1, z0 + 4), (x0 + 1, z0), (x0 + 3, z0), (x0, z0 + 1)):
        c.set(x, 1, z, "102")
    for z in range(z0 - 1, z1 + 2):
        c.set(x0 - 1, 3, z, "134:0"); c.set(x1 + 1, 3, z, "134:1")
        c.set(x0, 4, z, "134:0"); c.set(x1, 4, z, "134:1")
        c.set(x0 + 1, 5, z, "134:0"); c.set(x1 - 1, 5, z, "134:1")
        c.set(x0 + 2, 5, z, "126:1")
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            c.set(x, 3, z, PLANK)
        for x in range(x0 + 1, x1):
            c.set(x, 4, z, PLANK)
    for dy in range(1, 8):                              # the chimney over the stove
        c.set(x1 - 1, dy, z1 - 1, "4")
    c.set(x1 - 1, 8, z1 - 1, "44:4")
    c.set(x0 + 1, 0, z0 + 1, "26:0"); c.set(x0 + 1, 0, z0 + 2, "26:8")
    c.set(x1 - 1, 0, z1 - 1, "61:3"); c.set(x0 + 1, 0, z1 - 1, "54:2"); c.set(x1 - 1, 0, z0 + 1, "58")
    c.set(x0 + 2, 2, z0 + 3, "89")
    c.set(x0 - 2, 0, z0 + 2, "85"); c.set(x0 - 2, 1, z0 + 2, "85"); c.set(x0 - 2, 2, z0 + 2, "89")    # porch lantern
    c.set(x0 - 1, 0, z0 + 4, "126:1"); c.set(x0 - 1, 0, z0 + 5, "126:1")                             # a bench
    c.set(x0 - 2, 0, z0 + 4, "17:5")
    c.set(x0 - 1, 1, z0 + 3, "69:2")                    # a pick leaning on the wall


def yard(c, rng):
    """Clutter on the apron below the portal and by the cutting."""
    c.prop("barrels", 20, 0, 23)
    c.prop("crates", 12, 0, 22)
    c.box(11, 0, 19, 11, 0, 19, "46"); c.set(12, 0, 19, "46"); c.set(11, 1, 19, "46")      # TNT, chest, bench
    c.set(10, 0, 20, "54:4"); c.set(11, 0, 20, "170:0")
    c.set(14, 0, 22, "173"); c.set(13, 0, 22, "44:3")
    for x, z in ((14, 24), (18, 24), (14, 28), (18, 28)):                                  # lantern posts
        c.set(x, 0, z, "85"); c.set(x, 1, z, "85"); c.set(x, 2, z, "89")


def paint_hill(c, rng):
    """Patches of turf, coarse dirt, gravel and moss on the terrace tops, so the rock is not one grey."""
    for x in range(4, 29):
        for z in range(0, 23):
            courses = hill_courses(x, z)
            top = courses - 1
            if courses < 2 or (x, top, z) in c.blocks or (13 <= x <= 19 and FACE - 1 <= z <= 23):
                continue
            if math.hypot(x - 16, z - 11) > 9.3 and rng.random() < .5:
                continue
            roll = rng.random()
            c.set(x, top, z, "2" if roll < .35 else "3:1" if roll < .5 else "13" if roll < .65
                  else "48" if roll < .75 else "3:2" if roll < .82 else "1")


def ground_top(x, z):
    """Top course of the ground at a cell outside the hill."""
    if math.hypot(x - 24, z - 22) <= 6.3 or math.hypot(x - 26, z - 10) <= 3.5:
        return 1
    return -1


def paint_flats(c, rng):
    """Turf, gravel and coarse dirt in blobs over the flat rock, so the foot of the hill reads as ground."""
    blobs = [(rng.uniform(0, 32), rng.uniform(0, 32), rng.uniform(2.2, 4.5), rng.choice(("2", "2", "2", "13", "3:1")))
             for _ in range(16)]
    blobs += [(24, 22, 5.5, "2"), (26, 10, 3.2, "2"), (10, 25, 3.5, "13"), (20, 26, 3, "3:1")]
    for x in range(0, 32):
        for z in range(0, 32):
            if hill_courses(x, z) or (13 <= x <= 19 and FACE - 1 <= z <= 23):
                continue
            if x <= 6 and 17 <= z <= 27 or (x, z) == (CENTRE, z) or x == CENTRE:
                continue
            top = ground_top(x, z)
            if (x, top, z) in c.blocks:
                continue
            for bx, bz, radius, block in blobs:
                if math.hypot(x - bx, z - bz) <= radius * (0.75 + 0.25 * rng.random()):
                    c.set(x, top, z, block if block != "2" or rng.random() < .85 else "3:1")
                    break


def build():
    c = Chunk("mine", "Abandoned Mine", "rock",
              "A terraced hill with a timber-framed adit cut into it, ore carts on rails, a winch over a shaft and "
              "an ore-studded cave cut away on the west face, a miners' shack on its own knoll.", size=32)
    rng = random.Random(11)
    c.hill(HILL[0], HILL[1], HILL[2], HILL[3])
    c.lower(13, PORTAL + 1, 19, 23, 0)                 # the cutting in front of the portal
    c.mound(24, 22, 6.3, 2)                             # the shack's knoll
    c.mound(26, 10, 3.5, 2)                             # a spoil heap beside the hill
    adit(c, rng)
    cave(At(c, 0, CAVE_SHIFT), rng)
    shack(At(c, 0, 0, 2), rng, 22, 19)
    yard(c, rng)
    paint_hill(c, rng)
    paint_flats(c, rng)
    for x, z in ((20, 7), (10, 11)):                   # turf under each trunk
        c.set(x, hill_courses(x, z) - 1, z, "2")
    c.tree(20, 7, "tiny-spruce-4")
    c.tree(10, 11, "tiny-spruce-2")
    for x, z, y in ((24, 8, 1), (10, 14, 2), (22, 6, 3), (12, 7, 4)):                      # hand-heaped scree
        c.set(x, y, z, "4"); c.set(x - 1, y, z, "48"); c.set(x, y, z - 1, "1")
        c.set(x, y + 1, z, "48" if x % 2 else "1")
    c.prop("wheelbarrow", 9, 0, 27, 0)
    c.cover([(0, 0), (32, 0), (32, 14), (0, 14)], coverage=0.35, fernShare=0.3, flowerShare=0.02)
    c.cover([(0, 14), (32, 14), (32, 32), (0, 32)], coverage=0.25, fernShare=0.3, deadBushShare=0.2)
    return c
