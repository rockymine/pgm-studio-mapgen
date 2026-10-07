"""Below the ground: Falls Cave (water-cut, entered behind the waterfall), Ironhollow Mine (timbered
galleries from an adit by the spawn to the shaft under the headframe and on to the breakthrough), and the
Gaol Cellar under the old gaol in town, whose back wall has fallen into the cave.

Every passage is carved as a chain of flattened ellipsoids along a spline, so its floor is walkable and its
walls are round; a mine gallery is carved as a box and then timbered.
"""
import numpy as np

from mc import B
from noise import spline, fbm

RNG = np.random.default_rng(1234)

# ---- the cave, as 3-D polylines (x, y_floor, z) with a radius per point ------------------------------
CAVE = {
    # mouth in the rift face behind the falls, a long gallery under the south bank to the lake chamber
    "gallery": [(-9, 36, 2, 2.6), (-14, 36, 3, 3.0), (-20, 35, 5, 3.4), (-27, 34, 8, 3.2), (-34, 33, 11, 3.6),
                (-40, 32, 14, 4.0)],
    # south: up to the sinkhole by the south monument
    "south": [(-40, 32, 14, 3.0), (-44, 33, 20, 2.8), (-47, 35, 27, 2.6), (-49, 37, 33, 2.8), (-50, 39, 38, 3.0)],
    # north: under the river and up to the gaol cellar
    "north": [(-40, 32, 14, 3.0), (-43, 32, 7, 2.6), (-46, 33, 0, 2.6), (-49, 35, -8, 2.8), (-52, 37, -15, 2.6),
              (-53, 40, -21, 2.5), (-53, 42, -28, 2.2)],
    # a side passage off the north branch, under the mill, to the smugglers' grotto
    "grotto": [(-46, 33, 0, 2.2), (-50, 33, 2, 2.0), (-54, 33, 4, 2.4), (-58, 33, 5, 2.2)],
    # west: toward the mine's breakthrough
    "west": [(-49, 37, 33, 2.4), (-53, 38, 35, 2.2), (-57, 39, 37, 2.0)],
}
LAKE = (-40, 31, 14)          # the lake chamber's floor centre

MINE = [  # (x, y_floor, z): straight runs between these, three wide, three tall
    (-104, 59, 5), (-104, 57, 11), (-103, 53, 23), (-100, 50, 31), (-95, 47, 40), (-89, 45, 48), (-84, 45, 56),
    (-76, 44, 52), (-68, 42, 46), (-62, 40, 41), (-57, 39, 37),
]
SHAFT = (-84, 56)
CELLAR = (-55, 43, -37, -49, -31)   # x0, floor y, z0, x1, z1


def carve_ellipsoid(w, L, cx, cy, cz, r, rv, floor_y, allow_surface=False):
    x0, x1 = int(np.floor(cx - r)), int(np.ceil(cx + r))
    z0, z1 = int(np.floor(cz - r)), int(np.ceil(cz + r))
    y0, y1 = int(np.floor(floor_y)), int(np.ceil(cy + rv))
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not w.inside(x, 0, z) or x >= -1:
                continue
            ix, iz = x - L.x0, z - L.z0
            if not (0 <= ix < L.nx and 0 <= iz < L.nz):
                continue
            ground = L.H[ix, iz]
            for y in range(y0, y1 + 1):
                d = ((x - cx) / r) ** 2 + ((z - cz) / r) ** 2 + ((y - cy) / rv) ** 2
                if d > 1:
                    continue
                if not allow_surface and y > ground - 3 and L.land[ix, iz]:
                    continue
                if w.id(x, y, z) not in (B.WATER, B.WATER_FLOW):
                    w.set(x, y, z, B.AIR)


def carve_tube(w, L, pts, wobble=0.35, allow_surface=False):
    xyz = [(p[0], p[2]) for p in pts]
    sp = spline(xyz, 0.4)
    # interpolate floor and radius along the polyline by arc length
    arc = np.concatenate([[0], np.cumsum([np.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts[:-1], pts[1:])])])
    sarc = np.concatenate([[0], np.cumsum([np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(sp[:-1], sp[1:])])])
    sarc *= arc[-1] / max(sarc[-1], 1e-6)
    floors = np.interp(sarc, arc, [p[1] for p in pts])
    radii = np.interp(sarc, arc, [p[3] for p in pts])
    nz = np.cumsum(RNG.normal(0, 0.15, len(sp)))
    k = min(25, len(nz)); nz = (nz - np.convolve(nz, np.ones(k) / k, mode="same")) * wobble
    for (x, z), fy, r, n in zip(sp, floors, radii, nz):
        r2 = max(1.6, r + n)
        rv = r2 * 0.8
        carve_ellipsoid(w, L, x, fy + rv * 0.55, z, r2, rv, fy + 0.0, allow_surface)
    return sp, floors


def dress_cave(w, L, box):
    """Floors of gravel and clay, stalactites, mushrooms, ore glints, moss by the water."""
    x0, x1, z0, z1, y0, y1 = box
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not w.inside(x, 0, z) or x >= -1:
                continue
            col = w.ids[x - w.x0, :, z - w.z0]
            for y in range(max(2, y0), y1):
                if col[y] != B.AIR:
                    continue
                below, above = col[y - 1], col[y + 1]
                ix, iz = x - L.x0, z - L.z0
                if not (0 <= ix < L.nx and 0 <= iz < L.nz) or y > L.H[ix, iz] - 2:
                    continue
                r = RNG.random()
                if below in (B.STONE, B.COBBLE, B.DIRT) and y - 1 < L.H[ix, iz] - 3:
                    # the floor: gravel with clay, a few loose stones
                    w.set(x, y - 1, z, *((B.GRAVEL, 0) if r < 0.45 else (B.STONE, 5) if r < 0.7 else (B.CLAY, 0) if r < 0.8 else (B.COBBLE, 0)))
                    if r > 0.985:
                        w.set(x, y, z, B.BROWN_MUSHROOM if RNG.random() < 0.6 else B.RED_MUSHROOM)
                if above in (B.STONE,) and col[y - 1] == B.AIR and r < 0.05:
                    # a stalactite: stone tapering to a cobble wall tip
                    n = 1 + int(RNG.random() * 2.5)
                    for k in range(n):
                        if col[y - k] == B.AIR and col[y - k - 1] == B.AIR:
                            w.set(x, y - k, z, B.STONE if k < n - 1 else B.COBBLE_WALL, 0)
    # ore in the cave walls: a few iron and coal glints facing the air
    for _ in range(260):
        x = int(RNG.integers(x0, x1 + 1)); z = int(RNG.integers(z0, z1 + 1)); y = int(RNG.integers(y0, y1))
        if w.id(x, y, z) == B.STONE and any(w.id(x + dx, y + dy, z + dz) == B.AIR
                                            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0))):
            w.set(x, y, z, B.COAL_ORE if RNG.random() < 0.6 else B.IRON_ORE)


def lake(w, L):
    """The lake chamber's pool: still water in the hollow of its floor, a gravel beach round it."""
    cx, cy, cz = LAKE
    for x in range(cx - 7, cx + 8):
        for z in range(cz - 7, cz + 8):
            d = np.hypot((x - cx) / 5.5, (z - cz - 1) / 4.2)
            if d < 1.0:
                depth = 2 if d < 0.6 else 1
                for y in range(cy - depth + 1, cy + 1):
                    w.set(x, y, z, B.WATER)
                w.set(x, cy - depth, z, B.CLAY if d < 0.5 else B.GRAVEL)
                # keep the air above the pool clear
                for y in range(cy + 1, cy + 3):
                    if w.id(x, y, z) not in (B.AIR,):
                        pass


def mouth(w, L):
    """The cave's mouth in the rift face: a rock ledge in front of it, beside the falling water."""
    for z in range(1, 10):
        for x in (-11, -10):
            if x == -10 and z < 4:
                continue
            w.set(x, 35, z, B.STONE, 5 if (x + z) % 3 else 0)
            if z >= 5:
                w.set(x, 34, z, B.STONE, 0)
    # hanging vines over the mouth
    for z in range(-1, 6):
        for y in range(39, 42):
            if w.id(-11, y, z) == B.AIR and w.id(-12, y, z) not in (B.AIR, B.WATER, B.WATER_FLOW):
                if RNG.random() < 0.5:
                    w.set(-11, y, z, B.VINE, 2)


def sinkhole(w, L):
    """Where the cave roof fell in: a funnel in the field, ringed with stepped rubble a player can climb."""
    cx, cz = -50, 40
    ix, iz = cx - L.x0, cz - L.z0
    top = int(L.H[ix, iz])
    floor = 39
    for x in range(cx - 7, cx + 8):
        for z in range(cz - 7, cz + 8):
            d = np.hypot(x - cx, z - cz)
            if d > 6.5:
                continue
            gx, gz = x - L.x0, z - L.z0
            g = int(L.H[gx, gz])
            # funnel: the deeper the nearer the middle, in one-block steps
            depth_y = int(round(floor + max(0, (d - 2.0)) * 1.6))
            if depth_y >= g:
                continue
            for y in range(depth_y + 1, g + 1 + 2):
                w.set(x, y, z, B.AIR)
            r = RNG.random()
            w.set(x, depth_y, z, *((B.GRAVEL, 0) if r < 0.35 else (B.DIRT, 1) if r < 0.6 else (B.STONE, 5) if r < 0.8 else (B.COBBLE, 0)))
            if d > 5.2:
                w.set(x, depth_y, z, B.GRASS)
            L.H[gx, gz] = depth_y
    # grass overhang and a few roots: dirt lips with vines hanging in
    for x in range(cx - 6, cx + 7):
        for z in range(cz - 6, cz + 7):
            if 4.2 < np.hypot(x - cx, z - cz) < 5.5 and RNG.random() < 0.25:
                y = w.top(x, z) - 1
                # a vine hangs only off a face it can hold: rock or soil on its south side
                if w.id(x, y, z) == B.AIR and w.id(x, y, z + 1) in (B.STONE, B.DIRT, B.GRASS, B.COBBLE, B.GRAVEL):
                    w.set(x, y, z, B.VINE, 1)


def mine(w, L):
    """Three-wide, three-tall galleries; spruce sets every four blocks; rails on the level runs; iron in the walls."""
    path = []
    for (ax, ay, az), (bx, by, bz) in zip(MINE[:-1], MINE[1:]):
        n = int(max(abs(bx - ax), abs(bz - az)))
        for i in range(n):
            t = i / n
            path.append((ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t))
    path.append(MINE[-1])
    pts = [(int(round(x)), int(round(y)), int(round(z))) for x, y, z in path]
    # dedupe and make the floor change by at most one per step
    clean = [pts[0]]
    for p in pts[1:]:
        if (p[0], p[2]) == (clean[-1][0], clean[-1][2]):
            continue
        y = clean[-1][1] + int(np.clip(p[1] - clean[-1][1], -1, 1))
        clean.append((p[0], y, p[2]))
    for i, (x, y, z) in enumerate(clean):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dy in (0, 1, 2):
                    w.set(x + dx, y + dy, z + dz, B.AIR)
                w.set(x + dx, y - 1, z + dz, B.GRAVEL if RNG.random() < 0.3 else B.STONE, 0 if RNG.random() < 0.5 else 5)
    # the timber sets, the rails and the steps
    for i, (x, y, z) in enumerate(clean):
        nxt = clean[min(i + 1, len(clean) - 1)]
        prv = clean[max(i - 1, 0)]
        along_x = abs(nxt[0] - prv[0]) >= abs(nxt[2] - prv[2])
        if nxt[1] > y and i + 1 < len(clean):
            # a rise: a stair so the gallery walks rather than jumps
            sd = (0 if nxt[0] > x else 1) if along_x else (2 if nxt[2] > z else 3)
            for k in (-1, 0, 1):
                ox, oz = (0, k) if along_x else (k, 0)
                w.set(x + ox, y, z + oz, B.COBBLE_STAIRS, sd)
        elif prv[1] > y and i > 0:
            sd = (0 if prv[0] > x else 1) if along_x else (2 if prv[2] > z else 3)
            for k in (-1, 0, 1):
                ox, oz = (0, k) if along_x else (k, 0)
                if w.id(x + ox, y, z + oz) == B.AIR:
                    w.set(x + ox, y, z + oz, B.COBBLE_STAIRS, sd)
        level = nxt[1] == y and prv[1] == y
        if level and w.id(x, y, z) == B.AIR:
            w.set(x, y, z, B.RAIL, 1 if along_x else 0)
        if i % 4 == 2:
            for k in (-1, 1):
                ox, oz = (0, k * 2) if along_x else (k * 2, 0)
                for dy in (0, 1, 2):
                    if w.id(x + ox, y + dy, z + oz) not in (B.AIR,):
                        w.set(x + ox, y + dy, z + oz, B.LOG, 1)
                # posts stand just inside the wall line
                for dy in (0, 1):
                    w.set(x + ox // 2, y + dy, z + oz // 2, B.SPRUCE_FENCE)
            for k in (-1, 0, 1):
                ox, oz = (0, k) if along_x else (k, 0)
                w.set(x + ox, y + 2, z + oz, B.LOG, 1 | (8 if along_x else 4))
            if i % 12 == 2:
                # on the gallery wall: facing north off the south wall, or west off the east wall
                tx, tz = (x, z + 1) if along_x else (x + 1, z)
                w.set(tx, y + 1, tz, B.TORCH, 4 if along_x else 2)
    # iron ore in the gallery walls, richer toward the shaft
    for x, y, z in clean[::2]:
        for _ in range(3):
            ox, oy, oz = int(RNG.integers(-2, 3)), int(RNG.integers(0, 3)), int(RNG.integers(-2, 3))
            if w.id(x + ox, y + oy, z + oz) == B.STONE:
                w.set(x + ox, y + oy, z + oz, B.IRON_ORE)
    # the adit's portal: a timber frame in the hillside
    ax, ay, az = MINE[0]
    for dx in (-2, -1, 0, 1, 2):
        for dy in (0, 1, 2, 3):
            if dy == 3 or abs(dx) == 2:
                w.set(ax + dx, ay + dy, az - 1, B.LOG, 1 if dy < 3 else 5)
    for dx in (-1, 0, 1):
        for dy in (0, 1, 2):
            w.set(ax + dx, ay + dy, az - 1, B.AIR)
            w.set(ax + dx, ay + dy, az - 2, B.AIR)
    # the foreman's chest where the gallery breaks into the cave
    bx, by, bz = MINE[-2]
    w.chest(bx + 1, by, bz + 1, [(0, "minecraft:iron_ingot", 6, 0), (1, "minecraft:bread", 8, 0),
                                 (4, "minecraft:torch", 16, 0), (13, "minecraft:iron_pickaxe", 1, 0)], facing=3)
    L.mine_path = clean


def shaft(w, L):
    """The shaft from the gallery up to the headframe's floor: a ladder in a timber-lined well."""
    sx, sz = SHAFT
    ground = int(L.H[sx - L.x0, sz - L.z0])
    gy = 45
    for y in range(gy, ground + 2):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(sx + dx, y, sz + dz, B.AIR)
        for dx, dz in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
            w.set(sx + dx, y, sz + dz, B.LOG, 1)
        for d in (-1, 0, 1):
            for (ox, oz) in ((d, -2), (d, 2), (-2, d), (2, d)):
                if y <= ground:
                    w.set(sx + ox, y, sz + oz, B.PLANKS, 1)
        w.set(sx, y, sz + 1, B.LADDER, 2)
    w.set(sx, gy - 1, sz + 1, B.PLANKS, 1)
    L.shaft_top = ground


def cellar(w, L):
    """The gaol cellar: a vault of stone brick with three barred cells; its south wall has fallen into the cave."""
    x0, fy, z0, x1, z1 = CELLAR
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(fy - 1, fy + 6):
                edge = x in (x0, x1) or z in (z0, z1) or y in (fy - 1, fy + 5)
                if edge:
                    r = RNG.random()
                    w.set(x, y, z, B.STONEBRICK, 0 if r < 0.7 else (2 if r < 0.88 else 1))
                else:
                    w.set(x, y, z, B.AIR)
    # floor of the vault
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            r = RNG.random()
            w.set(x, fy - 1, z, *((B.STONEBRICK, 0) if r < 0.4 else (B.STONE, 6) if r < 0.65 else (B.STONE, 5) if r < 0.85 else (B.STONE, 0)))
    # three cells along the north wall, iron bars and an iron door each
    for c in range(3):
        cx0 = x0 + 1 + c * 3
        for z in (z0 + 3,):
            for x in range(cx0, cx0 + 3):
                for y in (fy, fy + 1, fy + 2):
                    w.set(x, y, z, B.IRON_BARS)
            w.set(cx0 + 1, fy, z0 + 3, B.IRON_DOOR, 3)
            w.set(cx0 + 1, fy + 1, z0 + 3, B.IRON_DOOR, 8)
        if c < 2:
            for y in (fy, fy + 1, fy + 2):
                for z in range(z0 + 1, z0 + 3):
                    w.set(cx0 + 3, y, z, B.STONEBRICK, 0)
        w.set(cx0 + 1, fy, z0 + 1, B.COBWEB if c == 2 else B.AIR)
    w.set(x0 + 2, fy, z0 + 1, B.WOOD_SLAB, 1)   # a bunk
    # the gaoler's table, a chest and torches
    w.set(x1 - 2, fy, z1 - 2, B.FENCE); w.set(x1 - 2, fy + 1, z1 - 2, B.PLATE_WOOD)
    w.set(x1 - 3, fy, z1 - 2, B.SPRUCE_STAIRS, 0)
    w.chest(x1 - 1, fy, z0 + 4, [(0, "minecraft:arrow", 32, 0), (1, "minecraft:golden_apple", 1, 0),
                                 (9, "minecraft:iron_chestplate", 1, 0), (22, "minecraft:bone", 5, 0)], facing=4)
    for tx, tz, f in ((x0 + 1, z1 - 3, 1), (x1 - 1, z1 - 3, 2)):
        w.set(tx, fy + 3, tz, B.TORCH, f)
    # the fallen south wall: a ragged breach into the cave, rubble spilling in
    for x in range(x1 - 6, x1 - 1):
        for y in range(fy, fy + 4):
            if y < fy + 3 or RNG.random() < 0.5:
                w.set(x, y, z1, B.AIR)
    for x in range(x1 - 7, x1):
        if RNG.random() < 0.6:
            w.set(x, fy, z1 - 1, B.COBBLE if RNG.random() < 0.5 else B.STONEBRICK, 2)
    for x in range(x1 - 6, x1 - 1):
        for z in range(z1 + 1, z1 + 4):
            for y in range(fy, fy + 3):
                w.set(x, y, z, B.AIR)
            w.set(x, fy - 1, z, B.GRAVEL)
    L.cellar = CELLAR


PILLAR_HALL = (-46, 34, 26)
GROTTO = (-60, 33, 6)


def pillar_hall(w, L):
    """A low wide hall on the south branch where the water once pooled: natural pillars hold its roof, and
    the fight in it is from pillar to pillar."""
    cx, cy, cz = PILLAR_HALL
    carve_ellipsoid(w, L, cx, cy + 2.6, cz, 7.5, 4.2, cy)
    carve_ellipsoid(w, L, cx + 3, cy + 2.2, cz - 3, 5.0, 3.6, cy)
    rng = np.random.default_rng(8)
    for _ in range(7):
        a = rng.uniform(0, 2 * np.pi); r = rng.uniform(2.5, 6.0)
        px, pz = int(round(cx + r * np.cos(a))), int(round(cz + r * 0.9 * np.sin(a)))
        wide = rng.random() < 0.4
        for x in range(px, px + (2 if wide else 1)):
            for y in range(cy - 1, cy + 9):
                if w.id(x, y, pz) == B.AIR:
                    w.set(x, y, pz, B.STONE, 5 if (y + x) % 3 else 0)


def grotto(w, L):
    """The smugglers' grotto: a dead end off the north branch, under the mill, with what they left."""
    cx, cy, cz = GROTTO
    carve_ellipsoid(w, L, cx, cy + 2.2, cz, 3.6, 3.0, cy)
    w.chest(cx - 2, cy, cz, [(0, "minecraft:golden_apple", 2, 0), (1, "minecraft:arrow", 32, 0),
                             (4, "minecraft:iron_leggings", 1, 0), (13, "minecraft:paper", 3, 0)], facing=5)
    w.set(cx - 2, cy, cz + 1, B.WOOD_SLAB, 1)    # barrels and a plank, as a stash would be
    w.set(cx - 1, cy, cz - 2, B.PLANKS, 1)
    w.set(cx - 1, cy + 1, cz - 2, B.WOOD_SLAB, 1)
    w.set(cx, cy, cz + 2, B.TORCH, 5)


def alcoves(w, L):
    """Pockets off the long gallery, so it is not a tube: each a step aside to wait in."""
    for (x, y, z, r) in ((-18, 35, 9, 2.2), (-26, 34, 2, 2.0), (-31, 33, 15, 2.4), (-48, 36, 31, 2.0), (-50, 35, -6, 2.0)):
        carve_ellipsoid(w, L, x, y + 1.6, z, r, 2.0, y)


def stalagmites(w, L, box):
    x0, x1, z0, z1, y0, y1 = box
    rng = np.random.default_rng(9)
    for _ in range(900):
        x = int(rng.integers(x0, x1 + 1)); z = int(rng.integers(z0, z1 + 1)); y = int(rng.integers(y0, y1))
        if w.id(x, y, z) != B.AIR or w.id(x, y - 1, z) not in (B.GRAVEL, B.STONE, B.CLAY, B.COBBLE):
            continue
        ix, iz = x - L.x0, z - L.z0
        if not (0 <= ix < L.nx and 0 <= iz < L.nz) or y > L.H[ix, iz] - 3:
            continue
        # only against a wall, so the floor stays walkable
        walls = sum(w.id(x + dx, y, z + dz) not in (B.AIR, B.WATER) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if walls >= 1 and w.id(x, y + 1, z) == B.AIR and w.id(x, y + 2, z) == B.AIR:
            w.set(x, y, z, B.STONE, 5)
            if rng.random() < 0.5:
                w.set(x, y + 1, z, B.COBBLE_WALL)


def build(w, L):
    for name, pts in CAVE.items():
        carve_tube(w, L, pts)
    pillar_hall(w, L)
    alcoves(w, L)
    # the lake chamber: a wide low hall
    cx, cy, cz = LAKE
    carve_ellipsoid(w, L, cx, cy + 3, cz + 1, 8.5, 4.8, cy - 1)
    carve_ellipsoid(w, L, cx - 3, cy + 2.5, cz - 2, 5.5, 4.0, cy)
    dress_cave(w, L, (-64, -9, -30, 45, 26, 46))
    stalagmites(w, L, (-64, -11, -30, 45, 28, 44))
    grotto(w, L)
    lake(w, L)
    mouth(w, L)
    sinkhole(w, L)
    mine(w, L)
    shaft(w, L)
    cellar(w, L)
