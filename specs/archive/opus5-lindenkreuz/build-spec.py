#!/usr/bin/env python3
"""Write the plan and the finish for `opus5-lindenkreuz`, for `tools/drive.py` to build.

    python3 specs/opus5-lindenkreuz/build-spec.py
    python3 tools/drive.py specs/opus5-lindenkreuz "Lindenkreuz" --out /tmp/lindenkreuz

**The board.** Two city blocks either side of a twenty-block gorge, joined by one railway bridge: a
car park with the monument standing in a marked bay, a Litfassaeule and a street piano on the station
forecourt, houses on two raised garden terraces, and the S-Bahn running out of a cut-and-cover tunnel
under the whole quarter, up a ramp in an open cutting and away over the bridge.

**Angular on purpose.** The board carries **no relief at all**. Every height on it is a stated one --
the plan's per-piece `surface`, an authored shape's `base_height`, a ramp's `anchor_heights` -- so
every face is sheer and every floor is flat, which is what a city block looks like from above and what
minuyo's boards look like from the ground. It also makes every surface height known at authoring time,
which is what lets a 5x3 car state an absolute floor and land on the tarmac rather than in it.

**The vertical model**, since everything below is written against it:

    y23   the two garden terraces (pieces at surface 24)
    y19   the city: forecourt, car park, cutting shoulders, the tunnel lid, the bridge deck
    y17   the lid's soffit -- the tunnel roof, a layer of its own at base_y 17
    y10   the station platform
    y8    the trackbed, at the bottom of a trench cut eleven courses into the city

The trench is an **override add**: an override add overwrites the column outright, which is the only
way to cut into ground a plain add has already claimed. The lid cannot be one -- among override adds on
one layer the taller wins, so a lid at y17..y19 would simply delete the trench under it -- so the lid is
a layer of its own.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))

from layers import compile_layers, stats                      # noqa: E402

SLUG = "opus5-lindenkreuz"
NAME = "Lindenkreuz"
CREATED = "2026-09-02"

# -- the board's numbers -------------------------------------------------------------------------
CELL = 5
CITY = 20            # top block y19 -- forecourt, car park, cutting shoulders
TERRACE = 24         # top block y23 -- the two garden blocks
TRACK = 9            # top block y8  -- the trackbed
PLATF = 11           # top block y10 -- the station platform
LID_Y, LID_H = 17, 3  # the tunnel roof: a layer of its own, y17..y19, flush with the city over it

X0, X1 = -45, 45     # the board, in blocks
Z0, Z1 = -100, 100

TRENCH_X = (-10, 11)          # x -10..10, 21 wide          (min inclusive, max exclusive)
TRENCH_Z = (-80, -35)         # the cut-and-cover tunnel, clear of the hall's own foundation
BOX_X = (10, 19)              # the station box widens the trench east to x 18
BOX_Z = (-80, -62)            # and stops north of the car park's east ramp, which stands on the lid
PLAT_X = (4, 19)              # the platform, 15 wide, along the box's east side
RAILS = (-9, -6, -2, 1)       # two tracks on the fourteen blocks the platform leaves
RAMP_Z = (-35, -11)           # the open cutting: the line climbs y8 -> y19 over 24 blocks
BRIDGE_Z = (-12, 12)
WELL_X, WELL_Z = (16, 19), (-78, -68)   # the light well the upper flight comes down in

GOAL = (-15, -51)             # the monument, dead centre of a marked bay

# -- blocks --------------------------------------------------------------------------------------
STONE, ANDESITE, POLISHED = (1, 0), (1, 5), (1, 6)
GRASS, DIRT, COARSE, COBBLE = (2, 0), (3, 0), (3, 1), (4, 0)
GRAVEL, SPONGE = (13, 0), (19, 0)
STONE_SLAB, BRICKS = (44, 0), (45, 0)
ICE, GLOWSTONE = (79, 0), (89, 0)
STONEBRICK, CRACKED, CHISELLED = (98, 0), (98, 2), (98, 3)
NETHERBRICK, QUARTZ = (112, 0), (155, 0)
SMOOTH_SLAB = (43, 8)
COAL = (173, 0)
CLAY_WHITE, CLAY_LGREY, CLAY_GREY, CLAY_BLACK = (159, 0), (159, 8), (159, 7), (159, 15)
CLAY_GREEN, CLAY_YELLOW = (159, 13), (159, 4)
WOOL_WHITE, WOOL_YELLOW, WOOL_RED, WOOL_BLUE = (35, 0), (35, 4), (35, 14), (35, 3)


def solid(block):
    return {"kind": "solid", "id": block[0], "data": block[1]}


def noise(seed, scale, *blocks, octaves=2, rise=0):
    """Two shades of one ground with grain in it -- never a border between two grounds."""
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": [solid(b) for b in blocks], "rise": rise}


def turf(top, *under):
    """A surfacing block over soil. `PT1`: grass is a **pick**, not a stack -- stated as a surface
    material three courses deep it surfaces the ground and then fills all three, which is a lawn
    with grass under it. One course of it at the top of a layered stack is what turf is."""
    bands = [{"material": top, "thickness": 1}]
    bands += [{"material": solid(b), "thickness": t} for b, t in under]
    return {"kind": "layered", "axis": "depth", "beyond": solid(under[-1][0]),
            "stack": {"ending": "handOver", "bands": bands}}


def face(*bands, beyond):
    """A wall bucket banded by depth from the top of the face. `DepthFromTop` counts down the cut, so
    on a board whose drops all start at one shelf, banding by depth is banding by altitude: three
    courses of brick coping over two of stone brick over the rock, all the way down."""
    return {"kind": "layered", "axis": "depth", "beyond": solid(beyond),
            "stack": {"ending": "handOver",
                      "bands": [{"material": solid(b), "thickness": t}
                                for b, t in zip(bands[::2], bands[1::2])]}}


def ground(surface, wall, fill, rim=None, depth=3, edges="void"):
    """A terrain theme in the five buckets.

    `edges` is where the rim runs. `boundary` caps every shape's outline, which on a board drawn out
    of a hundred rectangles is a chiselled line round each of them -- sixteen per cent of the plaza,
    measured. `void` caps only the edges that stand over nothing: the gorge and the board's own rim,
    which are the two edges this board wants capped. The kerbs and copings it wants elsewhere are
    drawn as shapes, where they can be put exactly."""
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": edges,
        "wallOnTerrainFaces": True,
        "rim": {"enabled": rim is not None, "depth": 1, "material": solid(rim or STONE)},
        "surface": {"enabled": True, "depth": depth, "material": surface},
        "wall": wall,
        "wallEnabled": True,
        "fill": fill,
    }


def flat(block):
    """One block in every bucket -- what a made thing is: a car is sponge all the way through."""
    return ground(solid(block), solid(block), solid(block), rim=block, depth=1)


def course(top, under=STONE):
    """One course of paint over ordinary ground.

    A theme owns a **whole column**, so an accent stated in all five buckets paints its column to
    bedrock -- and where that column is the wall of a trench, the marking runs eleven courses down
    the wall. A bay line is a surface, so only the surface bucket is the line."""
    return ground(solid(top), solid(under), solid(under), rim=None, depth=1)


THEMES = {
    # -- the five grounds --------------------------------------------------------------------------
    "city": ground(noise(11, 17, CLAY_LGREY, CLAY_LGREY, STONE), solid(ANDESITE), solid(STONE),
                   rim=CHISELLED),
    "tarmac": ground(noise(23, 19, CLAY_GREY, CLAY_GREY, CLAY_LGREY), solid(STONEBRICK), solid(STONE),
                     rim=SMOOTH_SLAB),
    # the one ground whose rim is wanted at its own outline: a brick kerb round the lawn
    "garden": ground(turf(noise(37, 14, GRASS, GRASS, COARSE), (DIRT, 1), (COARSE, 1)),
                     face(BRICKS, 3, STONEBRICK, 2, beyond=ANDESITE), solid(STONE), rim=BRICKS,
                     edges="boundary"),
    "ballast": ground(noise(41, 12, GRAVEL, GRAVEL, COBBLE), solid(STONEBRICK), solid(STONE)),
    "concrete": ground(noise(53, 15, STONEBRICK, STONEBRICK, CRACKED), solid(ANDESITE), solid(STONE),
                       rim=CHISELLED),
    # -- the accents, one course each --------------------------------------------------------------
    "steel": course(POLISHED),
    "line": course(CLAY_WHITE),
    "warnline": course(CLAY_YELLOW),
    "coping": course(SMOOTH_SLAB),
    "stage": course(QUARTZ),
    # -- what the made things are made of ----------------------------------------------------------
    "car-wheel": flat(COAL),
    "car-body": flat(SPONGE),
    "car-glass": flat(ICE),
    "car-roof": flat(STONE_SLAB),
    "col-base": flat(STONEBRICK),
    "col-shaft": flat(CLAY_GREEN),
    "col-cap": flat(STONE_SLAB),
    "poster-a": flat(WOOL_WHITE),
    "poster-b": flat(WOOL_YELLOW),
    "poster-c": flat(WOOL_RED),
    "poster-d": flat(WOOL_BLUE),
    "piano": flat(NETHERBRICK),
    "piano-keys": flat(QUARTZ),
    "lamp-mast": flat(CLAY_BLACK),
    "lamp-head": flat(GLOWSTONE),
}

# -- the plan ------------------------------------------------------------------------------------
# Cells, five blocks each, the origin at the symmetry centre. Only the north half is authored;
# rot_180 fans it. Two surfaces and no relief, so the compile emits one polygon per height and
# no subtract -- the gorge is simply ground no piece covers.
PLAN = {
    # Version 2: a marker's `at` is an offset in BLOCKS -- from the piece's minimum corner where one
    # is named, and from the symmetry centre where none is. Version 1 stated the same field in cells,
    # and the compile refuses rather than guessing which a number is in.
    "plan": 2,
    "meta": {"name": NAME},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24, "surface": CITY,
                "observerY": 64},
    "pieces": [
        # The station hall and the street either side of it. The hall is four cells square, and that
        # is WX3 rather than taste: the spawn pad is always square, so a piece of an even span on one
        # axis and an odd span on the other has no marker position whose parity agrees with itself.
        {"id": "stn", "role": "spawn", "rect": [-2, -20, 4, 4], "surface": CITY},
        {"id": "street-w", "role": "piece", "rect": [-9, -20, 7, 4], "surface": CITY},
        {"id": "street-e", "role": "piece", "rect": [2, -20, 7, 4], "surface": CITY},
        # the forecourt: the Litfassaeule, the piano stage, the way down to the platform
        {"id": "forecourt", "role": "piece", "rect": [-9, -16, 18, 3], "surface": CITY},
        # the car park between two raised garden terraces
        {"id": "garden-w", "role": "piece", "rect": [-9, -13, 4, 6], "surface": TERRACE},
        {"id": "carpark", "role": "piece", "rect": [-5, -13, 10, 6], "surface": CITY},
        {"id": "garden-e", "role": "piece", "rect": [5, -13, 4, 6], "surface": TERRACE},
        # the shoulders of the cutting, and the ground the bridge is reached over
        {"id": "cutting", "role": "piece", "rect": [-9, -7, 18, 5], "surface": CITY},
    ],
    # One zone, the whole board's width, over the gorge and a course of ground either side of it.
    "zones": [{"id": "mid", "rect": [-9, -3, 18, 6], "holes": []}],
    "placements": {
        # (0, -90), ten blocks in from the hall's north-west corner: the concourse's own middle.
        "spawns": [{"id": "spawn-1", "piece": "stn", "at": [10, 10], "facing": "back"}],
        # No piece, so the offset is from the symmetry centre: the monument stands where the bay is.
        "destroyables": [{"id": "destroyable-1", "at": [GOAL[0], GOAL[1]],
                          "style": "pillar-3", "materials": "obsidian", "float": 2,
                          "name": "Parking Meter"}],
    },
}


# -- ground shapes ---------------------------------------------------------------------------------
SHAPES = []


def rect(sid, x0, x1, z0, z1, *, paint=None, floor=0, height=None, override=False, keep=False):
    """One rectangle on the ground layer. `x1`/`z1` are exclusive, the way the rasterizer reads them.

    A shape with a height and `override` cuts or stands: the column becomes its own, floor and all
    (and where the ground's own span reaches its floor, the ground under it survives). A shape with
    `height=1` and no override is a **paint patch** -- the taller add keeps the column and the
    smaller shape keeps the paint, which is how a bay marking is drawn without punching a hole in
    the tarmac."""
    shape = {"id": sid, "type": "rectangle", "operation": "add",
             "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
             "floor": floor, "base_height": 1 if height is None else height}
    if override:
        # SK14: an override add states how its top is decided, or a relief takes it away. This board
        # has no relief and states them anyway -- the shape means a sheer face at a stated level.
        shape.update({"override": True, "height_mode": "level", "skirt": 0,
                      "relief_scope": "exclude"})
    if keep:
        shape["keepClear"] = True
    if paint:
        shape["theme"] = paint
    SHAPES.append(shape)
    return shape


def runs(z0, z1, step=12):
    """A long run split into shapes short enough to win their own paint. Paint scope goes to the
    smallest-area shape covering a cell, so a 21x49 trench loses its floor to anything smaller drawn
    over it; twelve-block segments keep it."""
    z = z0
    while z < z1:
        yield z, min(z + step, z1)
        z += step


LID_SHAPES = []


def lid(sid, x0, x1, z0, z1, paint, floor=0, height=None):
    """One rectangle on the lid, the layer that roofs the tunnel: base_y 17, three courses to y19.
    A `floor` of LID_H puts a course on top of the deck rather than in it."""
    LID_SHAPES.append({"id": sid, "type": "rectangle", "operation": "add",
                       "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
                       "floor": floor, "base_height": (LID_H if height is None else height),
                       "theme": paint, "keepClear": height is not None})


# What the lid covers where it runs under the car park -- the trench for its whole length and the
# station box beside it.
ROOFED = [(TRENCH_X[0], TRENCH_X[1], -65, TRENCH_Z[1]), (TRENCH_X[1], BOX_X[1], -65, BOX_Z[1])]


def without(rect_, boxes):
    """`rect_` minus every box, as axis-aligned pieces. Four splits a box at a time, which is exact
    for the rectangles this board draws and needs no cell grid."""
    out = [rect_]
    for bx0, bx1, bz0, bz1 in boxes:
        keep = []
        for x0, x1, z0, z1 in out:
            if bx1 <= x0 or bx0 >= x1 or bz1 <= z0 or bz0 >= z1:
                keep.append((x0, x1, z0, z1))
                continue
            if x0 < bx0:
                keep.append((x0, bx0, z0, z1))
            if bx1 < x1:
                keep.append((bx1, x1, z0, z1))
            mx0, mx1 = max(x0, bx0), min(x1, bx1)
            if z0 < bz0:
                keep.append((mx0, mx1, z0, bz0))
            if bz1 < z1:
                keep.append((mx0, mx1, bz1, z1))
        out = keep
    return out


def mark(sid, x0, x1, z0, z1, paint):
    """A course of paint, drawn on the ground where the ground is what a player sees and on the lid
    where the lid is.

    Paint scope is keyed by **layer** as well as by cell -- a cell covered on two layers is not
    contested, because each layer shows its own surface -- so a bay marking drawn on the ground layer
    alone does not appear on the twenty-nine blocks of car park that stand on the tunnel roof. It is
    the one thing a stacked board makes the author say twice.

    And the ground copy is **cut out** of the lid's footprint rather than left under it, because a
    theme owns a whole column: a one-course marking that wins a roofed cell paints the tunnel floor
    and the tunnel wall beneath it white, thirteen courses down, where nobody drew a line at all."""
    for i, (px0, px1, pz0, pz1) in enumerate(without((x0, x1, z0, z1), ROOFED)):
        rect(f"{sid}-{i}", px0, px1, pz0, pz1, paint=paint)
    for i, (rx0, rx1, rz0, rz1) in enumerate(ROOFED):
        cx0, cx1 = max(x0, rx0), min(x1, rx1)
        cz0, cz1 = max(z0, rz0), min(z1, rz1)
        if cx0 < cx1 and cz0 < cz1:
            lid(f"{sid}-lid{i}", cx0, cx1, cz0, cz1, paint)


# ---- the tunnel, the station box and the platform -------------------------------------------------
# The trench is cut with override adds, which is what overwrites a column a plain add already claimed.
for i, (a, b) in enumerate(runs(*TRENCH_Z)):
    rect(f"trench-{i}", TRENCH_X[0], TRENCH_X[1], a, b, paint="ballast", height=TRACK, override=True)
for i, (a, b) in enumerate(runs(*BOX_Z)):
    rect(f"box-{i}", BOX_X[0], BOX_X[1], a, b, paint="concrete", height=TRACK, override=True)

# The platform: taller than the trench, so among the override adds it takes its own cells.
for i, (a, b) in enumerate(runs(*BOX_Z)):
    rect(f"platform-{i}", PLAT_X[0], PLAT_X[1], a, b, paint="concrete", height=PLATF, override=True)
# and its yellow safety line, one course of paint laid on the platform's own top.
rect("platform-edge", PLAT_X[0], PLAT_X[0] + 1, BOX_Z[0], BOX_Z[1],
     paint="warnline", floor=PLATF - 1, height=1, override=True)

# Two tracks on the ballast, four rails, one course of paint each with its floor on the trackbed's own
# top block -- so the rail is drawn without anything about the trench's height changing.
for rail, x in enumerate(RAILS):
    for i, (a, b) in enumerate(runs(TRENCH_Z[0], RAMP_Z[0], step=16)):
        rect(f"rail-{rail}-{i}", x, x + 1, a, b, paint="steel", floor=TRACK - 1, height=1,
             override=True)

# The way down: nine courses from the forecourt to the platform, and eighteen blocks of run for them,
# which is three more than the forecourt is deep. So it is a **switchback** -- one flight south in the
# light well and one back north under the lid -- and every step is one rectangle, one block high.
# A ramp polygon over this run would rasterize as treads of two and charge a placed block to climb.
#
# The break between the two flights is not arbitrary: the lid's soffit is y17, so a step whose top
# block is 14 or higher has less than three blocks of headroom under it. Everything above that is in
# the well, everything below it is roofed.
for step in range(5):                                     # flight down, in the open: tops 18..14
    rect(f"stair-a{step}", WELL_X[0], WELL_X[1], WELL_Z[0] + 2 * step, WELL_Z[0] + 2 * step + 2,
         paint="concrete", height=19 - step, override=True)
for step in range(4):                                     # flight back, under the lid: tops 13..10
    rect(f"stair-b{step}", 12, WELL_X[0] - 1, WELL_Z[1] - 2 * step - 2, WELL_Z[1] - 2 * step,
         paint="concrete", height=14 - step, override=True)

# The ramp out of the tunnel: one tilted quad, 24 blocks of run for 11 courses of rise. `level` with
# per-vertex thicknesses is the whole instrument -- the courses are what a sloped surface rasterizes
# to, and at better than 2:1 every step is one block.
SHAPES.append({
    "id": "ramp", "type": "polygon", "operation": "add", "override": True,
    "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "floor": 0,
    "theme": "ballast",
    "vertices": [[TRENCH_X[0], RAMP_Z[0]], [TRENCH_X[1], RAMP_Z[0]],
                 [TRENCH_X[1], RAMP_Z[1]], [TRENCH_X[0], RAMP_Z[1]]],
    "anchor_heights": [TRACK, TRACK, CITY, CITY],
})
# The rails carry on up it, one course over the ramp's own top -- which climbs, so they are drawn per
# column at the height the ramp reaches there -- **one z at a time, and floored, not rounded**.
#
# Drawn in three-block segments at a rounded height they stood a course proud of the ballast wherever
# the ramp stepped inside a segment, and a rail one course proud beside ground one course lower is a
# **two-block rise**: `transect?points=-9,-36;-9,-10` read `scramble +2 at (-9, -26)` and again at
# (-9, -20) while the ballast beside it at x -8 read eleven clean rises and no scramble. Nothing in any
# render shows it; one line of `03-slopes.txt` and one transect do.
#
# The rasterizer's own arithmetic is the fix: a cell samples at its centre, interpolates the anchors
# across the footprint and takes the **floor**. Checked against all 25 stations of that transect.
def ramp_top(z):
    """The ramp's top block at column z, the way the rasterizer builds it."""
    t = (z + 0.5 - RAMP_Z[0]) / (RAMP_Z[1] - RAMP_Z[0])
    return int(TRACK + t * (CITY - TRACK)) - 1


for rail, x in enumerate(RAILS):
    for z in range(*RAMP_Z):
        rect(f"ramprail-{rail}-{z}", x, x + 1, z, z + 1, paint="steel", floor=ramp_top(z), height=1,
             override=True)

# ---- the bridge ------------------------------------------------------------------------------------
# A plain add with its own floor: past the coast there is no ground to read, so the column is the deck
# and the air under it. Over the land at either end the taller add keeps the column, so the deck runs
# into the cutting's shoulder rather than standing on top of it.
rect("bridge", TRENCH_X[0], TRENCH_X[1], BRIDGE_Z[0], BRIDGE_Z[1],
     paint="concrete", floor=LID_Y - 1, height=LID_H + 1, keep=True)
for side, x in ((0, TRENCH_X[0]), (1, TRENCH_X[1] - 1)):
    rect(f"parapet-{side}", x, x + 1, BRIDGE_Z[0], BRIDGE_Z[1],
         paint="coping", floor=CITY, height=1, override=True, keep=True)
# The rails across it.
for rail, x in enumerate(RAILS):
    rect(f"deckrail-{rail}", x, x + 1, BRIDGE_Z[0], BRIDGE_Z[1],
         paint="steel", floor=CITY - 1, height=1, override=True)

# ---- the car park ------------------------------------------------------------------------------
CP_X, CP_Z = (-25, 25), (-65, -35)
ROWS = (-64, -53, -42)                     # each row is five deep: z .. z+5
BAYS = [-24 + 4 * k for k in range(12)]    # each bay is three wide: x .. x+3

rect("carpark", CP_X[0], CP_X[1], CP_Z[0], CP_Z[1], paint="tarmac")
for r, z in enumerate(ROWS):
    for k, x in enumerate(BAYS):
        # One white line between bays, and one across the head of each row: the markings are what
        # say the ground is a car park, and they cost one course of paint each.
        mark(f"bayline-{r}-{k}", x + 3, x + 4, z, z + 5, "line")
    mark(f"rowline-{r}", BAYS[0], BAYS[-1] + 4, z + 5, z + 6, "line")
rect("cp-kerb-w", CP_X[0], CP_X[0] + 1, CP_Z[0], CP_Z[1], paint="coping")
rect("cp-kerb-e", CP_X[1] - 1, CP_X[1], CP_Z[0], CP_Z[1], paint="coping")

# -- the flights up onto the garden terraces -------------------------------------------------------
# Four courses over eight blocks is 2:1, which is what makes a tilted quad a stair rather than a wall:
# under it the courses come out as treads of two and cost a placed block on the way up.
#
# `EL1` complains about all six of these seams anyway, and it is right to at the tier it reads: the
# plan walks its pieces flat, so a four-block step between two rectangles is a four-block step, and an
# authored flight in the layout is invisible to it. There is one at every seam it names.
def flight(sid, x0, x1, z0, z1, corners):
    """A tilted quad, vertices anticlockwise from (x0, z0), a thickness per corner."""
    SHAPES.append({
        "id": sid, "type": "polygon", "operation": "add", "override": True,
        "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "floor": 0, "theme": "city",
        "vertices": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]],
        "anchor_heights": corners,
    })


UP, DOWN = TERRACE, CITY
# out of the car park, west and east: in the aisle, so no ramp is driven through a bay
flight("ramp-cp-w", -25, -17, -58, -53, [UP, DOWN, DOWN, UP])
flight("ramp-cp-e", 17, 25, -58, -53, [DOWN, UP, UP, DOWN])
# off the forecourt, at the outer corner of each terrace
flight("ramp-fc-w", -45, -41, -65, -56, [DOWN, DOWN, UP, UP])
flight("ramp-fc-e", 41, 45, -65, -56, [DOWN, DOWN, UP, UP])
# and down onto the cutting's shoulder at the south end of each
flight("ramp-ct-w", -45, -41, -44, -35, [UP, UP, DOWN, DOWN])
flight("ramp-ct-e", 41, 45, -44, -35, [UP, UP, DOWN, DOWN])

# ---- the forecourt ------------------------------------------------------------------------------
# The piano's stage, one course over the pavement, and the planting the plaza and the street carry.
rect("stage", 22, 33, -78, -70, paint="stage", floor=CITY, height=1, override=True, keep=True)
rect("green-w", -44, -28, -73, -68, paint="garden")
rect("green-e", 34, 45, -73, -68, paint="garden")
# and the two strips along the cutting's shoulders, which is the only planting on the frontline.
rect("green-cw", -44, -14, -32, -26, paint="garden")
rect("green-ce", 14, 44, -32, -26, paint="garden")
# A kerb round the cutting, so eleven courses of sheer face are marked rather than walked off. The
# route read is what asked for it: `spawn-red -> destroyable-1-1` drops **11 blocks at (0, -35)**,
# straight off the car park into the trackbed, because the walk prices a fall at nothing. The kerb
# does not stop the drop -- one course never does -- it says where it is.
rect("cut-kerb-w", TRENCH_X[0] - 1, TRENCH_X[0], RAMP_Z[0], RAMP_Z[1],
     paint="coping", floor=CITY, height=1, override=True, keep=True)
rect("cut-kerb-e", TRENCH_X[1], TRENCH_X[1] + 1, RAMP_Z[0], RAMP_Z[1],
     paint="coping", floor=CITY, height=1, override=True, keep=True)
# A kerb **across** the portal was tried and taken out again: at z -36 it stands on the lid, and an
# override add there reads the plain city polygon under it rather than the trench, keeps "the ground
# under its floor" and fills 42 columns of tunnel (SK10) -- and it deepened the fall it was drawn to
# mark from 11 courses to 12. The mouth of a tunnel is meant to be a hole.
# A kerb along the gorge, so the drop reads as made rather than as a coast.
rect("gorge-kerb-w", X0, TRENCH_X[0], -11, -10, paint="coping")
rect("gorge-kerb-e", TRENCH_X[1], X1, -11, -10, paint="coping")
# and a rail round three sides of the light well, one course on its lip. The fourth side is the
# well's own east wall, which is the solid ground the shaft was cut into.
#
# **It stands on the lid, so it is drawn on the lid -- and as one course thicker rather than as a
# course on top.** Two things had to be learnt here. An override add on the *ground* layer at floor 20
# reads the plain add under it -- the city polygon, top 20 -- and keeps "the ground under its floor",
# which re-filled the tunnel it stands over: 36 columns of solid rock where the platform should have
# had a ceiling, and `SK10` naming it. Moved onto the lid as a shape at floor 3 it then stacked on the
# deck, and a layer holds **one span per column**, so `SK9` declined the deck under it. A rail that is
# the deck plus a course is one span, and the taller shape simply keeps the column.
lid("well-rail-w", WELL_X[0] - 1, WELL_X[0], WELL_Z[0] + 1, WELL_Z[1], "coping", height=LID_H + 1)
lid("well-rail-n", WELL_X[0] - 1, WELL_X[1], WELL_Z[0] - 1, WELL_Z[0], "coping", height=LID_H + 1)
lid("well-rail-s", WELL_X[0] - 1, WELL_X[1], WELL_Z[1], WELL_Z[1] + 1, "coping", height=LID_H + 1)


# -- the lid: a layer of its own ------------------------------------------------------------------
# base_y 17, three courses to y19, flush with the city over it. It cannot be an override add on the
# ground layer: among override adds the taller wins, and a lid is taller than the trench it roofs.
# The bay markings that fall on it were drawn onto it by `mark` as they were drawn; these four are
# the deck itself, with the light well left out of them.
lid("lid-n", TRENCH_X[0], BOX_X[1], BOX_Z[0], WELL_Z[0], "city")
lid("lid-w", TRENCH_X[0], WELL_X[0], WELL_Z[0], WELL_Z[1], "city")
lid("lid-s", TRENCH_X[0], BOX_X[1], WELL_Z[1], -65, "city")
lid("lid-cp1", TRENCH_X[0], BOX_X[1], -65, BOX_Z[1], "tarmac")
lid("lid-cp2", TRENCH_X[0], TRENCH_X[1], BOX_Z[1], TRENCH_Z[1], "tarmac")

LID_LAYER = {
    "id": "lid", "name": "Tunnel lid", "base_y": LID_Y,
    "shapes": LID_SHAPES,
    "groups": [{"id": "lid", "name": "Tunnel lid", "mirrors": True,
                "shapeIds": [s["id"] for s in LID_SHAPES]}],
}


# -- the made things ------------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    """Every cell of an inclusive box."""
    return {(x, y, z) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1) for z in range(z0, z1 + 1)}


def paint_cells(model, *pairs):
    for cells, material in pairs:
        for cell in cells:
            model[cell] = material
    return model


def car():
    """A 5x3 car, four courses, and each course is one of the four layers it compiles to.

    Wheels of coal blocks, a body of sponge, a course of ice for the windows with the rest of the
    body beside it, and a roof of stone slabs. The bonnet is two blocks long and the cabin is at the
    back, which is the only thing that says which way the car is parked."""
    model = {}
    wheels = {(x, 0, z) for x in (-1, 1) for z in (-1, 1)}
    body = box(-1, 1, 1, 1, -2, 2)                                   # the whole footprint, one course
    bonnet = box(-1, 1, 2, 2, -2, -1)                                # the rest of the body, course two
    cabin = box(-1, 1, 2, 2, 0, 2) - {(0, 2, 1)}                     # the glass, hollow in the middle
    roof = box(-1, 1, 3, 3, 0, 2)
    return paint_cells(model, (wheels, "car-wheel"), (body, "car-body"), (bonnet, "car-body"),
                       (cabin, "car-glass"), (roof, "car-roof"))


def column():
    """A Litfassaeule, nine courses over a three-block plinth -- twice a car's height, which is what
    an advertising column stands to a car in the street.

    The shaft is the 3x3 with its corners taken off, so it reads round; the cap is the full square and
    therefore overhangs it, which is the moulding. Four posters, one to a face."""
    model = {}
    plinth = box(-1, 1, 0, 0, -1, 1)
    arms = {(0, 0, -1), (0, 0, 1), (-1, 0, 0), (1, 0, 0), (0, 0, 0)}
    shaft = {(x, y, z) for (x, _, z) in arms for y in range(1, 7)}
    posters = {"poster-a": (0, -1), "poster-b": (0, 1), "poster-c": (-1, 0), "poster-d": (1, 0)}
    model = paint_cells(model, (plinth, "col-base"), (shaft, "col-shaft"))
    for material, (x, z) in posters.items():
        for y in range(2, 6):
            model[(x, y, z)] = material
    model = paint_cells(model, (box(-1, 1, 7, 7, -1, 1), "col-cap"), ({(0, 8, 0)}, "col-cap"))
    return model


def piano():
    """An upright piano in nether brick -- a Klavier, not a Fluegel -- with a keyboard of quartz
    cantilevered off the front and a stool in front of that."""
    model = {}
    case = box(-3, 3, 0, 4, 0, 1)
    keys = box(-3, 3, 2, 2, -1, -1)
    fall = box(-3, 3, 3, 3, -1, -1)
    stool = box(0, 0, 0, 1, -3, -3)
    return paint_cells(model, (case, "piano"), (fall, "piano"), (stool, "piano"),
                       (keys, "piano-keys"))


def lamp():
    """A car-park light: a five-course mast under one block of glowstone."""
    model = {}
    return paint_cells(model, ({(0, y, 0) for y in range(5)}, "lamp-mast"),
                       ({(0, 5, 0)}, "lamp-head"))


def turn(model, quarter):
    """A model spun about its own origin in quarter turns, so a thing can face where it is put."""
    def spun(x, y, z):
        for _ in range(quarter % 4):
            x, z = -z, x
        return x, y, z
    return {spun(x, y, z): material for (x, y, z), material in model.items()}


def place(model, at, quarter=0):
    dx, dy, dz = at
    return {(x + dx, y + dy, z + dz): material
            for (x, y, z), material in turn(model, quarter).items()}


def made(name, voxels, mirrors=True):
    """A model compiled to layers, in the shape `addLayers` takes: one layer per run index, every
    layer marked `made` so the stacking rules stay off it, and `part_of` so the studio reads the
    whole thing as one.

    The floors are absolute rather than seated. A seat lands a thing's lowest course on the ground
    under it, which is right for a building's footing and wrong for a wheel; this board has no relief,
    so the tarmac is at y19 everywhere a car stands and the floor the model was drawn at is the floor
    it wants. `keepClear` is set here rather than by the seat, because these things do stand on the
    ground and the dressing pass must not plant in them."""
    compiled = compile_layers(voxels, prefix=f"{name}-", layer_prefix=f"{name}-L",
                              mirrors=mirrors, group_name=name, part_of=name)
    out = []
    for layer in compiled:
        for shape in layer["layout"]["shapes"]:
            shape["keepClear"] = True
        out.append({"id": layer["id"], "name": layer["name"], "base_y": 0, "kind": "made",
                    "part_of": name, "shapes": layer["layout"]["shapes"],
                    "groups": layer["layout"]["groups"]})
    return out, stats(voxels, compiled)


# Where the cars stand. A car park half full at night: fifteen bays taken out of thirty-six, the
# monument's own bay and the two beside it left open, and nothing over the stairwell.
PARKED = [
    (-23, 0, -62), (-19, 2, -62), (-11, 0, -62), (5, 2, -62), (9, 0, -62), (21, 2, -62),
    (-23, 2, -51), (-7, 0, -51), (9, 2, -51), (17, 0, -51),
    (-19, 0, -40), (-11, 2, -40), (5, 0, -40), (13, 2, -40), (21, 0, -40),
]
# The lamps: in the two aisles, and on the forecourt. Every one of them is at least four blocks and
# three courses from the nearest ice, which is what keeps a glowstone head from melting a windscreen.
LAMPS = [(-21, -56), (-5, -56), (11, -56), (-21, -45), (-5, -45), (11, -45),
         (-16, -77), (6, -76), (-6, -71)]


def sculpted():
    add_layers, table = [], []

    cars = {}
    for x, quarter, z in PARKED:
        cars.update(place(car(), (x, CITY, z), quarter))
    layers, row = made("cars", cars)
    add_layers += layers
    table.append(("cars (x15 a side)", row))

    layers, row = made("column", place(column(), (-22, CITY, -74)))
    add_layers += layers
    table.append(("Litfassaeule", row))

    layers, row = made("piano", place(piano(), (27, CITY + 1, -73), quarter=2))
    add_layers += layers
    table.append(("piano", row))

    lamps = {}
    for x, z in LAMPS:
        lamps.update(place(lamp(), (x, CITY, z)))
    layers, row = made("lamps", lamps)
    add_layers += layers
    table.append(("lamps (x9 a side)", row))

    return add_layers, table


# -- the dressing ---------------------------------------------------------------------------------
# Six buildings a side in two styles, and the ground decides which: the terrace houses stand on the
# garden blocks, the kiosks on the plaza. Neither is walled in the family under its feet -- brown clay
# and brick over grass, orange clay over grey pavement.
HOUSES = [
    # the two terrace rows, one to a garden block, looking down into the car park
    ("hs-w1", "@lk-terrace", (-37, -63), (-28, -55), "posX"),
    ("hs-w2", "@lk-terrace", (-37, -49), (-28, -41), "posX"),
    ("hs-e1", "@lk-terrace", (28, -63), (37, -55), "negX"),
    ("hs-e2", "@lk-terrace", (28, -49), (37, -41), "negX"),
    # the street behind the station, either side of the hall
    ("hs-n1", "@lk-terrace", (-40, -98), (-29, -89), "posZ"),
    ("hs-n2", "@lk-terrace", (27, -98), (38, -89), "posZ"),
    # and a kiosk at each end of the forecourt
    ("ks-w", "@lk-kiosk", (-41, -79), (-34, -74), "posZ"),
    ("ks-e", "@lk-kiosk", (34, -79), (41, -74), "posZ"),
]

TREES = [
    # the plaza's two planting strips
    (-42, -70, 8), (-36, -70, 7), (-30, -70, 9),
    (36, -70, 7), (42, -70, 9),
    # the street behind the station
    (-44, -85, 8), (44, -85, 8), (-20, -84, 7), (20, -84, 7),
    # and the two strips along the cutting, the only cover on the frontline
    (-41, -29, 9), (-33, -29, 7), (-24, -29, 8), (-16, -29, 7),
    (16, -29, 7), (24, -29, 8), (33, -29, 7), (41, -29, 9),
]

DRESSING = {"props": [
    {"id": h, "kind": "house", "seed": 20 + i, "front": front, "style": style,
     "wings": [{"corners": [list(lo), list(hi)]}]}
    for i, (h, style, lo, hi, front) in enumerate(HOUSES)
] + [
    {"id": f"t{i}", "kind": "tree", "seed": 300 + i, "x": x, "z": z,
     "form": "template", "species": "oak", "height": h}
    for i, (x, z, h) in enumerate(TREES)
] + [
    {"id": "fl-garden-w", "kind": "flora", "seed": 71,
     "points": [[-44, -64], [-26, -64], [-26, -36], [-44, -36]],
     "spec": {"coverage": 0.4, "scale": 8, "octaves": 2, "fernShare": 0.15,
              "flowerShare": 0.08, "flowerScale": 11, "tallShare": 0.25}},
    {"id": "fl-garden-e", "kind": "flora", "seed": 72,
     "points": [[26, -64], [44, -64], [44, -36], [26, -36]],
     "spec": {"coverage": 0.4, "scale": 8, "octaves": 2, "fernShare": 0.15,
              "flowerShare": 0.08, "flowerScale": 11, "tallShare": 0.25}},
    {"id": "fl-plaza", "kind": "flora", "seed": 73,
     "points": [[-44, -73], [-28, -73], [-28, -68], [-44, -68]],
     "spec": {"coverage": 0.5, "scale": 7, "octaves": 2, "fernShare": 0.1,
              "flowerShare": 0.12, "flowerScale": 9, "tallShare": 0.3}},
    {"id": "fl-cutting-w", "kind": "flora", "seed": 74,
     "points": [[-44, -32], [-14, -32], [-14, -26], [-44, -26]],
     "spec": {"coverage": 0.45, "scale": 7, "octaves": 2, "fernShare": 0.1,
              "flowerShare": 0.1, "flowerScale": 9, "tallShare": 0.3}},
    {"id": "fl-cutting-e", "kind": "flora", "seed": 75,
     "points": [[14, -32], [44, -32], [44, -26], [14, -26]],
     "spec": {"coverage": 0.45, "scale": 7, "octaves": 2, "fernShare": 0.1,
              "flowerShare": 0.1, "flowerScale": 9, "tallShare": 0.3}},
]}


def build():
    add_layers, table = sculpted()
    finish = {
        "authors": ["Opus 5"],
        "created": CREATED,
        "themes": THEMES,
        "mapTheme": "city",
        # Two surfaces, so the compile emits two polygons and the height is the key that tells them
        # apart. Everything else on the board is paint scoped to an authored shape.
        "themeByHeight": {str(CITY): "city", str(TERRACE): "garden"},
        "addShapes": SHAPES,
        "addLayers": [LID_LAYER] + add_layers,
        "roomStyles": {"spawn": "@lk-spawn"},
        "dressing": DRESSING,
    }
    return finish, table


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "specs", SLUG)
    os.makedirs(out, exist_ok=True)
    finish, table = build()
    with open(os.path.join(out, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(PLAN, handle, indent=1)
    with open(os.path.join(out, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    print(f"{len(SHAPES)} ground shapes, {len(finish['addLayers'])} layers, "
          f"{len(DRESSING['props'])} props, {len(THEMES)} themes")
    for name, row in table:
        print(f"  {name:<24} {row['blocks']:>6} blocks  {row['layers']:>3} layers  "
              f"{row['shapes']:>5} shapes")
    print("wrote", out)
