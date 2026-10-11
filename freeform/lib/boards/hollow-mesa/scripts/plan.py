"""Hollow Mesa's plan: every place, route and height the generator builds from, written for the red (west)
half. Blue's half is red's turned half a circle about the board's centre, (x, z) -> (-1 - x, -1 - z), so
the board reads as one canyon rather than two mirrored copies.

Coordinates are world x, z (north is -z). Heights are the ground a player stands on.
"""
import math

X_MIN, X_MAX = -130, 129
Z_MIN, Z_MAX = -100, 99

# ---- the canyon's cross-section, measured west of its wandering centreline ----------------------------
FLOOR_Y = 41          # the canyon floor, where Gilt stands
CREEK_Y = 40          # the creek's water
BENCH_Y = 57          # the ledge halfway up the wall, where the mine tram runs
PLATEAU_Y = 74        # the mesa top
FLOOR_HALF = 26       # canyon floor from the centreline to the foot of the lower cliff
LOWER_CLIFF = 5       # foot of the wall to the bench
BENCH_WIDTH = 10
UPPER_CLIFF = 5       # bench to rim


def rot(x, z):
    """Red's half to blue's: half a turn about the board's centre."""
    return -1 - x, -1 - z


def canyon_x(z):
    """The canyon's centreline. Odd about the centre, so the half-turn maps it onto itself; it passes through
    the centre, where the spring is."""
    a = (z + 0.5) * 2 * math.pi / 180.0
    return -0.5 + 7.0 * math.sin(a) + 2.5 * math.sin(2.3 * a)


def rim_x(z):
    return canyon_x(z) - (FLOOR_HALF + LOWER_CLIFF + BENCH_WIDTH + UPPER_CLIFF)


def bench_x(z):
    """The middle of the bench."""
    return canyon_x(z) - (FLOOR_HALF + LOWER_CLIFF + BENCH_WIDTH / 2)


# ---- the objective ----------------------------------------------------------------------------------
CORE = dict(x0=-67, x1=-64, y0=79, y1=82, z0=-26, z1=-23)   # obsidian shell, lava inside, floating five over the
#                                                             plateau at 73, over a well down through the mesa
#                                                             into the Throat; the shaft's head is a dozen west
CAVERN = (-70, -24)       # the Throat's centre
THROAT = (-65, -24, 3.2)  # the hole in the cavern floor to the void, east of the core
SPAWN = (-108, 75, 4)     # in the fort's courtyard

# ---- places (red half; blue's are their half-turn) ------------------------------------------------
PLACES = [
    dict(key="fort", name="Fort Ochre", at=(-108, 4), r=9,
         what="Red's spawn: an adobe compound with a timber gate and a watchtower, its back to High Butte",
         why="spawn; the gate looks east over the plateau to the arch", how="the gate onto Fort Road"),
    dict(key="butte", name="High Butte", at=(-124, 0), r=8,
         what="a flat-topped butte 18 blocks over the plateau behind the fort", why="frames the spawn; its top sees the whole board",
         how="a ladder up its east face from the fort's yard"),
    dict(key="grove", name="Olive Grove", at=(-88, -58), r=16,
         what="olives and acacias round a windmill and a stock tank: the north plateau's green",
         why="cover from the fort to the headframe and the Needles", how="Grove Track"),
    dict(key="needles", name="The Needles", poly=[(-80, -98), (-52, -98), (-54, -64), (-72, -60)],
         what="a field of banded clay spires on the north rim, 8 to 22 blocks tall",
         why="perches over Main Street; the Mule Trail tops out among them", how="Needles Path, the Mule Trail"),
    dict(key="headframe", name="Throat Headframe", at=(-78, -30), r=4,
         what="a timber headframe over the shaft down into the core's cavern", why="the defenders' way down to the core",
         how="Fort Road"),
    dict(key="throat", name="The Throat", at=CAVERN, r=12,
         what="a cavern in the banded clay with a hole in its floor to the void; the core stands on a stub of rock at the hole's lip, a miners' catwalk round its walls",
         why="RED CORE", how="the shaft from above, the Bench Adit from the canyon wall, the Chimney from the canyon floor"),
    dict(key="adit", name="Bench Adit", at=(-49, -34), r=3,
         what="a timbered drift from the bench into the Throat, arriving on the catwalk over the hole",
         why="the attack from the canyon wall", how="the bench, by the Mule Trail or the tipple"),
    dict(key="chimney", name="The Chimney", at=(-32, -14), r=3,
         what="a water-cut crack at the foot of the canyon wall that climbs inside the rock to the Throat's floor",
         why="the attack from below", how="from Main Street's south end"),
    dict(key="bench", name="The Bench", line=[(-39, -90), (-44, -34), (-36, 0), (-29, 26), (-32, 64), (-34, 82)],
         what="a ledge halfway up the canyon wall carrying the mine tram", why="the middle storey between town and mesa",
         how="the Mule Trail, the tipple, the Wash trestle"),
    dict(key="mule", name="Mule Trail", line=[(-30, -52), (-35, -58), (-40, -66), (-48, -74), (-54, -78)],
         what="stairs cut into the wall from the canyon floor to the bench and on to the rim", why="the climb from town to mesa",
         how="from Main Street"),
    dict(key="arch", name="Sky Arch", at=(-22, -1), r=4,
         what="a natural stone arch spanning the canyon rim to rim over the town", why="the high road between the mesas: short and exposed",
         how="Rim Path from the fort"),
    dict(key="main", name="Main Street", line=[(-16, -94), (-17, -50), (-15, -14), (-7, -5)],
         what="Gilt's commercial street: saloon, store, hotel, bank, assay office, the sheriff's jail",
         why="the town fought through, house by house", how="the spring at one end, the canyon's mouth at the other"),
    dict(key="spring", name="Gilt Spring", at=(0, 0), r=6,
         what="the spring the town grew round: a stone-rimmed pool at the board's centre, the creek leaving it north and south",
         why="the middle of the board; the arch passes over it", how="every street in town"),
    dict(key="adobe", name="Adobe Quarter", poly=[(-26, 8), (-2, 8), (-2, 40), (-22, 40)],
         what="flat-roofed adobe houses with log vigas, a mission chapel, the water tower, the livery",
         why="low cover between the spring and the Wash", how="Lower Street"),
    dict(key="tipple", name="The Tipple", at=(-21, 26), r=4,
         what="a timber tower where the tram dumps ore down a chute; its stair is the way up to the bench",
         why="the climb from the Adobe Quarter to the bench", how="Lower Street"),
    dict(key="wash", name="The Wash", line=[(-22, 51), (-40, 50), (-60, 53), (-80, 50), (-98, 52)],
         what="a dry side canyon climbing from the canyon floor to the mesa top, crossed by the tram's trestle",
         why="the long way up: the flank to the fort", how="from Lower Street; from the Rancho"),
    dict(key="trestle", name="Wash Trestle", at=(-32, 51), r=4,
         what="a timber trestle carrying the tram across the Wash at bench height", why="the bench goes on south; a bridge to fight on",
         how="the bench"),
    dict(key="drift", name="South Drift", at=(-40, 80), r=3,
         what="a played-out drift at the end of the tram with an ore cart and the foreman's chest", why="supplies; the tram's end",
         how="the bench, over the trestle"),
    dict(key="rancho", name="Rancho", at=(-104, 74), r=10,
         what="an adobe ranch house, a timber barn, a corral and a windmill over a trough", why="the outpost on the way from the Wash to the fort",
         how="Ranch Road"),
    dict(key="table", name="Table Rock", at=(-80, 86), r=8,
         what="a small flat butte with a ladder up it", why="a lookout over the Wash and the south canyon", how="its ladder"),
    dict(key="acacias", name="Acacia Flat", at=(-66, 78), r=12,
         what="acacias on the south plateau above the canyon", why="the south rim's cover and its colour", how="Ranch Road"),
]

ROUTES = [
    dict(name="Fort Road", kind="road", pts=[(-99, 4), (-88, 0), (-84, -12), (-78, -26)]),
    dict(name="Rim Path", kind="road", pts=[(-88, 0), (-70, 2), (-54, -1), (-47, -1)]),
    dict(name="Grove Track", kind="track", pts=[(-86, -6), (-88, -24), (-88, -42)]),
    dict(name="Needles Path", kind="track", pts=[(-78, -36), (-70, -50), (-62, -64), (-56, -76)]),
    dict(name="Ranch Road", kind="road", pts=[(-99, 10), (-100, 30), (-102, 46), (-104, 62)]),
    dict(name="Wash Track", kind="track", pts=[(-102, 52), (-80, 51), (-60, 53), (-40, 50), (-24, 51)]),
    dict(name="Main Street", kind="street", pts=[(-18, -96), (-19, -70), (-21, -40), (-18, -20), (-12, -8), (-7, -5)]),
    dict(name="Lower Street", kind="street", pts=[(-7, 5), (-9, 14), (-9, 30), (-12, 44), (-14, 60), (-15, 80), (-15, 97)]),
]
