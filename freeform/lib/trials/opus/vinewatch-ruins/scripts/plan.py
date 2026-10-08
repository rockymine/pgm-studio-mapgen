"""Vinewatch Ruins: the plan. Team deathmatch.

Identity: a white temple ruin in a jungle bowl, fought over in three lanes (a causeway over a marsh, a plaza round
a low lidded ziggurat, a sunken court) with a cistern under the middle that joins them, each team spawning in a
walled gate-court that nothing in the middle can see into.

Red holds the north (z < 0); blue's half is red's mirror image, z' = -1 - z, pgmvox's Symmetry("mirror_z"). The
plan is drawn as pieces in a Raster, each its own kind, so the checker, the sketch and the generator read the same
board; storey 1 is the cistern.

Combat boards are built to match-flow.md §10: built ground, entered from decided directions, placed cover in two
sizes (small, two or three high, inside the spaces; large, walls a space is split by), nothing in the middle that
looks into a spawn, height a small thing.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")))   # freeform/lib
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))               # trials/opus (common)

import numpy as np  # noqa: E402

import common  # noqa: E402,F401
from pgmvox.objectives import Box, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan import Raster, Symmetry  # noqa: E402

BOARD = "vinewatch-ruins"
X_MIN, X_MAX = -48, 47
Z_MIN, Z_MAX = -56, 55
SYM = Symmetry("mirror_z")
PLAZA_Y = 40
KINDS = ["bowl", "thicket", "jungle", "plaza", "causeway", "marsh", "court", "spawn", "tier1", "tier2", "tier3", "stair",
         "wall", "cover", "pillar", "cistern", "rim"]
COLOURS = {"bowl": (60, 90, 60), "jungle": (70, 140, 60), "plaza": (225, 225, 215), "causeway": (205, 205, 195),
           "marsh": (90, 130, 150), "court": (190, 190, 175), "spawn": (240, 230, 200), "tier1": (215, 210, 190),
           "tier2": (225, 220, 195), "tier3": (240, 225, 160), "stair": (170, 170, 160), "wall": (120, 120, 110),
           "cover": (150, 110, 80), "pillar": (100, 100, 95), "cistern": (90, 110, 140), "rim": (40, 60, 40),
           "thicket": (40, 100, 40)}
WALK = {"jungle", "plaza", "causeway", "marsh", "court", "spawn", "tier1", "tier2", "tier3", "stair", "cistern"}
WALLS = ("wall", "cover", "pillar", "rim", "thicket")

# ---- the pieces, red's, drawn in order; each later one over the earlier --------------------------------------
SPAWN_COURT = (-10, -50, 9, -40)          # the gate-court, 44, walled
SPAWN_Y = 44
PLAZA = (-21, -27, 20, 26)               # the plaza at 40 round the ziggurat (both halves at once: it is on the axis)
ZIG = [(13, 42), (9, 44), (5, 46)]       # half widths and floors of the three tiers (square)
SHRINE_ROOF = 51                         # the lid over the top tier, on four pillars
CAUSEWAY = (-38, -38, -28, 37)           # the west lane: a raised walk at 42 over the marsh at 38/39
CAUSEWAY_Y, MARSH_Y = 42, 39
COURT = (26, -36, 40, 35)                # the east lane: a sunken court at 36
COURT_Y = 36
CISTERN = (-38, -3, 24, 2)               # the tunnel under the middle at 34, stairwells up at each end
CISTERN_Y = 34
CISTERN_PILLARS = (-30, -18, 12)          # pillars in the tunnel at z -2 and 1, a pair each, off the hall
SPAWN_AT = (0, 45, -46)

# the ways out of the gate-court: west to the causeway, south to the plaza (behind a screen), east to the court
GATES = {"west": (-11, -50, -11, -48), "south": (-2, -39, 1, -39), "east": (10, -50, 10, -48)}
SCREEN = (-6, -33, 5, -33)               # a wall in front of the south gate, eight high: no line into the court
BAFFLES = [(-15, -51, -15, -41), (14, -51, 14, -41)]   # walls four off each side gate, its whole height
THICKET = [(-44, -52, -17, -42), (16, -52, 43, -42)]   # the jungle beside the gate-courts: planted, not walked
# large cover: walls a space is split by
WALL_PIECES = [(-26, -18, -24, -7), (-26, -3, -24, 1),          # the ruined west wall of the plaza, two breaches
               (-27, -33, -24, -30), (23, -33, 26, -30),        # the fallen gateposts at the plaza's north corners
               (22, -22, 24, -12), (22, -6, 24, -2),            # the court's parapet, broken by two stairs
               (-14, -31, -10, -29), (9, -31, 13, -29)]         # ruined blocks either side of the screen
# small cover: two or three high, inside the spaces
COVER = [(-16, -24, -15, -23), (14, -24, 15, -23), (-8, -21, -7, -20), (6, -21, 7, -20),
         (-35, -26, -35, -25), (-35, -12, -35, -11), (31, -28, 32, -28), (36, -16, 37, -16), (31, -6, 32, -6),
         (-3, -30, -2, -29), (1, -30, 2, -29)]
PILLARS = [(-37, -33), (-33, -20), (-37, -6), (29, -32), (38, -24), (29, -12), (38, -4)]
STAIRS = [  # (start cell, rises, width offsets, first floor, steps)
    ((-2, -37), "n", (0, 3), 42, 2),                  # the south gate down to the jungle, 44 to 41, behind the screen
    ((-13, -49), "e", (-1, 1), 42, 2),                # the west gate down to the jungle and the causeway's head
    ((12, -49), "w", (-1, 1), 42, 2),                 # the east gate down to the jungle
    ((33, -37), "n", (-1, 1), 37, 4),                 # the jungle down into the court at its head, 41 to 36
    ((25, -9), "w", (-2, 1), 37, 4),                  # the plaza down into the court through its parapet
]

PLACES = [("the Gate-court", (0, -52)), ("the Plaza", (-12, -14)), ("the Ziggurat", (0, 0)),
          ("the Causeway", (-35, -30)), ("the Marsh", (-44, -20)), ("the Sunken Court", (33, -20)),
          ("the Cistern", (0, 4)), ("the Screen", (0, -35))]


def build():
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=60, base_kind="rim", symmetry=SYM)
    R.box(-44, -52, 43, 51, 41, "jungle")                                   # the bowl's floor, jungle at 41
    R.box(-44, -52, -28, 51, MARSH_Y, "marsh")                              # the marsh along the west
    R.box(*CAUSEWAY, CAUSEWAY_Y, "causeway")
    R.box(-38, -40, -12, -38, CAUSEWAY_Y, "causeway")                       # its head, to the west gate
    R.box(25, -40, 41, 39, PLAZA_Y + 1, "jungle")
    R.box(*COURT, COURT_Y, "court")
    R.box(*PLAZA, PLAZA_Y, "plaza", both=False)
    R.box(-29, -24, -22, -21, PLAZA_Y + 1, "causeway")                      # the causeway's spur onto the plaza
    for half, h in ZIG:
        R.box(-half, -half, half - 1, half - 1, h, f"tier{ZIG.index((half, h)) + 1}", both=False)
    # the ziggurat's stairs: north and south faces, from the plaza to the top, two steps a tier
    for half, h in ZIG:
        R.flight((-1, -half - 1), "s", width=(0, 1), h0=h - 1, n=1)
    R.box(*SPAWN_COURT, SPAWN_Y, "spawn")
    for g in GATES.values():
        R.box(*g, SPAWN_Y, "spawn")
    for (x, z), rises, wd, h0, n in STAIRS:
        R.flight((x, z), rises, width=wd, h0=h0, n=n)
    # the gate-court's walls, all but its gates
    x0, z0, x1, z1 = SPAWN_COURT
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            if (x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1)) and not any(
                    g[0] <= x <= g[2] and g[1] <= z <= g[3] for g in GATES.values()):
                R.cell(x, z, SPAWN_Y + 5, "wall")
    R.box(*SCREEN, PLAZA_Y + 8, "wall")
    for b in BAFFLES:
        R.box(*b, SPAWN_Y + 3, "wall")
    for b in THICKET:
        R.box(*b, PLAZA_Y + 10, "thicket")
    for b in WALL_PIECES:
        R.box(*b, PLAZA_Y + 5, "wall")
    for b in COVER:
        R.box(*b, PLAZA_Y + 3, "cover")
    for x, z in PILLARS:
        R.cell(x, z, PLAZA_Y + 5, "pillar")
    for (x, z) in ((-5, -5), (4, -5), (-5, 4), (4, 4)):                     # the lid's pillars on the top tier
        R.cell(x, z, SHRINE_ROOF, "pillar", both=False)
    # storey 1: the cistern under the middle, with a stair down at each end
    U = R.storey(1)
    U.box(*CISTERN, CISTERN_Y, "cistern", both=False)
    U.box(-6, -7, 5, 6, CISTERN_Y, "cistern", both=False)            # the hall under the ziggurat
    for x in CISTERN_PILLARS:                                          # staggered cover: no straight firing line
        U.cell(x, -2, CISTERN_Y + 4, "pillar")                         # (and its image at z 1)
    # its stairwells are cut into the ground storey: west up through the marsh's floor, east up into the court
    for k, x in enumerate(range(CISTERN[0] - 1, CISTERN[0] - 5, -1)):
        R.box(x, -2, x, 1, CISTERN_Y + 1 + k, "stair", both=False)
        for z in range(-2, 2):
            R.stair[(x, z)] = "w"
    for k, x in enumerate(range(CISTERN[2] + 1, COURT[0] + 2)):
        R.box(x, -2, x, 1, CISTERN_Y + k, "stair", both=False)
        for z in range(-2, 2):
            R.stair[(x, z)] = "e"
    return R


def links(R):
    """Nothing the raster cannot see: the cistern's stairwells are drawn in the ground storey."""
    return []


def objectives():
    O = Objectives(Teams(("red-team", "Red", "red", 12), ("blue-team", "Blue", "blue", 12)), SYM)
    x0, z0, x1, z1 = SPAWN_COURT
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=Box(x0, SPAWN_Y + 1, z0, x1, SPAWN_Y + 6, z1)))
    O.add(Observer((0, 70, 0), yaw=90), mirror=False)
    return O


def spawn_cells(team="red"):
    x0, z0, x1, z1 = SPAWN_COURT
    cells = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
    return cells if team == "red" else [SYM.point(x, z) for x, z in cells]
