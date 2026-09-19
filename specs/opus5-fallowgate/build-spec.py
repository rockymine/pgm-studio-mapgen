#!/usr/bin/env python3
"""Fallowgate — a small destroy board, three areas at three heights.

A hillside sheep pasture with one stone-walled fold at the top of it. The fold's flagged
yard is made ground and is held out of the relief; the pasture shelf at the board's lip is
grown ground pinned high; the wet hollow between them is grown ground pinned low, and the
monument stands in it. The band between the two pinned areas is what the relief solves,
and it is the hillside the match is fought down.

Writes opus5-fallowgate.plan.json and opus5-fallowgate.finish.json beside this file.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-fallowgate"
CELL = 4


def cells(blocks):
    assert blocks % CELL == 0, blocks
    return blocks // CELL


# ---------------------------------------------------------------- the massing
# Three areas, three heights, one team unit fanned by rot_180.
#
#   z -40 .. -28   fold      y 24   made ground, excluded from the relief, spawn on it
#   z -28 .. -16   flat      y 13   the wet hollow — the monument stands here
#   z -16 ..  -8   pasture   y 20   the upland shelf at the lip of the crossing
#   z  -8 ..   8   (void)           the crossing, bridged from the build zone
#
# The fold is 24x12 because ST10 caps a protection region at 20x30 in either orientation;
# the yard is the spawn piece, so its own extent is what that cap is measured on.
FOLD_X, FOLD_Z = (-12, 12), (-40, -28)
FLAT_X, FLAT_Z = (-24, 24), (-28, -16)
PAST_X, PAST_Z = (-24, 24), (-16, -8)
GAP_X, GAP_Z = (-24, 24), (-8, 8)

Y_FOLD, Y_PASTURE, Y_FLAT = 24, 20, 13

SPAWN_AT = (0, -32)           # world blocks, on the fold, set back from its lip
MONUMENT_AT = (-15, -22)      # world blocks, in the hollow, off the centre line


def rect(xs, zs):
    return [cells(xs[0]), cells(zs[0]), cells(xs[1] - xs[0]), cells(zs[1] - zs[0])]


def at_in(piece_x, piece_z, x, z):
    """A placement offset: blocks from the piece's own corner (plan 2)."""
    return [x - piece_x[0], z - piece_z[0]]


def plan():
    return {
        "plan": 2,
        "meta": {"name": "Fallowgate"},
        "globals": {
            "cell": CELL,
            "symmetry": "rot_180",
            "maxPlayers": 10,   # per TEAM: map.xml writes it as each team.max, so 20 shipped 20 a side
            "surface": Y_FLAT,
            "observerY": 46,
        },
        "pieces": [
            {"id": "fold", "role": "spawn", "rect": rect(FOLD_X, FOLD_Z), "surface": Y_FOLD},
            {"id": "flat", "role": "piece", "rect": rect(FLAT_X, FLAT_Z), "surface": Y_FLAT},
            {"id": "pasture", "role": "piece", "rect": rect(PAST_X, PAST_Z), "surface": Y_PASTURE},
        ],
        "zones": [
            {"id": "crossing", "rect": rect(GAP_X, GAP_Z), "kind": "build"},
        ],
        "walls": [],
        "placements": {
            "spawns": [
                {"id": "spawn-1", "piece": "fold",
                 "at": at_in(FOLD_X, FOLD_Z, *SPAWN_AT), "facing": "back",
                 # Pulled back off the lip: at [5,2,19,9] the stamped hall's wall stood at
                 # z -30 with the fold's last ground row at z -29 and a nine-block drop at
                 # z -28, so a player stepping out of its south side stepped off the yard.
                 # The stamp reaches about two blocks past the stated footprint.
                 "footprint": [4, 1, 20, 6]},
            ],
            "destroyables": [
                {"id": "destroyable-1", "piece": "flat",
                 "at": at_in(FLAT_X, FLAT_Z, *MONUMENT_AT),
                 "style": "pillar-2", "materials": "obsidian", "float": 2,
                 "name": "The Fallowgate Stone"},
            ],
            "wools": [],
            "cores": [],
        },
    }


# ------------------------------------------------------------------ the relief
# The compiled ground carries three shapes, one per piece:
#   flat-13  the hollow · flat-20  the pasture shelf · flat-24  the fold
# and one group, "team", which mirrors.
#
# The fold is made ground and states relief_scope "exclude", so the solve bends round it and
# its yard keeps the height it was drawn at; the two grown areas are each pinned by one area
# mark, and the band between the two rings is pinned by nothing, which is what grades the
# hillside. Two marks, no push.

# Each ring runs past the ground it pins — north over the excluded fold, south over the
# crossing's void, east and west past the board's edge — because bevel eats INWARD from the
# ring, and a ring drawn on the area's own outline loses its whole floor to the bevel.
# The south edge of one and the north edge of the other are drawn wavy, so the free band
# between them is 7 blocks wide at x -10 and 11 at x +10: one hillside at 45 degrees and 32.
FLAT_BENCH = [(-26, -30), (26, -30), (26, -21),
              (14, -19), (2, -22), (-10, -18), (-26, -22)]
PASTURE_BENCH = [(-26, -13), (-10, -15), (4, -12), (26, -14),
                 (26, -6), (-26, -6)]


def relief():
    return {"team": {
        "base": 16, "reach": 0, "step": 1,
        # An even ramp between two benches solves as a mathematical surface, and a slope-banded
        # paint over one draws its bands as unbroken contour ribbons. The grain is what makes the
        # angle vary cell to cell, so the bands interleave along their edges the way ground does.
        "grain": {"amplitude": 1, "scale": 9, "seed": 4},
        "marks": [
            {"id": "hollow-bench", "kind": "area", "h": Y_FLAT, "bevel": 2,
             "ring": [list(p) for p in FLAT_BENCH]},
            {"id": "pasture-bench", "kind": "area", "h": Y_PASTURE, "bevel": 2,
             "ring": [list(p) for p in PASTURE_BENCH]},
        ]}}


# ------------------------------------------------------------------- the paint
# Two themes. The ground is one theme banded on the SLOPE axis, so a 40-degree hillside and
# the meadow above it are not painted alike; the fold is the one made thing and has its own.
#
# The cuts come off GET /map/opus5-fallowgate/incline?format=text, read on the built relief
# before any of this was written:
#     00-09 38.5%   10-19 13.1%   20-29 22.3%   30-39 17.5%   40-49 1%   60-79 7.7%
# so 0-20 is the two benches and the gentle shoulder, 20-34 is the graded hillside, and
# 34-up is the steep ground and the cut banks.

GRASS, DIRT, COARSE = (2, 0), (3, 0), (3, 1)
STONE, ANDESITE, COBBLE, BRICK = (1, 0), (1, 5), (4, 0), (98, 0)


def solid(block):
    return {"kind": "solid", "id": block[0], "data": block[1]}


def down(*courses):
    """A depth stack: (thickness, block) from the top course down."""
    return {"kind": "layered", "axis": "depth", "beyond": solid(STONE),
            "stack": {"ending": "handOver",
                      "bands": [{"thickness": t, "material": m} for t, m in courses]}}


def themes():
    fell_surface = {
        "kind": "layered", "axis": "slope", "beyond": solid(STONE),
        "stack": {"ending": "handOver", "bands": [
            # 0-20 degrees: the benches and the shoulder — turf
            {"thickness": 20, "material": down((1, solid(GRASS)), (2, solid(DIRT)))},
            # 20-34: the graded hillside, grazed thin — worn soil
            {"thickness": 14, "material": down((1, solid(COARSE)), (2, solid(DIRT)))},
            # 34 and steeper: the ground the turf has come off — rock
            {"thickness": 56, "material": down(
                (1, {"kind": "noise", "seed": 3, "scale": 14, "octaves": 2,
                     "stops": [solid(STONE), solid(COBBLE)]}),
                (2, solid(STONE)))},
        ]}}
    return {
        "fell": {
            "bedrock": {"relative": False, "value": 1},
            "rimEdges": "void",
            # No rim: the relief solved this ground, and a rim would cap every fall with a
            # band and draw contour lines across the hillside.
            "rim": {"enabled": False, "depth": 1, "material": solid(STONE)},
            "wallOnTerrainFaces": True,
            "surface": {"enabled": True, "depth": 3, "material": fell_surface},
            "wall": down((1, solid(COARSE)), (2, solid(DIRT)), (3, solid(STONE))),
            "wallEnabled": True,
            # A voronoi is the body of the rock nobody sees until a bank is cut, and it is stone.
            "fill": {"kind": "voronoi", "seed": 11, "cellSize": 14, "rise": 7, "bands": [
                {"depth": 1, "material": solid(ANDESITE)},
                {"depth": 1, "material": solid(STONE)}]},
        },
        "yard": {
            "bedrock": {"relative": False, "value": 1},
            # The fold's edge is a made lip, which is where a rim belongs: one coping course.
            "rimEdges": "drop",
            "rim": {"enabled": True, "depth": 1, "material": solid(BRICK)},
            "wallOnTerrainFaces": True,
            "surface": {"enabled": True, "depth": 2, "material": down(
                (1, {"kind": "cell", "seed": 5, "cellSize": 3, "jitter": 1, "warp": 0,
                     "palette": [solid(COBBLE), solid(ANDESITE)]}),
                (1, solid(STONE)))},
            # The retaining face is banded by world height, not by depth: a cobble footing
            # standing in the wet of the hollow, stone brick above it.
            "wall": {"kind": "layered", "axis": "height", "from": Y_FLAT,
                     "beyond": solid(BRICK),
                     "stack": {"ending": "handOver", "bands": [
                         {"thickness": 3, "material": solid(COBBLE)},
                         {"thickness": 9, "material": solid(BRICK)}]}},
            "wallEnabled": True,
            "fill": solid(STONE),
        },
    }


# ----------------------------------------------------------------- what is built
# One flight, and it exists because the areas asked for it: the fold is excluded from the
# relief, so it meets the hollow at a face 11 blocks tall — the only face 03-slopes.txt finds
# on the whole board, 48 cells at x -12..11, z -29..-28 — and nothing walks up it. SP8 says
# the same thing about the spawn's egress.
#
# It runs along the foot of that wall rather than out from it: 22 blocks of run for 11 of
# rise, head at the yard's south-west corner, foot out in the east of the hollow. Set that way
# the defenders' own road to their monument crosses the hollow instead of dropping onto it.
# It carries the yard's theme, because a flight is masonry and belongs to the made ground
# rather than to either of the two grounds it joins.

# The head sits on the fold's own south-west corner column, so its west face is continuous
# with the fold's and the flight is not a free-standing buttress in the middle of the hollow:
# headed at x -9 the transect read BARRIER +10 at (-9, -27), a ten-block wall with nothing
# behind it. Four blocks wide, because it is the whole of a ten-player spawn's egress.
STEPS_HEAD_X, STEPS_FOOT_X = -12, 13
STEPS_Z = (-28, -24)


def steps():
    return {
        "id": "yard-steps", "type": "polygon", "operation": "add",
        "override": True, "keepClear": True, "floor": 0,
        "base_height": Y_FOLD,
        "height_mode": "level", "skirt": 0,
        "relief_scope": "exclude",
        "theme": "yard",
        "vertices": [[STEPS_HEAD_X, STEPS_Z[0]], [STEPS_FOOT_X, STEPS_Z[0]],
                     [STEPS_FOOT_X, STEPS_Z[1]], [STEPS_HEAD_X, STEPS_Z[1]]],
        "anchor_heights": [Y_FOLD, Y_FLAT, Y_FLAT, Y_FOLD],
    }


# --------------------------------------------------------------- what is dressed
# Per area, and each placement has an answer to "why here":
#
#   the yard    a worked floor — swept, and it takes nothing. The flight is keepClear.
#   the shelf   one erratic, on the bare upland the crossing is bridged onto — a landmark at
#               the bridgehead. It is NOT on the hillside: DR-STEEP declined every seat there,
#               "the slope is already the feature and a rock pinned to it reads as [pinned]",
#               which is the studio agreeing that the slope band is doing that work already.
#   the hollow  one stand of birch in its north-east, out of the wind under the yard's east
#               end, where the water off the hill collects and stock cannot get at seedlings.
#   everywhere  one flora pass, because the board is a grazed pasture and that is what one is.
#
# One species in the stand and one rock in the pair. No house: the yard is the built thing and
# it already carries the hall, the hollow is a wet bottom nobody builds in, and the pasture is
# grazing. Nowhere on this board answers "why here" for a second building.

ERRATIC = {"kind": "voronoi", "seed": 9, "cellSize": 2, "bands": [
    {"depth": 1, "material": {"kind": "solid", "id": 1, "data": 0}},
    {"depth": 1, "material": {"kind": "solid", "id": 1, "data": 5}}]}

# One rock, not a pair: two 30 blocks apart on one shelf is a scatter, and the seats near
# enough to read as a pair were declined OB19 — the goal's clearance is about 11 blocks.
# At (-12,-11), size 3.5, the rock reached z -8: column (-12,-8) read three blocks of mossy
# cobble standing over the crossing's void. `size` is a RADIUS — 3.5 came out 7 across — so
# the centre has to sit at least that far in from the lip.
BOULDERS = [("erratic", 20, -13, 3, 1)]
BIRCHES = [("shelter-1", 16, -25, 8), ("shelter-2", 19, -23, 7), ("shelter-3", 14, -21, 9)]


def dressing():
    props = []
    for i, (pid, x, z, size, seed) in enumerate(BOULDERS):
        props.append({"kind": "boulder", "id": pid, "x": x, "z": z,
                      "form": "angular", "size": size, "mossy": True,
                      "rock": ERRATIC, "seed": seed})
    for i, (pid, x, z, height) in enumerate(BIRCHES):
        props.append({"kind": "tree", "id": pid, "x": x, "z": z,
                      "form": "Template", "species": "birch",
                      "height": height, "seed": 20 + i})
    props.append({
        "kind": "flora", "id": "sward", "seed": 9,
        "points": [[-24, -40], [24, -40], [24, 40], [-24, 40]],
        # coverage and tallShare stay low: cover nobody authored, in front of an objective
        # nobody chose, is what a high one buys. The character is in scale.
        "spec": {"coverage": 0.18, "scale": 20, "octaves": 2, "fernShare": 0.25,
                 "flowerShare": 0.03, "flowerScale": 18, "tallShare": 0.03}})
    return {"props": props}


def finish():
    return {
        "authors": ["Opus 5"],
        "created": "2026-09-19",
        "shapePropsById": {"flat-24": {"relief_scope": "exclude"}},
        "relief": relief(),
        "themes": themes(),
        "mapTheme": "fell",
        "themeById": {"flat-24": "yard"},
        "addShapes": [steps()],
        # A timber-framed barn on a stone yard: a building is never the ground it stands on,
        # and the default room is a bedrock box. Shipped preset, unforked — gable roof,
        # no footing, log posts with plank infill.
        "roomStyles": {"spawn": "@hw-minehouse"},
        "dressing": dressing(),
        # Extreme hills: grass #8ab689, a cool grey-green that sits with stone and coarse
        # dirt where Plains' #91bd59 would read as a summer lawn under them.
        "biome": {"kind": "solid", "id": 3},
    }


if __name__ == "__main__":
    with open(os.path.join(HERE, SLUG + ".plan.json"), "w") as f:
        json.dump(plan(), f, indent=1)
        f.write("\n")
    with open(os.path.join(HERE, SLUG + ".finish.json"), "w") as f:
        json.dump(finish(), f, indent=1)
        f.write("\n")
    print("wrote", SLUG + ".plan.json", "and", SLUG + ".finish.json")
