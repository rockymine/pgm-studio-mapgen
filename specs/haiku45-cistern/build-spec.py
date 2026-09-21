#!/usr/bin/env python3
"""Cistern — destroy the core. Scarp structure with core placement."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku45-cistern"

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

def layered(bands, axis="depth", ending="repeat"):
    stack = {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}
    return {"kind": "layered", "axis": axis, "stack": stack}

GRASS, DIRT, STONE, ANDESITE = solid(2, 0), solid(3, 0), solid(1, 0), solid(1, 5)
LOW, HIGH = 12, 17

# Scarp structure with core (lava 2-5 range)
plan = {
    "plan": 2,
    "meta": {"name": "Cistern"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": LOW, "observerY": 48},
    "pieces": [
        {"id": "hill", "role": "piece", "rect": [-3, -2, 6, 4], "surface": HIGH, "mirrors": False},
        {"id": "pasture", "role": "piece", "rect": [-11, 4, 14, 4], "surface": LOW},
        {"id": "platform", "role": "piece", "rect": [-11, 8, 10, 6], "surface": HIGH},
        {"id": "lane", "role": "piece", "rect": [-1, 8, 4, 6], "surface": LOW},
        {"id": "spawn-area", "role": "spawn", "rect": [-11, 14, 4, 3], "surface": LOW},
        {"id": "spawn-center", "role": "piece", "rect": [-7, 14, 6, 3], "surface": LOW},
        {"id": "dressing", "role": "piece", "rect": [-1, 14, 4, 3], "surface": LOW},
    ],
    "zones": [
        {"id": "pass", "rect": [-11, -4, 22, 8], "kind": "build"}
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-center", "at": [15, 8], "facing": "front",
             "footprint": [6, 3, 18, 9]}
        ],
        "iron": [
            {"id": "iron-1", "piece": "spawn-center", "at": [2, 7]},
            {"id": "iron-2", "piece": "spawn-center", "at": [28, 7]}
        ],
        "destroyables": [],
        "cores": [
            {"id": "core", "piece": "hill", "at": [0, 0], "lava": 3, "lavaHeight": 2,
             "float": 1, "leak": 1, "name": "The Cistern"}
        ],
        "wools": [],
    },
    "walls": [],
    "boxes": [],
}

relief = {
    "*": {
        "base": LOW, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.6, "scale": 12, "seed": 4701},
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
