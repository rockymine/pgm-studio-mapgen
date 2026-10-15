"""Coldbore's ground as heights, before any world: the snowfield, the hill raised on its east flank, the cliff with
its two buttresses and its gullies, the mountain each station is cut into, the courts in front of the gate and
the generator house, the rock breaking through the snow, the crevasse on the west flank and the fissure between
the two halves.

Every field is stated for red's half (z >= the fissure's line) and the board is that half and its half turn, so
blue's ground is red's turned about (-0.5, -0.5). Heights are the top block's y; a player's feet stand one over.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.geom import noise  # noqa: E402
from pgmvox.geom.noise import smoothstep  # noqa: E402
from pgmvox.geom.shapes import polyline, shatter  # noqa: E402

X0, X1, Z0, Z1 = -75, 74, -100, 99            # the board, inclusive; a half turn maps (x, z) to (-1 - x, -1 - z)
NX, NZ = X1 - X0 + 1, Z1 - Z0 + 1
GROUND = 71                                    # the snowfield's top block, feet at 72
LAVA = 22                                      # the fissure's lava surface
LAVA_FLOOR = 16
CLIFF_Z = 56                                   # the cliff's foot
TOP = 100                                      # the mountain's plateau, before its own relief
RIM_HALF = 12.0                                # the fissure's half width at the surface
BOTTOM_HALF = 4.5                              # its half width at the lava
PILLAR = 58                                    # the top of the bore's rock stump in the middle of the fissure
BUTTRESSES = [(-40.5, 13, 48), (34.0, 12, 50)]  # (centre x, half width, foot z): the gate's and the generator house's
GULLIES = [(-64, 3.0, 7), (-22, 2.5, 6), (-6, 3.5, 8), (17, 2.5, 6), (55, 3.0, 7), (68, 2.5, 5)]   # (x, width, depth)
COURTS = [dict(x0=-56, x1=-25, z0=38, z1=47), dict(x0=22, x1=46, z0=42, z1=49)]   # levelled at GROUND
OUTCROPS = [(-62, 32, 11), (-50, 22, 7), (-40, 80, 12), (30, 88, 10), (60, 72, 11)]  # x, z, reach: rock through snow
CREVASSES = [[(-71, 19), (-66, 24), (-60, 21), (-55, 26)]]


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


def buttress(xs):
    """How far each column x stands inside a buttress, 1 across its face falling to 0 at its shoulders, and the
    foot it pushes the cliff out to."""
    weight = np.zeros_like(xs)
    foot = np.full_like(xs, float(CLIFF_Z))
    for cx, half, fz in BUTTRESSES:
        w = 1 - smoothstep(half, half + 7, np.abs(xs - cx))
        foot = foot - (CLIFF_Z - fz) * w
        weight = np.maximum(weight, w)
    return weight, foot


def gullies(xs):
    """The gullies' depth per column x: each a groove cut back into the cliff, deepest at its line."""
    out = np.zeros_like(xs)
    for gx, width, depth in GULLIES:
        out = out + depth * np.exp(-((xs - gx) / width) ** 2)
    return out


def cliff_line():
    """The cliff's foot per column x: wandering, pushed out to the buttresses' feet, set back up each gully."""
    xs = np.arange(X0, X1 + 1, dtype=float)
    wander = 4.0 * noise.fbm((NX,), 30, 3, seed=21)
    weight, foot = buttress(xs)
    return foot + wander * (1 - weight) + 0.6 * gullies(xs)


def red_half(X, Z):
    """Red's ground, stated over the whole grid; only z >= the fissure's line is kept."""
    s = across(X, Z)
    c, half = fissure_line()
    ix = (X - X0).astype(int)
    hw = half[ix]
    # the snowfield: broad swells and drift ridges across a wind from the west
    H = GROUND + 1.6 * noise.fbm(X.shape, 60, 3, seed=1)
    Xw, Zw = noise.warp(X, Z, seed=2, big=8, small=2, big_cell=60, small_cell=14)
    H = H + 0.9 * np.sin(Xw / 7 + 0.3 * Zw / 7) * (0.5 + 0.5 * noise.fbm(X.shape, 40, 2, seed=3))
    # shoulders lifted beside the fissure, as the ground heaved when it opened
    H = H + 2.5 * np.exp(-((s - hw - 7) / 6) ** 2)
    # the east flank raised into a hill that climbs to meet the mountain
    hill = 15 * smoothstep(40, 66, X + 3 * noise.fbm(X.shape, 20, 2, seed=4)) * smoothstep(8, 50, Z)
    H = H + hill * (0.85 + 0.15 * noise.ridged(X.shape, 16, 3, seed=5))
    # the mountain: a cliff from the foot to the plateau, stepped once, ragged, cut by gullies with talus at their feet
    xs = np.arange(X0, X1 + 1, dtype=float)
    foot = cliff_line()[ix]
    groove = gullies(xs)[ix]
    rel = Z - foot
    jag = 1.8 * noise.fbm(X.shape, 5, 2, seed=6)
    top = TOP + 4 * noise.fbm(X.shape, 30, 3, seed=7) + 3 * noise.ridged(X.shape, 14, 3, seed=8)
    top = top - groove * 1.6 * np.exp(-np.maximum(rel, 0) / 14)
    rise = np.clip((rel + jag) / 3.5, 0, 1) * 0.55 + np.clip((rel + jag - 5) / 3.0, 0, 1) * 0.45
    H = np.where(rel > -2, np.maximum(H, H + (top - H) * rise), H)
    talus = 4 * np.exp(-((rel + 3) / 3.5) ** 2) * np.clip(groove / 6, 0, 1) * (rel < 0)
    H = H + talus
    # the courts: levelled in front of the gate and the generator house, eased into the snow round them
    for f in COURTS:
        dx = np.maximum(np.maximum(f["x0"] - X, X - f["x1"]), 0)
        dz = np.maximum(np.maximum(f["z0"] - Z, Z - f["z1"]), 0)
        d = np.hypot(dx, dz)
        H = np.where(rel <= 0, H + (GROUND - H) * (1 - smoothstep(0, 6, d)), H)
    # rock breaking through the snow: faceted, tilted, in clusters on the plateau and the west front
    cells = shatter(X, Z, 6, seed=50, jitter=0.8, warp=(4, 2, 40, 10))
    rng = np.random.default_rng(51)
    n = len(cells.centres)
    tilt_x, tilt_z = rng.uniform(-0.6, 0.6, n), rng.uniform(-0.6, 0.6, n)
    lift = rng.uniform(3, 10, n)
    cid, cen = cells.id, cells.centres
    plane = lift[cid] + tilt_x[cid] * (X - cen[cid, 0]) + tilt_z[cid] * (Z - cen[cid, 1])
    blob = np.zeros(X.shape)
    for cx, cz, r in OUTCROPS:
        blob = np.maximum(blob, 1 - np.hypot(X - cx, Z - cz) / r + 0.35 * noise.fbm(X.shape, 6, 2, seed=52))
    crag = np.clip(blob, 0, 1) ** 0.7
    H = H + np.clip(plane, 0, None) * crag * (cells.edge > 0.6)
    # the crevasse on the west flank
    for k, pts in enumerate(CREVASSES):
        dd, al = polyline(X, Z, pts)[:2]
        width = 1.4 + 1.2 * (0.5 + 0.5 * noise.fbm(X.shape, 9, 2, seed=30 + k))
        end = smoothstep(0, 6, al) * smoothstep(al.max(), al.max() - 6, al)
        H = np.where(dd < width * end, H - (9 + 5 * end) * smoothstep(width, 0.3 * width, dd), H)
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
