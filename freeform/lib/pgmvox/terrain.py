"""Terrain at block scale: heightfields, the paint that follows their slope, scenery mountains outside the play,
the undersides of floating ground, and a sea of cloud.

    H = mountain_ring(X, Z, clear=120, ...)       # a ring of separate massifs rising outside a clear radius
    deg = slope_deg(H)                            # each column's slope in degrees, without wrapping at the edges
    lay(w, H, mask, paint)                        # columns up to H, painted by a rule per column
    underside(w, mask, top_y, depth, paint)       # a tapering underside below a floating floor
    cloud_deck(w, y, mask, seed)                  # a deck of cloud with billows and breaks

The numbers that give a board its look stay in the board's plan; nothing here is a recipe.
"""
import numpy as np
from scipy.ndimage import gaussian_filter

from . import noise
from .blocks import B
from .shapes import edge_depth


def mountain_ring(X, Z, clear, rise=45.0, base=45.0, relief=45.0, crest=80.0, seed=21, cell=40, ridge_cell=20,
                  massif=0.3, edge=None, smooth=2.5, square=0.0):
    """Heights of a ring of mountains: nothing inside `clear` blocks of the centre, rising over `rise` blocks
    beyond it, broken into separate massifs (more of the ring is valley as `massif` falls), each with ridged
    crests. edge (half-width of the world box) lets the range fall back to nothing at the box's edge, so the world
    does not end in a cliff; square mixes the ring toward the box's own shape (0 round, 1 square)."""
    r = np.maximum(np.abs(X), np.abs(Z)) * square + np.hypot(X, Z) * (1 - square)
    ring = noise.smoothstep(clear, clear + rise, r)
    shape = X.shape
    big = noise.fbm(shape, cell + 6, 3, seed=seed)
    mass = np.clip((noise.fbm(shape, cell, 2, seed=seed + 3) + massif) * 1.3, 0, 1) ** 1.5
    ridge = noise.ridged(shape, ridge_cell, 4, seed=seed + 1)
    fine = noise.fbm(shape, 6, 2, seed=seed + 2)
    h = ring * (mass * (base + relief * (big + 0.5)) + mass ** 2 * crest * ridge ** 2)
    if edge is not None:
        h *= np.clip((edge - np.maximum(np.abs(X), np.abs(Z))) / 30.0, 0, 1)
    h = gaussian_filter(h, smooth) + 3 * fine * (h > 10)
    return h


def slope_deg(H):
    """The slope of every column in degrees, by Horn's 3x3 gradient as the studio reads it, edges padded by their
    own values so the west edge is not a neighbour of the east."""
    P = np.pad(H.astype(float), 1, mode="edge")
    gx = ((P[2:, :-2] + 2 * P[2:, 1:-1] + P[2:, 2:]) - (P[:-2, :-2] + 2 * P[:-2, 1:-1] + P[:-2, 2:])) / 8.0
    gz = ((P[:-2, 2:] + 2 * P[1:-1, 2:] + P[2:, 2:]) - (P[:-2, :-2] + 2 * P[1:-1, :-2] + P[2:, :-2])) / 8.0
    return np.degrees(np.arctan(np.hypot(gx, gz)))


def by_angle(stops):
    """A paint rule from slope stops: [(max_degrees, (id, data)), ...] in rising order; the last answers
    everything steeper."""
    def paint(deg, h):
        for limit, blk in stops:
            if deg <= limit:
                return blk
        return stops[-1][1]
    return paint


def banded(choices, period=6, offset=None):
    """A column fill in horizontal bands: choices is a list of (id, data) repeated every `period` blocks; offset
    (a (sx, sz) array) tilts and breaks the bands."""
    def fill(i, k, ys):
        o = 0 if offset is None else int(offset[i, k])
        return [choices[((y + o) // period) % len(choices)] for y in ys]
    return fill


def lay(w, H, mask=None, top=None, under=(B.DIRT, 0), rock=(B.STONE, 0), dirt_depth=3, snow_above=None,
        snow=(B.SNOW, 0), bands=None, from_y=1):
    """Columns of ground up to H (world heights): rock, then `dirt_depth` of `under`, then the top block, which
    `top(deg, h)` chooses by slope (default grass); above snow_above the top is snow with a layer over it.
    bands(i, k, ys) may paint the rock instead."""
    deg = slope_deg(H)
    sx, sz = H.shape
    for i in range(sx):
        for k in range(sz):
            if mask is not None and not mask[i, k]:
                continue
            h = int(H[i, k])
            if h < from_y:
                continue
            ys = range(from_y, max(from_y, h - dirt_depth))
            if bands:
                for y, (bid, d) in zip(ys, bands(i, k, ys)):
                    w.ids[i, y, k], w.dat[i, y, k] = bid, d
            else:
                w.ids[i, from_y:max(from_y, h - dirt_depth), k] = rock[0]
                w.dat[i, from_y:max(from_y, h - dirt_depth), k] = rock[1]
            w.ids[i, max(from_y, h - dirt_depth):h, k] = under[0]
            w.dat[i, max(from_y, h - dirt_depth):h, k] = under[1]
            bid, d = top(deg[i, k], h) if top else (B.GRASS, 0)
            if snow_above is not None and h > snow_above:
                bid, d = snow
                if h + 1 < w.sy:
                    w.ids[i, h + 1, k], w.dat[i, h + 1, k] = B.SNOW_LAYER, 1
            w.ids[i, h, k], w.dat[i, h, k] = bid, d
    return deg


def underside(w, mask, top_y, depth=lambda d: 1 + int(1.6 * min(d, 7) ** 0.9), paint=None, rng=None, jitter=1):
    """Hang a tapering underside below a floating floor: under every column of mask (a (sx, sz) boolean over the
    world), from top_y - 1 down by depth(edge_depth) blocks plus a little jitter, painted by paint(k, x, z) for
    the k-th block down (default stone). The underside lies wholly inside the floor's outline, so a player falling
    past an edge never touches it."""
    ed = edge_depth(mask)
    rng = rng or np.random.default_rng(0)
    for i, k in np.argwhere(mask):
        n = depth(int(ed[i, k])) + (int(rng.integers(0, jitter + 1)) if jitter else 0)
        for j in range(1, n + 1):
            y = top_y - j
            if y < 0:
                break
            bid, d = paint(j, i + w.x0, k + w.z0) if paint else (B.STONE, 0)
            w.ids[i, y, k], w.dat[i, y, k] = bid, d


def cloud_deck(w, y, mask=None, seed=7, cell=14, puff=9, breaks=-0.25, materials=((B.WOOL, 0), (B.SNOW, 0))):
    """A deck of cloud at height y: billows rising out of it, breaks where the sky below shows. Fills only air,
    so it wraps round mountains' feet instead of cutting into them."""
    n = noise.fbm((w.sx, w.sz), cell, 4, seed=seed)
    m = noise.fbm((w.sx, w.sz), 5, 2, seed=seed + 1)
    for i in range(w.sx):
        for k in range(w.sz):
            if mask is not None and not mask[i, k]:
                continue
            v = n[i, k]
            if v < breaks:
                continue
            top = y + int(max(0.0, v) * puff + m[i, k] * 1.5)
            bot = y - 1 - int(max(0.0, v) * 3)
            mat = materials[0] if m[i, k] > -0.2 or len(materials) == 1 else materials[1]
            col = w.ids[i, bot:top + 1, k]
            air = col == 0
            col[air] = mat[0]
            w.dat[i, bot:top + 1, k][air] = mat[1]
