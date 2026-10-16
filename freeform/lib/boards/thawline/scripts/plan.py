"""Thawline: a destroy-the-core and destroy-the-monument board for two teams of twenty, each a core and a monument.

One valley in one week of the year. Frost holds the north, where the winter has already come: a glacier behind the
hall, snow on the field, spruce on the slopes. Ember holds the south, the same ground still in its autumn: brown
oaks and golden larches, a charcoal burners' yard, fire in the hearths. Between them the ground has split along the
Thawline, a rift with lava at its bottom; the Rimefire Stack stands in it, half ice and half fire.

Frost is red's place in the library's terms: its half (z < 0) is drawn, and Ember is its image under the half turn,
(x, z) -> (-1 - x, -1 - z). The ground and every place stand the same on both halves; only what they are made of
changes, by season (season.py). Heights: H is the y of the floor block and a player stands at H + 1.

    Rimehall        the spawn, a terrace at 53 against the Glacier with the hall behind it
    the Kettle      a kettle hole 7 deep west of the hall: the Frost Heart (the core) hangs over it
    Lantern Green   a paved terrace at 48 east of the hall: the Frost Lantern (the monument) floats over it
    Hoarstead       the hamlet beside the green, on the Rime Beck: houses, an ice house, a hay yard
    Rimewood        a wood of snow-laden oaks between the Kettle and the rift
    Coldwater       a tarn in front of the Kettle; the Culvert runs from its shore under the rim to the Kettle's floor
    Hoarcrag        a tor at the coast over the Kettle
    the Moraine     the low ridge across the middle field, broken by the Knoll Road's pass
    the Knoll       a rise in the middle field with the Frostwatch on it, a ruined tower and its beacon
    the Thawline    the rift between the halves, bridged by building; the Stack in its middle

    build()          the plan raster over land.py's ground (steep and water marked) and the Culvert as storey 1
    objectives()     the teams, spawns, observer, the two cores and the two monuments
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import numpy as np  # noqa: E402

import land  # noqa: E402
from pgmvox.core.blocks import B  # noqa: E402
from pgmvox.play.objectives import Box, Core, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan.raster import Raster  # noqa: E402

BOARD = "thawline"
X_MIN, X_MAX = land.X0, land.X0 + land.NX - 1
Z_MIN, Z_MAX = land.Z0, land.Z0 + land.NZ - 1
SYM = land.SYM
KILL_Y = 28
MAX_BUILD = 82
RIFT_FLOOR = 13                         # the rift's floor of rock, its lava standing three over it
LAVA_Y = 16
PLAYERS = 20

X, Z, H, LAND, RIFT, STACK, WET, WATERS, MADE = land.ground()


def g(x, z):
    """The ground's floor block at a column."""
    return int(H[x - X_MIN, z - Z_MIN])


# ---- the objectives ------------------------------------------------------------------------------------------
SPAWN_AT = (0, land.SPAWN_Y + 1, -82)
SPAWN_AREA = Box(-13, land.SPAWN_Y + 1, -93, 12, land.SPAWN_Y + 9, -79)
CORE_BOX = Box(-38, 48, -58, -34, 52, -54)                 # 5 by 5 by 5 over the Kettle's floor at 40
LANTERN_BOX = Box(31, land.GREEN_Y + 4, -55, 31, land.GREEN_Y + 6, -55)   # three obsidian, four over the green
OBSERVER_AT = (0, 92, 0)

# ---- the places (Frost's; Ember's are their images) -----------------------------------------------------------
HALL = dict(cx=0, cz=-90, heading=0, L=17, W=7)            # the hall on the terrace's back, its door to the south
# the terrace's two flights down to the Hall Road and the field: (x0, x1, z of the top step, steps)
HOUSES = land.HOUSES
ICEHOUSES = land.DOMES
HAYYARD = (48, -66, 54, -63)                                 # hay under snow for Frost, pumpkins for Ember
KNOLL_TOWER = (10, -31)                                      # the Frostwatch: a ruined round tower on the Knoll
CULVERT = [(-25, -44), (-29, -48), (-33, -52)]              # from Coldwater's north shore to the Kettle's floor
CULVERT_FLOOR = [41, 41, 40]
KETTLE_PILLARS = [(-46, -62), (-26, -62), (-45, -48), (-27, -48)]   # four spires on the Kettle's rim
LANTERN_POSTS = [(26, -60), (36, -60), (26, -50), (36, -50)]        # four lamps round the monument

PLACES = [("RIMEHALL (spawn)", (0, -90)), ("the Glacier", (0, -98)), ("the Kettle", (-36, -70)),
          ("Frost Heart", (-36, -58)), ("Hoarcrag", (-55, -66)), ("Coldwater", (-20, -37)), ("the Culvert", (-30, -47)),
          ("Rimewood", (-50, -28)), ("LANTERN GREEN", (30, -70)), ("Frost Lantern", (30, -58)),
          ("HOARSTEAD", (50, -46)), ("the Rime Beck", (46, -66)), ("the Moraine", (-6, -46)), ("the Knoll", (10, -26)),
          ("THE THAWLINE", (-40, -1)), ("the Stack", (0, 0))]

KINDS = ["ground", "steep", "water", "culvert"]
WALK = {"ground", "water", "culvert"}
COLOURS = {"ground": (150, 165, 120), "steep": (128, 128, 124), "water": (70, 100, 150), "culvert": (110, 90, 120)}


@lru_cache(maxsize=1)
def terraces():
    """The two terraces' masks, Frost's half: Rimehall's ellipse and Lantern Green's disc, as land.py made them."""
    cx, cz = land.SPAWN
    hall = (np.hypot((X + 0.5 - cx) / 17.0, (Z + 0.5 - cz) / 7.5) < 1) & (Z < 0)
    gx, gz = land.GREEN
    green = MADE & (np.hypot(X - gx, Z - gz) < 11) & (Z < 0)
    return {"hall": hall, "green": green}


@lru_cache(maxsize=1)
def flights():
    """Every flight set into a terrace's face: (name, terrace, top, the way down, its rim cells, its steps), each
    step (x, y, z) a stair one under the last, out from the rim until it meets the ground. Frost's; Ember's are the
    images. The raster walks them and the generator lays them from this one list."""
    T = terraces()
    hall, green = T["hall"], T["green"]

    def rim_max_z(mask, x):
        return max(int(z) for z in Z[0][mask[x - X_MIN]])

    def rim_min_x(mask, z):
        return min(int(x) for x in X[:, 0][mask[:, z - Z_MIN]])
    spec = [("the Hall Stair", "hall", land.SPAWN_Y, "s", [(x, rim_max_z(hall, x)) for x in range(-2, 2)]),
            ("the Green's west stair", "green", land.GREEN_Y, "w", [(rim_min_x(green, z), z) for z in range(-57, -53)]),
            ("the Green's south stair", "green", land.GREEN_Y, "s", [(x, rim_max_z(green, x)) for x in range(30, 34)])]
    out = []
    for name, terrace, top, d, rim in spec:
        dx, dz = {"s": (0, 1), "w": (-1, 0), "n": (0, -1), "e": (1, 0)}[d]
        steps = []
        for x, z in rim:
            y, k = top, 1
            while True:
                cx, cz = x + dx * k, z + dz * k
                if not LAND[cx - X_MIN, cz - Z_MIN]:
                    break
                y -= 1
                if y <= g(cx, cz):
                    break
                steps.append((cx, y, cz))
                k += 1
        out.append((name, terrace, top, d, rim, steps))
    return out


@lru_cache(maxsize=1)
def build():
    """The plan raster: land.py's ground, ground past 52 degrees steep, the water; the rift is no kind of floor
    (base 0), crossed only by building; the Culvert as storey 1 under the Kettle's rim."""
    from pgmvox.surface.terrain import slope_deg
    R = Raster((X_MIN, X_MAX), (Z_MIN, Z_MAX), KINDS, 0, "ground", SYM)
    R.H[:] = H
    R.K[slope_deg(H, LAND) > 52] = R.kinds["steep"]
    R.K[WET] = R.kinds["water"]
    R.K[~LAND] = R.kinds["steep"]
    for _, _, top, _, rim, steps in flights():
        for x, z in rim:
            R.cell(x, z, top, "ground", both=True)
        for x, y, z in steps:
            R.cell(x, z, y, "ground", both=True)
    U = R.storey(1)
    for (x0, z0), (x1, z1), y0, y1 in zip(CULVERT, CULVERT[1:], CULVERT_FLOOR, CULVERT_FLOOR[1:]):
        n = max(abs(x1 - x0), abs(z1 - z0))
        for k in range(n + 1):
            x = round(x0 + (x1 - x0) * k / n)
            z = round(z0 + (z1 - z0) * k / n)
            y = round(y0 + (y1 - y0) * k / n)
            for dx in (0, 1):
                for dz in (0, 1):
                    if g(x + dx, z + dz) >= y + 3:
                        U.cell(x + dx, z + dz, y, "culvert")
    return R


def objectives():
    O = Objectives(Teams(("frost-team", "Frost", "aqua", PLAYERS), ("ember-team", "Ember", "gold", PLAYERS)), SYM)
    O.add(Spawn("frost-team", SPAWN_AT, yaw=0, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Observer(OBSERVER_AT, yaw=90), mirror=False)
    O.add(Core("frost-heart", "Frost Heart", "frost-team", CORE_BOX, leak=5), name="Ember Heart")
    O.add(Destroyable("frost-lantern", "Frost Lantern", "frost-team", LANTERN_BOX, (B.OBSIDIAN, 0), "obsidian", "100%"),
          name="Ember Lantern")
    return O
