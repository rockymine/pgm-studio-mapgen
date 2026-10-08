"""Below the ground (red half): Falls Cave, entered behind the waterfall, with its lake chamber, pillar hall,
grotto and alcoves; Ironhollow Mine from the adit by the spawn to the shaft and the breakthrough; the gaol
cellar whose south wall has fallen into the cave; the sinkhole's rubble.

The passages, chambers, cave finish, galleries and shaft are pgmvox.under's; what is local is where they go
(plan.py) and the pieces only this board has: the lake, the pillar hall, the grotto, the falls mouth, the
sinkhole's rubble, the adit portal and the gaol cellar.
"""
import math

import numpy as np

import plan as P
from pgmvox import B, rng
from pgmvox import under as U
from pgmvox.orient import ladder, torch

R_ = rng(P.BOARD, "under")


def ground_at(L, x, z):
    i, k = x - P.X_MIN, z - P.Z_MIN
    if 0 <= i < L.H.shape[0] and 0 <= k < L.H.shape[1] and L.land[i, k]:
        return int(L.H[i, k])
    return None


def red(x, y, z):
    """Held back from every carve and finish: the mirror line and blue's half, which the turn writes."""
    return x >= -1


def branch(w, L, pts):
    return U.tunnel(w, pts, ground=lambda x, z: ground_at(L, x, z), keep=red)[0]


def chamber(w, L, cx, fy, cz, rx, h):
    return U.chamber(w, cx, fy, cz, rx, h, ground=lambda x, z: ground_at(L, x, z), keep=red)


def lake(w):
    cx, cy, cz = P.LAKE
    for x in range(cx - 7, cx + 8):
        for z in range(cz - 7, cz + 8):
            d = math.hypot((x - cx) / 5.5, (z - cz - 1) / 4.2)
            if d < 1.0:
                depth = 2 if d < 0.6 else 1
                for y in range(cy - depth, cy):
                    w.set(x, y, z, B.WATER)
                w.set(x, cy - depth - 1, z, B.CLAY if d < 0.5 else B.GRAVEL)


def pillars(w):
    cx, cy, cz = -46, 34, 26
    r = np.random.default_rng(8)
    for _ in range(7):
        a, d = r.uniform(0, 2 * np.pi), r.uniform(2.5, 6.0)
        px, pz = int(round(cx + d * np.cos(a))), int(round(cz + d * 0.9 * np.sin(a)))
        for x in range(px, px + (2 if r.random() < 0.4 else 1)):
            for y in range(cy - 1, cy + 9):
                if w.id(x, y, pz) == B.AIR:
                    w.set(x, y, pz, B.STONE, 5 if (y + x) % 3 else 0)


def grotto(w):
    cx, cy, cz = -60, 33, 6
    w.chest(cx - 2, cy, cz, [(0, "minecraft:golden_apple", 2, 0), (1, "minecraft:arrow", 32, 0),
                             (4, "minecraft:iron_leggings", 1, 0), (13, "minecraft:paper", 3, 0)], facing=5)
    w.set(cx - 2, cy, cz + 1, B.WOOD_SLAB, 1)
    w.set(cx - 1, cy, cz - 2, B.PLANKS, 1)
    w.set(cx, cy, cz + 2, B.TORCH, torch())


def mouth(w):
    """A rock ledge in the rift face at the cave's mouth, beside the falling water, and vines over it."""
    for z in range(1, 10):
        for x in (-11, -10):
            if x == -10 and z < 4:
                continue
            w.set(x, 35, z, B.STONE, 5 if (x + z) % 3 else 0)
            if z >= 5:
                w.set(x, 34, z, B.STONE, 0)
            for y in range(36, 39):
                if w.id(x, y, z) not in (B.WATER, B.WATER_FLOW):
                    w.set(x, y, z, B.AIR)
    for z in range(-1, 6):
        for y in range(39, 42):
            if w.id(-11, y, z) == B.AIR and w.id(-12, y, z) not in (B.AIR, B.WATER, B.WATER_FLOW) and R_.random() < 0.5:
                w.set(-11, y, z, B.VINE, 2)                      # hung on the face to its west


def sinkhole(w, L):
    """The funnel is in the plan's heights; here its rubble, its grass lip and the air down into the cave."""
    (cx, cz), floor, rad = P.SINKHOLE
    for x in range(int(cx - rad) - 1, int(cx + rad) + 2):
        for z in range(int(cz - rad) - 1, int(cz + rad) + 2):
            d = math.hypot(x - cx, z - cz)
            g = ground_at(L, x, z)
            if g is None or d > rad or not L.sinkhole[x - P.X_MIN, z - P.Z_MIN]:
                continue
            r = R_.random()
            w.set(x, g, z, *((B.GRAVEL, 0) if r < 0.35 else (B.DIRT, 1) if r < 0.6 else (B.STONE, 5) if r < 0.8 else (B.COBBLE, 0)))
            if d > rad - 1.5:
                w.set(x, g, z, B.GRASS)
            if w.id(x, g - 1, z) in (B.AIR,):                   # a step over the cave: hold the gravel up
                w.set(x, g - 1, z, B.STONE, 5)


def mine(w, L):
    """The galleries (pgmvox.under.gallery: three wide, timber sets on the level, rails, stairs on the rises,
    iron in the walls), a timber portal at the adit and the foreman's chest at the breakthrough."""
    U.gallery(w, P.mine_line(), R_, floor=((B.GRAVEL, 0), (B.STONE, 0), (B.STONE, 5)))
    ax, ay, az = P.MINE[0]
    for dx in (-2, -1, 0, 1, 2):
        for dy in (0, 1, 2, 3):
            if dy == 3 or abs(dx) == 2:
                w.set(ax + dx, ay + dy, az - 1, B.LOG, 1 if dy < 3 else 5)
    for dx in (-1, 0, 1):
        for dy in (0, 1, 2):
            for dz in (-1, -2, -3):
                w.set(ax + dx, ay + dy, az + dz, B.AIR)
    bx, by, bz = P.MINE[-2]
    w.chest(bx + 1, by, bz + 1, [(0, "minecraft:iron_ingot", 6, 0), (1, "minecraft:bread", 8, 0),
                                 (4, "minecraft:torch", 16, 0), (13, "minecraft:iron_pickaxe", 1, 0)], facing=3)


def shaft(w, L):
    """The shaft from the gallery up to the headframe's collar: a ladder in a timber-lined well."""
    sx, sz = P.SHAFT
    g = ground_at(L, sx, sz)
    U.shaft(w, sx, sz, 45, g, ladder_on="s")
    return g


def cellar(w, L):
    """A vault of stone brick with three barred cells; its south wall fallen into the cave."""
    x0, fy, z0, x1, z1 = P.CELLAR
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(fy - 1, fy + 6):
                if x in (x0, x1) or z in (z0, z1) or y in (fy - 1, fy + 5):
                    r = R_.random()
                    w.set(x, y, z, B.STONEBRICK, 0 if r < 0.7 else (2 if r < 0.88 else 1))
                else:
                    w.set(x, y, z, B.AIR)
    for c in range(3):
        cx0 = x0 + 1 + c * 3
        for x in range(cx0, cx0 + 3):
            for y in (fy, fy + 1, fy + 2):
                w.set(x, y, z0 + 3, B.IRON_BARS)
        w.set(cx0 + 1, fy, z0 + 3, B.IRON_DOOR, 3)
        w.set(cx0 + 1, fy + 1, z0 + 3, B.IRON_DOOR, 8)
        if c < 2:
            for y in (fy, fy + 1, fy + 2):
                for z in range(z0 + 1, z0 + 3):
                    w.set(cx0 + 3, y, z, B.STONEBRICK, 0)
        w.set(cx0 + 1, fy, z0 + 1, B.COBWEB if c == 2 else B.AIR)
    w.chest(x1 - 1, fy, z0 + 4, [(0, "minecraft:arrow", 32, 0), (1, "minecraft:golden_apple", 1, 0),
                                 (9, "minecraft:iron_chestplate", 1, 0), (22, "minecraft:bone", 5, 0)], facing=4)
    for tx, tz, side in ((x0 + 1, z1 - 3, "w"), (x1 - 1, z1 - 3, "e")):
        w.set(tx, fy + 3, tz, B.TORCH, torch(side))
    # the fallen south wall: a ragged breach, rubble spilling in, a passage on to the cave
    for x in range(x1 - 5, x1):
        for y in range(fy, fy + 4):
            if y < fy + 3 or R_.random() < 0.5:
                w.set(x, y, z1, B.AIR)
        for z in range(z1 + 1, z1 + 5):
            for y in range(fy - 1, fy + 3):
                w.set(x, y, z, B.AIR)
            w.set(x, fy - 2, z, B.GRAVEL)


def gaol_ladder(w):
    """The ladder from the gaol's floor down into the cellar's corner (laid after the gaol is built)."""
    gx, gz = P.GAOL_LADDER
    fy = P.CELLAR[1]
    for y in range(fy, 53):
        w.set(gx, y, gz, B.LADDER, ladder("e"))                   # on the cellar's east wall, then the earth
        if w.id(gx + 1, y, gz) in (B.AIR,):
            w.set(gx + 1, y, gz, B.STONEBRICK, 0)
    for y in (53, 54):
        w.set(gx, y, gz, B.AIR)


def build(w, L):
    n = 0
    for pts in P.CAVE.values():
        n += branch(w, L, pts)
    for cx, fy, cz, rx, h, _ in P.CHAMBERS:
        n += chamber(w, L, cx, fy, cz, rx, h)
    pillars(w)
    U.dress_cave(w, (-64, -9, -30, 45, 26, 46), R_, ground=lambda x, z: ground_at(L, x, z), keep=red)
    grotto(w)
    lake(w)
    mouth(w)
    sinkhole(w, L)
    mine(w, L)
    top = shaft(w, L)
    cellar(w, L)
    return dict(carved=n, shaft_top=top)
