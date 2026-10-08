"""Planting and props on the red half: the Olive Grove and Acacia Flat as woods on green ground, the
Rancho's olive orchard in rows, trees along the creek and in the Wash, cacti and dead bushes on the orange,
rocks fallen at the foot of the cliffs, and Gilt's furniture — hitching rails, a cemetery by the chapel,
wagons, the town's name at the end of Main Street.

Nothing is scattered without a zone that says why: woods where the plan put woods, the rest sparse.
"""
import json
import os

import numpy as np

import plan as P
from mc import B
from noise import fbm, polyline_distance

RNG = np.random.default_rng(1717)
HERE = os.path.dirname(os.path.abspath(__file__))
TREES = json.load(open(os.path.join(HERE, "trees.json")))
SOFT = (B.AIR, B.TALLGRASS, B.DEADBUSH, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT)
GROUND = {B.GRASS, B.DIRT, B.SAND, B.STAINED_CLAY, B.HARDENED_CLAY, B.RED_SANDSTONE}


def H(L, x, z):
    return int(L.H[x - L.x0, z - L.z0])


def place(name):
    return dict((p["key"], p) for p in P.PLACES)[name]


def plant(w, L, x, z, tree, turn=0):
    g = H(L, x, z)
    if w.id(x, g, z) not in GROUND or w.id(x, g + 1, z) not in SOFT:
        return False
    cells = []
    for dx, dy, dz, i, d in tree["blocks"]:
        for _ in range(turn):
            dx, dz = -dz, dx
        X, Y, Z = x + dx, g + 1 + dy, z + dz
        if X >= 0 or not w.inside(X, Y, Z):
            return False
        cur = w.id(X, Y, Z)
        if cur in GROUND or cur in (B.STONE,):
            continue
        if cur not in SOFT and cur not in (B.LEAVES, B.LEAVES2):
            return False
        cells.append((X, Y, Z, i, d))
    for X, Y, Z, i, d in cells:
        if i in (17, 162) and turn % 2 == 1 and (d & 12) in (4, 8):
            d = (d & 3) | (12 - (d & 12))
        if w.id(X, Y, Z) in (B.LEAVES, B.LEAVES2) and i in (18, 161):
            continue
        w.set(X, Y, Z, i, d)
    return True


def blocked_mask(w, L):
    """Where no tree stands: on anything built, on a path, within four of a cliff's brink."""
    m = np.zeros(L.shape, bool)
    for ix in range(L.nx):
        x = L.x0 + ix
        for iz in range(L.nz):
            if not L.land[ix, iz] or L.water[ix, iz]:
                m[ix, iz] = True
                continue
            z = L.z0 + iz
            g = L.H[ix, iz]
            col = w.ids[x - w.x0, g:g + 24, z - w.z0]
            if int(col[0]) not in GROUND or np.any((col[1:] != 0) & ~np.isin(col[1:], list(SOFT))):
                m[ix, iz] = True
            if int(col[0]) in (B.GRAVEL,) or (int(col[0]) == B.DIRT and int(w.dat[x - w.x0, g, z - w.z0]) == 1 and False):
                m[ix, iz] = True
    # paths: every route, with a margin
    for r in P.ROUTES:
        d, _ = polyline_distance(L.X, L.Z, r["pts"])
        m |= d < {"street": 5, "road": 3.5, "track": 3}[r["kind"]]
    # the brink: any neighbour within four much lower
    Hf = np.where(L.land, L.H, -50).astype(float)
    from scipy import ndimage
    low = ndimage.minimum_filter(Hf, size=9)
    m |= (Hf - low) > 6
    return m


def wood(w, L, zone, kinds, weights, spacing, tries, seed):
    rng = np.random.default_rng(seed)
    pts = np.argwhere(zone & ~L.blocked)
    rng.shuffle(pts)
    n = 0
    for ix, iz in pts[:tries]:
        x, z = L.x0 + ix, L.z0 + iz
        kind = rng.choice(kinds, p=weights)
        t = TREES[kind][rng.integers(len(TREES[kind]))]
        c = t["crown"] * 0.5
        if any(np.hypot(x - a, z - b) < (c + pc) * spacing for a, b, pc in L.trees):
            continue
        if plant(w, L, x, z, t, int(rng.integers(4))):
            L.trees.append((x, z, c))
            n += 1
    return n


def green_ground(w, L, cx, cz, r, seed):
    """Under a wood the ground turns: grass and coarse dirt where the orange was, a ragged edge."""
    n = fbm(L.shape, 5, 2, seed=seed)
    d = np.hypot(L.X - cx, L.Z - cz) + 2.5 * n
    for ix, iz in np.argwhere((d < r) & L.land):
        x, z = L.x0 + ix, L.z0 + iz
        g = L.H[ix, iz]
        if w.id(x, g, z) in (B.SAND, B.STAINED_CLAY, B.HARDENED_CLAY, B.RED_SANDSTONE, B.DIRT) and w.id(x, g + 1, z) == B.AIR:
            if L.angle[ix, iz] < 40:
                q = RNG.random()
                w.set(x, g, z, *((B.GRASS, 0) if q < 0.72 else (B.DIRT, 1)))
                if w.id(x, g - 1, z) in (B.SAND,):
                    w.set(x, g - 1, z, B.DIRT)


def orchard(w, L, x0, z0, rows, cols, step=6):
    """The Rancho's olive orchard: trees in rows, which is what says somebody planted them."""
    for i in range(rows):
        for j in range(cols):
            x, z = x0 + j * step, z0 + i * step
            t = TREES["small-olive"][(i + j) % 3]
            if not L.blocked[x - L.x0, z - L.z0] and plant(w, L, x, z, t, (i * 3 + j) % 4):
                L.trees.append((x, z, 2.5))


def boulder(w, L, x, z, r, rng):
    """One rock fallen from the cliffs: red sandstone with hardened clay, darker than the ground it lies on."""
    g = H(L, x, z)
    for dx in range(-r - 1, r + 2):
        for dz in range(-r - 1, r + 2):
            for dy in range(-1, r + 1):
                d = np.hypot(dx / (r + 0.3), dz / (r * 0.85 + 0.3)) + max(0, dy) / (r * 0.9 + 0.5)
                if d > 1.0 + 0.15 * rng.standard_normal():
                    continue
                X, Y, Z = x + dx, g + dy, z + dz
                if X < 0 and w.id(X, Y, Z) in SOFT + (B.SAND, B.STAINED_CLAY, B.GRASS, B.DIRT):
                    q = rng.random()
                    w.set(X, Y, Z, *((B.RED_SANDSTONE, 0) if q < 0.5 else (B.HARDENED_CLAY, 0) if q < 0.8 else (B.STAINED_CLAY, 12)))


def scrub(w, L):
    """Dead bushes and cacti on the orange, grass on the soil patches, a little more in the green."""
    dens = fbm(L.shape, 10, 2, seed=91)
    for ix in range(L.nx):
        for iz in range(L.nz):
            if not L.land[ix, iz] or L.water[ix, iz]:
                continue
            x, z = L.x0 + ix, L.z0 + iz
            g = L.H[ix, iz]
            top = w.id(x, g, z)
            if w.id(x, g + 1, z) != B.AIR or L.angle[ix, iz] >= 40:
                continue
            r = RNG.random()
            green = L.green[ix, iz]
            if top == B.GRASS:
                if r < (0.28 if green else 0.12) * (0.7 + dens[ix, iz]):
                    w.set(x, g + 1, z, B.TALLGRASS, 1)
                elif green and r < 0.31:
                    w.set(x, g + 1, z, *((B.FLOWER, 2) if RNG.random() < 0.5 else (B.DANDELION, 0)))
            elif top in (B.SAND, B.STAINED_CLAY, B.HARDENED_CLAY) and not L.blocked[ix, iz]:
                if r < 0.018:
                    w.set(x, g + 1, z, B.DEADBUSH)
                elif top == B.SAND and r < 0.024:
                    # a cactus needs nothing solid beside it
                    if all(w.id(x + a, g + 1, z + b) == B.AIR for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        for k in range(1, 2 + int(RNG.integers(0, 3))):
                            w.set(x, g + k, z, B.CACTUS)


def cemetery(w, L, x0, z0):
    """Boot Hill: a fenced plot by the chapel, wooden crosses in two rows."""
    from buildings import claim
    claim(L, "cemetery", (x0, z0, x0 + 7, z0 + 6))
    g = H(L, x0 + 3, z0 + 3)
    for x in range(x0, x0 + 8):
        for z in range(z0, z0 + 7):
            if x in (x0, x0 + 7) or z in (z0, z0 + 6):
                if not (x == x0 + 7 and z == z0 + 3):
                    w.set(x, H(L, x, z) + 1, z, B.SPRUCE_FENCE)
    for x in range(x0 + 2, x0 + 7, 2):
        for z in (z0 + 2, z0 + 4):
            gy = H(L, x, z)
            w.set(x, gy, z, B.DIRT, 1)
            w.set(x, gy + 1, z, B.SPRUCE_FENCE); w.set(x, gy + 2, z, B.SPRUCE_FENCE)
            w.set(x, gy + 2, z - 1, B.TRAPDOOR, 4 | 0) if False else None


def hitching(w, L):
    """Hitching rails in front of the saloon, the hotel and the store, and a water trough."""
    for rec in L.records:
        if rec["kind"] not in ("saloon", "hotel", "store"):
            continue
        if rec["x0"] < -60:
            continue
        dx, dz = rec["door"]
        fx = {"e": 1, "w": -1}.get(rec["front"], 0)
        if not fx:
            continue
        X = dx + fx * 4
        for z in range(dz - 3, dz + 4):
            if z == dz:
                continue
            g = H(L, X, z)
            if w.id(X, g + 1, z) == B.AIR and X < 0:
                w.set(X, g + 1, z, B.FENCE)


def wagon(w, L, x, z, along_x=True, covered=True):
    """A wagon: a slab bed on log wheels, a canvas of white wool over hoops."""
    from buildings import claim
    claim(L, "wagon", (x - 2, z - 2, x + 4, z + 4) if along_x else (x - 2, z - 2, x + 2, z + 4))
    g = H(L, x, z)
    for k in range(4):
        X, Z = (x + k, z) if along_x else (x, z + k)
        for s in (-1, 0, 1):
            XX, ZZ = (X, Z + s) if along_x else (X + s, Z)
            w.set(XX, g + 2, ZZ, B.WOOD_SLAB, 1)
            if covered:
                if s == 0:
                    w.set(XX, g + 4, ZZ, B.WOOL, 0)
                else:
                    w.set(XX, g + 3, ZZ, B.WOOL, 0)
    for k in (0, 3):
        for s in (-2, 2):
            X, Z = (x + k, z + s) if along_x else (x + s, z + k)
            w.set(X, g + 1, Z, B.LOG, 4 if not along_x else 8)


def town_sign(w, L):
    z = -95
    x = int(round(P.canyon_x(z) - 12)) - 3
    g = H(L, x, z)
    for y in (g + 1, g + 2):
        w.set(x, y, z, B.SPRUCE_FENCE)
    w.sign(x, g + 3, z, ["Welcome to", "GILT", "pop. 212", ""], rot=0)


def build(w, L):
    L.blocked = blocked_mask(w, L)
    L.trees = []
    n = 0
    grove, acacias, rancho = place("grove"), place("acacias"), place("rancho")
    green_ground(w, L, *grove["at"], grove["r"] + 2, 101)
    green_ground(w, L, *acacias["at"], acacias["r"] + 2, 102)
    green_ground(w, L, rancho["at"][0] + 14, rancho["at"][1] + 12, 9, 103)
    zone = np.hypot(L.X - grove["at"][0], L.Z - grove["at"][1]) < grove["r"]
    n += wood(w, L, zone, ["olive", "small-olive", "acacia"], [0.55, 0.3, 0.15], 0.8, 3000, 1)
    zone = np.hypot(L.X - acacias["at"][0], L.Z - acacias["at"][1]) < acacias["r"]
    n += wood(w, L, zone, ["acacia", "olive"], [0.75, 0.25], 0.8, 3000, 2)
    orchard(w, L, rancho["at"][0] + 6, rancho["at"][1] + 18, 2, 4)
    # along the creek where nothing is built: the trees the spring waters
    creek_banks = (np.abs(L.X - L.cx) > 3) & (np.abs(L.X - L.cx) < 8) & (L.d < L.floor_edge)
    n += wood(w, L, creek_banks, ["acacia", "olive"], [0.6, 0.4], 0.9, 1500, 3)
    # in the Wash, where water runs after rain
    n += wood(w, L, L.wash_mask & (L.X < -45), ["acacia", "small-olive"], [0.6, 0.4], 1.1, 600, 4)
    # a few alone on the mesa: one by the fort's gate, one on the rim over the arch, two on the bench
    for (x, z, kind, i) in ((-92, 12, "olive", 3), (-56, 8, "acacia", 2), (-46, -60, "acacia", 5),
                            (-110, -40, "acacia", 1), (-120, 40, "olive", 7), (-70, 30, "acacia", 4),
                            (-100, -80, "olive", 2)):
        t = TREES[kind][i % len(TREES[kind])]
        if not L.blocked[x - L.x0, z - L.z0] and plant(w, L, x, z, t, i % 4):
            L.trees.append((x, z, t["crown"] * 0.5)); n += 1
    print(f"  planted {n} trees")
    # rocks fallen at the foot of the cliffs and lying on the mesa
    rng = np.random.default_rng(55)
    talus = (L.d > L.floor_edge - 4) & (L.d < L.floor_edge) & ~L.blocked
    pts = np.argwhere(talus); rng.shuffle(pts)
    for ix, iz in pts[:14]:
        boulder(w, L, L.x0 + ix, L.z0 + iz, int(rng.integers(1, 3)), rng)
    for x, z, r in ((-90, -20, 2), (-62, 50, 2), (-118, 60, 1), (-96, -92, 2), (-72, -8, 1), (-58, 92, 1)):
        if not L.blocked[x - L.x0, z - L.z0]:
            boulder(w, L, x, z, r, rng)
    cemetery(w, L, -22, 44)
    hitching(w, L)
    wagon(w, L, -86, 30, along_x=False)
    from terrain import wash_line
    wagon(w, L, -72, int(round(wash_line(-72))) - 1, along_x=True, covered=False)     # a broken wagon left in the Wash
    town_sign(w, L)
    scrub(w, L)
