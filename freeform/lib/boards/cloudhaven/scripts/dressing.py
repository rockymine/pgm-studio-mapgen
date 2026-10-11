"""Planting on red's half of Cloudhaven: willows on the rims, where their crowns trail over the edge, and
dense oaks inland; none on bridges or by buildings, and no crown within five blocks of a monument."""
import json
import os

import numpy as np

import plan as P
from mc import B

HERE = os.path.dirname(os.path.abspath(__file__))
TREES = json.load(open(os.path.join(HERE, "trees.json")))
SOFT = (B.AIR, B.TALLGRASS, B.FLOWER, B.DANDELION, B.VINE)


KEEP_RIM, KEEP_INNER = 0.05, 0.015      # the share of candidates kept: 36 trees on red's half before the playtest, 16 now


def plant(w, F, x, z, tree, turn):
    g = int(F.H[x - F.x0, z - F.z0])
    if w.id(x, g, z) != B.GRASS or w.id(x, g + 1, z) not in SOFT:
        return False
    cells = []
    for dx, dy, dz, i, d in tree["blocks"]:
        for _ in range(turn):
            dx, dz = -dz, dx
        X, Y, Z = x + dx, g + 1 + dy, z + dz
        if X >= 0 or not w.inside(X, Y, Z):
            return False
        cur = w.id(X, Y, Z)
        if cur in (B.GRASS, B.DIRT, B.STONE):
            continue
        if cur not in SOFT and cur not in (B.LEAVES, B.LEAVES2):
            return False
        if (X, Z) in F.bridge_cells or (X, Z) in F.ship_cells:
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
    F.trees = []
    blocked = np.zeros(F.shape, bool)
    for name, (x0, z0, x1, z1) in F.things:
        blocked[max(0, x0 - 2 - F.x0):x1 + 3 - F.x0, max(0, z0 - 2 - F.z0):z1 + 3 - F.z0] = True
    for x, z in F.bridge_cells | F.ship_cells:
        blocked[max(0, x - 2 - F.x0):x + 3 - F.x0, max(0, z - 2 - F.z0):z + 3 - F.z0] = True
    for (mx, my, mz) in (F.mon_a, F.mon_b):
        blocked |= np.hypot(F.X - mx, F.Z - mz) < 7
    # how far in from the rim each cell is
    from scipy.ndimage import distance_transform_edt
    inward = distance_transform_edt(F.land)
    rng = np.random.default_rng(31)
    ok = F.land & ~blocked & F.red & np.array([[not k.startswith("debris") for k in row] for row in F.key])
    pts = np.argwhere(ok)
    rng.shuffle(pts)
    n = 0
    per = {}
    for ix, iz in pts:
        x, z = F.x0 + ix, F.z0 + iz
        rim = inward[ix, iz] < 3.5
        if rng.random() > (KEEP_RIM if rim else KEEP_INNER):
            continue                        # thinned after the playtest: the floor shows, the edges keep their trees
        kind = "willow" if rim else ("dense-oak" if rng.random() < 0.6 else "small-dense-oak")
        if F.key[ix, iz] == "gardens" and rng.random() < 0.7:
            kind = "willow"
        t = TREES[kind][rng.integers(len(TREES[kind]))]
        c = t["crown"] * 0.42
        if any(np.hypot(x - mx, z - mz) < t["crown"] + 5 for (mx, my, mz) in (F.mon_a, F.mon_b)):
            continue                        # a crown keeps five blocks off a monument
        if any(np.hypot(x - a, z - b) < (c + pc) for a, b, pc in F.trees):
            continue
        if plant(w, F, x, z, t, int(rng.integers(4))):
            F.trees.append((x, z, c))
            n += 1
            per[F.key[ix, iz]] = per.get(F.key[ix, iz], 0) + 1
    print(f"  planted {n} trees; per island {dict(sorted(per.items()))}")
