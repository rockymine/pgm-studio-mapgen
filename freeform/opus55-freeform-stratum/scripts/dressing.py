"""The land's woods, and the city's few living things: oak and birch in the swathes the noise gathers into
woods, lilies on the lake."""
import json
import os

import numpy as np

from mc import B

HERE = os.path.dirname(os.path.abspath(__file__))
TREES = json.load(open(os.path.join(HERE, "trees.json")))
SOFT = (B.AIR, B.TALLGRASS, B.FLOWER, B.DANDELION)


def plant(w, F, x, z, tree, turn):
    g = int(F.H[x - F.x0, z - F.z0])
    if w.id(x, g, z) not in (B.GRASS, B.DIRT) or w.id(x, g + 1, z) not in SOFT:
        return False
    cells = []
    for dx, dy, dz, i, d in tree["blocks"]:
        for _ in range(turn):
            dx, dz = -dz, dx
        X, Y, Z = x + dx, g + 1 + dy, z + dz
        if X >= 0 or not w.inside(X, Y, Z) or Y > 42:
            return False
        cur = w.id(X, Y, Z)
        if cur in (B.GRASS, B.DIRT, B.STONE):
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


def build(w, F):
    rng = np.random.default_rng(3)
    F.trees = []
    pts = np.argwhere((F.wood > 0.25) & F.red & ~F.lake & ~F.shore & (F.angle < 40))
    rng.shuffle(pts)
    n = 0
    for ix, iz in pts:
        x, z = F.x0 + ix, F.z0 + iz
        kind = "birch" if F.band[ix, iz] % 2 else ("oak" if rng.random() < 0.6 else "tiny-oak")
        t = TREES[kind][rng.integers(len(TREES[kind]))]
        c = t["crown"] * 0.5
        if any(abs(x - a) < c + p and abs(z - b) < c + p and np.hypot(x - a, z - b) < c + p for a, b, p in F.trees):
            continue
        if plant(w, F, x, z, t, int(rng.integers(4))):
            F.trees.append((x, z, c))
            n += 1
    lil = 0
    for ix, iz in zip(*np.nonzero(F.lake & F.red & (F.sd > -3))):
        if rng.random() < 0.06:
            x, z = F.x0 + ix, F.z0 + iz
            if w.id(x, 16 + 1, z) == B.AIR:
                w.set(x, 17, z, B.LILY)
                lil += 1
    print(f"  planted {n} trees, {lil} lilies")
