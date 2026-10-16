"""Hoarfire's ground: every column's floor over the whole board, mirrored across the rift (z -> -1 - z), so Rowan's
half (z < 0) is drawn and Sloe's is its image. The numbers that decide play are here; plan.py names the places.

    the shore of the Rift at 47, the land rising to 54 at the back and to the Hearth Ridge (about 63) behind the lodge
    the Rimewall glacier in the north-west corner, a tongue falling south-east to a snout 9 over the Rime Shelf
    the Rime Shelf, level at 51: the old tarn bed the monument floats over; the Rime Tarn beside it, frozen at 49
    Kiln Hill in the east, 15 over the ground, with a ledge facing the core; the Ember Pit under the core, 5 deep
    the Thaw: a stream from the lodge's spring down the middle of the half in a dell, falling into the Rift; its
        east bank a step of three and a half over the dell
    the Hollow Way: a sunken lane from the Rift's shore to the Ember Pit, three under the ground
    the Berg and the Cinder: two islets in the Rift, each its own image
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.geom import noise, shapes
from pgmvox.geom.noise import smoothstep
from pgmvox.ground import landform as L
from pgmvox.plan.raster import Symmetry

X0, Z0 = -72, -98
NX, NZ = 144, 196                       # x -72..71, z -98..97: the board, the rift between the halves
SYM = Symmetry("mirror_z")              # z -> -1 - z: Sloe's half is Rowan's mirrored across the rift
SHORE = 47                              # the ground at the rift's edge
BACK = 54                               # the ground at the back, before the ridge
SHELF = 51                              # the Rime Shelf: level, the monument floats over it
TARN_ICE = 49                           # the Rime Tarn's ice
RIFT_Z = -13                            # Rowan's shore runs about here; the void is z -12..11 (ragged)

# Rowan's land, before the rift is cut: a ragged outline
OUTLINE = [(-68, -20), (-70, -34), (-64, -44), (-66, -56), (-71, -70), (-68, -86), (-58, -96), (-30, -97),
           (0, -95), (26, -97), (50, -96), (64, -88), (70, -72), (66, -62), (60, -52), (64, -40), (70, -30), (66, -4), (-62, -4)]

GLACIER = [(-74, -100), (-64, -88), (-54, -74), (-46, -64)]   # the Rimewall's crest line, from the corner to the snout
GLACIER_W = (17, 9)                     # its half-width at the corner and at the snout
GLACIER_RISE = (19, 9)                  # its crest over the ground at the corner and at the snout
DRIFT = [(-62, -46), (-58, -55), (-54, -60)]   # the snow drift up onto the tongue's west flank
MONUMENT = (-36, -51)                   # the monument's column (its 2x2 foot's north-west block)
SHELF_AT, SHELF_R = (-36, -50), 10
TARN_AT, TARN_R = (-50, -40), (7, 5)
KILN_HILL, KILN_R, KILN_RISE = (58, -57), 14, 15
CORE = (38, -50)                        # the core's 4x4 foot's middle
PIT_R, PIT_DEPTH = 5, 5
SPRING = (-1, -80)
THAW = [(-1, -79), (-4, -70), (1, -60), (-3, -49), (2, -38), (-2, -27), (1, -16), (1, -10)]
HOLLOW = [(22, -9), (24, -20), (27, -30), (31, -40), (34, -45)]
LODGE = (-10, -94, 10, -86)             # the lodge's footprint, x0, z0, x1, z1
LODGE_FLOOR = 56
COURT = (-12, -85, 12, -74)             # the spawn court in front of it
COURT_Y = 55
HAMLET_Y = 55
FIELD = (12, -72, 30, -58)              # the harvest field
FIELD_Y = 53
KNOLLS = [((-22, -30), 10, 7, 51), ((9, -45), 5, 6, 52), ((-58, -26), 8, 5, 53), ((52, -26), 10, 5, 54),
          ((44, -89), 9, 6, 55), ((-14, -62), 7, 4, 56), ((18, -36), 7, 4, 57)]
ISLETS = [((-34, -0.5), 7, 4.5, 49, 11), ((32, -0.5), 6.5, 4.5, 49, 12)]   # centre, rx, rz, top, seed


def grid():
    return np.meshgrid(np.arange(X0, X0 + NX), np.arange(Z0, Z0 + NZ), indexing="ij")


def fbm(cell, octaves, seed):
    return noise.fbm((NX, NZ), cell, octaves, seed=seed)


def land_mask(X, Z):
    """Rowan's land and the islets (the islets drawn whole, the halves mirrored later)."""
    Xw, Zw = noise.warp(X, Z, seed=3, big=3.0, small=1.5, big_cell=40, small_cell=10)
    red = shapes.inside(Xw, Zw, OUTLINE) & (Z < 0)
    shore = RIFT_Z + 1.2 * fbm(9, 2, 4) + 0.8 * fbm(4, 1, 5) + 4.5 * np.exp(-((X - 1) / 7.0) ** 2) \
        - 1.5 * np.exp(-((X + 34) / 9.0) ** 2) - 1.5 * np.exp(-((X - 32) / 9.0) ** 2)
    red &= Z <= shore
    isl = np.zeros(X.shape, bool)
    for (cx, cz), rx, rz, _, seed in ISLETS:
        e = shapes.ellipse_distance(X + 0.5, Z + 0.5, (cx + 0.5, cz + 0.5), rx, rz) * (1 + 0.18 * fbm(5, 2, seed))
        isl |= e <= 1
    return red, isl


def glacier_rise(X, Z):
    """The Rimewall: a dome along its crest line, high at the corner, a snout cliff at the end."""
    d, s = shapes.polyline(X, Z, GLACIER)
    t = np.clip(s / shapes.length(GLACIER), 0, 1)
    half = GLACIER_W[0] + (GLACIER_W[1] - GLACIER_W[0]) * t
    crest = GLACIER_RISE[0] + (GLACIER_RISE[1] - GLACIER_RISE[0]) * t
    lump = 1 + 0.12 * fbm(12, 2, 21)
    r = np.clip(d * lump / half, 0, 1)
    rise = crest * np.clip(1 - r ** 3.0, 0, 1) ** 0.45
    return rise


def ground():
    """(X, Z, H, red, islets, waters, extras): Rowan's half drawn and mirrored, the islets, the water."""
    X, Z = grid()
    red, isl = land_mask(X, Z)
    n1, n2 = fbm(30, 3, 1), fbm(9, 2, 2)
    H = SHORE + (BACK - SHORE) * smoothstep(-15, -88, Z) + 3.2 * n1 + 1.0 * n2
    # the Hearth Ridge behind the lodge, and the back rising to it everywhere
    H += 9 * smoothstep(-84, -97, Z) * (0.75 + 0.35 * fbm(18, 2, 6))
    ice = glacier_rise(X, Z)
    H += ice
    # the drift up the tongue's west flank: a ramp of snow from the tarn's ground to the tongue's shoulder
    d, s = shapes.polyline(X, Z, DRIFT)
    tlen = shapes.length(DRIFT)
    drift_top = SHELF - 1 + 9 * np.clip(s / tlen, 0, 1)
    H = np.where(d < 4, np.maximum(H, drift_top - 0.6 * smoothstep(2, 4, d) * 3), H)
    # the Rime Shelf: level ground the monument floats over
    e = shapes.ellipse_distance(*noise.warp(X, Z, seed=31, big=0, small=1.5, small_cell=8), SHELF_AT, SHELF_R, SHELF_R * 0.8)
    t = 1 - smoothstep(0.75, 1.35, e)
    H = H * (1 - t) + SHELF * t
    # Kiln Hill: a hill with a terrace facing the core
    e = shapes.ellipse_distance(*noise.warp(X, Z, seed=41, big=0, small=2.5, small_cell=9), KILN_HILL, KILN_R, KILN_R * 1.15)
    hill = KILN_RISE * (1 - smoothstep(0.15, 1.05, e)) ** 1.1
    H = H + hill
    # knolls: the Frost Knoll under the Frostwood, the Thaw Crag beside the bridge, the Rowan Knoll by the hamlet
    for (cx, cz), r, rise, seed in KNOLLS:
        e = shapes.ellipse_distance(*noise.warp(X, Z, seed=seed, big=0, small=2.0, small_cell=7), (cx, cz), r, r * 0.8)
        H = H + rise * (1 - smoothstep(0.1, 1.0, e)) ** 1.3
    # the east bank: the autumn ground stands a step over the Thaw's dell, a bank of three and a half that rock
    # shows through, eased out at both ends
    d, _, side = shapes.polyline(X, Z, THAW, side=True)
    east = (side < 0) * smoothstep(-74, -64, Z) * smoothstep(-16, -24, Z)
    H = H + 3.5 * east * smoothstep(6.5, 9.5, d + 1.2 * fbm(6, 2, 77))
    # the court, the lodge's terrace, the hamlet's yard and the field: level ground somebody made
    for (x0, z0, x1, z1), y, m in ((LODGE, LODGE_FLOOR, 3), (COURT, COURT_Y, 4), ((20, -86, 50, -72), HAMLET_Y, 5),
                                   (FIELD, FIELD_Y, 4)):
        dx = np.maximum(np.maximum(x0 - X, X - x1), 0)
        dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
        dd = np.hypot(dx, dz)
        t = 1 - smoothstep(0, m, dd)
        H = H * (1 - t) + y * t
    # the Thaw's dell: the ground eased down toward the stream
    d, _ = shapes.polyline(X, Z, THAW)
    H -= 2.5 * (1 - smoothstep(2, 9, d))
    # the Hollow Way: a lane cut three under the ground, banks easing back
    d, s = shapes.polyline(X, Z, HOLLOW)
    hollow_floor = SHORE - 2 + 2 * np.clip(s / shapes.length(HOLLOW), 0, 1)
    H = np.where(d < 2.2, np.minimum(H, hollow_floor), np.where(d < 5, np.minimum(H, hollow_floor + (d - 2.2) * 1.3), H))
    H = H.copy()
    # the Ember Pit under the core: a round pit, stepped
    pd = np.hypot(X - CORE[0] + 0.5, Z - CORE[1] + 0.5)
    ground_at_core = float(H[CORE[0] - X0, CORE[1] - Z0])
    pit = np.where(pd <= PIT_R - 1.5, ground_at_core - PIT_DEPTH,
                   np.where(pd <= PIT_R, ground_at_core - PIT_DEPTH + (pd - (PIT_R - 1.5)) * 2.4, np.inf))
    H = np.minimum(H, pit)
    # the stream and the tarn
    waters = []
    H, thaw = L.watercourse(H, X, Z, THAW, width=3, depth=2, water=1, bank=3, fall_min=2, reach_min=8)
    waters.append(thaw)
    H, tarn = L.lake(H, X, Z, TARN_AT, TARN_R[0], TARN_ICE, depth=2, shore=3, rz=TARN_R[1], jag=0.2, seed=8)
    waters.append(tarn)
    H, spring = L.lake(H, X, Z, SPRING, 3, COURT_Y - 1, depth=2, shore=1, rz=2.5, jag=0.0, seed=9)
    waters.append(spring)
    H = L.hold(H, *waters)
    # the islets: their own heights, drawn whole
    for (cx, cz), rx, rz, top, seed in ISLETS:
        e = shapes.ellipse_distance(X + 0.5, Z + 0.5, (cx + 0.5, cz + 0.5), rx, rz) * (1 + 0.18 * fbm(5, 2, seed))
        H = np.where(e <= 1, top + 2.5 * np.clip(1 - e, 0, 1) ** 0.7 + 0.8 * fbm(4, 1, seed + 1), H)
    keep = Z < 0
    H = SYM.field(H, keep=keep)
    land = SYM.field(red, keep=keep) | isl
    waters = [L.Water(SYM.field(w.mask, keep=keep), SYM.field(w.surface, keep=keep), w.falls) for w in waters]
    ice = SYM.field(ice, keep=keep)
    H = np.where(land, np.round(H), 0).astype(int)
    for w in waters:
        w.mask &= land
    return dict(X=X, Z=Z, H=H, land=land, islets=isl, waters=waters, ice=ice, thaw=waters[0], tarn=waters[1],
                spring=waters[2])
