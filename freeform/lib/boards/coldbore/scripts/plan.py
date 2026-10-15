"""Coldbore — the plan: two drilling stations cut into opposite cliffs on a frozen plain, split by the fissure their
shared bore tore open. Each station's reactor (the core) burns forward under its forecourt on level 1, and its
wool lies sealed in the cooling vault on level 2 directly under the reactor until the reactor leaks.

Red's half is stated (z >= the fissure's line); blue's is its half turn about (-0.5, -0.5). Heights in a space are
the feet's y; a raster cell's height is the floor block's, one under the feet.

    level 0   feet 72   the gate, the entrance hall, the armoury; the ramp down into the mountain
    level 1   feet 52   the turn hall, the return corridor, the reactor hall, the barracks and the vent bay
    level 2   feet 34   the vault under the reactor, the service corridor, the fissure gallery and the cave
    the station on the plateau, feet 104: the spawn, the monument, the stair's head and the drop
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
L0, L1, L2 = 72, 52, 34                        # feet
TOP = 104                                      # the station's yard, feet
KILL_Y = 8
BUILD_HEIGHT = 112
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
    kind: str = "corridor"                     # hall, room, corridor, vault, gallery, link

    def box(self):
        return Box(self.x0, self.feet, self.z0, self.x1, self.feet + self.h - 1, self.z1)

    def cells(self):
        return [(x, z) for x in range(self.x0, self.x1 + 1) for z in range(self.z0, self.z1 + 1)]


@dataclass(frozen=True)
class Flight:
    """A straight run of stairs along z, the feet stepping one a cell from `feet0` at z0 to `feet1` at z1."""
    name: str
    x0: int
    x1: int
    z0: int
    z1: int
    feet0: int
    feet1: int
    h: int = TUNNEL_H

    def feet_at(self, z):
        step = 1 if self.z1 > self.z0 else -1
        return self.feet0 + (self.feet1 - self.feet0) * (z - self.z0) // (self.z1 - self.z0) if self.z1 != self.z0 \
            else self.feet0

    def cells(self):
        lo, hi = sorted((self.z0, self.z1))
        return [(x, z, self.feet_at(z)) for x in range(self.x0, self.x1 + 1) for z in range(lo, hi + 1)]


# --- red's station -------------------------------------------------------------------------------------------
GATE = dict(x0=-4, x1=3, z=44, feet=L0, h=8)                    # the gate's opening in the facade's front
FACADE = dict(x0=-13, x1=12, z0=44, z1=62, y0=71, y1=88)        # the concrete front standing out of the cliff

SPACES = [
    # level 0
    Space("vestibule", -5, 4, 45, 58, L0, 9, "hall"),
    Space("entrance hall", -10, 9, 59, 72, L0, HALL_H, "hall"),
    Space("armoury", -26, -15, 61, 70, L0, 8, "room"),
    Space("armoury link", -14, -11, 64, 67, L0, TUNNEL_H),
    Space("stair link L0", 10, 21, 71, 74, L0, TUNNEL_H, "link"),
    # level 1
    Space("turn hall", -9, 8, 92, 97, L1, HALL_H, "hall"),
    Space("return corridor", 4, 7, 67, 91, L1, TUNNEL_H),
    Space("reactor hall", -12, 11, 44, 66, L1, HALL_H, "hall"),
    Space("stair link L1", 12, 15, 63, 69, L1, TUNNEL_H, "link"),
    Space("drop link", 8, 20, 71, 74, L1, TUNNEL_H, "link"),
    Space("drop room", 21, 27, 71, 77, L1, 9, "room"),
    Space("barracks", -30, -16, 50, 62, L1, 9, "room"),
    Space("barracks link", -15, -13, 54, 57, L1, TUNNEL_H),
    Space("vent bay", -17, -13, 40, 45, L1, 9, "room"),
    # level 2
    Space("vault", -10, 9, 46, 64, L2, HALL_H, "vault"),
    Space("service corridor", 12, 15, 25, 63, L2, TUNNEL_H),
    Space("vault door passage", 10, 11, 53, 56, L2, TUNNEL_H, "door"),
]
GALLERY = dict(x0=-14, x1=13, z1=25, feet=L2, h=HALL_H, open_from=5.0)   # open to the fissure where s >= open_from

FLIGHTS = [
    Flight("the ramp into the mountain", -2, 1, 73, 91, L0 - 1, L1 + 1),
    Flight("the stair to level 2", -2, 1, 43, 26, L1 - 1, L2),
    Flight("the cutting", 34, 37, 52, 84, L0, TOP),
]

# the stair core: a shaft whose stair climbs the 24 cells round a solid core, one block a cell, so every lap is 24
SHAFT = dict(x0=15, x1=23, z0=62, z1=70)
HELIX_START = L2
HELIX_TOP = TOP


def helix_ring():
    """The stair's cells in climbing order, starting beside the service corridor."""
    ring = [(x, 63) for x in range(16, 23)] + [(22, z) for z in range(64, 70)] + \
           [(x, 69) for x in range(21, 15, -1)] + [(16, z) for z in range(68, 63, -1)]
    assert len(ring) == 24
    return ring


def helix():
    """[(x, z, feet)] for every step of the stair from level 2 to the yard."""
    ring = helix_ring()
    return [(*ring[t % 24], HELIX_START + t) for t in range(HELIX_TOP - HELIX_START + 1)]


def helix_door(feet):
    """The stair's cell at a given feet height: where a level's door opens."""
    return next((x, z) for x, z, f in helix() if f == feet)


DROP = dict(x0=23, x1=25, z0=73, z1=75, water_top=L1 - 1, water_depth=3)   # the drop: the yard down into level 1
DOORS = [(15, 65, TOP), (20, 70, L0), (15, 69, L1), (15, 63, L2)]          # the stair core's doors, through its wall
LADDER = dict(x=-17, z0=41, z1=42, wall_x=-18, bottom=L1, top=land.GROUND)  # the vent bay's ladder to the forecourt
CULVERT = [(-31, L1, 56, 2.4), (-36, L1 + 4, 50, 2.6), (-40, L1 + 10, 43, 2.6), (-44, L1 + 16, 36, 2.6),
           (-46, L0 - 1, 30, 2.4)]                                            # the barracks' collapsed culvert up to the snow
YARD = dict(x0=4, x1=30, z0=62, z1=84, top=TOP - 1)                          # the station's yard on the plateau

CORE = Box(-4, 56, 52, 2, 62, 58)
WELL = Box(-5, 49, 51, 3, 51, 59)              # air under the core, its floor the hatch
HATCH = Box(-5, 48, 51, 3, 48, 59)             # bedrock, the vault's ceiling under the well: opened by the leak
LEAK = 5
LEAK_Y = CORE.y0 - LEAK                        # lava at or under this, within 15 blocks of the core, leaks it
VAULT_DOOR = Box(10, L2, 53, 11, L2 + 6, 56)   # bedrock, opened by the leak
POOL = dict(x0=-6, x1=4, z0=50, z1=60, y0=30, y1=33)   # the cooling pool under the hatch, its surface at the floor
WOOL_AT = (6, L2, 61)
MONUMENT = (9, TOP + 1, 66)                    # red's monument in its yard, the slot over a pedestal at the feet
SPAWN_AT = (13, TOP, 74)
SPAWN_AREA = Box(6, TOP, 72, 20, TOP + 5, 82)

CAVE = [  # (x, floor, z, radius): the cave off the gallery's west end, chambers and passages under the snowfield
    [(-15, 34, 18, 2.4), (-22, 33, 19, 2.8), (-30, 31, 16, 3.2), (-38, 30, 20, 3.0), (-46, 28, 17, 3.4)],
    [(-30, 31, 16, 2.6), (-33, 29, 27, 2.6), (-40, 27, 31, 2.8)],
    [(-46, 28, 17, 2.8), (-54, 27, 12, 2.6), (-58, 26, 8, 2.4)],
    [(-46, 28, 17, 2.6), (-55, 29, 24, 2.8), (-61, 31, 30, 2.4)],
]
CHAMBERS = [(-38, 30, 20, 7, 9, 6), (-47, 27, 30, 6, 8, 5), (-56, 26, 10, 5, 7, 5)]   # (x, floor, z, rx, h, rz)
LAVA_PONDS = [(-40, 30, 22, 3.5), (-46, 27, 31, 3.0), (-57, 26, 11, 2.6), (-24, 33, 20, 1.8)]  # (x, top, z, r)
CAVE_WINDOWS = [(-46, 28, 14), (-58, 26, 7)]   # where a passage breaks out onto the fissure's wall

ROADS = [  # red's roads on the snowfield: the gate to the bridgehead, and the two flanks
    [(0, 34), (2, 26), (-2, 18), (-1, 13)],
    [(-14, 36), (-26, 33), (-38, 26), (-47, 20), (-52, 14)],
    [(14, 36), (26, 31), (36, 26), (44, 20), (50, 14)],
    [(-38, 26), (-44, 29), (-46, 30)],
]
BRIDGE_STUB = dict(x0=-3, x1=1, length=6)      # the old road bridge, broken off over the fissure


def spaces():
    return SPACES


def objectives():
    """The teams, their spawns, cores, wools and the observer: drawn once for red and turned for blue."""
    O = Objectives(Teams(("red-team", "Red", "red", 20), ("blue-team", "Blue", "blue", 20)), SYM)
    O.add(Observer((0, 112, -1), yaw=90), mirror=False)
    O.add(Spawn("red-team", SPAWN_AT, yaw=180, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Core("red-core", "Reactor", "red-team", CORE, leak=LEAK))
    blue_slot = (*SYM.point(MONUMENT[0], MONUMENT[2]),)
    vault = next(s for s in SPACES if s.name == "vault").box()
    O.add(Wool("blue-team", "orange", (blue_slot[0], MONUMENT[1], blue_slot[1]), WOOL_AT, vault, delay="3s"),
          color="cyan")
    return O


# --- the plan raster -----------------------------------------------------------------------------------------
KINDS = ["rock", "snow", "floor", "stair", "water", "lava"]
WALK = {"snow", "floor", "stair", "water"}
BANDS = (44, 68, 92)                           # floor blocks up to 44 on storey 0, to 68 on 1, to 92 on 2, above on 3


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


def floors(opened=False):
    """Every walked floor of red's half: (x, z, floor block y, kind); `opened` once the leak has opened the
    vault's door."""
    out = []
    for s in SPACES:
        if s.kind == "door" and not opened:
            continue
        for x, z in s.cells():
            pool = POOL["x0"] <= x <= POOL["x1"] and POOL["z0"] <= z <= POOL["z1"] and s.kind == "vault"
            out.append((x, z, s.feet - 1, "water" if pool else "floor"))
    for x, z in gallery_cells():
        out.append((x, z, L2 - 1, "floor"))
    for f in FLIGHTS:
        out += [(x, z, feet - 1, "stair") for x, z, feet in f.cells()]
    out += [(x, z, feet - 1, "stair") for x, z, feet in helix()]
    out += [(x, z, YARD["top"], "floor") for x in range(YARD["x0"], YARD["x1"] + 1)
            for z in range(YARD["z0"], YARD["z1"] + 1)
            if not (SHAFT["x0"] <= x <= SHAFT["x1"] and SHAFT["z0"] <= z <= SHAFT["z1"])
            and not (DROP["x0"] <= x <= DROP["x1"] and DROP["z0"] <= z <= DROP["z1"])]
    out += [(x, z, YARD["top"], "floor") for x in range(30, 38) for z in range(80, 87)]
    out += culvert_cells()
    out += [(x, z, feet - 1, "floor") for x, z, feet in DOORS]
    return out


def culvert_cells():
    """The culvert's floor cells, its floor rising from the barracks to the snow along its waypoints."""
    from pgmvox.geom.shapes import polyline
    pts = [(x, z) for x, _, z, _ in CULVERT]
    xs = np.arange(-50, -28)
    zs = np.arange(26, 62)
    Xg, Zg = np.meshgrid(xs, zs, indexing="ij")
    d, al = polyline(Xg.astype(float), Zg.astype(float), pts)[:2]
    arc = np.concatenate([[0], np.cumsum(np.hypot(np.diff([p[0] for p in pts]), np.diff([p[1] for p in pts])))])
    feet = np.interp(al, arc, [p[1] for p in CULVERT])
    return [(int(x), int(z), int(round(f)) - 1, "floor") for x, z, f, dd in zip(Xg.ravel(), Zg.ravel(), feet.ravel(),
                                                                             d.ravel()) if dd < 1.6]


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
    # the shaft and the drop are open to the sky, so the plateau over them is not a floor
    for x in range(SHAFT["x0"], SHAFT["x1"] + 1):
        for z in range(SHAFT["z0"], SHAFT["z1"] + 1):
            for x2, z2 in ((x, z), SYM.point(x, z)):
                i, k = x2 - land.X0, z2 - land.Z0
                stories[3].K[i, k] = stories[3].kinds["none"]
    for x, z, h, kind in floors(opened):
        for x2, z2 in ((x, z), SYM.point(x, z)):
            S = stories[band(h)]
            S.H[x2 - land.X0, z2 - land.Z0] = h
            S.K[x2 - land.X0, z2 - land.Z0] = S.kinds[kind]
    return R


def node(x, z, h):
    return (x, z) if band(h) == 0 else (x, z, band(h))


def links():
    """What the raster cannot say: a bridge built over the fissure at the surface and between the two galleries,
    the drop from the yard, and the vent bay's ladder. [(a, b, cost, tag)], both halves."""
    H, X, Z = land.heights()
    top = np.round(H).astype(int)
    c, half = land.fissure_line()
    out = []
    for x in range(land.X0, land.X1 + 1):
        i = x - land.X0
        zr = int(np.ceil(c[i] + half[i]))                    # red's rim, and blue's at the same x across
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
    drop_top = node(DROP["x0"] + 1, DROP["z0"] - 1, TOP - 1)
    drop_foot = node(DROP["x0"] - 1, DROP["z0"] + 1, L1 - 1)
    ladder_foot = node(LADDER["x"], LADDER["z0"], L1 - 1)
    ladder_top = node(LADDER["x"] + 2, LADDER["z0"] - 2, land.GROUND)
    for a, b, cost, tag in [(drop_top, drop_foot, 4, "drop"),
                            (ladder_foot, ladder_top, 9, "ladder"), (ladder_top, ladder_foot, 7, "ladder")]:
        out.append((a, b, cost, tag))
        ia = (*SYM.point(a[0], a[1]),) + a[2:]
        ib = (*SYM.point(b[0], b[1]),) + b[2:]
        out.append((ia, ib, cost, tag))
    return out
