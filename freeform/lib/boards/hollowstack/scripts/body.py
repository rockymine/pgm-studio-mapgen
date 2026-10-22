"""Hollowstack's rock: blue's wall from the chasm's face to the back, its ground, its strata, and the two caverns cut
into it, the Underwood and the Deep, with the wells between them.

    rock(w)          the wall: a face that wanders in and out with height, ragged sides, the Tops' ground, strata
    underwood(w)     the cavern forest's hollow: terraces, the pond's basin, the gatehouse court, the domed roof
    deep(w)          the lava hall, the pool under the Root Well, the mushroom grotto, and the ways between them
    wells(w)         the light well from the Tops to the pond, the Root Well from the spur to the pool

Every function returns the floor and roof it cut, as grids over the world's columns (-1 where it cut nothing), so
what stands on a floor knows its ceiling.
"""
import math

import numpy as np

import layout as L
from pgmvox import B
from pgmvox.geom import noise as N
from pgmvox.volume import under as U


def smoothstep(a, b, v):
    t = np.clip((np.asarray(v, float) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def grid(w):
    X, Z = w.grid()
    return X, Z


def surface(w):
    """The Tops: rolling ground at the brink rising toward the back, the keep's hill levelled at KEEP_Y."""
    X, Z = grid(w)
    roll = 2.6 * N.fbm(X.shape, 16, 3, seed=13) + 1.2 * N.fbm(X.shape, 6, 2, seed=14)
    S = L.TOPS + roll + 5.0 * smoothstep(48, 74, X) - 1.5 * smoothstep(22, 13, X)
    kx0, kz0, kx1, kz1 = L.KEEP
    dx = np.maximum(np.maximum(kx0 - X, X - kx1), 0)
    dz = np.maximum(np.maximum(kz0 - Z, Z - kz1), 0)
    keep = 1 - smoothstep(0, 6, np.hypot(dx, dz))
    return np.round(S * (1 - keep) + L.KEEP_Y * keep).astype(int)


def rock(w):
    """Blue's wall, solid stone with its strata, grass and dirt on the Tops; the chasm and the sides left void."""
    X, Z = grid(w)
    S = surface(w)
    fyz = N.fbm((L.SY, w.sz), 9, 3, seed=11) + 1.3 * N.fbm((L.SY, w.sz), 22, 2, seed=19)
    face = L.FACE + np.clip(np.round(2.6 + 3.4 * fyz), 0, 8)       # (y, z): in and out with height and depth
    fxy = N.fbm((w.sx, L.SY), 8, 2, seed=12)
    gxy = N.fbm((w.sx, L.SY), 8, 2, seed=15)
    zlo = -L.SIDE + np.clip(np.round(1.2 + 2.4 * fxy), 0, 4)       # (x, y)
    zhi = L.SIDE - 1 - np.clip(np.round(1.2 + 2.4 * gxy), 0, 4)
    x3 = X[:, None, :]
    z3 = Z[:, None, :]
    y3 = np.arange(L.SY)[None, :, None]
    solid = (x3 >= 0) & (x3 <= L.BACK) & (y3 <= S[:, None, :]) & (x3 >= face[None, :, :]) \
        & (z3 >= zlo[:, :, None]) & (z3 <= zhi[:, :, None])
    ids, dat = w.ids, w.dat
    ids[solid] = B.STONE
    dat[solid] = 0
    band = N.fbm((w.sx, L.SY), 14, 2, seed=16)                     # andesite beds, tilted by the noise
    beds = (np.sin((np.arange(L.SY)[None, :] + 5 * band) / 2.6) > 0.72)[:, :, None] & solid
    ids[beds], dat[beds] = B.STONE, 5
    for lo, hi, d, seed in ((0, 32, 1, 17), (32, 72, 3, 20)):     # granite low, diorite in the middle, in lumps
        pxz = N.fbm((w.sx, w.sz), 6, 2, seed=seed)
        pxy = N.fbm((w.sx, L.SY), 6, 2, seed=seed + 100)
        m = solid & (pxz[:, None, :] + pxy[:, :, None] > 1.05) & (y3 >= lo) & (y3 < hi)
        ids[m], dat[m] = B.STONE, d
    rng = np.random.default_rng(18)
    r = rng.random(ids.shape)
    stone = solid & (ids == B.STONE)
    ids[stone & (r < 0.006)] = B.COAL_ORE
    ids[stone & (r > 0.9975) & (y3 < 60)] = B.IRON_ORE
    ids[stone & (r > 0.9995) & (y3 < 30)] = B.GOLD_ORE
    dat[(ids == B.COAL_ORE) | (ids == B.IRON_ORE) | (ids == B.GOLD_ORE)] = 0
    for i, k in np.argwhere((X >= 0) & (X <= L.BACK)):            # the Tops: grass over three of dirt
        col = ids[i, :, k]
        top = int(np.max(np.nonzero(col)[0])) if col.any() else -1
        if top < 60:
            continue
        ids[i, top, k], dat[i, top, k] = B.GRASS, 0
        for y in range(top - 3, top):
            if ids[i, y, k] != 0:
                ids[i, y, k], dat[i, y, k] = B.DIRT, 0
    ids[:, 0, :] = np.where(ids[:, 0, :] != 0, B.BEDROCK, 0)
    return S


def underwood(w):
    """The Underwood's hollow: each column of its plan ellipse cut from its floor to a domed roof, the floor laid in
    terraces (the mouth, the middle with the pond's basin and the gatehouse's court, the back and its high
    shelves) and finished with grass over dirt; the shrine's spur stands two blocks over the mouth."""
    X, Z = grid(w)
    u, f = L.UNDERWOOD, L.UNDERWOOD_FLOORS
    r = np.hypot((X - u["cx"]) / u["rx"], (Z - u["cz"]) / u["rz"])
    inside = (r < 1) & (X >= L.FACE - 2)
    n = N.fbm(X.shape, 6, 2, seed=21)
    floor = np.interp(X, [0, 22, 28, 52, 58, 99], [f["mouth"], f["mouth"], f["mid"], f["mid"], f["back"], f["back"]])
    floor = floor + 0.6 * n
    high = (X > 56) & (r > 0.72)
    floor = np.where(high, f["high"], floor)
    pond = np.hypot((X - 37) / 8.0, (Z + 9) / 5.5)
    floor = np.where(pond < 1, f["pond"] + 2 * smoothstep(0.65, 1.0, pond), floor)
    gx, gz = L.cell_box(L.UNDERCROFT, *L.GATEHOUSE)[0] + 2, L.cell_box(L.UNDERCROFT, *L.GATEHOUSE)[2] + 2
    court = np.hypot(X - gx, Z - gz)
    floor = np.where(court < 7, np.minimum(floor, f["court"] + np.clip(court - 4.5, 0, 2)), floor)
    s = L.SHRINE
    spur = (X >= s["x0"]) & (X <= s["x1"]) & (Z >= s["z0"]) & (Z <= s["z1"])
    floor = np.where(spur, s["floor"], floor)
    floor = np.where(r > 0.86, floor + (r - 0.86) * 28, floor)    # the floor banks up into the walls
    roof = u["roof"] + u["dome"] * np.sqrt(np.clip(1 - r * r, 0, 1)) + 1.5 * N.fbm(X.shape, 7, 2, seed=22)
    mz = 13 + 1.5 * N.fbm(X.shape, 5, 2, seed=23)                 # the mouth: an arch the cavern's whole front wide
    mouth = (X < 26) & (np.abs(Z) < mz) & (X >= L.FACE - 2)
    arch = f["mouth"] + 13 * np.sqrt(np.clip(1 - (Z / mz) ** 2, 0, 1)) + N.fbm(X.shape, 4, 2, seed=24)
    floor = np.where(mouth & ~spur, np.minimum(floor, f["mouth"] + np.clip((np.abs(Z) - mz + 3) * 1.5, 0, 6)), floor)
    roof = np.where(mouth, np.maximum(roof, arch), roof)
    inside = inside | mouth
    px, pz, _ = L.PLUNGE                                          # the plunge pool on the back terrace: its water a
    plunge = np.hypot(X - px, Z - pz) / 3.6                       # block under the lowest of its banks, three deep
    ring = (plunge >= 1) & (plunge < 1.5)
    top = int(np.floor(floor[ring].min())) - 1
    floor = np.where(plunge < 1, top - 3, floor)
    floor, roof = np.round(floor).astype(int), np.round(roof).astype(int)
    cut = inside & (roof > floor + 2)
    ids, dat = w.ids, w.dat
    for i, k in np.argwhere(spur):                                 # the spur stands out into the chasm on rock
        x = int(X[i, k])
        base = s["floor"] - 3 - 2 * max(0, 17 - x) - int(2 * abs(n[i, k]))
        ids[i, max(base, 1):s["floor"] + 1, k] = np.where(ids[i, max(base, 1):s["floor"] + 1, k] == 0, B.STONE,
                                                         ids[i, max(base, 1):s["floor"] + 1, k])
        cut[i, k] = True
    for i, k in np.argwhere(cut):
        fy, ry = floor[i, k], roof[i, k]
        ids[i, fy + 1:ry + 1, k] = 0
        dat[i, fy + 1:ry + 1, k] = 0
        if ids[i, fy, k] != 0:
            ids[i, fy, k], dat[i, fy, k] = (B.GRASS, 0) if not spur[i, k] else (B.STONE, 0)
            for y in range(fy - 2, fy):
                if ids[i, y, k] == B.STONE:
                    ids[i, y, k], dat[i, y, k] = B.DIRT, 0
    water = cut & (pond < 1) & (floor < f["water"]) & (plunge >= 1)
    for i, k in np.argwhere(cut & (plunge < 1)):                  # three deep under the drop
        fy = floor[i, k]
        ids[i, fy, k], dat[i, fy, k] = B.CLAY, 0
        ids[i, fy + 1:top + 1, k] = B.WATER
    for i, k in np.argwhere(water):
        fy = floor[i, k]
        ids[i, fy, k], dat[i, fy, k] = (B.SAND, 0) if (i + k) % 3 else (B.CLAY, 0)
        ids[i, fy + 1:f["water"] + 1, k] = B.WATER
    out_floor = np.where(cut, floor, -1)
    out_roof = np.where(cut, roof, -1)
    return out_floor, out_roof


def _hall(w, cx, cz, rx, rz, floor, roof, dome, seed, shape=None):
    X, Z = grid(w)
    r = np.hypot((X - cx) / rx, (Z - cz) / rz)
    if shape is not None:
        r = r + 0.12 * N.fbm(X.shape, 5, 2, seed=seed)
    top = np.round(roof + dome * np.sqrt(np.clip(1 - r * r, 0, 1)) + N.fbm(X.shape, 5, 2, seed=seed + 1)).astype(int)
    fl = np.round(floor + np.where(r > 0.8, (r - 0.8) * 20, 0)).astype(int)
    cut = (r < 1) & (top > fl + 2)
    for i, k in np.argwhere(cut):
        w.ids[i, fl[i, k] + 1:top[i, k] + 1, k] = 0
        w.dat[i, fl[i, k] + 1:top[i, k] + 1, k] = 0
    return cut, fl, top, r


def deep(w):
    """The Deep: the lava hall with its lake held in obsidian, the pool under the Root Well opening off it, the
    mushroom grotto on mycelium; a winding way from the hall up to the grotto, and a mouth from the hall out onto
    the chasm."""
    d = L.DEEP
    ids, dat = w.ids, w.dat
    hall, hf, ht, hr = _hall(w, 42, -4, 21, 13, d["floor"], d["floor"] + 4, 9, 31, shape=True)
    for i, k in np.argwhere(hall):
        f = hf[i, k]
        if hr[i, k] < 0.5:
            ids[i, f - 2:f, k] = B.LAVA                          # the lake one under the floor, lava two deep
            ids[i, f, k] = 0
            ids[i, f - 3, k] = B.STONE
        elif hr[i, k] < 0.58:
            ids[i, f, k], dat[i, f, k] = B.OBSIDIAN, 0
        else:
            ids[i, f, k], dat[i, f, k] = (B.GRAVEL, 0) if (i * 7 + k) % 5 == 0 else (B.STONE, 5)
    pool, pf, pt, pr = _hall(w, L.ROOT_WELL[0] + 1, L.ROOT_WELL[1], 8, 7, d["pool"] + 3, d["pool"] + 7, 5, 33)
    for i, k in np.argwhere(pool):                               # banks a block over the water, the basin in them
        f = pf[i, k]
        if pr[i, k] < 0.68:
            ids[i, d["pool"] - 1, k] = B.CLAY
            ids[i, d["pool"]:d["pool"] + 3, k] = B.WATER           # three deep under the well
            ids[i, d["pool"] + 3, k] = 0
    grotto, gf, gt, gr = _hall(w, 75, 9, 15, 10, 21, 25, 6, 35, shape=True)
    for i, k in np.argwhere(grotto):
        ids[i, gf[i, k], k], dat[i, gf[i, k], k] = B.MYCELIUM, 0
    pts = U.wander([(57, d["floor"], -6), (64, d["floor"] + 3, -9), (72, d["floor"] + 6, -4), (75, 21, 2)],
                   (2.2, 3.0), seed=36)
    U.tunnel(w, pts)
    pts = U.wander([(30, d["floor"] + 1, 2), (26, d["pool"] + 4, 6)], (2.2, 2.8), seed=37)    # the hall into the pool
    U.tunnel(w, pts)
    mouth = U.wander([(30, d["floor"] + 1, -9), (22, d["floor"] + 1, -11), (16, d["floor"] + 1, -12),
                      (8, d["floor"] + 1, -13)], (2.4, 3.2), seed=38,
                     mouth=4.0)
    U.tunnel(w, mouth)
    return {"hall": (hall, hf, ht), "pool": (pool, pf, pt), "grotto": (grotto, gf, gt)}


def wells(w, S, wood_roof):
    """The light well from the Tops down to the Underwood's roof over the pond, and the Root Well from the spur's
    side down to the pool: round holes with a ring of mossy stone at the top."""
    lx, lz, lr = L.LIGHT_WELL
    X, Z = grid(w)
    i, k = lx - w.x0, lz - w.z0
    top = int(S[i, k]) + 1
    U.bore(w, (lx, lz), lr, int(wood_roof[i, k]) - 1, top + 2, seed=41, r_noise=0.25)
    for x in range(lx - 4, lx + 5):
        for z in range(lz - 4, lz + 5):
            d = math.hypot(x - lx, z - lz)
            if lr < d < lr + 1.6:
                y = int(S[x - w.x0, z - w.z0])
                if w.id(x, y, z) in (B.GRASS, B.DIRT):
                    w.set(x, y, z, B.MOSSY)
    px, pz, pr = L.PLUNGE
    i, k = px - w.x0, pz - w.z0
    top = int(S[i, k]) + 1
    U.bore(w, (px, pz), pr, int(wood_roof[i, k]) - 1, top + 2, seed=43, r_noise=0.15)
    rx, rz, rr = L.ROOT_WELL
    U.bore(w, (rx, rz), rr, L.DEEP["pool"] + 3, L.UNDERWOOD_FLOORS["mouth"], seed=42, r_noise=0.2)
    for x in range(rx - 4, rx + 5):
        for z in range(rz - 4, rz + 5):
            d = math.hypot(x - rx, z - rz)
            if rr < d < rr + 1.4:
                y = L.UNDERWOOD_FLOORS["mouth"]
                if w.id(x, y, z) in (B.GRASS, B.DIRT, B.STONE):
                    w.set(x, y, z, B.MOSSY)
