"""Slatefold: a capture-the-wool board for two teams of twelve, a slate-quarrying hamlet on two terraced hillsides
that face each other across a band of void the teams build over. Each team keeps two wools:

    the Kiln         a red brick kiln house on the Quarry Floor, an island east of the hill, reached over the Cart
                     Gantry (a trestle of stairs and a landing) from the Cart Yard; a bedrock wall across the landing
    the Winding House an engine house with its headframe on the High Bench, a ledge out to the north-west at 82,
                     reached by the Winding Path (three flights and two landings up the hill's west flank); a
                     bedrock wall across the last landing

Red holds the north (z < 0), blue is red's mirror, z' = -1 - z (Symmetry("mirror_z")). Heights: H is the y of the
floor block, a player stands at H + 1. The hill steps down toward the band in four terraces, each four blocks below
the one behind it, and each flight is at most three stair blocks, four blocks of climb:

    spawn terrace   74   the Quarry Office; the iron, the two monuments
    cottage terrace 70   the Terrace Row, the Chapel
    cart yard       66   spoil heaps, the weighbridge, the cart track
    front terrace   62   the Dressing Floor: slate racks for cover, the front line to the band
    quarry floor    58   the island; the pit at 54; the Kiln beside it
    high bench      82   the Winding House

    PIECES / build()   the plan raster, both halves; ZONES the build zones (void a player may build over)
    objectives()       teams, spawns, observer, the four wools
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

BOARD = "slatefold"
X_MIN, X_MAX = -88, 79
Z_MIN, Z_MAX = -108, 107
SYM = Symmetry("mirror_z")
KILL_Y = 36
MAX_BUILD = 104
FOUNDATION = 6
BIOME = 5                                   # taiga: a cold green grass and leaf beside grey slate

SPAWN_H, ROW_H, YARD_H, FRONT_H, QUARRY_H, PIT_H, BENCH_H = 74, 70, 66, 62, 58, 54, 82
LAND1_H, LAND2_H = 74, 78                   # the Winding Path's two landings

SPAWN_AT = (0, SPAWN_H + 1, -93)
OBSERVER_AT = (0, 96, 0)
MONUMENT_SLOTS = [(-15, SPAWN_H + 1, -86), (15, SPAWN_H + 1, -86)]        # red's two, on the Quarry Office's lawn

KILN = (54, -74, 65, -62)                   # the kiln house, walls included: x0, z0, x1, z1
CHIMNEYS = [("kiln", (63, -72), QUARRY_H + 20), ("kiln", (56, -72), QUARRY_H + 16), ("wind", (-73, -88), BENCH_H + 15)]
HEADFRAME = (-70, -98, -66, -94)           # the winding gear: four legs and a wheel, on the bench
KILN_DOOR = (54, -68, 54, -68)              # one cell in its west wall
WIND = (-80, -96, -71, -86)                 # the engine house, walls included
WIND_DOOR = (-71, -91, -71, -91)            # one cell in its east wall
ROOM_H = 6                                  # interior height, floor to ceiling
WALL_G = dict(x0=28, x1=29, z0=-60, z1=-55, height=3)      # the Cart Gantry's wall: bedrock, 2 thick, 3 high
WALL_W = dict(x0=-60, x1=-59, z0=-85, z1=-79, height=3)    # the Winding Path's wall on its second landing


def red_half(x, z):
    return z < 0


def P(*pts):
    return list(pts)


# ---- red's pieces: (key, name, kind, polygon or (x0, z0, x1, z1), floor) ------------------------------------
PIECES = [
    ("spawn", "the Quarry Office terrace", "spawn", P((-36, -106), (30, -106), (32, -96), (30, -82), (-36, -82), (-38, -96)), SPAWN_H),
    ("row", "the Terrace Row", "row", P((-46, -81), (14, -81), (14, -64), (-46, -64)), ROW_H),
    ("yard", "the Cart Yard", "yard", P((-52, -63), (20, -63), (20, -48), (-52, -48)), YARD_H),
    ("front", "the Dressing Floor", "front", P((-52, -47), (40, -47), (42, -32), (34, -14), (-34, -14), (-50, -24), (-54, -38)), FRONT_H),
    ("quarry", "the Quarry Floor", "quarry", P((34, -61), (35, -69), (44, -78), (56, -78), (66, -75), (68, -66), (66, -58), (56, -55), (34, -55)), QUARRY_H),
    ("pit", "the Pit", "pit", (41, -70, 50, -60), PIT_H),
    ("land1", "the Chapel Landing", "landing", (-58, -75, -50, -63), LAND1_H),
    ("land2", "the Second Landing", "landing", (-60, -85, -50, -79), LAND2_H),
    ("bench", "the High Bench", "bench", (-80, -98, -64, -79), BENCH_H),
    ("gantry-land", "the Cart Gantry landing", "landing", (24, -60, 30, -55), 62),
]
PIECE = {p[0]: p for p in PIECES}

# flights: (name, start (x, z), rises, width (a, b), h0, n); a flight's cells climb one block each
FLIGHTS = [
    # spawn terrace down to the row (rises north): west, centre, east
    ("spawn W", (-29, -79), "n", (0, 6), ROW_H + 1, 3), ("spawn C", (-3, -79), "n", (0, 6), ROW_H + 1, 3),
    ("spawn E", (8, -79), "n", (0, 6), ROW_H + 1, 3),
    # row down to the yard
    ("row W", (-40, -61), "n", (0, 6), YARD_H + 1, 3), ("row C", (-3, -61), "n", (0, 6), YARD_H + 1, 3),
    ("row E", (8, -61), "n", (0, 6), YARD_H + 1, 3),
    # yard down to the front terrace
    ("yard W", (-44, -45), "n", (0, 6), FRONT_H + 1, 3), ("yard C", (-3, -45), "n", (0, 6), FRONT_H + 1, 3),
    ("yard E", (12, -45), "n", (0, 6), FRONT_H + 1, 3),
    # the Cart Gantry: yard (66) to the landing (62), landing to the quarry (58); rises toward the yard (west)
    ("gantry A", (23, -55), "w", (0, 5), 63, 3), ("gantry B", (33, -55), "w", (0, 5), 59, 3),
    # the Pit's two ways in (rises away from the pit)
    ("pit W", (40, -61), "w", (0, 4), PIT_H + 1, 3), ("pit S", (47, -59), "s", (0, 4), PIT_H + 1, 3),
    # the Winding Path: row to the first landing, to the second, to the bench
    ("path a", (-47, -65), "w", (0, 4), ROW_H + 1, 3), ("path b", (-57, -76), "n", (0, 4), LAND1_H + 1, 3),
    ("path c", (-61, -79), "w", (0, 4), LAND2_H + 1, 3),
]

# the spoil heaps: (centre x, centre z, radius, height above the floor): cones a player climbs a block at a time
HEAPS = [(-30, -55, 6, 5, "yard"), (-12, -53, 5, 4, "yard"), (46, -75, 3, 3, "quarry"), (-28, -101, 5, 4, "spawn")]
# knolls of turf: grass-topped swells of two or three blocks on the lawns, off every lane
KNOLLS = [(-33, -98, 4, 2), (26, -99, 4, 2), (-47, -20, 5, 3), (36, -24, 5, 3), (-46, -40, 4, 2), (37, -40, 4, 2),
          (-76, -83, 5, 3), (-74, -97, 4, 2)]

# build zones: void a player may build over, red's half (the image is drawn by the mirror)
ZONES = [("band", "the band", (-60, -13, 60, -1)), ("bay-w", "the West Bay", (-72, -40, -53, -14)),
         ("bay-e", "the East Bay", (41, -40, 60, -14))]

COLOURS = {"void": (24, 30, 44), "spawn": (200, 200, 188), "row": (170, 176, 160), "yard": (150, 156, 150),
           "front": (160, 168, 150), "quarry": (126, 130, 134), "pit": (96, 100, 106), "landing": (180, 170, 140),
           "bench": (150, 180, 130), "stair": (140, 130, 120), "heap": (110, 112, 116), "barrier": (20, 20, 20),
           "wall": (150, 80, 70), "room": (236, 214, 190), "door": (240, 230, 200), "rail": (120, 100, 70)}
KINDS = ["void", "spawn", "row", "yard", "front", "quarry", "pit", "landing", "bench", "stair", "heap", "barrier",
         "wall", "room", "door"]
WALK = {"spawn", "row", "yard", "front", "quarry", "pit", "landing", "bench", "stair", "heap", "room", "door"}
PLACES = [("THE QUARRY OFFICE", (0, -100)), ("monument", (-15, -86)), ("monument", (15, -86)),
          ("the Terrace Row", (-18, -72)), ("the Chapel", (-41, -74)), ("the Cart Yard", (-16, -56)),
          ("the weighbridge", (8, -55)), ("the Dressing Floor", (-6, -30)), ("the front", (0, -17)),
          ("the Cart Gantry", (25, -58)), ("the Quarry Floor", (45, -66)), ("the Pit", (45, -65)),
          ("THE KILN", (60, -68)), ("the Winding Path", (-54, -71)), ("land 2", (-54, -82)),
          ("the High Bench", (-70, -90)), ("WINDING HOUSE", (-75, -91)), ("the band", (0, -7))]


def grown(poly):
    """A polygon given by its corner cells, grown half a cell outward so the cells on its boundary are inside."""
    cx = sum(p[0] for p in poly) / len(poly)
    cz = sum(p[1] for p in poly) / len(poly)
    return [(x + 0.5 * (1 if x > cx else -1), z + 0.5 * (1 if z > cz else -1)) for x, z in poly]


def piece_cells(R, g):
    """The mask of a piece given as a rectangle (x0, z0, x1, z1) or a polygon of corner cells."""
    from pgmvox import shapes
    if isinstance(g, tuple):
        x0, z0, x1, z1 = g
        return (R.X >= x0) & (R.X <= x1) & (R.Z >= z0) & (R.Z <= z1)
    return shapes.inside(R.X, R.Z, grown(g))


def mirror_x(x):
    return -1 - x


@lru_cache(maxsize=1)
def build():
    """The plan raster, both halves: pieces, flights, heaps, the two houses' walls and their doorways, the walls."""
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    for key, _, kind, g, h in PIECES:
        R.where(piece_cells(R, g), h, kind)
    floor_of = {k: h for k, _, _, _, h in PIECES}
    R.base_floor = lambda x, z: floor_of[next(p[0] for p in PIECES if p[2] == R.kind(x, z))]
    for _, start, rises, width, h0, n in FLIGHTS:
        R.flight(start, rises, width, h0, n)
    # a bank behind the spawn: four rows rising one block every row (walkable), the hill going on up
    for z in range(-106, -102):
        for x in range(-30, 31):
            R.cell(x, z, SPAWN_H + (-102 - z), "heap")
    for cx, cz, r, hh, key in HEAPS:
        if r == 0:
            continue
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                d = np.hypot(x - cx, z - cz)
                if d <= r and R.kind(x, z) in ("yard", "quarry", "spawn", "heap"):
                    R.cell(x, z, int(R.h(x, z) if R.kind(x, z) != "heap" else R.h(x, z)) + int(round(hh * (1 - d / (r + 0.5)))) + 0, "heap")
    R.grass_heap = set()
    for cx, cz, r, hh in KNOLLS:
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                d = np.hypot(x - cx, z - cz)
                if d <= r and R.kind(x, z) in ("spawn", "front", "bench", "row"):
                    R.cell(x, z, R.base_floor(x, z) + int(round(hh * (1 - d / (r + 0.5)))), "heap")
                    R.grass_heap.add((x, z))
    R.base, R.piece = R.H.copy(), R.K.copy()
    # the two houses: a ring of wall round an interior, a doorway of two cells
    for (x0, z0, x1, z1), door, key in ((KILN, KILN_DOOR, "kiln"), (WIND, WIND_DOOR, "wind")):
        floor = QUARRY_H if key == "kiln" else BENCH_H
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                ring = x in (x0, x1) or z in (z0, z1)
                R.cell(x, z, floor + ROOM_H if ring else floor, "wall" if ring else "room")
        for x in range(door[0], door[2] + 1):
            for z in range(door[1], door[3] + 1):
                R.cell(x, z, floor, "door")
    for g in (WALL_G, WALL_W):
        for x in range(g["x0"], g["x1"] + 1):
            for z in range(g["z0"], g["z1"] + 1):
                R.cell(x, z, R.h(x, z) + g["height"], "barrier")
    return R


def zone_mask(R, keys=None):
    m = np.zeros(R.H.shape, bool)
    for key, _, (x0, z0, x1, z1) in ZONES:
        if keys is None or key in keys:
            m |= (R.X >= x0) & (R.X <= x1) & (R.Z >= z0) & (R.Z <= z1)
            m |= (R.X >= x0) & (R.X <= x1) & (R.Z >= -1 - z1) & (R.Z <= -1 - z0)
    return m & R.mask("void")


def objectives():
    """Red keeps the Kiln's orange and the Winding House's cyan; blue takes them and carries them to its own two
    monuments, the images of the slots below. Blue's rooms hold magenta and yellow, red's to take."""
    O = Objectives(Teams(("red-team", "Red", "red", 12), ("blue-team", "Blue", "blue", 12)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=Box(-38, 0, -106, 32, 127, -82),
                protect=("iron ore",)))
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    kx0, kz0, kx1, kz1 = KILN
    wx0, wz0, wx1, wz1 = WIND
    kiln_room = Box(kx0 + 1, QUARRY_H + 1, kz0 + 1, kx1 - 1, QUARRY_H + ROOM_H - 1, kz1 - 1)
    wind_room = Box(wx0 + 1, BENCH_H + 1, wz0 + 1, wx1 - 1, BENCH_H + ROOM_H - 1, wz1 - 1)
    (ax, ay, az), (bx, by, bz) = MONUMENT_SLOTS
    ia, ib = SYM.point(ax, az), SYM.point(bx, bz)
    O.add(Wool("blue-team", "orange", slot=(ia[0], ay, ia[1]), found=(60, QUARRY_H + 1, -68), room=kiln_room,
               spawn_at=(60, QUARRY_H + 2, -66)), color="magenta")
    O.add(Wool("blue-team", "cyan", slot=(ib[0], by, ib[1]), found=(-76, BENCH_H + 1, -91), room=wind_room,
               spawn_at=(-76, BENCH_H + 2, -89)), color="yellow")
    return O


def links():
    """Plan-walk edges a flight does not give: none (every join is a flight or a shared edge)."""
    return []
