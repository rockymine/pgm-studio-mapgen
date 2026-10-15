"""Winter studies: shapes only. Rock in three greys by slope, ice in two pale blues (top and face), water flat.
Each study returns layers: the rock top, and optionally an ice top and bottom (ice may hang over air: a portal) and a
water level.

    python3 winter.py [name ...]      # all by default; renders into ../renders
"""
import os
import sys
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World                                                   # noqa: E402
from pgmvox.geom import noise                                                 # noqa: E402
from pgmvox.geom.noise import smoothstep, spline                              # noqa: E402
from pgmvox.geom.shapes import polyline, ellipse_distance                     # noqa: E402
from pgmvox.ground import landform as L                                       # noqa: E402
from pgmvox.read import render                                                # noqa: E402
from pgmvox.surface.terrain import slope_deg                                  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders")
SIZE, SY = 300, 256
ROCK = ((B.WOOL, 0), (B.WOOL, 8), (B.WOOL, 7))                               # gentle, steep, cliff
ICE_TOP, ICE_FACE = (B.PACKED_ICE, 0), (B.ICE, 0)


@dataclass
class Layers:
    rock: np.ndarray                         # y of the rock's top block in each column
    ice: np.ndarray = None                   # y of the ice's top block, NaN where there is none
    ice_bottom: np.ndarray = None            # y under the ice's lowest block (rock top by default): above it, air
    water: object = None                     # water surface y: a number or a field, NaN where none
    rock_bottom: np.ndarray = None
    cap: int = 0                             # top blocks of the ice drawn as snow


def grid():
    w = World(-SIZE // 2, -SIZE // 2, SIZE, SIZE, sy=SY)
    X, Z = w.grid()
    return w, X.astype(float), Z.astype(float)


def at(F, x, z):
    return float(F[int(round(x)) + SIZE // 2, int(round(z)) + SIZE // 2])


def along_noise(along, cell, seed, lo, hi):
    n = int(along.max()) + 2
    f = noise.fbm((n,), cell, 3, seed=seed)
    f = (f - f.min()) / max(np.ptp(f), 1e-6)
    return lo + (hi - lo) * np.interp(along, np.arange(n), f)


def cells(X, Z, spacing, seed, jitter=0.8, warp=(6, 2)):
    """shapes.shatter, unpacked."""
    from pgmvox.geom.shapes import shatter
    p = shatter(X, Z, spacing, seed=seed, jitter=jitter, warp=(warp[0], warp[1], 60, 12))
    return p.id, p.edge, p.centres


def mountains(X, seed, base=60, relief=60):
    """High rough ground: ridged noise for crests and fbm for bulk."""
    r = noise.ridged(X.shape, 70, 4, seed=seed, sharpness=1.6)
    return base + relief * (0.55 * r + 0.45 * (0.5 + 0.5 * noise.fbm(X.shape, 110, 3, seed=seed + 1)))


# --- the studies ---------------------------------------------------------------------------------------------------

def glacier_tongue(X, Z):
    """A valley glacier running down a U-shaped canyon: a convex tongue between lateral moraines, an icefall where the
    floor drops and the ice breaks into seracs, transverse crevasses bowed down-valley below it and chevron crevasses
    at the margins, and a snout that ends in an ice cliff over a lake, calving into bergs, a meltwater portal under
    it, a terminal moraine ringing the lake."""
    rock = 92 + 55 * noise.ridged(X.shape, 95, 4, seed=1, sharpness=1.3) + 14 * noise.fbm(X.shape, 120, 3, seed=2)
    path = spline([(-165, -42), (-110, -38), (-60, -18), (-5, -24), (45, -2), (100, 6), (165, 26)], 2.0)
    d, along, side = polyline(X, Z, path, side=True)
    total = float(along.max())
    t = np.clip(along / total, 0, 1)
    drop = 26 * smoothstep(0.27, 0.38, t)                                  # the step the icefall pours over
    floor = 96 - 40 * t - drop
    snout, lake_end = 0.64, 0.88
    widen = 12 * smoothstep(snout - 0.12, snout - 0.02, t) * smoothstep(lake_end + 0.04, lake_end - 0.04, t)
    half = along_noise(along, 60, 11, 24, 34) + widen
    wall = np.where(side > 0, along_noise(along, 40, 12, 14, 24), along_noise(along, 40, 13, 20, 36))
    u = np.clip((d - half) / wall, 0, 1)
    jag = 2.5 * noise.fbm(X.shape, 7, 2, seed=14)
    spurs = 6 * noise.ridged(X.shape, 14, 2, seed=15, sharpness=3) * u * (1 - u) * 4        # spurs and gullies on the walls
    valley = floor + 80 * u ** 1.5 + spurs + 7 * smoothstep(half + wall * 0.55, half + wall * 0.62, d + jag)  # trimline
    rock = np.where(d < half + wall * 1.4, np.minimum(rock, valley), rock)
    a_c, a_r = (snout + 0.06) * total, 0.17 * total                       # the lake reaches back under the breaking ice
    le = np.hypot((along - a_c) / a_r, d / (half - 2)) + 0.07 * noise.fbm(X.shape, 14, 2, seed=28)
    rock = rock - 12 * smoothstep(1.0, 0.75, le)                            # the lake basin, rounded
    b0, b1 = snout - 0.11, snout + 0.03                                     # where the tongue breaks up, start to end
    level = float(np.median(floor[(np.abs(t - (snout - 0.04)) < 0.005) & (d < 2)])) - 2
    w_ice = half - 5
    end = b1 + 0.012 * noise.fbm(X.shape, 10, 2, seed=16) + 0.015 * (d / w_ice) ** 2
    thick = 22 - 12 * np.clip(t / snout, 0, 1)
    body = floor + thick * np.clip(1 - (d / w_ice) ** 4, 0, 1) ** 0.5            # flat across, rounded at the edges
    on = (d < w_ice) & (t < end) & (t > 0.01)
    ice = np.where(on, body, np.nan)
    # the icefall: seracs, blocks lifted or dropped and tilted, with gaps between them
    cid, edge, pts = cells(X, Z, 8, 17, warp=(3, 1))
    rng = np.random.default_rng(18)
    lift = rng.uniform(-6, 6, len(pts))
    tilt = rng.uniform(-0.6, 0.6, (len(pts), 2))
    fall = smoothstep(0.24, 0.29, t) * smoothstep(0.44, 0.38, t)
    serac = lift[cid] + tilt[cid, 0] * (X - pts[cid, 0]) + tilt[cid, 1] * (Z - pts[cid, 1])
    ice = ice + fall * (serac - 8 * smoothstep(1.8, 0.4, edge))
    # transverse crevasses below the icefall, bowed down-valley, opened by noise
    phase = (along + 0.025 * d ** 2) / 8 + 0.5 * noise.fbm(X.shape, 30, 2, seed=19)
    gap = np.abs(phase - np.round(phase)) * 8
    open_ = 0.7 + 0.8 * (0.5 + 0.5 * noise.fbm(X.shape, 9, 2, seed=20))
    zone = smoothstep(0.38, 0.42, t) * smoothstep(0.54, 0.48, t)
    ice = np.where((gap < open_) & (zone > 0.5), ice - 8, ice)
    # chevron crevasses at the margins, pointing up-glacier at about 45 degrees
    chev = (along - 0.9 * d) / 7 + 0.3 * noise.fbm(X.shape, 20, 2, seed=21)
    margin = (d > 0.62 * w_ice) & (t > 0.05) & (fall < 0.1) & (t < b0)
    ice = np.where(margin & (np.abs(chev - np.round(chev)) * 7 < 0.8), ice - 6, ice)
    # moraines: ridges along both margins, swinging round the lake as the terminal moraine
    lateral = 7 * np.exp(-((d - (w_ice + 3)) / 2.4) ** 2) * (t < b0 + 0.02) * (1 + 0.35 * noise.fbm(X.shape, 8, 2, seed=23))
    medial = 3 * np.exp(-((d - 6) / 1.6) ** 2) * (side > 0) * (t < b0)
    term = 9 * np.exp(-((le - 1.1) / 0.08) ** 2) * (along > a_c) * (1 + 0.3 * noise.fbm(X.shape, 7, 2, seed=24))
    rock = rock + lateral * (d < half + 6) + term
    ice = np.where(on, ice + medial, ice)
    # the break-up: the tongue splits into blocks whose gaps widen, which sink toward the water and tip, until only
    # scattered bergs are left
    bid, bedge, bpts = cells(X, Z, 9, 25, warp=(3, 1))
    rng = np.random.default_rng(26)
    n = len(bpts)
    size = rng.uniform(0.55, 1.0, n)
    roll = rng.random(n)
    btilt = rng.uniform(-0.35, 0.35, (n, 2))
    k = np.clip((t - b0) / (end - b0), 0, 1)                                  # 0 where it starts to break, 1 at its end
    afloat = level + 1.5 + 8 * size[bid] * (1 - 0.5 * k) + 1.2 * noise.fbm(X.shape, 5, 1, seed=27)
    afloat = afloat + k * (btilt[bid, 0] * (X - bpts[bid, 0]) + btilt[bid, 1] * (Z - bpts[bid, 1]))
    breaking = on & (t > b0)
    kept = (bedge > 0.3 + 4.0 * k ** 1.3) & (roll[bid] > 0.4 * k ** 1.5)
    ice = np.where(breaking, np.where(kept, body * (1 - k ** 0.7) + afloat * k ** 0.7, np.nan), ice)
    # bergs beyond the end, bigger and denser near it
    dist = np.clip((t - b1) / 0.18, 0, 1)
    berg = (t > end) & (le < 0.92) & (roll[bid] > 0.35 + 0.55 * dist) & (bedge > 1.2 + 3.5 * (1 - size[bid]) + 2 * dist)
    ice = np.where(berg, level + 1 + (7 - 5 * dist) * size[bid] + 1.2 * noise.fbm(X.shape, 5, 1, seed=27), ice)
    floating = berg | (breaking & kept & (k > 0.12))
    bottom = np.where(floating, level - 4, rock)
    outwash = (along > a_c + a_r * 1.2) & (d < half)
    rock = L.lumps(rock, X, Z, 140, (-150, -150, 150, 150), (2, 6), (1.5, 4), seed=29, mask=outwash, rough=0.2)   # hummocky moraine
    lake = (rock < level) & (le < 1.05)
    water = np.where(lake, level, np.nan)
    return Layers(rock, ice, bottom, water)


def pack_ice(X, Z):
    """Sea ice broken into big floes: plates cut along bent cell edges, each its own thickness, a few tipped; hairline
    cracks inside the plates where they have started to split; jagged pressure ridges where plates were driven
    together; a lead torn across the field, its edges ragged and stepped, full of broken ice and a few drifting
    floes; open water in an irregular polynya; ice piled against a rocky island."""
    level = 30.0
    rock = np.full(X.shape, 14.0) + 3 * noise.fbm(X.shape, 40, 2, seed=1)
    isle = ellipse_distance(X, Z, (70, -60), 34, 24, angle=30) + 0.18 * noise.fbm(X.shape, 14, 3, seed=2)
    rock = L.mound(rock, isle, 46, power=1.3)
    rock = L.terraces(rock, rock > level, step=6, riser=0.7)
    cid, edge, pts = cells(X, Z, 42, 3, jitter=0.9, warp=(12, 3))
    rng = np.random.default_rng(4)
    n = len(pts)
    thick = rng.uniform(1.5, 4.5, n)
    tipped = rng.random(n) < 0.15
    tilt = rng.uniform(-0.08, 0.08, (n, 2)) * tipped[:, None]
    gap = rng.uniform(0.8, 3.0, n)
    welded = rng.random(n) < 0.35                                          # plates pushed together: no gap, a ridge
    top = level + thick[cid] + tilt[cid, 0] * (X - pts[cid, 0]) + tilt[cid, 1] * (Z - pts[cid, 1])
    floe = (edge > np.where(welded[cid], 0, gap[cid]))
    # hairline cracks inside the plates, each piece settled a little differently
    sub, subedge, spts = cells(X, Z, 15, 5, warp=(4, 1.5))
    srng = np.random.default_rng(6)
    cracked = srng.random(len(spts)) < 0.55
    floe &= ~(cracked[sub] & (subedge < 0.55))
    top = top + srng.uniform(-0.8, 0.8, len(spts))[sub] * cracked[sub]
    # pressure ridges along welded borders: a jagged crest, not a row of mounds
    crest = (2 + 5 * noise.ridged(X.shape, 4, 2, seed=7, sharpness=2)) * (0.5 + 0.5 * noise.fbm(X.shape, 30, 2, seed=8))
    ridge = welded[cid] & (edge < 3.5)
    top = top + np.where(ridge, crest * np.exp(-(edge / 2.0) ** 2), 0)
    # the lead: a torn channel of varying width, its edges ragged and stepped, brash ice and floes in it
    path = spline([(-160, 70), (-110, 52), (-70, 66), (-20, 40), (30, 58), (80, 30), (120, 44), (160, 22)], 2.0)
    ld, lal = polyline(X, Z, path)[:2]
    width = along_noise(lal, 40, 9, 4, 16) + 3 * noise.fbm(X.shape, 6, 2, seed=10) + 2 * np.round(noise.fbm(X.shape, 20, 1, seed=11) * 2)
    lead = ld < width
    bid, bedge, bpts = cells(X, Z, 4.5, 12, warp=(1.5, 0.5))
    brng = np.random.default_rng(13)
    near_edge = np.clip(ld / np.maximum(width, 1), 0, 1)
    brash = lead & (brng.random(len(bpts))[bid] < 0.15 + 0.45 * near_edge) & (bedge > 0.7)
    mid, medge, mpts = cells(X, Z, 11, 14, warp=(3, 1))
    drifting = lead & (brng.random(len(mpts))[mid] < 0.18) & (medge > 1.4)
    # a polynya: open water of no particular shape
    near = np.hypot(pts[:, 0] + 80, pts[:, 1] + 70)
    gone = np.argsort(near)[:3]                                          # three neighbouring floes drifted away
    poly = np.isin(cid, gone) & (noise.fbm(X.shape, 9, 2, seed=15) > -0.55)
    plates = floe & ~lead & ~poly
    ice = np.where(plates, top, np.nan)
    ice = np.where(drifting, level + 1 + 2 * brng.uniform(0.5, 1, len(mpts))[mid], ice)
    ice = np.where(brash & ~drifting, level + 1 + (brng.random(len(bpts))[bid] < 0.4), ice)
    # ice driven up against the island's shore
    from scipy import ndimage
    off = ndimage.distance_transform_edt(rock < level)                    # blocks out from the shoreline
    reach = 3 + 7 * (0.5 + 0.5 * noise.fbm(X.shape, 20, 2, seed=17))
    piled = (off < reach) & (noise.fbm(X.shape, 25, 2, seed=18) > -0.2)
    ice = np.where(piled & np.isfinite(ice), ice + (2 + 6 * noise.ridged(X.shape, 4, 2, seed=16, sharpness=2)) * smoothstep(reach, 1, off), ice)
    on = np.isfinite(ice) & (rock < level)
    ice = np.where(on, np.maximum(ice, level + 1), np.nan)
    bottom = np.where(on, level - 2, rock)
    return Layers(rock, ice, bottom, np.where(rock < level, level, np.nan))


def ice_shelf(X, Z):
    """An ice shelf meeting the sea: a flat sheet flowing off a rocky coast, crevassed where it leaves the land, its
    surface rolled into flow stripes, rifts opening behind a ragged calving front, and tabular bergs broken off and
    drifting, one of them rolled over on its side."""
    level = 22.0
    coast = -70 + 18 * noise.fbm((X.shape[0],), 60, 3, seed=1)[:, None]
    rock = 10 + 70 * smoothstep(coast + 10, coast - 40, Z) + 25 * noise.ridged(X.shape, 50, 3, seed=2) * smoothstep(coast, coast - 40, Z)
    front = 40 + 14 * noise.fbm((X.shape[0],), 25, 3, seed=3)[:, None] + 6 * noise.fbm((X.shape[0],), 6, 2, seed=4)[:, None]
    surf = level + 18 + 2.5 * np.sin(X / 7 + 2 * noise.fbm(X.shape, 50, 2, seed=5)) * 0.5   # flow stripes
    surf = surf + 10 * smoothstep(coast + 30, coast - 5, Z)                                  # thicker on the land
    shelf = Z < front
    # crevasses where it leaves the land: cuts parallel to the coast
    g = (Z - coast) / 6 + 0.9 * noise.fbm(X.shape, 20, 2, seed=6) + 0.4 * noise.fbm(X.shape, 6, 1, seed=8)
    crev = (np.abs(g - np.round(g)) < 0.08 + 0.1 * (0.5 + 0.5 * noise.fbm(X.shape, 15, 2, seed=10))) & (Z > coast - 8) & (Z < coast + 28)
    surf = np.where(crev, surf - 9, surf)
    # rifts behind the front: two cracks running in from the edge
    for k, pts in enumerate([[(-90, 60), (-70, 32), (-40, 22)], [(30, 70), (45, 30), (80, 20), (110, 18)]]):
        rd = polyline(X, Z, spline(pts, 2.0))[0]
        width = 2 + 3 * k
        shelf &= rd > width + 1.2 * noise.fbm(X.shape, 6, 2, seed=7 + k)
    ice = np.where(shelf & (Z > coast - 40), surf, np.nan)
    bottom = np.where(np.isfinite(ice), np.minimum(rock, level - 8), rock)
    bottom = np.where(np.isfinite(ice) & (rock > level - 8), rock, bottom)
    # tabular bergs: warped polygons of shelf afloat beyond the front
    rng = np.random.default_rng(9)
    for k, (c, rx, rz, ang) in enumerate([((-100, 95), 26, 14, 10), ((-20, 105), 18, 12, -20), ((60, 92), 30, 16, 35),
                                          ((120, 120), 12, 9, 0), ((20, 135), 9, 6, 60)]):
        Xw, Zw = noise.warp(X, Z, seed=20 + k, big=4, small=1.5, big_cell=30, small_cell=8)
        e = ellipse_distance(Xw, Zw, c, rx, rz, angle=ang)
        poly = np.maximum(np.abs((Xw - c[0])) / (rx * 1.15), np.abs(Zw - c[1]) / (rz * 1.15))
        m = np.maximum(e * 0.6, poly) < 1
        t = level + 16 - 4 * k * 0.6 + 1.5 * np.sin(Xw / 7)
        if k == 2:                                                        # rolled: one edge up, one in the water
            t = level + 2 + 0.45 * ((Xw - c[0]) * np.cos(np.radians(ang)) + (Zw - c[1]) * np.sin(np.radians(ang)) + rx)
        ice = np.where(m & (Z > front + 4), t, ice)
        bottom = np.where(m & (Z > front + 4), level - 8, bottom)
    return Layers(rock, ice, bottom, np.where(rock < level, level, np.nan))


def cirques(X, Z):
    """A glaciated massif: a horn peak with four cirques bitten into its sides, knife-edge aretes between them, small
    glaciers filling the floors of two bowls up against their headwalls, tarns in the other two, and gullied flanks."""
    Xw, Zw = noise.warp(X, Z, seed=31, big=10, small=3)
    d = np.hypot(Xw, Zw)
    rock = 18 + 150 * np.clip(1 - d / 140, 0, 1) ** 1.8 + 10 * noise.fbm(X.shape, 40, 3, seed=32)
    rock = L.smooth_max(12 + 6 * noise.fbm(X.shape, 60, 2, seed=33), rock, 10)
    rock = L.gullies(rock, Xw, Zw, (0, 0), 22, 6, 60, 135, seed=50)
    bowls = []
    for k, (ang, r0, size, depth, tarn) in enumerate([(20, 36, 40, 50, True), (115, 32, 34, 44, False),
                                                      (205, 40, 44, 48, False), (295, 34, 30, 40, True)]):
        a = np.radians(ang)
        c = (r0 * np.cos(a), r0 * np.sin(a))                               # the bowl's centre, below the summit
        u = (Xw - c[0]) * np.cos(a) + (Zw - c[1]) * np.sin(a)                 # outward from the peak
        v = -(Xw - c[0]) * np.sin(a) + (Zw - c[1]) * np.cos(a)
        e = np.hypot(np.where(u < 0, u, 0.45 * u), v) / size              # a bowl open on its downhill side
        floor = at(rock, *c) - depth
        headwall = floor + 95 * np.clip(e - 0.35, 0, None) ** 1.25
        rock = np.where(e < 1.6, np.minimum(rock, headwall), rock)
        bowls.append((u, v, e, floor, size, tarn))
    ice = np.full(X.shape, np.nan)
    water = np.full(X.shape, np.nan)
    for k, (u, v, e, floor, size, tarn) in enumerate(bowls):
        if tarn:
            rock = np.where(e < 0.5, np.minimum(rock, floor - 3 + 7 * e), rock)
            lip = floor + 1.5 + 2 * noise.fbm(X.shape, 6, 1, seed=80 + k) - 70 * np.clip(e - 0.62, 0, None)
            rock = np.where((e > 0.5) & (u > 0), np.maximum(rock, lip), rock)   # a rock lip holding it, falling away downhill
            water = np.where((e < 0.55) & (rock < floor + 0.5), floor + 0.5, water)
        else:
            surf = floor + 3 + 18 * np.clip(-u / size + 0.25, 0, 1) ** 1.4 + 1.5 * noise.fbm(X.shape, 10, 2, seed=60 + k)
            fill = (e < 0.95) & (surf > rock + 1) & (u < size * 0.35)
            berg = np.abs((u / 5 + 0.4 * noise.fbm(X.shape, 12, 1, seed=70 + k)) % 1 - 0.5) < 0.08   # a bergschrund-like crack
            ice = np.where(fill, surf - 3 * (berg & (e > 0.8)), ice)
    return Layers(rock, ice, None, water)


def snowfield(X, Z):
    """Snow over rock: drifts shaped by a wind from the west, smooth and flowing, piled into tails behind every
    rock; irregular outcrops of faceted, tilted rock breaking through; and deep cracks splitting the ice under the
    snow, zigzagging and branching, some bridged by snow, opening down into the rock."""
    from scipy import ndimage
    base = 26 + 14 * noise.fbm(X.shape, 110, 3, seed=1)
    # outcrops: faceted blocks, each cell its own tilted plane, only where a blob of noise says rock comes up
    cid, edge, pts = cells(X, Z, 11, 2, warp=(5, 2))
    rng = np.random.default_rng(3)
    n = len(pts)
    plane = rng.uniform(3, 11, n)[cid] + rng.uniform(-0.55, 0.55, n)[cid] * (X - pts[cid, 0]) + rng.uniform(-0.55, 0.55, n)[cid] * (Z - pts[cid, 1])
    blob = noise.fbm(X.shape, 40, 3, seed=4) + 0.45 * noise.fbm(X.shape, 10, 2, seed=5)
    crag = np.clip(blob + 0.05, 0, None) / 0.45
    rock = base + np.clip(plane * crag, 0, None) * (1 + 0.25 * noise.ridged(X.shape, 5, 2, seed=6)) - 2 * smoothstep(0.8, 0, edge) * crag
    rock = rock + 3 * noise.ridged(X.shape, 18, 3, seed=7) * crag
    # the snow: rock smoothed far, a depth of snow, drift ridges across the wind, tails behind the rocks
    smooth = ndimage.gaussian_filter(rock, 9)
    tail = ndimage.gaussian_filter(np.roll(np.clip(rock - smooth, 0, None), 9, axis=0), (12, 3))   # downwind is east
    Xw, Zw = noise.warp(X, Z, seed=8, big=14, small=3, big_cell=70, small_cell=15)
    drift = 2.2 * np.sin(Xw / 9 + 0.3 * Zw / 9) * (0.6 + 0.4 * noise.fbm(X.shape, 50, 2, seed=9))
    drift = drift + 1.0 * np.abs(np.sin(Xw / 3.2 + Zw / 14))                # sastrugi: small sharp ridges
    scoured = np.clip(rock - smooth, 0, None)                             # the wind strips snow off what stands up
    snow = smooth + 3.5 + drift + 1.6 * tail - 0.6 * scoured
    # cracks: zigzag lines with branches, opening down through the ice into the rock, a few bridged
    ice_top = snow.copy()
    deep = np.zeros(X.shape)
    crng = np.random.default_rng(10)
    for k in range(10):
        x0, z0 = crng.uniform(-140, 140), crng.uniform(-140, 140)
        ang = crng.uniform(0, np.pi)
        pts_k = [(x0, z0)]
        for _ in range(7):
            ang += crng.uniform(-0.7, 0.7)
            step = crng.uniform(10, 22)
            pts_k.append((pts_k[-1][0] + step * np.cos(ang), pts_k[-1][1] + step * np.sin(ang)))
        dd, al = polyline(X, Z, pts_k)[:2]
        w = along_noise(al, 20, 20 + k, 1.2, 4.5) * smoothstep(0, 12, al) * smoothstep(al.max(), al.max() - 12, al)
        depth = along_noise(al, 30, 40 + k, 14, 30)
        bridged = noise.fbm(X.shape, 10, 1, seed=60 + k) > 0.45
        deep = np.where((dd < w) & ~bridged, np.maximum(deep, depth * smoothstep(w, w * 0.3, dd)), deep)
        if k % 2 == 0:                                                     # a branch
            j = crng.integers(2, 6)
            bx, bz = pts_k[j]
            ba = ang + crng.choice([-1, 1]) * crng.uniform(0.8, 1.3)
            br = [(bx, bz), (bx + 18 * np.cos(ba), bz + 18 * np.sin(ba)), (bx + 30 * np.cos(ba + 0.4), bz + 30 * np.sin(ba + 0.4))]
            bd, bal = polyline(X, Z, br)[:2]
            bw = 1.6 * smoothstep(bal.max(), 0, bal) + 0.4
            deep = np.where(bd < bw, np.maximum(deep, 16 * smoothstep(bw, bw * 0.3, bd)), deep)
    exposed = rock >= snow - 0.5
    floor = ice_top - deep
    rock = np.where(deep > 0, np.minimum(rock, floor), rock)
    ice = np.where(~exposed, ice_top, np.nan)
    ice = np.where(deep > 0.5, np.where(floor > rock + 0.5, floor, np.nan), ice)
    return Layers(rock, ice, None, None, cap=2)


STUDIES = [glacier_tongue, pack_ice, ice_shelf, cirques, snowfield]
BOXES = {"glacier_tongue": (-150, -150, 149, 40)}
ZOOMS = {"glacier_tongue": {"snout": ((10, -45, 149, 60), 4), "icefall": ((-110, -70, 20, 40), 4)},
         "snowfield": {"close": ((-60, -60, 60, 60), 4)}, "pack_ice": {"close": ((-80, -10, 60, 120), 4)}}
CORNER = {"glacier_tongue": "se", "pack_ice": "se", "ice_shelf": "nw", "cirques": "se", "snowfield": "se"}


# --- building and drawing ------------------------------------------------------------------------------------------

def build(lay):
    w, X, Z = grid()
    ys = np.arange(SY)[None, :, None]
    rock = np.clip(np.round(lay.rock), 1, SY - 2).astype(int)
    deg = slope_deg(rock)
    tone = np.where(deg < 30, 0, np.where(deg < 50, 1, 2))
    if lay.cap:
        tone = np.maximum(tone, 1)                                       # rock reads grey against the snow
    rb = 0 if lay.rock_bottom is None else lay.rock_bottom[:, None, :]
    solid = (ys <= rock[:, None, :]) & (ys >= rb)
    w.ids[...] = np.where(solid, B.STONE, 0)
    skin = solid & (ys > rock[:, None, :] - 3)
    w.ids[...] = np.where(skin, np.array([ROCK[k][0] for k in range(3)], np.uint16)[tone][:, None, :], w.ids)
    w.dat[...] = np.where(skin, np.array([ROCK[k][1] for k in range(3)], np.uint8)[tone][:, None, :], 0)
    top = rock.copy()
    if lay.ice is not None:
        has = np.isfinite(lay.ice)
        it = np.clip(np.round(np.nan_to_num(lay.ice, nan=-1)), -1, SY - 2).astype(int)
        ib = rock if lay.ice_bottom is None else np.round(lay.ice_bottom).astype(int)
        ideg = slope_deg(np.where(has, it, rock), mask=has)
        body = has[:, None, :] & (ys <= it[:, None, :]) & (ys > ib[:, None, :])
        steep = (ideg >= 45)[:, None, :]
        w.ids[...] = np.where(body, np.where((ys == it[:, None, :]) & ~steep, ICE_TOP[0], ICE_FACE[0]), w.ids)
        w.dat[...] = np.where(body, 0, w.dat)
        if lay.cap:
            w.ids[...] = np.where(body & (ys > it[:, None, :] - lay.cap), B.SNOW, w.ids)
        top = np.where(has, np.maximum(top, it), top)
    if lay.water is not None:
        wl = np.broadcast_to(np.asarray(lay.water, float), rock.shape)
        has = np.isfinite(wl)
        lv = np.round(np.nan_to_num(wl, nan=-1)).astype(int)
        wet = has[:, None, :] & (ys <= lv[:, None, :]) & (w.ids == 0)
        w.ids[...] = np.where(wet, B.WATER, w.ids)
        top = np.where(has, np.maximum(top, lv), top)
    return w, top


def plan_view(w, top, out, title, scale=3):
    """From above: the top block's colour, hill-shaded from the north-west, a contour every 5 blocks."""
    from pgmvox.core import blocks as K
    sx, sz = top.shape
    ids = w.ids[np.arange(sx)[:, None], np.clip(top, 0, SY - 1), np.arange(sz)[None, :]]
    dat = w.dat[np.arange(sx)[:, None], np.clip(top, 0, SY - 1), np.arange(sz)[None, :]]
    col = K.COLOURS[ids, dat & 15].astype(float)
    gx, gz = np.gradient(top.astype(float))
    col *= np.clip(1 + 0.12 * (gx + gz), 0.55, 1.35)[..., None]
    band = np.floor(top / 5)
    cont = (band != np.roll(band, 1, 0)) | (band != np.roll(band, 1, 1))
    col[cont] *= 0.7
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8).transpose(1, 0, 2)).resize((sx * scale, sz * scale), Image.NEAREST)
    ImageDraw.Draw(im).text((8, 6), f"{title}  (north up; contours every 5; y {top.min()}..{top.max()})", fill=(0, 0, 0))
    im.save(out)


def sheet(names, kind, out, cols=3, tw=600):
    tiles = [Image.open(f"{OUT}/{n}-{kind}.png").convert("RGB") for n in names]
    tiles = [t.resize((tw, int(t.height * tw / t.width))) for t in tiles]
    th = max(t.height for t in tiles) + 24
    rows = (len(tiles) + cols - 1) // cols
    im = Image.new("RGB", (cols * tw, rows * th), (205, 220, 235))
    d = ImageDraw.Draw(im)
    for k, (n, t) in enumerate(zip(names, tiles)):
        x, y = (k % cols) * tw, (k // cols) * th
        im.paste(t, (x, y + 22))
        d.text((x + 10, y + 6), f"{k + 1}. {n.replace('_', ' ')}", fill=(0, 0, 0))
    im.save(out)


def main(names):
    os.makedirs(OUT, exist_ok=True)
    done = []
    for f in STUDIES:
        n = f.__name__
        if names and n not in names:
            continue
        _, X, Z = grid()
        lay = f(X, Z)
        w, top = build(lay)
        box = BOXES.get(n)
        render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-iso.png", scale=2, corner=CORNER.get(n, "se"), box=box)
        for tag, (zbox, zscale) in ZOOMS.get(n, {}).items():
            render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}-{tag}.png", scale=zscale, corner=CORNER.get(n, "se"), box=zbox)
            render.trim(f"{OUT}/{n}-{tag}.png")
        render.trim(f"{OUT}/{n}-iso.png")
        plan_view(w, top, f"{OUT}/{n}-plan.png", n)
        ice = 0 if lay.ice is None else int(np.isfinite(lay.ice).sum())
        print(f"{n:17s} top {top.max():4d}  low {top.min():3d}  ice columns {ice:6d}")
        done.append(n)
    if not names:
        sheet(done, "iso", f"{OUT}/00-sheet.png")
        sheet(done, "plan", f"{OUT}/01-plans.png")


if __name__ == "__main__":
    main(sys.argv[1:])
