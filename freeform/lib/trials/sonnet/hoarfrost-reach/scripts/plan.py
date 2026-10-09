"""Hoarfrost Reach: a capture-the-wool board of ice-capped headlands standing out of a frozen sea. Each team starts
on a timber-hall headland at its back, comes down to a strand with a frozen pond in it, and has two wool rooms to
defend and two to take: the Lighthouse, a tower on its own stack at the strand's west end behind a twelve-block
gap, and the Ice Hall at the top of a nine-wide glacier stair at the east end. Between the two teams lies a band
the teams build across, with two floes in it for stepping stones.

Red holds the north (z < 0). Blue is red's mirror across the band, z' = -1 - z: pgmvox's Symmetry("mirror_z").
Heights follow the library: H is the y of the floor block, a player stands at H + 1.

    PIECES   red's pieces as polygons, each its own kind in the raster
    build()  the plan Raster (ground storey) with its flights, storey 1 for the two wool rooms' floors
    objectives()   teams, spawns, the four wools with their rooms and monuments, drawn once for red
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox import shapes  # noqa: E402
from pgmvox.build import Frame, House  # noqa: E402
from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402
from pgmvox.shapes import inside as poly_inside  # noqa: E402

BOARD = "hoarfrost-reach"
X_MIN, X_MAX = -88, 87
Z_MIN, Z_MAX = -100, 99
SYM = Symmetry("mirror_z")
KILL_Y = 44                      # below this a fall kills; the floes lie under it
MAX_BUILD = 118
SEA_Y = 30                       # the pack ice's deck
FOUNDATION = 5

SPAWN_AT = (0, 76, -84)
OBSERVER_AT = (0, 100, 0)
MONUMENT_Y = 76                  # the slots, on the skald's floor 75


def red_half(x, z):
    return z < 0


def P(*pts):
    return list(pts)


# ---- red's pieces: (key, name, class, polygon or (x0, z0, x1, z1), floor) ------------------------------------
PIECES = [
    ("skald", "the Skald headland", "spawn", P((-34, -98), (34, -98), (37, -82), (31, -66), (-31, -66), (-37, -82)), 75),
    ("balcony", "the Skald's balcony", "spawn", (-8, -66, 8, -63), 75),
    ("strand", "the Strand", "hub", P((-41, -58), (-37, -63), (37, -63), (41, -58), (41, -48), (37, -43), (-37, -43),
                                      (-41, -48)), 72),
    ("cause-w", "the West Causeway", "cause", (-55, -57, -41, -53), 72),
    ("cause-e", "the East Causeway", "cause", (41, -57, 49, -53), 72),
    ("bridge-w", "the West Breakwater Bridge", "bridge", (-22, -43, -18, -37), 71),
    ("bridge-e", "the East Breakwater Bridge", "bridge", (18, -43, 22, -37), 71),
    ("front", "the Breakwater", "front", (-36, -36, 36, -28), 70),
    ("leg-w", "the West Leg", "front", (-36, -27, -26, -17), 70),
    ("leg-e", "the East Leg", "front", (26, -27, 36, -17), 70),
    ("floe-1", "the Outer Floe", "floe", (-48, -11, -42, -5), 69),
    ("floe-2", "the Inner Floe", "floe", (-20, -11, -14, -5), 69),
    ("lighthouse", "the Lighthouse stack", "lighthouse", P((-87, -61), (-79, -66), (-70, -62), (-68, -55), (-71, -47),
                                                          (-79, -44), (-87, -49)), 72),
    ("icefall", "the Icefall shelf", "icefall", P((50, -63), (74, -63), (75, -54), (74, -45), (50, -45)), 72),
    ("glacier", "the Glacier landing", "glacier", (58, -77, 66, -67), 92),
    ("hall", "the Ice Hall", "hall", (54, -90, 70, -78), 92),
]
PIECE = {p[0]: p for p in PIECES}
HOLE = (0, -53, 6.5)                 # the strand's frozen pond: centre x, z, radius (void)
GLACIER = dict(x0=58, x1=66, z_from=-47, z_to=-66, h0=73)        # the stair: a flight climbing north, 9 wide
FLIGHTS = [((-12, -63), "n", (-2, 2), 73, 3), ((12, -63), "n", (-2, 2), 73, 3)]   # the skald's two stairs to the strand
HALL_SKALD = (-12, -89, 11, -79)     # the skald's hall, walls included: x0, z0, x1, z1
HOUSES = [
    dict(key="skald-hall", rect=HALL_SKALD, door="s", style="skald", floor=75, inside=True, storeys=1),
    dict(key="shed-w", rect=(-33, -61, -27, -56), door="s", style="shed", floor=72, storeys=1),
    dict(key="shed-e", rect=(27, -61, 33, -56), door="s", style="shed", floor=72, storeys=1),
]
TOWER = (-82, -59, -74, -51)         # the lighthouse's walls: x0, z0, x1, z1 (9 by 9)
TOWER_DOOR = (-74, -55)              # a doorway in its east wall
TOWER_LADDER = (-78, -52)            # the ladder up inside, against the south wall
ROOM_Y = 94
HALL_BOX = (54, -90, 70, -78)

# where blocks may be placed over the void; every other void stays uncrossable all match
ZONES = [("band", "the band", (-46, -16, 45, 15)), ("gap-w", "the Lighthouse gap", (-68, -58, -56, -52))]

COLOURS = {"void": (22, 26, 40), "spawn": (236, 238, 242), "hub": (200, 214, 226), "cause": (170, 200, 222),
           "bridge": (150, 180, 214), "front": (186, 200, 216), "floe": (210, 228, 240),
           "lighthouse": (214, 220, 230), "icefall": (190, 214, 232), "glacier": (160, 196, 226),
           "hall": (150, 230, 240), "stair": (150, 140, 130), "tower": (90, 100, 120), "inside": (230, 200, 150),
           "door": (240, 230, 200), "room": (120, 220, 235), "ice": (120, 190, 235)}
KINDS = ["void"] + [p[0] for p in PIECES] + ["stair", "tower", "inside", "door", "room"]
KIND_COLOURS = {p[0]: COLOURS[p[2]] for p in PIECES} | {k: COLOURS[k] for k in ("void", "stair", "tower", "inside", "door", "room")}
WALK = {p[0] for p in PIECES} | {"stair", "inside", "door", "room"}

PLACES = [("the Skald's Hall", (0, -88)), ("the Strand", (0, -53)), ("frozen pond", (0, -53)),
          ("the Breakwater", (0, -32)), ("West Leg", (-31, -22)), ("East Leg", (31, -22)),
          ("the Lighthouse", (-78, -55)), ("West Causeway", (-48, -55)), ("East Causeway", (45, -55)),
          ("Glacier Stair", (62, -72)), ("Ice Hall", (62, -84)), ("the Icefall shelf", (62, -52)),
          ("Outer Floe", (-45, -8)), ("Inner Floe", (-17, -8))]


STYLES = {
    "skald": dict(ground=[(98, 0), (4, 0), (98, 0)], upper=[(5, 1)], post=1, gable=(5, 1), floor=(5, 1),
                  roof=(80, 0), stair=156, slab=(44, 7), door=193, window=(102, 0), chimney=(4, 0)),
    "shed": dict(ground=[(5, 1)], upper=[(5, 1)], post=1, gable=(5, 1), floor=(5, 1), roof=(80, 0), stair=156,
                 slab=(44, 7), door=193, window=(102, 0), chimney=(4, 0)),
}


def spec(h):
    x0, z0, x1, z1 = h["rect"]
    nx, nz = x1 - x0 + 1, z1 - z0 + 1
    if h["door"] in "ns":
        heading, Lh, W, sign = 0, nx, nz, (1 if h["door"] == "s" else -1)
    else:
        heading, Lh, W, sign = 90, nz, nx, (1 if h["door"] == "w" else -1)
    return dict(cx=(x0 + x1 + 1) / 2, cz=(z0 + z1 + 1) / 2, heading=heading, L=Lh, W=W, door=sign)


def door_cell(s):
    fr = Frame(s["cx"], s["cz"], s["heading"])
    m, X, Z, U, V = fr.mask(s["L"], s["W"])
    wall = shapes.boundary(m, diagonal=True)
    cands = [(abs(U[i, k]), int(X[i, k]), int(Z[i, k])) for i, k in zip(*np.nonzero(wall))
             if s["door"] * V[i, k] > s["W"] / 2 - 1 and abs(U[i, k]) < s["L"] / 2 - 1.5]
    _, x, z = min(cands)
    return x, z


@lru_cache(maxsize=1)
def houses():
    """Red's buildings as the library's House with footprint and door cell, keyed. Blue's are the mirror."""
    out = {}
    for h in HOUSES:
        s = spec(h)
        cells = Frame(s["cx"], s["cz"], s["heading"]).cells(s["L"], s["W"])
        hs = House(s["cx"], s["cz"], s["heading"], L=s["L"], W=s["W"], floor=h["floor"], storeys=h["storeys"],
                   storey=5 if h["style"] == "skald" else 4, style=STYLES[h["style"]], door=s["door"], chimney=False,
                   roof="gable", overhang=1)
        out[h["key"]] = dict(spec=h, house=hs, cells=cells, door=door_cell(s), floor=h["floor"])
    return out


def box_cells(box):
    x0, z0, x1, z1 = box
    return {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}


def piece_mask(R, key):
    p = PIECE[key]
    g = p[3]
    if isinstance(g, tuple):
        x0, z0, x1, z1 = g
        return (R.X >= x0) & (R.X <= x1) & (R.Z >= z0) & (R.Z <= z1)
    return poly_inside(R.X, R.Z, g)


@lru_cache(maxsize=1)
def build():
    """The plan raster: red's pieces drawn at their floors (the image drawn by the symmetry), the pond a void
    hole, the flights, the glacier stair, the tower's walls and doorway, and storey 1: the two rooms."""
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    for key, _, _, g, h in PIECES:
        if h is None:
            continue
        if isinstance(g, tuple):
            x0, z0, x1, z1 = g
            R.rect(x0, x1, z0, z1, h, key)
        else:
            R.poly(g, h, key)
    cx, cz, rr = HOLE
    R.where((R.X - cx) ** 2 + (R.Z - cz) ** 2 <= rr * rr, 0, "void")
    for start, rises, width, h0, n in FLIGHTS:
        R.flight(start, rises, width, h0, n)
    g = GLACIER
    R.flight((g["x0"] + 4, g["z_from"]), "n", width=(-4, 4), h0=g["h0"], n=92 - g["h0"] + 1)
    # the skald hall: walls round an interior at the headland's floor, a doorway on the south (the strand's side)
    for key, b in houses().items():
        x0_, z0_, x1_, z1_ = b["spec"]["rect"]
        for x in range(x0_, x1_ + 1):
            for z in range(z0_, z1_ + 1):
                ring = x in (x0_, x1_) or z in (z0_, z1_)
                R.cell(x, z, b["floor"], "tower" if ring or not b["spec"].get("inside") else "inside")
        R.cell(b["door"][0], b["door"][1], b["floor"], "door")
    # the tower: walls round an interior at the island's floor, a doorway on the east
    x0, z0, x1, z1 = TOWER
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            R.cell(x, z, 72, "tower" if ring else "inside")
    R.cell(TOWER_DOOR[0], TOWER_DOOR[1], 72, "door")
    # storey 1: the two rooms' floors
    U = R.storey(1)
    U.rect(x0 + 1, x1 - 1, z0 + 1, z1 - 1, ROOM_Y, "room")
    hx0, hz0, hx1, hz1 = HALL_BOX
    return R


def stair_top():
    return 92


def zone_mask(R, keys=None):
    """The build zones over the raster, both halves: a box's image under the mirror is its z range turned."""
    m = np.zeros(R.H.shape, bool)
    for key, _, (x0, z0, x1, z1) in ZONES:
        if keys is None or key in keys:
            m |= (R.X >= x0) & (R.X <= x1) & (R.Z >= z0) & (R.Z <= z1)
            m |= (R.X >= x0) & (R.X <= x1) & (R.Z >= -1 - z1) & (R.Z <= -1 - z0)
    return m & R.mask("void")


def links():
    """The ladder inside the lighthouse, floor to room, both ways; mirrored for blue."""
    out = []
    a = (TOWER_LADDER[0], TOWER_LADDER[1])
    b = (a[0], a[1], 1)
    for p, q in ((a, b), (tuple(int(v) for v in SYM.point(*a)), tuple(int(v) for v in SYM.point(*a)) + (1,))):
        out += [(p, q, ROOM_Y - 72, "ladder"), (q, p, ROOM_Y - 72, "ladder")]
    return out


def objectives():
    """Teams, spawns, the observer and the four wools: red's two rooms (the Lighthouse's cyan, the Ice Hall's
    orange) are captured by blue and placed on blue's monuments, which are the images of the two slots drawn here on
    red's skald; the image wools (purple, yellow) are blue's, taken by red."""
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=Box(-34, 0, -98, 34, 127, -64), protect=True))
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    lh = Box(TOWER[0] + 1, ROOM_Y, TOWER[1] + 1, TOWER[2] - 1, ROOM_Y + 6, TOWER[3] - 1)
    hall = Box(HALL_BOX[0] + 1, 92, HALL_BOX[1] + 1, HALL_BOX[2] - 1, 98, HALL_BOX[3] - 1)
    # blue's monuments are the images of red's two slots: (-16, -80) and (16, -80) on the skald's front lawn
    O.add(Wool("blue-team", "cyan", slot=(-16, MONUMENT_Y, 79), found=(-78, ROOM_Y + 1, -55), room=lh,
               spawn_at=(-78, ROOM_Y + 2, -57)), color="purple")
    O.add(Wool("blue-team", "orange", slot=(16, MONUMENT_Y, 79), found=(62, 93, -84), room=hall,
               spawn_at=(62, 94, -82)), color="yellow")
    return O
