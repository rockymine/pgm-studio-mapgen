"""Emberfrost's ground: heights over the whole board, mirrored across the middle line (z -> -1 - z), so red's half (z < 0) is drawn
and blue's is its image. West is the ice lane, east the fire lane, the orchard between them; the Thaw gorge crosses the waist.

    the island      a rounded slab with a waist at the gorge, void bays bitten into the back-west and the east flank
    Hearth yard     the spawn's level yard at 66 under a ridge that closes the back
    the Glacier     a high ice mass in the north-west with the Rime terrace at 72 on its shoulder and the Mirror (a frozen lake) below
    the Caldera     a ring of rock at 77 round a level crater floor at 66 (the Forge), open in two gaps
    Amberford       rolling orchard land, Beacon Hill at 73 in its middle
    the Thaw        a gorge 21 deep across the waist: water in the west half, lava in the east, a stone bar where they meet
"""
import math

import numpy as np

from pgmvox.geom import noise
from pgmvox.geom.noise import smoothstep
from pgmvox.geom.shapes import ellipse_distance
from pgmvox.plan.raster import Symmetry
from sites import HOUSES

X0, Z0 = -72, -96
NX, NZ = 144, 192
SYM = Symmetry("mirror_z")
BASE = 64
RIM = 77
GORGE_FLOOR = 43
LIQUID = 46                       # the surface of the Thaw's water and its lava
LAKE_ICE = 62
PAD_SPAWN = (0, -81)
SPAWN_LEVEL = 66
RIME = (-35, -50)
RIME_LEVEL = 72
FORGE = (40, -60)
FORGE_LEVEL = 66
BEACON = (4, -37)
BEACON_LEVEL = 73
RAMPS = (-22, 23)
LAKE = (-46, -28, 12, 9)         # x, z, rx, rz


def grid():
    return np.meshgrid(np.arange(X0, X0 + NX), np.arange(Z0, Z0 + NZ), indexing="ij")


def sn(shape, cell, octaves, seed):
    """Noise carried to both halves by the mirror."""
    return SYM.field(noise.fbm(shape, cell, octaves, seed=seed))


def land_mask(X, Z):
    xs, zs = X + 0.5, Z + 0.5
    az = np.abs(zs)
    n = sn(X.shape, 17, 3, 91)
    hw = 66 - 11 * np.exp(-(az / 20.0) ** 2) + 5.0 * n
    ez = 95.5 + 3.0 * sn(X.shape, 11, 2, 92)
    inside = (np.abs(xs) / hw) ** 4 + (az / ez) ** 5 < 1
    # void bays bitten into the flanks and the back corners: (x, z, rx, rz), red's, each carried to blue by the mirror
    for (cx, cz, r, rz) in ((-64, -84, 17, 15), (63, -90, 15, 12), (68, -40, 13, 16), (-73, -17, 10, 12), (-35, -96, 9, 7), (30, -97, 8, 6)):
        for sz in (cz, -1 - cz):
            d = ellipse_distance(xs, zs, (cx, sz + 0.5), r, rz) * (1 + 0.22 * sn(X.shape, 6, 2, 93))
            inside &= d > 1
    return inside


def lake_distance(X, Z):
    """How far out from the Mirror's centre every column lies, in radii, 1 on its ragged shore."""
    cx, cz, rx, rz = LAKE
    return ellipse_distance(X + 0.5, Z + 0.5, (cx, cz), rx, rz) * (1 + 0.18 * sn(X.shape, 7, 2, 21))


SPIRES = [(-63, -62, 5.5, 101), (-45, -90, 5, 106), (-21, -92, 4.5, 98), (-67, -34, 4.5, 90), (-56, -46, 3.5, 86)]


def gap_weight(angle, centres, width):
    w = np.zeros_like(angle)
    for c in centres:
        d = np.angle(np.exp(1j * (angle - c)))
        w = np.maximum(w, np.exp(-(d / width) ** 2))
    return w


def level(H, d, inner, outer, target):
    t = 1 - smoothstep(inner, outer, d)
    return H * (1 - t) + target * t


def ground():
    X, Z = grid()
    xs, zs = X + 0.5, Z + 0.5
    land = land_mask(X, Z)
    n_big = sn(X.shape, 34, 3, 3)
    n_mid = sn(X.shape, 14, 2, 4)
    n_small = sn(X.shape, 6, 2, 5)
    H = BASE + 2.2 * n_big + 0.9 * n_mid + 0.35 * n_small

    # the ridge that closes the back, and the yard it shelters
    back = 14 * smoothstep(-76, -93, zs) * (0.8 + 0.45 * sn(X.shape, 17, 2, 6))
    H = H + back
    H = level(H, np.hypot(xs - PAD_SPAWN[0], (zs - PAD_SPAWN[1]) * 1.15), 13, 23, SPAWN_LEVEL)

    # the Glacier: a high ice mass, craggy, with two spurs running toward the gorge
    def gauss(cx, cz, rx, rz, rise, p=2):
        return rise * np.exp(-((((xs - cx) / rx) ** 2 + ((zs - cz) / rz) ** 2) ** (p / 2)))
    glacier = gauss(-52, -76, 25, 24, 27) + gauss(-24, -90, 13, 11, 12) + gauss(-62, -48, 10, 13, 12)
    crag = noise.ridged(X.shape, 12, 3, seed=11)
    weight = np.clip(glacier / 24.0, 0, 1)
    H = H + glacier + 9 * weight * (crag - 0.45)
    for k, (sx_, sz_, sr, st) in enumerate(SPIRES):
        base = BASE + 12
        d = np.hypot(xs - sx_, zs - sz_) * (1 + 0.22 * sn(X.shape, 4, 2, 50 + k))
        H = np.maximum(H, np.where(d < sr, base + (st - base) * np.clip(1 - d / sr, 0, 1) ** 0.7, 0))
    # the Rime terrace the keep stands on, and the way up to it
    H = level(H, np.hypot(xs - RIME[0], (zs - RIME[1]) * 1.0) + 1.2 * n_small, 9.5, 17, RIME_LEVEL)

    # the Mirror: a frozen lake sunk in the glacier's foot
    d_lake = lake_distance(X, Z)
    H = np.where(d_lake < 1.0, np.minimum(H, 59.0 + 5.5 * smoothstep(0.55, 1.0, d_lake)), H)

    # the Caldera: a ring of rock round a level floor, open in two gaps
    dx, dz = xs - FORGE[0], zs - FORGE[1]
    dist = np.hypot(dx, dz) * (1 + 0.05 * sn(X.shape, 9, 2, 31))
    ang = np.arctan2(dz, dx)
    gaps = gap_weight(ang, (np.pi, np.pi * 0.5 + 0.12), 0.34)
    rim = (RIM - BASE) * np.exp(-(((dist - 24.5) / 5.6) ** 2)) * (1 - 0.93 * gaps) * (0.85 + 0.3 * sn(X.shape, 8, 2, 32))
    H = H + rim
    H = np.where(dist < 19, FORGE_LEVEL - 2.4 * smoothstep(8, 17, dist) + 0.5 * n_small, H)
    H = np.where((dist >= 19) & (dist < 24.5) & (rim > 3), np.maximum(H, FORGE_LEVEL), H)
    # ash hills east of the caldera, stepped
    H = H + gauss(63, -15, 11, 9, 9) + gauss(58, -90, 12, 12, 8)

    # Amberford: Beacon Hill with its flat crown
    H = H + gauss(BEACON[0], BEACON[1], 10, 8, 8) + gauss(-9, -62, 8, 6, 3) + gauss(14, -22, 8, 6, 3)
    H = level(H, np.hypot(xs - BEACON[0], zs - BEACON[1]), 3.6, 7.5, BEACON_LEVEL)

    # the Thaw: a gorge with a river bed, banks a block above it and walls
    H_pre = H.copy()
    az = np.abs(zs)
    sill = smoothstep(47, 55, np.abs(xs))
    wall = smoothstep(5.0, 13.0, az + 1.8 * n_mid + 0.8 * n_small)
    # the walls step in ledges, a shelf and a riser, so the gorge reads as laid rock and not a ramp
    stepped = wall * 6
    wall = np.clip((np.floor(stepped) + smoothstep(0.35, 0.9, stepped - np.floor(stepped))) / 6 + 0.04 * sn(X.shape, 5, 2, 43), 0, 1)
    H_floor = np.where(az < 3.4, GORGE_FLOOR + 0.0 * az, GORGE_FLOOR + 4.0 * smoothstep(3.0, 4.2, az))
    cut = (1 - sill)
    gorge_h = H_floor * (1 - wall) + H * wall
    # two scree ways, a slope a block to the block, let down each wall so the river's banks can be reached from the rims
    wall_ramp = smoothstep(4.0, 22.0, az + 0.8 * n_small)
    for rx in RAMPS:
        near = np.exp(-(((xs - rx) / 4.2) ** 4))
        ramp_h = H_floor * (1 - wall_ramp) + H_pre * wall_ramp
        gorge_h = gorge_h * (1 - near) + ramp_h * near
    H = H * (1 - cut) + gorge_h * cut
    # the bar of stone where the water and the lava meet
    bar = np.abs(xs) < 3.5
    H = np.where(bar & (az < 5.0) & (sill < 0.5), GORGE_FLOOR + 5, H)

    # a pad under every house: made ground, levelled to the median of what was there, eased back out
    for (_key, hx, hz, heading, hl, hw_, *_rest) in HOUSES:
        r_in = math.hypot(hl, hw_) / 2 + 1.0
        e = np.hypot(xs - hx, zs - hz)
        target = float(np.median(H[e < r_in]))
        H = level(H, e, r_in, r_in + 4.5, round(target))

    # red's half is drawn; blue's is its image
    red = Z < 0
    H = SYM.field(H, keep=red)
    land = SYM.field(land.astype(float), keep=red) > 0.5
    H = np.where(land, np.round(H), 0).astype(int)
    # the scree ways climb a block at a time, so a player walks them
    for rx in RAMPS:
        for i in np.nonzero(np.abs(X[:, 0] + 0.5 - rx) <= 3.5)[0]:
            for k in range(np.nonzero(Z[0] == -6)[0][0], np.nonzero(Z[0] == -40)[0][0], -1):
                if land[i, k - 1]:
                    H[i, k - 1] = min(H[i, k - 1], H[i, k] + 1)
    H = SYM.field(H, keep=red).astype(int)
    return X, Z, H, land


if __name__ == "__main__":
    X, Z, H, land = ground()
    print(H.shape, int(land.sum()), H[land].min(), H[land].max())


def zones(X, Z):
    """How far west (ice) and east (fire) every column lies, 0 to 1, along a ragged line; the orchard is what neither holds."""
    xs = X + 0.5
    wob = 8.0 * sn(X.shape, 26, 3, 41) + 3.0 * sn(X.shape, 9, 2, 42)
    ice = smoothstep(-6, -30, xs + wob)
    fire = smoothstep(9, 31, xs + wob)
    return ice, fire
