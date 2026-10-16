"""Crucible — the plan: two foundries dug into facing volcanoes across a lava rift. Each foundry hangs its crucible
(the core) from a gantry crane over a casting pit sunk into the slag plain in front of the mountain, and keeps its
dye stock (the wool) in the cold store, the one cool room, at the foundry's deepest level under the mountain's back.

Red's half is stated (z >= 0); blue's is its half turn about (-0.5, -0.5). Heights of a space are the feet's y; a
plan cell's height is the floor block's, one under the feet.

    level 0   feet 52   the loading gate and hall, the crew hall (spawn), the pour room and its loggia over the pit
    level 1   feet 40   the casting pit's floor and apron, the furnace hall behind it, the slag run under the hall
    level 2   feet 28   the cold store (the wool) and its passage, the end of the flank cave
Every change of level inside is a ramp of two legs, one in two, turning on a level landing between them.
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
L0, L1, L2 = 52, 40, 28                        # feet
KILL_Y = 18
BUILD_HEIGHT = 100
TUNNEL_H = 5


@dataclass(frozen=True)
class Space:
    """A room or a corridor: an air box from the feet up `h` blocks, its floor one under the feet. `style` names
    how its walls, floor and ceiling are lined."""
    name: str
    x0: int
    x1: int
    z0: int
    z1: int
    feet: int
    h: int
    style: str = "tunnel"

    def box(self):
        return Box(self.x0, self.feet, self.z0, self.x1, self.feet + self.h - 1, self.z1)

    def cells(self):
        return [(x, z) for x in range(self.x0, self.x1 + 1) for z in range(self.z0, self.z1 + 1)]


@dataclass(frozen=True)
class Leg:
    """One straight leg of a ramp: a band x0..x1 by z0..z1, the feet falling evenly from `feet0` at its start to
    `feet1` at its end along `axis`, starting at the end named by `start` ("lo" or "hi")."""
    x0: int
    x1: int
    z0: int
    z1: int
    axis: str
    start: str
    feet0: float
    feet1: float

    def cells(self):
        """(x, z, feet) with the feet in half blocks."""
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
    """A way between two levels: legs walked in order, each about one in two, and the landings between them."""
    name: str
    legs: tuple
    h: int = TUNNEL_H

    def cells(self):
        return [c for leg in self.legs for c in leg.cells()]


# --- red's foundry -------------------------------------------------------------------------------------------
SPACES = [
    # level 0
    Space("loading gate", -33, -28, 58, 61, L0, 7, "gate"),
    Space("loading hall", -42, -20, 62, 78, L0, 12, "hall"),
    Space("west corridor", -19, -9, 74, 77, L0, TUNNEL_H),
    Space("crew hall", -8, 8, 72, 88, L0, 8, "crew"),
    Space("east corridor", 9, 15, 74, 77, L0, TUNNEL_H),
    Space("pour link", 12, 15, 70, 73, L0, TUNNEL_H),
    Space("pour room", 10, 32, 62, 69, L0, 7, "pour"),
    Space("loggia", 14, 30, 58, 61, L0, 6, "loggia"),
    Space("ramp door", -43, -43, 63, 66, L0, TUNNEL_H, "door"),
    # level 1
    Space("furnace hall", 4, 27, 62, 73, L1, 8, "furnace"),
    Space("west pit door", 15, 17, 58, 61, L1, 4, "door"),
    Space("east pit door", 23, 25, 58, 61, L1, 4, "door"),
    Space("slag run", -48, 3, 63, 66, L1, TUNNEL_H, "run"),
    # level 2
    Space("store passage", -38, -33, 79, 82, L2, TUNNEL_H),
    Space("cold store", -46, -32, 84, 95, L2, 9, "store"),
    Space("store door", -37, -35, 83, 83, L2, 4, "door"),
    Space("store west door", -48, -47, 88, 90, L2, 4, "door"),
]
RAMPS = [
    Ramp("the loading ramp", (Leg(-47, -44, 63, 74, "z", "lo", L0, 46.5), Leg(-52, -44, 75, 78, "z", "lo", 46, 46),
                              Leg(-52, -49, 63, 74, "z", "hi", 46, L1 + 0.5))),
    Ramp("the furnace ramp", (Leg(16, 27, 74, 77, "x", "lo", L0, 46.5), Leg(28, 31, 74, 77, "x", "lo", 46, 46),
                              Leg(28, 31, 62, 73, "z", "hi", 46, L1 + 0.5))),
    Ramp("the deep ramp", (Leg(-16, -13, 67, 78, "z", "lo", L1, 34.5), Leg(-20, -13, 79, 82, "z", "lo", 34, 34),
                           Leg(-32, -21, 79, 82, "x", "hi", 34, L2 + 0.5))),
]
RAMP_WALLS = [(-48, 63, 74)]                   # the wall between the loading ramp's two legs: x, z0..z1

# the casting pit: an ellipse sunk into the plain at the mountain's foot, its floor at level 1
PIT = dict(x=22, z=45, rx=17, rz=13, floor=L1 - 1, bench=44, floor_e=0.55, bench_e=0.8, ramp_e=0.86, ramp_top=47,
           ramp_from=260, ramp_to=100)          # the haul ramp: degrees round the pit, from its top to the floor
APRON = (15, 29, 52, 57)                         # the floor carried to the facade: x0, x1, z0, z1
CORE = Box(20, 46, 43, 24, 50, 47)               # lava 3x3x3 in obsidian, six blocks of air over the pit floor
LEAK = 5
LEAK_Y = CORE.y0 - LEAK - 1                      # PGM's leak line: lava at or under this, within 15 of the core
GANTRY = dict(z0=44, z1=46, y=55, x0=2, x1=46)   # the crane girder over the pit, chains down to the crucible
FACADE_PIT = dict(x0=8, x1=36, z0=58, z1=61, top=66)
FACADE_GATE = dict(x0=-40, x1=-21, z0=58, z1=61, top=68)

MONUMENT = (21, L0 + 1, 67)                      # red's monument on the pour room's desk
SPAWN_AT = (3, L0, 77)
SPAWN_AREA = Box(-8, L0, 72, 8, L0 + 7, 88)
WOOL_AT = (-39, L2 + 1, 90)                      # on the cold store's plinth
STORE = next(s for s in SPACES if s.name == "cold store")

# the lava tube from the sinkhole on the plain to the pit's floor (below), and the flank cave from the west spur to
# the cold store (around): (x, feet, z, radius)
TUBE = [(-5, 42, 31, 2.6), (2, 41, 33, 2.4), (9, 40, 36, 2.4), (14, 40, 39, 2.3)]
FLANK = [(-61, 51, 46, 2.4), (-63, 47, 56, 2.6), (-62, 43, 66, 2.6), (-60, 39, 75, 2.5), (-57, 34, 84, 2.6),
         (-52, 30, 89, 2.4), (-50, 28, 89, 2.0)]
CAVE_CHAMBERS = [(-62, 43, 66, 5, 7, 4)]         # (x, feet, z, rx, h, rz): a chamber halfway down the flank cave

RAILS = [(-30, 57), (-27, 46), (-21, 34), (-16, 22), (-13, 14), (-12, 9)]   # the slag line, gate to the tip
TIP = dict(x0=-15, x1=-10, z0=5, z1=10)          # the tipping trestle over the rift


def objectives():
    """The teams, their spawns, cores, wools and the observer: drawn once for red and turned for blue."""
    O = Objectives(Teams(("red-team", "Red", "red", 24), ("blue-team", "Blue", "blue", 24)), SYM)
    O.add(Observer((0, 92, -1), yaw=90), mirror=False)
    O.add(Spawn("red-team", SPAWN_AT, yaw=180, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Core("red-core", "Crucible", "red-team", CORE, leak=LEAK))
    blue_slot = SYM.point(MONUMENT[0], MONUMENT[2])
    O.add(Wool("blue-team", "lime", (blue_slot[0], MONUMENT[1], blue_slot[1]), WOOL_AT, STORE.box(), delay="3s"),
          color="yellow")
    return O


# --- the plan raster -----------------------------------------------------------------------------------------
KINDS = ["ground", "steep", "floor", "stair", "lava", "void"]
WALK = {"ground", "steep", "floor", "stair"}


def ramp_floor(feet):
    return int(np.ceil(feet)) - 1


def floors():
    """Every walked floor inside red's foundry and caves: (x, z, floor block y, kind)."""
    out = []
    for s in SPACES:
        out += [(x, z, s.feet - 1, "floor") for x, z in s.cells()]
    for r in RAMPS:
        out += [(x, z, ramp_floor(f), "stair") for x, z, f in r.cells()]
    g = GANTRY
    out += [(x, z, g["y"], "floor") for x in range(g["x0"], g["x1"] + 1) for z in range(g["z0"], g["z1"] + 1)]
    for path in (TUBE, FLANK):
        for (xa, fa, za, _), (xb, fb, zb, _) in zip(path, path[1:]):
            n = int(max(abs(xb - xa), abs(zb - za))) * 2
            for k in range(n + 1):
                t = k / n
                x, z, f = round(xa + (xb - xa) * t), round(za + (zb - za) * t), fa + (fb - fa) * t
                for dx in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        out.append((x + dx, z + dz, int(round(f)) - 1, "floor"))
    return out


def raster():
    """The board as a plan: the surface from land's heights, and under it every foundry and cave floor, each column's
    floors put on storeys in the order of their heights, both halves. A floor within two of a higher one in its
    column is the ceiling's business, not a floor: the higher is kept."""
    from pgmvox.surface.terrain import slope_deg
    H = np.round(land.heights()).astype(int)
    steep = slope_deg(H) > 50
    inside = land.inside()
    cols = {}
    for i in range(land.NX):
        for k in range(land.NZ):
            if not inside[i, k]:
                continue
            h = int(H[i, k])
            cols[(i, k)] = {h: "lava" if h <= land.LAVA else "steep" if steep[i, k] else "ground"}
    for x, z, h, kind in floors():
        for x2, z2 in ((x, z), SYM.point(x, z)):
            key = (int(x2) - land.X0, int(z2) - land.Z0)
            if key in cols:
                c = cols[key]
                for other in [o for o in c if abs(o - h) <= 2 and o != h and c[o] in ("ground", "steep")]:
                    if other < h:
                        del c[other]                       # the surface the foundry's floor replaces (the pit's apron)
                c[h] = kind
    R = Raster((land.X0, land.X1), (land.Z0, land.Z1), KINDS, 0, "void", SYM)
    stories = [R]
    for (i, k), c in cols.items():
        for n, h in enumerate(sorted(c)):
            while len(stories) <= n:
                stories.append(R.storey(len(stories)))
            S = stories[n]
            S.H[i, k] = h
            S.K[i, k] = S.kinds[c[h]]
    return R


def node(R, x, z, h):
    """The plan node of the floor at block height h in column (x, z)."""
    for n, S in enumerate(R.storeys):
        i, k = x - land.X0, z - land.Z0
        if S.has()[i, k] and S.H[i, k] == h:
            return (x, z) if n == 0 else (x, z, n)
    return None
