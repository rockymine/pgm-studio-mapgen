#!/usr/bin/env python3
"""Scarp — destroy the monument on a hill.

Based on opus5-heftfold structure: two yards, one hill. Monument on the high terrace, spawns on the pasture
below. One destroyable, one approach each from the sides.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku45-scarp"

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

def stack(bands, ending="repeat"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="repeat"):
    return {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}

# Materials
GRASS = solid(2, 0)
DIRT = solid(3, 0)
STONE = solid(1, 0)
ANDESITE = solid(1, 5)

# Plan based on opus5-heftfold: 22×34 cells = 110×170 blocks
# Three surfaces
LOW, HIGH, MID = 12, 17, 14

plan = {
    "plan": 2,
    "meta": {"name": "Scarp"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": LOW, "observerY": 48},
    "pieces": [
        # Monument hill on high ground
        {"id": "hill", "role": "piece", "rect": [-3, -2, 6, 4], "surface": HIGH, "mirrors": False},
        # Low pasture
        {"id": "pasture", "role": "piece", "rect": [-11, 4, 14, 4], "surface": LOW},
        # Monument platform
        {"id": "platform", "role": "piece", "rect": [-11, 8, 10, 6], "surface": HIGH},
        # Lane and build
        {"id": "lane", "role": "piece", "rect": [-1, 8, 4, 6], "surface": LOW},
        # Spawn area
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
        "destroyables": [
            {"id": "monument", "piece": "hill", "at": [0, 0], "style": "pillar-3",
             "materials": "obsidian", "float": 5, "leak": 4, "name": "The Scarp"}
        ],
        "cores": [],
        "wools": [],
    },
    "walls": [],
    "boxes": [],
}

# Simple relief with grain
relief = {
    "*": {
        "base": LOW, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.6, "scale": 12, "seed": 4601},
        "marks": [],
        "pushes": []
    }
}

# Ground theme with slope-based finish
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

addShapes = []

dressing = {"styles": {}, "props": []}

finish = {
    "authors": ["Claude Haiku 4.5"],
    "created": "2026-09-21",
    "themes": themes,
    "mapTheme": "ground",
    "relief": relief,
    "addShapes": addShapes,
    "addLayers": [],
    "roomStyles": {},
    "dressing": dressing
}

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=1)

write_json(os.path.join(HERE, f"{SLUG}.plan.json"), plan)
write_json(os.path.join(HERE, f"{SLUG}.finish.json"), finish)
print(f"Wrote {SLUG}.plan.json and {SLUG}.finish.json")
