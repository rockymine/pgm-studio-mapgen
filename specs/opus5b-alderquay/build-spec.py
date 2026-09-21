#!/usr/bin/env python3
"""opus5b-alderquay — a wool and a monument at once.

A dark alder holt on a slow backwater: each team's monument stands out in the
open on a timber quay at the water's edge, where anyone crossing the delta can
see it; the wool it defends sits in a room on a spur at the back, past a
prepared bedrock line. So a team is fighting for two different things at two
different depths, and the ground that carries the raid out to the enemy's spur
is the same ground its own monument watches.

Tone families: the ground is dark and wet — podzol, coarse dirt, clay; what is
built is white plaster framed in dark oak; the accent is the water.

Writes opus5b-alderquay.plan.json and opus5b-alderquay.finish.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import (solid, cells, field, band, stack, soil, lobe, lobed_rect,
                    tree_body, load_cache, save_cache, write)

SLUG = "opus5b-alderquay"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# blocks:  eyot-w     x -36..-20  z  16..44   surface  9   the west delta island
#          eyot-e     x  20..36   z  16..44   surface  9   the east one
#          holt-w     x -36..-20  z  44..72   surface 11   the west bank
#          holt-e     x  12..36   z  44..72   surface 11   the east bank and the quay
#          holt-n     x -20..12   z  60..72   surface 11   the head of the channel
#          spur       x -36..-20  z  72..92   surface 15   the wool approach
#          wool-room  x -36..-20  z  92..104  surface 15
#          yard       x   4..36   z  72..92   surface 15   the timber works
#          yard-w     x   4..8    z  92..112  surface 15
#          camp       x   8..28   z  92..112  surface 15   the spawn (20 x 20)
#          yard-e     x  28..36   z  92..112  surface 15
#          mid-band   x -36..36   z -16..16   the build zone over the delta
#
# The void down the middle is the delta's own channel, and it reaches the mid
# rather than sitting inside the team's ground: approaches.md withdraws the
# middle-of-terrain hole on a destroy board, and what it endorses instead is a
# river, which is what this is — a drop that forces a bridge, a chokepoint that
# has to be built before it can be used. The backwater on the west bank is the
# other half of that ruling, a depression a player drops into and comes up
# under the wool approach.
#
# Two frontline legs rather than one face: a single piece across the whole
# board read FR6 frontline-width 18 against a band of [1, 16]; each eyot reads
# four.
#
# The monument stands on the open bank above the quay, a short walk
# forward of its own spawn — the destroy topology, where the thing a team
# defends is its own and the contested space is everything beyond it. The wool
# it defends is on the far side of the board behind a bedrock line, which is
# the capture topology. A team fights for two things at two depths.
#
# The spur is exactly the width of the interface the wall is stamped on, so
# there is no shoulder of ground past the wall's ends for a player to walk
# round; a wall with a way round it has stopped being a decision.

SPAWN_AT = (19, 102)
GOAL_AT = (30, 52)
HOLT_E_MIN = (12, 44)
CAMP_MIN = (8, 92)

plan = {
    "plan": 2,
    "meta": {"name": "Alderquay"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 18,
                "surface": 9},
    "pieces": [
        {"id": "eyot-w", "role": "piece", "rect": [-9, 4, 4, 7], "surface": 9},
        {"id": "eyot-e", "role": "piece", "rect": [5, 4, 4, 7], "surface": 9},
        {"id": "holt-w", "role": "piece", "rect": [-9, 11, 4, 7], "surface": 11},
        {"id": "holt-e", "role": "piece", "rect": [3, 11, 6, 7], "surface": 11},
        {"id": "holt-n", "role": "piece", "rect": [-5, 15, 8, 3], "surface": 11},
        {"id": "spur", "role": "piece", "rect": [-9, 18, 4, 5], "surface": 15},
        {"id": "wool-room", "role": "wool-room", "rect": [-9, 23, 4, 3], "surface": 15},
        {"id": "yard", "role": "piece", "rect": [1, 18, 8, 5], "surface": 15},
        {"id": "yard-w", "role": "piece", "rect": [1, 23, 1, 5], "surface": 15},
        {"id": "camp", "role": "spawn", "rect": [2, 23, 5, 5], "surface": 15},
        {"id": "yard-e", "role": "piece", "rect": [7, 23, 2, 5], "surface": 15},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-9, -4, 18, 8], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-camp", "piece": "camp",
                    "at": [SPAWN_AT[0] - CAMP_MIN[0], SPAWN_AT[1] - CAMP_MIN[1]],
                    "facing": "front", "footprint": [6, 2, 10, 16]}],
        "wools": [{"id": "wool-spur", "piece": "wool-room", "at": [8, 6]}],
        "iron": [{"id": "iron-camp", "piece": "camp", "at": [2.5, 10.0]}],
        "destroyables": [{"id": "monument", "piece": "holt-e",
                          "at": [GOAL_AT[0] - HOLT_E_MIN[0],
                                 GOAL_AT[1] - HOLT_E_MIN[1]],
                          "style": "pillar-3", "materials": "obsidian",
                          "float": 4, "name": "Alderquay Monument"}],
        "cores": [],
    },
    "walls": [{"a": "holt-w", "b": "spur"}],
}

# ---------------------------------------------------------------- the ground

relief = {
    "*": {
        "base": 9, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.5, "scale": 20, "seed": 7103},
        "marks": [
            {"id": "strand", "kind": "area", "h": 9, "bevel": 2,
             "ring": lobed_rect(-38, 12, 38, 42, wobble=3.0, seed=7111)},
            {"id": "holt-flat", "kind": "area", "h": 11, "bevel": 4,
             "ring": lobed_rect(-38, 46, 38, 70, wobble=3.0, seed=7112)},
            # The backwater's pan. Water fills whatever is level, so the pool
            # is the size of the pan rather than of the outline drawn for it —
            # and a pool drawn across a grade cuts a shaft in the bank instead,
            # which is what DR-BANK says.
            {"id": "pool-pan", "kind": "area", "h": 8, "bevel": 3,
             "ring": lobe(-28, 58, 9, points=11, wobble=0.22, seed=7113)},
            {"id": "spur-pad", "kind": "area", "h": 15, "bevel": 3,
             "ring": lobed_rect(-38, 74, -18, 108, wobble=2.0, seed=7114)},
            {"id": "yard-pad", "kind": "area", "h": 15, "bevel": 3,
             "ring": lobed_rect(2, 74, 38, 116, wobble=2.0, seed=7115)},
        ],
        "pushes": [
            {"id": "bank-swell", "ring": lobe(-28, 28, 7, points=9, wobble=0.22,
                                              seed=7121),
             "amount": 7, "falloff": 9, "crown": 3, "roughness": 1.4,
             "seed": 7122},
            {"id": "alder-rise", "ring": lobe(30, 28, 6, points=9, wobble=0.2,
                                              seed=7123),
             "amount": 6, "falloff": 8, "crown": 2, "roughness": 1.2,
             "seed": 7124},
        ],
    }
}

# ---------------------------------------------------------------- the paint

TURF = solid(2, 0)
PODZOL = solid(3, 2)
EARTH = solid(3, 0)
WORN = solid(3, 1)
CLAY = solid(82, 0)
GRAVEL = solid(13, 0)
STONE = solid(1, 0)
COBBLE = solid(4, 0)
ANDESITE = solid(1, 5)
STONEBRICK = solid(98, 0)
DARKOAK = solid(5, 5)
PLASTER = solid(159, 0)

BANK_FACE = cells(7131, 7, 5, [STONE, CLAY])

# Cut off this board's own GET .../incline, which reads 55.7% of the ground
# under 10 degrees, 20.7% between 10 and 19, 13% between 20 and 29 and 3.7%
# at 40 or steeper. The cuts at 20 and 40 put the wood's floor on three
# quarters of the board, the worn clay bank on the fifth that is shoulder, and
# bare rock only on what is actually a face.
SLOPE_WOOD, SLOPE_BANK = 20, 40

carr_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": STONE,
    "wall": BANK_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": WORN},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": stack("slope", [
                    band(SLOPE_WOOD, soil(cells(7132, 9, 0, [TURF, PODZOL]),
                                          EARTH)),
                    band(SLOPE_BANK - SLOPE_WOOD,
                         soil(cells(7133, 7, 0, [WORN, CLAY]), EARTH)),
                    band(90 - SLOPE_BANK, stack("depth", [band(3, BANK_FACE)])),
                ])},
}

reed_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": STONE,
    "wall": BANK_FACE,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": WORN},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(7134, 6, 0, [CLAY, GRAVEL]), EARTH)},
}

works_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": STONE,
    "wall": cells(7135, 5, 4, [STONEBRICK, ANDESITE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(7136, 5, 0, [COBBLE, ANDESITE, STONEBRICK]),
                                 STONE)},
}

# ---------------------------------------------------------------- the shapes

FLATS_BASE, HOLT_BASE, BACK_BASE = 9, 11, 15

add_shapes = [
    {"id": "reed-bed", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": HOLT_BASE, "theme": "reed",
     "vertices": lobe(-28, 58, 12, points=13, wobble=0.2, seed=7141)},
    {"id": "works-ground", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": BACK_BASE, "theme": "works",
     "vertices": lobed_rect(6, 76, 34, 110, wobble=2.0, seed=7142)},
]

# The quay: a plank deck one course proud of the holt at the pool's north edge,
# and the ground the monument stands on. It is a made layer, so SK10's pair
# walk and SK11's reachability walk leave it alone, and the goal seats on the
# top of the column, which is the deck.
quay_posts = {
    "id": "quay-posts", "name": "the quay's posts", "base_y": 0,
    "kind": "made", "part_of": "quay",
    "groups": [{"id": "quay-posts", "name": "the quay's posts", "mirrors": True,
                "shapeIds": ["quay-posts-run"]}],
    "shapes": [
        {"id": "quay-posts-run", "type": "polyline", "operation": "add",
         "floor": 8, "base_height": 3, "radius": 1.0,
         "stroke_edge": "solid", "keepClear": True,
         "material": solid(17, 1),
         "vertices": [[15, 48], [14, 54], [15, 60], [19, 63]]},
    ],
}

# The deck stands on a layer of its own: a layer holds one span per column, so
# the posts under it and the deck over it on one layer is SK9 — the taller add
# wins and the lower shape is simply not in the world.
quay_deck = {
    "id": "quay-deck", "name": "the quay", "base_y": 0,
    "kind": "made", "part_of": "quay",
    "groups": [{"id": "quay-deck", "name": "the quay", "mirrors": True,
                "shapeIds": ["quay-deck-plate"]}],
    "shapes": [
        {"id": "quay-deck-plate", "type": "rectangle", "operation": "add",
         "floor": 11, "base_height": 1, "keepClear": True,
         "material": cells(7151, 4, 1, [DARKOAK, solid(5, 1)]),
         "min_x": 13, "max_x": 24, "min_z": 46, "max_z": 62},
    ],
}

# ---------------------------------------------------------------- the dressing

cache_path = os.path.join(HERE, "trees.json")
cache = load_cache(cache_path)
WILLOW = tree_body("showcase-r17-2", cache)     # willow
BIRCH_TREE = tree_body("showcase-r13-4", cache)  # birch
save_cache(cache_path, cache)

PAVE = cells(7162, 3, 0, [GRAVEL, WORN, COBBLE])

WILLOWS = [(-16, 62), (-4, 68), (8, 66)]
BIRCHES = [(-34, 22), (-24, 34), (22, 18), (22, 34)]
ROCKS = [(16, 44), (-12, 60), (33, 70)]
# Both positions come off POST .../sketch/seats for a 9 x 6 house, which marks
# 80 cells on this board: the spawn hall's own door apron is kept clear for
# thirty blocks in front of it and takes most of the works yard.
# One building, not two. The works yard holds none — the spawn hall's own door
# apron is kept clear for thirty blocks in front of it — and a second shed put
# anywhere the seats raster allowed fell inside the sawmill's claim or left the
# pair of them with no eight blocks of passable ground down one side (DR-PASS,
# which is asked of a group of buildings rather than of each one). The quay
# beside it is the board's other built thing.
HOUSES = [("sawmill", [[12, 64], [20, 69]], 2, "posZ")]

styles = {
    "willow": WILLOW,
    "birch": BIRCH_TREE,
    "erratic": {"kind": "boulder", "form": "round", "size": 2, "mossy": True,
                "rock": field(7161, 3, 3, [STONE, COBBLE, ANDESITE],
                              rise=3, kind="turbulence")},
    "delta-house": {"kind": "house", "shell": None},
}

props = [
    # spawn door to the quay, and the quay forward to the delta the crossing
    # lands on; and the spawn door out to the wool spur's mouth
    {"id": "quay-road", "kind": "stroke", "seed": 7171, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[19, 92], [22, 84], [26, 76], [28, 68], [26, 62]]},
    {"id": "spur-road", "kind": "stroke", "seed": 7172, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[10, 92], [4, 84], [-4, 78], [-14, 74], [-28, 76]]},
    {"id": "delta-road", "kind": "stroke", "seed": 7173, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-30, 68], [-30, 56], [-30, 44], [-28, 32], [-26, 20]]},

    {"id": "backwater", "kind": "water", "seed": 7174, "shape": "pool",
     "points": lobe(-28, 58, 6, points=11, wobble=0.2, seed=7175),
     "radius": 2, "depth": 2, "shore": 3, "shoreWander": True,
     "bank": cells(7176, 4, 0, [CLAY, GRAVEL, WORN])},
]

props += [{"id": f"willow-{i}", "kind": "tree", "seed": 7200 + i,
           "x": x, "z": z, "style": "willow"}
          for i, (x, z) in enumerate(WILLOWS)]
props += [{"id": f"birch-{i}", "kind": "tree", "seed": 7220 + i,
           "x": x, "z": z, "style": "birch"}
          for i, (x, z) in enumerate(BIRCHES)]
props += [{"id": f"rock-{i}", "kind": "boulder", "seed": 7240 + i,
           "x": x, "z": z, "style": "erratic"} for i, (x, z) in enumerate(ROCKS)]
props += [{"id": pid, "kind": "house", "seed": 7260 + i, "style": "delta-house",
           "front": front,
           "wings": [{"corners": corners, "spec": {"storeysHigh": high}}]}
          for i, (pid, corners, high, front) in enumerate(HOUSES)]

props += [
    {"id": "flora", "kind": "flora", "seed": 7180,
     "points": lobed_rect(-36, 16, 36, 110, wobble=3.0, seed=7181),
     "spec": {"coverage": 0.26, "scale": 24, "octaves": 3, "fernShare": 0.30,
              "flowerShare": 0.06, "flowerScale": 16, "tallShare": 0.06}},
]

# ---------------------------------------------------------------- the house
#
# White plaster framed in dark oak: the ground is the darkest of the four
# boards, so the buildings are the palest thing standing on it.

DARK_LOG = {"kind": "laidLog", "id": 162, "data": 1}
PLAIN_SURFACE = {"field": None, "border": None, "borderWidth": 1,
                 "inlay": None, "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

DELTA_STOREY = {
    "clear": 5,
    "wall": {"stack": {"bands": [
        {"material": STONEBRICK, "thickness": 1},
        {"material": cells(7191, 3, 2, [PLASTER, solid(155, 0)]), "thickness": 3},
        {"material": DARK_LOG, "thickness": 1}], "ending": "repeat"},
        "extent": 5},
    "post": solid(162, 1),
    "windows": {"form": "arched", "block": 164, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN_SURFACE, "deck": None, "headroom": 5,
}

DELTA_HOUSE = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONEBRICK, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN_SURFACE, "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 5,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": DARKOAK, "verge": DARK_LOG, "gable": PLASTER,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": STONEBRICK, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(162, 1),
    "windows": NO_WINDOW,
    "storeys": [DELTA_STOREY],
    "porch": None, "front": None,
    "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 164, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 5},
                "width": 2, "height": 3},
}

DELTA_HALL = json.loads(json.dumps(DELTA_HOUSE))
DELTA_HALL["roof"] = {"form": "hip", "pitch": 2, "slab": 126, "slabData": 5,
                      "overhang": 1, "ridgeCap": False, "hole": False,
                      "body": DARKOAK, "verge": DARK_LOG, "gable": None,
                      "gableWindows": NO_WINDOW}
DELTA_HALL["storeys"][0] = json.loads(json.dumps(DELTA_STOREY))
DELTA_HALL["storeys"][0]["clear"] = 7
DELTA_HALL["storeys"][0]["headroom"] = 7
DELTA_HALL["storeys"][0]["wall"]["extent"] = 7
DELTA_HALL["storeys"][0]["wall"]["stack"]["bands"][1]["thickness"] = 5

WOOL_ROOM = json.loads(json.dumps(DELTA_HOUSE))
WOOL_ROOM["roof"] = {"form": "flat", "pitch": 1, "slab": -1, "slabData": 0,
                     "overhang": 0, "ridgeCap": False, "hole": False,
                     "body": STONEBRICK, "verge": STONEBRICK, "gable": None,
                     "gableWindows": NO_WINDOW}
WOOL_ROOM["storeys"][0] = json.loads(json.dumps(DELTA_STOREY))
WOOL_ROOM["storeys"][0]["clear"] = 6
WOOL_ROOM["storeys"][0]["headroom"] = 6
WOOL_ROOM["storeys"][0]["wall"]["extent"] = 6
WOOL_ROOM["storeys"][0]["wall"]["stack"]["bands"] = [
    {"material": STONEBRICK, "thickness": 1},
    {"material": cells(7192, 4, 2, [PLASTER, STONEBRICK]), "thickness": 4},
    {"material": DARK_LOG, "thickness": 1}]

styles["delta-house"] = {"kind": "house", "shell": DELTA_HOUSE}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"carr": carr_theme, "reed": reed_theme, "works": works_theme},
    "mapTheme": "carr",
    # Swampland: grass tints #6a7039, which comes to meet podzol's brown so the
    # pair reads as one dark, leaf-littered floor. Read off /api/terrain/biomes.
    "biome": {"kind": "solid", "id": 6},
    "relief": relief,
    "addShapes": add_shapes,
    "addLayers": [quay_posts, quay_deck],
    "roomStyles": {"spawn": DELTA_HALL, "wool": WOOL_ROOM},
    "dressing": {"styles": styles, "props": props},
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
