"""Saltgate — an attack/defend plan: a walled harbour citadel stormed from the sea, in three stages.

The attackers (red) land from three ships moored off a beach. The defenders (blue) hold the town behind its
sea wall. The attackers win by completing all three stages in order before the clock runs out; the defenders
win when it does. Each stage, once done, opens the gates to the next and moves both teams' spawns forward:

    A  the Sea Gate      capture the yard behind the sea wall (a control point, defenders' at the start)
    B  the Powder Stores destroy both magazines' monuments in the lower town (obsidian, the defenders')
    C  the Banner        take the city's banner from the keep's treasury and carry it down to the Sea Gate

The ways into the Sea Gate's yard are the gate itself, two siege ladders up the wall, and a drain culvert under
it. The magazines' doors are shut until the Sea Gate falls; the citadel's gate and the keep's door are shut until
both magazines are down. The defenders have a postern through the citadel wall that only they can use.

The plan is a height raster with a kind for every column, an upper raster for the wall walk over the gate's
passage, and lists of what a raster cannot hold: gates by stage, ladders, the culvert, the objectives and the
spawns. The checker walks it stage by stage, the sketch draws it, and the generator will build from it.

    heights are the top block a player stands on: 18 the sea, 21 to 22 the landing and the beach, 24 the ships'
    decks, 22 the yard and the lowest street, 26 and 30 the town's terraces, 28 the wall walk, 34 the citadel's
    courtyard, 44 the citadel wall, 50 the keep
"""
import numpy as np

X_MIN, X_MAX = -48, 47
Z_MIN, Z_MAX = -72, 63
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
SEA = 18
KINDS = {"sea": 0, "beach": 1, "street": 2, "wall": 3, "rampart": 4, "tower": 5, "house": 6, "stair": 7,
         "ladder": 8, "gate": 9, "deck": 10, "pier": 11, "court": 12, "magazine": 13, "keep": 14, "floor": 15, "cover": 16}
WALK = {"beach", "street", "rampart", "stair", "deck", "pier", "court", "floor"}


def ix(x):
    return x - X_MIN


def iz(z):
    return z - Z_MIN


class Raster:
    def __init__(self):
        self.H = np.full((NX, NZ), SEA, int)
        self.K = np.full((NX, NZ), KINDS["sea"], int)
        self.U = np.full((NX, NZ), -1, int)
        self.stair = {}
        self.gate = {}                                  # (x, z) -> the stage whose fall opens it

    def rect(self, x0, x1, z0, z1, h, kind="street"):
        self.H[ix(x0):ix(x1) + 1, iz(z0):iz(z1) + 1] = h
        self.K[ix(x0):ix(x1) + 1, iz(z0):iz(z1) + 1] = KINDS[kind]

    def gates(self, x0, x1, z0, z1, h, opens):
        """A gate: floor at h, closed (a wall) until the stage `opens` is done."""
        self.rect(x0, x1, z0, z1, h, "gate")
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                self.gate[(x, z)] = opens

    def flight_z(self, rows, h0, rises):
        for k, (z, x0, x1) in enumerate(rows):
            for x in range(x0, x1 + 1):
                self.H[ix(x), iz(z)] = h0 + k
                self.K[ix(x), iz(z)] = KINDS["stair"]
                self.stair[(x, z)] = rises

    def flight_x(self, rows, h0, rises):
        for k, (x, z0, z1) in enumerate(rows):
            for z in range(z0, z1 + 1):
                self.H[ix(x), iz(z)] = h0 + k
                self.K[ix(x), iz(z)] = KINDS["stair"]
                self.stair[(x, z)] = rises


def build():
    R = Raster()
    # ---- the sea, the ships, the landing ------------------------------------------------------------------
    for x0, x1 in ((-30, -22), (-6, 5), (21, 29)):
        R.rect(x0, x1, -66, -56, 24, "deck")
        cx = (x0 + x1) // 2
        R.rect(cx - 1, cx + 1, -55, -54, 24, "deck")                       # the gangplank's head
        R.flight_z([(z, cx - 1, cx + 1) for z in (-51, -52, -53)], 22, "-z")  # down to the landing
        R.gates(cx - 1, cx + 1, -55, -55, 24, "warmup")                     # shut until the attackers go
    R.rect(-36, 35, -50, -47, 21, "pier")                                   # the landing stage
    # ---- stage A: the beach, the sea wall, the Sea Gate and its yard ---------------------------------------
    # the wall stands six over the beach; at the gatehouse an attacker has three ways in, side by side: the
    # passage under the gatehouse, a siege ladder either side of it up to the walk, and the culvert under it
    R.rect(-46, 45, -46, -40, 21, "beach")
    R.rect(-46, 45, -39, -32, 22, "beach")
    R.rect(-46, 45, -31, -29, 28, "rampart")                                # the wall, its walk on top
    for x0, x1 in ((-30, -25), (24, 29), (-48, -43), (42, 47)):
        R.rect(x0, x1, -33, -27, 33, "tower")
    R.rect(-3, 2, -31, -29, 22, "street")                                   # the gate's passage
    R.U[ix(-3):ix(2) + 1, iz(-31):iz(-29) + 1] = 28                         # the walk over it
    for x in (-8, 7):                                                       # the siege ladders
        R.rect(x, x, -32, -32, 28, "ladder")
    R.rect(-43, 42, -28, -20, 22, "street")                                 # the yard
    for xc in (-9, 8):                                                      # a stair from each ladder's head
        R.flight_z([(z, xc - 1, xc + 1) for z in range(-23, -29, -1)], 23, "-z")   # down into the yard
    # ---- stage B: the lower town, three terraces, the two magazines ---------------------------------------
    R.rect(-46, 45, -19, -8, 22, "street")
    R.rect(-46, 45, -7, 6, 26, "street")
    R.rect(-46, 45, 7, 22, 30, "street")
    for xc in (-1, -30, 29):                                                # stairs between the terraces
        R.flight_z([(z, xc - 1, xc + 1) for z in range(-7, -3)], 23, "+z")  # 23 at z -7 .. 26 at z -4
        R.flight_z([(z, xc - 1, xc + 1) for z in range(7, 11)], 27, "+z")   # 27 at z 7 .. 30 at z 10
    for x0, x1, z0, z1 in HOUSES:
        R.rect(x0, x1, z0, z1, R.H[ix(x0), iz(z0)] + 9, "house")
    for m in MAGAZINES:
        x0, x1, z0, z1 = m["box"]
        f = m["floor"]
        R.rect(x0, x1, z0, z1, f + 7, "magazine")                           # walls and vault
        R.rect(x0 + 1, x1 - 1, z0 + 1, z1 - 1, f, "floor")                  # the hall inside
        for dx0, dx1, dz0, dz1 in m["doors"]:
            R.gates(dx0, dx1, dz0, dz1, f, "A")
    # ---- stage C: the citadel wall, its gate and postern, the courtyard and the keep ----------------------
    R.rect(-48, 47, 23, 25, 44, "wall")
    R.gates(-3, 2, 23, 25, 30, "B")                                         # the citadel's gate
    R.rect(36, 37, 23, 25, 30, "street")                                    # the defenders' posterns
    R.rect(-38, -37, 23, 25, 30, "street")
    R.rect(-46, 45, 26, 60, 34, "court")
    R.flight_z([(z, -3, 2) for z in range(26, 30)], 31, "+z")               # 31 at z 26 .. 34 at z 29
    R.flight_z([(z, 36, 37) for z in range(26, 30)], 31, "+z")              # the posterns' stairs
    R.flight_z([(z, -38, -37) for z in range(26, 30)], 31, "+z")
    R.rect(-12, 11, 44, 60, 50, "keep")
    R.rect(-8, 7, 48, 57, 34, "floor")                                      # the treasury
    R.gates(-2, 1, 44, 47, 34, "B")                                         # the keep's door and passage
    R.gates(8, 11, 51, 53, 34, "B")                                         # and its side door, east
    for x0, x1, z0, z1 in COURT_BUILDINGS:
        R.rect(x0, x1, z0, z1, 34 + 9, "house")
    for x0, x1, z0, z1, tall in COVER:
        R.rect(x0, x1, z0, z1, int(R.H[ix(x0), iz(z0)]) + tall, "cover")
    return R


HOUSES = [  # x0, x1, z0, z1: closed houses in the lower town, streets left between them
    (-40, -34, -18, -14), (-26, -6, -18, -14), (5, 24, -18, -14), (35, 43, -18, -14),
    (-26, -6, -12, -9), (5, 24, -12, -9),
    (-44, -34, -3, 4), (-11, -5, -3, 4), (4, 10, -3, 4), (24, 26, -3, 4), (34, 44, -3, 4),
    (-44, -34, 12, 20), (-26, -6, 12, 20), (4, 11, 12, 20), (34, 44, 12, 20),
]
COURT_BUILDINGS = [(-40, -20, 33, 38), (18, 40, 33, 38), (-40, -28, 46, 58), (26, 40, 46, 58)]
COVER = [  # x0, x1, z0, z1, height over the ground: beached boats and rocks on the beach, carts and crates in the yard
    (-36, -32, -43, -42, 2), (-20, -18, -38, -36, 2), (14, 18, -44, -43, 2), (30, 32, -38, -36, 2),
    (-6, -5, -42, -41, 2), (5, 6, -37, -36, 2), (-42, -40, -36, -35, 2), (38, 41, -42, -41, 2),
    (-30, -28, -25, -24, 2), (16, 18, -26, -25, 2), (-38, -37, -22, -21, 2), (30, 31, -22, -21, 2),
    (-14, -12, 41, 42, 2), (10, 12, 41, 42, 2), (-3, 2, 38, 38, 2),
]
MAGAZINES = [
    dict(key="west", name="the West Powder Store", box=(-22, -14, -4, 5), floor=26,
         doors=[(-19, -17, -4, -4), (-19, -17, 5, 5)], monument=(-18, 27, 0)),
    dict(key="east", name="the East Powder Store", box=(14, 22, 11, 20), floor=30,
         doors=[(17, 19, 11, 11), (17, 19, 20, 20)], monument=(18, 31, 15)),
]
CONTROL = dict(key="sea-gate", name="the Sea Gate", box=(-6, 5, -26, -21), y=22)
WOOL = dict(at=(0, 35, 54), colour=10, monument=(0, 23, -23))
CULVERT = dict(a=(-14, -36), b=(-14, -22), pts=[(-14, -36, 21), (-14, -31, 18), (-14, -26, 18), (-14, -22, 22)])
# spawns by stage: (x, y, z, yaw)
SPAWNS = {
    "attackers": {"1": (0.5, 25, -61.5, 0), "2": (0.5, 23, -27.5, 0), "3": (0.5, 31, 13.5, 0)},
    "defenders": {"1": (0.5, 27, 0.5, 180), "2": (0.5, 31, 20.5, 180), "3": (-20.5, 35, 50.5, 180)},
}
TIME = "15m"
WARMUP = "20s"
