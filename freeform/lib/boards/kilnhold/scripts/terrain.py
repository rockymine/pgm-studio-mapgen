"""Kilnhold's ground: the heights of the whole caldera (red's half computed, blue's its half turn), the land's
outline and underside, and how the top and the rock are laid.

    land()        heights, the outline, the underside, the surface sets and their masks; cached
    lay(w, L)     rock in beds, the ash field and the scoria and the slopes laid over it, the crater's lava
"""
from functools import lru_cache

import numpy as np

import plan as P
from pgmvox import B, rng
from pgmvox.geom.noise import fbm, smoothstep
from pgmvox.surface.terrain import slope_deg

NX, NZ = P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1
HALF = NZ // 2                                      # red's columns: z -100 .. -1


class Land:
    pass


def _half_grid():
    X, Z = np.meshgrid(np.arange(P.X_MIN, P.X_MAX + 1), np.arange(P.Z_MIN, 0), indexing="ij")
    return X.astype(float), Z.astype(float)


def _whole(red):
    """A red-half array turned into the whole board: blue's half is its half turn."""
    return np.concatenate([red, red[::-1, ::-1]], axis=1)


def _heights_red():
    X, Z = _half_grid()
    u, v = X + 0.5, Z + 0.5
    sh = X.shape
    L = Land()

    # ---- the outline: a rounded box, its edge wandering, held straight toward the middle seam
    hx, hz, rad = 65.5, 96.5, 16.0
    qx, qz = np.abs(u) - (hx - rad), np.abs(v) - (hz - rad)
    sdf = np.hypot(np.maximum(qx, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qx, qz), 0) - rad
    fade = smoothstep(-2, -30, v)
    wobble = 3.0 * fbm(sh, 14, 2, seed=101) * fade
    d_in = -(sdf + wobble)
    land = d_in > 0.5

    # ---- the caldera floor: ash hummocks, never more than a block and a half either way
    ground = P.FIELD + 1.1 * fbm(sh, 34, 3, seed=102) + 0.5 * fbm(sh, 9, 2, seed=103)

    # ---- the slag banks that divide the lanes: two a half, with a gap between for a way through
    bank_u = 28.0 + 2.2 * fbm(sh, 16, 2, seed=104)
    bank_x = np.abs(np.abs(u) - bank_u)
    span = smoothstep(-45, -38, v) * (1 - smoothstep(-15, -9, v))
    gap = 1 - 0.85 * np.exp(-((v + 27.0) / 3.4) ** 4)
    crest = 7.5 + 2.0 * fbm(sh, 7, 2, seed=105)
    bank = crest * np.exp(-(bank_x / 4.2) ** 2) * span * gap

    # ---- the crater: climbable walls one block a block, a shelf, a lake of lava
    r = np.hypot(u, v)
    crest_y, shelf_y = P.FIELD + 5.0, 59.0
    outer = np.where(r > P.CRATER_R, ground + (crest_y - ground) * (1 - smoothstep(P.CRATER_R, 34, r)), 0)
    wall = np.clip(shelf_y + (r - 12.0) * (crest_y - shelf_y) / (P.CRATER_R - 12.0), shelf_y, crest_y)
    crater = np.where(r <= P.CRATER_R, np.where(r <= 12.0, shelf_y, wall), outer)
    crater_mask = r < 34
    h = np.where(crater_mask, crater + 0.6 * fbm(sh, 6, 2, seed=106) * (r > 12), ground) + bank

    # ---- the massif: a cliff face across the north, a rock top that the roof deck is laid on
    face = P.CROWN - 2.4 * np.maximum(0.0, v + 54.0)
    face = face + 1.2 * fbm(sh, 8, 3, seed=107) * (v > -56)
    dx0, dx1, dz0, dz1 = P.DECK_BOX
    in_deck = (X >= dx0) & (X <= dx1) & (Z >= dz0) & (Z <= dz1)
    deck_edge = smoothstep(0, 6, np.minimum.reduce([X - dx0, dx1 - X, Z - dz0, dz1 - Z]) + 4)
    rough = float(P.CROWN) + 1.2 * fbm(sh, 10, 2, seed=108)
    massif = np.where(v < -54, rough * (1 - deck_edge) + float(P.CROWN) * deck_edge, face)
    massif = np.where(in_deck, float(P.CROWN), massif)
    h = np.where(massif > h, massif, h)
    # ---- the rim: the caldera's wall round the edge, higher to the north
    rim = (11.0 + 5.0 * smoothstep(-20, -60, v)) * (1 - smoothstep(0, 11, d_in))
    h = np.maximum(h, np.where((d_in > 0) & (d_in < 11), P.FIELD + rim, 0))

    # ---- the made ground: the apron, the quarry pit, the tower's court, each a level the relief meets
    ax0, ax1, az0, az1 = P.APRON_BOX
    in_apron = (X >= ax0) & (X <= ax1) & (Z >= az0) & (Z <= az1)
    h = np.where(in_apron, P.APRON, h)
    px0, px1, pz0, pz1 = P.PIT_BOX
    in_pit = (X >= px0) & (X <= px1) & (Z >= pz0) & (Z <= pz1)
    h = np.where(in_pit, P.PIT, h)
    tx, tz = P.TOWER
    rt = np.hypot(u - tx, v - tz)
    in_court = rt < P.TOWER_R_IN
    h = np.where(in_court, P.PIT, h)

    h = np.where(in_deck, float(P.CROWN), h)
    L.red = dict(h=h, in_deck=in_deck, land=land, d_in=d_in, in_apron=in_apron, in_pit=in_pit, in_court=in_court, r=r, bank=bank,
                 crater_mask=crater_mask)
    return L


@lru_cache(maxsize=1)
def land():
    L = _heights_red()
    red = L.red
    L.H = np.round(_whole(red["h"])).astype(int)
    L.land = _whole(red["land"])
    L.d_in = _whole(red["d_in"])
    L.apron = _whole(red["in_apron"])
    L.pit = _whole(red["in_pit"])
    L.court = _whole(red["in_court"])
    L.deck = _whole(red["in_deck"])
    L.r = _whole(red["r"])
    L.bank = _whole(red["bank"])
    L.H = np.where(L.land, L.H, 0)
    L.slope = slope_deg(L.H, L.land)
    return L


# ---- laying ----------------------------------------------------------------------------------------------------
ROCK_BEDS = [((B.STONE, 0), 3), ((B.STAINED_CLAY, 15), 1), ((B.STONE, 5), 2), ((B.STONE, 0), 2), ((B.COBBLE, 0), 1),
             ((B.STAINED_CLAY, 15), 2), ((B.STONE, 5), 3), ((B.STONE, 0), 3), ((B.COAL_ORE, 0), 1),
             ((B.STONE, 5), 1)]


def _bed_table():
    out = []
    for blk, n in ROCK_BEDS:
        out += [blk] * n
    return np.array(out, dtype=np.int32)


def lay(w, L):
    """Fill every land column from its underside to its top: beds of rock, then the ground's own top by place and
    slope. The made ground (apron, deck, courts) is dressed by the works, so it is laid here only as rock."""
    sh = L.H.shape
    X, Z = w.grid()
    H, land_, d_in = L.H, L.land, L.d_in
    tilt = 2.2 * fbm(sh, 30, 2, seed=111) + 0.06 * (X + 0.6 * Z)
    beds = _bed_table()
    bed_ids = np.array([b[0] for b in beds]); bed_dat = np.array([b[1] for b in beds])
    nb = len(beds)
    # the underside: a rock that narrows downward, the rim a cliff of about twenty blocks, never under y 26 and always
    # deep enough under the deep halls (floor 57) to hold them
    di = np.maximum(d_in, 0)
    root = 54 - 30 * (1 - np.exp(-di / 24.0)) + 4.0 * fbm(sh, 14, 3, seed=112) * (1 - np.exp(-di / 10.0))
    bottom = np.clip(np.minimum(H - 10, root), 26, None).astype(int)
    bottom = np.where(land_, bottom, 0)
    deg = L.slope
    n_ash = fbm(sh, 9, 2, seed=113)
    n_dirt = fbm(sh, 5, 2, seed=114)
    n_scoria = fbm(sh, 18, 2, seed=115)
    n_rock = fbm(sh, 4, 2, seed=116)
    r = L.r
    scoria = ((n_scoria > 0.5) & (r > 12)) | ((r > 12) & (r < 26) & (n_scoria > 0.05)) | ((L.bank > 2.0) & (n_scoria > 0.1))
    cells = (np.floor((X + 0.5) / 3).astype(int) * 7 + np.floor((Z + 0.5) / 3).astype(int) * 13) % 4
    for i, k in zip(*np.nonzero(land_)):
        top, b = int(H[i, k]), int(bottom[i, k])
        ys = np.arange(b, top + 1)
        idx = ((ys + tilt[i, k]) / 3.1).astype(int) % nb
        w.ids[i, b:top + 1, k] = bed_ids[idx]
        w.dat[i, b:top + 1, k] = bed_dat[idx]
        d = deg[i, k]
        if d >= 34:                                           # rock showing through where the ground is steep
            blk = [(B.STONE, 0), (B.STONE, 5), (B.COBBLE, 0), (B.STAINED_CLAY, 15), (B.STONE, 5), (B.STAINED_CLAY, 7),
                   (B.STONE, 0), (B.COAL_ORE, 0)][(int(cells[i, k]) + int(n_rock[i, k] * 6)) % 8]
            w.ids[i, top, k], w.dat[i, top, k] = blk
            continue
        if scoria[i, k] and d < 34:
            pick = [(B.RED_SANDSTONE, 0), (B.STAINED_CLAY, 1), (B.RED_SANDSTONE, 0), (B.SAND, 1)][int(cells[i, k]) % 4]
            w.ids[i, top, k], w.dat[i, top, k] = pick
            if top - 1 >= b:
                w.ids[i, top - 1, k], w.dat[i, top - 1, k] = B.RED_SANDSTONE, 0
            continue
        t = n_ash[i, k]
        if n_dirt[i, k] > 0.3 and t < -0.15:
            blk = (B.DIRT, 1)
        elif t > 0.18:
            blk = (B.STAINED_CLAY, 15)
        else:
            blk = (B.STAINED_CLAY, 7) if (cells[i, k] % 3) else (B.STAINED_CLAY, 15)
        w.ids[i, top, k], w.dat[i, top, k] = blk
        for dy in (1, 2):
            if top - dy >= b:
                w.ids[i, top - dy, k], w.dat[i, top - dy, k] = (B.STAINED_CLAY, 7) if dy == 1 else (B.GRAVEL, 0)
    return deg
