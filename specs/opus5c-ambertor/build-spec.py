#!/usr/bin/env python3
"""opus5c-ambertor — destroy the monument. The approach dimension is ABOVE.

A gold limestone pavement with one tor standing on the contested ground in
front of each monument. The crag's crest is eighteen blocks over the pan the
goal floats on, so the shortest way at the goal is to climb something and
bridge down onto it — a commitment that takes time, is visible the whole while,
and makes the defender watch the sky as well as the two ways round the tor's
foot. A cut flight up the tor's south-west flank is the walked way onto it, so
the defence knows the one place a climber arrives.

Tone families: the ground is gold limestone and dry grass, what is built is
dark oak on dark cobble, and the accent is the deep green of three pines.

Writes opus5c-ambertor.plan.json and opus5c-ambertor.finish.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from opus5c import (solid, cells, field, voronoi, band, stack, soil,
                    slope_stack, blob, wander_rect, tree_body, load_cache,
                    save_cache, write)

SLUG = "opus5c-ambertor"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# Two height zones a team and nothing else, in blocks:
#
#   fell       x -24..24   z  16..92    surface  9   the pavement, the tor, the pan
#   garth-w    x -20..-12  z  92..116   surface 19   the shelf the steading stands on
#   spawn      x -12..8    z  92..116   surface 19   20 x 24, inside ST10's cap
#   garth-e    x   8..20   z  92..116   surface 19
#   mid-band   x -24..24   z -16..16                 a build zone over 32 of void
#
# The two lands never touch. A corridor is a place a defender stands and a
# crossing a team has to pay to bridge is a decision an attacker makes, so the
# join is a build zone spanning the whole eighty-block width.
#
# The board was 80 wide with a garth the full width of it and G8 read a dead
# share of 0.398 against a band topping at 0.12; at 64 it read 0.199. A lane
# board carries two journeys and everything off them is dead, so the width IS
# the measure — and a spawn shelf carried out to the board's own corners is
# ground behind a spawn that no journey ever reaches.
#
# Which is what moved the tor off the centre line. A crag with a lane each side
# needs a board wide enough for three things; a crag against the WEST edge
# needs one wide enough for two, and the ways at the monument are then the open
# east lane or the climb — which differ in dimension, where two lanes round a
# central tor differ only in hand.
#
# The goal's position is arithmetic rather than a thing found later. With the
# spawns 208 apart along the lane and the monument 45 from its own, GO1 reads
# about 3.7 against a band of [3, 4], GO4 45 against [40, 90] and GO3 127
# against [85, 150]. It sits fourteen blocks EAST of the centre line, because a
# goal on the line leaves both flanks on nobody's journey — the coverage
# measure moves by tens of points on that alone.

SPAWN_AT = (-2, 104)
GOAL_AT = (12, 62)
TOR_AT = (-12, 48)
FELL_MIN = (-24, 16)

plan = {
    "plan": 2,
    "meta": {"name": "Ambertor"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 18,
                "surface": 9},
    "pieces": [
        {"id": "fell", "role": "piece", "rect": [-6, 4, 12, 19], "surface": 9},
        {"id": "garth-w", "role": "piece", "rect": [-5, 23, 2, 6], "surface": 19},
        {"id": "spawn", "role": "spawn", "rect": [-3, 23, 5, 6], "surface": 19},
        {"id": "garth-e", "role": "piece", "rect": [2, 23, 3, 6], "surface": 19},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-6, -4, 12, 8], "holes": []},
    ],
    "placements": {
        # The steading is 12 x 12 inside a 20 x 24 piece, and the iron cube
        # stands in the strip between its front wall and the shelf's lip, two
        # blocks clear of both, which is what WX8 asks for.
        "spawns": [{"id": "spawn-garth", "piece": "spawn",
                    "at": [10, 13], "facing": "front",
                    "footprint": [4, 7, 12, 12]}],
        "wools": [],
        "iron": [{"id": "iron-garth", "piece": "spawn", "at": [10.0, 3.5]}],
        "destroyables": [{"id": "monument", "piece": "fell",
                          "at": [GOAL_AT[0] - FELL_MIN[0],
                                 GOAL_AT[1] - FELL_MIN[1]],
                          "style": "pillar-3", "materials": "obsidian",
                          "float": 4, "name": "Ambertor Monument"}],
        "cores": [],
    },
    "walls": [],
}

# ---------------------------------------------------------------- the ground
#
# Three marks and one push, and the push is the board.
#
# The marks pin only the ground a player stands on — the strand a bridger lands
# on, the pan the monument stands alone on, the steading's apron — and
# everything between them is unpinned, which is where the ground gets its
# shape. Pinning the flanks too would leave the solver nothing to solve.
#
# The tor is the one landform, and it stands against the board's west edge
# rather than on its centre line. Ring 10 plus falloff 9 reaches from off the
# west coast to x 7, which leaves the east lane 17 blocks wide — LN1's floor is
# 10. Its skirt grades 16 over 10, 1.6 blocks a cell, which scrambles rather
# than walks, so climbing costs something; its crown climbs 9 over a radius of
# 10, which is 0.9. The two are 1.78 apart, and past twice RL6 says the
# landform steps at its own outline.
#
# Its crest stands about 34 against the pan's 14, so a bridger on it is fifteen
# blocks over the monument's own underside and every block of that bridge is
# visible from the pan.

relief = {
    "*": {
        "base": 9, "reach": 0, "step": 1, "landform": "hills",
        "grain": {"amplitude": 1.4, "scale": 21, "seed": 5301},
        "marks": [
            {"id": "strand", "kind": "area", "h": 9, "bevel": 2,
             "ring": wander_rect(-26, 14, 26, 32, wobble=2.5, seed=5311)},
            {"id": "pan", "kind": "area", "h": 14, "bevel": 4,
             "ring": blob(GOAL_AT[0], GOAL_AT[1], 20, points=13, wobble=0.2,
                          seed=5312)},
            {"id": "garth-apron", "kind": "area", "h": 19, "bevel": 4,
             "ring": wander_rect(-22, 90, 22, 118, wobble=2.5, seed=5313)},
            # The garth stands ten blocks over the fell and a player walks up
            # one, so the riser carries three cut ramps rather than a grade
            # across the whole seam: one out of the spawn's own door, which is
            # what SP8 asks for, and one at each hand, which is what makes the
            # descent a choice instead of a funnel. A line mark pins every cell
            # to the nearest pass of the line, so each is stated as a single
            # run with a height at either end.
            {"id": "ramp-spawn", "kind": "line", "width": 6,
             "points": [[-2, 91], [-2, 77]], "h": [19, 9], "tread": 2},
            {"id": "ramp-west", "kind": "line", "width": 6,
             "points": [[-16, 91], [-16, 77]], "h": [19, 9], "tread": 2},
            {"id": "ramp-east", "kind": "line", "width": 6,
             "points": [[14, 91], [14, 77]], "h": [19, 9], "tread": 2},
        ],
        "pushes": [
            {"id": "tor", "ring": blob(TOR_AT[0], TOR_AT[1], 10, points=11,
                                       wobble=0.2, seed=5321),
             "amount": 16, "falloff": 10, "crown": 9, "roughness": 0,
             "seed": 5322},
        ],
    }
}

# ---------------------------------------------------------------- the paint
#
# Three themes. The pavement is the board's one ground, finished on the slope
# axis so the flat, the shoulder and the crag face are three grounds on one
# hillside; the clints and the garth are the two places made of something else,
# each a shape carrying its own theme.

SANDSTONE = solid(24, 0)
SAND_SMOOTH = solid(24, 2)
SAND_CHISEL = solid(24, 1)
TURF = solid(2, 0)
EARTH = solid(3, 0)
WORN = solid(3, 1)
STONE = solid(1, 0)
COBBLE = solid(4, 0)
GRAVEL = solid(13, 0)
DARKOAK = solid(5, 5)

CRAG_FACE = cells(5331, 7, 5, [SANDSTONE, SAND_SMOOTH, SAND_CHISEL])
SHOULDER = cells(5332, 7, 3, [SANDSTONE, SAND_SMOOTH, WORN])

# Cut off this board's own GET .../incline rather than chosen: it reads 40.6%
# of the ground under 10 degrees, 16.1% to 19 and 15.4% to 29, then a trough of
# 5.1% across 30-39 and 22.8% at 40 or steeper. Cuts at 20 and 32 fall between
# three real populations and neither runs through the middle of one.
SLOPE_FLAT, SLOPE_SHOULDER = 20, 32

pavement_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5333, 9, [(5, SANDSTONE), (4, STONE)]),
    "wall": CRAG_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": SANDSTONE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": slope_stack([
                    (SLOPE_FLAT, soil(TURF, EARTH)),
                    (SLOPE_SHOULDER, soil(SHOULDER, EARTH)),
                    (90, stack("depth", [band(3, CRAG_FACE)])),
                ])},
}

clint_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5334, 9, [(5, SANDSTONE), (4, STONE)]),
    "wall": CRAG_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": SANDSTONE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5335, 8, 0,
                                       [SANDSTONE, SAND_SMOOTH, STONE]),
                                 SANDSTONE)},
}

garth_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5336, 9, [(5, SANDSTONE), (4, STONE)]),
    "wall": cells(5337, 6, 4, [COBBLE, STONE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": COBBLE},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5338, 5, 0, [COBBLE, GRAVEL, DARKOAK]),
                                 STONE)},
}

# ---------------------------------------------------------------- the shapes
#
# The compile emits one shape per surface — fell at 9 and the garth row at 19 —
# so each patch states the base_height of the ground it lies on. A patch owns
# a cell's paint only where its own drawn top is the tallest there, and one
# stated a course too low paints nothing and says so on a 200.

FELL, GARTH = 9, 19

# The flight up the tor: one polygon, two anchors at the foot and two at the
# head, height_mode level, skirt 0, keepClear true, and a MATERIAL rather than
# a theme — a stair is a thing somebody built and a theme is a place. It runs
# 34 blocks for a rise of 17, which is the twice-the-run the ground wants, and
# it is the one walked way onto the crag, running 33 blocks for a rise of 15.
add_shapes = [
    {"id": "tor-flight", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": FELL, "height_mode": "level", "skirt": 0,
     "keepClear": True,
     "anchor_heights": [11, 11, 26, 26],
     "material": cells(5341, 4, 2, [COBBLE, STONE, GRAVEL]),
     "vertices": [[9.2, 25.9], [14.8, 30.1], [-5.2, 56.1], [-10.8, 51.9]]},

    {"id": "clint-pan", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": FELL, "theme": "clint",
     "vertices": blob(4, 74, 11, points=13, wobble=0.26, seed=5342)},
    {"id": "clint-west", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": FELL, "theme": "clint",
     "vertices": blob(-19, 70, 8, points=11, wobble=0.24, seed=5343)},
    {"id": "clint-east", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": FELL, "theme": "clint",
     "vertices": blob(19, 34, 8, points=11, wobble=0.24, seed=5344)},
    {"id": "clint-front", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": FELL, "theme": "clint",
     "vertices": blob(-14, 22, 8, points=11, wobble=0.24, seed=5345)},
    {"id": "garth-yard", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GARTH, "theme": "garth",
     "vertices": wander_rect(-18, 94, 18, 114, wobble=2.0, seed=5346)},
]

# The drystone wall: one run across the pavement west of the pan, drawn as a
# polyline so the rasterizer splines its four points into a curve rather than a
# chain of chords. It is cover on the way in rather than a barrier — it stops
# twelve blocks short of the pan's own edge, because the ground in front of a
# goal is fought over and wants reading at a glance.
field_wall = {
    "id": "field-wall", "name": "the drystone wall", "base_y": 0,
    "kind": "made", "part_of": "fell",
    "groups": [{"id": "field-wall", "name": "the drystone wall",
                "mirrors": True, "shapeIds": ["field-wall-run"]}],
    "shapes": [
        {"id": "field-wall-run", "type": "polyline", "operation": "add",
         "floor": 12, "base_height": 2, "radius": 1.0,
         "stroke_edge": "solid", "keepClear": True,
         "material": cells(5351, 4, 2, [COBBLE, STONE]),
         "vertices": [[-23, 62], [-20, 70], [-18, 78], [-19, 86]]},
    ],
}

# ---------------------------------------------------------------- the dressing
#
# Circulation first: the steading's door forward to the monument, and the
# monument forward to the tor's two feet, which are the two ways an attacker
# on the ground may come. Nothing stands on the strand, because that is where
# a bridger arrives; nothing stands within ten blocks of the goal's marker,
# because OB19 leaves it out of the world and only a header says so.

cache_path = os.path.join(HERE, "trees.json")
cache = load_cache(cache_path)
PINE = tree_body("showcase-r2-1", cache)       # large pine — the one accent
THORN = tree_body("showcase-r6-5", cache)      # tiny oak — the scrub
save_cache(cache_path, cache)

styles = {
    "pine": PINE,
    "thorn": THORN,
    "erratic": {"kind": "boulder", "form": "round", "size": 2, "mossy": False,
                "rock": field(5361, 3, 3, [STONE, COBBLE, solid(1, 5)],
                              rise=3, kind="turbulence")},
    "barn": {"kind": "house", "shell": None},   # filled below
}

# gravel, andesite and cobblestone: three blocks a reader cannot quite tell
# apart, which is what a path on hard ground is
PAVE = cells(5362, 3, 0, [GRAVEL, solid(1, 5), COBBLE])

props = [
    {"id": "garth-way", "kind": "stroke", "seed": 5371, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-2, 96], [2, 88], [8, 78], [11, 70], [12, 64]]},
    {"id": "tor-foot", "kind": "stroke", "seed": 5372, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[10, 58], [2, 52], [-2, 44], [0, 34], [6, 24]]},
    {"id": "east-foot", "kind": "stroke", "seed": 5373, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[16, 56], [20, 46], [20, 34], [18, 24]]},

    # One barn, standing alone out on the pavement, and the board carries no
    # other free-standing house. The garth has three free columns on it once
    # the hall, its door approach and the iron cube are down, and a karst
    # pavement is bare ground on purpose — bare ground chosen beats dressing
    # that was not.
    # the field barn out on the pavement: a building alone on open ground, and
    # the second placement idea on the board
    {"id": "field-barn", "kind": "house", "seed": 5376, "style": "barn",
     "front": "posX",
     "wings": [{"corners": [[-8, 68], [1, 74]], "spec": {"storeysHigh": 1}}]},
]

# three pines, the one deep-green thing on a gold board, standing to the
# outside of the fell rather than down the middle of it
props += [{"id": f"pine-{i}", "kind": "tree", "seed": 5400 + i,
           "x": x, "z": z, "style": "pine"}
          for i, (x, z) in enumerate([(-22, 54), (20, 74), (-20, 66)])]
# thorn scrub, and none of it on the strand a bridger lands on
props += [{"id": f"thorn-{i}", "kind": "tree", "seed": 5420 + i,
           "x": x, "z": z, "style": "thorn"}
          for i, (x, z) in enumerate([(-18, 20), (-8, 34), (-16, 38),
                                      (12, 42), (-14, 52)])]
# Three erratics on the strand, which the relief pins flat: the tor's own foot
# is 48 to 55 degrees and the theme calls the ground a face from 32, so a rock
# pinned to it reads as neither, which is what DR-STEEP says. Three rather than
# five, because a boulder in five places is a sample board.
props += [{"id": f"erratic-{i}", "kind": "boulder", "seed": 5440 + i,
           "x": x, "z": z, "style": "erratic"}
          for i, (x, z) in enumerate([(-20, 22), (-8, 26), (14, 26)])]

# a dry karst is sparse: the coverage is low and the tall share lower, because
# two-block grass in front of an objective is cover nobody authored
props += [
    {"id": "flora", "kind": "flora", "seed": 5380,
     "points": wander_rect(-24, 16, 24, 114, wobble=2.5, seed=5381),
     "spec": {"coverage": 0.17, "scale": 27, "octaves": 3, "fernShare": 0.22,
              "flowerShare": 0.06, "flowerScale": 19, "tallShare": 0.04}},
]

# ---------------------------------------------------------------- the house
#
# Forked from the shipped `alpine mining` preset, whose footing is already
# null — a footing over a plate of one course is a rim round a building with no
# foundation to speak of. The ground is gold limestone, so what stands on it is
# dark oak over dark cobble: a building has to read as a built thing from
# across the pavement, which means its walls are not in the family under its
# feet.

DARKOAK_LOG = {"kind": "laidLog", "id": 162, "data": 1}
OAK = solid(5, 0)

PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
         "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

BARN_STOREY = {
    "clear": 5,
    "wall": {"stack": {"bands": [
        {"material": COBBLE, "thickness": 1},
        {"material": cells(5391, 3, 2, [DARKOAK, OAK]), "thickness": 3},
        {"material": DARKOAK_LOG, "thickness": 1}], "ending": "repeat"},
        "extent": 5},
    "post": solid(162, 1),
    "windows": {"form": "arched", "block": 164, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN, "deck": None, "headroom": 5,
}

BARN = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": COBBLE, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN,
        "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 5,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": DARKOAK, "verge": COBBLE, "gable": DARKOAK,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": COBBLE, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(162, 1),
    "windows": NO_WINDOW,
    "storeys": [BARN_STOREY],
    "porch": None, "front": None,
    # a beam has to be the end of something, so the wall under it carries a
    # course of laid log, which is the last band of the storey
    "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 164, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 5},
                "width": 2, "height": 3},
}

# The spawn hall is the two structures a player sees from the inside, and a
# finish stating no roomStyles leaves it on the studio's bedrock box at 200
# with no finding. It is this board's barn, hipped and built taller.
HALL = json.loads(json.dumps(BARN))
HALL["roof"] = {"form": "hip", "pitch": 2, "slab": 126, "slabData": 5,
                "overhang": 1, "ridgeCap": False, "hole": False,
                "body": DARKOAK, "verge": COBBLE, "gable": None,
                "gableWindows": NO_WINDOW}
HALL["storeys"][0] = json.loads(json.dumps(BARN_STOREY))
HALL["storeys"][0]["clear"] = 7
HALL["storeys"][0]["headroom"] = 7
HALL["storeys"][0]["wall"]["extent"] = 7
HALL["storeys"][0]["wall"]["stack"]["bands"][1]["thickness"] = 5

styles["barn"] = {"kind": "house", "shell": BARN}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"pavement": pavement_theme, "clint": clint_theme,
               "garth": garth_theme},
    "mapTheme": "pavement",
    # Savanna (#bfb755): a dry gold grass that agrees with sandstone instead of
    # fighting it. A tinted block takes its colour from the chunk's biome byte
    # and nothing else does, so the biome is a palette decision rather than a
    # line added at the end. Asked of GET /api/terrain/biomes.
    "biome": {"kind": "solid", "id": 35},
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": [field_wall],
    "roomStyles": {"spawn": HALL, "wool": HALL},
    "dressing": {"styles": styles, "props": props},
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
