#!/usr/bin/env python3
"""Haiku45-bastion: Mixed wool + monument board."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku45-bastion"

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

def layered(bands, axis="depth", ending="repeat"):
    stack = {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}
    return {"kind": "layered", "axis": axis, "stack": stack}

GRASS, DIRT, STONE, ANDESITE = solid(2, 0), solid(3, 0), solid(1, 0), solid(1, 5)
COARSE = solid(3, 1)
BASE_Y, MON_Y, WOOL_Y = 22, 30, 27

plan = {
    "plan": 2,
    "meta": {"name": "Bastion"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": BASE_Y, "observerY": 50},
    "pieces": [
        # Monument tower (non-mirrored, center)
        {"id": "tower", "role": "piece", "rect": [-4, -4, 8, 8], "surface": MON_Y, "mirrors": False},
        # Wool platform (fanned)
        {"id": "wool-platform", "role": "piece", "rect": [6, -6, 5, 5], "surface": WOOL_Y},
        # Spawn zone (non-mirrored)
        {"id": "spawn-zone", "role": "spawn", "rect": [-10, 16, 20, 3], "surface": BASE_Y, "mirrors": False},
        # Approach lanes
        {"id": "lane-a", "role": "piece", "rect": [-14, -2, 8, 8], "surface": BASE_Y, "mirrors": False},
        {"id": "lane-b", "role": "piece", "rect": [6, -2, 8, 8], "surface": BASE_Y, "mirrors": False},
    ],
    "zones": [],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-zone", "at": [40, 6], "facing": "front",
             "footprint": [8, 3, 20, 10]},
        ],
        "iron": [
            {"id": "iron-1", "piece": "spawn-zone", "at": [12, 5]},
            {"id": "iron-2", "piece": "spawn-zone", "at": [32, 5]},
        ],
        "destroyables": [
            {"id": "monument", "piece": "", "at": [0, 0], "style": "pillar-3",
             "materials": "obsidian", "float": 2, "name": "The Bastion"}
        ],
        "cores": [],
        "wools": [
            {"id": "wool-team-a", "piece": "wool-platform", "at": [2, 1]},
        ],
    },
    "walls": [],
    "boxes": [],
}

relief = {
    "*": {
        "base": BASE_Y, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.5, "scale": 14, "seed": 5001},
        "marks": [
            {"id": "base-level", "kind": "area", "h": BASE_Y, "bevel": 0,
             "ring": [[-70, -50], [70, -50], [70, 80], [-70, 80]]},
            {"id": "tower-top", "kind": "area", "h": MON_Y, "bevel": 2,
             "ring": [[-20, -20], [20, -20], [20, 20], [-20, 20]]},
            {"id": "wool-bench", "kind": "area", "h": WOOL_Y, "bevel": 1,
             "ring": [[30, -30], [60, -30], [60, 0], [30, 0]]},
        ],
        "pushes": [
            {"id": "tower-swell", "ring": [[-25, -25], [25, -25], [25, 25], [-25, 25]],
             "amount": 3, "falloff": 8, "crown": 1.5, "roughness": 0, "seed": 123}
        ]
    }
}

# Stone theme for tower
STONE_SURFACE = layered([
    (25, STONE),
    (40, COARSE),
    (65, GRASS)
], axis="slope")

# Grass theme for approaches
GRASS_SURFACE = layered([
    (20, GRASS),
    (35, DIRT),
    (55, COARSE)
], axis="slope")

themes = {
    "stone": {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE,
        "wall": ANDESITE,
        "wallEnabled": True,
        "rim": {"enabled": True, "depth": 1, "material": COARSE},
        "rimEdges": "void",
        "surface": {"enabled": True, "depth": 3, "material": STONE_SURFACE}
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
    {"id": "stone-tower", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": MON_Y, "theme": "stone",
     "vertices": [[-20, -20], [20, -20], [20, 20], [-20, 20]]}
]

dressing = {
    "styles": {
        "oak-9": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
        "oak-11": {"kind": "tree", "form": "template", "species": "oak", "height": 11},
        "boulder-2": {"kind": "boulder", "form": "round", "size": 2, "mossy": True,
                      "rock": "granite"},
        "boulder-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": True,
                      "rock": "granite"}
    },
    "props": [
        {"id": "tree-1", "kind": "tree", "seed": 5001, "x": -90, "z": -45, "style": "oak-9"},
        {"id": "tree-2", "kind": "tree", "seed": 5002, "x": -70, "z": -40, "style": "oak-11"},
        {"id": "tree-3", "kind": "tree", "seed": 5003, "x": 60, "z": 35, "style": "oak-9"},
        {"id": "tree-4", "kind": "tree", "seed": 5004, "x": 80, "z": 40, "style": "oak-11"},
        {"id": "boulder-1", "kind": "boulder", "seed": 6001, "x": -100, "z": -50, "style": "boulder-3"},
        {"id": "boulder-2", "kind": "boulder", "seed": 6002, "x": 70, "z": 45, "style": "boulder-2"}
    ]
}

finish = {
    "authors": ["Claude Haiku 4.5"],
    "created": "2026-09-21",
    "themes": themes,
    "mapTheme": "grass",
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
