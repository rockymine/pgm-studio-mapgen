"""Lantern Karst, ported onto pgmvox: a capture-the-wool board of floating karst islands, two wools a team.

The plan is the original's (freeform/opus55-freeform-lantern-karst/PLAN.md), piece for piece and block for
block, drawn as a `Raster` with its half turn: red holds the north (z < 0), blue's half is red's turned half a
circle, (x, z) -> (-1 - x, -1 - z). Each piece is its own kind, so the checker, the sketch and the generator
all read which piece a column belongs to from the raster itself.

    the spawn       three terraces (70, 72, 74) up from two exits (67/68) to the hub
    the hub         the Tea Court at 66, a ring round a 16 x 16 sinkhole
    the front       the Gate Terrace at 65 on two Stairs at 64, down to the band (a build zone) and the Bell Rock
    the Pillar      an F (the Long Terrace and two Arms) round a pit (a build zone); the shrine on a pillar at 74,
                    16 off each Arm and the Terrace; two Ledges at 46, twenty down; the Mist Steps (a build zone)
    the Store       an F (the Tea Rows, the Drying Floor, the Store Road climbing 66 -> 69) to the Store at 70,
                    a bedrock wall across the road; the Tea Steps (a build zone)

Joins of two blocks between pieces are drawn as stair flights in the plan (`joins`), so the plan walk climbs
them and is stopped by the retaining walls beside them, as the built world is.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

X_MIN, X_MAX = -112, 111
Z_MIN, Z_MAX = -128, 127
KILL_Y = 40                 # below this a fall kills; the mist lies under it
MIST_Y = (24, 38)
MAX_BUILD = 92
FOUNDATION = 6              # the bedrock course, this far under every floor
SYM = Symmetry("half")


def red_half(x, z):
    """Red's half of the board: the plan is drawn here and turned onto blue's. The sketch's paler half is z >= 0."""
    return z < 0


# ---- the pieces: (key, name, class, (x0, z0, x1, z1) inclusive, floor) -- red's; blue's are the half turn ----
# The class decides the sketch colour and the generator's paint; the key is the piece's kind in the raster.
PIECES = [
    ("leg-w", "the West Stair", "front", (-28, -26, -11, -12), 64),
    ("leg-e", "the East Stair", "front", (10, -26, 27, -12), 64),
    ("bar", "the Gate Terrace", "front", (-28, -38, 27, -27), 65),
    ("hub", "the Tea Court", "hub", (-32, -78, 31, -39), 66),
    ("neck-w", "the West Lantern Steps", "spawn", (-20, -86, -9, -79), None),
    ("neck-e", "the East Lantern Steps", "spawn", (8, -86, 19, -79), None),
    ("sp-front", "the Monument Terrace", "spawn", (-20, -98, 19, -87), 70),
    ("sp-mid", "the Pool Terrace", "spawn", (-16, -110, 15, -99), 72),
    ("sp-back", "the Pavilion of Arrival", "spawn", (-10, -120, 9, -111), 74),
    ("f-stem", "the Long Terrace", "lane", (-92, -73, -33, -60), 66),
    ("f-west", "the Far Arm", "lane", (-92, -97, -83, -74), 67),
    ("f-east", "the Near Arm", "lane", (-42, -97, -33, -74), 67),
    ("pillar", "the Pillar Shrine", "wool", (-66, -97, -59, -90), 74),
    ("ledge-w", "the West Ledge", "ledge", (-75, -82, -70, -76), 46),
    ("ledge-e", "the East Ledge", "ledge", (-55, -82, -50, -76), 46),
    ("w-1", "Mist Step I", "islet", (-50, -29, -45, -24), 63),
    ("w-2", "Mist Step II", "islet", (-68, -29, -63, -24), 64),
    ("w-3", "Mist Step III", "islet", (-50, -47, -45, -42), 64),
    ("w-4", "Mist Step IV", "islet", (-68, -47, -63, -42), 65),
    ("rows", "the Tea Rows", "lane", (32, -50, 49, -39), 66),
    ("drying", "the Drying Floor", "lane", (32, -78, 49, -67), None),
    ("road", "the Store Road", "lane", (50, -96, 63, -39), None),
    ("store", "the Tea Store", "wool", (47, -110, 66, -97), 70),
    ("e-1", "Tea Step I", "islet", (44, -27, 49, -22), 64),
    ("e-2", "Tea Step II", "islet", (62, -27, 67, -22), 65),
    ("bell", "the Bell Rock", "rock", (-5, -5, 4, 4), 68),
]
PIECE = {p[0]: p for p in PIECES}
HOLE = (-8, -66, 7, -51)                       # the Tea Court's sinkhole

# the floors that are not one height: the Store Road's climb, the Drying Floor's ramp, the spawn's exits
FLOORS = {
    "road": [((50, -58, 63, -39), 66), ((50, -66, 63, -59), 67), ((50, -78, 63, -67), 68), ((50, -96, 63, -79), 69)],
    "drying": [((32, -78, 37, -67), 66), ((38, -78, 43, -67), 67), ((44, -78, 49, -67), 68)],
    "neck-w": [((-20, -82, -9, -79), 67), ((-20, -86, -9, -83), 68)],
    "neck-e": [((8, -82, 19, -79), 67), ((8, -86, 19, -83), 68)],
}

# where blocks may be placed over the void; every other void stays uncrossable all match
ZONES = [("band", "the band", (-57, -11, 56, 10)), ("pit", "the Pillar's pit", (-82, -97, -43, -74)),
         ("w-steps", "the Mist Steps", (-70, -59, -43, -12)), ("e-steps", "the Tea Steps", (40, -38, 69, -12))]

# the Store's prepared line: two thick across the road, three of bedrock and one of cobweb, crossed by building
WALL = dict(x0=50, x1=63, z0=-83, z1=-82, height=3)
# the Store's own walls in the plan (so the walk goes in by the door): a ring round the room, the door 12 wide
STORE_BOX = (47, -110, 66, -97)
STORE_DOOR = (51, 62)

# the monuments: on the Monument Terrace between its two exits, the floor at 70 and the slot over it
MONUMENT_Y = 71
SPAWN_AT = (-1, 73, -105)
OBSERVER_AT = (0, 90, 0)

COLOURS = {"void": (34, 38, 52), "front": (196, 180, 150), "hub": (128, 170, 96), "spawn": (205, 190, 160),
           "lane": (140, 178, 104), "wool": (240, 240, 240), "ledge": (100, 120, 180), "islet": (150, 150, 140),
           "rock": (190, 190, 200), "stair": (150, 140, 120), "storewall": (110, 80, 60), "barrier": (20, 20, 20)}
KIND_COLOURS = {k: COLOURS[c] for k, _, c, _, _ in PIECES} | {k: COLOURS[k] for k in ("void", "stair", "storewall",
                                                                                          "barrier")}
WALK = {k for k, *_ in PIECES} | {"stair"}
KINDS = ["void"] + [p[0] for p in PIECES] + ["stair", "storewall", "barrier"]


def rect(R, box, h, kind, both=True):
    """The original's rectangles are (x0, z0, x1, z1); Raster.rect takes (x0, x1, z0, z1)."""
    x0, z0, x1, z1 = box
    R.rect(x0, x1, z0, z1, h, kind, both)


def joins(R):
    """Every two-block step between neighbouring floors on red's half, made a flight of stairs as the original's
    builder made it: the whole run when it is 14 or narrower, else a flight of 10 in its middle and a retaining
    wall either side. Draws the flights into the raster (both halves) and returns them for the generator:
    [(cells of the flight, the side it rises toward, lower floor)], [retaining-wall cells on the upper side]."""
    land = ~R.mask("void")
    runs = {}
    for i, k in np.argwhere(land):
        x, z = int(R.X[i, k]), int(R.Z[i, k])
        if not red_half(x, z):
            continue
        for d, (dx, dz) in (("e", (1, 0)), ("w", (-1, 0)), ("s", (0, 1)), ("n", (0, -1))):
            a, b = i + dx, k + dz
            if 0 <= a < R.nx and 0 <= b < R.nz and land[a, b] and R.H[a, b] - R.H[i, k] == 2:
                runs.setdefault((d, int(R.H[i, k])), []).append((x, z))
    flights, walls = [], []
    for (d, lo), cells in runs.items():
        along = 0 if d in ("n", "s") else 1                     # a run lies across its climb
        cells.sort(key=lambda c: (c[1 - along], c[along]))
        groups, cur = [], []
        for c in cells:
            if cur and (c[1 - along] != cur[-1][1 - along] or c[along] != cur[-1][along] + 1):
                groups.append(cur)
                cur = []
            cur.append(c)
        groups.append(cur)
        for g in groups:
            n = len(g)
            a, b = (0, n) if n <= 14 else ((n - 10) // 2, (n - 10) // 2 + 10)
            flights.append((g[a:b], d, lo))
            dx, dz = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}[d]
            walls += [(x + dx, z + dz) for x, z in g[:a] + g[b:]]
            for x, z in g[a:b]:
                R.flight((x, z), d, h0=lo + 1, n=2)
    return flights, walls


def build():
    """The plan raster, both halves, and the joins the generator lays."""
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    for key, _, _, box, h in PIECES:
        if key in FLOORS:
            for sub, hh in FLOORS[key]:
                rect(R, sub, hh, key)
        else:
            rect(R, box, h, key)
    rect(R, HOLE, 0, "void")
    # what the generator builds the ground from: every column's floor and piece before the Store's walls, the
    # stairs and the bedrock wall are drawn over them (a Raster keeps one floor and one kind a column)
    R.floor, R.piece = R.H.copy(), R.K.copy()
    x0, z0, x1, z1 = STORE_BOX                                   # the Store's walls, all but the door
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            if ring and not (z == z1 and STORE_DOOR[0] <= x <= STORE_DOOR[1]):
                R.cell(x, z, 78, "storewall")
    flights, walls = joins(R)
    for x in range(WALL["x0"], WALL["x1"] + 1):
        for z in range(WALL["z0"], WALL["z1"] + 1):
            R.cell(x, z, R.h(x, z) + WALL["height"] + 1, "barrier")
    return R, flights, walls


def zone_mask(R, keys=None):
    """The build zones over the raster (both halves), less the land in them: where a bridge may be built."""
    from pgmvox.shapes import inside
    m = np.zeros(R.H.shape, bool)
    for key, _, (x0, z0, x1, z1) in ZONES:
        if keys is None or key in keys:
            m |= _box_mask(R, (x0, z0, x1, z1))
            m |= _box_mask(R, (-1 - x1, -1 - z1, -1 - x0, -1 - z0))     # its half turn, by hand (see below)
    return m & R.mask("void")


def _box_mask(R, box):
    """A rectangle of whole blocks as a mask. Its image is taken by hand: Symmetry.point rounds a half-block
    corner with Python's round(), so (-57.5, -11.5) goes to (56, 10) but (57.5, ...) to (-58, ...)."""
    x0, z0, x1, z1 = box
    return (R.X >= x0) & (R.X <= x1) & (R.Z >= z0) & (R.Z <= z1)


def objectives():
    """Teams, spawns and the four wools, drawn once for red's rooms: a Wool's team is the team that captures it,
    so red's lime is blue's to take and place on blue's monument; its image is red's to take from blue's room."""
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=Box(-20, 0, -120, 19, 127, -79),
                protect=("iron block",)))                         # its iron is mined and grows back
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    pillar_room = Box(-66, 75, -97, -59, 91, -90)
    store_room = Box(47, 71, -110, 66, 83, -97)
    # blue's monuments are the images of red's, (-4, -89) and (3, -89) on red's Monument Terrace
    O.add(Wool("blue-team", "lime", slot=(3, MONUMENT_Y, 88), found=(-63, 75, -94), room=pillar_room,
               spawn_at=(-63, 76, -92)), color="magenta")
    O.add(Wool("blue-team", "yellow", slot=(-4, MONUMENT_Y, 88), found=(56, 71, -106), room=store_room,
               spawn_at=(56, 72, -104)), color="orange")
    return O


PLACES = [("the Pavilion of Arrival", (0, -116)), ("the Tea Court", (0, -45)), ("the Gate Terrace", (0, -33)),
          ("the Bell Rock", (0, 6)), ("the Long Terrace", (-62, -66)), ("the Far Arm", (-88, -100)),
          ("the Near Arm", (-37, -100)), ("PILLAR", (-62, -101)), ("the Mist Steps", (-57, -36)),
          ("the Tea Rows", (40, -44)), ("the Drying Floor", (40, -73)), ("the Store Road", (75, -60)),
          ("TEA STORE", (56, -114)), ("the Tea Steps", (55, -18))]
