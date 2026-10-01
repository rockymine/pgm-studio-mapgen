#!/usr/bin/env python3
"""Delverdale: writes delverdale.plan.json and delverdale.refinement.json beside this file.

A wooded lead-mining dale for thirty-two a side. Each team holds a village green on a raised terrace
in the middle of its half; one wool is kept up the west side in the mine yard behind a bedrock wall,
the other in the quarry cut into the east fell, reached over the fell or through the drift driven under it.

Every rectangle is written in blocks and divided by the cell here, so the numbers read as the board.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SLUG = "delverdale"
CELL = 4


def rect(x0, z0, x1, z1):
    """A block rectangle [x0, x1) × [z0, z1) as the plan's cell rect."""
    for v in (x0, z0, x1, z1):
        assert v % CELL == 0, (x0, z0, x1, z1)
    return [x0 // CELL, z0 // CELL, (x1 - x0) // CELL, (z1 - z0) // CELL]


def piece(pid, x0, z0, x1, z1, surface=None, role="piece", mirrors=None):
    p = {"id": pid, "role": role, "rect": rect(x0, z0, x1, z1)}
    if surface is not None:
        p["surface"] = surface
    if mirrors is not None:
        p["mirrors"] = mirrors
    return p


# ── the plan ─────────────────────────────────────────────────────────────────────────────────────
# Team 0's unit is the +z half; rot_180 fans it onto the -z half. x runs across the board, z along it.
PIECES = [
    # the crossing: a holm on the axis and a stone either side of it, inside one build band
    piece("holm", -20, -8, 20, 8, mirrors=False),
    piece("stone", 32, -4, 48, 4),
    # the front: two tips with the rotation hole between them, hung off the hub's front bar
    piece("tip-w", -52, 20, -20, 36),
    piece("tip-e", 20, 20, 52, 36),
    # the hub: a front bar, three lanes north with two holes between them, a back bar
    piece("hub-front", -52, 36, 52, 52),
    piece("w-fell", -60, 52, -40, 88),
    piece("green", -24, 52, 24, 88, surface=20),
    piece("e-fell", 40, 52, 72, 100),
    piece("hub-back", -60, 88, 40, 100),
    # the spawn, on the back bar
    piece("apron", -20, 100, 4, 108),
    piece("spawn", -16, 108, 4, 128, role="spawn"),
    # wool A: the mine yard up the west side, walled at its neck
    piece("a-lane", -60, 100, -44, 112),
    piece("a-neck", -60, 112, -44, 116),
    piece("a-yard", -60, 116, -44, 140),
    piece("a-room", -72, 124, -60, 140, role="wool-room"),
    # wool B: the quarry at the north end of the east fell
    piece("quarry", 40, 100, 72, 124),
    piece("b-room", 72, 112, 84, 128, role="wool-room"),
]

PLAN = {
    "plan": 2,
    "meta": {"name": "Delverdale", "authors": ["Opus 5.5"]},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 32, "surface": 9, "observerY": 56},
    "pieces": PIECES,
    "zones": [{"id": "band", "rect": rect(-52, -20, 52, 20), "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn", "piece": "spawn", "at": [10, 10], "facing": "front"}],
        "wools": [
            {"id": "wool-a", "piece": "a-room", "at": [6, 8]},
            {"id": "wool-b", "piece": "b-room", "at": [6, 8]},
        ],
        "iron": [],
        "destroyables": [],
        "cores": [],
    },
    "walls": [{"a": "a-neck", "b": "a-yard"}],
}


# ── the finish ───────────────────────────────────────────────────────────────────────────────────
# The compile names a component after its alphabetically first piece and its height, so the team's
# ground is `a-lane-9` and the village terrace, stated at 20, is `a-lane-20`.
GROUND = "a-lane-9"
TERRACE = "a-lane-20"


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def depth_stack(top, under, under_courses=2):
    """A surfacing course over soil: one course of `top` over `under_courses` of `under`."""
    return {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [
        {"thickness": 1, "material": top},
        {"thickness": under_courses, "material": under}]}}


def cell(seed, size, palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": 1, "warp": 1,
            "palette": palette, "rise": rise}


GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
STONE, ANDESITE, COBBLE, GRAVEL = solid(1), solid(1, 5), solid(4), solid(13)

# the dale's rock: stone and andesite as the base, cobble as the accent at a quarter
ROCK = cell(31, 3, [STONE, ANDESITE, STONE, COBBLE])
ROCK_FILL = cell(32, 5, [STONE, STONE, ANDESITE], rise=3)
EARTH = cell(33, 2, [DIRT, COARSE])

THEMES = {
    # the dale: meadow on the flat, worn earth on the shoulder, limestone on the face
    "dale": {
        "bedrock": {"relative": False, "value": 1},
        "fill": ROCK_FILL,
        "wallEnabled": True, "wallOnTerrainFaces": True,
        "wall": cell(34, 3, [STONE, ANDESITE, STONE], rise=2),
        "surface": {"enabled": True, "depth": 3, "material": {
            "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
                {"thickness": 32, "material": depth_stack(GRASS, DIRT)},
                {"thickness": 12, "material": depth_stack(EARTH, DIRT)},
                {"thickness": 46, "material": depth_stack(ROCK, STONE)}]}}},
        "rim": {"enabled": False, "depth": 1, "material": STONE},
        "rimEdges": "void",
    },
    # the village terrace: a lawn on made ground, its retaining face coursed stone brick
    "green": {
        "bedrock": {"relative": False, "value": 1},
        "fill": ROCK_FILL,
        "wallEnabled": True, "wallOnTerrainFaces": True,
        "wall": cell(35, 3, [solid(98), solid(98), solid(1, 6)], rise=2),
        "surface": {"enabled": True, "depth": 1, "material": GRASS},
        "rim": {"enabled": True, "depth": 1, "material": solid(98, 0)},
        "rimEdges": "boundary",
    },
    # the workings: a floor of worked rock with gravel and rubble lying in it as patches, over the rock
    "mine": {
        "bedrock": {"relative": False, "value": 1},
        "fill": ROCK_FILL,
        "wallEnabled": True, "wallOnTerrainFaces": True,
        "wall": cell(36, 3, [STONE, ANDESITE, STONE], rise=2),
        "surface": {"enabled": True, "depth": 2, "material": {
            "kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [
                {"thickness": 1, "material": {"kind": "noise", "seed": 37, "scale": 2, "octaves": 2,
                                               "stops": [GRAVEL, cell(38, 2, [STONE, ANDESITE, STONE]),
                                                         cell(39, 2, [ANDESITE, STONE, ANDESITE]), COBBLE],
                                               "rise": 0}},
                {"thickness": 1, "material": STONE}]}}},
        "rim": {"enabled": False, "depth": 1, "material": STONE},
        "rimEdges": "void",
    },
}


def ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def lobed(cx, cz, radius, lobes=5, wobble=0.18, turn=0.0, points=20):
    """A ring of `points` round (cx, cz) whose radius swells and shrinks `lobes` times, so a push
    reads as ground rather than as a stamped disc."""
    import math
    out = []
    for i in range(points):
        a = turn + 2 * math.pi * i / points
        r = radius * (1 + wobble * math.sin(lobes * a + 0.7))
        out.append([round(cx + r * math.cos(a), 1), round(cz + r * math.sin(a), 1)])
    return out


# ── the ground ──
# Standing levels rise from the front to the back: the tips at 14, the hub's front bar at 16, the
# village terrace at 20 (made ground, out of the solve), the back bar, the spawn and the mine yard at 24.
# The east fell is a crest at 28 pinned along the drift's own line, so the roof over the drift is flush
# with the ground either side of it; its south face is the adit face and its north face the quarry wall.
TEAM_RELIEF = {
    "base": 18, "reach": 0, "step": 1,
    "marks": [
        {"id": "tips-w", "kind": "area", "h": 14, "bevel": 0, "ring": ring(-52, 20, -20, 34)},
        {"id": "tips-e", "kind": "area", "h": 14, "bevel": 0, "ring": ring(20, 20, 52, 34)},
        {"id": "stone", "kind": "area", "h": 14, "bevel": 0, "ring": ring(32, -4, 48, 4)},
        {"id": "hub-front", "kind": "area", "h": 16, "bevel": 0, "ring": ring(-38, 40, 52, 50)},
        {"id": "hub-back", "kind": "area", "h": 24, "bevel": 0, "ring": ring(-60, 90, 38, 100)},
        # the quarry stair lands on the fell's corner, so the corner is stated at the stair's own head
        {"id": "quarry-landing", "kind": "area", "h": 24, "bevel": 0, "ring": ring(38, 88, 48, 99)},
        {"id": "spawn", "kind": "area", "h": 24, "bevel": 0, "ring": ring(-20, 100, 4, 128)},
        {"id": "mine-yard", "kind": "area", "h": 24, "bevel": 0, "ring": ring(-72, 100, -44, 140)},
        {"id": "crest", "kind": "line", "points": [[46, 57], [46, 58], [49, 72], [55, 86], [57, 95]], "h": 28, "r": 5},
        {"id": "east-flank", "kind": "line", "points": [[71, 58], [71, 96]], "h": 22, "r": 1},
        {"id": "rake", "kind": "line", "points": [[53, 53], [60, 55], [67, 60]], "h": [17, 21, 25], "r": 2},
        {"id": "quarry", "kind": "area", "h": 16, "bevel": 0, "ring": ring(40, 102, 72, 124)},
        {"id": "quarry-room", "kind": "area", "h": 16, "bevel": 0, "ring": ring(72, 112, 84, 128)},
    ],
    "grain": {"amplitude": 1, "scale": 28, "seed": 7},
    "pushes": [
        # the west fell: a knoll whose ring stands over the void past the coast, so its skirt lands
        # on the lane's outer half as a flank and leaves the inner half to walk
        {"id": "west-knoll", "ring": lobed(-70, 68, 11, lobes=3, turn=0.4), "amount": 7, "falloff": 10,
         "crown": 0, "roughness": 0, "seed": 3},
        # its other rim, over the hole: the west fell is a small dale with the road in its floor
        {"id": "dale-rim", "ring": lobed(-30, 84, 10, lobes=3, turn=1.1), "amount": 5, "falloff": 8,
         "crown": 0, "roughness": 0, "seed": 4},
    ],
}

HOLM_RELIEF = {
    "base": 14, "reach": 0, "step": 1,
    "marks": [{"id": "holm", "kind": "area", "h": 14, "bevel": 2, "ring": ring(-20, -8, 20, 8)}],
    # a low howe in the middle of the holm, which the engine house stands on
    "pushes": [{"id": "howe", "ring": lobed(0, 0, 5, lobes=4), "amount": 2, "falloff": 6, "crown": 1,
                "roughness": 0, "seed": 5}],
}


def flight(fid, verts, anchors, material):
    """A stair: a tilted plane at absolute heights, set into the higher tier and kept clear of props."""
    return {"id": fid, "type": "polygon", "operation": "add", "override": True, "floor": 0,
            "base_height": max(anchors), "height_mode": "level", "skirt": 0,
            "vertices": verts, "anchor_heights": anchors, "keepClear": True, "material": material,
            "group": "team"}


STAIR_STONE = cell(41, 2, [solid(98), solid(1, 6), solid(98), solid(1, 5)], rise=2)
TRACK = cell(42, 3, [GRAVEL, ANDESITE, COBBLE], rise=2)

def band(points, half):
    """A straight-sided band of half-width `half` about a centreline, as one polygon ring with mitred
    joins. The floor and the roof are both drawn with it, so the roof over the floor's middle stretch
    covers exactly the columns the floor cut."""
    import math
    left, right = [], []
    for i, (x, z) in enumerate(points):
        dirs = []
        if i > 0:
            dirs.append((x - points[i - 1][0], z - points[i - 1][1]))
        if i < len(points) - 1:
            dirs.append((points[i + 1][0] - x, points[i + 1][1] - z))
        normals = []
        for dx, dz in dirs:
            length = math.hypot(dx, dz)
            normals.append((-dz / length, dx / length))
        nx = sum(n[0] for n in normals) / len(normals)
        nz = sum(n[1] for n in normals) / len(normals)
        scale = half / max(0.5, (nx * normals[0][0] + nz * normals[0][1]))
        norm = math.hypot(nx, nz)
        nx, nz = nx / norm, nz / norm
        left.append([round(x + nx * scale, 2), round(z + nz * scale, 2)])
        right.append([round(x - nx * scale, 2), round(z - nz * scale, 2)])
    return left + right[::-1]


# the drift's centreline, from the hub's front bar under the east fell to the quarry floor; the roof
# covers the stretch inside the fell, z 53 to 98, on the same line, and a portal stands at each end
DRIFT = [[46, 44], [46, 58], [49, 72], [55, 86], [58, 95], [58, 110]]
DRIFT_ROOF = [[46, 53], [46, 58], [49, 72], [55, 86], [58, 95], [58, 99]]
DRIFT_HALF = 2.5

ADD_SHAPES = [
    # the village terrace's two flights, each set into the higher tier it climbs
    flight("green-stair-s", [[-4, 52], [4, 52], [4, 60], [-4, 60]], [16, 16, 20, 20], STAIR_STONE),
    flight("green-stair-n", [[-4, 88], [4, 88], [4, 96], [-4, 96]], [20, 20, 24, 24], STAIR_STONE),
    # the quarry stair, down the pit's west side from the back bar
    flight("quarry-stair", [[40, 98], [46, 98], [46, 114], [40, 114]], [24, 24, 16, 16], TRACK),
    # the worked ground: the quarry floor and the mine yard behind the wall, each stated at the height
    # the relief pins it to, so the shape forms the surface there and paints it
    {"id": "quarry-floor", "type": "polygon", "operation": "add", "floor": 0, "base_height": 16,
     "vertices": [[47, 102], [72, 102], [72, 124], [47, 124]], "theme": "mine", "group": "team"},
    {"id": "mine-yard", "type": "polygon", "operation": "add", "floor": 0, "base_height": 24,
     "vertices": [[-60, 117], [-44, 117], [-44, 140], [-60, 140]], "theme": "mine", "group": "team"},
    # the drift's floor: the fell cut down to the quarry floor along a band 2.5 either side of the line
    {"id": "drift-floor", "type": "polygon", "operation": "add", "override": True, "floor": 0,
     "base_height": 16, "height_mode": "level", "skirt": 0,
     "vertices": band(DRIFT, DRIFT_HALF), "keepClear": True, "theme": "mine", "group": "team"},
]

ADD_LAYERS = [
    # the drift's roof: four courses over its floor, flush with the crest the relief pins either side
    {"id": "drift-roof", "name": "drift roof", "base_y": 20,
     "shapes": [{"id": "drift-roof", "type": "polygon", "operation": "add", "floor": 0, "base_height": 8,
                 "vertices": band(DRIFT_ROOF, DRIFT_HALF), "theme": "dale"}],
     "groups": [{"id": "drift-roof", "name": "drift roof", "mirrors": True, "shapeIds": ["drift-roof"]}]},
]

# ── the outlines, reshaped one point at a time ──
# Inserts are written against the compiled ring's own indices and replayed in descending order, so an
# insert never shifts an index a later op still names; moves come first because they shift nothing.
def edits(moves=(), inserts=()):
    ops = [{"index": i, "x": x, "z": z} for i, (x, z) in moves]
    for after, points in sorted(inserts, key=lambda item: -item[0]):
        for step, (x, z) in enumerate(points):
            ops.append({"after": after + step, "x": x, "z": z})
    return ops


def chamfer_rect(x0, z0, x1, z1, cut):
    """A rectangle ring (x0,z0)->(x1,z0)->(x1,z1)->(x0,z1) with every corner cut back by `cut`."""
    moves = [(0, (x0 + cut, z0)), (1, (x1, z0 + cut)), (2, (x1 - cut, z1)), (3, (x0, z1 - cut))]
    inserts = [(0, [(x1 - cut, z0)]), (1, [(x1, z1 - cut)]), (2, [(x0 + cut, z1)]), (3, [(x0, z0 + cut)])]
    return edits(moves, inserts)


EDIT_SHAPES = {
    GROUND: edits(inserts=[
        # the west fell's coast, pushed out into a wandering edge under the knoll
        (1, [(-60, 104), (-62, 96), (-66, 84), (-65, 72), (-63, 62), (-61, 56)]),
        # the hub's front bar bellies a little past the west tip
        (3, [(-55, 46), (-53, 40)]),
        # the east fell's coast
        (11, [(74, 60), (77, 72), (76, 86), (73, 96)]),
        # the quarry's north lip
        (16, [(64, 127), (54, 126), (46, 128)]),
        # the back bar's two stretches of coast
        (18, [(30, 102), (16, 101)]),
        (24, [(-28, 102), (-38, 101)]),
    ]),
    # the two hub holes, their corners taken off
    "void-1-cut": chamfer_rect(-40, 52, -24, 88, 3),
    "void-2-cut": chamfer_rect(24, 52, 40, 88, 3),
    # the holm and the stone, cut to octagons; the holm stays its own image under the turn
    # the holm lies across the centre and is its own image, and its eight edits are every corner of it
    "holm-9": [{**op, "fan": False} for op in chamfer_rect(-20, -8, 20, 8, 4)],
    "stone-9": chamfer_rect(32, -4, 48, 4, 2),
}


# ── the buildings ──
# One house style for every dwelling on the board: a dark-oak frame, brick to the sill, whitewashed clay
# above, a laid-log course under the eaves and a brick roof. The rooms are the works: the same frame and
# brick, one storey, under dark-oak boards, so the three things a player enters read as the mine's.
DARK_LOG = solid(162, 1)
LAID_DARK = {"kind": "laidLog", "id": 162, "data": 1}
WHITE = solid(159, 0)
BRICK = solid(45)
PANE = {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
        "sill": 2, "width": 2, "height": 2, "spacing": 3}


def stack(*bands):
    return {"stack": {"ending": "repeat", "bands": [{"thickness": t, "material": m} for t, m in bands]}}


def house_style(roof_body, storeys, gable=WHITE, pitch=2):
    style = {
        "foundation": {"plate": {**stack((1, solid(5, 1))), "extent": 1},
                       "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                   "inlayInset": 2, "isPlain": True},
                       "footing": None},
        "roof": {"form": "gable", "pitch": pitch, "slab": -1, "slabData": 0, "overhang": 1,
                 "ridgeCap": True, "hole": False, "body": roof_body, "verge": LAID_DARK, "gable": gable,
                 "gableWindows": {**PANE, "sill": 1, "width": 1, "height": 1}},
        "wall": {**stack((2, BRICK), (3, WHITE)), "extent": 5},
        "post": DARK_LOG,
        "windows": PANE,
        "storeys": storeys,
        "porch": None, "front": None,
        "beams": {"block": 162, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "none", "block": 53, "fill": "upperSlab",
                                            "fillBlock": 126, "fillData": 5}, "width": 2, "height": 3},
    }
    return style


COTTAGE = house_style(BRICK, [
    {"clear": 5, "post": DARK_LOG, "deck": None, "wall": {**stack((2, BRICK), (3, WHITE)), "extent": 5},
     "windows": PANE},
    {"clear": 4, "post": DARK_LOG, "deck": None, "wall": {**stack((3, WHITE), (1, LAID_DARK)), "extent": 4},
     "windows": PANE},
])
WORKS = house_style(solid(5, 5), [
    {"clear": 5, "post": DARK_LOG, "deck": None, "wall": {**stack((4, BRICK), (1, LAID_DARK)), "extent": 5},
     "windows": PANE},
], gable=solid(5, 5), pitch=1)

# the copied trees are the showcase's own: each key names the showcase tree it is, and its recipe
# comes whole from the showcase snapshot
with open(os.path.join(ROOT, "corpus", "tree-showcase", "trees.json")) as handle:
    SHOWCASE = json.load(handle)["trees"]
TREES = {key: SHOWCASE[name]["style"] for key, name in {
    "oak-1": "tiny-oak-1", "oak-2": "tiny-oak-2", "oak-5": "tiny-oak-5", "oak-8": "tiny-oak-8",
    "oak-great-3": "oak-7", "oak-great-5": "oak-9",
    "birch-1": "birch-1", "birch-4": "birch-4", "birch-6": "birch-6", "birch-9": "birch-9"}.items()}

ROCK_BOULDER = {"kind": "boulder", "form": "round", "size": 3, "mossy": False,
                "rock": cell(51, 3, [STONE, ANDESITE, STONE, COBBLE])}
OUTCROP = {"kind": "boulder", "form": "outcrop", "size": 4, "mossy": False,
           "rock": cell(52, 3, [STONE, ANDESITE, STONE, COBBLE])}

SOFT_PATH = cell(61, 2, [DIRT, COARSE, solid(5, 1)])
HARD_PATH = cell(62, 2, [GRAVEL, ANDESITE, COBBLE])


def house(hid, x0, z0, x1, z1, front, storeys, ridge, seed):
    return {"id": hid, "kind": "house", "seed": seed, "style": "cottage", "front": front,
            "wings": [{"corners": [[x0, z0], [x1, z1]], "spec": {"storeysHigh": storeys, "ridge": ridge}}]}


def path(pid, points, radius, pave, seed):
    return {"id": pid, "kind": "stroke", "seed": seed, "points": points, "radius": radius,
            "style": "solid", "claimsGround": True, "pave": pave}


def tree(tid, x, z, style, seed, layer=None):
    t = {"id": tid, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}
    if layer:
        t["layer"] = layer
    return t


def boulder(bid, x, z, style, seed):
    return {"id": bid, "kind": "boulder", "seed": seed, "x": x, "z": z, "style": style}


HOUSES = [
    # the village on the green: two rows facing each other across the street, one tall and one low each
    house("green-sw", -24, 55, -16, 61, "posX", 2, "alongX", 101),
    house("green-nw", -24, 72, -16, 78, "posX", 1, "alongX", 102),
    house("green-se", 15, 55, 23, 61, "negX", 1, "alongX", 103),
    house("green-ne", 15, 72, 23, 78, "negX", 2, "alongX", 104),
    # the farmhouse on the west fell, on the hole's rim, clear of the knoll
    house("farm", -49, 62, -41, 68, "negX", 1, "alongZ", 105),
    # the miner's cottage on the fell top, beside the drift's roof
    house("fell-cottage", 55, 66, 63, 72, "negZ", 1, "alongX", 106),
]

PATHS = [
    # the street across the green, stair to stair, and on to the spawn
    path("street", [[0, 58], [0, 74], [0, 90]], 2, SOFT_PATH, 201),
    path("spawn-road", [[0, 94], [-4, 99], [-6, 106]], 2, SOFT_PATH, 202),
    # from the south stair's foot to each tip
    path("front-w", [[-2, 50], [-18, 46], [-34, 38], [-38, 28]], 2, SOFT_PATH, 203),
    path("front-e", [[2, 50], [18, 46], [32, 40], [36, 28]], 2, SOFT_PATH, 204),
    # the west fell's road, the hub bar to the back bar
    path("fell-road", [[-46, 46], [-50, 58], [-53, 72], [-52, 86], [-48, 94]], 2, SOFT_PATH, 205),
    # the mine track: the back bar west to the yard, through the wall line to the ore house door
    path("mine-track", [[-8, 92], [-30, 92], [-50, 94], [-52, 104], [-52, 124], [-58, 132]], 2, HARD_PATH, 206),
    # the quarry track: the back bar east to the quarry stair's head, and across the floor to the room
    path("quarry-track", [[8, 92], [26, 92], [38, 96]], 2, HARD_PATH, 207),
    path("quarry-floor", [[44, 116], [56, 118], [70, 120]], 2, HARD_PATH, 208),
    # the rake up the fell's face, and on across the top to the cottage
    path("rake", [[52, 50], [60, 54], [66, 59], [64, 64]], 1, SOFT_PATH, 209),
]

# Trees go to the outside of a piece: a copse on the west knoll, a wood down the east fell's far flank,
# a line on the back bar's coast, three on the fell's rim over the hole and two on the quarry lip. None on
# the front, the tips, the green, the approach to the wall or the holm. Oak is the wood, birch its accent.
TREE_SITES = [
    ("knoll-2", -64, 72, "oak-great-3"), ("knoll-3", -63, 84, "birch-4"),
    ("knoll-4", -60, 96, "oak-8"),
    ("farm-yard", -45, 78, "birch-6"),
    ("back-1", 16, 98, "oak-5"), ("back-2", 30, 98, "birch-1"), ("back-3", -32, 98, "oak-8"),
    ("east-wood-1", 70, 61, "birch-4"), ("east-wood-2", 74, 70, "oak-1"), ("east-wood-3", 69, 79, "birch-6"),
    ("east-wood-4", 73, 88, "birch-1"), ("east-wood-5", 68, 96, "birch-9"),
    ("cottage-oak", 56, 61, "oak-5"), ("fell-west-rim", 41, 76, "oak-8"),
    ("fell-rim-south", 41, 62, "birch-1"), ("fell-rim-north", 42, 88, "oak-1"),
    ("quarry-lip-1", 48, 124, "birch-1"), ("quarry-lip-2", 58, 124, "birch-4"),
]
TREE_PROPS = [tree(tid, x, z, style, 400 + i) for i, (tid, x, z, style) in enumerate(TREE_SITES)]
BOULDER_PROPS = [
    boulder("knoll-stone", -61, 77, "rock", 501),
    boulder("fell-stone", 62, 80, "outcrop", 502),
]

BOARD_RING = [[-88, -144], [88, -144], [88, 144], [-88, 144]]

DRESSING = {
    "styles": {"cottage": {"kind": "house", "shell": COTTAGE},
               "rock": ROCK_BOULDER, "outcrop": OUTCROP, **TREES},
    "props": HOUSES + PATHS + BOULDER_PROPS + TREE_PROPS + [
        {"id": "cover", "kind": "flora", "seed": 301, "points": BOARD_RING,
         "spec": {"coverage": 0.3, "scale": 7, "octaves": 2, "fernShare": 0.3, "flowerShare": 0.06,
                  "flowerScale": 9, "tallShare": 0.08}},
    ],
}


# ── made things ──
# The engine house on the holm: a roofless shell twelve by eight with a chimney at each end, laid out
# about the turn's own centre so it is its own image and is built once.
def rect_shape(sid, x0, z0, x1, z1, height, material, floor=0):
    return {"id": sid, "type": "rectangle", "operation": "add", "floor": floor, "base_height": height,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1, "material": material}


RUIN = cell(71, 2, [solid(98), solid(98), solid(98, 2), solid(98), solid(98, 1)], rise=2)
ENGINE_HOUSE = [
    rect_shape("eh-n-w", -6, 3, -1, 4, 6, RUIN), rect_shape("eh-n-e", 1, 3, 6, 4, 6, RUIN),
    rect_shape("eh-s-w", -6, -4, -1, -3, 6, RUIN), rect_shape("eh-s-e", 1, -4, 6, -3, 6, RUIN),
    rect_shape("eh-w", -6, -3, -5, 3, 5, RUIN), rect_shape("eh-e", 5, -3, 6, 3, 5, RUIN),
    rect_shape("eh-stack-w", -8, -1, -6, 1, 14, BRICK), rect_shape("eh-stack-e", 6, -1, 8, 1, 14, BRICK),
]


def inside(ring, px, pz):
    """Whether a point lies in a polygon ring or on its edge (even-odd, edge-inclusive)."""
    hit = False
    for (x1, z1), (x2, z2) in zip(ring, ring[1:] + ring[:1]):
        if min(z1, z2) <= pz <= max(z1, z2) and z1 != z2:
            cross = x1 + (pz - z1) * (x2 - x1) / (z2 - z1)
            if abs(cross - px) < 1e-9:
                return True
            if (z1 > pz) != (z2 > pz) and px < cross:
                hit = not hit
    return hit


def timber_sets():
    """Timber sets down the covered stretch of the drift: a post each side and a cap beam across under
    the roof, with a lamp in the middle of the beam, every eight blocks along the line. Each post stands
    on the outermost cell of the drift's own band in that row."""
    import math
    roof = band(DRIFT_ROOF, DRIFT_HALF)
    pts = DRIFT_ROOF
    segs = [(a, b, math.hypot(b[0] - a[0], b[1] - a[1])) for a, b in zip(pts, pts[1:])]
    total = sum(length for _, _, length in segs)
    shapes, station, n = [], 5.0, 0
    while station < total - 3:
        walked = 0.0
        for a, b, length in segs:
            if walked + length >= station:
                t = (station - walked) / length
                cx, cz = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                break
            walked += length
        z = int(math.floor(cz))
        cells = [x for x in range(int(cx) - 6, int(cx) + 7) if inside(roof, x + 0.5, z + 0.5)]
        west, east = cells[0], cells[-1]
        mid = (west + east) // 2
        n += 1
        shapes += [
            rect_shape(f"set{n}-post-w", west, z, west + 1, z + 1, 4, DARK_LOG),
            rect_shape(f"set{n}-post-e", east, z, east + 1, z + 1, 4, DARK_LOG),
            rect_shape(f"set{n}-beam-w", west + 1, z, mid, z + 1, 1, solid(162, 5), floor=3),
            rect_shape(f"set{n}-beam-e", mid + 1, z, east, z + 1, 1, solid(162, 5), floor=3),
            rect_shape(f"set{n}-lamp", mid, z, mid + 1, z + 1, 1, solid(89), floor=3),
        ]
        station += 8.0
    return shapes


TIMBERING = timber_sets()

# The two portals: a dark-oak frame, two posts and a laid lintel, under a rock face one row deep where
# the roof slab stops, so the drift opens out of the fell's own stone rather than out of turf.
PORTAL_ROCK = cell(72, 2, [STONE, ANDESITE, STONE], rise=2)
PORTALS = [(43, 49, 52), (55, 61, 99)]      # x from, x to (exclusive), the row z
PORTAL_FRAME, PORTAL_FACE = [], []
for n, (x0, x1, z) in enumerate(PORTALS, 1):
    PORTAL_FRAME += [rect_shape(f"portal{n}-post-w", x0, z, x0 + 1, z + 1, 4, DARK_LOG),
                     rect_shape(f"portal{n}-post-e", x1 - 1, z, x1, z + 1, 4, DARK_LOG),
                     rect_shape(f"portal{n}-lintel", x0 + 1, z, x1 - 1, z + 1, 1, solid(162, 5), floor=4)]
    PORTAL_FACE.append(rect_shape(f"portal{n}-rock", x0, z, x1, z + 1, 7, PORTAL_ROCK))
# the lintel's two end columns are the posts', so the posts carry on through it
for shape in PORTAL_FRAME:
    if "-post-" in shape["id"]:
        shape["base_height"] = 5

# The village well on the green: a stone-brick kerb round one block of water, two posts and a windlass bar.
WELL_KERB = [rect_shape("well-n", -12, 64, -9, 65, 1, solid(98)), rect_shape("well-s", -12, 66, -9, 67, 1, solid(98)),
             rect_shape("well-post-w", -12, 65, -11, 66, 3, DARK_LOG),
             rect_shape("well-post-e", -10, 65, -9, 66, 3, DARK_LOG),
             rect_shape("well-water", -11, 65, -10, 66, 1, solid(9))]
WELL_BAR = [rect_shape("well-bar", -12, 65, -9, 66, 1, solid(162, 5))]

MADE_LAYERS = [
    {"id": "engine-house", "name": "engine house", "base_y": 16, "kind": "made", "part_of": "engine-house",
     "seat": "ground", "shapes": ENGINE_HOUSE,
     "groups": [{"id": "engine-house", "name": "engine house", "mirrors": False,
                 "shapeIds": [shape["id"] for shape in ENGINE_HOUSE]}]},
    {"id": "portal-frames", "name": "portal frames", "base_y": 16, "kind": "made", "part_of": "portals",
     "shapes": PORTAL_FRAME,
     "groups": [{"id": "portal-frames", "name": "portal frames", "mirrors": True,
                 "shapeIds": [shape["id"] for shape in PORTAL_FRAME]}]},
    {"id": "portal-faces", "name": "portal faces", "base_y": 21, "kind": "made", "part_of": "portals",
     "shapes": PORTAL_FACE,
     "groups": [{"id": "portal-faces", "name": "portal faces", "mirrors": True,
                 "shapeIds": [shape["id"] for shape in PORTAL_FACE]}]},
    {"id": "well", "name": "village well", "base_y": 20, "kind": "made", "part_of": "well", "shapes": WELL_KERB,
     "groups": [{"id": "well", "name": "village well", "mirrors": True,
                 "shapeIds": [shape["id"] for shape in WELL_KERB]}]},
    {"id": "well-bar", "name": "village well bar", "base_y": 23, "kind": "made", "part_of": "well",
     "shapes": WELL_BAR,
     "groups": [{"id": "well-bar", "name": "village well bar", "mirrors": True,
                 "shapeIds": [shape["id"] for shape in WELL_BAR]}]},
    {"id": "timbering", "name": "drift timbering", "base_y": 16, "kind": "made", "part_of": "timbering",
     "shapes": TIMBERING,
     "groups": [{"id": "timbering", "name": "drift timbering", "mirrors": True,
                 "shapeIds": [shape["id"] for shape in TIMBERING]}]},
]


FINISH = {
    "authors": ["Opus 5.5"],
    "created": "2026-09-27",
    "biome": {"kind": "solid", "id": 4},
    "themes": THEMES,
    "mapTheme": "dale",
    "themeById": {TERRACE: "green"},
    "shapePropsById": {TERRACE: {"relief_scope": "exclude"}},
    "relief": {"team": TEAM_RELIEF, "neutral": HOLM_RELIEF},
    "addShapes": ADD_SHAPES,
    "addLayers": ADD_LAYERS + MADE_LAYERS,
    "editShapes": EDIT_SHAPES,
    "roomStyles": {"wool": WORKS, "spawn": WORKS},
    "dressing": DRESSING,
}


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(PLAN, handle, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w") as handle:
        json.dump(FINISH, handle, indent=1)
    print(f"wrote {SLUG}.plan.json ({len(PIECES)} pieces) and {SLUG}.refinement.json")


if __name__ == "__main__":
    main()
