#!/usr/bin/env python3
"""
haiku45-moor: Capture the Wool board

A moorland capture board with two wools placed high on opposite hillsides.
Central terrain rises as a shared barrier that both teams navigate around.
Wools are positioned to require travelling across open ground or skirting the hill.

Plan: 8 pieces, asymmetric to create terrain flow
- hill: central high terrain
- wool-north-east, wool-south-west: platforms for wool placement
- passage-north, passage-south, passage-center: lanes for team movement
- spawn-left, spawn-right: team spawns

Relief: minimal grain only, keeping focus on piece arrangement.
Themes: slope-axis layered ground surface, emphasizing angle over height.
"""

import json
import math

def solid(i, d=0):
    """Material: solid color/texture at given data value."""
    return {"kind": "solid", "id": i, "data": d}

def layered(bands, axis="depth", ending="repeat"):
    """Material: layered stack of materials with thickness bands.

    bands: list of (thickness, material) tuples
    axis: "depth" (Y), "slope" (terrain angle), "height" (Y bands)
    ending: "repeat" or "clamp"
    """
    stack = {
        "ending": ending,
        "bands": [{"thickness": t, "material": m} for t, m in bands]
    }
    return {"kind": "layered", "axis": axis, "stack": stack}

# ============================================================================
# PLAN
# ============================================================================

plan = {
    "kind": "plan",
    "pieces": [
        # Central hill - high terrain
        {
            "name": "hill",
            "kind": "rectangle",
            "at": {"x": -5, "z": -6},
            "size": {"x": 10, "z": 12},
            "base_y": 23,
        },
        # Wool placement areas
        {
            "name": "wool-north-east",
            "kind": "rectangle",
            "at": {"x": 8, "z": -8},
            "size": {"x": 4, "z": 4},
            "base_y": 28,
        },
        {
            "name": "wool-south-west",
            "kind": "rectangle",
            "at": {"x": -12, "z": 8},
            "size": {"x": 4, "z": 4},
            "base_y": 28,
        },
        # Passages for team movement
        {
            "name": "passage-north",
            "kind": "rectangle",
            "at": {"x": 5, "z": -12},
            "size": {"x": 8, "z": 3},
            "base_y": 20,
        },
        {
            "name": "passage-south",
            "kind": "rectangle",
            "at": {"x": -13, "z": 10},
            "size": {"x": 8, "z": 3},
            "base_y": 20,
        },
        {
            "name": "passage-center",
            "kind": "rectangle",
            "at": {"x": -2, "z": -1},
            "size": {"x": 4, "z": 2},
            "base_y": 21,
        },
        # Team spawns
        {
            "name": "spawn-left",
            "kind": "rectangle",
            "at": {"x": -17, "z": -8},
            "size": {"x": 4, "z": 4},
            "base_y": 19,
        },
        {
            "name": "spawn-right",
            "kind": "rectangle",
            "at": {"x": 13, "z": 8},
            "size": {"x": 4, "z": 4},
            "base_y": 19,
        },
    ],
}

# ============================================================================
# FINISH
# ============================================================================

# Ground material: slope-axis layering
ground_material = layered([
    (30, solid("grass_block")),
    (15, solid("dirt")),
    (45, solid("stone")),
], axis="slope", ending="repeat")

finish = {
    "kind": "finish",
    "themes": {
        "ground": {
            "buckets": {
                "surface": ground_material,
                "fill": solid("dirt"),
                "bedrock": solid("bedrock"),
            },
        },
    },
    "placements": {
        "wools": [
            {
                "kind": "wool",
                "color": "red",
                "location": {"piece": "wool-north-east", "at": [2, 1]},
            },
            {
                "kind": "wool",
                "color": "blue",
                "location": {"piece": "wool-south-west", "at": [2, 1]},
            },
        ],
    },
    "relief": {
        "grain": {"amplitude": 0.5, "frequency": 0.05},
    },
}

# ============================================================================
# OUTPUT
# ============================================================================

if __name__ == "__main__":
    import sys

    plan_file = f"{sys.argv[1]}.plan.json"
    finish_file = f"{sys.argv[1]}.finish.json"

    with open(plan_file, "w") as f:
        json.dump(plan, f, indent=2)

    with open(finish_file, "w") as f:
        json.dump(finish, f, indent=2)

    print(f"✓ {plan_file}")
    print(f"✓ {finish_file}")
