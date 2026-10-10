"""Landforms: operations that shape a heightfield the way the boards shaped theirs by hand.

    X, Z = w.grid()                                   # world x, z of every column
    H = 40 + 12 * noise.fbm(X.shape, 40, 4, seed=3)   # any ground
    H, river = watercourse(H, X, Z, [(-90, -20), (-30, 0), (40, 10), (90, 40)], width=6, depth=2)
    H = canyon(H, X, Z, [(-60, 60), (60, 70)], width=24, depth=14, ledges=3)
    H = butte(H, X, Z, (30, -40), r=10, top=72)
    H, road = grade(H, X, Z, [(-80, 50), (0, 30), (80, 60)], width=5, max_grade=0.2)
    H, sea = coast(H, X, Z, sea=30, outline=[...])
    H = profile(H, d, floor=41, steps=[Step(26, 34, 57), Step(46, 63, 74)], jag=jag)   # a canyon's cross-section

Every function takes the heights H (floats or ints, the y of each column's top) over the world's X and Z and returns
new heights, and where a landform holds water, a description of it. Nothing here is a recipe: the numbers that give
a board its look are the board's, passed in. Each function only cuts or only lifts unless it says otherwise, so they
compose in any order without one undoing another, and the board decides the order.
"""
from dataclasses import dataclass

import numpy as np
from scipy import ndimage

from . import noise
from .noise import smoothstep
from .shapes import distance_in, polyline, signed_distance


MODES = ("set", "lift", "cut")


def _apply(H, shaped, mode):
    """What an op that shapes ground does to it: replaces it (`set`), only raises it (`lift`), only lowers it (`cut`)."""
    assert mode in MODES, mode
    if mode == "lift":
        return np.maximum(H, shaped)
    if mode == "cut":
        return np.minimum(H, shaped)
    return shaped


@dataclass
class Step:
    """One cliff of a cross-section and the ground past it: from `start` to `end` blocks out the ground eases
    (smoothstep) from the level before it to `top`, and from `end` on it is `ground`, `top` where none is given.
    `top` is the cliff's nominal height; `ground` (a field, or "ground" for the ground the cross-section is laid
    on) is what the flat past it is, noise and all."""
    start: object
    end: object
    top: object
    ground: object = None


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


def watercourse(H, X, Z, pts, width=6, depth=2, water=1, bank=4, fall_min=2, reach_min=10, lowest=None, into=None):
    """A river along a path, flowing from its first point to its last: a bed that never climbs, held level in
    reaches and stepping down in falls where the ground drops `fall_min` or more, and only once a reach has run
    `reach_min` blocks. The channel is `width` wide with its floor `depth` under the ground it follows, banks easing
    back to the ground over `bank` blocks from the water's surface, and `water` blocks of water in it. `lowest` holds
    the bed no lower than that: a river running into a sea or a lake takes lowest = its surface - water, so its last
    reach arrives at that level. It only cuts, except the ring of cells beside the water, which is raised to the
    surface where the ground there is lower, so no water stands over its bank. `into` is the Water it runs into (a
    lake, a sea), whose cells get no bank. Returns (H, Water)."""
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
    b = np.floor(np.interp(along, s, bed))
    half = width / 2
    surf = b + water
    mask = d <= half
    t = smoothstep(half, half + bank, d)
    cut = np.where(mask, b, surf + t * (H - surf))                  # banks rise from the water's surface
    Hn = np.where(d <= half + bank, np.minimum(H, cut), H)
    held = ndimage.maximum_filter(np.where(mask, surf, -np.inf), size=3)
    lip = ~mask & np.isfinite(held)                                 # every cell beside water is at least as high
    if into is not None:
        lip &= ~into.mask
    Hn = np.where(lip, np.maximum(Hn, held), Hn)                    # as the highest water next to it
    return Hn, Water(mask, np.where(mask, surf, -1), falls)


def lake(H, X, Z, centre, r, level, depth=3, shore=3, rz=None, jag=0.2, seed=0):
    """A lake: an outline r across (rz the other way) about centre, broken by `jag`, holding water to `level`. Its
    bed lies `depth` under the level in the middle and rises to a block under it at the edge; the ground within
    `shore` blocks outside is held at the level or above, rising back to the ground, so no water stands against air.
    Returns (H, Water)."""
    H = np.asarray(H, float)
    cx, cz = centre
    rz = r if rz is None else rz
    e = np.hypot((X - cx) / r, (Z - cz) / rz) * (1 + jag * noise.fbm(X.shape, 6, 3, seed=seed))
    mask = e <= 1
    bed = np.floor(level - 1 - (depth - 1) * np.clip(1 - e, 0, 1) ** 0.6)
    Hn = np.where(mask, np.minimum(H, bed), H)
    d = distance_in(~mask, "euclid")
    t = smoothstep(0, shore, d)
    rim = ~mask & (d <= shore)
    Hn = np.where(rim, np.maximum(H, level) * (1 - t) + H * t, Hn)   # the shore eases from the level to the ground
    Hn = np.where(rim & (d <= 1.5), np.maximum(Hn, level), Hn)      # and the cells beside the water hold it
    return Hn, Water(mask, np.where(mask, float(level), -1), [])


def hold(H, *waters):
    """Raise every dry cell beside water to that water's surface, so nothing laid after a river or a lake (a road
    graded down to a bridge, a path) leaves water standing over its bank. Call it last, with every Water."""
    H = np.asarray(H, float)
    wet = np.zeros(H.shape, bool)
    level = np.full(H.shape, -np.inf)
    for wat in waters:
        wet |= wat.mask
        level = np.maximum(level, np.where(wat.mask, wat.surface, -np.inf))
    near = ndimage.maximum_filter(level, size=3)
    return np.where(~wet & np.isfinite(near), np.maximum(H, near), H)


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


def _radial(X, Z, centre, jag=0.0, cell=6, seed=0, stretch=None, angle=0.0):
    """Distance from `centre` in blocks of the x radius: with `stretch` (z radius over x radius) and `angle`
    (degrees from east toward south) an ellipse's, otherwise a circle's; `jag` roughens it."""
    if stretch is None and not angle:
        d = np.hypot(X - centre[0], Z - centre[1])
    else:
        dx, dz = X - centre[0], Z - centre[1]
        if angle:
            a = np.radians(angle)
            dx, dz = dx * np.cos(a) + dz * np.sin(a), -dx * np.sin(a) + dz * np.cos(a)
        d = np.hypot(dx, dz / (stretch or 1.0))
    if jag:
        d = d * (1 + jag * noise.fbm(X.shape, cell, 3, seed=seed))
    return d


def spire(H, X, Z, centre, r, top, taper=1.6, jag=0.15, seed=0, rz=None, angle=0.0):
    """A spire: rising from the ground at radius r to `top` at its centre, its sides falling as
    (1 - d / r) ** (1 / taper), so a higher taper is a needle and a lower one a cone. With `rz` its foot is an
    ellipse, r across x and rz across z, turned `angle` degrees. Only lifts."""
    H = np.asarray(H, float)
    d = _radial(X, Z, centre, jag, 4, seed, None if rz is None else rz / r, angle)
    base = float(H[np.unravel_index(np.argmin(np.hypot(X - centre[0], Z - centre[1])), H.shape)])
    rise = (top - base) * np.clip(1 - d / r, 0, 1) ** (1 / taper)
    return np.where(d < r, np.maximum(H, base + rise), H)              # nothing outside its own radius


def butte(H, X, Z, centre, r, top, cliff=1.5, talus=6, talus_height=0.3, jag=0.12, seed=0, rz=None, angle=0.0):
    """A butte or a mesa: a flat top at `top` out to radius r, a cliff `cliff` blocks wide, and a talus apron
    `talus` blocks wide from `talus_height` of the way up the cliff down to the ground. With `rz` its top is an
    ellipse, r across x and rz across z, turned `angle` degrees. Only lifts."""
    H = np.asarray(H, float)
    d = _radial(X, Z, centre, jag, 8, seed, None if rz is None else rz / r, angle)
    foot = H + (top - H) * talus_height
    shape = np.where(d <= r, top,
                     np.where(d <= r + cliff, foot + (top - foot) * (1 - (d - r) / cliff),
                              foot + (H - foot) * np.clip((d - r - cliff) / max(talus, 1e-6), 0, 1)))
    return np.maximum(H, shape)


def scarp(H, X, Z, pts, height, side=1, cliff=2, talus=5, talus_height=0.3, reach=None):
    """A scarp: the ground on `side` of a path (+1 right walking along it, -1 left) lifted `height`, a cliff
    `cliff` blocks wide on the line and a talus apron below it; `reach` (blocks) lets the lift fade far back from
    the line, so the scarp is a step in the land rather than a wall round the world. Only lifts."""
    H = np.asarray(H, float)
    d, _, sd = polyline(X, Z, pts, side=True)
    on = sd == side
    lift = height * (1.0 if reach is None else np.clip(1 - (d - cliff) / reach, 0, 1))
    up = np.where(on, np.where(d <= cliff, lift * (0.5 + 0.5 * d / cliff), lift), 0.0)
    apron = np.where(~on, lift * talus_height * np.clip(1 - d / max(talus, 1e-6), 0, 1), 0.0)
    return np.maximum(H, H + np.maximum(up, apron))


def terraces(H, mask, step=4, base=None, riser=1.0):
    """Ground cut into terraces `step` blocks apart inside mask: each column held to the terrace under it, so a
    slope becomes a flight of level stages with risers between. riser < 1 keeps some of the slope on each
    terrace instead: 1 is level, 0 the slope as it was. Only cuts."""
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


def grade(H, X, Z, pts, width=5, max_grade=0.25, shoulder=4, water=None, keep=None):
    """A route graded into the ground: the ground along the path smoothed so it climbs or falls no more than
    `max_grade` blocks a block, cut and filled to that level `width` wide, with shoulders easing back to the
    ground over `shoulder` blocks. Over `water` (a mask) the ground is not followed: the level runs on from bank
    to bank, which is a bridge deck's, and the water is neither cut nor filled. Ground in `keep` (roads already
    graded) is left as it is, and the route's ends hold the ground they stand on, so a branch meets the road it
    joins at that road's level; where the grade cannot join the two, the last point's ground wins, which is the
    end a network branch joins by. Cuts and fills. Returns (H, (s, level)), the level along the path by arc length."""
    H = np.asarray(H, float)
    s, g, xz = _sample(H, X, Z, pts)
    if water is not None:
        x0, z0 = X[0, 0], Z[0, 0]
        wet = np.array([bool(water[int(np.clip(round(x - x0), 0, H.shape[0] - 1)),
                                   int(np.clip(round(z - z0), 0, H.shape[1] - 1))]) for x, z in xz])
        if wet.any() and (~wet).any():
            g = np.where(wet, np.interp(s, s[~wet], g[~wet]), g)
    p = g.copy()
    for j in range(1, len(p)):                                   # forward and back: no step steeper than the grade
        dg = max_grade * (s[j] - s[j - 1])
        p[j] = np.clip(p[j], p[j - 1] - dg, p[j - 1] + dg)
    for j in range(len(p) - 2, -1, -1):
        dg = max_grade * (s[j + 1] - s[j])
        p[j] = np.clip(p[j], p[j + 1] - dg, p[j + 1] + dg)
    for end in (0, -1):                                          # the ends hold their ground, eased in
        p = _pin(p, s, end, g[end], max_grade)
    d, along = polyline(X, Z, pts)
    r = np.round(np.interp(along, s, p))
    half = width / 2
    t = smoothstep(half, half + shoulder, d)
    Hn = np.where(d <= half, r, np.where(d <= half + shoulder, r + t * (H - r), H))
    if water is not None:
        Hn = np.where(water, H, Hn)
    if keep is not None:
        Hn = np.where(keep, H, Hn)
    return Hn, (s, p)


def _pin(p, s, end, value, max_grade):
    """The profile held to `value` at one end, the change eased back along it no steeper than the grade."""
    p = p.copy()
    idx = range(len(p)) if end == 0 else range(len(p) - 1, -1, -1)
    origin = s[0] if end == 0 else s[-1]
    for j in idx:
        reach = max_grade * abs(s[j] - origin)
        lo, hi = value - reach, value + reach
        if lo <= p[j] <= hi:
            break
        p[j] = min(max(p[j], lo), hi)
    return p


def coast(H, X, Z, sea, outline=None, shelf=10, depth=6, slope=0.35):
    """Land meeting the sea at an outline (a polygon), or at the world's edge when none is given: inland the
    ground eases down to the sea over `shelf` blocks, so the shore is a beach and not a cliff, and nothing inside
    the outline lies under the sea; seaward the floor falls `slope` blocks a block to `depth` under the surface
    at `sea`. Cuts, and lifts low land inside the outline to a block over the sea. The sea runs on to the world's
    edge, where it meets the void. Returns (H, Water)."""
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
    inside = distance_in(mask, "euclid")
    t = np.clip(inside / max(width, 1e-6), 0, 1)
    t = t * t * (3 - 2 * t)
    return np.asarray(Ha, float) * (1 - t) + np.asarray(Hb, float) * t


def profile(H, d, floor, steps, floor_ground=None, jag=0.0, talus=None, mode="set"):
    """A cross-section set by distance from a line: `d` is how far out each column lies (shapes.polyline gives it
    from a path, `x - f(z)` from a straight one). Out to the first step the ground is `floor_ground` (a field; the
    floor's nominal height `floor` where none is given); each `Step` then eases from the nominal level before it to
    its `top` and holds its ground past its end, so floor, lower cliff, bench, upper cliff and plateau are a floor
    and two steps. The first cliff rises out of the floor and never cuts it (or, falling, never lifts it), so a
    talus against its foot stays; `talus` (rise, reach) lifts the floor by up to `rise` over the last `reach`
    blocks before it. `jag` (a number or a field) is added to every start and end, so cliffs are ragged and not
    ruled. A level of "ground" is the ground the cross-section is laid on. `mode` is set, lift or cut."""
    H = np.asarray(H, float)
    level = lambda v: H if isinstance(v, str) and v == "ground" else v          # noqa: E731
    h = np.zeros(np.shape(d)) + (floor if floor_ground is None else level(floor_ground))
    if talus is not None and steps:
        rise, reach = talus
        h = h + rise * smoothstep(steps[0].start - reach, steps[0].start, d)
    before = level(floor)
    for n, step in enumerate(steps):
        top = level(step.top)
        cliff = before + (top - before) * smoothstep(step.start + jag, step.end + jag, d)
        if n == 0:
            cliff = np.where(top >= before, np.maximum(h, cliff), np.minimum(h, cliff))
        h = np.where(d >= step.start + jag, cliff, h)
        h = np.where(d >= step.end + jag, top if step.ground is None else level(step.ground), h)
        before = top
    return _apply(H, h, mode)


def level(H, e, y="median", inner=1.0, outer=1.5, mode="set"):
    """Level ground: `y` (a height, or "median" for the median ground inside) where the distance field `e` is under
    `inner`, eased back to the ground (y * (1 - k) + H * k, k a smoothstep) out to `outer`. `e` is any distance, in
    blocks from a point or a path, or 1 on an ellipse's rim (shapes.ellipse_distance), plus noise for a ragged edge;
    `inner` and `outer` are in its units. `mode` lift only raises the skirt, cut only lowers it; inside it is y."""
    H = np.asarray(H, float)
    if isinstance(y, str) and y == "median":
        y = float(np.median(H[e < inner]))
    k = smoothstep(inner, outer, e)
    skirt = _apply(H, y * (1 - k) + H * k, mode)
    return np.where(e < inner, y, np.where(e < outer, skirt, H))


def mound(H, e, rise, power=1.6, mode="lift"):
    """A heap on the ground: `rise` blocks at the centre of the distance field `e` (0 there, 1 on the rim; a
    shapes.ellipse_distance, noise added for a ragged foot), falling as 1 - e ** power to nothing at the rim. A
    negative rise with mode cut is a hollow."""
    H = np.asarray(H, float)
    return np.where(e < 1, _apply(H, H + rise * (1 - np.clip(e, 0, 1) ** power), mode), H)


def crater(H, e, floor, r, flat=0.0, slope=1.0):
    """A bowl cut into the ground out to `r` of the distance field `e` (blocks from its centre): its floor at
    `floor` out to `flat`, then climbing `slope` blocks a block, so at one it is a flight a player walks out of.
    Only cuts."""
    H = np.asarray(H, float)
    return np.where(e <= r, np.minimum(H, floor + slope * np.maximum(0, e - flat)), H)


def ridge(H, coord, foot, width, crest, rough=0.0, spurs=(), terrace=None):
    """A ridge along a board's back: from its `foot` (a line along the other axis, noise.line) it climbs over
    `width` blocks toward lower `coord` (X or Z; a negative width climbs toward higher) to `crest` (a height or a
    field), with `rough` (a field) added in proportion as it climbs. Each spur (d, top, (far, near)) is an arm
    reaching out from it: `top` (a field) where d, the distance from the spur's line, is under `near`, eased to
    the ground by `far`. `terrace` (step, riser, above) cuts the slope into terraces where it has climbed more
    than `above` of the way. Only lifts."""
    H = np.asarray(H, float)
    t = smoothstep(foot, foot - width, coord)
    lifted = H + (crest - H).clip(0) * t + t * rough
    for d, top, (far, near) in spurs:
        lifted = np.maximum(lifted, H + (top - H).clip(0) * smoothstep(far, near, d))
    if terrace is not None:
        step, riser, above = terrace
        lifted = terraces(lifted, t > above, step=step, riser=riser)
    return np.where(lifted > H, lifted, H)

