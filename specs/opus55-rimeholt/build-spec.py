"""Rimeholt — writes opus55-rimeholt.plan.json and .finish.json.

A capture board in snow and spruce: each team's hub is a snowfield leaning up from its frontline to a timber
lookout on a hamlet behind it, log cabins on its corners, spruce fells off both its coasts, with a frozen tarn in its west corner and spruce standing along
its coasts. A ring of standing stones stands on the mid stone in the build band. Two wools a team, each at
the end of a spur behind a bedrock wall.

The arrangement is composed board p12 t2 #7 (`composed-p12-seed7.plan.json`, pinned off GET /api/compose).
One piece is added — the hamlet, twenty by eight blocks behind the hub's west half, flush with the spawn — and
nothing else about where the pieces stand is changed. Team 0 is the z > 0 half; rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (S, cell, noise, depth, beds, by_slope, theme, one, ROCK, ring, patch, path, tree,
                        boulder, house, flora, house_style, boulder_style, copied_trees, made, coast_edits)
import props

SLUG = "opus55-rimeholt"
plan = json.load(open(os.path.join(HERE, "composed-p12-seed7.plan.json")))
plan["meta"] = {"name": "Rimeholt", "authors": ["Opus 5.5"],
                "notes": "composed p12 t2 seed 7 (walled-4), with a hamlet piece added behind the hub"}
plan["pieces"].append({"id": "hamlet", "rect": [-4, 20, 5, 2]})   # flush with the spawn, no gap (WL12)

# --- paint ----------------------------------------------------------------------------------------------
# Families: the ground white (snow over packed ice, grey rock where it is too steep to hold snow), the built
# brown (spruce logs laid and stood), the accent grey (the standing stones, the gravel of the paths).
SNOW = noise([S(174), S(80), S(80), S(80)], scale=3, seed=4)
snowfield = theme(by_slope((32, depth(SNOW, S(80))), (12, depth(cell([S(80), S(1), S(1, 5)], 2, 5), S(1))),
                           (46, cell([S(1), S(1, 5), S(1), S(4)], 2, 6))), wall=ROCK, fill=ROCK)
# Under the spruce: podzol and coarse dirt, the needle floor the snow does not lie on.
needles = theme(by_slope((46, depth(noise([S(80), S(3, 2), S(3, 2), S(3, 1)], 2, 7), S(3))),
                         (44, cell([S(1), S(1, 5), S(4)], 2, 8))), wall=ROCK, fill=ROCK)
# The tarn: packed ice set a course into the snow.
tarn = theme(depth(cell([S(174), S(174), S(79)], 2, 9), S(1)), wall=ROCK, fill=ROCK, depth_=1)
stones = one(cell([S(1), S(1, 5), S(1, 6)], 2, 10, rise=2))
spruce = one(S(5, 1))
logpost = one(S(17, 1))

PAVE = cell([S(13), S(4), S(1, 5)], size=2, seed=21)

relief = {"team": {
    "base": 10, "reach": 0, "step": 1, "landform": "rolling",
    "marks": [
        {"id": "front", "kind": "area", "h": 9, "ring": [[-17, 20], [17, 20], [17, 36], [-17, 36]]},
        {"id": "hub-back", "kind": "area", "h": 14, "bevel": 4, "ring": [[-17, 66], [17, 66], [17, 93], [-17, 93]]},
        {"id": "tarn-bed", "kind": "area", "h": 11, "bevel": 2, "ring": ring(-9, 52, 6, 5, 20, 0.12, 3)},
        {"id": "spur-a", "kind": "line", "r": 6, "tread": 4, "points": [[-18, 74], [-38, 74]], "h": [13, 12]},
        {"id": "spur-b", "kind": "line", "r": 6, "tread": 4, "points": [[18, 58], [38, 58]], "h": [12, 11]},
    ],
    "pushes": [
        # fells centred off the hub's two coasts: the spruce stands on their flanks, the snowfield between
        {"id": "fell-west", "ring": ring(-27, 50, 10, 12, 24, 0.15, 3), "amount": 8, "falloff": 7,
         "roughness": 0.4, "crown": 0, "seed": 5},
        {"id": "fell-east", "ring": ring(28, 36, 8, 7, 24, 0.15, 3, 1), "amount": 6, "falloff": 6,
         "roughness": 0.4, "crown": 0, "seed": 6},
    ],
}}

# --- made things -------------------------------------------------------------------------------------------
layers = []
# Standing stones on the mid stone: eight, round its middle, belonging to nobody.
layers += made(props.colonnade("stones", -0.5, -0.5, 7, 8, 1.3, 9, 4, "stones", mirrors=False), "stones",
               seat="ground")
# The lookout over the hamlet: four log legs, a spruce deck nine up, and a roof over it on posts.
LX, LZ = -14, 82
legs = props.LayerBuilder("lookout-legs")
for dx in (0, 4):
    for dz in (0, 4):
        legs.rect(LX + dx, LZ + dz, LX + dx + 1, LZ + dz + 1, 13, 14, "logpost")
deck = props.LayerBuilder("lookout-deck")
deck.rect(LX + 1, LZ + 1, LX + 4, LZ + 4, 21, 1, "spruce")
roof = props.LayerBuilder("lookout-roof")
roof.rect(LX - 1, LZ - 1, LX + 6, LZ + 6, 27, 1, "spruce")
layers += made([legs.done(), deck.done(), roof.done()], "lookout")
# Log piles on the frontline's two prongs, cover two courses tall.
piles = props.LayerBuilder("log-piles")
for x0, z0, x1, z1 in [(-14, 22, -11, 24), (11, 25, 14, 27), (-6, 31, -3, 33), (4, 34, 7, 36)]:
    piles.rect(x0, z0, x1, z1, 9, 2, "logpost")
layers += made(piles.done(), "log-piles", seat="ground")

# --- patches -------------------------------------------------------------------------------------------
shapes = [
    patch("tarn", ring(-9, 52, 5, 4, 20, 0.12, 3), "tarn", 9, group="team"),
    patch("needles-west", [[-17, 40], [-9, 41], [-8, 46], [-9, 60], [-11, 66], [-17, 66]], "needles", 9,
          group="team"),
    patch("needles-east", [[11, 40], [17, 40], [17, 54], [11, 54]], "needles", 9, group="team"),
]

# --- dressing -------------------------------------------------------------------------------------------
TREES = ["tree-showcase-r7-1", "tree-showcase-r7-3", "tree-showcase-r4-2", "tree-showcase-r4-4"]
styles = dict(copied_trees(HERE, TREES))
styles["cabin"] = house_style("talltimber-cottage")
styles["rock"] = boulder_style(cell([S(1), S(1, 5), S(4)], 2, 31), form="angular", size=2)

props_ = [
    path("path-front", 51, [[10, 82], [8, 70], [2, 56], [0, 42], [0, 30]], PAVE),
    path("path-wool-a", 52, [[-4, 74], [-16, 74], [-26, 74]], PAVE, wander=1),
    path("path-wool-b", 53, [[4, 58], [16, 58], [24, 58]], PAVE, wander=1),
    house("cabin-a", "cabin", [[-16, 63], [-9, 70]], front="posX", seed=31),
    house("cabin-b", "cabin", [[12, 44], [16, 49]], front="negX", seed=32),
    tree("s1", -15, 44, "tree-showcase-r7-1", 1), tree("s2", -15, 58, "tree-showcase-r7-3", 2),
    tree("s6", 14, 52, "tree-showcase-r4-2", 6),
    boulder("r1", -12, 26, "rock", 7),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 30},
    "themes": {"snowfield": snowfield, "needles": needles, "tarn": tarn, "stones": stones, "spruce": spruce,
               "logpost": logpost},
    "mapTheme": "snowfield",
    "relief": relief,
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": "@talltimber-hall", "wool": "@talltimber-hall"},
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
