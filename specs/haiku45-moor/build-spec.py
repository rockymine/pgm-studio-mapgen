#!/usr/bin/env python3
"""haiku45-moor: Capture the Wool board. Two wools on opposite terrain."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku45-moor"

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

def layered(bands, axis="depth", ending="repeat"):
    stack = {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}
    return {"kind": "layered", "axis": axis, "stack": stack}

GRASS, DIRT, STONE, ANDESITE = solid(2, 0), solid(3, 0), solid(1, 0), solid(1, 5)
BASE_Y = 20

# Simple CTW: two wools on opposite terrain (mirrored)
plan = {
    "plan": 2,
    "meta": {"name": "Moor"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": BASE_Y, "observerY": 48},
    "pieces": [
        # Central barrier
        {"id": "hill", "role": "piece", "rect": [-5, -4, 10, 8], "surface": BASE_Y},
        # Wool platforms (mirrored in rot_180)
        {"id": "wool-high", "role": "piece", "rect": [8, -10, 4, 3], "surface": 26},
        # Large spawn area
        {"id": "spawn-zone", "role": "spawn", "rect": [-8, 14, 16, 4], "surface": BASE_Y},
    ],
    "zones": [
        {"id": "main", "rect": [-12, -10, 28, 28], "kind": "build"}
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-zone", "at": [40, 8], "facing": "front",
             "footprint": [8, 4, 16, 10]},
        ],
        "iron": [
            {"id": "iron-1", "piece": "spawn-zone", "at": [4, 8]},
            {"id": "iron-2", "piece": "spawn-zone", "at": [28, 8]},
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
        "grain": {"amplitude": 0.6, "scale": 12, "seed": 4703},
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
