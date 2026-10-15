"""Calcite — a King of the Hill plan: a white marble quarry cut in two grounds round a lava pit.

Three hills. The Middle stands on an island in the pit and pays double; the North and South hills stand in
alcoves cut into the quarry wall behind the Bench and pay single. Red spawns in the west wall, blue in the east;
blue's half is red's turned half a circle, (x, z) -> (-1 - x, -1 - z), and each side hill is mirrored about its
own middle, so either team may take either of its flanks.

The plan is a height raster: every column's floor, and what kind of floor it is. The checker walks it, the
sketch draws it, and the generator builds from it, so all three read the same board.

    levels:  11 the lava, 13 the Ledge, 14 the Middle's apron, 17 the Bench and the Middle's top, 20 the side
             hills, 21 the spawns' terraces; the quarry wall stands to 28 round everything.
"""
import numpy as np

X_MIN, X_MAX = -60, 59
Z_MIN, Z_MAX = -48, 47
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
WALL_Y = 28
LAVA_Y = 11                 # the pit is lava, two below the Ledge: a fall into it is the end
KINDS = {"wall": 0, "floor": 1, "lava": 2, "stair": 3, "ladder": 4, "pad": 5, "hill": 6, "spawn": 7}


def rot(x, z):
    return -1 - x, -1 - z


def ix(x):
    return x - X_MIN


def iz(z):
    return z - Z_MIN


class Raster:
    def __init__(self):
        self.H = np.full((NX, NZ), WALL_Y, int)
        self.K = np.full((NX, NZ), KINDS["wall"], int)
        self.stair = {}                           # (x, z) -> the direction the stair rises: +x -x +z -z

    def rect(self, x0, x1, z0, z1, h, kind="floor", both=True):
        for (a0, a1, b0, b1) in ([(x0, x1, z0, z1)] + ([self._rot(x0, x1, z0, z1)] if both else [])):
            self.H[ix(a0):ix(a1) + 1, iz(b0):iz(b1) + 1] = h
            self.K[ix(a0):ix(a1) + 1, iz(b0):iz(b1) + 1] = KINDS[kind]

    @staticmethod
    def _rot(x0, x1, z0, z1):
        a, b = rot(x1, z1)
        return (a, -1 - x0, b, -1 - z0)

    def flight(self, cells, h0, rises, both=True):
        """A run of stair cells along `cells` (in climbing order), the first at h0, one up per cell."""
        for k, (x, z0, z1) in enumerate(cells):
            for z in range(z0, z1 + 1):
                self._stair(x, z, h0 + k, rises, both)

    def flight_z(self, cells, h0, rises, both=True):
        for k, (z, x0, x1) in enumerate(cells):
            for x in range(x0, x1 + 1):
                self._stair(x, z, h0 + k, rises, both)

    def _stair(self, x, z, h, rises, both):
        pts = [(x, z, rises)]
        if both:
            rx, rz = rot(x, z)
            pts.append((rx, rz, {"+x": "-x", "-x": "+x", "+z": "-z", "-z": "+z"}[rises]))
        for a, b, r in pts:
            self.H[ix(a), iz(b)] = h
            self.K[ix(a), iz(b)] = KINDS["stair"]
            self.stair[(a, b)] = r


def build():
    R = Raster()
    # the bowl: two grounds round the lava, four blocks apart, the quarry wall standing straight behind the Bench
    R.rect(-37, 36, -33, 32, 17, both=False)                 # the Bench, the high ground
    R.rect(-29, 28, -25, 24, 13, both=False)                 # the Ledge, the low ground
    R.rect(-23, 22, -19, 18, LAVA_Y, "lava", both=False)     # the lava pit
    # the spawns: a terrace cut into the wall, four over the Bench, a stair of three down to a landing
    R.rect(-49, -42, -6, 5, 21, "spawn")
    R.rect(-41, -38, -6, 5, 17)                              # the notch beside the stair, open to the Bench
    R.flight([(x, -3, 2) for x in range(-38, -42, -1)], 18, "-x")          # 18 at -38 .. 21 at -41, the terrace's level
    # the Middle: an island apron at 14, two steps of ring, the hill on top at 17, level with the Bench
    R.rect(-9, 8, -9, 8, 14, both=False)
    R.rect(-6, 5, -6, 5, 15, both=False)
    R.rect(-5, 4, -5, 4, 16, both=False)
    R.rect(-4, 3, -4, 3, 17, "hill", both=False)
    # the causeways from the Ledge to the island, a step up onto the apron
    R.rect(-23, -11, -2, 1, 13)
    R.flight([(-10, -2, 1)], 14, "+x")
    # the main stair from the Bench down to the Ledge, on each team's axis: three steps, landings either end
    R.flight([(x, -2, 1) for x in range(-30, -34, -1)], 14, "-x")          # 14 at -30 .. 17 at -33, the Bench's level
    # the stairs from the Ledge up to the Bench, each straight off the Ledge into the Bench with the Bench's width
    # as its landing: at every corner, and either side of each side hill's forecourt
    for x0, x1 in ((-29, -28), (27, 28), (-14, -11), (10, 13)):
        R.flight_z([(z, x0, x1) for z in range(-26, -30, -1)], 14, "-z")   # 14 at -26 .. 17 at -29
    # the side hills: each in an alcove cut into the wall behind the Bench, three over it, its front stair two
    # steps up out of the Bench, which is its forecourt
    R.rect(-4, 3, -41, -34, 20, "hill")
    R.flight_z([(z, -4, 3) for z in range(-31, -34, -1)], 18, "-z")       # 18 at -31 .. 20 at -33
    # either side, a passage cut into the wall from the Bench, wide enough to turn in, and a stair of two up
    # through a door in the alcove's wall onto the hill
    R.rect(-13, -8, -40, -34, 17)                             # the west passage
    R.flight([(x, -39, -37) for x in range(-11, -8)], 18, "+x")            # 18 at -11 .. 20 at -9
    R.rect(-8, -5, -39, -37, 20)                              # the west door, at the hill's height
    R.rect(7, 12, -40, -34, 17)                               # the east passage, its mirror
    R.flight([(x, -39, -37) for x in range(10, 7, -1)], 18, "-x")          # 18 at 10 .. 20 at 8
    R.rect(4, 7, -39, -37, 20)                                # the east door
    # the parkour from the Ledge to the Middle: two pillars, gaps of two, the first a block up
    R.rect(-1, 0, -17, -16, 14, "floor")
    R.rect(-1, 0, -13, -12, 14, "floor")
    # the Spring's tunnel forks under the lava, runs on under the Ledge, and turns to climb a trench of stairs
    # along the Ledge, coming up in line with it, two cells of Ledge ahead
    R.flight([(x, -23, -21) for x in range(8, 14)], 8, "+x")               # 8 at 8 .. 13 at 13, the Ledge's level
    R.flight([(x, -23, -21) for x in range(-9, -15, -1)], 8, "-x")         # its mirror
    # the diagonal steps from the arrows' corner of the Ledge to the Middle's apron: three pillars, each jump a
    # gap of two by one; in the north-east, and turned, the south-west
    R.rect(19, 20, -17, -16, 14, "floor")
    R.rect(15, 16, -14, -13, 14, "floor")
    R.rect(11, 12, -11, -10, 14, "floor")
    return R


# ---- the routes' special edges, which a height raster cannot hold ----------------------------------------------
# tunnels: two surface cells and the way between them, a polyline of (x, z, y). Each has a turned twin.
TUNNELS = [
    # red's: from the spawn terrace, down inside the wall to the Ledge's north-west corner
    dict(key="spawn-tunnel", a=(-46, -6), b=(-29, -21), pts=[(-46, -6, 21), (-46, -15, 13), (-46, -21, 13), (-29, -21, 13)]),
    # the Spring: down a stairwell from the apron's west side to the apples under the Middle, north under the
    # lava, a fork, and up a trench onto the Ledge on either side of the North hill's forecourt stairs
    dict(key="spring-w-e", a=(-8, 8), b=(8, -22), pts=[(-8, 8, 14), (-8, 2, 9), (-4, 2, 9), (-1, -5, 9), (-1, -7, 7), (-1, -12, 7), (6, -12, 7), (6, -22, 7), (8, -22, 8)]),
    dict(key="spring-w-w", a=(-8, 8), b=(-9, -22), pts=[(-8, 8, 14), (-8, 2, 9), (-4, 2, 9), (-1, -5, 9), (-1, -7, 7), (-1, -12, 7), (-7, -12, 7), (-7, -22, 7), (-9, -22, 8)]),
    dict(key="spring-e-e", a=(7, -9), b=(8, -22), pts=[(7, -9, 14), (7, -3, 9), (3, -3, 9), (-1, -5, 9), (-1, -7, 7), (-1, -12, 7), (6, -12, 7), (6, -22, 7), (8, -22, 8)]),
    dict(key="spring-e-w", a=(7, -9), b=(-9, -22), pts=[(7, -9, 14), (7, -3, 9), (3, -3, 9), (-1, -5, 9), (-1, -7, 7), (-1, -12, 7), (-7, -12, 7), (-7, -22, 7), (-9, -22, 8)]),
    dict(key="spring-across", a=(-8, 8), b=(7, -9), pts=[(-8, 8, 14), (-8, 2, 9), (7, -3, 9), (7, -9, 14)]),
]
SPRING = dict(box=(-4, 3, -4, 3), floor=9, ceil=13)         # the room under the Middle; the apples at its centre
TUNNEL_FLOOR = 7                                            # under the lava: air 8..9, a glass roof at 10, lava at 11

# jump pads: the pad's cells (x0, x1, z0, z1, floor y), the velocity, and what it is for. Each has a turned twin.
PADS = [
    dict(key="mid-north-w", cells=(-6, -5, -9, -8, 14), v=(-0.7, 0.75, -2.87),
         why="from the Middle's apron to the Bench at the mouth of the North hill's west passage"),
    dict(key="mid-north-e", cells=(4, 5, -9, -8, 14), v=(0.7, 0.75, -2.87),
         why="its mirror: to the mouth of the east passage"),
    dict(key="ledge-mid", cells=(-29, -27, -25, -23, 13), v=(2.1, 0.8, 1.78),
         why="from the Ledge's corner over the lava onto the Middle's apron, answering the diagonal steps"),
]
DROPS = []
# arrows in two diagonal inner corners of the Ledge (the north-east, and its turn, the south-west), where the
# diagonal steps to the Middle start; the other two corners carry a pad onto the Middle
ARROWS_AT = [(25.5, 14, -22.5), (-25.5, 14, 21.5)]

HILLS = [dict(key="mid", name="the Middle", box=(-4, 3, -4, 3), y=17, points=2),
         dict(key="north", name="the North hill", box=(-4, 3, -41, -34), y=20, points=1),
         dict(key="south", name="the South hill", box=(-4, 3, 33, 40), y=20, points=1)]
GAPPLE_AT = (-0.5, 10, -0.5)        # the Spring: under the Middle
SPAWN_POINT = (-46.5, 22, -0.5)
