"""Writes the plan for haiku55-bracken-vale: a destroy-the-monument valley, two teams of 16.

Coordinates: the proxy grid is 4 blocks a cell, origin at the symmetry centre, and a rect
[x, z, w, h] covers cells x..x+w-1. Under rot_180 a rect maps to [-(x+w), z(-(z+h)), w, h], so
every piece below is stated once for the west team and fanned to the east.

    spawn-a  x -27..-23 ; hub-a x -22..-9 ; floor-a x -8..-5 ; mid x -4..3 (on the axis, fanned onto itself)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku55-bracken-vale"

plan = {
    "plan": 2,
    "meta": {
        "name": "Bracken Vale",
        "notes": "Destroy-the-monument valley. A slow river runs across the middle between two wooded banks.",
        "authors": ["Haiku 5.5"],
    },
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 10},
    "pieces": [
        {"id": "spawn-a", "role": "spawn", "rect": [-27, -3, 5, 6]},
        {"id": "hub-a", "rect": [-22, -10, 14, 20]},
        {"id": "floor-a", "rect": [-8, -10, 4, 20]},
        {"id": "mid", "rect": [-4, -10, 8, 20]},
    ],
    "zones": [],
    "walls": [],
    "placements": {
        "spawns": [{"id": "spawn-a-1", "piece": "spawn-a", "at": [4, 12], "facing": "right",
                        "footprint": [0, 2, 20, 20]}],
        "destroyables": [
            {"id": "monument-a", "piece": "hub-a", "at": [31, 40], "style": "cube-4",
             "materials": "ender stone", "float": 4, "name": "Bracken Monument"}
        ],
        "wools": [],
        "iron": [],
        "cores": [],
    },
}

with open(os.path.join(HERE, SLUG + ".plan.json"), "w") as f:
    json.dump(plan, f, indent=2)
    f.write("\n")
print("wrote", SLUG + ".plan.json")


# ---------------------------------------------------------------------------------------------
# The refinement: what a plan cannot state. Applied onto the compiled ground on every run.
# ---------------------------------------------------------------------------------------------

GRASS = {"kind": "solid", "id": 2}
DIRT = {"kind": "solid", "id": 3}
COARSE = {"kind": "solid", "id": 3, "data": 1}
STONE = {"kind": "solid", "id": 1}
ANDESITE = {"kind": "solid", "id": 1, "data": 5}
COBBLE = {"kind": "solid", "id": 4}
GRAVEL = {"kind": "solid", "id": 13}
SAND = {"kind": "solid", "id": 12}
SPRUCE_PLANKS = {"kind": "solid", "id": 5, "data": 1}


def layered_depth(bands):
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": bands}}


# The valley floor and its banks: meadow turf over two dirt, then stone on the steep flanks.
MEADOW = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
            {"thickness": 40, "material": layered_depth([
                {"thickness": 1, "material": GRASS}, {"thickness": 2, "material": DIRT}])},
            {"thickness": 10, "material": layered_depth([
                {"thickness": 1, "material": COARSE}, {"thickness": 2, "material": DIRT}])},
            {"thickness": 40, "material": {"kind": "cell", "seed": 11, "cellSize": 3, "jitter": 1,
                                           "warp": 1, "palette": [STONE, ANDESITE, COBBLE], "rise": 0}},
        ]}}},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": {"kind": "solid", "id": 1},
    "fill": {"kind": "solid", "id": 1},
}

# The path to each monument and the spawn walk: soft, three blocks laid a third each.
PATH = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "surface": {"enabled": True, "depth": 1, "material": {
        "kind": "cell", "seed": 31, "cellSize": 2, "jitter": 0, "warp": 0,
        "palette": [DIRT, COARSE, SPRUCE_PLANKS], "rise": 0}},
    "wallEnabled": False,
    "fill": {"kind": "solid", "id": 1},
}

refinement = {
    "authors": ["Haiku 5.5"],
    "created": "2026-10-07",
    "biome": {"kind": "solid", "id": 35},
    "themes": {"meadow": MEADOW, "path": PATH},
    "mapTheme": "meadow",
    "themeById": {},
    "relief": {
        "*": {
            "base": 10, "reach": 0, "step": 1,
            "marks": [
                # The monument bank stands a few blocks proud of the floor it rises from.
                {"id": "bank-a", "kind": "area", "h": 14, "bevel": 4,
                 "ring": [[-86, -34], [-34, -34], [-34, 34], [-86, 34]]},
            ],
            "pushes": [
                # The valley walls: a ridge along each flank, stopped short of the river so the
                # water meets the flat ground at the mouth of the valley rather than a cliff.
                {"id": "wall-north", "ring": [[-108, -36], [-36, -36], [-36, -20], [-108, -20]],
                 "amount": 14, "falloff": 12, "crown": 10, "roughness": 1, "seed": 7},
                {"id": "wall-south", "ring": [[36, 20], [108, 20], [108, 36], [36, 36]],
                 "amount": 14, "falloff": 12, "crown": 10, "roughness": 1, "seed": 8},
            ],
        }
    },
    "addShapes": [
        # The cellar under the hub: a void with a floor under it and a ceiling over it, open along the
        # north edge so a player drops in. The subtract is what removes the ground; the floor is an
        # override add six courses high; the ceiling sits on a made layer of its own.
        {"id": "cellar-void", "type": "rectangle", "operation": "subtract", "override": False,
         "keepClear": False, "floor": 6, "base_height": 5, "min_x": -52, "min_z": 14,
         "max_x": -40, "max_z": 26, "group": "team"},
        {"id": "cellar-floor", "type": "rectangle", "operation": "add", "override": True,
         "keepClear": False, "floor": 0, "base_height": 6, "relief_scope": "exclude", "min_x": -52, "min_z": 14,
         "max_x": -40, "max_z": 26, "material": {"kind": "solid", "id": 1}, "group": "team"},
        # The two ways a team walks: spawn to its monument, and monument to the bridge. Laid
        # on the ground they stand on, so the path owns the top course and nothing beneath it.
        {"id": "path-spawn-a", "type": "rectangle", "operation": "add", "override": False,
         "keepClear": False, "min_x": -104, "min_z": -2, "max_x": -58, "max_z": 2,
         "base_height": 14, "theme": "path", "group": "team"},
        {"id": "path-bridge-a", "type": "rectangle", "operation": "add", "override": False,
         "keepClear": False, "min_x": -56, "min_z": -2, "max_x": -20, "max_z": 2,
         "base_height": 14, "theme": "path", "group": "team"},
    ],
    "addLayers": [
        {"id": "cellar-roof", "name": "The cellar's roof", "base_y": 0, "below": False, "kind": "made",
         "part_of": "cellar", "shapes": [
            {"id": "cellar-roof-plate", "type": "rectangle", "operation": "add", "override": False,
             "keepClear": False, "floor": 11, "base_height": 3, "min_x": -52, "min_z": 14,
             "max_x": -40, "max_z": 22, "material": {"kind": "solid", "id": 1}}],
         "groups": [{"id": "cellar-roof", "name": "The cellar's roof", "mirrors": True,
                     "shapeIds": ["cellar-roof-plate"]}]},
        {"id": "bridge", "name": "Bridge", "base_y": 14, "below": False, "kind": "made",
         "part_of": "river-bridge", "shapes": [
            {"id": "bridge-deck", "type": "rectangle", "operation": "add", "override": False,
             "keepClear": False, "min_x": -12, "min_z": -3, "max_x": 12, "max_z": 3,
             "theme": "path"}],
         "groups": []},
    ],
    "roomStyles": {"spawn": {"library": "oak-and-spruce-timbered-house"}},
    "dressing": {
        "styles": {
            "mill": {"kind": "house", "library": "oak-stilt-house"},
            "cottage": {"kind": "house", "library": "oak-and-spruce-timbered-house"},
            "barn": {"kind": "house", "library": "hay-gambrel-barn"},
            "oak-9": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
            "birch-8": {"kind": "tree", "form": "template", "species": "birch", "height": 8},
        },
        "props": [
            # The river: a canal down the valley, a shore of gravel and sand where it meets the land.
            {"kind": "fluid", "id": "river", "shape": "channel", "form": "canal", "layer": "ground",
             "points": [[-2, -40], [5, -28], [-4, -14], [3, 2], [-3, 16], [4, 28], [-1, 40]],
             "radius": 9, "depth": 4, "level": 9, "shore": 3, "shoreWander": True, "edge": 2,
             "bank": {"kind": "cell", "seed": 41, "cellSize": 3, "jitter": 1, "warp": 1,
                      "palette": [GRAVEL, SAND], "rise": 0}},
            # One watermill a bank: a stilt house with the river under its floor.
            {"kind": "house", "id": "mill-a", "layer": "ground", "seed": 5, "front": "posX",
             "style": "mill", "wings": [{"corners": [[-30, -12], [-20, -5]], "spec": {"ridge": "alongZ"}}]},
            {"kind": "house", "id": "cottage-a", "layer": "ground", "seed": 6, "front": "posZ",
             "style": "cottage", "wings": [{"corners": [[-38, 6], [-28, 13]], "spec": {"ridge": "alongX"}}]},
            {"kind": "house", "id": "barn-a", "layer": "ground", "seed": 7, "front": "posX",
             "style": "barn", "wings": [{"corners": [[-72, 18], [-60, 26]], "spec": {"ridge": "alongZ"}}]},
            {"kind": "tree", "id": "oak-a1", "seed": 21, "x": -46, "z": 8, "style": "oak-9"},
            {"kind": "tree", "id": "oak-a2", "seed": 22, "x": -72, "z": -30, "style": "oak-9"},
            {"kind": "tree", "id": "birch-a1", "seed": 23, "x": -64, "z": 28, "style": "birch-8"},
            {"kind": "tree", "id": "birch-a2", "seed": 24, "x": -84, "z": 26, "style": "birch-8"},
            {"kind": "tree", "id": "birch-a3", "seed": 25, "x": -34, "z": 24, "style": "birch-8"},
        ],
    },
}

with open(os.path.join(HERE, SLUG + ".refinement.json"), "w") as f:
    json.dump(refinement, f, indent=2)
    f.write("\n")
print("wrote", SLUG + ".refinement.json")
