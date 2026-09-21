"""sonnet5b-highgarth-fell — a red-earth hill-fort, played for a wool and a monument at once.

Identity: each team must both hold a beacon standing exposed on the open rampart and
carry a wool out of a stone grain-store tucked into the fort's corner, so the defence
is split between a goal that cannot be moved and one that must be walked home.

Writes sonnet5b-highgarth-fell.plan.json and sonnet5b-highgarth-fell.finish.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet5b-highgarth-fell"


def write(name, doc):
    with open(os.path.join(HERE, f"{SLUG}.{name}.json"), "w") as f:
        json.dump(doc, f, indent=1)


plan = {
    "plan": 2,
    "meta": {"name": "Highgarth Fell"},
    "globals": {
        "cell": 4,
        "symmetry": "rot_180",
        "maxPlayers": 8,
        "surface": 11,
    },
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-30, -3, 5, 7]},
        {"id": "yard", "role": "piece", "rect": [-25, -8, 21, 16]},
        {"id": "approach", "role": "piece", "rect": [-24, 8, 5, 4]},
        {"id": "wool-room", "role": "wool-room", "rect": [-24, 12, 5, 6]},
    ],
    "zones": [
        {"id": "strait", "rect": [-4, -8, 8, 16], "kind": "build"},
    ],
    "walls": [
        {"a": "approach", "b": "yard"},
    ],
    "placements": {
        "spawns": [
            {"id": "red-spawn", "piece": "spawn", "at": [10, 14], "facing": "right",
             "footprint": [2, 4, 16, 20]},
        ],
        "wools": [
            {"id": "red-wool", "piece": "wool-room", "at": [10, 12],
             "footprint": [2, 2, 16, 20]},
        ],
        "destroyables": [
            {"id": "red-beacon", "piece": "yard", "at": [38, 32],
             "style": "pillar-3", "materials": "obsidian", "float": 4,
             "name": "Highgarth Beacon"},
        ],
    },
}

write("plan", plan)
print("wrote", SLUG + ".plan.json")

# --------------------------------------------------------------- the finish --

RED_SAND = {"kind": "solid", "id": 12, "data": 1}
RED_SANDSTONE = {"kind": "solid", "id": 179, "data": 0}
SMOOTH_RED_SANDSTONE = {"kind": "solid", "id": 181, "data": 8}
COARSE_DIRT = {"kind": "solid", "id": 3, "data": 1}
DIRT = {"kind": "solid", "id": 3, "data": 0}
STONE = {"kind": "solid", "id": 1, "data": 0}
CHISELED_STONE_BRICK = {"kind": "solid", "id": 98, "data": 3}
STONE_BRICK = {"kind": "solid", "id": 98, "data": 0}
GRASS = {"kind": "solid", "id": 2, "data": 0}
ANDESITE = {"kind": "solid", "id": 1, "data": 5}
OAK_PLANKS = {"kind": "solid", "id": 5, "data": 0}
ACACIA_LOG = {"kind": "solid", "id": 162, "data": 0}


def depth_stack(top, under, thickness=3):
    return {
        "kind": "layered", "axis": "depth",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 1, "material": top},
            {"thickness": thickness - 1, "material": under},
        ]},
    }


fell_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": RED_SANDSTONE,
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": RED_SANDSTONE,
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 20, "material": depth_stack(GRASS, DIRT)},
            {"thickness": 20, "material": depth_stack(COARSE_DIRT, RED_SAND)},
            {"thickness": 50, "material": depth_stack(RED_SANDSTONE, STONE)},
        ]},
    }},
    "rim": {"enabled": True, "depth": 1, "material": SMOOTH_RED_SANDSTONE},
    "rimEdges": "void",
}

# --- the store: forked from "counting house" (id 9) ---
store_style = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": RED_SANDSTONE, "thickness": 1}], "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": STONE_BRICK, "verge": STONE_BRICK, "gable": RED_SANDSTONE,
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                          "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": {
        "stack": {"bands": [
            {"material": CHISELED_STONE_BRICK, "thickness": 2},
            {"material": RED_SANDSTONE, "thickness": 5},
        ], "ending": "repeat"},
        "extent": 7,
    },
    "post": ACACIA_LOG,
    "windows": {"form": "stairLattice", "block": 163, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 4, "width": 2, "height": 2, "spacing": 3},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": 162, "data": 0, "reach": 1, "any": False},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 163, "fill": "upperSlab", "fillBlock": 126, "fillData": 4},
                "width": 2, "height": 3},
}

hall_style = dict(store_style)
hall_style["roof"] = dict(store_style["roof"])
hall_style["roof"]["form"] = "gable"
hall_style["wall"] = {
    "stack": {"bands": [
        {"material": RED_SANDSTONE, "thickness": 3},
        {"material": OAK_PLANKS, "thickness": 4},
    ], "ending": "repeat"},
    "extent": 7,
}

finish = {
    "created": "2026-09-21",
    "authors": ["Sonnet 5"],
    "themes": {"fell": fell_theme},
    "mapTheme": "fell",
    "roomStyles": {"spawn": hall_style, "wool": store_style},
    "relief": {
        "team": {"base": 11, "reach": 0, "step": 1, "marks": []}
    },
    "dressing": {
        "styles": {
            "windbent": {"kind": "tree", "form": "template", "species": "acacia", "height": 7},
            "fell-rock": {"kind": "boulder", "form": "outcrop", "size": 2.4, "rock": ANDESITE, "mossy": False},
        },
        "props": [
            {"kind": "flora", "id": "fell-cover",
             "points": [[-100, -32], [-16, -32], [-16, 32], [-100, 32]],
             "spec": {"coverage": 0.25, "scale": 9, "octaves": 3, "fernShare": 0.1,
                      "flowerShare": 0.1, "flowerScale": 6, "tallShare": 0.08}},
            {"kind": "stroke", "id": "fell-road",
             "points": [[-110, 2], [-62, 0]], "radius": 2, "style": "solid",
             "claimsGround": True,
             "pave": {"kind": "cell", "seed": 31, "cellSize": 3, "jitter": 55, "warp": 2,
                       "palette": [DIRT, COARSE_DIRT, RED_SAND], "rise": 0}},
            {"kind": "stroke", "id": "store-path",
             "points": [[-86, 32], [-86, 68]], "radius": 2, "style": "worn", "coverage": 0.7,
             "claimsGround": True,
             "pave": {"kind": "cell", "seed": 33, "cellSize": 3, "jitter": 55, "warp": 2,
                       "palette": [DIRT, COARSE_DIRT, RED_SAND], "rise": 0}},
            {"kind": "tree", "id": "windbent-1", "x": -40, "z": -22, "style": "windbent", "routeStandoff": 3},
            {"kind": "tree", "id": "windbent-2", "x": -35, "z": 20, "style": "windbent", "routeStandoff": 3},
            {"kind": "boulder", "id": "fellrock-1", "x": -25, "z": -18, "style": "fell-rock", "routeStandoff": 2},
            {"kind": "boulder", "id": "fellrock-2", "x": -25, "z": 18, "style": "fell-rock", "routeStandoff": 2},
            {"kind": "boulder", "id": "fellrock-3", "x": -70, "z": -24, "style": "fell-rock", "routeStandoff": 2},
        ],
    },
}

write("finish", finish)
print("wrote", SLUG + ".finish.json")
