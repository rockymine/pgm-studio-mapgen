#!/usr/bin/env python3
"""Scarp — DTM board with monument on central hill.

Simple 120x100 cell board: spawn regions, monument hill, connecting lanes.
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
COARSE = solid(3, 1)

# Heights
LOW, HIGH = 32, 40

# Simple plan: 24 cells × 20 cells = 120 blocks × 100 blocks
plan = {
    "plan": 2,
    "meta": {"name": "Scarp"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 16, "surface": LOW, "observerY": 48},
    "pieces": [
        # Spawn piece - does not fan (one spawn at center)
        {"id": "spawn-a", "role": "spawn", "rect": [-12, -10, 8, 4], "surface": LOW, "mirrors": False},
        # Monument hill in center - stands alone, non-mirrored
        {"id": "hill", "role": "piece", "rect": [-4, -2, 8, 4], "surface": HIGH, "mirrors": False},
        # Approach lanes - non-mirrored to stay with hill
        {"id": "lane-a", "role": "piece", "rect": [-12, -2, 6, 4], "surface": LOW, "mirrors": False},
        {"id": "lane-b", "role": "piece", "rect": [4, -2, 6, 4], "surface": LOW, "mirrors": False},
        # Neutral area - mirrored
        {"id": "neutral", "role": "piece", "rect": [-8, 6, 16, 4], "surface": LOW},
    ],
    "zones": [],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-a", "at": [15, 10], "facing": "front",
             "footprint": [6, 3, 18, 9]}
        ],
        "iron": [
            {"id": "iron-1", "piece": "spawn-a", "at": [8, 6]},
            {"id": "iron-2", "piece": "spawn-a", "at": [18, 6]}
        ],
        "destroyables": [
            {"id": "monument", "piece": "", "at": [0, 0], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "The Scarp"}
        ],
        "cores": [],
        "wools": [],
    },
    "walls": [],
    "boxes": [],
}

# Relief with marks and push
relief = {
    "*": {
        "base": LOW, "reach": 0, "step": 1, "landform": "rolling",
        "grain": {"amplitude": 0.4, "scale": 12, "seed": 4601},
        "marks": [
            # Spawn platform
            {"id": "spawn-level", "kind": "area", "h": LOW, "bevel": 0,
             "ring": [[-60, -50], [60, -50], [60, 30], [-60, 30]]},
            # Hill top
            {"id": "hilltop", "kind": "area", "h": HIGH, "bevel": 2,
             "ring": [[-20, -10], [20, -10], [20, 10], [-20, 10]]},
        ],
        "pushes": [
            # Central swell
            {"id": "swell", "ring": [[-25, -15], [25, -15], [25, 15], [-25, 15]],
             "amount": 3, "falloff": 8, "crown": 1, "roughness": 0, "seed": 42}
        ]
    }
}

# Meadow theme - grass
MEADOW_SURFACE = layered([
    (20, GRASS),
    (30, DIRT),
    (50, STONE)
], axis="slope")

# Stone theme - rocky
STONE_SURFACE = layered([
    (35, STONE),
    (50, COARSE),
    (65, GRASS)
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
    "stone": {
        "bedrock": {"relative": False, "value": 1},
        "fill": STONE,
        "wall": ANDESITE,
        "wallEnabled": True,
        "rim": {"enabled": True, "depth": 1, "material": COARSE},
        "rimEdges": "void",
        "surface": {"enabled": True, "depth": 3, "material": STONE_SURFACE}
    }
}

# Stone patch on hill
addShapes = [
    {"id": "stone-hill", "type": "polygon", "operation": "add",
     "floor": 0, "base_height": HIGH, "theme": "stone",
     "vertices": [[-20, -10], [20, -10], [20, 10], [-20, 10]]}
]

# Props
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
        {"id": "tree-1", "kind": "tree", "seed": 1001, "x": -80, "z": -40, "style": "oak-9"},
        {"id": "tree-2", "kind": "tree", "seed": 1002, "x": -60, "z": -35, "style": "oak-11"},
        {"id": "tree-3", "kind": "tree", "seed": 1003, "x": 50, "z": 20, "style": "oak-9"},
        {"id": "tree-4", "kind": "tree", "seed": 1004, "x": 70, "z": 25, "style": "oak-11"},
        {"id": "boulder-1", "kind": "boulder", "seed": 2001, "x": -90, "z": -45, "style": "boulder-3"},
        {"id": "boulder-2", "kind": "boulder", "seed": 2002, "x": 60, "z": 30, "style": "boulder-2"}
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
