"""Planting and props (red half): the woods of rockymine's oaks and birches planted whole, the knoll's big oak,
the wheat field with its ditches and scarecrow, the Cutting's stumps and log piles, vines down the rift face,
grass and flowers.

The trees are the original board's cut from the tree showcase (its trees.json, read, not copied), planted and
spaced by pgmvox.trees. The field, the Cutting and the ground cover are local.
"""
import os

import numpy as np
from scipy import ndimage

import plan as P
from pgmvox import B, rng
from pgmvox import props, shapes
from pgmvox import trees as T
from pgmvox.noise import fbm

TREES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trees.json")
NATURAL = {B.GRASS, B.DIRT}


def red(x, z):
    """Trees stand on red's half only; the turn writes blue's."""
    return x < -1


def build(w, L):
    trees = T.kinds(T.load(TREES_JSON))
    r = rng(P.BOARD, "dress")
    X, Z = L.X, L.Z
    Xf, Zf = X.astype(float), Z.astype(float)
    route_d = np.full(X.shape, np.inf)
    for rt in L.routes:
        route_d = np.minimum(route_d, shapes.polyline(Xf, Zf, rt["line"])[0] - rt["width"] / 2)
    mon_d = np.min([np.hypot(X - mx, Z - mz) for (mx, mz), _, _ in P.MONUMENTS.values()], axis=0)
    edge_d = ndimage.distance_transform_edt(L.land)
    natural = np.zeros(X.shape, bool)
    for i, k in np.argwhere(L.land):
        x, z = P.X_MIN + int(i), P.Z_MIN + int(k)
        g = w.top(x, z)
        col = w.ids[x - w.x0, g + 1:g + 30, z - w.z0]
        natural[i, k] = w.id(x, g, z) in NATURAL and not np.any((col != 0) & (col != B.TALLGRASS))
    blocked = ~natural | (edge_d < 4) | (route_d < 3)

    planted = []

    def forest(zone, kinds, weights, spacing, seed, tries=4000):
        return T.scatter(w, zone & ~blocked, trees, dict(zip(kinds, weights)), np.random.default_rng(seed),
                         spacing, tries, planted, ok=lambda x, z, t: mon_d[x - P.X_MIN, z - P.Z_MIN] >= 4 + t.crown,
                         allowed=red)

    woods = shapes.inside(Xf, Zf, P.NORTH_WOOD)
    ridge = (X < -101) & ~((X > -110) & (Z > -18) & (Z < 6))
    south_wood = (X < -98) & (Z > 36) & (np.hypot(X + 110, Z - 68) > 9)
    n = forest(woods & ~ridge, ["oak", "birch", "tiny-oak"], [0.22, 0.43, 0.35], 0.85, 1)
    n += forest(ridge & ~south_wood, ["birch", "oak", "tiny-oak"], [0.45, 0.2, 0.35], 0.85, 2)
    n += forest(south_wood, ["oak", "birch", "tiny-oak"], [0.25, 0.4, 0.35], 0.85, 3)
    n += forest(np.abs(np.hypot(X + 110, Z - 68) - 11) < 2, ["tiny-oak", "birch"], [0.6, 0.4], 0.8, 4)
    if T.plant(w, -22, 74, trees["big-oak"][1], 1, red):
        n += 1
    for (x, z, kind, i) in ((-22, -24, "tiny-oak", 2), (-36, -84, "oak", 6), (-70, 4, "birch", 3),
                            (-28, 20, "birch", 1), (-20, 24, "birch", 4), (-44, 18, "birch", 7),
                            (-68, 78, "oak", 8), (-90, 80, "tiny-oak", 3), (-80, -36, "oak", 7), (-82, 30, "birch", 2)):
        t = trees[kind][i % len(trees[kind])]
        ii, kk = x - P.X_MIN, z - P.Z_MIN
        if mon_d[ii, kk] >= 4 + t.crown and not blocked[ii, kk] and T.plant(w, x, z, t, i % 4, red):
            n += 1

    # the wheat field: strips of wheat, carrots and potatoes on farmland, a ditch every ninth row, a fence
    x0, z0, x1, z1 = P.FIELD
    base = int(np.median(L.H[x0 - P.X_MIN:x1 - P.X_MIN + 1, z0 - P.Z_MIN:z1 - P.Z_MIN + 1]))
    crops = [(B.WHEAT, 7), (B.WHEAT, 7), (B.WHEAT, 6), (B.CARROTS, 7), (B.WHEAT, 7), (B.POTATOES, 7)]
    props.crop_field(w, (x0, z0, x1, z1), base, crops, r, rows=9, ditch=4, tilt=0.06, fence="w")
    props.scarecrow(w, (x0 + x1) // 2 + 1, (z0 + z1) // 2 - 3, facing="e")     # facing the rift

    # the Cutting: stumps and two log piles
    for _ in range(14):
        a, d = r.uniform(0, 2 * np.pi), r.uniform(0, 7)
        x, z = int(round(-110 + d * np.cos(a))), int(round(68 + d * np.sin(a)))
        g = w.top(x, z)
        if w.id(x, g, z) in NATURAL and w.id(x, g + 1, z) == B.AIR:
            w.set(x, g + 1, z, B.LOG, 0 if r.random() < 0.6 else 1)
    for (px, pz) in ((-106, 64), (-113, 72)):
        g = w.top(px, pz)
        for dz in range(3):
            for dy in range(2 if dz else 3):
                for dx in range(5):
                    w.set(px + dx, g + 1 + dy, pz + dz, B.LOG, 4 | (dx % 2))

    # the rift face: vines hanging from the lip
    for k in range(L.H.shape[1]):
        xs = np.nonzero(L.land[:, k])[0]
        if len(xs) == 0 or L.water[xs.max(), k]:
            continue
        x, z = P.X_MIN + int(xs.max()), P.Z_MIN + k
        tp = w.top(x, z)
        if r.random() < 0.35:
            for y in range(tp - int(r.integers(3, 12)), tp):
                if w.id(x + 1, y, z) == B.AIR and w.id(x, y, z) != B.AIR:
                    w.set(x + 1, y, z, B.VINE, 2)

    # grass, ferns and flowers on bare grass: sparse in the open, fuller in the woods, flowers in drifts
    dens, flowers, ftype = fbm(X.shape, 9, 2, seed=81), fbm(X.shape, 14, 2, seed=82), fbm(X.shape, 30, 1, seed=83)
    for i, k in np.argwhere(L.land):
        x, z = P.X_MIN + int(i), P.Z_MIN + int(k)
        g = w.top(x, z)
        if w.id(x, g, z) != B.GRASS or w.id(x, g + 1, z) != B.AIR or mon_d[i, k] < 2:
            continue
        wood = L.forest[i, k]
        p = (0.30 if wood else 0.07) * (0.6 + dens[i, k])
        c = r.random()
        if flowers[i, k] > 0.6 and not wood and c < 0.18:
            t = ftype[i, k]
            w.set(x, g + 1, z, *((B.DANDELION, 0) if t < -0.3 else (B.FLOWER, 3) if t < 0 else (B.FLOWER, 8) if t < 0.3 else (B.FLOWER, 0)))
        elif c < p:
            w.set(x, g + 1, z, B.TALLGRASS, 2 if wood and r.random() < 0.45 else 1)
    return dict(trees=n)
