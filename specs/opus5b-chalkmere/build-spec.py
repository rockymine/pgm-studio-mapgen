#!/usr/bin/env python3
"""opus5b-chalkmere — destroy the monument.

A chalk downland split by a dry combe: each team's monument stands alone on a
pale turf shoulder above its own steading, and the two downs are joined only by
a build zone over the gap between them — so every attack is a crossing made in
the open, and the combe is the one place to drop out of sight once across.

Tone families: the ground is pale chalk and turf, what is built is dark flint
and cobble, and the accent is weathered oak.

Writes opus5b-chalkmere.plan.json and opus5b-chalkmere.finish.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import (solid, cells, field, band, stack, soil, lobe, lobed_rect,
                    tree_body, load_cache, save_cache, write)

SLUG = "opus5b-chalkmere"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# Four pieces a team. The down is the board; the steading and the two folds are
# the shallow back band the spawn hall is seated in, so the hall is not a
# promontory with void on three sides.
#
# blocks:  down      x -28..28   z   8..92
#          fold-w    x -28..-16  z  92..108
#          steading  x -16..4    z  92..108   (20 x 16 - inside ST10's cap)
#          fold-e    x   4..28   z  92..108
#          strait    x -28..28   z -16..16    a build zone over 16 blocks of void
#
# Two numbers were read rather than chosen. The board is 56 blocks wide: the
# first cut was 72 and G8 read a dead share of 0.272 against its band of
# [0, 0.12], because the flanks were ground no journey went to. And the back
# band is 16 blocks deep rather than 24, because the ground behind a spawn is
# ground nobody walks (SP2) and it was the next largest dead patch.

SPAWN_AT = (-5, 100)           # blocks, world - the hall's own centre
GOAL_AT = (14, 62)             # blocks, world - off the centre line on purpose

DOWN_MIN = (-28, 8)            # the down piece's minimum corner, in blocks
STEAD_MIN = (-16, 92)

plan = {
    "plan": 2,
    "meta": {"name": "Chalkmere"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                "surface": 9},
    "pieces": [
        {"id": "down", "role": "piece", "rect": [-7, 2, 14, 21], "surface": 9},
        {"id": "fold-w", "role": "piece", "rect": [-7, 23, 3, 4], "surface": 19},
        {"id": "steading", "role": "spawn", "rect": [-4, 23, 5, 4], "surface": 19},
        {"id": "fold-e", "role": "piece", "rect": [1, 23, 6, 4], "surface": 19},
    ],
    "zones": [
        {"id": "strait", "rect": [-7, -4, 14, 8], "holes": []},
    ],
    "placements": {
        # The hall is 10 x 12 inside a 20 x 16 piece, which leaves a six-block
        # strip down the west side; the iron cube stands in that strip with two
        # blocks of air to the shell, which is what WX8 asks for. Both numbers
        # come from POST /plan/room rather than from arithmetic.
        "spawns": [{"id": "spawn-steading", "piece": "steading",
                    "at": [SPAWN_AT[0] - STEAD_MIN[0], SPAWN_AT[1] - STEAD_MIN[1]],
                    "facing": "front", "footprint": [6, 2, 10, 12]}],
        "wools": [],
        "iron": [{"id": "iron-steading", "piece": "steading", "at": [2.5, 8.0]}],
        "destroyables": [{"id": "monument", "piece": "down",
                          "at": [GOAL_AT[0] - DOWN_MIN[0], GOAL_AT[1] - DOWN_MIN[1]],
                          "style": "pillar-3", "materials": "obsidian",
                          "float": 4, "name": "Chalkmere Monument"}],
        "cores": [],
    },
    "walls": [],
}

# ---------------------------------------------------------------- the ground
#
# Three marks and two pushes. The strand is the shelf a bridger lands on, the
# shoulder is the open turf the monument stands alone on, and the apron is the
# steading's flat. Everything between them is unpinned, which is where the
# ground gets its shape.
#
# The nab is the hill an attacker climbs to bridge at the monument from above;
# the combe is the hollow on the other hand, an entrance from below that opens
# onto the strand. Each push's ring plus its falloff clears the shoulder mark.

relief = {
    "*": {
        "base": 9, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.5, "scale": 20, "seed": 4103},
        "marks": [
            {"id": "strand", "kind": "area", "h": 9, "bevel": 2,
             "ring": lobed_rect(-30, 4, 30, 24, wobble=2.5, seed=4111)},
            {"id": "shoulder", "kind": "area", "h": 17, "bevel": 4,
             "ring": lobe(GOAL_AT[0], GOAL_AT[1], 13, points=11, wobble=0.2,
                          seed=4112)},
            {"id": "steading-apron", "kind": "area", "h": 19, "bevel": 4,
             "ring": lobed_rect(-30, 88, 30, 114, wobble=2.5, seed=4113)},
        ],
        "pushes": [
            {"id": "nab", "ring": lobe(18, 26, 8, points=9, wobble=0.22, seed=4121),
             "amount": 11, "falloff": 11, "crown": 4, "roughness": 1.2,
             "seed": 4122},
            {"id": "combe", "ring": lobe(-17, 38, 9, points=11, wobble=0.24,
                                         seed=4123),
             "amount": -7, "falloff": 11, "crown": -3, "roughness": 1.0,
             "seed": 4124},
        ],
    }
}

# ---------------------------------------------------------------- the paint
#
# Three themes. The down is the board's one ground, finished on the slope axis
# so the shoulder of a hill is not painted like the meadow beside it; the combe
# floor and the steading yard are the two places that are made of something
# else, and each is a shape carrying its own theme.
#
# The band edges are cut off this board's own GET .../incline.

CHALK = solid(24, 0)             # sandstone — the chalk itself
CHALK_SMOOTH = solid(24, 2)
FLINT = solid(1, 5)              # andesite
TURF = solid(2, 0)
EARTH = solid(3, 0)
WORN = solid(3, 1)               # coarse dirt
GRAVEL = solid(13, 0)

CHALK_FACE = cells(4131, 7, 5, [CHALK, CHALK_SMOOTH])

# slope band edges — recut from incline after the first drive
SLOPE_TURF, SLOPE_WORN = 14, 30

down_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": CHALK,
    "wall": CHALK_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": CHALK},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": stack("slope", [
                    band(SLOPE_TURF, soil(TURF, EARTH)),
                    band(SLOPE_WORN - SLOPE_TURF, soil(WORN, EARTH)),
                    band(90 - SLOPE_WORN, stack("depth", [band(3, CHALK_FACE)])),
                ])},
}

combe_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": CHALK,
    "wall": CHALK_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": CHALK},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(4132, 6, 0, [GRAVEL, WORN]), EARTH)},
}

yard_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": CHALK,
    "wall": cells(4133, 6, 4, [FLINT, solid(4, 0)]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": solid(4, 0)},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(4134, 5, 0,
                                       [solid(4, 0), FLINT, solid(98, 0)]),
                                 solid(1, 0))},
}

# ---------------------------------------------------------------- the shapes
#
# Two patches on the ground layer, each stating the compiled down's own
# base_height so it forms the surface of the cells it covers, and one made
# layer: the dry-stone wall that encloses the steading yard, drawn as a
# polyline so it flows rather than turning square corners.

DOWN_BASE = 10   # read off the compiled layout — see README in this directory

add_shapes = [
    {"id": "combe-floor", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": DOWN_BASE, "theme": "combe",
     "vertices": lobe(-17, 38, 11, points=13, wobble=0.22, seed=4141)},
    {"id": "steading-yard", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": DOWN_BASE, "theme": "yard",
     "vertices": lobed_rect(-24, 90, 12, 107, wobble=2.0, seed=4142)},
]

yard_wall = {
    "id": "yard-wall", "name": "the steading wall", "base_y": 0,
    "kind": "made", "part_of": "steading",
    "groups": [{"id": "yard-wall", "name": "the steading wall",
                "mirrors": True, "shapeIds": ["yard-wall-run"]}],
    "shapes": [
        {"id": "yard-wall-run", "type": "path", "operation": "add",
         "floor": 19, "base_height": 2, "radius": 1.0,
         "stroke_edge": "solid", "keepClear": True,
         "material": cells(4151, 4, 2, [solid(4, 0), FLINT]),
         "vertices": [[-22, 93], [-23, 100], [-18, 106], [-6, 107],
                      [6, 105], [12, 99]]},
    ],
}

# ---------------------------------------------------------------- the dressing

cache_path = os.path.join(HERE, "trees.json")
cache = load_cache(cache_path)
BEECH = tree_body("showcase-r11-3", cache)      # dense oak — the shaw
THORN = tree_body("showcase-r6-4", cache)       # tiny oak — the hedge line
save_cache(cache_path, cache)

styles = {
    "beech": BEECH,
    "thorn": THORN,
    "flint-rock": {"kind": "boulder", "form": "round", "size": 2, "mossy": False,
                   "rock": field(4161, 3, 3, [solid(1, 0), solid(4, 0), FLINT],
                                 rise=3, kind="turbulence")},
}

PAVE = cells(4162, 3, 0, [GRAVEL, FLINT, solid(4, 0)])

props = [
    # the two routes, drawn before the scenery: spawn door to the monument, and
    # the monument forward to the strand a crossing lands on.
    {"id": "steading-track", "kind": "stroke", "seed": 4171, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-5, 94], [-2, 86], [4, 78], [10, 70], [13, 66]]},
    {"id": "forward-track", "kind": "stroke", "seed": 4172, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[14, 54], [13, 42], [9, 30], [5, 18], [3, 10]]},
]

props += [
    {"id": "flora", "kind": "flora", "seed": 4180,
     "points": lobed_rect(-28, 8, 28, 108, wobble=2.0, seed=4181),
     "spec": {"coverage": 0.22, "scale": 26, "octaves": 3, "fernShare": 0.12,
              "flowerShare": 0.10, "flowerScale": 18, "tallShare": 0.06}},
]

# ---------------------------------------------------------------- the house
#
# The ground is pale chalk, so what is built on it is dark timber over a cobble
# plinth: a building has to read as a built thing from across the board, which
# means its walls are not in the tone family under its feet. One style, and the
# variety is in the plan rather than in a second palette.
#
# The frame is one wood throughout — post, beam, every storey's post and the
# laid-log course the beams are the ends of — which is what HS4 and HS9 ask.

SPRUCE = solid(5, 1)
DARKOAK = solid(5, 5)
SPRUCE_LOG = {"kind": "laidLog", "id": 17, "data": 1}

PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1,
                 "inlay": None, "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

STEADING_STOREY = {
    "clear": 5,
    "wall": {"stack": {"bands": [
        {"material": solid(4, 0), "thickness": 1},
        {"material": cells(4191, 3, 2, [SPRUCE, DARKOAK]), "thickness": 3},
        {"material": SPRUCE_LOG, "thickness": 1}], "ending": "repeat"},
        "extent": 5},
    "post": solid(17, 1),
    "windows": {"form": "arched", "block": 134, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN_SURFACE, "deck": None, "headroom": 5,
}

CHALK_HOUSE = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": solid(4, 0), "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN_SURFACE,
        "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 1,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": SPRUCE, "verge": DARKOAK, "gable": DARKOAK,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": solid(4, 0), "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(17, 1),
    "windows": NO_WINDOW,
    "storeys": [STEADING_STOREY],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 1},
                "width": 2, "height": 3},
}

# The spawn hall is the same steading built taller and hipped, so what a player
# walks out of belongs to the farm rather than to the studio's bedrock default.
SPAWN_HALL = json.loads(json.dumps(CHALK_HOUSE))
SPAWN_HALL["roof"] = {"form": "hip", "pitch": 2, "slab": 126, "slabData": 1,
                      "overhang": 1, "ridgeCap": False, "hole": False,
                      "body": SPRUCE, "verge": DARKOAK, "gable": None,
                      "gableWindows": NO_WINDOW}
SPAWN_HALL["storeys"][0] = json.loads(json.dumps(STEADING_STOREY))
SPAWN_HALL["storeys"][0]["clear"] = 7
SPAWN_HALL["storeys"][0]["headroom"] = 7
SPAWN_HALL["storeys"][0]["wall"]["extent"] = 7
SPAWN_HALL["storeys"][0]["wall"]["stack"]["bands"][1]["thickness"] = 5

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"down": down_theme, "combe": combe_theme, "yard": yard_theme},
    "mapTheme": "down",
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": [yard_wall],
    "roomStyles": {"spawn": SPAWN_HALL, "wool": SPAWN_HALL},
    "dressing": {"styles": styles, "props": props},
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
