"""Quarrymoot — writes opus55-quarrymoot.plan.json and .refinement.json.

A King of the Hill board in a red-sandstone quarry. The two spawns stand on the quarry's rim at either end
and look into a pit that steps down one bench to a floor. Three hills: the centre on the floor under a
crusher house's roof, paying double, and one on each side of the bench across the line between the spawns.
Four haul roads come down the benches, a conveyor gantry crosses the whole pit at rim height over the
crusher house, and quarried blocks stand about the floor and the benches as cover.

`match-flow.md` §10 is the law it is built to: the ground is made, a point is not raised over the ground
round it, the centre pays more than the flanks, cover is placed in two sizes, and every part of the board
is a way toward a point. The centre sits lowest and is roofed, so nothing on the rim has a line onto its pad
and the gantry above it is a second storey fought over the same footprint.

The board is one landmass: each team's half of the quarry is one piece, the two meeting on the axis (a
landmass may not mix a fanned piece with an unfanned one, PL12). rot_180 fans the halves, the spawns, the
made things marked to mirror and every prop; the crusher house and the gantry are stated once, off it.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (S, cell, noise, depth, beds, by_slope, theme, one, ROCK, ring, patch, path, tree,
                        boulder, house, flora, pool, house_style, boulder_style, copied_trees, made)
import props

SLUG = "opus55-quarrymoot"
RIM, BENCH, FLOOR = 22, 18, 14

plan = {
    "plan": 2,
    "meta": {"name": "Quarrymoot", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": RIM},
    "pieces": [
        {"id": "half", "rect": [-16, 0, 32, 18]},
        {"id": "spawn", "role": "spawn", "rect": [-3, 18, 6, 4], "surface": 24},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "sp", "piece": "spawn", "at": [12, 10], "facing": "front",
                    "footprint": [2, 2, 20, 12]}],
        "controlPoints": 3,
    },
}

# --- paint ------------------------------------------------------------------------------------------------
# Families: the ground orange (red sand, red sandstone and orange clay in the pit; turf on the rim under a
# Mesa sky that tints it to meet them), the built grey and dark (stone brick, dark-oak timber), the accent the
# gravel of the haul roads and the iron of the gantry's rails.
ORANGE = cell([S(12, 1), S(179), S(159, 1)], 2, 3)
WORN = cell([S(3), S(3, 1)], 2, 4)
PIT_FLOOR = noise([WORN, ORANGE, ORANGE, ORANGE, S(172)], scale=2, seed=5)
STRATA = beds([(cell([S(179), S(179, 2)], 2, 6, rise=2), 3), (S(159, 1), 1), (S(179), 2), (S(172), 1),
               (S(179, 2), 2), (S(159, 1), 1)] * 7 + [(S(179), 1)], start=-40, beyond=S(179))
quarry = theme(by_slope((30, depth(PIT_FLOOR, S(179))), (14, depth(cell([S(12, 1), S(179)], 2, 7), S(179))),
                        (46, STRATA)), wall=STRATA, fill=STRATA)
turf = theme(by_slope((30, depth(noise([WORN, S(2), S(2), S(2)], 2, 8), S(3))), (60, STRATA)),
             wall=STRATA, fill=STRATA)
brick = one(cell([S(98), S(98), S(98, 2), S(1, 5)], 2, 9, rise=2))
timber = one(S(5, 5))
post = one(S(162, 1))
blocks = one(cell([S(179), S(179, 2), S(179)], 2, 10, rise=2))

PAVE = cell([S(13), S(1, 5), S(4)], size=2, seed=21)


def haul(pid, pts):
    return {"id": pid, "kind": "line", "r": 5, "tread": 2, "points": pts, "h": [RIM, BENCH, FLOOR]}


def image(p):
    """A block's rot_180 image."""
    return [-p[0] - 1, -p[1] - 1]


ROAD_A = [[-12, 66], [-38, 40], [-26, 17]]
ROAD_B = [[12, 66], [38, 40], [26, 17]]
relief = {"*": {
    "base": RIM, "reach": 0, "step": 1, "landform": "rolling",
    "marks": [
        {"id": "bench", "kind": "area", "h": BENCH, "bevel": 2, "ring": ring(-0.5, -0.5, 50, 42, 48)},
        {"id": "floor", "kind": "area", "h": FLOOR, "bevel": 2, "ring": ring(-0.5, -0.5, 30, 24, 40)},
        {"id": "spawn-rim", "kind": "area", "h": 24, "bevel": 3,
         "ring": [[-14, 72], [14, 72], [14, 90], [-14, 90]]},
        haul("road-a", ROAD_A), haul("road-b", ROAD_B),
        haul("road-a2", [image(p) for p in ROAD_A]), haul("road-b2", [image(p) for p in ROAD_B]),
    ],
    "pushes": [
        # spoil heaps on the rim, either side of each spawn's view down into the pit
        {"id": "spoil-w", "ring": ring(-34, 62, 9, 6, 20, 0.15, 3), "amount": 6, "falloff": 5,
         "roughness": 0.4, "crown": 0, "seed": 3},
        {"id": "spoil-e", "ring": ring(33, -63, 9, 6, 20, 0.15, 3), "amount": 6, "falloff": 5,
         "roughness": 0.4, "crown": 0, "seed": 3},
        {"id": "spoil-e2", "ring": ring(34, 60, 7, 5, 20, 0.15, 3, 1), "amount": 5, "falloff": 5,
         "roughness": 0.4, "crown": 0, "seed": 4},
        {"id": "spoil-w2", "ring": ring(-35, -61, 7, 5, 20, 0.15, 3, 1), "amount": 5, "falloff": 5,
         "roughness": 0.4, "crown": 0, "seed": 4},
    ],
}}

# --- made things ----------------------------------------------------------------------------------------
layers = []
# The crusher house over the centre: four 3x3 stone piers at its corners and a stone-slab roof six courses
# over the floor, open on every side. Stated for the whole board, off the mirror.
crusher = props.LayerBuilder("crusher-piers", mirrors=False)
for cx, cz in [(-10, -10), (8, -10), (-10, 8), (8, 8)]:
    crusher.rect(cx, cz, cx + 3, cz + 3, FLOOR - 1, 7, "brick")
roof = props.LayerBuilder("crusher-roof", mirrors=False)
roof.rect(-11, -11, 12, 12, FLOOR + 6, 1, "brick")
layers += made([crusher.done(), roof.done()], "crusher-house")
# The conveyor gantry: a timber deck at the rim's height from rim to rim across the pit, on log trestles
# stood on whatever they land on, passing over the crusher's roof.
gantry = props.LayerBuilder("gantry-deck", mirrors=False)
gantry.rect(-56, -3, 56, 3, RIM, 1, "timber", keepClear=False)
layers += made(gantry.done(), "gantry")
trestle = props.LayerBuilder("gantry-trestles", mirrors=False)
for x in (-54, -32, -21, 20, 31, 53):
    for z in (-3, 2):
        base = BENCH - 1 if abs(x + 0.5) > 30 else FLOOR - 1
        trestle.rect(x, z, x + 1, z + 1, base, RIM - base, "post")
layers += made(trestle.done(), "gantry")
# Quarried blocks as cover: small (two courses) on the floor and the benches, and two large stacks by the
# flank hills that a player goes round from two sides — one stated here, beside the west hill on this team's
# side, and its image beside the east hill on the other. One team's half, fanned.
cover = props.LayerBuilder("cover-blocks")
for x0, z0, w, d, h in [(-22, 6, 3, 2, 2), (-16, 16, 2, 3, 3), (16, 10, 2, 2, 2), (6, 20, 2, 3, 2),
                        (-28, 4, 2, 3, 2), (12, 16, 2, 2, 2)]:
    cover.rect(x0, z0, x0 + w, z0 + d, FLOOR - 1, h + 1, "blocks")
for x0, z0, w, d, h in [(-36, 14, 3, 2, 2), (34, 12, 3, 3, 3), (-48, 24, 3, 2, 2)]:
    cover.rect(x0, z0, x0 + w, z0 + d, BENCH - 1, h + 1, "blocks")
for x0, z0, w, d in [(-46, 8, 6, 7)]:
    cover.rect(x0, z0, x0 + w, z0 + d, BENCH - 1, 6, "blocks")
layers += made(cover.done(), "cover-blocks")

# --- patches ----------------------------------------------------------------------------------------------
# Turf on the rim outside the bench, one ring for the board.
outer = [[-64, -72], [64, -72], [64, 72], [-64, 72]]
shapes = [{"id": "rim-turf", "type": "polygon", "operation": "add",
           "vertices": outer + [outer[0]] + list(reversed(ring(-0.5, -0.5, 53, 45, 48))) + [ring(-0.5, -0.5, 53, 45, 48)[-1]],
           "base_height": RIM, "theme": "turf", "group": "team"}]

# --- dressing --------------------------------------------------------------------------------------------
TREES = ["tree-showcase-r8-2", "tree-showcase-r8-4"]
styles = dict(copied_trees(HERE, TREES))
styles["works"] = house_style("hw-stonehouse")

props_ = [
    path("road-a", 41, ROAD_A, PAVE, radius=2, wander=0),
    path("road-b", 42, ROAD_B, PAVE, radius=2, wander=0),
    path("rim-road", 43, [[-12, 70], [0, 71], [12, 70]], PAVE, radius=2, wander=0),
    pool("sump", ring(-2, 17, 4, 3, 20, 0.15, 3), depth=2, shelf=2, shore=1,
         bank=cell([S(13), S(12, 1)], 2, 61)),
    house("works-a", "works", [[-54, 50], [-46, 58]], front="posX", seed=31, storeys=2),
    house("works-b", "works", [[44, 52], [52, 59]], front="negX", seed=32),
    tree("a1", -56, 36, "tree-showcase-r8-2", 1), tree("a2", -58, 64, "tree-showcase-r8-4", 2),
    tree("a3", 56, 36, "tree-showcase-r8-4", 3), tree("a4", 24, 66, "tree-showcase-r8-2", 4),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 37},
    "themes": {"quarry": quarry, "turf": turf, "brick": brick, "timber": timber, "post": post,
               "blocks": blocks},
    "mapTheme": "quarry",
    "relief": relief,
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": "@sb-spawn"},
    "controlPoints": [
        {"name": "Crusher", "anchor": {"x": 0, "z": 0}, "size": 7, "points": 2},
        {"name": "West Bench", "anchor": {"x": -42, "z": 0}, "size": 7, "points": 1},
        {"name": "East Bench", "anchor": {"x": 41, "z": -1}, "size": 7, "points": 1},
    ],
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG)
