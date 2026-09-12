#!/usr/bin/env python3
"""Writes sonnet5-talltimber-yard.plan.json and .finish.json.

Two rival logging outfits, each running a small timber yard around a tall counting-house where their
ledger-core is kept; the two yards face each other across the felled ground between them, joined only by
a build-zone-spanned gap. Team 0 is authored; rot_180 fans it.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet5-talltimber-yard"


def mat(kind, **kw):
    d = {"kind": kind}
    d.update(kw)
    return d


def solid(id_, data=0):
    return mat("solid", id=id_, data=data)


def cellmat(seed, size, palette, jitter=45, warp=3, rise=0):
    return mat("cell", seed=seed, cellSize=size, jitter=jitter, warp=warp, palette=palette, rise=rise)


# blocks
DIRT = solid(3, 0)
COARSE_DIRT = solid(3, 1)
GRASS = solid(2, 0)
GRAVEL = solid(13, 0)
STONE = solid(1, 0)
COBBLE = solid(4, 0)
ANDESITE = solid(1, 5)
SPRUCE_PLANK = solid(5, 1)

# ---------------------------------------------------------------- plan -----

plan = {
    "plan": 2,
    "meta": {"name": "Talltimber Yard"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 10, "surface": 9},
    "pieces": [
        {"id": "spawn-0", "role": "spawn", "rect": [-3, -23, 6, 4]},
        {"id": "yard-0", "role": "piece", "rect": [-9, -19, 18, 16]},
    ],
    "zones": [
        {"id": "clearing", "rect": [-9, -3, 18, 6], "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-0", "at": [15, 10], "facing": "back",
             "footprint": [5, 3, 20, 14]},
        ],
        "wools": [],
        "iron": [],
        "destroyables": [],
        "cores": [
            {"id": "core-0", "piece": "yard-0", "at": [62, 33],
             "lava": 3, "lavaHeight": 3, "float": 5, "leak": 6, "name": "Ledger"},
        ],
    },
    "walls": [],
    "boxes": [],
}

# ------------------------------------------------------------- finish -----

# The felled/open ground: a plain ordinary add over the forward third of the yard, painted its own theme.
felled_patch = {
    "id": "felled-open-0", "type": "rectangle", "operation": "add",
    "floor": 0, "base_height": 10, "relief_scope": "exclude",
    "min_x": -45, "min_z": -40, "max_x": 45, "max_z": -15,
    "theme": "felled-open",
}

finish = {
    "themes": {
        "yard-worked": {
            "bedrock": {"relative": True, "value": 3},
            "rimEdges": "drop",
            "wallOnTerrainFaces": True,
            "rim": {"material": STONE, "depth": 1, "enabled": False},
            "surface": {
                "material": mat(
                    "layered", axis="slope",
                    stack={"bands": [
                        {"material": mat("layered", stack={"bands": [
                            {"material": cellmat(11, 4, [DIRT, COARSE_DIRT, GRAVEL]), "thickness": 1},
                            {"material": solid(3, 1), "thickness": 2},
                        ], "ending": "repeat"}), "thickness": 25},
                        {"material": cellmat(12, 4, [COARSE_DIRT, GRAVEL, ANDESITE]), "thickness": 15},
                        {"material": cellmat(13, 3, [STONE, COBBLE, ANDESITE]), "thickness": 50},
                    ], "ending": "repeat"},
                ),
                "depth": 3, "enabled": True,
            },
            "wall": cellmat(14, 4, [STONE, COBBLE, ANDESITE], rise=3),
            "wallEnabled": True,
            "fill": cellmat(15, 6, [STONE, COBBLE, ANDESITE], rise=4),
        },
        "felled-open": {
            "bedrock": {"relative": True, "value": 3},
            "rimEdges": "drop",
            "wallOnTerrainFaces": True,
            "rim": {"material": STONE, "depth": 1, "enabled": False},
            "surface": {
                "material": mat(
                    "layered", axis="slope",
                    stack={"bands": [
                        {"material": mat("layered", stack={"bands": [
                            {"material": cellmat(21, 5, [GRASS, GRASS, COARSE_DIRT]), "thickness": 1},
                            {"material": solid(3, 0), "thickness": 2},
                        ], "ending": "repeat"}), "thickness": 25},
                        {"material": cellmat(22, 4, [COARSE_DIRT, DIRT, GRAVEL]), "thickness": 15},
                        {"material": cellmat(23, 3, [STONE, COBBLE, ANDESITE]), "thickness": 50},
                    ], "ending": "repeat"},
                ),
                "depth": 3, "enabled": True,
            },
            "wall": cellmat(24, 4, [STONE, COBBLE, ANDESITE], rise=3),
            "wallEnabled": True,
            "fill": cellmat(25, 6, [STONE, COBBLE, ANDESITE], rise=4),
        },
    },
    "mapTheme": "yard-worked",
    "relief": {
        "*": {
            "landform": "plain",
            "base": 9,
            "reach": 40,
            "step": 1,
            "grain": {"amplitude": 1, "scale": 10, "seed": 71},
            "marks": [
                {"id": "yard-pad", "kind": "area", "h": 10,
                 "ring": [[-46, -117], [46, -117], [46, -13], [-46, -13]]},
            ],
            "pushes": [
                {"id": "spawn-rise", "amount": 4, "falloff": 24, "crown": 2, "roughness": 0.3, "seed": 72,
                 "ring": [[-24, -128], [24, -128], [24, -106], [-24, -106]]},
            ],
        },
    },
    "addShapes": [felled_patch],
    "roomStyles": {"spawn": "@talltimber-cottage"},
    "dressing": {"props": []},
    "authors": ["Sonnet 5"],
    "created": "2026-09-11",
}

# --------------------------------------------------------- house styles -----

def style_ref(name):
    return "@" + name


# counting-house: two wings, a lower gambrel annex against the tall hall
counting_house = {
    "kind": "house", "id": "counting-house", "seed": 301,
    "wings": [
        {"corners": [[-5, -68], [5, -56]]},
        {"corners": [[-13, -62], [-6, -58]], "spec": {"form": "gambrel"}},
    ],
    "front": "negZ",
    "style": style_ref("talltimber-hall"),
}

cottage = {
    "kind": "house", "id": "cottage", "seed": 302,
    "points": [[20, -88], [28, -80]],
    "front": "negX",
    "style": style_ref("talltimber-cottage"),
}

store = {
    "kind": "house", "id": "store", "seed": 303,
    "points": [[-30, -86], [-22, -78]],
    "front": "posX",
    "style": style_ref("talltimber-store"),
}

finish["dressing"]["props"] = [
    counting_house, cottage, store,
    # -- road: spawn door -> between the small buildings -> counting-house door
    {"kind": "stroke", "id": "camp-road", "seed": 401,
     "points": [[0, -95], [0, -84], [0, -74], [0, -68]],
     "radius": 2.5, "style": "solid", "claimsGround": True,
     "pave": cellmat(51, 3, [DIRT, COARSE_DIRT, SPRUCE_PLANK], jitter=35, warp=2)},
    # -- spur: forks off the camp road, round the hall's east flank, to the core plaza
    {"kind": "stroke", "id": "plaza-road", "seed": 402,
     "points": [[0, -74], [7, -72], [7, -64], [17, -62]],
     "radius": 2.2, "style": "solid", "claimsGround": True,
     "pave": cellmat(52, 3, [DIRT, COARSE_DIRT, SPRUCE_PLANK], jitter=35, warp=2)},
    # -- spurs to the two small buildings, off the camp road
    {"kind": "stroke", "id": "cottage-road", "seed": 403,
     "points": [[0, -84], [18, -84]],
     "radius": 2, "style": "solid", "claimsGround": True,
     "pave": cellmat(53, 3, [DIRT, COARSE_DIRT, SPRUCE_PLANK], jitter=35, warp=2)},
    {"kind": "stroke", "id": "store-road", "seed": 404,
     "points": [[0, -84], [-20, -83]],
     "radius": 2, "style": "solid", "claimsGround": True,
     "pave": cellmat(54, 3, [DIRT, COARSE_DIRT, SPRUCE_PLANK], jitter=35, warp=2)},
    # -- sparse street trees, team 0 only (fanned)
    {"kind": "tree", "id": "oak-1", "seed": 501, "x": 38, "z": -83,
     "style": "oak-street"},
    {"kind": "tree", "id": "oak-2", "seed": 502, "x": -37, "z": -30,
     "style": "oak-street"},
    {"kind": "tree", "id": "oak-3", "seed": 503, "x": 34, "z": -27,
     "style": "oak-street"},
]

finish["dressing"]["styles"] = {
    "oak-street": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
}

if __name__ == "__main__":
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(plan, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(finish, handle, indent=1)
    print("wrote", SLUG, "plan + finish")
