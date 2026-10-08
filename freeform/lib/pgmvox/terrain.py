"""Terrain at block scale: heights read and painted by slope, rock beds, scenery mountains outside the play, the
undersides of floating ground, and a sea of cloud. The landforms that shape the heights are in `landform`.

    deg = slope_deg(H)                            # each column's slope, as the studio's SurfaceGradient reads it
    beds = beds(Strata(...), bed_offset(H.shape, dip=(0.04, 0), fold=3))
    lay(w, H, mask, top=by_angle([...]), bands=beds)   # columns up to H, painted by slope, rock in beds
    H = mountain_ring(X, Z, clear=120, ...)       # a ring of separate massifs rising outside a clear radius
    underside(w, mask, top_y, root_depth(mask, flutes=4, spires=12))
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


SLOPE_WINDOW = 2                                  # the studio's SurfaceGradient.Window


def slope_deg(H, mask=None, window=SLOPE_WINDOW):
    """Each column's slope in whole degrees from level, 0 to 89, as the studio's SurfaceGradient reads it: Horn's
    3x3 gradient over the tops `window` cells either side, a neighbour off the board or outside `mask` read as
    level with the column itself, rounded half to even. The window is two because ground quantised to whole
    blocks is a staircase, and one cell reads each step (27 degrees on a riser, 0 on a tread) instead of the grade."""
    H = np.asarray(H).astype(np.int64)
    sx, sz = H.shape
    m = np.ones(H.shape, bool) if mask is None else np.asarray(mask, bool)
    step = max(1, int(window))

    def top(dx, dz):
        out = H.copy()
        a0, a1 = max(0, -dx * step), min(sx, sx - dx * step)
        b0, b1 = max(0, -dz * step), min(sz, sz - dz * step)
        if a0 < a1 and b0 < b1:
            src = H[a0 + dx * step:a1 + dx * step, b0 + dz * step:b1 + dz * step]
            ok = m[a0 + dx * step:a1 + dx * step, b0 + dz * step:b1 + dz * step]
            out[a0:a1, b0:b1] = np.where(ok, src, H[a0:a1, b0:b1])
        return out
    along_x = top(-1, -1) + 2 * top(-1, 0) + top(-1, 1) - top(1, -1) - 2 * top(1, 0) - top(1, 1)
    along_z = top(-1, -1) + 2 * top(0, -1) + top(1, -1) - top(-1, 1) - 2 * top(0, 1) - top(1, 1)
    rise = np.hypot(along_x, along_z) / (8.0 * step)
    deg = np.minimum(89, np.round(np.degrees(np.arctan(rise)))).astype(int)
    return np.where(m, deg, 0)


def _slope_cases(path, seed=5):
    """Write the test grounds data/export_slopes.cs reads: ramps, a staircase, a cliff, noise, and holes."""
    import json
    rng = np.random.default_rng(seed)
    X, Z = np.meshgrid(np.arange(24), np.arange(20), indexing="ij")
    grounds = [X // 1, X // 2, X // 3, (X + Z) // 2, np.where(X > 11, 40, 34), 30 + 6 * noise.fbm((24, 20), 6, 3, seed=1),
               30 + 18 * noise.fbm((24, 20), 4, 3, seed=2), rng.integers(20, 40, (24, 20))]
    cases = []
    for k, g in enumerate(grounds):
        g = np.asarray(g).astype(int)
        hole = (np.hypot(X - 12, Z - 10) < 4) if k % 2 else (X + 2 * Z) % 11 == 0
        for m in (np.ones(g.shape, bool), ~hole):
            cases.append([[int(g[i, j]) if m[i, j] else None for j in range(g.shape[1])] for i in range(g.shape[0])])
    with open(path, "w") as f:
        json.dump(cases, f)


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


class Strata:
    """A sequence of rock beds by height, drawn from weighted choices: each (block, weight, thickest), a bed `thickest`
    blocks at most, 1 for a bed that is only ever one block (the red in a mesa). A weight counts per draw, and no
    bed follows itself, which lifts the rarer beds a little (a weight of 0.04 among four came out 9 in 100). Two
    draws of one block would read as one bed. Below `start` the rock is `below`; past the drawn length the
    sequence repeats."""

    def __init__(self, choices, length=160, seed=0, start=0, below=(B.STONE, 0)):
        rng = np.random.default_rng(seed)
        w = np.array([c[1] for c in choices], float)
        self.seq = []
        while len(self.seq) < length:
            block, _, thickest = choices[int(rng.choice(len(choices), p=w / w.sum()))]
            if self.seq and self.seq[-1] == block:
                continue
            self.seq += [block] * int(rng.integers(1, max(1, thickest) + 1))
        self.start, self.below = start, below

    def __call__(self, y):
        if y < self.start:
            return self.below
        return self.seq[(y - self.start) % len(self.seq)]

    def thicknesses(self):
        """[(block, thickness)] bed by bed, for a legend or a test."""
        out = []
        for b in self.seq:
            if out and out[-1][0] == b:
                out[-1][1] += 1
            else:
                out.append([b, 1])
        return [tuple(o) for o in out]


def bed_offset(shape, dip=(0.0, 0.0), fold=0.0, cell=24, seed=0):
    """How far the beds are lifted at each column: a planar dip (blocks of lift per block east and south) and folds
    of `fold` blocks from noise, so the beds tilt and bend across a cliff instead of running dead level."""
    sx, sz = shape
    X, Z = np.meshgrid(np.arange(sx), np.arange(sz), indexing="ij")
    off = dip[0] * X + dip[1] * Z
    if fold:
        off = off + fold * noise.fbm(shape, cell, 3, seed=seed)
    return np.round(off).astype(int)


def beds(strata, offset=None, flecks=(), seed=0):
    """A column fill for lay(bands=...): the strata at each height, shifted by the column's offset, with flecks:
    [(in_bed, block, chance)], another block now and then inside one bed (cobble in stone, gravel in andesite)."""
    rng = np.random.default_rng(seed)

    def fill(i, k, ys):
        o = 0 if offset is None else int(offset[i, k])
        out = []
        for y in ys:
            b = strata(y - o)
            for bed, other, chance in flecks:
                if b == bed and rng.random() < chance:
                    b = other
                    break
            out.append(b)
        return out
    return fill


SOIL = ((25, 3), (38, 2), (55, 1))                  # (steeper than this, soil this deep): none past the last


def ledge_angle(H, deg, mask=None):
    """The slope a paint should read: a cell exactly level with three or more of its four neighbours reads as a
    ledge, at most 30 degrees, however steep the hill it sits on, so grass holds on it and the rock shows on the
    risers between ledges. Level means level: on an even slope of block steps every cell is within a block of its
    neighbours, and counting those turned whole hillsides into ledges. Cells past 60 degrees are left alone."""
    Hp = np.pad(np.asarray(H).astype(int), 1, mode="edge")
    c = Hp[1:-1, 1:-1]
    flat = sum((Hp[1 + di:Hp.shape[0] - 1 + di, 1 + dj:Hp.shape[1] - 1 + dj] == c).astype(int)
               for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return np.where((flat >= 3) & (deg < 60), np.minimum(deg, 30), deg)


def soil_depth(deg, soil=SOIL):
    """How deep the soil lies on ground of each slope: `soil` is ((up to degrees, depth), ...) in rising order, and
    ground steeper than the last has none, so a cliff is rock to its face and shows no band of dirt."""
    out = np.zeros(np.shape(deg), int)
    for limit, depth in reversed(soil):
        out = np.where(deg < limit, depth, out)
    return out


def lay(w, H, mask=None, top=None, under=(B.DIRT, 0), rock=(B.STONE, 0), dirt_depth=None, snow_above=None,
        snow=(B.SNOW, 0), bands=None, from_y=1, soil=SOIL, ledges=True):
    """Columns of ground up to H (world heights): rock, then soil of `under`, then the top block, which
    `top(deg, h)` chooses by slope (default grass); above snow_above the top is snow with a layer over it.
    bands(i, k, ys) may paint the rock instead.

    The soil's depth follows the slope (`soil`): three blocks on gentle ground, less on steeper, none on a cliff,
    so a cliff face is rock and a terrace's riser is not a band of dirt. With `ledges`, a cell level with its
    neighbours reads as gentle however steep its hill (ledge_angle). `dirt_depth` gives one depth everywhere
    instead. Returns the slope the paint read."""
    deg = slope_deg(H, mask)
    if ledges:
        deg = ledge_angle(H, deg, mask)
    depth = soil_depth(deg, soil) if dirt_depth is None else np.full(np.shape(H), dirt_depth, int)
    sx, sz = H.shape
    for i in range(sx):
        for k in range(sz):
            if mask is not None and not mask[i, k]:
                continue
            h = int(H[i, k])
            if h < from_y:
                continue
            dd = int(depth[i, k])
            ys = range(from_y, max(from_y, h - dd))
            if bands:
                for y, (bid, d) in zip(ys, bands(i, k, ys)):
                    w.ids[i, y, k], w.dat[i, y, k] = bid, d
            else:
                w.ids[i, from_y:max(from_y, h - dd), k] = rock[0]
                w.dat[i, from_y:max(from_y, h - dd), k] = rock[1]
            w.ids[i, max(from_y, h - dd):h, k] = under[0]
            w.dat[i, max(from_y, h - dd):h, k] = under[1]
            bid, d = top(deg[i, k], h) if top else ((B.GRASS, 0) if dd > 0 else rock)
            if snow_above is not None and h > snow_above:
                bid, d = snow
                if h + 1 < w.sy:
                    w.ids[i, h + 1, k], w.dat[i, h + 1, k] = B.SNOW_LAYER, 1
            w.ids[i, h, k], w.dat[i, h, k] = bid, d
    return deg


def root_depth(mask, cone=3.2, power=0.85, rough=0.35, flutes=0.0, flute_cell=5, spires=0.0, spire_cell=18,
               cap=None, seed=0):
    """How far a floating island's underside hangs under each column: a cone deeper inland (cone * edge
    distance ** power), roughened by `rough`, with vertical flutes of `flutes` blocks and spires of up to `spires`
    blocks hanging from it, as the karst islands were cut. An array for underside(depth=...)."""
    d = np.maximum(edge_depth(mask), 0).astype(float) + 1
    shape = mask.shape
    n = noise.fbm(shape, 12, 3, seed=seed)
    out = cone * d ** power * (1 + rough * n)
    if flutes:
        out += flutes * np.abs(noise.fbm(shape, flute_cell, 2, seed=seed + 1))
    if spires:
        sp = noise.fbm(shape, spire_cell, 2, seed=seed + 2)
        out += spires * np.maximum(sp - 0.25, 0) / 0.75
    if cap is not None:
        out = np.minimum(out, cap)
    return np.where(mask, np.maximum(1, np.round(out)), 0).astype(int)


def underside(w, mask, top_y, depth=lambda d: 1 + int(1.6 * min(d, 7) ** 0.9), paint=None, rng=None, jitter=1):
    """Hang a tapering underside below a floating floor: under every column of mask (a (sx, sz) boolean over the
    world), from top_y - 1 down by depth blocks plus a little jitter, painted by paint(k, x, z) for the k-th block
    down (default stone). top_y is one height, or an array (each column's own: islands at several heights in one
    call). depth is a function of the column's edge depth, or an array (root_depth). The underside lies wholly
    inside the floor's outline, so a player falling past an edge never touches it."""
    ed = edge_depth(mask)
    rng = rng or np.random.default_rng(0)
    table = depth if isinstance(depth, np.ndarray) else None
    for i, k in np.argwhere(mask):
        n = (int(table[i, k]) if table is not None else depth(int(ed[i, k]))) + \
            (int(rng.integers(0, jitter + 1)) if jitter else 0)
        ty = int(top_y[i, k]) if isinstance(top_y, np.ndarray) else top_y
        for j in range(1, n + 1):
            y = ty - j
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
