"""Water and lava studies: shapes only. Rock in three greys by slope, sand pale, water blue, lava orange, cooled crust
dark. Each study returns a Scene: rock heights, liquid surfaces per column, and 3-D masks for what a heightfield
cannot say (a cave behind a fall, a lava tube, falling curtains).

    cascades     a mountain stream stepping down a valley in reaches and falls, a plunge pool under every fall
    plunge       a river pouring off a cliff lip into a gorge, a cave behind the curtain, the river running on
    delta        a river fanning into the sea through branching channels, islands and bars between them
    meanders     a meandering river on a floodplain, oxbow lakes cut off beside it, kettle ponds in hummocky ground
    terraces     travertine pools stepping down a hillside, each brimming over its lobed rim into the next
    lava         a crater lava lake with crust plates, a levéed lava river, a lavafall, perched ponds and a lava tube

    python3 water.py [name ...]      # renders into ../renders/round1
"""
import heapq
import os
import sys
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World                                                   # noqa: E402
from pgmvox.geom import noise                                                 # noqa: E402
from pgmvox.geom.noise import smoothstep, spline                              # noqa: E402
from pgmvox.geom.shapes import polyline, ellipse_distance, shatter            # noqa: E402
from pgmvox.ground import landform as L                                       # noqa: E402
from pgmvox.read import render                                                # noqa: E402
from pgmvox.scenery.forms import sweep, flare                                 # noqa: E402
from pgmvox.surface.terrain import slope_deg                                  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "round1")
SIZE, SY = 300, 170
X0 = Z0 = -SIZE // 2


@dataclass
class Scene:
    rock: np.ndarray
    water: np.ndarray = None                 # water surface y per column, NaN where dry
    lava: np.ndarray = None
    sand: np.ndarray = None                  # columns whose top is sand (bars, beaches)
    crust: np.ndarray = None                 # columns of cooled crust floating on lava, a block over it
    carve: np.ndarray = None                 # 3-D air cut out of the ground (caves, tubes)
    water3d: np.ndarray = None               # 3-D water laid where it is air (curtains)
    lava3d: np.ndarray = None


def world():
    return World(X0, Z0, SIZE, SIZE, sy=SY)


def grid():
    X, Z = world().grid()
    return X.astype(float), Z.astype(float)


def at(F, x, z):
    return float(F[min(max(int(round(x)) - X0, 0), SIZE - 1), min(max(int(round(z)) - Z0, 0), SIZE - 1)])


def fill_basins(H, open_edges=True):
    """Every hollow filled to the level it spills at (priority flood from the board's edges): the surface water
    would stand at if it rained until every hollow overflowed. Returns that surface; where it is above the ground,
    there is a pond."""
    H = np.asarray(H, float)
    filled = H.copy()
    seen = np.zeros(H.shape, bool)
    heap = []
    n, m = H.shape
    for i in range(n):
        for k in (0, m - 1):
            heapq.heappush(heap, (H[i, k], i, k)); seen[i, k] = True
    for k in range(m):
        for i in (0, n - 1):
            if not seen[i, k]:
                heapq.heappush(heap, (H[i, k], i, k)); seen[i, k] = True
    while heap:
        h, i, k = heapq.heappop(heap)
        for a, b in ((i + 1, k), (i - 1, k), (i, k + 1), (i, k - 1)):
            if 0 <= a < n and 0 <= b < m and not seen[a, b]:
                seen[a, b] = True
                filled[a, b] = max(H[a, b], h)
                heapq.heappush(heap, (filled[a, b], a, b))
    return filled


def curtains(level, H, min_drop=2):
    """Falling water wherever a wet column stands two or more over a wet neighbour: that neighbour's column is
    filled from its surface up to the higher one, the face of the fall. A 3-D mask over the world."""
    w = world()
    vol = np.zeros(w.ids.shape, bool)
    lv = np.where(np.isfinite(level), np.round(level), -1).astype(int)
    for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        hi = np.roll(lv, (di, dk), axis=(0, 1))
        fall = (lv >= 0) & (hi - lv >= min_drop)
        for i, k in np.argwhere(fall):
            vol[i, lv[i, k] + 1:hi[i, k] + 1, k] = True
    return vol


def hold_banks(H, level):
    """Every dry cell beside water raised to that water's surface, so none stands against air."""
    lv = np.where(np.isfinite(level), level, -np.inf)
    near = ndimage.maximum_filter(lv, size=3)
    dry = ~np.isfinite(level)
    return np.where(dry & np.isfinite(near), np.maximum(H, near), H)


# --- the studies ---------------------------------------------------------------------------------------------------

def cascades(X, Z):
    """A mountain stream: a V valley winding down from the north-west, rock bars across its floor where the stream
    steps down, its bed held level in reaches and falling in falls over them, a plunge pool scoured under each fall,
    boulders along the reaches."""
    H = 30 + 95 * smoothstep(140, -150, X * 0.7 + Z * 0.5) + 10 * noise.fbm(X.shape, 50, 3, seed=1)
    path = spline([(-150, -140), (-110, -95), (-60, -80), (-30, -30), (20, -10), (50, 40), (100, 60), (150, 120)], 2.0)
    d, along = polyline(X, Z, path)[:2]
    H = H - 34 * np.clip(1 - d / 44, 0, 1) ** 1.4                         # the V valley
    total = float(along.max())
    for k, f in enumerate((0.18, 0.33, 0.47, 0.62, 0.78)):                 # rock bars across the floor
        bar = along - f * total + 5 * noise.fbm(X.shape, 12, 2, seed=10 + k)
        H = H + 8 * smoothstep(1.5, -1.5, bar) * smoothstep(-12, -6, bar) * smoothstep(30, 14, d)
    H, river = L.watercourse(H, X, Z, path, width=8, depth=2, water=2, bank=3, fall_min=3, reach_min=10)
    level = np.where(river.mask, river.surface, np.nan)
    for x, z, drop in river.falls:                                         # a plunge pool below each fall
        e = np.hypot(X - x, Z - z)
        below = river.mask & (e < 6)
        lo = float(np.min(river.surface[below])) if below.any() else at(level, x, z)
        pool = (e < 6 + 0.5 * drop) & (d < 10) & (np.nan_to_num(level, nan=lo) <= lo + 0.5)
        H = np.where(pool, np.minimum(H, lo - 2 - 0.5 * drop * smoothstep(8, 0, e)), H)
        level = np.where(pool, lo, level)
    H = hold_banks(H, level)
    H = L.lumps(H, X, Z, 70, (-150, -150, 150, 150), (1.5, 3.5), (1.5, 3.5), seed=4, mask=(d > 5) & (d < 16))
    return Scene(H, water=level, water3d=curtains(level, H))


def plunge(X, Z):
    """A river crossing a plateau to the lip of an amphitheatre and plunging 50 blocks into it: the lip a ledge of
    hard rock standing out over a cave cut back behind the curtain, a plunge pool at the foot, and the river running
    on east across the amphitheatre's floor and out between its cliffs."""
    Xw, Zw = noise.warp(X, Z, seed=1, big=10, small=3)
    top = 100 + 5 * noise.fbm(X.shape, 60, 3, seed=2)
    low = 48 + 3 * noise.fbm(X.shape, 40, 2, seed=3)
    bowl = np.hypot((Xw - 40) / 75, Zw / 62) + 0.05 * noise.fbm(X.shape, 7, 2, seed=5) + 0.08 * noise.ridged(X.shape, 14, 2, seed=6)
    basin = (bowl < 1) | ((Xw > 40) & (np.abs(Zw) < 62 - 0.25 * (Xw - 40)))
    cliff = np.where(basin, 0.0, 1.0)
    cliff = ndimage.gaussian_filter(cliff, 0.8)
    H = low + (top - low) * smoothstep(0.35, 0.65, cliff)
    H = L.lumps(H, X, Z, 50, (-40, -70, 150, 70), (3, 8), (2, 6), seed=4, mask=basin & (ndimage.distance_transform_edt(basin) < 10))
    upper = spline([(-150, 40), (-100, 22), (-60, 6), (-36, 0)], 2.0)
    du = polyline(X, Z, upper)[0]
    edge_x = float(np.min(X[basin & (np.abs(Z) < 2)]))                  # where the river reaches the lip
    on_top = ~basin & (du < 5)
    H = np.where(on_top, np.minimum(H, top - 3), H)
    lvl = np.where(on_top, top - 1, np.nan)
    pool = np.hypot((X - edge_x - 12) / 14, Z / 16) < 1
    H = np.where(pool, np.minimum(H, low - 6), H)
    lower = polyline(X, Z, spline([(edge_x + 20, 0), (70, 12), (110, -6), (150, 4)], 2.0))[0] < 5
    H = np.where(lower & ~pool, np.minimum(H, low - 2), H)
    lvl = np.where(pool | lower, low, lvl)
    H = hold_banks(H, lvl)
    ys = np.arange(SY)[None, :, None]
    lip = top - 6
    cut = ((X > edge_x - 9) & (X < edge_x + 1) & (np.abs(Z) < 14 - 0.3 * np.abs(X - edge_x + 4)))[:, None, :]
    carve = cut & (ys > low[:, None, :]) & (ys < (lip - 3 * smoothstep(edge_x - 9, edge_x, X))[:, None, :])
    ledge = (X >= edge_x - 1) & (X < edge_x + 3) & (np.abs(Z) < 12)
    H = np.where(ledge, np.maximum(H, top - 1), H)
    carve |= ledge[:, None, :] & (ys < lip[:, None, :]) & (ys > low[:, None, :])
    curtain = ((X >= edge_x + 3) & (X < edge_x + 5) & (np.abs(Z) < 5.5))[:, None, :]
    curtain = curtain & (ys > low[:, None, :]) & (ys <= (top - 1)[:, None, :])
    return Scene(H, water=lvl, carve=carve, water3d=curtain)


def branches(apex, heading, length, width, depth, rng, out):
    """A river splitting as it goes: from apex along heading, wandering, then two children turned apart, one of them
    now and then dying out early."""
    pts = [apex]
    a = heading
    for _ in range(4):
        a += rng.normal(0, 0.16)
        p = pts[-1]
        pts.append((p[0] + length / 4 * np.cos(a), p[1] + length / 4 * np.sin(a)))
    out.append((pts, width))
    if depth == 0:
        return
    spread = rng.uniform(0.35, 0.55)
    for sgn in (-1, 1):
        if depth >= 3 or rng.random() < 0.75:
            branches(pts[-1], a + sgn * spread, length * rng.uniform(0.6, 0.8), max(width * rng.uniform(0.62, 0.75), 2.5),
                     depth - 1, rng, out)


def delta(X, Z):
    """A river reaching the sea and fanning out through channels that split and split again, the land between them
    low islands barely over the water, sand bars at the channel mouths, the fan's front lobed into the sea."""
    sea = 20.0
    apex = (-70.0, 0.0)
    Xw, Zw = noise.warp(X, Z, seed=5, big=14, small=4)
    rad = np.hypot(Xw - apex[0], Zw - apex[1])
    ang = np.arctan2(Zw - apex[1], Xw - apex[0])
    lobes = 150 + 18 * np.sin(ang * 5 + 1.0) + 10 * noise.fbm(X.shape, 30, 2, seed=6)
    fan = (rad < lobes) & (np.abs(ang) < 1.25)
    land = sea + 1.5 + 2.5 * (1 - rad / lobes) + 0.8 * noise.fbm(X.shape, 12, 2, seed=7)
    hills = 40 + 30 * smoothstep(-60, -150, X) + 8 * noise.fbm(X.shape, 60, 3, seed=8)
    H = np.where(X < apex[0], np.minimum(hills, sea + 3 + 0.45 * (apex[0] - X) + 8 * smoothstep(20, 70, np.abs(Z))), sea - 6 - 4 * smoothstep(0, 60, rad - lobes))
    H = np.where(fan, land, H)
    H, river = L.watercourse(H, X, Z, [(-150, 10), (-110, -5), (-70, 0)], width=12, depth=3, water=2, lowest=sea - 2)
    rng = np.random.default_rng(9)
    chans = []
    branches(apex, 0.0, 60, 11, 4, rng, chans)
    for pts, wd in chans:
        dd = polyline(X, Z, spline(pts, 1.5))[0]
        H = np.where(dd < wd / 2 + 0.8 * noise.fbm(X.shape, 6, 1, seed=int(wd * 10)), np.minimum(H, sea - 2), H)
    bars = np.zeros(X.shape, bool)
    for pts, wd in chans:
        if wd < 4:
            x, z = pts[-1]
            e = ellipse_distance(X, Z, (x + 6, z), 5, 3, angle=0) + 0.3 * noise.fbm(X.shape, 4, 1, seed=int(x))
            bars |= (e < 1) & (H < sea)
    H = np.where(bars, sea + 0.6, H)
    level = np.where((H < sea) | river.mask, np.where(river.mask, river.surface, sea), np.nan)
    near_water = ndimage.distance_transform_edt(~np.isfinite(level)) < 3
    sand = (near_water & ~np.isfinite(level) & (H < sea + 3)) | bars
    return Scene(H, water=level, sand=sand)


def meanders(X, Z):
    """A meandering river across a floodplain between bluffs: its bends swelling downstream, two old loops cut off as
    oxbow lakes beside it, a scroll of point bars on the inside of each bend, and kettle ponds filling the hollows of
    hummocky ground on the north bank, each to the level it spills at."""
    plain = 24 + 0.8 * noise.fbm(X.shape, 40, 2, seed=1)
    bluffs = 24 + 26 * smoothstep(60, 90, np.abs(Z - 10 * np.sin(X / 70))) + 6 * noise.fbm(X.shape, 50, 2, seed=2)
    H = np.maximum(plain, bluffs)
    xs = np.linspace(-160, 160, 200)
    amp = 22 + 14 * (xs + 160) / 320
    zs = amp * np.sin(xs / 24 + 0.4 * np.sin(xs / 61)) + 4 * noise.fbm((200,), 30, 2, seed=3)
    path = list(zip(xs, zs))
    d, along, side = polyline(X, Z, path, side=True)
    width = 4.5 + 1.5 * noise.fbm(X.shape, 30, 2, seed=4)
    H = np.where(d < width, np.minimum(H, 20 - smoothstep(width, 0, d) * 2), H)
    # point bars: low sand scrolls on the inside of the bends
    curv = np.gradient(np.gradient(np.interp(X[:, 0], xs, zs)))[:, None] * np.ones((1, SIZE))
    inside = np.sign(curv) * np.sign(Z - np.interp(X, xs, zs)) > 0
    bar = inside & (d > width) & (d < width + 9) & (H < 27)
    H = np.where(bar, np.minimum(H, 22.5 + 0.5 * np.sin(d * 1.3)), H)
    lakes = np.full(X.shape, np.nan)
    for k, (cx, cz, rx, rz, a0, a1, ang) in enumerate([(-40, 34, 20, 13, 0.3, 3.3, 10), (78, -46, 22, 14, 3.4, 6.4, -20)]):
        th = np.linspace(a0, a1, 40)
        arc = [(cx + rx * np.cos(t) * np.cos(np.radians(ang)) - rz * np.sin(t) * np.sin(np.radians(ang)),
                cz + rx * np.cos(t) * np.sin(np.radians(ang)) + rz * np.sin(t) * np.cos(np.radians(ang))) for t in th]
        da, al = polyline(X, Z, arc)[:2]
        taper = np.sin(np.pi * np.clip(al / al.max(), 0, 1)) ** 0.5
        ox = (da < 4.5 * taper + 0.5) & (d > width + 3)
        H = np.where(ox, np.minimum(H, 21), H)
        lakes = np.where(ox, 23.0, lakes)
    # hummocky ground with kettles on the north bank
    region = (Z < -45) & (Z > -110)
    hum = L.lumps(np.zeros(X.shape), X, Z, 120, (-150, -110, 150, -45), (4, 10), (1.5, 4), seed=5, rough=0.3)
    kettles = L.lumps(np.zeros(X.shape), X, Z, 40, (-150, -105, 150, -50), (4, 9), (2, 5), seed=6, rough=0.3)
    H = np.where(region, plain + 2 + hum - kettles, H)
    filled = fill_basins(np.round(H))
    ponds = region & (filled - np.round(H) >= 1)
    level = np.where(d < width, 23.0, np.nan)
    level = np.where(np.isfinite(lakes), lakes, level)
    level = np.where(ponds, filled, level)
    H = hold_banks(H, level)
    return Scene(H, water=level, sand=bar)


def terraces(X, Z):
    """Travertine terraces: a hillside built of pools, each held behind a lobed rim a block or two high and brimming
    over it, so water steps down the slope in small falls from pool to pool, a spring at the top."""
    slope = 30 + 70 * smoothstep(150, -150, X + 0.3 * Z) + 4 * noise.fbm(X.shape, 50, 2, seed=1)
    Xw, Zw = noise.warp(X, Z, seed=2, big=10, small=3, big_cell=40, small_cell=9)
    scallop = 7.0 * np.abs(np.sin(Zw / 11 + 1.5 * noise.fbm(X.shape, 40, 2, seed=3))) + 2.0 * noise.fbm(X.shape, 14, 2, seed=4)
    q = slope + scallop
    step = 3.0
    flat = np.floor(q / step) * step
    frac = (q - flat) / step                                               # 0 at a rim's outer lip, 1 at the riser's top
    lower = ndimage.minimum_filter(flat, size=3) < flat                    # cells of a terrace touching a lower one
    H = flat + 1 + lower                                                   # the rim: a lip a block over each pool's water
    H = np.where(np.abs(Z) < 110, H, slope + 14)                           # terraced across its middle, banked at the sides
    H = np.round(H)
    filled = fill_basins(H)
    pools = (filled - H >= 1) & (np.abs(Z) < 110)
    level = np.where(pools, filled, np.nan)
    return Scene(H, water=level, water3d=curtains(level, H, min_drop=2))


def lava(X, Z):
    """Fire's water: a lava lake in a summit crater with cooled crust floating on it; a lava river leaving through a
    breach, held level in reaches between raised levées and falling where a scarp crosses the flank, a pool at the
    foot of the fall; two perched ponds held in their own rims; a lava tube under the west flank, open to the sky
    through three skylights."""
    Xw, Zw = noise.warp(X, Z, seed=1, big=10, small=3)
    r = np.hypot(Xw + 40, Zw + 30)
    H = 22 + 100 * np.clip(1 - r / 150, 0, 1) ** 1.4 + 4 * noise.fbm(X.shape, 40, 3, seed=2)
    H = L.gullies(H, Xw, Zw, (-40, -30), 20, 4, 40, 140, seed=3)
    # a scarp across the south-east flank: the ground past it 16 lower, the step easing out away from it and
    # dying out at both ends, where the river will fall
    sc_line = spline([(-20, 80), (12, 52), (40, 34), (75, 12), (100, -4)], 1.5)
    sd, sal, sside = polyline(X, Z, sc_line, side=True)
    fade = np.sin(np.pi * np.clip(sal / sal.max(), 0, 1)) ** 0.7
    low_side = sside < 0
    step = smoothstep(-1.2, 1.2, np.where(low_side, sd, -sd) + 1.5 * noise.fbm(X.shape, 6, 2, seed=9))
    H = H - 20 * step * fade * (1 - smoothstep(12, 70, np.where(low_side, sd, 0)))
    crater = np.hypot(Xw + 40, Zw + 30) / 26 + 0.08 * noise.fbm(X.shape, 10, 2, seed=4)
    lake_lv = 98.0
    H = np.where(crater < 1, np.minimum(H, lake_lv - 4), H)
    H = np.where((crater > 1) & (crater < 1.25), np.maximum(H, lake_lv + 3 + 2 * noise.fbm(X.shape, 6, 2, seed=5)), H)
    lavalv = np.where(crater < 1, lake_lv, np.nan)
    crust = shatter(X, Z, 6, seed=6, warp=(2, 1, 20, 6))
    rng = np.random.default_rng(7)
    plates = (crater < 0.95) & (crust.edge > 0.9) & (rng.random(len(crust.centres))[crust.id] < 0.55)
    # the river: a channel from the breach following the ground down, never climbing, between raised levées; its
    # surface steps a block at a time down the slope and falls where the scarp drops it, a pool at the foot
    path = spline([(-24, -8), (0, 14), (22, 34), (38, 56), (54, 80), (72, 104), (84, 118)], 1.0)
    H = np.where(np.hypot(X + 22, Z + 8) < 6, np.minimum(H, lake_lv - 1), H)   # the breach in the rim
    d, along = polyline(X, Z, path)[:2]
    samples = np.array([at(H, *p) for p in path])
    cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(np.array(path), axis=0).T))])
    surf_s = np.minimum(np.minimum.accumulate(ndimage.uniform_filter1d(samples, 5)), lake_lv) - 1
    surf = np.floor(np.interp(along, cum, surf_s))
    chan = (d < 3.2) & ~(crater < 1)
    H = np.where(d < 3.8, np.minimum(H, surf - 1), H)
    levee = (d >= 3.8) & (d < 6.5) & ~(crater < 1.3)
    H = np.where(levee, np.maximum(H, surf + 2 + noise.fbm(X.shape, 5, 1, seed=8)), H)
    lavalv = np.where(chan, surf, lavalv)
    jump = np.abs(np.diff(surf_s))
    if jump.max() >= 4:
        j = int(np.argmax(jump)) + 3
        fx, fz = path[min(j, len(path) - 1)]
        lo = surf_s[min(j, len(path) - 1)]
        pool = (np.hypot(X - fx, Z - fz) < 9 + 1.5 * noise.fbm(X.shape, 5, 1, seed=10)) & (d < 12)
        H = np.where(pool, np.minimum(H, lo - 3), H)
        H = np.where(~pool & (np.hypot(X - fx, Z - fz) < 12) & (d < 15), np.maximum(H, lo + 1), H)
        lavalv = np.where(pool, lo, lavalv)
    # where it runs out: a pond spreading at the foot of the cone, its edge lobed
    fan = np.hypot((X - 90) / 20, (Z - 124) / 14) + 0.15 * noise.fbm(X.shape, 8, 2, seed=13) < 1
    end = surf_s[-1]
    H = np.where(fan, np.minimum(H, end - 2), H)
    H = np.where(~fan & (np.hypot((X - 90) / 23, (Z - 124) / 17) < 1), np.maximum(H, end + 1), H)
    lavalv = np.where(fan, end, lavalv)
    H = hold_banks(H, lavalv)
    # perched ponds: a ring of rim round a lava pond on the flank
    for k, (c, rr) in enumerate([((-100, 30), 9), ((-80, -95), 7)]):
        e = np.hypot(X - c[0], Z - c[1]) / rr + 0.12 * noise.fbm(X.shape, 5, 1, seed=11 + k)
        g = at(H, *c)
        H = np.where(e < 1.35, np.maximum(H, g + 4 * smoothstep(1.35, 1.0, e)), H)
        H = np.where(e < 1.0, np.minimum(H, g + 1), H)
        lavalv = np.where(e < 1.0, g + 3, lavalv)
    # the lava tube: eight under the ground the whole way, a stream of lava in its floor, three skylights
    w = world()
    tube_path = spline([(-70, -20), (-90, 20), (-95, 60), (-80, 100)], 2.0)
    ts = np.linspace(0, 1, len(tube_path))
    deep = np.array([at(H, *p) for p in tube_path]) - 9
    tube = sweep(w, tube_path, lambda t: np.interp(t, ts, deep), 3.5, 3.0, 1.5, power=2.4, rough=0.12, seed=12)
    ys = np.arange(SY)[None, :, None]
    floor_y = np.where(tube.any(axis=1), np.argmax(tube, axis=1), SY)
    lava3d = tube & (ys <= floor_y[:, None, :] + 1)
    carve = tube.copy()
    for k in (0.2, 0.5, 0.8):
        sx, sz = tube_path[int(k * (len(tube_path) - 1))]
        hole = (np.hypot(X - sx, Z - sz) < 3.0 + 0.6 * noise.fbm(X.shape, 3, 1, seed=int(k * 10)))[:, None, :]
        carve |= hole & (ys > floor_y[:, None, :]) & (ys <= np.round(H)[:, None, :])
    return Scene(H, lava=lavalv, crust=plates, carve=carve, lava3d=lava3d | curtains(lavalv, H, min_drop=3))


STUDIES = [cascades, plunge, delta, meanders, terraces, lava]
CORNER = {"cascades": ("se", "nw"), "plunge": ("se", "sw"), "delta": ("se", "ne"), "meanders": ("se", "sw"),
          "terraces": ("se", "ne"), "lava": ("se", "sw")}
ZOOM = {"plunge": (-70, -60, 60, 60), "terraces": (-60, -60, 60, 60), "lava": (-120, -120, 149, 149),
        "cascades": (-80, -110, 40, 10)}


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
    if sc.sand is not None:
        top = ground & (ys == rock[:, None, :]) & sc.sand[:, None, :]
        w.ids[top] = B.SAND; w.dat[top] = 0
    if sc.carve is not None:
        w.ids[sc.carve] = 0; w.dat[sc.carve] = 0
    for level, block in ((sc.water, B.WATER), (sc.lava, B.LAVA)):
        if level is None:
            continue
        has = np.isfinite(level)
        lv = np.round(np.nan_to_num(level, nan=-1)).astype(int)
        wet = has[:, None, :] & (ys <= lv[:, None, :]) & (ys > rock[:, None, :] - 0) & (w.ids == 0)
        w.ids[wet] = block
    if sc.crust is not None and sc.lava is not None:
        lv = np.round(np.nan_to_num(sc.lava, nan=-1)).astype(int)
        c = sc.crust & np.isfinite(sc.lava)
        for i, k in np.argwhere(c):
            w.ids[i, lv[i, k], k], w.dat[i, lv[i, k], k] = B.WOOL, 7
    for vol, block in ((sc.water3d, B.WATER_FLOW), (sc.lava3d, B.LAVA)):
        if vol is not None:
            sel = vol & (w.ids == 0)
            w.ids[sel] = block
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
    band = np.floor(top / 5)
    col[(band != np.roll(band, 1, 0)) | (band != np.roll(band, 1, 1))] *= 0.75
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8).transpose(1, 0, 2)).resize((SIZE * scale, SIZE * scale), Image.NEAREST)
    ImageDraw.Draw(im).text((8, 6), f"{title}  (north up, contours every 5)", fill=(0, 0, 0))
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
            render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-close.png", 3 if n == "lava" else 4, a, ZOOM[n], 8)
        for p in ("iso", "iso2", "close"):
            if os.path.exists(f"{OUT}/{n}-{p}.png"):
                render.trim(f"{OUT}/{n}-{p}.png")
        plan_view(w, f"{OUT}/{n}-plan.png", n)
        print(f"{n:10s} water {int(np.isin(w.ids, [B.WATER, B.WATER_FLOW]).sum()):7d}  lava {int((w.ids == B.LAVA).sum()):6d}")
    if not names:
        tiles = [(f.__name__, Image.open(f"{OUT}/{f.__name__}-iso.png").convert("RGB")) for f in STUDIES]
        tiles = [(n, t.resize((600, int(t.height * 600 / t.width)))) for n, t in tiles]
        h = max(t.height for _, t in tiles) + 24
        sheet = Image.new("RGB", (1800, 2 * h), (205, 220, 235))
        d = ImageDraw.Draw(sheet)
        for k, (n, t) in enumerate(tiles):
            x, y = (k % 3) * 600, (k // 3) * h
            sheet.paste(t, (x, y + 22)); d.text((x + 8, y + 6), f"{k + 1}. {n}", fill=(0, 0, 0))
        sheet.save(f"{OUT}/00-sheet.png")


if __name__ == "__main__":
    main(sys.argv[1:])
