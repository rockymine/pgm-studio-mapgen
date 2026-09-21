"""sonnet5b-turbary-cut — a cut-over peat moor, destroy-the-core.

Identity: each team's core stands on a raised turbary island with ground all round its
casing, a drained cutting into one flank and alder scrub on the other, the two teams'
banks joined only by a build zone over the open bog.

Writes sonnet5b-turbary-cut.plan.json and sonnet5b-turbary-cut.finish.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet5b-turbary-cut"


def write(name, doc):
    with open(os.path.join(HERE, f"{SLUG}.{name}.json"), "w") as f:
        json.dump(doc, f, indent=1)


plan = {
    "plan": 2,
    "meta": {"name": "Turbary Cut"},
    "globals": {
        "cell": 4,
        "symmetry": "rot_180",
        "maxPlayers": 8,
        "surface": 8,
    },
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-26, -3, 5, 6]},
        {"id": "field", "role": "piece", "rect": [-21, -8, 17, 16]},
    ],
    "zones": [
        {"id": "strait", "rect": [-4, -8, 8, 16], "kind": "build"},
    ],
    "placements": {
        "spawns": [
            {"id": "red-spawn", "piece": "spawn", "at": [10, 12], "facing": "right",
             "footprint": [2, 6, 16, 12]},
        ],
        "cores": [
            {"id": "red-core", "piece": "field", "at": [33, 32],
             "lava": 3, "lavaHeight": 3, "float": 6, "leak": 5, "openTop": False,
             "name": "Turbary Core"},
        ],
    },
    "walls": [],
}

write("plan", plan)
print("wrote", SLUG + ".plan.json")

# --------------------------------------------------------------- the finish --

DIRT = {"kind": "solid", "id": 3, "data": 0}
COARSE_DIRT = {"kind": "solid", "id": 3, "data": 1}
PODZOL = {"kind": "solid", "id": 3, "data": 2}
GRAVEL = {"kind": "solid", "id": 13, "data": 0}
STONE = {"kind": "solid", "id": 1, "data": 0}
COBBLE = {"kind": "solid", "id": 4, "data": 0}
ANDESITE = {"kind": "solid", "id": 1, "data": 5}
OAK_PLANKS = {"kind": "solid", "id": 5, "data": 0}
SPRUCE_PLANKS = {"kind": "solid", "id": 5, "data": 1}
COBBLE_STAIR_MAT = {"kind": "solid", "id": 4, "data": 0}


def depth_stack(top, under, thickness=3):
    return {
        "kind": "layered", "axis": "depth",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 1, "material": top},
            {"thickness": thickness - 1, "material": under},
        ]},
    }


peat_moor_theme = {
    "bedrock": {"relative": False, "value": 1},
    "fill": DIRT,
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": COARSE_DIRT,
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope",
        "stack": {"ending": "repeat", "bands": [
            {"thickness": 20, "material": depth_stack(PODZOL, DIRT)},
            {"thickness": 20, "material": depth_stack(COARSE_DIRT, DIRT)},
            {"thickness": 50, "material": depth_stack(GRAVEL, DIRT)},
        ]},
    }},
    "rim": {"enabled": True, "depth": 1, "material": COARSE_DIRT},
    "rimEdges": "void",
}

# --- the spawn hall: forked from the "cottage" preset (id 6) ---
hall_style = {
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
        "stack": {"bands": [
            {"material": COBBLE, "thickness": 3},
            {"material": OAK_PLANKS, "thickness": 4},
        ], "ending": "repeat"},
        "extent": 7,
    },
    "post": {"kind": "solid", "id": 17, "data": 1},
    "windows": {"form": "stairLattice", "block": 134, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 4, "width": 2, "height": 2, "spacing": 3},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": 17, "data": 1, "reach": 1, "any": False},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 134, "fill": "upperSlab", "fillBlock": 126, "fillData": 1},
                "width": 2, "height": 3},
}

finish = {
    "created": "2026-09-21",
    "authors": ["Sonnet 5"],
    "themes": {"peat-moor": peat_moor_theme},
    "mapTheme": "peat-moor",
    "roomStyles": {"spawn": hall_style},
    "relief": {
        "team": {
            "base": 8, "reach": 0, "step": 1,
            "marks": [
                {"id": "cutting", "kind": "area", "h": 2, "bevel": 5,
                 "ring": [[-78, -30], [-64, -30], [-64, -13], [-78, -13]]},
            ],
            "pushes": [
                {"id": "turbary", "ring": [[-80, 12], [-55, 12], [-55, 30], [-80, 30]],
                 "amount": 4, "falloff": 12, "crown": 0, "roughness": 3, "seed": 13},
            ],
        }
    },
    "dressing": {
        "styles": {
            "alder": {"kind": "tree", "form": "template", "species": "birch", "height": 7},
            "peat-boulder": {"kind": "boulder", "form": "round", "size": 2.0, "rock": ANDESITE, "mossy": True},
        },
        "props": [
            {"kind": "flora", "id": "moor-cover",
             "points": [[-84, -32], [-16, -32], [-16, 32], [-84, 32]],
             "spec": {"coverage": 0.3, "scale": 8, "octaves": 3, "fernShare": 0.35,
                      "flowerShare": 0.06, "flowerScale": 5, "tallShare": 0.15}},
            {"kind": "stroke", "id": "moor-track",
             "points": [[-92, 0], [-56, 0]], "radius": 2, "style": "worn", "coverage": 0.6,
             "claimsGround": True,
             "pave": {"kind": "cell", "seed": 17, "cellSize": 3, "jitter": 60, "warp": 2,
                       "palette": [DIRT, COARSE_DIRT, SPRUCE_PLANKS], "rise": 0}},
            {"kind": "tree", "id": "alder-1", "x": -68, "z": 18, "style": "alder", "routeStandoff": 3},
            {"kind": "tree", "id": "alder-2", "x": -60, "z": 25, "style": "alder", "routeStandoff": 3},
            {"kind": "tree", "id": "alder-3", "x": -72, "z": 28, "style": "alder", "routeStandoff": 3},
            {"kind": "tree", "id": "alder-4", "x": -63, "z": 14, "style": "alder", "routeStandoff": 3},
            {"kind": "boulder", "id": "peatrock-1", "x": -66, "z": -22, "style": "peat-boulder", "routeStandoff": 2},
            {"kind": "boulder", "id": "peatrock-2", "x": -74, "z": -18, "style": "peat-boulder", "routeStandoff": 2},
            {"kind": "boulder", "id": "peatrock-3", "x": -30, "z": -18, "style": "peat-boulder", "routeStandoff": 2},
        ],
    },
}

write("finish", finish)
print("wrote", SLUG + ".finish.json")
