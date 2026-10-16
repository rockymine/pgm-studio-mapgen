"""The three crossings of the Thaw, built as red's half (z up to -1) of a mirrored board: the other half is their image.

    Frostspan        x -42..-39 over the water: stone brick under quartz kerbs, ice hung from the soffit
    the Cinder Span  x -3..3 over the stone bar: a nether-brick viaduct whose centre pier is pierced, so the bar runs through it
    Brimstone Bridge x 39..42 over the lava: nether brick and chains of fence, braziers at the ends

Each deck is carried on one arch from the rim to a pier standing in the river.
"""
import math

import land
import plan as P
from pgmvox import B
from util import pick, stairs

PIER_Z = (-2, -1)
REACH = (-14, -1)


def thick(t, depth):
    """Solid under the deck at a fraction t (0 abutment to 1 pier) of the arch: deep at the ends, a block at the crown."""
    return 1 + int(round(depth * (1 - math.sin(math.pi * min(max(t, 0), 1)) ** 0.8)))


def span(w, rng, xc, half, deck, style, apron=8):
    cols = range(xc - half, xc + half + 1)
    z0, z1 = REACH[0], PIER_Z[0] - 1
    for z in range(z0 - apron, PIER_Z[1] + 1):
        over = z >= z0
        t = (z - z0) / (z1 - z0)
        for x in cols:
            edge = x in (xc - half, xc + half)
            g = P.g(x, z)
            if not over:                                           # the apron: ground brought to the deck
                for yy in range(min(g, deck) - 1, deck):
                    w.set(x, yy, z, *style["under"])
                for yy in range(deck + 1, max(g, deck) + 4):
                    w.set(x, yy, z, B.AIR)
                w.set(x, deck, z, *(style["edge"] if edge else pick(rng, style["deck"])))
                continue
            th = thick(t, style["depth"]) if z <= z1 else 4
            for yy in range(deck - th, deck):
                w.set(x, yy, z, *style["under"])
            w.set(x, deck, z, *(style["edge"] if edge else pick(rng, style["deck"])))
            for yy in range(deck + 1, deck + 5):
                w.set(x, yy, z, B.AIR)
    # the pier: from the river's floor up under the deck
    for z in PIER_Z:
        for x in cols:
            floor = P.g(x, z)
            for yy in range(floor, deck):
                w.set(x, yy, z, *style["pier"])
    # rails and lamps
    for z in range(z0 - apron // 2, PIER_Z[1] + 1):
        for x in (xc - half, xc + half):
            w.set(x, deck + 1, z, *style["rail"])
            if (z - z0) % 6 == 0:
                for k in range(2, 4):
                    w.set(x, deck + k, z, *style["post"])
                w.set(x, deck + 4, z, *style["light"])
    return deck


def frostspan(w, rng):
    style = dict(deck=[((B.STONEBRICK, 0), 5), ((B.STONE, 6), 3), ((B.STONEBRICK, 2), 2)], edge=(B.QUARTZ, 0),
                 under=(B.STONEBRICK, 0), pier=(B.STONEBRICK, 0), rail=(B.COBBLE_WALL, 0), post=(B.SPRUCE_FENCE, 0),
                 light=(B.SEA_LANTERN, 0), depth=4)
    xc, half, deck = -41, 2, 65
    span(w, rng, xc, half, deck, style)
    for x in range(xc - half, xc + half + 1):                      # icicles from the soffit, longest toward the crown
        for z in range(REACH[0] + 1, PIER_Z[0]):
            if rng.random() < 0.16:
                t = (z - REACH[0]) / (PIER_Z[0] - 1 - REACH[0])
                th = thick(t, 4)
                for j in range(int(rng.integers(1, 4))):
                    w.set(x, deck - th - j, z, B.ICE if j == 0 else B.PACKED_ICE)
    for x in (xc - half - 1, xc + half + 1):                       # a buttress at the abutment either side
        for z in (REACH[0] - 1, REACH[0]):
            for yy in range(P.g(x, z) - 1, deck + 2):
                w.set(x, yy, z, B.STONEBRICK, 0)


def cinder(w, rng):
    style = dict(deck=[((B.NETHER_BRICK, 0), 5), ((B.STONEBRICK, 0), 2), ((B.STONE, 6), 2)], edge=(B.RED_SANDSTONE, 2),
                 under=(B.NETHER_BRICK, 0), pier=(B.NETHER_BRICK, 0), rail=(B.NETHER_FENCE, 0), post=(B.NETHER_FENCE, 0),
                 light=(B.GLOWSTONE, 0), depth=5)
    xc, half, deck = 0, 3, 64
    span(w, rng, xc, half, deck, style)
    for z in PIER_Z:                                               # the bar runs through the pier: a vaulted opening
        for x in range(-1, 2):
            for yy in range(50, 58):
                w.set(x, yy, z, B.AIR)
        for yy in range(50, 58):
            for x in (-2, 2):
                w.set(x, yy, z, B.NETHER_BRICK, 0)
        for x in (-1, 0, 1):
            w.set(x, 58, z, B.AIR)
        w.set(-1, 57, z, *stairs(B.NETHER_STAIRS, (1, 0), True))
        w.set(1, 57, z, *stairs(B.NETHER_STAIRS, (-1, 0), True))
        w.set(0, 57, z, B.NETHER_BRICK, 0)
    for yy in range(49, 51):
        for z in (-4, -3):
            for x in (-3, 3):
                w.set(x, yy, z, B.NETHER_BRICK, 0)


def brimstone(w, rng):
    style = dict(deck=[((B.NETHER_BRICK, 0), 6), ((B.STAINED_CLAY, 15), 2), ((B.STONE, 6), 2)], edge=(B.NETHER_BRICK, 0),
                 under=(B.NETHER_BRICK, 0), pier=(B.NETHER_BRICK, 0), rail=(B.NETHER_FENCE, 0), post=(B.NETHER_FENCE, 0),
                 light=(B.GLOWSTONE, 0), depth=4)
    xc, half, deck = 40, 2, 64
    span(w, rng, xc, half, deck, style)
    for x in range(xc - half + 1, xc + half, 1):                  # chains of fence hung under the arch, a glow at each foot
        for z in (-12, -9, -6, -4):
            t = (z - REACH[0]) / (PIER_Z[0] - 1 - REACH[0])
            th = thick(t, 4)
            if x in (xc - 1, xc + 1) or z == -9:
                n = int(rng.integers(2, 5))
                for j in range(n):
                    w.set(x, deck - th - j, z, B.NETHER_FENCE)
                w.set(x, deck - th - n, z, B.GLOWSTONE)
    for x in (xc - half - 1, xc + half + 1):
        base = P.g(x, REACH[0] - 2)
        for yy in range(base, base + 3):
            w.set(x, yy, REACH[0] - 1, B.NETHER_BRICK, 0)
        w.set(x, base + 3, REACH[0] - 1, B.NETHERRACK)
        w.set(x, base + 4, REACH[0] - 1, B.FIRE)


def build(w, rng, stats):
    frostspan(w, rng)
    cinder(w, rng)
    brimstone(w, rng)
