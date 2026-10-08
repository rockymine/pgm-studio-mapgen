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
WATER_Y = 10
KINDS = {"wall": 0, "floor": 1, "water": 2, "stair": 3, "ladder": 4, "pad": 5, "hill": 6, "spawn": 7}


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
    # the bowl: four square rings stepping down to the pool
    R.rect(-45, 44, -41, 40, 28, both=False)                 # the Rim
    R.rect(-37, 36, -33, 32, 22, both=False)                 # the Bench
    R.rect(-29, 28, -25, 24, 16, both=False)                 # the Ledge
    R.rect(-23, 22, -19, 18, WATER_Y, "water", both=False)   # the pool
    # the spawns, cut into the wall behind the Rim
    R.rect(-55, -46, -6, 5, 28, "spawn")
    # the Middle: an island apron at 19, two steps of ring, the hill on top at 22
    R.rect(-9, 8, -9, 8, 19, both=False)
    R.rect(-6, 5, -6, 5, 20, both=False)
    R.rect(-5, 4, -5, 4, 21, both=False)
    R.rect(-4, 3, -4, 3, 22, "hill", both=False)
    # the side hills on the Bench, one step up
    R.rect(-4, 3, -33, -26, 23, "hill")
    # the causeways from the Ledge to the island, and their stairs up onto the apron
    R.rect(-23, -10, -2, 1, 16)
    R.flight([(-12, -2, 1), (-11, -2, 1), (-10, -2, 1)], 17, "+x")
    # the main stairs: Rim to Bench in a notch, Bench to Ledge in a well, on the team's axis
    R.flight([(x, -2, 1) for x in range(-38, -44, -1)], 23, "-x")          # climbing west: 23 at -38 .. 28 at -43
    R.flight([(x, -2, 1) for x in range(-30, -36, -1)], 17, "-x")          # 17 at -30 .. 22 at -35
    # the side stairs from the Ledge up to the Bench beside each side hill, one from each end
    R.flight([(x, -27, -26) for x in range(-16, -10)], 17, "+x")           # west of the North hill, rising east
    R.flight([(x, -27, -26) for x in range(15, 9, -1)], 17, "-x")          # east of the North hill, rising west
    # the corner stairs from the Bench up to the Rim, one at each corner of the bowl
    R.flight_z([(z, -37, -36) for z in range(-28, -34, -1)], 23, "-z")     # the north-west corner, rising north
    R.flight_z([(z, 35, 36) for z in range(-28, -34, -1)], 23, "-z")       # the north-east corner
    # the parkour from the Ledge to the Middle: two pillars, 2 then 2 then 3 blocks apart, each a block higher
    R.rect(-1, 0, -17, -16, 17, "floor")
    R.rect(-1, 0, -13, -12, 18, "floor")
    # ladders out of the pool, up the Ledge's face, four a side
    # a ladder is the pool cell against the Ledge's face; its top is the Ledge, so it is climbed out onto the Ledge
    for x, z in ((-20, -19), (-20, 18), (-23, -12), (-23, 11)):
        for a, b in ((x, z), rot(x, z)):
            R.K[ix(a), iz(b)] = KINDS["ladder"]
            R.H[ix(a), iz(b)] = 16
    return R


# ---- the routes' special edges, which a height raster cannot hold ----------------------------------------------
# the tunnel: from red's spawn, down inside the wall to the Ledge's north-west corner. A polyline of (x, z, y).
TUNNEL = [(-50, -7, 28), (-50, -24, 16), (-30, -24, 16)]

# jump pads: the pad's cells (x0, x1, z0, z1, floor y), the velocity, and what it is for
PADS = [
    dict(key="mid-north", cells=(-9, -8, -9, -8, 19), v=(-0.62, 0.85, -2.42),
         why="from the Middle's apron to the North hill's west flank: rotate to a side hill after taking mid"),
    dict(key="ledge-rim", cells=(-29, -27, -25, -23, 16), v=(-1.33, 1.55, -1.43),
         why="from the Ledge's corner up to the Rim's corner: out of the low ground, onto the drop above a hill"),
]
# the drop: from the Rim straight down onto a side hill, 5 blocks, one way
DROPS = [dict(key="rim-north", at=(-4, 3, -36, -34), onto="hill N", height=5)]

HILLS = [dict(key="mid", name="the Middle", box=(-4, 3, -4, 3), y=22, points=2),
         dict(key="north", name="the North hill", box=(-4, 3, -33, -26), y=23, points=1),
         dict(key="south", name="the South hill", box=(-4, 3, 25, 32), y=23, points=1)]
GAPPLE_AT = (-0.5, 15, -0.5)        # the Spring: under the Middle, reached by two stairwells off the apron
SPAWN_POINT = (-51.5, 29, -0.5)
