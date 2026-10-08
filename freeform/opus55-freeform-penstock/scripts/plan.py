"""Penstock — a Team Deathmatch plan: the inside of a hydroelectric station, carved out of one block of concrete.

Red holds the west (x < 0), blue the east; blue's half is red's mirrored, x -> -1 - x. Every piece below is red's.
The station is mostly z-symmetric as well, so both flanks play alike, but the two score boxes on a team's back
wall differ: one is entered through a cobweb door, the other across a cobweb floor.

A space is a box of air (x0, x1, z0, z1, floor y, ceiling y): the floor block is at `floor`, players stand at
floor + 1, and the first solid block overhead is at `ceil`. A slab is a deck at a height inside a space.

    levels:  14 the penstock tunnels, 20 the hall and the galleries, 22 the exciter dais, 24 the spawns,
             27 the control walk, the catwalks and the gantry; the roof at 36.
"""
X_MIN, X_MAX = -70, 69
Z_MIN, Z_MAX = -48, 47
Y_TOP = 64
ROOF = 36
MASS_BOTTOM = 12           # the underside of the station; void below
KILL_Y = 8                 # a fall down a tailrace shaft ends here


def mx(x):
    return -1 - x


def both_z(x0, x1, z0, z1):
    """A piece and its twin across the station's long axis (z -> -1 - z)."""
    return [(x0, x1, z0, z1), (x0, x1, -1 - z1, -1 - z0)]


# ---- the spaces (air) -------------------------------------------------------------------------------------
SPACES = [
    dict(key="spawn", name="the Gatehouse", box=(-69, -57, -11, 10), floor=24, ceil=32),
    dict(key="gallery", name="the Intake Gallery", box=(-55, -44, -47, 46), floor=20, ceil=ROOF),
    dict(key="hall", name="the Turbine Hall", box=(-43, -1, -36, 35), floor=20, ceil=ROOF),
]
for i, b in enumerate(both_z(-43, -17, -47, -38)):
    SPACES.append(dict(key=f"corridor-{i}", name="the Cable Corridor", box=b, floor=20, ceil=27))
for i, b in enumerate(both_z(-16, -1, -47, -38)):
    SPACES.append(dict(key=f"pumps-{i}", name="the Pump Room", box=b, floor=20, ceil=29))

# doorways in the hall's long walls (z -37 and z 36), from the corridors and pump rooms into the hall
DOORS = [(x0, x1) for x0, x1 in ((-40, -37), (-25, -21), (-11, -7))]          # along x, y 21..24

# ---- decks at 27 -------------------------------------------------------------------------------------------
DECKS = [dict(key="walk", name="the Control Walk", box=(-48, -44, -36, 35), y=27)]
for i, b in enumerate(both_z(-43, -1, -36, -31)):
    DECKS.append(dict(key=f"catwalk-{i}", name="the Catwalk", box=b, y=27))
DECKS.append(dict(key="gantry", name="the Gantry", box=(-2, -1, -30, 29), y=27))

# stair flights: (x0, x1, z0, z1, axis, direction, from_y, to_y) — the floor rises one a block along the axis
FLIGHTS = [
    # gallery up to the Control Walk, rising east
    dict(key="walk-n", box=(-55, -49, -20, -17), axis="x", step=+1, y0=21, y1=26),
    dict(key="walk-s", box=(-55, -49, 16, 19), axis="x", step=+1, y0=21, y1=26),
    # hall floor up to the catwalks, rising west, landing beside the catwalk
    dict(key="cat-n", box=(-16, -10, -30, -27), axis="x", step=-1, y0=21, y1=26),
    dict(key="cat-s", box=(-16, -10, 26, 29), axis="x", step=-1, y0=21, y1=26),
    # the spawn's two exits, down from 24 to the gallery
    dict(key="exit-n", box=(-55, -53, -9, -6), axis="x", step=-1, y0=21, y1=23),
    dict(key="exit-s", box=(-55, -53, 5, 8), axis="x", step=-1, y0=21, y1=23),
]
LANDINGS = [dict(box=(-19, -17, -30, -27), y=27), dict(box=(-19, -17, 26, 29), y=27)]

# ---- the penstocks: tunnels under the hall floor --------------------------------------------------------------
TUNNELS = [dict(key=f"penstock-{i}", z=(z0, z1)) for i, (_, _, z0, z1) in enumerate(both_z(0, 0, -28, -24))]
TUNNEL_FLOOR = 14
TUNNEL_DOWN = (-53, -48)       # stairs from the gallery floor (20) down to 14, descending east
TUNNEL_RUN = (-47, -14)
TUNNEL_UP = (-13, -8)          # stairs from 14 up to the hall floor, rising east

# ---- the middle -----------------------------------------------------------------------------------------------
DAIS = dict(name="the Exciter", box=(-4, -1, -4, 3), y=22)                  # mirrored to x -4..3
GENERATORS = [(-24.5, -18.5), (-24.5, 17.5)]
GEN_R = 4.5
SHAFTS = [dict(name="the Tailrace Shaft", box=b) for b in both_z(-12, -7, -14, -9)]

# ---- score boxes in the gallery's back wall (x -56), and what guards each --------------------------------------
BOXES = [
    dict(key="box-n", name="the North Sluice", z=(-36, -31), guard="door"),    # a cobweb curtain in the doorway
    dict(key="box-s", name="the South Sluice", z=(30, 35), guard="floor"),     # a cobweb strip on the floor before it
]
BOX_X = (-60, -57)              # the alcove, behind the gallery's back wall
BOX_FLOOR = 21

# ---- spawners and the shop --------------------------------------------------------------------------------------
DIAMOND_AT = (-0.5, 23, -0.5)        # over the Exciter dais
ARROWS_AT = [(-0.5, 21, -42.5), (-0.5, 21, 41.5)]          # in the two Pump Rooms, astride the centre line
SPAWN_POINT = (-63.5, 25, -0.5)
SHOPKEEPER = (-67.5, 25, -6.5)

PLACES = [
    ("the Gatehouse", "spawn: a room raised four over the gallery, the shop at its back, two exits down"),
    ("the Intake Gallery", "the team's back line, full width; the two score boxes in its back wall"),
    ("the Control Walk", "a deck at 27 over the gallery's front, reached by two flights, joining the catwalks"),
    ("the Turbine Hall", "the middle: open to the roof, two generators a side, the Exciter on its dais"),
    ("the Catwalks and the Gantry", "the upper level at 27 along both long walls and across the middle"),
    ("the Tailrace Shafts", "two holes a side in the hall floor, railed on two sides only, straight into the void"),
    ("the Penstocks", "two tunnels a side under the hall floor, from the gallery to the middle"),
    ("the Cable Corridors and the Pump Rooms", "the flanks, low and covered; arrows in the Pump Rooms"),
]
