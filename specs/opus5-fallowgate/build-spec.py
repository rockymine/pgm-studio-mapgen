#!/usr/bin/env python3
"""Fallowgate — a small destroy board, three areas at three heights.

A hillside sheep pasture with one stone-walled fold at the top of it. The fold's flagged
yard is made ground and is held out of the relief; the pasture shelf at the board's lip is
grown ground, the wet hollow between them is grown ground, and the monument stands in the
hollow. The band between the two benches is what the relief solves, and it is the hillside
the match is fought down.

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
# Three areas, three heights, one team unit fanned by rot_180. Eighty by eighty a side is
# the cap, so the board is 56 x 160 and each team's own half is 56 x 68 with the crossing
# between them.
#
#   z -80 .. -64   fold      y 24   made ground, excluded from the relief, spawn on it
#   z -64 .. -36   flat      y 13   the wet hollow — the monument stands here
#   z -36 .. -12   pasture   y 20   the upland the crossing is bridged onto
#   z -12 ..  12   (void)           the crossing, bridged from the build zone
#
# The fold is 24x16 because ST10 caps a protection region at 20x30 in either orientation;
# the yard is the spawn piece, so its own extent is what that cap is measured on.
FOLD_X, FOLD_Z = (-12, 12), (-80, -64)
FLAT_X, FLAT_Z = (-28, 28), (-64, -36)
PAST_X, PAST_Z = (-28, 28), (-36, -12)
GAP_X, GAP_Z = (-28, 28), (-12, 12)

Y_FOLD, Y_PASTURE, Y_FLAT = 24, 20, 13

SPAWN_AT = (0, -78)           # world blocks, on the fold, set back from its lip
MONUMENT_AT = (-17, -46)      # world blocks, in the hollow, off the centre line


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
            "maxPlayers": 10,   # per TEAM: map.xml writes it as each team.max
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
                 # Pulled back off the lip: the stamp reaches about two blocks past the
                 # stated footprint, and at the first one the hall's wall stood one block
                 # from an eleven-block fall.
                 "footprint": [4, 1, 20, 8]},
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
#   flat-13  the hollow · flat-20  the pasture · flat-24  the fold
# and one group, "team", which mirrors.
#
# The fold is made ground and states relief_scope "exclude", so the solve bends round it and
# its yard keeps the height it was drawn at. The two grown areas are each pinned by one area
# mark — and two benches sharing one axis can only produce one gradient between them, which
# is a ramp with identical rows. So two LINE marks run ACROSS that axis, down the fall line:
# a spur held above the grade and a gill cut below it, each with a tread so its band lofts
# rather than walling. The push crowns the shelf, which would otherwise be a terrace.
#
# Each area ring runs past the ground it pins — north over the excluded fold, south over the
# crossing's void, east and west past the board's edge — because bevel eats INWARD from the
# ring, and a ring drawn on the area's own outline loses its whole floor to the bevel.
# The hollow's bench stops short of the board's edges, so its east and west margins are free
# and roll up toward base: a hollow has banks. Pinned edge to edge it printed twenty identical
# rows of zeroes.
FLAT_BENCH = [(-22, -68), (22, -68), (22, -44),
              (16, -40), (2, -45), (-14, -42), (-22, -45)]
PASTURE_BENCH = [(-32, -28), (-12, -30), (4, -25), (32, -29),
                 (32, -8), (-32, -8)]

# The fall line runs north–south; both benches run east–west. These two run the other way.
SPUR = {"points": [[18, -24], [15, -32], [12, -39], [9, -46]], "h": [21, 20, 18, 14]}
# The gill runs on past the bench's edge and one block under it, so it drains across the
# hollow floor instead of stopping at its lip.
# Its tail bends west across the hollow rather than running straight: straight, the four rows
# z -60..-57 printed the same byte sequence, which is the fault this whole pass is about.
GILL = {"points": [[-16, -24], [-14, -32], [-12, -39], [-10, -48], [-11, -55], [-15, -62]],
        "h": [19, 16, 14, 13, 12, 13]}

KNOLL = [(-22, -26), (-8, -29), (0, -21), (-8, -15), (-20, -17)]


def relief():
    return {"team": {
        "base": 16, "reach": 0, "step": 1,
        # An even ramp between two benches solves as a mathematical surface, and a
        # slope-banded paint over one draws its bands as unbroken contour ribbons. The grain
        # is what makes the angle vary cell to cell, so the bands interleave as ground does.
        "grain": {"amplitude": 1, "scale": 9, "seed": 4},
        "marks": [
            {"id": "hollow-bench", "kind": "area", "h": Y_FLAT, "bevel": 2,
             "ring": [list(p) for p in FLAT_BENCH]},
            {"id": "pasture-bench", "kind": "area", "h": Y_PASTURE, "bevel": 2,
             "ring": [list(p) for p in PASTURE_BENCH]},
            {"id": "spur", "kind": "line", "r": 8, "tread": 2,
             "points": SPUR["points"], "h": SPUR["h"]},
            {"id": "gill", "kind": "line", "r": 7, "tread": 2,
             "points": GILL["points"], "h": GILL["h"]},
        ],
        "pushes": [
            {"id": "knoll", "ring": [list(p) for p in KNOLL],
             "amount": 2, "falloff": 8, "crown": 1, "roughness": 1, "seed": 3},
        ]}}


# ----------------------------------------------------------------- what is built
# One flight, and it exists because the areas asked for it: the fold is excluded from the
# relief, so it meets the hollow at a face 11 blocks tall — the only face the slopes read
# finds in the grown ground — and nothing walks up it. SP8 says the same of the egress.
#
# It runs along the foot of that wall rather than out from it: 25 blocks of run for 11 of
# rise, head on the fold's own south-west corner column so its west face is continuous with
# the yard's, foot out in the east of the hollow. Set that way the defenders' own road to
# their monument crosses the hollow instead of dropping onto it. It carries the yard's theme,
# because a flight is masonry and belongs to the made ground rather than to either of the two
# grounds it joins.
STEPS_HEAD_X, STEPS_FOOT_X = -12, 13
STEPS_Z = (-64, -60)


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


# ------------------------------------------------------------------- the paint
# Two themes. The ground is one theme banded on the SLOPE axis, so a 40-degree hillside and
# the meadow above it are not painted alike; the fold is the one made thing and has its own.
# The cuts come off GET /map/opus5-fallowgate/incline?format=text, read on the built relief.

GRASS, DIRT, COARSE = (2, 0), (3, 0), (3, 1)
STONE, ANDESITE, COBBLE, BRICK = (1, 0), (1, 5), (4, 0), (98, 0)

# Re-read on the revised relief, which is far gentler than the first pass because the same
# seven blocks of rise are now spread over sixteen rather than eleven:
#   00-09 42.8%  10-19 32.5%  20-29 13.5%  30-39 6%  40-49 1.3%  50-59 1.1%  60-69 2.6%
# At the old cuts of 20 and 34 that is 75% turf — one green sheet, which is the fault the
# slope axis exists to prevent. 14 and 30 divide it about 56 / 33 / 11, which puts bare rock
# only on ground that is genuinely steep: at 24 the board came out a stone mesa from any
# camera, because a quarter of a grazed fell is not scree.
SLOPE_TURF, SLOPE_WORN = 14, 30


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
            # the benches and the shoulder — turf
            {"thickness": SLOPE_TURF,
             "material": down((1, solid(GRASS)), (2, solid(DIRT)))},
            # the graded hillside, grazed thin — worn soil
            {"thickness": SLOPE_WORN - SLOPE_TURF,
             "material": down((1, solid(COARSE)), (2, solid(DIRT)))},
            # the ground the turf has come off — rock
            {"thickness": 90 - SLOPE_WORN, "material": down(
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
            # A voronoi is the body of the rock nobody sees until a bank is cut, and it is
            # stone. The rise is the vertical period PT4 refuses a fill without.
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


# --------------------------------------------------------------- what is dressed
# Per area, and each placement has an answer to "why here":
#
#   the yard    a worked floor — swept, and it takes nothing. The flight is keepClear.
#   the shelf   one erratic on the bare upland the crossing is bridged onto — a landmark at
#               the bridgehead. NOT on the hillside: DR-STEEP declines every seat there,
#               "the slope is already the feature", against the same 34 degrees the paint cuts at.
#   the hollow  one stand of birch, out of the wind under the yard's east end, where the water
#               off the hill collects and stock cannot get at seedlings.
#   everywhere  one flora pass, because the board is a grazed pasture and that is what one is.
#
# One species in the stand. No house: the yard is the built thing and it already carries the
# hall, the hollow is a wet bottom nobody builds in, and the pasture is grazing.

ERRATIC = {"kind": "voronoi", "seed": 9, "cellSize": 2, "bands": [
    {"depth": 1, "material": {"kind": "solid", "id": 1, "data": 0}},
    {"depth": 1, "material": {"kind": "solid", "id": 1, "data": 5}}]}

# `size` is a RADIUS — 3.5 came out 7 across — so the centre sits that far in from any lip.
BOULDERS = [("erratic", 21, -30, 3, 1)]
BIRCHES = [("shelter-1", 19, -60, 8), ("shelter-2", 22, -57, 7), ("shelter-3", 17, -55, 9)]


def dressing():
    props = []
    for pid, x, z, size, seed in BOULDERS:
        props.append({"kind": "boulder", "id": pid, "x": x, "z": z,
                      "form": "angular", "size": size, "mossy": True,
                      "rock": ERRATIC, "seed": seed})
    for i, (pid, x, z, height) in enumerate(BIRCHES):
        props.append({"kind": "tree", "id": pid, "x": x, "z": z,
                      "form": "Template", "species": "birch",
                      "height": height, "seed": 20 + i})
    props.append({
        "kind": "flora", "id": "sward", "seed": 9,
        "points": [[-32, -80], [32, -80], [32, 80], [-32, 80]],
        # coverage and tallShare stay low: cover nobody authored, in front of an objective
        # nobody chose, is what a high one buys. The character is in scale.
        "spec": {"coverage": 0.18, "scale": 20, "octaves": 2, "fernShare": 0.25,
                 "flowerShare": 0.03, "flowerScale": 18, "tallShare": 0.03}})
    return {"props": props}


# -------------------------------------------------------------------- the coast
# The compiler emits a staircase of the plan's rectangles, which is the board's shape and not
# its coast, so every island arrives as four straight edges and the board reads as a set of
# boxes. Two instruments answer that, and they answer different questions.
#
# editShapes states the places that are MEANT: the lip the crossing is bridged onto gets two
# headlands and a bay between them, so a bridgehead is a decision rather than a choice of any
# x. Each op names one index and the indices shift as they are replayed, so they are stated in
# the order they run.
#
# The fold's own wall is NOT edited. A re-entrant cut into it opened void rather than a step —
# transect (2, -74..-58) read `void` at z -69..-67 between the yard at 24 and the hollow at 13,
# because nothing else on the board covers the ground a made shape gives up. A salient is no
# better: the whole of that wall is fronted by the flight, and an excluded shape at yard height
# over it would bury the steps. So the wall is straight and the flight is its gate.
#
# bendShapes states the places that are merely THERE: the long outer runs of the two grown
# areas, resampled and wandered so land ends the way land ends. side "out" only bloats, so
# nothing can be left hanging over void, and the plan's own vertices never move. The fold is
# not bent — it is a built wall, and a wandering retaining wall reads as a natural edge.

def edit_shapes():
    return {
        # the crossing lip: headland, bay, headland
        "flat-20": [
            {"after": 2, "x": 15, "z": -8},
            {"after": 3, "x": 2, "z": -17},
            {"after": 4, "x": -13, "z": -9},
        ],
    }


def bend_shapes():
    return {
        "flat-13": {"wander": 3, "step": 8, "seed": 5, "side": "out"},
        "flat-20": {"wander": 2.5, "step": 9, "seed": 7, "side": "out"},
    }


def finish():
    return {
        "authors": ["Opus 5"],
        "created": "2026-09-19",
        "shapePropsById": {"flat-24": {"relief_scope": "exclude"}},
        "relief": relief(),
        "themes": themes(),
        "mapTheme": "fell",
        "themeById": {"flat-24": "yard"},
        # Extreme hills: grass #8ab689, a cool grey-green that sits with stone and coarse
        # dirt where Plains' #91bd59 would read as a summer lawn under them.
        "biome": {"kind": "solid", "id": 3},
        "editShapes": edit_shapes(),
        "bendShapes": bend_shapes(),
        "addShapes": [steps()],
        # A timber-framed barn on a stone yard: a building is never the ground it stands on,
        # and the default room is a bedrock box. Shipped preset, unforked — gable roof,
        # no footing, log posts with plank infill.
        "roomStyles": {"spawn": "@hw-minehouse"},
        "dressing": dressing(),
    }


if __name__ == "__main__":
    with open(os.path.join(HERE, SLUG + ".plan.json"), "w") as f:
        json.dump(plan(), f, indent=1)
        f.write("\n")
    with open(os.path.join(HERE, SLUG + ".finish.json"), "w") as f:
        json.dump(finish(), f, indent=1)
        f.write("\n")
    print("wrote", SLUG + ".plan.json", "and", SLUG + ".finish.json")
