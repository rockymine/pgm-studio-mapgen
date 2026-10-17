"""Sixes and Sevens — the plan. A frozen wasteland between two bunkers dug into the ice cliffs at either end of a
long board: bunker 06 in the west for Red, bunker 07 in the east for Blue, each the half turn of the other.

    floors: 40 the snowfield, the bunker halls and the yard; 47 the high shelf; 34 the cut; the crevasses holes
    with lava at their foot; the mountain stands round everything at 70 and over

Each team defends two monuments: the Reactor, floating in the tall hall behind the bunker's door, and the Pump,
in the yard cut into the cliff beside the facade. The spawn hall lies deep in the mountain behind both.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan.raster import Raster, Symmetry  # noqa: E402

X = (-130, 129)
Z = (-90, 89)
FIELD = 40
SHELF = 47
CUT = 34
MOUNTAIN = 70
KINDS = ["field", "path", "mountain", "hall", "dark", "yard", "shelf", "stair", "rock", "crevasse", "cut", "door"]
COLOURS = {"field": (226, 232, 238), "path": (150, 128, 104), "mountain": (92, 96, 104), "hall": (196, 188, 170),
           "dark": (70, 66, 72), "yard": (206, 210, 200), "shelf": (176, 196, 214), "stair": (160, 170, 190),
           "rock": (120, 120, 124), "crevasse": (200, 70, 30), "cut": (150, 170, 190), "door": (230, 200, 90)}
WALK = {"field", "path", "hall", "dark", "yard", "shelf", "stair", "cut", "door"}
WALLS = {"mountain", "rock"}

# Red's bunker, x west of the facade; Blue's is its half turn
FACADE_X = -46                          # the face column; the field starts a block east of it
FACADE_Z = (-12, 29)
DOOR_Z = (0, 17)
HALL = (-71, -48, -6, 23)               # x0, x1, z0, z1: the tall hall, three segments, the Reactor in it
SPAWN_HALL = (-104, -84, 16, 37)
TUNNEL = (-83, -72, 18, 23)             # spawn hall to the tall hall, 6 wide
YARD_TUNNEL = (-83, -67, 34, 39)        # spawn hall to the yard, 6 wide
YARD = (-66, -47, 34, 55)               # cut into the cliff south of the facade, open to the field
DARK = (-108, -91, -14, 3)              # the generator room
DARK_TUNNEL = (-99, -94, 4, 15)         # dark room to the spawn hall
SIDE_TUNNEL = (-90, -72, -6, -1)        # dark room to the tall hall's back corner
VENT = (-54, 6)                         # a shaft from the cliff top into the tall hall, over the Reactor's front

SPAWN = (-97, 26)
REACTOR = (-60, 8)
PUMP = (-54, 41)

# the crevasse seam between the teams, red's half from the centre southward, with the snow bridge left standing
SEAM = [(-1, 6), (-6, 14), (-3, 22), (-8, 30)]
SEAM_ON = [(-8, 43), (-4, 51), (-11, 60), (-7, 68), (-12, 76)]
SEAM_WIDTH = 5


def _band(R, pts, half, h, kind):
    """Cells within `half` of a polyline."""
    import numpy as np
    m = np.zeros_like(R.H, bool)
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        dx, dz = bx - ax, bz - az
        L2 = dx * dx + dz * dz
        t = np.clip(((R.X - ax) * dx + (R.Z - az) * dz) / L2, 0, 1)
        m |= np.hypot(R.X - (ax + t * dx), R.Z - (az + t * dz)) <= half
    R.where(m, h, kind)


def build():
    R = Raster(X, Z, KINDS, base_h=FIELD, base_kind="field", symmetry=Symmetry("half"))
    R.rect(X[0], FACADE_X, Z[0], Z[1], MOUNTAIN, "mountain")                      # the cliffs the bunkers are in
    R.rect(FACADE_X + 1, -1, Z[0], -80, MOUNTAIN, "mountain")                      # the board's north and south rims
    R.rect(FACADE_X + 1, -1, 80, Z[1], MOUNTAIN, "mountain")
    R.poly([(-45, -62), (-28, -58), (-24, -40), (-33, -20), (-45, -14)], MOUNTAIN, "mountain")   # the north spur
    R.poly([(-45, 57), (-30, 58), (-36, 80), (-45, 80)], MOUNTAIN, "mountain")                   # the south spur

    # the high shelf along the south rim, held by a lofted wall on its north edge, a ramp at its east end
    R.poly([(-32, 62), (8, 61), (14, 70), (14, 79), (-34, 79)], SHELF, "shelf")
    for k in range(SHELF - FIELD - 1):
        R.rect(21 - k, 21 - k, 63, 68, FIELD + 1 + k, "stair")

    # the bunker, inside the mountain
    R.rect(*HALL[:2], *HALL[2:], FIELD, "hall")
    R.rect(FACADE_X - 1, FACADE_X, *DOOR_Z, FIELD, "door")
    R.rect(*SPAWN_HALL[:2], *SPAWN_HALL[2:], FIELD, "hall")
    R.rect(*TUNNEL[:2], *TUNNEL[2:], FIELD, "hall")
    R.rect(*YARD_TUNNEL[:2], *YARD_TUNNEL[2:], FIELD, "hall")
    R.rect(*YARD[:2], *YARD[2:], FIELD, "yard")
    R.rect(*DARK[:2], *DARK[2:], FIELD, "dark")
    R.rect(*DARK_TUNNEL[:2], *DARK_TUNNEL[2:], FIELD, "hall")
    R.rect(*SIDE_TUNNEL[:2], *SIDE_TUNNEL[2:], FIELD, "hall")

    # the field: the Teeth in front of the door, the cut toward the yard, the paths, the seam
    R.poly([(-30, -6), (-22, -9), (-17, -2), (-19, 6), (-26, 4)], FIELD + 6, "rock")
    R.poly([(-24, 12), (-18, 10), (-15, 15), (-21, 18)], FIELD + 4, "rock")
    _band(R, [(-24, 46), (-34, 52), (-46, 52)], 1.5, CUT, "cut")
    _band(R, [(-44, 9), (-33, 9), (-20, 21), (-8, 22), (-4, 0)], 1.5, FIELD, "path")
    _band(R, [(-45, 44), (-30, 40), (-14, 38), (-8, 36)], 1.5, FIELD, "path")
    _band(R, SEAM, SEAM_WIDTH / 2, FIELD - 14, "crevasse")
    _band(R, SEAM_ON, SEAM_WIDTH / 2, FIELD - 14, "crevasse")
    return R


def objectives():
    """The teams, their spawns and their two monuments each: drawn once here, Blue's the half turn of Red's, read
    by map.xml, the sketch and the read-back alike."""
    O = Objectives(Teams(("red-team", "Red", "red"), ("blue-team", "Blue", "blue")), Symmetry("half"))
    sx, sz = SPAWN
    O.add(Spawn("red-team", (sx, FIELD + 1, sz), yaw=-90, area=Box(sx - 4, FIELD + 1, sz - 4, sx + 4, FIELD + 4, sz + 4)))
    rx, rz = REACTOR
    O.add(Destroyable("red-reactor", "Reactor", "red-team", Box(rx, FIELD + 5, rz, rx, FIELD + 6, rz)))
    px, pz = PUMP
    O.add(Destroyable("red-pump", "Pump", "red-team", Box(px, FIELD + 4, pz, px, FIELD + 5, pz)))
    O.add(Observer((0, 90, 0), yaw=90), mirror=False)
    return O
