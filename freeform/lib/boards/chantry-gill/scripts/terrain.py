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
    ptop = base + L.PLATEAU_RISE
    brow_fade = smoothstep(46, 58, Z) * (1 - smoothstep(92, 102, Z))
    benchd = ndimage.binary_dilation(bench, iterations=2)
    brow = (across > -reach * brow_fade) & (across < 3) & (brow_fade > 0.25) & land & (benchd | (across > 0))
    lab, n = ndimage.label(brow)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    brow = np.isin(lab, [k + 1 for k, sz in enumerate(sizes) if sz >= 30])     # no stray blocks in the air
    return {"brow": brow.astype(float), "landmask": land.astype(float), "relief": relief, "piece": piece.astype(float),
            "gill": between.astype(float), "across": across, "reach": reach * brow_fade, "ptop": ptop,
            "brow_fade": brow_fade, "bench": ndimage.binary_dilation(bench, iterations=2).astype(float)}


def bank(grids, x, z):
    """The ground at (x, z) on the board's grid, from the relief."""
    return float(grids["relief"][x - X_RANGE[0], z - Z_RANGE[0]])


def crossing(grids, z, x0, x1):
    """Where the gill is crossed along row z between x0 and x1: (west rim x, east rim x, rim height) - the last
    column at each side before the ground falls under the rims' height by two."""
    hs = [(x, bank(grids, x, z)) for x in range(x0, x1 + 1)]
    deep = [x for x, h in hs if h < 38]
    w, e = min(deep), max(deep)
    rim = round(max(bank(grids, w - 2, z), bank(grids, e + 2, z)))
    return w - 1, e + 1, rim


PAINT = [
    {"block": ["STONE", 5], "slope": [54, None], "noise": {"field": "patch", "lo": 0.15}},
    {"block": "COBBLE", "slope": [60, None], "noise": {"field": "grain", "lo": 0.6}},
    {"block": ["STONE", 0], "slope": [54, None]},
    {"block": "GRAVEL", "slope": [48, 54], "noise": {"field": "scree", "lo": -0.15}},
    {"block": ["STONE", 5], "slope": [48, 54]},
]


TARN = [[47, 27], [56, 23], [67, 25], [73, 32], [70, 42], [58, 46], [49, 40]]
BECK = [[37, 96], [36, 90], [30, 78], [37, 64], [28, 50], [35, 36], [31, 28], [40, 31], [52, 32]]


def document(grids=None):
    grids = grids or arrays()
    bw, be, brim = crossing(grids, 38, 14, 50)
    tw, te, trim = crossing(grids, 92, 20, 52)
    # the timber bridge climbs from the fell's rim to the bench's, a stair on every rise
    hw, he = round(bank(grids, tw - 1, 92)), round(bank(grids, te + 1, 92))
    timber = []
    span = list(range(tw - 1, te + 2))
    for j, x in enumerate(span):
        y = round(hw + (he - hw) * j / max(len(span) - 1, 1))
        nxt = round(hw + (he - hw) * (j + 1) / max(len(span) - 1, 1))
        timber.append({"box": [x, y, 91, x, y, 94], "block": ["PLANKS", 1]})
        if nxt > y and j + 1 < len(span):
            timber.append({"box": [x, y + 1, 92, x, y + 1, 93], "block": ["SPRUCE_STAIRS", 0]})
        timber += [{"box": [x, y + 1, 91, x, y + 1, 91], "block": "SPRUCE_FENCE"},
                   {"box": [x, y + 1, 94, x, y + 1, 94], "block": "SPRUCE_FENCE"}]
        if (x - tw) % 4 == 2 and tw < x < te:
            timber.append({"box": [x, 35, 91, x, y - 1, 91], "block": ["LOG", 1]})
            timber.append({"box": [x, 35, 94, x, y - 1, 94], "block": ["LOG", 1]})
    trim = f"{hw} to {he}"
    doc = _document()
    doc["volume"] = [
        {"id": "brig", "op": "arch", "line": {"pts": [[bw - 1, 38], [be + 1, 38]], "spline": False}, "width": 5,
         "deck": [brim + 1, brim, 2], "camber": 0, "thick": [2, 9, 2.5], "clear": 3, "top": "GRAVEL",
         "under": "STONE", "rock": "STONE", "note": f"the brig: a stone arch over the gill, x {bw} to {be}, deck at {brim}"}]
    doc["build"] = [{"id": "chimney-foot", "op": "blocks", "boxes": [{"box": [49, 35, 76, 49, 37, 76], "block": "STONE"}],
                     "note": "rock behind the chimney ladder's foot, where the shelter opened the shaft's wall"},
                    {"id": "back-bridge", "op": "blocks", "boxes": timber,
                     "note": f"a timber bridge over the gill behind the brow, x {tw} to {te}, its deck at {trim}"}]
    return doc


def _document():
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
            {"id": "tarn", "op": "crater", "floor": 30, "flat": 3, "slope": 0.5, "melt": 5,
             "areas": [{"polygon": TARN, "rough": {"amp": 0.12, "cell": 5, "seed": 7}}],
             "note": "the tarn's bowl on the Scar's front"},
            {"id": "shore", "op": "level", "mode": "cut", "top": 36, "inner": 0.5, "outer": 1.6,
             "areas": [{"ellipse": {"at": [60, 22], "rx": 16, "rz": 7}, "rough": {"amp": 0.1, "cell": 6, "seed": 14}}],
             "note": "the ground let down to the tarn's north shore, where the beach is"},
            {"id": "beck", "op": "river", "line": BECK, "width": 4, "depth": 1, "water": 1, "bank": 1,
             "note": "the beck: rising at the gill's head, down its floor, turning east through its mouth into the tarn"},
            {"id": "tarn-water", "op": "water", "level": 34,
             "where": {"and": [{"lt": ["H", 34]}, {"lt": [{"distance": {"polygon": TARN}}, 1.3]}]}},
        ],
        "paint": [{"block": "SAND", "slope": [None, 30], "height": [None, 35],
                   "area": {"polygon": TARN, "plus": -0.12}, "note": "the beach at the water's edge"},
                  {"block": "SAND", "slope": [None, 24], "height": [None, 36],
                   "area": {"polygon": TARN, "plus": -0.08}, "noise": {"field": "patch", "lo": 0.1}},
                  {"block": "GRAVEL", "slope": [None, 30], "area": {"line": {"near": "beck", "width": 7}},
                   "noise": {"field": "patch", "lo": 0}}] + PAINT,
        "water": {"bed": [{"block": "GRAVEL", "noise": {"field": "patch", "lo": 0.1}}, {"block": "CLAY"}]},
        "levels": [
            {"id": "brow", "floor": 58,
             "ground": [{"id": "brow-outline", "op": "outline",
                         "where": {"gt": ["brow", 0.5]}},
                        {"id": "brow-ground", "op": "set", "height": "ptop"}],
             "paint": [{"block": ["STONE", 5], "noise": {"field": "patch", "lo": 0.2}}, {"block": ["STONE", 0]}],
             "soil": 0,
             "underside": {"bottom": {"sub": ["ptop", {"add": [2, {"mul": [2.0, {"add": ["reach", "across"]}]}]}]},
                           "clear": 2},
             "note": "the upper face's brow, leaning out over the bench a block for every two up"}],
        "carve": [
            {"id": "shelter", "op": "tunnel", "mouths": [0], "cover": 2,
             "pts": [[39, 35, 73, 3.0], [43, 35, 74, 4.0], [46, 35, 76, 3.2]],
             "dress": {"seed": 12, "stalagmites": 30, "ores": 20},
             "note": "the shelter worn into the gill's east wall under the bench"},
            {"id": "chimney", "op": "shaft", "at": [47, 76], "bottom": 35, "top": "ground", "ladder_on": "e",
             "wall": "STONE", "post": "STONE", "note": "a chimney from the shelter up onto the bench, a ladder in it"}],
        "lay": {"soil": [[34, 3], [48, 2], [54, 1]], "ledges": True},
        "symmetry": [{"id": "red", "op": "half", "keep": {"ge": ["z", 0]},
                      "note": "red's half: blue's turned about the middle"}],
    }
