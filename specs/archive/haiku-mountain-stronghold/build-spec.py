#!/usr/bin/env python3
"""Mountain Pass Stronghold — simple DTM with clear terrain."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "mountain-stronghold"
CELL = 5

plan = {
    "plan": 1,
    "meta": {"name": "Mountain Stronghold"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 14, "surface": 8},
    "pieces": [
        {"id": "spawn-blue", "role": "piece", "rect": [-35, -30, 12, 10], "surface": 8},
        {"id": "valley-blue", "role": "piece", "rect": [-35, -10, 12, 15], "surface": 8},
        {"id": "peak-blue", "role": "piece", "rect": [-35, 5, 12, 15], "surface": 14},

        {"id": "center", "role": "piece", "rect": [-15, -15, 30, 30], "surface": 9},

        {"id": "peak-red", "role": "piece", "rect": [23, 5, 12, 15], "surface": 14},
        {"id": "valley-red", "role": "piece", "rect": [23, -10, 12, 15], "surface": 8},
        {"id": "spawn-red", "role": "piece", "rect": [23, -30, 12, 10], "surface": 8},
    ],
    "walls": []
}

finish = {
    "themeByHeight": {
        "8": {"bucket": "stone", "material": "stone"},
        "9": {"bucket": "stone", "material": "gravel"},
        "14": {"bucket": "stone", "material": "cobblestone"}
    },
    "relief": {
        "mountains": {
            "pieces": ["peak-blue", "peak-red", "center"],
            "marks": [
                {"id": "peak-blue-summit", "kind": "radial", "at": [-29, 12], "r": 8, "h": 12, "tread": 1},
                {"id": "peak-red-summit", "kind": "radial", "at": [29, 12], "r": 8, "h": 12, "tread": 1}
            ]
        }
    },
    "themes": {
        "stone": {
            "surfaces": ["spawn-blue", "spawn-red", "valley-blue", "valley-red", "peak-blue", "peak-red", "center"],
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
