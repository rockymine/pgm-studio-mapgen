"""Blastworks' natural ground: the spawn and the front, solid to the bottom like every piece of the board, their tops
real ground and their sides cliffs of stone and diorite.

    ground(w, rect, base, joins, flats, seed)   lay one piece; returns its heights
    green(w, rect, H, keep, seed)               grass, ferns, a few small spruces and boulders on it

**Ground meets a made piece at the piece's own height.** `joins` are (rect, height): every column within three of
the rect is pulled to that height, the nearer the harder, so a stair, a lane or the descent steps onto ground that
lies level with it. `flats` are (rect, height) laid dead level: a monument's slot. `skip` are rects the ground
leaves to a made piece standing in it, which it meets at whatever height it has there.
"""
import numpy as np

from pgmvox import B
from pgmvox.geom import noise
from pgmvox.geom.shapes import edge_depth
from pgmvox.scenery import green as G, trees
from pgmvox.surface import terrain as T

ROCK = T.Strata([((B.STONE, 0), 5, 4), ((B.STONE, 3), 2, 2), ((B.STONE, 0), 3, 3), ((B.COBBLE, 0), 0.4, 1)], seed=8)


def _dist_to(rect, X, Z):
    x0, z0, x1, z1 = rect
    dx = np.maximum(np.maximum(x0 - X, X - x1), 0)
    dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
    return np.maximum(dx, dz)


def ground(w, rect, base, joins=(), flats=(), seed=1, relief=1.6, skip=()):
    x0, z0, x1, z1 = rect
    X, Z = w.grid()
    whole = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
    land = whole.copy()
    for r in skip:
        land &= _dist_to(r, X, Z) > 0
    n = noise.fbm(X.shape, 8, 3, seed=seed)
    H = base + relief * n
    for r, h in joins:
        d = _dist_to(r, X, Z)
        t = np.clip(d / 4.0, 0, 1)
        H = np.where(d <= 4, h * (1 - t) + H * t, H)
    for r, h in flats:
        H = np.where(_dist_to(r, X, Z) == 0, h, H)
    H = np.where(land, np.round(H), 0).astype(int)
    ed = edge_depth(whole)
    rng = np.random.default_rng(seed)
    joined = np.zeros_like(land)
    for r, _ in list(joins) + list(flats):
        joined |= _dist_to(r, X, Z) <= 1
    crag = land & (ed <= 1) & ~joined & (noise.fbm(X.shape, 3, 2, seed=seed + 4) > 0.35)
    H = np.where(crag, H - 1 - (noise.fbm(X.shape, 2, 1, seed=seed + 5) > 0.5), H)   # a broken rim, here and there
    for i, k in np.argwhere(land):
        h = int(H[i, k])
        soil = 1 if ed[i, k] <= 1 else 2 if ed[i, k] <= 3 else 3
        for y in range(1, h - soil + 1):
            w.ids[i, y, k], w.dat[i, y, k] = ROCK(y)
        for y in range(h - soil + 1, h):
            w.ids[i, y, k], w.dat[i, y, k] = B.DIRT, 0
        w.ids[i, h, k], w.dat[i, h, k] = B.GRASS, 0
        w.ids[i, 0, k], w.dat[i, 0, k] = B.BEDROCK, 0              # the concept's floor
        if ed[i, k] == 0:                                  # the face weathered: notches and moss in the rock
            for y in range(3, h - 2):
                r = rng.random()
                if r < 0.05:
                    w.ids[i, y, k], w.dat[i, y, k] = B.MOSSY, 0
                elif r < 0.09:
                    w.ids[i, y, k], w.dat[i, y, k] = B.STONE, 3
    worn = land & (noise.fbm(X.shape, 4, 2, seed=seed + 6) > 0.55) & (ed > 1)
    for i, k in np.argwhere(worn):                         # coarse dirt where the ground is trodden
        w.ids[i, int(H[i, k]), k], w.dat[i, int(H[i, k]), k] = B.DIRT, 1
    return H


def green(w, rect, H, keep=(), seed=1, spruces=4, boulders=2):
    """Plants on a piece, never within two of a rect in `keep` (paths, the yard, the slot, the joins)."""
    x0, z0, x1, z1 = rect
    X, Z = w.grid()
    land = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
    free = land & (edge_depth(land) > 1)
    for r in keep:
        free &= _dist_to(r, X, Z) > 2
    rng = np.random.default_rng(seed)
    by = trees.kinds(trees.library())
    if spruces:
        trees.scatter(w, free, by, {"tiny-spruce": 1}, rng, tries=spruces * 6, spacing=1.8)
    cells = np.argwhere(free)
    rng.shuffle(cells)
    for i, k in cells[:boulders]:
        G.boulder(w, int(X[i, k]), int(Z[i, k]), lambda x, z: w.top(x, z), 1.3 + rng.random(), rng,
                  rock=((B.STONE, 0), (B.STONE, 3)), accent=(B.MOSSY, 0))
    G.ground_cover(w, [(int(X[i, k]), int(H[i, k]), int(Z[i, k])) for i, k in np.argwhere(free)
                       if rng.random() < 0.35], rng, {"grass": 6, "fern": 3, "large_fern": 1})
