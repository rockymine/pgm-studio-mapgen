"""Riad — a King of the Flag plan: a walled water-garden palace, one flag, three posts.

One flag, shared: a player standing with it scores a point a second for their team, and while a team holds it
its dead do not come back. When the carrier dies the flag is gone for a while and then comes back at one of
three posts, chosen at random:

    the Cistern   the middle: a banner on a tower standing in a deep pool, reached only by swimming up one
                  of two water columns caged against its faces
    the Mirador   the west: a banner on a pad at the end of a bridge over the void, ten long, from a raised
                  porch that each team climbs to by its own stair
    the Minaret   the east: a banner on a pillar in a garden, reached by a ladder on any of its four faces

Red spawns in the north, blue in the south, and blue's half is red's mirrored, z -> -z; nothing is mirrored
in x, which is why the east and the west posts can be different things and still the same walk for both
teams. A spawn is a room raised over its patio, and a player leaves it by dropping through a hole in its
floor into a pool: the way out is one-way.

The plan is two rasters: the ground, every column's floor height and kind, and over it the upper storey,
the arcade roofs and the spawn decks. The checker walks both, the sketch draws both, and the generator will
build from both.

    heights are the top block a player stands on: 12 the Cistern's floor, 19 the water in it, 20 the ground,
    21..23 the parkour stones, 24 the porch, bridge and pad, the Cistern's tower and the arcade roofs, 25 the
    Minaret, 32 the spawn decks
"""
import numpy as np

X_MIN, X_MAX = -48, 47
Z_MIN, Z_MAX = -60, 60
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
G = 20                      # the ground
KINDS = {"void": 0, "floor": 1, "wall": 2, "water": 3, "canal": 4, "stair": 5, "ladder": 6, "post": 7,
         "spawn": 8, "hedge": 9, "column": 10, "swim": 11, "cage": 12, "stone": 13, "bridge": 14}
UKINDS = {"none": 0, "roof": 1, "deck": 2}
WALK = {"floor", "canal", "stair", "post", "spawn", "stone", "bridge"}
SOLID = {"wall", "hedge", "column", "cage"}


def ix(x):
    return x - X_MIN


def iz(z):
    return z - Z_MIN


def mz(z):
    return -z


class Raster:
    def __init__(self):
        self.H = np.full((NX, NZ), 0, int)
        self.K = np.full((NX, NZ), KINDS["void"], int)
        self.U = np.full((NX, NZ), -1, int)            # the upper storey's floor, or -1
        self.UK = np.full((NX, NZ), 0, int)
        self.stair = {}                                # (x, z) -> the way it rises: +x -x +z -z

    def rect(self, x0, x1, z0, z1, h, kind="floor", both=True):
        for a0, a1 in ([(z0, z1)] + ([(mz(z1), mz(z0))] if both else [])):
            self.H[ix(x0):ix(x1) + 1, iz(a0):iz(a1) + 1] = h
            self.K[ix(x0):ix(x1) + 1, iz(a0):iz(a1) + 1] = KINDS[kind]

    def upper(self, x0, x1, z0, z1, h, kind="roof", both=True):
        for a0, a1 in ([(z0, z1)] + ([(mz(z1), mz(z0))] if both else [])):
            self.U[ix(x0):ix(x1) + 1, iz(a0):iz(a1) + 1] = h
            self.UK[ix(x0):ix(x1) + 1, iz(a0):iz(a1) + 1] = UKINDS[kind]

    def cell(self, x, z, h, kind, both=True):
        self.rect(x, x, z, z, h, kind, both)

    def flight_z(self, rows, h0, rises, both=True):
        """A stair along z: `rows` are (z, x0, x1) in climbing order, the first at h0, one up per row."""
        for k, (z, x0, x1) in enumerate(rows):
            for x in range(x0, x1 + 1):
                for zz, r in ([(z, rises)] + ([(mz(z), {"+z": "-z", "-z": "+z"}[rises])] if both else [])):
                    self.H[ix(x), iz(zz)] = h0 + k
                    self.K[ix(x), iz(zz)] = KINDS["stair"]
                    self.stair[(x, zz)] = r


def build():
    R = Raster()
    # ---- the middle band: the court, the Cistern, the Mirador to the west and the Minaret's garden east ----
    R.rect(-19, 17, -16, 16, G, both=False)                    # the court, up to the porch's foot
    R.rect(-6, 6, -6, 6, G - 1, "water", both=False)           # the Cistern: a pool, floor at 12, water to 19
    R.rect(-1, 1, -1, 1, 24, "post", both=False)               # its tower, four over the court
    R.cell(0, 2, 24, "swim")                                   # a water column on its north and south faces,
    for x, z in ((-1, 2), (1, 2), (0, 3)):                     # caged in glass from 20 to 24: dive under the
        R.cell(x, z, 24, "cage")                               # cage's lip, swim up, step out onto the top
    for x, z in ((-11, 11), (11, 11)):                         # the court's cover: four planters, 3 x 3, two high
        R.rect(x - 1, x + 1, z - 1, z + 1, G + 2, "hedge")
    for x, z in ((-9, 0), (9, 0), (0, 9)):                     # and four cypresses on the Cistern's axes, one
        R.cell(x, z, G + 5, "hedge")                           # in front of each swim column and either side
    # the Mirador: a porch four up, each team's stair onto it, a bridge west over the void to the post's pad
    R.rect(-44, -18, 6, 16, G)                                 # the balconies beside the bridge, at the ground
    R.rect(-30, -20, -5, 5, 24, both=False)                    # the porch, where a team waits for the flag
    R.flight_z([(z, -27, -25) for z in range(9, 5, -1)], 21, "-z")     # 21 at z 9 .. 24 at z 6: the porch
    R.rect(-40, -31, -1, 1, 24, "bridge", both=False)          # ten long, three wide, nothing either side
    R.rect(-43, -41, -1, 1, 24, "post", both=False)            # the pad, 3 x 3
    R.rect(-44, -44, 6, 7, G + 2, "hedge")                     # a parapet at the balcony's far corner
    # the Minaret's garden: the pillar five up, a ladder on each face, hedges round it, the void behind
    R.rect(18, 42, -16, 16, G, both=False)
    R.rect(29, 31, -1, 1, 25, "post", both=False)
    for x, z in ((30, -2), (30, 2), (28, 0), (32, 0)):
        R.cell(x, z, 25, "ladder", both=False)
    for x0, x1, z0, z1 in ((23, 25, 5, 6), (35, 37, 5, 6), (23, 23, 3, 4), (37, 37, 3, 4), (38, 39, -1, 1)):
        R.rect(x0, x1, z0, z1, G + 2, "hedge")
    # ---- each team's half, z 17 .. 60 (blue's; red's is its mirror) ---------------------------------------
    R.rect(-36, 36, 17, 36, G)                                 # the gardens
    R.rect(-22, 22, 37, 40, G)
    R.rect(-2, 2, 17, 36, G, "canal")                          # the canal, one deep, down the axis
    for x0 in (-13, 9):                                        # an arcade either side of the canal: columns
        for z in range(18, 39, 4):                             # every four, a walk three wide under a roof
            R.cell(x0, z, 24, "column")
            R.cell(x0 + 4, z, 24, "column")
        R.upper(x0, x0 + 4, 18, 38, 24)
    R.rect(-28, -22, 24, 30, 26, "wall")                       # the west garden's kiosk: large cover
    R.rect(22, 28, 24, 30, 26, "wall")                         # the east garden's fountain house
    for x0, x1, z0, z1 in ((-34, -30, 20, 20), (-19, -17, 33, 33), (30, 34, 20, 20), (17, 19, 33, 33),
                           (-19, -16, 25, 26), (16, 19, 25, 26), (-34, -33, 28, 31), (33, 34, 28, 31),
                           (-6, -5, 26, 27), (5, 6, 26, 27)):  # small cover in the gardens and by the canal
        R.rect(x0, x1, z0, z1, G + 2, "hedge")
    R.rect(-22, 22, 41, 56, G)                                 # the back garden, round the spawn house
    # the parkour onto the arcade roofs: three stones from the back garden, each a block up and two apart
    for k, z in enumerate((46, 43, 40)):
        R.rect(11, 11, z, z, G + 1 + k, "stone")
        R.rect(-11, -11, z, z, G + 1 + k, "stone")
    # the spawn house: a room on the deck at 32 over a patio; a hole in the deck over the pool; a door either
    # side, each behind a screen wall so nothing on the board sees into it
    R.rect(-9, 9, 45, 58, 37, "wall")
    R.rect(-7, 7, 46, 56, G, "spawn")                          # the patio
    R.rect(-2, 2, 47, 51, G, "water")                          # the pool, three deep, under the hole
    R.rect(-9, -8, 50, 54, G, "spawn")                         # the doors out, west and east
    R.rect(8, 9, 50, 54, G, "spawn")
    R.rect(-13, -13, 44, 57, 25, "wall")                       # the screens
    R.rect(13, 13, 44, 57, 25, "wall")
    R.upper(-7, 7, 46, 56, 32, "deck")
    for z0, z1 in ((47, 51), (-51, -47)):                      # the hole
        R.U[ix(-2):ix(2) + 1, iz(z0):iz(z1) + 1] = -1
        R.UK[ix(-2):ix(2) + 1, iz(z0):iz(z1) + 1] = 0
    return R


# the flag's posts: where the banner stands, and the first is where the flag is at the start
POSTS = [dict(key="cistern", name="the Cistern", at=(0.5, 25, 0.5), yaw=None),
         dict(key="mirador", name="the Mirador", at=(-41.5, 25, 0.5), yaw=90),
         dict(key="minaret", name="the Minaret", at=(30.5, 26, 0.5), yaw=-90)]
SPAWNS = dict(red=(0.5, 33, -54.5, 0), blue=(0.5, 33, 55.5, 180))
CARRIER_LINE = 32           # the carrier may not pass |z| >= 38: the back gardens are where the dead come back
CISTERN = dict(floor=12, water=19)
