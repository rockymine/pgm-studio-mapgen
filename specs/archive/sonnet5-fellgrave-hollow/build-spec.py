#!/usr/bin/env python3
"""Fellgrave Hollow — a snowbound highland valley, one dig per team.

Two mining camps have followed the same frost-locked seam up opposite sides of a highland valley,
each holding what it found in a hollow cut into the hillside at the head of its own dig. The valley
floor runs snow over dirt; its flanks rise into two long ridges banded by slope — a rocky shoulder
where the ground steepens, bare stone on the sheer faces. Between the two camps the valley narrows
to a frozen tarn whose centre has calved into a void gorge: the required team-to-team gap, dressed
as the thing it would actually be up here rather than as a hole in the ground.

The board is one fused landmass a side (spawn and dig share one nominal height, so they compile to
one polygon) with the whole climb, the hollow and the ridges stated in the relief rather than in a
second plan piece — the anti-firnline rule: a piece earns its place by stating something the
arrangement needs, not by giving a theme somewhere to hang.

Writes sonnet5-fellgrave-hollow.plan.json and .finish.json beside this file.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet5-fellgrave-hollow"


def solid(blockId, data=0):
    return {"kind": "solid", "id": blockId, "data": data}


def cellmat(members, cellSize):
    return {"kind": "cell", "cellSize": cellSize, "palette": [solid(*m) for m in members]}


def depthStack(bands, ending="repeat"):
    return {"kind": "layered", "stack": {"ending": ending, "bands": bands}}


def ring(cx, cz, rx, rz, n=16, rot=0.0):
    return [[round(cx + rx * math.cos(rot + 2 * math.pi * i / n), 2),
             round(cz + rz * math.sin(rot + 2 * math.pi * i / n), 2)] for i in range(n)]


SNOW = solid(80, 0)
DIRT = solid(3, 0)
COARSE_DIRT = solid(3, 1)
PODZOL = solid(3, 2)
STONE = solid(1, 0)
ANDESITE = solid(1, 5)
POLISHED_ANDESITE = solid(1, 6)
COBBLE = solid(4, 0)
GRAVEL = solid(13, 0)
PACKED_ICE = solid(174, 0)
SPRUCE_PLANK = solid(5, 1)
SPRUCE_LOG = solid(17, 1)
OBSIDIAN = solid(49, 0)

# ── the valley floor: flat, worn by the dig above it into gravel, bare stone on the sheer faces.
FLAT_BAND = depthStack([{"material": SNOW, "thickness": 1}, {"material": DIRT, "thickness": 2}])
SHOULDER_BAND = depthStack([
    {"material": cellmat([(1, 0), (1, 5), (13, 0)], 9), "thickness": 1},
    {"material": STONE, "thickness": 2},
])
STEEP_BAND = cellmat([(1, 0), (4, 0), (1, 5), (1, 0)], 8)

# read `incline?format=text` against these once the board is built; the cuts below are the author's
# first guess at where a highland valley's flat/shoulder/face actually fall.
FROST_SURFACE = {"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
    {"material": FLAT_BAND, "thickness": 22},
    {"material": SHOULDER_BAND, "thickness": 18},
    {"material": STEEP_BAND, "thickness": 50},
]}}

WORKED_SURFACE = cellmat([(1, 0), (1, 5), (4, 0), (4, 0), (1, 5), (174, 0)], 8)
OLD_FIRS_SURFACE = depthStack([
    {"material": PODZOL, "thickness": 1},
    {"material": COARSE_DIRT, "thickness": 2},
    {"material": GRAVEL, "thickness": 1},
])

ROCK_WALL = {"kind": "wallRun", "runs": [
    {"material": STONE, "width": 4}, {"material": ANDESITE, "width": 3},
    {"material": COBBLE, "width": 3}, {"material": ANDESITE, "width": 3},
]}


def theme(surface, wall=ROCK_WALL, rimEnabled=False, rimMaterial=None, depth=3):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop",
        "wallOnTerrainFaces": True,
        "rim": {"material": rimMaterial or COBBLE, "depth": 1, "enabled": rimEnabled},
        "surface": {"material": surface, "depth": depth, "enabled": True},
        "wall": wall,
        "wallEnabled": True,
        "fill": STONE,
    }


THEMES = {
    "frost-valley": theme(FROST_SURFACE),
    "worked-hollow": theme(WORKED_SURFACE, rimEnabled=True, rimMaterial=COBBLE, depth=2),
    "old-firs": theme(OLD_FIRS_SURFACE, depth=2),
}

# ── the relief: base valley, a guiding lane, ridges as pushes, the hollow as a rim/floor pair
#    (the "state the rim and the floor as two area marks, let the relaxation solve a smooth bowl
#    between them" idiom) — solved wide enough (14 cells between the two rings) that the bowl's own
#    wall grades at run >= 2x rise rather than needing a built stair.
BASE = 10
HOLLOW_CX, HOLLOW_CZ = 0, -70
HOLLOW_RIM_H, HOLLOW_FLOOR_H = 12, 5

marks = [
    {"id": "lane", "kind": "line", "r": 22,
     "points": [[0, -125], [0, -95], [0, -45], [0, -16]],
     "h": [BASE + 1, BASE, BASE - 1, BASE - 3]},
    {"id": "hollow-rim", "kind": "area", "bevel": 9,
     "ring": ring(HOLLOW_CX, HOLLOW_CZ, 22, 18, n=14), "h": HOLLOW_RIM_H},
    {"id": "hollow-floor", "kind": "area", "bevel": 3,
     "ring": ring(HOLLOW_CX, HOLLOW_CZ, 5, 4, n=14), "h": HOLLOW_FLOOR_H},
]

# ridges hug the board's outer edge (x 38..50 either side of a 100-wide board) so the flat lane a
# player actually walks is most of the board's width rather than a thin strip between two huge
# ornamental ranges — the "22968 of 28592 blocks reached and on the way to nothing" first drive read.
pushes = [
    {"id": "ridge-w", "ring": [[-50, -140], [-38, -140], [-38, -14], [-50, -14]],
     "amount": 26, "crown": 16, "falloff": 12, "roughness": 5, "seed": 101},
    {"id": "ridge-e", "ring": [[38, -140], [50, -140], [50, -14], [38, -14]],
     "amount": 26, "crown": 16, "falloff": 12, "roughness": 5, "seed": 102},
]

# ── the paint patches: the dig floor + the frozen shore, and one taiga stand, each its own shape
#    rather than a field sampled over ground that has no reason to carry it.
# A patch's own base_height has to be tall enough to plausibly "reach the visible top" in the
# pre-repair ranking `ShapeThemeOwners` reads (docs/world-export/terrain-painting.md §"a scope is a
# layer and a cell") — a thin `base_height: 1` patch never wins the smallest-area contest against the
# much taller relief-governed ground it sits on, however small its footprint, and paints nothing.
# RasterizeLayout still clamps the *built* height to the solved surface either way (Max(floor+1,
# field)), so a tall-stated patch inside a solved group reads at the terrain's own height, not its own.
PATCH_HEIGHT = 60

addShapes = [
    {"id": "hollow-paint", "type": "polygon", "operation": "add", "base_height": PATCH_HEIGHT,
     "vertices": ring(HOLLOW_CX, HOLLOW_CZ, 23, 19, n=14), "theme": "worked-hollow"},
    {"id": "shore-band", "type": "rectangle", "operation": "add", "base_height": PATCH_HEIGHT,
     "min_x": -50, "max_x": 50, "min_z": -20, "max_z": -14, "theme": "worked-hollow"},
    {"id": "old-firs-patch", "type": "polygon", "operation": "add", "base_height": PATCH_HEIGHT,
     "vertices": [[-44, -100], [-26, -102], [-22, -86], [-40, -82]], "theme": "old-firs"},
]

# ── the timber-and-stone spawn hut: alpine mining, forked — cobble base, ONE laid-log beam course
#    (never beams alone), spruce infill, no footing, gable (never shed), snow-capped.
SPAWN_HUT_STYLE = {
    "foundation": {
        "plate": {"stack": {"ending": "repeat", "bands": [{"material": COBBLE, "thickness": 1}]}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": SNOW, "verge": ANDESITE, "gable": SPRUCE_PLANK,
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                         "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": {
        "stack": {"ending": "repeat", "bands": [
            {"material": COBBLE, "thickness": 2},
            {"material": {"kind": "laidLog", "id": 17, "data": 1}, "thickness": 3},
            {"material": SPRUCE_PLANK, "thickness": 2},
        ]},
        "extent": 7,
    },
    "post": SPRUCE_LOG,
    "windows": {"form": "stairLattice", "block": 134, "hostBlock": 5, "hostData": 1, "data": 0,
               "sill": 3, "width": 2, "height": 2, "spacing": 1},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                        "fillBlock": 126, "fillData": 0}, "width": 2, "height": 3},
}

TREE_STYLES = {
    "spruce-tall": {"kind": "tree", "form": "template", "species": "spruce", "height": 13},
    "spruce-short": {"kind": "tree", "form": "template", "species": "spruce", "height": 9},
}
BOULDER_STYLES = {
    "grey-outcrop": {"kind": "boulder", "form": "outcrop", "size": 3.0,
                     "rock": cellmat([(1, 0), (1, 5), (4, 0)], 4), "mossy": False},
    "grey-round": {"kind": "boulder", "form": "round", "size": 2.2,
                   "rock": cellmat([(1, 0), (4, 0)], 4), "mossy": False},
}

trees = [
    {"kind": "tree", "id": "fir-1", "x": -36, "z": -96, "style": "spruce-tall", "seed": 401},
    {"kind": "tree", "id": "fir-2", "x": -29, "z": -90, "style": "spruce-short", "seed": 402},
    {"kind": "tree", "id": "fir-3", "x": -34, "z": -84, "style": "spruce-tall", "seed": 403},
    {"kind": "tree", "id": "fir-4", "x": -26, "z": -98, "style": "spruce-short", "seed": 404},
    {"kind": "tree", "id": "fir-5", "x": -38, "z": -88, "style": "spruce-short", "seed": 405},
    {"kind": "tree", "id": "fir-6", "x": -23, "z": -88, "style": "spruce-tall", "seed": 406},
    {"kind": "tree", "id": "spar-1", "x": 22, "z": -108, "style": "spruce-tall", "seed": 411},
    {"kind": "tree", "id": "spar-2", "x": 22, "z": -55, "style": "spruce-short", "seed": 412},
    {"kind": "tree", "id": "spar-3", "x": -24, "z": -45, "style": "spruce-tall", "seed": 413},
]
boulders = [
    {"kind": "boulder", "id": "boulder-1", "x": 16, "z": -85, "style": "grey-outcrop", "seed": 501},
    {"kind": "boulder", "id": "boulder-2", "x": -18, "z": -55, "style": "grey-round", "seed": 502},
    {"kind": "boulder", "id": "boulder-3", "x": 13, "z": -50, "style": "grey-outcrop", "seed": 503},
    {"kind": "boulder", "id": "boulder-4", "x": -30, "z": -108, "style": "grey-round", "seed": 504},
]
paths = [
    {"kind": "stroke", "id": "dig-road", "points": [[0, -119], [0, -95], [0, -82]], "radius": 2.5,
     "style": "solid", "pave": cellmat([(13, 0), (1, 5), (4, 0)], 4), "claimsGround": True},
]

finish = {
    "authors": ["Sonnet 5"], "created": "2026-09-11",
    "relief": {"*": {"base": BASE, "reach": 0, "step": 1, "landform": "hills",
                     "grain": {"amplitude": 0.6, "scale": 17, "seed": 71},
                     "marks": marks, "pushes": pushes}},
    "addShapes": addShapes,
    "themes": THEMES, "mapTheme": "frost-valley",
    "biome": {"kind": "solid", "id": 12},
    "roomStyles": {"spawn": SPAWN_HUT_STYLE},
    "dressing": {"props": paths + boulders + trees,
                "styles": dict(TREE_STYLES, **BOULDER_STYLES)},
}

plan = {
    "plan": 2,
    "meta": {"name": "Fellgrave Hollow"},
    "globals": {"cell": 2, "symmetry": "rot_180", "maxPlayers": 8, "surface": BASE, "observerY": 58},
    "pieces": [
        {"id": "spawn", "role": "spawn", "rect": [-5, -70, 10, 15]},
        {"id": "ground-1", "role": "piece", "rect": [-25, -55, 50, 16]},
        {"id": "ground-2", "role": "piece", "rect": [-25, -39, 50, 16]},
        {"id": "ground-3", "role": "piece", "rect": [-25, -23, 50, 16]},
        {"id": "east-adit", "role": "piece", "rect": [25, -41, 6, 8]},
    ],
    "zones": [
        {"id": "tarn-crossing", "rect": [-25, -7, 50, 14]},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 16], "facing": "back",
                    "footprint": [2, 10, 16, 12]}],
        "destroyables": [
            {"id": "relic-1", "piece": "", "at": [0, -70], "style": "pillar-2",
             "materials": "obsidian", "float": 4, "name": "Frozen Relic"},
        ],
        "cores": [],
        "wools": [],
    },
    "walls": [],
    "boxes": [],
}

for name, doc in (("plan", plan), ("finish", finish)):
    with open(f"{HERE}/{SLUG}.{name}.json", "w") as fh:
        json.dump(doc, fh, indent=1)

print(f"{len(marks)} relief mark(s), {len(pushes)} push(es), {len(addShapes)} shape(s), "
      f"{len(THEMES)} themes, {len(trees)} trees, {len(boulders)} boulders")
