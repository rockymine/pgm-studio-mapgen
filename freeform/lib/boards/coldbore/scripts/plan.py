"""Coldbore — the plan: two drilling stations cut into opposite cliffs on a frozen plain, split by the fissure their
shared bore tore open. Each station's reactor (the core) burns in a tall hall inside the mountain, and its wool
lies in a cooling vault deep in the mountain's other side, sealed until the reactor leaks.

Red's half is stated (z >= the fissure's line); blue's is its half turn about (-0.5, -0.5). Heights in a space are
the feet's y; a raster cell's height is the floor block's, one under the feet.

    level 0   feet 72   the gate in the west buttress, the entrance hall, the armoury, the spawn and iron rooms,
                        the generator house in the east buttress, the reactor hall's balcony and gantry
    level 1   feet 58   the reactor hall's floor, the south corridor, the collapsed store under the snowfield
    level 2   feet 44   the fissure gallery and the cave west of it, the service corridor, the vault
Every change of level is a ramp of two legs, about one in two, turning on a level landing between them.
"""
import os
import sys
from dataclasses import dataclass

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.plan.raster import Raster, Symmetry  # noqa: E402
from pgmvox.play.objectives import Box, Core, Objectives, Observer, Spawn, Teams, Wool  # noqa: E402

import land  # noqa: E402

SYM = Symmetry("half")
L0, L1, L2 = 72, 58, 44                        # feet
TOP = 104                                      # the plateau's yard, feet
KILL_Y = 8
BUILD_HEIGHT = 116
TUNNEL_H, HALL_H = 7, 14


@dataclass(frozen=True)
class Space:
    """A room or a corridor: an air box from the feet up `h` blocks, its floor one under the feet."""
    name: str
    x0: int
    x1: int
    z0: int
    z1: int
    feet: int
    h: int
    kind: str = "corridor"                     # hall, room, corridor, vault, link, door

    def box(self):
        return Box(self.x0, self.feet, self.z0, self.x1, self.feet + self.h - 1, self.z1)

    def cells(self):
        return [(x, z) for x in range(self.x0, self.x1 + 1) for z in range(self.z0, self.z1 + 1)]


@dataclass(frozen=True)
class Leg:
    """One straight leg of a ramp: a band `x0..x1` by `z0..z1`, the feet falling evenly from `feet0` at its start
    to `feet1` at its end along `axis` ("x" or "z"), starting at the end named by `start` ("lo" or "hi")."""
    x0: int
    x1: int
    z0: int
    z1: int
    axis: str
    start: str
    feet0: float
    feet1: float

    def cells(self):
        """(x, z, feet) with feet in half blocks."""
        lo, hi = (self.x0, self.x1) if self.axis == "x" else (self.z0, self.z1)
        n = hi - lo
        out = []
        for x in range(self.x0, self.x1 + 1):
            for z in range(self.z0, self.z1 + 1):
                a = x if self.axis == "x" else z
                t = (a - lo) / n if self.start == "lo" else (hi - a) / n
                out.append((x, z, round(2 * (self.feet0 + (self.feet1 - self.feet0) * t)) / 2))
        return out


@dataclass(frozen=True)
class Ramp:
    """A way between two levels: legs walked in order, each a gentle slope, the second turning off the first.
    `solid` ramps stand as a wedge against a hall's walls; the others are tunnels cut through the rock."""
    name: str
    legs: tuple
    h: int = TUNNEL_H
    solid: bool = False

    def cells(self):
        return [c for leg in self.legs for c in leg.cells()]


@dataclass(frozen=True)
class Deck:
    """A floor built inside a tall hall: a balcony or a gantry, its top block at the feet less one."""
    name: str
    x0: int
    x1: int
    z0: int
    z1: int
    feet: int

    def cells(self):
        return [(x, z) for x in range(self.x0, self.x1 + 1) for z in range(self.z0, self.z1 + 1)]


# --- red's station -------------------------------------------------------------------------------------------
GATE = dict(x0=-43, x1=-38, z=48, feet=L0, h=8)                 # the gate in the west buttress's facade
FACADE = dict(x0=-50, x1=-31, z0=48, z1=60, y0=71, y1=88)       # the west facade, the buttress's face
ANNEX = dict(x0=24, x1=44, z0=50, z1=60, y0=71, y1=84)          # the generator house in the east buttress
GARAGE = dict(x0=31, x1=36, z=50, feet=L0, h=6)                 # its door onto the yard
HALL = dict(x0=-12, x1=12, z0=62, z1=84, feet=L1, h=22)         # the reactor hall, floor to above the balcony

SPACES = [
    # level 0
    Space("gate vestibule", -44, -37, 49, 58, L0, 9, "hall"),
    Space("entrance hall", -48, -30, 59, 84, L0, HALL_H, "hall"),
    Space("armoury", -62, -51, 64, 74, L0, 8, "room"),
    Space("armoury door", -50, -49, 68, 71, L0, TUNNEL_H, "link"),
    Space("west corridor", -29, -13, 80, 83, L0, TUNNEL_H),
    Space("spawn room", 14, 30, 76, 92, L0, 9, "room"),
    Space("iron room", 31, 37, 78, 90, L0, 7, "room"),
    Space("spawn door", 13, 13, 80, 83, L0, TUNNEL_H, "link"),
    Space("generator house", 25, 43, 51, 60, L0, 9, "hall"),
    Space("annex corridor", 13, 29, 70, 73, L0, TUNNEL_H),
    Space("annex link", 26, 29, 61, 69, L0, TUNNEL_H),
    Space("reactor hall", HALL["x0"], HALL["x1"], HALL["z0"], HALL["z1"], L1, HALL["h"], "hall"),
    # level 1
    Space("south door", 9, 12, 61, 61, L1, TUNNEL_H, "link"),
    Space("south corridor", 9, 12, 40, 60, L1, TUNNEL_H),
    Space("store passage", 13, 21, 40, 43, L1, TUNNEL_H),
    Space("collapsed store", 22, 34, 34, 46, L1, 9, "room"),
    # level 2
    Space("service corridor", 14, 17, 30, 79, L2, TUNNEL_H),
    Space("vault passage", 18, 24, 76, 79, L2, TUNNEL_H),
    Space("vault door passage", 25, 25, 76, 79, L2, TUNNEL_H, "door"),
    Space("vault", 26, 44, 70, 88, L2, HALL_H, "vault"),
    Space("gallery door", -14, -13, 22, 25, L2, TUNNEL_H, "link"),
]
GALLERY = dict(x0=-12, x1=13, z1=34, feet=L2, h=HALL_H, open_from=9.5)   # open where the distance across passes

DECKS = [
    Deck("balcony", -12, 12, 80, 84, L0),
    Deck("gantry", 9, 12, 70, 79, L0),
]
RAMPS = [
    Ramp("the hall's ramp", (Leg(-12, -9, 66, 79, "z", "hi", L0, 65.5), Leg(-12, -9, 62, 65, "z", "hi", 65, 65),
                             Leg(-8, 8, 62, 65, "x", "lo", 64.5, L1 + 0.5)), h=8, solid=True),
    Ramp("the ramp to the gallery", (Leg(-14, 8, 37, 40, "x", "hi", L1, 51.5), Leg(-18, -15, 37, 40, "z", "hi", 51.5, 51.5),
                                     Leg(-18, -15, 22, 36, "z", "hi", 51, L2))),
]
CORE = Box(-4, 62, 69, 2, 68, 75)
PIT = Box(-5, 50, 68, 3, 57, 76)               # the sump under the core: air from its floor up to the hall's floor
LEAK = 5
LEAK_Y = CORE.y0 - LEAK                        # lava at or under this, within 15 blocks of the core, leaks it
VAULT_DOOR = Box(25, L2, 76, 25, L2 + 6, 79)   # bedrock, opened by the leak
ROOF_HOLE = dict(x0=26, x1=30, z0=37, z1=41)   # where the store's ceiling fell in, open to the snowfield
WOOL_AT = (40, L2, 84)
MONUMENT = (5, L0 + 1, 83)                     # red's monument on the balcony by the spawn door
SPAWN_AT = (24, L0, 86)
SPAWN_AREA = Box(14, L0, 76, 37, L0 + 8, 92)   # the spawn room and the iron room
IRON = [(x, y, z) for z in (78, 90) for x in range(32, 37, 2) for y in (L0, L0 + 1)] + \
       [(37, y, z) for z in range(79, 90, 2) for y in (L0, L0 + 1)]                     # iron in the walls, mined and grown back

CAVE = [  # (x, floor, z, radius): the cave off the gallery's ramp, chambers and passages under the snowfield
    [(-19, 44, 24, 2.4), (-26, 43, 21, 2.8), (-33, 41, 18, 3.2), (-40, 40, 22, 3.0), (-48, 38, 19, 3.4)],
    [(-33, 41, 18, 2.6), (-36, 39, 28, 2.6), (-42, 37, 32, 2.8)],
    [(-48, 38, 19, 2.8), (-56, 37, 14, 2.6), (-60, 36, 10, 2.4)],
    [(-48, 38, 19, 2.6), (-56, 39, 26, 2.8), (-62, 41, 31, 2.4)],
]
CHAMBERS = [(-40, 40, 22, 7, 9, 6), (-48, 37, 31, 6, 8, 5), (-58, 36, 12, 5, 7, 5)]   # (x, floor, z, rx, h, rz)
LAVA_PONDS = [(-42, 40, 24, 3.5), (-47, 37, 32, 3.0), (-59, 36, 13, 2.6), (-27, 43, 22, 1.8)]  # (x, top, z, r)
CAVE_WINDOWS = [(-48, 38, 16), (-60, 36, 9)]   # where a passage breaks out onto the fissure's wall

ROADS = [  # red's roads on the snowfield: from the gate and the generator house to the bridgehead and the flanks
    [(-40, 40), (-34, 30), (-20, 22), (-6, 17), (-1, 13)],
    [(-40, 40), (-50, 30), (-58, 22), (-62, 15)],
    [(33, 44), (24, 34), (10, 24), (2, 16), (-1, 13)],
    [(33, 44), (40, 34), (44, 24)],
]
GATE_COURT = dict(x0=-56, x1=-25, z0=38, z1=47)                # paved in front of the gate
ANNEX_YARD = dict(x0=22, x1=46, z0=42, z1=49)                  # paved in front of the generator house
BRIDGE_STUB = dict(x0=-3, x1=1, length=6)
YARD = dict(x0=-10, x1=24, z0=64, z1=90, top=TOP - 1)          # the plateau's yard: the dish and the buildings
DISH = dict(x=5, z=78, r=10, y=TOP + 7, tilt=35)
CUTTING = dict(x0=50, x1=53, z0=50, z1=74, feet0=81, feet1=TOP)    # stairs from the hill up to the plateau


def spaces():
    return SPACES


def objectives():
    """The teams, their spawns, cores, wools and the observer: drawn once for red and turned for blue."""
    O = Objectives(Teams(("red-team", "Red", "red", 20), ("blue-team", "Blue", "blue", 20)), SYM)
    O.add(Observer((0, 116, -1), yaw=90), mirror=False)
    O.add(Spawn("red-team", SPAWN_AT, yaw=90, kit="spawn-kit", area=SPAWN_AREA, protect=("iron block",)))
    O.add(Core("red-core", "Reactor", "red-team", CORE, leak=LEAK))
    blue_slot = SYM.point(MONUMENT[0], MONUMENT[2])
    vault = next(s for s in SPACES if s.name == "vault").box()
    O.add(Wool("blue-team", "orange", (blue_slot[0], MONUMENT[1], blue_slot[1]), WOOL_AT, vault, delay="3s"),
          color="cyan")
    return O


# --- the plan raster -----------------------------------------------------------------------------------------
KINDS = ["rock", "snow", "floor", "stair", "water", "lava"]
WALK = {"snow", "floor", "stair", "water"}
BANDS = (50, 64, 92)                           # floor blocks up to 50 on storey 0, to 64 on 1, to 92 on 2, above on 3


def band(h):
    return sum(h > b for b in BANDS)


def gallery_cells():
    """The gallery's floor cells: its box, open to the fissure where the distance across passes open_from."""
    g = GALLERY
    c, _ = land.fissure_line()
    out = []
    for x in range(g["x0"], g["x1"] + 1):
        z0 = int(np.ceil(c[x - land.X0] + g["open_from"]))
        out += [(x, z) for z in range(z0, g["z1"] + 1)]
    return out


def ramp_floor(feet):
    """A ramp cell's floor block: the block under the feet, a half step standing on the block under that."""
    return int(np.ceil(feet)) - 1


def floors(opened=False):
    """Every walked floor of red's half: (x, z, floor block y, kind); `opened` once the leak has opened the
    vault's door."""
    out = []
    hall = next(s for s in SPACES if s.name == "reactor hall")
    covered = {(x, z) for r in RAMPS if r.solid for x, z, _ in r.cells()}
    pit = {(x, z) for x in range(PIT.x0, PIT.x1 + 1) for z in range(PIT.z0, PIT.z1 + 1)}
    for s in SPACES:
        if s.kind == "door" and not opened:
            continue
        for x, z in s.cells():
            if s is hall and ((x, z) in covered or (x, z) in pit):
                continue
            out.append((x, z, s.feet - 1, "floor"))
    for x, z in gallery_cells():
        out.append((x, z, L2 - 1, "floor"))
    for d in DECKS:
        out += [(x, z, d.feet - 1, "floor") for x, z in d.cells()]
    for r in RAMPS:
        out += [(x, z, ramp_floor(f), "stair") for x, z, f in r.cells()]
    out += [(x, z, PIT.y0 - 1, "floor") for x, z in pit]
    return out


def raster(opened=False):
    """The board as a plan: the surface from land's heights on the storey its height falls in, every bunker floor
    on its own, both halves; `opened` after the leak."""
    H, X, Z = land.heights()
    R = Raster((land.X0, land.X1), (land.Z0, land.Z1), KINDS, 0, "rock", SYM)
    stories = [R] + [R.storey(n) for n in (1, 2, 3)]
    top = np.round(H).astype(int)
    lava = top <= land.LAVA
    for i in range(land.NX):
        for k in range(land.NZ):
            h = int(top[i, k])
            S = stories[band(h)]
            S.H[i, k] = h
            S.K[i, k] = S.kinds["lava" if lava[i, k] else "snow"]
    hole = [(x, z) for x in range(ROOF_HOLE["x0"], ROOF_HOLE["x1"] + 1) for z in range(ROOF_HOLE["z0"], ROOF_HOLE["z1"] + 1)]
    for x, z in hole:                                          # the fallen ceiling: the snow there is gone
        for x2, z2 in ((x, z), SYM.point(x, z)):
            i, k = x2 - land.X0, z2 - land.Z0
            S = stories[band(int(top[i, k]))]
            S.K[i, k] = S.kinds["none"] if S is not R else S.kinds["rock"]
    for x, z, h, kind in floors(opened):
        for x2, z2 in ((x, z), SYM.point(x, z)):
            S = stories[band(h)]
            S.H[x2 - land.X0, z2 - land.Z0] = h
            S.K[x2 - land.X0, z2 - land.Z0] = S.kinds[kind]
    return R


def node(x, z, h):
    return (int(x), int(z)) if band(h) == 0 else (int(x), int(z), band(h))


def links():
    """What the raster cannot say: a bridge built over the fissure at the surface and between the two galleries,
    and the climb down the rubble under the store's fallen ceiling. [(a, b, cost, tag)], both halves."""
    H, X, Z = land.heights()
    top = np.round(H).astype(int)
    c, half = land.fissure_line()
    out = []
    for x in range(land.X0, land.X1 + 1):
        i = x - land.X0
        zr = int(np.ceil(c[i] + half[i]))
        zb = int(np.floor(c[i] - half[i]))
        if land.Z0 <= zb < zr <= land.Z1:
            a, b = node(x, zr, top[i, zr - land.Z0]), node(x, zb, top[i, zb - land.Z0])
            out += [(a, b, zr - zb, "bridge"), (b, a, zr - zb, "bridge")]
    reds = {}
    for x, z in gallery_cells():
        reds[x] = min(z, reds.get(x, z))
    for x, zr in reds.items():
        xb, _ = SYM.point(x, zr)
        zb = SYM.point(xb, reds[xb])[1] if xb in reds else None
        if zb is not None:
            a, b = node(x, zr, L2 - 1), node(x, zb, L2 - 1)
            out += [(a, b, zr - zb, "deep bridge"), (b, a, zr - zb, "deep bridge")]
    rh = ROOF_HOLE
    edge = (rh["x0"] - 1, rh["z0"] + 2)
    surface = node(*edge, top[edge[0] - land.X0, edge[1] - land.Z0])
    rubble = node(rh["x0"] + 2, rh["z0"] + 2, L1 - 1)
    for a, b, cost in [(surface, rubble, 10), (rubble, surface, 14)]:
        out.append((a, b, cost, "rubble"))
        out.append(((*SYM.point(a[0], a[1]),) + a[2:], (*SYM.point(b[0], b[1]),) + b[2:], cost, "rubble"))
    return out
