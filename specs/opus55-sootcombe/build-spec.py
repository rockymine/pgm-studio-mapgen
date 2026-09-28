"""Sootcombe — writes opus55-sootcombe.plan.json and .finish.json.

A capture board on an ash field: a combe of grey slag falling from each team's brick hamlet, standing on a
terrace four blocks over its hub, down to a flat frontline and a slag stone in the middle of the build band
with a ruined engine house on it. Two wools a team: one at the end of a spur west of the hub behind a
bedrock wall, one at the east end of the terrace behind another. A timber headframe stands over the shaft
at the hub bar's west end, beside the slag heap the shaft threw up.

The arrangement is composed board p12 t2 #21 (`composed-p12-seed21.plan.json`, pinned off GET /api/compose),
taken whole: this spec states its elevation, its paint, its made things and its dressing, and nothing about
where the pieces are. Team 0 is the z > 0 half; rot_180 fans the rest.

Second pass, after the author's review: the first build was bare ash. The ash is now gravel and andesite, since
both stained clays read as terracotta in game (note 6), the heap is slag, the outer coasts are cut point by point, the mid
stone carries the engine house, the frontline carries timber stacks for cover, the hub bar carries the
headframe, and birch and tiny spruce stand on regrowth along the hub's outer rims.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (S, cell, noise, depth, by_slope, theme, one, ROCK, ring, patch, path, tree, flora,
                        boulder, boulder_style, copied_trees, made, coast_edits)
import props

SLUG = "opus55-sootcombe"
plan = json.load(open(os.path.join(HERE, "composed-p12-seed21.plan.json")))
plan["meta"] = {"name": "Sootcombe", "authors": ["Opus 5.5"],
                "notes": "composed p12 t2 seed 21 (walled-4), arrangement unchanged"}

# The one fused ground shape the plan compiles to, as it compiles.
GROUND = [[-44, 56], [-20, 56], [-20, 40], [-16, 40], [-16, 20], [16, 20], [16, 40], [0, 40], [0, 68],
          [36, 68], [36, 80], [-4, 80], [-4, 96], [-16, 96], [-16, 80], [-20, 80], [-20, 68], [-44, 68]]

# --- paint -----------------------------------------------------------------------------------------------
# Three families: the ground grey (gravel and andesite ash), the built warm (brick and dark oak), the
# accent granite in the paths and the black of the slag.
LGREY, GREY, BLACK = S(159, 8), S(159, 7), S(159, 15)
WORN = cell([S(3, 1), S(3, 0)], 2, 7)
# Stained clay was tried first, grey and then light grey, and in the game's textures both read as brown
# terracotta rather than ash. The ground is gravel, andesite and stone instead — one grey carried by three
# textures — with coal-dark slag at one end of the stop list and worn earth at the other.
ASH_SET = cell([S(13), S(13), S(1, 5), S(1)], 2, 4)
ASH = noise([WORN, ASH_SET, ASH_SET, ASH_SET, BLACK], scale=2, seed=5)
SHOULDER = cell([S(1, 5), S(1), S(13)], 2, 6)
ash = theme(by_slope((30, depth(ASH, S(1, 5))), (15, depth(SHOULDER, S(1, 5))), (45, ROCK)), wall=ROCK, fill=ROCK)
# The heap: slag — black clay, gravel and coal-dark cobble, loose on its flanks.
SLAG = noise([S(13), BLACK, BLACK, S(4), GREY], scale=2, seed=9)
slag = theme(by_slope((25, depth(SLAG, BLACK)), (65, depth(cell([S(13), BLACK, S(4)], 2, 10), BLACK))),
             wall=cell([BLACK, S(4), S(1)], 2, 11, rise=2), fill=ROCK)
# Regrowth: grass and worn earth where birch has taken hold on the spoil.
regrowth = theme(by_slope((30, depth(noise([WORN, S(2), S(2), S(2)], 2, 12), S(3))), (60, ROCK)),
                 wall=ROCK, fill=ROCK)
# Made: brick walls, dark-oak timber, a brick stack.
brick = one(cell([S(45), S(45), S(45), S(98)], 2, 21, rise=2))
timber = one(S(5, 5))
post = one(S(162, 1))

PAVE = cell([S(1, 1), S(1, 2), S(45), S(1, 1)], size=2, seed=21)

relief = {"team": {
    "base": 10, "reach": 0, "step": 1, "landform": "rolling",
    "marks": [
        {"id": "terrace", "kind": "area", "h": 13, "ring": [[-20, 70], [36, 70], [36, 97], [-20, 97]]},
        {"id": "front", "kind": "area", "h": 9, "ring": [[-17, 20], [17, 20], [17, 33], [-17, 33]]},
        {"id": "spur", "kind": "line", "r": 6, "tread": 4, "points": [[-22, 62], [-42, 62]], "h": [11, 10]},
    ],
    "pushes": [
        {"id": "heap", "ring": ring(-28, 80, 10, 8, wobble=0.12, lobes=3), "amount": 8, "falloff": 4,
         "roughness": 0.4, "crown": 0, "seed": 9},
    ],
}}

# --- made things -----------------------------------------------------------------------------------------
layers = []

# The engine house on the mid stone, one for the board and so off the mirror: a roofless brick shell with a
# doorway in each long side, and two stacks at opposite corners so it is the same building from both sides.
eh = props.LayerBuilder("engine-walls", mirrors=False)
for x0, z0, x1, z1 in [(-6, -4, 6, -3),      # north wall
                       (-6, 3, 6, 4),        # south wall
                       (-6, -3, -5, -1), (-6, 1, -5, 3),   # west wall, a door between
                       (5, -3, 6, -1), (5, 1, 6, 3)]:      # east wall, a door between
    eh.rect(x0, z0, x1, z1, 10, 7, "brick")
layers += made(eh.done(), "engine-house")
# One stack, stated once and fanned: its rot_180 image is the other corner's.
layers += made(props.tapered_tower("engine-stack", 4.5, -6.5, 2.2, 1.5, 1.2, 10, 16, "brick", courses=4),
               "engine-house")

# The headframe over the shaft at the hub bar's west end: four log legs, a timber frame halfway up, a cap.
HX, HZ, HW = -17, 71, 5          # its west-north corner and its width
legs = props.LayerBuilder("headframe-legs")
for dx in (0, HW - 1):
    for dz in (0, HW - 1):
        legs.rect(HX + dx, HZ + dz, HX + dx + 1, HZ + dz + 1, 12, 15, "post")
frame = props.LayerBuilder("headframe-frame")
for x0, z0, x1, z1 in [(HX + 1, HZ, HX + HW - 1, HZ + 1), (HX + 1, HZ + HW - 1, HX + HW - 1, HZ + HW),
                       (HX, HZ + 1, HX + 1, HZ + HW - 1), (HX + HW - 1, HZ + 1, HX + HW, HZ + HW - 1)]:
    frame.rect(x0, z0, x1, z1, 20, 1, "timber")
cap = props.LayerBuilder("headframe-cap")
cap.rect(HX - 1, HZ - 1, HX + HW + 1, HZ + HW + 1, 27, 2, "timber")
layers += made([legs.done(), frame.done(), cap.done()], "headframe")

# Timber stacks on the frontline: cover two and three courses tall, off the paths and off the edge.
stacks = props.LayerBuilder("timber-stacks")
for x0, z0, x1, z1, h in [(-12, 26, -9, 28, 3), (6, 31, 8, 34, 2), (-4, 35, -1, 37, 2), (10, 24, 13, 26, 3)]:
    stacks.rect(x0, z0, x1, z1, 9, h, "timber")
layers += made(stacks.done(), "timber-stacks", seat="ground")

# --- patches -------------------------------------------------------------------------------------------
shapes = [
    patch("heap-slag", ring(-26, 80, 10, 9, 24, 0.15, 3), "slag", 9, group="team"),
    patch("regrowth-west", [[-20, 42], [-14, 43], [-13, 52], [-15, 60], [-14, 67], [-20, 67]], "regrowth", 9,
          group="team"),
    patch("regrowth-bar", [[-2, 76], [10, 76], [12, 80], [-2, 80]], "regrowth", 9, group="team"),
]

# --- dressing ------------------------------------------------------------------------------------------
TREES = ["tree-showcase-r13-2", "tree-showcase-r4-1", "tree-showcase-r4-3"]
styles = dict(copied_trees(HERE, TREES))

props_ = [
    path("path-front", 51, [[-10, 86], [-10, 72], [-8, 54], [-4, 38], [0, 23]], PAVE),
    path("path-wool-a", 52, [[-12, 60], [-24, 62], [-33, 62]], PAVE, wander=1),
    path("path-wool-b", 53, [[-6, 75], [8, 74], [25, 74]], PAVE, wander=1),
    tree("birch-1", -18, 45, "tree-showcase-r13-2", 1),
    tree("spruce-1", -18, 54, "tree-showcase-r4-1", 3),
    tree("spruce-2", 0, 78, "tree-showcase-r4-3", 4),
    flora("regrowth-cover", [[-21, 41], [-12, 41], [-12, 68], [-21, 68]], coverage=0.3, scale=6, fern=0.4,
          flowers=0.03, tall=0.02, seed=8),
]

finish = {
    "created": "2026-09-28",
    "authors": ["Opus 5.5"],
    "biome": {"kind": "solid", "id": 32},
    "themes": {"ash": ash, "slag": slag, "regrowth": regrowth, "brick": brick, "timber": timber, "post": post},
    "mapTheme": "ash",
    "relief": relief,
    # The outer coasts only. The frontline's face to the band, the wall seams at x -24 and x 12, and the
    # wool rooms' own faces stay as the composer cut them.
    "editShapes": {"frontline-t1-9": coast_edits(GROUND, {
        0: [(0.25, 1), (0.5, 2)],                 # the spur's south coast, west of its wall
        1: [(0.3, 2), (0.7, 3)],                  # the hub's west coast
        3: [(0.3, 2), (0.65, 1)],                 # the frontline's west coast
        5: [(0.4, 2), (0.75, 1)],                 # the frontline's east coast
        7: [(0.25, 2), (0.5, 3), (0.8, 1)],       # the hub's east coast, along the hole
        8: [(0.14, 2)],                           # the east approach's south coast, short of its wall
        16: [(0.5, 2), (0.78, 1)],                # the spur's north coast
    })},
    "addShapes": shapes,
    "addLayers": layers,
    "roomStyles": {"spawn": "@lk-spawn", "wool": "@lk-spawn"},
    "dressing": {"styles": styles, "props": props_},
}

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.finish.json"), "w"), indent=1)
print("wrote", SLUG)
