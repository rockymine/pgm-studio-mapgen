#!/usr/bin/env python3
"""haiku45-bastion: Mixed Wool + Monument board."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku45-bastion"

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

def layered(bands, axis="depth", ending="repeat"):
    stack = {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}
    return {"kind": "layered", "axis": axis, "stack": stack}

GRASS, DIRT, STONE, ANDESITE = solid(2, 0), solid(3, 0), solid(1, 0), solid(1, 5)
BASE_Y = 20

# Mixed board: monument tower, wool platform, spawns, non-overlapping pieces
plan = {
    "plan": 2,
    "meta": {"name": "Bastion"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": BASE_Y, "observerY": 48},
    "pieces": [
        # Central tower
        {"id": "tower", "role": "piece", "rect": [-2, -2, 4, 4], "surface": BASE_Y},
        # Monument on tower (high)
        {"id": "monument-peak", "role": "piece", "rect": [-1, -3, 2, 1], "surface": 30},
        # Wool platform (offset, non-overlapping)
        {"id": "wool-platform", "role": "piece", "rect": [4, 1, 3, 3], "surface": 27},
        # Defense terraces (non-overlapping)
        {"id": "rampart-left", "role": "piece", "rect": [-8, -1, 3, 5], "surface": 22},
        # Shared spawn
        {"id": "spawn-zone", "role": "spawn", "rect": [-5, 6, 10, 3], "surface": BASE_Y},
    ],
    "zones": [
        {"id": "main", "rect": [-8, -3, 16, 12], "kind": "build"}
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-zone", "at": [25, 6], "facing": "front",
             "footprint": [5, 3, 10, 9]},
        ],
        "iron": [
            {"id": "iron-1", "piece": "spawn-zone", "at": [2, 6]},
            {"id": "iron-2", "piece": "spawn-zone", "at": [18, 6]},
        ],
        "destroyables": [
            {"id": "monument", "piece": "monument-peak", "at": [0, 0], "style": "pillar-3",
             "materials": "obsidian", "float": 2, "leak": 1, "name": "The Bastion"}
        ],
        "cores": [],
        "wools": [
            {"id": "wool", "piece": "wool-platform", "at": [1, 1]},
        ],
    },
    "walls": [],
    "boxes": [],
}

relief = {
    "*": {
        "base": BASE_Y, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.6, "scale": 12, "seed": 4704},
        "marks": [],
        "pushes": []
    }
}

GROUND_SURFACE = layered([
    (20, layered([(1, GRASS), (1, DIRT)])),
    (30, layered([(1, DIRT), (2, STONE)])),
    (50, solid(1, 0))
], axis="slope")

themes = {
    "ground": {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE,
        "wall": ANDESITE,
        "wallEnabled": True,
        "rim": {"enabled": True, "depth": 1, "material": GRASS},
        "rimEdges": "void",
        "surface": {"enabled": True, "depth": 3, "material": GROUND_SURFACE}
    }
}

finish = {
    "authors": ["Claude Haiku 4.5"],
    "created": "2026-09-21",
    "themes": themes,
    "mapTheme": "ground",
    "relief": relief,
    "addShapes": [],
    "addLayers": [],
    "roomStyles": {},
    "dressing": {"styles": {}, "props": []}
}

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=1)

write_json(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write_json(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
print(f"Wrote {SLUG}.plan.json and {SLUG}.finish.json")
