"""What was built on Rimeburn, laid in Frost's half (and the Thaw, which is symmetric by itself) before the half
turn carries it to Ember's and season.py re-seasons it.

    the Hold          the spawn's longhouse: stone-brick foot, spruce walls on spruce posts, a dark roof; its yard
    the Hearth        the core's hearthstone and its fire ring on the hollow floor, braziers round the rim
    the Shrine        the Icestone's dais on the Rime Shelf, four spires of packed ice at its corners
    Rimecroft         a long house, a byre and a smithy with its forge, in the Hold's style; a woodpile
    the bridges       two timber bridges over the burn, on stone abutments
    the Thaw deck     a deck on four legs over the island in the seam, the meeting fire on it
    the Vent          a passage from the coast's cliff to the hollow, lit
    the steps         stone-brick stairs on every rise of a ramp
"""
import math

import numpy as np

import land as LD
import plan as P
from pgmvox import B
from pgmvox.built import build as BLD
from pgmvox.core import orient as O
from pgmvox.volume import under

FROST_STYLE = dict(ground=[(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 0)], upper=[(B.PLANKS, 1)], post=1,
                   gable=(B.PLANKS, 1), floor=(B.PLANKS, 1), roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS,
                   slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR, window=(B.PANE, 0), chimney=(B.STONEBRICK, 0),
                   chimney_cap=(B.COBBLE_WALL, 0))
FLOOR_SET = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]


def cellset(x, z, blocks, seed=0, cell=3):
    """A built floor: four blocks of one tone, a quarter each, laid in cells about `cell` across."""
    cx, cz = (x + 1000) // cell, (z + 1000) // cell
    h = (cx * 73856093 ^ cz * 19349663 ^ seed * 83492791) & 0xffff
    return blocks[h % len(blocks)]


def is_north(z):
    return z < 0


# ---- the Hold -------------------------------------------------------------------------------------------------
def hold(w, H):
    cx, cz, heading, L, W, floor, storeys, door = P.BUILDINGS["the Hold"]
    yard_cells = []
    sx, sz = LD.SPAWN
    for x in range(sx - 9, sx + 10):                 # the yard, the spawn's floor, before the hall
        for z in range(sz - 6, sz + 6):
            if abs(x - sx) + max(0, z - sz - 3) * 1.5 > 10.5:
                continue
            w.set(x, LD.TERRACE, z, *cellset(x, z, FLOOR_SET, 1))
            w.set(x, LD.TERRACE + 1, z, B.AIR)
            yard_cells.append((x, z))
    for x in range(sx - 1, sx + 2):                  # the walk from the yard to the hall's door
        for z in range(-85, sz - 5):
            w.set(x, LD.TERRACE, z, *cellset(x, z, FLOOR_SET, 1))
            w.set(x, LD.TERRACE + 1, z, B.AIR)
    out = BLD.house(w, BLD.House(cx, cz, heading, L=L, W=W, floor=floor, storeys=storeys, style=FROST_STYLE,
                                 door=door, chimney=True, roof="gable", pitch=1, overhang=1),
                    ground_at=lambda x, z: int(H[x - LD.X0, z - LD.Z0]))
    for dx in (-7, 7):                               # braziers at the yard's front corners
        brazier(w, sx + dx, LD.TERRACE, sz + 2)
    return out


def brazier(w, x, y, z, height=2):
    """A fire kept on a stone post: a stone-brick wall post, netherrack on it, and the fire burning on the rack."""
    for k in range(1, height):
        w.set(x, y + k, z, B.COBBLE_WALL, 0)
    w.set(x, y + height, z, B.NETHERRACK, 0)
    w.set(x, y + height + 1, z, B.FIRE, 0)


# ---- the Hearth -----------------------------------------------------------------------------------------------
def hearth(w, H):
    cx, cz = LD.HEARTH
    f = LD.HOLLOW_FLOOR
    for dx in range(-4, 5):                          # the hearthstone, round, under the core
        for dz in range(-4, 5):
            r = math.hypot(dx, dz)
            if r > 4.6:
                continue
            x, z = cx + dx, cz + dz
            blk = (B.STONEBRICK, 0) if r > 3.6 else (B.STONE, 6) if r > 2.2 else (B.NETHER_BRICK, 0)
            w.set(x, f, z, *blk)
            w.set(x, f + 1, z, B.AIR)
    for dx, dz in ((-5, 0), (5, 0), (0, -5), (0, 5)):   # four fires at the hearthstone's ends
        x, z = cx + dx, cz + dz
        w.set(x, f, z, B.NETHERRACK, 0)
        w.set(x, f + 1, z, B.FIRE, 0)
    for k in range(7):                               # braziers round the hollow's rim, the side to the front open
        a = math.radians(-30 + k * 40)
        x, z = int(round(cx + 13.5 * math.cos(a))), int(round(cz - 13.5 * math.sin(a)))
        y = int(H[x - LD.X0, z - LD.Z0])
        brazier(w, x, y, z, 3)


# ---- the Shrine -----------------------------------------------------------------------------------------------
def shrine(w, rng):
    cx, cz = LD.SHELF
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            x, z = cx + dx, cz + dz
            edge = max(abs(dx), abs(dz)) == 4
            w.set(x, P.DAIS, z, *((B.STONEBRICK, 0) if edge else (B.QUARTZ, 0) if max(abs(dx), abs(dz)) <= 1
                                  else (B.STONE, 6)))
            for y in range(P.DAIS + 1, P.DAIS + 4):
                w.set(x, y, z, B.AIR)
            if edge and (dx + dz) % 2 == 0 and abs(dx) != abs(dz):
                w.set(x, P.DAIS + 1, z, B.SLAB, 5)
    for dx, dz in ((-5, -5), (5, -5), (-5, 5), (5, 5)):
        spire(w, cx + dx, P.DAIS, cz + dz, int(rng.integers(8, 12)), rng)


def spire(w, x, y, z, height, rng):
    """A spire of packed ice standing on the floor at y: a 3 by 3 foot, a cross above it, a single needle on top."""
    for k in range(1, height + 1):
        t = k / height
        r = 1.5 if t < 0.35 else 1.0 if t < 0.7 else 0.0
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if math.hypot(dx, dz) <= r + 0.01 or (dx == 0 and dz == 0):
                    w.set(x + dx, y + k, z + dz, B.PACKED_ICE, 0)
    w.set(x, y + height + 1, z, B.PACKED_ICE, 0)


# ---- Rimecroft ------------------------------------------------------------------------------------------------
def hamlet(w, H, rng):
    doors = {}
    for name in P.BUILDINGS:
        if not name.startswith("Rimecroft"):
            continue
        cx, cz, heading, L, W, floor, storeys, door = P.BUILDINGS[name]
        out = BLD.house(w, BLD.House(cx, cz, heading, L=L, W=W, floor=floor, storeys=storeys, style=FROST_STYLE,
                                     door=door, chimney=name.endswith("smithy"), roof="gable", pitch=1, overhang=1),
                        ground_at=lambda x, z: int(H[x - LD.X0, z - LD.Z0]))
        doors[name] = out["door"]
    # the smithy's forge, against its east gable outside: a stone hearth with its fire, an anvil, a water trough
    cx, cz = P.BUILDINGS["Rimecroft: the smithy"][:2]
    fx, fz, f = int(cx) + 5, int(cz), LD.HAMLET_FLOOR
    for dz in (-1, 0, 1):
        w.set(fx, f + 1, fz + dz, B.STONEBRICK, 0)
    w.set(fx, f + 1, fz, B.NETHERRACK, 0)
    w.set(fx, f + 2, fz, B.FIRE, 0)
    w.set(fx, f + 2, fz - 1, B.STONEBRICK_STAIRS, O.stair("e", True))
    w.set(fx, f + 2, fz + 1, B.STONEBRICK_STAIRS, O.stair("e", True))
    w.set(fx - 1, f + 1, fz + 2, B.ANVIL, 0)
    w.set(fx, f + 1, fz + 3, B.CAULDRON, 3)
    # the woodpile by the byre: spruce logs laid along x, two courses, a slab roof
    bx, bz = int(P.BUILDINGS["Rimecroft: the byre"][0]) - 1, int(P.BUILDINGS["Rimecroft: the byre"][1]) + 6
    for dx in range(4):
        for dy in (1, 2):
            w.set(bx + dx, f + dy, bz, B.LOG, 1 | 4)
        w.set(bx + dx, f + 3, bz, B.WOOD_SLAB, 1)
    return doors


# ---- the bridges ----------------------------------------------------------------------------------------------
def bridges(w, H, water):
    """A timber bridge where each path crosses the burn: a deck a block over the banks, spruce fence rails, stone
    abutments at its ends. Found from the path and the water rather than placed by hand."""
    made = []
    for name in ("Hold to the Hearth", "Hold to the front"):
        pts = P.PATHS[name]
        crossing = None
        for (ax, az), (bx, bz) in zip(pts, pts[1:]):
            n = int(math.hypot(bx - ax, bz - az) * 2)
            for t in np.linspace(0, 1, n):
                x, z = int(round(ax + (bx - ax) * t)), int(round(az + (bz - az) * t))
                if water[x - LD.X0, z - LD.Z0]:
                    crossing = (x, z, (bx - ax, bz - az))
                    break
            if crossing:
                break
        if not crossing:
            continue
        x, z, (dx, dz) = crossing
        along_x = abs(dx) >= abs(dz)
        ux, uz = (1, 0) if along_x else (0, 1)
        px, pz = -uz, ux
        bank = []
        for s in range(-6, 7):
            cx, cz = x + ux * s, z + uz * s
            bank.append((s, int(H[cx - LD.X0, cz - LD.Z0]), bool(water[cx - LD.X0, cz - LD.Z0])))
        wet = [s for s, h, wt in bank if wt]
        lo, hi = min(wet) - 2, max(wet) + 2
        deck = max(h for s, h, wt in bank if not wt and lo <= s <= hi) + 1
        for s in range(lo, hi + 1):
            for wdt in (-1, 0, 1):
                cx, cz = x + ux * s + px * wdt, z + uz * s + pz * wdt
                end = s in (lo, hi)
                w.set(cx, deck, cz, *((B.STONEBRICK, 0) if end else (B.PLANKS, 1)))
                for y in range(deck + 1, deck + 3):
                    w.set(cx, y, cz, B.AIR)
                if end:
                    g = int(H[cx - LD.X0, cz - LD.Z0])
                    for y in range(g, deck):
                        w.set(cx, y, cz, B.STONEBRICK, 0)
            for wdt in (-2, 2):
                cx, cz = x + ux * s + px * wdt, z + uz * s + pz * wdt
                w.set(cx, deck, cz, B.LOG, 1 | (4 if along_x else 8))
                w.set(cx, deck + 1, cz, B.SPRUCE_FENCE, 0)
        # the steps up onto it at each end
        for s, step_dir in ((lo - 1, 1), (hi + 1, -1)):
            for wdt in (-1, 0, 1):
                cx, cz = x + ux * s + px * wdt, z + uz * s + pz * wdt
                g = int(H[cx - LD.X0, cz - LD.Z0])
                if deck - g >= 2:
                    rises = "e" if (along_x and step_dir > 0) else "w" if along_x else "s" if step_dir > 0 else "n"
                    w.set(cx, deck, cz, B.SPRUCE_STAIRS, O.stair(rises))
        made.append((x, z, deck, lo, hi, along_x))
    return made


# ---- the Thaw deck --------------------------------------------------------------------------------------------
def thaw_deck(w, H):
    x0, z0, x1, z1, f = P.THAW_DECK
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            rim = x in (x0, x1) or z in (z0, z1)
            w.set(x, f, z, *((B.STONEBRICK, 0) if rim else (B.PLANKS, 1)))
            if rim and not ((x in (x0, x1)) and (z in (z0, z1))) and (x + z) % 3 != 0:
                w.set(x, f + 1, z, B.SPRUCE_FENCE, 0)
    for lx, lz in ((x0, z0), (x1, z1), (x0, z1), (x1, z0)):     # four legs, two by two, down to the ground
        for dx in (0, 1 if lx == x0 else -1):
            for dz in (0, 1 if lz == z0 else -1):
                x, z = lx + dx, lz + dz
                g = int(H[x - LD.X0, z - LD.Z0])
                for y in range(g + 1, f):
                    w.set(x, y, z, B.STONEBRICK, 0)
        w.set(lx, f + 1, lz, B.COBBLE_WALL, 0)
        w.set(lx, f + 2, lz, B.SEA_LANTERN, 0)
    # a ladder up the north face of the north-west and north-east legs (and so the south ones, in the image)
    for lx in (x0 + 1, x1 - 1):
        g = int(H[lx - LD.X0, z0 - 1 - LD.Z0])
        for y in range(g + 1, f + 1):
            w.set(lx, y, z0 - 1, B.LADDER, O.ladder("s"))
        w.set(lx, f + 1, z0, B.AIR)
    # the meeting fire in the middle, in a ring of nether brick
    for x in range(-2, 2):
        for z in range(-2, 2):
            ring = x in (-2, 1) or z in (-2, 1)
            w.set(x, f, z, *((B.NETHER_BRICK, 0) if ring else (B.NETHERRACK, 0)))
            if not ring:
                w.set(x, f + 1, z, B.FIRE, 0)


# ---- the Vent -------------------------------------------------------------------------------------------------
def vent(w, H, rng):
    n, floor = under.tunnel(w, [(x, y, z, 2.0) for x, y, z in LD.VENT], ground=H, cover=1)
    from pgmvox.geom import shapes
    plan = [(x, z) for x, y, z in LD.VENT]
    for x in range(min(p[0] for p in plan) - 3, max(p[0] for p in plan) + 4):
        for z in range(min(p[1] for p in plan) - 3, max(p[1] for p in plan) + 4):
            if shapes.nearest_on(plan, x, z)[0] > 2.5:
                continue
            fy = floor(x, z)
            if w.id(x, fy, z) == B.AIR and w.id(x, fy - 1, z) != B.AIR:
                w.set(x, fy - 1, z, *[(B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0)][int(rng.integers(3))])
    for x, y, z in LD.VENT[1:-1]:                                  # a light in the roof at each bend
        for yy in range(y + 5, y, -1):
            if w.id(x, yy, z) != B.AIR and w.id(x, yy - 1, z) == B.AIR:
                w.set(x, yy, z, B.GLOWSTONE, 0)
                break
    return n


# ---- the March ------------------------------------------------------------------------------------------------
def march(w, H, rng):
    """The dyke: drystone two courses high on its own ground, a cap of slabs here and there, ends broken down."""
    stones = [(B.COBBLE, 0), (B.STONE, 5), (B.STONE, 0), (B.STONE, 5)]
    cells = P.march_cells()
    for x, z in cells:
        g = int(H[x - LD.X0, z - LD.Z0])
        near_gap = min(abs(x - gx) - wd / 2 for gx, wd in P.MARCH_GAPS)
        top = 1 if near_gap < 1.5 or x in (P.MARCH[0][0], P.MARCH[-1][0]) else 2
        for k in range(1, top + 1):
            w.set(x, g + k, z, *stones[int(rng.integers(len(stones)))])
        if top == 2 and rng.random() < 0.3:
            w.set(x, g + 3, z, B.SLAB, 3)


# ---- boulders and the jetty ----------------------------------------------------------------------------------------
# rock fallen where rock falls: under the Rimewall, round the Anvil's foot, one on the Tarn's east shore
BOULDERS = [(-31, -86, 2.2), (-37, -91, 1.6), (33, -90, 2.0), (-57, -47, 1.8), (-41, -47, 1.5), (32, -47, 1.7),
            (-3, -88, 1.5)]


def boulders(w, H, rng):
    rock = [(B.STONE, 0), (B.STONE, 5), (B.STONE, 5), (B.COBBLE, 0)]
    for bx, bz, r in BOULDERS:
        g = int(H[bx - LD.X0, bz - LD.Z0])
        R = int(math.ceil(r))
        for dx in range(-R, R + 1):
            for dz in range(-R, R + 1):
                d = math.hypot(dx, dz * 1.2) + rng.uniform(-0.3, 0.3)
                if d > r:
                    continue
                gg = int(H[bx + dx - LD.X0, bz + dz - LD.Z0])
                top = g + int(round((r - d) * 1.3)) + 1
                for y in range(min(gg, g), top + 1):
                    w.set(bx + dx, y, bz + dz, *rock[int(rng.integers(len(rock)))])
                if rng.random() < 0.7:
                    w.set(bx + dx, top + 1, bz + dz, B.SNOW_LAYER, 0)


def jetty(w, H):
    """A spruce jetty out over the Tarn from its north shore, on posts, and a hole cut in the ice at its end."""
    x0, z0 = 17, -49
    deck = LD.TARN_LEVEL + 1
    for z in range(z0, z0 + 6):
        for x in (x0, x0 + 1):
            w.set(x, deck, z, B.WOOD_SLAB, 1)
            w.set(x, deck + 1, z, B.AIR)
        if (z - z0) % 2 == 0:
            for x in (x0 - 1, x0 + 2):
                g = int(H[x - LD.X0, z - LD.Z0])
                for y in range(g + 1, deck + 1):
                    w.set(x, y, z, B.LOG, 1)
                w.set(x, deck + 1, z, B.SPRUCE_FENCE, 0)
    w.set(x0, LD.TARN_LEVEL, z0 + 6, B.WATER, 0)                  # the fishing hole in the ice


# ---- the Rime Falls -----------------------------------------------------------------------------------------------
def falls(w, H):
    """The burn's source: a notch two wide cut down the Rimewall's face from its crest to the burn's first pool, its
    floor lined in ice two deep, Frost's frozen fall. Returns the notch's cells, top first, for Ember's water."""
    fx, fz = LD.FALLS
    cells = []
    for z in range(-96, fz + 1):
        for x in (fx - 1, fx):
            i, k = x - LD.X0, z - LD.Z0
            g = int(H[i, k])
            if g <= LD.TERRACE:
                continue
            w.set(x, g, z, B.AIR)
            w.set(x, g + 1, z, B.AIR)
            w.set(x, g - 1, z, B.ICE, 0)
            w.set(x, g - 2, z, B.PACKED_ICE, 0)
            cells.append((x, g - 1, z))
    return cells


# ---- the steps ------------------------------------------------------------------------------------------------
def steps(w, H, ramps):
    """Every ramp cell with a neighbour one higher along the ramp takes a stone-brick stair rising to it."""
    for name, m in ramps.items():
        pts = LD.RAMPS[name][0]
        for i, k in np.argwhere(m):
            x, z = int(LD.X0 + i), int(LD.Z0 + k)
            if not is_north(z):
                continue
            h = int(H[i, k])
            for d, (dx, dz) in O.DIRS.items():
                a, b = i + dx, k + dz
                if 0 <= a < H.shape[0] and 0 <= b < H.shape[1] and m[a, b] and H[a, b] == h + 1:
                    w.set(x, h + 1, z, B.STONEBRICK_STAIRS, O.stair(d))
                    break
