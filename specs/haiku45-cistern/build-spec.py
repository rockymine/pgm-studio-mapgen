#!/usr/bin/env python3
"""Cistern — destroy the core in an open well.

Core floated above a deep well. Two spawns flank it on level ground. Symmetric approaches, open center.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku45-cistern"

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

def layered(bands, axis="depth", ending="repeat"):
    stack = {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}
    return {"kind": "layered", "axis": axis, "stack": stack}

GRASS, DIRT, STONE, ANDESITE = solid(2, 0), solid(3, 0), solid(1, 0), solid(1, 5)

BASE_Y = 20

plan = {
    "plan": 2,
    "meta": {"name": "Cistern"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": BASE_Y, "observerY": 54},
    "pieces": [
        {"id": "ground", "role": "piece", "rect": [-11, 4, 22, 12], "surface": BASE_Y},
        {"id": "spawn-left", "role": "spawn", "rect": [-11, 14, 4, 3], "surface": BASE_Y},
        {"id": "spawn-right", "role": "piece", "rect": [-7, 14, 6, 3], "surface": BASE_Y},
        {"id": "spawn-extra", "role": "piece", "rect": [-1, 14, 4, 3], "surface": BASE_Y},
    ],
    "zones": [
        {"id": "middle", "rect": [-11, -2, 22, 18], "kind": "build"}
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-right", "at": [15, 8], "facing": "front",
             "footprint": [6, 3, 18, 9]}
        ],
        "iron": [
            {"id": "iron-1", "piece": "spawn-right", "at": [2, 7]},
            {"id": "iron-2", "piece": "spawn-right", "at": [28, 7]}
        ],
        "destroyables": [],
        "cores": [
            {"id": "core", "piece": "ground", "at": [0, 10], "lava": 3, "lavaHeight": 3,
             "float": 6, "leak": 5, "name": "The Cistern"}
        ],
        "wools": [],
    },
    "walls": [],
    "boxes": [],
}

relief = {
    "*": {
        "base": BASE_Y, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.5, "scale": 10, "seed": 4701},
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
