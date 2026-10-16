"""Crucible's land: the heights of every column, stated for red's half (z >= 0) and turned onto blue's.

Red's half from the rift outward: the rift's wall falling to the lava sea; the slag plain rising from 45 at the rim
to 50 at the mountain's foot, with the black flow (a cooled lobe with a lava channel down it) on the west, the
sinkhole in the middle, the casting pit at the mountain's foot and the cinder cone on the east; the mountain, its
cliff at z 58 and its spurs at both edges. The board's outline is ragged on the three sides that meet the void.
"""
import math
import os
import sys
from functools import lru_cache

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.geom.noise import fbm, smoothstep

X0, X1, Z0, Z1 = -70, 69, -100, 99
NX, NZ = X1 - X0 + 1, Z1 - Z0 + 1
LAVA = 6                                       # the lava sea's surface
RIFT_FLOOR = 2
FOOT = 58                                      # the mountain's cliff foot, where the facades stand
SEED = 7307
CONE = (47, 38, 14)                            # the cinder cone: x, z, radius; its west flank is cut by the pit
HEAPS = [(-18, 44, 4.5, 4.0), (-29, 31, 3.8, 3.0)]
HORNITOS = [(-3, 22, 2.6, 3.0), (27, 19, 2.8, 3.5)]
ROADS = [[(-30, 57), (-27, 47), (-22, 36), (-17, 25), (-14, 16), (-12, 11)],
         [(15, 31), (9, 24), (0, 18), (-8, 14), (-12, 11)]]


def grid():
    return np.meshgrid(np.arange(X0, X1 + 1), np.arange(Z0, Z1 + 1), indexing="ij")


def red_mask(X, Z):
    return Z >= 0


def sym(a):
    """A field drawn for red's half, carried onto blue's by the half turn: (i, k) -> (NX-1-i, NZ-1-k)."""
    X, Z = grid()
    return np.where(red_mask(X, Z), a, a[::-1, ::-1])


@lru_cache(None)
def rim():
    """The z of red's rim for every x: about 10, wandering two blocks."""
    n = fbm((NX,), 30, 3, seed=SEED)
    return 10.0 + 3.4 * n


@lru_cache(None)
def flow_line():
    """The black flow's centre line, from the mountain to the rift: (x, z) points."""
    return [(-56, 62), (-52, 50), (-46, 38), (-43, 26), (-41, 14), (-40, 6)]


def _dist_to_polyline(X, Z, pts):
    best = np.full(X.shape, np.inf)
    along = np.zeros(X.shape)
    acc = 0.0
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        dx, dz = bx - ax, bz - az
        L2 = dx * dx + dz * dz
        t = np.clip(((X - ax) * dx + (Z - az) * dz) / L2, 0, 1)
        d = np.hypot(X - (ax + t * dx), Z - (az + t * dz))
        closer = d < best
        best = np.where(closer, d, best)
        along = np.where(closer, acc + t * math.sqrt(L2), along)
        acc += math.sqrt(L2)
    return best, along


@lru_cache(None)
def flow():
    """The black flow: (mask of the lobe, mask of its channel, the lobe's top) over the grid, red's half only."""
    X, Z = grid()
    d, along = _dist_to_polyline(X, Z, flow_line())
    width = 7.0 + 2.0 * fbm(X.shape, 9, 2, seed=SEED + 5) + 1.5 * np.clip(along / 60.0, 0, 1)
    lobe = (d <= width) & (Z >= rim()[:, None] - 0.5)
    channel = (d <= 1.0) & (Z >= rim()[:, None] - 0.5)
    return lobe, channel, d, width


def pit_polar(X, Z):
    from plan import PIT
    u, v = (X - PIT["x"]) / PIT["rx"], (Z - PIT["z"]) / PIT["rz"]
    e = np.hypot(u, v)
    theta = np.degrees(np.arctan2(v, u)) % 360
    return e, theta


def pit_heights(X, Z, plain):
    """The casting pit's floor, its east bench and the haul ramp spiralling down its west wall, where they cut the
    plain; NaN outside the pit."""
    from plan import APRON, PIT
    e, th = pit_polar(X, Z)
    out = np.full(X.shape, np.nan)
    on_ramp = (th >= PIT["ramp_to"]) & (th <= PIT["ramp_from"])
    s = (PIT["ramp_from"] - th) / (PIT["ramp_from"] - PIT["ramp_to"])
    ramp = np.round(PIT["ramp_top"] + (PIT["floor"] - PIT["ramp_top"]) * s)
    out = np.where(on_ramp & (e <= PIT["ramp_e"]) & (e > PIT["floor_e"]), ramp, out)
    out = np.where(~on_ramp & (e <= PIT["bench_e"]) & (e > PIT["floor_e"]), PIT["bench"], out)
    out = np.where(e <= PIT["floor_e"], PIT["floor"], out)
    x0, x1, z0, z1 = APRON
    out = np.where((X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1), PIT["floor"], out)
    return out


@lru_cache(None)
def heights():
    """Every column's top block y, both halves, as floats (rounded by the caller)."""
    from plan import FACADE_GATE, FACADE_PIT
    X, Z = grid()
    r = rim()[:, None]
    n1 = fbm(X.shape, 24, 3, seed=SEED + 1)
    n2 = fbm(X.shape, 8, 2, seed=SEED + 2)
    plain = 45.0 + 5.0 * smoothstep(r, 56.0, Z) + 1.1 * n1 + 0.5 * n2

    # the rift: the wall falls from the rim to the lava sea's floor in a few ragged ledges
    d = r - Z
    jag = 2.5 * fbm(X.shape, 6, 2, seed=SEED + 3)
    wall = RIFT_FLOOR + (45.0 - RIFT_FLOOR) * np.clip(1 - (d + 0.4 * jag) / 6.0, 0, 1) ** 0.55
    H = np.where(d > 0, np.minimum(plain, wall), plain)

    # the black flow: a lobe two to three over the plain, its edges steep
    lobe, channel, dl, width = flow()
    lift = 2.6 * smoothstep(width, width - 2.0, dl) + 0.4 * n2
    H = np.where(lobe, H + lift, H)

    # the cinder cone on the east, with a small crater
    cx, cz, cr = CONE
    rc = np.hypot(X - cx, Z - cz) + 1.0 * fbm(X.shape, 7, 2, seed=SEED + 4)
    cone = 46.0 + 17.0 * np.clip(1 - rc / cr, 0, 1) ** 1.15
    cone = np.where(rc < 3.2, cone - 3.5 * (1 - rc / 3.2), cone)
    H = np.where(rc < cr, np.maximum(H, cone), H)

    # slag heaps beside the slag road, and hornitos (small spatter cones) on the open plain
    for hx, hz, hr, hh in HEAPS + HORNITOS:
        rr = np.hypot(X - hx, Z - hz) + 0.6 * fbm(X.shape, 4, 2, seed=SEED + int(hx * 7 + hz))
        H = np.where(rr < hr, np.maximum(H, H + hh * np.clip(1 - rr / hr, 0, 1) ** 0.8), H)

    # the sinkhole: a pit sunk six blocks, its floor at 41
    rs = np.hypot(X + 6, Z - 30) + 0.8 * fbm(X.shape, 5, 2, seed=SEED + 6)
    H = np.where(rs < 6.0, np.minimum(H, 41.0 + (H - 41.0) * smoothstep(3.6, 6.0, rs)), H)

    # the mountain: a cliff from the foot, then the long climb to its crest, crests and gullies on it
    ridge = fbm(X.shape, 30, 3, seed=SEED + 8)
    spur_w = smoothstep(-48.0, -62.0, X)
    spur_e = smoothstep(50.0, 62.0, X)
    pinned = np.zeros(X.shape)                                     # the facades' stretches: the foot held at FOOT
    for f in (FACADE_PIT, FACADE_GATE):
        pinned = np.maximum(pinned, smoothstep(f["x0"] - 5.0, f["x0"] - 1.0, X) * smoothstep(f["x1"] + 5.0, f["x1"] + 1.0, X))
    wander = 2.6 * fbm(X.shape, 9, 2, seed=SEED + 9)
    foot = FOOT - 12.0 * spur_w - 10.0 * spur_e + wander * (1 - pinned)
    t = Z - foot
    cliff = 1.0 - 0.45 * np.maximum(spur_w, spur_e)               # the spurs climb more gently
    ledge = 2.5 + 1.2 * fbm(X.shape, 11, 2, seed=SEED + 10)       # how deep the ledge between the cliff's tiers is
    M = 49.0 + cliff * (17.0 * smoothstep(0.0, 2.0, t) + 12.0 * smoothstep(2.0 + ledge, 4.5 + ledge, t)) \
        + 9.0 * (1 - cliff) * smoothstep(0, 10.0, t) + 16.0 * smoothstep(8.0, 30.0, t) \
        + 3.0 * ridge * smoothstep(6.0, 18.0, t)
    M = np.where(t < 0, -1.0, M)
    H = np.maximum(H, M)

    # the pit is cut last, through whatever stood there
    P = pit_heights(X, Z, plain)
    H = np.where(np.isnan(P), H, P)
    # the facades stand in the cliff's foot: the plan reads their tops
    for f in (FACADE_PIT, FACADE_GATE):
        m = (X >= f["x0"]) & (X <= f["x1"]) & (Z >= f["z0"]) & (Z <= f["z1"])
        H = np.where(m, np.maximum(H, f["top"]), H)
    return sym(H)


@lru_cache(None)
def inside():
    """The board's outline: ragged on the east, west and back, where the land meets the void."""
    X, Z = grid()
    bite_x = np.round(1.6 + 1.6 * fbm((NZ,), 7, 2, seed=SEED + 11))[None, :]
    bite_x2 = np.round(1.6 + 1.6 * fbm((NZ,), 7, 2, seed=SEED + 12))[None, :]
    bite_z = np.round(1.6 + 1.6 * fbm((NX,), 7, 2, seed=SEED + 13))[:, None]
    m = (X - X0 >= bite_x) & (X1 - X >= bite_x2) & (Z1 - Z >= bite_z)
    return sym(m)


@lru_cache(None)
def lava_channel():
    """The black flow's channel, red's half and blue's: columns whose top holds lava a block under the lobe."""
    X, Z = grid()
    _, channel, _, _ = flow()
    return sym(channel & (Z >= 0))
