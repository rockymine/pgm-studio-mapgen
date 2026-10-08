"""Landforms: operations that shape a heightfield the way the boards shaped theirs by hand.

    X, Z = w.grid()                                   # world x, z of every column
    H = 40 + 12 * noise.fbm(X.shape, 40, 4, seed=3)   # any ground
    H, river = watercourse(H, X, Z, [(-90, -20), (-30, 0), (40, 10), (90, 40)], width=6, depth=2)
    H = canyon(H, X, Z, [(-60, 60), (60, 70)], width=24, depth=14, ledges=3)
    H = butte(H, X, Z, (30, -40), r=10, top=72)
    H, road = grade(H, X, Z, [(-80, 50), (0, 30), (80, 60)], width=5, max_grade=0.2)
    H, sea = coast(H, X, Z, sea=30, outline=[...])

Every function takes the heights H (floats or ints, the y of each column's top) over the world's X and Z and returns
new heights, and where a landform holds water, a description of it. Nothing here is a recipe: the numbers that give
a board its look are the board's, passed in. Each function only cuts or only lifts unless it says otherwise, so they
compose in any order without one undoing another, and the board decides the order.
"""
from dataclasses import dataclass

import numpy as np
from scipy.ndimage import distance_transform_edt

from . import noise
from .noise import smoothstep
from .shapes import polyline, signed_distance


@dataclass
class Water:
    """Where a landform holds water: the cells and the surface y over each (the top water block)."""
    mask: np.ndarray
    surface: np.ndarray
    falls: list = None                    # [(x, z, drop)] where a watercourse steps down


def _sample(H, X, Z, pts, step=1.0):
    """The ground along a path: arc lengths s and the height of the column nearest each sample."""
    x0, z0 = X[0, 0], Z[0, 0]
    segs = list(zip(pts, pts[1:]))
    L = [float(np.hypot(b[0] - a[0], b[1] - a[1])) for a, b in segs]
    s_all, g_all, xz = [], [], []
    acc = 0.0
    for (a, b), l in zip(segs, L):
        n = max(1, int(l / step))
        for t in np.arange(n) / n:
            x, z = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            i = int(np.clip(round(x - x0), 0, H.shape[0] - 1))
            k = int(np.clip(round(z - z0), 0, H.shape[1] - 1))
            s_all.append(acc + t * l)
            g_all.append(float(H[i, k]))
            xz.append((x, z))
        acc += l
    i = int(np.clip(round(pts[-1][0] - x0), 0, H.shape[0] - 1))
    k = int(np.clip(round(pts[-1][1] - z0), 0, H.shape[1] - 1))
    s_all.append(acc); g_all.append(float(H[i, k])); xz.append(pts[-1])
    return np.array(s_all), np.array(g_all), xz


def _downhill(level):
    """A profile that never rises downstream: the running minimum."""
    return np.minimum.accumulate(level)


def watercourse(H, X, Z, pts, width=6, depth=2, water=1, bank=4, fall_min=2, reach_min=10, lowest=None):
    """A river along a path, flowing from its first point to its last: a bed that never climbs, held level in
    reaches and stepping down in falls where the ground drops `fall_min` or more, and only once a reach has run
    `reach_min` blocks. The channel is `width` wide with its floor `depth` under the ground it follows, banks easing
    back to the ground over `bank` blocks, and `water` blocks of water in it. `lowest` holds the bed no lower than
    that (the floor under the sea it runs to). Only cuts. Returns (H, Water)."""
    H = np.asarray(H, float)
    s, g, xz = _sample(H, X, Z, pts)
    want = _downhill(g - depth)
    if lowest is not None:
        want = np.maximum(want, lowest)
    bed = np.empty_like(want)
    level, since, falls = want[0], 0.0, []
    for j in range(len(want)):
        if j and want[j] <= level - fall_min and since >= reach_min:
            falls.append((xz[j][0], xz[j][1], float(level - want[j])))
            level, since = want[j], 0.0
        bed[j] = level
        since += (s[j] - s[j - 1]) if j else 0.0
    bed = np.floor(bed)
    d, along = polyline(X, Z, pts)
    b = np.interp(along, s, bed)
    half = width / 2
    t = smoothstep(half, half + bank, d)
    cut = np.where(d <= half, b, b + t * (H - b))
    Hn = np.where(d <= half + bank, np.minimum(H, cut), H)
    mask = d <= half
    return Hn, Water(mask, np.where(mask, b + water, -1), falls)


def canyon(H, X, Z, pts, width=20, depth=12, floor=0.35, wall=2.5, ledges=0, downhill=False, lowest=None):
    """A canyon along a path: a floor `floor` of the width across and `depth` under the ground it follows (with
    downhill, never climbing along the path, which cuts deeper wherever the ground rises again), walls rising to the rim as (distance across) ** `wall` (higher is steeper and
    more cliff-like), cut in steps of `ledges` blocks if given, its floor no lower than `lowest`. A wash is the same
    with a wide floor, a small depth and a wall of 1. Only cuts."""
    H = np.asarray(H, float)
    s, g, _ = _sample(H, X, Z, pts)
    lvl = g - depth
    if downhill:
        lvl = _downhill(lvl)
    if lowest is not None:
        lvl = np.maximum(lvl, lowest)
    d, along = polyline(X, Z, pts)
    f = np.interp(along, s, lvl)
    half, flat = width / 2, floor * width / 2
    u = np.clip((d - flat) / max(half - flat, 1e-6), 0, 1)
    target = f + (H - f) * u ** wall
    if ledges:
        target = np.where(d <= half, f + np.floor((target - f) / ledges) * ledges, target)
    return np.where(d <= half, np.minimum(H, target), H)


def _radial(X, Z, centre, jag=0.0, cell=6, seed=0):
    d = np.hypot(X - centre[0], Z - centre[1])
    if jag:
        d = d * (1 + jag * noise.fbm(X.shape, cell, 3, seed=seed))
    return d


def spire(H, X, Z, centre, r, top, taper=1.6, jag=0.15, seed=0):
    """A spire: rising from the ground at radius r to `top` at its centre, its sides falling as
    (1 - d / r) ** (1 / taper), so a higher taper is a needle and a lower one a cone. Only lifts."""
    H = np.asarray(H, float)
    d = _radial(X, Z, centre, jag, 4, seed)
    base = float(H[np.unravel_index(np.argmin(np.hypot(X - centre[0], Z - centre[1])), H.shape)])
    rise = (top - base) * np.clip(1 - d / r, 0, 1) ** (1 / taper)
    return np.where(d < r, np.maximum(H, base + rise), H)              # nothing outside its own radius


def butte(H, X, Z, centre, r, top, cliff=1.5, talus=6, talus_height=0.3, jag=0.12, seed=0):
    """A butte or a mesa: a flat top at `top` out to radius r, a cliff `cliff` blocks wide, and a talus apron
    `talus` blocks wide from `talus_height` of the way up the cliff down to the ground. Only lifts."""
    H = np.asarray(H, float)
    d = _radial(X, Z, centre, jag, 8, seed)
    foot = H + (top - H) * talus_height
    shape = np.where(d <= r, top,
                     np.where(d <= r + cliff, foot + (top - foot) * (1 - (d - r) / cliff),
                              foot + (H - foot) * np.clip((d - r - cliff) / max(talus, 1e-6), 0, 1)))
    return np.maximum(H, shape)


def _side(X, Z, pts):
    """Which side of a path each column lies: +1 to the right walking along it (x east, z south), -1 left."""
    best = np.full(X.shape, np.inf)
    side = np.ones(X.shape)
    for a, b in zip(pts, pts[1:]):
        dx, dz = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dz * dz or 1e-9
        t = np.clip(((X - a[0]) * dx + (Z - a[1]) * dz) / L2, 0, 1)
        d = np.hypot(X - (a[0] + t * dx), Z - (a[1] + t * dz))
        cross = dx * (Z - a[1]) - dz * (X - a[0])
        m = d < best
        best = np.where(m, d, best)
        side = np.where(m, np.where(cross >= 0, 1.0, -1.0), side)
    return side, best


def scarp(H, X, Z, pts, height, side=1, cliff=2, talus=5, talus_height=0.3, reach=None):
    """A scarp: the ground on `side` of a path (+1 right walking along it, -1 left) lifted `height`, a cliff
    `cliff` blocks wide on the line and a talus apron below it; `reach` (blocks) lets the lift fade far back from
    the line, so the scarp is a step in the land rather than a wall round the world. Only lifts."""
    H = np.asarray(H, float)
    sd, d = _side(X, Z, pts)
    on = sd == side
    lift = height * (1.0 if reach is None else np.clip(1 - (d - cliff) / reach, 0, 1))
    up = np.where(on, np.where(d <= cliff, lift * (0.5 + 0.5 * d / cliff), lift), 0.0)
    apron = np.where(~on, lift * talus_height * np.clip(1 - d / max(talus, 1e-6), 0, 1), 0.0)
    return np.maximum(H, H + np.maximum(up, apron))


def terraces(H, mask, step=4, base=None, riser=1.0):
    """Ground cut into terraces `step` blocks apart inside mask: each column held to the terrace under it, so a
    slope becomes a flight of level stages with risers between. riser < 1 keeps that much of the slope on each
    terrace instead (0 is level, 1 the slope as it was). Only cuts."""
    H = np.asarray(H, float)
    b = np.min(H[mask]) if base is None else base
    q = b + np.floor((H - b) / step) * step
    t = q + (H - q) * (1 - riser) if riser < 1 else q
    return np.where(mask, np.minimum(H, t), H)


def stage(H, X, Z, centre, rings, jag=0.0, seed=0):
    """A stepped stage: rings [(radius, y)] from the outside in, each a level disc at y, the next one up inside
    it. Lifts and cuts to the given levels inside the outermost ring."""
    H = np.asarray(H, float)
    d = _radial(X, Z, centre, jag, 8, seed)
    out = H.copy()
    for r, y in sorted(rings, key=lambda ry: -ry[0]):
        out = np.where(d <= r, y, out)
    return out


def grade(H, X, Z, pts, width=5, max_grade=0.25, shoulder=4):
    """A route graded into the ground: the ground along the path smoothed so it climbs or falls no more than
    `max_grade` blocks a block, cut and filled to that level `width` wide, with shoulders easing back to the
    ground over `shoulder` blocks. Cuts and fills. Returns (H, level along the path as (s, y) arrays)."""
    H = np.asarray(H, float)
    s, g, _ = _sample(H, X, Z, pts)
    p = g.copy()
    for j in range(1, len(p)):                                   # forward and back: no step steeper than the grade
        dg = max_grade * (s[j] - s[j - 1])
        p[j] = np.clip(p[j], p[j - 1] - dg, p[j - 1] + dg)
    for j in range(len(p) - 2, -1, -1):
        dg = max_grade * (s[j + 1] - s[j])
        p[j] = np.clip(p[j], p[j + 1] - dg, p[j + 1] + dg)
    d, along = polyline(X, Z, pts)
    r = np.round(np.interp(along, s, p))
    half = width / 2
    t = smoothstep(half, half + shoulder, d)
    Hn = np.where(d <= half, r, np.where(d <= half + shoulder, r + t * (H - r), H))
    return Hn, (s, p)


def coast(H, X, Z, sea, outline=None, shelf=10, depth=6, slope=0.35):
    """Land meeting the sea at an outline (a polygon), or at the world's edge when none is given: inland the
    ground eases down to the sea over `shelf` blocks, so the shore is a beach and not a cliff, and nothing inside
    the outline lies under the sea; seaward the floor falls `slope` blocks a block to `depth` under the surface
    at `sea`. Cuts, and lifts low land inside the outline to a block over the sea. Returns (H, Water)."""
    H = np.asarray(H, float)
    if outline is not None:
        sd = signed_distance(X, Z, outline)                         # negative inland
    else:
        x0, x1, z0, z1 = X.min(), X.max(), Z.min(), Z.max()
        sd = -np.minimum.reduce([X - x0, x1 - X, Z - z0, z1 - Z]) + shelf / 2
    inland = np.clip(-sd / shelf, 0, 1)
    land = sea + 1 + (H - sea - 1) * smoothstep(0, 1, inland)
    floor = sea - np.minimum(depth, 1 + slope * np.maximum(sd, 0))
    Hn = np.where(sd < 0, np.maximum(np.minimum(H, land), sea + 1), np.minimum(H, floor))
    mask = Hn < sea
    return Hn, Water(mask, np.where(mask, sea, -1))


def blend(Ha, Hb, mask, width=8):
    """One terrain inside mask and another outside, eased together over `width` blocks inside the mask's edge,
    so a built quarter meets the wild ground without a seam."""
    inside = distance_transform_edt(mask)
    t = np.clip(inside / max(width, 1e-6), 0, 1)
    t = t * t * (3 - 2 * t)
    return np.asarray(Ha, float) * (1 - t) + np.asarray(Hb, float) * t
