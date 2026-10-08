"""Whitecliff Cistern: a king-of-the-hill board in a whitewashed cliff town on a sea stack. Three hills on the town's
own axis: the Cistern, a vault under a sunken court in the middle, worth two a second; the Garden in a walled terrace
at the north end, and the Boatyard in a dry dock at the south end, worth one each, and pushed out to 0.8 of the way
from the middle to a spawn. A hill is never raised over the ground round it: the Cistern is eight under, the Boatyard
four under, the Garden two over and walled. Nothing in the town looks down a gate into a spawn.

I chose king of the hill for the fifth board because the author's law for a capture board (match-flow section 10) is
a different law from the four destroy and deathmatch boards: the ground is built, a point is entered from a decided
number of ways, cover is placed, and the centre pays double. This board is made to those sentences.

Red holds the west (x < 0). Blue is red's mirror across the town's axis, x' = -1 - x: pgmvox's Symmetry("mirror_x").
The north and south halves are not each other's image: the Garden and the Boatyard are different places.
H is the y of the floor block; a player stands at H + 1.

    build()       the plan Raster: ground storey (streets, plazas, court, garden, dock, blocks), storey 1 the vault
                  and its tunnels, storey 2 the roofs
    objectives()  teams, spawns, the three hills
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.objectives import Box, Hill, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

BOARD = "whitecliff-cistern"
X_MIN, X_MAX = -60, 59
Z_MIN, Z_MAX = -50, 49
SYM = Symmetry("mirror_x")
TOWN = 70
QUAY = 68
COURT = 62
VAULT = 56
GARDEN = 72
DOCK = 66
ROOF = 74
KILL_Y = 30
MAX_BUILD = 112

SPAWN_AT = (-52, 69, 0)
SPAWN_AREA = Box(-59, 0, -9, -47, 127, 8)

HILLS = [
    ("cistern", "The Cistern", Box(-3, VAULT, -3, 2, VAULT, 2), 2),
    ("garden", "The Garden", Box(-3, GARDEN, -45, 2, GARDEN, -40), 1),
    ("boatyard", "The Boatyard", Box(-3, DOCK, 40, 2, DOCK, 45), 1),
]

KINDS = ["void", "yard", "street", "plaza", "quay", "wall", "gate", "house", "ring", "court", "garden", "dock",
         "hill", "stair", "vault", "tunnel", "roof", "cover", "slot"]
COLOURS = {"void": (24, 40, 70), "yard": (230, 220, 200), "street": (214, 200, 176), "plaza": (236, 228, 212),
           "quay": (160, 190, 210), "wall": (120, 120, 120), "gate": (240, 230, 150), "house": (250, 250, 250),
           "ring": (200, 190, 170), "court": (150, 180, 200), "garden": (120, 180, 110), "dock": (120, 160, 190),
           "hill": (255, 215, 60), "stair": (180, 170, 150), "vault": (90, 100, 130), "tunnel": (80, 90, 120),
           "roof": (200, 100, 70), "cover": (140, 140, 120), "slot": (40, 40, 60)}
WALK = {"yard", "street", "plaza", "quay", "gate", "ring", "court", "garden", "dock", "hill", "stair", "vault",
        "tunnel", "roof"}

PLACES = [("the West Quay", (-52, 0)), ("Harbour Street", (-43, -20)), ("the Middle Way", (-30, 0)),
          ("Almond Lane", (-24, 10)), ("North Street", (-30, -24)), ("South Street", (-30, 21)),
          ("Sailmakers' Row", (-33, -13)), ("Net Lofts", (-33, 11)), ("the Cistern Court", (0, 0)),
          ("the Cistern", (0, 0)), ("the Oculus", (0, 8)), ("North Plaza", (0, -25)), ("the Garden", (0, -41)),
          ("South Plaza", (0, 24)), ("the Boatyard", (0, 41)), ("the Undercroft", (-17, 0)),
          ("the Cellar Stair", (-34, 0)), ("the Rooftop Walk", (-33, -13)), ("Wharf Terrace", (-53, -42)),
          ("Wharf Terrace", (-53, 42))]

# ---- red's pieces -----------------------------------------------------------------------------------------
BLOCKS = [("A1", (-40, -22, -27, -4)), ("A2", (-40, 3, -27, 19)), ("A3", (-40, -36, -27, -28)),
          ("A4", (-40, 24, -27, 37)), ("B1", (-21, -22, -17, -4)), ("B2", (-21, 3, -17, 19)),
          ("W1", (-58, -34, -47, -15)), ("W2", (-58, 14, -47, 33)), ("W3", (-58, -48, -47, -36)), ("W4", (-58, 36, -47, 47)), ("B3", (-21, -38, -17, -28)), ("N1", (-46, -48, -27, -37)), ("N2", (-21, -48, -15, -42)),
          ("S1", (-46, 42, -14, 47)), ("S2", (-46, 36, -27, 41)),
          ("B4", (-21, 24, -17, 37))]
STREETS = [(-45, -36, -41, 41), (-40, -2, -17, 1), (-40, -26, -17, -23), (-40, 20, -17, 23), (-26, -42, -22, 41),
           (-58, -14, -46, -12), (-58, 11, -46, 13)]
FLIGHTS = [
    ((-54, -10), "n", (0, 3), 69, 2), ((-51, 9), "s", (0, 3), 69, 2), ((-46, -2), "e", (0, 3), 69, 2),     # the quay's three ways out
    ((-9, 1), "w", (0, 3), 63, 8), ((-2, -9), "n", (0, 3), 63, 8), ((1, 8), "s", (0, 3), 63, 8),         # the court's stairs
    ((-2, -32), "n", (0, 3), 71, 2), ((-16, -41), "e", (0, 2), 71, 2),                                      # the garden's steps and gate stair
    ((-2, 35), "n", (0, 3), 67, 4), ((-14, 41), "w", (0, 3), 67, 4),                                        # the dock's stair and ramp
    ((-26, -11), "w", (0, 2), 71, 4), ((-26, 12), "w", (0, 2), 71, 4),                                      # up to the two roofs
]
COVER = [
    dict(kind="baffle", rect=(-50, -4, -49, 3), h=5), dict(kind="baffle", rect=(-55, -7, -50, -7), h=5),
    dict(kind="baffle", rect=(-55, 6, -50, 6), h=5),
    dict(kind="planter", rect=(-9, -9, -7, -7), h=2), dict(kind="planter", rect=(6, -9, 8, -7), h=2),
    dict(kind="planter", rect=(-9, 6, -7, 8), h=2), dict(kind="planter", rect=(6, 6, 8, 8), h=2),
    dict(kind="column", rect=(-11, -4, -11, -4), h=4), dict(kind="column", rect=(10, -4, 10, -4), h=4),
    dict(kind="column", rect=(-11, 4, -11, 4), h=4), dict(kind="column", rect=(10, 4, 10, 4), h=4),
    dict(kind="fountain", rect=(-2, -27, 1, -24), h=1), dict(kind="stall", rect=(-12, -19, -10, -17), h=3),
    dict(kind="stall", rect=(9, -19, 11, -17), h=3), dict(kind="stall", rect=(-12, 27, -10, 29), h=3),
    dict(kind="stall", rect=(9, 27, 11, 29), h=3), dict(kind="planter", rect=(-6, -30, -4, -28), h=2),
    dict(kind="planter", rect=(3, -30, 5, -28), h=2), dict(kind="planter", rect=(-6, 20, -4, 22), h=2),
    dict(kind="planter", rect=(3, 20, 5, 22), h=2),
    # the garden's own: a fountain, hedges that make a bay of the pad
    dict(kind="fountain", rect=(-2, -38, 1, -36), h=1), dict(kind="hedge", rect=(-9, -45, -6, -45), h=2),
    dict(kind="hedge", rect=(5, -45, 8, -45), h=2), dict(kind="hedge", rect=(-10, -41, -10, -38), h=2),
    dict(kind="hedge", rect=(9, -41, 9, -38), h=2),
    dict(kind="hedge", rect=(-12, -44, -9, -44), h=2), dict(kind="hedge", rect=(8, -44, 11, -44), h=2),
    dict(kind="hedge", rect=(-8, -36, -5, -36), h=2), dict(kind="hedge", rect=(4, -36, 7, -36), h=2),
    dict(kind="hedge", rect=(-12, -40, -12, -37), h=2), dict(kind="hedge", rect=(11, -40, 11, -37), h=2),
    # the dock: moored boats' hulls and a crane's foot
    dict(kind="hull", rect=(-10, 38, -7, 41), h=2), dict(kind="hull", rect=(6, 38, 9, 41), h=2),
    dict(kind="crate", rect=(-8, 45, -7, 46), h=2),
    dict(kind="hull", rect=(-12, 43, -9, 46), h=2), dict(kind="hull", rect=(8, 43, 11, 46), h=2),
    dict(kind="crate", rect=(-5, 37, -4, 38), h=2), dict(kind="crate", rect=(3, 37, 4, 38), h=2),
    dict(kind="crate", rect=(-12, 36, -11, 37), h=2), dict(kind="crate", rect=(6, 45, 7, 46), h=2),
    dict(kind="column", rect=(-5, 43, -5, 43), h=4), dict(kind="column", rect=(4, 43, 4, 43), h=4),
    # the vault: four piers, two low walls
    dict(kind="pier", rect=(-6, -6, -5, -5), h=4), dict(kind="pier", rect=(4, -6, 5, -5), h=4),
    dict(kind="pier", rect=(-6, 4, -5, 5), h=4), dict(kind="pier", rect=(4, 4, 5, 5), h=4),
    dict(kind="lowwall", rect=(-8, -1, -8, 0), h=2),
    # the wharf terraces and the almond squares: planters and crates to break the lines
    dict(kind="crate", rect=(-44, -30, -43, -29), h=2), dict(kind="crate", rect=(-44, 30, -43, 31), h=2),
    dict(kind="crate", rect=(-36, -3, -35, -3), h=2), dict(kind="crate", rect=(-36, 2, -35, 2), h=2),
    dict(kind="crate", rect=(-33, -25, -32, -24), h=2), dict(kind="crate", rect=(-33, 21, -32, 22), h=2),
    dict(kind="planter", rect=(-21, -34, -19, -32), h=2), dict(kind="planter", rect=(-21, 30, -19, 32), h=2),
]
# chicanes down the long streets, so no street is a shooting gallery: a barricade three wide across one side of a
# street, the next across the other, a gap of two between, clear of the junctions
JUNCTION_Z = (-24.5, -13, -0.5, 12, 21.5, -40, 39.5)
JUNCTION_X = (-43, -24)
for _k, _z in enumerate(range(-34, 36, 9)):
    if all(abs(_z - j) > 4 for j in JUNCTION_Z):
        COVER.append(dict(kind="barricade", rect=((-45, _z, -43, _z) if _k % 2 else (-43, _z, -41, _z)), h=3))
for _k, _z in enumerate(range(-40, 42, 9)):
    if all(abs(_z - j) > 4 for j in JUNCTION_Z):
        COVER.append(dict(kind="barricade", rect=((-26, _z, -24, _z) if _k % 2 else (-24, _z, -22, _z)), h=3))
for _k, _x in enumerate(range(-38, -18, 6)):
    if all(abs(_x - j) > 4 for j in JUNCTION_X):
        COVER.append(dict(kind="barricade", rect=((_x, -26, _x, -25) if _k % 2 else (_x, -24, _x, -23)), h=3))
        COVER.append(dict(kind="barricade", rect=((_x, 20, _x, 21) if _k % 2 else (_x, 22, _x, 23)), h=3))
for _k, _x in enumerate(range(-38, -18, 7)):
    if all(abs(_x - j) > 4 for j in JUNCTION_X):
        COVER.append(dict(kind="barricade", rect=((_x, -2, _x, -1) if _k % 2 else (_x, 0, _x, 1)), h=3))
HOLES = [(-2, -2, 1, 1)]                          # the oculus, in the court's floor
SLOTS = [(-7, -8, -6, -4), (-7, 4, -6, 7)]        # the stairwells' openings in the court floor (red's; images by the mirror)
CELLAR = (-39, -1, -27, 0)                         # the cellar stair's slot in the Middle Way's floor, red's


@lru_cache(maxsize=1)
def build():
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    plate = lambda x0, z0, x1, z1: R.rect(x0, x1, z0, z1, TOWN, "yard")                              # noqa: E731
    R.rect(-58, 57, -48, 47, TOWN, "yard")                         # the stack's top: chamfered by the generator's outline
    for key, (x0, z0, x1, z1) in BLOCKS:
        R.rect(x0, x1, z0, z1, TOWN, "house")
    for x0, z0, x1, z1 in STREETS:
        R.rect(x0, x1, z0, z1, TOWN, "street")
    # the quay: lowered, walled, three gates
    R.rect(-58, -47, -9, 8, QUAY, "quay")
    for x in range(-58, -46):
        for z in range(-9, 9):
            if x in (-58, -47) or z in (-9, 8):
                R.cell(x, z, QUAY, "wall")
    for x0, z0, x1, z1 in ((-54, -9, -51, -9), (-54, 8, -51, 8), (-47, -2, -47, 1)):
        R.rect(x0, x1, z0, z1, QUAY, "gate")
    # the ring, the court, the plazas, the garden, the dock
    R.rect(-16, 15, -16, 15, TOWN, "ring")
    R.rect(-12, 11, -12, 11, COURT, "court")
    R.rect(-16, 15, -31, -17, TOWN, "plaza")
    R.rect(-16, 15, 16, 31, TOWN, "plaza")
    R.rect(-14, 13, -47, -34, GARDEN, "garden")
    for x in range(-14, 14):
        for z in range(-47, -33):
            if x in (-14, 13) or z in (-47, -34):
                R.cell(x, z, GARDEN, "wall")
    for x0, z0, x1, z1 in ((-14, -41, -14, -39), (-2, -34, 1, -34)):
        R.rect(x0, x1, z0, z1, GARDEN, "gate")
    R.rect(-14, 13, -33, -32, TOWN, "wall")
    R.rect(-13, 12, 36, 47, DOCK, "dock")
    R.rect(-13, 12, 32, 35, TOWN, "wall")
    R.rect(-21, -18, 38, 41, TOWN, "street")
    R.rect(-21, -17, -41, -39, TOWN, "street")                     # the garden walk
    for x0, z0, x1, z1 in ((-21, -41, -15, -39),):
        R.rect(x0, x1, z0, z1, TOWN, "street")
    for key, name, box, pts in HILLS[1:]:
        R.rect(box.x0, box.x1, box.z0, box.z1, box.y0, "hill", both=False)
    # flights
    for start, rises, width, h0, n in FLIGHTS:
        R.flight(start, rises, width, h0, n)
    # the oculus and the slots are holes in the court's floor; the cellar's slot a hole in the Middle Way's
    for x0, z0, x1, z1 in HOLES + SLOTS:
        R.rect(x0, x1, z0, z1, 0, "void")
    x0, z0, x1, z1 = CELLAR
    R.rect(x0, x1, z0, z1, 0, "void")
    # the cover
    for c in COVER:
        x0, z0, x1, z1 = c["rect"]
        base = R.h(x0, z0)
        R.rect(x0, x1, z0, z1, base + c["h"], "cover")
    # storey 1: the vault, its pad, the stairwells' flights, the undercroft and the cellar's stair
    U = R.storey(1)
    U.rect(-8, 7, -8, 7, VAULT, "vault")
    for key, name, box, pts in HILLS[:1]:
        U.rect(box.x0, box.x1, box.z0, box.z1, VAULT, "hill", both=False)
    U.flight((-7, -4), "n", width=(0, 1), h0=VAULT + 1, n=6)
    U.flight((-6, 3), "s", width=(0, 1), h0=VAULT + 1, n=6)
    U.rect(-26, -9, -2, 1, VAULT, "tunnel")
    U.flight((-27, 0), "w", width=(0, 1), h0=VAULT + 1, n=14)
    for c in COVER:
        if c["kind"] in ("pier", "lowwall"):
            x0, z0, x1, z1 = c["rect"]
            U.rect(x0, x1, z0, z1, VAULT + c["h"], "cover")
    # storey 2: the roofs and the walk across the Middle Way
    V = R.storey(2)
    V.rect(-40, -30, -22, -4, ROOF, "roof")
    V.rect(-40, -30, 3, 19, ROOF, "roof")
    V.rect(-35, -33, -3, 2, ROOF, "roof")
    return R


def zone_mask(R, keys=None):
    return np.zeros(R.H.shape, bool)


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=270, kit="spawn-kit", area=SPAWN_AREA))
    for key, name, box, points in HILLS:
        O.add(Hill(key, name, box, capture_height=5, points=points, capture_time="5s"), mirror=False)
    O.add(Observer((0, 100, 0), yaw=90), mirror=False)
    return O
