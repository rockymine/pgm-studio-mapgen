#!/usr/bin/env python3
"""opus5b-ochredrift — capture the wool.

A red mesa mining camp over a dry wash: each team keeps two wools in rock-cut
rooms on spurs at the far corners of its own ground, one bedrock line across
each spur's mouth, and a hole through the middle of its hub — so a raider
chooses which side of that hole to come round, and a defender has two prepared
lines and cannot hold both.

Tone families: the ground is red — clay, red sandstone and dry litter; what is
built is pale sandstone and birch on a grey plinth; the accent is the grey of
the crusher yard's paving.

The crusher terrace is the one piece of made ground on the board: its compiled
shape carries relief_scope exclude, so it meets the hub at a face rather than a
grade, and a flight cut into that face is the way up.

Writes opus5b-ochredrift.plan.json and opus5b-ochredrift.finish.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import (solid, cells, field, band, stack, soil, lobe, lobed_rect,
                    tree_body, load_cache, save_cache, write)

SLUG = "opus5b-ochredrift"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# blocks:  front-w      x -48..-8   z  16..40   surface  9   the wash-side shelf
#          front-e      x  12..48   z  16..36   surface  9
#          hub-w        x -48..-32  z  36..64   surface 15
#          hub-e        x  32..48   z  36..64   surface 15
#          hub-link-w   x -32..-16  z  52..64   surface 15
#          hub-n        x -16..16   z  48..64   surface 15
#          hub-link-e   x  16..32   z  52..64   surface 15
#          w-approach   x -48..-32  z  64..80   surface 15
#          w-room       x -48..-32  z  80..92   surface 15
#          e-approach   x  32..48   z  64..80   surface 15
#          e-room       x  32..48   z  80..92   surface 15
#          yard         x -16..16   z  64..84   surface 21   the crusher terrace
#          spawn        x -16..4    z  84..104  surface 21   (20 x 20)
#          yard-ne      x   4..12   z  84..104  surface 21
#          mid-band     x -48..48   z -16..16   the build zone over the wash
#
# Two holes are made by arrangement and neither is covered by any piece: a
# notch between the two frontline legs, x -12..12 from z 16 to 36, and a slot
# across the hub, x -32..32 from z 36 up to 48 in the middle and 52 at the
# flanks. They meet, so what the compile declares is one T of void through the
# middle of a team's own ground.
#
# What that buys is the funnel. The only ground joining the wash shelf to the
# hub is the sixteen blocks at each end, x -48..-32 and x 32..48, and a ramp is
# cut through each — so an attacker who has crossed the wash chooses a hand,
# and a defender knows the two places anyone arrives by. Nothing bridges the
# holes, because no build zone covers them.
#
# The frontline is what a build zone touches, and FR6 caps it at sixteen cells.
# One piece across the whole 96-block face read 24; the two legs read ten each.
#
# Each wool room has three faces on void and one connecting piece, which is the
# corner a room is defended from, and the bay between a room and the terrace is
# sixteen blocks — WL12's floor, because a shorter one is crossed by towering
# at the near edge and jumping in rather than by building.

SPAWN_PIECE_MIN = (-16, 84)

plan = {
    "plan": 2,
    "meta": {"name": "Ochre Drift"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 22,
                "surface": 9},
    "pieces": [
        {"id": "front-w", "role": "piece", "rect": [-12, 4, 9, 5], "surface": 9},
        {"id": "front-e", "role": "piece", "rect": [3, 4, 9, 5], "surface": 9},
        {"id": "hub-w", "role": "piece", "rect": [-12, 9, 4, 7], "surface": 15},
        {"id": "hub-e", "role": "piece", "rect": [8, 9, 4, 7], "surface": 15},
        {"id": "hub-link-w", "role": "piece", "rect": [-8, 13, 4, 3], "surface": 15},
        {"id": "hub-n", "role": "piece", "rect": [-4, 12, 8, 4], "surface": 15},
        {"id": "hub-link-e", "role": "piece", "rect": [4, 13, 4, 3], "surface": 15},
        {"id": "w-approach", "role": "piece", "rect": [-12, 16, 4, 4], "surface": 15},
        {"id": "w-room", "role": "wool-room", "rect": [-12, 20, 4, 3], "surface": 15},
        {"id": "e-approach", "role": "piece", "rect": [8, 16, 4, 4], "surface": 15},
        {"id": "e-room", "role": "wool-room", "rect": [8, 20, 4, 3], "surface": 15},
        {"id": "yard", "role": "piece", "rect": [-4, 16, 8, 5], "surface": 21},
        {"id": "spawn", "role": "spawn", "rect": [-4, 21, 5, 5], "surface": 21},
        {"id": "yard-ne", "role": "piece", "rect": [1, 21, 2, 5], "surface": 21},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-12, -4, 24, 8], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-camp", "piece": "spawn", "at": [11, 10],
                    "facing": "front", "footprint": [6, 2, 10, 16]}],
        "wools": [
            {"id": "wool-west", "piece": "w-room", "at": [8, 6]},
            {"id": "wool-east", "piece": "e-room", "at": [8, 6]},
        ],
        "iron": [{"id": "iron-camp", "piece": "spawn", "at": [2.5, 10.0]}],
        "destroyables": [],
        "cores": [],
    },
    # One wall on one interface each, at the mouth of a spur rather than on the
    # room's own edge — PL13 refuses that, and two in series is a sealed room
    # rather than a prepared line. The interface is sixteen blocks wide, inside
    # ST8's ten-to-twenty lane mouth, and the spur carries no ground past the
    # wall's ends for a player to stroll round.
    "walls": [
        {"a": "hub-w", "b": "w-approach"},
        {"a": "hub-e", "b": "e-approach"},
    ],
}

# ---------------------------------------------------------------- the ground

relief = {
    "*": {
        "base": 9, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.2, "scale": 16, "seed": 6103},
        "marks": [
            {"id": "wash-shelf", "kind": "area", "h": 9, "bevel": 2,
             "ring": lobed_rect(-50, 12, 50, 34, wobble=3.0, seed=6111)},
            {"id": "hub-bar", "kind": "area", "h": 15, "bevel": 3,
             "ring": lobed_rect(-50, 46, 50, 66, wobble=3.0, seed=6112)},
            {"id": "spur-west", "kind": "area", "h": 15, "bevel": 3,
             "ring": lobed_rect(-50, 38, -30, 94, wobble=2.0, seed=6113)},
            {"id": "spur-east", "kind": "area", "h": 15, "bevel": 3,
             "ring": lobed_rect(30, 38, 50, 94, wobble=2.0, seed=6114)},
            # the two cuts up off the wash, one at each end of the funnel
            {"id": "ramp-west", "kind": "line", "r": 5, "tread": 3,
             "points": [[-40, 28], [-40, 46]], "h": [9, 15]},
            {"id": "ramp-east", "kind": "line", "r": 5, "tread": 3,
             "points": [[40, 28], [40, 46]], "h": [9, 15]},
        ],
        "pushes": [
            # Two buttes on the hub, one a side of the hole, so the ground an
            # attacker crosses has height on it to climb and bridge from and
            # the two lanes round the hole are not the same walk.
            {"id": "butte-west", "ring": lobe(-20, 26, 7, points=9, wobble=0.2,
                                              seed=6121),
             "amount": 9, "falloff": 9, "crown": 4, "roughness": 1.4,
             "seed": 6122},
            {"id": "butte-east", "ring": lobe(22, 24, 6, points=9, wobble=0.24,
                                              seed=6123),
             "amount": 6, "falloff": 8, "crown": 3, "roughness": 1.2,
             "seed": 6124},
        ],
    }
}

# ---------------------------------------------------------------- the paint

RED_SAND = solid(12, 1)
RED_SANDSTONE = solid(179, 0)
RED_SANDSTONE_SM = solid(179, 2)
CLAY_RED = solid(172, 0)
WORN = solid(3, 1)
EARTH = solid(3, 0)
PODZOL = solid(3, 2)
TURF = solid(2, 0)
GRAVEL = solid(13, 0)
STONEBRICK = solid(98, 0)
PALE_ANDESITE = solid(1, 6)
COBBLE = solid(4, 0)
SANDSTONE = solid(24, 0)
BIRCH = solid(5, 2)

MESA_FACE = cells(6131, 7, 5, [CLAY_RED, RED_SANDSTONE])

# Cut off this board's own GET .../incline, which reads 69.8% of the ground
# under 10 degrees, 15.8% between 10 and 29 and 7.2% at 40 or steeper: the
# cuts at 10 and 30 land on bucket walls, so the mesa tops take the dry litter,
# the ramps and skirts take red sand, and only the risers take bare rock.
SLOPE_LITTER, SLOPE_SCREE = 10, 30

mesa_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": RED_SANDSTONE,
    "wall": MESA_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": RED_SANDSTONE_SM},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": stack("slope", [
                    band(SLOPE_LITTER, soil(cells(6132, 8, 0, [TURF, PODZOL]),
                                            EARTH)),
                    band(SLOPE_SCREE - SLOPE_LITTER,
                         soil(cells(6133, 7, 0, [RED_SAND, WORN]), EARTH)),
                    band(90 - SLOPE_SCREE,
                         stack("depth", [band(3, MESA_FACE)])),
                ])},
}

wash_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": RED_SANDSTONE,
    "wall": MESA_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": RED_SANDSTONE_SM},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(6134, 7, 0, [RED_SAND, GRAVEL]),
                                 RED_SANDSTONE)},
}

works_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": RED_SANDSTONE,
    "wall": cells(6135, 5, 4, [STONEBRICK, PALE_ANDESITE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(6136, 5, 0,
                                       [STONEBRICK, PALE_ANDESITE, COBBLE]),
                                 solid(1, 0))},
}

# ---------------------------------------------------------------- the shapes

FRONT_BASE, BENCH_BASE, TERRACE_BASE = 9, 15, 21

add_shapes = [
    {"id": "wash-floor", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": FRONT_BASE, "theme": "wash",
     "vertices": lobed_rect(-44, 16, 44, 34, wobble=3.0, seed=6141)},
]

# The flight down off the crusher terrace. It is a made layer of its own, so
# nothing in the ground's relief answers for it and SK10's pair walk leaves it
# alone; anchor_heights are thicknesses at the polygon's corners, so the four
# read foot, foot, head, head. Twelve blocks of run for six of rise, which is
# twice the rise, and the head lands on the terrace's own top block.
terrace_steps = {
    "id": "crusher-steps", "name": "the crusher steps", "base_y": 0,
    "kind": "made", "part_of": "crusher",
    "groups": [{"id": "crusher-steps", "name": "the crusher steps",
                "mirrors": True, "shapeIds": ["steps-main"]}],
    "shapes": [
        {"id": "steps-main", "type": "polygon", "operation": "add",
         "floor": 0, "keepClear": True,
         "anchor_heights": [BENCH_BASE, BENCH_BASE, TERRACE_BASE, TERRACE_BASE],
         "material": cells(6151, 4, 3, [STONEBRICK, PALE_ANDESITE]),
         "vertices": [[-5, 52], [5, 52], [5, 64], [-5, 64]]},
    ],
}

# ---------------------------------------------------------------- the dressing

cache_path = os.path.join(HERE, "trees.json")
cache = load_cache(cache_path)
SCRUB = tree_body("showcase-r8-3", cache)       # acacia
OLIVE = tree_body("showcase-r10-2", cache)      # small olive
save_cache(cache_path, cache)

PAVE = cells(6162, 3, 0, [GRAVEL, WORN, COBBLE])

SCRUBS = [(-47, 40), (-47, 54), (44, 44), (40, 40)]
OLIVES = [(-30, 30), (24, 28)]
ROCKS = [(-46, 26), (22, 22), (36, 40)]
# The crusher terrace itself seats no building: the hall, its door apron and
# the flight take all of it, and POST .../sketch/seats for a 9 x 6 house marks
# 216 cells on the whole board and none of them there. So the stamp mill stands
# on the wash edge where a stamp mill belongs — one side against the coast,
# which DR-PASS allows — and the winding house on the east arm of the hub.
HOUSES = [("crusher", [[-24, 17], [-16, 22]], 2, "posZ"),
          ("winding-house", [[38, 52], [46, 57]], 1, "negX")]

styles = {
    "scrub": SCRUB,
    "olive": OLIVE,
    "erratic": {"kind": "boulder", "form": "round", "size": 2, "mossy": False,
                "rock": field(6161, 3, 3, [solid(1, 0), COBBLE, solid(1, 5)],
                              rise=3, kind="turbulence")},
    "camp-house": {"kind": "house", "shell": None},
}

props = [
    # spawn door to each spur's mouth, drawn before the scenery
    {"id": "west-haul", "kind": "stroke", "seed": 6171, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-2, 84], [-8, 78], [-18, 70], [-28, 66], [-38, 68]]},
    {"id": "east-haul", "kind": "stroke", "seed": 6172, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[4, 84], [10, 78], [20, 70], [30, 66], [38, 68]]},
    {"id": "front-haul", "kind": "stroke", "seed": 6173, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-40, 60], [-40, 48], [-38, 36], [-34, 26], [-30, 18]]},
]

props += [{"id": f"scrub-{i}", "kind": "tree", "seed": 6200 + i,
           "x": x, "z": z, "style": "scrub"} for i, (x, z) in enumerate(SCRUBS)]
props += [{"id": f"olive-{i}", "kind": "tree", "seed": 6220 + i,
           "x": x, "z": z, "style": "olive"} for i, (x, z) in enumerate(OLIVES)]
props += [{"id": f"rock-{i}", "kind": "boulder", "seed": 6240 + i,
           "x": x, "z": z, "style": "erratic"} for i, (x, z) in enumerate(ROCKS)]
props += [{"id": pid, "kind": "house", "seed": 6260 + i, "style": "camp-house",
           "front": front,
           "wings": [{"corners": corners, "spec": {"storeysHigh": high}}]}
          for i, (pid, corners, high, front) in enumerate(HOUSES)]

props += [
    {"id": "flora", "kind": "flora", "seed": 6180,
     "points": lobed_rect(-48, 16, 48, 102, wobble=3.0, seed=6181),
     "spec": {"coverage": 0.14, "scale": 28, "octaves": 3, "fernShare": 0.06,
              "flowerShare": 0.05, "flowerScale": 20, "tallShare": 0.04}},
]

# ---------------------------------------------------------------- the house
#
# Pale sandstone and birch on a grey plinth: the ground is red, so a building
# reads as built by not being in the ground's family at all.

BIRCH_LOG = {"kind": "laidLog", "id": 17, "data": 2}
PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1,
                 "inlay": None, "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

CAMP_STOREY = {
    "clear": 5,
    "wall": {"stack": {"bands": [
        {"material": STONEBRICK, "thickness": 1},
        {"material": cells(6191, 3, 2, [SANDSTONE, BIRCH]), "thickness": 3},
        {"material": BIRCH_LOG, "thickness": 1}], "ending": "repeat"},
        "extent": 5},
    "post": solid(17, 2),
    "windows": {"form": "arched", "block": 135, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN_SURFACE, "deck": None, "headroom": 5,
}

CAMP_HOUSE = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONEBRICK, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN_SURFACE, "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 2,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": BIRCH, "verge": SANDSTONE, "gable": SANDSTONE,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": STONEBRICK, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(17, 2),
    "windows": NO_WINDOW,
    "storeys": [CAMP_STOREY],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 135, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 2},
                "width": 2, "height": 3},
}

CAMP_HALL = json.loads(json.dumps(CAMP_HOUSE))
CAMP_HALL["roof"] = {"form": "hip", "pitch": 2, "slab": 126, "slabData": 2,
                     "overhang": 1, "ridgeCap": False, "hole": False,
                     "body": BIRCH, "verge": SANDSTONE, "gable": None,
                     "gableWindows": NO_WINDOW}
CAMP_HALL["storeys"][0] = json.loads(json.dumps(CAMP_STOREY))
CAMP_HALL["storeys"][0]["clear"] = 7
CAMP_HALL["storeys"][0]["headroom"] = 7
CAMP_HALL["storeys"][0]["wall"]["extent"] = 7
CAMP_HALL["storeys"][0]["wall"]["stack"]["bands"][1]["thickness"] = 5

# The wool room is a rock-cut chamber: sandstone walls on a stone plinth under
# a flat sandstone lid, so what a raider stands inside belongs to the camp
# rather than to the studio's bedrock default.
WOOL_ROOM = json.loads(json.dumps(CAMP_HOUSE))
WOOL_ROOM["roof"] = {"form": "flat", "pitch": 1, "slab": -1, "slabData": 0,
                     "overhang": 0, "ridgeCap": False, "hole": False,
                     "body": solid(24, 2), "verge": solid(24, 2), "gable": None,
                     "gableWindows": NO_WINDOW}
WOOL_ROOM["storeys"][0] = json.loads(json.dumps(CAMP_STOREY))
WOOL_ROOM["storeys"][0]["clear"] = 6
WOOL_ROOM["storeys"][0]["headroom"] = 6
WOOL_ROOM["storeys"][0]["wall"]["extent"] = 6
WOOL_ROOM["storeys"][0]["wall"]["stack"]["bands"] = [
    {"material": STONEBRICK, "thickness": 1},
    {"material": cells(6192, 4, 2, [SANDSTONE, solid(24, 2)]), "thickness": 4},
    {"material": BIRCH_LOG, "thickness": 1}]

styles["camp-house"] = {"kind": "house", "shell": CAMP_HOUSE}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"mesa": mesa_theme, "wash": wash_theme, "works": works_theme},
    "mapTheme": "mesa",
    # Mesa: grass tints #90814d, which is where podzol's brown comes to meet it
    # and the pair reads as one dry, leaf-littered floor rather than as two
    # grounds. Read off GET /api/terrain/biomes.
    "biome": {"kind": "solid", "id": 37},
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": [terrace_steps],
    # Keyed on the compiled shape id, which is what POST /plan/compile answers;
    # a height key cannot tell two pieces at one surface apart.
    # The crusher terrace is made ground, so its compiled shape is taken out of
    # the solve: `exclude` keeps the raw column and the two tiers meet at a
    # face, where `hold` would let the relief bring the hub up to it and there
    # would be no step and no reason for a flight. The key is the shape id
    # POST /plan/compile answers, because a height key cannot tell two pieces
    # at one surface apart.
    # The crusher terrace is made ground, so its compiled shape comes out of
    # the solve: `exclude` keeps the raw column and the two tiers meet at a
    # face, where `hold` would let the relief bring the hub up to it and there
    # would be no step and no reason for a flight. The key is the shape id
    # POST /plan/compile answers — a height key cannot tell two pieces at one
    # surface apart, and the compile fuses every piece at 21 into this one.
    "shapePropsById": {"e-approach-21": {"relief_scope": "exclude"}},
    "themeById": {"e-approach-21": "works"},
    "roomStyles": {"spawn": CAMP_HALL, "wool": WOOL_ROOM},
    "dressing": {"styles": styles, "props": props},
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
