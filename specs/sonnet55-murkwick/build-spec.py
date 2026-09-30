"""Murkwick — writes sonnet55-murkwick.plan.json and .refinement.json for the stage in $STAGE (1..4).

The arrangement is composed board p16 t2 seed 43 (`composed-p16-seed43.plan.json`, pinned off GET /api/compose),
taken whole. Team 0 is the z > 0 half; rot_180 fans the rest.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools", "sculpt"))
from opus55_kit import (ring, coast_edits, pool, channel, made, patch, path, tree, boulder, house, flora,
                        boulder_style, copied_trees)
from sonnet55_kit import *
import props

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet55-murkwick"
STAGE = int(os.environ.get("STAGE", "4"))

plan = json.load(open(os.path.join(HERE, "composed-p16-seed43.plan.json")))
plan["meta"] = {"name": "Murkwick", "authors": ["Sonnet 5.5"],
                "notes": "composed p16 t2 seed 43 (walled-4), arrangement unchanged"}
finish = {"created": "2026-09-29", "authors": ["Sonnet 5.5"]}

# --- stage 2: the outer coasts reshaped point by point, the relief, the water. No theme. -------------------------------
# The ring the plan compiles the team-0 ground to. Its wall seams (x -29..-27 and 27..29), the wool rooms' faces
# and the frontline's face to the band stay exactly as the composer cut them.
GROUND = [[-48, 68], [-24, 68], [-24, 32], [-20, 32], [-20, 24], [-4, 24], [-4, 32], [8, 32], [8, 24], [20, 24],
          [20, 32], [24, 32], [24, 60], [48, 60], [48, 72], [24, 72], [24, 96], [12, 96], [12, 108], [-4, 108],
          [-4, 96], [-24, 96], [-24, 80], [-48, 80]]
VARIANT = os.environ.get("RELIEF", "d")


def relief(variant):
    spur_a = {"id": "spur-a", "kind": "area", "h": 9, "bevel": 0, "ring": [[-50, 64], [-26, 64], [-26, 84], [-50, 84]]}
    spur_b = {"id": "spur-b", "kind": "area", "h": 9, "bevel": 0, "ring": [[26, 56], [50, 56], [50, 76], [26, 76]]}
    front = {"id": "front", "kind": "area", "h": 9, "bevel": 0, "ring": [[-24, 22], [24, 22], [24, 44], [-24, 44]]}
    mid = {"id": "mid", "kind": "area", "h": 9, "bevel": 0, "ring": [[-17, -13], [17, -13], [17, 13], [-17, 13]]}
    if variant == "a":      # a flat swamp: the hub two over the frontline and nothing else
        marks = [front, mid, spur_a, spur_b,
                 {"id": "hub", "kind": "area", "h": 11, "bevel": 0, "ring": [[-21, 52], [21, 52], [21, 98], [-21, 98]]},
                 {"id": "spawn", "kind": "area", "h": 11, "bevel": 0, "ring": [[-6, 98], [14, 98], [14, 110], [-6, 110]]}]
        pushes = []
    elif variant == "b":    # the hub a village island three over the wet flat, grading up across the front bar
        marks = [front, mid, spur_a, spur_b,
                 {"id": "hub", "kind": "area", "h": 12, "bevel": 0, "ring": [[-21, 52], [21, 52], [21, 98], [-21, 98]]},
                 {"id": "spawn", "kind": "area", "h": 12, "bevel": 0, "ring": [[-6, 98], [14, 98], [14, 110], [-6, 110]]}]
        pushes = [
            {"id": "hummock-w", "ring": ring(-19, 29, 4, 3, 12, 0.1, 3), "amount": 2, "falloff": 5, "crown": 0, "seed": 4},
            {"id": "hummock-e", "ring": ring(19, 30, 4, 3, 12, 0.1, 3), "amount": 2, "falloff": 5, "crown": 0, "seed": 5},
        ]
    elif variant == "d":    # b with the hub's bars carrying low hammocks, so the island is not a table
        marks = [front, mid, spur_a, spur_b,
                 {"id": "hub", "kind": "area", "h": 12, "bevel": 0, "ring": [[-21, 52], [21, 52], [21, 98], [-21, 98]]},
                 {"id": "spawn", "kind": "area", "h": 12, "bevel": 0, "ring": [[-6, 98], [14, 98], [14, 110], [-6, 110]]}]
        pushes = [
            {"id": "hummock-w", "ring": ring(-19, 29, 4, 3, 12, 0.1, 3), "amount": 2, "falloff": 5, "crown": 0, "seed": 4},
            {"id": "hummock-e", "ring": ring(19, 30, 4, 3, 12, 0.1, 3), "amount": 2, "falloff": 5, "crown": 0, "seed": 5},
            {"id": "ham-1", "ring": ring(15, 57, 5, 4, 14, 0.12, 3), "amount": 3, "falloff": 6, "crown": 0, "seed": 6},
            {"id": "ham-2", "ring": ring(17, 88, 4, 4, 14, 0.12, 3), "amount": 3, "falloff": 5, "crown": 0, "seed": 7},
            {"id": "ham-3", "ring": ring(-16, 72, 4, 5, 14, 0.12, 3), "amount": 2, "falloff": 5, "crown": 0, "seed": 8},
            {"id": "ham-4", "ring": ring(17, 74, 3, 4, 14, 0.12, 3), "amount": 2, "falloff": 5, "crown": 0, "seed": 9},
            {"id": "ham-5", "ring": ring(-14, 60, 3, 3, 14, 0.12, 3), "amount": 2, "falloff": 4, "crown": 0, "seed": 10},
        ]
    else:                   # a sunken bog: the hub at 10 with its bars' middles hollowed to basins, rims left standing
        marks = [front, mid, spur_a, spur_b,
                 {"id": "hub", "kind": "area", "h": 10, "bevel": 0, "ring": [[-21, 52], [21, 52], [21, 98], [-21, 98]]},
                 {"id": "spawn", "kind": "area", "h": 10, "bevel": 0, "ring": [[-6, 98], [14, 98], [14, 110], [-6, 110]]}]
        pushes = [
            {"id": "basin-f", "ring": ring(-6, 56, 10, 4, 14, 0.1, 3), "amount": -3, "falloff": 5, "crown": 0, "seed": 4},
            {"id": "basin-b", "ring": ring(8, 88, 10, 4, 14, 0.1, 3), "amount": -3, "falloff": 5, "crown": 0, "seed": 5},
        ]
    return {"team": {"base": 9, "reach": 0, "step": 1, "landform": "plain", "marks": marks, "pushes": pushes}}


if STAGE >= 2:
    finish["relief"] = relief(VARIANT)
    finish["editShapes"] = {"frontline-t1-9": coast_edits(GROUND, {
        0: [(0.58, 2)],
        1: [(0.15, 3), (0.35, 5), (0.55, 2), (0.75, 4), (0.90, 1)],
        11: [(0.12, 2), (0.30, 5), (0.50, 2), (0.70, 4), (0.88, 1)],
        12: [(0.42, 2)],
        14: [(0.58, 2)],
        15: [(0.20, 3), (0.50, 5), (0.80, 2)],
        16: [(0.5, 2)],
        20: [(0.3, 3), (0.7, 2)],
        21: [(0.25, 4), (0.60, 2)],
        22: [(0.42, 2)],
    })}
    finish["dressing"] = {"styles": {}, "props": [
        pool("pond-front", ring(-4, 56, 8, 3.5, 14, 0.1, 3), depth=2, shelf=2, shore=1),
        pool("pond-back", ring(-12, 88, 7, 3.5, 14, 0.1, 3), depth=2, shelf=2, shore=1),
    ]}

# --- stage 3: made things on layers, the biome, the themes finished by angle, patches, room styles --------------------
# Three families, named before any theme: the GROUND is olive and brown — swamp-tinted turf with podzol and coarse
# dirt, which Swampland's tint meets rather than fights; what is BUILT is dark timber, dark oak and spruce; the ACCENT
# is thatch, hay bale, on every roof and on the mid stone's platform.
MUD = cell([S(DIRT, 0), S(DIRT, 0), S(*PODZOL), S(*COARSE)], 2, 41)
if STAGE >= 3:
    PODSET = cell([S(*PODZOL), S(*COARSE), S(*PODZOL)], 2, 3)
    TURF = noise([PODSET, S(GRASS), S(GRASS), S(GRASS), cell([S(*COARSE), S(DIRT, 0)], 2, 4)], scale=2, seed=17)
    SOIL = cell([S(DIRT, 0), S(*COARSE)], 2, 5)
    EARTH = cell([S(*PODZOL), S(*COARSE), S(DIRT, 0)], 2, 6)
    SOILR = cell([S(*COARSE), S(DIRT, 0)], 2, 5, rise=2)
    STRATA = [(SOILR, 3), (ROCK, 5), (SOILR, 1), (ROCK, 4)] * 9
    bog = theme(by_slope((40, depth(TURF, SOIL)), (14, depth(EARTH, SOIL)), (36, ROCK)),
                wall=beds(STRATA, start=-40, reach=16, beyond=ROCK), fill=beds(STRATA, start=-40, reach=16, beyond=ROCK))
    mud = theme(depth(MUD, S(DIRT, 0)), wall=ROCK, fill=ROCK)
    peat = theme(depth(cell([S(*PODZOL), S(*PODZOL), S(*COARSE), S(DIRT, 0)], 2, 43), S(DIRT, 0)), wall=ROCK, fill=ROCK)
    timber = one(cell([S(*DARKOAK_PLANK), S(*SPRUCE_PLANK), S(*DARKOAK_PLANK), S(*DARKOAK_PLANK)], 2, 22, rise=2))
    thatch = one(cell([S(HAY), S(HAY)], 2, 23, rise=2))
    finish["biome"] = {"kind": "solid", "id": 6}
    finish["themes"] = {"bog": bog, "mud": mud, "peat": peat, "timber": timber, "thatch": thatch}
    finish["mapTheme"] = "bog"
    finish["addShapes"] = [
        patch("mudflat", [[-14, 34], [10, 34], [12, 42], [-16, 44]], "mud", 9, group="team"),
        patch("peat-1", ring(15, 57, 4, 3.2, 14, 0.12, 3), "peat", 9, group="team"),
        patch("peat-2", ring(17, 88, 3.4, 3.2, 14, 0.12, 3), "peat", 9, group="team"),
        patch("peat-3", ring(-16, 72, 3.2, 4, 14, 0.12, 3), "peat", 9, group="team"),
    ]
    for p_ in finish["dressing"]["props"]:
        p_["bank"] = MUD

    layers = []
    # The mid stone's platform: one for the board, so off the mirror. Four corner posts and a deck on stilts three
    # over the stone, a hay roof on four posts over it, and a stair of three steps up the east side.
    hut = props.LayerBuilder("hut-deck", name="Stilt platform deck", mirrors=False)
    hut.rect(-7, -4, 5, 4, 12, 1, "timber")
    layers += made(hut.done(), "stilt-platform")
    legs = props.LayerBuilder("hut-legs", name="Stilt platform legs", mirrors=False)
    for x, z in [(-7, -4), (4, -4), (-7, 3), (4, 3)]:
        legs.rect(x, z, x + 1, z + 1, 9, 3, "timber")
    for h, x in zip((3, 2, 1), (5, 6, 7)):
        legs.rect(x, -1, x + 1, 1, 9, h, "timber")
    layers += made(legs.done(), "stilt-platform")
    posts = props.LayerBuilder("hut-posts", name="Roof posts", mirrors=False)
    for x, z in [(-7, -4), (4, -4), (-7, 3), (4, 3)]:
        posts.rect(x, z, x + 1, z + 1, 13, 4, "timber")
    layers += made(posts.done(), "stilt-platform")
    roof = props.spire("hut-roof", -1, 0, 8.5, 17, 4, "thatch", sides=4, mirrors=False, name="Thatch roof")
    layers += made(roof, "stilt-platform")
    # Two planked walks over the ponds, a course over the ground beside the water, and off the kept-clear rule.
    walk = props.LayerBuilder("pond-walk", name="Pond walks")
    walk.rect(-6, 50, -3, 62, 12, 1, "timber", keepClear=False)
    walk.rect(-13, 87, -3, 89, 12, 1, "timber", keepClear=False)
    layers += made(walk.done(), "pond-walk")
    finish["addLayers"] = layers

    finish["roomStyles"] = {
        "spawn": repaint(shipped("showcase-hall"), roof_body={"kind": "solid", "id": HAY, "data": 0}),
        "wool": repaint(shipped("17h-hall"), solids={(45, 0): SPRUCE_PLANK, (5, 0): SPRUCE_PLANK},
                        roof_body={"kind": "solid", "id": HAY, "data": 0})}

# --- stage 4: dressing — the roads first, then ground cover, then trees, rocks and cabins -------------------------------
if STAGE >= 4:
    PAVE = cell([S(*SPRUCE_PLANK), S(*DARKOAK_PLANK), S(*SPRUCE_PLANK), S(*COARSE)], 2, 21)
    props_ = list(finish["dressing"]["props"])
    props_ += [
        # the spawn door down the hub's east side to the front bar, and on to the frontline
        path("road-main", 61, [[5, 98], [8, 92], [15, 86], [18, 78], [16, 68], [12, 58], [8, 50], [6, 46]], PAVE),
        # the front bar's edge west, then north up the hub's west side to the first wool's neck
        path("road-a", 62, [[8, 50], [-4, 49.5], [-14, 50], [-19, 56], [-19, 66], [-21, 73], [-25, 74]], PAVE),
        # and east to the second wool's neck
        path("road-b", 63, [[14, 54], [20, 61], [23, 66], [26, 66]], PAVE, wander=1),
        flora("reed-cover", [[-48, 68], [-24, 68], [-24, 32], [-4, 24], [20, 24], [24, 32], [24, 60], [48, 60], [48, 72], [24, 72],
                              [24, 96], [12, 96], [12, 108], [-4, 108], [-4, 96], [-24, 96], [-24, 80], [-48, 80]],
              coverage=0.35, scale=8, fern=0.3, flowers=0.02, flower_scale=10, tall=0.03, seed=5),
    ]
    finish["dressing"]["props"] = props_

    # Cover on the frontline: hay stacks two and three courses tall, off the road and off the hummocks — a box a
    # player crouches behind, which is what a capture board wants small cover to be.
    stacks = props.LayerBuilder("hay-stacks", name="Hay stacks")
    for x0, z0, x1, z1, h in [(-16, 27, -12, 29, 2), (-9, 34, -6, 36, 2), (10, 27, 13, 29, 3), (15, 35, 18, 37, 2),
                              (-20, 43, -17, 45, 2)]:
        stacks.rect(x0, z0, x1, z1, 9, h, "thatch")
    finish["addLayers"] += made(stacks.done(), "hay-stacks", seat="ground")

    # Two species and no third: willows (row r17) on the ring and the back bar, and under them a small oak (row r6).
    WILLOW = [f"tree-showcase-r17-{i}" for i in range(1, 6)]
    OAK = [f"tree-showcase-r6-{i}" for i in (1, 4, 6)]
    finish["dressing"]["styles"] = dict(copied_trees(HERE, WILLOW + OAK))
    # The marsh: the frontline's middle drowned a course deep, so the contested ground is waded and the hay stacks stand
    # in it as dry hummocks. Water on ground pinned level, so it digs no trench.
    finish["dressing"]["props"] += [
        pool("marsh", ring(-2, 39, 12, 5, 18, 0.15, 3), depth=1, shelf=1, shore=1, bank=MUD),
    ]
    finish["dressing"]["props"] += [
        tree("w-2", -13, 68, WILLOW[2], 2), tree("w-3", 10, 74, WILLOW[1], 3),
        tree("w-4", 19, 92, WILLOW[3], 4), tree("w-5", -17, 44, WILLOW[4], 5),
        tree("o-1", 6, 61, OAK[0], 6), tree("o-2", -6, 81, OAK[1], 7),
    ]

json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
json.dump(finish, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
print("wrote", SLUG, "stage", STAGE)
