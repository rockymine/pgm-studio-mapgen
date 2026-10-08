"""Riad — a King of the Flag plan: a palace water-garden over the void, one flag, three posts.

One flag, shared: a player standing with it scores a point a second for their team, and while a team holds it
its dead do not come back. When the carrier dies the flag is gone for a while and then comes back at one of
three posts, chosen at random:

    the Cistern   the middle: a banner on a tower in a pool one deep, reached only by swimming up one of two
                  water columns caged against its faces; a landing either side, two under the top, takes the
                  carrier back to the court
    the Mirador   the west: a banner on a pad at the end of a bridge over the void, ten long, from a raised
                  porch that each team climbs to by its own stair
    the Minaret   the east: a banner on a pillar in a sunken garden, reached by a ladder on any of its faces

Red spawns in the north, blue in the south, and blue's half is red's mirrored, z -> -z; nothing is mirrored
in x, which is why the east and the west posts can be different things and still the same walk for both
teams. A spawn is a terrace two over the ground: a player steps off it and nobody climbs back.

The plan is two rasters: the ground, every column's floor height and kind, and over it the arcade roofs. The
checker walks both, the sketch draws both, and the generator builds from both.

    heights are the top block a player stands on: 17 the sunken gardens, 18 the Cistern's floor and 19 its
    water, 20 the ground, 21..23 the parkour stones, 22 the Cistern's landings, the Minaret and the spawn
    terraces, 24 the porch, bridge and pad, the Cistern's tower and the arcade roofs
"""
import numpy as np

X_MIN, X_MAX = -48, 47
Z_MIN, Z_MAX = -60, 60
NX, NZ = X_MAX - X_MIN + 1, Z_MAX - Z_MIN + 1
G = 20                      # the ground
LOW = 17                    # the sunken gardens
CISTERN = dict(floor=18, water=19, sump=17)
KINDS = {"void": 0, "floor": 1, "wall": 2, "water": 3, "canal": 4, "stair": 5, "ladder": 6, "post": 7,
         "spawn": 8, "hedge": 9, "column": 10, "swim": 11, "cage": 12, "stone": 13, "bridge": 14, "tree": 15}
UKINDS = {"none": 0, "roof": 1, "deck": 2}
WALK = {"floor", "canal", "stair", "post", "spawn", "stone", "bridge"}
SOLID = {"wall", "hedge", "column", "cage", "tree"}


def ix(x):
    return x - X_MIN


def iz(z):
    return z - Z_MIN


def H_at(x, z):
    return int(_R.H[ix(x), iz(z)])


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

    def flight_x(self, rows, h0, rises, both=True):
        """A stair along x: `rows` are (x, z0, z1) in climbing order, the first at h0, one up per row."""
        for k, (x, z0, z1) in enumerate(rows):
            for z in range(z0, z1 + 1):
                for zz in ([z] + ([mz(z)] if both else [])):
                    self.H[ix(x), iz(zz)] = h0 + k
                    self.K[ix(x), iz(zz)] = KINDS["stair"]
                    self.stair[(x, zz)] = rises

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
    R.rect(-6, 6, -6, 6, CISTERN["water"], "water", both=False)  # the Cistern: a pool one deep
    R.rect(-1, 1, -1, 1, 24, "post", both=False)               # its tower, four over the court
    R.cell(0, 2, 24, "swim")                                   # a water column on its north and south faces,
    for x, z in ((-1, 2), (1, 2), (0, 3)):                     # caged in glass from 20 to 24, over a sump two
        R.cell(x, z, 24, "cage")                               # deep: duck under the cage's lip, swim up
    R.rect(2, 6, -1, 1, 22, both=False)                        # the landings: a causeway east and west off the
    R.rect(-6, -2, -1, 1, 22, both=False)                      # tower, two under its top and two over the court
    for sx in (-1, 1):                                         # the court's void holes, a stone in each
        R.rect(min(8 * sx, 12 * sx), max(8 * sx, 12 * sx), 8, 12, 0, "void")
        R.cell(10 * sx, 10, G, "stone")
    for x, z in ((-15, 13), (14, 13)):                         # trees at the court's corners
        R.cell(x, z, G + 5, "tree")
    # the Mirador: a porch four up, each team's stair onto it, a bridge west over the void to the post's pad
    R.rect(-44, -18, 6, 16, G)                                 # the balconies beside the bridge, at the ground
    R.rect(-30, -20, -5, 5, 24, both=False)                    # the porch, where a team waits for the flag
    R.flight_z([(z, -27, -25) for z in range(9, 5, -1)], 21, "-z")     # 21 at z 9 .. 24 at z 6: the porch
    R.rect(-40, -31, -1, 1, 24, "bridge", both=False)          # ten long, three wide, nothing either side
    R.rect(-43, -41, -1, 1, 24, "post", both=False)            # the pad, 3 x 3
    R.cell(-38, 12, G + 5, "tree")
    # the Minaret's garden, sunk three: a ring at the ground round it, a stair down from the court and one from
    # either side of the ring, the pillar five over the garden with a ladder on each face, the void behind
    R.rect(18, 42, -16, 16, G, both=False)
    R.rect(21, 42, -13, 13, LOW, both=False)
    R.flight_x([(x, -2, 2) for x in range(20, 17, -1)], LOW + 1, "-x", both=False)   # 18 at x 20 .. 20 at x 18
    R.flight_z([(z, 33, 35) for z in range(11, 14)], LOW + 1, "+z")                  # 18 at z 11 .. 20 at z 13
    R.rect(29, 31, -1, 1, LOW + 5, "post", both=False)
    for x, z in ((30, -2), (30, 2), (28, 0), (32, 0)):
        R.cell(x, z, LOW + 5, "ladder", both=False)
    for x0, x1, z0, z1 in ((24, 25, 5, 6), (35, 36, 5, 6), (38, 39, -1, 1)):
        R.rect(x0, x1, z0, z1, LOW + 2, "hedge")
    R.cell(38, 9, LOW + 5, "tree")
    # ---- each team's half, z 17 .. 56 (blue's; red's is its mirror) ---------------------------------------
    for sx in (-1, 1):                                         # the gardens, sunk three either side of the lane
        R.rect(*sorted((14 * sx, 36 * sx)), 17, 36, LOW)
    R.rect(-8, 8, 17, 36, G)                                   # the lane down the axis
    R.rect(-2, 2, 17, 36, G, "canal")                          # the canal, one deep
    for x0 in (-13, 9):                                        # an arcade either side of the canal: columns
        R.rect(x0, x0 + 4, 17, 38, G)                          # every four, a walk three wide under a roof
        for z in range(18, 39, 4):
            R.cell(x0, z, 24, "column")
            R.cell(x0 + 4, z, 24, "column")
        R.upper(x0, x0 + 4, 18, 38, 24)
    R.rect(-22, 22, 37, 56, G)                                 # the back garden
    for sx in (-1, 1):
        lo = lambda a, b: sorted((a * sx, b * sx))
        # the stairs into each garden: from the middle band, from the arcade, from the back garden
        R.flight_z([(z, *lo(24, 26)) for z in range(19, 16, -1)], LOW + 1, "-z")     # 18 at z 19 .. 20 at z 17
        if sx > 0:
            R.flight_x([(x, 27, 29) for x in range(16, 13, -1)], LOW + 1, "-x")      # 18 at x 16 .. 20 at x 14
        else:
            R.flight_x([(x, 27, 29) for x in range(-16, -13)], LOW + 1, "+x")
        R.flight_z([(z, *lo(18, 20)) for z in range(34, 37)], LOW + 1, "+z")         # 18 at z 34 .. 20 at z 36
        R.rect(*lo(22, 28), 24, 30, LOW + 9, "wall")                                # the kiosk / fountain house
        R.rect(*lo(31, 35), 23, 29, 0, "void")                                       # a void hole by the edge,
        R.cell(33 * sx, 25, LOW, "stone")                                            # two stones to cross it by
        R.cell(33 * sx, 27, LOW, "stone")
        for x, z in ((19, 23), (33, 20), (31, 33)):                                  # trees
            R.cell(x * sx, z, LOW + 5, "tree")
        for x0, x1, z0, z1 in ((20, 22, 31, 31), (29, 29, 19, 21)):                  # hedges
            R.rect(*lo(x0, x1), z0, z1, LOW + 2, "hedge")
        # the parkour onto the arcade roof: three stones from the back garden, each a block up
        for k, (x, z) in enumerate(((17, 44), (16, 41), (14, 40))):
            R.cell(x * sx, z, G + 1 + k, "stone")
    for x0, x1 in ((-6, -5), (5, 6)):                          # small cover by the canal
        R.rect(x0, x1, 26, 27, G + 2, "hedge")
    # the spawn: a terrace two over the back garden, so nobody climbs back onto it
    R.rect(-10, 10, 46, 56, G + 2, "spawn")
    return R


# the flag's posts: where the banner stands, and the first is where the flag is at the start
POSTS = [dict(key="cistern", name="the Cistern", at=(0.5, 25, 0.5), yaw=None),
         dict(key="mirador", name="the Mirador", at=(-41.5, 25, 0.5), yaw=90),
         dict(key="minaret", name="the Minaret", at=(30.5, 23, 0.5), yaw=-90)]
SPAWNS = dict(red=(0.5, 23, -51.5, 0), blue=(0.5, 23, 52.5, 180))
SUMP = {(x, z) for x in range(-2, 3) for z in (2, 3, 4, -2, -3, -4)}    # the water two deep at the columns' feet


_R = build()
