"""Gullhaven — a free-for-all plan: a fishing island, everyone against everyone, one hit kills.

No teams and no symmetry. A player spawns at one of many points spread over the island, picked away from the
others, with a sword, a bow and one arrow; a kill pays one more arrow. So the island is built for the meeting:
places where a player can see a little and be seen a little, ways round every open ground, cover a step away,
and nothing a player can hide inside. The houses are closed; nobody walks into them.

The island, north at the top:

    the Headland   the north-west: a grass plateau at 38 to 41, rolling and falling toward its edges, with
                   cliffs on three sides,, a lighthouse and a
                   ruined chapel whose crypt drops into the caves
    the Ravine     a cleft between the Headland and the town, its floor at 24 with a stream; a bridge across
    the Town       the north-east: three terraces at 36, 32 and 28, streets and stairs between closed houses
    the Harbour    the south-east: a quay at 22 round a basin open to the sea, piers, sheds, boats, crates
    the Downs      the south-west: grass rising from 24 at the shore to 31 under the Headland, rolling, a
                   ring of standing stones, a mill, a sinkhole
    the Cove       the west: a beach at 19 to 21 under the Downs' edge, with the sea cave's mouth
    the Caves      under the Headland and the Downs: a grotto at 21 and four ways into it
    the Skerry     a rocky islet off the Downs' south shore, 23 at its rim to 26 at its crown, reached by a bridge over the sea

The plan is a height raster with a kind for every column, an upper raster for the bridge, and lists of what
a raster cannot hold: the caves, the ramps, the houses and the cover. The checker walks it, the sketch draws
it, and the generator will build from it.
"""
import math

import numpy as np

from geometry import inside, polyline, signed_distance
from noise import fbm

X_MIN, X_MAX = -68, 67              # the island and twelve blocks of sea round it, so every cliff has a foot
Z_MIN, Z_MAX = -62, 80
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
SEA = 18                    # the sea's surface; its floor at 13
KINDS = {"sea": 0, "grass": 1, "beach": 2, "rock": 3, "street": 4, "quay": 5, "ramp": 6, "ravine": 7,
         "stream": 8, "house": 9, "cover": 10, "tree": 11, "pier": 12, "landmark": 13}
WALK = {"grass", "beach", "rock", "street", "quay", "ramp", "ravine", "stream", "pier"}

XS, ZS = np.meshgrid(np.arange(X_MIN, X_MAX + 1), np.arange(Z_MIN, Z_MAX + 1), indexing="ij")


def ix(x):
    return x - X_MIN


def iz(z):
    return z - Z_MIN


ISLAND = [(-52, -36), (-38, -48), (-14, -49), (4, -48), (24, -48), (40, -44), (50, -30), (51, -10), (48, 6),
          (50, 22), (46, 40), (36, 46), (18, 46), (2, 42), (-14, 44), (-30, 38), (-42, 28), (-54, 22),
          (-55, 0), (-54, -20)]
HEADLAND = [(-52, -36), (-38, -48), (-13, -49), (-11, -32), (-13, -20), (-24, -13), (-40, -12), (-54, -18)]
COVE = [(-56, -12), (-44, -11), (-41, -2), (-41, 14), (-47, 22), (-56, 21)]
RAVINE = [(-11, -52), (-9, -40), (-8, -28), (-6, -17)]
TOWN = [  # three terraces, high to low, each a polygon
    (36, [(-3, -49), (40, -47), (36, -28), (-2, -27)]),
    (32, [(-3, -27), (36, -28), (50, -26), (51, -12), (-4, -12)]),
    (28, [(-4, -12), (51, -12), (48, 8), (2, 8)]),
]
QUAY = [(8, 8), (48, 8), (49, 18), (40, 18), (20, 20), (19, 36), (8, 36)]
SKERRY = [(-27, 52), (-14, 50), (-8, 56), (-11, 64), (-22, 66), (-30, 60)]   # the islet off the Downs
BASIN = [(20, 19), (42, 17), (47, 50), (18, 50)]
PIERS = [(26, 27, 19, 34), (35, 36, 18, 30)]           # x0, x1, z0, z1 at the quay's height


# the noise was laid on the first board, x -56..55 and z -50..68; it is laid there still and padded out over the
# sea margin added round it, so the island the reviews approved is the island built
NOISE_BOX = (-56, -50, 112, 119)


def noise(cell, octaves, seed):
    x0, z0, sx, sz = NOISE_BOX
    n = fbm((sx, sz), cell, octaves, seed=seed)
    return np.pad(n, ((x0 - X_MIN, X_MAX - (x0 + sx - 1)), (z0 - Z_MIN, Z_MAX - (z0 + sz - 1))), mode="edge")


class Raster:
    def __init__(self):
        self.H = np.full((NX, NZ), SEA, int)
        self.K = np.full((NX, NZ), KINDS["sea"], int)
        self.U = np.full((NX, NZ), -1, int)            # the bridge's deck, or -1

    def set(self, mask, h, kind):
        self.H[mask] = h if np.isscalar(h) else h[mask]
        self.K[mask] = KINDS[kind]


def build():
    R = Raster()
    n1 = noise(24, 3, 11)
    n2 = noise(9, 2, 12)
    land = signed_distance(XS, ZS, ISLAND) + 2.2 * n2 < 0
    # the Downs: everything on the island not otherwise claimed, rolling between 26 and 30
    # the Downs: rising from about 24 at the shore to about 31 under the Headland, rolling a block or two
    from scipy import ndimage
    d_sea = ndimage.distance_transform_edt(land)
    d_head = signed_distance(XS, ZS, HEADLAND)
    rise = 4.5 * np.clip(d_sea / 14.0, 0, 1) + 2.5 * (1 - np.clip(d_head / 30.0, 0, 1))
    downs = np.rint(24 + rise + 1.4 * n1 + 0.6 * n2).astype(int)
    R.set(land, downs, "grass")
    # the Skerry: a rocky islet off the Downs' south shore, at 24 to 26
    sk = signed_distance(XS, ZS, SKERRY) + 1.2 * n2 < 0
    d_sk = -signed_distance(XS, ZS, SKERRY)
    R.set(sk, np.rint(23 + 3.0 * np.clip(d_sk / 5.0, 0, 1) + 1.2 * n1).astype(int), "grass")
    land = land | sk
    # the Cove: a beach rising from the sea to the Downs' foot
    cove = inside(XS, ZS, COVE) & land
    R.set(cove, np.clip(19 + (XS + 56) // 5, 19, 21).astype(int), "beach")
    # the Headland: a plateau at 40, cliffs on every side
    head = inside(XS, ZS, HEADLAND) & land
    d_edge = -d_head
    R.set(head, np.rint(38 + 2.2 * np.clip(d_edge / 6.0, 0, 1) + 1.3 * n1 + 0.6 * n2).astype(int), "grass")
    # the Town's terraces
    for h, poly in TOWN:
        R.set(inside(XS, ZS, poly) & land, h, "street")
    # the Harbour: the quay, the basin cut into it, the piers
    R.set(inside(XS, ZS, QUAY) & land, 22, "quay")
    basin = inside(XS, ZS, BASIN)
    R.set(basin, SEA, "sea")
    for x0, x1, z0, z1 in PIERS:
        m = (XS >= x0) & (XS <= x1) & (ZS >= z0) & (ZS <= z1)
        R.set(m, 22, "pier")
    # the Ravine: a floor at 24 seven wide, a stream down its middle, rising at its south end to the Downs
    d, along = polyline(XS, ZS, RAVINE)
    floor = np.where(ZS > -24, np.minimum(24 + (ZS + 24) // 2, R.H), 24)
    rv = (d < 3.6) & land                                     # it ends at the shore, a valley mouth over the sea
    R.set(rv, floor, "ravine")
    R.set(rv & (d < 0.9) & (ZS < -22), 23, "stream")
    for ramp in RAMPS:
        lay_ramp(R, ramp)
    R.ramp_heights = {r["key"]: (r["_h0"], r["_h1"]) for r in RAMPS}
    R.set(~land & ~rv & (R.K != KINDS["beach"]), SEA, "sea")
    # the bridges: over the Ravine from the Headland's lip to the upper terrace, and over the sea from the
    # Downs' south shore to the Skerry; each deck slopes no more than one in three
    for br in BRIDGES:
        d, along = polyline(XS, ZS, br["pts"])
        L = sum(math.dist(a, b) for a, b in zip(br["pts"], br["pts"][1:]))
        h0, h1 = end_height(R, br["pts"], br["h0"], True), end_height(R, br["pts"], br["h1"], False)
        deck = np.rint(h0 + (h1 - h0) * along / L).astype(int)
        m = (d <= br["half"]) & np.isin(R.K, [KINDS[k] for k in br["over"]])
        R.U[m] = deck[m]
    R.G = R.H.copy()                                           # the ground, before anything stands on it
    # what stands on the ground: houses, landmarks, cover, trees
    for hs in HOUSES:
        for x, z in house_cells(hs):
            R.H[ix(x), iz(z)] = R.H[ix(x), iz(z)] + 8
            R.K[ix(x), iz(z)] = KINDS["house"]
    for lm in LANDMARKS:
        for x, z in lm["cells"]:
            R.H[ix(x), iz(z)] += lm["tall"]
            R.K[ix(x), iz(z)] = KINDS["landmark"]
    for x, z, tall in COVER:
        R.H[ix(x), iz(z)] += tall
        R.K[ix(x), iz(z)] = KINDS["cover"]
    for line, tall in [(l, 2) for l in HEDGES] + [(l, 2) for l in WALLS]:
        d, along = polyline(XS, ZS, line)
        m = (d < 0.75) & np.isin(R.K, [KINDS["grass"], KINDS["street"]])
        R.H[m] += tall
        R.K[m] = KINDS["cover"]
    for x, z in TREES:
        R.H[ix(x), iz(z)] += 6
        R.K[ix(x), iz(z)] = KINDS["tree"]
    return R


# ---- ramps: a polyline, its half-width, and the heights at its two ends. Slope at most one in one. -------
RAMPS = [
    dict(key="headland-path", pts=[(-38, -15), (-31, -9), (-24, -3)], half=1.5, h0=None, h1=None),
    dict(key="town-stair-1", pts=[(14, -30), (14, -24)], half=1.5, h0=36, h1=32),
    dict(key="town-stair-2", pts=[(22, -14), (22, -8)], half=1.5, h0=32, h1=28),
    dict(key="town-stair-3", pts=[(-1, -14), (-1, -9)], half=1.0, h0=32, h1=28),
    dict(key="quay-road", pts=[(30, 6), (30, 14)], half=2.0, h0=28, h1=22),
    dict(key="quay-steps", pts=[(9, 6), (9, 12)], half=1.0, h0=28, h1=22),
    dict(key="cove-path", pts=[(-43, 8), (-34, 9)], half=1.5, h0=21, h1=None),
    dict(key="downs-quay", pts=[(8, 30), (1, 30)], half=1.5, h0=22, h1=None),
]


def end_height(R, pts, h, at_start):
    """A ramp's or bridge's end height: as written, or, where None, the ground's just past that end."""
    if h is not None:
        return h
    (ax, az), (bx, bz) = (pts[0], pts[1]) if at_start else (pts[-1], pts[-2])
    L = math.dist((ax, az), (bx, bz))
    x, z = int(round(ax + (ax - bx) / L * 2)), int(round(az + (az - bz) / L * 2))
    return int(R.H[ix(x), iz(z)])


def lay_ramp(R, ramp):
    d, along = polyline(XS, ZS, ramp["pts"])
    L = sum(math.dist(a, b) for a, b in zip(ramp["pts"], ramp["pts"][1:]))
    h0, h1 = end_height(R, ramp["pts"], ramp["h0"], True), end_height(R, ramp["pts"], ramp["h1"], False)
    assert abs(h1 - h0) <= L, (ramp["key"], h0, h1, L)
    ramp["_h0"], ramp["_h1"] = h0, h1
    h = np.rint(h0 + (h1 - h0) * np.clip(along / L, 0, 1)).astype(int)
    m = d <= ramp["half"]
    R.H[m] = h[m]
    R.K[m] = KINDS["ramp"]


BRIDGES = [dict(key="ravine-bridge", pts=[(-14, -34), (-2, -33)], half=1.0, h0=40, h1=36, over=("ravine", "stream")),
           dict(key="skerry-bridge", pts=[(-13, 43), (-15, 52)], half=1.0, h0=None, h1=None, over=("sea",))]

# ---- the caves: (x, z, floor) polylines three wide and three high, and the grotto they meet in -----------
GROTTO = dict(box=(-38, -30, -28, -20), floor=21, ceil=27)
TUNNELS = [
    dict(key="sea-cave", a=(-46, -6), b=(-34, -24), pts=[(-46, -6, 21), (-42, -8, 21), (-40, -14, 21), (-34, -22, 21)]),
    dict(key="sinkhole", a=(-20, 6), b=(-34, -24), pts=[(-20, 6, 27), (-20, -2, 21), (-28, -14, 21), (-32, -22, 21)]),
    dict(key="ravine-door", a=(-11, -24), b=(-34, -24), pts=[(-11, -24, 24), (-16, -24, 23), (-24, -24, 22), (-30, -24, 21)]),
    dict(key="crypt", a=(-24, -32), b=(-34, -24), pts=[(-24, -32, 40), (-24, -32, 22), (-29, -28, 21)], ladder=True),
]

# ---- what stands on the ground ----------------------------------------------------------------------------
HOUSES = [  # cx, cz, heading, L, W, storeys, style: closed, no way in
    # the upper terrace: a row along the north edge, a row facing it across a street, a square at the stair
    dict(cx=3, cz=-44, heading=0, L=9, W=6, storeys=2, style="plaster"),
    dict(cx=22, cz=-44, heading=0, L=10, W=6, storeys=2, style="town"),
    dict(cx=33, cz=-43, heading=0, L=8, W=6, storeys=2, style="plaster"),
    dict(cx=3, cz=-32, heading=0, L=8, W=5, storeys=1, style="stone"),
    dict(cx=24, cz=-32, heading=0, L=9, W=6, storeys=2, style="town"),
    dict(cx=34, cz=-33, heading=90, L=7, W=5, storeys=2, style="plaster"),
    # the middle terrace: houses stepped along its north wall, a row in the middle, a lane between
    dict(cx=5, cz=-21, heading=0, L=9, W=6, storeys=2, style="town"),
    dict(cx=30, cz=-22, heading=0, L=9, W=6, storeys=2, style="plaster"),
    dict(cx=43, cz=-20, heading=90, L=8, W=6, storeys=1, style="stone"),
    dict(cx=18, cz=-20, heading=12, L=6, W=5, storeys=2, style="brick"),
    # the lower terrace
    dict(cx=11, cz=-3, heading=0, L=9, W=6, storeys=2, style="plaster"),
    dict(cx=36, cz=-4, heading=0, L=10, W=6, storeys=2, style="town"),
    dict(cx=24, cz=-2, heading=-10, L=7, W=5, storeys=2, style="brick"),
    dict(cx=44, cz=3, heading=90, L=6, W=5, storeys=1, style="stone"),
    # the harbour
    dict(cx=44, cz=13, heading=90, L=7, W=5, storeys=1, style="stone"),     # the fish shed
    dict(cx=14, cz=28, heading=90, L=9, W=6, storeys=1, style="stone"),     # the net loft
]


def house_cells(hs):
    t = math.radians(hs["heading"])
    c, s = math.cos(t), math.sin(t)
    out = []
    R = int(max(hs["L"], hs["W"]))
    for x in range(int(hs["cx"]) - R, int(hs["cx"]) + R + 1):
        for z in range(int(hs["cz"]) - R, int(hs["cz"]) + R + 1):
            dx, dz = x - hs["cx"], z - hs["cz"]
            u, v = dx * c + dz * s, -dx * s + dz * c
            if abs(u) <= hs["L"] / 2 and abs(v) <= hs["W"] / 2:
                out.append((x, z))
    return out


def disc(cx, cz, r):
    return [(x, z) for x in range(int(cx - r) - 1, int(cx + r) + 2) for z in range(int(cz - r) - 1, int(cz + r) + 2)
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r]


LANDMARKS = [
    dict(key="lighthouse", name="the lighthouse", cells=disc(-42, -38, 3.5), tall=20),
    dict(key="mill", name="the mill", cells=disc(-30, 26, 3.0), tall=12),
]
# the chapel is a ruin: walls two high with gaps, open to the sky, the crypt's ladder inside
CHAPEL = dict(box=(-28, -20, -38, -26), walls=2)
STONES = [(-8 + round(6 * math.cos(a)), 18 + round(6 * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 9)[:-1]]
COVER = ([(x, z, 3) for x, z in STONES] +                                               # the standing stones
         [(x, z, 2) for x, z in ((-24, -44), (-30, -42), (-46, -26), (-18, -20), (-36, -18),   # rocks on the Headland
                                 (-14, 30), (-22, 34), (-36, 4), (-2, 12), (2, 24), (-26, 14),   # rocks on the Downs
                                 (16, -38), (18, -38), (38, -38), (20, -16), (40, -14),          # crates and carts in town
                                 (18, -4), (26, 2), (2, -8),
                                 (18, 12), (19, 12), (24, 14), (12, 13), (13, 13), (12, 16), (38, 14), (12, 22), (12, 23),     # crates on the quay
                                 (-50, 6), (-48, 14), (-46, -6),                                 # driftwood on the Cove
                                 (-18, 56), (-19, 56), (-26, 57), (-16, 62))])                  # the Skerry's rocks
# hedgerows on the Downs and a dry-stone wall across the Headland: lines of cover two high, with gaps
HEDGES = [[(-34, 0), (-26, 0)], [(-22, 0), (-14, 2)], [(-6, 22), (-6, 30)], [(-26, 16), (-26, 24)],
          [(-40, 30), (-34, 34)], [(4, 18), (4, 24)]]
WALLS = [[(-48, -24), (-40, -24)], [(-36, -24), (-30, -22)], [(-20, -46), (-20, -40)], [(-16, -26), (-14, -20)]]
COPSE = [(-16, 6), (-13, 9), (-17, 11), (-11, 13), (-14, 16), (-19, 15), (-9, 6)]
TREES = COPSE + [(-24, 62), (-11, 55), (-48, -18), (-42, -15), (-30, -17), (-20, -19), (-50, -28), (-34, -44), (-20, -42), (-48, -30), (-16, 14), (-28, 4), (-38, 18), (-20, 26), (-10, 36), (4, 34),
         (0, 2), (-34, 32), (14, -46), (46, -40), (46, -6), (-2, -20)]
# the spawn points: spread over every part of the island; PGM picks the one farthest from the players
SPAWNS = [  # x, z, and what the player faces (yaw)
    (-44, -30, -90), (-30, -36, 0), (-18, -44, 90), (-34, -16, 180),       # the Headland
    (-7, -37, 0), (-8, -44, 180),                                          # the Ravine
    (8, -46, 0), (30, -38, 90), (20, -26, 0), (46, -26, 90), (-1, -17, 0), (40, -8, 180), (16, -8, 0), (4, 4, 90),  # the Town
    (30, 12, 0), (16, 16, 180), (26, 31, 180), (9, 33, 0),                # the Harbour
    (-6, 10, 0), (-20, 20, 0), (-12, 30, 90), (-30, 12, 0), (-4, 36, 180),  # the Downs
    (-52, 2, -90), (-50, 16, -90),                                         # the Cove
    (-22, 59, 0), (-13, 58, 90),                                           # the Skerry
]
CAVE_SPAWNS = [(-34, -26, 0, 21), (-20, -4, 180, 21)]                      # in the grotto and the sinkhole tunnel


_R = None


def H_at(x, z):
    global _R
    if _R is None:
        _R = build()
    return int(_R.H[ix(x), iz(z)])
