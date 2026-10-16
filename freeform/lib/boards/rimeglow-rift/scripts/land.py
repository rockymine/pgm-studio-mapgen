"""The ground of Rimeglow Rift: one heightfield, a lava rift across its middle, a half turn between the teams.

Everything is stated for the north (Rime) half and carried onto the south (Ember) half by the half turn
(x, z) -> (-1 - x, -1 - z), so the field is symmetric by construction. Coordinates u = x + 0.5, v = z + 0.5 turn
as (u, v) -> (-u, -v).
"""
import os
import sys

import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..")))
from pgmvox.geom import noise  # noqa: E402
from pgmvox.geom.shapes import inside, polyline  # noqa: E402

X0, Z0, SX, SZ = -70, -100, 140, 200
SY = 112
RIM = 57                    # the shelf either side of the rift
FLOOR = 35                  # the rift's solid floor
LAVA = 38                   # the lava surface
KILL_Y = 6
DECK_Y = 59
FLOW = [(-26, -92), (-31, -80), (-24, -68), (-17, -60), (-12, -54)]     # glacier / cooled lava flow into the mere
FLOW_W = 6.0
SHELF_Y = 41                 # the ledge along the lava, three above it
SHELF_W = 3.6                # and its width
SHELF_X = 52                 # and how far along the rift it runs


def LD_sstep(Z, near, far):
    """1 at and beyond `far`, 0 at `near` (z falls to the north)."""
    return sstep(near, far, Z)


def grid():
    return np.meshgrid(np.arange(X0, X0 + SX), np.arange(Z0, Z0 + SZ), indexing="ij")


def turned(a):
    """The half turn of a world-grid array."""
    return a[::-1, ::-1]


def sym(a):
    return (a + turned(a)) / 2.0


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# ---- the rift's centre line and half width, both stated in u so the half turn maps them onto themselves -----------
def centre(U):
    return 4.5 * np.sin(2 * np.pi * U / 76.0)            # odd in u, so the rift maps onto itself


def half_width(U):
    return 5.5 - 1.5 * np.cos(2 * np.pi * U / 76.0)      # 4 at the middle, 7 at u = +-38


def mound(X, Z, at, rx, rz, rise, angle=0.0, power=1.5):
    a = np.radians(angle)
    dx, dz = X - at[0], Z - at[1]
    px, pz = dx * np.cos(a) + dz * np.sin(a), -dx * np.sin(a) + dz * np.cos(a)
    e2 = (px / rx) ** 2 + (pz / rz) ** 2
    return rise * np.clip(1 - e2, 0, 1) ** power


def rect_d(X, Z, cx, cz, hx, hz):
    """Distance outside a rectangle (0 inside)."""
    return np.hypot(np.maximum(np.abs(X - cx) - hx, 0), np.maximum(np.abs(Z - cz) - hz, 0))


def pad(H, X, Z, cx, cz, hx, hz, level, edge=7, both=True):
    """Level a rectangle to `level`, eased into the ground over `edge` blocks; carried onto the south as well."""
    for (px, pz) in ([(cx, cz), (-1 - cx, -1 - cz)] if both else [(cx, cz)]):
        d = rect_d(X, Z, px, pz, hx, hz)
        t = 1 - sstep(0, edge, d)
        H = H * (1 - t) + level * t
    return H


# ---- the places (north half; south are their half turns) -------------------------------------------------------
SPAWN = (13, -78)           # Rime Hall
SPAWN_PAD = (13, -76, 15, 13, 71)          # cx, cz, hx, hz, level
CAMP = (-40, -60)            # the woodcutters' pad on the ridge's foot; Amberwood's is its half turn
CORE_AT = (46, -48)          # the core's centre column
CORE_PAD = (46, -48, 9, 9, 73)
LAKE = dict(at=(-8, -42), rx=26, rz=13, level=53)           # Frostmere / the Cinder Mere
GATE = dict(west=-38, centre=0, east=38)                    # the three crossings, by u

def ledges(e, levels, soft=0.05):
    out = np.zeros(e.shape)
    for r, h in levels:
        out += h * (1 - sstep(r - soft, r + soft, e))
    return out


def warped(X, Z, seed, big=7.0, small=2.5):
    Xw, Zw = noise.warp(X, Z, seed=seed, big=big, small=small, big_cell=40, small_cell=14)
    return Xw, Zw


def spine(X, Z, pts, half, rise, power=1.3, seed=0, rough=0.0):
    """A ridge along a polyline: `rise` on its crest, falling to nothing `half` blocks out."""
    d, _ = polyline(X, Z, pts)
    if rough:
        d = d + rough * noise.fbm(X.shape, 9, 2, seed=seed)
    return rise * np.clip(1 - d / half, 0, 1) ** power


BAYS = [[(-52, -22), (-68, -26), (-70, -40), (-58, -42)],         # the west flank bitten twice
        [(-50, -84), (-64, -80), (-66, -66), (-54, -60)],
        [(64, -22), (72, -26), (72, -38), (66, -34)],             # the east, past the butte
        [(62, -76), (72, -84), (62, -98), (50, -92)],
        [(-48, -98), (-32, -100), (-36, -90), (-50, -86)],        # a notch in the back, west of the highland
        [(30, -100), (46, -100), (44, -94), (32, -92)],           # and one east of the hall
        [(-40, -26), (-52, -30), (-46, -38), (-36, -33)]]         # a cove below the west ridge


def land_mask(X, Z):
    Xw, Zw = noise.warp(X, Z, seed=61, big=7.0, small=2.5, big_cell=46, small_cell=12)
    e = np.hypot(Xw / 60.0, (Zw + 49.0) / 43.0)
    n = e <= 1.0
    for bay in BAYS:
        n &= ~inside(Xw, Zw, bay)
    rift = (np.abs(Z + 0.5 - centre(X + 0.5)) < half_width(X + 0.5) + 12) & (np.abs(Xw + 0.5) < 62)
    m = n | rift
    return m | turned(m)


def lake_e(X, Z):
    """How far out every column lies in the north mere's own radii: 1 on its rim."""
    Xw, Zw = warped(X, Z, 21, big=9.0)
    return np.hypot((Xw - LAKE["at"][0]) / LAKE["rx"], (Zw - LAKE["at"][1]) / LAKE["rz"])


def flow_mask(X, Z):
    """The glacier's tongue and the cooled lava's: a ragged band along FLOW and its half turn."""
    d, _ = polyline(X, Z, FLOW)
    width = FLOW_W * (1 + 0.35 * noise.fbm(X.shape, 12, 2, seed=73))
    m = (d < width * 0.85) & (Z < -8)
    return m | turned(m)


def mere_mask(X, Z):
    """The flat floor of both meres: the north one and its half turn."""
    m = (lake_e(X, Z) < 0.9) & (Z < -8)
    return m | turned(m)


def ground():
    X, Z = grid()
    U, V = X + 0.5, Z + 0.5
    wob = sym(noise.fbm(X.shape, 26, 3, seed=11)) * 2.0
    lumps = sym(noise.fbm(X.shape, 8, 2, seed=12)) * 0.7
    H = np.full(X.shape, float(RIM)) + wob + lumps

    N = np.zeros(X.shape)
    Xw, Zw = warped(X, Z, 21, big=9.0)
    # the highland behind the spawn: a rising shelf, its front a scarp, its back broken into crags
    shelf = LD_sstep(Zw, -58, -70)
    crags = np.clip(np.clip(1 - np.abs(noise.fbm(X.shape, 22, 3, seed=24)), 0, 1) * 1.2 - 0.3, 0, 1)
    N += 13 * shelf + 12 * crags * LD_sstep(Zw, -66, -84)
    # Rimewatch: a butte for the core, cliffed all round, two ways up
    e = np.hypot((Xw - 46) / 16.0, (Zw + 48) / 14.0)
    N += 16 * (1 - sstep(0.78, 1.0, e)) + 6 * np.clip(1.7 - e, 0, 1) ** 1.5
    # the east ridge, a wooded spine from the crags down toward the gate
    N += spine(X, Z, [(-50, -88), (-52, -68), (-47, -48), (-43, -34)], 20, 14, power=1.6, seed=25, rough=3.0)
    # moraine ridges rolling across the plain, and the crevasses between some of them
    r1 = np.clip(1 - np.abs(noise.fbm(X.shape, 30, 3, seed=71)), 0, 1) ** 1.2
    r2 = np.clip(1 - np.abs(noise.fbm(X.shape, 18, 2, seed=72)), 0, 1)
    far = sstep(-14, -32, Z)
    N += 8 * np.clip((r1 - 0.70) / 0.30, 0, 1) ** 1.5 * far
    N -= 3 * np.clip((r2 - 0.93) / 0.07, 0, 1) * far
    # a flow from the highland into the mere: the glacier's tongue in the north, the cooled lava's in the south
    d_flow, _ = polyline(X, Z, FLOW)
    width = FLOW_W * (1 + 0.35 * noise.fbm(X.shape, 12, 2, seed=73))
    N -= 2.2 * np.clip(1 - d_flow / width, 0, 1) ** 0.6
    # knolls either side of the gate
    N += mound(X, Z, (22, -26), 11, 7, 7)
    N += mound(X, Z, (-22, -27), 9, 6, 6)
    H = H + N + turned(N)
    H = ndimage.gaussian_filter(H, 0.7, mode='nearest')

    lk = LAKE
    e = lake_e(X, Z)
    tn = 1 - sstep(0.9, 1.4, e)
    tn = np.where(Z < -8, tn, 0)
    t = np.clip(tn + turned(tn), 0, 1)
    H = H * (1 - t) + lk["level"] * t

    camp_level = round(float(H[CAMP[0] - X0, CAMP[1] - Z0]))
    H = pad(H, X, Z, CAMP[0], CAMP[1], 8, 6, camp_level, edge=8)
    H = pad(H, X, Z, *SPAWN_PAD)
    H = pad(H, X, Z, *CORE_PAD)
    for u in (GATE["west"], GATE["centre"], GATE["east"]):
        for s in (-1, 1):
            cx = u if s == -1 else -1 - u
            cz = -22 if s == -1 else 21
            H = pad(H, X, Z, cx, cz, 10, 6, DECK_Y, edge=6, both=False)

    cd = np.abs(V - centre(U)) - half_width(U)
    wall = FLOOR + np.maximum(cd, 0) * 2.6
    shelf = (cd >= 0) & (cd < SHELF_W) & (np.abs(U) < SHELF_X)
    wall = np.where((cd >= SHELF_W) & (np.abs(U) < SHELF_X), SHELF_Y + (cd - SHELF_W) * 2.6, wall)
    wall = np.where(cd > 0, np.floor(wall / 2.0) * 2.0 + (SHELF_Y % 2), wall)
    wall = np.where(cd > 0, np.maximum(wall, LAVA + 1), wall)        # the lava's banks stand above its surface
    wall = np.where(shelf, SHELF_Y, wall)
    inrift = cd < 12
    H = np.where(inrift, np.minimum(H, np.maximum(wall, FLOOR)), H)
    return X, Z, H, cd


ROADS = {
    "hall-mere-gate": [(13, -64), (20, -56), (22, -44), (14, -32), (4, -24), (0, -21)],
    "hall-core": [(27, -72), (36, -66), (42, -57)],
    "core-east-gate": [(47, -41), (46, -34), (42, -27), (38, -21)],
    "hall-west-gate": [(-1, -72), (-14, -70), (-34, -66), (-45, -58), (-48, -44), (-42, -30), (-38, -21)],
    "mere-shore": [(4, -25), (-12, -30), (-30, -33), (-42, -31)],
    "gate-core": [(0, -21), (14, -24), (28, -28), (41, -33)],
}


def ramp_paths():
    """The two flights that take the north bank's rim down to the ledge, cut diagonally across the wall's face."""
    out = {}
    for name, (xa, xb) in (("ramp-west", (-30, -46)), ("ramp-east", (30, 46))):
        pts = []
        for x, offset in ((xa, 9.7), (xb, 2.4)):
            u = x + 0.5
            pts.append((x, round(float(centre(u) - half_width(u) - offset - 0.5), 1)))
        out[name] = pts
    return out


def graded(H, X, Z, width=4, max_grade=0.5):
    """Every road of the north half cut into the ground; returns the new field and the cells they claim."""
    from pgmvox.ground import landform as L
    from pgmvox.routes import route as R
    laid = np.zeros(H.shape, bool)
    paths = {}
    for name, pts in ROADS.items():
        pts = R.smooth(R.simplify(list(pts), 1.0), 1)
        H, _ = L.grade(H, X, Z, pts, width=width, max_grade=max_grade, shoulder=3, keep=laid)
        laid |= R.footprint(X, Z, pts, width)
        paths[name] = pts
    U, V = X + 0.5, Z + 0.5
    inrift = (np.abs(V - centre(U)) - half_width(U)) < 0.5
    for name, pts in ramp_paths().items():
        H, _ = L.grade(H, X, Z, pts, width=3, max_grade=1.0, shoulder=2, water=inrift, keep=laid)
        laid |= R.footprint(X, Z, pts, 3) & ~inrift
        paths[name] = pts
    return H, laid, paths


if __name__ == "__main__":
    X, Z, H, cd = ground()
    print(H.min(), H.max())
