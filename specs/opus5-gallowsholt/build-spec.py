#!/usr/bin/env python3
"""Gallowsholt — the plan and the finish.

Adapted from a composed board:
    GET /api/compose?players=20&symmetry=rot_180  seed 0
    composerVersion markers-in-blocks-1, cell 5, score 0.302
    structure: hub ring · frontline twin · wools i, i

The composer's arrangement is kept — the ring hub with its hole, the twin frontline, the
proportions. Three things are not: the mid, which arrives as twenty blocks of flush build zone and
leaves as a flagged causey island with a crossing either side of it; the two wools, which arrive
138 and 94 blocks from the spawn that has to attack them and are re-hung off the hub's two back
shoulders; and the spawn, which arrives on the hub's west flank and moves to its back so that a team
stands between its wools rather than behind both of them.

The one idea: a limestone moor whose only made ground is the causey in the middle of the crossing
and the walled garths the wools sit in, and everything between is grown.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-gallowsholt"

MOOR, CAUSEY = 11, 15          # the two plan surfaces; a top block is surface - 1
GARTH = 15                     # the made ground, stated downstream as excluded shapes

# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
# Cell rects, [x, z, w, h], x/z the min corner, origin at the symmetry centre. The composed unit is
# shifted +2 cells of z so the mid gap is 40 blocks rather than 20 — an island with a 15-block
# crossing on each side needs the room, and 20 blocks is one bridge with nothing in it.
plan = {
    "plan": 2,
    "meta": {"name": "Gallowsholt"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 20, "surface": MOOR,
                "observerY": 40},
    "pieces": [
        # the ring, as composed: a back bar, a front bar, two arms and a four-cell hole between them
        {"id": "hub-back",  "role": "piece", "rect": [-3, 13, 8, 2]},
        {"id": "hub-front", "role": "piece", "rect": [-3, 9, 8, 2]},
        {"id": "hub-west",  "role": "piece", "rect": [-3, 11, 4, 2]},
        {"id": "hub-east",  "role": "piece", "rect": [3, 11, 2, 2]},
        # the frontline, composed as two 10-block tips; FR9 reads 10 blocks as a funnel rather than
        # somewhere to fight, so each tip is widened to 15 and the bar behind them with it
        {"id": "front-bar", "role": "piece", "rect": [-4, 6, 9, 3]},
        {"id": "front-w",   "role": "piece", "rect": [-4, 4, 3, 2]},
        {"id": "front-e",   "role": "piece", "rect": [1, 4, 3, 2]},
        # the spawn, re-hung off the hub's BACK rather than its west flank
        {"id": "spawn-t1",   "role": "piece", "rect": [-2, 15, 2, 2]},
        {"id": "spawn-room", "role": "spawn", "rect": [-2, 17, 2, 3]},
        # the two wools at the hub's two back shoulders, at one depth, so neither is the raid and
        # neither the walk-in. Each is an approach piece and a room and nothing else: the ground that
        # rings the room — a stamped room fills its piece and fills DOWNWARD in bedrock, so a cell of
        # void beside one is a plinth — is the garth, stated downstream as a shape.
        {"id": "wool-a-t1",   "role": "piece",     "rect": [3, 15, 2, 2]},
        {"id": "wool-a-room", "role": "wool-room", "rect": [5, 15, 2, 2]},
        {"id": "wool-b-t1",   "role": "piece",     "rect": [-9, 13, 6, 2]},
        {"id": "wool-b-room", "role": "wool-room", "rect": [-9, 15, 2, 2]},
        # THE MID THE COMPOSER DOES NOT PLACE. A piece seated in the mid band, centred on the origin
        # and therefore its own rot_180 image, so it is stated once and mirrors: False keeps it from
        # being doubled onto itself. Its surface is four blocks over the moor, which is what makes
        # it a thing to take rather than a floor to walk over.
        {"id": "causey", "role": "piece", "rect": [-3, -1, 6, 2], "surface": CAUSEY,
         "mirrors": False},
    ],
    # two zones rather than one, which BZ11 allows for exactly this reason: one flush crossing per
    # side of the island. Each is 15 blocks of void — G5's hop — and the island is the thing between.
    "zones": [
        {"id": "crossing-s", "rect": [-4, 1, 8, 3], "holes": []},
        {"id": "crossing-n", "rect": [-4, -4, 8, 3], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 7], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [],
    "boxes": [],
}


# ── materials ────────────────────────────────────────────────────────────────────────────────────
# Three families, named before a block was chosen. The GROUND is pale — limestone, bleached turf,
# grey gravel. What is BUILT is dark spruce over stone brick, so a wall reads against the hill from
# the far bank. The ACCENT is red brick, and it appears twice: the kiln in each team's garth and the
# marker on the causey.
def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}

GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)
STONEBRICK, SPRUCE, SPRUCE_LOG = solid(98), solid(5, 1), solid(17, 1)
LAID_SPRUCE = {"kind": "laidLog", "id": 17, "data": 1}
GRANITE, DIORITE = solid(1, 1), solid(1, 3)   # the accent: the erratics, and nothing else


def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}


def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}


def layered(bands, axis="depth", ending="handOver"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}


# the body of the hill and the face it cuts: two blocks each, wider than they are tall, so a cut
# reads as bedded rock rather than as vertical stripes
LIMESTONE_BODY = cell_(21, 9, [STONE, ANDESITE, STONE, COBBLE], rise=5)
LIMESTONE_FACE = cell_(22, 7, [STONE, COBBLE, GRAVEL], rise=4)
FLAGS = cell_(23, 5, [COBBLE, STONE, GRAVEL])          # the working floor, three close greys
TRACK = cell_(24, 5, [GRAVEL, ANDESITE, COBBLE])       # the drove road, hard ground

# The moor finished by its ANGLE. A thickness on the slope axis is a span of degrees, so one stack
# finishes the flat, the shoulder and the face of the same hill — which is the only thing that tells
# a 45-degree hillside from a meadow. The cuts are read off GET …/incline over the built board rather
# than guessed: 43% of this ground stands under ten degrees, 34% between ten and thirty and 23% over
# thirty, and the fell's own two gradients are 0.55 and 0.67 a block, which is 29 and 34 degrees. A cut
# at 24 therefore put the whole hillside on the shoulder band and the board came out grey; at 32 and 44
# the fell is turf, the brow is worn and only the cut faces are rock.
MOOR_SURFACE = layered([
    (32, layered([(1, GRASS), (2, DIRT), (1, COARSE)])),      # the turf
    (12, layered([(1, COARSE), (1, GRAVEL), (2, DIRT)])),     # the worn shoulder the sheep keep bare
    (46, LIMESTONE_FACE),                                     # the rock itself
], axis="slope")

# the strata: one stack on the WALL bucket, read down from the top of every face on the board, so
# every cut shows the same rock in the same order
STRATA = layered([(2, STONE), (1, GRAVEL), (3, STONE), (1, ANDESITE), (2, COBBLE)])

themes = {
    "moor": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": LIMESTONE_FACE},
        "surface": {"enabled": True, "depth": 4, "material": MOOR_SURFACE},
        "wall": STRATA, "wallEnabled": True,
        "fill": LIMESTONE_BODY,
    },
    # the works: the quarried apron at the crossing and the two garth floors at the back. One theme
    # for both, because they are the same thing — the few square yards of this hill somebody flagged.
    "works": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
        "surface": {"enabled": True, "depth": 2, "material": FLAGS},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": STONEBRICK, "width": 2},
            {"material": COBBLE, "width": 3},
            {"material": ANDESITE, "width": 2},
            {"material": COBBLE, "width": 4},
        ]},
        "fill": LIMESTONE_BODY,
    },
    # the causey: the island in the middle, and the one ground on the board neither team made
    "causey": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
        "surface": {"enabled": True, "depth": 2,
                    "material": cell_(25, 6, [STONEBRICK, ANDESITE, COBBLE])},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": STONEBRICK, "width": 3},
            {"material": ANDESITE, "width": 2},
        ]},
        "fill": LIMESTONE_BODY,
    },
}

STEP = cell_(26, 4, [STONEBRICK, COBBLE, ANDESITE], rise=2)      # every stair on the board, one stone
DYKE = cell_(27, 4, [COBBLE, STONE, ANDESITE], rise=2)           # every drystone wall, one stone

# ── the shapes the plan cannot state ─────────────────────────────────────────────────────────────
FELL, APRON = 17, 11        # the shelf the rakes arrive on, and the quarried floor they leave


def pad(id_, ring, height, theme=None, scope="exclude"):
    """Made ground: flat to its own edge and OUT of the relief solve, so the moor bends round it and
    the two grounds meet at a face rather than being graded into each other."""
    shape = {"id": id_, "type": "polygon", "operation": "add", "group": "team",
             "floor": 0, "base_height": height, "height_mode": "level", "skirt": 0,
             "relief_scope": scope,
             "vertices": [[x, z] for x, z in ring],
             "anchor_heights": [height] * len(ring)}
    if theme:
        shape["theme"] = theme
    return shape


def flight(id_, ring, low, high, group="team"):
    """A flight: one polygon, two anchors at the foot and two at the head, at least twice the run as
    rise. It is MADE, so it carries a material rather than a theme, and it is excluded — a relief
    graded across the seam would delete the boundary the flight exists to state."""
    return {"id": id_, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": group, "floor": 0, "base_height": high, "material": STEP,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}


def dyke(id_, points, top, radius=1, group="team"):
    """A drystone wall as a POLYLINE: the rasterizer splines the points before offsetting the band,
    so four clicked points draw as a curve rather than a chain of chords. A polyline states its
    bounds rather than the points a height is stated at, so it takes one base_height and no
    anchor_heights (SK22)."""
    return {"id": id_, "type": "polyline", "operation": "add", "override": True, "keepClear": True,
            "group": group, "floor": 0, "base_height": top, "material": DYKE,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
            "radius": radius, "stroke_edge": "solid",
            "vertices": [[x, z] for x, z in points]}


add_shapes = [
    # THE APRON — the one piece of made ground on the board that decides a fight. The frontline is
    # ground that has to be stood on, so it is cut flat at the moor's own base and taken out of the
    # solve; the fell rises behind it and the two meet at a FACE. Its outline follows the land's own
    # after the vertex edits, inset a couple of blocks, because a shape that hangs over the void
    # builds a plinth of bedrock there and nothing declines it.
    pad("apron", [(-25, 42), (-26, 30), (-21, 22), (-14, 21), (-8, 25), (-6, 36),
                  (6, 36), (8, 25), (14, 21), (21, 22), (26, 28), (27, 42),
                  (10, 45), (-10, 45)], APRON, theme="works"),
    # the two garth floors, flat to their walls, with each wool room's bedrock plinth buried under
    # them. `hold` rather than `exclude`: the moor is solved knowing where it has to arrive, so a
    # gate is a step and not a wall.
    pad("garth-a", [(19, 71), (36, 69), (38, 75), (38, 88), (28, 91), (19, 88)], APRON,
        theme="works", scope="hold"),
    pad("garth-b", [(-47, 73), (-32, 76), (-31, 88), (-40, 90), (-47, 87)], APRON,
        theme="works", scope="hold"),
    # the spawn's own yard, the same
    pad("stell", [(-17, 79), (0, 78), (0, 102), (-17, 102)], APRON, theme="works", scope="hold"),
    # THE RAKES: the two ways up off the apron onto the fell, one either side of the gate. Fourteen
    # blocks of run for six of rise, which is what separates a stair from a wall — and their heads
    # land at the height the push puts the ring's own edge at, so the flight arrives on the ground
    # rather than two courses over it.
    flight("rake-w", [(-20, 34), (-10, 34), (-10, 48), (-20, 48)], APRON, FELL),
    flight("rake-e", [(10, 34), (20, 34), (20, 48), (10, 48)], APRON, FELL),
    # the garth walls: drystone round each enclosure, with the gate left open where the lane comes in
    dyke("dyke-a", [(20, 72), (36, 70), (38, 78), (38, 87)], APRON + 3),
    dyke("dyke-b", [(-46, 74), (-33, 77), (-32, 86), (-39, 89)], APRON + 3),
    # THE CAUSEY. Its own group, which does not mirror, so every shape on it is authored as its own
    # rot_180 image about the origin — the wall is a pair and each half is the other's.
    dyke("causey-wall-n", [(-12, -3), (-4, -5), (5, -4), (13, -2)], 18, group="neutral"),
    dyke("causey-wall-s", [(12, 3), (4, 5), (-5, 4), (-13, 2)], 18, group="neutral"),
]

# ── the relief ───────────────────────────────────────────────────────────────────────────────────
def area(id_, ring, h, **kw):
    return dict(id=id_, kind="area", h=h, ring=[[x, z] for x, z in ring], **kw)


def point(id_, at, r, h, **kw):
    return dict(id=id_, kind="point", at=list(at), r=r, h=h, **kw)


relief = {
    # The moor. NO marks and two pushes: a mark is a constraint honoured exactly and a push is the
    # only thing that builds a landform, and a push is added to the surface the marks solved — which
    # is why a board that states both ends up with the mark's height plus the push's on top of it.
    # The flat this board needs is stated as made ground instead, where it can be walked on.
    "team": {
        "base": 11, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1, "scale": 17, "seed": 5},
        "marks": [],
        "pushes": [
            # THE FELL: the swell the ring hub stands on, and the reason the middle of this board is
            # the high ground. Its two gradients are set to agree — 6 over a falloff of 9 outside the
            # ring is 0.67 a block, and a crown of 6 over a half-width of about 11 is 0.55 inside it
            # — so the landform has no step at its own outline. Its skirt dies at z 78 and x -21,
            # which is what keeps the two garths and the spawn yard on level ground.
            {"id": "fell", "amount": 6, "crown": 6, "falloff": 9, "roughness": 2, "seed": 9,
             "ring": [(-12, 50), (6, 48), (24, 51), (28, 60), (20, 68), (0, 69), (-12, 64)],
             "amounts": [6, 6, 6, 5, 6, 6, 6]},
        ],
    },
    # The causey is its own group and NOTHING on a group that does not mirror is mirrored for it, so
    # the one mark it carries is centred on the origin and is therefore its own image.
    "neutral": {
        "base": 15, "reach": 6, "step": 1, "landform": "plain",
        "grain": {"amplitude": 0, "scale": 8, "seed": 6},
        "marks": [area("flagstones", [(-15, -5), (15, -5), (15, 5), (-15, 5)], 15)],
        "pushes": [],
    },
}

# ── the two halls ────────────────────────────────────────────────────────────────────────────────
def hall(wall_stack, storeys, clear=5):
    return {
        "foundation": {"plate": {"stack": stack([(1, COBBLE)], "repeat"), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       # null by default and that is the answer: over a plate of one course a footing
                       # is a rim of a second material round a building with no foundation to speak of
                       "footing": None},
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False,
                 "body": STONEBRICK, "verge": LAID_SPRUCE, "gable": SPRUCE,
                 "gableWindows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                                  "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3}},
        "wall": {"stack": wall_stack, "extent": 5},
        "post": SPRUCE_LOG,
        "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 2, "height": 2, "spacing": 3},
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 1},
                    "width": 2, "height": 3},
    }


GROUND_STOREY = {
    "clear": 5, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(3, cell_(28, 3, [STONEBRICK, COBBLE])), (2, SPRUCE)], "repeat"),
             "extent": 5},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
}
UPPER_STOREY = {
    "clear": 4, "post": SPRUCE_LOG, "deck": None,
    "wall": {"stack": stack([(3, SPRUCE), (1, LAID_SPRUCE)], "repeat"), "extent": 4},
    "windows": {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 1, "width": 1, "height": 2, "spacing": 4},
}

stell = hall(stack([(1, SPRUCE)], "repeat"), [GROUND_STOREY, UPPER_STOREY])
laithe = hall(stack([(1, SPRUCE)], "repeat"), [dict(GROUND_STOREY, clear=6)])

# ── what stands on the board ─────────────────────────────────────────────────────────────────────
trees = json.load(open(os.path.join(HERE, "trees.json")))
tree_styles = {name: trees[name] for name in ("thorn-1", "thorn-2", "thorn-3", "spar-1", "spar-2")}

props = [
    # the drove road: the spawn door, over the fell by the west rake, down onto the apron. One line,
    # both ends attached, running TO a door rather than through anything.
    {"id": "drove", "kind": "stroke", "seed": 41, "radius": 2, "style": "solid", "coverage": 1.0,
     "claimsGround": True, "pave": TRACK,
     "points": [[-5, 84], [-6, 74], [-12, 62], [-14, 52], [-14, 40], [-12, 26]]},
    # the two garth lanes, each ending at its own gate
    {"id": "lane-to-a", "kind": "stroke", "seed": 42, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": TRACK,
     "points": [[2, 78], [12, 74], [20, 72], [26, 74]]},
    {"id": "lane-to-b", "kind": "stroke", "seed": 43, "radius": 2, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": TRACK,
     "points": [[-10, 80], [-20, 72], [-30, 74], [-38, 78]]},
    # ground cover: ONE shape, the whole board, and the patchiness left to the density field. Both
    # gameplay numbers stay low — tall grass hides a player, and nothing authored that cover.
    {"id": "ling", "kind": "flora", "seed": 44,
     "points": [[-50, 14], [30, 14], [42, 70], [30, 96], [-50, 96]],
     "spec": {"coverage": 0.22, "scale": 26, "octaves": 3, "fernShare": 0.3,
              "flowerShare": 0.06, "flowerScale": 14, "tallShare": 0.05}},
]

# ONE building beside the two stamped rooms, and it stands where POST …/sketch/seats says a 7x5
# footprint may stand rather than where it looked right: a field barn on the fell's own lip, above
# the east rake, which is the one built thing on the high ground both teams cross.
props += [
    {"id": "laithe-a", "kind": "house", "seed": 511, "front": "negZ", "style": "laithe",
     "wings": [{"corners": [[16, 48], [22, 52]], "spec": {"ridge": "alongX", "storeysHigh": 1}}]},
]
# thorns in the lee of the two garth walls and along the wool-b lane, every position read off the
# same seats mask rather than guessed and then declined
for i, (x, z, style) in enumerate([(-23, 26, "thorn-1"), (20, 30, "thorn-2"), (-33, 66, "thorn-3"),
                                   (-3, 57, "spar-1"), (3, 70, "spar-2")]):
    props.append({"id": f"thorn-{i}", "kind": "tree", "seed": 620 + i, "x": x, "z": z,
                  "style": style})
# the erratics: on the flat, because a rock pinned to a 37-degree face reads as neither rock nor
# slope, and the slope is already the feature there
for i, (x, z) in enumerate([(24, 41), (24, 57), (-7, 41), (-17, 92)]):
    props.append({"id": f"clint-{i}", "kind": "boulder", "seed": 660 + i, "x": x, "z": z,
                  "style": "clint"})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-15",
    "themes": themes,
    "mapTheme": "moor",
    "themeById": {"causey-15": "causey"},
    "biome": {"kind": "solid", "id": 3},
    # THE OUTLINE, ONE POINT AT A TIME. The compile hands back one 24-vertex ring for the whole team
    # unit; these are the places one part of it should differ from the others, and every other point
    # is exactly where the plan put it after each of them. A bend cannot do any of this: it moves
    # every cut point at once by a formula.
    #
    # Read down the ring as the compile emitted it:
    #   0 (-45,65)  1 (-15,65)  2 (-15,45)  3 (-20,45)  4 (-20,20)  5 (-5,20)  6 (-5,30)
    #   7 (5,30)    8 (5,20)    9 (20,20)  10 (20,30)  11 (25,30)  12 (25,75)  13 (35,75)
    #  14 (35,85)  15 (15,85)  16 (15,75)  17 (0,75)   18 (0,100)  19 (-10,100) 20 (-10,75)
    #  21 (-35,75) 22 (-35,85) 23 (-45,85)
    # An insert names the edge LEAVING the vertex it states, and every index after it has moved, so
    # the list runs back to front and the run prints where each point landed.
    "editShapes": {
        "front-bar-11": [
            # THE WEST GARTH. The composed room has ground on one side and a bedrock plinth on the
            # other three — a stamped room fills its piece and fills downward in bedrock, so a cell
            # of void beside one is a 25-course cliff. Four points put a garth round it.
            {"after": 23, "x": -50, "z": 74},
            {"index": 23, "x": -42, "z": 93},
            {"index": 22, "x": -31, "z": 91},
            {"index": 21, "x": -29, "z": 77},
            # THE SPAWN YARD. The composed spawn column is exactly its two pieces wide, so the
            # stamped hall's bedrock foundation stands as a 25-course cliff on three sides. Four
            # points give it a yard.
            {"index": 20, "x": -20, "z": 77},
            {"index": 19, "x": -18, "z": 104},
            {"index": 18, "x": 2, "z": 104},
            {"index": 17, "x": 2, "z": 76},
            # THE EAST GARTH, the same fault and the same answer. The moves run before the insert
            # because an insert shifts every index above it.
            {"index": 15, "x": 17, "z": 91},
            {"index": 14, "x": 29, "z": 93},
            {"index": 13, "x": 40, "z": 87},
            {"after": 12, "x": 40, "z": 71},
            {"index": 12, "x": 31, "z": 66},
            # THE TWO FRONTLINE TIPS. The composer draws them 10 blocks wide and FR9 reads 10 blocks
            # as a funnel rather than as somewhere to cross; the plan widened each to 15 and these
            # push the noses out and break their corners, so a tip reads as a headland rather than
            # as the end of a rectangle. Nothing is pushed forward of z 18, which is what keeps the
            # hop from the causey's shoulders inside G5's ten blocks.
            {"index": 11, "x": 29, "z": 34},
            {"index": 10, "x": 28, "z": 26},
            {"index": 9, "x": 22, "z": 19},
            {"after": 8, "x": 13, "z": 18},
            # THE GATE: the notch the composer leaves between the two tips, pulled into a rounded
            # inlet. It is the one place on the front where the crossing is 25 blocks rather than
            # 13, so a team that bridges there is bridging the long way in on purpose.
            {"index": 8, "x": 7, "z": 23},
            {"index": 7, "x": 4, "z": 34},
            {"index": 6, "x": -4, "z": 34},
            {"index": 5, "x": -7, "z": 23},
            {"after": 4, "x": -14, "z": 18},
            {"index": 4, "x": -23, "z": 19},
            {"index": 3, "x": -29, "z": 28},
            {"after": 2, "x": -24, "z": 43},
            # THE NECK. A bite out of the hub's west flank, cut to the apex at x -8: the lane
            # between the flank and the shakehole narrows from 20 blocks to 12, so the west way
            # round the hole is a decision rather than an open field.
            {"index": 2, "x": -15, "z": 47},
            {"after": 1, "x": -8, "z": 57},
            {"index": 1, "x": -15, "z": 64},
        ],
        # the causey: a rectangle in the plan and a lens in the world, its two shoulders 13 blocks
        # off each front and its two tips 25 off the gate
        "causey-15": [
            {"after": 0, "x": 0, "z": -7},
            {"after": 2, "x": 18, "z": 0},
            {"after": 4, "x": 0, "z": 7},
            {"after": 6, "x": -18, "z": 0},
        ],
    },
    # THE HOLE IS NOT SCENERY. The ring hub's four cells compile to a subtract, and a subtract is
    # the board's own statement of its negative space: it may be redrawn but never filled. This one
    # is rounded off and opened two blocks on every side — the shakehole the ring was drawn round —
    # which cuts ground rather than adding it and is the only thing on this board that does.
    "shapePropsById": {
        "void-1-cut": {"vertices": [[7, 54], [13, 54], [16, 57], [16, 63],
                                    [13, 66], [7, 66], [4, 63], [4, 57]]},
    },
    # and then the roughener, over the whole coast at once: `out` is the studio's own slight bloat,
    # which is what makes a compiled rectangle read as land
    "bendShapes": {"front-bar-11": {"wander": 2.5, "step": 9, "seed": 7, "side": "out"}},
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": {"spawn": stell, "wool": laithe},
    "dressing": {"styles": dict(tree_styles,
                                laithe={"kind": "house", "shell": laithe},
                                # a boulder is stone: stone, cobblestone and andesite is the whole
                                # palette that reads as rock from any distance
                                # an erratic is rock a glacier carried from somewhere else, so it
                                # is NOT the ground's own family: pink granite on a grey limestone
                                # moor, two blocks and no more
                                clint={"kind": "boulder", "form": "angular", "size": 3,
                                       "rock": cell_(29, 3, [GRANITE, DIORITE]),
                                       "mossy": False}),
                 "props": props},
}


if __name__ == "__main__":
    json.dump(plan,   open(os.path.join(HERE, f"{SLUG}.plan.json"),   "w"), indent=1)
    json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
