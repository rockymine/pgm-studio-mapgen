"""Kilnhold: the plan. Two geothermal bunkers dug into the walls of a volcanic caldera, destroy the monuments and
capture the flag. Everything is written for red (north, z < 0); blue is the half turn about the board's middle,
(x, z) -> (-1 - x, -1 - z), which is pgmvox's Symmetry("half").

A bunker has four levels. The roof deck (the Crown, floor 77) is the open surface fight and carries one monument.
The gate level (floor 65) is the spawn, the spine and the gate hall behind the facade, with galleries a half level
up (70). The deep level (floor 57) holds the pump hall with the other monument in the west wing and the turbine
hall with the flag in the east, joined by a cross gallery under the gate hall. Levels meet by slab ramps that
rise half a block a cell, never by a tall stair.

Heights follow the library: a "floor" is the y of the floor block, and a player stands at floor + 1.

    SPAWN, BEACON_AT, PUMP_AT, FLAG_POST, NET_BOX   the objectives, drawn once for red
    ROOMS, PASSAGES                                 the interior as data the generator, the check and the sketch read
    objectives()                                    the teams, spawns, monuments and flag as pgmvox objects, imaged
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B  # noqa: E402
from pgmvox.play.objectives import Box, Destroyable, Flag, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan.raster import Symmetry  # noqa: E402

BOARD = "kilnhold"
X_MIN, X_MAX = -70, 69
Z_MIN, Z_MAX = -100, 99
SY = 128
SYM = Symmetry("half")

# floors (the y of the floor block)
FIELD = 62            # the caldera floor
APRON = 65            # the paved forecourt in front of the facade, level with the gate hall
GATE = 65             # spawn, spine, gate hall, workshop and command post
MEZ = 70              # the gate hall's galleries
DEEP = 57             # pump hall, turbine hall, cross gallery, the culverts, the courts of the tower and the pit
PIT = DEEP
CROWN = 77            # the roof deck

# ---- the interior: rooms as (x0, x1, z0, z1, floor, height of air) -------------------------------------------
ROOMS = {
    "muster": (-12, 11, -94, -80, GATE, 9),
    "spine": (-3, 2, -79, -75, GATE, 6),
    "gate_hall": (-15, 14, -74, -54, GATE, 10),
    "workshop": (-31, -17, -92, -80, GATE, 7),
    "command": (16, 30, -92, -80, GATE, 7),
    "pump": (-52, -34, -76, -58, DEEP, 10),
    "turbine": (33, 51, -76, -58, DEEP, 10),
    "shrine": (52, 56, -70, -64, DEEP, 7),
}
PASSAGES = {
    "workshop_door": dict(x=(-16, -13), z=(-87, -85), floor=GATE, h=5),
    "command_door": dict(x=(12, 15), z=(-87, -85), floor=GATE, h=5),
    "cross": dict(x=(-33, 32), z=(-70, -67), floor=DEEP, h=5),
    "descent_w": dict(x=(-33, -16), z=(-62, -59), floor=GATE, h=6),
    "descent_e": dict(x=(15, 32), z=(-62, -59), floor=GATE, h=6),
    # the west culvert bends: north from the tower's court, west along the hall's south side, north again, east into the
    # hall's west wall; the east one runs straight from the pit to the turbine hall
    "culvert_w": dict(parts=[(-48, -45, -51, -44), (-57, -45, -54, -51), (-57, -54, -66, -51), (-53, -52, -66, -63)],
                      floor=DEEP, h=6),
    "culvert_e": dict(parts=[(44, 47, -58, -44)], floor=DEEP, h=6),
    "crown_ramp_w": dict(x=(-37, -16), z=(-58, -55), floor=MEZ, h=6),
    "crown_ramp_e": dict(x=(15, 36), z=(-58, -55), floor=MEZ, h=6),
}

# ---- the surface -----------------------------------------------------------------------------------------------
TOWER = (-46.0, -36.0)            # the cooling tower's centre in block-centre coordinates; its court is sunk to PIT
TOWER_R_OUT, TOWER_R_IN = 9.5, 7.5
PIT_BOX = (40, 51, -47, -34)      # the quarry pit's floor, x0, x1, z0, z1
APRON_BOX = (-26, 25, -47, -32)
CRATER_R = 19                     # the crest of the central crater, about the board's middle
DECK_BOX = (-58, 57, -93, -55)    # the Crown, a paved roof
FACADE_TOP = CROWN

# ---- the objectives (red) ---------------------------------------------------------------------------------------
SPAWN = (0, GATE + 1, -83)
SPAWN_AREA = Box(-12, GATE + 1, -94, 11, GATE + 9, -80)
BEACON_AT = (-34, -70)            # the Crown monument, over the deck at CROWN
PUMP_AT = (-43, -67)              # the deep monument, over the pump hall's sump
TURBINE_AT = (42, -67)            # the turbine hall's drum
FLAG_POST = (55, DEEP + 2, -67)   # the banner's block, on the dais (a block over the floor)
NET_BOX = Box(-4, GATE + 1, -66, 3, GATE + 3, -58)     # the capture dais in the gate hall
OBSERVER = (0, 100, 0)

TEAMS = Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16))

PLACES = [
    ("Muster Hall", (0, -87)), ("The Spine", (0, -77)), ("Gate Hall", (0, -64)), ("The Gate", (0, -50)),
    ("Workshop", (-24, -86)), ("Command Post", (23, -86)), ("Pump Hall", (-43, -67)), ("Turbine Hall", (42, -67)), ("Shrine", (54, -67)),
    ("Cross Gallery", (0, -68)), ("West Descent", (-28, -60)), ("East Descent", (27, -60)),
    ("Crown Beacon", (-34, -70)), ("The Crown", (0, -75)), ("West Crown Ramp", (-26, -57)),
    ("East Crown Ramp", (25, -57)), ("Cooling Tower", (-47, -37)), ("Quarry Pit", (45, -41)),
    ("The Apron", (0, -40)), ("The Crater", (0, -8)), ("West Lane", (-52, -12)), ("East Lane", (52, -12)),
    ("West Slagbank", (-28, -27)), ("East Slagbank", (27, -27)),
]


# ---- the routes the plan states, as axis-aligned polylines of cell centres: a player walks them in cardinal moves,
# so a route's length is the sum of its legs, the unit the read-back's walk counts in --------------------------
ROUTES = {
    "spawn to the Crown Beacon": [(0, -83), (0, -74), (-13, -74), (-13, -57), (-31, -57), (-31, -70), (-34, -70)],
    "spawn to the Pump Hall Monument": [(0, -83), (0, -74), (-10, -74), (-10, -61), (-34, -61), (-34, -67), (-43, -67)],
    "spawn to the flag": [(0, -83), (0, -74), (10, -74), (10, -61), (33, -61), (33, -67), (54, -67)],
    # the enemy's way in: blue's spawn to the dais in red's gate hall, then red's own legs from the dais
    "enemy spawn to the gate hall dais": [(-1, 82), (-1, 56), (-1, 33), (0, 33), (0, -27), (-23, -27), (-23, -44), (0, -44),
                                          (0, -60)],
    "dais to the Crown Beacon": [(0, -60), (-10, -60), (-10, -74), (-13, -74), (-13, -57), (-31, -57), (-31, -70),
                                 (-34, -70)],
    "dais to the Pump Hall Monument": [(0, -60), (-34, -60), (-34, -67), (-43, -67)],
    "dais to the flag": [(0, -60), (33, -60), (33, -67), (54, -67)],
    # the other ways in: through the cooling tower and the west culvert, and up the west ramp onto the Crown
    "enemy spawn to the Pump Hall Monument by the culvert": [(-1, 82), (-1, 56), (-1, 33), (0, 33), (0, -24), (-46, -24),
                                                           (-46, -51), (-55, -51), (-55, -64), (-52, -64), (-52, -67),
                                                           (-43, -67)],
    "enemy spawn to the Crown Beacon by the west ramp": [(-1, 82), (-1, 56), (-1, 33), (0, 33), (0, -24), (-60, -24),
                                                       (-60, -51), (-46, -51), (-46, -70), (-34, -70)],
    "enemy spawn to the flag by the east culvert": [(-1, 82), (-1, 56), (-1, 33), (0, 33), (0, -24), (45, -24),
                                                  (45, -67), (54, -67)],
}


def route_length(name):
    """The cardinal length of a stated route, in blocks."""
    pts = ROUTES[name]
    return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def monument_box(at, floor):
    """A 3x3x3 monument centred over (x, z), its lowest block three blocks of air over `floor`'s surface."""
    x, z = at
    return Box(x - 1, floor + 4, z - 1, x + 1, floor + 6, z + 1)


def flag():
    return Flag("red-flag", "Red Flag", "red", [("Turbine Dais", FLAG_POST, 270)], team="red-team",
                pickup_kit="carrier", return_time="15s", show_respawn=False, points_rate=None)


def objectives():
    O = Objectives(TEAMS, SYM)
    O.add(Observer(OBSERVER, yaw=0), mirror=False)
    O.add(Spawn("red-team", SPAWN, yaw=0, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Destroyable("red-beacon", "Crown Beacon", "red-team", monument_box(BEACON_AT, CROWN)))
    O.add(Destroyable("red-sump", "Pump Hall Monument", "red-team", monument_box(PUMP_AT, DEEP)))
    O.add(flag(), color="blue", name="Blue Flag")
    return O


def net_boxes():
    """(team id, flag id, the net's Box) for each team: a team captures at its own dais, a box over it."""
    img = NET_BOX.image(SYM)
    return [("red-team", "blue-flag", NET_BOX), ("blue-team", "red-flag", img)]
