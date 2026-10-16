"""Rimefire's ground: one heightfield drawn for the north half and turned half round the board's middle, so the
fire half and the ice half are the same bones in two skins. Heights are the y of the top block.

    the seam      a ravine across the whole island at z -0.5; lava runs in its north foot, meltwater ice in its south
    the crossings three bridges over it: two flank spans and the keystone in the middle
    the back      a ridge at each end of the board with the spawn plateau in front of it
    the furnace   a tor on the east of the fire half whose top holds the fire core (the ice core is its half turn)
    the hollow    a basin on the west where the hamlet stands
"""
import numpy as np

from pgmvox.geom import noise, shapes
from pgmvox.ground import landform as L
from pgmvox.routes import route as R

X0, Z0, NX, NZ = -80, -110, 160, 220
SY = 128
LEVEL = 63                 # the plateau, the landings and the bridge decks: the y of the top block
FLOOR = 45                 # the seam's floor
SEAM_Z = -0.5              # the half turn's centre line in z (and in x)
KILL_Y = 26

# north-half places (x, z); the south half is the half turn: (-1 - x, -1 - z)
SPAWN = (-14, -76)
FURNACE = (27, -53)
HOLLOW = (-40, -41)
OVERLOOK = (-7, -34)
SPAWN_R = 13
FURNACE_R = 11
TOR = 9                    # the furnace's plateau stands this far over the level
BRIDGES = {"west": (-40, 4), "keystone": (-0.5, 6), "east": (39, 4)}      # centre x, half width (west/east are images)
CORE_BOX = (FURNACE[0] - 2, LEVEL + TOR - 1, FURNACE[1] - 2, FURNACE[0] + 2, LEVEL + TOR + 3, FURNACE[1] + 2)
RAMPS = [("charred stair", (-24, 1)), ("slag stair", (22, 1))]          # (x where it starts on the floor, direction)

RIDGE_W = [(-27, -66), (-25, -46), (-22, -27), (-28, -12)]
RIDGE_E = [(8, -64), (13, -48), (11, -31), (17, -15)]

OUTLINE = [(-62, 1), (-65, -18), (-59, -42), (-63, -64), (-52, -86), (-34, -99), (-4, -101), (22, -102), (47, -93),
           (61, -68), (58, -42), (65, -18), (61, 1)]


def turn(x, z):
    return -1 - x, -1 - z


def grid():
    return np.meshgrid(np.arange(X0, X0 + NX), np.arange(Z0, Z0 + NZ), indexing="ij")


def half(F, blend=14.0, Z=None):
    """A field drawn for the north half, made whole: the half turn of it south of the line, blended across it, so
    the result is exactly its own half turn."""
    if Z is None:
        _, Z = grid()
    t = noise.smoothstep(SEAM_Z - blend, SEAM_Z + blend, Z)        # 0 north, 1 south
    return (1 - t) * F + t * F[::-1, ::-1]


def seam_zone(X, Z, extra=0):
    return np.abs(Z - centre(X)) < 9.5 + extra


def sym(F):
    """A field made its own half turn: the mean of it and its turn."""
    return (F + F[::-1, ::-1]) / 2


_XS = np.arange(X0, X0 + NX)
_MT = noise.fbm((NX,), 40, 2, seed=41)
_MT = 9.0 * (_MT - _MT[::-1]) + 5.0 * np.sin((_XS + 0.5) / 22.0)


def centre(x):
    """The seam's centre line: its z at x. Odd about x -0.5 around z -0.5, so the line is its own half turn."""
    return SEAM_Z + np.interp(x, _XS, _MT)


def seam_d(X, Z):
    return np.abs(Z - centre(X))


def landmask(X, Z):
    Xw, Zw = noise.warp(X, Z, seed=17, big=5.0, small=2.2, big_cell=60, small_cell=14)
    a = shapes.inside(Xw, Zw, OUTLINE)
    return a | a[::-1, ::-1]                                   # the grid is its own half turn when flipped


def bump(X, Z, at, r, power=2.0):
    d = np.hypot(X - at[0], Z - at[1]) / r
    return np.clip(1 - d ** power, 0, 1)


def level_to(H, X, Z, at, r, y, reach=8, rx=None):
    """Level ground toward y inside radius r, eased back to what was there over `reach` more blocks."""
    d = np.hypot((X - at[0]) / (rx or 1), Z - at[1]) if rx is None else np.hypot((X - at[0]) * r / rx, Z - at[1])
    t = noise.smoothstep(r + reach, r, d)
    return H * (1 - t) + y * t


def ramp(H, X, Z, a, b, y0, y1, width, reach=2.0):
    """A graded way from a (height y0) to b (height y1): the ground within `width` of the line is set to the grade, so
    it cuts the rock above it and fills the ground below it, and eases back to the ground over `reach` more."""
    d, t = shapes.seg_distance(X, Z, a, b)
    y = y0 + (y1 - y0) * t
    k = noise.smoothstep(width / 2 + reach, width / 2, d)
    return H * (1 - k) + y * k


def ground():
    """The ground, computed once per version of this file and kept beside the build."""
    import hashlib, os, pickle
    key = hashlib.sha1(open(__file__, 'rb').read()).hexdigest()[:12]
    path = os.path.join(os.environ.get('RIMEFIRE_CACHE', '/tmp'), f'rimefire-land-{key}.pkl')
    if os.path.isfile(path):
        with open(path, 'rb') as fh:
            return pickle.load(fh)
    g = _ground()
    with open(path, 'wb') as fh:
        pickle.dump(g, fh)
    return g


def _ground():
    X, Z = grid()
    shape = X.shape
    land = landmask(X, Z)
    Xw, Zw = noise.warp(X, Z, seed=5, big=9.0, small=3.0, big_cell=45, small_cell=12)   # features are measured in a bent frame
    n1 = noise.fbm(shape, 64, 4, seed=3)
    n2 = noise.fbm(shape, 20, 3, seed=4)
    n3 = noise.fbm(shape, 9, 2, seed=5)
    F = LEVEL + 6.0 * n1 + 2.2 * n2 + 0.6 * n3 + 5.0 * (noise.ridged(shape, 40, 3, seed=6) - 0.6)   # rolling ground

    # the back ridge behind the spawn: a crest wandering along the north end, with a pass either side of the spawn
    crest = -90 + 5 * noise.fbm(shape, 50, 2, seed=8)
    ridge = np.exp(-(((Z - crest) / 10.5) ** 2))
    F += ridge * (24 + 10 * noise.ridged(shape, 22, 3, seed=9)) * (0.75 + 0.25 * noise.fbm(shape, 30, 2, seed=10))
    # a second, lower line of knolls in front of it, so the spawn plateau sits in a cradle of ground
    knolls = noise.fbm(shape, 28, 3, seed=11)
    F += np.clip(knolls - 0.15, 0, 1) * 16 * np.exp(-(((Z + 66) / 16) ** 2))

    # two ridges running toward the seam divide the half into three lanes; each is broken by a pass
    for pts, seed in ((RIDGE_W, 31), (RIDGE_E, 32)):
        dist, along = shapes.polyline(X, Z, pts)
        crest = 13 + 7 * noise.fbm(shape, 24, 2, seed=seed)
        F += crest * np.exp(-((dist / (7.5 + 2 * n2)) ** 2)) * noise.smoothstep(-0.1, 0.35, noise.fbm(shape, 34, 2, seed=seed + 5))
    # the overlook: a hill in the lane between the spawn and the keystone, longer along the lane than across
    F += 17 * bump(Xw, Zw, OVERLOOK, 17, 2.3) * (0.85 + 0.15 * n2)
    # the hollow: a basin on the west with a rim to its west
    F -= 8 * bump(Xw, Zw, HOLLOW, 22, 2.0)
    F += 13 * bump(Xw, Zw, (HOLLOW[0] - 25, HOLLOW[1] - 6), 16, 2.0) * (0.8 + 0.2 * n2)
    # the basalt scarp on the east: a wall of ground standing over the furnace's flank
    F += 22 * np.exp(-(((Xw - 55) / 6.5) ** 2)) * np.exp(-(((Zw + 46) / 26) ** 2)) * (0.8 + 0.2 * n2)
    # the furnace tor
    tor = bump(Xw, Zw, FURNACE, 18, 2.6)
    F += 11 * tor * (0.9 + 0.1 * n2)
    F = level_to(F, Xw, Zw, FURNACE, FURNACE_R, LEVEL + TOR, reach=7)
    # the spawn plateau
    F = level_to(F, Xw, Zw, SPAWN, SPAWN_R, LEVEL + 1, reach=11)
    # the island's own edge: ground falls to a shoulder before the void, so no edge is a wall of its full height
    d_edge = shapes.distance_in(land, "euclid")
    F -= 7 * noise.smoothstep(7, 0, d_edge)

    H = half(F, Z=Z)
    land = land

    # landings at each crossing: level ground on both rims
    for cx, hw in BRIDGES.values():
        for sgn in (1, -1):
            zc = float(centre(cx)) + sgn * 13
            H = level_to(H, X, Z, (cx, zc), 7, LEVEL, reach=8)

    # roads, found over the north half and graded 1 in 5 or gentler, then turned for the south half
    lanes = {}
    heads = {k: (cx, float(centre(cx)) - 10.5) for k, (cx, hw_) in BRIDGES.items() if k != "east"}
    heads["east"] = (BRIDGES["east"][0], float(centre(BRIDGES["east"][0])) - 10.5)
    PLACES = dict(spawn=(-14, -64), hollow=(-38, -44), overlook=(-7, -35), tor_foot=(12, -58),
                  furnace=(16.5, -53), west_head=heads["west"], key_head=heads["keystone"], east_head=heads["east"])
    JOINS = [("spawn", "hollow"), ("spawn", "overlook"), ("spawn", "tor_foot"), ("tor_foot", "furnace"),
             ("hollow", "west_head"), ("overlook", "key_head"), ("furnace", "east_head"), ("tor_foot", "east_head"),
             ("hollow", "overlook")]
    laid = np.zeros(H.shape, bool)
    roads = []
    Hn = H.copy()
    for a, b in JOINS:
        way = R.find(Hn, X, Z, PLACES[a], PLACES[b], max_grade=0.2, cell=3, turn=3.0, bridge=None,
                     avoid=~land | seam_zone(X, Z))
        if not way:
            print("no road", a, b)
            continue
        pts = R.smooth(R.simplify(way, 1.2), 1)
        for img in (False, True):
            p = [turn(*q) for q in pts] if img else pts
            Hn, _ = L.grade(Hn, X, Z, p, width=4, max_grade=0.2, shoulder=3, keep=laid)
            roads.append((a + ("-s" if img else ""), b, p))
            laid |= R.footprint(X, Z, p, 4)
    H = Hn

    # the seam, cut after the halves are joined so it is exactly symmetric
    d = seam_d(X, Z)
    hw = 8.2 + 1.6 * sym(noise.fbm(shape, 30, 2, seed=21)) + 0.9 * sym(noise.fbm(shape, 9, 1, seed=22))
    wall = noise.smoothstep(hw + 3.2, hw - 0.6, d)                    # 1 in the seam, 0 outside the rim
    floor = FLOOR + 1.6 * sym(noise.fbm(shape, 14, 2, seed=23)) * noise.smoothstep(4.5, 9.0, d) + 0.5 * (d / 7) ** 2
    H = H * (1 - wall) + floor * wall
    seam = d < hw + 1

    # stairs up the seam's walls: one pair per ramp, climbing along the wall
    ramps = []
    for name, (xs, direc) in RAMPS:
        for img in (False, True):
            ax, az = xs, float(centre(xs)) - 2.5
            bx, bz = xs + 22, float(centre(xs + 22)) - 12.5
            if img:
                ax, az = turn(ax, az)
                bx, bz = turn(bx, bz)
            H = ramp(H, X, Z, (ax, az), (bx, bz), FLOOR, LEVEL, 3.4)
            ramps.append((name + (" (south)" if img else ""), [(ax, az), (bx, bz)]))

    H = np.where(Z < SEAM_Z, H, H[::-1, ::-1])                        # whole ground exactly its own half turn
    H = np.where(land, H, 0)
    return dict(X=X, Z=Z, H=np.round(H).astype(int), land=land, seam=seam, hw=hw, d=d, south=Z > centre(X), roads=roads, ramps=ramps,
                places=PLACES, laid=laid)


if __name__ == "__main__":
    g = ground()
    H = g["H"]
    print(H.shape, H[g["land"]].min(), H.max(), int(g["land"].sum()))
    S = H[::-1, ::-1]
    print("symmetric:", bool((np.where(g["land"], H, 0) == np.where(g["land"][::-1, ::-1], S, 0)).all()))
