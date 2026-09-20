#!/usr/bin/env python3
"""Orchard Holm — example 3, widened where it had no room, with a holm in the middle.

Three changes to the board the author drew:

  * the lane straight out of spawn runs 5 blocks further into the void, and the build zone with it.
    A 15-block lane takes a 7-block building and nothing else; 20 takes a 12-block one, which is a
    house rather than a shed. That is what the widening is for and where the houses go.
  * the terrain either side of the middle is pulled back 10 blocks, which leaves 50 blocks of gap.
  * a holm sits in the middle of it, 30 by 20, two courses above the team ground, with a golden
    apple generator on its own 2x2 pad at the board's centre.

Run: python3 specs/opus5-orchard-holm/build-spec.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CELL = 5


def rect(x, z, w, h):
    return [x, z, w, h]


plan = {
    "plan": 2,
    "meta": {"name": "Orchard Holm"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12, "surface": 9},
    "pieces": [
        # The spawn, and the lane straight out of it — a cell wider to the west than the author drew,
        # which is the 20 blocks a house needs to stand in and still leave a way past.
        {"id": "spawn-yard", "role": "spawn", "rect": rect(-4, -17, 3, 3)},
        {"id": "broadway", "role": "piece", "rect": rect(-5, -14, 4, 5)},
        {"id": "market-bar", "role": "piece", "rect": rect(-5, -9, 9, 3)},
        {"id": "front-west", "role": "piece", "rect": rect(-5, -6, 4, 1)},
        # The east lane and the room it leads to, as drawn.
        {"id": "east-lane", "role": "piece", "rect": rect(-1, -14, 6, 3)},
        {"id": "east-spur", "role": "piece", "rect": rect(1, -11, 3, 2)},
        {"id": "front-east", "role": "piece", "rect": rect(1, -6, 3, 1)},
        {"id": "wool-approach", "role": "piece", "rect": rect(5, -14, 3, 3)},
        {"id": "wool-room", "role": "wool-room", "rect": rect(8, -14, 3, 3)},
        {"id": "wool-flank", "role": "piece", "rect": rect(8, -11, 3, 5)},
        # The holm: self-mirroring about the board's centre, so one rectangle is the whole island.
        {"id": "holm", "role": "piece", "rect": rect(-3, -2, 6, 4), "surface": 11},
    ],
    "zones": [
        # The water either side of the holm — 15 blocks of it, which is a hop inside G5's band. Its x span
        # is the ground it docks to and not a block more, or it carries on past the last piece it meets.
        {"id": "strait", "rect": rect(-5, -5, 9, 3), "holes": []},
        # The east bridge to the wool island, as drawn.
        {"id": "wool-bridge", "rect": rect(4, -9, 4, 3), "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-yard", "at": [7.5, 7.5], "facing": "back"}],
        "wools": [{"id": "wool-1", "piece": "wool-room", "at": [7.5, 7.5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [{"a": "wool-approach", "b": "east-lane"}],
    "boxes": [],
}


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def depth_stack(bands, beyond):
    return {"kind": "layered", "axis": "depth", "beyond": beyond,
            "stack": {"ending": "handOver", "bands": bands}}


STONE, GRASS, DIRT, COBBLE = 1, 2, 3, 4
COARSE, PODZOL = 1, 2
ANDESITE = 5

# The ground is finished by its ANGLE, not by its height: one stack carries the pasture, the shoulder
# where it falls away and the rock face at the water. A theme hung on pieces or on height bands paints
# a board flat from above however much relief is under it.
turf = depth_stack([{"thickness": 1, "material": solid(GRASS)},
                    {"thickness": 2, "material": solid(DIRT)}], solid(STONE))
shoulder = depth_stack([{"thickness": 1, "material": solid(DIRT, COARSE)},
                        {"thickness": 2, "material": solid(DIRT)}], solid(STONE))
crag = depth_stack([{"thickness": 2, "material": {"kind": "voronoi", "seed": 11, "cellSize": 9, "bands": [
                        {"depth": 1, "material": solid(STONE)},
                        {"depth": 1, "material": solid(COBBLE)},
                        {"depth": 1, "material": solid(STONE, ANDESITE)}]}},
                    {"thickness": 3, "material": solid(STONE)}], solid(STONE))


def by_slope(flat, bank, face):
    """One stack for the flat, the shoulder and the face of the same ground. A thickness on the slope axis
    is a span of DEGREES, and the cuts are where this board's ground actually stands: `incline` reads
    77% under 10 degrees, 22.6% in the teens and 0.5% above twenty, with nothing at all past forty. Bands
    cut at 30 and 45 would have left every cell in the first one and painted the board a flat sheet."""
    return {"kind": "layered", "axis": "slope", "beyond": solid(STONE),
            "stack": {"ending": "repeat", "bands": [
                {"thickness": 10, "material": flat},
                {"thickness": 10, "material": bank},
                {"thickness": 80, "material": face}]}}


def ground_theme(flat, bank, wall):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": solid(COBBLE)},
        "surface": {"enabled": True, "depth": 3, "material": by_slope(flat, bank, crag)},
        "wall": wall,
        "wallEnabled": True,
        "fill": solid(STONE),
    }


# The holm is a second ground, not a second colour: podzol under its trees where the pasture is grass,
# and a gravel strand at the water it stands two courses above.
orchard_turf = depth_stack([{"thickness": 1, "material": {"kind": "voronoi", "seed": 5, "cellSize": 7, "bands": [
                                {"depth": 2, "material": solid(GRASS)},
                                {"depth": 1, "material": solid(DIRT, PODZOL)}]}},
                            {"thickness": 2, "material": solid(DIRT)}], solid(STONE))
GRAVEL = 13
strand = depth_stack([{"thickness": 1, "material": solid(GRAVEL)},
                      {"thickness": 2, "material": solid(DIRT)}], solid(STONE))

# The wall is what a face is painted with, and a face is where the two grounds meet: a cut bank on the
# pasture, and a gravel strand where the holm stands two courses out of the water.
bank_wall = depth_stack([{"thickness": 1, "material": solid(DIRT, COARSE)},
                         {"thickness": 2, "material": solid(DIRT)},
                         {"thickness": 3, "material": solid(STONE, ANDESITE)}], solid(STONE))
strand_wall = depth_stack([{"thickness": 2, "material": solid(GRAVEL)},
                           {"thickness": 2, "material": solid(COBBLE)},
                           {"thickness": 3, "material": solid(STONE)}], solid(STONE))

# Where the buildings go, and every one of them a seat `sketch/seats` offered rather than a guess.
houses = [
    # The house the widening bought. The lane out of spawn is 20 blocks across; this stamps 12 of them
    # against its west wall and leaves 8, which is the passage exactly. On the 15-block lane the author
    # drew, nothing this size could stand anywhere in it.
    {"kind": "house", "id": "longhouse", "seed": 41, "front": "posX", "style": "@17h-hall",
     "wings": [{"corners": [[-25, -53], [-16, -44]]}]},
    # Four blocks off the longhouse's gable: one block of buildings, and the passage goes round the pair.
    # Judged on its own, with the longhouse standing, its north side is a wall and it would be crowded.
    {"kind": "house", "id": "byre", "seed": 42, "front": "posX", "style": "@17h-croft",
     "wings": [{"corners": [[-25, -39], [-21, -35]]}]},
    # And one on the far flank, standing alone, to say what a lone building still costs.
    {"kind": "house", "id": "wool-store", "seed": 43, "front": "negX", "style": "@hoar-store",
     "wings": [{"corners": [[14, -44], [18, -40]]}]},
]

# A prop is stated once and stamped at every image of its orbit, so one side is the whole board. A mark
# is not: the relief group is one side's ground and the rasterizer mirrors what it solves.
trees = [
    {"kind": "tree", "id": f"holm-apple-{i}", "x": x, "z": z, "form": "Template",
     "species": "oak", "height": 7, "seed": 60 + i}
    for i, (x, z) in enumerate([(-12, -7), (-6, -8), (-12, 4)])
] + [
    {"kind": "tree", "id": f"bank-{i}", "x": x, "z": z, "form": "Template",
     "species": "birch", "height": 9, "seed": 70 + i}
    for i, (x, z) in enumerate([(-21, -66), (-21, -60), (49, -34), (46, -36)])
]

boulders = [
    {"kind": "boulder", "id": f"holm-rock-{i}", "x": x, "z": z, "form": "angular", "size": 2,
     "mossy": True, "rock": solid(STONE, ANDESITE), "seed": 80 + i}
    for i, (x, z) in enumerate([(-14, 0), (0, -9)])
] + [
    {"kind": "boulder", "id": f"shore-rock-{i}", "x": x, "z": z, "form": "round", "size": 2,
     "mossy": False, "rock": solid(STONE), "seed": 90 + i}
    for i, (x, z) in enumerate([(-23, -29), (17, -29)])
]

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-15",
    "mapTheme": "pasture",
    "themes": {
        "pasture": ground_theme(turf, shoulder, bank_wall),
        "orchard": ground_theme(orchard_turf, strand, strand_wall),
    },
    "themeById": {"holm-11": "orchard"},
    "roomStyles": {"spawn": "@showcase-hall", "wool": "@showcase-cage"},
    # A golden apple on the board's own centre. `at` is a whole number on both axes, so the pad is the
    # four blocks it corners rather than the one it is the centre of — which is the only placement that
    # reads the same from both ends of a rot_180 board.
    "spawners": [{
        "id": "orchard-apples",
        "at": {"x": 0, "y": 11, "z": 0},
        "pad": "gold block",
        "reach": 8,
        "protect": 7,
        "delay": "45s",
        "maxEntities": 4,
        "drops": [{"material": "golden apple", "amount": 1}],
    }],
    # The relief is the team ground's alone. The holm is taken out of the solve, so the two grounds meet
    # at a face rather than being graded into each other — which is what a holm's shore is.
    "shapePropsById": {"holm-11": {"relief_scope": "exclude"}},
    "relief": {"team": {
        "base": 9, "step": 1, "reach": 26,
        "grain": {"amplitude": 1, "scale": 13, "seed": 7},
        "marks": [
            # A brow over the spawn yard, a bluff behind the wool room, a hollow at the frontline and a
            # swell down the lane's east side. The ground the buildings stand on stays near level: a house
            # seats on the lowest column of its plan, and one on a slope is a house dug into a hill.
            {"id": "spawn-brow", "kind": "point", "at": [-13, -80], "r": 15, "h": 12},
            {"id": "wool-bluff", "kind": "point", "at": [50, -40], "r": 19, "h": 14},
            # A block off the bluff and no more: two marks pin their bands exactly, so a bigger
            # difference between them lands in the one cell where they touch, which is a wall at the
            # wool's approach rather than a shelf behind it.
            {"id": "wool-shelf", "kind": "point", "at": [47, -63], "r": 12, "h": 13},
            {"id": "lane-swell", "kind": "point", "at": [-8, -58], "r": 10, "h": 11},
            {"id": "front-hollow", "kind": "point", "at": [-2, -28], "r": 9, "h": 8},
        ],
    }},
    "dressing": {"props": houses + trees + boulders},
}

with open(os.path.join(HERE, "opus5-orchard-holm.plan.json"), "w") as out:
    json.dump(plan, out, indent=1)
with open(os.path.join(HERE, "opus5-orchard-holm.finish.json"), "w") as out:
    json.dump(finish, out, indent=1)
print("wrote the plan and the finish")
