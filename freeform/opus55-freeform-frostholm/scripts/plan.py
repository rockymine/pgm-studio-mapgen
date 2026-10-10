"""Frostholm's plan (second version, after the author's look at the first): a winter landscape, mostly land,
played corner to corner along a band. Red holds the north-west, blue the south-east; blue's half is red's
turned half a circle about the centre, (x, z) -> (-1 - x, -1 - z).

Two narrow straits a side cross the band at right angles to the line between the spawns — Ravnsund off each
home island, and Midsund, the lead between the teams, through the middle — cutting it into four landmasses:
red's home, red's middle, blue's middle, blue's home. Straits are frozen in stretches and open in others.

Coordinates are world x, z (north is -z). u = x - z runs along a strait; x + z runs from red to blue.
"""
import math

X_MIN, X_MAX = -90, 89
Z_MIN, Z_MAX = -90, 89
BAND = 116                 # the board is |x - z| < BAND: the corners off the diagonal are cut away
WATER_Y = 47               # the straits' surface; their ice is at this height too
LAND_Y = 50                # the lowland


def rot(x, z):
    return -1 - x, -1 - z


# ---- the straits: x + z = c + wander(u), half-width w; frozen where u is in `ice` ----------------------
STRAITS = [
    dict(key="ravnsund", name="Ravnsund", c=-66, w=5.5, ice=[(-40, -15), (3, 40)], end=-52),
    dict(key="midsund", name="Midsund", c=-1, w=4.5, ice=[(-78, -46), (46, 78)]),
]


def wander(u, key):
    """Odd in u for the middle strait, so the half-turn maps it onto itself."""
    if key == "midsund":
        return 5.0 * math.sin(u * 2 * math.pi / 96.0) + 2.0 * math.sin(u * 2 * math.pi / 41.0)
    return 4.0 * math.sin(u * 2 * math.pi / 70.0 + 1.3) + 2.0 * math.sin(u * 2 * math.pi / 29.0)


# ---- objectives ---------------------------------------------------------------------------------------
SPAWN = (-64, -64)
BEACON = (-17, -67)        # the lighthouse on Ravnsodde, the headland over Ravnsund; its lantern is lit, empty
CORE = (-28, -58)          # the core: on open ground south-west of the lighthouse, on a plinth over a pit
CORE_GROUND = 55           # the plinth's top course
PIT_DEPTH = 7              # the pit under the core: its floor is this far under the plinth
MONUMENT = (-58, -20)      # on Holmstein, the rock knoll on Kaldvatn's shore
LAKE = (-70, -26)

PLACES = [
    dict(key="hall", name="Jarlshall", at=SPAWN, r=9,
         what="Red's spawn: a long hall of dark timber on a stone plinth, the crags at its back",
         why="spawn; its doors look out over the island", how="its two doors"),
    dict(key="crags", name="Ulvefjell", at=(-80, -80), r=10,
         what="sea crags in the corner, snow on their ledges", why="the back wall of the spawn", how="not climbed without blocks"),
    dict(key="beacon", name="The Beacon", at=BEACON, r=6,
         what="a stone lighthouse on the headland over Ravnsund; its lantern is lit, and the core stands in the open beside it",
         why="the landmark the core stands by", how="the headland path; its stair; the strait below"),
    dict(key="core", name="The Beacon Core", at=CORE, r=5,
         what="red's core: obsidian round lava, hanging three blocks over a stone brick plinth in the open snow south-west of the lighthouse",
         why="RED CORE", how="the headland path and the snowfield"),
    dict(key="lake", name="Kaldvatn", at=LAKE, r=10,
         what="a frozen lake in a hollow of the snowfields, ice-fishing huts on it", why="frames the monument; its ice is the open approach",
         how="the lake path"),
    dict(key="holmstein", name="Holmstein", at=MONUMENT, r=5,
         what="a rock knoll on the lake's east shore with standing stones round its foot", why="RED MONUMENT",
         how="up the knoll from the lake ice, the wood or the road"),
    dict(key="wood", name="Granskog", at=(-80, -44), r=12,
         what="pine and spruce between the hall and the lake", why="cover from the hall to the monument", how="the lake path"),
    dict(key="northwood", name="Nordskog", at=(-40, -78), r=10,
         what="pine on the north shore toward the headland", why="cover on the way to the Beacon", how="the headland path"),
    dict(key="bridge", name="The Old Bridge", at=(-40, -26), r=5,
         what="a timber trestle bridge over Ravnsund", why="the one dry crossing between home and the middle", how="the bridge road"),
    dict(key="whaler", name="The Whaler", at=(-25, -42), r=7,
         what="a three-master frozen into Ravnsund's ice", why="cover and height on the strait", how="over the ice"),
    dict(key="village", name="Skarvik", at=(-16, -14), r=13,
         what="a fishing village on the middle island: boathouses on Midsund, drying racks, a stave church, the smithy, longhouses",
         why="cover the whole way over the middle island", how="the bridge road"),
    dict(key="tingholm", name="Tingholm", at=(-0.5, -0.5), r=7,
         what="a rock islet in Midsund with a ring of standing stones", why="the stepping stone over the lead", how="from Skarvik's pier"),
    dict(key="kraak", name="Kraakodde", at=(38, -60), r=9,
         what="the middle island's north-east point: a ruined watchtower", why="the high ground over the north-east crossings", how="the point path"),
    dict(key="sealers", name="Sealers' Point", at=(-60, 38), r=9,
         what="the middle island's south-west point: a sealers' hut, its boats drawn up", why="the south-west crossing", how="the point path"),
]

ROUTES = [
    dict(name="Headland Path", kind="path", pts=[(-56, -66), (-44, -72), (-30, -72), (-18, -66)]),
    dict(name="Lake Path", kind="path", pts=[(-66, -56), (-76, -44), (-72, -34), (-62, -24)]),
    dict(name="Bridge Road", kind="road", pts=[(-58, -58), (-50, -46), (-48, -28), (-30, -25), (-22, -22), (-16, -18)]),
    dict(name="Point Path NE", kind="path", pts=[(-12, -24), (4, -38), (22, -50), (34, -58)]),
    dict(name="Point Path SW", kind="path", pts=[(-24, -12), (-38, 4), (-50, 22), (-58, 34)]),
]
