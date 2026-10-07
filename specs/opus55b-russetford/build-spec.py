#!/usr/bin/env python3
"""Russetford — an autumn river valley, destroy the monument, 16 a side.

Writes opus55b-russetford.plan.json and opus55b-russetford.refinement.json beside itself.
Team 0 holds the north bank (z < 0); rot_180 fans the south bank.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus55b-russetford"

# ---- heights (blocks) -------------------------------------------------------------------------
WATER = 20          # the river's line
STRAND = 21         # the bank the water meets
SPAWN_Y = 44        # the spawn plateau
SHELF = 33          # the monument's shelf
YARD = 23           # the mill yard

# ---- the plan ---------------------------------------------------------------------------------
plan = {
    "plan": 2,
    "meta": {"name": "Russetford", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 24},
    "pieces": [
        # the bank: one landmass from the river to the ridge behind the spawn
        {"id": "brow",  "rect": [-16, -25, 32, 3]},
        {"id": "westbrow", "rect": [-16, -22, 6, 4]},
        {"id": "eastbrow", "rect": [-6, -22, 22, 4]},
        {"id": "bank",  "rect": [-16, -18, 32, 16]},
        {"id": "spawn-room", "role": "spawn", "rect": [-10, -22, 4, 4], "surface": SPAWN_Y},
    ],
    # the river's middle is void, bridged from the first minute
    "zones": [{"id": "ford", "rect": [-16, -3, 32, 6], "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [8, 8], "facing": "back"}],
        "destroyables": [{"id": "monument", "piece": "", "at": [7, -61],
                          "style": "pillar-3", "float": 4}],
    },
}

# ---- relief -----------------------------------------------------------------------------------
def rect_ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]

def disc(cx, cz, r, n=10):
    import math
    return [[round(cx + r * math.cos(2 * math.pi * i / n), 1), round(cz + r * math.sin(2 * math.pi * i / n), 1)]
            for i in range(n)]

relief = {"*": {
    "base": 24, "reach": 0, "step": 1,
    "marks": [
        {"id": "strand", "kind": "area", "h": STRAND, "ring": rect_ring(-64, -21, 64, -8)},
        {"id": "ridge",  "kind": "area", "h": SPAWN_Y, "ring": rect_ring(-46, -96, -18, -68)},
        {"id": "shelf",  "kind": "area", "h": SHELF, "ring": disc(7, -61, 10)},
        {"id": "yard",   "kind": "area", "h": YARD, "ring": rect_ring(22, -41, 58, -23)},
        {"id": "bench",  "kind": "area", "h": 28, "ring": rect_ring(-64, -48, -16, -40)},
        {"id": "pithead", "kind": "area", "h": YARD, "ring": rect_ring(-34, -33, -23, -23)},
    ],
    "pushes": [
        {"id": "crag", "ring": disc(-56, -86, 8), "amount": 12, "falloff": 14, "crown": 6,
         "roughness": 0.3, "seed": 3},
        {"id": "spur", "ring": disc(44, -64, 11), "amount": 8, "falloff": 14, "crown": 4,
         "roughness": 0.3, "seed": 5},
    ],
}}


# ---- materials ------------------------------------------------------------------------------
def B(i, d=0): return {"kind": "solid", "id": i, "data": d}
GRASS, DIRT, COARSE, PODZOL = B(2), B(3), B(3, 1), B(3, 2)
STONE, GRANITE, PGRANITE, ANDESITE, COBBLE = B(1), B(1, 1), B(1, 2), B(1, 5), B(4)
SAND, SANDSTONE, HCLAY = B(12), B(24), B(172)
DARKOAK_PLANK, SPRUCE_PLANK = B(5, 5), B(5, 1)

def layered(axis, *bands, ending="repeat"):
    return {"kind": "layered", "axis": axis,
            "stack": {"ending": ending, "bands": [{"material": m, "thickness": t} for m, t in bands]}}

def over_soil(top, under=DIRT):
    return layered("depth", (top, 1), (under, 2), ending="handOver")

def noise(stops, scale=2, seed=1):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 2, "stops": stops}

def cell(palette, size=2, seed=1):
    return {"kind": "cell", "seed": seed, "cellSize": size, "palette": palette}

ROCK = noise([ANDESITE, STONE, STONE, COBBLE], scale=2, seed=4)     # stone and andesite, cobble patches
EARTH = cell([DIRT, COARSE], size=2, seed=2)                         # worn ground, half and half
WALLROCK = dict(ROCK, rise=3)                                        # the same rock on a cut face
FILL = {"kind": "cell", "cellSize": 5, "rise": 4, "seed": 9, "palette": [STONE, STONE, ANDESITE]}

def theme(flat, cut_grass=30, cut_earth=12):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "rim": {"enabled": False, "depth": 1, "material": STONE},
        "surface": {"enabled": True, "depth": 3, "material": layered(
            "slope", (over_soil(flat), cut_grass), (over_soil(EARTH), cut_earth),
            (over_soil(ROCK, STONE), 90 - cut_grass - cut_earth))},
        "wallEnabled": True, "wallOnTerrainFaces": True, "wall": WALLROCK,
        "fill": FILL,
    }

THEMES = {
    "valley": theme(GRASS),
    "strand": theme(noise([SAND, SAND, SAND, SANDSTONE], scale=2, seed=6), cut_grass=22, cut_earth=14),
    "wood":   theme(noise([GRASS, PODZOL, PODZOL, COARSE], scale=2, seed=8)),
}

# ---- shapes on the compiled ground ----------------------------------------------------------
# the mine: an adit from the strand under the valley side to a chamber under the shelf's west lip
CUT = [[-22, -20], [-18, -20], [-18, -31], [-22, -31]]              # the open cutting from the strand
ADIT = [[-22, -31], [-18, -31], [-18, -32], [-7, -43], [-2, -43], [-2, -55], [-12, -55], [-12, -46],
        [-22, -34]]                                                     # the roofed adit and its chamber
MINE_FLOOR_TOP = STRAND          # the adit's floor is the strand's own level
MINE_ROOF = STRAND + 4           # three courses of headroom

add_shapes = [
    # the roof of the mine: the valley's own ground, lifted off a floor so the adit runs under it
    {"id": "mine-roof", "type": "polygon", "operation": "add", "override": True,
     "floor": MINE_ROOF, "vertices": ADIT},
    # the cutting into the hillside: the ground taken down to the strand's level, out of the relief
    {"id": "mine-cut", "type": "polygon", "operation": "add", "override": True, "relief_scope": "exclude",
     "floor": 0, "base_height": MINE_FLOOR_TOP + 1, "vertices": CUT},
    # the strand the river meets
    {"id": "strand-flat", "type": "polygon", "operation": "add", "theme": "strand", "floor": 0, "base_height": 24,
     "vertices": [[-64, -22], [64, -22], [64, -8], [-64, -8]]},
    # the leaf floor of the wood on the spur
    {"id": "wood-floor", "type": "polygon", "operation": "add", "theme": "wood", "floor": 0, "base_height": 24,
     "vertices": [[26, -82], [44, -88], [62, -84], [63, -50], [52, -44], [36, -46], [26, -60]]},
]

add_layers = [
    # the adit's floor, under the compiled ground
    {"id": "mine", "name": "Mine", "base_y": 0, "below": True,
     "shapes": [{"id": "mine-floor", "type": "polygon", "operation": "add", "floor": 0,
                 "base_height": MINE_FLOOR_TOP + 1, "material": FILL, "vertices": ADIT}],
     "groups": [{"id": "mine", "name": "mine", "mirrors": True, "shapeIds": ["mine-floor"]}]},
]

# the waterwheel: a disc standing in the mill pool against the hall's river wall, one strip a column
import math
WHEEL_X, WHEEL_Y, WHEEL_R = 34, STRAND + 1, 5
PADDLES = {"kind": "checker", "size": 1, "even": DARKOAK_PLANK, "odd": SPRUCE_PLANK}
wheel = []
for dx in range(-WHEEL_R, WHEEL_R + 1):
    h = int(math.floor(math.sqrt(WHEEL_R * WHEEL_R - dx * dx) + 0.4))
    wheel.append({"id": f"wheel-{dx + WHEEL_R}", "type": "rectangle", "operation": "add",
                  "floor": WHEEL_Y - h, "base_height": 2 * h + 1, "material": PADDLES,
                  "min_x": WHEEL_X + dx, "max_x": WHEEL_X + dx + 1, "min_z": -22, "max_z": -20})
# the axle, from the wheel's hub to the hall's river wall
wheel.append({"id": "axle", "type": "rectangle", "operation": "add", "floor": WHEEL_Y, "base_height": 1,
              "material": {"kind": "solid", "id": 162, "data": 9}, "min_x": WHEEL_X, "max_x": WHEEL_X + 1,
              "min_z": -23, "max_z": -22})
add_layers.append({"id": "wheel", "name": "Mill wheel", "base_y": 0, "kind": "made", "part_of": "mill-wheel",
                   "shapes": wheel,
                   "groups": [{"id": "wheel", "name": "wheel", "mirrors": True,
                               "shapeIds": [s["id"] for s in wheel]}]})

# the adit's timbering: two dark-oak posts and a laid lintel at the first roofed row
POST, LINTEL = {"kind": "solid", "id": 162, "data": 1}, {"kind": "solid", "id": 162, "data": 5}
timber = [
    {"id": "post-w", "type": "rectangle", "operation": "add", "floor": MINE_FLOOR_TOP + 1, "base_height": 3,
     "material": POST, "min_x": -22, "max_x": -21, "min_z": -32, "max_z": -31},
    {"id": "post-e", "type": "rectangle", "operation": "add", "floor": MINE_FLOOR_TOP + 1, "base_height": 3,
     "material": POST, "min_x": -19, "max_x": -18, "min_z": -32, "max_z": -31},
    {"id": "lintel", "type": "rectangle", "operation": "add", "floor": MINE_FLOOR_TOP + 3, "base_height": 1,
     "material": LINTEL, "min_x": -21, "max_x": -19, "min_z": -32, "max_z": -31},
]
add_layers.append({"id": "timbering", "name": "Adit timbering", "base_y": 0, "kind": "made", "part_of": "adit",
                   "shapes": timber,
                   "groups": [{"id": "timbering", "name": "timbering", "mirrors": True,
                               "shapeIds": [t["id"] for t in timber]}]})

# ---- dressing -------------------------------------------------------------------------------
import sys
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import showcase
TREES = showcase.trees()

# a lane of one brown: leaf-strewn podzol, coarse dirt and boards, a third each
PATH = cell([PODZOL, COARSE, SPRUCE_PLANK], size=1, seed=11)

def path(pid, pts, radius=1.5, wander=3):
    return {"id": pid, "kind": "stroke", "points": pts, "radius": radius, "style": "solid",
            "pave": PATH, "claimsGround": True, "wander": wander, "wanderLength": 14, "seed": 3}

def tree(tid, x, z, style="valley-oak"):
    return {"id": tid, "kind": "tree", "style": style, "x": x, "z": z, "layer": "ground"}

props = [
    {"id": "river", "kind": "fluid", "layer": "ground", "shape": "pool", "form": "natural",
     "points": [[-70, -3], [70, -3], [70, -17], [46, -17], [44, -22], [24, -22], [22, -17], [-70, -17]],
     "radius": 3, "depth": 4, "level": WATER, "shore": 0, "shoreWander": True, "edge": 0, "seed": 7,
     "bank": noise([SAND, SAND, SAND, SANDSTONE], scale=2, seed=6)},
    {"id": "mill", "kind": "house", "layer": "ground", "seed": 5, "front": "negX", "style": "whiteclay",
     "wings": [{"corners": [[27, -31], [41, -24]], "spec": {"ridge": "alongX"}},
               {"corners": [[31, -38], [37, -32]], "spec": {"ridge": "alongZ", "projects": True}}]},
    {"id": "cottage", "kind": "house", "layer": "ground", "seed": 6, "front": "negX", "style": "whiteclay",
     "wings": [{"corners": [[50, -40], [56, -34]], "spec": {"ridge": "alongX"}}]},
    {"id": "minehead", "kind": "house", "layer": "ground", "seed": 7, "front": "posX", "style": "whiteclay",
     "wings": [{"corners": [[-31, -31], [-25, -25]], "spec": {"ridge": "alongZ"}}]},
    # the ways players go: spawn door to the shelf to the ford, the shelf to the mill, the lane to the pithead
    path("spawn-lane", [[-32, -70], [-24, -62], [-6, -60], [6, -50], [0, -36], [-8, -26], [-14, -21]]),
    path("mill-lane", [[12, -52], [18, -42], [22, -32], [25, -28]]),
    path("pit-lane", [[-8, -26], [-16, -25], [-24, -24]], wander=2),
    path("ford-lane", [[8, -22], [18, -24], [25, -27]], wander=2),
    # the wood on the spur, and the trees round the spawn
    tree("spur-1", 34, -56), tree("spur-3", 46, -68),
    tree("spur-5", 28, -76), tree("spur-6", 58, -86, "valley-oak-large"),
    tree("ridge-1", -14, -84), tree("ridge-2", -50, -62), tree("ridge-3", 4, -88, "valley-oak-large"),
    {"id": "flora", "kind": "flora", "layer": "ground", "seed": 13,
     "points": [[-64, -100], [64, -100], [64, -8], [-64, -8]],
     "spec": {"coverage": 0.22, "scale": 6, "octaves": 2, "fernShare": 0.25, "flowerShare": 0.04,
              "flowerScale": 10, "tallShare": 0.04}},
]

styles = {
    "valley-oak": TREES["oak-3"]["style"],
    "valley-oak-large": TREES["large-oak-1"]["style"],
    "whiteclay": {"library": "spruce-roofed-white-clay-cottage", "kind": "house"},
}

# the bank's coast: the compiled rectangle reshaped one point at a time, then drawn as a coast
COAST = [
    {"index": 0, "x": -60, "z": -93},
    {"after": 0, "x": -48, "z": -101}, {"after": 1, "x": -24, "z": -102}, {"after": 2, "x": -6, "z": -96},
    {"after": 3, "x": 18, "z": -92}, {"after": 4, "x": 40, "z": -95},
    {"index": 6, "x": 58, "z": -90},
    {"after": 6, "x": 64, "z": -80}, {"after": 7, "x": 59, "z": -60}, {"after": 8, "x": 64, "z": -40},
    {"after": 11, "x": -61, "z": -30}, {"after": 12, "x": -64, "z": -56}, {"after": 13, "x": -58, "z": -76},
]

refinement = {
    "editShapes": {"bank-24": COAST},
    "bendShapes": {"bank-24": {"tension": 0.22, "wander": 3, "step": 9, "seed": 5, "side": "in"},
                   "strand-flat": {"tension": 0.22, "wander": 3, "step": 7, "seed": 8, "side": "both"}},
    "relief": relief,
    "biome": {"kind": "solid", "id": 37},   # Mesa: grass #90814d, leaves #9e814d — the autumn
    "themes": THEMES,
    "mapTheme": "valley",
    "addShapes": add_shapes,
    "addLayers": add_layers,
    "roomStyles": {"spawn": {"library": "spruce-roofed-white-clay-cottage"}},
    "dressing": {"styles": styles, "props": props},
    "authors": ["Opus 5.5"],
    "created": "2026-10-07",
}

for name, doc in (("plan", plan), ("refinement", refinement)):
    with open(os.path.join(HERE, f"{SLUG}.{name}.json"), "w") as f:
        json.dump(doc, f, indent=1)
print("wrote", SLUG)
