#!/usr/bin/env python3
"""Whitegape — a limestone gorge quarried from both rims.

Writes opus5-whitegape.plan.json and opus5-whitegape.finish.json for tools/drive.py.

The board in one sentence: two teams face each other across a chasm; each holds a stone-built quarry
yard on its own rim, with its monument on the floor of the pit cut into that yard, and the only way
over is a bridge the attackers build.

The board is deliberately two kinds of place. The BACK HALF (z -100..-64) is grown ground: open
limestone fell, rolling, pinned in three places and left to the solver everywhere else. The FRONT
HALF (z -64..-12) is made ground: one level stone yard with the pit sunk into it, a loading dock cut
five courses lower at the lip, a kiln on the dock and a works shed on the yard. The boundary between
them is a retaining face with two flights let into it — a line a player crosses and can see.

Everything here is measured in blocks unless the name says cells. The authored unit is team A, on
negative z; rot_180 fans it (image of (x, z) is (-x-1, -z-1)).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from sculpt import props as P  # noqa: E402

SLUG = "opus5-whitegape"
CELL = 4

# ── the five numbers ──────────────────────────────────────────────────────────────────────────────
# lane 176 blocks spawn to spawn; goal 42 along it from its own spawn; 56 wide before the coast is
# cut; a 24-block void gap. Solved against GO1 (3-4), GO3 (>=85), GO4 (>=40).
GOAL_XZ = (-9, -50)
BASE = 24                     # globals.surface
SHELF = 25                    # the spawn shelf: one step over the moor, which is what SP8 allows
GATEBANK = 21                 # the fell where it meets the works — the foot of the retaining face
LIPFELL = 19                  # the fell at the gorge lip, either side of the dock
YARD = 23                     # the made terrace: level, excluded from the relief, faced with courses
DOCK = 18                     # the loading dock, cut five courses below the yard at the lip
PIT_DEPTH = 10                # so the pit floor is YARD - 10 = 13


# ── blocks ────────────────────────────────────────────────────────────────────────────────────────
def solid(b, d=0):
    return {"kind": "solid", "id": b, "data": d}


STONE, ANDESITE, DIORITE = solid(1), solid(1, 5), solid(1, 3)
GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
COBBLE, GRAVEL = solid(4), solid(13)
SPRUCE, SPRUCE_LOG = solid(5, 1), solid(17, 1)
BRICK, HARDCLAY, STONEBRICK = solid(45), solid(172), solid(98)


def cell(palette, size, seed, jitter=25, warp=4, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": palette, "rise": rise}


def layered(bands, axis="depth", ending="handOver", beyond=None):
    m = {"kind": "layered", "axis": axis,
         "stack": {"ending": ending,
                   "bands": [{"material": mat, "thickness": t} for mat, t in bands]}}
    if beyond is not None:
        m["beyond"] = beyond
    return m


# The board's rock, stated once. Every cut on the map — the gorge walls, the quarry faces, the bank
# behind the yard — is the same beds in the same order, which is what makes them read as one
# limestone rather than as three separate decisions.
BEDS = layered([(STONE, 2), (DIORITE, 1), (STONE, 3), (ANDESITE, 1),
                (STONE, 4), (DIORITE, 2)], ending="repeat")
# The body nobody sees until a wall is cut: cells wider than tall, so a cut face reads as blobs
# rather than as vertical runs.
BODY = cell([STONE, ANDESITE, DIORITE], 9, 41, jitter=25, warp=4, rise=5)
# Three blocks a reader cannot quite tell apart, for ground worked and walked on. It carries a rise
# because it is also the whole material of the ramps, and PT4 refuses a fill sampled in the plane.
HARDCORE = cell([GRAVEL, ANDESITE, COBBLE], 7, 47, jitter=30, warp=3, rise=4)
# The yard's flags: a made floor is laid, so it is stone brick and stone rather than quarry gravel.
FLAGS = cell([STONEBRICK, STONE, COBBLE], 9, 51, jitter=20, warp=3, rise=4)

# ── themes ────────────────────────────────────────────────────────────────────────────────────────
FELL = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    # No rim: the gorge lip and the fell's shoulders are ground a relief solved, and a rim caps every
    # fall with a band and turns a hillside into contour lines.
    "rim": {"enabled": False, "depth": 1, "material": COBBLE},
    # The ground is finished by its ANGLE, with the bands cut where GET …/incline said the ground
    # actually lies: meadow to 16 degrees, worn shoulder to 34, bare rock past it.
    "surface": {"enabled": True, "depth": 3, "material": layered([
        (layered([(GRASS, 1), (COARSE, 1), (DIRT, 1)], beyond=STONE), 16),
        (layered([(cell([COARSE, GRAVEL], 9, 43), 1), (DIRT, 2)], beyond=STONE), 18),
        (layered([(cell([STONE, ANDESITE], 11, 45, rise=4), 2), (STONE, 1)], beyond=STONE), 56),
    ], axis="slope", ending="repeat", beyond=STONE)},
    "wall": BEDS,
    "wallEnabled": True,
    "fill": BODY,
}

# The pit: quarry spoil and swept rock, sharing the fell's beds on every face it cuts.
WORKS = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": COBBLE},
    "surface": {"enabled": True, "depth": 2, "material": layered([
        (HARDCORE, 1), (cell([STONE, GRAVEL], 9, 49, rise=3), 1)], beyond=STONE)},
    "wall": BEDS,
    "wallEnabled": True,
    "fill": BODY,
}

# The yard and the dock: made ground, so the floor is laid and the face is coursed rather than
# bedded. `wallRun` stripes along the perimeter, which is the one surface on a board that wants it.
MADE_WALL = {"kind": "wallRun", "runs": [
    {"material": STONEBRICK, "width": 5},
    {"material": STONE, "width": 3},
    {"material": COBBLE, "width": 2}]}

YARD_THEME = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
    "surface": {"enabled": True, "depth": 2, "material": layered([
        (FLAGS, 1), (STONE, 1)], beyond=STONE)},
    "wall": MADE_WALL,
    "wallEnabled": True,
    "fill": cell([STONE, COBBLE], 9, 53, rise=5),
}

DOCK_THEME = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
    "surface": {"enabled": True, "depth": 2, "material": layered([
        (HARDCORE, 1), (STONE, 1)], beyond=STONE)},
    "wall": MADE_WALL,
    "wallEnabled": True,
    "fill": cell([COBBLE, STONE], 9, 55, rise=5),
}

# The kiln. Brick, because a lime kiln is brick-lined and because nothing else on the board is —
# it is the one thing read from the far rim, and it may not be the ground it stands on.
KILN_BRICK = cell([BRICK, HARDCLAY, BRICK], 6, 57, jitter=20, warp=2, rise=4)
KILN = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": BRICK},
    "surface": {"enabled": True, "depth": 2, "material": KILN_BRICK},
    "wall": KILN_BRICK,
    "wallEnabled": True,
    "fill": KILN_BRICK,
}

THEMES = {"fell": FELL, "works": WORKS, "yard": YARD_THEME, "dock": DOCK_THEME, "kiln": KILN}

# ── the plan ──────────────────────────────────────────────────────────────────────────────────────
# Four pieces and no more. The plan states the arrangement — the ground and the room the spawn stands
# in — and every landform below is relief or an authored shape. PL4 refuses two pieces that overlap
# at different surfaces, so the fell is tiled AROUND the spawn rather than drawn under it.
SPAWN_PIECE = [-5, -25, 4, 4]        # cells: blocks x -20..-5, z -100..-85
BUILD_ZONE = [-7, -6, 14, 12]        # cells: blocks x -28..27, z -24..23 — over the whole chasm

plan = {
    "plan": 2,
    "meta": {"name": "Whitegape"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                "surface": BASE, "observerY": 52},
    "pieces": [
        {"id": "fell", "role": "piece", "rect": [-7, -21, 14, 18], "surface": BASE},
        {"id": "fell-w", "role": "piece", "rect": [-7, -25, 2, 4], "surface": BASE},
        {"id": "fell-e", "role": "piece", "rect": [-1, -25, 8, 4], "surface": BASE},
        {"id": "head", "role": "spawn", "rect": SPAWN_PIECE, "surface": SHELF},
    ],
    "zones": [{"id": "chasm", "rect": BUILD_ZONE, "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "head", "at": [8, 8], "facing": "back",
                    "footprint": [2, 2, 12, 12]}],
        "wools": [], "iron": [], "cores": [],
        "destroyables": [{"id": "destroyable-1", "piece": "", "at": list(GOAL_XZ),
                          "style": "pillar-3", "materials": "obsidian", "float": 4,
                          "name": "The Whitegape Pillar"}],
    },
    "walls": [], "boxes": [],
}

# ── the coast ─────────────────────────────────────────────────────────────────────────────────────
# The compiler emits the plan's rectangles, which is the board's shape and not its coast. `fell-24`
# comes back as eight vertices:
#   0 (-28,-100)  1 (-20,-100)  2 (-20,-84)  3 (-4,-84)  4 (-4,-100)
#   5 (28,-100)   6 (28,-12)    7 (-28,-12)
# Edges 5->6 (east flank), 6->7 (the gorge lip) and 7->0 (west flank) are the three long runs, and
# they are where the board reads as a rectangle. A vertex move states one place; the bend roughens
# the rest. The ops run in DESCENDING index, because an insert shifts every index after it.
#
# The lip is cut only OUTSIDE the dock's own span (x -14..13): a made edge is straight and a grown
# one is not, and that difference is the point of the two halves.
EDITS = []


def move(index, x, z):
    EDITS.append({"index": index, "x": x, "z": z})


def insert_run(after, points):
    """Points in the order they should read along the edge. Each insert lands immediately after the
    same index, so the list is replayed in reverse for the run to come out forwards."""
    for x, z in reversed(points):
        EDITS.append({"after": after, "x": x, "z": z})


# west flank, read north from the lip to the back corner
insert_run(7, [(-30, -34), (-26, -54), (-30, -74), (-25, -90)])
move(7, -24, -16)                                    # the west lip pulls back: a bay
# the lip, read west from the east corner — flank only, the dock's own edge left straight
insert_run(6, [(23, -16), (17, -9), (15, -13),
               (-16, -13), (-19, -18), (-24, -13)])
move(5, 22, -98)                                     # the back-east corner cut off
# east flank, read south from the back corner to the lip
insert_run(5, [(30, -84), (26, -64), (31, -46), (25, -28)])
move(0, -24, -98)                                    # the back-west corner cut off

# `side: out` only bloats, so nothing the coast does can leave the yard or the dock hanging over
# void, and the strait it narrows stays well inside CT12's 15-40.
BENDS = {"fell-24": {"wander": 2.5, "step": 11, "seed": 23, "side": "out"}}

# ── relief: the grown half ────────────────────────────────────────────────────────────────────────
# Four marks and two pushes, and all of them in the back and along the lip. The front of the board is
# made ground and takes no part in the solve at all, which is what keeps the relief from piling up in
# one place: it has half a board to spread over and marks at both ends to do it between.
MARKS = [
    {"id": "shelf", "kind": "area", "h": SHELF, "bevel": 3, "ring": [
        [-27, -100], [-27, -88], [-22, -80], [-12, -78], [-2, -83], [-1, -96], [-3, -100]]},
    # The bank the works are cut against: the foot of the retaining face, so the flights have a
    # definite height to arrive at.
    {"id": "gatebank", "kind": "area", "h": GATEBANK, "bevel": 4, "ring": [
        [-28, -74], [-14, -78], [2, -76], [16, -78], [28, -72],
        [28, -62], [12, -66], [-4, -68], [-20, -64], [-28, -66]]},
    # The lip either side of the dock. The gorge edge wants one height, or the cliff reads as a
    # ragged accident rather than as a rim.
    {"id": "liprim", "kind": "area", "h": LIPFELL, "bevel": 3, "ring": [
        [-28, -26], [-16, -29], [0, -26], [16, -29], [28, -24],
        [28, -12], [0, -16], [-28, -12]]},
    # The cart road down off the fell to the works gate.
    {"id": "cartway", "kind": "line", "r": 6, "tread": 3,
     "points": [[-13, -84], [-18, -76], [-19, -68]], "h": [SHELF, 23, GATEBANK]},
]

PUSHES = [
    # The knott, on the east fell: the one landform nobody made. amount/falloff 5/14 outside is 20
    # degrees against crown/half 4/8 inside at 27 — a hillside a player walks up, not a wall with a
    # hill on top of it. Its first draft was 8/9 against 8/8, which is 42, and the boulders said so.
    {"id": "knott", "seed": 11, "roughness": 3, "falloff": 14, "crown": 4,
     "amounts": [3, 4, 5, 5, 4, 3, 4], "ring": [
         [17, -92], [25, -89], [27, -78], [26, -68], [21, -62], [16, -70], [15, -84]]},
    # The slack: a damp hollow on the west fell the cart road skirts, so the two flanks of the grown
    # half are not one gradient.
    {"id": "slack", "seed": 19, "roughness": 2, "falloff": 10, "crown": -3,
     "amount": -5, "ring": [[-27, -78], [-20, -74], [-16, -82], [-23, -88]]},
]

RELIEF = {"*": {"base": 22, "reach": 0, "step": 1,
                "grain": {"amplitude": 1.2, "scale": 16, "seed": 7},
                "marks": MARKS, "pushes": PUSHES}}

# ── the made half ─────────────────────────────────────────────────────────────────────────────────
ADD = []


def made(shape):
    ADD.append(shape)
    return shape


def flight(fid, verts, tops, material=None, theme=None):
    """A flight is one polygon with a height per vertex, `level` so it keeps its stated top and
    `skirt: 0` so its sides are sheer. The run is at least twice the rise on every one of them,
    which is what separates a stair from a wall."""
    s = {"id": fid, "type": "polygon", "operation": "add", "keepClear": True,
         "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
         "floor": 0, "base_height": max(tops) + 1, "vertices": verts,
         "anchor_heights": [t + 1 for t in tops]}
    if theme:
        s["theme"] = theme
    else:
        s["material"] = material
    return made(s)


# THE YARD. One level terrace, excluded from the solve so it meets the fell at a face rather than
# being graded into it. Its outline is not a rectangle and not a straight line anywhere: it pushes
# out to the board's east coast where the works shed stands, cuts back on the west, and carries two
# re-entrants on its front edge, each sized to exactly the flight that fills it.
# Three notches are cut out of its front edge, each sized to exactly the thing that fills it: the
# east stair, the tramway's slot down into the pit, and the west stair. A shape drawn INTO the yard
# would lose every column to it, because the taller add wins and the yard is five courses higher.
YARD_RING = [
    [-22, -40], [-21, -56], [-14, -64], [-2, -66], [8, -62], [17, -58], [27, -56],
    [27, -38], [20, -32], [20, -30], [13, -26],
    [13, -36], [6, -36], [5, -26],
    [-6, -26], [-6, -42], [-13, -42], [-13, -26],
    [-14, -26], [-14, -36], [-20, -36], [-21, -26], [-22, -30],
]
made({"id": "yard", "type": "polygon", "operation": "add", "theme": "yard",
      "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
      "floor": 0, "base_height": YARD + 1, "vertices": YARD_RING})

# THE DOCK. Cut five courses below the yard at the lip, so whatever lands on it is below the
# defence and the yard looks down into it. Its front edge is straight, because it is a made edge.
made({"id": "dock", "type": "polygon", "operation": "add", "theme": "dock",
      "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
      "floor": 0, "base_height": DOCK + 1,
      "vertices": [[-14, -25], [13, -25], [13, -13], [-14, -13]]})

# THE PIT, sunk into the yard. A sink cuts sheer and leaves a flat floor; nested area marks would
# have built a funnel.
PIT_RING = [[-19, -52], [-17, -59], [-6, -61], [2, -55],
            [2, -45], [-3, -39], [-14, -40], [-18, -46]]
made({"id": "pit", "type": "polygon", "operation": "add", "theme": "works",
      "height_mode": "sink", "skirt": 1, "floor": 0, "base_height": PIT_DEPTH,
      "anchor_heights": [PIT_DEPTH] * len(PIT_RING), "vertices": PIT_RING})

# Two flights off the fell up onto the yard — the retaining face is what the works are cut against,
# and these are the chosen ways through it. Ten of run for two of rise.
flight("gate-w", [[-20, -70], [-14, -70], [-14, -60], [-20, -60]],
       [GATEBANK, GATEBANK, YARD, YARD], theme="yard")
flight("gate-e", [[8, -70], [14, -70], [14, -60], [8, -60]],
       [GATEBANK, GATEBANK, YARD, YARD], theme="yard")

# Two flights down off the yard into the dock, each filling one re-entrant of the yard's front edge.
flight("stair-w", [[-20, -36], [-14, -36], [-14, -26], [-20, -26]],
       [YARD, YARD, DOCK, DOCK], theme="yard")
flight("stair-e", [[6, -36], [13, -36], [13, -26], [6, -26]],
       [YARD, YARD, DOCK, DOCK], theme="yard")

# The haul ramp: the defenders' way down into the pit, off the yard's east side. Ten courses over 24
# blocks of run.
flight("haul-ramp", [[14, -30], [19, -35], [4, -49], [-1, -44]],
       [YARD, YARD, YARD - PIT_DEPTH, YARD - PIT_DEPTH], material=HARDCORE)
# The tramway cutting: a slot driven through the yard from the dock straight into the pit, five
# courses over fourteen. It is the attackers' way in, and the yard stands five courses over it on
# both sides, which is the whole of what makes it a defended place rather than a corridor.
flight("tramway", [[-13, -25], [-6, -25], [-6, -42], [-13, -42]],
       [DOCK, DOCK, YARD - PIT_DEPTH, YARD - PIT_DEPTH], material=HARDCORE)
# The charging ramp: off the yard up to the kiln's rim, three courses over seven, so a barrow of
# limestone goes from the quarry floor up the haul ramp, across the yard and straight into the top
# of the kiln. It is the reason the kiln stands where it does.
flight("charge-ramp", [[-3, -34], [1, -34], [1, -25], [-3, -25]],
       [YARD, YARD, DOCK + 8, DOCK + 8], material=HARDCORE)

MASONRY = cell([STONEBRICK, STONE, COBBLE], 4, 63, jitter=20, warp=2, rise=3)

# THE REVETMENT. The retaining wall along the yard's back edge — the line between the grown half and
# the made one, and the one thing on the board a player can see that boundary as. It is in three
# runs: both ends die into the board's own coast, and the two gaps in it are exactly the two gate
# flights, so it has ends, it has gates, and it has the fell on one side and the works on the other.
for pid, pts in (("revet-w", [[-23, -42], [-21, -52], [-21, -60]]),
                 ("revet-m", [[-13, -63], [-2, -65], [7, -61]]),
                 ("revet-e", [[15, -59], [22, -57], [28, -55]])):
    made({"id": pid, "type": "polyline", "operation": "add", "keepClear": True,
          "stroke_edge": "solid", "radius": 1.5, "material": MASONRY,
          "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
          "floor": 0, "base_height": YARD + 4, "vertices": pts})

# The dock's parapet, three blocks in from the void so there is a loading walk outside it. Split, so
# the middle is open to the chasm — which is where a bridge wants to leave from.
for pid, pts in (("kerb-w", [[-13, -16], [-10, -17], [-8, -16]]),
                 ("kerb-e", [[6, -16], [9, -17], [12, -16]])):
    made({"id": pid, "type": "polyline", "operation": "add", "keepClear": True,
          "stroke_edge": "solid", "radius": 1.2, "material": STONEBRICK,
          "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
          "floor": 0, "base_height": DOCK + 3, "vertices": pts})

# ── the kiln ──────────────────────────────────────────────────────────────────────────────────────
# THE LIME KILN, built rather than emitted. A bank kiln is a stone base with a draw arch at the low
# level, a tapering stack over it, and a charging mouth reached from the high ground behind — every
# one of those is a rectangle on a made layer, and the arch is drawn as the masonry AROUND the
# opening rather than cut out of it, because SK13 reads a subtract as the board's negative space and
# refuses any add that fills it.
#
# It stands on the dock (surface y18) with its back against the yard (y23), which is the whole point
# of a bank kiln: you draw burnt lime out of the arch at the bottom and tip limestone into the top
# from the bank behind. Layer base_y is DOCK + 1, so a shape's floor f tops out at y = 19 + f.
# A layer holds ONE span per column (SK9), so the base and the stack are two layers rather than two
# heights on one. A rectangle is [min, max), so every piece here has max > min or it draws no ground
# (SK4), and no two pieces of one layer share a column.
def kiln_layer(lid, base_y, pieces):
    b = P.LayerBuilder(lid, name="The lime kiln", base_y=base_y, mirrors=True, tag=lid)
    for x0, z0, x1, z1, floor, height in pieces:
        b.rect(x0, z0, x1, z1, floor, height, "kiln")
    d = b.done()
    return {"id": d["id"], "name": d["name"], "base_y": d["base_y"], "kind": "made",
            "part_of": "kiln", "shapes": d["layout"]["shapes"], "groups": d["layout"]["groups"]}


LAYERS = [
    # The base, five courses, drawn in four pieces AROUND a draw arch four wide and three high that
    # opens toward the chasm — the masonry is the complement of the opening rather than a subtract
    # out of it, because SK13 reads a subtract as the board's negative space.
    kiln_layer("kiln-base", DOCK + 1, [
        (-5, -24, -2, -17, 0, 5),      # west cheek
        (2, -24, 5, -17, 0, 5),        # east cheek
        (-2, -24, 2, -21, 0, 5),       # the back, behind the draw hole
        (-2, -21, 2, -17, 3, 2),       # the lintel over the arch
    ]),
    # The stack: a hollow shell stepped in one block all round, so the kiln tapers, with the shaft
    # open from the charging mouth at its rim down onto the burning floor.
    kiln_layer("kiln-stack", DOCK + 6, [
        (-4, -23, 4, -22, 0, 3),
        (-4, -19, 4, -18, 0, 3),
        (-4, -22, -3, -19, 0, 3),
        (3, -22, 4, -19, 0, 3),
    ]),
]

# ── buildings ─────────────────────────────────────────────────────────────────────────────────────
SHELL = json.load(open(os.path.join(ROOT, "tools", "styles", "showcase-hall.json")))


def stack(bands, extent):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]},
            "extent": extent}


LAID_SPRUCE = {"kind": "laidLog", "id": 17, "data": 1}
# One built family: spruce over a brick plinth, spruce posts, spruce roof. Neither is the pale
# limestone under its feet, and the brick is the accent the kiln already wears.
SHELL["foundation"]["plate"] = stack([(BRICK, 1)], 1)
SHELL["foundation"]["footing"] = None
SHELL["post"] = SPRUCE_LOG
SHELL["wall"] = stack([(BRICK, 1), (SPRUCE, 4)], 5)
SHELL["roof"].update({"form": "gable", "pitch": 1, "slab": 126, "slabData": 1, "overhang": 1,
                      "ridgeCap": True, "body": SPRUCE, "verge": LAID_SPRUCE, "gable": SPRUCE})
SHELL["beams"] = {"block": 17, "data": 1, "reach": 1, "any": False}
# A storey carries clear + 1 courses of wall, so each stack is sized to its own storey or the rest
# is truncated in silence.
SHELL["storeys"][0].update({
    "clear": 5, "post": SPRUCE_LOG,
    "wall": stack([(BRICK, 2), (SPRUCE, 3), (LAID_SPRUCE, 1)], 5)})
SHELL["storeys"][1].update({
    "clear": 4, "post": SPRUCE_LOG,
    "wall": stack([(SPRUCE, 4), (LAID_SPRUCE, 1)], 4)})

WORKS_SHELL = json.loads(json.dumps(SHELL))

# ── dressing ──────────────────────────────────────────────────────────────────────────────────────
BODIES = json.load(open(os.path.join(ROOT, "specs", "fable-millrace-revamp", "trees.json")))
SCRUB = ["fir-small-1", "fir-small-2", "fir-small-3", "fir-small-4", "fir-small-5"]
SHELTER = ["oak-dense-1", "oak-dense-4"]

styles = {k: {"kind": "tree", "form": "copied", "body": BODIES[k]["body"]}
          for k in SCRUB + SHELTER}
styles["limestone"] = {"kind": "boulder", "form": "angular", "size": 6, "mossy": False,
                       "rock": {"kind": "noise", "seed": 71, "scale": 3, "octaves": 3, "rise": 2,
                                "stops": [STONE, COBBLE, ANDESITE, STONE]}}
styles["clint"] = {"kind": "boulder", "form": "outcrop", "size": 7, "mossy": False,
                   "rock": {"kind": "noise", "seed": 73, "scale": 3, "octaves": 3, "rise": 2,
                            "stops": [STONE, ANDESITE, COBBLE]}}
styles["works-shed"] = {"kind": "house", "shell": WORKS_SHELL}

props = []


def tree(pid, x, z, style):
    props.append({"id": pid, "kind": "tree", "seed": abs(x * 31 + z * 17) % 9973,
                  "x": x, "z": z, "style": style})


def boulder(pid, x, z, style):
    props.append({"id": pid, "kind": "boulder", "seed": abs(x * 11 + z * 5) % 9973,
                  "x": x, "z": z, "style": style})


def road(pid, pts, radius, seed):
    props.append({"id": pid, "kind": "stroke", "claimsGround": True, "radius": radius,
                  "seed": seed, "style": "solid", "points": pts, "pave": HARDCORE})


def house(pid, wings, seed, front):
    props.append({"id": pid, "kind": "house", "seed": seed, "front": front,
                  "wings": wings, "style": "works-shed"})


# Two ways, each of them somewhere a load or a man actually went.
road("cart-road", [[-14, -88], [-18, -78], [-19, -70]], 3, 81)      # spawn to the works gate
road("fell-path", [[8, -88], [11, -78], [11, -70]], 2, 85)          # the east fell to the east gate

# THE WORKS SHED. One building on one outline: a two-storey hall with a single-storey range built
# against it, which is what the wing model is for. 8x14 + 7x8 = 168 blocks, inside HP3's 192. The
# hall's ridge runs ALONG the shared edge and the range's runs INTO it, which is what keeps HJ3 and
# HJ4 off a pair meeting on a vertical seam.
# Both buildings stand where `POST …/sketch/seats` said a footprint of their size may stand, asked
# of a board with no props on it at all. A 15x14 bounding box seats in exactly one place on this
# half — minimum corner x 2..5, z -58..-52 — and that is where the shed is.
SEAT_PASS = os.environ.get("WHITEGAPE_SEATS") == "1"
if not SEAT_PASS:
    house("works-shed",
          [{"corners": [[3, -56], [10, -43]], "spec": {"storeysHigh": 2, "ridge": "alongZ"}},
           {"corners": [[11, -56], [17, -49]], "spec": {"storeysHigh": 1, "ridge": "alongX"}}],
          601, "negX")

# The powder house: a magazine stands apart from the works by rule, which is why it is out on the
# grown half on its own with nothing near it.
    house("powder-house", [{"corners": [[-4, -80], [3, -73]], "spec": {"storeysHigh": 1}}],
          607, "posZ")

# Erratics on the open fell. Each one is checked with a `column` read for what it stands ON: a stone
# boulder on stone reads as nothing, and no rule in the studio says so.
for i, (x, z, st) in enumerate([] if SEAT_PASS else
                               # Each of these four was `column`-read first: a stone boulder on
                               # (18,-70) andesite, (2,-66) stone or (20,-58) gravel reads as
                               # nothing, and no rule in the studio says so. These stand on grass
                               # and on coarse dirt.
                               [(6, -80, "clint"), (16, -92, "limestone"),
                                (22, -72, "limestone"), (-22, -62, "clint")]):
    boulder(f"erratic-{i}", x, z, st)

# Scrub where sheep cannot reach it — the fell's steeper shoulders and the gorge lip — and a planted
# shelter belt behind the spawn. Nothing in the pit and nothing on the yard: a working floor is
# swept, and OB19 keeps ten blocks round the goal clear anyway.
for i, (x, z, st) in enumerate([] if SEAT_PASS else [
        # The gorge lip, both flanks: thorn grows on a crag edge because nothing grazes it there.
        (-27, -28, SCRUB[0]), (-24, -22, SCRUB[1]), (-26, -36, SCRUB[2]),
        (-27, -50, SCRUB[3]), (-25, -44, SCRUB[4]),
        (21, -20, SCRUB[0]), (16, -26, SCRUB[1]), (23, -28, SCRUB[2]), (24, -34, SCRUB[3]),
        # The knott's shoulders and the ground behind the works.
        (14, -62, SCRUB[4]), (4, -66, SCRUB[0]), (6, -74, SCRUB[2]),
        # A planted shelter belt behind the spawn — the only trees on the board somebody chose.
        (2, -96, SHELTER[0]), (10, -98, SCRUB[1]), (2, -86, SCRUB[3])]):
    tree(f"thorn-{i}", x, z, st)

# Ground cover over the whole half, not a patch of it — the density field is better at patchiness
# than a hand-drawn polygon. Both gameplay numbers stay low: tall grass is cover nobody authored.
props.append({"id": "fell-cover", "kind": "flora",
              "points": [[-30, -100], [30, -100], [30, -14], [-30, -14]],
              "spec": {"coverage": 0.28, "scale": 18, "octaves": 3, "fernShare": 0.25,
                       "flowerShare": 0.04, "flowerScale": 11, "tallShare": 0.12}})

# ── the finish ────────────────────────────────────────────────────────────────────────────────────
finish = {
    "created": "2026-09-19",
    "authors": ["Opus 5"],
    "themes": THEMES,
    "mapTheme": "fell",
    # Extreme hills tints grass #8ab689 — the pale grey-green a limestone fell has, against the
    # #91bd59 Plains would paint on the same blocks.
    "biome": {"kind": "solid", "id": 3},
    "relief": RELIEF,
    "editShapes": {"fell-24": EDITS},
    "bendShapes": BENDS,
    "addShapes": ADD,
    "addLayers": LAYERS,
    "roomStyles": {"spawn": SHELL},
    "dressing": {"styles": styles, "props": props},
}

for name, doc in ((f"{SLUG}.plan.json", plan), (f"{SLUG}.finish.json", finish)):
    with open(os.path.join(HERE, name), "w") as fh:
        json.dump(doc, fh, indent=1)
    print(f"wrote {name}  ({os.path.getsize(os.path.join(HERE, name)):,} bytes)")
