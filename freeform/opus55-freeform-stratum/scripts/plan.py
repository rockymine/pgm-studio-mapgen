"""Stratum's plan: a brutalist city of floating masses above a sea of cloud, over a painted land.

Three layers, top to bottom:
  the city, y 62 to 118 — concrete masses with patterned faces, joined by a few skyways, the rest of the
      gaps to be bridged;
  the cloud sea, y 44 to 54 — glass, broken, so the land shows through; everything below y 58 kills;
  the land, y 6 to 40 — rolling hills laid in swathes of colour, a lake, woods, and the city's own geometry
      stuck into it: the spawn's pylons coming down to the ground, a monolith driven in at a slant, a fallen
      obelisk, a cube half sunk in the lake.

Red holds the west (x < 0), blue the east; blue's half is red's mirrored across x = -0.5, (x, z) -> (-1 - x, z).
Every mass is a footprint polygon extruded between two heights; a facade preset says how its faces are
patterned. A skyway is a polyline with its deck heights at the ends.
"""

X_MIN, X_MAX = -100, 99
Z_MIN, Z_MAX = -72, 71
KILL_Y = 58                 # below this a player dies: the cloud sea and the land are not played on
CLOUD_Y = (44, 54)
LAKE_Y = 16
MAX_BUILD = 122


def mir(x, z):
    return -1 - x, z


def rect(x0, z0, x1, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def octagon(cx, cz, r):
    import math
    return [(cx + r * math.cos(math.radians(22.5 + 45 * k)), cz + r * math.sin(math.radians(22.5 + 45 * k)))
            for k in range(8)]


# ---- the city ----------------------------------------------------------------------------------------
SPAWN = (-80, 0)
ATRIUM = rect(-93, -13, -67, 13)
ATRIUM_COURT = rect(-87, -7, -73, 7)
COURT_Y = 80
PYLONS = [rect(-92, -12, -89, -9), rect(-71, -12, -68, -9), rect(-92, 9, -89, 12), rect(-71, 9, -68, 12)]

PLAZA = [(-68, -60), (-45, -59), (-43, -41), (-66, -39)]          # the Obelisk's plaza, a skewed slab
OBELISK = rect(-59, -52, -54, -47)
OBELISK_TOP = 118
MONUMENT_Y = 100                                                   # on a balcony cut into the east face

REACTOR = octagon(-56, 48, 10.5)
REACTOR_HOLLOW = octagon(-56, 48, 7.0)
CORE_Y = 84                                                        # the core's lowest course

COLUMNS = [dict(c=(-41, -17), top=98), dict(c=(-47, 0), top=106), dict(c=(-41, 17), top=92)]
COLUMN_HALF = 2                                                    # 5 by 5

FORUM = rect(-26, -9, 25, 8)                                       # self-mirrored across the seam
FORUM_COURT = rect(-10, -4, 9, 3)
FORUM_Y = 80

GATE = dict(x0=-14, x1=13, z0=-52, z1=-48, y0=68, y1=94, bar=4)  # a square frame standing across the seam, its foot a bridge
LENS = dict(outer=rect(-13, 38, 12, 61), inner=rect(-6, 45, 5, 54), y0=70, y1=74)

ZIGGURAT = dict(c=(-29, -46), tiers=[(9, 64, 68), (7, 68, 72), (5, 72, 76), (3, 76, 80)])
CANTILEVER = dict(core=rect(-35, 42, -27, 50), core_y=(62, 88), arm=rect(-26, 43, -16, 49), arm_y=(84, 88))

MASSES = [
    dict(key="atrium", name="the Atrium", poly=ATRIUM, y0=76, y1=88, style="atrium", role="spawn"),
    dict(key="plaza", name="the Obelisk's plaza", poly=PLAZA, y0=72, y1=78, style="slab", role="monument"),
    dict(key="obelisk", name="the Obelisk", poly=OBELISK, y0=78, y1=OBELISK_TOP, style="obelisk", role="monument"),
    dict(key="reactor", name="the Reactor", poly=REACTOR, y0=66, y1=96, style="reactor", role="core"),
    dict(key="forum", name="the Forum", poly=FORUM, y0=74, y1=FORUM_Y, style="slab", role="middle"),
    dict(key="cantilever", name="the Cantilever", poly=CANTILEVER["core"], y0=62, y1=88, style="tower", role="south flank"),
]

SKYWAYS = [
    dict(name="the North Skyway", pts=[(-74, -14), (-62, -25), (-58, -38)], y=(80, 78), half=2),
    dict(name="the South Skyway", pts=[(-74, 14), (-62, 26), (-57, 36)], y=(80, 80), half=2),
]

# ---- the land below ----------------------------------------------------------------------------------
LAKE = [(-24, -26), (-8, -32), (7, -32), (23, -26), (28, -6), (23, 18), (7, 28), (-8, 28), (-24, 18), (-29, -6)]
# fragments of the city stuck into the land: (kind, centre x, z, size, yaw degrees, tilt degrees)
FRAGMENTS = [
    dict(kind="monolith", at=(-74, -52), size=(5, 30, 9), yaw=20, tilt=24),
    dict(kind="fallen-obelisk", at=(-40, 46), size=(6, 34, 6), yaw=-35, tilt=80),
    dict(kind="sunk-cube", at=(-13, -12), size=(11, 11, 11), yaw=27, tilt=18),
    dict(kind="ring", at=(-88, 50), size=(16, 16, 4), yaw=0, tilt=62),
    dict(kind="slab", at=(-50, -20), size=(18, 3, 10), yaw=-12, tilt=8),
]

PLACES = [
    dict(key="atrium", name="the Atrium", poly=ATRIUM, layer="city",
         what="a hollow square of concrete, the court open to the sky, four pylons down to the land",
         why="RED SPAWN", y="76-88, court 80"),
    dict(key="obelisk", name="the Obelisk", poly=PLAZA, layer="city",
         what="a skewed plaza and an obelisk of glyph-cut concrete, a stair round it, the monument on a balcony",
         why="RED MONUMENT", y="plaza 78, balcony 100, top 118"),
    dict(key="reactor", name="the Reactor", poly=REACTOR, layer="city",
         what="an octagonal tower, hollow, the core hung over a shaft open to the void", why="RED CORE", y="66-96, core 84"),
    dict(key="columns", name="the Columns", poly=rect(-50, -20, -38, 20), layer="city",
         what="three pillars with stairs wound round them, 92 to 106 high", why="the high ground over the middle",
         y="62-106"),
    dict(key="forum", name="the Forum", poly=FORUM, layer="city",
         what="the long slab astride the seam, a colonnade down each side, a sunken court with a glyph floor",
         why="THE MIDDLE", y="80"),
    dict(key="gate", name="the Gate", poly=rect(-14, -52, 13, -48), layer="city",
         what="a square frame 26 high standing across the seam; its foot is a bridge", why="the north crossing", y="68-94"),
    dict(key="lens", name="the Lens", poly=LENS["outer"], layer="city",
         what="a square ring lying flat across the seam", why="the south crossing", y="74"),
    dict(key="ziggurat", name="the Ziggurat", poly=rect(-38, -55, -20, -37), layer="city",
         what="four stepped tiers", why="the north flank, toward the enemy's Obelisk", y="64-80"),
    dict(key="cantilever", name="the Cantilever", poly=rect(-35, 42, -13, 50), layer="city",
         what="a tower with a slab thrown out from its head toward the Lens", why="the south flank, toward the enemy's Reactor",
         y="62-88"),
    dict(key="lake", name="the Mirror", poly=LAKE, layer="land",
         what="a lake under the Forum, shelving shores, the sunk cube in it", why="seen through the clouds", y="16"),
]
