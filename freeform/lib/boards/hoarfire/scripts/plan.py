"""Hoarfire: a destroy-the-core and destroy-the-monument board for two teams of twenty, played across the first
night of winter. Each team holds one half of a valley: its west under the Rimewall glacier's snow, its east still in
autumn. A team defends an Ember Core (lava in obsidian) in the autumn woods and a Rime Monument (packed ice) on the
snow, and wins by leaking the enemy's core and breaking the enemy's monument. The halves face each other across the
Rift, a void crossed by building. Rowan (red) holds the north (z < 0); Sloe (blue) is its mirror image, z -> -1 - z.

    the Hearth Lodge   the spawn: a timber lodge on the Hearth Ridge over the spring the Thaw rises from
    the Rimewall       the glacier in the north-west corner; its tongue ends in a snout cliff over the Rime Shelf
    the Rime Shelf     level snow, the old tarn bed: the Rime Monument floats over it, ringed by four seracs
    the Rime Tarn      frozen; the Ice Cave runs from its bank under the snow to a ledge on the Rift's cliff
    the Frostwood      snowy spruce on the Frost Knoll, between the monument and the Rift
    the Thaw           the stream down the middle of the half, in a dell; the Thaw Bridge, the ford, the falls
    Emberstead         a barn and a farmhouse east of the lodge, the harvest field below them
    the Ember Pit      the core floats over it in a clearing of charcoal kilns
    Kiln Hill          a hill on the east edge, its terrace a bridge's length from the core and above it
    the Russet Wood    autumn oaks between the core and the Rift
    the Hollow Way     a sunken lane from the Rift's shore into the Ember Pit
    the Rift           the void between the halves, a build zone from edge to edge; the Berg and the Cinder in it

Heights: H is the y of the floor block; a player stands at H + 1.
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

import land  # noqa: E402
from pgmvox.core.blocks import B  # noqa: E402
from pgmvox.geom import shapes  # noqa: E402
from dataclasses import dataclass  # noqa: E402

from pgmvox.play.objectives import (Box, Core, Destroyable, Objectives, Observer, Spawn, Teams,  # noqa: E402
                                    float_problems, ground_problems)
from pgmvox.plan.raster import Raster  # noqa: E402
from pgmvox.surface import terrain as T  # noqa: E402

BOARD = "hoarfire"
X_MIN, X_MAX = land.X0, land.X0 + land.NX - 1
Z_MIN, Z_MAX = land.Z0, land.Z0 + land.NZ - 1
SYM = land.SYM
KILL_Y = 30
MAX_BUILD = 92
PLAYERS = 20
BUILD_ZONE = (X_MIN, -16, X_MAX, 15)        # the Rift's build zone, x0, z0, x1, z1 inclusive: void inside it is built over

G = land.ground()
X, Z, H, LAND = G["X"], G["Z"], G["H"], G["land"]
WET = np.zeros(H.shape, bool)
for _w in G["waters"]:
    WET |= _w.mask


def g(x, z):
    return int(H[x - X_MIN, z - Z_MIN])


# ---- the objectives ---------------------------------------------------------------------------------------------
MONUMENT_BOX = Box(-37, land.SHELF + 4, -52, -35, land.SHELF + 8, -50)          # a crystal of packed ice in a 3x5x3 box
CORE_BOX = Box(36, 54, -52, 39, 57, -49)                                         # 4x4x4 obsidian round 2x2x2 lava
SPAWN_AT = (0, land.LODGE_FLOOR + 1, -89)
SPAWN_SPREAD = Box(-6, land.LODGE_FLOOR + 1, -91, 6, land.LODGE_FLOOR + 1, -88)
SPAWN_AREA = Box(-11, land.COURT_Y - 6, -96, 11, land.COURT_Y + 24, -82)
OBSERVER_AT = (0, 88, 0)
SERACS = [(-44, -56, 7), (-28, -57, 6), (-44, -44, 5), (-27, -44, 6), (-36, -60, 5)]   # the Rime Shelf's standing stones: x, z, height

# ---- the buildings: (key, x0, z0, x1, z1, floor, door side, name) ---------------------------------------------------
BUILDINGS = [
    ("lodge", -10, -94, 10, -86, land.LODGE_FLOOR, "s", "the Hearth Lodge"),
    ("barn", 22, -85, 32, -78, land.HAMLET_Y, "s", "Emberstead Barn"),
    ("farmhouse", 39, -84, 46, -78, land.HAMLET_Y, "s", "Emberstead Farm"),
    ("hut", -64, -42, -60, -38, None, "e", "the Ice Hut"),
]
KILNS = [(30, -58), (46, -60), (27, -45), (47, -44)]              # charcoal kilns round the Ember Pit (domes, r 2)
CAVE = [(-59, -32, 47), (-58, -27, 45), (-55, -21, 43), (-52, -16, 41), (-50, -12, 41)]   # the Ice Cave's floor: x, z, y
BRIDGE = (-3, -51, 4, -46)                                        # the Thaw Bridge's deck, x0, z0, x1, z1
FORD = (-4, -33, 4, -31)

PATHS = {
    "Rime Path": [(-10, -80), (-18, -74), (-26, -66), (-31, -58), (-33, -55)],
    "Ember Lane": [(10, -80), (18, -76), (26, -74), (34, -72), (38, -64), (37, -57)],
    "Thaw Path": [(5, -74), (6, -64), (4, -54), (3, -50)],
    "Cross Road": [(-30, -47), (-20, -46), (-8, -48), (-3, -48), (5, -48), (14, -50), (24, -51), (31, -51)],
    "Frost Track": [(-34, -46), (-30, -38), (-24, -26), (-18, -16)],
    "Ford Path": [(0, -47), (2, -40), (0, -32), (-2, -24), (0, -16)],
}

PLACES = [("THE HEARTH LODGE", (0, -90)), ("the court", (0, -78)), ("RIMEWALL", (-60, -82)), ("the snout", (-46, -64)),
          ("RIME SHELF", (-36, -46)), ("Rime Tarn", (-50, -40)), ("the Ice Hut", (-62, -40)), ("Ice Cave mouth", (-50, -13)),
          ("FROSTWOOD", (-22, -28)), ("the drift", (-58, -52)), ("THE THAW", (-3, -60)), ("Thaw Bridge", (0, -48)),
          ("the ford", (0, -32)), ("the falls", (1, -10)), ("EMBERSTEAD", (34, -86)), ("harvest field", (21, -65)),
          ("EMBER PIT", (38, -46)), ("KILN HILL", (58, -58)), ("RUSSET WOOD", (46, -26)), ("Hollow Way", (26, -26)),
          ("THE RIFT", (-10, 0)), ("the Berg", (-34, 0)), ("the Cinder", (32, 0))]

KINDS = ["void", "ground", "steep", "water", "ice", "glacier", "path", "court", "wall", "floor", "door", "field", "pit", "rift",
         "cave", "bridge"]
WALK = {"ground", "steep", "ice", "glacier", "path", "court", "floor", "door", "field", "pit", "cave", "bridge"}
COLOURS = {"void": (22, 24, 36), "ground": (158, 150, 112), "steep": (128, 124, 118), "water": (70, 110, 170), "ice": (170, 210, 240),
           "glacier": (200, 225, 245), "path": (196, 178, 140), "court": (210, 200, 180), "wall": (140, 92, 70),
           "floor": (220, 196, 160), "door": (246, 236, 200), "field": (214, 160, 70), "pit": (70, 56, 50),
           "rift": (46, 50, 76), "cave": (120, 140, 170), "bridge": (160, 120, 80)}


def winter(x, z):
    """How far west of the seam a column lies (positive: winter), the seam being the Thaw's line."""
    d, _, side = shapes.polyline(np.array([[x]], float), np.array([[z]], float), land.THAW, side=True)
    return float(d[0, 0] * side[0, 0])


@lru_cache(maxsize=1)
def build():
    """The plan raster over the ground: kinds by slope, water, the glacier, then the places."""
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, base_h=0, base_kind="void", symmetry=SYM)
    R.H[:] = H
    deg = T.slope_deg(H, LAND)
    K = np.full(H.shape, R.kinds["void"], int)
    K[LAND] = R.kinds["ground"]
    K[LAND & (deg > 50)] = R.kinds["steep"]
    K[LAND & (G["ice"] > 2)] = R.kinds["glacier"]
    K[WET] = R.kinds["water"]
    K[G["tarn"].mask] = R.kinds["ice"]
    bz = (X >= BUILD_ZONE[0]) & (X <= BUILD_ZONE[2]) & (Z >= BUILD_ZONE[1]) & (Z <= BUILD_ZONE[3]) & ~LAND
    K[bz] = R.kinds["rift"]
    R.K[:] = K
    red = Z < 0

    def paint(mask, kind, h=None):
        for i, k in np.argwhere(mask & red & LAND):
            R.cell(int(X[i, k]), int(Z[i, k]), int(R.H[i, k]) if h is None else h, kind)
    for name, pts in PATHS.items():
        paint((shapes.polyline(X, Z, pts)[0] <= 1.6) & ~WET, "path")
    x0, z0, x1, z1 = land.COURT
    paint((X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1) & ~WET, "court")
    x0, z0, x1, z1 = land.FIELD
    paint((X >= x0) & (X <= x1) & (Z >= z0) & (Z <= z1), "field")
    pd = np.hypot(X - land.CORE[0] + 0.5, Z - land.CORE[1] + 0.5)
    paint(pd <= land.PIT_R, "pit")
    for key, bx0, bz0, bx1, bz1, floor, door, _ in BUILDINGS:
        if floor is None:
            floor = g((bx0 + bx1) // 2, (bz0 + bz1) // 2)
        for x in range(bx0, bx1 + 1):
            for z in range(bz0, bz1 + 1):
                edge = x in (bx0, bx1) or z in (bz0, bz1)
                R.cell(x, z, floor + (6 if edge else 0), "wall" if edge else "floor")
        for x, z in door_cells(key):
            R.cell(x, z, floor, "door")
    a, b, c, d = BRIDGE
    for x in range(a, c + 1):
        for z in range(b, d + 1):
            R.cell(x, z, max(g(a - 1, z), g(c + 1, z)), "bridge")
    return R


def door_cells(key):
    spec = next(b for b in BUILDINGS if b[0] == key)
    _, x0, z0, x1, z1, _, side, _ = spec
    mx, mz = (x0 + x1) // 2, (z0 + z1) // 2
    if key == "lodge":
        return [(x, z1) for x in range(mx - 1, mx + 2)]
    return {"s": [(mx, z1)], "n": [(mx, z0)], "e": [(x1, mz)], "w": [(x0, mz)]}[side]


def rift_mask(R=None):
    R = R or build()
    return R.mask("rift")


def cave_edges():
    """The Ice Cave as walk edges: the tarn's bank to the cliff ledge, each way, for both teams."""
    out = []
    pts = CAVE
    for (ax, az, ay), (bx, bz, by) in zip(pts, pts[1:]):
        c = float(np.hypot(bx - ax, bz - az)) + 0.2 * abs(by - ay)
        for p, q in (((ax, az), (bx, bz)), ((bx, bz), (ax, az))):
            out.append((p, q, c, "cave"))
            out.append((SYM.point(*p), SYM.point(*q), c, "cave"))
    return out


@dataclass
class Crystal(Destroyable):
    """The Rime Monument: a crystal of packed ice in its box, one block at the foot, a cross, the full square, a
    cross and one block at the head (21 blocks), its heart bedrock. The box is the destroyable's region; the air in
    its corners is not counted."""

    def shape(self):
        b = self.box
        cx, cz = (b.x0 + b.x1) // 2, (b.z0 + b.z1) // 2
        out = []
        for j, y in enumerate(range(b.y0, b.y1 + 1)):
            reach = (0, 1, 2, 1, 0)[j] if b.y1 - b.y0 == 4 else 2
            for x in range(b.x0, b.x1 + 1):
                for z in range(b.z0, b.z1 + 1):
                    d = abs(x - cx) + abs(z - cz)
                    if d <= reach and not (reach == 2 and d > 2):
                        out.append((x, y, z))
        return out

    def stamp(self, w):
        for p in self.shape():
            w.set(*p, *self.material)
        if self.heart:
            w.set(*self.middle(), *self.heart)

    def check(self, w):
        wrong = [p for p in self.shape() if w.get(*p)[0] != self.material[0] and p != self.middle()]
        bad = [f"destroyable {self.id}: {len(wrong)} blocks of its crystal are not its material"] if wrong else []
        return float_problems("destroyable", self.id, self.box, w) + ground_problems("destroyable", self.id,
                                                                                   self.box.cells(), w) + bad


def objectives():
    O = Objectives(Teams(("red-team", "Rowan", "red", PLAYERS), ("blue-team", "Sloe", "blue", PLAYERS)), SYM)
    O.add(Spawn("red-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=SPAWN_AREA, spread=SPAWN_SPREAD))
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    O.add(Crystal("red-rime", "Rowan Rime Monument", "red-team", MONUMENT_BOX, (B.PACKED_ICE, 0), "packed ice",
                      "100%", heart=(B.BEDROCK, 0)), name="Sloe Rime Monument")
    O.add(Core("red-ember", "Rowan Ember Core", "red-team", CORE_BOX, leak=5), name="Sloe Ember Core")
    return O
