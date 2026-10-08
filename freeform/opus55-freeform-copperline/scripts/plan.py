"""Copperline — a payload plan: a mining railway pushed up a valley, from the rail yard to the mine, in three legs.

The attackers (red) push an ore cart along the line; the defenders (blue) stop it. A payload is a control point
that moves: the cart stands on the track, and while attackers stand within its radius and no defender does, it
rolls forward along the rails; left alone it rolls back. Each leg is its own length of track and its own cart,
and the next cart cannot be pushed until the leg before it is done:

    A  Main Street   from the rail yard up the town's main street, along Station Road, into the station
    B  the Gorge     from the station along the brow, then north over the trestle bridge and up the cutting
    C  the Mine Head from the depot up the shelf along the mountainside, through the portal into the mine hall

Each leg's ground gives the attackers three ways forward that are not the same way: the track itself, which is
where the cart is and where the fight is; a way above it; and a way below it or round it. When a leg is done the
attackers' spawn moves up to its end and the defenders' falls back to the next one.

The plan is a height raster with a kind for every column, an upper raster for what spans over something else
(the two bridges over the gorge), the track as waypoints, and lists of what a raster cannot hold: the ladders,
stair towers and the adit as connectors, the houses, the spawns. The checker lays the rails and traces them
the way PGM's Track does, walks each leg from both spawns, and the sketch draws all of it.

    heights are the top block a player stands on: 24 the rail yard, 26 the town and the brow, 12 the riverbed
    (the river over it, two deep), 26 the bridges' decks, 28 the north bank, 36 the mine yard and the mine
    hall; a rail stands one above its cell
"""
import numpy as np

X_MIN, X_MAX = -56, 55
Z_MIN, Z_MAX = -72, 71
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
ROCK = 60
KINDS = {"rock": 0, "yard": 1, "street": 2, "ground": 3, "house": 4, "track": 5, "bed": 6, "stair": 7,
         "river": 8, "floor": 9, "wall": 10, "gate": 11, "heap": 12, "platform": 13, "cover": 14, "bumper": 15}
WALK = {"yard", "street", "ground", "track", "bed", "stair", "river", "floor", "heap", "platform"}


def ix(x):
    return x - X_MIN


def iz(z):
    return z - Z_MIN


class Raster:
    def __init__(self):
        self.H = np.full((NX, NZ), ROCK, int)
        self.K = np.full((NX, NZ), KINDS["rock"], int)
        self.U = np.full((NX, NZ), -1, int)
        self.stair = {}
        self.gate = {}                                  # (x, z) -> the stage whose fall opens it

    def rect(self, x0, x1, z0, z1, h, kind="street"):
        self.H[ix(x0):ix(x1) + 1, iz(z0):iz(z1) + 1] = h
        self.K[ix(x0):ix(x1) + 1, iz(z0):iz(z1) + 1] = KINDS[kind]

    def gates(self, x0, x1, z0, z1, h, opens):
        self.rect(x0, x1, z0, z1, h, "gate")
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                self.gate[(x, z)] = opens

    def flight_x(self, xs, z0, z1, h0, step, rises):
        for k, x in enumerate(xs):
            for z in range(z0, z1 + 1):
                self.H[ix(x), iz(z)] = h0 + k * step
                self.K[ix(x), iz(z)] = KINDS["stair"]
                self.stair[(x, z)] = rises

    def flight_z(self, zs, x0, x1, h0, step, rises):
        for k, z in enumerate(zs):
            for x in range(x0, x1 + 1):
                self.H[ix(x), iz(z)] = h0 + k * step
                self.K[ix(x), iz(z)] = KINDS["stair"]
                self.stair[(x, z)] = rises


# ---- the track ------------------------------------------------------------------------------------------------
# Each leg is a list of waypoints (x, z, h): h is the height of the cell under the rail. Consecutive waypoints
# share an x or a z. A waypoint where the line turns is a curve; one where it runs on is a plain straight. A leg
# that rises climbs on its last cells: n cells of sloped rail before a waypoint n higher, so every curve and
# every waypoint is flat. Between two legs a bumper block stands on the line, so PGM's trace of one leg stops at
# its end and the next leg's trace starts away from it.
LEGS = [
    dict(key="A", id="checkpoint-a", name="Main Street",
         pts=[(8, 66, 24), (8, 56, 24), (8, 53, 26), (8, 34, 26), (-12, 34, 26), (-12, 14, 26)]),
    dict(key="B", id="checkpoint-b", name="the Gorge",
         pts=[(-12, 12, 26), (-12, 4, 26), (2, 4, 26), (2, 0, 26), (16, 0, 26), (16, -20, 26), (16, -23, 28),
              (16, -24, 28)]),
    dict(key="C", id="checkpoint-c", name="the Mine Head",
         pts=[(16, -26, 28), (16, -38, 28), (10, -38, 28), (5, -38, 32), (-2, -38, 32), (-7, -38, 36),
              (-20, -38, 36), (-20, -47, 36), (-12, -47, 36), (-12, -66, 36)]),
]
BUMPERS = [(-12, 13, 26), (16, -25, 28)]
FACE = {(0, -1): "N", (0, 1): "S", (1, 0): "E", (-1, 0): "W"}
CURVE = {frozenset("SE"): 6, frozenset("SW"): 7, frozenset("NW"): 8, frozenset("NE"): 9}
SLOPE = {"E": 2, "W": 3, "N": 4, "S": 5}


def sign(v):
    return (v > 0) - (v < 0)


def lay(leg):
    """The leg's cells in order: (x, z, h, rail data), h the height of the cell under the rail."""
    pts = leg["pts"]
    cells = [[pts[0][0], pts[0][1], pts[0][2], None]]
    for (x0, z0, h0), (x1, z1, h1) in zip(pts, pts[1:]):
        assert (x0 == x1) != (z0 == z1), (x0, z0, x1, z1)
        dx, dz = sign(x1 - x0), sign(z1 - z0)
        L = abs(x1 - x0) + abs(z1 - z0)
        n = h1 - h0
        assert 0 <= n <= L - 1, ("a leg only climbs, on its last cells, and ends flat", pts)
        for k in range(1, L + 1):
            slope = k > L - 1 - n and k < L if n else False
            h = h0 + max(0, k - (L - n)) if n else h0
            if k == L:
                h = h1
            cells.append([x0 + dx * k, z0 + dz * k, h, ("slope", FACE[(dx, dz)]) if slope else None])
    out = []
    for i, (x, z, h, s) in enumerate(cells):
        prev = cells[i - 1] if i else None
        nxt = cells[i + 1] if i + 1 < len(cells) else None
        faces = set()
        if prev:
            faces.add(FACE[(prev[0] - x, prev[1] - z)])
        if nxt:
            faces.add(FACE[(nxt[0] - x, nxt[1] - z)])
        if s:
            d = SLOPE[s[1]]
        elif len(faces) == 2 and faces not in ({"N", "S"}, {"E", "W"}):
            d = CURVE[frozenset(faces)]
        else:
            d = 0 if faces <= {"N", "S"} else 1
        out.append((x, z, h, d))
    return out


# ---- the board ------------------------------------------------------------------------------------------------
HOUSES = [  # x0, x1, z0, z1: closed houses, nine high over the street
    (-3, 3, 37, 41), (-3, 3, 44, 47), (-3, 3, 50, 53),                     # Main Street, its west side
    (13, 19, 38, 42), (13, 19, 45, 48), (13, 19, 51, 53),                  # and its east side
    (-16, -8, 38, 43), (-16, -8, 46, 53),                                  # across the back alley
    (-34, -20, 38, 46), (-34, -20, 49, 53),                                # the hotel and the bank
    (12, 20, 14, 22), (-2, 5, 12, 18), (-2, 4, 23, 27), (14, 20, 26, 28),  # round the square: the chapel, shops
]
COVER = [  # x0, x1, z0, z1, height over the ground: wagons, coal stacks, crates, carts, rocks
    (-6, -2, 60, 61, 2), (12, 16, 58, 59, 2), (-14, -10, 64, 65, 2), (30, 34, 54, 55, 2), (0, 2, 66, 67, 1),
    (6, 6, 47, 47, 2), (11, 11, 42, 42, 2), (5, 5, 38, 38, 1), (-5, -5, 44, 44, 2),
    (-3, -1, 31, 31, 1), (16, 18, 31, 32, 2), (-26, -24, 31, 32, 2),
    (-8, -7, 20, 21, 1), (-17, -16, 26, 27, 2), (6, 8, 21, 22, 2),
    (-30, -26, 1, 2, 3), (-8, -6, -1, 0, 2), (4, 6, 7, 8, 2), (22, 25, 0, 2, 3), (-40, -38, -2, -1, 2),
    (6, 8, -27, -26, 2), (-6, -4, -24, -23, 2), (-30, -27, -32, -31, 2), (20, 21, -36, -35, 2),
    (-6, -4, -53, -52, 2), (-30, -27, -50, -48, 3), (0, 2, -55, -54, 2), (20, 24, -54, -52, 2),
    (-26, -25, -44, -43, 2), (-2, 0, -42, -41, 1),
]
HEAP = dict(c=(34, 36), r=13, top=8)                                       # the slag heap, east of the town
TRESTLE = dict(x0=12, x1=20, z0=-20, z1=-4, h=26)                          # the track's bridge, the track on x 16
FOOTBRIDGE = dict(x0=-26, x1=-25, z0=-20, z1=-4, h=26)                     # a plank bridge, the west crossing
WATER_TOWER = (-12, -28)
BUILDINGS = {  # spawn rooms and halls: x0, x1, z0, z1, floor, doors (x0, x1, z0, z1, stage or None)
    "engine-shed": dict(box=(18, 34, 58, 68), floor=24, doors=[(18, 18, 61, 65, "warmup")]),
    "station": dict(box=(-32, -22, 14, 26), floor=26, doors=[(-22, -22, 18, 22, "A")]),
    "depot": dict(box=(22, 32, -34, -26), floor=28, doors=[(22, 22, -32, -28, "B")]),
    "office": dict(box=(28, 40, 0, 12), floor=26, doors=[(28, 28, 4, 8, None), (32, 36, 12, 12, None)]),
    "bunkhouse": dict(box=(36, 48, -34, -24), floor=28, doors=[(36, 36, -31, -27, None), (40, 44, -24, -24, None)]),
    "mine-hall": dict(box=(-33, -7, -71, -59), floor=36, doors=[(-15, -9, -59, -59, None)]),
    "lamp-room": dict(box=(-4, 8, -71, -59), floor=36, doors=[(0, 4, -59, -59, None)]),
}
# what a raster cannot hold: (name, approach, a, b, length) between two cells, each way
CONNECTORS = [
    ("the north ladder", "below", (2, -20), (2, -22), 22),               # up the gorge's north cliff, 16 rungs
    ("the gantry", "above", (4, -27), (4, -51), 50),                       # a stair tower to 42, the gantry over
    #                                                                         the shelf, the headframe's stair down
    ("the adit", "below", (-16, -30), (-30, -66), 42),                      # an old drift under the mine yard,
    #                                                                         into the mine hall's west end
]
# spawns by stage: (x, y, z, yaw)
SPAWNS = {
    "attackers": {"1": (26.5, 25, 63.5, 90), "2": (-27.5, 27, 20.5, -90), "3": (27.5, 29, -30.5, 90)},
    "defenders": {"1": (34.5, 27, 5.5, 180), "2": (42.5, 29, -29.5, 180), "3": (2.5, 37, -65.5, 180)},
}
TIME = "12m"
WARMUP = "20s"
CAPTURE = "60s"
RADIUS = 3.5


def heap_h(x, z):
    d = ((x - HEAP["c"][0]) ** 2 + (z - HEAP["c"][1]) ** 2) ** 0.5
    return 26 + int(min(HEAP["top"], max(0, round(HEAP["r"] - d))))


def build():
    R = Raster()
    # ---- leg A: the rail yard, the town, Station Road, the station --------------------------------------------
    R.rect(-24, 40, 54, 69, 24, "yard")
    R.rect(-24, 40, 54, 54, 25, "yard")                                     # one step up into the town
    R.rect(-36, 24, 8, 53, 26, "street")
    R.rect(25, 44, 8, 21, 26, "street")                                    # the office's yard
    for x in range(HEAP["c"][0] - HEAP["r"], HEAP["c"][0] + HEAP["r"] + 1):
        for z in range(HEAP["c"][1] - HEAP["r"], HEAP["c"][1] + HEAP["r"] + 1):
            if heap_h(x, z) > 26 or (x > 24 and ((x - 34) ** 2 + (z - 36) ** 2) <= 14 ** 2):
                R.rect(x, x, z, z, heap_h(x, z), "heap")
    R.rect(-18, -16, 12, 29, 27, "platform")                               # the station's two platforms
    R.rect(-8, -6, 12, 29, 27, "platform")
    # ---- leg B: the brow, the gorge and its crossings, the north bank -----------------------------------------
    R.rect(-48, 44, -3, 7, 26, "ground")
    R.rect(X_MIN, X_MAX, -20, -4, 12, "river")
    R.flight_x(range(-17, -3), -5, -4, 25, -1, "-x")                       # down the south wall to the river
    for b in (TRESTLE, FOOTBRIDGE):
        R.U[ix(b["x0"]):ix(b["x1"]) + 1, iz(b["z0"]):iz(b["z1"]) + 1] = b["h"]
    R.rect(-48, 50, -36, -21, 28, "ground")
    R.rect(-27, -24, -21, -21, 27, "ground")                               # the footbridge's landing
    R.rect(12, 20, -21, -21, 26, "bed")                                    # the cutting, climbing with the track
    R.rect(12, 20, -22, -22, 27, "bed")
    # ---- leg C: the shelf, the mine yard, the portal and the mine hall ----------------------------------------
    R.rect(13, 30, -40, -37, 28, "ground")
    R.rect(13, 25, -48, -41, 28, "ground")
    R.rect(-44, 12, -58, -37, 36, "yard")
    R.rect(13, 30, -58, -49, 36, "yard")
    R.flight_z(range(-41, -49, -1), 26, 30, 29, 1, "-z")                    # the east ramp, up to the yard
    R.flight_z(range(-29, -37, -1), -34, -32, 29, 1, "-z")                  # the west steps
    for name, b in BUILDINGS.items():
        x0, x1, z0, z1 = b["box"]
        R.rect(x0, x1, z0, z1, b["floor"] + 8, "wall")
        R.rect(x0 + 1, x1 - 1, z0 + 1, z1 - 1, b["floor"], "floor")
        for dx0, dx1, dz0, dz1, st in b["doors"]:
            if st:
                R.gates(dx0, dx1, dz0, dz1, b["floor"], st)
            else:
                R.rect(dx0, dx1, dz0, dz1, b["floor"], "floor")
    # ---- the track and its bed -----------------------------------------------------------------------------
    for leg in LEGS:
        for x, z, h, d in lay(leg):
            for ox in (-1, 0, 1):                                           # the bed is three wide
                for oz in (-1, 0, 1):
                    p, q = x + ox, z + oz
                    k = R.K[ix(p), iz(q)]
                    if k in (KINDS["house"], KINDS["wall"]) or (ox or oz) and k == KINDS["track"]:
                        continue
                    if (ox or oz) and KN[k] in ("river", "floor"):
                        continue
                    if KN[k] == "river" or R.U[ix(p), iz(q)] >= 0:
                        continue
                    R.rect(p, p, q, q, h, "bed" if (ox or oz) else "track")
            if R.U[ix(x), iz(z)] < 0 and KN[R.K[ix(x), iz(z)]] != "floor":
                R.rect(x, x, z, z, h, "track")
    for x, z, h in BUMPERS:
        R.rect(x, x, z, z, h, "bumper")
    for x0, x1, z0, z1 in HOUSES:
        R.rect(x0, x1, z0, z1, int(R.H[ix(x0), iz(z0)]) + 9, "house")
    for x0, x1, z0, z1, tall in COVER:
        R.rect(x0, x1, z0, z1, int(R.H[ix(x0), iz(z0)]) + tall, "cover")
    x, z = WATER_TOWER
    R.rect(x - 1, x + 1, z - 1, z + 1, 28 + 12, "cover")
    return R


KN = {v: k for k, v in KINDS.items()}
