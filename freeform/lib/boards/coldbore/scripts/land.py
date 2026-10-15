"""Coldbore's ground as heights, before any world: the snowfield, the cliff and the mountain each station is cut
into, the forecourt in front of each gate, the flank crevasses and the fissure between the two halves.

Every field is stated for red's half (z >= the fissure's line) and the board is that half and its half turn, so
blue's ground is red's turned about (-0.5, -0.5). Heights are the top block's y; a player's feet stand one over.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.geom import noise  # noqa: E402
from pgmvox.geom.noise import smoothstep  # noqa: E402
from pgmvox.geom.shapes import polyline  # noqa: E402

X0, X1, Z0, Z1 = -75, 74, -100, 99            # the board, inclusive; a half turn maps (x, z) to (-1 - x, -1 - z)
NX, NZ = X1 - X0 + 1, Z1 - Z0 + 1
GROUND = 71                                    # the snowfield's top block, feet at 72
LAVA = 22                                      # the fissure's lava surface
LAVA_FLOOR = 16
CLIFF_Z = 56                                   # the cliff's foot
BUTTRESS_Z = 44                                # the foot of the buttress the station's facade is the face of
TOP = 100                                      # the mountain's plateau, before its own relief
RIM_HALF = 12.0                                # the fissure's half width at the surface
BOTTOM_HALF = 4.5                              # its half width at the lava
PILLAR = 58                                    # the top of the bore's rock stump in the middle of the fissure
FORECOURT = dict(x0=-20, x1=19, z0=34, z1=56)  # red's forecourt, levelled at GROUND
OUTCROPS = [(-44, 40, 9), (31, 39, 7), (58, 24, 8)]   # where rock pokes through the snowfield: x, z, reach


def grid():
    return np.meshgrid(np.arange(X0, X1 + 1, dtype=float), np.arange(Z0, Z1 + 1, dtype=float), indexing="ij")


def odd(g):
    """A 1-D field along x made odd about -0.5: f(-1 - x) = -f(x)."""
    return (g - g[::-1]) / 2


def even(g):
    return (g + g[::-1]) / 2


def fissure_line():
    """The fissure's centre z and its half width at the surface, per column x: the centre wanders and its image is
    itself under the half turn, c(-1 - x) = -1 - c(x)."""
    xs = np.arange(X0, X1 + 1, dtype=float)
    g = 5.0 * noise.fbm((NX,), 40, 3, seed=11) + 2.5 * np.sin(xs / 17.0)
    centre = odd(g) - 0.5
    half = RIM_HALF + even(1.6 * noise.fbm((NX,), 25, 2, seed=12))
    return centre, half


def across(X, Z):
    """Signed distance across the fissure: positive on red's side."""
    c, _ = fissure_line()
    return Z - c[(X - X0).astype(int)]


def cliff_line():
    """The cliff's foot per column x: a buttress of the mountain pushed out over the station's front, so the facade
    is its face, and wandering elsewhere."""
    xs = np.arange(X0, X1 + 1, dtype=float)
    wander = 4.0 * noise.fbm((NX,), 30, 3, seed=21)
    bay = 1 - smoothstep(15, 27, np.abs(xs + 0.5))
    return CLIFF_Z - (CLIFF_Z - BUTTRESS_Z) * bay + wander * (1 - bay)


def red_half(X, Z):
    """Red's ground, stated over the whole grid; only z >= the fissure's line is kept."""
    s = across(X, Z)
    c, half = fissure_line()
    hw = half[(X - X0).astype(int)]
    # the snowfield: broad swells and drift ridges across a wind from the west
    H = GROUND + 1.6 * noise.fbm(X.shape, 60, 3, seed=1)
    Xw, Zw = noise.warp(X, Z, seed=2, big=8, small=2, big_cell=60, small_cell=14)
    H = H + 0.9 * np.sin(Xw / 7 + 0.3 * Zw / 7) * (0.5 + 0.5 * noise.fbm(X.shape, 40, 2, seed=3))
    # shoulders lifted beside the fissure, as the ground heaved when it opened
    H = H + 2.5 * np.exp(-((s - hw - 7) / 6) ** 2)
    # the frame: rock rising along the board's sides toward the cliff
    side = smoothstep(58, 72, np.abs(X + 0.5))
    H = H + side * (6 + 10 * smoothstep(20, 60, Z) + 4 * noise.ridged(X.shape, 18, 3, seed=5))
    # the mountain: a cliff from the foot to the plateau, stepped once and ragged
    foot = cliff_line()[(X - X0).astype(int)]
    rel = Z - foot
    jag = 1.8 * noise.fbm(X.shape, 5, 2, seed=6)
    top = TOP + 4 * noise.fbm(X.shape, 30, 3, seed=7) + 3 * noise.ridged(X.shape, 14, 3, seed=8)
    rise = np.clip((rel + jag) / 3.5, 0, 1) * 0.55 + np.clip((rel + jag - 5) / 3.0, 0, 1) * 0.45
    H = np.where(rel > -2, np.maximum(H, H + (top - H) * rise), H)
    # the forecourt: levelled in front of the gate and eased into the snow round it
    f = FORECOURT
    dx = np.maximum(np.maximum(f["x0"] - X, X - f["x1"]), 0)
    dz = np.maximum(np.maximum(f["z0"] - Z, Z - f["z1"]), 0)
    d = np.hypot(dx, dz)
    H = np.where(rel <= 0, H + (GROUND - H) * (1 - smoothstep(0, 6, d)), H)
    # two crevasses on each flank, cracks in the snowfield clear of the roads
    for k, pts in enumerate([[(-71, 19), (-66, 24), (-60, 21), (-55, 26)],
                             [(42, 36), (50, 33), (56, 38), (64, 35)]]):
        dd, al = polyline(X, Z, pts)[:2]
        width = 1.4 + 1.2 * (0.5 + 0.5 * noise.fbm(X.shape, 9, 2, seed=30 + k))
        end = smoothstep(0, 6, al) * smoothstep(al.max(), al.max() - 6, al)
        H = np.where(dd < width * end, H - (9 + 5 * end) * smoothstep(width, 0.3 * width, dd), H)
    # outcrops: faceted rock poking through the snow in three clusters off the routes
    from pgmvox.geom.shapes import shatter
    cells = shatter(X, Z, 6, seed=50, jitter=0.8, warp=(4, 2, 40, 10))
    rng = np.random.default_rng(51)
    n = len(cells.centres)
    tilt_x, tilt_z = rng.uniform(-0.5, 0.5, n), rng.uniform(-0.5, 0.5, n)
    rise = rng.uniform(2, 7, n)
    cid, cen = cells.id, cells.centres
    plane = rise[cid] + tilt_x[cid] * (X - cen[cid, 0]) + tilt_z[cid] * (Z - cen[cid, 1])
    blob = np.zeros(X.shape)
    for cx, cz, r in OUTCROPS:
        blob = np.maximum(blob, 1 - np.hypot(X - cx, Z - cz) / r + 0.35 * noise.fbm(X.shape, 6, 2, seed=52))
    crag = np.clip(blob, 0, 1) ** 0.7
    H = H + np.clip(plane, 0, None) * crag * (cells.edge > 0.6)
    # the fissure: lips, walls ragged down to the lava in ledges, the floor under it
    jag = 1.4 * noise.fbm(X.shape, 4, 2, seed=9) + 2.4 * noise.fbm(X.shape, 11, 2, seed=14)
    t = np.clip((np.abs(s) - BOTTOM_HALF + jag) / (hw - BOTTOM_HALF), 0, 1)
    profile = LAVA_FLOOR + (GROUND - 2 - LAVA_FLOOR) * t ** 2.2 + 3 * (t > 0.2) * noise.fbm(X.shape, 6, 2, seed=10)
    ledge = 5 + 2 * noise.fbm(X.shape, 20, 1, seed=15)
    terraced = profile - 0.6 * np.mod(profile - LAVA_FLOOR, ledge) * (t > 0.15) * (t < 0.92)
    H = np.where(np.abs(s) < hw, np.minimum(H, terraced), H)
    # the bore's stump: a pillar of rock standing in the lava on the board's middle
    r = np.hypot(X + 0.5, Z + 0.5)
    H = np.where(r < 3.6 + 0.6 * noise.fbm(X.shape, 3, 1, seed=13), np.maximum(H, PILLAR), H)
    return H


def heights():
    """The whole board: red's half and its half turn."""
    X, Z = grid()
    H = red_half(X, Z)
    red = across(X, Z) >= 0
    return np.where(red, H, H[::-1, ::-1]), X, Z


def red_mask(X, Z):
    return across(X, Z) >= 0
