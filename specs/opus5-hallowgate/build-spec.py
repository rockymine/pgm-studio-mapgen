#!/usr/bin/env python3
"""Hallowgate — a capture-the-wool board on a drowned churchyard.

Writes `opus5-hallowgate.plan.json` and `opus5-hallowgate.finish.json` beside this file.

The arrangement is taken over from the composer rather than invented: a hub ringing an
enclosed hole, a spawn hung off its flank, an L of causeway to a wool room in a corner, a
frontline bar with two stepping stones, and a mid band over black water. That arrangement
is the thing that is hard to invent and easy to get wrong, and `composed-seed-3.plan.json`
beside this file is the composer's own answer, committed so the starting point is
reproducible.

Everything the composer does not state is authored here: the elevation, the coast that is
not a ruled line, the defence wall, the churchyard's own wall, the lychgate over the
causeway, the relief and the whole finish. The hole in the hub is left alone — it is the
rotation device, and the long way round it is the one route that does not spend its whole
approach inside the defenders' reinforcement lane.

Scale: cell 4. The team unit is authored at +z and rot_180 fans the rest.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-hallowgate"

# ── blocks ────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE = 1, 2, 3, 4
GRAVEL, MOSSY_COBBLE = 13, 48
STONE_BRICK, LOG, LOG2 = 98, 17, 162
BIRCH_PLANKS, DARK_OAK_PLANKS = (5, 2), (5, 5)
BIRCH_LOG, DARK_OAK_LOG = (LOG, 2), (LOG2, 1)
BIRCH_STAIRS, BIRCH_SLAB = 135, (126, 2)
COARSE_DIRT, PODZOL = (DIRT, 1), (DIRT, 2)
ANDESITE, DIORITE = (STONE, 5), (STONE, 3)
MOSSY_BRICK, CRACKED_BRICK, CHISELLED_BRICK = (STONE_BRICK, 1), (STONE_BRICK, 2), (STONE_BRICK, 3)


def solid(block, data=0):
    if isinstance(block, tuple):
        block, data = block
    return {"kind": "solid", "id": block, "data": data}


def _stack(axis, flat):
    pairs = list(zip(flat[0::2], flat[1::2]))
    return {"kind": "layered", "axis": axis, "stack": {
        "ending": "repeat",
        "bands": [{"material": m, "thickness": t} for m, t in pairs]}}


def depth(*flat):
    """A stack down from the surface, so a surfacing block stays one course over its soil."""
    return _stack("depth", flat)


def slope(*flat):
    """A stack across the ground's angle: a thickness here is a span of degrees."""
    return _stack("slope", flat)


def cells(palette, size, seed, jitter=40, warp=2, rise=3):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": [solid(b) for b in palette], "rise": rise}


def voronoi(palette, size, seed, rise=4):
    return {"kind": "voronoi", "seed": seed, "cellSize": size, "rise": rise,
            "bands": [{"material": solid(b), "depth": d}
                      for b, d in zip(palette, (1, 2, 3))]}


def theme(surface, wall, fill, rim=None, surface_depth=3):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "rim": ({"enabled": False, "depth": 1, "material": solid(STONE)} if rim is None
                else {"enabled": True, "depth": rim[0], "material": rim[1]}),
        "surface": {"enabled": True, "depth": surface_depth, "material": surface},
        "wallEnabled": True,
        "wallOnTerrainFaces": True,
        "wall": wall,
        "fill": fill,
    }


# ── the plan: the composer's arrangement, adapted ─────────────────────────────
# Four things are changed and nothing else is: the spawn's two pieces become one piece big
# enough to hold a yard (the composer's default shell leaves a one-block ring, and an iron
# cube wants 3×3 with two blocks of clear air to the shell); the chapel terrace is lifted
# five courses so the board has a made ground meeting a grown one; a defence wall is stated
# on the causeway's outer interface; and a footprint is stated on the spawn.
GROUND, YARD = 9, 14


plan = {
    "plan": 2,
    "meta": {
        "name": "Hallowgate",
        "notes": ("CTW. One wool a team in a chapel on a raised churchyard, reached along a "
                  "walled causeway with a lychgate on it. The hub rings a grave-pit nothing "
                  "crosses, and the middle is a bar of stepping stones over black water."),
    },
    "globals": {
        "cell": 4,
        "symmetry": "rot_180",
        "maxPlayers": 12,
        "surface": GROUND,
        "observerY": 54,
    },
    "pieces": [
        # the hub, a ring of four bars round an enclosed hole. The hole is the composer's
        # and it stays: it is what gives an attacker a long way round that does not spend
        # the whole approach inside the defenders' reinforcement lane.
        {"id": "hub-t1", "role": "piece", "rect": [-4, 16, 11, 3]},
        {"id": "hub-t2", "role": "piece", "rect": [-4, 10, 11, 3]},
        {"id": "hub-t3", "role": "piece", "rect": [-4, 13, 3, 3]},
        {"id": "hub-t4", "role": "piece", "rect": [4, 13, 3, 3]},
        # blocks x[-32,-16] z[60,80] — one spawn piece where the composer had two, so the
        # hall has a yard round it and the iron cube has somewhere to stand
        {"id": "spawn-room", "role": "spawn", "rect": [-8, 15, 4, 5]},
        # the causeway, an L off the hub's back
        {"id": "wool-a-t1", "role": "piece", "rect": [0, 19, 3, 4]},
        # the churchyard terrace and the chapel in its corner, five courses up
        {"id": "wool-a-t2", "role": "piece", "rect": [0, 23, 4, 3], "surface": YARD},
        {"id": "wool-a-room", "role": "wool-room", "rect": [4, 23, 2, 3], "surface": YARD},
        # the frontline bar and its two stepping stones
        {"id": "frontline-t1", "role": "piece", "rect": [-4, 7, 10, 3]},
        {"id": "frontline-t2", "role": "piece", "rect": [-6, 5, 4, 2]},
        {"id": "frontline-t3", "role": "piece", "rect": [2, 5, 4, 2]},
        # the centre island, on the axis and therefore not fanned onto itself
        {"id": "mid-stone", "role": "piece", "rect": [-3, -2, 6, 4], "mirrors": False},
    ],
    "zones": [
        {"id": "mid-band", "rect": [-6, -5, 12, 10], "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn-room", "at": [8, 10], "facing": "right",
             "footprint": [3, 5, 10, 10]},
        ],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [4, 6]}],
        # in the yard behind the hall, two blocks clear of its shell
        "iron": [{"id": "iron-1", "piece": "spawn-room", "at": [8, 18]}],
        "destroyables": [],
        "cores": [],
    },
    # One wall, on one interface, and not on the room's own: the causeway's outer interface
    # is where the approach meets the hub, about fifteen blocks out from the chapel. The
    # wall spans the whole of that interface, so there is no shoulder to stroll round —
    # which is the thing that turns a prepared line back into an obstacle.
    "walls": [{"a": "wool-a-t1", "b": "hub-t1"}],
    "boxes": [],
}

# ── the themes ────────────────────────────────────────────────────────────────
# Three. The mire is the ground, the churchyard is what was built on it, and the sill is
# the stone of the wall, the gate and the chapel's own terrace face.
#
# The ground family is dark and wet — podzol and coarse dirt under a Swampland biome, whose
# grass tint (#6a7039) comes to meet podzol's brown so the pair reads as one leaf-littered
# floor rather than as two grounds arguing. The built family is pale birch, which is not the
# family under its feet, and the accent is dark oak.
MIRE_FLAT = depth(cells([GRASS, PODZOL], 12, 13), 1, solid(DIRT), 2)
MIRE_SHOULDER = depth(cells([COARSE_DIRT, PODZOL], 8, 29), 1, solid(DIRT), 2)
MIRE_FACE = depth(cells([STONE, MOSSY_COBBLE], 7, 31), 2, solid(STONE), 3)

themes = {
    "mire": theme(
        surface=slope(MIRE_FLAT, 30, MIRE_SHOULDER, 20, MIRE_FACE, 40),
        wall=depth(solid(COARSE_DIRT), 1, solid(DIRT), 2, solid(STONE), 4),
        fill=voronoi([STONE, ANDESITE, DIORITE], 13, 3),
    ),
    # the churchyard terrace: turf kept over a made floor, with a mossy retaining face
    "churchyard": theme(
        surface=depth(cells([GRASS, COARSE_DIRT], 6, 41), 1, solid(DIRT), 1,
                      solid(STONE_BRICK), 2),
        wall={"kind": "wallRun", "runs": [
            {"material": solid(CHISELLED_BRICK), "thickness": 1},
            {"material": solid(STONE_BRICK), "thickness": 3},
            {"material": solid(MOSSY_BRICK), "thickness": 2},
            {"material": solid(STONE_BRICK), "thickness": 3},
        ]},
        fill=voronoi([STONE, ANDESITE], 12, 19),
        rim=(1, solid(MOSSY_BRICK)),
    ),
    # the sill: the churchyard wall, the lychgate's footing and the causeway's kerb
    "sill": theme(
        surface=depth(cells([STONE_BRICK, MOSSY_BRICK], 5, 47), 1, solid(STONE_BRICK), 2),
        wall=depth(solid(MOSSY_BRICK), 1, solid(STONE_BRICK), 3, solid(STONE), 3),
        fill=voronoi([STONE, ANDESITE], 11, 23),
    ),
}

# ── the shapes ────────────────────────────────────────────────────────────────
# The churchyard is made ground and comes out of the solve, so it meets the causeway at a
# face rather than being graded into it. One flight answers the five courses — sixteen
# blocks of run, `height_mode` and `skirt` for the relief, `keepClear` for the dressing,
# and a material rather than a theme.
FLIGHT = depth(solid(STONE_BRICK), 1, solid(MOSSY_BRICK), 1, solid(STONE), 3)

add_shapes = [
    {"id": "chapel-steps", "type": "polygon", "operation": "add", "override": True,
     "keepClear": True, "floor": 0, "base_height": YARD,
     "height_mode": "level", "skirt": 0, "material": FLIGHT,
     "vertices": [[3, 96], [11, 96], [11, 86], [3, 86]],
     "anchor_heights": [YARD, YARD, GROUND, GROUND]},

    # The churchyard wall, drawn as a polyline: the rasterizer splines its points before
    # offsetting the band, so five clicked points read as a wall that follows the terrace's
    # edge rather than as a chain of chords. It stands three courses on its own columns.
    {"id": "yard-wall", "type": "polyline", "operation": "add", "keepClear": True,
     "floor": 0, "base_height": YARD + 3, "theme": "sill",
     "stroke_edge": "solid", "radius": 1,
     "vertices": [[1, 92], [1, 99], [3, 102]]},

    # the causeway's kerb, the same instrument at the other end of the approach
    {"id": "causeway-kerb", "type": "polyline", "operation": "add", "keepClear": True,
     "floor": 0, "base_height": GROUND + 2, "theme": "sill",
     "stroke_edge": "rough", "stroke_seed": 4, "radius": 1,
     "vertices": [[1, 78], [2, 82], [4, 86], [3, 90]]},

    # a patch of bare, trodden ground where the causeway meets the hub — the ground in
    # front of the defence wall, which is fought over and wants reading at a glance
    {"id": "gate-apron", "type": "polygon", "operation": "add", "keepClear": False,
     "floor": 0, "base_height": GROUND, "theme": "sill",
     "vertices": [[0, 70], [12, 70], [12, 76], [0, 76]]},
]

# ── the lychgate ──────────────────────────────────────────────────────────────
# A made layer, and the one thing on this board that is a second storey: a roofed gate the
# causeway runs under, between the defence wall and the chapel steps. Its `base_y` is the
# ground's own top block plus one, and the roof's is the walls' top — one lower on either
# and the slab is absorbed by the layer beneath it (SK10). `kind: "made"` and `part_of`
# keep the pair walk and the reachability walk off it, because a gate standing on the
# causeway has no gap to lose and its roof is not a stair somebody forgot.
GATE_WALL_Y = GROUND
GATE_ROOF_Y = GATE_WALL_Y + 5

add_layers = [
    {"id": "gate-posts", "name": "gate-posts", "base_y": GATE_WALL_Y,
     "kind": "made", "part_of": "lychgate",
     "shapes": [
         {"id": "gate-post-w", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 5, "theme": "sill",
          "min_x": 1, "min_z": 79, "max_x": 3, "max_z": 82},
         {"id": "gate-post-e", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 5, "theme": "sill",
          "min_x": 9, "min_z": 79, "max_x": 11, "max_z": 82},
     ],
     "groups": [{"id": "lychgate-posts", "name": "lychgate posts", "mirrors": True,
                 "shapeIds": ["gate-post-w", "gate-post-e"]}]},
    # The chapel the board is named for: walls on the terrace's own top block plus one,
    # a roof on the walls' top. One course lower on either and the slab is absorbed by the
    # layer beneath it (SK10). Seven blocks wide on a sixteen-block terrace, so there is a
    # way past it on both sides, and five blocks of yard south of it for the route to the room.
    {"id": "chapel-walls", "name": "chapel-walls", "base_y": YARD,
     "kind": "made", "part_of": "chapel",
     "shapes": [
         {"id": "chapel-w", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 5, "theme": "sill",
          "min_x": 3, "min_z": 97, "max_x": 4, "max_z": 103},
         {"id": "chapel-e", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 5, "theme": "sill",
          "min_x": 9, "min_z": 97, "max_x": 10, "max_z": 103},
         {"id": "chapel-n", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 5, "theme": "sill",
          "min_x": 3, "min_z": 102, "max_x": 10, "max_z": 103},
     ],
     "groups": [{"id": "chapel-shell", "name": "chapel shell", "mirrors": True,
                 "shapeIds": ["chapel-w", "chapel-e", "chapel-n"]}]},
    {"id": "chapel-roof", "name": "chapel-roof", "base_y": YARD + 5,
     "kind": "made", "part_of": "chapel",
     "shapes": [
         {"id": "chapel-lid", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 2, "theme": "sill",
          "min_x": 2, "min_z": 96, "max_x": 11, "max_z": 104},
     ],
     "groups": [{"id": "chapel-cap", "name": "chapel roof", "mirrors": True,
                 "shapeIds": ["chapel-lid"]}]},
    {"id": "gate-roof", "name": "gate-roof", "base_y": GATE_ROOF_Y,
     "kind": "made", "part_of": "lychgate",
     "shapes": [
         {"id": "gate-lid", "type": "rectangle", "operation": "add", "floor": 0,
          "base_height": 2, "theme": "sill",
          "min_x": 0, "min_z": 78, "max_x": 12, "max_z": 83},
     ],
     "groups": [{"id": "lychgate-roof", "name": "lychgate roof", "mirrors": True,
                 "shapeIds": ["gate-lid"]}]},
]

# ── the relief ────────────────────────────────────────────────────────────────
# Two groups, because a compiled board has one per role and the centre island is neutral —
# so the board is genuinely two grounds meeting rather than one field with a gradient in it.
#
# On the team's ground: the hub's yard held flat because it is where the match is fought,
# the frontline shore held low because that is where an attacker lands, and a burial mound
# pushed up on the hub's east arm, which is the one landform. Nothing else is pinned.
relief = {
    "team": {
        "base": GROUND,
        "reach": 0,
        "step": 1,
        "landform": "rolling",
        "grain": {"amplitude": 0.6, "scale": 12, "seed": 7},
        "marks": [
            # the hub's own floor, flat to its edge and therefore carrying no tread
            {"id": "hub-floor", "kind": "area", "h": GROUND, "bevel": 0,
             "ring": [[-16, 42], [28, 42], [28, 74], [-16, 74]]},
            # the frontline shore, two courses lower, where the crossing lands
            {"id": "shore", "kind": "area", "h": GROUND - 2, "bevel": 0,
             "ring": [[-16, 28], [24, 28], [24, 38], [-16, 38]]},
        ],
        "pushes": [
            # the burial mound on the hub's east arm: the board's one landform, and the
            # height a raider takes to see over the churchyard wall. Skirt 6/8 = 0.75 a
            # block against a crown of 4/5 = 0.80 — inside RL6's factor of two.
            {"id": "barrow", "amount": 6, "falloff": 8, "crown": 4,
             "roughness": 0, "seed": 2,
             "ring": [[18, 55], [26, 54], [28, 59], [26, 62], [19, 61]]},
        ],
    },
    # The centre island is its own ground: a bar of wet stone standing a course out of the
    # water, pinned flat because it is a stepping stone and not a landform.
    "neutral": {
        "base": GROUND - 2,
        "reach": 0,
        "step": 1,
        "landform": "plain",
        "grain": {"amplitude": 0.3, "scale": 9, "seed": 11},
        "marks": [
            {"id": "stone-top", "kind": "area", "h": GROUND - 2, "bevel": 1,
             "ring": [[-12, -8], [12, -8], [12, 8], [-12, 8]]},
        ],
        "pushes": [],
    },
}

# ── the buildings ─────────────────────────────────────────────────────────────
# One idea: the chapel standing in its own yard, beside the room the wool is in. Pale birch
# over stone brick on a dark, wet ground — a building has to read as a built thing from
# across the map, which means its walls are not in the tone family under its feet.
CHAPEL_SHELL = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": solid(STONE_BRICK), "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                    "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {
        "form": "gable", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": solid(DARK_OAK_PLANKS),
        "verge": {"kind": "laidLog", "id": LOG2, "data": 1},
        "gable": solid(BIRCH_PLANKS),
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": {"stack": {"bands": [
        {"material": {"kind": "laidLog", "id": LOG2, "data": 1}, "thickness": 1},
        {"material": solid(BIRCH_PLANKS), "thickness": 3},
        {"material": solid(STONE_BRICK), "thickness": 4},
    ], "ending": "repeat"}, "extent": 8},
    "post": solid(DARK_OAK_LOG),          # one wood for post, beam and the laid course
    "windows": {"form": "arched", "block": BIRCH_STAIRS, "hostBlock": -1, "hostData": 0,
                "data": 0, "sill": 3, "width": 2, "height": 3, "spacing": 4},
    "storeys": [],
    "porch": None,
    "front": None,
    "beams": {"block": LOG2, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": BIRCH_STAIRS, "fill": "upperSlab",
                         "fillBlock": BIRCH_SLAB[0], "fillData": BIRCH_SLAB[1]},
                "width": 2, "height": 4},
}

# ── the dressing ──────────────────────────────────────────────────────────────
# The ground here is soft, so the path is dirt, coarse dirt and spruce planks — three
# colours a reader cannot quite tell apart.
TRACK = cells([DIRT, COARSE_DIRT, (5, 1)], 3, 53, rise=0)

TREES = json.load(open(os.path.join(HERE, "trees.json")))
# Four modest recipes rather than the biggest in the corpus: a copied tree's foot is every
# cell of its lowest course and its crown is wider again, and this board's seats mask leaves
# very little ground with room round it.
TREE_KEYS = {"willow-a": "showcase-r17-1", "birch-a": "showcase-r13-4",
             "yew-a": "showcase-r6-1", "olive-a": "showcase-r10-1"}


def tree(pid, style, x, z):
    return {"id": pid, "kind": "tree", "style": style, "x": x, "z": z, "layer": "ground"}


def rock(pid, x, z, size, seed, form="angular"):
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "layer": "ground",
            "form": form, "size": size, "mossy": True, "seed": seed,
            "rock": cells([STONE, COBBLE, ANDESITE], 5, seed + 80, rise=4)}


dressing = {
    "styles": {
        **{key: TREES[name] for key, name in TREE_KEYS.items()},
    },
    "props": [
        # The flooded corner of the graveyard, on the hub's east flank where no route runs.
        # It states no `level`: the hub's floor is ground that is already there, so the line
        # is found rather than stated, and its run is level so nothing is trenched.
        {"id": "tarn", "kind": "water", "seed": 63, "layer": "ground",
         "shape": "pool", "form": "natural",
         "points": [[-14, 54], [-6, 54], [-5, 60], [-9, 63], [-14, 60]],
         "radius": 3, "depth": 3, "shore": 2, "shoreWander": True, "edge": 1,
         "bank": cells([GRAVEL, COARSE_DIRT, PODZOL], 6, 73, rise=3)},

        # the way out of the spawn, round the hub's west arm and up the causeway — the
        # circulation drawn before the scenery, so the routes are clean by construction
        {"id": "trod-spawn", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[-17, 70], [-10, 70], [-2, 70], [4, 73], [7, 78]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},
        # and the hub's own lap, round the far side of the grave-pit: the long way round is
        # a route somebody walks, so it is drawn
        {"id": "trod-lap", "kind": "stroke", "seed": 6, "layer": "ground",
         "points": [[-2, 68], [6, 65], [13, 60], [15, 52], [10, 45], [1, 43]],
         "radius": 2, "style": "solid", "claimsGround": False, "pave": TRACK},

        # A wood on the hub's west flank, where no route runs, and a pair on the churchyard.
        # Nothing on the approach in front of the wall, nothing on the stepping stones, and
        # nothing on the ground an attacker lands on.
        tree("yew-1", "willow-a", 20, 40),
        tree("yew-2", "yew-a", 26, 50),
        tree("yew-3", "birch-a", 25, 73),
        tree("yew-4", "olive-a", -13, 41),

        # boulders are stone, and here they are the fallen stones of the yard
        rock("stone-1", -4, 46, 2, 21, form="cairn"),
        rock("stone-2", 10, 68, 2, 22),
        rock("stone-3", 5, 66, 2, 23, form="round"),

        # Ground cover over the team's own land, held off the frontline shore and the
        # stepping stones: the ground an attacker lands on wants reading at a glance.
        # A wet churchyard is mostly fern.
        {"id": "sward", "kind": "flora", "seed": 9,
         "points": [[-32, 42], [28, 42], [28, 104], [-32, 104]],
         "spec": {"coverage": 0.26, "scale": 20, "octaves": 3,
                  "fernShare": 0.45, "flowerShare": 0.06, "flowerScale": 24,
                  "tallShare": 0.05}},
    ],
}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    # Swampland, #6a7039. The grass tint comes to meet podzol's brown, so the pair reads as
    # one dry, leaf-littered floor instead of as two grounds arguing.
    "biome": {"kind": "solid", "id": 6},
    "mapTheme": "mire",
    "themes": themes,
    # Keyed on the compiled shape ids, read off POST /plan/compile: the compiler fuses every
    # piece that shares a height, so the hub, the spawn, the causeway and the frontline are
    # one shape at 9 and the churchyard terrace with its room is one shape at 14. The
    # enclosed hole comes back as `void-1-cut`, which is the compiler declaring the
    # arrangement's own negative space.
    "themeById": {"frontline-t1-14": "churchyard"},
    # The terrace is made ground and comes out of the solve, so it keeps the height it was
    # drawn at and meets the causeway at a face for the chapel steps to state.
    "shapePropsById": {"frontline-t1-14": {"relief_scope": "exclude"}},
    # The compiler emits a staircase of the plan's rectangles, which is the board's shape
    # and not its coast. This resamples the compiled rings along their long edges and pulls
    # the inserted points inward — `side: "in"`, because nothing may move outward: a point
    # that did could close the strait the board is measured on.
    "bendShapes": {"frontline-t1-9": {"k": 0.18, "wander": 2, "step": 8,
                                     "seed": 5, "side": "in"}},
    "addShapes": add_shapes,
    "addLayers": add_layers,
    "relief": relief,
    "dressing": dressing,
}


def write(name, document):
    path = os.path.join(HERE, name)
    with open(path, "w") as handle:
        json.dump(document, handle, indent=1)
        handle.write("\n")
    print(f"wrote {path}")


write(f"{SLUG}.plan.json", plan)
write(f"{SLUG}.finish.json", finish)
