#!/usr/bin/env python3
"""Block Realm — the plan and the finish.

A DTC board built the way a side-scrolling platformer draws a level: flat grass with a hard brown
edge, blocky stepped plates instead of hills, warp pipes and floating brick rows as made things, and
two lava-cored keeps a team.

    python3 specs/opus5-blockrealm/build-spec.py

writes `opus5-blockrealm.plan.json` and `opus5-blockrealm.finish.json` beside itself.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-blockrealm"

CELL = 5
SURFACE = 14

# ── blocks ──────────────────────────────────────────────────────────────────────
STONE, GRASS, DIRT, COBBLE, PLANKS = 1, 2, 3, 4, 5
SAND, GRAVEL, SANDSTONE = 12, 13, 24
LOG, LEAVES = 17, 18
BRICK, STONE_BRICK, QUARTZ = 45, 98, 155
HARDENED_CLAY, STAINED_CLAY, WOOL = 172, 159, 35
RED_MUSHROOM_BLOCK, ALL_CAP = 100, 14
GLASS_PANE, OAK_STAIRS, STONE_BRICK_STAIRS = 102, 53, 109
STONE_SLAB, WOOD_SLAB = 44, 126
OAK = 0
# the dye nibbles a platformer palette is stated in
WHITE, ORANGE, MAGENTA, YELLOW, LIME, GREEN, RED, BROWN, LIGHT_BLUE = 0, 1, 2, 4, 5, 13, 14, 12, 3
STONE_BRICK_SLAB, BRICK_SLAB = 5, 4              # stone-slab data nibbles


def solid(block_id, data=0):
    """A material. `kind` first, always — it is read positionally on an older build."""
    return {"kind": "solid", "id": block_id, "data": data}


def noise(seed, scale, stops, octaves=3, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
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
    """A ring that covers the band it states — an ellipse over the same box covers less than half."""
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


FIELD_BOX = (-55, -100, 55, -38)
MIDWAY_BOX = (-40, -18, 40, 18)


def inside(ring, box, margin):
    min_x, min_z, max_x, max_z = box
    return [[min(max(x, min_x + margin), max_x - margin),
             min(max(z, min_z + margin), max_z - margin)] for x, z in ring]


def on_field(ring, margin=10):
    return inside(ring, FIELD_BOX, margin)


def on_midway(ring, margin=9):
    return inside(ring, MIDWAY_BOX, margin)


# ── the copied trees ────────────────────────────────────────────────────────────
def block_tree(rng, trunk, radius, tiers):
    """A platformer tree: a short bare trunk under a flat-topped green disc.

    A template oak grows a blob and a grown oak grows a fractal; neither draws the two flat courses a
    drawn tree has. A copied body is the one recipe that states its own silhouette.
    """
    cells = {}
    for y in range(trunk):
        cells[(0, y, 0)] = (LOG, OAK)
    for tier in range(tiers):
        span = radius - tier
        for dx in range(-span, span + 1):
            for dz in range(-span, span + 1):
                if abs(dx) + abs(dz) > span + 1:
                    continue
                cells.setdefault((dx, trunk + tier, dz), (LEAVES, OAK))
    # two lower leaves either side, so the disc does not read as a plate on a stick
    for dx, dz in ((radius, 0), (-radius, 0), (0, radius), (0, -radius)):
        cells.setdefault((dx, trunk - 1, dz), (LEAVES, OAK))
    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def clump_body(spots, block, data=0):
    return [[x, 0, z, block, data] for x, z in spots]


# ══════════════════════════════════════════════════════════════════════════════
# THE PLAN
# ══════════════════════════════════════════════════════════════════════════════
#   field     x -55..55   z -100..-40   the team's ground, 110 x 60
#   keep      x -10..10   z -100..-80   the spawn piece inside its back
#   midway    x -40..40   z  -20..20    the one mid landmass, on the axis
#   gap       x -50..50   z  -40..-20   the build zone over the pit between them
#
#   spawn marker (0, -90) · cores (-30, -56) and (30, -56)
PLAN = {
    "plan": 2,
    "meta": {"name": "Block Realm",
             "notes": "DTC. Flat ground, blocky stepped plates, warp pipes, two lava keeps a team."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16,
                "surface": SURFACE, "observerY": 62},
    "pieces": [
        {"id": "field", "role": "piece", "rect": [-11, -20, 22, 12], "surface": SURFACE},
        {"id": "keep", "role": "spawn", "rect": [-2, -20, 4, 4], "surface": SURFACE},
        {"id": "midway", "role": "piece", "rect": [-8, -4, 16, 8], "surface": SURFACE,
         "mirrors": False},
    ],
    "zones": [
        {"id": "gap", "rect": [-10, -8, 20, 4], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "keep", "at": [10, 10], "facing": "back",
                    "footprint": [5, 5, 10, 10]}],
        "wools": [],
        "iron": [],
        "destroyables": [],
        # open-topped, so the lava a core is played for shows from across the field
        "cores": [{"id": "core-w", "piece": "", "at": [-30, -56], "lava": 3, "lavaHeight": 3,
                   "openTop": True, "float": 6, "leak": 5},
                  {"id": "core-e", "piece": "", "at": [30, -56], "lava": 3, "lavaHeight": 3,
                   "openTop": True, "float": 6, "leak": 5}],
    },
    "walls": [],
    "boxes": [],
}


# ══════════════════════════════════════════════════════════════════════════════
# THE FINISH
# ══════════════════════════════════════════════════════════════════════════════

# ── themes ──────────────────────────────────────────────────────────────────────
# Six, and the split is the point of the board: ONE is terrain — grass over hardened clay, which is
# what a drawn ground tile is — and the other five are stated colours on made things and on erected
# plates. Stained clay is a shade row rather than a ground, and every use of it here is a thing
# somebody built rather than ground somebody walks on.
TURF_WALL = layered(bands(
    (solid(STAINED_CLAY, BROWN), 2),
    (solid(HARDENED_CLAY), 40),
), beyond=solid(HARDENED_CLAY))

THEMES = {
    # the ground: one course of grass on a hard brown edge, and the rim is off so the edge is the
    # wall's own band rather than a cap that contours every fall
    "turf": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(layered(bands(
            (noise(301, 14, [solid(DIRT), solid(GRASS), solid(GRASS), solid(GRASS),
                             solid(GRASS), solid(DIRT, 1)]), 1),
            (solid(DIRT), 3),
        )), 4),
        "wall": TURF_WALL,
        "wallEnabled": True,
        "fill": solid(HARDENED_CLAY),
        "rim": off(solid(HARDENED_CLAY)),
        "rimEdges": "void",
    },
    # the stepped plates: brick, with a stone-brick course under the lip
    "brickwork": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(solid(BRICK), 1),
        "wall": layered(bands((solid(BRICK), 1), (solid(STONE_BRICK), 1), (solid(BRICK), 40)),
                        beyond=solid(BRICK)),
        "wallEnabled": True,
        "fill": solid(BRICK),
        "rim": off(solid(BRICK)),
        "rimEdges": "void",
    },
    # a warp pipe: a lime rim over a green barrel
    "pipe": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(solid(STAINED_CLAY, LIME), 1),
        "wall": solid(STAINED_CLAY, GREEN),
        "wallEnabled": True,
        "fill": solid(STAINED_CLAY, GREEN),
        "rim": off(solid(STAINED_CLAY, LIME)),
        "rimEdges": "void",
    },
    # a drawn hill: dark green with two lighter patches, which is what the two-tone hill is
    "hillside": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(cell_patches(302, 7, 45, 1, [
            solid(STAINED_CLAY, GREEN), solid(STAINED_CLAY, LIME)]), 2),
        "wall": cell_patches(303, 9, 45, 1, [
            solid(STAINED_CLAY, GREEN), solid(STAINED_CLAY, GREEN), solid(STAINED_CLAY, LIME)]),
        "wallEnabled": True,
        "fill": solid(STAINED_CLAY, GREEN),
        "rim": off(solid(STAINED_CLAY, LIME)),
        "rimEdges": "void",
    },
    # the sky: the same shape as a hill, in white — which is the joke the drawn levels made
    "cloudstuff": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(noise(304, 9, [solid(WOOL, WHITE), solid(WOOL, WHITE),
                                      solid(STAINED_CLAY, WHITE)]), 3),
        "wall": noise(305, 9, [solid(WOOL, WHITE), solid(WOOL, WHITE),
                               solid(STAINED_CLAY, WHITE)]),
        "wallEnabled": True,
        "fill": solid(WOOL, WHITE),
        "rim": off(solid(WOOL, WHITE)),
        "rimEdges": "void",
    },
    # the block a row of them is one of
    "qblock": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(solid(STAINED_CLAY, YELLOW), 1),
        "wall": layered(bands((solid(STAINED_CLAY, ORANGE), 1), (solid(STAINED_CLAY, YELLOW), 8)),
                        beyond=solid(STAINED_CLAY, YELLOW)),
        "wallEnabled": True,
        "fill": solid(STAINED_CLAY, YELLOW),
        "rim": off(solid(STAINED_CLAY, ORANGE)),
        "rimEdges": "void",
    },
}


# ── relief ──────────────────────────────────────────────────────────────────────
# The ground is flat and stays flat: this board's height is *plates*, which is what a drawn level
# does instead of a hill, and the two pits are the only thing the solver shapes. So there are three
# marks and two pushes, and `landform: plain` is what the read-back answers.
mark_rng = random.Random(3311)

#   keeppad  x -34..34  z -100..-74  h 18  the keep's own shelf and the two block houses
#   field    x -34..34  z  -70..-42  h 14  the flat the two cores stand on
KEEPPAD = lobed_box(-34, -100, 34, -74, 6, 0.02, mark_rng)
FIELDFLAT = lobed_box(-34, -70, 34, -42, 6, 0.02, mark_rng)

TEAM_MARKS = [
    {"id": "edge", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "keeppad", "kind": "area", "ring": KEEPPAD, "h": 18},
    {"id": "fieldflat", "kind": "area", "ring": FIELDFLAT, "h": SURFACE},
    # the three ways down off the keep's shelf, pinned so the tracks laid on them step by one
    {"id": "way-w", "kind": "line",
     "points": [[-8, -78], [-16, -74], [-22, -70], [-22, -64], [-22, -60]],
     "h": [18, 17, 16, 15, 14], "r": 5},
    {"id": "way-e", "kind": "line",
     "points": [[8, -78], [16, -74], [22, -70], [22, -64], [22, -60]],
     "h": [18, 17, 16, 15, 14], "r": 5},
    {"id": "way-mid", "kind": "line",
     "points": [[0, -78], [0, -76], [0, -74], [0, -72], [0, -68]],
     "h": [18, 17, 16, 15, 14], "r": 4},
]

# the two pits — the depression a destroy board takes instead of a hole cut in a team's own ground
TEAM_PUSHES = [
    {"id": "pit-w", "ring": lobed_ring(-8, -48, 9, 6, 11, 0.12, mark_rng),
     "amount": 0, "falloff": 8, "roughness": 0.20, "crown": -4, "seed": 21},
    {"id": "pit-e", "ring": lobed_ring(8, -48, 9, 6, 11, 0.12, mark_rng),
     "amount": 0, "falloff": 8, "roughness": 0.20, "crown": -4, "seed": 22},
]

MIDWAY_FLAT = lobed_box(-44, -14, 44, 14, 6, 0.02, mark_rng)
MID_MARKS = [
    {"id": "midway-edge", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "midway-flat", "kind": "area", "ring": MIDWAY_FLAT, "h": 15},
]

RELIEF = {
    "team": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "plain",
             "grain": {"amplitude": 0, "scale": 12, "seed": 31},
             "marks": TEAM_MARKS, "pushes": TEAM_PUSHES},
    "neutral": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "plain",
                "grain": {"amplitude": 0, "scale": 12, "seed": 32},
                "marks": MID_MARKS, "pushes": []},
}


# ── the plates: this board's height, in place of a hill ─────────────────────────
def plate(shape_id, min_x, min_z, max_x, max_z, absolute_top, theme):
    """One blocky step: an override add held at an absolute top with a sheer face.

    `height_mode: level` holds it at the top its own floor and height state, `skirt: 0` is the cut
    face a drawn platform has, and `relief_scope: exclude` keeps its ground out of the group's solve —
    without all three a relief solves straight through an override add's stated top (SK14).

    Two blocks a step, not four: a one-block rise walks, a two-block rise costs one placed block, and
    three or more is a barrier. A staircase of twos is the tallest thing that still reads as a climb.
    """
    return {"id": shape_id, "type": "rectangle", "operation": "add", "override": True,
            "min_x": min_x, "min_z": min_z, "max_x": max_x, "max_z": max_z,
            "floor": 0, "base_height": absolute_top, "height_mode": "level", "skirt": 0,
            "relief_scope": "exclude", "theme": theme}


def staircase(name, from_x, step_x, min_z, max_z, tops, theme="brickwork"):
    """A run of plates climbing in x, each one clear of the last in plan.

    Two override adds over one column is the taller winning the geometry and the *smaller* winning
    the paint (SK15), so the steps are laid side by side and never overlapped.
    """
    return [plate(f"{name}-{i}", from_x + i * step_x, min_z, from_x + (i + 1) * step_x, max_z,
                  absolute_top, theme)
            for i, absolute_top in enumerate(tops)]


patch_rng = random.Random(4141)


def patch(shape_id, ring, theme):
    """A splotch: an ordinary one-course add, so the taller add keeps the height and the smallest
    shape keeps the colour."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
            "vertices": ring, "theme": theme}


ADD_SHAPES = (
    # one staircase a side, climbing outward from the level pan the cores stand on. It starts at the
    # pinned flat's own edge (x 34) so its bottom step is flush with the ground a core is on, and it
    # stops two blocks short of the core row in z.
    staircase("stair-w", -52, 6, -70, -58, [22, 20, 18])
    + staircase("stair-e", 34, 6, -70, -58, [18, 20, 22])
    # and one low plate a side ahead of it, which is what a drawn level puts between two gaps
    + [plate("shelf-w", -52, -52, -40, -44, 18, "brickwork"),
       plate("shelf-e", 40, -52, 52, -44, 18, "brickwork")]
)


# ── the made things: pipes, hills, clouds and block rows ───────────────────────
def pipe(name, cx, cz, radius, height, seed):
    """A warp pipe: a barrel with a wider lip, seated on the ground.

    Two slabs, sharing a `part_of` so `seat` settles them as one thing. It is `made` rather than
    terrain for the reason every standing thing on these boards is: the build ceiling is the tallest
    *terrain* column plus twenty, and a made layer is out of that reckoning.
    """
    rng = random.Random(seed)
    return [
        {"id": f"{name}-barrel", "name": f"{name} barrel", "base_y": 0,
         "kind": "made", "part_of": name, "seat": "ground",
         "shapes": [{"id": f"{name}-b0", "type": "circle", "operation": "add",
                     "center_x": cx, "center_z": cz, "radius": radius,
                     "floor": 0, "base_height": height, "height_mode": "level", "skirt": 0,
                     "relief_scope": "exclude", "theme": "pipe"}],
         "groups": [{"id": f"{name}-b0-g", "name": name, "mirrors": True,
                     "shapeIds": [f"{name}-b0"]}]},
        {"id": f"{name}-lip", "name": f"{name} lip", "base_y": height,
         "kind": "made", "part_of": name, "seat": "ground",
         "shapes": [{"id": f"{name}-l0", "type": "circle", "operation": "add",
                     "center_x": cx + rng.randint(0, 0), "center_z": cz,
                     "radius": radius + 1,
                     "floor": 0, "base_height": 2, "height_mode": "level", "skirt": 0,
                     "relief_scope": "exclude", "theme": "pipe"}],
         "groups": [{"id": f"{name}-l0-g", "name": name, "mirrors": True,
                     "shapeIds": [f"{name}-l0"]}]},
    ]


def mound(name, cx, cz, seed, theme, seat, base_y=0, scale=1.0):
    """The drawn hill, and the drawn cloud: the same three narrowing tiers in two colours.

    Seated it is a hill standing on the ground; unseated at a stated `base_y` it is a cloud. That
    they are one recipe is the joke the drawn levels made, and it is also one fewer shape to author.
    `scale` shrinks the lobes about the centre. At 1.0 the silhouette is 32 blocks across, which is
    wider than the ground either side of a core on this board, and a hill overhanging a house shares
    its columns.

    The lobes state no `relief_scope`, so they inherit their group's ground. `exclude` takes a
    footprint out of the relief solve entirely, which for a seated hill standing on a pinned pad
    punches the hill's own outline out of the pad and leaves the ground under it at the base — and
    the house beside it then foundations into that face.
    """
    rng = random.Random(seed)
    tiers = [(0, 4, [(0, 0, 11), (-8, 2, 7), (9, -2, 7)]),
             (4, 4, [(0, 1, 8), (-5, 2, 5), (6, -1, 5)]),
             (8, 4, [(0, 0, 5), (3, 2, 4)])]
    layers = []
    for tier, (floor_y, thickness, lobes) in enumerate(tiers):
        shapes = [{
            "id": f"{name}-{tier}-{index}", "type": "circle", "operation": "add",
            "center_x": cx + round(dx * scale) + rng.randint(-1, 1),
            "center_z": cz + round(dz * scale) + rng.randint(-1, 1),
            "radius": max(2, round(radius * scale)), "floor": 0, "base_height": thickness,
            "height_mode": "level", "skirt": 0, "theme": theme,
        } for index, (dx, dz, radius) in enumerate(lobes)]
        layer = {"id": f"{name}-{tier}", "name": f"{name} tier {tier}",
                 "base_y": base_y + floor_y, "kind": "made", "part_of": name, "shapes": shapes,
                 "groups": [{"id": f"{name}-{tier}-g", "name": name, "mirrors": True,
                             "shapeIds": [shape["id"] for shape in shapes]}]}
        if seat:
            layer["seat"] = "ground"
        layers.append(layer)
    return layers


def block_row(name, from_x, cz, count, at_y, size=2, gap=2):
    """A row of floating blocks, brick and question alternating.

    One made layer, one small rectangle a block. A made layer is not ground, so a row hanging ten
    over the field raises no `SK11` about standable ground nothing reaches — which is exactly what
    the same row drawn as terrain would have raised.
    """
    shapes = []
    for index in range(count):
        min_x = from_x + index * (size + gap)
        shapes.append({"id": f"{name}-{index}", "type": "rectangle", "operation": "add",
                       "min_x": min_x, "min_z": cz, "max_x": min_x + size, "max_z": cz + size,
                       "floor": 0, "base_height": size, "height_mode": "level", "skirt": 0,
                       "relief_scope": "exclude",
                       "theme": "qblock" if index % 2 else "brickwork"})
    return [{"id": name, "name": name, "base_y": at_y, "kind": "made", "part_of": name,
             "shapes": shapes,
             "groups": [{"id": f"{name}-g", "name": name, "mirrors": True,
                         "shapeIds": [shape["id"] for shape in shapes]}]}]


ADD_LAYERS = (
    # the two warp pipes a side, behind each staircase's foot
    pipe("pipe-w", -44, -76, 3, 6, 51)
    + pipe("pipe-e", 44, -76, 3, 6, 52)
    # one on the midway, whose rot_180 image is the far side's
    + pipe("pipe-mid", -34, 2, 3, 7, 53)
    # the two drawn hills, behind the keep's own shelf where no route runs
    + mound("hill-w", -46, -92, 61, "hillside", seat=True, scale=0.55)
    + mound("hill-e", 46, -92, 62, "hillside", seat=True, scale=0.55)
    # and three clouds, in the sky and clear of every roof
    + mound("cloud-w", -52, -78, 71, "cloudstuff", seat=False, base_y=82, scale=0.7)
    + mound("cloud-e", 52, -78, 72, "cloudstuff", seat=False, base_y=88, scale=0.7)
    + mound("cloud-mid", -52, 4, 73, "cloudstuff", seat=False, base_y=76, scale=0.7)
    # two block rows a side over the field's flanks, and one over the midway
    + block_row("row-w", -18, -49, 5, 24)
    + block_row("row-e", 6, -30, 5, 24)
    + block_row("row-mid", -12, 4, 5, 28)
)


# ── house styles ────────────────────────────────────────────────────────────────
def keep_style():
    """The keep: brick over a stone-brick plinth, stone-brick corner towers, a flat lid."""
    return {
        "foundation": {
            "plate": {"stack": bands((solid(STONE_BRICK), 1), (solid(STONE_BRICK), 1),
                                     (solid(COBBLE), 1)), "extent": 3},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(STONE_BRICK),
        },
        "roof": {
            "form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": False, "hole": True,
            "body": solid(BRICK),
            "verge": solid(STONE_BRICK),
            "gable": solid(BRICK),
            "gableWindows": {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 2, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": {"stack": bands((solid(STONE_BRICK), 2), (solid(BRICK), 5)), "extent": 7},
        "post": solid(STONE_BRICK),
        "windows": {"form": "arched", "block": STONE_BRICK_STAIRS, "hostBlock": -1, "hostData": 0,
                    "data": 0, "sill": 3, "width": 2, "height": 2, "spacing": 3},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": STONE_BRICK_STAIRS, "fill": "upperSlab",
                             "fillBlock": STONE_SLAB, "fillData": STONE_BRICK_SLAB},
                    "width": 2, "height": 3},
    }


def blockhouse_style():
    """A brick block house: a two-storey cube with a flat brick lid, the way a drawn level
    draws a building — no pitch, no eave, a hard silhouette."""
    walls = {"stack": bands((solid(BRICK), 2), (solid(STONE_BRICK), 1), (solid(BRICK), 2)),
             "extent": 5}
    return {
        "foundation": {
            "plate": {"stack": bands((solid(STONE_BRICK), 1), (solid(COBBLE), 1)), "extent": 2},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(STONE_BRICK),
        },
        "roof": {
            "form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": False, "hole": False,
            "body": solid(BRICK),
            "verge": solid(STONE_BRICK),
            "gable": solid(BRICK),
            "gableWindows": {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 2, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": walls,
        "post": solid(STONE_BRICK),
        "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0, "data": 0,
                    "sill": 2, "width": 1, "height": 2, "spacing": 2},
        "storeys": [
            {"clear": 3, "wall": walls, "post": solid(STONE_BRICK),
             "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 2, "width": 1, "height": 2, "spacing": 2},
             "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                         "inlayInset": 2, "isPlain": True},
             "deck": None, "headroom": 3},
            {"clear": 3, "wall": walls, "post": solid(STONE_BRICK),
             "windows": {"form": "pane", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                         "data": 0, "sill": 1, "width": 1, "height": 2, "spacing": 2},
             "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                         "inlayInset": 2, "isPlain": True},
             "deck": solid(STONE_BRICK), "headroom": 3},
        ],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": STONE_BRICK_STAIRS, "fill": "upperSlab",
                             "fillBlock": STONE_SLAB, "fillData": STONE_BRICK_SLAB},
                    "width": 2, "height": 3},
    }


def caphouse_style():
    """A tiny cap house: quartz walls with a red band, and a red mushroom-block dome."""
    return {
        "foundation": {
            "plate": {"stack": bands((solid(QUARTZ), 1), (solid(STONE_BRICK), 1)), "extent": 2},
            "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                        "inlayInset": 2, "isPlain": True},
            "footing": solid(QUARTZ),
        },
        "roof": {
            # hip, so a five-by-six hut wears a dome rather than a ridge
            "form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": True, "hole": False,
            "body": solid(RED_MUSHROOM_BLOCK, ALL_CAP),
            "verge": solid(RED_MUSHROOM_BLOCK, ALL_CAP),
            "gable": solid(QUARTZ),
            "gableWindows": {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
                             "data": 0, "sill": 1, "width": 1, "height": 1, "spacing": 3},
        },
        "wall": {"stack": bands((solid(QUARTZ), 2), (solid(STAINED_CLAY, RED), 1),
                                (solid(QUARTZ), 2)), "extent": 5},
        "post": None,
        "windows": {"form": "pane", "block": STAINED_CLAY, "hostBlock": -1, "hostData": 0,
                    "data": WHITE, "sill": 2, "width": 1, "height": 1, "spacing": 2},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "none", "block": OAK_STAIRS, "fill": "upperSlab",
                             "fillBlock": WOOD_SLAB, "fillData": OAK},
                    "width": 2, "height": 3},
    }


# ── the dressing ────────────────────────────────────────────────────────────────
tree_rng = random.Random(2211)

STYLES = {}
for index in range(4):
    STYLES[f"blocktree-{index + 1}"] = {
        "kind": "tree", "form": "copied",
        "body": block_tree(tree_rng, trunk=tree_rng.randint(3, 5),
                           radius=tree_rng.randint(3, 4), tiers=2),
    }
STYLES["flowerbed"] = {"kind": "tree", "form": "copied",
                       "body": clump_body([(0, 0), (2, 1), (1, 3), (3, 2)], 38, 0)}
STYLES["flowerbed-2"] = {"kind": "tree", "form": "copied",
                         "body": clump_body([(0, 0), (2, 2), (3, 0)], 37, 0)}

STYLES["keep"] = {"kind": "house", "shell": keep_style()}
STYLES["blockhouse"] = {"kind": "house", "shell": blockhouse_style()}
STYLES["caphouse"] = {"kind": "house", "shell": caphouse_style()}

# the track: the hard brown ground line a drawn level rules under its grass
TRACK_PAVE = cell_patches(311, 3, 55, 1, [solid(HARDENED_CLAY), solid(STAINED_CLAY, BROWN)])

PROPS = []

# the tracks: the keep's own door out to the field, one to each core, on the corridors the relief
# pinned for them. Every corner is chamfered, because a band follows a Catmull-Rom through the drawn
# line and a spline overshoots the outside of a sharp turn.
PROPS.append({"id": "track-w", "kind": "stroke", "seed": 41, "radius": 2.5, "style": "solid",
              "coverage": 1.0, "route": True, "pave": TRACK_PAVE,
              "points": [[-6, -79], [-12, -76], [-17, -73], [-21, -69], [-22, -65],
                         [-22, -61], [-22, -50], [-23, -46]]})
PROPS.append({"id": "track-e", "kind": "stroke", "seed": 42, "radius": 2.5, "style": "solid",
              "coverage": 1.0, "route": True, "pave": TRACK_PAVE,
              "points": [[6, -79], [12, -76], [17, -73], [21, -69], [22, -65],
                         [22, -61], [22, -50], [23, -46]]})

# the buildings: three ideas, every one on ground a relief mark pinned level, and two clear columns
# between each pair's stamped extent
PROPS.append({"id": "block-w", "kind": "house", "seed": 441,
              "wings": [{"corners": [[-26, -97], [-18, -90]]}], "front": "posX",
              "style": "blockhouse"})
PROPS.append({"id": "block-e", "kind": "house", "seed": 442,
              "wings": [{"corners": [[18, -97], [26, -90]]}], "front": "negX",
              "style": "blockhouse"})
PROPS.append({"id": "cap-w", "kind": "house", "seed": 443,
              "wings": [{"corners": [[-24, -86], [-18, -81]]}], "front": "posZ",
              "style": "caphouse"})
PROPS.append({"id": "cap-e", "kind": "house", "seed": 444,
              "wings": [{"corners": [[18, -86], [24, -81]]}], "front": "posZ",
              "style": "caphouse"})
PROPS.append({"id": "cap-mid", "kind": "house", "seed": 445,
              "wings": [{"corners": [[-22, -14], [-16, -9]]}], "front": "posZ",
              "style": "caphouse"})

# the trees, in stands rather than scattered: one either side of each core's apron, a row along the
# field's front, and three on the midway
STAND_FIELD = [(-28, -80), (28, -80), (-12, -64), (12, -64), (-14, -42), (14, -42)]
STAND_MID = [(-4, 12), (6, 2)]

TREE_STYLES = ["blocktree-1", "blocktree-2", "blocktree-3", "blocktree-4"]
for index, (x, z) in enumerate(STAND_FIELD + STAND_MID):
    PROPS.append({"id": f"tree-{index}", "kind": "tree", "seed": 3000 + index * 7,
                  "x": x, "z": z, "style": TREE_STYLES[index % len(TREE_STYLES)]})

# the flower beds, on the field's own grass
PROPS.append({"id": "flower-w", "kind": "tree", "seed": 451, "x": -36, "z": -74,
              "style": "flowerbed"})
PROPS.append({"id": "flower-e", "kind": "tree", "seed": 452, "x": 36, "z": -74,
              "style": "flowerbed-2"})
PROPS.append({"id": "flower-mid", "kind": "tree", "seed": 453, "x": -26, "z": 10,
              "style": "flowerbed"})

# the cover: flower-heavy and no fern, which is what a drawn meadow is
FLORA = {"coverage": 0.55, "scale": 10, "octaves": 3, "fernShare": 0.0,
         "flowerShare": 0.30, "flowerScale": 14, "tallShare": 0.05}
flora_rng = random.Random(5151)
PROPS.append({"id": "cover-field", "kind": "flora", "seed": 91, "spec": FLORA,
              "points": on_field(lobed_ring(0, -56, 34, 14, 13, 0.08, flora_rng))})
PROPS.append({"id": "cover-keep", "kind": "flora", "seed": 92, "spec": FLORA,
              "points": on_field(lobed_ring(0, -88, 30, 11, 11, 0.10, flora_rng))})
PROPS.append({"id": "cover-mid", "kind": "flora", "seed": 93, "spec": FLORA,
              "points": on_midway(lobed_ring(0, 0, 26, 12, 13, 0.08, flora_rng))})


FINISH = {
    "themeById": {},
    # the coasts drawn rather than ruled — but only a little: a drawn level's ground has a hard edge,
    # so five blocks of wander is as organic as this board wants to be
    "bendShapes": {"field-14": {"k": 0.14, "wander": 4, "step": 14, "seed": 3},
                   "midway-14": {"k": 0.12, "wander": 3, "step": 12, "seed": 5}},
    "addShapes": ADD_SHAPES,
    "addLayers": ADD_LAYERS,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "turf",
    # plains for the grass and a little forest for the darker leaves, and nothing else: the board's
    # colour is stated in blocks, so a biome that re-tinted it would be arguing with the paint
    "biome": {"kind": "cell", "seed": 19, "cellSize": 40, "jitter": 35,
              "palette": [1, 1, 4, 1]},
    "roomStyles": {"spawn": keep_style()},
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
