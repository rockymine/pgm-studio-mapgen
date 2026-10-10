"""Abbeymoor: a destroy-the-monument board for two teams of sixteen, two monuments a team, on a high moor joined by land.
Each team holds the hill of a ruined abbey and, below it, an orchard village; between the two lies a peat bog with
standing stones. Red holds the north (z < 0); blue is red's image under the half turn, (x, z) -> (-1 - x, -1 - z).

    Hall Farm       the spawn, at the back, in a hollow with the ridge behind it; a farmhouse, a barn, a sheepfold
    Abbey Hill      a plateau at 80 with the ruined nave on it; Monument A floats over the crossing, in the open sky
    The Crypt       under the nave at 70; the Night Stair down from the chancel, a passage of 60 blocks under the hill
                    and the valley, and the Tithe Barn's cellar stair up into the village near Monument B
    The Village     an orchard village in a valley at 66: a green with Monument B, the Moorcock inn, four cottages,
                    the Tithe Barn, two orchards
    The Bog         a basin across the middle, pools held at 61, the Standing Stones, a boardwalk, the peat cuttings
    Roads           the Drove Road (spawn to the green), the Hill Track (spawn to the abbey's north door), the Monks' Way
                    (green to the abbey's east gap), the Peat Track (village to the boardwalk)

Heights: H is the y of the floor block, a player stands at H + 1. The ground is land.py's; the plan adds the places.

    build()        the raster over the ground (storey 0) and the crypt and its passage (storey 1)
    objectives()   teams, spawns, observer, the four monuments (two a team)
    links()        the stairs between the storeys, as plan-walk edges
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

import land  # noqa: E402
from pgmvox import shapes  # noqa: E402
from pgmvox import terrain as T  # noqa: E402
from pgmvox.build import Frame, House  # noqa: E402
from pgmvox.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.blocks import B  # noqa: E402

BOARD = "abbeymoor"
X_MIN, X_MAX = land.X0, land.X0 + land.NX - 1
Z_MIN, Z_MAX = land.Z0, land.Z0 + land.NZ - 1
SYM = Symmetry("half")
KILL_Y = 8
MAX_BUILD = 120
BIOME = 6                                   # swampland: a dark water, an olive grass, a podzol it meets
PLATEAU = land.PLATEAU
BOG = land.BOG_LEVEL

X, Z, H, LAND, WATERS, WET = land.ground()


def g(x, z):
    """The ground's floor block at a column."""
    return int(H[x - X_MIN, z - Z_MIN])


SPAWN_AT = (0, g(0, -112) + 1, -112)
OBSERVER_AT = (0, 100, 0)
SPAWN_AREA = Box(-24, 0, -130, 24, 140, -100)

# ---- the monuments: a three-block cube of obsidian, two blocks of air over the ground -------------------------------
A_CENTRE = (-40, -72)                       # Monument A, at the abbey's crossing
B_CENTRE = (30, -70)                        # Monument B, on the village green
FLOAT = 3                                   # the cube's lowest course is this far over the floor (a dais under A adds DAIS)
DAIS = 3                                    # Monument A stands over a stepped dais three high, so it clears the nave's walls


def monument_box(cx, cz):
    y = g(cx, cz) + FLOAT + (DAIS if (cx, cz) == A_CENTRE else 0)
    return Box(cx - 1, y, cz - 1, cx + 1, y + 2, cz + 1)


# ---- the abbey: the nave's walls (inclusive), its doors, the tower stump, the stair slot, the crypt ---------------
NAVE = (-54, -78, -29, -66)                 # outer walls x0, z0, x1, z1
NAVE_DOORS = [("north door", (-45, -78, -43, -78)), ("east gap", (-29, -73, -29, -71)), ("south door", (-37, -66, -35, -66))]
TOWER = (-54, -78, -50, -74)                # the crossing tower's stump, in the nave's north-west corner
SLOT = (-41, -70, -31, -68)                 # the Night Stair's slot in the chancel floor, x0, z0, x1, z1
CRYPT = (-53, -77, -42, -67)                # the crypt's outer walls; the hall inside is x -52..-43, z -76..-68
CRYPT_FLOOR = 70
CRYPT_H = 5                                 # floor to ceiling, in air
PASSAGE_Z = -61                             # the passage runs east along this row
BARN_AT = (15, -60)

# the Night Stair: from the crypt's floor (70) up to the nave's (80), x -41 east to -31, three stairs a flight
NIGHT_STAIR = [(-41, 71), (-40, 72), (-39, 72), (-38, 73), (-37, 74), (-36, 75), (-35, 76), (-34, 76), (-33, 77), (-32, 78), (-31, 79)]
# the passage's floor along x (after the crypt's door and its six cells south): flat 70, three flights down, flat 59,
# the cellar stair up in the barn
PASSAGE_FLOORS = {}
for _x in range(-47, -44):
    PASSAGE_FLOORS[_x] = 70
for _x, _y in zip(range(-44, -26), [69, 68, 67, 67, 67, 66, 65, 64, 64, 64, 63, 62, 61, 61, 61, 60, 59, 59]):
    PASSAGE_FLOORS[_x] = _y
for _x in range(-26, 11):
    PASSAGE_FLOORS[_x] = 59
for _x, _y in zip(range(11, 19), [60, 61, 62, 62, 62, 63, 64, 65]):
    PASSAGE_FLOORS[_x] = _y
PASSAGE_SOUTH = [(-48, z) for z in range(-66, PASSAGE_Z)]       # six cells from the crypt's south door to the corner
CELLAR = (11, PASSAGE_Z - 1, 18, PASSAGE_Z + 1)                 # the cellar stair's slot in the Tithe Barn's floor

# ---- the village and the farm: (key, cx, cz, heading, L, W, door side, name) --------------------------------------
HOUSES = [
    ("farmhouse", 0, -120, 0, 12, 7, 1, "the Farmhouse"),
    ("farm-barn", 24, -118, 0, 10, 7, 1, "the Hay Barn"),
    ("c1", 16, -86, 0, 8, 6, 1, "Thorn Cottage"),
    ("c2", 40, -88, 12, 9, 6, 1, "Mill Cottage"),
    ("c3", 47, -70, 90, 8, 6, 1, "Orchard Cottage"),
    ("c4", 12, -76, 0, 8, 6, 1, "Brook Cottage"),
    ("inn", 33, -52, 0, 12, 8, -1, "the Moorcock"),
    ("tithe", 15, -60, 0, 18, 10, 1, "the Tithe Barn"),
]
FOLD = (-22, -112, 7)                        # the sheepfold: a ring of drystone, x, z, radius
ORCHARDS = [("north orchard", (2, -104, 16, -90)), ("south orchard", (40, -60, 56, -44))]
CUTTINGS = [(-44, -42, -18, -40), (-44, -37, -18, -35), (-44, -32, -18, -30)]     # peat trenches, x0, z0, x1, z1
STONES_R = 12                                # the ring of standing stones about the bog's middle
GATE = (-30, -52)                            # a ruined gatehouse on the Monks' Way, at the hill's foot

ROADS = {
    "Drove Road": [(2, -108), (10, -100), (20, -92), (26, -84), (29, -78)],
    "Hill Track": [(-4, -108), (-18, -102), (-28, -92), (-36, -84), (-44, -79)],
    "Monks' Way": [(21, -70), (8, -68), (-8, -70), (-20, -72), (-28, -72)],
    "Peat Track": [(33, -47), (26, -40), (14, -34), (0, -31)],
}
BOARDWALK = [(-1, -31), (-1, -1)]            # two wide, x -1 and 0 once turned

PLACES = [("HALL FARM (spawn)", (0, -118)), ("sheepfold", (-22, -112)), ("the Hill Track", (-24, -94)),
          ("ABBEY HILL", (-42, -72)), ("Monument A", (-40, -72)), ("the Night Stair", (-36, -69)), ("the Crypt", (-48, -72)),
          ("the Gatehouse", (-30, -52)), ("the Drove Road", (14, -98)), ("north orchard", (9, -97)),
          ("Thorn Cottage", (16, -86)), ("the Green", (30, -70)), ("Monument B", (30, -70)), ("Brook Cottage", (12, -76)),
          ("the Tithe Barn", (17, -60)), ("the Moorcock", (33, -52)), ("Orchard Cottage", (47, -70)),
          ("south orchard", (52, -52)), ("the Peat Cuttings", (-31, -36)), ("the Peat Track", (14, -35)),
          ("the Standing Stones", (0, -13)), ("the Bog", (-22, -14)), ("the Beck", (60, -50)), ("the boardwalk", (-1, -16))]

KINDS = ["void", "ground", "steep", "water", "road", "wall", "room", "door", "nave", "ruin", "green", "hole", "stair", "crypt",
         "passage", "boardwalk", "peat", "orchard"]
WALK = {"ground", "steep", "road", "room", "door", "nave", "green", "stair", "crypt", "passage", "boardwalk", "peat", "orchard"}
COLOURS = {"void": (20, 24, 34), "ground": (150, 160, 110), "steep": (130, 130, 124), "water": (60, 90, 120), "road": (190, 176, 140),
           "wall": (150, 100, 80), "room": (225, 205, 175), "door": (240, 230, 200), "nave": (190, 190, 180), "ruin": (120, 120, 126),
           "green": (130, 175, 100), "hole": (60, 60, 70), "stair": (140, 130, 120), "crypt": (100, 90, 110), "passage": (120, 100, 130),
           "boardwalk": (150, 110, 70), "peat": (80, 60, 50), "orchard": (110, 160, 90)}


def door_cell(spec):
    """A house's door as the library will put it: the wall cell nearest the middle of the door's long side."""
    _, cx, cz, heading, L, W, door, _ = spec
    square = heading % 90 == 0
    if square:
        along_x = heading % 180 == 0
        lx, lz = (L, W) if along_x else (W, L)
        cx = np.floor(cx) + (0.5 if lx % 2 else 0)
        cz = np.floor(cz) + (0.5 if lz % 2 else 0)
    fr = Frame(cx, cz, heading)
    m, Xs, Zs, U, V = fr.mask(L, W)
    wall = shapes.boundary(m, diagonal=True)
    cands = [(abs(U[i, k]), int(Xs[i, k]), int(Zs[i, k])) for i, k in zip(*np.nonzero(wall))
             if door * V[i, k] > W / 2 - 1 and abs(U[i, k]) < L / 2 - 1.5]
    _, x, z = min(cands)
    return x, z, fr, m, Xs, Zs


def house(spec):
    key, cx, cz, heading, L, W, door, name = spec
    x, z, fr, m, Xs, Zs = door_cell(spec)
    cells = {(int(Xs[i, k]), int(Zs[i, k])) for i, k in zip(*np.nonzero(m))}
    gx, gz = int(round(cx)), int(round(cz))
    floor = g(gx, gz)
    return dict(spec=spec, cells=cells, door=(x, z), floor=floor, wall=shapes.boundary(m, diagonal=True), mask=(m, Xs, Zs))


@lru_cache(maxsize=1)
def houses():
    return {spec[0]: house(spec) for spec in HOUSES}


def barn_cellar_cells():
    return [(x, z) for x in range(CELLAR[0], CELLAR[2] + 1) for z in range(CELLAR[1], CELLAR[3] + 1)]


@lru_cache(maxsize=1)
def build():
    """The plan raster: the ground as land.py leaves it, kinds by where each place is, and storey 1 under it."""
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    R.H[:] = H
    deg = T.slope_deg(H, LAND)
    K = np.full(H.shape, R.kinds["void"], int)
    K[LAND] = R.kinds["ground"]
    K[LAND & (deg > 52)] = R.kinds["steep"]
    K[WET] = R.kinds["water"]
    R.K[:] = K
    red = Z < 0

    def paint(mask, kind, h=None, both=True):
        for i, k in np.argwhere(mask & red):
            x, z = int(X[i, k]), int(Z[i, k])
            R.cell(x, z, int(R.H[i, k]) if h is None else h, kind, both)
    for name, pts in ROADS.items():
        paint(R.mask("ground", "steep", "water") & ~R.mask("water") & (shapes.polyline(X, Z, pts)[0] <= 1.6), "road")
    paint(shapes.polyline(X, Z, BOARDWALK)[0] <= 0.9, "boardwalk")
    for x0, z0, x1, z1 in CUTTINGS:
        paint((X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1), "peat")
    for _, (x0, z0, x1, z1) in ORCHARDS:
        paint((X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1) & R.mask("ground"), "orchard")
    paint(np.hypot(X - B_CENTRE[0], Z - B_CENTRE[1]) <= 9, "green")
    # the abbey: the nave's floor, its walls as ruin (a player walks through the doors), the tower
    x0, z0, x1, z1 = NAVE
    paint((X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1), "nave", PLATEAU)
    ring = (X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1) & ((X == x0) | (X == x1) | (Z == z0) | (Z == z1))
    paint(ring, "ruin", PLATEAU + 5)
    tx0, tz0, tx1, tz1 = TOWER
    paint((X >= tx0) & (X <= tx1) & (Z >= tz0) & (Z <= tz1), "ruin", PLATEAU + 11)
    for _, (a, b, c, d) in NAVE_DOORS:
        paint((X >= a) & (X <= c) & (Z >= b) & (Z <= d), "door", PLATEAU)
    sx0, sz0, sx1, sz1 = SLOT
    paint((X >= sx0) & (X <= sx1) & (Z >= sz0) & (Z <= sz1), "hole", 0)
    # the houses: a wall ring round a room, the door cell
    for key, hs in houses().items():
        m, Xs, Zs = hs["mask"]
        for i, k in zip(*np.nonzero(m)):
            x, z = int(Xs[i, k]), int(Zs[i, k])
            ring_ = hs["wall"][i, k]
            R.cell(x, z, hs["floor"] + (5 if ring_ else 0), "wall" if ring_ else "room")
        R.cell(hs["door"][0], hs["door"][1], hs["floor"], "door")
    # the barn's cellar slot: a hole in its floor
    for x, z in barn_cellar_cells():
        R.cell(x, z, 0, "hole")
    # storey 1: the crypt hall and its stair, the passage, the cellar stair
    U = R.storey(1)
    hx0, hz0, hx1, hz1 = CRYPT[0] + 1, CRYPT[1] + 1, CRYPT[2] - 1, CRYPT[3] - 1
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            U.cell(x, z, CRYPT_FLOOR, "crypt")
    for x, y in NIGHT_STAIR:
        for z in range(SLOT[1], SLOT[3] + 1):
            U.cell(x, z, y, "stair" if y != 72 and y != 76 else "crypt")
    for x, z in PASSAGE_SOUTH:
        for dx in (-1, 0, 1):
            U.cell(x + dx, z, CRYPT_FLOOR, "passage")
    for x, y in PASSAGE_FLOORS.items():
        for dz in (-1, 0, 1):
            U.cell(x, PASSAGE_Z + dz, y, "passage")
    for x in (-48,):
        for dx in (-1, 0, 1):
            U.cell(x + dx, PASSAGE_Z, CRYPT_FLOOR, "passage")
    return R


def zone_mask(R, keys=None):
    return np.zeros(R.H.shape, bool)


def links():
    """The stairs between the storeys as plan-walk edges: the nave to the Night Stair's head, the cellar stair's head to the
    barn's floor. Each both ways, and for blue."""
    out = []
    ph = houses()["tithe"]["floor"]
    pairs = [((-30, -69), (-31, -69, 1), 2.4), ((19, PASSAGE_Z), (18, PASSAGE_Z, 1), 2.4)]
    for a, b, c in pairs:
        for p, q in ((a, b), (b, a)):
            out.append((p, q, c, "stair"))
            ip = tuple(int(v) for v in SYM.point(*p[:2])) + tuple(p[2:])
            iq = tuple(int(v) for v in SYM.point(*q[:2])) + tuple(q[2:])
            out.append((ip, iq, c, "stair"))
    return out


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=SPAWN_AREA, protect=("iron ore",)))
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    O.add(Destroyable("red-abbey", "Red Abbey Monument", "red-team", monument_box(*A_CENTRE), (B.OBSIDIAN, 0), "obsidian", "50%"),
          name="Blue Abbey Monument")
    O.add(Destroyable("red-village", "Red Village Monument", "red-team", monument_box(*B_CENTRE), (B.OBSIDIAN, 0), "obsidian", "50%"),
          name="Blue Village Monument")
    return O
