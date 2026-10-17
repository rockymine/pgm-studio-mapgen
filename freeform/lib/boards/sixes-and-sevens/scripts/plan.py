"""Sixes and Sevens — the plan. A frozen wasteland between two bunkers dug into the mountains at either end of a long
board: bunker 06 in the west for Red, bunker 07 in the east for Blue, each the half turn of the other. The snowfield
runs the whole width of the board between them, and goes on over the mountains above the bunkers, where nobody
plays and the ground is pushed further: deeper drifts, more rock, a tall needle over each bunker.

    floors: 40 the snowfield, the bunker's ground floor and the yard; 48 the bunker's upper floor; 47 the high
    shelf; 34 the cut; the crevasses holes with lava at their foot; the mountain over 70

Each team defends two monuments: the Reactor, floating in the tall hall behind the bunker's door, and the Pump, in
the yard cut into the cliff beside the facade. The spawn hall lies deep in the mountain behind both.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan.raster import Raster, Symmetry  # noqa: E402

SYM = Symmetry("half")
WORLD = (-150, -110, 300, 220)          # x0, z0, sx, sz
X = (-140, 139)                         # the play area
Z = (-100, 99)
FIELD = 40
UPPER = 49
FRONT_H = 32                            # the facade, four segments high
SHELF = 47
CUT = 34
LAVA = 22                               # the lava's surface at a crevasse's foot
KINDS = ["field", "path", "mountain", "hall", "dark", "yard", "shelf", "stair", "rock", "crevasse", "cut", "door"]
COLOURS = {"field": (226, 232, 238), "path": (150, 128, 104), "mountain": (92, 96, 104), "hall": (196, 188, 170),
           "dark": (70, 66, 72), "yard": (206, 210, 200), "shelf": (176, 196, 214), "stair": (160, 170, 190),
           "rock": (120, 120, 124), "crevasse": (200, 70, 30), "cut": (150, 170, 190), "door": (230, 200, 90)}
WALK = {"field", "path", "hall", "dark", "yard", "shelf", "stair", "cut", "door"}
WALLS = {"mountain", "rock"}

# ---- Red's bunker, west of the facade; Blue's is its half turn ------------------------------------------------
FACADE_X = -46                          # the face column; the field starts a block east of it
FACADE_Z = (-13, 31)
DOOR_Z = (0, 17)
HALL = (-71, -48, -6, 23)               # x0, x1, z0, z1: the tall hall, three segments high
SPAWN_HALL = (-104, -84, 16, 37)
TUNNEL = (-81, -74, 18, 23)             # spawn hall to the tall hall
YARD_TUNNEL = (-81, -69, 34, 39)        # spawn hall to the yard
YARD = (-66, -47, 34, 57)               # cut into the cliff south of the facade, open to the field
DARK = (-108, -91, -14, 3)              # the generator room
DARK_TUNNEL = (-99, -94, 6, 13)         # dark room to the spawn hall
SIDE_TUNNEL = (-88, -74, -6, -1)        # dark room to the tall hall's back corner
# the upper floor, one segment up: a gallery round the tall hall's back and south side, a corridor over the spawn
# tunnel to the spawn hall, and a switchback stair down in the spawn hall
GALLERY = [(-71, -66, -6, 23), (-71, -48, 18, 23)]
UPPER_CORRIDOR = (-81, -74, 18, 23)
STAIR_FLIGHTS = [((-87, 16), "w", 4), ((-98, 19), "e", 5)]    # (x, z) of its first tread, the way it climbs, rises;
STAIR_WIDTH, TREAD = 3, 3                                     # each tread 3 deep, a landing between the flights
STAIR_TOP = (-86, -84, 16, 21)                                # the upper landing, at 49, into the corridor

# where a tunnel passes a room's wall: the carved box, and the face lines it opens in (side, line)
MOUTHS = [((-83, 18, -82, 23), [("w", -83), ("e", -82)]), ((-73, 18, -72, 23), [("e", -72), ("w", -73)]),
          ((-83, 34, -82, 39), [("w", -83), ("e", -82)]), ((-68, 34, -67, 39), [("e", -67), ("w", -68)]),
          ((-99, 4, -94, 5), [("s", 4), ("n", 5)]), ((-99, 14, -94, 15), [("s", 14), ("n", 15)]),
          ((-90, -6, -89, -1), [("w", -90), ("e", -89)]), ((-73, -6, -72, -1), [("e", -72), ("w", -73)])]

SPAWN = (-91, 27)
REACTOR = (-60, 1)
PUMP = (-51, 43)

# ---- the mountain: its front, north to south, the field east of it ----------------------------------------------
FRONT = [(-84, -110), (-74, -90), (-60, -76), (-40, -64), (-27, -51), (-26, -37), (-35, -21), (-46, -14),
         (-46, 30), (-46, 56), (-46, 59), (-32, 62), (-32, 86), (-48, 92), (-62, 98), (-70, 110)]
SHELF_POLY = [(-31, 64), (-5, 66), (-5, 86), (-31, 86)]        # wholly in Red's half, so the half turn keeps it
SHELF_RAMP = (-4, -1, 57, 6)            # x0, x1, the first tread's z, treads: 3 deep each, climbing south, at its east end

# the lofted walls: chains of (bottom, top) edges, each facing (-dz, dx) of the chain's direction
LOFTS = {
    "north spur": [((-46, FIELD, -14), (-50, 72, -18)), ((-36, FIELD, -21), (-40, 64, -24)),
                   ((-27, FIELD, -37), (-31, 56, -38)), ((-28, FIELD, -51), (-32, 50, -49)),
                   ((-40, FIELD, -64), (-42, 46, -60))],
    "shelf": [((-5, FIELD, 63), (-5, SHELF, 66)), ((-32, FIELD, 61), (-32, 50, 64)),        # one retaining wall from
              ((-46, FIELD, 58), (-46, 72, 61))],                                         # the shelf to the yard
}
BOULDERS = [(-36, -30, 3), (-14, -18, 2), (-33, 28, 3), (-18, 48, 2), (-40, 70, 2), (-22, -70, 3), (-8, -60, 2),
            (-30, -86, 2), (-12, 92, 2), (-38, 92, 3)]                      # (x, z, radius) on the field

# ---- the field --------------------------------------------------------------------------------------------------
TEETH = [[(-30, -6), (-22, -9), (-17, -2), (-19, 6), (-26, 4)], [(-24, 12), (-18, 10), (-15, 15), (-21, 18)]]
CUT_LINE = [(-24, 46), (-34, 52), (-46, 52)]
# the path network: strokes that meet at shared points, laid as one surface
PATHS = [[(-45, 8), (-36, 9), (-30, 16), (-24, 22), (-12, 22), (-3, 1)],      # door, south of the Teeth, to the Spine
         [(-46, 45), (-34, 40), (-20, 37), (-9, 36)],                         # yard to the snow bridge
         [(-34, 40), (-31, 29), (-30, 16)],                                   # yard up to the door's path
         [(-36, 9), (-37, -4), (-30, -16), (-18, -28), (-8, -44)]]            # west of the Teeth, north to the snow
PATH_OPEN = [False, False, False, True]  # whether a stroke's far end runs out into the snow, narrowing as it goes
PATH_WIDTH = 9
# the crevasses, red's half: the seam from the centre southward (its half turn runs north), the bridges left standing;
# and one across the open snow north of the Teeth
SEAM = [(-1, 6), (-5, 10), (-2, 15), (-7, 21), (-3, 26), (-8, 30)]
SEAM_ON = [(-8, 43), (-3, 47), (-6, 53)]                      # the shelf and its wall stand between the teams south of it
OPEN_CRACK = [(-52, -84), (-44, -76), (-37, -83), (-28, -75), (-20, -82), (-12, -76), (-7, -88)]
OPEN_BRIDGE = (-28, -75)
CRACK_WIDTH = (2.0, 6.0)


def front_x(z):
    """The mountain front's x at z (the field lies east of it)."""
    for (x0, z0), (x1, z1) in zip(FRONT, FRONT[1:]):
        if z0 <= z <= z1:
            return x0 + (x1 - x0) * (z - z0) / max(1e-9, z1 - z0)
    return FRONT[0][0] if z < FRONT[0][1] else FRONT[-1][0]


def crack(pts, seed, lo=CRACK_WIDTH[0], hi=CRACK_WIDTH[1]):
    """A crevasse's half widths along its line, wandering between lo and hi, narrowing at both ends: [(x, z, half)]
    sampled every block."""
    r = np.random.default_rng(seed)
    out, acc = [], 0.0
    total = sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))
    phase = r.uniform(0, 6.3, 3)
    for p, q in zip(pts, pts[1:]):
        n = max(1, int(math.dist(p, q)))
        for k in range(n):
            t = k / n
            x, z = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            s = acc + math.dist(p, q) * t
            wob = 0.5 + 0.25 * math.sin(s / 7 + phase[0]) + 0.25 * math.sin(s / 3.1 + phase[1])
            taper = min(1.0, s / 8, (total - s) / 8)
            out.append((x, z, (lo + (hi - lo) * wob) / 2 * max(0.35, taper)))
        acc += math.dist(p, q)
    return out


def crack_mask(Xg, Zg, samples, keep=None):
    m = np.zeros(Xg.shape, bool)
    for x, z, half in samples:
        if keep is not None and math.dist((x, z), keep) < 3:
            continue
        m |= (Xg - x) ** 2 + (Zg - z) ** 2 <= half * half
    return m


def cracks():
    """Every crevasse of red's half, as samples."""
    return [crack(SEAM, 1), crack(SEAM_ON, 2), crack(OPEN_CRACK, 3)]


def ramp():
    """The shelf's steps: [((x0, x1, z0, z1), floor)], treads three deep climbing south to one under the shelf."""
    x0, x1, z, n = SHELF_RAMP
    return [((x0, x1, z + 3 * k, z + 3 * k + 2), FIELD + 1 + k) for k in range(n)]


def _band(R, pts, half, h, kind):
    m = np.zeros_like(R.H, bool)
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        dx, dz = bx - ax, bz - az
        t = np.clip(((R.X - ax) * dx + (R.Z - az) * dz) / (dx * dx + dz * dz), 0, 1)
        m |= np.hypot(R.X - (ax + t * dx), R.Z - (az + t * dz)) <= half
    R.where(m, h, kind)


def build():
    R = Raster(X, Z, KINDS, base_h=FIELD, base_kind="field", symmetry=SYM)
    mountain = (R.X <= np.vectorize(front_x)(R.Z)) & (R.X < 0)
    R.where(mountain, 70, "mountain")
    R.poly(SHELF_POLY, SHELF, "shelf")
    for (x0, x1, z0, z1), h in ramp():
        R.rect(x0, x1, z0, z1, h, "stair")

    for box in (HALL, SPAWN_HALL, TUNNEL, YARD_TUNNEL, DARK_TUNNEL, SIDE_TUNNEL):
        R.rect(box[0], box[1], box[2], box[3], FIELD, "hall")
    for (x0, z0, x1, z1), _ in MOUTHS:
        R.rect(x0, x1, z0, z1, FIELD, "hall")
    R.rect(*YARD[:2], *YARD[2:], FIELD, "yard")
    R.rect(*DARK[:2], *DARK[2:], FIELD, "dark")
    R.rect(FACADE_X - 1, FACADE_X, *DOOR_Z, FIELD, "door")
    U = R.storey(1)
    for box in GALLERY + [UPPER_CORRIDOR, STAIR_TOP, (-83, -72, 18, 23)]:
        U.rect(box[0], box[1], box[2], box[3], UPPER, "hall")

    for poly, h in zip(TEETH, (FIELD + 6, FIELD + 4)):
        R.poly(poly, h, "rock")
    _band(R, CUT_LINE, 1.5, CUT, "cut")
    for p in PATHS:
        _band(R, p, PATH_WIDTH / 2, FIELD, "path")
    for k, samples in enumerate(cracks()):
        R.where(crack_mask(R.X, R.Z, samples, OPEN_BRIDGE if k == 2 else None), LAVA, "crevasse")
    return R


def objectives():
    """The teams, their spawns and their two monuments each: drawn once here, Blue's the half turn of Red's, read
    by map.xml, the sketch and the read-back alike."""
    O = Objectives(Teams(("red-team", "Red", "red", 20), ("blue-team", "Blue", "blue", 20)), SYM)
    sx, sz = SPAWN
    O.add(Spawn("red-team", (sx, FIELD + 1, sz), yaw=-90, area=Box(sx - 4, FIELD + 1, sz - 4, sx + 4, FIELD + 4, sz + 4)))
    rx, rz = REACTOR
    O.add(Destroyable("red-reactor", "Reactor", "red-team", Box(rx, FIELD + 5, rz, rx, FIELD + 6, rz)))
    px, pz = PUMP
    O.add(Destroyable("red-pump", "Pump", "red-team", Box(px, FIELD + 4, pz, px, FIELD + 5, pz)))
    O.add(Observer((0, 90, 0), yaw=90), mirror=False)
    return O
