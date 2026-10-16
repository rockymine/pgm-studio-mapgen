"""Emberfrost's rock, soil and paint, laid over land.py's heights, then the Thaw's water and lava and the Mirror's ice.

The ground is three tone families: the ice lane (snow, packed ice, andesite), the fire lane (netherrack, brown and orange clay, red
sandstone) and the orchard between (grass, podzol, coarse dirt), each finished by its slope. Rock under them is in beds that follow
the ground: packed-ice veins in the west, banded clay in the east, stone between."""
import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.geom import noise
from pgmvox.geom.shapes import distance_in
from pgmvox.surface import terrain as T

ICE_ROCK = [((B.PACKED_ICE, 0), 2, 3), ((B.STONE, 5), 3, 4), ((B.STONE, 0), 3, 4), ((B.COBBLE, 0), 1, 2), ((B.SNOW, 0), 1, 2)]
FIRE_ROCK = [((B.STAINED_CLAY, 12), 3, 3), ((B.STAINED_CLAY, 1), 3, 2), ((B.HARDENED_CLAY, 0), 3, 2), ((B.RED_SANDSTONE, 0), 3, 3),
             ((B.STAINED_CLAY, 4), 1, 1), ((B.NETHERRACK, 0), 2, 2), ((B.STAINED_CLAY, 15), 1, 1)]
MID_ROCK = [((B.STONE, 0), 3, 4), ((B.STONE, 5), 3, 3), ((B.SANDSTONE, 0), 2, 3), ((B.STAINED_CLAY, 12), 2, 1.5), ((B.COBBLE, 0), 2, 2), ((B.STONE, 6), 1, 1), ((B.HARDENED_CLAY, 0), 1, 1), ((B.COAL_ORE, 0), 1, 0.2)]


def pick(u, table):
    """A block from [(block, share), ...] by one uniform draw."""
    total = sum(s for _, s in table)
    acc = 0.0
    for blk, s in table:
        acc += s / total
        if u <= acc:
            return blk
    return table[-1][0]


def lay_land(w, stats):
    H, LAND = P.H, P.LAND
    X, Z = P.X, P.Z
    ice, fire = land.zones(X, Z)
    sym = land.SYM
    deg = T.slope_deg(H, LAND)
    deg = T.ledge_angle(H, deg, LAND)
    depth = T.soil_depth(deg)
    patch = sym.field(noise.fbm(H.shape, 11, 3, seed=61))
    grain = sym.field(noise.fbm(H.shape, 4, 2, seed=62))
    rng = np.random.default_rng(63)
    u = rng.random(H.shape)

    def fill(strata_choices, seed):
        return T.beds(T.Strata(strata_choices, seed=seed, start=1),
                      T.bed_offset(H.shape, dip=(0.04, -0.03), fold=3, cell=17, seed=seed + 1, drape=(H, 0.35, 5)), seed=seed + 2)
    f_ice, f_fire, f_mid = fill(ICE_ROCK, 70), fill(FIRE_ROCK, 80), fill(MID_ROCK, 90)

    def bands(i, k, ys):
        xs_, zs_ = X[i, k] + 0.5, abs(Z[i, k] + 0.5)
        if zs_ < 15:                                    # the gorge's walls are the lane's rock either side of the bar
            return f_ice(i, k, ys) if xs_ < -5 else f_fire(i, k, ys) if xs_ > 5 else f_mid(i, k, ys)
        if ice[i, k] > 0.45:
            return f_ice(i, k, ys)
        if fire[i, k] > 0.45:
            return f_fire(i, k, ys)
        return f_mid(i, k, ys)

    patch2 = sym.field(noise.fbm(H.shape, 8, 2, seed=66))
    top = np.zeros(H.shape + (2,), int)
    under = np.zeros(H.shape + (2,), int)
    for i, k in np.argwhere(LAND):
        d, h, uu, pp, qq = deg[i, k], int(H[i, k]), u[i, k], patch[i, k], patch2[i, k]
        I, F = ice[i, k], fire[i, k]
        cliff = d > 46
        if I > 0.55:
            under[i, k] = (B.PACKED_ICE, 0)
            if cliff:
                blk = bands(i, k, [h])[0]
            elif pp > 0.33 or (pp > 0.24 and uu < 0.35):
                blk = (B.PACKED_ICE, 0)
            elif qq < -0.42 and uu < 0.85:
                blk = (B.STONE, 5)
            else:
                blk = (B.PACKED_ICE, 0) if uu < 0.03 else (B.SNOW, 0)
        elif F > 0.55:
            under[i, k] = (B.STAINED_CLAY, 12)
            if cliff:
                blk = bands(i, k, [h])[0]
            elif pp > 0.3 or (pp > 0.2 and uu < 0.4):
                blk = (B.STAINED_CLAY, 12)
            elif qq > 0.4:
                blk = (B.HARDENED_CLAY, 0)
            elif qq < -0.4:
                blk = (B.RED_SANDSTONE, 0)
            else:
                blk = (B.SOUL_SAND, 0) if uu < 0.03 else (B.NETHERRACK, 0)
        elif I > 0.12:
            under[i, k] = (B.DIRT, 0)
            blk = bands(i, k, [h])[0] if cliff else (B.DIRT, 2) if pp > 0.25 else (B.DIRT, 1) if qq > 0.42 else (B.GRASS, 0)
        elif F > 0.12:
            under[i, k] = (B.DIRT, 0)
            blk = bands(i, k, [h])[0] if cliff else (B.NETHERRACK, 0) if pp > 0.38 else (B.DIRT, 1) if qq > 0.15 else (B.DIRT, 2) if pp > 0.1 else (B.GRASS, 0)
        else:
            under[i, k] = (B.DIRT, 0)
            blk = bands(i, k, [h])[0] if cliff else (B.DIRT, 2) if pp > 0.22 else (B.DIRT, 1) if qq > 0.4 else (B.GRAVEL, 0) if uu < 0.012 else (B.GRASS, 0)
        top[i, k] = blk

    # the underside: a floating island's cone, each column's rock ending a thickness under it that grows with the way in
    d_out = distance_in(LAND, "euclid")
    rough = 7 * noise.fbm(H.shape, 9, 3, seed=64) + 5 * noise.ridged(H.shape, 14, 2, seed=65)
    bottom = np.maximum(H - (6 + 0.95 * d_out + rough), 9).round().astype(int)
    sx, sz = H.shape
    for i, k in np.argwhere(LAND):
        h = int(H[i, k])
        dd = int(depth[i, k])
        lo = int(bottom[i, k])
        ys = range(1, max(1, h - dd))
        for y, (bid, dat) in zip(ys, bands(i, k, ys)):
            w.ids[i, y, k], w.dat[i, y, k] = bid, dat
        w.ids[i, max(1, h - dd):h, k] = under[i, k][0]
        w.dat[i, max(1, h - dd):h, k] = under[i, k][1]
        w.ids[i, h, k], w.dat[i, h, k] = top[i, k]
        w.ids[i, :lo, k] = 0
        w.dat[i, :lo, k] = 0
    stats["steep>46"] = int((deg[LAND] > 46).sum())
    return deg, ice, fire, bottom


def thaw(w, ice, fire, stats):
    """The river in the gorge: gravel and clay bed, water in the west half, lava in the east, obsidian where they meet."""
    H, LAND, X, Z = P.H, P.LAND, P.X, P.Z
    xs, zs = X + 0.5, Z + 0.5
    az = np.abs(zs)
    low = LAND & (az < 9.5) & (H <= land.GORGE_FLOOR + 4)
    inland = distance_in(LAND, "euclid") > 2.5
    wet_w = low & (xs < -3.5) & (H < land.LIQUID) & inland
    wet_e = low & (xs > 3.5) & (H < land.LIQUID) & inland
    bar = LAND & (np.abs(xs) <= 3.5) & (az < 6.0) & (H <= land.GORGE_FLOOR + 6)
    rng = np.random.default_rng(66)
    for i, k in np.argwhere(wet_w):
        h = int(H[i, k])
        w.ids[i, h, k], w.dat[i, h, k] = [(B.STONE, 5), (B.CLAY, 0), (B.COBBLE, 0), (B.STONE, 6)][int(rng.integers(4))]
        w.ids[i, h + 1:land.LIQUID + 1, k] = B.WATER
        w.dat[i, h + 1:land.LIQUID + 1, k] = 0
    for i, k in np.argwhere(wet_e):
        h = int(H[i, k])
        w.ids[i, h, k], w.dat[i, h, k] = [(B.NETHERRACK, 0), (B.SOUL_SAND, 0), (B.STAINED_CLAY, 15), (B.OBSIDIAN, 0)][int(rng.integers(4))]
        w.ids[i, h + 1:land.LIQUID + 1, k] = B.LAVA
        w.dat[i, h + 1:land.LIQUID + 1, k] = 0
    for i, k in np.argwhere(bar):
        h = int(H[i, k])
        top = land.LIQUID + 2 if abs(xs[i, k]) < 2.5 else land.LIQUID + 1
        w.ids[i, h:top + 1, k] = B.OBSIDIAN
        w.dat[i, h:top + 1, k] = 0
    stats["water"] = int(wet_w.sum())
    stats["lava"] = int(wet_e.sum())
    return wet_w, wet_e, bar


def mirror_lake(w, stats):
    """Water in the Mirror's bowl up to y 61 and a skin of ice on it at 62."""
    H, LAND, X, Z = P.H, P.LAND, P.X, P.Z
    d = land.lake_distance(X, Z)
    lake = LAND & (d < 1.0) & (H < land.LAKE_ICE) & (distance_in(LAND, "euclid") > 3)
    for i, k in np.argwhere(lake):
        h = int(H[i, k])
        w.ids[i, h, k], w.dat[i, h, k] = (B.STONE, 5) if (i + k) % 3 else (B.PACKED_ICE, 0)
        w.ids[i, h + 1:land.LAKE_ICE, k] = B.WATER
        w.dat[i, h + 1:land.LAKE_ICE, k] = 0
        w.ids[i, land.LAKE_ICE, k] = B.ICE
        w.dat[i, land.LAKE_ICE, k] = 0
    stats["lake"] = int(lake.sum())
    return lake
