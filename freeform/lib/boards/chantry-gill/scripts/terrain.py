"""Chantry Gill's base terrain, stated as a layer document and the grids it reads: the two islands a team, the gill
cut between them, the highlands lifted piece by piece, the Scar's plateau. Nothing built, no water, no dressing.

    document(), arrays()       the document and its grids, for pgmvox.document.layers.build
"""
import math
import os
import sys

import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import layout as L                                                                     # noqa: E402
from pgmvox.geom import noise as N                                                     # noqa: E402

FLOOR = 40                                     # the fell at the front coast
X_RANGE, Z_RANGE = L.X_RANGE, (-130, 129)


def smoothstep(a, b, v):
    t = np.clip((v - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def highland_lift(X, Z, piece, land):
    """Each piece raised to its rise over whatever lower ground it stands on: a scenery piece through a scree slope
    of wandering reach and height into a ragged face, a foothill as a mound eased over ten blocks. A piece's foot is
    the lower ground nearest it, the fell or a foothill, so a height rises out of the foothill in front of it."""
    rise = np.array([r for _, _, r, _ in L.SEEDS], float)
    target = np.where(piece >= 0, rise[np.maximum(piece, 0)], 0.0)
    reach = np.clip(8 + 9 * N.fbm(X.shape, 11, 2, seed=25), 2, 15)
    share = np.clip(0.32 + 0.4 * N.fbm(X.shape, 13, 2, seed=26), 0.05, 0.65)
    jag = 2.5 * N.fbm(X.shape, 4, 2, seed=5)
    out = np.zeros(X.shape)
    for k, (_, _, r, _) in enumerate(L.SEEDS):
        m = piece == k
        if not m.any():
            continue
        lower = (target < r - 2.5) & land                # the void is not lower ground: a height runs to the coast
        d, (ii, kk) = ndimage.distance_transform_edt(~lower, return_indices=True)
        low = target[ii, kk]
        if r > L.SCENERY_RISE:
            p = share * smoothstep(0, reach, d) + (1 - share) * smoothstep(reach + jag - 1, reach + jag + 3, d)
        else:
            p = smoothstep(0, 10, d)
        out = np.where(m, low + (r - low) * p, out)
    # a height is a hill or a plateau, never a needle: its top eased toward the piece's own mean over a few
    # blocks, so a narrow piece comes out a ridge with shoulders rather than a column
    soft = ndimage.gaussian_filter(out, 2.2)
    out = np.where(target > L.SCENERY_RISE, np.minimum(out, soft + 0.35 * (out - soft) + 3), out)
    rough = np.where(target > L.SCENERY_RISE, 1.6 * N.fbm(X.shape, 9, 2, seed=27), 0.6 * N.fbm(X.shape, 9, 2, seed=28))
    return np.where(piece >= 0, np.maximum(out + rough * smoothstep(1, 6, out), 0), 0)


def arrays():
    X, Z = L.grid(X_RANGE, Z_RANGE)
    main, side = L.mask(L.MAIN, X, Z), L.mask(L.SIDE, X, Z)
    gd = L.gill_distance(X, Z)
    wob = 4 * N.fbm(X.shape, 9, 2, seed=33)
    between = (gd < 1) & (Z > 12 + wob) & (Z < 102 + wob) & (X > 18) & (X < 48)
    land = main | side | between
    land = ndimage.binary_fill_holes(ndimage.binary_closing(land, np.ones((9, 9))) | land) & (Z >= 0)
    side = side | (land & ~main & (X > 30))                # what the closing joined east of the gill is the Scar's
    base = FLOOR + 0.05 * np.clip(Z - 14, 0, None) + 1.5 * N.fbm(X.shape, 34, 3, seed=2)
    piece = L.highlands(X, Z)
    high = highland_lift(X, Z, piece, main)
    # the Scar in three storeys: the gill's rim, a bench stepped back where the gill bends away, the plateau
    # behind the upper face, its line slanting to the gill's; all fading out toward the tarn at the front
    zu, xu = [p[1] for p in L.UPPER], [p[0] for p in L.UPPER]
    across = X - np.interp(Z, zu, xu) + 3 * N.fbm(X.shape, 8, 2, seed=30)
    reach = np.clip(5 + 4 * N.fbm(X.shape, 11, 2, seed=31), 2, 9)
    face = 0.3 * smoothstep(-reach, 0, across) + 0.7 * smoothstep(0, 3, across)
    front = smoothstep(24, 46, Z + 4 * N.fbm(X.shape, 12, 2, seed=29))
    bench = L.mask(L.BENCH, X, Z)
    bench_soft = ndimage.gaussian_filter(bench.astype(float), 1.2)
    scar = side * front * np.maximum(L.PLATEAU_RISE * face, L.BENCH_RISE * bench_soft)
    relief = base + high + scar
    # the gill: its walls from the rims down to a floor at 34 over the inner half of its width
    floor = 34.0
    relief = np.where(between, floor + (relief - floor) * smoothstep(0.5, 1.0, gd), relief)
    return {"landmask": land.astype(float), "relief": relief, "piece": piece.astype(float),
            "gill": between.astype(float)}


PAINT = [
    {"block": ["STONE", 5], "slope": [54, None], "noise": {"field": "patch", "lo": 0.15}},
    {"block": "COBBLE", "slope": [60, None], "noise": {"field": "grain", "lo": 0.6}},
    {"block": ["STONE", 0], "slope": [54, None]},
    {"block": "GRAVEL", "slope": [48, 54], "noise": {"field": "scree", "lo": -0.15}},
    {"block": ["STONE", 5], "slope": [48, 54]},
]


def document():
    return {
        "document": "layers", "version": "draft-1",
        "board": {"name": "Chantry Gill", "x": list(X_RANGE), "z": list(Z_RANGE), "floor": FLOOR, "height": 100,
                  "seed": 7, "biome": 1},
        "fields": {"patch": {"fbm": {"cell": 3, "octaves": 2, "seed": 3}},
                   "grain": {"fbm": {"cell": 2, "octaves": 1, "seed": 4}},
                   "scree": {"fbm": {"cell": 6, "octaves": 2, "seed": 27}}},
        "ground": [
            {"id": "land", "op": "outline", "where": {"gt": ["landmask", 0.5]},
             "note": "blue's two islands and the gill between them; red's are their half turn"},
            {"id": "relief", "op": "set", "height": "relief",
             "note": "the fell rising five to the back, the highlands piece by piece, the Scar in three storeys, the gill"},
        ],
        "paint": PAINT,
        "lay": {"soil": [[34, 3], [48, 2], [54, 1]], "ledges": True},
        "symmetry": [{"id": "red", "op": "half", "keep": {"ge": ["z", 0]},
                      "note": "red's half: blue's turned about the middle"}],
    }
