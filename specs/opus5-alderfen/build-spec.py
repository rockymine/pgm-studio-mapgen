#!/usr/bin/env python3
"""Alderfen Holm — the plan and the finish.

A DTC swamp board. Each team's core stands on level bog in front of a hill-backed island, and the
one holm between the two sides is reached over twenty blocks of void.

    python3 specs/opus5-alderfen/build-spec.py

writes `opus5-alderfen.plan.json` and `opus5-alderfen.finish.json` beside itself.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-alderfen"

CELL = 5
SURFACE = 14

# ── blocks ──────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE, PLANKS = 1, 2, 3, 4, 5
SAND, GRAVEL, WATER = 12, 13, 9
LOG, LEAVES, LOG2, LEAVES2 = 17, 18, 162, 161
VINE, BROWN_MUSHROOM = 106, 39
MOSSY_COBBLE, ANDESITE_DATA, POLISHED_ANDESITE_DATA = 48, 5, 6
HARDENED_CLAY, STAINED_CLAY, WOOL = 172, 159, 35
GLASS_PANE, STONE_BRICK = 102, 98
WOOD_SLAB, STONE_SLAB = 126, 44
LIGHT_GRAY = 8
COARSE_DIRT, PODZOL = 1, 2
SPRUCE, JUNGLE, DARK_OAK = 1, 3, 5           # plank/slab variants
LOG_SPRUCE, LOG_JUNGLE = 1, 3                # log id 17 variants
LOG2_DARK_OAK = 1                            # log id 162 variant
LILY_PAD = 111
LOG_AXIS_X, LOG_AXIS_Z = 4, 8                # the two "laid" orientations


def solid(block_id, data=0):
    """A material. `kind` first, always — it is read positionally on an older build."""
    return {"kind": "solid", "id": block_id, "data": data}


def noise(seed, scale, stops, octaves=3, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": stops, "rise": rise}


def turbulence(seed, scale, stops, octaves=3, rise=0):
    return {"kind": "turbulence", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": stops, "rise": rise}


def cell_patches(seed, size, jitter, warp, palette, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": palette, "rise": rise}


def laid_log(block_id, data=0):
    return {"kind": "laidLog", "id": block_id, "data": data}


def bands(*pairs):
    return {"bands": [{"material": material, "thickness": thickness} for material, thickness in pairs],
            "ending": "handOver"}


def top(material, depth):
    return {"enabled": True, "depth": depth, "material": material}


# ── geometry helpers (authoring, not measuring) ─────────────────────────────────
def lobed_ring(cx, cz, rx, rz, points, wobble, rng):
    """A closed ring with lobes rather than a rectangle.

    A four-vertex rectangle used as a relief ring builds a mesa with sheer sides; the same mark on a
    nine- or eleven-vertex lobed ring is indistinguishable from ground.
    """
    ring = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        pull = 1 + rng.uniform(-wobble, wobble)
        ring.append([round(cx + math.cos(angle) * rx * pull, 1),
                     round(cz + math.sin(angle) * rz * pull, 1)])
    return ring


def lobed_box(min_x, min_z, max_x, max_z, per_side, wobble, rng):
    """A closed ring that actually covers the band it states, with lobed sides and rounded corners.

    An ellipse states a box and covers less than half of it: at 0.8 of its own half-width it reaches
    0.6 of its half-depth, so a pad drawn as `lobed_ring` leaves the ends of its own stated band
    unpinned — which is where a building ends up half on a slope. This walks the perimeter instead,
    so every vertex is on the box and the wobble only ever pulls inward.
    """
    corner = min(4.0, (max_x - min_x) / 6, (max_z - min_z) / 6)
    ring = []

    def edge(x0, z0, x1, z1):
        for step in range(per_side):
            t = step / per_side
            pull = rng.uniform(0, wobble)
            x, z = x0 + (x1 - x0) * t, z0 + (z1 - z0) * t
            # inward is toward the box's middle, so a wobble never hangs a pad over the void
            cx, cz = (min_x + max_x) / 2, (min_z + max_z) / 2
            ring.append([round(x + (cx - x) * pull, 1), round(z + (cz - z) * pull, 1)])

    edge(min_x + corner, min_z, max_x - corner, min_z)
    edge(max_x, min_z + corner, max_x, max_z - corner)
    edge(max_x - corner, max_z, min_x + corner, max_z)
    edge(min_x, max_z - corner, min_x, min_z + corner)
    return ring


def negate(ring):
    """The ring's rot_180 image about the origin."""
    return [[-x, -z] for x, z in ring]


# The two landmasses in blocks, and the margin a paint patch is held inside them by. A one-course add
# is the only shape on a cell that has no ground under it, and there it builds a speck of bedrock in
# the void — so every patch ring is pulled inside the coast rather than trusted to land on it.
HOLM_BOX = (-75, -105, 75, -41)
MID_BOX = (-60, -20, 60, 20)


def inside(ring, box, margin=2):
    min_x, min_z, max_x, max_z = box
    return [[min(max(x, min_x + margin), max_x - margin),
             min(max(z, min_z + margin), max_z - margin)] for x, z in ring]


def on_holm(ring, margin=10):
    return inside(ring, HOLM_BOX, margin)


def on_mid(ring, margin=9):
    return inside(ring, MID_BOX, margin)


# ── the copied trees: a small vanilla oak, its vines, and the wood it is cut from ─
def oak_body(rng, trunk, crown_radius, curtains, wood=(LOG, 0), leaf=(LEAVES, 0)):
    """A small vanilla-shaped oak with vine curtains hanging off its crown at different lengths.

    The trunk stands at (0, 0..trunk-1, 0); its foot is what rests on the ground. The crown is the
    vanilla profile — two wide courses with trimmed corners, then two narrow ones. Every vine cell is
    given a face-pair (5 = north|south, 10 = west|east) so the bit naming the leaf it hangs off is
    always set and the pair survives a rot_180 image, which turns no vine data of its own.
    """
    cells = {}
    log_id, log_data = wood
    leaf_id, leaf_data = leaf
    for y in range(trunk):
        cells[(0, y, 0)] = (log_id, log_data)

    courses = [(trunk - 2, crown_radius), (trunk - 1, crown_radius),
               (trunk, crown_radius - 1), (trunk + 1, max(1, crown_radius - 2))]
    for y, radius in courses:
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if abs(dx) == radius and abs(dz) == radius:
                    if radius >= 2 and rng.random() < 0.55:
                        continue                        # vanilla trims a wide course's corners
                    if radius == 1:
                        continue                        # the top course is a plus
                if (dx, y, dz) in cells:
                    continue
                cells[(dx, y, dz)] = (leaf_id, leaf_data)

    # Where a curtain may hang: an outer leaf cell with air beside it on a horizontal face.
    seats = []
    for (dx, y, dz), (block, _) in cells.items():
        if block not in (LEAVES, LEAVES2):
            continue
        for step, data in (((0, 1), 5), ((0, -1), 5), ((1, 0), 10), ((-1, 0), 10)):
            side = (dx + step[0], y, dz + step[1])
            if side not in cells and abs(side[0]) + abs(side[2]) >= crown_radius:
                seats.append((side, data, y))
    seats.sort(key=lambda seat: (seat[2], seat[0]))
    rng.shuffle(seats)

    hung = 0
    for (sx, sy, sz), data, _ in seats:
        if hung >= curtains:
            break
        if (sx, sy, sz) in cells:
            continue
        drop = rng.randint(2, 7)                        # the "different heights" the vines hang to
        column = [(sx, sy - k, sz) for k in range(drop)]
        if any(spot in cells for spot in column) or min(spot[1] for spot in column) < 1:
            continue
        for spot in column:
            cells[spot] = (VINE, data)
        hung += 1

    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def logpile_body(rng, woods):
    """A laid log pile: two or three courses of logs lying across each other.

    Every log carries a laid axis, so the pile reads as timber rather than as posts; the orbit turns
    the axis with the body, which is why a laid log is stated rather than an upright one.
    """
    cells = {}
    length = rng.randint(4, 6)
    rows = [(0, LOG_AXIS_X, [(i, 0) for i in range(length)]),
            (0, LOG_AXIS_X, [(i, 1) for i in range(length)])]
    for _, axis, spots in rows:
        for x, z in spots:
            block, data = woods[rng.randrange(len(woods))]
            cells[(x, 0, z)] = (block, data | axis)
    for x, z in [(i, 0) for i in range(1, length - 1)]:
        block, data = woods[rng.randrange(len(woods))]
        cells[(x, 1, z)] = (block, data | LOG_AXIS_X)
    if length >= 5:
        block, data = woods[rng.randrange(len(woods))]
        cells[(2, 1, 1)] = (block, data | LOG_AXIS_Z)
    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def clump_body(spots, block, data=0):
    """A handful of one-block plants: a mushroom bed, a raft of lily pads."""
    return [[x, 0, z, block, data] for x, z in spots]


# ══════════════════════════════════════════════════════════════════════════════
# THE PLAN
# ══════════════════════════════════════════════════════════════════════════════
#   holm      x -75..75   z -105..-41   the team island, 150 x 65
#   garth     x -10..10   z -105..-86   the spawn piece inside its back
#   holm-mid  x -60..60   z  -20..20    the one mid island, on the axis
#   span      x -65..65   z  -40..-20   the build zone, over the whole width the holm reaches
#
#   spawn marker (0, -95) · cores (-22, -56) and (22, -56) · spawn-to-spawn 190 blocks
PLAN = {
    "plan": 2,
    "meta": {"name": "Alderfen Holm",
             "notes": "DTC. One core a team on level bog; one holm between the sides."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": SURFACE, "observerY": 58},
    "pieces": [
        {"id": "holm", "role": "piece", "rect": [-15, -21, 30, 13], "surface": SURFACE},
        {"id": "garth", "role": "spawn", "rect": [-2, -21, 4, 4], "surface": SURFACE},
        {"id": "holm-mid", "role": "piece", "rect": [-12, -4, 24, 8], "surface": SURFACE,
         "mirrors": False},
    ],
    "zones": [
        {"id": "span", "rect": [-13, -8, 26, 4], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "garth", "at": [10, 10], "facing": "back",
                    "footprint": [5, 5, 10, 10]}],
        "wools": [],
        "iron": [],
        "destroyables": [],
        # two cores, a west and an east rather than one on the axis: a single central goal on a
        # 150-wide board puts every journey down x 0 and leaves both flanks off every route
        # (`plan/flow` read 83% of the ground dead). Fifty blocks apart is GO2's own band.
        "cores": [{"id": "core-w", "piece": "", "at": [-22, -56], "lava": 3, "lavaHeight": 3,
                   "float": 6, "leak": 5},
                  {"id": "core-e", "piece": "", "at": [22, -56], "lava": 3, "lavaHeight": 3,
                   "float": 6, "leak": 5}],
    },
    "walls": [],
    "boxes": [],
}


# ══════════════════════════════════════════════════════════════════════════════
# THE FINISH
# ══════════════════════════════════════════════════════════════════════════════
rng = random.Random(20260902)

# ── themes ──────────────────────────────────────────────────────────────────────
# Five, and each is a place: the bog, the hills over it, the pools in it, the podzol beds under the
# trees, and the sky. The rock under all of them is one rock, so the wall and fill buckets are shared.
FEN_WALL = cell_patches(701, 9, 45, 1, [
    turbulence(711, 7, [solid(STONE), solid(STONE, ANDESITE_DATA)], rise=4),
    turbulence(712, 7, [solid(COBBLE), solid(STONE)], rise=4),
    turbulence(713, 7, [solid(DIRT, COARSE_DIRT), solid(GRAVEL)], rise=4),
], rise=5)

FEN_FILL = cell_patches(702, 9, 45, 1, [
    turbulence(714, 7, [solid(STONE), solid(STONE, ANDESITE_DATA)], rise=5),
    turbulence(715, 7, [solid(STONE, ANDESITE_DATA), solid(STONE)], rise=5),
], rise=5)

FEN_RIM = cell_patches(703, 7, 50, 1, [solid(SAND), solid(GRAVEL)])

# The bog's own turf: a fractal field whose ends are the accents, so podzol and dirt come out as the
# few specks the author asked for and grass is the body.
BOG_TURF = noise(704, 12, [
    solid(DIRT, PODZOL),
    solid(GRASS), solid(GRASS), solid(GRASS), solid(GRASS), solid(GRASS),
    solid(DIRT),
])

# Three courses of earth under it, with a rise, so a column's soil is one material and the mix reads
# across the ground rather than down a cut.
BOG_EARTH = noise(705, 6, [solid(DIRT), solid(DIRT, COARSE_DIRT)], rise=8)


def fen_theme(surface_material, rim=True, surface_depth=4):
    return {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": False,
        "surface": top({"kind": "layered", "axis": "depth",
                        "stack": bands((surface_material, 1), (BOG_EARTH, surface_depth - 1))},
                       surface_depth),
        "wall": FEN_WALL,
        "wallEnabled": True,
        "fill": FEN_FILL,
        "rim": top(FEN_RIM, 1) if rim else {"enabled": False, "depth": 1, "material": FEN_RIM},
        "rimEdges": "void",
    }


THEMES = {
    # the bog — the map's default ground
    "bog": fen_theme(BOG_TURF),
    # the hills: dirt and grass mixed, in eight-block patches rather than a field
    "brae": fen_theme(cell_patches(706, 8, 55, 2, [
        solid(GRASS), solid(DIRT), solid(GRASS), solid(DIRT, COARSE_DIRT), solid(GRASS)])),
    # the bog pools: one course of standing water over the earth, flush in its own pan
    "marsh": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": False,
        "surface": top({"kind": "layered", "axis": "depth",
                        "stack": bands((solid(WATER), 1),
                                       (noise(707, 6, [solid(DIRT, COARSE_DIRT), solid(SAND)], rise=8), 3))},
                       4),
        "wall": FEN_WALL,
        "wallEnabled": True,
        "fill": FEN_FILL,
        "rim": {"enabled": False, "depth": 1, "material": FEN_RIM},
        "rimEdges": "void",
    },
    # the strand round a bog pool: sand, and gravel where the water has worked it
    "strand": fen_theme(cell_patches(711, 6, 50, 1, [solid(SAND), solid(SAND), solid(GRAVEL)])),
    # the beds under the tree stands: podzol, which is the one footing a mushroom keeps in daylight
    "fenbed": fen_theme(noise(708, 7, [
        solid(DIRT), solid(DIRT, PODZOL), solid(DIRT, PODZOL), solid(DIRT, PODZOL), solid(DIRT, COARSE_DIRT)])),
    # the sky
    "cloud": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(noise(709, 9, [solid(WOOL, 0), solid(WOOL, 0), solid(STAINED_CLAY, 0)]), 3),
        "wall": noise(710, 9, [solid(WOOL, 0), solid(WOOL, 0), solid(STAINED_CLAY, 0)]),
        "wallEnabled": True,
        "fill": solid(WOOL, 0),
        "rim": {"enabled": False, "depth": 1, "material": solid(WOOL, 0)},
        "rimEdges": "void",
    },
}


# ── relief ──────────────────────────────────────────────────────────────────────
# The marks pin only ground a player walks — the spawn pad, the level bog the core stands on, the two
# road corridors and the coast. Everything else is a push, because a push is the only thing that
# builds a landform and a mark on every region is a table with bumps on it.
mark_rng = random.Random(4711)

#   garthpad   x -34..34   z -108..-80   h 18   the spawn shelf, the steading and the two fen houses
#   foreshore  x -36..36   z  -76..-42   h 14   the level bog the two cores stand on
# Four blocks of unpinned ground between them, which is what the solver turns into four one-block
# steps rather than one four-block wall.
GARTHPAD = lobed_box(-34, -108, 34, -80, 5, 0.02, mark_rng)
FORESHORE = lobed_box(-36, -76, 36, -42, 6, 0.02, mark_rng)

TEAM_MARKS = [
    {"id": "coast", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "garthpad", "kind": "area", "ring": GARTHPAD, "h": 18},
    {"id": "foreshore", "kind": "area", "ring": FORESHORE, "h": SURFACE},
    # the three ways down off the spawn shelf, pinned so the roads laid on them step by one
    {"id": "way-w", "kind": "line",
     "points": [[-8, -84], [-20, -78], [-27, -70], [-20, -62], [-10, -56]],
     "h": [18, 17, 16, 15, 14], "r": 5},
    {"id": "way-e", "kind": "line",
     "points": [[8, -84], [20, -78], [27, -70], [20, -62], [10, -56]],
     "h": [18, 17, 16, 15, 14], "r": 5},
    {"id": "way-mid", "kind": "line",
     "points": [[0, -84], [0, -81], [0, -78], [0, -75], [0, -70]],
     "h": [18, 17, 16, 15, 14], "r": 4},
]

TEAM_PUSHES = [
    # the back hills, either side of the spawn shelf: hilly the moment a player is out of the door.
    # Their rings stop nine blocks short of the pad, which is the falloff, so the skirt reaches the
    # pad's own edge at nothing rather than lifting the ground the spawn is measured against.
    {"id": "brae-w", "ring": lobed_ring(-58, -90, 14, 15, 11, 0.16, mark_rng),
     "amounts": [16, 19, 18, 15, 13, 14, 16, 19, 17, 15, 14], "falloff": 9,
     "roughness": 0.40, "crown": 7, "seed": 21},
    {"id": "brae-e", "ring": lobed_ring(58, -90, 14, 15, 11, 0.16, mark_rng),
     "amounts": [15, 18, 19, 16, 14, 13, 15, 18, 19, 16, 14], "falloff": 9,
     "roughness": 0.40, "crown": 7, "seed": 22},
    # the rough edges: the flanks forward of the braes, where the ground is nobody's road
    {"id": "edge-w", "ring": lobed_ring(-62, -56, 10, 14, 11, 0.18, mark_rng),
     "amounts": [10, 13, 14, 12, 10, 11, 13, 14, 12, 11, 10], "falloff": 10,
     "roughness": 0.50, "crown": 8, "seed": 23},
    {"id": "edge-e", "ring": lobed_ring(62, -56, 10, 14, 11, 0.18, mark_rng),
     "amounts": [11, 12, 14, 13, 11, 10, 12, 14, 13, 11, 11], "falloff": 10,
     "roughness": 0.50, "crown": 8, "seed": 24},
]

# The mid holm is the level half of the board, and nothing on it is mirrored for the author: its
# group does not fan, so every mark is stated as an explicit pair about the origin.
HOLM_FLAT = lobed_box(-54, -16, 54, 16, 6, 0.02, mark_rng)
POOL_W = lobed_ring(-30, 4, 7, 6, 9, 0.14, mark_rng)

MID_MARKS = [
    {"id": "holm-coast", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "holm-flat", "kind": "area", "ring": HOLM_FLAT, "h": 15},
]
MID_PUSHES = [
    {"id": "holm-pool-w", "ring": POOL_W, "amount": 0, "falloff": 6,
     "roughness": 0.30, "crown": -4, "seed": 31},
    {"id": "holm-pool-e", "ring": negate(POOL_W), "amount": 0, "falloff": 6,
     "roughness": 0.30, "crown": -4, "seed": 31},
]

RELIEF = {
    "team": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "rolling",
             "grain": {"amplitude": 1, "scale": 9, "seed": 41},
             "marks": TEAM_MARKS, "pushes": TEAM_PUSHES},
    "neutral": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "plain",
                "grain": {"amplitude": 1, "scale": 11, "seed": 42},
                "marks": MID_MARKS, "pushes": MID_PUSHES},
}


# ── the shapes the paint is stated on ───────────────────────────────────────────
# A splotch beats a pattern, and a splotch is a shape: an ordinary one-course add, base_height 1, no
# override, so the taller add keeps the height and the smallest shape keeps the colour.
def patch(shape_id, ring, theme):
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
            "vertices": ring, "theme": theme}


patch_rng = random.Random(5150)

ADD_SHAPES = [
    # the hills wear their own ground: dirt and grass mixed
    patch("brae-w-paint", on_holm(lobed_ring(-56, -88, 22, 17, 13, 0.14, patch_rng)), "brae"),
    patch("brae-e-paint", on_holm(lobed_ring(56, -88, 22, 17, 13, 0.14, patch_rng)), "brae"),
    patch("edge-w-paint", on_holm(lobed_ring(-60, -56, 15, 17, 13, 0.16, patch_rng)), "brae"),
    patch("edge-e-paint", on_holm(lobed_ring(60, -56, 15, 17, 13, 0.16, patch_rng)), "brae"),
    # the bog pools: a course of standing water, level in its own pan, down the middle of the
    # defended line where neither core's ten-block clearance reaches and neither road runs
    patch("strand-mid", on_holm(lobed_ring(0, -62, 13, 7, 11, 0.14, patch_rng)), "strand"),
    patch("marsh-mid", on_holm(lobed_ring(0, -62, 9, 4, 9, 0.16, patch_rng)), "marsh"),
    # the podzol beds beside the tree stands: the one footing a mushroom keeps in daylight
    patch("fenbed-w", on_holm(lobed_ring(-36, -54, 8, 6, 9, 0.18, patch_rng)), "fenbed"),
    patch("fenbed-brae", on_holm(lobed_ring(-34, -84, 8, 6, 9, 0.18, patch_rng)), "fenbed"),
    patch("fenbed-e", on_holm(lobed_ring(50, -46, 8, 6, 9, 0.18, patch_rng)), "fenbed"),
]

# The marsh pans are pinned level and one course under the bog around them, so the water they are
# painted with sits in a lip rather than on a slope.
TEAM_MARKS.append({"id": "marsh-mid-pan", "kind": "area",
                   "ring": ADD_SHAPES[5]["vertices"], "h": SURFACE - 1})


# ── the sky: three cumulus, each three made slabs ───────────────────────────────
def cumulus(name, cx, cz, base_y, seed):
    """A cumulus as three made slabs: a flat base and two narrowing tiers of overlapping lobes.

    A made layer is out of the stacking rules and out of the build ceiling, and its floor is far above
    the bedrock course, so it plates nothing at the bottom of the world. What it is *not* out of is
    the projective reads: `walk`, `slopes` and `heightmap` take the topmost solid block, so a cloud
    stands in every one of them as ground. They are therefore placed over the flanks no route runs
    down, never over the crossing, and `renders/close/` carries a cloud-free control of the three.
    """
    cloud_rng = random.Random(seed)
    tiers = [(base_y, 3, [(0, 0, 8), (-6, 2, 6), (7, -2, 5), (1, 5, 5)]),
             (base_y + 3, 3, [(0, 1, 6), (-5, 2, 4), (5, -1, 4)]),
             (base_y + 6, 3, [(-1, 2, 4), (3, 0, 3)])]
    layers = []
    for tier, (floor_y, thickness, lobes) in enumerate(tiers):
        shapes = []
        for index, (dx, dz, radius) in enumerate(lobes):
            shapes.append({
                "id": f"{name}-{tier}-{index}", "type": "circle", "operation": "add",
                "center_x": cx + dx + cloud_rng.randint(-1, 1),
                "center_z": cz + dz + cloud_rng.randint(-1, 1),
                "radius": radius, "floor": 0, "base_height": thickness,
                "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                "theme": "cloud",
            })
        layers.append({
            "id": f"{name}-{tier}", "name": f"{name} tier {tier}", "base_y": floor_y,
            "kind": "made", "part_of": name,
            "shapes": shapes,
            "groups": [{"id": f"{name}-{tier}-g", "name": name, "mirrors": True,
                        "shapeIds": [shape["id"] for shape in shapes]}],
        })
    return layers


ADD_LAYERS = (cumulus("cloud-brae", -56, -94, 80, 91)
              + cumulus("cloud-edge", -62, -50, 88, 92)
              + cumulus("cloud-holm", 0, 0, 84, 93))


# ── house styles ────────────────────────────────────────────────────────────────
def croft_style():
    """A small croft: two courses of damp stone under spruce boarding, dark oak posts and roof."""
    return {
        "foundation": {
            "plate": {"stack": bands((solid(PLANKS, SPRUCE), 1)), "extent": 2},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(COBBLE),
        },
        "roof": {
            "form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": True, "hole": False,
            "body": solid(PLANKS, DARK_OAK),
            "verge": laid_log(LOG2, LOG2_DARK_OAK),
            "gable": solid(PLANKS, SPRUCE),
            "gableWindows": {"form": "open", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 2, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": {"stack": bands((noise(801, 4, [solid(COBBLE), solid(MOSSY_COBBLE)]), 2),
                                (noise(802, 5, [solid(PLANKS, SPRUCE), solid(PLANKS, SPRUCE),
                                                solid(PLANKS, DARK_OAK)]), 4)),
                 "extent": 6},
        "post": solid(LOG2, LOG2_DARK_OAK),
        "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 3, "width": 1, "height": 2, "spacing": 3},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                             "fillBlock": WOOD_SLAB, "fillData": SPRUCE},
                    "width": 2, "height": 3},
    }


def stilthouse_style():
    """A medium two-storey house standing over the bog on spruce posts, boarded in dark oak.

    Storey 0's wall is the whole idiom — four courses of air between the posts, capped by one laid
    spruce beam — so it is stated rather than repainted, and only the storey over it is boarded.
    """
    boarded = {"stack": bands((solid(PLANKS, DARK_OAK), 2),
                              (noise(803, 5, [solid(PLANKS, DARK_OAK),
                                              solid(PLANKS, SPRUCE)]), 2)),
               "extent": 4}
    return {
        "foundation": {
            # no footing: a footing is the foot of a foundation, and a house on posts has none
            "plate": {"stack": bands((solid(PLANKS, SPRUCE), 1)), "extent": 1},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": None,
        },
        "roof": {
            # a slab roof climbs half a block per block, which is what a twelve-deep hall wants:
            # at a whole course it stands six over its own wall and reads as all roof
            "form": "gable", "pitch": 1, "slab": WOOD_SLAB, "slabData": DARK_OAK, "overhang": 1,
            "ridgeCap": True, "hole": False,
            "body": solid(PLANKS, DARK_OAK),
            "verge": laid_log(LOG, LOG_SPRUCE),
            "gable": solid(PLANKS, SPRUCE),
            "gableWindows": {"form": "open", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": boarded,
        "post": solid(LOG, LOG_SPRUCE),
        "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 1, "height": 2, "spacing": 2},
        "storeys": [
            {"clear": 4,
             "wall": {"stack": bands((solid(0, 0), 4), (laid_log(LOG, LOG_SPRUCE), 1)), "extent": 4},
             "post": solid(LOG, LOG_SPRUCE),
             "windows": {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3},
             "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                         "inlayInset": 2, "isPlain": True},
             "deck": None, "headroom": 4},
            {"clear": 3, "wall": boarded,
             "post": solid(LOG, LOG_SPRUCE),
             "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 1, "width": 1, "height": 2, "spacing": 2},
             "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                         "inlayInset": 2, "isPlain": True},
             "deck": None, "headroom": 3},
        ],
        "porch": None,
        "front": None,
        "beams": {"block": LOG, "data": LOG_SPRUCE, "reach": 1, "any": True},
        "doorway": {"door": "air",
                    "head": {"form": "none", "block": 134, "fill": "upperSlab",
                             "fillBlock": WOOD_SLAB, "fillData": SPRUCE},
                    "width": 2, "height": 3},
    }


def mirehut_style():
    """A tiny hut: a small noise of clay and jungle boarding, a laid-log roof, and one 1x1
    light-grey clay window a wall."""
    return {
        "foundation": {
            "plate": {"stack": bands((solid(COBBLE), 1), (solid(MOSSY_COBBLE), 1)), "extent": 2},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(MOSSY_COBBLE),
        },
        "roof": {
            "form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": True, "hole": False,
            # the laid-log roof: spruce logs lying along the ridge, trimmed with dark oak. A roof's
            # body and verge are each one block (HS3), so the three woods are two here and the third
            # is the log piles' — a cell pattern of laid logs is refused rather than sampled.
            "body": laid_log(LOG, LOG_SPRUCE),
            "verge": laid_log(LOG2, LOG2_DARK_OAK),
            "gable": noise(805, 3, [solid(PLANKS, JUNGLE), solid(HARDENED_CLAY),
                                    solid(HARDENED_CLAY), solid(STAINED_CLAY, LIGHT_GRAY)], octaves=2),
            "gableWindows": {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": {"stack": bands((noise(805, 3, [solid(PLANKS, JUNGLE), solid(HARDENED_CLAY),
                                                solid(HARDENED_CLAY),
                                                solid(STAINED_CLAY, LIGHT_GRAY)], octaves=2), 5)),
                 "extent": 5},
        "post": None,
        "windows": {"form": "pane", "block": STAINED_CLAY, "hostBlock": -1, "hostData": 0,
                    "data": LIGHT_GRAY, "sill": 2, "width": 1, "height": 1, "spacing": 2},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "none", "block": 136, "fill": "upperSlab",
                             "fillBlock": WOOD_SLAB, "fillData": JUNGLE},
                    "width": 2, "height": 3},
    }


# ── the dressing ────────────────────────────────────────────────────────────────
tree_rng = random.Random(9001)

STYLES = {}
for index in range(4):
    STYLES[f"fenoak-{index + 1}"] = {
        "kind": "tree", "form": "copied",
        "body": oak_body(tree_rng, trunk=tree_rng.randint(5, 7), crown_radius=3,
                         curtains=tree_rng.randint(3, 5)),
    }
for index in range(2):
    STYLES[f"fenoak-small-{index + 1}"] = {
        "kind": "tree", "form": "copied",
        "body": oak_body(tree_rng, trunk=4, crown_radius=2, curtains=2),
    }
STYLES["darkfen-1"] = {
    "kind": "tree", "form": "copied",
    "body": oak_body(tree_rng, trunk=6, crown_radius=3, curtains=4,
                     wood=(LOG2, LOG2_DARK_OAK), leaf=(LEAVES2, LOG2_DARK_OAK)),
}
STYLES["sprucefen"] = {"kind": "tree", "form": "template", "species": "spruce", "height": 13}

for index in range(3):
    STYLES[f"logpile-{index + 1}"] = {
        "kind": "tree", "form": "copied",
        "body": logpile_body(tree_rng, [(LOG, 0), (LOG, LOG_SPRUCE), (LOG2, LOG2_DARK_OAK)]),
    }

STYLES["mushbed"] = {"kind": "tree", "form": "copied",
                     "body": clump_body([(0, 0), (2, 1), (1, 3), (3, 2), (-1, 2)], BROWN_MUSHROOM)}
STYLES["mushbed-2"] = {"kind": "tree", "form": "copied",
                       "body": clump_body([(0, 0), (1, 2), (3, 1), (2, 3)], BROWN_MUSHROOM)}
STYLES["lilyraft"] = {"kind": "tree", "form": "copied",
                      "body": clump_body([(0, 0), (2, 1), (1, 3), (3, 0), (4, 2)], LILY_PAD)}
STYLES["lilyraft-2"] = {"kind": "tree", "form": "copied",
                        "body": clump_body([(0, 0), (2, 2), (3, 0)], LILY_PAD)}

BOULDER_ROCK = turbulence(806, 3, [solid(COBBLE), solid(MOSSY_COBBLE),
                                   solid(STONE, ANDESITE_DATA)], rise=3)
STYLES["erratic"] = {"kind": "boulder", "form": "angular", "size": 5, "mossy": True,
                     "rock": BOULDER_ROCK}
STYLES["shelf"] = {"kind": "boulder", "form": "outcrop", "size": 3, "mossy": True,
                   "rock": BOULDER_ROCK}
STYLES["waycairn"] = {"kind": "boulder", "form": "cairn", "size": 3, "mossy": True,
                      "rock": BOULDER_ROCK}

STYLES["croft"] = {"kind": "house", "shell": croft_style()}
STYLES["stilthouse"] = {"kind": "house", "shell": stilthouse_style()}
STYLES["mirehut"] = {"kind": "house", "shell": mirehut_style()}

# The road: coarse dirt with polished andesite laid through it, in three-block patches — two blocks,
# which is a texture, at a brush a player reads as paving rather than as static.
ROAD_PAVE = cell_patches(807, 3, 60, 1, [solid(DIRT, COARSE_DIRT),
                                         solid(STONE, POLISHED_ANDESITE_DATA)])

PROPS = []

# water first: it is the one prop that changes the ground
PROPS.append({
    "id": "holm-pool", "kind": "water", "seed": 62, "shape": "pool", "form": "natural",
    "points": lobed_ring(-30, 4, 5, 4, 9, 0.10, random.Random(62)),
    "radius": 3, "depth": 3, "level": 13, "edge": 0.6, "shore": 2.5, "shoreWander": True,
    "bank": cell_patches(809, 6, 55, 1, [solid(SAND), solid(SAND), solid(GRAVEL)]),
})

# the roads: the spawn door out to the level bog, one to each core, on the corridors the relief
# pinned for them. Every corner is chamfered with two bracketing points, because the band follows a
# Catmull-Rom through the drawn line and a spline overshoots the outside of a sharp turn.
PROPS.append({"id": "road-w", "kind": "stroke", "seed": 71, "radius": 2.5, "style": "rough",
              "coverage": 0.85, "route": True, "pave": ROAD_PAVE,
              "points": [[-6, -84], [-13, -80], [-20, -77], [-25, -72], [-27, -67],
                         [-25, -63], [-23, -60], [-22, -55], [-23, -49], [-25, -45]]})
PROPS.append({"id": "road-e", "kind": "stroke", "seed": 72, "radius": 2.5, "style": "rough",
              "coverage": 0.85, "route": True, "pave": ROAD_PAVE,
              "points": [[6, -84], [13, -80], [20, -77], [25, -72], [27, -67],
                         [25, -63], [23, -60], [22, -55], [23, -49], [25, -45]]})
# The holm carries no road. A lane across forty blocks of holm puts a three-block tree standoff over
# the whole of it, and what the board was asked for is a road from the spawn — which these two are,
# ending at the shore the crossing starts from.

# the buildings: three ideas, and every one on ground a relief mark pinned level. A building seats
# on the lowest column of its own footprint and carves the rest out, so a hillside site is refused
# (DR-SLOPE) — the hills here are rough ground rather than built-on ground.
#   the steading behind the spawn, on the garth pad
PROPS.append({"id": "steading-w", "kind": "house", "seed": 811,
              "wings": [{"corners": [[-27, -103], [-19, -96]]}], "front": "posX",
              "style": "croft"})
PROPS.append({"id": "steading-e", "kind": "house", "seed": 812,
              "wings": [{"corners": [[19, -103], [27, -96]]}], "front": "negX",
              "style": "croft"})
#   the two fen houses on posts, on the pad's wings either side of the spawn hut
PROPS.append({"id": "fenhouse-w", "kind": "house", "seed": 813,
              "wings": [{"corners": [[-28, -92], [-17, -83]]}], "front": "posZ",
              "style": "stilthouse"})
PROPS.append({"id": "fenhouse-e", "kind": "house", "seed": 814,
              "wings": [{"corners": [[17, -92], [28, -83]]}], "front": "posZ",
              "style": "stilthouse"})
#   two tiny huts on the bog behind the cores, where a defender falls back to
PROPS.append({"id": "hut-w", "kind": "house", "seed": 815,
              "wings": [{"corners": [[-46, -4], [-40, 1]]}], "front": "posX",
              "style": "mirehut"})
PROPS.append({"id": "hut-e", "kind": "house", "seed": 816,
              "wings": [{"corners": [[40, -14], [46, -9]]}], "front": "negX",
              "style": "mirehut"})
#   and a third on its east shoulder — three tiny huts and their three images is a hamlet on the
#   contested holm, spread so no pair and no image of a pair share ground
PROPS.append({"id": "hut-holm", "kind": "house", "seed": 817,
              "wings": [{"corners": [[26, 8], [32, 13]]}], "front": "negZ",
              "style": "mirehut"})

# the boulders: cover a defender uses on each core's outer flank, rock showing through the rough
# edges, and a cairn where the two roads part. Every one is kept out of OB19's ten-block square
# about a core's marker and off the roads' own cells.
PROPS.append({"id": "stone-core-w", "kind": "boulder", "seed": 821, "x": -46, "z": -60,
              "style": "erratic"})
PROPS.append({"id": "stone-core-e", "kind": "boulder", "seed": 822, "x": 46, "z": -60,
              "style": "erratic"})
PROPS.append({"id": "stone-edge-w", "kind": "boulder", "seed": 823, "x": -64, "z": -56,
              "style": "shelf"})
PROPS.append({"id": "stone-edge-e", "kind": "boulder", "seed": 824, "x": 62, "z": -70,
              "style": "shelf"})
PROPS.append({"id": "cairn-brae", "kind": "boulder", "seed": 826, "x": -50, "z": -96,
              "style": "waycairn"})
PROPS.append({"id": "stone-holm", "kind": "boulder", "seed": 827, "x": 0, "z": 12,
              "style": "erratic"})

# the trees, in stands rather than scattered: a wood on the west flank between the tarn and the
# rough edge, a copse on the brae behind the spawn, spruce along the two rough edges, and three on
# the holm's shoulders. Every pair stands at least seven blocks apart, which is the crown claim at
# these heights with the variance divided out.
STAND_WEST = [(-58, -76), (-50, -78), (-42, -72), (-60, -62), (-52, -66), (-38, -62),
              (-44, -84), (-56, -88), (-34, -70)]
STAND_BACK = [(-38, -100), (-40, -80), (-58, -82), (-62, -96), (38, -100), (40, -80), (58, -84)]
STAND_EDGE = [(62, -78), (68, -62), (58, -50), (70, -44), (-66, -60), (-70, -74)]
STAND_HOLM = [(-40, -14), (-14, -10), (52, 10)]

TREE_STYLES = ["fenoak-1", "fenoak-2", "fenoak-3", "fenoak-4",
               "fenoak-small-1", "fenoak-small-2", "darkfen-1"]
for index, (x, z) in enumerate(STAND_WEST + STAND_BACK + STAND_HOLM):
    PROPS.append({"id": f"tree-{index}", "kind": "tree", "seed": 1000 + index * 7,
                  "x": x, "z": z, "style": TREE_STYLES[index % len(TREE_STYLES)]})
for index, (x, z) in enumerate(STAND_EDGE):
    PROPS.append({"id": f"fir-{index}", "kind": "tree", "seed": 1300 + index * 11,
                  "x": x, "z": z, "style": "sprucefen"})

# the log piles: firewood beside the steading, beside the west hut, and one in the wood
PROPS.append({"id": "pile-steading", "kind": "tree", "seed": 831, "x": -38, "z": -92,
              "style": "logpile-1"})
PROPS.append({"id": "pile-hut", "kind": "tree", "seed": 832, "x": -12, "z": -72,
              "style": "logpile-2"})
PROPS.append({"id": "pile-wood", "kind": "tree", "seed": 833, "x": -66, "z": -72,
              "style": "logpile-3"})

# the mushroom beds, on the podzol the fen beds were painted with
PROPS.append({"id": "mush-w", "kind": "tree", "seed": 841, "x": -36, "z": -54,
              "style": "mushbed"})
PROPS.append({"id": "mush-brae", "kind": "tree", "seed": 842, "x": -34, "z": -84,
              "style": "mushbed-2"})
PROPS.append({"id": "mush-e", "kind": "tree", "seed": 843, "x": 50, "z": -54,
              "style": "mushbed"})

# the lily pads: on the marsh pans, whose surface is a course of standing water painted as terrain
PROPS.append({"id": "lily-mid", "kind": "tree", "seed": 851, "x": -7, "z": -64,
              "style": "lilyraft"})
PROPS.append({"id": "lily-mid2", "kind": "tree", "seed": 852, "x": 1, "z": -62,
              "style": "lilyraft-2"})
PROPS.append({"id": "lily-far", "kind": "tree", "seed": 853, "x": 5, "z": -60,
              "style": "lilyraft"})
# There is no pad on the tarn. A lily pad is a placement like any other and a water prop claims every
# column of its bed and beach, so one inside the tarn is declined DR-CLAIM: measured twice, at
# (-34, -54) and at (-38, -50). What carries pads instead is the marsh pans above — water painted as
# terrain, which claims nothing.

# the cover: fern-heavy, as a swamp floor is
FLORA = {"coverage": 0.72, "scale": 8, "octaves": 3, "fernShare": 0.55,
         "flowerShare": 0.05, "flowerScale": 16, "tallShare": 0.06}
flora_rng = random.Random(6001)
PROPS.append({"id": "cover-bog", "kind": "flora", "seed": 91, "spec": FLORA,
              "points": on_holm(lobed_ring(0, -56, 36, 18, 13, 0.08, flora_rng))})
PROPS.append({"id": "cover-brae-w", "kind": "flora", "seed": 92, "spec": FLORA,
              "points": on_holm(lobed_ring(-48, -82, 26, 20, 13, 0.12, flora_rng))})
PROPS.append({"id": "cover-brae-e", "kind": "flora", "seed": 93, "spec": FLORA,
              "points": on_holm(lobed_ring(48, -82, 26, 20, 13, 0.12, flora_rng))})
PROPS.append({"id": "cover-garth", "kind": "flora", "seed": 94, "spec": FLORA,
              "points": on_holm(lobed_ring(0, -94, 30, 12, 11, 0.10, flora_rng))})
PROPS.append({"id": "cover-holm", "kind": "flora", "seed": 95, "spec": FLORA,
              "points": on_mid(lobed_ring(0, 0, 50, 15, 13, 0.08, flora_rng))})


FINISH = {
    "themeById": {},
    "bendShapes": {"garth-14": {"k": 0.22, "wander": 6, "step": 12, "seed": 5},
                   "holm-mid-14": {"k": 0.20, "wander": 5, "step": 10, "seed": 6}},
    "addShapes": ADD_SHAPES,
    "addLayers": ADD_LAYERS,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "bog",
    "biome": {"kind": "cell", "seed": 77, "cellSize": 34, "jitter": 45,
              "palette": [6, 6, 37, 6, 37, 6]},
    "roomStyles": {"spawn": croft_style()},
    "dressing": {"props": PROPS, "styles": STYLES},
    "authors": ["Opus 5"],
    "created": "2026-09-02",
}


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(PLAN, handle, indent=1)
        handle.write("\n")
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(FINISH, handle, indent=1)
        handle.write("\n")
    trees = sum(1 for prop in PROPS if prop["kind"] == "tree")
    print(f"{SLUG}: {len(PLAN['pieces'])} pieces · {len(ADD_SHAPES)} paint shapes · "
          f"{len(ADD_LAYERS)} made layers · {len(THEMES)} themes · "
          f"{len(PROPS)} props ({trees} tree-kind) · {len(STYLES)} recipes")
    for key, style in STYLES.items():
        if style.get("form") == "copied":
            print(f"    {key}: {len(style['body'])} cells")


if __name__ == "__main__":
    main()
