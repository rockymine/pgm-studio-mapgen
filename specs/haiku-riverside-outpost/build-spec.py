#!/usr/bin/env python3
"""Riverside Trading Post — simple CTW with clear non-overlapping pieces."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "riverside-outpost"
CELL = 5

plan = {
    "plan": 2,
    "meta": {"name": "Riverside Outpost"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12, "surface": 8},
    "pieces": [
        {"id": "spawn-blue", "role": "piece", "rect": [-40, -25, 15, 10], "surface": 8},
        {"id": "approach-blue", "role": "piece", "rect": [-40, -5, 15, 10], "surface": 8},
        {"id": "river", "role": "piece", "rect": [-5, -15, 10, 30], "surface": 6},
        {"id": "spawn-red", "role": "piece", "rect": [25, 15, 15, 10], "surface": 8},
        {"id": "approach-red", "role": "piece", "rect": [25, -5, 15, 10], "surface": 8},
        {"id": "outpost", "role": "piece", "rect": [-8, -5, 16, 10], "surface": 10},
    ],
    "walls": [],
    "placements": {
        "spawns": [
            {"id": "spawn-blue-1", "piece": "spawn-blue", "at": [-32, -20], "facing": "north"},
            {"id": "spawn-red-1", "piece": "spawn-red", "at": [32, 20], "facing": "south"}
        ],
        "woolRooms": [
            {"id": "wool-room-1", "piece": "outpost", "at": [0, 0]}
        ],
        "wools": [
            {"id": "wool-1", "location": {"piece": "outpost", "at": [0, 0], "line": [[-10, -10], [10, 10]]}, "laneWidth": 40, "laneLength": [30, 110]}
        ]
    }
}

finish = {
    "themeByHeight": {
        "6": {"bucket": "water", "material": "water"},
        "8": {"bucket": "grass", "material": "grass_block"},
        "10": {"bucket": "stone", "material": "stone"}
    },
    "relief": {
        "terrain": {
            "pieces": ["approach-blue", "approach-red"],
            "marks": [
                {"id": "blue-slope", "kind": "radial", "at": [-32, 0], "r": 8, "h": 5, "tread": 0},
                {"id": "red-slope", "kind": "radial", "at": [32, 0], "r": 8, "h": 5, "tread": 0}
            ]
        }
    },
    "themes": {
        "grass": {
            "surfaces": ["spawn-blue", "spawn-red", "approach-blue", "approach-red"],
            "material": {"kind": "single", "material": "grass_block"}
        },
        "water": {
            "surfaces": ["river"],
            "material": {"kind": "single", "material": "water"}
        },
        "stone": {
            "surfaces": ["outpost"],
            "material": {"kind": "single", "material": "stone"}
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
