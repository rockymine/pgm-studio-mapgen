"""sonnet5b-ropeworks-quay — a fishing harbour, capture-the-wool.

Identity: each team's wool sits in a stone cellar tucked into a corner off the yard,
one prepared wall guarding the cellar's outer approach about twenty blocks out, and
the two teams' quays are joined only by a build zone over the tidal strait.

Writes sonnet5b-ropeworks-quay.plan.json and sonnet5b-ropeworks-quay.finish.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet5b-ropeworks-quay"


def write(name, doc):
    with open(os.path.join(HERE, f"{SLUG}.{name}.json"), "w") as f:
        json.dump(doc, f, indent=1)


plan = {
    "plan": 2,
    "meta": {"name": "Ropeworks Quay"},
    "globals": {
        "cell": 4,
        "symmetry": "rot_180",
        "maxPlayers": 8,
        "surface": 9,
    },
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-48, -3, 5, 7]},
        {"id": "yard", "role": "piece", "rect": [-43, -8, 39, 16]},
        {"id": "approach", "role": "piece", "rect": [-15, 8, 5, 4]},
        {"id": "wool-room", "role": "wool-room", "rect": [-15, 12, 5, 6]},
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
    },
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
GRAVEL = {"kind": "solid", "id": 13, "data": 0}
SAND = {"kind": "solid", "id": 12, "data": 0}
OAK_PLANKS = {"kind": "solid", "id": 5, "data": 0}
SPRUCE_PLANKS = {"kind": "solid", "id": 5, "data": 1}
STONE_BRICK = {"kind": "solid", "id": 98, "data": 0}
CHISELED_STONE_BRICK = {"kind": "solid", "id": 98, "data": 3}


def depth_stack(top, under, thickness=3):
    return {
        "kind": "layered", "axis": "depth",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 1, "material": top},
            {"thickness": thickness - 1, "material": under},
        ]},
    }


quay_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": STONE,
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": COBBLE,
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 20, "material": depth_stack(GRASS, DIRT)},
            {"thickness": 20, "material": depth_stack(GRAVEL, DIRT)},
            {"thickness": 50, "material": depth_stack(COBBLE, STONE)},
        ]},
    }},
    "rim": {"enabled": True, "depth": 1, "material": COBBLE},
    "rimEdges": "void",
}

# --- the cellar and the hall: forked from "stonemason" (id 11) ---
cellar_style = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": COBBLE, "thickness": 1}], "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": STONE_BRICK, "verge": STONE_BRICK, "gable": COBBLE,
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                          "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": {
        "stack": {"bands": [
            {"material": CHISELED_STONE_BRICK, "thickness": 2},
            {"material": COBBLE, "thickness": 5},
        ], "ending": "repeat"},
        "extent": 7,
    },
    "post": STONE_BRICK,
    "windows": {"form": "stairLattice", "block": 67, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 4, "width": 2, "height": 2, "spacing": 3},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 67, "fill": "upperSlab", "fillBlock": 44, "fillData": 3},
                "width": 2, "height": 3},
}

hall_style = dict(cellar_style)
hall_style["roof"] = dict(cellar_style["roof"])
hall_style["roof"]["form"] = "gable"
hall_style["post"] = {"kind": "solid", "id": 17, "data": 0}
hall_style["wall"] = {
    "stack": {"bands": [
        {"material": COBBLE, "thickness": 3},
        {"material": OAK_PLANKS, "thickness": 4},
    ], "ending": "repeat"},
    "extent": 7,
}

ropewalk_style = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": COBBLE, "thickness": 1}], "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": SPRUCE_PLANKS, "verge": SPRUCE_PLANKS, "gable": OAK_PLANKS,
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                          "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": {
        "stack": {"bands": [{"material": OAK_PLANKS, "thickness": 7}], "ending": "repeat"},
        "extent": 7,
    },
    "post": {"kind": "solid", "id": 17, "data": 0},
    "windows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 4, "width": 2, "height": 2, "spacing": 3},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": 17, "data": 0, "reach": 1, "any": False},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 53, "fill": "upperSlab", "fillBlock": 126, "fillData": 0},
                "width": 2, "height": 3},
}

finish = {
    "created": "2026-09-21",
    "authors": ["Sonnet 5"],
    "themes": {"quay": quay_theme},
    "mapTheme": "quay",
    "roomStyles": {"spawn": hall_style, "wool": cellar_style},
    "relief": {
        "team": {"base": 9, "reach": 0, "step": 1, "marks": []}
    },
    "dressing": {
        "styles": {
            "mast-pine": {"kind": "tree", "form": "template", "species": "spruce", "height": 8},
            "quay-rock": {"kind": "boulder", "form": "angular", "size": 2.2, "rock": ANDESITE, "mossy": False},
            "ropewalk": {"kind": "house", "shell": ropewalk_style},
        },
        "props": [
            {"kind": "flora", "id": "yard-cover",
             "points": [[-172, -32], [-16, -32], [-16, 32], [-172, 32]],
             "spec": {"coverage": 0.22, "scale": 10, "octaves": 3, "fernShare": 0.15,
                      "flowerShare": 0.08, "flowerScale": 6, "tallShare": 0.08}},
            {"kind": "stroke", "id": "quay-road",
             "points": [[-182, 2], [-40, 2]], "radius": 2, "style": "solid",
             "claimsGround": True,
             "pave": {"kind": "cell", "seed": 21, "cellSize": 3, "jitter": 55, "warp": 2,
                       "palette": [GRAVEL, ANDESITE, COBBLE], "rise": 0}},
            {"kind": "stroke", "id": "cellar-path",
             "points": [[-50, 32], [-50, 68]], "radius": 2, "style": "worn", "coverage": 0.7,
             "claimsGround": True,
             "pave": {"kind": "cell", "seed": 23, "cellSize": 3, "jitter": 55, "warp": 2,
                       "palette": [GRAVEL, ANDESITE, COBBLE], "rise": 0}},
            {"kind": "tree", "id": "mast-1", "x": -60, "z": -22, "style": "mast-pine", "routeStandoff": 3},
            {"kind": "tree", "id": "mast-2", "x": -50, "z": 20, "style": "mast-pine", "routeStandoff": 3},
            {"kind": "tree", "id": "mast-3", "x": -100, "z": -24, "style": "mast-pine", "routeStandoff": 3},
            {"kind": "boulder", "id": "quayrock-1", "x": -30, "z": -18, "style": "quay-rock", "routeStandoff": 2},
            {"kind": "boulder", "id": "quayrock-2", "x": -30, "z": 18, "style": "quay-rock", "routeStandoff": 2},
            {"kind": "house", "id": "ropewalk", "style": "ropewalk",
             "wings": [{"corners": [[-106, -21], [-92, -12]]}]},
        ],
    },
}

write("finish", finish)
print("wrote", SLUG + ".finish.json")
