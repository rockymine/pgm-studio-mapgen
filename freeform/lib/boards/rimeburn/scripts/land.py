"""Rimeburn's ground: one land drawn for the Frost half (north, z < 0) and carried onto the Ember half by the half
turn, so every height a player meets is the same on both sides; only the season differs.

    the board         x -64..63, z -96..95 (128 by 192); the seam z -16..15 is void under a build zone
    the Frost half    the Rimewall ridge behind (62 to 70), the Hold's terrace (46), the Hearth Hollow (floor 34),
                      the Rime Shelf (45), the Tarn (37), the burn between them, the Anvil crag (52), the front (36-38)
    the Thaw          the island on the symmetry centre, floor 38

Everything here is arrays over the board grid, indexed (x - X0, z - Z0); nothing touches a world.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.geom import noise  # noqa: E402
from pgmvox.geom import shapes  # noqa: E402
from pgmvox.ground import landform as L  # noqa: E402
from pgmvox.plan.raster import Symmetry  # noqa: E402

X0, X1, Z0, Z1 = -64, 63, -96, 95
SYM = Symmetry("half")
SEED = 4207

# ---- the places, Frost's (north); Ember's are their half turn ----------------------------------------------
SPAWN = (3, -78)                  # the feet of the Hold's spawn, on its terrace
TERRACE = 46                      # the Hold's terrace
HEARTH = (-35, -58)               # the core's middle (x, z)
HOLLOW_FLOOR = 34
HOLLOW_RIM = 40
SHELF = (38, -56)                 # the monument's middle
SHELF_TOP = 45
TARN = (21, -41)
TARN_LEVEL = 37
ANVIL = (-48, -40)                # the crag west of the hearth
ANVIL_TOP = 52
THAW_FLOOR = 38                   # the island in the seam
COAST = -12                       # the Frost land's front reaches no further south than this
BURN = [(-21, -87), (-21, -80), (-15, -73), (-12, -66), (-4, -62), (2, -55), (9, -52), (14, -46)]
OUTFLOW = [(29, -40), (33, -33), (36, -26), (40, -21)]
FALLS = (-21, -88)                # the Rime Falls: where the burn comes down the Rimewall into its pool
HAMLET = (47, -31)                # Rimecroft, on the east of the outflow
HAMLET_FLOOR = 38
# ramps cut into a slope, each (points from its foot to its head, foot height, head height, width): the Anvil's
# ledge path winding up its east and north faces, and the Rime Shelf's two flights
RAMPS = {
    "anvil": ([(round(ANVIL[0] + (7.5 - a / 150) * np.cos(np.radians(a)), 1),
                round(ANVIL[1] - (7.5 - a / 150) * np.sin(np.radians(a)), 1)) for a in range(-30, 241, 30)],
              39, ANVIL_TOP, 2.4),
    "shelf-west": ([(SHELF[0] - 15, SHELF[1] - 2), (SHELF[0] - 9, SHELF[1] - 3)], 41, SHELF_TOP, 3.2),
    "shelf-south": ([(SHELF[0] - 3, SHELF[1] + 14), (SHELF[0] - 2, SHELF[1] + 8)], 39, SHELF_TOP, 3.2),
}
# the front's cover: low rock knolls a player fights round, (x, z, radius, rise)
# the Vent runs under a low barrow from the coast's cliff into the Hearth Hollow: (x, the y a player's feet
# are at, z)
VENT = [(-24, 32, -22), (-25, 32, -28), (-29, 33, -37), (-33, 34, -45), (-35, 35, -52)]
KNOLLS = [(-14, -31, 5.5, 5), (3, -35, 4, 4), (-28, -30, 3.5, 4), (18, -28, 5, 4), (-45, -24, 4, 4), (10, -62, 5, 3),
          (-14, -50, 5, 3)]

# the Frost land's outline, before it is roughened
OUTLINE = [(-50, -95), (-20, -96), (20, -96), (46, -95), (60, -86), (63, -66), (60, -48), (61, -32), (56, -18),
           (48, -12), (36, -13), (28, -18), (20, -23), (8, -24), (-6, -22), (-18, -24), (-30, -20), (-38, -13),
           (-50, -12), (-58, -18), (-62, -34), (-62, -56), (-63, -76), (-58, -90)]
THAW = [(-21, -3), (-14, -8), (-3, -10), (8, -9), (17, -6), (20, 2), (13, 7), (2, 9), (-9, 8), (-18, 5)]


def grid():
    xs = np.arange(X0, X1 + 1)
    zs = np.arange(Z0, Z1 + 1)
    return np.meshgrid(xs, zs, indexing="ij")


def ix(x, z):
    return x - X0, z - Z0


def land_mask(X, Z):
    """Frost's land roughened at its edge, its image for Ember's, and the Thaw in the middle."""
    Xw, Zw = noise.warp(X, Z, seed=SEED, big=3.0, small=1.6, big_cell=40, small_cell=9)
    north = shapes.inside(Xw, Zw, OUTLINE) & (Z < 0)
    north &= Z <= COAST - 0 + 0
    thaw = shapes.inside(Xw, Zw, THAW)
    half = north | (thaw & (Z < 0))
    return SYM.field(half, keep=Z < 0).astype(bool)


def heights(X, Z):
    """The ground's height in every column (the y of its top block), and the burn's and the tarn's water."""
    shape = X.shape
    n1 = noise.fbm(shape, 22, 3, seed=SEED + 1)
    n2 = noise.fbm(shape, 9, 2, seed=SEED + 2)
    # the land falls from the back toward the front: 43 under the Rimewall, 37 at the coast
    n3 = noise.fbm(shape, 34, 2, seed=SEED + 8)
    H = 37 + 6 * noise.smoothstep(-34, -84, Z) + 1.3 * n1 + 0.5 * n2 + 2.6 * n3
    # the coast settles a block or two in its last eight blocks
    H -= 1.5 * noise.smoothstep(-26, -17, Z)
    # the Rimewall: a ridge behind the Hold, crest 60 to 70, ridged noise on its crest
    crest = 62 + 7 * noise.ridged(shape, 18, 3, seed=SEED + 3, sharpness=1.5)
    foot = noise.line(shape, "x", 20, seed=SEED + 4, amp=3, base=-85)
    H = L.ridge(H, Z, foot, 9, crest, rough=1.5 * n2)
    H -= 12 * noise.smoothstep(-91, -96.5, Z) * noise.smoothstep(-80, -88, Z)   # the crest falls away behind
    # the two flank spurs reaching forward from it: west to z -64, east to z -72
    west = shapes.ellipse_distance(X, Z, (-60, -80), 9, 22) + 0.12 * n2
    H = L.mound(H, west, 15, power=1.3)
    east = shapes.ellipse_distance(X, Z, (61, -84), 8, 17) + 0.12 * n2
    H = L.mound(H, east, 14, power=1.3)
    # the Hold's terrace, cut into the Rimewall's foot
    e = shapes.ellipse_distance(X, Z, (SPAWN[0], SPAWN[1] - 4), 16, 10) + 0.08 * n2
    H = L.level(H, e, TERRACE, inner=1.0, outer=1.55)
    # the Hearth Hollow: ground levelled to its rim, a bowl cut in it, a flight's slope out of it
    e = shapes.ellipse_distance(X, Z, HEARTH, 16, 14) + 0.06 * n2
    H = L.level(H, e, HOLLOW_RIM, inner=1.0, outer=1.5)
    d = np.hypot(X - HEARTH[0], Z - HEARTH[1]) * (1 + 0.07 * n2)
    H = L.crater(H, d, HOLLOW_FLOOR, 12, flat=6.5, slope=1.0)
    # the Anvil: a crag west of the hearth, its top a little stage to bridge from
    H = L.butte(H, X, Z, ANVIL, 5, ANVIL_TOP, cliff=1.5, talus=5, talus_height=0.35, jag=0.15, seed=SEED + 5,
                rz=4.2, angle=30)
    # the Rime Shelf: a mesa with a flat top under the monument
    H = L.butte(H, X, Z, SHELF, 10, SHELF_TOP, cliff=1.2, talus=4, talus_height=0.25, jag=0.1, seed=SEED + 6,
                rz=8, angle=-15)
    # the Tarn and the burn into it, then the outflow down to the coast
    H, tarn = L.lake(H, X, Z, TARN, 9, TARN_LEVEL, depth=3, shore=3, rz=6, jag=0.15, seed=SEED + 7)
    H, burn = L.watercourse(H, X, Z, BURN, width=3, depth=2, water=1, bank=3, fall_min=2, reach_min=6,
                            lowest=TARN_LEVEL - 1, into=tarn)
    H, out = L.watercourse(H, X, Z, OUTFLOW, width=3, depth=1, water=1, bank=3, fall_min=1, reach_min=4)
    H = L.hold(H, tarn, burn, out)
    water = tarn.mask | burn.mask | out.mask
    surface = np.where(tarn.mask, tarn.surface, np.where(burn.mask, burn.surface, out.surface))
    # Rimecroft's ground, held level for its three houses
    e = shapes.ellipse_distance(X, Z, HAMLET, 12, 9, 20) + 0.08 * n2
    H = L.level(H, e, HAMLET_FLOOR, inner=1.0, outer=1.5)
    # the barrow over the Vent, so its roof has rock over it
    d, _ = shapes.polyline(X, Z, [(x, z) for x, y, z in VENT[:-1]])
    H = np.where(d < 6, H + 3.5 * np.clip(1 - (d / 6) ** 2, 0, 1), H)
    # the knolls on the front
    for kx, kz, r, rise in KNOLLS:
        e = shapes.ellipse_distance(X, Z, (kx, kz), r, r * 0.7, 25) + 0.15 * n2
        H = L.mound(H, e, rise, power=1.2)
    # the ramps last, so nothing reshapes them
    for pts, h0, h1, width in RAMPS.values():
        H = ramp(H, X, Z, pts, h0, h1, width)
    # the Thaw: an island held level in the seam
    thaw = shapes.inside(X, Z, THAW)
    H = np.where(thaw, THAW_FLOOR + 0.6 * n2, H)
    H = np.round(H).astype(int)
    keep = Z < 0
    H = SYM.field(H, keep=keep).astype(int)
    water = SYM.field(water, keep=keep).astype(bool)
    surface = SYM.field(surface, keep=keep)
    return H, water, np.round(surface).astype(int)


def ramp(H, X, Z, pts, h0, h1, width):
    """A way cut into a slope: every cell within half `width` of the path takes the level rising evenly from `h0`
    at its first point to `h1` at its last, cut where the ground is higher and filled where it is lower."""
    d, along = shapes.polyline(X, Z, pts)
    total = shapes.length(pts)
    level = np.round(h0 + (h1 - h0) * np.clip(along / total, 0, 1))
    return np.where(d <= width / 2, level, H)


def ramp_cells(X, Z):
    """Every ramp's cells, {name: mask}, both halves."""
    out = {}
    for name, (pts, h0, h1, width) in RAMPS.items():
        d, _ = shapes.polyline(X, Z, pts)
        m = (d <= width / 2) & (Z < 0)
        out[name] = SYM.field(m, keep=Z < 0).astype(bool)
    return out


def build():
    """(X, Z, H, land, water, surface): the board's ground, ready for the plan and the generator."""
    X, Z = grid()
    land = land_mask(X, Z)
    H, water, surface = heights(X, Z)
    water &= land
    return X, Z, H, land, water, surface


if __name__ == "__main__":
    X, Z, H, land, water, surface = build()
    print("land columns", int(land.sum()), "of", land.size, " heights", H[land].min(), H[land].max())
