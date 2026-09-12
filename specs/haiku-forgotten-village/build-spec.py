#!/usr/bin/env python3
"""Forgotten Village — snow-themed king-of-the-hill."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "forgotten-village"
CELL = 5

plan = {
    "plan": 1,
    "meta": {"name": "Forgotten Village"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12, "surface": 8, "biome": "snowy_taiga"},
    "pieces": [
        {"id": "spawn-blue", "role": "piece", "rect": [-50, -45, 20, 15], "surface": 8},
        {"id": "slope-blue", "role": "piece", "rect": [-50, -20, 20, 20], "surface": 9},

        {"id": "peak", "role": "piece", "rect": [-15, -15, 30, 30], "surface": 12},

        {"id": "slope-red", "role": "piece", "rect": [30, -20, 20, 20], "surface": 9},
        {"id": "spawn-red", "role": "piece", "rect": [30, -45, 20, 15], "surface": 8},
    ],
    "walls": []
}

finish = {
    "themeByHeight": {
        "8": {"bucket": "grass", "material": "grass_block"},
        "9": {"bucket": "grass", "material": "grass_block"},
        "12": {"bucket": "snow", "material": "snow_block"}
    },
    "relief": {
        "mountain": {
            "pieces": ["slope-blue", "slope-red", "peak"],
            "marks": [
                {"id": "peak-summit", "kind": "radial", "at": [0, 0], "r": 12, "h": 16, "tread": 1}
            ]
        }
    },
    "themes": {
        "snow": {
            "surfaces": ["spawn-blue", "spawn-red", "slope-blue", "slope-red"],
            "material": {"kind": "single", "material": "grass_block"}
        },
        "peak": {
            "surfaces": ["peak"],
            "material": {"kind": "single", "material": "snow_block"}
        }
    },
    "mapTheme": {"flood": {"kind": "simple", "material": "snow_block"}}
}

os.makedirs(HERE, exist_ok=True)
with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as f:
    json.dump(plan, f, indent=1)
with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as f:
    json.dump(finish, f, indent=1)

print(f"✓ {SLUG}.plan.json")
print(f"✓ {SLUG}.finish.json")
