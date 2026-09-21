#!/usr/bin/env python3
"""opus5c-wetherslack — destroy the core. The approach dimension is BELOW.

A wooded gill with a beck down it, and the core standing on a vaulted terrace
built out over the gill's west side. The terrace's deck is flush with the
shoulder behind it, so from the west a player walks straight on; from the gill
floor the way at it is the undercroft underneath, entered by two mouths and
leaving by a shaft in the deck that comes up four blocks from the casing. The
two ways differ in dimension rather than in hand — one is across and one is
under — and nobody standing on the deck can see the second one coming.

Tone families: the ground is deep green moss and wet leaf, what is built is
pale birch and quartz on a stone plinth, and the accent is the gill's own
grey rock where the slope bands expose it.

Writes opus5c-wetherslack.plan.json and opus5c-wetherslack.finish.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from opus5c import (solid, cells, field, voronoi, band, stack, soil,
                    slope_stack, blob, wander_rect, tree_body, load_cache,
                    save_cache, write)

SLUG = "opus5c-wetherslack"
CELL = 4

# ---------------------------------------------------------------- the plan
#
# Two pieces a team and both at the board's own surface, in blocks:
#
#   slack      x -24..24   z  16..96    the gill, its shoulders and its floor
#   spawn      x   0..20   z  96..120   20 x 24, inside ST10's cap
#   mid-band   x -24..24   z -16..16    a build zone over 32 of void
#
# The spawn stands at the same height as the gill rather than on a shelf over
# it, so there is no riser to cut a ramp into and no seam for EL1 to walk flat.
# What gives this board its height is the relief and the terrace, and both are
# downstream of the plan — a piece that exists so a landform can be hung on it
# should have been a shape scope.
#
# The spawn is offset EAST of the centre line, which puts the walk out of the
# door on the gill's east shoulder and the core on its west: a defender
# returning and a raider arriving are on opposite sides of the beck for the
# whole length of it.

SPAWN_AT = (10, 108)
CORE_AT = (-4, 62)
SLACK_MIN = (-24, 16)

plan = {
    "plan": 2,
    "meta": {"name": "Wetherslack"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 18,
                "surface": 9},
    "pieces": [
        {"id": "slack", "role": "piece", "rect": [-6, 4, 12, 20], "surface": 9},
        {"id": "spawn", "role": "spawn", "rect": [0, 24, 5, 6], "surface": 9},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-6, -4, 12, 8], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-slack", "piece": "spawn",
                    "at": [10, 13], "facing": "front",
                    "footprint": [4, 7, 12, 12]}],
        "wools": [],
        "iron": [{"id": "iron-slack", "piece": "spawn", "at": [10.0, 3.5]}],
        "destroyables": [],
        # A core is breached where it stands, so it belongs where it will be
        # fought over and nothing is put between it and the middle. It NAMES
        # the deck's layer: a stacked board has a surface per layer, and a core
        # naming none seated on the terrain under the terrace instead — casing
        # at y18 over ground at y11, hanging in the undercroft's own airspace
        # with the deck running through it at y21.
        "cores": [{"id": "core", "piece": "slack",
                   "at": [CORE_AT[0] - SLACK_MIN[0], CORE_AT[1] - SLACK_MIN[1]],
                   "layer": "vault-deck",
                   "lava": 3, "float": 6, "leak": 5,
                   "name": "Wetherslack Cistern"}],
    },
    "walls": [],
}

# ---------------------------------------------------------------- the ground
#
# A gill is two shoulders and a floor, and the sides between them are pinned by
# nothing — which is where the ground gets its shape. Five marks, no push: the
# landform here is a valley, and a valley is what a relaxation makes between
# two heights when nothing in the middle argues with it.
#
# The beck is a LINE mark rather than an area, because a watercourse is a line
# and an area mark of that shape would pin a pan. It carries a tread, since a
# line pins every cell to the nearest pass of itself and two passes a winding
# apart put the whole difference in one cell.

relief = {
    "*": {
        "base": 9, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 1.3, "scale": 19, "seed": 5501},
        "marks": [
            {"id": "strand", "kind": "area", "h": 9, "bevel": 2,
             "ring": wander_rect(-26, 14, 26, 30, wobble=2.5, seed=5511)},
            # The tread is what decides how wide the water may be: it grades
            # the band's shoulder, so only 2*(half-width - tread) blocks in the
            # middle are pinned flat and the rest lofts. At tread 3 the channel
            # at radius 3 reached into the lofted part and DR-BANK read a
            # straight-sided wall three courses over the water's own line.
            {"id": "beck", "kind": "line", "width": 10, "tread": 2,
             "points": [[12, 30], [9, 50], [13, 70], [11, 92]],
             "h": [8, 8, 8, 8]},
            # A bevel grades inward from BOTH edges of a mark's ring, so a
            # bevel of 5 on a strip ten blocks wide leaves no flat core to pin
            # and the mark is silent — which is what RL4 read of the first cut
            # of this shoulder.
            #
            # And the gill carries ONE shoulder rather than two. A scar on the
            # west and a bank that grades away east is what a gill cut into a
            # dipping bed looks like, and two 10-wide shoulders in a board 48
            # across leave the beck's own band nothing to sit in — the second
            # one won the cells beside the water and stood a 20-block rim on
            # the bank the channel was about to be carved into.
            {"id": "shoulder-w", "kind": "area", "h": 21, "bevel": 4,
             "ring": wander_rect(-26, 30, -10, 92, wobble=2.0, seed=5512)},
            # the bench the terrace's walls stand on, stated LAST so it wins
            # the cells it shares with the west shoulder: the walls want a
            # level floor at 12 and the shoulder behind them wants 21
            {"id": "bench", "kind": "area", "h": 12, "bevel": 3,
             "ring": blob(-4, 62, 14, points=13, wobble=0.18, seed=5514)},
        ],
        "pushes": [],
    }
}

# ---------------------------------------------------------------- the terrace
#
# Two layers, and what they make is the air between them. The walls stand on
# the bench at base_y 12 and run nine courses to a segment top of 21; the deck
# rests at 21, which is one course over the west shoulder's own top block, so a
# player walks onto it from the shoulder with a single step up.
#
# The undercroft is ground nobody drew on. An opening is a gap between shapes
# rather than a subtract — SK13 reads a subtract as the board's negative space
# and refuses any add that fills it — so the walls are six rectangles with two
# mouths left between them, and the shaft is a four-block square the deck's own
# four rectangles are drawn around.

WALL_Y, DECK_Y = 12, 21
VAULT = cells(5521, 5, 3, [solid(98, 0), solid(98, 3), solid(4, 0)])
DECK_MAT = cells(5522, 4, 2, [solid(98, 0), solid(1, 0)])


def slab(sid, x0, z0, x1, z1, material):
    return {"id": sid, "type": "rectangle", "operation": "add", "floor": 0,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "material": material, "keepClear": True}


wall_shapes = [
    slab("vault-w", -16, 52, -14, 72, VAULT),
    slab("vault-n", -14, 70, 6, 72, VAULT),
    # the east mouth, onto the beck: the gap at z 60..64
    slab("vault-e-s", 6, 52, 8, 60, VAULT),
    slab("vault-e-n", 6, 64, 8, 72, VAULT),
    # the south mouth, onto the strand: the gap at x -6..-2
    slab("vault-s-w", -14, 52, -6, 54, VAULT),
    slab("vault-s-e", -2, 52, 6, 54, VAULT),
]
for shape in wall_shapes:
    shape["base_height"] = 9

deck_shapes = [
    slab("deck-s", -16, 52, 8, 56, DECK_MAT),
    slab("deck-n", -16, 60, 8, 72, DECK_MAT),
    slab("deck-w", -16, 56, -12, 60, DECK_MAT),
    slab("deck-e", -8, 56, 8, 60, DECK_MAT),
    # the shaft is x -12..-8, z 56..60 — the four blocks no rectangle covers
]
for shape in deck_shapes:
    shape["base_height"] = 1

vault_walls = {
    "id": "vault-walls", "name": "the vault's walls", "base_y": WALL_Y,
    "kind": "made", "part_of": "slack",
    "groups": [{"id": "vault-walls", "name": "the vault's walls",
                "mirrors": True,
                "shapeIds": [s["id"] for s in wall_shapes]}],
    "shapes": wall_shapes,
}

vault_deck = {
    "id": "vault-deck", "name": "the terrace deck", "base_y": DECK_Y,
    "kind": "made", "part_of": "slack",
    "groups": [{"id": "vault-deck", "name": "the terrace deck",
                "mirrors": True,
                "shapeIds": [s["id"] for s in deck_shapes]}],
    "shapes": deck_shapes,
}

# ---------------------------------------------------------------- the paint

MOSS = solid(2, 0)
EARTH = solid(3, 0)
WORN = solid(3, 1)
STONE = solid(1, 0)
COBBLE = solid(4, 0)
ANDESITE = solid(1, 5)
GRAVEL = solid(13, 0)
CLAY = solid(82, 0)
BIRCH = solid(5, 2)
QUARTZ = solid(155, 0)
DARKOAK = solid(5, 5)

GILL_ROCK = cells(5531, 7, 5, [STONE, COBBLE, ANDESITE])
GILL_BRAE = cells(5532, 7, 3, [WORN, GRAVEL, EARTH])

# cut off this board's own GET .../incline
SLOPE_FLAT, SLOPE_BRAE = 18, 34

gill_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5533, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": GILL_ROCK,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": slope_stack([
                    (SLOPE_FLAT, soil(MOSS, EARTH)),
                    (SLOPE_BRAE, soil(GILL_BRAE, EARTH)),
                    (90, stack("depth", [band(3, GILL_ROCK)])),
                ])},
}

flush_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5534, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": GILL_ROCK,
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": STONE},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5535, 7, 0, [GRAVEL, COBBLE, CLAY]),
                                 GRAVEL)},
}

garth_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": voronoi(5536, 9, [(5, STONE), (4, ANDESITE)]),
    "wall": cells(5537, 6, 4, [COBBLE, STONE]),
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": COBBLE},
    "rimEdges": "boundary",
    "surface": {"enabled": True, "depth": 3,
                "material": soil(cells(5538, 5, 0, [COBBLE, GRAVEL, STONE]),
                                 STONE)},
}

# ---------------------------------------------------------------- the shapes

GROUND = 9

add_shapes = [
    # the undercroft's own floor, marked with a shape rather than a stroke: a
    # stroke ignores `layer` and would come back on the deck. It will not
    # appear in themes/census either, which counts the top surface per column
    # and every cell of it has a deck over it.
    {"id": "vault-floor", "type": "rectangle", "operation": "add", "floor": 0,
     "min_x": -14, "min_z": 54, "max_x": 6, "max_z": 70,
     "base_height": GROUND, "theme": "garth"},
    {"id": "shoulder-flight", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "height_mode": "level", "skirt": 0,
     "keepClear": True,
     "anchor_heights": [21, 21, 12, 12],
     "material": cells(5545, 4, 2, [COBBLE, STONE, GRAVEL]),
     "vertices": [[-21.5, 38.3], [-26.5, 41.7], [-14.5, 59.7], [-9.5, 56.3]]},

    {"id": "shingle-lower", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "flush",
     "vertices": blob(11, 36, 9, points=13, wobble=0.26, seed=5541)},
    {"id": "shingle-upper", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "flush",
     "vertices": blob(12, 80, 8, points=13, wobble=0.26, seed=5542)},
    {"id": "shingle-mid", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "flush",
     "vertices": blob(10, 56, 7, points=11, wobble=0.24, seed=5543)},
    {"id": "spawn-yard", "type": "polygon", "operation": "add", "floor": 0,
     "base_height": GROUND, "theme": "garth",
     "vertices": wander_rect(0, 96, 20, 118, wobble=2.0, seed=5544)},
]

# ---------------------------------------------------------------- the dressing

cache_path = os.path.join(HERE, "trees.json")
cache = load_cache(cache_path)
OAK = tree_body("showcase-r11-5", cache)     # dense oak — the gill's wood
BIRCH_T = tree_body("showcase-r13-4", cache)  # birch — the shoulders
WILLOW = tree_body("showcase-r17-2", cache)   # willow — the beck
save_cache(cache_path, cache)

styles = {
    "oak": OAK,
    "birch": BIRCH_T,
    "willow": WILLOW,
    "gritstone": {"kind": "boulder", "form": "round", "size": 2, "mossy": False,
                  "rock": field(5551, 3, 3, [STONE, COBBLE, ANDESITE],
                                rise=3, kind="turbulence")},
    "mill": {"kind": "house", "shell": None},   # filled below
}

# dirt, coarse dirt and spruce planks: three blocks a reader cannot quite tell
# apart, which is what a path on soft ground is
PAVE = cells(5552, 3, 0, [EARTH, WORN, solid(5, 1)])

props = [
    {"id": "beck-water", "kind": "water", "seed": 5561, "shape": "channel",
     "points": [[12, 34], [9, 50], [13, 70], [11, 88]],
     "radius": 2, "depth": 2, "level": 6, "shore": 2, "shoreWander": True,
     "bank": cells(5562, 4, 0, [GRAVEL, CLAY, COBBLE])},

    {"id": "spawn-way", "kind": "stroke", "seed": 5571, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[10, 96], [14, 88], [18, 76], [20, 64], [20, 50]]},
    {"id": "shoulder-way", "kind": "stroke", "seed": 5572, "radius": 2,
     "style": "solid", "claimsGround": True, "pave": PAVE,
     "points": [[-20, 88], [-22, 76], [-22, 64], [-21, 56]]},

    {"id": "bank-house", "kind": "house", "seed": 5574, "style": "mill",
     "front": "posX",
     "wings": [{"corners": [[-13, 30], [-4, 36]], "spec": {"storeysHigh": 2}}]},
    {"id": "gill-house", "kind": "house", "seed": 5575, "style": "mill",
     "front": "posX",
     "wings": [{"corners": [[-15, 76], [-7, 81]], "spec": {"storeysHigh": 1}}]},
]

# Every position below sits on a cell POST .../sketch/seats marks legal for its
# own kind, and the willows stand on the beck's BANK rather than in it: a tree
# drawn on the channel's own cells is claimed by the water and is not in the
# world. Three of each, to the outside of the gill rather than down the middle
# of it, and none within four blocks of a road or of the flight's keep-clear.
props += [{"id": f"oak-{i}", "kind": "tree", "seed": 5600 + i,
           "x": x, "z": z, "style": "oak"}
          for i, (x, z) in enumerate([(-6, 42), (-20, 30), (-16, 93),
                                      (-14, 84), (-4, 84)])]
props += [{"id": f"birch-{i}", "kind": "tree", "seed": 5620 + i,
           "x": x, "z": z, "style": "birch"}
          for i, (x, z) in enumerate([(17, 42), (0, 25)])]
props += [{"id": f"willow-{i}", "kind": "tree", "seed": 5640 + i,
           "x": x, "z": z, "style": "willow"}
          for i, (x, z) in enumerate([(15, 30), (4, 35), (22, 78)])]
props += [{"id": f"gritstone-{i}", "kind": "boulder", "seed": 5660 + i,
           "x": x, "z": z, "style": "gritstone"}
          for i, (x, z) in enumerate([(-6, 25), (22, 88)])]

# A wooded gill is the one board of this run where ground cover is the place
# rather than a dressing over it, so the coverage is high and the fern share
# higher. The tall share stays low all the same: two-block grass in front of a
# core is cover nobody authored.
props += [
    {"id": "flora", "kind": "flora", "seed": 5580,
     "points": wander_rect(-24, 16, 24, 118, wobble=2.5, seed=5581),
     "spec": {"coverage": 0.34, "scale": 24, "octaves": 3, "fernShare": 0.38,
              "flowerShare": 0.08, "flowerScale": 16, "tallShare": 0.05}},
]

# ---------------------------------------------------------------- the house
#
# Forked from the shipped `alpine mining` preset, whose footing is already
# null. The ground is deep green moss, so what stands on it is pale birch and
# quartz over a stone plinth — a building has to read as a built thing from
# across the gill, which means its walls are not in the family under its feet.

BIRCH_LOG = {"kind": "laidLog", "id": 17, "data": 2}

PLAIN = {"field": None, "border": None, "borderWidth": 1, "inlay": None,
         "inlayInset": 2, "isPlain": True}
NO_WINDOW = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
             "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}

MILL_STOREY = {
    "clear": 5,
    "wall": {"stack": {"bands": [
        {"material": STONE, "thickness": 1},
        {"material": cells(5591, 3, 2, [QUARTZ, BIRCH]), "thickness": 3},
        {"material": BIRCH_LOG, "thickness": 1}], "ending": "repeat"},
        "extent": 5},
    "post": solid(17, 2),
    "windows": {"form": "arched", "block": 135, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "surface": PLAIN, "deck": None, "headroom": 5,
}

MILL = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONE, "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": PLAIN,
        "footing": None},
    "roof": {"form": "gable", "pitch": 2, "slab": 126, "slabData": 5,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": DARKOAK, "verge": STONE, "gable": BIRCH,
             "gableWindows": {"form": "open", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 1, "width": 1,
                              "height": 1, "spacing": 3}},
    "wall": {"stack": {"bands": [{"material": STONE, "thickness": 1}],
                       "ending": "repeat"}, "extent": 5},
    "post": solid(17, 2),
    "windows": NO_WINDOW,
    "storeys": [MILL_STOREY],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 2, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 135, "fill": "upperSlab",
                         "fillBlock": 126, "fillData": 2},
                "width": 2, "height": 3},
}

HALL = json.loads(json.dumps(MILL))
HALL["roof"] = {"form": "hip", "pitch": 2, "slab": 126, "slabData": 5,
                "overhang": 1, "ridgeCap": False, "hole": False,
                "body": DARKOAK, "verge": STONE, "gable": None,
                "gableWindows": NO_WINDOW}
HALL["storeys"][0] = json.loads(json.dumps(MILL_STOREY))
HALL["storeys"][0]["clear"] = 7
HALL["storeys"][0]["headroom"] = 7
HALL["storeys"][0]["wall"]["extent"] = 7
HALL["storeys"][0]["wall"]["stack"]["bands"][1]["thickness"] = 5

styles["mill"] = {"kind": "house", "shell": MILL}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    "themes": {"gill": gill_theme, "flush": flush_theme, "garth": garth_theme},
    "mapTheme": "gill",
    # Roofed forest (#79c05a): a deep wooded green for a board whose grass and
    # leaves are most of what a player sees. The palette states no podzol,
    # because that tint is too bright to meet brown and the pair would read as
    # neither ground. Asked of GET /api/terrain/biomes.
    "biome": {"kind": "solid", "id": 29},
    "relief": relief,
    "addShapes": add_shapes,
    # in base_y order, which is the order the world builds them in and what
    # SK20 complains about otherwise
    "addLayers": [vault_walls, vault_deck],
    "roomStyles": {"spawn": HALL, "wool": HALL},
    "dressing": {"styles": styles, "props": props},
}

write(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
