"""Tidewell Canals: the plan. King of the hill, three points.

Identity: a canal quarter on a lagoon, two customs houses at its ends, three markets fought over: the Campo in the
middle, a square ringed by arcades with a gallery over them, worth two a second, and a fish market under an open
loggia at either side, worth one; every way between them crosses a canal by a bridge.

The board turns by a half (x, z) -> (-1 - x, -1 - z), pgmvox's Symmetry("half"); red holds the west. Red's half
is itself drawn mirrored in z (`quad`), so the whole board is symmetric both ways, every hill is the same walk
for both teams, and the flank hills are the images of each other.

    the Customs House   the spawn's court at 40, walled on three sides, its portico opening east
    the Sestiere        red's district: three streets east to three bridges over the Grand Canal, blocks of houses
                        between them, a campiello with a wellhead
    the Grand Canal     water at 38 between banks at 40, crossed by three bridges (a block to two over the street)
    the Campo           the middle at 40: the centre pad, four cisterns as large cover, arcades north and south with
                        the gallery over them at 45 (storey 1)
    the Rii             two cross canals cutting the Campo off from the fish markets, two bridges each
    the Fish Markets    the flank pads under loggias on the board's north and south edges
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")))   # freeform/lib
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))               # trials/opus (common)

import common  # noqa: E402,F401
from pgmvox.objectives import Box, Hill, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

BOARD = "tidewell-canals"
X_MIN, X_MAX = -80, 79
Z_MIN, Z_MAX = -64, 63
SYM = Symmetry("half")
STREET, WATER, GALLERY = 40, 38, 45
KINDS = ["lagoon", "street", "campo", "quay", "canal", "bridge", "steps", "stair", "court", "market", "pad",
         "house", "wall", "cistern", "cover", "pillar", "gallery"]
COLOURS = {"lagoon": (50, 90, 140), "street": (170, 168, 160), "campo": (205, 195, 175), "quay": (150, 148, 142),
           "canal": (70, 120, 170), "bridge": (215, 205, 180), "steps": (130, 130, 125), "stair": (190, 185, 170),
           "court": (225, 215, 195), "market": (200, 185, 160), "pad": (235, 205, 110), "house": (200, 120, 90),
           "wall": (120, 115, 110), "cistern": (110, 110, 105), "cover": (150, 110, 80), "pillar": (95, 95, 92),
           "gallery": (230, 170, 120)}
WALK = {"street", "campo", "quay", "canal", "bridge", "steps", "stair", "court", "market", "pad", "gallery"}
WALLS = ("house", "wall", "cistern", "cover", "pillar")

# ---- red's north quadrant (x < 0, z < 0); quad() draws it and its mirror in z, and the half turn adds blue's ----
EDGE = 76                                   # the sea wall: |x| and |z| past this are lagoon
CUSTOMS = (-72, -9, -64, -1)                # the customs house's court (and its mirror): the spawn
CUSTOMS_WINGS = [(-75, -14, -64, -10), (-75, -9, -73, -1)]   # its north wing and back
PORTICO = [(-64, -9, -64, -6)]              # the portico's piers on the court's open east side (each half)
GRAND = (-21, -60, -15, -1)                 # the Grand Canal (and its mirror)
BRIDGES = [(-22, -50, -14, -46), (-22, -3, -14, -1)]   # the north bridge and half the centre bridge
RIO = (-13, -35, -1, -28)                   # the cross canal north of the Campo (its half; the half turn adds x >= 0)
RIO_BRIDGES = [(-9, -36, -7, -27)]          # a bridge over the Rio (and its images)
CAMPO = (-13, -27, -1, -1)                  # the Campo's red quarter
MARKET = (-13, -60, -1, -36)                # the fish market's red quarter
PAD_C = (-4, 40, -4, 3, 40, 3)              # the centre pad: 8 x 8, level with the Campo
PAD_N = (-4, 40, -54, 3, 40, -47)           # the north flank pad: 8 x 8 under the loggia; the south is its image
LOGGIA = (-11, -58, 10, -42)                # the loggia's roof span over the north market
LOGGIA_ROOF = 46
LOGGIA_PILLARS = [(-11, -42), (-5, -42), (4, -42), (10, -42), (-11, -50), (10, -50)]
LOGGIA_WALL = (-11, -59, 10, -59)            # its back wall on the sea wall's side
CISTERNS = [(-12, -13, -9, -10)]            # four large cover blocks round the centre pad (one a quarter)
GALLERY_SPAN = (-12, -24, -1, -21)          # the gallery over the arcade on the Campo's north side, storey 1
ARCADE_PILLARS = [(-12, -21), (-8, -21), (-4, -21)]
# red's district: blocks of houses between the streets, a campiello with a wellhead
HOUSES = [(-61, -44, -49, -32, 3), (-45, -44, -26, -34, 2), (-61, -27, -49, -15, 2), (-34, -27, -26, -6, 3),
          (-58, -11, -49, -5, 2)]           # x0, z0, x1, z1, storeys
CAMPIELLO = (-48, -30, -36, -16)
WELL = (-43, -24, -41, -22)
COVER = [(-58, -50, -57, -49), (-40, -50, -39, -49), (-30, -12, -29, -11), (-11, -6, -10, -5),
         (-7, -18, -6, -17), (-10, -40, -9, -39), (-6, -46, -5, -45), (-60, -2, -59, -1)]
COLUMN = (-42, -6, -38, -1)                 # the column on its plinth in the central street: no line from the Campo to the spawn
SHOPS = [(-13, -60, -13, -52), (-13, -44, -13, -36)]   # the fishmongers' fronts walling the market, a gate between
STEPS = [(-21, -30, -21, -28), (-21, -14, -21, -12), (-13, -31, -11, -31)]   # ways out of the water

SPAWN_AT = (-70, 41, -1)
PLACES = [("the Customs House", (-70, -12)), ("the Sestiere", (-44, -38)), ("the campiello", (-42, -19)),
          ("the Grand Canal", (-18, -56)), ("the Campo", (-8, -8)), ("the Gallery", (-8, -26)),
          ("Rio del Nord", (0, -31)), ("the Fish Market", (0, -40)), ("the Loggia", (-8, -56))]


def quad(fn, box, *a, **k):
    """Draw a red box and its mirror in z within red's half (z' = -1 - z); the raster's half turn adds blue's."""
    x0, z0, x1, z1 = box
    fn(x0, z0, x1, z1, *a, **k)
    fn(x0, -1 - z1, x1, -1 - z0, *a, **k)


def build():
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=WATER, base_kind="lagoon", symmetry=SYM)
    quad(R.box, (-EDGE + 1, -60, -1, -1), STREET, "street")
    quad(R.box, GRAND, WATER, "canal")
    quad(R.box, (GRAND[0] - 1, -60, GRAND[0] - 1, -1), STREET, "quay")
    quad(R.box, (GRAND[2] + 1, -60, GRAND[2] + 1, -1), STREET, "quay")
    quad(R.box, CAMPO, STREET, "campo")
    quad(R.box, MARKET, STREET, "market")
    quad(R.box, RIO, WATER, "canal")
    for b in BRIDGES:                                          # arched: a block up at each end, two in the middle
        x0, z0, x1, z1 = b
        quad(R.box, (x0, z0, x0, z1), STREET + 1, "bridge")
        quad(R.box, (x1, z0, x1, z1), STREET + 1, "bridge")
        quad(R.box, (x0 + 1, z0, x1 - 1, z1), STREET + 2, "bridge")
    for x0, z0, x1, z1 in RIO_BRIDGES:
        quad(R.box, (x0, z0, x1, z0), STREET + 1, "bridge")
        quad(R.box, (x0, z1, x1, z1), STREET + 1, "bridge")
        quad(R.box, (x0, z0 + 1, x1, z1 - 1), STREET + 2, "bridge")
    for b in STEPS:
        quad(R.box, b, WATER + 1, "steps")
    quad(R.box, CUSTOMS, STREET, "court")
    for b in CUSTOMS_WINGS:
        quad(R.box, b, STREET + 12, "house")
    for b in PORTICO:
        x0, z0, x1, z1 = b
        quad(R.box, (x0, z0, x1, z0), STREET + 7, "pillar")
    for x0, z0, x1, z1, n in HOUSES:
        quad(R.box, (x0, z0, x1, z1), STREET + 1 + 4 * n + 3, "house")
    quad(R.box, CAMPIELLO, STREET, "campo")
    quad(R.box, WELL, STREET + 2, "cover")
    quad(R.box, COLUMN, STREET + 12, "wall")
    for b in SHOPS:
        quad(R.box, b, STREET + 8, "house")
    for b in COVER:
        quad(R.box, b, STREET + 3, "cover")
    for b in CISTERNS:
        quad(R.box, b, STREET + 4, "cistern")
    for x, z in LOGGIA_PILLARS + ARCADE_PILLARS:
        quad(R.box, (x, z, x, z), STREET + 6, "pillar")
    quad(R.box, LOGGIA_WALL, STREET + 6, "wall")
    # the sea wall: a parapet four high on the quarter's edge, so nobody steps into the lagoon
    quad(R.box, (-EDGE, -61, -EDGE, -1), STREET + 4, "wall")
    quad(R.box, (-EDGE, -61, -1, -61), STREET + 4, "wall")
    # the hills
    x0, _, z0, x1, _, z1 = PAD_C
    R.box(x0, z0, x1, z1, STREET, "pad", both=False)
    x0, _, z0, x1, _, z1 = PAD_N
    R.box(x0, z0, x1, z1, STREET, "pad")
    # storey 1: the gallery over the north arcade (and its mirror), stairs up at its west end
    U = R.storey(1)
    quad(U.box, GALLERY_SPAN, GALLERY, "gallery")
    gx0, gz0, gx1, gz1 = GALLERY_SPAN
    for k in range(5):                                         # the stair: up along x from the Campo's west edge
        quad(R.box, (gx0 + k, gz0 - 2, gx0 + k, gz0 - 1), STREET + 1 + k, "stair")
    return R


def stair_links(R):
    """None needed: the gallery stair's top is on the ground storey at 45, and the walk graph steps from it onto
    the gallery (storey 1) beside it at the same height."""
    return []


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    x0, z0, x1, z1 = CUSTOMS
    O.add(Spawn("red-team", SPAWN_AT, yaw=-90, kit="spawn-kit", area=Box(x0, STREET + 1, z0, x1, STREET + 6, -1 - z0)))
    O.add(Hill("campo", "the Campo", Box(*PAD_C), points=2, capture_time="10s"), mirror=False)
    O.add(Hill("north-market", "the North Fish Market", Box(*PAD_N), points=1, capture_time="10s"), mirror=False)
    s = Box(*PAD_N).image(SYM)
    O.add(Hill("south-market", "the South Fish Market", Box(s.x0, STREET, s.z0, s.x1, STREET, s.z1), points=1,
               capture_time="10s"), mirror=False)
    O.add(Observer((0, 70, 0), yaw=90), mirror=False)
    return O


def pad_ring(pad, at):
    """The pad's cells `at` blocks in from its edge, as boxes (four, one block thick) for a region: the progress ring."""
    x0, y, z0, x1, _, z1 = pad.x0, pad.y0, pad.z0, pad.x1, pad.y1, pad.z1
    a = at
    return [Box(x0 + a, y, z0 + a, x1 - a, y, z0 + a), Box(x0 + a, y, z1 - a, x1 - a, y, z1 - a),
            Box(x0 + a, y, z0 + a + 1, x0 + a, y, z1 - a - 1), Box(x1 - a, y, z0 + a + 1, x1 - a, y, z1 - a - 1)]


def pad_cells(name):
    for o in objectives().items:
        if getattr(o, "id", None) == name:
            return sorted(o.pad.cells())
    raise KeyError(name)
