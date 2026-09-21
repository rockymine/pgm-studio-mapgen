"""sonnet5b-white-scarp — a wind-scoured chalk down, destroy-the-monument.

Identity: each team's beacon monument stands alone on open sward, a quarry cut into
one flank and a stand of wind-bent pines guarding the other, the two teams' ground
joined only by a build zone over void.

Writes sonnet5b-white-scarp.plan.json and sonnet5b-white-scarp.finish.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet5b-white-scarp"


def write(name, doc):
    with open(os.path.join(HERE, f"{SLUG}.{name}.json"), "w") as f:
        json.dump(doc, f, indent=1)


# ---------------------------------------------------------------- the plan --

plan = {
    "plan": 2,
    "meta": {"name": "White Scarp"},
    "globals": {
        "cell": 4,
        "symmetry": "rot_180",
        "maxPlayers": 8,
        "surface": 10,
    },
    "pieces": [
        {
            "id": "spawn",
            "role": "spawn",
            "rect": [-26, -3, 5, 6],
        },
        {
            "id": "field",
            "role": "piece",
            "rect": [-21, -8, 17, 16],
        },
    ],
    "zones": [
        {
            "id": "strait",
            "rect": [-4, -8, 8, 16],
            "kind": "build",
        }
    ],
    "placements": {
        "spawns": [
            {
                "id": "red-spawn",
                "piece": "spawn",
                "at": [10, 12],
                "facing": "right",
                "footprint": [2, 6, 16, 12],
            }
        ],
        "destroyables": [
            {
                "id": "red-monument",
                "piece": "field",
                "at": [33, 40],
                "style": "pillar-3",
                "materials": "obsidian",
                "float": 4,
                "name": "White Scarp Beacon",
            }
        ],
    },
    "walls": [],
}

write("plan", plan)
print("wrote", SLUG + ".plan.json")

# --------------------------------------------------------------- the finish --

STONE = {"kind": "solid", "id": 1, "data": 0}
COBBLE = {"kind": "solid", "id": 4, "data": 0}
ANDESITE = {"kind": "solid", "id": 1, "data": 5}
GRASS = {"kind": "solid", "id": 2, "data": 0}
DIRT = {"kind": "solid", "id": 3, "data": 0}
COARSE_DIRT = {"kind": "solid", "id": 3, "data": 1}
SANDSTONE = {"kind": "solid", "id": 24, "data": 0}
SMOOTH_SANDSTONE = {"kind": "solid", "id": 24, "data": 2}
STONE_BRICK = {"kind": "solid", "id": 98, "data": 0}
CHISELED_STONE_BRICK = {"kind": "solid", "id": 98, "data": 3}
SPRUCE_PLANKS = {"kind": "solid", "id": 5, "data": 1}


def depth_stack(top, under, thickness=3):
    return {
        "kind": "layered", "axis": "depth",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 1, "material": top},
            {"thickness": thickness - 1, "material": under},
        ]},
    }


chalk_down_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": STONE,
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": SANDSTONE,
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 20, "material": depth_stack(GRASS, DIRT)},
            {"thickness": 20, "material": depth_stack(COARSE_DIRT, DIRT)},
            {"thickness": 50, "material": depth_stack(SANDSTONE, STONE)},
        ]},
    }},
    "rim": {"enabled": True, "depth": 1, "material": SMOOTH_SANDSTONE},
    "rimEdges": "void",
}

# --- the spawn hall: forked from the "desert brick" preset (id 2) ---
hall_style = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": SANDSTONE, "thickness": 1}], "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": STONE_BRICK, "verge": STONE_BRICK, "gable": SMOOTH_SANDSTONE,
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                          "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": {
        "stack": {"bands": [
            {"material": CHISELED_STONE_BRICK, "thickness": 2},
            {"material": SANDSTONE, "thickness": 5},
        ], "ending": "repeat"},
        "extent": 7,
    },
    "post": None,
    "windows": {"form": "stairLattice", "block": 135, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 4, "width": 2, "height": 2, "spacing": 3},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 135, "fill": "upperSlab", "fillBlock": 126, "fillData": 2},
                "width": 2, "height": 3},
}

finish = {
    "created": "2026-09-21",
    "authors": ["Sonnet 5"],
    "themes": {"chalk-down": chalk_down_theme},
    "mapTheme": "chalk-down",
    "roomStyles": {"spawn": hall_style},
    "relief": {
        "team": {
            "base": 10, "reach": 0, "step": 1,
            "marks": [
                {"id": "quarry", "kind": "area", "h": 4, "bevel": 5,
                 "ring": [[-78, -30], [-64, -30], [-64, -13], [-78, -13]]},
            ],
            "pushes": [
                {"id": "knoll", "ring": [[-80, 12], [-55, 12], [-55, 30], [-80, 30]],
                 "amount": 5, "falloff": 12, "crown": 0, "roughness": 3, "seed": 7},
            ],
        }
    },
    "dressing": {
        "styles": {
            "pine": {"kind": "tree", "form": "template", "species": "spruce", "height": 9},
            "chalk-erratic": {"kind": "boulder", "form": "outcrop", "size": 2.2, "rock": ANDESITE, "mossy": False},
        },
        "props": [
            {"kind": "flora", "id": "sward-cover",
             "points": [[-84, -32], [-16, -32], [-16, 32], [-84, 32]],
             "spec": {"coverage": 0.35, "scale": 9, "octaves": 3, "fernShare": 0.2,
                      "flowerShare": 0.12, "flowerScale": 6, "tallShare": 0.1}},
            {"kind": "stroke", "id": "beacon-path",
             "points": [[-92, 0], [-56, 0]], "radius": 2, "style": "solid",
             "claimsGround": True,
             "pave": {"kind": "cell", "seed": 11, "cellSize": 3, "jitter": 60, "warp": 2,
                       "palette": [DIRT, COARSE_DIRT, SPRUCE_PLANKS], "rise": 0}},
            {"kind": "tree", "id": "pine-1", "x": -68, "z": 18, "style": "pine", "routeStandoff": 3},
            {"kind": "tree", "id": "pine-2", "x": -60, "z": 26, "style": "pine", "routeStandoff": 3},
            {"kind": "tree", "id": "pine-3", "x": -72, "z": 30, "style": "pine", "routeStandoff": 3},
            {"kind": "tree", "id": "pine-4", "x": -63, "z": 14, "style": "pine", "routeStandoff": 3},
            {"kind": "boulder", "id": "erratic-1", "x": -66, "z": -30, "style": "chalk-erratic", "routeStandoff": 2},
            {"kind": "boulder", "id": "erratic-2", "x": -74, "z": -18, "style": "chalk-erratic", "routeStandoff": 2},
            {"kind": "boulder", "id": "erratic-3", "x": -30, "z": -18, "style": "chalk-erratic", "routeStandoff": 2},
        ],
    },
}

write("finish", finish)
print("wrote", SLUG + ".finish.json")
