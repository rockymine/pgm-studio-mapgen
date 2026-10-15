"""Combinations: the forms of the earlier studies in one place each. Rock in three greys by slope, lava, water, ice
and snow in their own colours; nothing else textured.

    lava_rift      a winding canyon floored with lava, mesas standing in it, bridges tangled across at every height
    ice_rift       the same rift, the lava water under broken pack ice
    somma_ice      the somma facing a high ice plateau whose ice overhangs the cliff and calves into a lake

    python3 combos.py [name ...]      # renders into ../renders
"""
import os
import sys
from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "volcanoes", "scripts"))
from pgmvox import B, World                                                   # noqa: E402
from pgmvox.geom import noise                                                 # noqa: E402
from pgmvox.geom.noise import smoothstep, spline                              # noqa: E402
from pgmvox.geom.shapes import polyline, ellipse_distance, shatter            # noqa: E402
from pgmvox.ground import landform as L                                       # noqa: E402
from pgmvox.read import render                                                # noqa: E402
from pgmvox.scenery.forms import sweep, spike, flare                          # noqa: E402
from pgmvox.surface.terrain import slope_deg                                  # noqa: E402
import round2 as R                                                            # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders")
SIZE, SY = 300, 220
X0 = Z0 = -SIZE // 2


@dataclass
class Scene:
    rock: np.ndarray                                   # the ground's top y per column
    solid: np.ndarray = None                           # extra rock over the ground: bridges, spikes, overhangs
    ice: np.ndarray = None                             # ice top per column, NaN where none
    ice_bottom: np.ndarray = None                      # under the ice: air above this (an overhang), rock below
    lava: object = None                                # lava surface y, NaN where none
    water: object = None
    icicles: np.ndarray = None                         # ice hanging under the overhang, as a mask
    notes: list = field(default_factory=list)


def world():
    return World(X0, Z0, SIZE, SIZE, sy=SY)


def grid():
    X, Z = world().grid()
    return X.astype(float), Z.astype(float)


def at(F, x, z):
    return float(F[min(max(int(round(x)) - X0, 0), SIZE - 1), min(max(int(round(z)) - Z0, 0), SIZE - 1)])


def mesa(H, X, Z, c, r, top, seed, benches=((0.6, 3), (0.4, 4)), stretch=0.75, angle=0.0, crag=18):
    """A monolith: a lobed outline bitten into by bays, walls down in sheer drops broken by ragged benches, a skirt
    of talus, and a top that is its own small landscape (tilted, a crag at one end, gullies cut back from the rim)."""
    Xw, Zw = noise.warp(X, Z, seed=seed, big=4 + 0.15 * r, small=2.5, big_cell=45, small_cell=11)
    d = R.r_at(Xw, Zw, c, stretch, angle)
    theta = np.arctan2(Zw - c[1], Xw - c[0])
    d = d + 0.16 * r * np.maximum(0, np.sin(theta * 5 + 1.7 * noise.fbm(X.shape, 40, 2, seed=seed + 1))) ** 6
    base = float(np.median(H[np.abs(d - r) < 2])) if (np.abs(d - r) < 2).any() else float(H.mean())
    tilt = 0.15 * ((X - c[0]) * 0.8 + (Z - c[1]) * 0.6)
    surface = top + 5 * noise.fbm(X.shape, 18, 3, seed=seed + 2) + tilt
    surface += crag * np.clip(1 - R.r_at(Xw, Zw, (c[0] + 0.45 * r, c[1] + 0.25 * r), 0.7, 30) / (0.33 * r), 0, 1) ** 1.3
    surface -= 10 * noise.ridged(X.shape, 6, 2, seed=seed + 3, sharpness=5) * smoothstep(r - 12, r, d)
    jag = 2.2 * noise.fbm(X.shape, 7, 2, seed=seed + 4)
    steps, edge = [], r
    for k, (frac, out) in enumerate(benches):
        level = base + frac * (top - base) + 4 * noise.fbm(X.shape, 30, 2, seed=seed + 5 + k)
        steps.append(L.Step(edge, edge + 1.2, level))
        edge = edge + out * (0.6 + 0.8 * (0.5 + 0.5 * noise.fbm(X.shape, 25, 2, seed=seed + 8 + k)))
    steps.append(L.Step(edge, edge + 1.5, "ground"))
    H = L.profile(H, d, floor=top, floor_ground=surface, steps=steps, jag=jag, mode="lift")
    skirt = base + 0.2 * (top - base) * np.clip(1 - (d - edge) / (0.6 * r + 10), 0, 1) ** 1.8 + 2 * noise.fbm(X.shape, 8, 2, seed=seed + 9)
    return np.maximum(H, np.where(d > edge - 2, skirt, -1e9))


def gully(H, X, Z, head, mouth, floor, seed, width=(3, 16)):
    """A side gully cut back into the plateau from the canyon: wandering from its mouth to its head, `width` from
    narrow at the head to wide at the mouth, its floor falling from the plateau at the head to `floor` at the mouth,
    its walls steep and ragged."""
    rng = np.random.default_rng(seed)
    hx, hz = head
    mx, mz = mouth
    pts = [(mx + (hx - mx) * f + rng.normal(0, 6) * (0 < f < 1), mz + (hz - mz) * f + rng.normal(0, 6) * (0 < f < 1))
           for f in np.linspace(0, 1, 5)]
    d, along = polyline(X, Z, spline(pts, 1.5))[:2]
    t = np.clip(along / max(along.max(), 1), 0, 1)                         # 0 at the mouth, 1 at the head
    half = (width[1] + (width[0] - width[1]) * t) / 2 + 1.5 * noise.fbm(X.shape, 6, 2, seed=seed)
    top = float(np.median(H[np.hypot(X - hx, Z - hz) < 6]))
    bed = floor + (top - floor) * smoothstep(0.2, 1.05, t) + 1.5 * noise.fbm(X.shape, 10, 2, seed=seed + 1)
    u = np.clip(d / np.maximum(half, 0.5), 0, 1)
    cut = bed + (H - bed) * u ** 3
    return np.where((d < half) & (t < 0.999), np.minimum(H, cut), H)


def piece_mesa(H, X, Z, c, n, top, seed, spacing=11, drop=(4, 26), slots=0.3):
    """A monolith from `n` neighbouring pieces of shattered ground grown out from the piece under `c`: an angular,
    irregular outline; each piece its own height, the first the highest, so the top steps down in blocks; a share
    `slots` of the joins between pieces opened into narrow clefts; a talus skirt round the foot. Returns the
    ground and the monolith's mask."""
    p = shatter(X, Z, spacing, seed=seed, warp=(5, 2, 40, 10))
    rng = np.random.default_rng(seed)
    first = p.id[int(round(c[0])) - X0, int(round(c[1])) - Z0]
    pairs = set()
    for a, b in ((p.id[:-1], p.id[1:]), (p.id[:, :-1], p.id[:, 1:])):
        m = a != b
        pairs |= set(zip(a[m].tolist(), b[m].tolist()))
    nbrs = {}
    for a, b in pairs:
        nbrs.setdefault(a, set()).add(b)
        nbrs.setdefault(b, set()).add(a)
    chosen = [first]
    while len(chosen) < n:
        frontier = sorted({q for k in chosen for q in nbrs.get(k, ()) if q not in chosen})
        if not frontier:
            break
        chosen.append(frontier[int(rng.integers(len(frontier)))])
    heights = {k: top - (0 if j == 0 else rng.uniform(*drop)) for j, k in enumerate(chosen)}
    cleft = {k: rng.random() < slots for k in chosen[1:]}
    mask = np.isin(p.id, chosen)
    gap = np.vectorize(lambda k: 1.3 if cleft.get(k, False) else 0.0)(p.id)
    body = mask & (p.edge > gap)
    tops = np.vectorize(lambda k: heights.get(k, 0.0))(p.id)
    tops = tops + 3 * noise.fbm(X.shape, 12, 2, seed=seed + 1) - 6 * noise.ridged(X.shape, 5, 2, seed=seed + 2, sharpness=5) * smoothstep(3, 0, p.edge)
    out = ndimage.distance_transform_edt(~mask)
    base = float(np.median(H[(out > 0) & (out < 3)]))
    skirt = base + 0.18 * (top - base) * np.clip(1 - out / 14, 0, 1) ** 1.8 + 2 * noise.fbm(X.shape, 8, 2, seed=seed + 3)
    H = np.maximum(H, np.where(body, tops, np.where(~mask & (out < 14), skirt, H)))   # the skirt only near it
    return H, body


def bridge(w, a, b, width=4.0, sag=3.0, under=12.0, rough=0.2, seed=0, broken=None):
    """A swept bridge from a to b, each (x, z, y): carried a little past both ends so it grows out of the rock,
    its deck on the line between the two heights less a sag, thin in the middle and thick at the ends. `broken`
    (where, gap) leaves open air across that share of the span."""
    (ax, az, ay), (bx, bz, by) = a, b
    L_ = np.hypot(bx - ax, bz - az)
    ux, uz = (bx - ax) / L_, (bz - az) / L_
    ext = 8.0
    path = [(ax - ux * ext, az - uz * ext), (bx + ux * ext, bz + uz * ext)]
    f0, f1 = ext / (L_ + 2 * ext), (ext + L_) / (L_ + 2 * ext)
    above = flare(2.5, 6, 2.5)
    def centre(t):                                                         # the deck's top on the line, less the sag
        s = np.clip((np.asarray(t) - f0) / (f1 - f0), 0, 1)
        return ay + (by - ay) * s - sag * np.sin(np.pi * s) - above(t)
    vol = sweep(w, path, centre, flare(width, width * 1.9, 3), above, flare(3, under, 2.2),
                power=3.2, rough=rough, seed=seed)
    if broken:
        where, gap = broken
        X, Z = w.grid()
        s = ((X - ax) * ux + (Z - az) * uz) / L_
        vol &= ~(np.abs(s - where) < gap / 2)[:, None, :]
    return vol


def hanging(w, vol, n, seed, length=(4, 16), radius=(1.0, 2.2), region=None):
    """Spikes hanging from the underside of a solid: n tries at random columns under it."""
    rng = np.random.default_rng(seed)
    cols = np.argwhere(vol.any(axis=1) & (np.ones(vol.shape[::2], bool) if region is None else region))
    out = np.zeros_like(vol)
    if len(cols) == 0:
        return out
    for i, k in cols[rng.choice(len(cols), size=min(n, len(cols)), replace=False)]:
        ys = np.nonzero(vol[i, :, k])[0]
        y = ys.min()
        out |= spike(w, [(i + w.x0, y + 1, k + w.z0), (i + w.x0 + rng.normal(0, 0.5), y + 1 - rng.uniform(*length), k + w.z0)],
                     (rng.uniform(*radius), 0, 1.4), rough=0.1, seed=int(rng.integers(1 << 30)))
    return out


# --- the combinations --------------------------------------------------------------------------------------------

def rift(X, Z, seed=1):
    """The rift both rifts share: a plateau rising and falling into broad swells and saddles, side gullies biting
    into its rim, a winding canyon whose walls are benched only in places and at different heights, a rough floor,
    five monoliths of shattered rock standing in it, and the tangle of bridges between them and the rims."""
    w = world()
    H = 88 + 20 * noise.fbm(X.shape, 110, 3, seed=seed) + 7 * noise.ridged(X.shape, 40, 3, seed=seed + 1)
    path = spline([(-170, -60), (-100, -40), (-40, -70), (20, -10), (80, 20), (170, -20)], 2.0)
    d, along = polyline(X, Z, path)[:2]
    half = R.along_noise(along, 70, seed + 2, 46, 62)
    jag = 2.5 * noise.fbm(X.shape, 7, 2, seed=seed + 3) + 1.5 * noise.fbm(X.shape, 3, 1, seed=seed + 9)
    floor = 25 + 2 * noise.fbm(X.shape, 25, 2, seed=seed + 4)
    bench_w = np.clip(14 * noise.fbm(X.shape, 45, 2, seed=seed + 5), 0, None)           # 0 where there is no bench
    bench_y = 52 + 16 * noise.fbm(X.shape, 60, 2, seed=seed + 6)
    upper_w = np.clip(10 * noise.fbm(X.shape, 35, 2, seed=seed + 7) - 3, 0, None)
    upper_y = np.maximum(bench_y + 14, 74 + 8 * noise.fbm(X.shape, 40, 2, seed=seed + 8))
    e1 = half - bench_w - upper_w
    H = L.profile(H, d, floor=25, floor_ground=floor,
                  steps=[L.Step(e1 - 4, e1, bench_y), L.Step(e1 + bench_w - 1, e1 + bench_w + 2, upper_y),
                         L.Step(half - 1, half + 3, "ground")], jag=jag, talus=(6, 8), mode="cut")
    for k, (head, mouth) in enumerate([((-134, -128), (-118, -78)), ((-30, -150), (-14, -92)), ((66, 96), (56, 42)),
                                        ((-74, 52), (-64, -16)), ((150, -84), (128, -46))]):
        H = gully(H, X, Z, head, mouth, floor=26, seed=90 + k)
    mesas = [((-110, -48), 7, 108, 1), ((-48, -64), 5, 88, 2), ((10, -18), 8, 116, 3), ((70, 14), 5, 82, 4),
             ((128, -6), 6, 98, 5)]
    bodies = []
    for c, n, top, s_ in mesas:
        H, body = piece_mesa(H, X, Z, c, n, top, seed=40 + 10 * s_)
        bodies.append(body)
    solid = np.zeros(w.ids.shape, bool)
    rng = np.random.default_rng(seed + 7)

    def anchor(a, toward, lower=0.0):
        """Where a bridge meets its end: on a rim, the column given; on a monolith, its column nearest the other
        end, set four blocks back in, at its top less `lower` so some bridges enter the wall instead."""
        if a[0] == "rim":
            x, z = a[1]
            return (x, z, at(H, x, z))
        body = bodies[a[1]]
        cols = np.argwhere(body)
        tx, tz = toward
        dd = np.hypot(cols[:, 0] + X0 - tx, cols[:, 1] + Z0 - tz)
        i, k = cols[np.argmin(dd)]
        cx, cz = cols[:, 0].mean() + X0, cols[:, 1].mean() + Z0
        x, z = i + X0, k + Z0
        v = np.array([cx - x, cz - z]); v = v / max(np.linalg.norm(v), 1e-6)
        x, z = x + 4 * v[0], z + 4 * v[1]
        return (x, z, at(H, x, z) - lower)

    def where(a):
        if a[0] == "rim":
            return a[1]
        cols = np.argwhere(bodies[a[1]])
        return (cols[:, 0].mean() + X0, cols[:, 1].mean() + Z0)

    M = lambda k: ("mesa", k)                                                    # noqa: E731
    Rm = lambda x, z: ("rim", (x, z))                                            # noqa: E731
    spans = [(Rm(-118, -112), M(0), 4.0, 2, None, 0), (M(0), Rm(-96, 20), 3.5, 3, None, 6),
             (M(0), M(1), 3.0, 5, None, 10), (Rm(-70, -130), Rm(-30, -6), 5.0, 6, None, 0),
             (M(1), M(2), 3.5, 2, None, 0), (Rm(2, -80), M(2), 4.5, 4, None, 14),
             (M(2), Rm(-8, 54), 4.0, 3, (0.55, 7), 4), (M(2), M(3), 3.0, 4, None, 18),
             (Rm(40, -48), Rm(96, 72), 3.0, 1, None, 0), (M(3), M(4), 3.5, 3, None, 0),
             (M(4), Rm(132, 60), 4.0, 2, None, 8), (M(4), Rm(150, -72), 3.5, 3, None, 0)]
    for k, (a, b_, wd, sag, broken, lower) in enumerate(spans):
        pa = anchor(a, where(b_), lower if a[0] == "mesa" else 0)
        pb = anchor(b_, where(a), lower if b_[0] == "mesa" else 0)
        b_vol = bridge(w, pa, pb, width=wd, sag=sag, under=10 + 6 * rng.random(), seed=seed * 100 + k, broken=broken)
        if k in (1, 3, 8):
            b_vol |= hanging(w, b_vol, 14, seed * 100 + 50 + k)
        solid |= b_vol
    for k, body in enumerate(bodies):                                          # spikes on the monoliths' tops
        cols = np.argwhere(body & (p_top := (H >= np.percentile(H[body], 70))))
        for j in range(3):
            i, kk = cols[int(rng.integers(len(cols)))]
            x, z, y = i + X0, kk + Z0, H[i, kk]
            solid |= spike(w, [(x, y - 2, z), (x + rng.normal(0, 3), y + rng.uniform(8, 20), z + rng.normal(0, 3))],
                           (rng.uniform(2, 3.2), 0, 1.1), flutes=(7, 0.25), rough=0.15, seed=seed * 1000 + 10 * k + j)
    return H, solid, d, along


def lava_rift(X, Z):
    """A winding canyon floored with lava, five mesas standing in it, twelve bridges tangled across at every height,
    one broken, stalactites under three, spikes on the mesa tops."""
    H, solid, d, along = rift(X, Z)
    level = 29.0
    crust = shatter(X, Z, 9, seed=11, warp=(3, 1, 30, 8))                   # cooled plates floating on the lava
    rng = np.random.default_rng(12)
    plate = (rng.random(len(crust.centres)) < 0.25)[crust.id] & (crust.edge > 1.2) & (H < level)
    H = np.where(plate, level + 0.4, H)
    return Scene(H, solid, lava=np.where(H < level, level, np.nan))


def ice_rift(X, Z):
    """The same rift, its floor water under pack ice broken into floes, one lead open down the middle."""
    H, solid, d, along = rift(X, Z)
    level = 29.0
    floes = shatter(X, Z, 14, seed=21, warp=(5, 2, 40, 10))
    rng = np.random.default_rng(22)
    lead = d < 3 + 4 * (0.5 + 0.5 * noise.fbm(X.shape, 30, 2, seed=23))
    keep = (floes.edge > rng.uniform(0.6, 2.2, len(floes.centres))[floes.id]) & ~lead & (H < level)
    ice = np.where(keep, level + rng.uniform(1, 2.5, len(floes.centres))[floes.id], np.nan)
    return Scene(H, solid, ice=ice, ice_bottom=np.where(keep, level - 2, H), water=np.where(H < level, level, np.nan))


def somma_ice(X, Z):
    """The somma in the west, its lava flow running out east; in the east the ice plateau rises in three tiers,
    each edge wandering into bays and out onto spurs, each tier's ice hanging out over its own drop with icicles
    under it; seracs broken off at the foot into a lake half frozen over between the cliff and the volcano."""
    H = R.somma(X + 60, Z)
    w = world()
    rng = np.random.default_rng(39)
    tiers = [(48, 64, 31), (66, 88, 32), (88, 112, 33)]                    # (where its edge runs, its height, seed)
    ice = np.full(X.shape, np.nan)
    ice_bottom = H.copy()
    icicles = np.zeros(w.ids.shape, bool)
    edges = []
    for k, (at_x, height, sd) in enumerate(tiers):
        wander = 16 * noise.fbm((SIZE,), 60, 3, seed=sd)[None, :] + 5 * noise.fbm((SIZE,), 12, 2, seed=sd + 10)[None, :]
        spurs = 10 * np.maximum(noise.fbm((SIZE,), 22, 2, seed=sd + 20), 0)[None, :] ** 1.5
        edge = at_x + wander - spurs + 2 * noise.fbm(X.shape, 5, 2, seed=sd + 30)
        top = height + 5 * noise.fbm(X.shape, 50, 3, seed=sd + 40)
        cliff = smoothstep(edge - 2, edge + 1.5, X)
        H = np.maximum(H, H * (1 - cliff) + top * cliff)
        edges.append((edge, top))
    lake = ellipse_distance(X, Z, (22, 10), 24, 70, angle=8) + 0.18 * noise.fbm(X.shape, 15, 2, seed=34)
    H = np.where(lake < 1, np.minimum(H, 16 + 6 * lake), H)
    level = 19.0
    for k, (edge, top) in enumerate(edges):
        nxt = edges[k + 1][0] if k + 1 < len(edges) else np.full_like(edge, 1e9)
        over = 4 + 9 * (0.5 + 0.5 * noise.fbm((SIZE,), 26, 2, seed=50 + k))[None, :]
        on = (X > edge - over) & (X < nxt - 1)
        ice_top = top + 6 + 2 * noise.fbm(X.shape, 20, 2, seed=60 + k)
        phase = (X - edge) / 6 + 0.6 * noise.fbm(X.shape, 25, 2, seed=70 + k)
        crev = (np.abs(phase - np.round(phase)) * 6 < 0.9) & (X > edge) & (X < edge + 16)
        ice = np.where(on, np.where(crev, ice_top - 6, ice_top), ice)
        hang = on & (X < edge + 1)
        ice_bottom = np.where(hang, top - 2, np.where(on, H, ice_bottom))
        cols = np.argwhere(hang & (X < edge - 1))
        for i, kk in cols[rng.choice(len(cols), size=min(36, len(cols)), replace=False)]:
            y = int(round(top[i, kk] - 2))
            icicles |= spike(w, [(i + X0, y, kk + Z0), (i + X0, y - rng.uniform(4, 20), kk + Z0)],
                             (rng.uniform(1.0, 2.4), 0, 1.5), rough=0.1, seed=int(rng.integers(1 << 30)))
    pieces = shatter(X, Z, 8, seed=38, warp=(3, 1, 30, 8))
    n = len(pieces.centres)
    near_cliff = smoothstep(edges[0][0] - 2, edges[0][0] - 26, X)
    fallen = (lake < 0.95) & (pieces.edge > 1.0) & (rng.random(n)[pieces.id] < 0.2 + 0.6 * near_cliff)
    ice = np.where(fallen, level + 1 + rng.uniform(1, 9, n)[pieces.id] * near_cliff, ice)
    ice_bottom = np.where(fallen, level - 3, ice_bottom)
    flow_line = spline([(-50, 70), (-20, 80), (2, 60), (6, 40)], 2.0)
    fd = polyline(X, Z, flow_line)[0]
    channel = fd < 4 + 2 * noise.fbm(X.shape, 6, 2, seed=40)
    H = np.where(channel & (lake >= 1), H - 1.5, H)
    lava = np.where(channel & (lake >= 1), H + 1, np.nan)
    water = np.where((lake < 1.05) & (H < level), level, np.nan)
    return Scene(H, None, ice=ice, ice_bottom=ice_bottom, lava=lava, water=water, icicles=icicles)


STUDIES = [lava_rift, ice_rift, somma_ice]
CORNER = {"somma_ice": ("sw", "nw")}
ZOOM = {"somma_ice": ((-10, -110, 130, 110), "nw"), "lava_rift": ((-60, -110, 60, 40), "se")}


# --- building and drawing ------------------------------------------------------------------------------------------

def build(sc):
    w = world()
    ys = np.arange(SY)[None, :, None]
    rock = np.clip(np.round(sc.rock), 1, SY - 2).astype(int)
    deg = slope_deg(rock)
    tone = np.where(deg < 30, 0, np.where(deg < 50, 1, 2)).astype(np.uint8)
    ground = ys <= rock[:, None, :]
    w.ids[...] = np.where(ground, B.WOOL, 0)
    w.dat[...] = np.where(ground, np.array([0, 8, 7], np.uint8)[tone][:, None, :], 0)
    if sc.solid is not None:
        extra = sc.solid & ~ground
        above = np.ones_like(extra); above[:, :-1] = ~extra[:, 1:] & ~ground[:, 1:]
        w.ids[extra] = B.WOOL
        w.dat[extra] = np.where(above, 0, 8)[extra]
    if sc.ice is not None:
        has = np.isfinite(sc.ice)
        it = np.round(np.nan_to_num(sc.ice, nan=-1)).astype(int)
        ib = rock if sc.ice_bottom is None else np.round(sc.ice_bottom).astype(int)
        body = has[:, None, :] & (ys <= it[:, None, :]) & (ys > ib[:, None, :]) & (w.ids == 0)
        w.ids[body] = B.PACKED_ICE
        w.ids[body & (ys < it[:, None, :])] = B.ICE
        w.ids[body & (ys == it[:, None, :])] = B.SNOW
        w.dat[body] = 0
    if sc.icicles is not None:
        sel = sc.icicles & (w.ids == 0)
        w.ids[sel] = B.ICE
    for level, block in ((sc.lava, B.LAVA), (sc.water, B.WATER)):
        if level is None:
            continue
        lv = np.broadcast_to(np.asarray(level, float), rock.shape)
        has = np.isfinite(lv)
        top = np.round(np.nan_to_num(lv, nan=-1)).astype(int)
        wet = has[:, None, :] & (ys <= top[:, None, :]) & (w.ids == 0)
        w.ids[wet] = block
    return w


def plan_view(w, out, title, scale=3):
    from pgmvox.core import blocks as K
    solid = w.ids > 0
    top = SY - 1 - np.argmax(solid[:, ::-1, :], axis=1)
    ids = w.ids[np.arange(SIZE)[:, None], top, np.arange(SIZE)[None, :]]
    dat = w.dat[np.arange(SIZE)[:, None], top, np.arange(SIZE)[None, :]]
    col = K.COLOURS[ids, dat & 15].astype(float)
    gx, gz = np.gradient(top.astype(float))
    col *= np.clip(1 + 0.1 * (gx + gz), 0.55, 1.35)[..., None]
    band = np.floor(top / 6)
    cont = (band != np.roll(band, 1, 0)) | (band != np.roll(band, 1, 1))
    col[cont] *= 0.72
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8).transpose(1, 0, 2)).resize((SIZE * scale, SIZE * scale), Image.NEAREST)
    ImageDraw.Draw(im).text((8, 6), f"{title}  (north up, contours every 6)", fill=(0, 0, 0))
    im.save(out)


def main(names):
    os.makedirs(OUT, exist_ok=True)
    X, Z = grid()
    for f in STUDIES:
        n = f.__name__
        if names and n not in names:
            continue
        sc = f(X, Z)
        w = build(sc)
        a, b = CORNER.get(n, ("se", "nw"))
        render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-iso.png", 2, a, ymin=8)
        render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-iso2.png", 2, b, ymin=8)
        if n in ZOOM:
            box, corner = ZOOM[n]
            render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-close.png", 4, corner, box, 8)
            render.trim(f"{OUT}/{n}-close.png")
        for p in ("iso", "iso2"):
            render.trim(f"{OUT}/{n}-{p}.png")
        plan_view(w, f"{OUT}/{n}-plan.png", n)
        print(f"{n:13s} top {int(np.max(np.nonzero(w.ids.any(axis=(0, 2)))[0]))}  "
              f"lava {int((w.ids == B.LAVA).sum())}  ice {int(np.isin(w.ids, [B.ICE, B.PACKED_ICE, B.SNOW]).sum())}  "
              f"water {int((w.ids == B.WATER).sum())}")


if __name__ == "__main__":
    main(sys.argv[1:])
