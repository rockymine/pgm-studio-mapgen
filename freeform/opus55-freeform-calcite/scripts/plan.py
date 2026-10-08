"""Calcite — a King of the Hill plan: a white marble quarry cut in square benches round a flooded pit.

Three hills. The Middle stands on an island in the pit and pays double; the North and South hills stand on the
second bench and pay single. Red spawns in the west wall, blue in the east; blue's half is red's turned half a
circle, (x, z) -> (-1 - x, -1 - z), so the North hill is red's near side hill and the South hill blue's.

The plan is a height raster: every column's floor, and what kind of floor it is. The checker walks it, the
sketch draws it, and the generator builds from it, so all three read the same board.

    levels:  10 the pool, 16 the Ledge, 19 the Middle's apron, 22 the Bench and the Middle's top,
             23 the side hills, 28 the Rim and the spawns; the quarry wall stands to 40 round everything.
"""
import numpy as np

X_MIN, X_MAX = -60, 59
Z_MIN, Z_MAX = -48, 47
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
WALL_Y = 40
LAVA_Y = 10                 # the pool is lava: a fall into it is the end
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
    # the bowl: four square rings stepping down to the pool — three grounds to fight on, the pool under them
    R.rect(-45, 44, -41, 40, 28, both=False)                 # the Rim, the high ground
    R.rect(-37, 36, -33, 32, 22, both=False)                 # the Bench, the middle ground
    R.rect(-29, 28, -25, 24, 16, both=False)                 # the Ledge, the low ground
    R.rect(-23, 22, -19, 18, LAVA_Y, "lava", both=False)     # the lava pool
    # the spawns, cut into the wall behind the Rim
    R.rect(-55, -46, -6, 5, 28, "spawn")
    # the Middle: an island apron at 19, two steps of ring, the hill on top at 22
    R.rect(-9, 8, -9, 8, 19, both=False)
    R.rect(-6, 5, -6, 5, 20, both=False)
    R.rect(-5, 4, -5, 4, 21, both=False)
    R.rect(-4, 3, -4, 3, 22, "hill", both=False)
    # the side hills: each in an alcove cut into the Rim's face, walled on three sides and open toward the Middle.
    # The hill is one step over the Bench; the walls stand two over the Rim, so nobody walks along their tops.
    R.rect(-4, 3, -34, -27, 23, "hill")
    R.rect(-7, -5, -34, -26, 30, "wall")                     # the west wall
    R.rect(4, 6, -34, -26, 30, "wall")                       # the east wall
    # the hill's front: a stair eight wide from the Ledge straight up onto it
    R.flight_z([(z, -4, 3) for z in range(-21, -27, -1)], 17, "-z")
    # the side ways in, one through each wall, the hill mirrored about its own middle so either team may take
    # either side: a narrow stair up the outside of the wall, a window through it, a drop of four
    R.flight_z([(z, -9, -8) for z in range(-31, -26)], 23, "+z")             # west: 23 at -31 .. 27 at -27
    R.flight_z([(z, 7, 8) for z in range(-31, -26)], 23, "+z")               # east, its mirror
    R.rect(-7, -5, -27, -27, 27, "floor")                    # the west window's sill, out of reach of the Rim
    R.rect(4, 6, -27, -27, 27, "floor")                      # the east window's sill
    # the causeways from the Ledge to the island, and their stairs up onto the apron
    R.rect(-23, -10, -2, 1, 16)
    R.flight([(-12, -2, 1), (-11, -2, 1), (-10, -2, 1)], 17, "+x")
    # the main stairs: Rim to Bench in a notch, Bench to Ledge in a well, on the team's axis
    R.flight([(x, -2, 1) for x in range(-38, -44, -1)], 23, "-x")          # 23 at -38 .. 28 at -43
    R.flight([(x, -2, 1) for x in range(-30, -36, -1)], 17, "-x")          # 17 at -30 .. 22 at -35
    # the side stairs from the Ledge up to the Bench on either side of each side hill's alcove
    R.flight([(x, -27, -26) for x in range(-16, -10)], 17, "+x")           # west, rising east
    R.flight([(x, -27, -26) for x in range(15, 9, -1)], 17, "-x")          # east, rising west
    # the corner stairs: Ledge up to Bench, and Bench up to Rim, at every corner of the bowl
    R.flight_z([(z, -31, -30) for z in range(-26, -32, -1)], 17, "-z")     # north-west, Ledge to Bench
    R.flight_z([(z, 29, 30) for z in range(-26, -32, -1)], 17, "-z")       # north-east, Ledge to Bench
    R.flight_z([(z, -37, -36) for z in range(-28, -34, -1)], 23, "-z")     # north-west, Bench to Rim
    R.flight_z([(z, 35, 36) for z in range(-28, -34, -1)], 23, "-z")       # north-east, Bench to Rim
    # the parkour from the Ledge to the Middle: two pillars, 2 then 2 then 3 blocks apart, each a block higher
    R.rect(-1, 0, -17, -16, 17, "floor")
    R.rect(-1, 0, -13, -12, 18, "floor")
    # the Spring's tunnel forks under the Ledge and comes up in a trench of stairs on either side of each side
    # hill's front stair
    R.flight_z([(z, 5, 7) for z in range(-20, -26, -1)], 11, "-z")       # east: 11 at -20 .. 16 at -25
    R.flight_z([(z, -8, -6) for z in range(-20, -26, -1)], 11, "-z")     # west, its mirror
    # the diagonal steps from the arrows' corner of the Ledge to the Middle's apron: three pillars, each jump a
    # gap of two by one, each a block higher; in the north-east, and turned, the south-west
    R.rect(19, 20, -17, -16, 17, "floor")                   # two clear of both edges of the Ledge's corner
    R.rect(15, 16, -14, -13, 18, "floor")
    R.rect(11, 12, -11, -10, 19, "floor")                   # then a straight gap of two onto the apron
    return R


# ---- the routes' special edges, which a height raster cannot hold ----------------------------------------------
# tunnels: two surface cells and the way between them, a polyline of (x, z, y). Each has a turned twin.
TUNNELS = [
    # red's: from the spawn, down inside the wall to the Ledge's north-west corner
    dict(key="spawn-tunnel", a=(-50, -6), b=(-29, -21), pts=[(-50, -7, 28), (-50, -21, 16), (-29, -21, 16)]),
    # the Spring: down a stairwell from the apron's west side to the golden apples under the hill, then north
    # under the pool in a glass tube, and up the trench onto the Ledge below the North hill
    dict(key="spring-north", a=(-9, 5), b=(6, -20),
         pts=[(-9, 5, 19), (-4, 5, 13), (-1, -5, 13), (-1, -13, 6), (-1, -17, 6), (6, -20, 11)]),
    dict(key="spring-north-e", a=(8, -6), b=(6, -20),
         pts=[(8, -6, 19), (3, -6, 13), (-1, -6, 13), (-1, -13, 6), (-1, -17, 6), (6, -20, 11)]),
    dict(key="spring-north-w", a=(8, -6), b=(-7, -20),
         pts=[(8, -6, 19), (3, -6, 13), (-1, -6, 13), (-1, -13, 6), (-1, -17, 6), (-7, -20, 11)]),
    dict(key="spring-north-ww", a=(-9, 5), b=(-7, -20),
         pts=[(-9, 5, 19), (-4, 5, 13), (-1, -5, 13), (-1, -13, 6), (-1, -17, 6), (-7, -20, 11)]),
    # the Spring's two stairwells joined under the hill: west to east, past the apples
    dict(key="spring-across", a=(-9, 5), b=(8, -6), pts=[(-9, 5, 19), (-4, 5, 13), (3, -6, 13), (8, -6, 19)]),
]
SPRING = dict(box=(-5, 4, -5, 4), floor=13, ceil=18)        # the room under the Middle; the apples at its centre

# jump pads: the pad's cells (x0, x1, z0, z1, floor y), the velocity, and what it is for
PADS = [
    dict(key="mid-north-w", cells=(-6, -5, -9, -8, 19), v=(-1.08, 0.75, -2.74),
         why="from the Middle's apron to the Bench beside the North hill's west side stair"),
    dict(key="mid-north-e", cells=(4, 5, -9, -8, 19), v=(1.08, 0.75, -2.74),
         why="its mirror: to the Bench beside the North hill's east side stair"),
    dict(key="ledge-mid", cells=(-29, -27, -25, -23, 16), v=(2.21, 0.90, 1.88),
         why="from the Ledge's corner over the lava onto the Middle's apron: the corner's way onto the Middle, "
             "answering the diagonal steps in the other two corners"),
]
# the drop: from the Rim straight down onto a side hill, 5 blocks, one way
DROPS = [dict(key="rim-north", at=(-4, 3, -35, -35), onto="hill N", height=5)]
# arrows in two diagonal inner corners of the Ledge (the north-east, and its turn, the south-west), where the
# diagonal steps to the Middle start; the other two corners carry the pads up to the Rim
ARROWS_AT = [(25.5, 17, -22.5), (-25.5, 17, 21.5)]

HILLS = [dict(key="mid", name="the Middle", box=(-4, 3, -4, 3), y=22, points=2),
         dict(key="north", name="the North hill", box=(-4, 3, -34, -27), y=23, points=1),
         dict(key="south", name="the South hill", box=(-4, 3, 26, 33), y=23, points=1)]
GAPPLE_AT = (-0.5, 14, -0.5)        # the Spring: under the Middle
SPAWN_POINT = (-51.5, 29, -0.5)
