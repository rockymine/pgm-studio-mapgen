"""Claywork: a standard capture-the-wool board, grounded, two wools a team.

Every piece stands on the world's floor: its surface, twelve blocks of ground under it, then bedrock down to y 1.
The void between pieces runs to the bottom of the world, so a fall between them is a death. The board is mirrored
north and south across z = -0.5, red holding the north (z < 0); within each half the west and the east wing are
mirror images across x = -0.5, so the two wools of a team are walked the same.

The levels step up from the front to the back in broad steps, each one block up and three blocks deep:

    the front       the Forecourt and the two Aprons at 20, build zones between them; the band before the middle
    the hub         the Clay Court at 23, up the two flights of the Grand Steps either side of the Rostrum
    the Undercroft  under the Court and the Arcades at 17: the well drops into it, a passage three wide runs out
                    under each Arcade as a balcony open toward the spawn, and a ladder climbs to each Walk
    the spawn       the Gatehouse at 27 and its two Statue Terraces out to the Court, the Spawn Steps cut between
    the wings       the Arcades at 23, from the Court out to the Walks
    the walks       the West and East Walks: up from each Apron (20 to 23), along to the Kilns (23 to 26)
    the wools       the West and East Kilns at 26, in the back corners, each behind a bedrock wall across its Walk

    plan()          the raster (both halves), every piece a kind
    objectives()    teams, spawns, the four wools
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

BOARD = "claywork"
X_MIN, X_MAX = -72, 71
Z_MIN, Z_MAX = -104, 103
SYM = Symmetry("mirror_z")                 # (x, z) -> (x, -1 - z): blue's half is red's seen in a mirror

FRONT, HUB, WOOL, SPAWN = 20, 23, 26, 27   # the four levels, floor blocks (a player stands one above)
GROUND = 12                                # blocks of ground under every surface; bedrock below
TREAD = 3                                  # a broad step: one block up, three deep
MAX_BUILD = 44                             # the sky layer: seventeen over the spawn
ROOM_H = 6                                 # a Kiln's walls, floor to roof


def red_half(x, z):
    return z < 0


def mx(x):
    """The west-east mirror inside a half: x -> -1 - x."""
    return -1 - x


# ---- the pieces, red's west side: (key, name, (x0, z0, x1, z1) inclusive, floor or a stepped rule) ----------
# A floor given as ("steps", z_low_edge, h_low, h_high, rising) climbs one block every TREAD rows away from its
# low edge, from h_low (the first row) to h_high (the rest).
PIECES = [
    ("front", "the Forecourt", (-28, -30, 27, -13), FRONT),
    ("apron", "the West Apron", (-72, -30, -53, -13), FRONT),
    ("steps", "the Grand Steps, west flight", (-28, -39, -19, -31), ("steps", -31, FRONT + 1, HUB, "n")),
    ("rostrum", "the Rostrum", (-18, -39, 17, -31), HUB),
    ("hub", "the Clay Court", (-32, -68, 31, -40), HUB),
    ("neck", "the Spawn Steps", (-6, -80, 5, -69), ("steps", -69, HUB + 1, SPAWN, "n")),
    ("spawn", "the Gatehouse", (-16, -100, 15, -81), SPAWN),
    ("terrace", "the West Statue Terrace", (-16, -80, -7, -69), SPAWN),
    ("wing", "the West Arcade", (-60, -64, -33, -53), HUB),
    ("walk", "the West Walk", (-72, -81, -61, -31), None),     # its floor is WALK_FLOORS
    ("kiln", "the West Kiln", (-72, -98, -59, -82), WOOL),
]
WALK_FLOORS = [((-72, -39, -61, -31), ("steps", -31, FRONT + 1, HUB, "n")),
               ((-72, -72, -61, -40), HUB),
               ((-72, -81, -61, -73), ("steps", -73, HUB + 1, WOOL, "n"))]
HOLE = (-7, -62, 6, -51)                   # the Court's well: 14 by 12 of void in the middle of the hub
PIECE = {p[0]: p for p in PIECES}

# the bedrock wall across each Walk, 2 thick and 3 high, just before the Walk climbs to its Kiln
WALL = dict(x0=-72, x1=-61, z0=-72, z1=-71, height=3)
# the Kiln: walls ROOM_H high and a roof, the door 8 wide in its south face onto the Walk
KILN = (-72, -98, -59, -82)
KILN_DOOR = (-70, -63)
# arches: a span over a way, legs one block wide on its edges, clear to ARCH_CLEAR over the floor
ARCH_CLEAR = 5
ARCHES = [("the Grand Steps' arch", "x", (-28, -19), -35), ("the Walk's first arch", "x", (-72, -61), -48),
          ("the Walk's second arch", "x", (-72, -61), -62), ("the Arcade arch", "z", (-64, -53), -46)]

# the band: void a player may build over, between the two front lines, from one Apron's inner edge to the other's;
# nothing is built out in front of an Apron, so the board's edge is no crossing. The flanks are build zones too,
# between the Forecourt and each Apron, the front's full depth, so the front line is joined only by building.
BAND = (-52, -12, 51, 11)
FLANK = (-52, -30, -29, -13)

# the stepping stones: four in the void between each Arcade and the flank zone in front of it, two wide and a
# tread deep, stepping down a level a stone (22, 21, 20, 19) toward the front as the Walk beside them does. Every
# gap is two, the most a running jump one block up clears, so they are crossed both ways: an attacker's way back,
# from a block placed at the zone's edge, two short of the last stone.
STONES = [((-45, -50, -44, -48), 22), ((-45, -45, -44, -43), 21), ((-45, -40, -44, -38), 20),
          ((-45, -35, -44, -33), 19)]

# the Undercroft: a floor UNDER under the Court and the Arcades, three high with a roof three thick over it; the well
# is its pit, open to the sky, a way down only, a pool at its foot to land in: nothing climbs out of it but the
# ladders at the Walks
UNDER = HUB - 6
UNDER_CLEAR = 3
PASSAGE = (-60, -64, -7, -62)              # three wide, from the Arcade's far end to the well, under the floors
LADDER = (-60, -65)                        # the landing past the Arcade's north edge; a ladder up the Walk's face

SPAWN_AT = (0, SPAWN + 1, -92)
# the Gatehouse's iron: a cube three a side in each back corner, two clear of its walls, mined and grown back
IRON_SPAN = 3
IRON = [(-13, -97)]                        # the west cube's low corner; the east is its mirror
MONUMENTS = [(-8, -83), (7, -83)]          # red's two, on the Gatehouse's front edge, west and east
OBSERVER_AT = (0, 50, 0)

COLOURS = {"void": (34, 38, 52), "front": (214, 204, 180), "apron": (214, 204, 180), "rostrum": (226, 220, 202), "under": (120, 92, 70), "stone": (150, 150, 160),
           "terrace": (226, 220, 202), "parapet": (150, 110, 90), "steps": (196, 186, 160),
           "hub": (180, 190, 200), "wing": (170, 180, 192), "walk": (200, 190, 170), "neck": (196, 186, 160),
           "spawn": (232, 226, 210), "kiln": (245, 245, 245), "kilnwall": (150, 110, 90),
           "barrier": (20, 20, 20), "arch": (120, 120, 130)}
KINDS = ["void", "front", "rostrum", "apron", "terrace", "parapet", "under", "stone", "steps", "hub", "wing", "walk", "neck", "spawn", "kiln", "kilnwall",
         "barrier", "arch"]
WALK_KINDS = {"front", "rostrum", "under", "stone", "terrace", "apron", "steps", "hub", "wing", "walk", "neck", "spawn", "kiln"}
PLACES = [("THE GATEHOUSE", (0, -97)), ("statue", (-11, -75)), ("statue", (10, -75)), ("the Clay Court", (-20, -46)),
          ("the well", (0, -56)), ("the Rostrum", (0, -35)), ("the Forecourt", (0, -22)), ("build", (-40, -22)),
          ("the West Apron", (-62, -22)), ("the West Walk", (-66, -55)), ("the West Arcade", (-46, -66)),
          ("WEST KILN", (-66, -101)), ("EAST KILN", (65, -101)), ("the band", (0, 0))]


def _floor(R, box, rule, kind, mirror_x=True):
    """Lay a rectangle at one floor, or as broad steps, on red's side and (mirror_x) its west-east image; the
    raster's own symmetry carries both onto blue's half."""
    x0, z0, x1, z1 = box
    boxes = [(x0, z0, x1, z1)]
    if mirror_x and not (x0 <= -1 and x1 >= 0):
        boxes.append((mx(x1), z0, mx(x0), z1))
    for a0, b0, a1, b1 in boxes:
        for x in range(a0, a1 + 1):
            for z in range(b0, b1 + 1):
                if isinstance(rule, tuple):
                    _, edge, lo, hi, _ = rule
                    h = min(hi, lo + abs(z - edge) // TREAD)
                else:
                    h = rule
                R.cell(x, z, h, kind)


def plan():
    """The raster, both halves. R.floor and R.piece keep each column's ground before the walls are drawn over it."""
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    for key, _, box, rule in PIECES:
        if key == "walk":
            for sub, r in WALK_FLOORS:
                _floor(R, sub, r, key)
        else:
            _floor(R, box, rule, key)
    # the Undercroft: the passage under the Court and the Arcade, its landing, and the well over it. The floors
    # above stay as the first storey, six over the passage: a player walks the Court over the passage's roof
    up = R.storey(1)
    px0, pz0, px1, pz1 = PASSAGE
    for x in range(px0, px1 + 1):
        for z in range(pz0, pz1 + 1):
            for a in (x, mx(x)):
                if R.kind(a, z) != "void":
                    up.cell(a, z, int(R.h(a, z)), R.kind(a, z))
    _floor(R, PASSAGE, UNDER, "under")
    _floor(R, (LADDER[0], LADDER[1], LADDER[0], LADDER[1]), UNDER, "under")
    x0, z0, x1, z1 = HOLE
    R.rect(x0, x1, z0, z1, UNDER, "under")
    for box, h in STONES:
        _floor(R, box, h, "stone")
    R.floor, R.piece = R.H.copy(), R.K.copy()
    # the Kilns' walls, all round but the door; a wall column stands to the roof
    for sign in (1, -1):
        kx0, kz0, kx1, kz1 = KILN
        dx0, dx1 = KILN_DOOR
        if sign < 0:
            kx0, kx1, dx0, dx1 = mx(kx1), mx(kx0), mx(dx1), mx(dx0)
        for x in range(kx0, kx1 + 1):
            for z in range(kz0, kz1 + 1):
                ring = x in (kx0, kx1) or z in (kz0, kz1)
                if ring and not (z == kz1 and dx0 <= x <= dx1):
                    R.cell(x, z, WOOL + ROOM_H, "kilnwall")
    # a parapet two high along each Statue Terrace's edge over the Spawn Steps: the steps are cut down between the
    # terraces, and without it a terrace's edge stands two over the stair's middle, a ledge that looks climbable
    x0, z0, x1, z1 = P_TERRACE = PIECE["terrace"][2]
    for x in (x1, mx(x1)):
        for z in range(z0, z1 + 1):
            R.cell(x, z, SPAWN + 2, "parapet")
    # a parapet along each side of the Rostrum over the Grand Steps, for the same reason
    rx0, rz0, rx1, rz1 = PIECE["rostrum"][2]
    for x in (rx0, rx1):
        for z in range(rz0, rz1 + 1):
            R.cell(x, z, HUB + 2, "parapet")
    # the bedrock walls across the Walks, crossed only by building over them
    for sign in (1, -1):
        a, b = (WALL["x0"], WALL["x1"]) if sign > 0 else (mx(WALL["x1"]), mx(WALL["x0"]))
        for x in range(a, b + 1):
            for z in range(WALL["z0"], WALL["z1"] + 1):
                R.cell(x, z, R.floor[R.ix(x), R.iz(z)] + WALL["height"], "barrier")
    # the arches' legs: one block at each edge of the way they span (a block a player walks round)
    R.arch_legs = []
    for _, axis, (a, b), at in ARCHES:
        for e in (a, b):
            cells = [(e, at)] if axis == "x" else [(at, e)]
            for x, z in cells + [(mx(c[0]), c[1]) for c in cells]:
                R.cell(x, z, R.floor[R.ix(x), R.iz(z)] + ARCH_CLEAR + 2, "arch")
                R.arch_legs.append((x, z))
    return R


def band_mask(R):
    """The build zones: the band, and the flanks between the Forecourt and the Aprons, on both halves."""
    m = np.zeros(R.H.shape, bool)
    for x0, z0, x1, z1 in (BAND, FLANK, (mx(FLANK[2]), FLANK[1], mx(FLANK[0]), FLANK[3])):
        for a0, b0, a1, b1 in ((x0, z0, x1, z1), (x0, -1 - z1, x1, -1 - z0)):
            m |= (R.X >= a0) & (R.X <= a1) & (R.Z >= b0) & (R.Z <= b1)
    return m & R.mask("void")


def ladders():
    """The ladders out of the Undercroft, as plan-walk edges: (landing, the Walk beside it, cost, tag), both
    halves and both sides. A ladder is climbed and descended."""
    out = []
    lx, lz = LADDER
    for x in (lx, mx(lx)):
        wx = x - 1 if x < 0 else x + 1
        for z in (lz, -1 - lz):
            out += [((x, z), (wx, z), HUB - UNDER + 1, "ladder"), ((wx, z), (x, z), HUB - UNDER + 1, "ladder")]
    return out


def objectives():
    """Teams, spawns and the four wools, drawn once for red's Kilns: a Wool's team is the team that captures it,
    so red's yellow and lime are blue's to take; their images are red's orange and light blue in blue's Kilns."""
    O = Objectives(Teams(("red-team", "Red", "red", 16), ("blue-team", "Blue", "blue", 16)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=Box(-16, 0, -100, 15, 127, -81),
                protect=("iron block",)))
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    west = Box(KILN[0], WOOL + 1, KILN[1], KILN[2], WOOL + ROOM_H - 1, KILN[3])
    east = Box(mx(KILN[2]), WOOL + 1, KILN[1], mx(KILN[0]), WOOL + ROOM_H - 1, KILN[3])
    (wx, wz), (ex, ez) = MONUMENTS
    blue_w, blue_e = SYM.point(wx, wz), SYM.point(ex, ez)
    O.add(Wool("blue-team", "yellow", slot=(blue_w[0], SPAWN + 1, blue_w[1]), found=(-66, WOOL + 1, -93), room=west,
               spawn_at=(-66, WOOL + 2, -90)), color="orange")
    O.add(Wool("blue-team", "lime", slot=(blue_e[0], SPAWN + 1, blue_e[1]), found=(65, WOOL + 1, -93), room=east,
               spawn_at=(65, WOOL + 2, -90)), color="light_blue")
    return O
