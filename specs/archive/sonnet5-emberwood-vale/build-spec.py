#!/usr/bin/env python3
"""Emberwood Vale — two hamlets at opposite ends of an autumn forest clearing.

Generates <slug>.plan.json and <slug>.finish.json for tools/drive.py. The plan states one
team's half (spawn hamlet, split-off garden island, forest approach, flank trail, wool
shrine) plus the shared on-axis forest clearing; rot_180 fans the rest. The finish carries
the relief, the three themes, the two timber house styles, the shrine style, the garden
footbridge and the forest/hamlet dressing.
"""
import json
import os

SLUG = "sonnet5-emberwood-vale"
HERE = os.path.dirname(os.path.abspath(__file__))
CELL = 5


def R(x, z, w, h):
    return [x, z, w, h]


# ---------------------------------------------------------------------------
# PLAN — one team's half in cells; rot_180 fans the rest.
# ---------------------------------------------------------------------------

pieces = [
    # The shrine: the deepest, best-protected ground, behind the hamlet.
    {"id": "wool-room-red", "role": "wool-room", "rect": R(-2, -24, 4, 5)},

    # The hamlet: two piece rectangles either side of the village green void.
    {"id": "spawn-red", "role": "spawn", "rect": R(-6, -19, 4, 6)},
    {"id": "hamlet-east-red", "role": "piece", "rect": R(0, -19, 4, 6)},

    # A flank trail behind and beside the hamlet — the harder second route.
    {"id": "flank-red", "role": "piece", "rect": R(-11, -15, 4, 12)},

    # The main approach lawn, connecting the hamlet to the shared clearing.
    {"id": "approach-red", "role": "piece", "rect": R(-7, -13, 11, 10)},

    # The garden/clearing island, split off from the approach by a void.
    {"id": "garden-red", "role": "piece", "rect": R(6, -9, 4, 6)},

    # Red's half of the forest clearing. A brook (void, 20 blocks across
    # after the fan) cuts the clearing in two along its whole width — the
    # void the composer never puts to work inside a capture board's own
    # middle, doing exactly what approaches.md asks of one: it is the
    # instrument, not leftover space.
    # 15 cells wide — approach-red's 11 plus flank-red's 4, so the flank
    # trail reaches the brook in its own right rather than only rejoining
    # the main street, and the frontline stays inside FR6's 16-cell cap.
    {"id": "clearing-red", "role": "piece", "rect": R(-11, -3, 15, 1)},
]

zones = [
    # The village green: a void courtyard inside the hamlet, buildable from
    # the first tick — the composer never puts a build zone inside a team's
    # own site, so this is drawn by hand.
    {"id": "village-green", "rect": R(-2, -19, 2, 6)},

    # The ford: the mid band the brook opens, spanning the whole width of
    # the crossing it docks against rather than funnelling through a slice
    # of it (FR8).
    {"id": "ford", "rect": R(-11, -2, 15, 4)},
]

placements = {
    "spawns": [
        # Footprint capped at 20x20 (ST9): a 14x18 hall inside the 20x30 pad,
        # margined 3 either side and 6 front, 6 back.
        {"id": "spawn-red-1", "piece": "spawn-red", "at": [10.0, 15.0],
         "facing": "back", "footprint": [3, 6, 14, 18]},
    ],
    "wools": [
        # Footprint capped at 20x20 (ST9): an 18x18 shrine inside the 20x25 pad.
        {"id": "wool-red-1", "piece": "wool-room-red", "at": [10.0, 12.0],
         "footprint": [1, 3, 18, 18]},
    ],
    "iron": [
        {"id": "iron-red-1", "piece": "spawn-red", "at": [6.5, 27.5]},
    ],
}

plan = {
    "plan": 2,
    "meta": {"name": "Emberwood Vale"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 10, "surface": 9,
                "observerY": 34},
    "pieces": pieces,
    "zones": zones,
    "placements": placements,
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as f:
    json.dump(plan, f, indent=2)

print(f"wrote {SLUG}.plan.json — {len(pieces)} pieces, {len(zones)} zones")

# ---------------------------------------------------------------------------
# FINISH — themes, relief, the garden bridge, the two house styles, and the
# forest/hamlet dressing. Keyed on the shape ids POST /plan/compile answers:
# the fused landmass is "approach-red-9", the garden island "garden-red-9".
# ---------------------------------------------------------------------------

import random

RNG = random.Random(20260911)

# Vanilla block ids/data used below (GET /api/terrain/blocks).
GRASS = (2, 0)
DIRT = (3, 0)
COARSE_DIRT = (3, 1)
STONE = (1, 0)
COBBLE = (4, 0)
ANDESITE = (1, 5)
POL_ANDESITE = (1, 6)
GRAVEL = (13, 0)
STONE_BRICK = (98, 0)
CHISELED_STONE_BRICK = (98, 3)
QUARTZ = (155, 0)
CHISELED_QUARTZ = (155, 1)
QUARTZ_PILLAR = (155, 2)
OAK_LOG = (17, 0)
SPRUCE_LOG = (17, 1)
OAK_PLANKS = (5, 0)
SPRUCE_PLANKS = (5, 1)
DARK_OAK_PLANKS = (5, 5)
GLASS_PANE = (102, 0)
PODZOL = (3, 2)


def solid(pair):
    return {"kind": "solid", "id": pair[0], "data": pair[1]}


def layered(axis, bands, ending="repeat"):
    return {"kind": "layered", "axis": axis,
            "stack": {"bands": [{"material": m, "thickness": t} for m, t in bands],
                      "ending": ending}}


def cellmat(seed, cell_size, palette, jitter=40, warp=3, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": cell_size, "jitter": jitter,
            "warp": warp, "palette": [solid(p) for p in palette], "rise": rise}


def checker(size, even, odd):
    return {"kind": "checker", "size": size, "even": solid(even), "odd": solid(odd)}


def laidlog(pair):
    return {"kind": "laidLog", "id": pair[0], "data": pair[1]}


def topband(material, depth, enabled=True):
    return {"material": material, "depth": depth, "enabled": enabled}


# The stone family every steep face and every cut on the board shares —
# Stone/Cobblestone/Andesite, never mossy cobble or cracked brick (brief).
ROCK_PALETTE = [STONE, COBBLE, ANDESITE]

# ---- three themes: the forest floor, the hamlet dooryards, the shrine ----

emberwood_floor = {
    "rim": topband(solid(STONE), 1, enabled=False),
    "surface": topband(
        layered("slope", [
            (layered("depth", [(solid(GRASS), 1), (solid(DIRT), 2)]), 28),
            (layered("depth", [(solid(COARSE_DIRT), 1), (solid(DIRT), 2)]), 17),
            (cellmat(4471, 7, ROCK_PALETTE, jitter=45, warp=3), 90),
        ]),
        3),
    "wall": cellmat(4472, 7, ROCK_PALETTE, jitter=45, warp=3, rise=3),
    "fill": cellmat(4473, 9, ROCK_PALETTE, jitter=45, warp=3, rise=5),
}

hearth_yard = {
    "rim": topband(solid(COBBLE), 1, enabled=True),
    "surface": topband(
        layered("slope", [
            (layered("depth", [(solid(COARSE_DIRT), 1), (solid(DIRT), 2)]), 28),
            (layered("depth", [(solid(DIRT), 1), (solid(GRAVEL), 2)]), 17),
            (cellmat(5581, 6, ROCK_PALETTE, jitter=35, warp=2), 90),
        ]),
        3),
    "wall": cellmat(5582, 6, ROCK_PALETTE, jitter=35, warp=2, rise=3),
    "fill": cellmat(5583, 9, ROCK_PALETTE, jitter=40, warp=3, rise=5),
}

shrine_stone = {
    "rim": topband(solid(QUARTZ), 1, enabled=True),
    "surface": topband(
        cellmat(6691, 5, [STONE_BRICK, QUARTZ, CHISELED_STONE_BRICK], jitter=30, warp=2),
        2),
    "wall": solid(STONE_BRICK),
    "fill": cellmat(6693, 8, [STONE_BRICK, QUARTZ, ANDESITE], jitter=30, warp=2, rise=4),
}

themes = {
    "emberwood-floor": emberwood_floor,
    "hearth-yard": hearth_yard,
    "shrine-stone": shrine_stone,
}

# ---- relief: three gentle rises, kept local with a modest reach ----

relief = {
    "team": {
        "base": 9,
        "reach": 22,
        "marks": [
            {"kind": "point", "at": [-45, -45], "r": 5, "h": 12},
            {"kind": "point", "at": [-10, -30], "r": 6, "h": 6},
            {"kind": "point", "at": [40, -30], "r": 4, "h": 11},
        ],
    }
}

# `emberwood-floor` is the map default (below), so the forest and the
# garden island need no per-shape theme at all. `hearth-yard` and
# `shrine-stone` reach the board only as the two accent patches in
# `add_shapes`, because a spawn/wool piece is projected onto a role-tagged
# shape `themeById` cannot see (GENERATION-NOTES: "a spawn shape's interior
# is never painted by its theme") — a patch drawn over the pad is what
# still gets the dooryard and the shrine yard themed at all.

# ---- the two timber cottages and the shrine's stone-and-quartz hut -----

def timber_wall(plank):
    """A wall carrying beams (below) also carries a plain laid-log course
    (brief) plus a checker of two DIFFERENT log species — never one twice."""
    return {"stack": {"bands": [
        {"material": laidlog(SPRUCE_LOG), "thickness": 2},
        {"material": checker(1, OAK_LOG, SPRUCE_LOG), "thickness": 2},
        {"material": solid(plank), "thickness": 3},
    ], "ending": "repeat"}, "extent": 7}


DOORWAY_TIMBER = {"door": "air",
                   "head": {"form": "arched", "block": 134, "fill": "upperSlab",
                             "fillBlock": 126, "fillData": 1},
                   "width": 3, "height": 4}
WINDOW_TIMBER = {"form": "pane", "block": 102, "hostBlock": -1, "hostData": 0,
                  "data": 0, "sill": 3, "width": 1, "height": 2, "spacing": 3}
GABLE_WINDOWS_NONE = {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0,
                       "data": 0, "sill": 2, "width": 2, "height": 2, "spacing": 3}
BEAMS_LOG = {"block": SPRUCE_LOG[0], "data": SPRUCE_LOG[1], "reach": 1, "any": True}

cottage_a = {
    "foundation": {"plate": {"stack": {"bands": [{"material": solid(COBBLE), "thickness": 1}],
                                        "ending": "repeat"}, "extent": 2},
                   "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                "inlayInset": 2, "isPlain": True},
                   "footing": None},
    "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
             "ridgeCap": True, "hole": False,
             "body": solid(SPRUCE_PLANKS), "verge": solid(DARK_OAK_PLANKS),
             "gable": solid(SPRUCE_PLANKS), "gableWindows": GABLE_WINDOWS_NONE},
    "wall": timber_wall(SPRUCE_PLANKS),
    "post": solid(OAK_LOG),
    "windows": WINDOW_TIMBER,
    "storeys": [],
    "porch": None, "front": None,
    "beams": BEAMS_LOG,
    "doorway": DOORWAY_TIMBER,
}

# The variant: a hip roof and a darker infill on the same timber recipe —
# a repaint and a roof swap, not a second design (brief).
cottage_b = {
    "foundation": cottage_a["foundation"],
    "roof": {"form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
             "ridgeCap": True, "hole": False,
             "body": solid(DARK_OAK_PLANKS), "verge": solid(SPRUCE_PLANKS),
             "gable": solid(DARK_OAK_PLANKS), "gableWindows": GABLE_WINDOWS_NONE},
    "wall": timber_wall(DARK_OAK_PLANKS),
    "post": solid(SPRUCE_LOG),
    "windows": WINDOW_TIMBER,
    "storeys": [],
    "porch": None, "front": None,
    "beams": BEAMS_LOG,
    "doorway": DOORWAY_TIMBER,
}

shrine = {
    "foundation": {"plate": {"stack": {"bands": [{"material": solid(STONE_BRICK), "thickness": 1}],
                                        "ending": "repeat"}, "extent": 1},
                   "surface": {"field": None, "border": None, "borderWidth": 1, "inlay": None,
                                "inlayInset": 2, "isPlain": True},
                   "footing": None},
    "roof": {"form": "hip", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
             "ridgeCap": True, "hole": False,
             "body": solid(STONE_BRICK), "verge": solid(QUARTZ),
             "gable": solid(QUARTZ), "gableWindows": GABLE_WINDOWS_NONE},
    "wall": {"stack": {"bands": [
        {"material": solid(STONE_BRICK), "thickness": 2},
        {"material": solid(QUARTZ), "thickness": 2},
    ], "ending": "repeat"}, "extent": 4},
    "post": solid(QUARTZ_PILLAR),
    "windows": {"form": "none", "block": 102, "hostBlock": -1, "hostData": 0, "data": 0,
                "sill": 2, "width": 2, "height": 2, "spacing": 3},
    "storeys": [],
    "porch": None, "front": None,
    "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
    "doorway": {"door": "air",
                "head": {"form": "arched", "block": 109, "fill": "upperSlab",
                          "fillBlock": 44, "fillData": 5},
                "width": 2, "height": 3},
}

room_styles = {"spawn": cottage_a, "wool": shrine}

add_shapes = [
    # The garden footbridge: an ordinary add across the void between
    # approach-red and garden-red — nothing subtracts that ground, so no
    # override is needed, only a material of its own (a made thing, not a
    # theme's ground).
    {
        "id": "garden-bridge", "type": "rectangle", "operation": "add",
        "min_x": 20, "min_z": -33, "max_x": 30, "max_z": -27,
        "base_height": 9, "floor": 0, "relief_scope": "exclude",
        "keepClear": True, "material": solid(SPRUCE_PLANKS),
    },
    # The leaf-litter patch: its own small accent shape rather than a
    # blended noise field over the whole floor.
    {
        "id": "leaf-litter", "type": "polygon", "operation": "add",
        "vertices": [[-30, -55], [-14, -58], [-6, -48], [-16, -38], [-30, -42]],
        "base_height": 1, "floor": 0,
        "material": layered("depth", [
            (cellmat(7781, 6, [PODZOL, COARSE_DIRT], jitter=35, warp=4, rise=2), 1),
            (solid(DIRT), 2),
        ]),
    },
    # The hamlet's worn-earth dooryard: a paint patch at the ground's own
    # height, so it changes nothing but the theme. Two rectangles, one
    # either side of the green plaza's own void, which a plain add cannot
    # draw over (SK13 — the subtract always wins).
    {
        "id": "dooryard-w", "type": "rectangle", "operation": "add",
        "min_x": -32, "min_z": -93, "max_x": -10, "max_z": -63,
        "base_height": 9, "floor": 0, "theme": "hearth-yard",
    },
    {
        "id": "dooryard-e", "type": "rectangle", "operation": "add",
        "min_x": 0, "min_z": -93, "max_x": 22, "max_z": -63,
        "base_height": 9, "floor": 0, "theme": "hearth-yard",
    },
    # The shrine yard: the same technique, around the wool room's own pad.
    {
        "id": "shrine-yard", "type": "rectangle", "operation": "add",
        "min_x": -12, "min_z": -122, "max_x": 12, "max_z": -95,
        "base_height": 9, "floor": 0, "theme": "shrine-stone",
    },
]

# ---------------------------------------------------------------------------
# DRESSING — the second cottage, the forest and its paths.
# ---------------------------------------------------------------------------

dressing_styles = {
    "cottage-b": {**cottage_b, "kind": "house"},
    "oak-a": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
    "oak-b": {"kind": "tree", "form": "template", "species": "oak", "height": 12},
    "birch-a": {"kind": "tree", "form": "template", "species": "birch", "height": 8},
    "birch-b": {"kind": "tree", "form": "template", "species": "birch", "height": 10},
    "darkoak-a": {"kind": "tree", "form": "template", "species": "dark oak", "height": 9},
    "erratic-a": {"kind": "boulder", "form": "round", "size": 4, "rock": cellmat(
        8801, 3, ROCK_PALETTE, jitter=30, warp=1), "mossy": True},
}

props = []


def house_prop(prop_id, x0, z0, x1, z1, style, seed):
    props.append({"kind": "house", "id": prop_id, "seed": seed, "style": style,
                   "wings": [{"corners": [[x0, z0], [x1, z1]]}]})


def tree_prop(prop_id, x, z, style, seed):
    props.append({"kind": "tree", "id": prop_id, "x": x, "z": z, "style": style, "seed": seed})


def boulder_prop(prop_id, x, z, style, seed):
    props.append({"kind": "boulder", "id": prop_id, "x": x, "z": z, "style": style, "seed": seed})


def stroke_prop(prop_id, points, radius, style, claims, materials, seed, coverage=1.0):
    props.append({"kind": "stroke", "id": prop_id, "points": points, "radius": radius,
                   "style": style, "claimsGround": claims, "coverage": coverage,
                   "seed": seed, "pave": cellmat(seed, 3, materials, jitter=25, warp=1)})


def flora_prop(prop_id, points, coverage, scale, seed):
    props.append({"kind": "flora", "id": prop_id, "points": points, "seed": seed,
                   "spec": {"coverage": coverage, "scale": scale, "octaves": 2,
                            "fernShare": 0.25, "flowerShare": 0.18, "flowerScale": 6,
                            "tallShare": 0.15}})


# The second cottage — hamlet-east-red's own building, the hip-roofed
# variant. Spawn opens two doors (south to approach-red, east across the
# green) and each keeps a 20-block apron, so the cottage sits east of the
# spawn door's reach as well as south of the wool room's own 10-block one.
house_prop("hamlet-east-cottage", 8, -78, 20, -68, "cottage-b", 501)

# The forest — a jittered grid of oak, birch and dark oak, spaced so a pair
# of average heights clears the DR-CLAIM Chebyshev rule with room to spare
# ((h_a+h_b)/4.7 tops out around 4-5 blocks here; 13-16 leaves real gaps).
SPECIES = ["oak-a", "oak-b", "birch-a", "birch-b", "darkoak-a"]


def scatter_trees(prefix, xmin, xmax, zmin, zmax, spacing, seed_base):
    x = xmin + spacing / 2
    n = 0
    while x < xmax:
        z = zmin + spacing / 2
        while z < zmax:
            jx = x + RNG.uniform(-spacing * 0.35, spacing * 0.35)
            jz = z + RNG.uniform(-spacing * 0.35, spacing * 0.35)
            style = SPECIES[RNG.randrange(len(SPECIES))]
            tree_prop(f"{prefix}-{n}", round(jx), round(jz), style, seed_base + n)
            n += 1
            z += spacing
        x += spacing
    return n


# Either side of the main street through approach-red, leaving the street
# itself (x -8..8) and the spawn's door apron (twenty blocks south of its
# face at z -71) clear.
scatter_trees("wood-w", -33, -9, -50, -18, 13, 1001)
scatter_trees("wood-e", 9, 18, -50, -18, 13, 2001)
# The flank trail's own wood — denser, rougher, the wool's harder route.
# The trail itself hugs flank-red's own west edge, so the wood fills the
# strip east of it clear of DR-ROAD's standoff.
scatter_trees("wood-flank", -47, -37, -73, -18, 8, 3001)
# A light scatter over the garden island — ornamental, not a wall of trees.
scatter_trees("wood-garden", 33, 47, -43, -18, 15, 4001)

# A few boulders reading as stone, well off the road and the doors — and
# placed before the tree scatter runs, so it seats the ground first.
boulder_prop("rock-1", -20, -42, "erratic-a", 9101)
boulder_prop("rock-2", 15, -40, "erratic-a", 9102)
boulder_prop("rock-3", -40, -66, "erratic-a", 9103)

# Paths: a solid three-colour dirt road down the main street, a worn track
# along the harder flank trail, and light ground cover in the clearing and
# the garden.
stroke_prop("street-main", [[-15, -78], [-4, -70], [0, -60], [0, -40], [0, -18]], 4,
            "solid", True, [DIRT, COARSE_DIRT, SPRUCE_PLANKS], 6001)
stroke_prop("trail-flank", [[-53, -70], [-53, -45], [-51, -20]], 2, "worn", True,
            [DIRT, COARSE_DIRT, GRAVEL], 6003, coverage=0.65)
stroke_prop("trail-garden", [[24, -35], [26, -25]], 2, "worn", True,
            [COARSE_DIRT, DIRT, GRAVEL], 6004, coverage=0.7)

flora_prop("cover-clearing", [[-30, -14], [10, -14], [10, -10], [-30, -10]], 0.5, 8, 7101)
flora_prop("cover-garden", [[32, -40], [48, -40], [48, -18], [32, -18]], 0.6, 7, 7102)

# ---------------------------------------------------------------------------
# ASSEMBLE
# ---------------------------------------------------------------------------

finish = {
    "authors": ["Sonnet 5"],
    "created": "2026-09-11",
    "themes": themes,
    "mapTheme": "emberwood-floor",
    "relief": relief,
    "addShapes": add_shapes,
    "roomStyles": room_styles,
    "dressing": {"styles": dressing_styles, "props": props},
}

with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as f:
    json.dump(finish, f, indent=2)

print(f"wrote {SLUG}.finish.json — {len(themes)} themes, {len(add_shapes)} addShapes, "
      f"{len(dressing_styles)} dressing styles, {len(props)} props")
