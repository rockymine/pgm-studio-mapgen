"""The ground of Sixes and Sevens, Red's half: the snowfield, its rock, drifts, mud paths and crevasses; the mountain
over the bunker, carrying the same snowfield pushed further; laid into the world. Blue's half is its half turn.

    rock, snow = heights(X, Z)        # the rock's top and the snow's surface in every column
    lay(w, rock, snow, X, Z)          # stone, rock skin, snow, mud, crevasses and their lava
"""
import math

import numpy as np
from scipy import ndimage

from pgmvox import B
from pgmvox.geom import noise
from pgmvox.geom.noise import smoothstep
from pgmvox.geom.shapes import inside, polyline, shatter
from pgmvox.surface.terrain import slope_deg

import plan as P

SNOW = (B.SNOW, 0)
PACKED = (B.PACKED_ICE, 0)
STONE, ANDESITE, POL_ANDESITE, COBBLE = (B.STONE, 0), (B.STONE, 5), (B.STONE, 6), (B.COBBLE, 0)
GRAVEL = (B.GRAVEL, 0)
MUD = [((B.DIRT, 1), 5), ((B.DIRT, 2), 3), (GRAVEL, 2), ((B.DIRT, 0), 2), (COBBLE, 1)]
ROCK_SKIN = [(STONE, ANDESITE, COBBLE), (ANDESITE, COBBLE, STONE), (COBBLE, ANDESITE, GRAVEL)]   # gentle, steep, cliff
STRATA = [STONE, ANDESITE, STONE, COBBLE, ANDESITE, POL_ANDESITE, STONE, ANDESITE]
FIELD_SNOW = 2                          # snow over the field's rock
TIER = [(-72, -110), (-74, -62), (-70, -26), (-80, 14), (-76, 58), (-84, 110)]   # the mountain's upper step
NEEDLES = [((-104, -40), 66), ((-122, 46), 40)]          # (x, z) and how far each rises over the ground


def snowfield(X, Z, base, rock_amp, rock_cover, drift, seed, spacing=11):
    """The winter study's snowfield as a pattern over any base: faceted rock breaking through where a blob of noise
    brings it up, each facet its own tilted plane; drifts across a wind from the west, sharp small ridges on them,
    piled into tails behind the rock and scoured off what stands up. `rock_amp` (blocks) and `drift` (a share of
    the study's drifts) may be fields, so a calm lane and a wild mountain are one pattern. Returns (rock, snow)."""
    p = shatter(X, Z, spacing, seed=seed, warp=(5, 2, 60, 12))
    rng = np.random.default_rng(seed + 1)
    n = len(p.centres)
    cx, cz = p.centres[p.id, 0], p.centres[p.id, 1]
    plane = rng.uniform(0.3, 1.0, n)[p.id] * rock_amp + rng.uniform(-0.55, 0.55, n)[p.id] * (X - cx) \
        + rng.uniform(-0.55, 0.55, n)[p.id] * (Z - cz)
    blob = noise.fbm(X.shape, 40, 3, seed=seed + 2) + 0.45 * noise.fbm(X.shape, 10, 2, seed=seed + 3)
    crag = np.clip(blob + rock_cover, 0, None) / 0.45
    rock = base + np.clip(plane * crag, 0, None) * (1 + 0.25 * noise.ridged(X.shape, 5, 2, seed=seed + 4)) \
        - 2 * smoothstep(0.8, 0, p.edge) * crag
    rock = rock + 3 * noise.ridged(X.shape, 18, 3, seed=seed + 5) * crag * np.clip(rock_amp / 10, 0, 1.5)
    smooth = ndimage.gaussian_filter(rock, 9)
    tail = ndimage.gaussian_filter(np.roll(np.clip(rock - smooth, 0, None), 9, axis=0), (12, 3))   # downwind east
    Xw, Zw = noise.warp(X, Z, seed=seed + 6, big=14, small=3, big_cell=70, small_cell=15)
    wave = 2.2 * np.sin(Xw / 9 + 0.3 * Zw / 9) * (0.6 + 0.4 * noise.fbm(X.shape, 50, 2, seed=seed + 7)) \
        + 1.0 * np.abs(np.sin(Xw / 3.2 + Zw / 14))
    scoured = np.clip(rock - smooth, 0, None)
    snow = smooth + drift * wave + 1.6 * drift * tail - 0.6 * scoured
    return rock, snow


def _cracks_on(X, Z, mask, seed, count, depth=(10, 22)):
    """Zigzag cracks with branches inside `mask`, some bridged by snow, as a depth below the surface."""
    deep = np.zeros(X.shape)
    r = np.random.default_rng(seed)
    xs, zs = X[mask], Z[mask]
    for k in range(count):
        i = r.integers(len(xs))
        pts, ang = [(xs[i], zs[i])], r.uniform(0, math.pi)
        for _ in range(6):
            ang += r.uniform(-0.7, 0.7)
            step = r.uniform(8, 16)
            pts.append((pts[-1][0] + step * math.cos(ang), pts[-1][1] + step * math.sin(ang)))
        d, al = polyline(X, Z, pts)
        width = 0.8 + 1.6 * smoothstep(0, 10, al) * smoothstep(al.max(), al.max() - 10, al)
        bridged = noise.fbm(X.shape, 10, 1, seed=seed + 60 + k) > 0.45
        dep = r.uniform(*depth)
        deep = np.where((d < width) & ~bridged, np.maximum(deep, dep * smoothstep(width, width * 0.3, d)), deep)
    return np.where(mask, deep, 0)


def _behind(X, Z, pts, face_right=False):
    """Distance from a line, positive on the side away from its face and negative in front, and the share along
    it. A lofted wall faces (-dz, dx) of its direction, which is the polyline's right side (x east, z south)."""
    d, al, side = polyline(X, Z, pts, side=True)
    total = max(1e-9, sum(math.dist(a, b) for a, b in zip(pts, pts[1:])))
    return (-d * side if face_right else d * side), al / total


def crests():
    """Every edge the ground behind must stay a block under for three blocks: (top line [(x, z)], tops, foot line or
    None, the feet's heights). Between a lofted wall's foot and its top the ground stays under the foot, since the
    wall stands there."""
    out = []
    for edges in P.LOFTS.values():
        out.append(([(t[0], t[2]) for b, t in edges], [t[1] for b, t in edges], [(b[0], b[2]) for b, t in edges],
                    [b[1] for b, t in edges]))
    top = P.FIELD + P.FRONT_H
    out.append(([(P.FACADE_X - 1.5, P.FACADE_Z[1] + 2.5), (P.FACADE_X - 1.5, P.FACADE_Z[0] - 2.5)], [top, top], None,
                None))
    return out


def heights(X, Z):
    """The rock's top and the snow's surface over Red's half (and, unused, the rest of the grid)."""
    dfront = np.vectorize(P.front_x)(Z) - X                     # inside the mountain where positive
    mountain = (dfront > 0) & (X < 0)
    # the field: calm by the paths, the bunker's front, the yard and the crossings, rock and drift let out elsewhere
    calm = np.zeros(X.shape)
    for p in P.PATHS:
        d, _ = polyline(X, Z, p)
        calm = np.maximum(calm, smoothstep(P.PATH_WIDTH / 2 + 6, P.PATH_WIDTH / 2, d))
    apron = smoothstep(30, 8, np.hypot(np.maximum(0, X - P.FACADE_X), np.maximum(0, np.abs(Z - 22) - 34)))
    calm = np.maximum(calm, apron * (X > P.FACADE_X))
    calm = np.maximum(calm, smoothstep(14, 4, np.hypot(X + 0.5, Z + 0.5)))                     # the Spine
    rock_amp = 7 * (1 - calm)
    drift = 0.45 * (1 - 0.85 * calm)
    frock, fsnow = snowfield(X, Z, P.FIELD - FIELD_SNOW, rock_amp, -0.14, drift, seed=11)
    fsnow = fsnow - (ndimage.gaussian_filter(fsnow, 30) - P.FIELD)                              # level on average
    fsnow = np.where(calm > 0.6, P.FIELD + np.clip(fsnow - P.FIELD, -0.4, 0.4), fsnow)
    # the shelf, the Teeth, the cut
    shelf = inside(X, Z, P.SHELF_POLY)
    fsnow = np.where(shelf, P.SHELF + np.clip(fsnow - P.FIELD, -0.6, 0.6), fsnow)
    frock = np.where(shelf, np.minimum(frock + (P.SHELF - P.FIELD), P.SHELF - 1), frock)
    x0, z0, x1, z1 = P.SHELF_RAMP
    ramp = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1)
    step = P.FIELD + 1 + ((x1 - X) // 3) * 1.0
    fsnow = np.where(ramp, np.minimum(step, P.SHELF), fsnow)
    teeth = np.zeros(X.shape, bool)
    for poly, rise in zip(P.TEETH, (12, 8)):
        m = inside(X, Z, poly)
        p = shatter(X, Z, 5, seed=31, warp=(2, 1, 40, 10))
        r = np.random.default_rng(32)
        facet = r.uniform(0.5, 1.0, len(p.centres))[p.id] * rise - 2 * smoothstep(0.7, 0, p.edge)
        frock = np.where(m, np.maximum(frock, P.FIELD + facet), frock)
        teeth |= m
    for p in P.PATHS:                                             # the paths: level mud, the snow cleared off
        d, _ = polyline(X, Z, p)
        on = d < P.PATH_WIDTH / 2 + 1.5
        fsnow = np.where(on, P.FIELD, fsnow)
        frock = np.where(on, np.minimum(frock, P.FIELD - 1), frock)
    cut, _ = polyline(X, Z, P.CUT_LINE)
    fsnow = np.where(cut <= 1.5, P.CUT, fsnow)
    frock = np.where(cut <= 1.5, P.CUT - 1, frock)

    # the mountain: a plateau over the bunker, a step up behind the tier, the snowfield pushed further on it
    tier, _ = _behind(X, Z, TIER)
    plateau = 78 + 5 * noise.fbm(X.shape, 60, 3, seed=41) + 16 * smoothstep(-1, 3, tier)
    base = P.FIELD + (plateau - P.FIELD) * smoothstep(0, 9, dfront) + 3 * noise.ridged(X.shape, 9, 2, seed=42) \
        * smoothstep(2, 0, np.abs(dfront - 4))
    mrock, msnow = snowfield(X, Z, base - 3.5, 13 * smoothstep(4, 14, dfront), 0.06, 1.3, seed=51, spacing=13)
    for (nx, nz), rise in NEEDLES:                                # a needle's foot: the ground heaped round it
        mrock = mrock + rise * 0.18 * smoothstep(14, 0, np.hypot(X - nx, Z - nz))
    msnow = np.minimum(msnow, mrock + 3.5)                       # snow lies on the rock, it does not hang off it
    cracks = _cracks_on(X, Z, mountain & (dfront > 16), 61, 14)
    msnow = msnow - cracks
    mrock = np.where(cracks > 0, np.minimum(mrock, np.maximum(msnow - 1, 68)), mrock)

    rock = np.where(mountain, mrock, frock)
    snow = np.where(mountain, msnow, fsnow)
    # behind every crest the ground stays a block under it for three blocks, then rises
    for line, tops, foot, feet in crests():
        d, share = _behind(X, Z, line, face_right=True)
        top = np.interp(share, np.linspace(0, 1, len(tops)), tops)
        cap = top - 1 + 2.5 * np.maximum(0, d - 3)
        along = (share > 0.001) & (share < 0.999)                   # beside the wall, not past its ends
        near = (d > 0) & (d < 40) & along
        if foot is not None:
            fd, _ = _behind(X, Z, foot, face_right=True)
            zone = (fd > -3) & (d <= 0) & along
            low = np.interp(share, np.linspace(0, 1, len(feet)), feet)
            rock = np.where(zone, np.minimum(rock, low - 1), rock)
            snow = np.where(zone, np.minimum(snow, low), snow)
            near &= fd > 0
        rock = np.where(near, np.minimum(rock, cap), rock)
        snow = np.where(near, np.minimum(snow, cap), snow)
    yx0, yx1, yz0, yz1 = P.YARD
    yard = (X >= yx0) & (X <= yx1 + 1) & (Z >= yz0) & (Z <= yz1)
    dyard = np.hypot(np.maximum(0, np.maximum(yx0 - X, X - yx1)), np.maximum(0, np.maximum(yz0 - Z, Z - yz1)))
    wall_top = P.FIELD + 16
    yard_cap = wall_top - 1 + 2.5 * np.maximum(0, dyard - 5)
    rock = np.where((dyard > 0) & (dyard < 40) & mountain, np.minimum(rock, yard_cap), rock)
    snow = np.where((dyard > 0) & (dyard < 40) & mountain, np.minimum(snow, yard_cap), snow)
    rock = np.where(yard, P.FIELD - 1, rock)
    snow = np.where(yard, P.FIELD, snow)
    return rock, snow, teeth


def lay(w, rock, snow, teeth, X, Z, half):
    """Red's half into the world: stone to the rock's top, its skin by slope (the cliffs in strata), snow over it,
    mud on the paths, and the crevasses cut down to their lava."""
    sy = w.sy
    ys = np.arange(sy)[None, :, None]
    rk = np.clip(np.round(rock), 1, sy - 3).astype(int)
    sn = np.clip(np.round(snow), 1, sy - 3).astype(int)
    top = np.maximum(rk, sn)
    deg = slope_deg(top.astype(float))
    tone = np.where(deg < 30, 0, np.where(deg < 55, 1, 2))
    pick = (noise.fbm(X.shape, 4, 2, seed=71) > 0).astype(int) + (noise.fbm(X.shape, 9, 1, seed=72) > 0.3)
    solid = (ys <= rk[:, None, :])
    ids = np.where(solid, B.STONE, 0).astype(np.uint16)
    dat = np.zeros(ids.shape, np.uint8)
    skin = solid & (ys > rk[:, None, :] - 3)
    table_id = np.array([[ROCK_SKIN[t][k][0] for k in range(3)] for t in range(3)], np.uint16)
    table_dat = np.array([[ROCK_SKIN[t][k][1] for k in range(3)] for t in range(3)], np.uint8)
    ids = np.where(skin, table_id[tone, pick][:, None, :], ids)
    dat = np.where(skin, table_dat[tone, pick][:, None, :], dat)
    cliff = (deg >= 55)[:, None, :] & solid & (ys > rk[:, None, :] - 8)
    band = ((ys + np.round(3 * noise.fbm(X.shape, 25, 2, seed=73))[:, None, :].astype(int)) // 2) % len(STRATA)
    strata_id = np.array([s[0] for s in STRATA], np.uint16)[band]
    strata_dat = np.array([s[1] for s in STRATA], np.uint8)[band]
    ids = np.where(cliff, strata_id, ids)
    dat = np.where(cliff, strata_dat, dat)
    lie = slope_deg(sn.astype(float)) < 50                       # snow does not lie on a cliff
    sn = np.where(lie, sn, np.minimum(sn, rk))
    snowed = (sn > rk)[:, None, :] & (ys > rk[:, None, :]) & (ys <= sn[:, None, :]) & ~teeth[:, None, :]
    ids = np.where(snowed, B.SNOW, ids)
    dat = np.where(snowed, 0, dat)
    # mud on the paths, ragged at the edges, on the field only
    mud = np.zeros(X.shape, bool)
    for p in P.PATHS:
        d, _ = polyline(X, Z, p)
        mud |= d < P.PATH_WIDTH / 2 + 1.6 * noise.fbm(X.shape, 6, 2, seed=74)
    mud &= np.abs(top - P.FIELD) <= 1
    mud &= ~teeth
    r = np.random.default_rng(75)
    weights = np.array([wt for _, wt in MUD], float)
    choice = r.choice(len(MUD), size=X.shape, p=weights / weights.sum())
    patch = noise.fbm(X.shape, 5, 2, seed=76) > 0.62                    # a few patches of snow left on the mud
    for k, (blk, _) in enumerate(MUD):
        m = (mud & (choice == k) & ~patch)[:, None, :] & (ys == top[:, None, :])
        ids = np.where(m, blk[0], ids)
        dat = np.where(m, blk[1], dat)
    # the crevasses: a V narrowing to the lava, packed ice in the top of their walls
    crev = np.zeros(X.shape)
    for k, samples in enumerate(P.cracks()):
        for x, z, h in samples:
            if k == 2 and math.dist((x, z), P.OPEN_BRIDGE) < 3:
                continue
            crev = np.maximum(crev, np.clip(1 - np.hypot(X - x, Z - z) / max(h, 0.6), 0, None))
    depth_share = (ys - P.LAVA) / np.maximum(1, top[:, None, :] - P.LAVA)
    open_ = (crev[:, None, :] > 0) & (crev[:, None, :] >= 0.55 * (1 - np.clip(depth_share, 0, 1))) \
        & (ys > P.LAVA - 3) & (ys <= top[:, None, :])
    near_crev = ndimage.maximum_filter(crev > 0, size=3)
    ice_wall = near_crev[:, None, :] & (ids != 0) & (ys > top[:, None, :] - 4) & (ys <= top[:, None, :]) & ~open_
    ids = np.where(ice_wall, B.PACKED_ICE, ids)
    dat = np.where(ice_wall, 0, dat)
    lava = open_ & (ys <= P.LAVA)
    ids = np.where(open_, np.where(lava, B.LAVA, 0), ids)
    dat = np.where(open_, 0, dat)
    keep = half[:, None, :]
    w.ids[...] = np.where(keep, ids, w.ids)
    w.dat[...] = np.where(keep, dat, w.dat)
    return top
