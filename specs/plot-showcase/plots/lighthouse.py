"""Lighthouse Point as a 32 x 32 plot: a red-and-white lighthouse on a terraced rocky headland, a keeper's cottage
on its own knoll, a curving cove with a plank pier, a rowboat, buoys and nets, and a smugglers' cave cut away
under the south-west."""
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


LX, LZ = 9, 8            # lighthouse centre
RED, WHITE = "35:14", "35:0"
MOUNDS = [(LX, LZ, 9.5, 1), (LX, LZ, 7.5, 2), (LX, LZ, 5.8, 3), (24, 6, 5.5, 2),     # (cx, cz, radius, courses)
          (29, 1, 3.2, 3), (2, 2, 5.5, 3), (2, 2, 4.0, 4), (1, 1, 2.5, 5), (29, 10, 3.0, 2)]
COVE = [((17, 20), 2.4), ((22, 18), 3.2), ((24, 19), 3.6), ((26, 22), 3.2), ((25, 25), 2.8), ((22, 27), 1.8)]


def ground_top(x, z):
    """Top course of the ground over a cell, over the headland and cottage steps."""
    top = -1
    for cx, cz, radius, height in MOUNDS:
        if math.hypot(x - cx, z - cz) <= radius:
            top = max(top, height - 1)
    return top


def cove_cells():
    """Cells of the curving cove: within a half-width of the centre line, the width easing between its points."""
    cells = set()
    for x in range(0, 32):
        for z in range(0, 32):
            for ((x0, z0), w0), ((x1, z1), w1) in zip(COVE, COVE[1:]):
                dx, dz = x1 - x0, z1 - z0
                t = max(0.0, min(1.0, ((x - x0) * dx + (z - z0) * dz) / (dx * dx + dz * dz)))
                if math.hypot(x - (x0 + t * dx), z - (z0 + t * dz)) <= w0 + (w1 - w0) * t:
                    cells.add((x, z))
                    break
    return cells


def body(c, rng):
    """The striped tower in tower-relative cells: stone foundation, three sections, gallery, lantern room, cap."""
    c.disc(0, 0, 4.6, 2, "98:2")
    c.disc(0, 0, 4.3, 3, "98:0")
    for y in range(4, 22):
        radius = 3.4 if y <= 10 else 2.9 if y <= 16 else 2.5
        stripe = RED if ((y - 4) // 3) % 2 == 0 else WHITE
        c.disc(0, 0, radius, y, stripe, ring=1.0)
    for y in (11, 17):                                    # ledges where the tower steps in
        c.disc(0, 0, 3.4 if y == 11 else 2.9, y, "98:0", ring=1.0)
    c.set(0, 4, 3, "64:3"); c.set(0, 5, 3, "64:11")
    c.set(-1, 4, 3, "98:3"); c.set(1, 4, 3, "98:3"); c.set(0, 6, 3, "98:3")
    c.set(0, 3, 4, "109:3"); c.set(-1, 3, 4, "44:5"); c.set(1, 3, 4, "44:5")
    for y, (dx, dz) in ((8, (0, -3)), (8, (3, 0)), (13, (-3, 0)), (13, (0, 3)), (18, (0, -2)), (18, (2, 0)),
                        (19, (-2, 0))):
        c.set(dx, y, dz, "102"); c.set(dx, y + 1, dz, "102")
    c.set(-3, 7, 0, "102"); c.set(-3, 8, 0, "102")
    for y in range(4, 25):                                # the ladder inside
        c.set(0, y, -2, "98:0"); c.set(0, y, -1, "65:3")
    c.disc(0, 0, 3.6, 22, "98:2", ring=1.4)               # gallery, its rail, and the stone under it
    c.disc(0, 0, 4.2, 23, "98:0")
    c.disc(0, 0, 4.2, 24, "85", ring=0.8)
    c.set(0, 23, -1, None); c.set(0, 23, -1, "65:3")
    for y in (24, 25, 26):                                # lantern room
        c.disc(0, 0, 2.5, y, "20", ring=1.0)
        c.set(0, y, -1, "65:3") if y < 26 else None
    for dx, dz in ((2, 0), (-2, 0), (0, -2), (0, 2)):     # mullion posts, a door to the gallery
        for y in (24, 25, 26):
            c.set(dx, y, dz, "98:3" if y == 26 else "101")
    c.set(0, 24, -2, "98:0"); c.set(0, 25, -2, "98:0")
    c.set(0, 24, 2, None); c.set(0, 25, 2, None)
    c.set(0, 24, 0, "89"); c.set(0, 25, 0, "169"); c.set(0, 26, 0, "89")
    for y, radius in ((27, 3.6), (28, 2.8), (29, 1.9)):   # cap
        c.disc(0, 0, radius, y, "159:14")
    c.disc(0, 0, 0.8, 30, "159:14")
    c.set(0, 31, 0, "101")
    c.set(2, 4, 5, "85"); c.set(2, 5, 5, "85"); c.set(2, 6, 5, "89")      # lanterns by the door
    c.set(-2, 4, 5, "85"); c.set(-2, 5, 5, "85"); c.set(-2, 6, 5, "89")


def cottage(c, rng, x0, z0):
    """The keeper's cottage: whitewash on a stone footing, a red stair roof, a chimney and a lit window; seven
    wide, five deep, its ridge along x."""
    x1, z1, zc = x0 + 6, z0 + 4, z0 + 2
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
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            c.set(x, 0, z, "5:1")
    c.set(x0, 1, zc, "64:0"); c.set(x0, 2, zc, "64:8"); c.set(x0, 3, zc, WHITE)
    for x, z in ((x0 + 2, z0), (x0 + 4, z0), (x0 + 2, z1), (x0 + 4, z1), (x1, zc), (x0 + 1, z1)):
        c.set(x, 2, z, "102"); c.set(x, 3, z, "102")
    for x in range(x0 - 1, x1 + 2):                       # roof along x
        c.set(x, 4, z0 - 1, "108:2"); c.set(x, 5, z0, "108:2"); c.set(x, 6, z0 + 1, "108:2")
        c.set(x, 4, z1 + 1, "108:3"); c.set(x, 5, z1, "108:3"); c.set(x, 6, z1 - 1, "108:3")
        c.set(x, 7, zc, "44:4"); c.set(x, 6, zc, "4")
        if x0 <= x <= x1:
            c.set(x, 4, z0, WHITE); c.set(x, 4, z1, WHITE)
    for x in (x0, x1):
        for z in range(z0 + 1, z1):
            c.set(x, 4, z, WHITE); c.set(x, 5, z, WHITE)
    for dy in range(2, 10):                               # the chimney over the stove
        c.set(x1 - 1, dy, z1 - 1, "98:0")
    c.set(x1 - 1, 10, z1 - 1, "44:0")
    c.set(x1 - 1, 1, z0 + 1, "26:0"); c.set(x1 - 1, 1, z0 + 2, "26:8")
    c.set(x0 + 1, 1, z0 + 1, "54:3"); c.set(x0 + 2, 1, z1 - 1, "58"); c.set(x1 - 1, 1, z1 - 1, "61:2")
    c.set(x0 + 3, 3, zc, "89")
    c.set(x0 - 2, 1, z0 + 1, "85"); c.set(x0 - 2, 2, z0 + 1, "85"); c.set(x0 - 2, 3, z0 + 1, "89")   # porch
    c.set(x0 - 1, 1, z1, "126:1"); c.set(x0 - 1, 1, z1 + 1, "126:1")


def cove(c, rng, water):
    """The cove: lowered ground, water, a stone and sand shore, a pier with a T head, a boat and buoys."""
    for z in range(32):
        row = [x for x in range(32) if (x, z) in water]
        if not row:
            continue
        start = previous = row[0]
        for x in row[1:] + [None]:
            if x != previous + 1 if x is not None else True:
                c.lower(start, z, previous, z, -3)
                start = x
            previous = x if x is not None else previous
    for x, z in water:
        for y in (-3, -2, -1):
            c.set(x, y, z, "9")
    for x, z in list(water):                              # shore ring: stone below the surface, sand above
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                nx, nz = x + dx, z + dz
                if (nx, nz) in water or not (0 <= nx < 32 and 0 <= nz < 32) or ground_top(nx, nz) > -1:
                    continue
                c.set(nx, -1, nz, "12" if rng.random() < .7 else "13")
    # the pier along row 19: deck flush with the ground, posts into the water, a T head
    row = [x for x in range(32) if (x, 19) in water]
    head = row[0] + 7
    for x in range(row[0] - 3, head + 1):
        c.set(x, -1, 19, "5:1" if x % 2 else "126:9")
    for z in (18, 20):
        c.set(head, -1, z, "5:1")
    for x in range(row[0], head + 1, 2):
        for y in (-3, -2):
            c.set(x, y, 19, "17:1")
    for z in (18, 20):
        for y in (-3, -2):
            c.set(head, y, z, "17:1")
        c.set(head, 0, z, "85"); c.set(head, 1, z, "85"); c.set(head, 2, z, "50:5")
    c.set(row[0] + 1, 0, 18, "54:3"); c.set(row[0], 0, 18, "170:0")        # crates and a barrel on the pier
    c.set(row[0] + 4, 0, 20, "118:0")
    slips = [(bx, bz) for bx in range(2, 28) for bz in range(22, 30)
             if all((bx + dx, bz + dz) in water for dx in range(0, 5) for dz in range(-1, 2))]
    if slips:                                              # the rowboat lies in the water nearest the pier head
        bx, bz = min(slips, key=lambda slip: math.hypot(slip[0] - (head - 3), slip[1] - 24))
        c.prop("rowboat", bx, -1, bz, 0)
    for x, z in ((head + 2, 17), (head - 2, 22), (head + 1, 22), (head - 1, 16)):
        if (x, z) in water:
            c.set(x, -1, z, "35:14"); c.set(x, 0, z, "35:0")


def path(c, rng, points, width=2):
    """Gravel and flagstones along a poly-line, flush with the ground wherever it runs."""
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        steps = max(abs(x1 - x0), abs(z1 - z0))
        for step in range(steps + 1):
            x = round(x0 + (x1 - x0) * step / steps)
            z = round(z0 + (z1 - z0) * step / steps)
            for dz in range(width):
                top = ground_top(x, z + dz)
                if (x, top, z + dz) not in c.blocks and (x, top + 1, z + dz) not in c.blocks:
                    c.set(x, top, z + dz, rng.choice(("13", "98:2", "13", "48")))


def yard(c, rng):
    """Nets, pots, rope and driftwood on the flat south of the headland, by the pier landing."""
    for z in (23, 27):                                    # nets drying on a pole frame
        for y in range(1, 4):
            c.set(11, y, z, "85")
    for z in range(23, 28):
        c.set(11, 3, z, "85")
        c.set(11, 2, z, "30") if z in (24, 25, 26) else None
    c.set(11, 1, 25, "30")
    c.set(13, 0, 23, "118:0"); c.set(13, 0, 24, "118:0")                   # lobster pots
    c.set(13, 0, 28, "171:12"); c.set(14, 0, 28, "171:12"); c.set(13, 0, 29, "171:12")    # rope coils
    c.set(15, 0, 28, "145:0")
    c.set(10, 0, 21, "17:5"); c.set(9, 0, 21, "17:5"); c.set(8, 0, 22, "17:1")            # driftwood


def rocks(c):
    """Hand-heaped rock piles on the headland terraces and the cottage knoll: cobble, mossy cobble and stone."""
    for x, z in ((3, 11), (15, 12), (4, 3), (13, 3), (20, 10), (27, 11), (5, 8)):
        y = ground_top(x, z) + 1
        c.set(x, y, z, "48"); c.set(x + 1, y, z, "4"); c.set(x, y, z + 1, "1")
        c.set(x, y + 1, z, "4" if (x + z) % 2 else "48"); c.set(x - 1, y, z, "44:3")
        c.set(x + 1, y + 1, z, "44:3") if (x + z) % 3 == 0 else None


def shore_paint(c, rng, water):
    """Turf, gravel and coarse dirt in blobs over the rock, so neither the headland nor the flats are one grey."""
    blobs = [(rng.uniform(0, 32), rng.uniform(0, 32), rng.uniform(2.2, 4.2), rng.choice(("2", "2", "13", "3:1")))
             for _ in range(18)]
    blobs += [(24, 6, 4.5, "2"), (14, 26, 3.5, "13"), (6, 22, 3, "2")]
    for x in range(0, 32):
        for z in range(0, 32):
            top = ground_top(x, z)
            if (x, z) in water or (x, top, z) in c.blocks or (x, top + 1, z) in c.blocks:
                continue
            if math.hypot(x - LX, z - LZ) < 4.8 or (x <= 9 and 19 <= z <= 28):
                continue
            inside = top >= 0
            for bx, bz, radius, block in blobs:
                if math.hypot(x - bx, z - bz) <= radius * (0.7 + 0.3 * rng.random()) or (inside and rng.random() < .3):
                    c.set(x, top, z, block if inside or block != "13" else "13")
                    break


def smugglers_cave(c, rng):
    """A cave under the south-west corner: a hidden cache, a lantern and a stretch of tide (cave coordinates)."""
    width, depth = 8, 16
    c.lower(0, 9, width, depth, -7)
    c.roof(0, 9, width, depth, -2, 0)
    floor = -8
    for x in range(0, width + 1):
        for z in range(9, depth + 1):
            c.set(x, floor, z, "13" if rng.random() < .5 else "12")
    for y in range(-7, -2):
        for z in range(9, depth + 1):
            if rng.random() < .3:
                c.set(width + 1, y, z, rng.choice(("16", "15", "1:5", "4", "14")))
    for z in (9, depth):
        for y in range(-7, -2):
            c.set(0, y, z, "17:1")
    for z in range(9, depth + 1):
        c.set(0, -3, z, "17:9")
        c.set(4, -3, z, "17:9")
    for y in range(-7, -3):
        c.set(4, y, 9, "17:1"); c.set(4, y, depth, "17:1")
    c.set(1, -7, 10, "54:3"); c.set(2, -7, 10, "54:3")
    c.set(1, -7, 15, "118:3"); c.set(2, -7, 15, "170:0"); c.set(2, -6, 15, "170:0")
    c.set(5, -7, 10, "145:0"); c.set(7, -7, 11, "46"); c.set(7, -7, 12, "46"); c.set(7, -6, 11, "46")
    c.set(8, -7, 13, "89"); c.set(8, -6, 15, "89")
    c.set(3, -7, 11, "144:1"); c.set(0, -7, 12, "144:1")
    c.set(8, -3, 15, "30"); c.set(0, -3, 10, "30"); c.set(5, -3, 9, "30")
    for x, z in ((4, 13), (5, 13), (4, 14), (5, 14), (6, 14), (3, 13)):
        c.set(x, -8, z, "9"); c.set(x, -7, z, "9") if (x + z) % 2 else None
    c.set(1, -4, 13, "85"); c.set(1, -5, 13, "85"); c.set(1, -6, 13, "89")


def build():
    c = Chunk("lighthouse", "Lighthouse Point", "rock",
              "A red-and-white lighthouse on a terraced headland, a keeper's cottage on its own knoll, and a "
              "curving cove with a pier, rowboat, nets and buoys above a cut-away smugglers' cave.", size=32)
    rng = random.Random(41)
    for cx, cz, radius, height in MOUNDS:
        c.mound(cx, cz, radius, height)
    water = cove_cells()
    cove(c, rng, water)
    body(At(c, LX, LZ), rng)
    cottage(At(c, 0, 0, 2), rng, 21, 4)
    yard(c, rng)
    shore_paint(c, rng, water)
    rocks(c)
    smugglers_cave(At(c, 0, 11), rng)
    path(c, rng, [(16, 0), (16, 5), (13, 10), (11, 12)])
    path(c, rng, [(0, 16), (6, 16), (9, 13)])
    path(c, rng, [(31, 16), (26, 14), (21, 13), (15, 13)])
    path(c, rng, [(16, 30), (16, 26), (13, 22), (11, 19)])
    c.cover([(0, 0), (32, 0), (32, 18), (0, 18)], coverage=0.15, fernShare=0.3, deadBushShare=0.2)
    return c
