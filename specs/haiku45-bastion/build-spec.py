#!/usr/bin/env python3
"""
haiku45-bastion: Mixed Wool + Monument board

A fortified structure board combining monument destruction and wool capture objectives.
Central high tower holds the monument; wool is positioned for team advancement.
Design emphasizes dual objectives requiring different tactical approaches.

Plan: 8 pieces
- tower: central elevated structure
- monument-peak: platform for monument placement
- wool-ledge: wool placement area
- rampart-left, rampart-right: defensive terraces
- approach-north, approach-south: team advances
- spawn-center: shared spawn area between teams

Relief: minimal grain only.
Themes: slope-axis layered ground, emphasizing structural contrast.
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
        # Central tower structure
        {
            "name": "tower",
            "kind": "rectangle",
            "at": {"x": -3, "z": -3},
            "size": {"x": 6, "z": 6},
            "base_y": 25,
        },
        # Monument platform at peak
        {
            "name": "monument-peak",
            "kind": "rectangle",
            "at": {"x": -1, "z": -1},
            "size": {"x": 2, "z": 2},
            "base_y": 30,
        },
        # Wool placement on side ledge
        {
            "name": "wool-ledge",
            "kind": "rectangle",
            "at": {"x": 5, "z": -1},
            "size": {"x": 3, "z": 3},
            "base_y": 27,
        },
        # Defensive terraces
        {
            "name": "rampart-left",
            "kind": "rectangle",
            "at": {"x": -10, "z": -3},
            "size": {"x": 4, "z": 6},
            "base_y": 22,
        },
        {
            "name": "rampart-right",
            "kind": "rectangle",
            "at": {"x": 7, "z": -3},
            "size": {"x": 4, "z": 6},
            "base_y": 22,
        },
        # Team approach areas
        {
            "name": "approach-north",
            "kind": "rectangle",
            "at": {"x": -3, "z": -9},
            "size": {"x": 6, "z": 4},
            "base_y": 20,
        },
        {
            "name": "approach-south",
            "kind": "rectangle",
            "at": {"x": -3, "z": 6},
            "size": {"x": 6, "z": 4},
            "base_y": 20,
        },
        # Shared spawn
        {
            "name": "spawn-center",
            "kind": "rectangle",
            "at": {"x": -2, "z": 12},
            "size": {"x": 4, "z": 3},
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
        "objectives": [
            {
                "kind": "monument",
                "name": "The Bastion",
                "location": {"piece": "monument-peak", "at": [1, 1]},
                "float": 3,
                "leak": 2,
            },
            {
                "kind": "wool",
                "color": "green",
                "location": {"piece": "wool-ledge", "at": [1, 1]},
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
