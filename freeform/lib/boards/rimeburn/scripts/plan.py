"""Rimeburn — the plan. One land in two seasons: Frost holds the north in deep winter, Ember the south in the last
of autumn, and each team guards a fire and an ice. The ground is `land.py`; this file holds the places, the
buildings' footprints, the routes and the objectives, and every other script reads them from here.

    teams       Ember (gold, south) and Frost (aqua, north), 24 a team, the half turn between them
    objectives  a team's Hearth (a core, lava in obsidian over a hollow) and its Icestone (a monument of packed ice
                on the Rime Shelf); destroy both of the enemy's to win
    void        the seam z -24..23 between the two lands, every column of it a build zone; the Thaw in its middle
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import land as LD  # noqa: E402
from pgmvox.built.build import Frame  # noqa: E402
from pgmvox.core.blocks import B  # noqa: E402
from pgmvox.play.objectives import Box, Core, Destroyable, Objectives, Observer, Spawn, Teams  # noqa: E402
from pgmvox.plan.raster import Raster  # noqa: E402

SYM = LD.SYM
KILL_Y = 20
MAX_BUILD = 78
SEAM = (-64, -26, 63, 25)            # the build zone over the void between the lands: x0, z0, x1, z1
TEAMS = Teams(("ember-team", "Ember", "gold", 24), ("frost-team", "Frost", "aqua", 24))

# ---- the objectives, Frost's; Ember's are their half turn --------------------------------------------------
CORE = Box(LD.HEARTH[0] - 2, 40, LD.HEARTH[1] - 2, LD.HEARTH[0] + 2, 44, LD.HEARTH[1] + 2)     # 5 cube, lava 3 cube
ICESTONE = Box(LD.SHELF[0] - 1, 50, LD.SHELF[1] - 1, LD.SHELF[0] + 1, 52, LD.SHELF[1] + 1)      # 3 cube of packed ice
DAIS = 46                                                       # the shrine's floor, a step over the shelf top
SPAWN_BOX = Box(LD.SPAWN[0] - 5, 47, LD.SPAWN[1] - 4, LD.SPAWN[0] + 5, 50, LD.SPAWN[1] + 3)

# ---- the buildings: (centre x, centre z, heading, L along its ridge, W across, floor, storeys, door side) ------
BUILDINGS = {
    "the Hold": (LD.SPAWN[0], -88, 0, 15, 7, LD.TERRACE, 2, 1),                     # the spawn's longhouse, door south
    "Rimecroft: the long house": (43, -36, 0, 8, 5, LD.HAMLET_FLOOR, 1, 1),
    "Rimecroft: the byre": (54, -31, 90, 7, 5, LD.HAMLET_FLOOR, 1, -1),
    "Rimecroft: the smithy": (47, -25, 0, 6, 5, LD.HAMLET_FLOOR, 1, -1),
}
# the deck in the Thaw: four legs, a floor at 44, stairs up from each side's shore
THAW_DECK = (-5, -5, 4, 4, 44)       # x0, z0, x1, z1, floor (symmetric under the half turn by itself)
# the Vent: a passage from the coast's cliff under the front into the Hearth Hollow, (x, floor y, z) waypoints
VENT = LD.VENT
# the March: a broken drystone dyke across the front, two blocks high with gaps where the paths and the Vent's
# barrow cross; cover to fight from, never a line that closes the front
MARCH = [(-57, -33), (-47, -32), (-37, -35), (-27, -38), (-17, -39), (-7, -41), (5, -42)]
MARCH_GAPS = [(-48.5, 3), (-36, 3), (-24, 4), (-12, 3), (-4, 4)]      # (x at the gap's middle, width)
# the bridges over the burn: (x0, z0, x1, z1, deck y)
BRIDGES = [(-13, -68, -9, -64, 0), (-3, -59, 3, -56, 0)]

# ---- the routes a player walks, drawn as paths (Frost's; Ember's are their image) ---------------------------
PATHS = {
    "Hold to the Hearth": [(4, -76), (-2, -72), (-11, -66), (-18, -63), (-22, -61)],
    "Hold to the Shelf": [(10, -76), (17, -70), (24, -63), (27, -59)],
    "Hold to the front": [(6, -74), (3, -66), (0, -57), (-2, -46), (-6, -36), (-8, -27)],
    "Shelf to Rimecroft": [(41, -47), (43, -40), (46, -34)],
    "Hearth to the Anvil": [(-24, -50), (-30, -42), (-37, -37)],
    "Rimecroft to the front": [(45, -28), (40, -22), (34, -20)],
}

PLACES = {
    "the Hold": (6, -86), "the Rimewall": (-10, -93), "Hearth Hollow": (-30, -66), "the Anvil": LD.ANVIL,
    "the Rime Shelf": (40, -66), "the Tarn": LD.TARN, "Rimecroft": LD.HAMLET, "the Vent": (-27, -29),
    "the Thaw": (0, 0), "the knolls": (-14, -32), "the burn": (-15, -73),
}

KINDS = ["void", "ground", "water", "seam", "wall", "stair"]
COLOURS = {"void": (24, 28, 40), "ground": (150, 170, 140), "water": (120, 170, 220), "seam": (60, 64, 90),
           "wall": (150, 100, 70), "stair": (190, 180, 150)}
WALK = {"ground", "water", "stair"}


def building_cells(name):
    cx, cz, heading, L, W, floor, storeys, door = BUILDINGS[name]
    return Frame(cx, cz, heading).cells(L, W)


def build():
    """The plan raster: every column's floor and kind, both halves."""
    X, Z, H, land, water, surface = LD.build()
    R = Raster((LD.X0, LD.X1), (LD.Z0, LD.Z1), KINDS, 0, "void", SYM)
    R.H[:] = np.where(land, H, 0)
    R.K[land] = R.kinds["ground"]
    R.K[land & water] = R.kinds["water"]
    R.H[land & water] = np.where(water, surface, H)[land & water]
    sx0, sz0, sx1, sz1 = SEAM
    seam = (~land) & (X >= sx0) & (X <= sx1) & (Z >= sz0) & (Z <= sz1)
    R.K[seam] = R.kinds["seam"]
    for m in LD.ramp_cells(X, Z).values():
        R.K[m & land] = R.kinds["stair"]
    for name in BUILDINGS:
        for x, z in building_cells(name):
            R.cell(x, z, BUILDINGS[name][5] + 6, "wall")
    for x, z in march_cells():
        R.cell(x, z, int(R.H[R.ix(x), R.iz(z)]) + 2, "wall")
    return R


def march_cells():
    """The March's cells, Frost's (the raster's cell() draws the image too)."""
    from pgmvox.geom import shapes
    out = set()
    for (ax, az), (bx, bz) in zip(MARCH, MARCH[1:]):
        n = int(max(abs(bx - ax), abs(bz - az)) * 2) + 1
        for t in np.linspace(0, 1, n):
            x, z = int(round(ax + (bx - ax) * t)), int(round(az + (bz - az) * t))
            if any(abs(x - gx) <= w / 2 for gx, w in MARCH_GAPS):
                continue
            out.add((x, z))
    return sorted(out)


def vent_extra(R):
    """The Vent as edges for the walk graph: a passage under the ground the raster cannot draw, from the void
    face of the coast (reached by building) to the hollow's floor, in both halves."""
    from pgmvox.plan.graph import node
    cells = [(x, z) for x, y, z in VENT]
    total = float(sum(np.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(cells, cells[1:])))
    out = []
    for mouth, end in ((cells[0], cells[-1]), (SYM.point(*cells[0]), SYM.point(*cells[-1]))):
        out.append((node(R, *mouth), node(R, *end), total, "vent"))
        out.append((node(R, *end), node(R, *mouth), total, "vent"))
    return out


def objectives():
    O = Objectives(TEAMS, SYM)
    O.add(Spawn("frost-team", (LD.SPAWN[0], 47, LD.SPAWN[1]), yaw=0, area=SPAWN_BOX, kit="frost-kit"),
          kit="ember-kit")
    O.add(Core("frost-hearth", "Frost Hearth", "frost-team", CORE, leak=5), name="Ember Hearth")
    O.add(Destroyable("frost-icestone", "Frost Icestone", "frost-team", ICESTONE, material=(B.PACKED_ICE, 0),
                      materials="packed ice"), name="Ember Icestone")
    O.add(Observer((0, 62, 0), yaw=0), mirror=False)
    return O


def goal_cells(box, ring=2):
    """The ground a player attacks a floating goal from: every column within `ring` of its footprint."""
    return [(x, z) for x in range(box.x0 - ring, box.x1 + ring + 1) for z in range(box.z0 - ring, box.z1 + ring + 1)]
