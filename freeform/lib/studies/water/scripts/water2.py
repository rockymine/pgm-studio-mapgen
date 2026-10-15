"""Water and lava, second round. Two rules: every form is a graded profile eased into the ground (no mask is ever
set to a height, so no wall appears where a mask ends), and a river is stated first, its surface a gentle slope
falling a block at a time with falls only where placed, and the ground around it is shaped to it.

    python3 water2.py [name ...]      # renders into ../renders/round2
"""
import os
import sys

import numpy as np
from scipy import ndimage

import water as W
from water import (Scene, grid, world, at, fill_basins, curtains, noise, smoothstep, spline, polyline, ellipse_distance,
                   shatter, L, sweep, SIZE, SY, X0, Z0)
from PIL import Image, ImageDraw

W.OUT = OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "round2")


def ease(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def along_noise(along, cell, seed, lo, hi):
    n = int(np.max(along)) + 2
    f = noise.fbm((n,), cell, 3, seed=seed)
    f = (f - f.min()) / max(np.ptp(f), 1e-6)
    return lo + (hi - lo) * np.interp(along, np.arange(n), f)


def surface_profile(total, start, slope, falls=(), step=1.0):
    """A river's water surface along its length: falling `slope` blocks a block, in whole-block steps (water flowing
    over a one-block step), and dropping each fall's height at its place. Returns a function of along."""
    s = np.arange(0, total + 2, 0.5)
    z = start - slope * s
    for at_s, drop in falls:
        z = z - drop * (s >= at_s)
    z = np.floor(z / step) * step
    return lambda a: np.interp(a, s, z)


def channel(H, d, surf, half, depth=2.5, bank=8, seed=0):
    """Cut a river into the ground: a bed `depth` under the surface in the middle, rising as a parabola to the water's
    edge at `half`, banks easing from a block over the water back to the ground over `bank` blocks; cells at the
    water's edge are held a block over it so no water stands against air. Only the banks' first block ever lifts."""
    half = half + 1.2 * noise.fbm(d.shape, 9, 2, seed=seed)
    u = np.clip(d / half, 0, 1)
    bed = surf - depth * (1 - u ** 2) - 0.5
    rim = surf + 1
    out = rim + (H - rim) * ease((d - half) / bank)
    cut = np.where(d < half, bed, np.minimum(H, out))
    cut = np.where((d >= half) & (d < half + 1.5), np.maximum(cut, rim), cut)
    level = np.where((d < half) & (bed < surf), surf, np.nan)
    return cut, level


# --- the studies ---------------------------------------------------------------------------------------------------

def mountain_river(X, Z):
    """A river down a mountain valley: its surface falling gently a block at a time, then three falls where hard rock
    crosses the valley, each lip bitten unevenly into the rock, a curtain over it and a pool widened and scoured
    under it. The valley's floor is shaped to the river; its sides rise to mountains that fall away smoothly, so the
    hillsides never step where the river does."""
    path = spline([(-160, -120), (-110, -96), (-70, -60), (-40, -20), (0, 0), (40, 30), (80, 40), (120, 80), (165, 110)], 1.0)
    d, along = polyline(X, Z, path)[:2]
    total = float(along.max())
    falls = [(0.30 * total, 9), (0.52 * total, 14), (0.74 * total, 6)]
    lip = along + 5 * noise.fbm(X.shape, 10, 2, seed=1) + 0.04 * d ** 2 * 0      # the lip's line, uneven across
    surf = surface_profile(total, 112, 0.06, falls)(lip)
    proj = (X + 160) * 0.78 + (Z + 120) * 0.62                            # down the valley, smooth everywhere
    far = 112 + 10 - 0.06 * proj * total / 420 - sum(drp * smoothstep(a - 70, a + 70, proj * total / 420) for a, drp in falls)
    hills = far + 55 * ease((d - 10) / 90) ** 1.1 + 12 * noise.fbm(X.shape, 60, 3, seed=2) * ease((d - 10) / 40) \
        + 6 * noise.ridged(X.shape, 30, 2, seed=3) * ease((d - 20) / 50)
    smooth = surface_profile(total, 112, 0.06)(lip) - sum(drp * smoothstep(a - 30, a + 30, lip) for a, drp in falls)
    near = ease((14 - d) / 8)                                            # the step only where the river cuts it
    floor = (surf * near + smooth * (1 - near)) + 1 + 2 * noise.fbm(X.shape, 15, 2, seed=4)
    w_floor = ease((d - 10) / 30)
    H = floor * (1 - w_floor) + hills * w_floor
    half = along_noise(along, 50, 5, 4.5, 7.5)
    for a, drp in falls:                                                   # a pool under each fall, wide and deep
        below = np.clip(1 - np.hypot((along - a - 9) / 11, d / 13), 0, 1)
        half = half + 6 * below
        H = H - 3 * below                                                  # its banks sink to the pool
    H, level = channel(H, d, surf, half, depth=2.5 + 2.5 * sum(np.clip(1 - np.hypot((along - a - 8) / 9, d / 9), 0, 1) for a, _ in falls), bank=7, seed=6)
    H = L.lumps(H, X, Z, 90, (-160, -160, 160, 160), (1.5, 3.5), (1.5, 3), seed=7, mask=(d > half + 1.5) & (d < half + 9))
    return Scene(H, water=level, water3d=curtains(level, H))


def plunge(X, Z):
    """A river crossing a plateau to the lip of an amphitheatre and falling 46 blocks into it, cut a notch into the lip
    so the curtain falls in a slot of rock; a cave scoured back behind the curtain; a plunge pool at the foot; the
    river running on east out of the amphitheatre through a gorge. The amphitheatre's wall is one cross-section by
    distance (a cliff, a ledge, a second cliff, talus at the foot) with every number noise, as the caldera was."""
    Xw, Zw = noise.warp(X, Z, seed=1, big=10, small=3)
    top, low = 100.0, 54.0
    plateau = top + 4 * noise.fbm(X.shape, 60, 3, seed=2)
    th = np.arctan2(Zw, Xw - 30)
    bays = 14 * np.maximum(0, np.sin(th * 4 + 2.5 * noise.fbm(X.shape, 60, 2, seed=10))) ** 3 + 6 * noise.fbm(X.shape, 25, 2, seed=11)
    bowl = np.hypot((Xw - 30) / 1.0, Zw / 0.8) - bays
    gorge = np.abs(Zw - 6 * np.sin(Xw / 30)) * 1.0 + 0.0 * Xw
    dist = np.where(Xw > 30, np.minimum(bowl, 50 + gorge * 1.9 - 0.0), bowl)            # the gorge opens east
    dist = np.minimum(dist, np.where(Xw > 30, 18 + gorge * 1.6, np.inf))
    jag = 3 * noise.fbm(X.shape, 7, 2, seed=3) + 2 * noise.fbm(X.shape, 3, 1, seed=4)
    width = 3 + 10 * (0.5 + 0.5 * noise.fbm(X.shape, 30, 2, seed=5))
    H = L.profile(plateau, dist, floor=low, floor_ground=low + 1.5 * noise.fbm(X.shape, 20, 2, seed=6),
                  steps=[L.Step(56, 56 + width, 78 + 6 * noise.fbm(X.shape, 30, 2, seed=7)),
                         L.Step(62 + width, 64 + 1.5 * width, "ground")], jag=jag, talus=(7, 10), mode="cut")
    path = spline([(-160, 30), (-120, 16), (-80, 4), (-48, 0), (-26, 0), (-6, 4), (40, 6), (90, -4), (160, 2)], 1.0)
    d, along = polyline(X, Z, path)[:2]
    lip_x = -34.0                                                          # where the plateau ends on the river
    lip_s = float(np.interp(lip_x, [p[0] for p in path], np.concatenate([[0], np.cumsum(np.hypot(*np.diff(np.array(path), axis=0).T))])))
    up = along < lip_s
    s_up = surface_profile(lip_s + 2, top - 1, 0.012)(along)
    s_low = surface_profile(400, low + 1, 0.02)(np.maximum(along - lip_s, 0))
    surf = np.where(up, s_up, s_low)
    half = np.where(up, 4.5, along_noise(along, 40, 8, 4.5, 7))
    pool = np.clip(1 - np.hypot((along - lip_s - 14) / 14, d / 15), 0, 1)
    half = half + 9 * pool
    H, level = channel(H, d, surf, half, depth=2 + 4 * pool, bank=6, seed=9)
    # the notch the curtain falls in, and the cave behind it
    ys = np.arange(SY)[None, :, None]
    slot = (d < 4.5)[:, None, :] & ((along > lip_s - 0.5) & (along < lip_s + 14))[:, None, :]
    carve = slot & (ys > (low + 1)) & (ys < top)
    cave = (d < 9 - 0.25 * np.abs(along - lip_s))[:, None, :] & ((along > lip_s - 7) & (along < lip_s + 2))[:, None, :]
    carve |= cave & (ys > low + 1) & (ys < top - 7 - 3 * ease((lip_s - along) / 7)[:, None, :])
    curtain = (d < 4.5)[:, None, :] & ((along >= lip_s + 1) & (along < lip_s + 3))[:, None, :] & (ys > low) & (ys <= top - 1)
    return Scene(H, water=level, carve=carve, water3d=curtain)


def branches(apex, heading, length, width, depth, rng, out):
    pts = [apex]
    a = heading
    for _ in range(5):
        a += rng.normal(0, 0.14)
        p = pts[-1]
        pts.append((p[0] + length / 5 * np.cos(a), p[1] + length / 5 * np.sin(a)))
    out.append((pts, width))
    if depth == 0:
        return
    spread = rng.uniform(0.3, 0.5)
    for sgn in (-1, 1):
        if depth >= 3 or rng.random() < 0.75:
            branches(pts[-1], a + sgn * spread, length * rng.uniform(0.6, 0.8), max(width * rng.uniform(0.62, 0.75), 2.5),
                     depth - 1, rng, out)


def delta(X, Z):
    """A river leaving its valley and fanning into the sea: the valley's sides easing down onto the fan, the fan a low
    plain barely over the water and shelving gently under it, its channels splitting and splitting again, each with
    a curved bed and banks easing back to the islands, sand where the land meets the water."""
    sea = 22.0
    apex = (-60.0, 0.0)
    Xw, Zw = noise.warp(X, Z, seed=5, big=14, small=4)
    rad = np.hypot(Xw - apex[0], Zw - apex[1])
    ang = np.arctan2(Zw - apex[1], Xw - apex[0])
    lobes = 140 + 18 * np.sin(ang * 5 + 1.0) + 10 * noise.fbm(X.shape, 30, 2, seed=6)
    side = np.clip(np.abs(ang) / 1.3, 0, 1)
    shore = rad - lobes * (1 - 0.25 * side ** 4)                            # under zero on the fan
    fan = sea + 0.6 + 2.6 * ease(-shore / 120) + 0.7 * noise.fbm(X.shape, 14, 2, seed=7)
    shelf = sea - 0.5 - 9 * ease(shore / 70)
    H = np.where(shore < 0, fan, shelf)
    H = H * 1.0
    H = np.where(np.abs(shore) < 6, fan * ease((6 - shore) / 12) + shelf * (1 - ease((6 - shore) / 12)), H)
    # the valley: hills easing down to the fan behind the apex
    behind = ease((apex[0] + 10 - Xw + 12 * noise.fbm(X.shape, 40, 2, seed=12)) / 90)
    hills = sea + 3 + 26 * ease((np.abs(Zw) - 20) / 80) * behind + 8 * behind + 6 * noise.fbm(X.shape, 50, 3, seed=8) * behind
    H = H * (1 - behind) + np.maximum(H, hills) * behind
    rng = np.random.default_rng(9)
    chans = [([(-160, 6), (-120, -4), (-90, 2), apex], 12)]
    branches(apex, 0.0, 60, 11, 4, rng, chans)
    level = np.where(H < sea, sea, np.nan)
    for k, (pts, wd) in enumerate(chans):
        dd, al = polyline(X, Z, spline(pts, 1.5))[:2]
        surf = sea + (0.04 * np.maximum(-60 - X, 0) if k == 0 else 0.0)
        surf = np.floor(surf)
        H2, lv = channel(H, dd, surf, wd / 2, depth=1.5 + wd / 8, bank=5, seed=20 + k)
        near = dd < wd / 2 + 6
        H = np.where(near, np.minimum(H, H2) if k else H2, H)
        level = np.where(np.isfinite(lv), np.fmax(lv, level), level)
    level = np.where(H < sea, np.fmax(level, sea), level)
    near_water = ndimage.distance_transform_edt(~np.isfinite(level)) < 2.5
    sand = near_water & ~np.isfinite(level) & (H < sea + 3)
    return Scene(H, water=level, sand=sand)


def meanders(X, Z):
    """A meandering river on a floodplain: the plain rising gently toward bluffs that climb in two broken steps,
    their foot and lip wandering; the river's bends swelling downstream with sand on their insides; two old loops cut
    off as oxbow lakes; and kettle ponds filling the hollows of hummocky ground on the north bank."""
    Xw, Zw = noise.warp(X, Z, seed=1, big=16, small=4)
    plain = 24 + 1.0 * noise.fbm(X.shape, 40, 2, seed=2) + 0.012 * np.abs(Z)
    dist = np.abs(Zw - 12 * np.sin(Xw / 70)) + 3 * noise.fbm(X.shape, 10, 2, seed=3)
    H = L.profile(plain, dist, floor=24, floor_ground=plain,
                  steps=[L.Step(70, 92, 31 + 3 * noise.fbm(X.shape, 30, 2, seed=4)),
                         L.Step(104, 134, 42 + 5 * noise.fbm(X.shape, 40, 2, seed=5))],
                  jag=4 * noise.fbm(X.shape, 12, 2, seed=6), talus=(3, 10), mode="lift")
    xs = np.linspace(-170, 170, 260)
    amp = 20 + 14 * (xs + 170) / 340
    zs = amp * np.sin(xs / 24 + 0.4 * np.sin(xs / 61)) + 4 * noise.fbm((260,), 30, 2, seed=7)
    d, along = polyline(X, Z, list(zip(xs, zs)))[:2]
    surf = np.floor(23.0 - 0.004 * (X + 170))
    H, level = channel(H, d, surf, along_noise(along, 60, 8, 4.5, 6.5), depth=2.5, bank=6, seed=9)
    curv = np.gradient(np.gradient(np.interp(X[:, 0], xs, zs)))[:, None] * np.ones((1, SIZE))
    inside = np.sign(curv) * np.sign(Z - np.interp(X, xs, zs)) > 0
    bar = inside & (d > 6) & (d < 16)
    H = np.where(bar, np.minimum(H, surf + 1 + 1.2 * ease((d - 6) / 10)), H)
    for k, (cx, cz, rx, rz, a0, a1, ang) in enumerate([(-40, 36, 20, 13, 0.3, 3.3, 10), (78, -48, 22, 14, 3.4, 6.4, -20)]):
        th = np.linspace(a0, a1, 50)
        arc = [(cx + rx * np.cos(t) * np.cos(np.radians(ang)) - rz * np.sin(t) * np.sin(np.radians(ang)),
                cz + rx * np.cos(t) * np.sin(np.radians(ang)) + rz * np.sin(t) * np.cos(np.radians(ang))) for t in th]
        da, al = polyline(X, Z, arc)[:2]
        taper = np.sin(np.pi * np.clip(al / al.max(), 0, 1)) ** 0.6
        H2, lv = channel(H, da, np.floor(at(H, cx, cz)) - 0.0, 1 + 4 * taper, depth=2, bank=5, seed=30 + k)
        keep = (da < 12) & (d > 12)
        H = np.where(keep, H2, H)
        level = np.where(keep & np.isfinite(lv), lv, level)
    region = (Z < -40) & (Z > -110)
    fade = ease((-40 - Z) / 12) * ease((Z + 110) / 12)
    hum = L.lumps(np.zeros(X.shape), X, Z, 130, (-160, -110, 160, -40), (4, 11), (1.5, 4), seed=10, rough=0.3)
    ket = L.lumps(np.zeros(X.shape), X, Z, 45, (-160, -105, 160, -45), (4, 10), (2, 5), seed=11, rough=0.3)
    H = H + (2 + hum - ket) * fade
    filled = fill_basins(np.round(H))
    ponds = region & (filled - np.round(H) >= 1) & ~np.isfinite(level)
    level = np.where(ponds, filled, level)
    return Scene(H, water=level, sand=bar & ~np.isfinite(level))


def terraces(X, Z):
    """Travertine terraces: pools held behind lobed rims a block over their water, stepping down a hillside and
    brimming from each into the next, the terraced ground easing back into the plain slope round its edges."""
    slope = 30 + 70 * ease((150 - (X + 0.3 * Z)) / 300) + 4 * noise.fbm(X.shape, 50, 2, seed=1)
    Xw, Zw = noise.warp(X, Z, seed=2, big=10, small=3, big_cell=40, small_cell=9)
    scallop = 7.0 * np.abs(np.sin(Zw / 11 + 1.5 * noise.fbm(X.shape, 40, 2, seed=3))) + 2.0 * noise.fbm(X.shape, 14, 2, seed=4)
    q = slope + scallop
    flat = np.floor(q / 3.0) * 3.0
    lower = ndimage.minimum_filter(flat, size=3) < flat
    T = flat + 1 + lower
    region = ellipse_distance(Xw, Zw, (0, 0), 130, 105, angle=20) + 0.15 * noise.fbm(X.shape, 20, 2, seed=5)
    k = ease((1 - region) / 0.18)
    H = np.round(T * k + (slope + scallop * 0.3 + 2) * (1 - k))
    filled = fill_basins(H)
    pools = (filled - H >= 1) & (k > 0.95)
    level = np.where(pools, filled, np.nan)
    return Scene(H, water=level, water3d=curtains(level, H, min_drop=2))


def lava(X, Z):
    """A stratovolcano, as the first study built it (concave, warped, gullied), with its summit crater holding a lava
    lake under cooled crust; the crater rim notched on one side where the lake spills into a lava river that runs
    down the flank on a slant between levées easing out into the slope, spreading at the foot into a lobed flow;
    two spatter cones on the flank, each holding a small pond in its own crater; and a lava tube under the west
    flank open through three skylights."""
    Xw, Zw = noise.warp(X, Z, seed=200, big=18, small=5)
    c = (-10, -10)
    dist = np.hypot(Xw - c[0], (Zw - c[1]) / 0.9)
    H = 14 + 116 * np.clip(1 - dist / 150, 0, 1) ** 1.5 + 5 * noise.fbm(X.shape, 40, 3, seed=201)
    H = L.gullies(H, Xw, Zw, c, 24, 6, 30, 140, seed=4)
    rim_r = 18
    rim = float(np.median(H[np.abs(np.hypot(Xw - c[0], Zw - c[1]) - rim_r) < 1.5]))
    cr = np.hypot(Xw - c[0], Zw - c[1])
    crater = rim - 16 + 1.1 * np.maximum(0, cr - 6) ** 1.2
    H = L.smooth_min(H, crater, 4)
    theta = np.arctan2(Zw - c[1], Xw - c[0])
    notch_a = 0.7
    notch = np.exp(-((np.angle(np.exp(1j * (theta - notch_a)))) / 0.22) ** 2) * ease((34 - cr) / 16)
    lake_lv = rim - 8.0
    H = np.where(notch > 0.05, np.minimum(H, H - (H - (lake_lv - 1)) * notch * ease((cr - 8) / 6)), H)
    lv = np.where((cr < rim_r + 2) & (H < lake_lv), lake_lv, np.nan)
    crust = shatter(X, Z, 5, seed=6, warp=(2, 1, 20, 6))
    rng = np.random.default_rng(7)
    plates = np.isfinite(lv) & (crust.edge > 0.8) & (rng.random(len(crust.centres))[crust.id] < 0.5) & (cr < rim_r - 4)
    # the river: from the notch, slanting across the flank so it falls gently, a block at a time
    start = (c[0] + 22 * np.cos(notch_a), c[1] + 22 * np.sin(notch_a))
    path = spline([start, (start[0] + 20, start[1] + 26), (start[0] + 10, start[1] + 60), (start[0] + 40, start[1] + 92),
                   (start[0] + 70, start[1] + 112)], 1.0)
    d, along = polyline(X, Z, path)[:2]
    g = np.array([at(H, *p) for p in path])
    cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(np.array(path), axis=0).T))])
    g = ndimage.gaussian_filter1d(g, 6)
    s_prof = np.floor(np.minimum.accumulate(np.minimum(g - 1, lake_lv)))
    surf = np.interp(along, cum, s_prof)
    half = 3.0 + 3 * ease((along - cum[-1] * 0.8) / (cum[-1] * 0.2))
    H, rl = channel(H, d, surf, half, depth=2, bank=7, seed=8)
    levee = ease(1 - np.abs(d - half - 2.5) / 3) * 2.5 * (d < half + 7) * ease((along - 15) / 10)
    H = np.where(d > half + 0.5, H + levee, H)
    end = cum[-1]
    lobe = np.hypot((along - end) / 18, d / 22) + 0.15 * noise.fbm(X.shape, 7, 2, seed=9)
    flow_top = s_prof[-1] + 1.5 * ease((1 - lobe) / 0.3)
    H = np.where((lobe < 1) & (along > end - 25), np.maximum(H, flow_top - 1), H)
    lava_lv = np.where(np.isfinite(rl) & (d < half), surf, lv)
    # spatter cones on the flank, each with a pond in its crater
    for k, (sc, rr, hh) in enumerate([((-62, 28), 18, 14), ((-48, -78), 14, 11)]):
        Xs, Zs = noise.warp(X, Z, seed=40 + k, big=4, small=1.5, big_cell=25, small_cell=6)
        e = np.hypot(Xs - sc[0], Zs - sc[1]) / rr
        H = H + hh * np.clip(1 - e, 0, 1) ** 1.3                              # grown onto the flank, no plinth
        top = at(H, *sc)
        ce = np.hypot(X - sc[0], Z - sc[1])
        H = L.smooth_min(H, top - 6 + 1.0 * np.maximum(0, ce - 2), 3)
        cones_at = (ce < rr * 0.5) if k == 0 else cones_at | (ce < rr * 0.5)
    filled = fill_basins(np.round(H))                                      # each cone's crater, filled to its lip
    lava_lv = np.where(cones_at & (filled - np.round(H) >= 1), filled - 1, lava_lv)
    # the lava tube
    w = world()
    tube_path = spline([(-60, -20), (-82, 20), (-90, 60), (-78, 100)], 2.0)
    ts = np.linspace(0, 1, len(tube_path))
    deep = np.array([at(H, *p) for p in tube_path]) - 9
    tube = sweep(w, tube_path, lambda t: np.interp(t, ts, deep), 3.5, 3.0, 1.5, power=2.4, rough=0.12, seed=12)
    ys = np.arange(SY)[None, :, None]
    floor_y = np.where(tube.any(axis=1), np.argmax(tube, axis=1), SY)
    lava3d = tube & (ys <= floor_y[:, None, :] + 1)
    carve = tube.copy()
    for kk in (0.2, 0.5, 0.8):
        sx, sz = tube_path[int(kk * (len(tube_path) - 1))]
        hole = (np.hypot(X - sx, Z - sz) < 3.0 + 0.6 * noise.fbm(X.shape, 3, 1, seed=int(kk * 10)))[:, None, :]
        carve |= hole & (ys > floor_y[:, None, :]) & (ys <= np.round(H)[:, None, :])
    return Scene(H, lava=lava_lv, crust=plates, carve=carve, lava3d=lava3d | curtains(lava_lv, H, min_drop=3))


STUDIES = [mountain_river, plunge, delta, meanders, terraces, lava]
CORNER = {"mountain_river": ("se", "nw"), "plunge": ("se", "ne"), "delta": ("se", "ne"), "meanders": ("se", "sw"),
          "terraces": ("se", "ne"), "lava": ("se", "sw")}
ZOOM = {"plunge": (-70, -60, 60, 60), "terraces": (-60, -60, 60, 60), "lava": (-110, -110, 149, 149),
        "mountain_river": (-60, -70, 90, 70), "meanders": (-100, -100, 40, 60)}


if __name__ == "__main__":
    W.STUDIES, W.CORNER, W.ZOOM = STUDIES, CORNER, ZOOM
    W.main(sys.argv[1:])
