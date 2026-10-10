"""Brassmoor Works: the plan. Capture the wool, two a team.

Identity: an ironworks hung in the smog, its decks of stone-brick paving joined by iron; each team spawns at a
gatehouse over its marshalling yard, keeps one wool in a boiler house and one under a water tower at the far
ends of two lanes walled with bedrock, and crosses to the other works over a band of open air with a crane in it.

Red holds the north (z < 0); blue's half is red's turned half a circle, (x, z) -> (-1 - x, -1 - z),
pgmvox's Symmetry("half"). Each piece is its own kind in the raster, so the checker, the sketch and the generator
all read which piece a column is.

    the Gatehouse   the spawn deck at 70, the two monuments on its front edge, two stairs down to the Yard
    the Yard        the hub at 66, a hole in its middle (the Turntable Pit), rails across it
    the Gantry      the west lane at 66 under a crane gantry, a bedrock wall five before the Boiler House
    the Spur        the east lane at 64, a bedrock wall five before the Water Tower
    the Quays       the front at 64, two legs down to the band
    the band        a build zone over the void, the Crane Island in its middle
    the Flats       two build zones beside the rooms, each with a stepping stone: the Slag Heap, the Coal Stage
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")))   # freeform/lib
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))               # trials/opus (common)

import numpy as np  # noqa: E402

import common  # noqa: E402
from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

BOARD = "brassmoor-works"
X_MIN, X_MAX = -88, 87
Z_MIN, Z_MAX = -112, 111
SYM = Symmetry("half")
KILL_Y = 50
SMOG_Y = (28, 42)
MAX_BUILD = 92

# ---- the pieces (red's): (key, name, class, (x0, z0, x1, z1) inclusive, floor) ------------------------------
PIECES = [
    ("gate", "the Gatehouse", "spawn", (-12, -100, 11, -86), 70),
    ("neck-w", "the West Steps", "spawn", (-10, -85, -6, -81), 68),
    ("neck-e", "the East Steps", "spawn", (5, -85, 9, -81), 68),
    ("yard", "the Yard", "hub", (-28, -80, 27, -58), 66),
    ("gantry", "the Gantry", "lane", (-63, -84, -29, -74), 66),
    ("boiler", "the Boiler House", "wool", (-79, -90, -64, -73), 68),
    ("spur", "the Spur", "lane", (28, -82, 59, -73), 64),
    ("tower", "the Water Tower", "wool", (60, -88, 75, -71), 66),
    ("quay-w", "the West Quay", "front", (-28, -57, -17, -12), 64),
    ("quay-e", "the East Quay", "front", (16, -57, 27, -12), 64),
    ("slag", "the Slag Heap", "islet", (-47, -56, -41, -50), 64),
    ("coal", "the Coal Stage", "islet", (40, -54, 46, -48), 64),
    ("crane", "the Crane Island", "mid", (-5, -5, 4, 4), 66),
]
PIECE = {p[0]: p for p in PIECES}
PIT = (-7, -76, 6, -66)                      # the Yard's hole, void all match

ZONES = [  # (key, name, box, (strip box kept clear beside a lane, or None))
    ("band", "the band", (-56, -11, 55, 10), None),
    ("flats-w", "the Boiler Flats", (-79, -72, -29, -38), (-63, -73, -29, -70)),
    ("flats-e", "the Tank Flats", (28, -70, 75, -38), (28, -72, 59, -69)),
]
WALLS = {  # the bedrock line across each lane: x0, x1 (two thick), the lane's z range, three high and a web
    "gantry": dict(x0=-59, x1=-58, z0=-84, z1=-74),
    "spur": dict(x0=54, x1=55, z0=-82, z1=-73),
}
ROOMS = {  # the room's walls round the deck, its doors: (side, from, to) along the face
    "boiler": dict(box=(-79, -90, -64, -73), height=11, doors=[("e", -82, -77), ("s", -68, -66)], wool="boiler"),
    "tower": dict(box=(60, -88, 75, -71), height=9, doors=[("w", -80, -76), ("s", 62, 64)], wool="tower"),
}
MONUMENT_Y = 71
SPAWN_AT = (0, 71, -95)
OBSERVER_AT = (0, 96, 0)

COLOURS = {"void": (34, 38, 52), "spawn": (210, 200, 180), "hub": (170, 168, 160), "lane": (150, 150, 150),
           "wool": (240, 240, 240), "front": (180, 176, 168), "islet": (120, 110, 100), "mid": (200, 180, 120),
           "stair": (150, 140, 120), "roomwall": (150, 70, 50), "barrier": (20, 20, 20)}
KIND_COLOURS = {k: COLOURS[c] for k, _, c, _, _ in PIECES} | {k: COLOURS[k] for k in ("void", "stair", "roomwall",
                                                                                          "barrier")}
KINDS = ["void"] + [p[0] for p in PIECES] + ["stair", "roomwall", "barrier"]
WALK = {p[0] for p in PIECES} | {"stair"}

PLACES = [("the Gatehouse", (0, -106)), ("the Yard", (-18, -62)), ("Turntable Pit", (0, -71)),
          ("the Gantry", (-46, -88)), ("BOILER HOUSE", (-72, -102)), ("the Spur", (44, -86)),
          ("WATER TOWER", (68, -101)), ("the West Quay", (-34, -30)), ("the East Quay", (34, -30)),
          ("the Slag Heap", (-44, -46)), ("the Coal Stage", (43, -44)), ("Crane Island", (0, 7)),
          ("the band", (-34, -4))]


def build():
    """The plan raster, both halves: the pieces at their floors, the pit, the rooms' walls, the bedrock lines and
    the flights of stairs between floors."""
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    for key, _, _, box, h in PIECES:
        R.box(*box, h, key, both=key != "crane")
    R.box(*PIT, 0, "void")
    R.floor, R.piece = R.H.copy(), R.K.copy()                   # what the ground is built from, under the walls
    # the flights: Gatehouse 70 to the steps 68 to the Yard 66; the Yard 66 down to the Spur 64; the lanes up to
    # the rooms; the Yard down to the Quays
    for x in (-8, 7):
        R.flight((x, -85), "n", width=(-1, 1), h0=69, n=1)           # steps to the Gatehouse
        R.flight((x, -81), "n", width=(-1, 1), h0=67, n=1)           # the Yard up to the steps
    R.flight((28, -78), "w", width=(-3, 3), h0=65, n=1)               # down from the Yard to the Spur
    R.flight((-63, -79), "w", width=(-2, 3), h0=67, n=1)              # up from the Gantry into the Boiler House
    R.flight((59, -78), "e", width=(-2, 2), h0=65, n=1)               # up from the Spur into the Water Tower
    for x0, x1 in ((-28, -17), (16, 27)):
        R.box(x0, -58, x1, -58, 65, "stair")                          # the Quays' head, a step under the Yard
        for x in range(x0, x1 + 1):
            R.stair[(x, -58)] = "n"
            R.stair[SYM.point(x, -58)] = "s"
    # the rooms' walls, all but their doors (so the walk goes in by a door)
    for key, room in ROOMS.items():
        x0, z0, x1, z1 = room["box"]
        top = PIECE[key][4] + room["height"]
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    if not door_at(room, x, z):
                        R.cell(x, z, top, "roomwall")
    for key, wl in WALLS.items():
        floor = PIECE[key][4]
        for x in range(wl["x0"], wl["x1"] + 1):
            for z in range(wl["z0"], wl["z1"] + 1):
                R.cell(x, z, floor + 4, "barrier")
    return R


def door_at(room, x, z):
    x0, z0, x1, z1 = room["box"]
    for side, a, b in room["doors"]:
        if side == "e" and x == x1 and a <= z <= b or side == "w" and x == x0 and a <= z <= b:
            return True
        if side == "s" and z == z1 and a <= x <= b or side == "n" and z == z0 and a <= x <= b:
            return True
    return False


def zone_mask(R, keys=None):
    """The build zones over the raster, both halves, less the land in them and less the strips kept clear."""
    m = np.zeros(R.H.shape, bool)
    for key, _, box, strip in ZONES:
        if keys is not None and key not in keys:
            continue
        for b, add in ((box, True), (strip, False)):
            if b is None:
                continue
            for bb in (b, common.image_box(SYM, *b)):
                x0, z0, x1, z1 = bb
                cells = (R.X >= x0) & (R.X <= x1) & (R.Z >= z0) & (R.Z <= z1)
                m = (m | cells) if add else (m & ~cells)
    return m & (R.K == R.kinds["void"]) & ~pit_mask(R)


def pit_mask(R):
    m = np.zeros(R.H.shape, bool)
    for b in (PIT, common.image_box(SYM, *PIT)):
        x0, z0, x1, z1 = b
        m |= (R.X >= x0) & (R.X <= x1) & (R.Z >= z0) & (R.Z <= z1)
    return m


def wall_mask(R):
    return R.mask("barrier")


def red_half(x, z):
    return z < 0


def objectives():
    """Teams, spawns and the four wools, drawn once for red's rooms: a Wool's team is the team that captures it,
    so the wool kept in red's Boiler House is blue's to take to blue's monument; its image is red's."""
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    x0, z0, x1, z1 = PIECE["gate"][3]
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=Box(x0, 70, z0, x1, 90, z1 - 3),
                protect=("iron block",)))
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    b, t = ROOMS["boiler"]["box"], ROOMS["tower"]["box"]
    boiler = Box(b[0], 69, b[1], b[2], 69 + ROOMS["boiler"]["height"] - 2, b[3])
    tower = Box(t[0], 67, t[1], t[2], 67 + ROOMS["tower"]["height"] - 2, t[3])
    # blue's monuments stand on blue's Gatehouse front: the images of (-4, -88) and (3, -88) are (3, 87), (-4, 87)
    O.add(Wool("blue-team", "lime", slot=(3, MONUMENT_Y, 87), found=(-73, 69, -86), room=boiler,
               spawn_at=(-73, 70, -84)), color="magenta")
    O.add(Wool("blue-team", "yellow", slot=(-4, MONUMENT_Y, 87), found=(68, 67, -84), room=tower,
               spawn_at=(68, 68, -82)), color="orange")
    return O


def room_cells(R, key, half="red"):
    """A room's floor inside its walls: where a wool is taken."""
    x0, z0, x1, z1 = ROOMS[key]["box"]
    cells = [(x, z) for x in range(x0 + 1, x1) for z in range(z0 + 1, z1)]
    return cells if half == "red" else [SYM.point(x, z) for x, z in cells]
