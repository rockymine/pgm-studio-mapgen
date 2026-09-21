#!/usr/bin/env python3
"""opus5b-slakefell — destroy the core.

A cold slate fell in three benches over a frozen tarn: each team's core stands
in a walled fold on the middle bench, with ground on every side of it so the
lava has somewhere to fall, and every way up the fell is a cut ramp — so the
raid is a climb, and the defence knows which four places it arrives by.

Tone families: the ground is slate grey and snow, what is built is dark timber
on a brick plinth under a brick-red roof, and the accent is that red.

The board's shape is deliberately not Chalkmere's. That one is a single wide
piece with the relief doing all the work; this is four height zones as pieces,
which is the plan's other legitimate form, and its risers are faces with
authored ramps cut through them.

Writes opus5b-slakefell.plan.json and opus5b-slakefell.finish.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import (solid, cells, field, band, stack, soil, lobe, lobed_rect,
                    tree_body, load_cache, save_cache, write)

SLUG = "opus5b-slakefell"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# blocks:  strand  x -24..24  z   8..32    surface  9   the shore under the fell
#          bench   x -24..24  z  32..64    surface 17   the core's bench
#          brow    x -24..24  z  64..84    surface 25   the shelf above it
#          fold-w  x -24..-16 z  84..104   surface 29
#          lodge   x -16..4   z  84..104   surface 29   (20 x 20 — ST10's cap)
#          fold-e  x   4..24  z  84..104   surface 29
#          strait  x -24..24  z -16..16    a build zone over 16 blocks of void
#
# The core sits on the west hand of the bench and the spawn on the east of
# centre, so a team's two journeys cross the board instead of running down one
# side of it — which is what the dead share reads.

SPAWN_AT = (-1, 94)
GOAL_AT = (-14, 48)

BENCH_MIN = (-24, 32)
LODGE_MIN = (-16, 84)

plan = {
    "plan": 2,
    "meta": {"name": "Slakefell"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": 9},
    "pieces": [
        {"id": "strand", "role": "piece", "rect": [-6, 2, 12, 6], "surface": 9},
        {"id": "bench", "role": "piece", "rect": [-6, 8, 12, 8], "surface": 17},
        {"id": "brow", "role": "piece", "rect": [-6, 16, 12, 5], "surface": 25},
        {"id": "fold-w", "role": "piece", "rect": [-6, 21, 2, 5], "surface": 29},
        {"id": "lodge", "role": "spawn", "rect": [-4, 21, 5, 5], "surface": 29},
        {"id": "fold-e", "role": "piece", "rect": [1, 21, 5, 5], "surface": 29},
    ],
    "zones": [
        {"id": "strait", "rect": [-6, -4, 12, 8], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-lodge", "piece": "lodge",
                    "at": [SPAWN_AT[0] - LODGE_MIN[0], SPAWN_AT[1] - LODGE_MIN[1]],
                    "facing": "front", "footprint": [6, 4, 12, 12]}],
        "wools": [],
        "iron": [{"id": "iron-lodge", "piece": "lodge", "at": [2.5, 10.0]}],
        "destroyables": [],
        # float 6 and leak 5 are the vocabulary's own: a core at float 0 has no
        # floor under its lava and cannot leak at all, which is the whole of
        # what a core is.
        "cores": [{"id": "core", "piece": "bench",
                   "at": [GOAL_AT[0] - BENCH_MIN[0], GOAL_AT[1] - BENCH_MIN[1]],
                   "lava": 3, "lavaHeight": 3, "float": 6, "leak": 5,
                   "name": "Slakefell Core"}],
    },
    "walls": [],
}

# ---------------------------------------------------------------- the ground
#
# Four pinned pans with three-block gaps between them, so each riser is a face
# rather than a grade; and four `line` marks with heights at both ends, which
# are the ramps cut through those faces. Two ways up each riser, on opposite
# hands, so a goal has more than one angle onto it and a defence has two places
# to watch rather than a doorway.
#
# A line mark's band is twice its `r` either side of the centreline, and its
# `tread` is how much of that band is flat; the rest lofts into whatever the
# marks beside it say.

RAMP_RUN = 18          # blocks of run for eight of rise: twice the rise and more

relief = {
    "*": {
        "base": 9, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.2, "scale": 18, "seed": 5103},
        "marks": [
            {"id": "strand-pan", "kind": "area", "h": 9, "bevel": 2,
             "ring": lobed_rect(-26, 4, 26, 30, wobble=2.5, seed=5111)},
            {"id": "core-bench", "kind": "area", "h": 17, "bevel": 4,
             "ring": lobed_rect(-26, 33, 26, 62, wobble=2.5, seed=5112)},
            {"id": "brow-shelf", "kind": "area", "h": 25, "bevel": 3,
             "ring": lobed_rect(-26, 65, 26, 82, wobble=2.0, seed=5113)},
            {"id": "lodge-apron", "kind": "area", "h": 29, "bevel": 3,
             "ring": lobed_rect(-26, 85, 26, 110, wobble=2.0, seed=5114)},
            {"id": "ramp-lower-west", "kind": "line", "r": 5, "tread": 3,
             "points": [[-18, 22], [-18, 22 + RAMP_RUN]], "h": [9, 17]},
            {"id": "ramp-lower-east", "kind": "line", "r": 5, "tread": 3,
             "points": [[16, 22], [16, 22 + RAMP_RUN]], "h": [9, 17]},
            {"id": "ramp-upper-mid", "kind": "line", "r": 5, "tread": 3,
             "points": [[-4, 56], [-4, 56 + RAMP_RUN]], "h": [17, 25]},
            {"id": "ramp-upper-east", "kind": "line", "r": 5, "tread": 3,
             "points": [[18, 56], [18, 56 + RAMP_RUN]], "h": [17, 25]},
        ],
        "pushes": [
            # the crag over the core's bench: the height an attacker climbs for,
            # placed so its ring plus its falloff clears the casing by a margin
            {"id": "crag", "ring": lobe(14, 44, 8, points=9, wobble=0.22,
                                        seed=5121),
             "amount": 9, "falloff": 10, "crown": 4, "roughness": 1.4,
             "seed": 5122},
        ],
    }
}

# ---------------------------------------------------------------- the paint

SLATE = solid(1, 0)
ANDESITE = solid(1, 5)
COBBLE = solid(4, 0)
SNOW = solid(80, 0)
TURF = solid(2, 0)
EARTH = solid(3, 0)
WORN = solid(3, 1)
GRAVEL = solid(13, 0)
CLAY = solid(82, 0)
BRICK = solid(45, 0)
STONEBRICK = solid(98, 0)

SLATE_FACE = cells(5131, 6, 5, [SLATE, ANDESITE])

# The band edges are this board's own. GET .../incline reads 45.5% of the
# ground under 10 degrees, 15.3% between 10 and 19, 16.6% between 20 and 29
# and 11.6% at 40 or steeper, so the cuts at 20 and 40 sit on bucket walls:
# snow and turf on the benches, scree on the shoulders, slate on the risers.
SLOPE_SNOW, SLOPE_SCREE = 20, 40

fell_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": SLATE,
    "wall": SLATE_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": ANDESITE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": stack("slope", [
                    band(SLOPE_SNOW, stack("depth", [
                        band(1, cells(5132, 9, 0, [SNOW, TURF])),
                        band(2, EARTH)])),
                    band(SLOPE_SCREE - SLOPE_SNOW,
                         soil(cells(5133, 7, 0, [GRAVEL, WORN]), EARTH)),
                    band(90 - SLOPE_SCREE, stack("depth", [band(3, SLATE_FACE)])),
                ])},
}

tarn_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": SLATE,
    "wall": SLATE_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": ANDESITE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5134, 7, 0, [GRAVEL, CLAY]), EARTH)},
}

works_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": SLATE,
    "wall": cells(5135, 5, 4, [STONEBRICK, ANDESITE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5136, 5, 0, [STONEBRICK, ANDESITE, BRICK]),
                                 SLATE)},
}

# ---------------------------------------------------------------- the shapes

STRAND_BASE, BENCH_BASE, BROW_BASE, LODGE_BASE = 9, 17, 25, 29

add_shapes = [
    {"id": "tarn-shore", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": STRAND_BASE, "theme": "tarn",
     "vertices": lobe(-12, 20, 11, points=13, wobble=0.22, seed=5141)},
    {"id": "fold-ground", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": BENCH_BASE, "theme": "works",
     "vertices": lobe(GOAL_AT[0], GOAL_AT[1], 10, points=11, wobble=0.15,
                      seed=5142)},
    {"id": "lodge-yard", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": LODGE_BASE, "theme": "works",
     "vertices": lobed_rect(-22, 86, 22, 102, wobble=1.5, seed=5143)},
]

# The fold: a drystone ring round the core, open on the south so the way in is
# a gate rather than a wall. It is a made layer, so SK10's pair walk and SK11's
# reachability walk leave it alone, and it is drawn clear of the casing — a
# core at float 6 over ground at 17 has its lowest course at y24 and the wall
# tops out at y20, so the two never hold the same courses.
fold_wall = {
    "id": "core-fold", "name": "the fold", "base_y": 0,
    "kind": "made", "part_of": "fold",
    "groups": [{"id": "core-fold", "name": "the fold", "mirrors": True,
                "shapeIds": ["fold-arc-west", "fold-arc-east"]}],
    "shapes": [
        {"id": "fold-arc-west", "type": "polyline", "operation": "add",
         "floor": 17, "base_height": 3, "radius": 1.0,
         "stroke_edge": "solid", "keepClear": True,
         "material": cells(5151, 4, 2, [COBBLE, ANDESITE]),
         "vertices": [[-17, 55], [-22, 50], [-22, 44], [-18, 41]]},
        {"id": "fold-arc-east", "type": "polyline", "operation": "add",
         "floor": 17, "base_height": 3, "radius": 1.0,
         "stroke_edge": "solid", "keepClear": True,
         "material": cells(5151, 4, 2, [COBBLE, ANDESITE]),
         "vertices": [[-10, 41], [-6, 45], [-6, 51], [-10, 55]]},
    ],
}

# ---------------------------------------------------------------- the dressing

cache_path = os.path.join(HERE, "trees.json")
cache = load_cache(cache_path)
PINE = tree_body("showcase-r2-2", cache)        # large pine
FIR = tree_body("showcase-r4-3", cache)         # tiny spruce
save_cache(cache_path, cache)

PAVE = cells(5162, 3, 0, [GRAVEL, COBBLE, ANDESITE])

BOULDERS = [(-20, 70), (10, 72), (-22, 14)]
PINES = [(-20, 76), (-14, 72), (-21, 62), (8, 60)]
FIRS = [(4, 74), (14, 66)]

styles = {
    "pine": PINE,
    "fir": FIR,
    "erratic": {"kind": "boulder", "form": "round", "size": 2, "mossy": False,
                "rock": field(5161, 3, 3, [SLATE, COBBLE, ANDESITE],
                              rise=3, kind="turbulence")},
    "fell-house": {"kind": "house", "shell": None},
}

props = [
    # the two routes: the lodge door down the fell to the fold's gate, and the
    # fold forward to the strand a crossing lands on. Both take the ramps,
    # because the ramps are where the ground goes.
    {"id": "fell-track", "kind": "stroke", "seed": 5171, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-1, 88], [-3, 78], [-4, 68], [-6, 58], [-11, 52]]},
    {"id": "haul-road", "kind": "stroke", "seed": 5172, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-14, 38], [-16, 32], [-18, 24], [-17, 16], [-15, 10]]},

    {"id": "frozen-tarn", "kind": "water", "seed": 5173, "shape": "pool",
     "points": lobe(-12, 20, 7, points=9, wobble=0.2, seed=5174),
     "radius": 2, "depth": 2, "shore": 3, "shoreWander": True,
     "bank": cells(5175, 4, 0, [GRAVEL, CLAY, SLATE])},

    # Two buildings, each on the only ground its own footprint seats on. The
    # bench cannot hold one: the core's clearance takes the west of it and the
    # crag's skirt the east, and a byre tried there was declined DR-SLOPE for
    # ten blocks of rise across its own plan. The seats raster for a 9 x 6
    # house is what these two positions come off.
    {"id": "lodge-byre", "kind": "house", "seed": 5176, "style": "fell-house",
     "front": "negX",
     "wings": [{"corners": [[14, 88], [22, 93]], "spec": {"storeysHigh": 2}}]},
    {"id": "tarn-store", "kind": "house", "seed": 5177, "style": "fell-house",
     "front": "negZ",
     "wings": [{"corners": [[-2, 18], [6, 23]], "spec": {"storeysHigh": 1}}]},
]

props += [{"id": f"pine-{i}", "kind": "tree", "seed": 5200 + i,
           "x": x, "z": z, "style": "pine"} for i, (x, z) in enumerate(PINES)]
props += [{"id": f"fir-{i}", "kind": "tree", "seed": 5220 + i,
           "x": x, "z": z, "style": "fir"} for i, (x, z) in enumerate(FIRS)]
props += [{"id": f"erratic-{i}", "kind": "boulder", "seed": 5240 + i,
           "x": x, "z": z, "style": "erratic"}
          for i, (x, z) in enumerate(BOULDERS)]

props += [
    {"id": "flora", "kind": "flora", "seed": 5180,
     "points": lobed_rect(-24, 8, 24, 102, wobble=2.0, seed=5181),
     "spec": {"coverage": 0.16, "scale": 30, "octaves": 3, "fernShare": 0.20,
              "flowerShare": 0.04, "flowerScale": 22, "tallShare": 0.04}},
]

# ---------------------------------------------------------------- the house
#
# Dark timber on a brick plinth under a brick roof: the ground is slate and
# snow, so the buildings are the one warm thing on the board. The frame is one
# wood — post, beams, and the laid-log course the beams are the ends of.

SPRUCE = solid(5, 1)
DARKOAK = solid(5, 5)
SPRUCE_LOG = {"kind": "laidLog", "id": 17, "data": 1}

PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1,
                 "inlay": None, "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

FELL_STOREY = {
    "clear": 5,
    "wall": {"stack": {"bands": [
        {"material": BRICK, "thickness": 1},
        {"material": cells(5191, 3, 2, [DARKOAK, SPRUCE]), "thickness": 3},
        {"material": SPRUCE_LOG, "thickness": 1}], "ending": "repeat"},
        "extent": 5},
    "post": solid(17, 1),
    "windows": {"form": "arched", "block": 134, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN_SURFACE, "deck": None, "headroom": 5,
}

FELL_HOUSE = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": BRICK, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN_SURFACE, "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 44, "slabData": 4,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": BRICK, "verge": DARKOAK, "gable": DARKOAK,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": BRICK, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(17, 1),
    "windows": NO_WINDOW,
    "storeys": [FELL_STOREY],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 1},
                "width": 2, "height": 3},
}

LODGE_HALL = json.loads(json.dumps(FELL_HOUSE))
LODGE_HALL["roof"] = {"form": "hip", "pitch": 2, "slab": 44, "slabData": 4,
                      "overhang": 1, "ridgeCap": False, "hole": False,
                      "body": BRICK, "verge": DARKOAK, "gable": None,
                      "gableWindows": NO_WINDOW}
LODGE_HALL["storeys"][0] = json.loads(json.dumps(FELL_STOREY))
LODGE_HALL["storeys"][0]["clear"] = 7
LODGE_HALL["storeys"][0]["headroom"] = 7
LODGE_HALL["storeys"][0]["wall"]["extent"] = 7
LODGE_HALL["storeys"][0]["wall"]["stack"]["bands"][1]["thickness"] = 5

styles["fell-house"] = {"kind": "house", "shell": FELL_HOUSE}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"fell": fell_theme, "tarn": tarn_theme, "works": works_theme},
    "mapTheme": "fell",
    # Ice plains: grass, leaves and water tint #80b497, which is what makes a
    # snowfield and a meadow agree instead of a summer meadow running through
    # the snow. Read off GET /api/terrain/biomes.
    "biome": {"kind": "solid", "id": 12},
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": [fold_wall],
    "roomStyles": {"spawn": LODGE_HALL, "wool": LODGE_HALL},
    "dressing": {"styles": styles, "props": props},
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
