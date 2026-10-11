"""Hollowcrown's plan, drawn in polygons and polylines rather than circles.

Two mountains face each other across a river valley. On each stands a fortress town: Crownhold, the citadel
on the summit, where the team spawns; Wendholm, the town that climbs the mountain's valley face along the
Wend, a serpentine road of four switchback legs; and the Eyrie, a tower on a spur to the north holding the
upper monument. Under each mountain lies Underhall, a delved city in a cavern round an underground lake,
with the lower monument in its temple and the team's second spawn at its Lower Gate.

Red holds the west (x < 0), blue the east; blue's half is red's turned half a circle about the centre,
(x, z) -> (-1 - x, -1 - z). North is -z. A route's points are (x, z, y): the y it is graded to there.
"""
import math

X_MIN, X_MAX = -120, 119
Z_MIN, Z_MAX = -96, 95
WATER_Y = 40               # the river
PLAIN_Y = 43               # the floodplain by the river
FOOT_Y = 46                # where the mountain meets the valley


def rot(x, z):
    return -1 - x, -1 - z


# ---- the river: x = -0.5 + wander(z), odd about z = -0.5 so the half-turn maps it onto itself ------------
def river_x(z):
    t = z + 0.5
    return -0.5 + 6.0 * math.sin(2 * math.pi * t / 112.0) + 2.0 * math.sin(2 * math.pi * t / 47.0)


RIVER_HALF = 5.5

# ---- the mountain: its foot, and the summits it rises to (each a polygon at a height) ---------------------
FOOT = [(-120, -96), (-32, -96), (-27, -72), (-30, -46), (-27, -22), (-24, 6), (-28, 34), (-34, 62), (-42, 95),
        (-120, 95)]
CROWN = [(-102, -36), (-84, -43), (-66, -33), (-62, -15), (-72, -2), (-92, -4), (-104, -18)]
EYRIE = [(-64, -76), (-52, -80), (-44, -70), (-49, -60), (-60, -62)]
SHOULDER = [(-108, 30), (-84, 28), (-66, 38), (-68, 62), (-90, 70), (-110, 56)]
SUMMITS = [dict(key="crown", poly=CROWN, y=98), dict(key="eyrie", poly=EYRIE, y=92),
           dict(key="shoulder", poly=SHOULDER, y=73)]

# ---- the water on the mountain ------------------------------------------------------------------------
TARN = [(-100, 40), (-86, 37), (-76, 45), (-78, 56), (-92, 60), (-102, 52)]
TARN_Y = 71
# Millbrook: from the tarn's outlet down two falls to the river, (x, z, water y)
BROOK = [(-76, 48, 71), (-70, 49, 71), (-66, 50, 71), (-63, 51, 59), (-58, 52, 59), (-52, 54, 59), (-48, 55, 59),
         (-45, 55, 46), (-38, 57, 45), (-30, 56, 44), (-22, 57, 43), (-14, 56, 42), (-8, 55, 41), (-3, 55, 40)]
FALLS = [(-64, 51), (-46, 55)]          # Greyfall (upper) and the Mill Leap (lower)

# ---- the town ------------------------------------------------------------------------------------------
TOWN = [(-70, -32), (-28, -34), (-18, -12), (-17, 22), (-26, 38), (-52, 38), (-68, 12)]
# The Wend: four legs and three hairpins from the valley to Crownhold's gate.
WEND = [(-20, 22, 45), (-25, 8, 48), (-30, -6, 52), (-33, -18, 56),        # leg 1, north
        (-37, -23, 58),                                                    # hairpin
        (-39, -10, 61), (-40, 2, 64), (-41, 14, 67), (-43, 24, 69),        # leg 2, south, through the market
        (-47, 28, 70),                                                     # hairpin
        (-50, 16, 73), (-52, 2, 77), (-54, -12, 81), (-56, -20, 83),       # leg 3, north
        (-59, -24, 84),                                                    # hairpin
        (-61, -14, 87), (-62, -6, 90), (-66, -9, 94), (-70, -12, 98)]      # leg 4, up to the gate
MARKET = [(-47, -8), (-35, -10), (-33, 4), (-36, 12), (-47, 10)]
MARKET_Y = 64

# ---- the Eyrie's ways: the Knife from Crownhold, the Goat Stair from the valley ---------------------------
KNIFE = [(-76, -38, 98), (-68, -46, 96), (-62, -54, 94), (-56, -62, 92)]
GOAT_STAIR = [(-27, -62, 46), (-32, -55, 50), (-37, -61, 55), (-35, -70, 60), (-40, -76, 65), (-43, -67, 70),
              (-39, -59, 75), (-44, -55, 80), (-48, -61, 85), (-46, -65, 89), (-48, -69, 92)]

# ---- the valley -------------------------------------------------------------------------------------------
VALLEY_ROAD = [(-12, 0, 44), (-16, 6, 44), (-19, 14, 45), (-20, 22, 45)]
NORTH_PATH = [(-16, -2, 44), (-20, -18, 45), (-23, -34, 46), (-26, -50, 46), (-27, -62, 46)]
FIELDS = [[(-22, -40), (-12, -44), (-11, -30), (-19, -24)],
          [(-24, -58), (-12, -62), (-10, -48), (-20, -42)],
          [(-30, 66), (-18, 62), (-14, 78), (-26, 84)]]
BRIDGE = dict(x0=-14, z=-0.5, half=2)           # Kingsbridge, along x across the river, symmetric
FORDS = [-74, 73]                               # stepping stones across the river; each half builds both
MILL = (-20, 50)
GREEN = (-15, 32)                                # Wendfoot green, at the foot of the Wend

# ---- under the mountain -----------------------------------------------------------------------------------
UNDERHALL = [(-106, -26), (-86, -36), (-64, -32), (-48, -14), (-46, 10), (-58, 30), (-84, 32), (-108, 16)]
HALL_FLOOR = 20
DEEPMERE = [(-106, 2), (-92, -2), (-82, 8), (-84, 24), (-98, 27), (-108, 16)]
MERE_Y = 19
TEMPLE = (-66, 16)                              # the Hall of Echoes: monument B
LOWER_GATE = [(-118, -22), (-108, -26), (-104, -14), (-110, -4), (-118, -8)]
DEEP_STAIR = (-86, -28)                         # a spiral shaft from Crownhold to Underhall
UNDERGATE = [(-104, -14, 20), (-90, -16, 20), (-74, -14, 20), (-58, -8, 20), (-54, 4, 20), (-60, 12, 20)]
MINE_ROAD = [(-29, -36, 46), (-37, -41, 42), (-45, -35, 37), (-44, -25, 32), (-50, -17, 26), (-55, -10, 21)]
DELVING = [(-48, 6, 20), (-34, 4, 19), (-18, 2, 18), (-0.5, -0.5, 18)]

# ---- objectives and spawns --------------------------------------------------------------------------------
SPAWN_TOP = (-84, -18)                          # Crownhold's court
SPAWN_LOW = (-112, -14)                         # the Lower Gate
MON_A = (-54, -70)                              # the Eyrie
MON_B = TEMPLE

# ---- glass clouds: (x, z, y, length, width, heading in degrees) -------------------------------------------
CLOUDS = [(-96, -70, 118, 26, 11, 20), (-40, -86, 117, 20, 9, -15), (-70, 44, 119, 30, 12, 35),
          (-20, 30, 121, 22, 9, 70), (-110, 74, 117, 18, 8, 0), (-56, -40, 120, 16, 7, 50)]

PLACES = [
    dict(key="crown", name="Crownhold", poly=CROWN, kind="citadel",
         what="the citadel on the summit: curtain walls, four towers, a keep set at an angle, the gatehouse",
         why="red's spawn (the top one); the head of the Wend, the Knife and the Deep Stair"),
    dict(key="eyrie", name="the Eyrie", poly=EYRIE, kind="objective",
         what="a tower on the north spur, the monument in its open crown", why="RED MONUMENT A"),
    dict(key="town", name="Wendholm", poly=TOWN, kind="town",
         what="the town on the valley face: houses along the Wend's four legs, set to the road's angle",
         why="the main way up, and cover the whole way"),
    dict(key="market", name="Market Cross", poly=MARKET, kind="plaza",
         what="the market square on the second leg: a cross, a well, stalls",
         why="the middle of the climb"),
    dict(key="shoulder", name="Tarnhollow", poly=TARN, kind="water",
         what="a tarn on the south shoulder, shelving shores, reeds", why="the head of Millbrook"),
    dict(key="valley", name="the Vale", poly=[(-30, -96), (-6, -96), (-6, 95), (-42, 95), (-28, 34), (-24, 6),
                                              (-27, -22), (-30, -46), (-27, -72)], kind="valley",
         what="the floodplain: fields set at angles, the mill, the fords", why="the ground between the towns"),
    dict(key="underhall", name="Underhall", poly=UNDERHALL, kind="cavern",
         what="the delved city under the mountain, its houses cut at angles, round Deepmere", why="the lower town"),
    dict(key="mere", name="Deepmere", poly=DEEPMERE, kind="cavern-water",
         what="the lake in the cavern, shelving to gravel and clay shores", why="frames the lower spawn"),
    dict(key="lowergate", name="the Lower Gate", poly=LOWER_GATE, kind="spawn",
         what="the second spawn: a gate hall at the cavern's west end", why="red's lower spawn"),
]
POINTS = [
    dict(key="temple", name="the Hall of Echoes", at=TEMPLE, why="RED MONUMENT B"),
    dict(key="bridge", name="Kingsbridge", at=(-8, 0), why="the middle crossing"),
    dict(key="mill", name="the Mill", at=MILL, why="where Millbrook meets the river"),
    dict(key="green", name="Wendfoot", at=GREEN, why="the green at the Wend's foot: three houses at 0, 12 and 45 degrees"),
    dict(key="minedoor", name="Delver's Door", at=MINE_ROAD[0][:2], why="the valley's way into Underhall"),
    dict(key="stair", name="the Deep Stair", at=DEEP_STAIR, why="Crownhold to Underhall, eighty steps"),
    dict(key="gallery", name="the Weeping Gallery", at=(-1, -1), why="the Delving's middle, under the river"),
]
ROUTES = [
    dict(name="the Wend", kind="road", pts=WEND, half=2),
    dict(name="the Knife", kind="path", pts=KNIFE, half=1),
    dict(name="the Goat Stair", kind="stair", pts=GOAT_STAIR, half=1),
    dict(name="the Valley Road", kind="road", pts=VALLEY_ROAD, half=2),
    dict(name="the North Path", kind="path", pts=NORTH_PATH, half=1),
]
TUNNELS = [
    dict(name="the Mine Road", pts=MINE_ROAD, half=1, height=4),
    dict(name="the Delving", pts=DELVING, half=2, height=5),
    dict(name="Undergate", pts=UNDERGATE, half=2, height=0),
]
