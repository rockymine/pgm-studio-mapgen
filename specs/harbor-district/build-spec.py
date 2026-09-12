#!/usr/bin/env python3
"""Harbor District — coastal mixed-game port."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "harbor-district"
CELL = 5

plan = {
    "plan": 1,
    "meta": {"name": "Harbor District"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16, "surface": 8},
    "pieces": [
        {"id": "spawn-blue", "role": "piece", "rect": [-40, -50, 18, 15], "surface": 8},
        {"id": "grass-blue", "role": "piece", "rect": [-40, -25, 18, 15], "surface": 8},
        {"id": "beach-blue", "role": "piece", "rect": [-40, 0, 18, 12], "surface": 7},
        {"id": "dock-blue", "role": "piece", "rect": [-40, 12, 18, 13], "surface": 8},

        {"id": "water", "role": "piece", "rect": [-15, -30, 30, 60], "surface": 5},

        {"id": "dock-red", "role": "piece", "rect": [22, 12, 18, 13], "surface": 8},
        {"id": "beach-red", "role": "piece", "rect": [22, 0, 18, 12], "surface": 7},
        {"id": "grass-red", "role": "piece", "rect": [22, -25, 18, 15], "surface": 8},
        {"id": "spawn-red", "role": "piece", "rect": [22, -50, 18, 15], "surface": 8},
    ],
    "walls": []
}

finish = {
    "themeByHeight": {
        "5": {"bucket": "water", "material": "water"},
        "7": {"bucket": "sand", "material": "sand"},
        "8": {"bucket": "grass", "material": "grass_block"}
    },
    "relief": {
        "coastal": {
            "pieces": ["grass-blue", "grass-red"],
            "marks": [
                {"id": "blue-slope", "kind": "radial", "at": [-31, -17], "r": 8, "h": 4, "tread": 0},
                {"id": "red-slope", "kind": "radial", "at": [31, -17], "r": 8, "h": 4, "tread": 0}
            ]
        }
    },
    "themes": {
        "grass": {
            "surfaces": ["spawn-blue", "spawn-red", "grass-blue", "grass-red"],
            "material": {"kind": "single", "material": "grass_block"}
        },
        "beach": {
            "surfaces": ["beach-blue", "beach-red"],
            "material": {"kind": "single", "material": "sand"}
        },
        "dock": {
            "surfaces": ["dock-blue", "dock-red"],
            "material": {"kind": "single", "material": "oak_planks"}
        },
        "water": {
            "surfaces": ["water"],
            "material": {"kind": "single", "material": "water"}
        }
    },
    "mapTheme": {"flood": {"kind": "simple", "material": "water"}}
}

os.makedirs(HERE, exist_ok=True)
with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as f:
    json.dump(plan, f, indent=1)
with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as f:
    json.dump(finish, f, indent=1)

print(f"✓ {SLUG}.plan.json")
print(f"✓ {SLUG}.finish.json")
