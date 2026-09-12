#!/usr/bin/env python3
"""Quarry Clash — CTF in layered quarry."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "quarry-clash"
CELL = 5

plan = {
    "plan": 1,
    "meta": {"name": "Quarry Clash"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 10, "surface": 9},
    "pieces": [
        {"id": "rim-blue", "role": "piece", "rect": [-40, -40, 18, 15], "surface": 13},
        {"id": "shelf-blue", "role": "piece", "rect": [-40, -15, 18, 15], "surface": 10},
        {"id": "floor-blue", "role": "piece", "rect": [-40, 10, 18, 15], "surface": 7},

        {"id": "center", "role": "piece", "rect": [-15, -20, 30, 40], "surface": 9},

        {"id": "floor-red", "role": "piece", "rect": [22, 10, 18, 15], "surface": 7},
        {"id": "shelf-red", "role": "piece", "rect": [22, -15, 18, 15], "surface": 10},
        {"id": "rim-red", "role": "piece", "rect": [22, -40, 18, 15], "surface": 13},
    ],
    "walls": []
}

finish = {
    "themeByHeight": {
        "7": {"bucket": "stone", "material": "gravel"},
        "9": {"bucket": "stone", "material": "stone"},
        "10": {"bucket": "stone", "material": "cobblestone"},
        "13": {"bucket": "stone", "material": "andesite"}
    },
    "relief": {
        "quarry": {
            "pieces": ["rim-blue", "rim-red", "center"],
            "marks": [
                {"id": "rim-blue-edge", "kind": "radial", "at": [-31, -32], "r": 7, "h": 8, "tread": 0},
                {"id": "rim-red-edge", "kind": "radial", "at": [31, -32], "r": 7, "h": 8, "tread": 0}
            ]
        }
    },
    "themes": {
        "stone": {
            "surfaces": ["rim-blue", "rim-red", "shelf-blue", "shelf-red", "floor-blue", "floor-red", "center"],
            "material": {"kind": "single", "material": "stone"}
        }
    },
    "mapTheme": {"flood": {"kind": "simple", "material": "stone"}}
}

os.makedirs(HERE, exist_ok=True)
with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as f:
    json.dump(plan, f, indent=1)
with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as f:
    json.dump(finish, f, indent=1)

print(f"✓ {SLUG}.plan.json")
print(f"✓ {SLUG}.finish.json")
