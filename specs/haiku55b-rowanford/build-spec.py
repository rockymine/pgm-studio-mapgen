"""Writes the plan and the refinement for Rowan Ford, a destroy board for two teams.

Units: plan rects are in proxy cells (4 blocks each), origin at the symmetry centre. The refinement is in
blocks, absolute. The team-0 unit is authored on the west side; `mirror_x` fans it to the east. The river is
the void gap between the two banks, and a build zone bridges it.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "haiku55b-rowanford"


def plan():
    return {
        "plan": 2,
        "meta": {"name": "Rowan Ford", "authors": ["Haiku 5.5"],
                 "notes": "An autumn valley cut by a slow river. One monument a team, set forward on the bank."},
        "globals": {"cell": 4, "symmetry": "mirror_x", "maxPlayers": 16, "surface": 9},
        "pieces": [
            {"id": "highland-north", "rect": [-21, -11, 5, 9]},
            {"id": "spawn-highland", "role": "spawn", "rect": [-21, -2, 5, 4]},
            {"id": "highland-south", "rect": [-21, 2, 5, 9]},
            {"id": "bank", "rect": [-16, -11, 14, 22]},
        ],
        "zones": [{"id": "river-crossing", "rect": [-2, -11, 4, 22]}],
        "placements": {
            "spawns": [{"id": "spawn", "piece": "spawn-highland", "at": [2, 8], "facing": "right"}],
            "destroyables": [{"id": "monument", "piece": "bank", "at": [3, 6], "style": "pillar-3"}],
            "wools": [], "iron": [],
        },
        "walls": [],
        "boxes": [],
    }


def relief():
    return {"*": {
        "base": 9, "reach": 0, "step": 1,
        "marks": [
            {"id": "highland-crest", "kind": "area", "h": 13, "bevel": 1,
             "ring": [[-83, -43], [-65, -43], [-65, 43], [-83, 43]]},
            {"id": "bank-flat", "kind": "area", "h": 9, "bevel": 2,
             "ring": [[-60, -28], [-12, -28], [-12, 36], [-60, 36]]},
            {"id": "monument-pad", "kind": "area", "h": 9, "bevel": 2,
             "ring": [[-63, -44], [-49, -44], [-49, -30], [-63, -30]]},
        ],
        "pushes": [],
    }}


def themes():
    grass, dirt, coarse = {"kind": "solid", "id": 2}, {"kind": "solid", "id": 3}, {"kind": "solid", "id": 3, "data": 1}
    stone, andesite = {"kind": "solid", "id": 1}, {"kind": "solid", "id": 1, "data": 5}
    cobble = {"kind": "solid", "id": 4}
    return {"valley": {
        "bedrock": {"relative": False, "value": 1},
        "fill": stone,
        "wall": {"kind": "cell", "seed": 3, "cellSize": 3, "rise": 1, "palette": [stone, andesite]},
        "wallEnabled": True, "wallOnTerrainFaces": True,
        "surface": {"enabled": True, "depth": 3, "material": {"kind": "layered", "axis": "slope", "stack": {
            "ending": "repeat", "bands": [
                {"thickness": 30, "material": {"kind": "layered", "axis": "depth", "stack": {
                    "ending": "repeat", "bands": [{"thickness": 1, "material": grass},
                                                  {"thickness": 2, "material": dirt}]}}},
                {"thickness": 15, "material": {"kind": "cell", "seed": 5, "cellSize": 3, "rise": 1,
                                               "palette": [dirt, coarse]}},
                {"thickness": 45, "material": {"kind": "cell", "seed": 7, "cellSize": 3, "rise": 1,
                                               "palette": [stone, andesite, cobble]}},
            ]}}},
        "rim": {"enabled": False, "depth": 1, "material": stone},
        "rimEdges": "void",
    }}


def house(name, style, x0, z0, x1, z1, front=None):
    return {"id": name, "kind": "house", "style": style, "front": front,
            "wings": [{"corners": [[x0, z0], [x1, z1]], "spec": {"ridge": "alongX"}}]}


def refinement():
    west = [
        house("mill-west", "mill", -26, 8, -18, 16),
        house("store-west", "store", -44, 26, -36, 34),
        house("lookout-west", "lookout", -36, -20, -28, -12),
    ]
    east = []  # mirror_x fans each team-0 building onto team 1; an authored copy would collide with the fan
    return {
        "created": "2026-10-07",
        "biome": {"kind": "solid", "id": 35},
        "authors": ["Haiku 5.5"],
        "relief": relief(),
        "themes": themes(),
        "mapTheme": "valley",
        "roomStyles": {"spawn": {"library": "spruce-roofed-oak-cottage"}},
        "addShapes": [],  # no below-ground place yet: see review, a subtract cuts to the void
        "dressing": {
            "props": west + east,
            "styles": {
                "mill": {"library": "oak-framed-rubble-house", "kind": "house"},
                "store": {"library": "rubble-and-spruce-house", "kind": "house"},
                "lookout": {"library": "spruce-roofed-oak-cottage", "kind": "house"},
            },
        },
    }


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan(), handle, indent=2)
        handle.write("\n")
    with open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w") as handle:
        json.dump(refinement(), handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
