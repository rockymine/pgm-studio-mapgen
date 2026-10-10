"""Lantern Pass — a runners-and-shooters plan: a festival road from a harbour up a mountain to a temple bell.

Twenty-odd runners, one life each, cross a long lane of seven sections; four shooters with power bows run along
two walkways that flank the lane across fourteen blocks of void, ten above it. A runner who stands under the
temple bell for two seconds wins it for the runners; the shooters win when the clock runs out.

    0  the boathouse   the runners' spawn, shut for the warm-up
    1  the harbour     a boardwalk, a chain of moored barges, open water between them
    2  the market      three avenues between rows of stalls, the stalls' awnings over them
    3  the terraces    five rice terraces climbing ten, paddies and bunds, stair cuts in the risers
    4  the bamboo      a grove too thick to see through, a path through it, a shrine that heals
    5  the gorge       void across the lane, crossed by a rope bridge, stepping pillars, or a low arch
    6  the stairs      the temple's great stair, sixteen up, torii gates over it
    7  the temple      a court, and the bell tower at its head

The plan is a height raster over the lane and the walkways with a kind for every column, the top of whatever
stands on it, and the height of an awning or a roof over it where one is. The checker walks the lane and reads,
for every cell a runner can stand on, whether a shooter on either walkway can see it.

    heights are the top block a player stands on: 20 the harbour, 22 the market, 24 to 32 the terraces, 32 the
    bamboo and the gorge's near side, 34 its far side, 34 to 50 the stairs, 50 the temple; a walkway stands ten
    over the highest lane beside it
"""
import math

import numpy as np

X_MIN, X_MAX = -34, 33
Z_MIN, Z_MAX = -12, 374
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
LANE = (-12, 11)
WALKS = {"left": (-31, -27), "right": (26, 30)}                 # x ranges; the outer row is the side-swap
SWAP_DX = {"left": 58, "right": -58}
VOID = -99
KINDS = {"void": 0, "plank": 1, "street": 2, "grass": 3, "paddy": 4, "bund": 5, "stair": 6, "bamboo": 7,
         "cover": 8, "house": 9, "water": 10, "bridge": 11, "pillar": 12, "stone": 13, "walk": 14, "swap": 15,
         "wall": 16, "gate": 17, "floor": 18}
WALK = {"plank", "street", "grass", "paddy", "bund", "stair", "bridge", "pillar", "stone", "floor", "water"}
SECTIONS = [  # key, name, z0, z1
    (0, "the boathouse", -10, 4), (1, "the harbour", 5, 60), (2, "the market", 61, 115),
    (3, "the terraces", 116, 170), (4, "the bamboo", 171, 225), (5, "the gorge", 226, 275),
    (6, "the stairs", 276, 330), (7, "the temple", 331, 372),
]
BELL = dict(box=(-3, 2, 357, 363), y=51)                       # the capture region under the bell
HEAL = dict(box=(-5, 4, 218, 224))                              # the shrine's floor: health on entering
SPAWN_GATE = (-3, 2, 4, 4)
WARMUP = "10s"
TIME = "5m"


def ix(x):
    return x - X_MIN


def iz(z):
    return z - Z_MIN


class Raster:
    def __init__(self):
        self.H = np.full((NX, NZ), VOID, int)                   # the floor a player stands on
        self.K = np.full((NX, NZ), KINDS["void"], int)
        self.T = np.full((NX, NZ), VOID, int)                   # the top of what is solid in the column
        self.C = np.full((NX, NZ), -1, int)                     # an awning or a roof: one block at this y
        self.stair = {}

    def rect(self, x0, x1, z0, z1, h, kind, top=None):
        sl = (slice(ix(x0), ix(x1) + 1), slice(iz(z0), iz(z1) + 1))
        self.H[sl] = h
        self.K[sl] = KINDS[kind]
        self.T[sl] = h if top is None else top

    def solid(self, x0, x1, z0, z1, tall, kind="cover"):
        """Something standing on the floor, `tall` high: cover, a stall, a hut, a house."""
        sl = (slice(ix(x0), ix(x1) + 1), slice(iz(z0), iz(z1) + 1))
        self.T[sl] = self.H[sl] + tall
        self.K[sl] = KINDS[kind]

    def canopy(self, x0, x1, z0, z1, y):
        self.C[ix(x0):ix(x1) + 1, iz(z0):iz(z1) + 1] = y

    def flight(self, x0, x1, zs, h0, rises="+z"):
        for k, z in enumerate(zs):
            self.rect(x0, x1, z, z, h0 + k, "stair")
            for x in range(x0, x1 + 1):
                self.stair[(x, z)] = rises


rng = np.random.default_rng(7)


def _leaves():
    from scipy import ndimage
    g = np.random.default_rng(11).normal(size=(NX // 3 + 3, NZ // 3 + 3))
    return ndimage.zoom(g, 3, order=1)[:NX, :NZ]


LEAVES = _leaves()

# ---- the sections -------------------------------------------------------------------------------------------
BARGES = [(4, 10, 8, 16), (4, 10, 19, 27), (4, 10, 30, 38), (4, 10, 41, 49)]      # moored, a jump apart
PIERS = [(-12, 3, 15, 17), (-12, 3, 32, 34), (-12, 3, 49, 51)]
HARBOUR_COVER = [(-11, -10, 9, 10, 2), (-9, -9, 22, 23, 2), (-11, -10, 28, 28, 1), (-10, -9, 40, 41, 2),
                 (-11, -11, 46, 47, 2), (-4, -2, 56, 57, 2), (5, 7, 56, 56, 1)]
CABINS = [(6, 9, 10, 13), (6, 9, 32, 35)]                       # deckhouses on two barges
STALL_ROWS = [(-7, -3), (2, 5)]                                 # x ranges; the avenues lie either side
STALLS_Z = [(64, 68), (71, 75), (78, 82), (86, 90), (93, 97), (100, 104), (107, 111)]
TERRACES = [(116, 125, 24), (126, 135, 26), (136, 145, 28), (146, 155, 30), (156, 170, 32)]
TERRACE_CUTS = [(-10, -8), (0, 2), (8, 10)]                      # stair cuts in each riser, by x
HUTS = [(4, 6, 119, 121), (-9, -7, 130, 132), (1, 3, 140, 142), (-5, -3, 150, 152)]
GORGE = dict(z0=232, z1=267)
ROPE = dict(x0=-9, x1=-8)
PILLARS = [(0, 234, 32), (-1, 238, 33), (1, 242, 33), (0, 246, 34), (-1, 250, 33), (1, 254, 34), (0, 258, 34),
           (-1, 262, 34), (0, 266, 34)]                                       # (x, z, h): 2 x 2 tops, a sprint jump apart
ARCH = dict(x0=7, x1=9, h=26)
TORII = [284, 294, 304, 314, 324]
LANTERNS = [(-11, 288), (10, 288), (-11, 300), (10, 300), (-11, 312), (10, 312), (-6, 336), (5, 336),
            (-6, 346), (5, 346)]
PINES = [(-11, 280), (10, 283), (-11, 296), (10, 307), (-11, 320), (10, 322)]


def stair_h(z):
    """The great stair: two steps up, three flat, from 34 at z 280 to 50 at z 320."""
    if z < 280:
        return 34
    if z > 319:
        return 50
    k = z - 280
    return 34 + 2 * (k // 5) + min(2, k % 5)


def build():
    R = Raster()
    lx0, lx1 = LANE
    # 0 the boathouse
    R.rect(lx0 + 2, lx1 - 2, -10, 4, 20, "floor")
    for x in range(lx0 + 2, lx1 - 1):
        for z in (-10, 4):
            R.solid(x, x, z, z, 7, "wall")
    for z in range(-10, 5):
        R.solid(lx0 + 2, lx0 + 2, z, z, 7, "wall")
        R.solid(lx1 - 2, lx1 - 2, z, z, 7, "wall")
    R.canopy(lx0 + 2, lx1 - 2, -10, 4, 28)
    R.rect(SPAWN_GATE[0], SPAWN_GATE[1], 4, 4, 20, "gate", top=27)
    # 1 the harbour: water, a boardwalk on the west, piers across, barges on the east, a quay at its head
    R.rect(lx0, lx1, 5, 60, 17, "water")
    R.rect(lx0, lx0 + 3, 5, 60, 20, "plank")
    for x0, x1, z0, z1 in PIERS:
        R.rect(x0, x1, z0, z1, 20, "plank")
    for x0, x1, z0, z1 in BARGES:
        R.rect(x0, x1, z0, z1, 20, "plank")
    R.rect(lx0, lx1, 5, 6, 20, "plank")                       # the landing outside the boathouse
    R.rect(lx0, lx1, 53, 60, 20, "stone")                     # the quay
    R.rect(lx1, lx1, 5, 60, 20, "stone")                      # the harbour wall on the east, holding the water
    for x0, x1, z0, z1 in CABINS:
        R.solid(x0, x1, z0, z1, 3, "house")
    for x0, x1, z0, z1, t in HARBOUR_COVER:
        R.solid(x0, x1, z0, z1, t)
    # 2 the market: up two onto the street; stalls in two rows, awnings over the rows and a block either side
    R.rect(lx0, lx1, 61, 115, 22, "street")
    R.flight(lx0, lx1, [59, 60], 21)
    for x0, x1 in STALL_ROWS:
        for z0, z1 in STALLS_Z:
            R.solid(x0, x1, z0, z1, 3, "house")
            R.canopy(x0 - 1, x1 + 1, z0, z1, 26)
    for z in range(63, 113):                                    # the arcade: the middle of the street roofed over,
        if z not in (76, 77, 91, 92):                           # open to the sky at two light wells
            R.canopy(-8, 6, z, z, 26)
    # 3 the terraces: risers two high, cut by stairs; paddies with bunds every fifth block either way
    for z0, z1, h in TERRACES:
        R.rect(lx0, lx1, z0, z1, h, "paddy")
        R.H[ix(lx0):ix(lx1) + 1, iz(z0):iz(z1) + 1] = h - 1     # a paddy's floor is a block under its bund
        R.T[ix(lx0):ix(lx1) + 1, iz(z0):iz(z1) + 1] = h - 1
        for x in range(lx0, lx1 + 1):
            for z in range(z0, z1 + 1):
                if (x - lx0) % 5 == 0 or (z - z0) % 5 == 0 or z == z1 or x == lx1:
                    R.rect(x, x, z, z, h, "bund")
        if z0 > 116:
            n = (z0 - 116) // 10
            cx0, cx1 = TERRACE_CUTS[(n + 1) % 3]
            R.flight(cx0, cx1, [z0 - 1, z0], h - 1)             # the cut: a step from the bund below
    R.flight(lx0, lx1, [116, 117], 23)                          # up from the market
    for x0, x1, z0, z1 in HUTS:
        R.solid(x0, x1, z0, z1, 4, "house")
    # 4 the bamboo: thick, with one path through it and the shrine at its head
    R.rect(lx0, lx1, 171, 225, 32, "grass")
    path = bamboo_path()
    for z in range(171, 218):
        for x in range(lx0, lx1 + 1):
            if (x, z) in path:
                R.rect(x, x, z, z, 32, "stone")
            elif rng.random() < 0.145:
                R.solid(x, x, z, z, 9, "bamboo")
            if LEAVES[ix(x), iz(z)] > -0.15:                    # the grove's crown, closed over most of it
                R.canopy(x, x, z, z, 40)
    R.rect(HEAL["box"][0], HEAL["box"][1], HEAL["box"][2], HEAL["box"][3], 32, "floor")
    R.canopy(HEAL["box"][0] - 1, HEAL["box"][1] + 1, HEAL["box"][2], HEAL["box"][3], 37)
    # 5 the gorge: void; a rope bridge, stepping pillars, a low arch under a gallery roof
    R.rect(lx0, lx1, 226, 231, 32, "grass")
    R.rect(lx0, lx1, 268, 275, 34, "grass")
    R.rect(ROPE["x0"], ROPE["x1"], GORGE["z0"], GORGE["z1"], 0, "bridge")
    for z in range(GORGE["z0"], GORGE["z1"] + 1):               # the rope bridge sags three in its middle
        t = (z - GORGE["z0"]) / (GORGE["z1"] - GORGE["z0"])
        h = int(round(32 + 2 * t - 3 * math.sin(math.pi * t)))
        R.rect(ROPE["x0"], ROPE["x1"], z, z, h, "bridge")
    for x, z, h in PILLARS:
        R.rect(x, x + 1, z, z + 1, h, "pillar")
    R.flight(ARCH["x0"], ARCH["x1"], list(range(231, 225, -1)), ARCH["h"], "-z")   # down from the near side
    R.rect(ARCH["x0"], ARCH["x1"], GORGE["z0"], GORGE["z1"], ARCH["h"], "stone")
    R.canopy(ARCH["x0"] - 1, ARCH["x1"] + 1, GORGE["z0"], GORGE["z1"], ARCH["h"] + 4)
    for z in range(GORGE["z0"], GORGE["z1"] + 1):               # the gallery's walls, with windows
        if (z - GORGE["z0"]) % 7 not in (3, 4):
            for x in (ARCH["x0"] - 1, ARCH["x1"] + 1):
                R.rect(x, x, z, z, ARCH["h"], "wall", top=ARCH["h"] + 3)
    R.flight(ARCH["x0"], ARCH["x1"], list(range(268, 276)), ARCH["h"] + 1)         # up to the far side, 27 .. 34
    # 6 the stairs: the great stair in the middle, terraces either side with lanterns and pines
    for z in range(276, 331):
        h = stair_h(z)
        rising = 280 <= z <= 319 and (z - 280) % 5 in (1, 2)
        R.rect(lx0 + 4, lx1 - 4, z, z, h, "stair" if rising else "stone")
        for x in range(lx0 + 4, lx1 - 3):
            if rising:
                R.stair[(x, z)] = "+z"
        R.rect(lx0, lx0 + 3, z, z, h, "grass")
        R.rect(lx1 - 3, lx1, z, z, h, "grass")
    for z in TORII:
        for x in (lx0 + 5, lx1 - 5):
            R.solid(x, x, z, z, 6, "cover")
        R.canopy(lx0 + 3, lx1 - 3, z, z, stair_h(z) + 6)
    for x, z in LANTERNS[:6]:
        R.solid(x, x, z, z, 3)
    for x, z in PINES:
        R.solid(x, x, z, z, 8)
    # 7 the temple court and the bell tower
    R.rect(lx0, lx1, 331, 372, 50, "stone")
    for x, z in LANTERNS[6:]:
        R.solid(x, x, z, z, 3)
    R.solid(-2, 1, 340, 341, 2)                                  # the incense burner
    bx0, bx1, bz0, bz1 = BELL["box"]
    for x in (bx0 - 1, bx1 + 1):
        for z in (bz0 - 1, bz1 + 1):
            R.solid(x, x, z, z, 7, "cover")                     # the tower's four posts
    R.canopy(bx0 - 2, bx1 + 2, bz0 - 2, bz1 + 2, 57)
    R.solid(lx0, lx1, 366, 372, 12, "house")                    # the temple hall behind
    # the walkways: ten over the highest lane beside them, never more than a block a block between
    hw = walkway_heights(R)
    for side, (x0, x1) in WALKS.items():
        outer = x0 if side == "left" else x1
        for z in range(Z_MIN + 2, Z_MAX - 1):
            R.rect(x0, x1, z, z, hw[iz(z)], "walk")
            R.rect(outer, outer, z, z, hw[iz(z)], "swap")
            wall = outer - 1 if side == "left" else outer + 1
            R.rect(wall, wall, z, z, hw[iz(z)], "wall", top=hw[iz(z)] + 4)
    return R


def bamboo_path():
    """The path through the bamboo: a wandering line two wide, from the terraces' head to the shrine."""
    pts = []
    x = -1.0
    for z in range(171, 218):
        x += math.sin(z / 6.0) * 1.1
        x = max(-10, min(9, x))
        for dx in (0, 1):
            pts.append((int(round(x)) + dx, z))
    return set(pts)


def walkway_heights(R):
    lane = R.H[ix(LANE[0]):ix(LANE[1]) + 1, :]
    top = lane.max(axis=0)
    hw = np.array([max(top[max(0, j - 6):j + 7].max(), 20) + 10 for j in range(NZ)])
    for j in range(1, NZ):                                      # rise early: never more than a block a block
        hw[j] = max(hw[j], hw[j - 1] - 1)
    for j in range(NZ - 2, -1, -1):
        hw[j] = max(hw[j], hw[j + 1] - 1)
    return hw


KN = {v: k for k, v in KINDS.items()}
