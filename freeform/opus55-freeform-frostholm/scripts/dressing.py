"""Planting and props on red's half: pine and spruce woods — Granskog between the hall and the lake,
Nordskog on the way to the Beacon, copses on the middle island — snow caught on the crowns, boulders left by
the ice, woodpiles by the houses, a sled by the hall.
"""
import json
import os

import numpy as np

import plan as P
from mc import B
from noise import fbm, polyline_distance

RNG = np.random.default_rng(4545)
HERE = os.path.dirname(os.path.abspath(__file__))
TREES = json.load(open(os.path.join(HERE, "trees.json")))
SOFT = (B.AIR, B.SNOW_LAYER, B.TALLGRASS, B.DOUBLE_PLANT)
GROUND = {B.GRASS, B.DIRT, B.STONE, B.SNOW}


def H(F, x, z):
    return int(F.H[x - F.x0, z - F.z0])


def red(x, z):
    return x + z < -1 or (x + z == -1 and x <= -1)


def plant(w, F, x, z, tree, turn):
    g = H(F, x, z)
    if w.id(x, g, z) not in (B.GRASS, B.DIRT) or w.id(x, g + 1, z) not in SOFT:
        return False
    cells = []
    for dx, dy, dz, i, d in tree["blocks"]:
        for _ in range(turn):
            dx, dz = -dz, dx
        X, Y, Z = x + dx, g + 1 + dy, z + dz
        if not red(X, Z) or not w.inside(X, Y, Z):
            return False
        cur = w.id(X, Y, Z)
        if cur in GROUND or cur == B.COBBLE:
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
    w.set(x, g + 1, z, *[(c[3], c[4]) for c in cells if c[0] == x and c[2] == z and c[1] == g + 1][0]) if any(c[0] == x and c[2] == z and c[1] == g + 1 for c in cells) else None
    return True


def blocked(w, F):
    m = ~F.inside | F.water | F.lake
    for name, (x0, z0, x1, z1) in F.things:
        m[max(0, x0 - 2 - F.x0):x1 + 3 - F.x0, max(0, z0 - 2 - F.z0):z1 + 3 - F.z0] = True
    for r in P.ROUTES:
        d, _ = polyline_distance(F.X, F.Z, r["pts"])
        m |= d < 3
    mx, mz = P.MONUMENT
    m |= np.hypot(F.X - mx, F.Z - mz) < 14            # Holmstein stays open: cover keeps its distance
    bx, bz = P.BEACON
    m |= np.hypot(F.X - bx, F.Z - bz) < 11
    m |= F.angle > 40
    return m


def wood(w, F, zone, kinds, weights, spacing, tries, seed):
    rng = np.random.default_rng(seed)
    pts = np.argwhere(zone & ~F.blocked & F.red)
    rng.shuffle(pts)
    n = 0
    for ix, iz in pts[:tries]:
        x, z = F.x0 + ix, F.z0 + iz
        kind = rng.choice(kinds, p=weights)
        t = TREES[kind][rng.integers(len(TREES[kind]))]
        c = t["crown"] * 0.45
        if any(np.hypot(x - a, z - b) < (c + pc) * spacing for a, b, pc in F.trees):
            continue
        if plant(w, F, x, z, t, int(rng.integers(4))):
            F.trees.append((x, z, c))
            n += 1
    return n


def snow_on_crowns(w, F):
    """Snow caught on the tops of the crowns: a layer on every leaf block the sky can see, most of them."""
    for ix in range(F.nx):
        for iz in range(F.nz):
            if not F.red[ix, iz] or not F.inside[ix, iz]:
                continue
            x, z = F.x0 + ix, F.z0 + iz
            col = w.ids[x - w.x0, :, z - w.z0]
            nz = np.nonzero(col)[0]
            if len(nz) == 0:
                continue
            top = nz[-1]
            if col[top] in (B.LEAVES, B.LEAVES2) and top + 1 < w.sy and RNG.random() < 0.8:
                w.set(x, top + 1, z, B.SNOW_LAYER, 0)


def boulder(w, F, x, z, r, rng):
    g = H(F, x, z)
    for dx in range(-r - 1, r + 2):
        for dz in range(-r - 1, r + 2):
            for dy in range(-1, r + 1):
                d = np.hypot(dx / (r + 0.3), dz / (r * 0.85 + 0.3)) + max(0, dy) / (r * 0.9 + 0.5)
                if d > 1.0 + 0.15 * rng.standard_normal():
                    continue
                X, Y, Z = x + dx, g + dy, z + dz
                if red(X, Z) and w.id(X, Y, Z) in SOFT + (B.GRASS, B.DIRT):
                    q = rng.random()
                    w.set(X, Y, Z, *((B.STONE, 0) if q < 0.5 else (B.STONE, 5) if q < 0.85 else (B.COBBLE, 0)))
            top = g + r
            if red(x + dx, z + dz) and w.id(x + dx, top + 1, z + dz) == B.AIR and w.id(x + dx, top, z + dz) == B.STONE:
                w.set(x + dx, top + 1, z + dz, B.SNOW_LAYER, 0)


def woodpile(w, F, x, z, along_x=True):
    g = H(F, x, z)
    for k in range(4):
        for layer in range(2):
            X, Z = (x + k, z) if along_x else (x, z + k)
            if w.id(X, g + 1 + layer, Z) in SOFT:
                w.set(X, g + 1 + layer, Z, B.LOG, 1 | (8 if along_x else 4))
    X, Z = (x, z - 1) if along_x else (x - 1, z)
    for k in range(4):
        XX, ZZ = (x + k, z - 1) if along_x else (x - 1, z + k)
        if w.id(XX, g + 3, ZZ) == B.AIR:
            pass


def sled(w, F, x, z):
    g = H(F, x, z)
    for k in range(4):
        w.set(x + k, g + 1, z, B.WOOD_SLAB, 1)
        w.set(x + k, g + 1, z + 1, B.WOOD_SLAB, 1)
    w.set(x + 4, g + 1, z, B.SPRUCE_FENCE); w.set(x + 4, g + 1, z + 1, B.SPRUCE_FENCE)
    w.set(x + 1, g + 2, z, B.CHEST, 3); w.set(x + 2, g + 2, z + 1, B.LOG, 1 | 4)


def build(w, F):
    F.blocked = blocked(w, F)
    F.trees = []
    n = 0
    places = dict((p["key"], p) for p in P.PLACES)
    wd = fbm(F.shape, 10, 2, seed=77)
    for key, kinds, weights in (("wood", ["pine", "spruce", "tiny-spruce"], [0.35, 0.45, 0.2]),
                                ("northwood", ["pine", "spruce", "tiny-spruce"], [0.45, 0.35, 0.2])):
        (cx, cz), r = places[key]["at"], places[key]["r"]
        zone = np.hypot(F.X - cx, F.Z - cz) + 3 * wd < r + 4
        n += wood(w, F, zone, kinds, weights, 0.75, 3000, hash(key) % 100)
    # copses on the middle island and round the hall, where the ground is sheltered: a field, not a scatter
    copse = (wd > 0.6) & ((F.X + F.Z) > -60) & ((F.X + F.Z) < -10)
    n += wood(w, F, copse, ["spruce", "tiny-spruce"], [0.6, 0.4], 0.85, 2000, 5)
    behind = (np.hypot(F.X - P.SPAWN[0], F.Z - P.SPAWN[1]) < 26) & ((F.X + F.Z) < -135)
    n += wood(w, F, behind, ["pine", "spruce"], [0.5, 0.5], 0.85, 800, 6)
    print(f"  planted {n} trees")
    snow_on_crowns(w, F)
    rng = np.random.default_rng(9)
    pts = np.argwhere(~F.blocked & F.red & (wd < -0.2))
    rng.shuffle(pts)
    for ix, iz in pts[:16]:
        boulder(w, F, F.x0 + ix, F.z0 + iz, int(rng.integers(1, 3)), rng)
    sx, sz = P.SPAWN
    woodpile(w, F, sx - 8, sz + 7)
    woodpile(w, F, sx + 4, sz + 7)
    sled(w, F, sx + 16, sz + 6)
