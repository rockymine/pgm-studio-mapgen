#!/usr/bin/env python3
"""Quiverstone Mesa — the plan and the finish.

A DTM board on a badlands shelf: two hardened-clay buttes standing over a dry wash, the monument on
the open pan between them, and one sandstone reef in the middle that both sides bridge to.

    python3 specs/opus5-quiverstone/build-spec.py

writes `opus5-quiverstone.plan.json` and `opus5-quiverstone.finish.json` beside itself.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-quiverstone"

CELL = 5
SURFACE = 16

# ── blocks ──────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE, PLANKS = 1, 2, 3, 4, 5
SAND, GRAVEL, SANDSTONE = 12, 13, 24
LOG, LEAVES, LOG2, LEAVES2 = 17, 18, 162, 161
DEAD_BUSH, RED_SAND_DATA = 32, 1
HARDENED_CLAY, STAINED_CLAY = 172, 159
RED_SANDSTONE = 179
STONE_SLAB, WOOD_SLAB = 44, 126
GLASS_PANE, BIRCH_STAIRS, ACACIA_STAIRS = 102, 135, 163
BRICK = 45
ACACIA, BIRCH = 4, 2                            # plank/slab variants
LOG2_ACACIA = 0
SMOOTH_SANDSTONE, CHISELLED_SANDSTONE = 2, 1    # sandstone data
# the stained-clay dye nibbles a badlands wants
ORANGE, WHITE, LIGHT_GRAY, BROWN, RED, YELLOW, GRAY = 1, 0, 8, 12, 14, 4, 7
COARSE_DIRT, PODZOL = 1, 2
ANDESITE_DATA = 5


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


def layered(stack, axis="depth", beyond=None):
    material = {"kind": "layered", "stack": stack, "axis": axis}
    if beyond is not None:
        material["beyond"] = beyond
    return material


def bands(*pairs, ending="handOver"):
    return {"bands": [{"material": material, "thickness": thickness} for material, thickness in pairs],
            "ending": ending}


def top(material, depth):
    return {"enabled": True, "depth": depth, "material": material}


def off(material):
    return {"enabled": False, "depth": 1, "material": material}


# ── geometry (authoring, not measuring) ─────────────────────────────────────────
def lobed_ring(cx, cz, rx, rz, points, wobble, rng):
    ring = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        pull = 1 + rng.uniform(-wobble, wobble)
        ring.append([round(cx + math.cos(angle) * rx * pull, 1),
                     round(cz + math.sin(angle) * rz * pull, 1)])
    return ring


def lobed_box(min_x, min_z, max_x, max_z, per_side, wobble, rng):
    """A ring that covers the band it states. An ellipse over the same box covers less than half of
    it, which is where a building drawn at the pad's own corner finds unpinned ground beside it."""
    corner = min(4.0, (max_x - min_x) / 6, (max_z - min_z) / 6)
    ring, cx, cz = [], (min_x + max_x) / 2, (min_z + max_z) / 2

    def edge(x0, z0, x1, z1):
        for step in range(per_side):
            t = step / per_side
            pull = rng.uniform(0, wobble)
            x, z = x0 + (x1 - x0) * t, z0 + (z1 - z0) * t
            ring.append([round(x + (cx - x) * pull, 1), round(z + (cz - z) * pull, 1)])

    edge(min_x + corner, min_z, max_x - corner, min_z)
    edge(max_x, min_z + corner, max_x, max_z - corner)
    edge(max_x - corner, max_z, min_x + corner, max_z)
    edge(min_x, max_z - corner, min_x, min_z + corner)
    return ring


def negate(ring):
    return [[-x, -z] for x, z in ring]


SHELF_BOX = (-72, -100, 72, -38)
REEF_BOX = (-52, -18, 52, 18)


def inside(ring, box, margin):
    min_x, min_z, max_x, max_z = box
    return [[min(max(x, min_x + margin), max_x - margin),
             min(max(z, min_z + margin), max_z - margin)] for x, z in ring]


def on_shelf(ring, margin=10):
    return inside(ring, SHELF_BOX, margin)


def on_reef(ring, margin=9):
    return inside(ring, REEF_BOX, margin)


# ── the copied props ────────────────────────────────────────────────────────────
def acacia_body(rng, trunk, lean, radius):
    """An acacia: a leaning trunk, a flat umbrella crown, and a dead bush or two at its foot.

    The template species already builds one; this is authored because the request's board wants dead
    bushes and stripped branches, and a copied body is the one recipe that writes a block that is
    neither wood nor leaf.
    """
    cells = {}
    x = 0
    for y in range(trunk):
        if y >= trunk - lean and (y - (trunk - lean)) % 2 == 0:
            x += 1
        cells[(x, y, 0)] = (LOG2, LOG2_ACACIA)
    top_y, top_x = trunk, x
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            if abs(dx) + abs(dz) > radius + 1:
                continue
            cells.setdefault((top_x + dx, top_y, dz), (LEAVES2, 0))
            if abs(dx) + abs(dz) <= radius - 1:
                cells.setdefault((top_x + dx, top_y - 1, dz), (LEAVES2, 0))
    # one bare limb, which is what separates a badlands acacia from a park tree
    limb = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    for step in range(1, 3):
        cells.setdefault((top_x + limb[0] * step, top_y - 2, limb[1] * step), (LOG2, LOG2_ACACIA | 4))
    for spot in rng.sample([(2, 1), (-2, 1), (1, -2), (-1, 2), (2, -2)], 2):
        cells.setdefault((spot[0], 0, spot[1]), (DEAD_BUSH, 0))
    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def bonepile_body(rng):
    """A cairn of stripped acacia laid on the pan — the badlands' answer to a log pile."""
    cells = {}
    length = rng.randint(4, 6)
    for i in range(length):
        cells[(i, 0, 0)] = (LOG2, LOG2_ACACIA | 4)
        if i < length - 1:
            cells[(i, 0, 1)] = (LOG2, LOG2_ACACIA | 4)
    for i in range(1, length - 1):
        cells[(i, 1, 0)] = (LOG2, LOG2_ACACIA | 4)
    cells[(2, 1, 1)] = (LOG2, LOG2_ACACIA | 8)
    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def clump_body(spots, block, data=0):
    return [[x, 0, z, block, data] for x, z in spots]


# ══════════════════════════════════════════════════════════════════════════════
# THE PLAN
# ══════════════════════════════════════════════════════════════════════════════
#   shelf     x -72..72   z -100..-38   the team shelf, 144 x 62
#   camp      x -10..10   z -100..-80   the spawn piece inside its back
#   reef      x -52..52   z  -18..18    the one mid landmass, on the axis
#   wash      x -60..60   z  -38..-18   the build zone over the dry wash
#
#   spawn marker (0, -90) · monuments (-24, -54) and (24, -54)
PLAN = {
    "plan": 2,
    "meta": {"name": "Quiverstone Mesa",
             "notes": "DTM. Two monuments a team on the open pan, buttes either side of the spawn."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": SURFACE, "observerY": 60},
    "pieces": [
        {"id": "shelf", "role": "piece", "rect": [-14, -20, 28, 12], "surface": SURFACE},
        {"id": "camp", "role": "spawn", "rect": [-2, -20, 4, 4], "surface": SURFACE},
        {"id": "reef", "role": "piece", "rect": [-10, -4, 20, 8], "surface": SURFACE,
         "mirrors": False},
    ],
    "zones": [
        {"id": "wash", "rect": [-12, -8, 24, 4], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "camp", "at": [10, 10], "facing": "back",
                    "footprint": [5, 5, 10, 10]}],
        "wools": [],
        "iron": [],
        # a west and an east rather than one on the axis: a single central goal puts every journey
        # down x 0 and leaves both flanks off every route
        "destroyables": [
            {"id": "mon-w", "piece": "", "at": [-24, -54], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "Quiverstone"},
            {"id": "mon-e", "piece": "", "at": [24, -54], "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "Redscar"},
        ],
        "cores": [],
    },
    "walls": [],
    "boxes": [],
}


# ══════════════════════════════════════════════════════════════════════════════
# THE FINISH
# ══════════════════════════════════════════════════════════════════════════════

# ── themes ──────────────────────────────────────────────────────────────────────
# Four grounds and one made thing. The rock under all of them is one rock, so the wall and fill
# buckets are shared — what differs is the two courses on top.
PAN_WALL = layered(bands(
    (noise(601, 5, [solid(SANDSTONE), solid(SANDSTONE, SMOOTH_SANDSTONE)]), 2),
    (solid(STAINED_CLAY, ORANGE), 2),
    (solid(HARDENED_CLAY), 3),
    (solid(STAINED_CLAY, BROWN), 2),
    (solid(HARDENED_CLAY), 4),
    (solid(STAINED_CLAY, LIGHT_GRAY), 2),
    (noise(602, 6, [solid(STONE), solid(STONE, ANDESITE_DATA)]), 6),
), beyond=solid(STONE))

PAN_FILL = cell_patches(603, 9, 45, 1, [
    turbulence(611, 7, [solid(HARDENED_CLAY), solid(STAINED_CLAY, ORANGE)], rise=5),
    turbulence(612, 7, [solid(STONE), solid(STONE, ANDESITE_DATA)], rise=5),
], rise=5)

PAN_RIM = cell_patches(604, 7, 50, 1, [solid(SANDSTONE), solid(SAND)])

# the pan's own dust: sand with the two accents the request asked of the swamp's turf, in badlands
# colours — a fractal field's end stops are its accents, so gravel and red sand come out as specks
PAN_DUST = noise(605, 12, [
    solid(GRAVEL),
    solid(SAND), solid(SAND), solid(SAND), solid(SAND), solid(SAND),
    solid(STAINED_CLAY, ORANGE),
])


def pan_theme(surface_material, rim=True, depth=4):
    return {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": False,
        "surface": top(layered(bands(
            (surface_material, 1),
            (noise(606, 6, [solid(SANDSTONE), solid(SANDSTONE, SMOOTH_SANDSTONE)], rise=8), depth - 1),
        )), depth),
        "wall": PAN_WALL,
        "wallEnabled": True,
        "fill": PAN_FILL,
        "rim": top(PAN_RIM, 1) if rim else off(PAN_RIM),
        "rimEdges": "void",
    }


THEMES = {
    # the pan — the map's default ground
    "pan": pan_theme(PAN_DUST),
    # the slopes off the buttes: red sand and clay where the strata have weathered out
    "scree": pan_theme(cell_patches(607, 8, 55, 2, [
        solid(SAND, RED_SAND_DATA), solid(STAINED_CLAY, ORANGE),
        solid(SAND, RED_SAND_DATA), solid(GRAVEL), solid(SAND, RED_SAND_DATA)])),
    # the butte itself: the strata run the whole face, so the stack is in surface AND wall AND fill
    "butte": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(cell_patches(608, 7, 50, 1, [
            solid(STAINED_CLAY, ORANGE), solid(HARDENED_CLAY), solid(STAINED_CLAY, BROWN)]), 2),
        "wall": PAN_WALL,
        "wallEnabled": True,
        "fill": PAN_WALL,
        "rim": off(PAN_RIM),
        "rimEdges": "void",
    },
    # the caliche flats a monument stands on: pale, hard and bare, so the goal reads against it
    "caliche": pan_theme(cell_patches(609, 6, 50, 1, [
        solid(STAINED_CLAY, WHITE), solid(STAINED_CLAY, LIGHT_GRAY), solid(SANDSTONE, SMOOTH_SANDSTONE)])),
    # the wash floor: what a river left when it stopped running
    "wash": pan_theme(cell_patches(610, 6, 55, 1, [solid(GRAVEL), solid(SAND), solid(GRAVEL)])),
}


# ── relief ──────────────────────────────────────────────────────────────────────
# The marks pin only ground a player walks; the buttes are erected shapes standing out of the solve
# and the flanks carry pushes. A mark on every region is a table with bumps on it.
mark_rng = random.Random(8121)

#   camppad  x -30..30  z -100..-74  h 20  the spawn shelf, the pueblos and the assay offices
#   pan      x -34..34  z  -70..-40  h 16  the level caliche the two monuments stand on
CAMPPAD = lobed_box(-30, -100, 30, -74, 6, 0.02, mark_rng)
PANFLAT = lobed_box(-34, -70, 34, -40, 6, 0.02, mark_rng)

TEAM_MARKS = [
    {"id": "rimrock", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "camppad", "kind": "area", "ring": CAMPPAD, "h": 20},
    {"id": "panflat", "kind": "area", "ring": PANFLAT, "h": SURFACE},
    # the three ways down off the camp, pinned so the tracks laid on them step by one
    {"id": "track-w", "kind": "line",
     "points": [[-8, -78], [-18, -74], [-24, -68], [-24, -62], [-24, -58]],
     "h": [20, 19, 18, 17, 16], "r": 5},
    {"id": "track-e", "kind": "line",
     "points": [[8, -78], [18, -74], [24, -68], [24, -62], [24, -58]],
     "h": [20, 19, 18, 17, 16], "r": 5},
    {"id": "track-mid", "kind": "line",
     "points": [[0, -78], [0, -76], [0, -74], [0, -72], [0, -68]],
     "h": [20, 19, 18, 17, 16], "r": 4},
]

TEAM_PUSHES = [
    # the two shoulders the buttes stand on: a raise measures from the median ground under its own
    # footprint, so the pad under a butte is what decides how tall its face reads
    {"id": "shoulder-w", "ring": lobed_ring(-52, -86, 14, 12, 11, 0.16, mark_rng),
     "amounts": [9, 12, 11, 9, 8, 9, 11, 12, 10, 9, 8], "falloff": 9,
     "roughness": 0.35, "crown": 5, "seed": 41},
    {"id": "shoulder-e", "ring": lobed_ring(52, -86, 14, 12, 11, 0.16, mark_rng),
     "amounts": [8, 11, 12, 10, 8, 9, 12, 11, 9, 8, 9], "falloff": 9,
     "roughness": 0.35, "crown": 5, "seed": 42},
    # the rough edges: the flanks forward of the shoulders
    {"id": "edge-w", "ring": lobed_ring(-58, -54, 10, 13, 11, 0.18, mark_rng),
     "amounts": [8, 11, 12, 10, 8, 9, 11, 12, 10, 9, 8], "falloff": 10,
     "roughness": 0.50, "crown": 7, "seed": 43},
    {"id": "edge-e", "ring": lobed_ring(58, -54, 10, 13, 11, 0.18, mark_rng),
     "amounts": [9, 10, 12, 11, 9, 8, 10, 12, 11, 9, 9], "falloff": 10,
     "roughness": 0.50, "crown": 7, "seed": 44},
    # the wash: a dished channel across the pan's own front, which is the depression a destroy board
    # takes instead of a hole cut in a team's own ground
    {"id": "wash-dip", "ring": lobed_ring(0, -46, 26, 5, 13, 0.10, mark_rng),
     "amount": 0, "falloff": 9, "roughness": 0.35, "crown": -3, "seed": 45},
]

REEF_FLAT = lobed_box(-46, -14, 46, 14, 6, 0.02, mark_rng)

MID_MARKS = [
    {"id": "reef-rim", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "reef-flat", "kind": "area", "ring": REEF_FLAT, "h": 17},
]
MID_PUSHES = []

RELIEF = {
    "team": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "rolling",
             "grain": {"amplitude": 1, "scale": 10, "seed": 51},
             "marks": TEAM_MARKS, "pushes": TEAM_PUSHES},
    "neutral": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "plain",
                "grain": {"amplitude": 1, "scale": 12, "seed": 52},
                "marks": MID_MARKS, "pushes": MID_PUSHES},
}


# ── the shapes the paint and the buttes are stated on ───────────────────────────
patch_rng = random.Random(6262)


def patch(shape_id, ring, theme):
    """A splotch: an ordinary one-course add, so the taller add keeps the height and the smallest
    shape keeps the colour."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
            "vertices": ring, "theme": theme}


def butte(shape_id, cx, cz, rx, rz, lift, rng):
    """A butte: an erected shape standing out of the relief, sheer on every side.

    `skirt: 0` is a cut face and `relief_scope: exclude` keeps its ground out of the solve, so the
    stated top is the top that builds. Its theme's strata go in `surface`, `wall` AND `fill`, because
    the surface bucket is only the top courses and the face is the whole point.
    """
    return {"id": shape_id, "type": "polygon", "operation": "add", "override": True,
            "floor": 0, "base_height": lift, "height_mode": "raise", "skirt": 0,
            "relief_scope": "exclude", "theme": "butte",
            "vertices": lobed_ring(cx, cz, rx, rz, 11, 0.12, rng)}


ADD_SHAPES = [
    # the two buttes, on the shoulders behind the camp. Sixteen over the shoulder and not thirty:
    # the build ceiling is the tallest terrain column plus twenty, and an erected shape is terrain,
    # so a tall butte hands the whole board a ceiling it did not want.
    butte("butte-w", -52, -86, 13, 11, 16, patch_rng),
    butte("butte-e", 52, -86, 13, 11, 16, patch_rng),
    # scree round each butte's foot, and a tongue of it pulled out over the shoulder so the rock
    # shows through the dust rather than stopping dead at the shape's own outline
    patch("scree-w", on_shelf(lobed_ring(-52, -86, 22, 19, 13, 0.14, patch_rng)), "scree"),
    patch("scree-e", on_shelf(lobed_ring(52, -86, 22, 19, 13, 0.14, patch_rng)), "scree"),
    patch("scree-edge-w", on_shelf(lobed_ring(-58, -54, 15, 18, 13, 0.16, patch_rng)), "scree"),
    patch("scree-edge-e", on_shelf(lobed_ring(58, -54, 15, 18, 13, 0.16, patch_rng)), "scree"),
    # the caliche the two monuments stand on: one patch a goal, so each reads against pale ground
    patch("caliche-w", on_shelf(lobed_ring(-24, -54, 15, 12, 11, 0.12, patch_rng)), "caliche"),
    patch("caliche-e", on_shelf(lobed_ring(24, -54, 15, 12, 11, 0.12, patch_rng)), "caliche"),
    # the wash floor, on the dish the push cut
    patch("wash-floor", on_shelf(lobed_ring(0, -46, 28, 6, 13, 0.10, patch_rng)), "wash"),
]


# ── the sky: the mesa's own hoodoos, standing free over the wash ────────────────
def hoodoo(name, cx, cz, seed):
    """A pinnacle standing on the pan — three made slabs narrowing upward, seated on the ground.

    A made layer is out of the stacking rules and out of the build ceiling, which is exactly what a
    twenty-course rock beside a monument has to be: an erected terrain shape of the same height would
    hand the whole board a ceiling twenty blocks over its own top. `seat` settles the three slabs
    onto the terrain as one thing, and `part_of` is what makes them one thing. What a made layer is
    *not* out of is the projective reads — `walk`, `slopes` and `heightmap` take the topmost solid
    block — so these stand where no route runs.
    """
    rng = random.Random(seed)
    tiers = [(0, 7, [(0, 0, 6), (-4, 2, 4), (4, -2, 4)]),
             (7, 7, [(0, 1, 5), (-3, 1, 3)]),
             (14, 6, [(0, 0, 4), (2, 2, 3)])]
    layers = []
    for tier, (floor_y, thickness, lobes) in enumerate(tiers):
        shapes = [{
            "id": f"{name}-{tier}-{index}", "type": "circle", "operation": "add",
            "center_x": cx + dx + rng.randint(-1, 1), "center_z": cz + dz + rng.randint(-1, 1),
            "radius": radius, "floor": 0, "base_height": thickness,
            "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "theme": "butte",
        } for index, (dx, dz, radius) in enumerate(lobes)]
        layers.append({
            "id": f"{name}-{tier}", "name": f"{name} tier {tier}", "base_y": floor_y,
            "kind": "made", "part_of": name, "seat": "ground", "shapes": shapes,
            "groups": [{"id": f"{name}-{tier}-g", "name": name, "mirrors": True,
                        "shapeIds": [shape["id"] for shape in shapes]}],
        })
    return layers


ADD_LAYERS = (hoodoo("stack-w", -66, -62, 71)
              + hoodoo("stack-e", -30, -74, 72)
              + hoodoo("stack-reef", -6, 12, 73))


# ── house styles ────────────────────────────────────────────────────────────────
def dwelling_style():
    """A pueblo: sandstone courses under a flat clay lid, acacia beams out past the corners."""
    return {
        "foundation": {
            "plate": {"stack": bands((solid(SANDSTONE, SMOOTH_SANDSTONE), 1),
                                     (solid(SANDSTONE), 1)), "extent": 2},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(SANDSTONE),
        },
        "roof": {
            # flat, because a pueblo has no pitch and the request's board wants a badlands silhouette
            "form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": False, "hole": True,
            "body": solid(STAINED_CLAY, ORANGE),
            "verge": {"kind": "laidLog", "id": LOG2, "data": LOG2_ACACIA},
            "gable": solid(STAINED_CLAY, ORANGE),
            "gableWindows": {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 2, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": {"stack": bands((solid(SANDSTONE), 2),
                                (noise(621, 4, [solid(SANDSTONE, SMOOTH_SANDSTONE),
                                                solid(STAINED_CLAY, ORANGE)]), 4)),
                 "extent": 6},
        "post": solid(LOG2, LOG2_ACACIA),
        "windows": {"form": "pane", "block": STAINED_CLAY, "hostBlock": -1, "hostData": 0,
                    "data": BROWN, "sill": 3, "width": 1, "height": 1, "spacing": 3},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": LOG2, "data": LOG2_ACACIA, "reach": 1, "any": True},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": ACACIA_STAIRS, "fill": "upperSlab",
                             "fillBlock": WOOD_SLAB, "fillData": ACACIA},
                    "width": 2, "height": 3},
    }


def assay_style():
    """The two-storey assay office: sandstone below, acacia boarding above, a shallow slab roof."""
    boarded = {"stack": bands((solid(PLANKS, ACACIA), 2),
                              (noise(622, 5, [solid(PLANKS, ACACIA),
                                              solid(SANDSTONE, SMOOTH_SANDSTONE)]), 2)),
               "extent": 4}
    return {
        "foundation": {
            "plate": {"stack": bands((solid(SANDSTONE), 1), (solid(SANDSTONE, SMOOTH_SANDSTONE), 1),
                                     (solid(SANDSTONE), 1)), "extent": 3},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(SANDSTONE, CHISELLED_SANDSTONE),
        },
        "roof": {
            "form": "gable", "pitch": 1, "slab": WOOD_SLAB, "slabData": ACACIA, "overhang": 1,
            "ridgeCap": True, "hole": False,
            "body": solid(PLANKS, ACACIA),
            "verge": {"kind": "laidLog", "id": LOG2, "data": LOG2_ACACIA},
            "gable": solid(SANDSTONE, SMOOTH_SANDSTONE),
            "gableWindows": {"form": "open", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": boarded,
        "post": solid(LOG2, LOG2_ACACIA),
        "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 1, "height": 2, "spacing": 2},
        "storeys": [
            {"clear": 3, "wall": {"stack": bands((solid(SANDSTONE), 2),
                                                 (solid(SANDSTONE, SMOOTH_SANDSTONE), 2)),
                                  "extent": 4},
             "post": solid(LOG2, LOG2_ACACIA),
             "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 2, "width": 1, "height": 2, "spacing": 3},
             "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                         "inlayInset": 2, "isPlain": True},
             "deck": None, "headroom": 3},
            {"clear": 3, "wall": boarded,
             "post": solid(LOG2, LOG2_ACACIA),
             "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 1, "width": 1, "height": 2, "spacing": 2},
             "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                         "inlayInset": 2, "isPlain": True},
             "deck": solid(PLANKS, ACACIA), "headroom": 3},
        ],
        "porch": None,
        "front": None,
        "beams": {"block": LOG2, "data": LOG2_ACACIA, "reach": 1, "any": True},
        "doorway": {"door": "air",
                    "head": {"form": "none", "block": ACACIA_STAIRS, "fill": "upperSlab",
                             "fillBlock": WOOD_SLAB, "fillData": ACACIA},
                    "width": 2, "height": 3},
    }


def shrine_style():
    """A tiny wayside shrine: a chiselled-sandstone box under a stepped clay lid, one 1x1 window."""
    return {
        "foundation": {
            "plate": {"stack": bands((solid(SANDSTONE), 1), (solid(SANDSTONE, SMOOTH_SANDSTONE), 1)),
                      "extent": 2},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(SANDSTONE),
        },
        "roof": {
            "form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": True, "hole": False,
            "body": solid(STAINED_CLAY, BROWN),
            "verge": solid(STAINED_CLAY, ORANGE),
            "gable": solid(SANDSTONE, CHISELLED_SANDSTONE),
            "gableWindows": {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": {"stack": bands((noise(623, 3, [solid(SANDSTONE, CHISELLED_SANDSTONE),
                                                solid(SANDSTONE), solid(SANDSTONE),
                                                solid(STAINED_CLAY, WHITE)], octaves=2), 5)),
                 "extent": 5},
        "post": None,
        "windows": {"form": "pane", "block": STAINED_CLAY, "hostBlock": -1, "hostData": 0,
                    "data": WHITE, "sill": 2, "width": 1, "height": 1, "spacing": 2},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "none", "block": BIRCH_STAIRS, "fill": "upperSlab",
                             "fillBlock": WOOD_SLAB, "fillData": BIRCH},
                    "width": 2, "height": 3},
    }


# ── the dressing ────────────────────────────────────────────────────────────────
tree_rng = random.Random(7311)

STYLES = {}
for index in range(4):
    STYLES[f"quiver-acacia-{index + 1}"] = {
        "kind": "tree", "form": "copied",
        "body": acacia_body(tree_rng, trunk=tree_rng.randint(5, 7), lean=tree_rng.randint(2, 4),
                            radius=tree_rng.randint(3, 4)),
    }
STYLES["quiver-birch"] = {"kind": "tree", "form": "template", "species": "birch", "height": 8}
for index in range(3):
    STYLES[f"bonepile-{index + 1}"] = {
        "kind": "tree", "form": "copied", "body": bonepile_body(tree_rng)}
STYLES["bushbed"] = {"kind": "tree", "form": "copied",
                     "body": clump_body([(0, 0), (2, 1), (1, 3), (3, 2)], DEAD_BUSH)}
STYLES["bushbed-2"] = {"kind": "tree", "form": "copied",
                       "body": clump_body([(0, 0), (2, 2), (3, 0)], DEAD_BUSH)}

ROCK = turbulence(631, 3, [solid(SANDSTONE), solid(HARDENED_CLAY),
                           solid(STAINED_CLAY, ORANGE)], rise=3)
STYLES["erratic"] = {"kind": "boulder", "form": "angular", "size": 5, "mossy": False, "rock": ROCK}
STYLES["waycairn"] = {"kind": "boulder", "form": "cairn", "size": 3, "mossy": False, "rock": ROCK}

STYLES["dwelling"] = {"kind": "house", "shell": dwelling_style()}
STYLES["assay"] = {"kind": "house", "shell": assay_style()}
STYLES["shrine"] = {"kind": "house", "shell": shrine_style()}

# the track: gravel with red sand through it, in three-block patches
TRACK_PAVE = cell_patches(632, 3, 60, 1, [solid(GRAVEL), solid(SAND, RED_SAND_DATA)])

PROPS = []

# the tracks: the camp's door out to the pan, one to each monument, on the corridors the relief
# pinned for them. Every corner is chamfered, because the band follows a Catmull-Rom through the
# drawn line and a spline overshoots the outside of a sharp turn.
PROPS.append({"id": "track-w", "kind": "stroke", "seed": 81, "radius": 2.5, "style": "rough",
              "coverage": 0.85, "route": True, "pave": TRACK_PAVE,
              "points": [[-6, -79], [-13, -76], [-19, -73], [-23, -69], [-24, -65],
                         [-24, -61], [-24, -58], [-25, -50], [-26, -46]]})
PROPS.append({"id": "track-e", "kind": "stroke", "seed": 82, "radius": 2.5, "style": "rough",
              "coverage": 0.85, "route": True, "pave": TRACK_PAVE,
              "points": [[6, -79], [13, -76], [19, -73], [23, -69], [24, -65],
                         [24, -61], [24, -58], [25, -50], [26, -46]]})

# the buildings: three ideas, every one on ground a relief mark pinned level, and two clear columns
# between each pair's stamped extent
PROPS.append({"id": "dwelling-w", "kind": "house", "seed": 841,
              "wings": [{"corners": [[-25, -97], [-17, -92]]}], "front": "posX",
              "style": "dwelling"})
PROPS.append({"id": "dwelling-e", "kind": "house", "seed": 842,
              "wings": [{"corners": [[17, -97], [25, -92]]}], "front": "negX",
              "style": "dwelling"})
PROPS.append({"id": "assay-w", "kind": "house", "seed": 843,
              "wings": [{"corners": [[-24, -87], [-13, -82]]}], "front": "posZ",
              "style": "assay"})
PROPS.append({"id": "assay-e", "kind": "house", "seed": 844,
              "wings": [{"corners": [[13, -87], [24, -82]]}], "front": "posZ",
              "style": "assay"})
# three shrines on the reef, spread so no pair and no image of a pair share ground
PROPS.append({"id": "shrine-w", "kind": "house", "seed": 845,
              "wings": [{"corners": [[-42, -4], [-36, 1]]}], "front": "posX",
              "style": "shrine"})
PROPS.append({"id": "shrine-e", "kind": "house", "seed": 846,
              "wings": [{"corners": [[36, -12], [42, -7]]}], "front": "negX",
              "style": "shrine"})

# the boulders: one on each monument's outer flank, two on the rough edges, a cairn on the shoulder.
# OB19's keep-out is a ten-block square about a marker tested against a prop's whole footprint, and
# a size-5 erratic is fifteen blocks across, so the anchor is not what to reason about.
PROPS.append({"id": "stone-mon-w", "kind": "boulder", "seed": 851, "x": -44, "z": -50,
              "style": "erratic"})
PROPS.append({"id": "stone-mon-e", "kind": "boulder", "seed": 852, "x": 44, "z": -50,
              "style": "erratic"})
PROPS.append({"id": "cairn-shoulder", "kind": "boulder", "seed": 855, "x": -38, "z": -78,
              "style": "waycairn"})

# the acacia, in stands rather than scattered: a grove in the wash where the water used to run, a
# few on each butte's scree, and three on the reef
STAND_WASH = []
STAND_SCREE = [(-60, -68), (-44, -66), (60, -68), (44, -66)]
STAND_REEF = [(-20, -4), (4, -10)]

TREE_STYLES = ["quiver-acacia-1", "quiver-acacia-2", "quiver-acacia-3", "quiver-acacia-4"]
for index, (x, z) in enumerate(STAND_WASH + STAND_SCREE + STAND_REEF):
    PROPS.append({"id": f"tree-{index}", "kind": "tree", "seed": 2000 + index * 7,
                  "x": x, "z": z, "style": TREE_STYLES[index % len(TREE_STYLES)]})
for index, (x, z) in enumerate([(-64, -94), (-52, -100), (60, -96)]):
    PROPS.append({"id": f"birch-{index}", "kind": "tree", "seed": 2300 + index * 11,
                  "x": x, "z": z, "style": "quiver-birch"})

# the bone piles: stripped acacia laid on the pan
PROPS.append({"id": "pile-camp", "kind": "tree", "seed": 861, "x": -34, "z": -94,
              "style": "bonepile-1"})
PROPS.append({"id": "pile-shoulder", "kind": "tree", "seed": 862, "x": -34, "z": -88,
              "style": "bonepile-2"})
PROPS.append({"id": "pile-reef", "kind": "tree", "seed": 863, "x": -16, "z": 8,
              "style": "bonepile-3"})

# the dead-bush beds
PROPS.append({"id": "bush-w", "kind": "tree", "seed": 871, "x": -34, "z": -72,
              "style": "bushbed"})
PROPS.append({"id": "bush-e", "kind": "tree", "seed": 872, "x": 34, "z": -72,
              "style": "bushbed-2"})
PROPS.append({"id": "bush-reef", "kind": "tree", "seed": 873, "x": 10, "z": 4,
              "style": "bushbed"})

# the cover: sparse, and no flowers — a badlands floor is grass in the lee of a rock and nothing else
FLORA = {"coverage": 0.30, "scale": 9, "octaves": 3, "fernShare": 0.15,
         "flowerShare": 0.0, "flowerScale": 16, "tallShare": 0.04}
flora_rng = random.Random(9091)
PROPS.append({"id": "cover-wash", "kind": "flora", "seed": 91, "spec": FLORA,
              "points": on_shelf(lobed_ring(0, -46, 30, 8, 13, 0.10, flora_rng))})
PROPS.append({"id": "cover-scree-w", "kind": "flora", "seed": 92, "spec": FLORA,
              "points": on_shelf(lobed_ring(-50, -76, 24, 20, 13, 0.12, flora_rng))})
PROPS.append({"id": "cover-scree-e", "kind": "flora", "seed": 93, "spec": FLORA,
              "points": on_shelf(lobed_ring(50, -76, 24, 20, 13, 0.12, flora_rng))})
PROPS.append({"id": "cover-reef", "kind": "flora", "seed": 94, "spec": FLORA,
              "points": on_reef(lobed_ring(0, 0, 44, 13, 13, 0.08, flora_rng))})


FINISH = {
    "themeById": {},
    # the coasts drawn rather than ruled: the compile emits the plan's own rectangles, which is the
    # board's shape and not its shoreline. Two blocks of wander is invisible at map scale.
    "bendShapes": {"camp-16": {"k": 0.22, "wander": 6, "step": 12, "seed": 9},
                   "reef-16": {"k": 0.20, "wander": 5, "step": 10, "seed": 11}},
    "addShapes": ADD_SHAPES,
    "addLayers": ADD_LAYERS,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "pan",
    "biome": {"kind": "cell", "seed": 33, "cellSize": 30, "jitter": 45,
              "palette": [37, 2, 37, 2, 35, 37]},
    "roomStyles": {"spawn": dwelling_style()},
    "dressing": {"props": PROPS, "styles": STYLES},
    "authors": ["Opus 5"],
    "created": "2026-09-03",
}


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as handle:
        json.dump(PLAN, handle, indent=1)
        handle.write("\n")
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as handle:
        json.dump(FINISH, handle, indent=1)
        handle.write("\n")
    trees = sum(1 for prop in PROPS if prop["kind"] == "tree")
    print(f"{SLUG}: {len(PLAN['pieces'])} pieces · {len(ADD_SHAPES)} authored shapes · "
          f"{len(ADD_LAYERS)} made layers · {len(THEMES)} themes · "
          f"{len(PROPS)} props ({trees} tree-kind) · {len(STYLES)} recipes")


if __name__ == "__main__":
    main()
