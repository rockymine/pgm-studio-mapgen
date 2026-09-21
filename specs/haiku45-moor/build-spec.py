#!/usr/bin/env python3
"""Haiku45-moor: Capture the Wool board with central barrier."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku45-moor"

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

def layered(bands, axis="depth", ending="repeat"):
    stack = {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}
    return {"kind": "layered", "axis": axis, "stack": stack}

GRASS, DIRT, STONE, ANDESITE = solid(2, 0), solid(3, 0), solid(1, 0), solid(1, 5)
COARSE = solid(3, 1)
BASE_Y, HIGH_Y = 20, 26

plan = {
    "plan": 2,
    "meta": {"name": "Moor"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": BASE_Y, "observerY": 48},
    "pieces": [
        # Central barrier (non-mirrored)
        {"id": "hill", "role": "piece", "rect": [-4, -4, 8, 8], "surface": HIGH_Y, "mirrors": False},
        # Wool platforms on sides (fanned/mirrored)
        {"id": "wool-high", "role": "piece", "rect": [6, -8, 4, 4], "surface": HIGH_Y},
        # Spawn zone (non-mirrored, center)
        {"id": "spawn-zone", "role": "spawn", "rect": [-8, 16, 16, 3], "surface": BASE_Y, "mirrors": False},
        # Approach lanes (non-mirrored)
        {"id": "lane-a", "role": "piece", "rect": [-12, -4, 6, 8], "surface": BASE_Y, "mirrors": False},
        {"id": "lane-b", "role": "piece", "rect": [6, -4, 6, 8], "surface": BASE_Y, "mirrors": False},
    ],
    "zones": [],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-zone", "at": [40, 6], "facing": "front",
             "footprint": [8, 3, 16, 9]},
        ],
        "iron": [
            {"id": "iron-1", "piece": "spawn-zone", "at": [10, 5]},
            {"id": "iron-2", "piece": "spawn-zone", "at": [30, 5]},
        ],
        "destroyables": [],
        "cores": [],
        "wools": [
            {"id": "wool-team-a", "piece": "wool-high", "at": [2, 1]},
        ],
    },
    "walls": [],
    "boxes": [],
}

relief = {
    "*": {
        "base": BASE_Y, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.5, "scale": 14, "seed": 4703},
        "marks": [
            {"id": "base-level", "kind": "area", "h": BASE_Y, "bevel": 0,
             "ring": [[-60, -50], [60, -50], [60, 80], [-60, 80]]},
            {"id": "hill-top", "kind": "area", "h": HIGH_Y, "bevel": 2,
             "ring": [[-20, -20], [20, -20], [20, 20], [-20, 20]]},
        ],
        "pushes": [
            {"id": "mound", "ring": [[-25, -25], [25, -25], [25, 25], [-25, 25]],
             "amount": 3, "falloff": 8, "crown": 1, "roughness": 0, "seed": 72}
        ]
    }
}

# Meadow theme
MEADOW_SURFACE = layered([
    (20, GRASS),
    (30, DIRT),
    (50, STONE)
], axis="slope")

# Grass/dirt theme
GRASS_SURFACE = layered([
    (25, GRASS),
    (40, DIRT),
    (60, COARSE)
], axis="slope")

themes = {
    "meadow": {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE,
        "wall": ANDESITE,
        "wallEnabled": True,
        "rim": {"enabled": True, "depth": 1, "material": GRASS},
        "rimEdges": "void",
        "surface": {"enabled": True, "depth": 3, "material": MEADOW_SURFACE}
    },
    "grass": {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE,
        "wall": ANDESITE,
        "wallEnabled": True,
        "rim": {"enabled": True, "depth": 1, "material": GRASS},
        "rimEdges": "void",
        "surface": {"enabled": True, "depth": 3, "material": GRASS_SURFACE}
    }
}

addShapes = [
    {"id": "grass-hill", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": HIGH_Y, "theme": "grass",
     "vertices": [[-20, -20], [20, -20], [20, 20], [-20, 20]]}
]

dressing = {
    "styles": {
        "oak-8": {"kind": "tree", "form": "template", "species": "oak", "height": 8},
        "oak-10": {"kind": "tree", "form": "template", "species": "oak", "height": 10},
        "boulder-2": {"kind": "boulder", "form": "round", "size": 2, "mossy": True,
                      "rock": "granite"},
        "boulder-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": True,
                      "rock": "granite"}
    },
    "props": [
        {"id": "tree-1", "kind": "tree", "seed": 3001, "x": -80, "z": -40, "style": "oak-8"},
        {"id": "tree-2", "kind": "tree", "seed": 3002, "x": -60, "z": -35, "style": "oak-10"},
        {"id": "tree-3", "kind": "tree", "seed": 3003, "x": 50, "z": 30, "style": "oak-8"},
        {"id": "tree-4", "kind": "tree", "seed": 3004, "x": 70, "z": 35, "style": "oak-10"},
        {"id": "boulder-1", "kind": "boulder", "seed": 4001, "x": -90, "z": -50, "style": "boulder-3"},
        {"id": "boulder-2", "kind": "boulder", "seed": 4002, "x": 60, "z": 40, "style": "boulder-2"}
    ]
}

finish = {
    "authors": ["Claude Haiku 4.5"],
    "created": "2026-09-21",
    "themes": themes,
    "mapTheme": "meadow",
    "relief": relief,
    "addShapes": addShapes,
    "addLayers": [],
    "roomStyles": {
        "spawn": {
            "floor": {"material": GRASS},
            "ceiling": {"height": 8, "material": solid(52, 0)},
            "wall": {"material": ANDESITE}
        },
        "default": {
            "floor": {"material": GRASS},
            "ceiling": {"height": 6, "material": solid(52, 0)},
            "wall": {"material": ANDESITE}
        }
    },
    "dressing": dressing
}

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=1)

write_json(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write_json(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
print(f"Wrote {SLUG}.plan.json and {SLUG}.finish.json")
