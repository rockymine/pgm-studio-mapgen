"""Below the ground (red half): Falls Cave, entered behind the waterfall, with its lake chamber, pillar hall,
grotto and alcoves; Ironhollow Mine from the adit by the spawn to the shaft and the breakthrough; the gaol
cellar whose south wall has fallen into the cave; the sinkhole's rubble.

The cave's passages are pgmvox.solid tubes (capsules along the branch) clamped to a level floor and kept three
blocks under the surface; the chambers are solid ellipsoids. The floor clamp, the surface guard, the dressing,
the mine's timbering and the cellar are local: the library has no tunnel, gallery or cave finish.
"""
import math

import numpy as np

import plan as P
from pgmvox import B, rng
from pgmvox import solid as S
from pgmvox.orient import ladder, stair, torch

R_ = rng(P.BOARD, "under")


def ground_at(L, x, z):
    i, k = x - P.X_MIN, z - P.Z_MIN
    if 0 <= i < L.H.shape[0] and 0 <= k < L.H.shape[1] and L.land[i, k]:
        return int(L.H[i, k])
    return None


def carve(w, L, solid, floor, keep_surface=True):
    """Air in a solid's cells at or over floor(x, z), never within three of the surface, never into water."""
    n = 0
    for x, y, z in solid.cells():
        if x >= -1 or y < floor(x, z):
            continue
        g = ground_at(L, x, z)
        if keep_surface and g is not None and y > g - 3:
            continue
        if w.id(x, y, z) in (B.WATER, B.WATER_FLOW):
            continue
        w.set(x, y, z, B.AIR)
        n += 1
    return n


def branch(w, L, pts):
    """One cave branch: a tube through (x, floor + 0.45 r, z) with its radius, its floor held level across."""
    arc = np.concatenate([[0], np.cumsum([math.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts, pts[1:])])])
    path = [(x + 0.5, fy + 0.45 * r, z + 0.5) for x, fy, z, r in pts]
    tube = S.tube(path, [p[3] for p in pts])

    def floor(x, z):
        return int(round(np.interp(P._arc_of(pts, x, z), arc, [p[1] for p in pts])))
    return carve(w, L, tube, floor)


def chamber(w, L, cx, fy, cz, rx, h):
    e = S.ellipsoid(cx + 0.5, fy + 0.6 * h, cz + 0.5, rx, h, rx * 0.9)
    return carve(w, L, e, lambda x, z: fy)


def dress(w, L, box):
    """Floors of gravel and clay, stalactites, mushrooms; ore in the walls; stalagmites against the walls."""
    x0, x1, z0, z1, y0, y1 = box
    for x in range(x0, min(x1, -2) + 1):
        for z in range(z0, z1 + 1):
            g = ground_at(L, x, z)
            if g is None:
                continue
            col = w.ids[x - w.x0, :, z - w.z0]
            for y in range(max(2, y0), min(y1, g - 2)):
                if col[y] != B.AIR:
                    continue
                r = R_.random()
                if col[y - 1] in (B.STONE, B.COBBLE, B.DIRT) and y - 1 < g - 3:
                    w.set(x, y - 1, z, *((B.GRAVEL, 0) if r < 0.45 else (B.STONE, 5) if r < 0.7 else
                                         (B.CLAY, 0) if r < 0.8 else (B.COBBLE, 0)))
                    if r > 0.985:
                        w.set(x, y, z, B.BROWN_MUSHROOM if R_.random() < 0.6 else B.RED_MUSHROOM)
                if col[y + 1] == B.STONE and col[y - 1] == B.AIR and r < 0.05:
                    n = 1 + int(R_.random() * 2.5)
                    for k in range(n):
                        if col[y - k] == B.AIR and col[y - k - 1] == B.AIR:
                            w.set(x, y - k, z, B.STONE if k < n - 1 else B.COBBLE_WALL, 0)
    for _ in range(300):
        x, z, y = int(R_.integers(x0, x1 + 1)), int(R_.integers(z0, z1 + 1)), int(R_.integers(y0, y1))
        if x < -1 and w.id(x, y, z) == B.STONE and any(w.id(x + a, y + b, z + c) == B.AIR for a, b, c in
                                                        ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0))):
            w.set(x, y, z, B.COAL_ORE if R_.random() < 0.6 else B.IRON_ORE)
    for _ in range(900):
        x, z, y = int(R_.integers(x0, x1 + 1)), int(R_.integers(z0, z1 + 1)), int(R_.integers(y0, y1))
        g = ground_at(L, x, z)
        if g is None or x >= -1 or y > g - 3 or w.id(x, y, z) != B.AIR:
            continue
        if w.id(x, y - 1, z) not in (B.GRAVEL, B.STONE, B.CLAY, B.COBBLE):
            continue
        walls = sum(w.id(x + a, y, z + c) not in (B.AIR, B.WATER) for a, c in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if walls >= 1 and w.id(x, y + 1, z) == B.AIR and w.id(x, y + 2, z) == B.AIR:
            w.set(x, y, z, B.STONE, 5)
            if R_.random() < 0.5:
                w.set(x, y + 1, z, B.COBBLE_WALL)


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
    """Three-wide, three-tall galleries; spruce sets every four blocks; rails on the level runs; stairs on the
    rises; iron in the walls; a timber portal at the adit; the foreman's chest at the breakthrough."""
    clean = P.mine_line()
    for x, y, z in clean:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dy in (0, 1, 2):
                    w.set(x + dx, y + dy, z + dz, B.AIR)
                w.set(x + dx, y - 1, z + dz, B.GRAVEL if R_.random() < 0.3 else B.STONE, 0 if R_.random() < 0.5 else 5)
    for i, (x, y, z) in enumerate(clean):
        nxt, prv = clean[min(i + 1, len(clean) - 1)], clean[max(i - 1, 0)]
        along_x = abs(nxt[0] - prv[0]) >= abs(nxt[2] - prv[2])
        step = None
        if nxt[1] > y and i + 1 < len(clean):
            step = (nxt[0] - x, nxt[2] - z)
        elif prv[1] > y and i > 0:
            step = (prv[0] - x, prv[2] - z)
        if step is not None and step != (0, 0):
            for k in (-1, 0, 1):
                ox, oz = (0, k) if along_x else (k, 0)
                if w.id(x + ox, y, z + oz) == B.AIR:
                    w.set(x + ox, y, z + oz, B.COBBLE_STAIRS, stair(step))
        elif nxt[1] == y and prv[1] == y and w.id(x, y, z) == B.AIR:
            w.set(x, y, z, B.RAIL, 1 if along_x else 0)
        if i % 4 == 2 and nxt[1] == y and prv[1] == y:          # a timber set only where the floor is level:
            for k in (-1, 1):                                      # over a stair its cap takes the headroom
                ox, oz = (0, k * 2) if along_x else (k * 2, 0)
                for dy in (0, 1, 2):
                    if w.id(x + ox, y + dy, z + oz) != B.AIR:
                        w.set(x + ox, y + dy, z + oz, B.LOG, 1)
                for dy in (0, 1):
                    if w.id(x + ox // 2, y + dy, z + oz // 2) in (B.AIR, B.RAIL):
                        w.set(x + ox // 2, y + dy, z + oz // 2, B.SPRUCE_FENCE)
            for k in (-1, 0, 1):
                ox, oz = (0, k) if along_x else (k, 0)
                w.set(x + ox, y + 2, z + oz, B.LOG, 1 | (4 if along_x else 8))
            if i % 12 == 2:
                tx, tz = (x, z + 1) if along_x else (x + 1, z)
                if w.id(tx, y + 1, tz) == B.AIR:
                    w.set(tx, y + 1, tz, B.TORCH, torch("s" if along_x else "e"))
    for x, y, z in clean[::2]:
        for _ in range(3):
            ox, oy, oz = int(R_.integers(-2, 3)), int(R_.integers(0, 3)), int(R_.integers(-2, 3))
            if w.id(x + ox, y + oy, z + oz) == B.STONE:
                w.set(x + ox, y + oy, z + oz, B.IRON_ORE)
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
    gy = 45
    for y in range(gy, g + 1):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(sx + dx, y, sz + dz, B.AIR)
        for dx, dz in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
            w.set(sx + dx, y, sz + dz, B.LOG, 1)
        for d in (-1, 0, 1):
            for ox, oz in ((d, -2), (d, 2), (-2, d), (2, d)):
                if y <= g:
                    w.set(sx + ox, y, sz + oz, B.PLANKS, 1)
        w.set(sx, y, sz + 1, B.LADDER, 2)
    w.set(sx, gy - 1, sz + 1, B.PLANKS, 1)
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
    dress(w, L, (-64, -9, -30, 45, 26, 46))
    grotto(w)
    lake(w)
    mouth(w)
    sinkhole(w, L)
    mine(w, L)
    top = shaft(w, L)
    cellar(w, L)
    return dict(carved=n, shaft_top=top)
