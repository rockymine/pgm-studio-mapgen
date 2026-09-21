#!/usr/bin/env python3
"""Sluicehead — a destroy-the-core board in a frozen glacial trough.

Writes `opus5-sluicehead.plan.json` and `opus5-sluicehead.finish.json` beside this file.

Where Kilnbrow is a terrace over a pan, this board is a trough: a flat sluice floor of
frozen gravel with a moraine ridge over each shoulder, and each team's core standing out on
that floor rather than behind anything. A core is breached where it stands, so it belongs
where it will be fought over — and its casing wants ground all round it, because a breach
near an edge spills the lava into the void and ends the objective at once.

The four approaches to it: down either moraine, from above; along the cut leat, from below
and unseen; through the sluice house beside it; and over the open floor in front.

Scale: cell 5. The team unit is authored at -z and rot_180 fans the rest.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-sluicehead"

# ── blocks ────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE = 1, 2, 3, 4
GRAVEL, SNOW, ICE = 13, 80, 79
STONE_BRICK, STAINED_CLAY, PACKED_ICE = 98, 159, 174
LOG, SPRUCE_STAIRS = 17, 134
SPRUCE_PLANKS, SPRUCE_LOG = (5, 1), (LOG, 1)
SPRUCE_SLAB = (126, 1)
ANDESITE, DIORITE = (STONE, 5), (STONE, 3)
MOSSY_BRICK, PODZOL = (STONE_BRICK, 1), (DIRT, 2)


def solid(block, data=0):
    """One block, the leaf every pattern bottoms out in."""
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
    """The body of the rock nobody sees until a wall is cut, and it is stone."""
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


# ── the plan ──────────────────────────────────────────────────────────────────
# Three pieces. The floor is the trough the match is played in; the head is the low terrace
# the spawn opens onto; the spawn hall sits behind it. Both moraines are relief, and so is
# the cistern's own pad — a piece per landform is a plan deciding what the board looks like.
CELL = 5
FLOOR_SURFACE, HEAD_SURFACE = 10, 14

plan = {
    "plan": 2,
    "meta": {
        "name": "Sluicehead",
        "notes": ("DTC. One core a team, out on an open frozen floor with ground all round "
                  "its casing: a moraine over each shoulder to bridge from, a cut leat past "
                  "it to move along unseen, and the sluice house to fight through."),
    },
    "globals": {
        "cell": CELL,
        "symmetry": "rot_180",
        "maxPlayers": 12,
        "surface": FLOOR_SURFACE,
        "observerY": 58,
    },
    "pieces": [
        # blocks x[-35,35] z[-85,-20] — the sluice floor, the trough the contest happens in
        {"id": "floor", "role": "piece", "rect": [-7, -17, 14, 13], "surface": FLOOR_SURFACE},
        # blocks x[-35,35] z[-100,-85] — the head, four courses up. It carries no building:
        # fifteen blocks cannot hold one and still leave eight of passable ground on a side,
        # so both of this board's houses stand out on the floor instead.
        {"id": "head", "role": "piece", "rect": [-7, -20, 14, 3], "surface": HEAD_SURFACE},
        # blocks x[-10,10] z[-120,-100] — the spawn hall at the back of the head
        {"id": "spawn", "role": "spawn", "rect": [-2, -24, 4, 4], "surface": HEAD_SURFACE},
    ],
    "zones": [
        # blocks x[-35,35] z[-20,20] — the whole width, over void
        {"id": "sound", "rect": [-7, -4, 14, 8], "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn", "at": [10, 5], "facing": "back",
             "footprint": [3, 3, 14, 9]},
        ],
        "wools": [],
        "iron": [{"id": "iron-1", "piece": "spawn", "at": [10, 16]}],
        "destroyables": [],
        # block (20, -64): out on the open floor, fifteen blocks clear of the board's east
        # edge and of the head's face, so a breach anywhere on the casing still has terrain
        # under it for the lava to fall to. `float` and `leak` are one knob and are stated
        # together — their difference is how far players must dig.
        "cores": [
            {"id": "core-1", "piece": "floor", "at": [55, 21],
             "lava": 3, "lavaHeight": 3, "float": 6, "leak": 5, "openTop": False,
             "name": "Sluicehead Cistern"},
        ],
    },
    "walls": [],
    "boxes": [],
}

# ── the themes ────────────────────────────────────────────────────────────────
# Three. The floor is the ground, the moraine is the rock the ice left on it, and the works
# is what somebody built.
#
# The ground family is pale and cold — snow over packed ice — on a Cold taiga biome, because
# snow and ice are blocks and a snowfield on a summer biome has a meadow running through it.
# The built family is dark spruce over stone brick, which is not the family under its feet,
# and the accent is the leat's own blue.
ICE_FLAT = depth(cells([SNOW, PACKED_ICE], 13, 11), 1,
                 solid(PACKED_ICE), 2)
ICE_SHOULDER = depth(cells([SNOW, GRAVEL], 9, 19), 1,
                     solid(GRAVEL), 2)
ICE_FACE = depth(cells([STONE, COBBLE], 8, 27), 2,
                 solid(STONE), 3)

themes = {
    # the frozen floor: snow where it lies flat, swept gravel where it steepens, bare rock
    # on a face. The bands are cut against this board's own incline.
    "ice": theme(
        surface=slope(ICE_FLAT, 30, ICE_SHOULDER, 15, ICE_FACE, 45),
        wall=depth(solid(PACKED_ICE), 1, solid(STONE), 2, solid(COBBLE), 4),
        fill=voronoi([STONE, ANDESITE, DIORITE], 13, 7),
    ),
    # the moraine ridges: the rubble a glacier dumped, and it is stone
    "moraine": theme(
        surface=slope(depth(cells([GRAVEL, COBBLE], 7, 33), 1, solid(GRAVEL), 2), 30,
                      depth(cells([COBBLE, ANDESITE], 6, 37), 2, solid(STONE), 3), 60),
        wall=depth(solid(COBBLE), 1, solid(ANDESITE), 2, solid(STONE), 4),
        fill=voronoi([STONE, ANDESITE], 11, 17),
    ),
    # the made stone of the sluice works and the head's own face
    "works": theme(
        surface=depth(cells([SNOW, STONE_BRICK], 5, 51), 1, solid(STONE_BRICK), 2,
                      solid(STONE), 2),
        wall={"kind": "wallRun", "runs": [
            {"material": solid((STONE_BRICK, 3)), "thickness": 1},
            {"material": solid(STONE_BRICK), "thickness": 4},
            {"material": solid(MOSSY_BRICK), "thickness": 1},
            {"material": solid(STONE_BRICK), "thickness": 3},
        ]},
        fill=voronoi([STONE, ANDESITE], 12, 23),
        rim=(1, solid((STONE_BRICK, 3))),
    ),
}

# ── the shapes ────────────────────────────────────────────────────────────────
# The head is made ground and comes out of the solve, so it meets the floor at a face rather
# than being graded into it. Four blocks is a short face and two broad ramps answer it —
# `height_mode` and `skirt` for the relief, `keepClear` for the dressing, and a material
# rather than a theme, because a ramp is a thing somebody built.
RAMP = depth(solid(COBBLE), 1, solid(STONE), 2, solid(ANDESITE), 3)


def ramp(name, x0, x1):
    return {
        "id": name, "type": "polygon", "operation": "add", "override": True,
        "keepClear": True, "floor": 0, "base_height": HEAD_SURFACE,
        "height_mode": "level", "skirt": 0, "material": RAMP,
        "vertices": [[x0, -93], [x1, -93], [x1, -81], [x0, -81]],
        "anchor_heights": [HEAD_SURFACE, HEAD_SURFACE, FLOOR_SURFACE, FLOOR_SURFACE],
    }


# A patch owns the paint on a cell only where its own drawn top is the tallest drawn top
# there, so every one of these states the floor's own `base_height`.
add_shapes = [
    ramp("ramp-w", -27, -17),
    ramp("ramp-e", 20, 30),
    # the two moraines' rubble, drawn over the ground the pushes raise
    {"id": "moraine-w-cap", "type": "polygon", "operation": "add", "keepClear": False,
     "floor": 0, "base_height": FLOOR_SURFACE, "theme": "moraine",
     "vertices": [[-33, -65], [-24, -67], [-20, -56], [-22, -43], [-28, -38], [-33, -43]]},
    {"id": "moraine-e-cap", "type": "polygon", "operation": "add", "keepClear": False,
     "floor": 0, "base_height": FLOOR_SURFACE, "theme": "moraine",
     "vertices": [[23, -45], [30, -48], [33, -39], [32, -28], [26, -26], [22, -33]]},
    # The leat's east revetment, drawn as a polyline so the wall follows the channel's own
    # curve: a cut leat is walled, and four clicked points spline into that curve.
    {"id": "leat-wall", "type": "polyline", "operation": "add", "keepClear": True,
     "floor": 0, "base_height": FLOOR_SURFACE + 2, "theme": "works",
     "stroke_edge": "solid", "radius": 1,
     "vertices": [[1, -77], [4, -69], [5, -60], [3, -51], [1, -46]]},
    # the cistern's own quay: the made stone apron the core's casing stands over
    {"id": "quay", "type": "polygon", "operation": "add", "keepClear": False,
     "floor": 0, "base_height": FLOOR_SURFACE, "theme": "works",
     "vertices": [[11, -72], [31, -72], [32, -55], [23, -51], [12, -55]]},
]

# ── the relief ────────────────────────────────────────────────────────────────
# A trough is two long ridges facing each other across a floor, and the floor is what a
# player stands on — so it is pinned wide and flat, and the ridges are pushes rising out of
# it. Pinning the flanks as well would leave the solver nothing to solve.
relief = {
    "team": {
        "base": FLOOR_SURFACE,
        "reach": 0,
        "step": 1,
        "landform": "rolling",
        "grain": {"amplitude": 0.5, "scale": 17, "seed": 5},
        "marks": [
            # the sluice floor itself, flat and wide: the ground the match is fought on, and
            # the share of level ground RL5 measures
            {"id": "floor-pan", "kind": "area", "h": FLOOR_SURFACE, "bevel": 0,
             "ring": [[-35, -82], [35, -82], [35, -34], [-35, -34]]},
            # the apron at the frontline, where an attacker lands off the build zone
            {"id": "apron", "kind": "area", "h": 8, "bevel": 0,
             "ring": [[-35, -30], [35, -30], [35, -20], [-35, -20]]},
        ],
        "pushes": [
            # The west moraine, a long ridge: its crown climbs to a line rather than a peak
            # because the ring is long, which is what builds a crest instead of a cone.
            # Skirt 10/12 = 0.83 a block, crown 6/9 = 0.67 — inside RL6's factor of two.
            {"id": "moraine-w", "amount": 9, "falloff": 9, "crown": 5,
             "roughness": 0, "seed": 3,
             "ring": [[-32, -64], [-24, -66], [-19, -56], [-21, -43], [-28, -37], [-32, -42]]},
            # The east moraine, shorter and further forward, so the two are not one shape
            # twice. Its ring plus its falloff stop clear of the cistern's own pad.
            {"id": "moraine-e", "amount": 8, "falloff": 8, "crown": 4,
             "roughness": 0, "seed": 4,
             "ring": [[23, -44], [30, -47], [33, -39], [32, -28], [26, -25], [22, -32]]},
        ],
    },
}

# ── the buildings ─────────────────────────────────────────────────────────────
# Two placement ideas rather than a village: the sluice house standing over the leat on the
# floor, which is the approach a player fights through, and a gatehouse on the head where
# the leat leaves it. Both are dark spruce over stone brick on a white floor — a building
# has to read as a built thing from across the map, which means its walls are not in the
# tone family under its feet.
SLUICE_WALL = {"stack": {"bands": [
    {"material": {"kind": "laidLog", "id": LOG, "data": 1}, "thickness": 1},
    {"material": solid(STONE_BRICK), "thickness": 3},
    {"material": solid(MOSSY_BRICK), "thickness": 1},
    {"material": solid(STONE_BRICK), "thickness": 3},
], "ending": "repeat"}, "extent": 8}

SLUICE_SHELL = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": solid(STONE_BRICK), "thickness": 1}],
                            "ending": "repeat"}, "extent": 1},
        "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                    "inlayInset": 2, "isPlain": True},
        "footing": None,     # a footing over a one-course plate is a rim, not masonry
    },
    "roof": {
        "form": "gable", "pitch": 2, "slab": -1, "slabData": 0, "overhang": 1,
        "ridgeCap": False, "hole": False,
        "body": solid(SPRUCE_PLANKS),
        "verge": {"kind": "laidLog", "id": LOG, "data": 1},
        "gable": solid(SPRUCE_PLANKS),
        "gableWindows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3},
    },
    "wall": SLUICE_WALL,
    "post": solid(SPRUCE_LOG),              # one wood for post, beam and laid course (HS4)
    "windows": {"form": "stairLattice", "block": SPRUCE_STAIRS, "hostBlock": -1,
                "hostData": 0, "data": 0, "sill": 3, "width": 2, "height": 2, "spacing": 4},
    "storeys": [{
        "clear": 4,
        "wall": {"stack": {"bands": [
            {"material": {"kind": "laidLog", "id": LOG, "data": 1}, "thickness": 1},
            {"material": solid(SPRUCE_PLANKS), "thickness": 3},
            {"material": solid(STONE_BRICK), "thickness": 3},
        ], "ending": "repeat"}, "extent": 7},
        "post": solid(SPRUCE_LOG),
        "windows": {"form": "arched", "block": SPRUCE_STAIRS, "hostBlock": -1,
                    "hostData": 0, "data": 0, "sill": 2, "width": 2, "height": 2,
                    "spacing": 4},
    }],
    "porch": None,
    "front": None,
    "beams": {"block": LOG, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": SPRUCE_STAIRS,
                         "fill": "upperSlab", "fillBlock": SPRUCE_SLAB[0],
                         "fillData": SPRUCE_SLAB[1]},
                "width": 2, "height": 3},
}

# ── the dressing ──────────────────────────────────────────────────────────────
# A path is solid and three colours a reader cannot quite tell apart. This ground is hard
# and frozen, so the swept track is gravel, andesite and cobblestone.
TRACK = cells([GRAVEL, ANDESITE, COBBLE], 3, 43, rise=0)

TREES = json.load(open(os.path.join(HERE, "trees.json")))
TREE_KEYS = {"pine-a": "showcase-r2-1", "pine-b": "showcase-r7-3",
             "spruce-a": "showcase-r4-2", "spruce-b": "showcase-r4-5"}


def tree(pid, style, x, z):
    return {"id": pid, "kind": "tree", "style": style, "x": x, "z": z, "layer": "ground"}


def rock(pid, x, z, size, seed, form="angular"):
    """A boulder is stone — stone, cobblestone and andesite, and nothing else."""
    return {"id": pid, "kind": "boulder", "x": x, "z": z, "layer": "ground",
            "form": form, "size": size, "mossy": False, "seed": seed,
            "rock": cells([STONE, COBBLE, ANDESITE], 5, seed + 60, rise=4)}


def house(pid, x0, z0, x1, z1, seed, front, storeys_high=0):
    return {"id": pid, "kind": "house", "seed": seed, "layer": "ground",
            "style": "sluice", "front": front,
            "wings": [{"corners": [[x0, z0], [x1, z1]],
                       "spec": {"ridge": "alongX", "storeysHigh": storeys_high}}]}


dressing = {
    "styles": {
        "sluice": {"kind": "house", "shell": SLUICE_SHELL},
        **{key: TREES[name] for key, name in TREE_KEYS.items()},
    },
    "props": [
        # The leat: a cut channel of meltwater running the length of the floor, past the
        # cistern and out to the frontline. It names its layer, because a prop naming none
        # carves against the top of the stack; it states no level, because the floor it
        # crosses is ground that is already there and the line is found; and its run is
        # kept level, because a channel down a fall is trenched by the fall's whole height.
        {"id": "leat", "kind": "water", "seed": 61, "layer": "ground",
         "shape": "channel", "form": "canal",
         "points": [[-6, -80], [-2, -71], [0, -60], [-2, -50], [-4, -44]],
         "radius": 3, "depth": 3, "shore": 2, "shoreWander": True, "edge": 1,
         "bank": cells([PACKED_ICE, SNOW, GRAVEL], 7, 71, rise=3)},

        # the swept track: the spawn door, down the west ramp, along the floor to the quay
        {"id": "track-head", "kind": "stroke", "seed": 5, "layer": "ground",
         "points": [[0, -104], [-6, -98], [-14, -94], [-20, -91]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},
        {"id": "track-floor", "kind": "stroke", "seed": 6, "layer": "ground",
         "points": [[-22, -78], [-19, -68], [-15, -58], [-12, -50]],
         "radius": 2, "style": "solid", "claimsGround": True, "pave": TRACK},

        # The sluice house, standing over the leat on the open floor — the approach a player
        # fights through. Its nearest cell is twelve blocks from the core's marker, clear of
        # OB19's 21×21 clearance.
        house("sluice-house", 4, -82, 18, -75, 311, front="posZ", storeys_high=0),
        # and the winding house by the leat's tail, a storey lower: a row is two buildings
        # that differ in height and footprint and in nothing else
        house("winding-house", 5, -44, 15, -37, 312, front="posZ", storeys_high=1),

        # Trees to the outside of the floor, never on the approach in front of the cistern
        # and never on the brink an attacker arrives at. All are eleven or more blocks from
        # the core's marker and three or more from any claimed paving.
        tree("tree-w1", "pine-a", -32, -60),
        tree("tree-w2", "spruce-a", -30, -95),
        tree("tree-e1", "pine-b", 32, -93),
        tree("tree-e2", "spruce-b", 33, -68),
        # one on the west moraine's own crest, where a climber tops out
        tree("tree-m1", "spruce-a", -26, -52),

        # boulders on flat ground: a rock pinned to a face reads as neither
        rock("rock-w1", 9, -52, 3, 21),
        rock("rock-e1", 8, -56, 3, 22, form="round"),
        rock("rock-h1", 30, -97, 3, 23, form="cairn"),

        # Ground cover over the whole board, held off the frontline apron: the ground in
        # front of a line is fought over and wants to be read at a glance. Both of its
        # gameplay numbers stay low, and on a cold board most of what it lays is fern.
        {"id": "sward", "kind": "flora", "seed": 9,
         "points": [[-35, -98], [35, -98], [35, -38], [-35, -38]],
         "spec": {"coverage": 0.18, "scale": 24, "octaves": 2,
                  "fernShare": 0.40, "flowerShare": 0.04, "flowerScale": 30,
                  "tallShare": 0.04}},
    ],
}

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-21",
    # Cold taiga, #80b497. Snow and ice are blocks, so a snowfield on a summer biome has a
    # meadow running through it — the biome is a palette decision, not a line added at the end.
    "biome": {"kind": "solid", "id": 30},
    "mapTheme": "ice",
    "themes": themes,
    # Keyed on the compiled shape ids, read off POST /plan/compile: the compiler fuses the
    # pieces that share a height, so the floor is `floor-10` and the head and the spawn
    # together are `floor-14`.
    "themeById": {"floor-14": "works"},
    # The head is made ground and comes out of the solve, so it keeps the height it was
    # drawn at and meets the floor at a face. Left in the solve it settled to the floor's
    # own level and the ramps stood three blocks proud of it — a solved shape's own
    # `base_height` decides nothing about where its ground ends up.
    "shapePropsById": {"floor-14": {"relief_scope": "exclude"}},
    "addShapes": add_shapes,
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
