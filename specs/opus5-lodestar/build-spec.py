"""Lodestar Yard — a capture-the-wool board on a derelict orbital dock.

Three boards before this one were destroy boards, and a destroy board is not read for routes: there
is no wool to carry back, so the two sides never meet at a definite place and `01-flow.txt` says as
much and stops. This one is wool, which is what makes the flow read say something — a split, a merge,
and the ground each of them passes.

The look is the second thing it is for. The three before it painted ground that grows: a bog, a
badlands, a meadow. A station has no soil, so every ground here is a *made* surface and the patterns
that state one are the ones the earlier boards had no use for — a `voronoi` of hull plate, a
`teamTint` that reads its own owner's colour out of the cell, an `electric` filament of lit seams,
and a `checker` deck. None of the four appears on any of the other three.
"""

import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-lodestar"
CELL = 5
SURFACE = 20

# ── blocks ──────────────────────────────────────────────────────────────────────
STONE, COBBLE = 1, 4
GLASS, LAPIS, SANDSTONE = 20, 22, 24
WOOL, IRON_BLOCK, DOUBLE_SLAB = 35, 42, 43
BRICK, MOSSY_COBBLE, OBSIDIAN = 45, 48, 49
GLOWSTONE, STONE_BRICK, IRON_BARS = 89, 98, 101
GLASS_PANE, NETHER_BRICK, END_STONE = 102, 112, 121
QUARTZ, STAINED_GLASS, HARDENED_CLAY = 155, 95, 172
STAINED_CLAY, COAL_BLOCK, PRISMARINE = 159, 173, 168
STONE_SLAB, QUARTZ_SLAB, STONE_BRICK_STAIRS, QUARTZ_STAIRS = 44, 44, 109, 156
SEA_LANTERN, PACKED_ICE = 169, 174

# stone data nibbles
ANDESITE, POLISHED_ANDESITE, DIORITE, POLISHED_DIORITE = 5, 6, 3, 4
# stone-brick nibbles
MOSSY_BRICK, CRACKED_BRICK, CHISELLED_BRICK = 1, 2, 3
# quartz nibbles
CHISELLED_QUARTZ, PILLAR_QUARTZ = 1, 2
# stone-slab nibbles
STONE_SLAB_D, SANDSTONE_SLAB, COBBLE_SLAB, BRICK_SLAB, STONE_BRICK_SLAB, QUARTZ_SLAB_D = 0, 1, 3, 4, 5, 7
# dye nibbles
WHITE, ORANGE, MAGENTA, LIGHT_BLUE, YELLOW, LIME, PINK, GRAY = 0, 1, 2, 3, 4, 5, 6, 7
LIGHT_GRAY, CYAN, PURPLE, BLUE, BROWN, GREEN, RED, BLACK = 8, 9, 10, 11, 12, 13, 14, 15


def solid(block_id, data=0):
    """A material. `kind` first, always — it is read positionally on an older build."""
    return {"kind": "solid", "id": block_id, "data": data}


def noise(seed, scale, stops, octaves=3, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": stops, "rise": rise}


def voronoi(seed, size, *pairs, rise=0):
    """Straight-edged convex cells about `size` across — a plated hull rather than a weathered one.

    It is the pattern the three earlier boards had no use for: every ground they painted was
    something that grew, and a voronoi's hard edges read as a seam somebody welded.

    Each pair is one `VoronoiBand` — a material and how many blocks inward from the cell boundary it
    runs, with the last band's depth ignored because it takes whatever is left of the cell. A bare
    list of materials is accepted by `PUT /sketch` and then throws in the painter, so the pairs are
    stated here rather than at every call site.
    """
    return {"kind": "voronoi", "seed": seed, "cellSize": size, "rise": rise,
            "bands": [{"material": material, "depth": depth} for material, depth in pairs]}


def electric(seed, scale, stops, octaves=3, rise=0):
    """The fold inverted: thin branching filaments with everything else fallen away from them."""
    return {"kind": "electric", "seed": seed, "scale": scale, "octaves": octaves,
            "stops": stops, "rise": rise}


def checker(size, even, odd):
    return {"kind": "checker", "size": size, "even": even, "odd": odd}


def team_tint(block_id, neutral):
    """The bucket's block dyed by whichever team owns the cell, on wool's own 0-15 scale.

    A neutral cell falls back to `neutral`, which is why the mid of this board reads grey while both
    docks read their own colour out of the same one material.
    """
    return {"kind": "teamTint", "blockId": block_id, "neutral": neutral}


def wall_frame(edge, fill, angle=40, thickness=1):
    return {"kind": "wallFrame", "edge": edge, "fill": fill, "angle": angle,
            "thickness": thickness}


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


# ── geometry ────────────────────────────────────────────────────────────────────
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


DOCK_BOX = (-60, -100, 60, -35)
SPINE_BOX = (-30, -15, 30, 15)


def inside(ring, box, margin):
    min_x, min_z, max_x, max_z = box
    return [[min(max(x, min_x + margin), max_x - margin),
             min(max(z, min_z + margin), max_z - margin)] for x, z in ring]


def on_dock(ring, margin=6):
    return inside(ring, DOCK_BOX, margin)


def on_spine(ring, margin=6):
    return inside(ring, SPINE_BOX, margin)


# ══════════════════════════════════════════════════════════════════════════════
# THE PLAN
# ══════════════════════════════════════════════════════════════════════════════
# Seven pieces a team rather than one, and the shape is what two wool-board rules ask for.
#
# `FR6` caps a frontline's width at sixteen cells and names six to eight as the wool board's own
# figure — and it says why the three destroy boards before this one never met it: *"on a board played
# for cores or destroyables there is no width cap at all"*. So the deck cannot meet the void along
# its whole width. It meets it at one **neck** eight cells across, hung off a hub, which is the split
# frontline the rule describes.
#
# `STRUCT` will not have a wool room drawn inside another piece: *"wool room is unreachable: no land
# seam and no abutting build zone to enter by"*. A piece's rect is what it claims, so a room cut out
# of the middle of a deck is a hole with nothing to enter by. Each vault therefore **abuts** its own
# arm along fifteen blocks of shared edge, out on the flank where the arm ends.
#
# And `G8` reads fill ratio against the bounding box: a solid rectangle a side came out 0.773 against
# a band of [0.201, 0.542]. A yard built of arms with void between them is 0.375, and it is also what
# a dock looks like.
#
#   berth     x -15..15   z -100..-80   the spawn bay
#   hub       x -20..20   z  -80..-50   the deck behind the neck, where both arms meet
#   arm-w     x -45..-20  z  -75..-50   the west arm, out to its vault
#   arm-e     x  20..45   z  -75..-50   the east arm
#   vault-w   x -60..-45  z  -75..-50   the west wool room, abutting the arm's own end
#   vault-e   x  45..60   z  -75..-50   the east wool room
#   neck      x -20..20   z  -50..-35   the frontline: eight cells, and the only edge on the void
#   spine     x -30..30   z  -15..15    the neutral gantry
#   cross     x -20..20   z  -35..-15   the build zone, twenty blocks over nothing
#
#   spawn (0, -90) · wools at (-52, -62) and (52, -62)
#
# `maxPlayers` is 24 and it is an input rather than an afterthought: `G8` couples land per team
# to players per team, saturating near 175-185 blocks a player. 4 400 blocks of arm and deck a
# side is 183 a player at 24, which is where the corpus curve flattens.
PLAN = {
    "plan": 2,
    "meta": {"name": "Lodestar Yard",
             "notes": "CTW. Two wool bays a team on the ends of two arms, one neck onto the void, "
                      "and every ground on the board a plate somebody welded."},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 24,
                "surface": SURFACE, "observerY": 66},
    "pieces": [
        {"id": "berth", "role": "spawn", "rect": [-3, -20, 6, 4], "surface": SURFACE},
        {"id": "hub", "role": "piece", "rect": [-4, -16, 8, 6], "surface": SURFACE},
        {"id": "arm-w", "role": "piece", "rect": [-9, -15, 5, 5], "surface": SURFACE},
        {"id": "arm-e", "role": "piece", "rect": [4, -15, 5, 5], "surface": SURFACE},
        {"id": "vault-w", "role": "wool-room", "rect": [-12, -15, 3, 5], "surface": SURFACE},
        {"id": "vault-e", "role": "wool-room", "rect": [9, -15, 3, 5], "surface": SURFACE},
        {"id": "neck", "role": "piece", "rect": [-4, -10, 8, 3], "surface": SURFACE},
        {"id": "spine", "role": "piece", "rect": [-6, -3, 12, 6], "surface": SURFACE,
         "mirrors": False},
    ],
    "zones": [
        {"id": "cross", "rect": [-4, -7, 8, 4], "holes": []},
    ],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "berth", "at": [15, 10], "facing": "back",
                    "footprint": [8, 5, 14, 10]}],
        # `at` and `footprint` are both in BLOCKS from the piece's minimum corner, whatever the field
        # description says about cells — a spawn `at [10, 10]` on a twenty-block piece is its centre,
        # which it could not be in cells.
        "wools": [{"id": "wool-w", "piece": "vault-w", "at": [8, 13],
                   "footprint": [2, 4, 11, 17]},
                  {"id": "wool-e", "piece": "vault-e", "at": [7, 13],
                   "footprint": [2, 4, 11, 17]}],
        "iron": [],
        "destroyables": [],
        "cores": [],
    },
    "walls": [],
    "boxes": [],
}
# ══════════════════════════════════════════════════════════════════════════════
# THE FINISH
# ══════════════════════════════════════════════════════════════════════════════

# ── themes ──────────────────────────────────────────────────────────────────────
# A station has no soil, so nothing here is a ground that grew. The five grounds are five ways of
# stating a made surface, and the shares are what say which is the deck and which are markings on it.
#
# One `layered` stack is the `wall` bucket of every one of them, as `opus5-quiverstone`'s strata were
# of its: a cut through a deck shows plate, then insulation, then frame, then the dark of the hull,
# at the same courses wherever the cut is. It is in `fill` too, so a cut face is banded all the way
# down rather than banded in its top four courses.
HULL_WALL = layered(bands(
    (solid(QUARTZ), 1),
    (solid(IRON_BLOCK), 1),
    (solid(STONE_BRICK, CHISELLED_BRICK), 2),
    (solid(STAINED_CLAY, LIGHT_GRAY), 3),
    (solid(STONE_BRICK), 4),
    (solid(COAL_BLOCK), 6),
), beyond=solid(OBSIDIAN))

THEMES = {
    # the deck: a voronoi of hull plate. Straight-edged convex cells about seven blocks across, which
    # is a plate somebody welded rather than a stone somebody weathered
    "plate": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(voronoi(701, 7,
                               (solid(STONE_BRICK, CHISELLED_BRICK), 1),
                               (solid(STAINED_CLAY, LIGHT_GRAY), 1),
                               (solid(STONE, POLISHED_ANDESITE), 2),
                               (solid(STONE, ANDESITE), 2),
                               (solid(STAINED_CLAY, GRAY), 1)), 2),
        "wall": HULL_WALL,
        "wallEnabled": True,
        "fill": HULL_WALL,
        "rim": top(solid(STONE_BRICK, CHISELLED_BRICK), 1),
        "rimEdges": "void",
    },
    # the owned deck: one material that reads its own cell's team off the map. Both docks are painted
    # with this one theme and each comes out its own colour; the neutral fallback is what the gantry
    # would read if it were painted with it, which is why the fallback is grey rather than a dye
    "livery": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(checker(3,
                               team_tint(STAINED_CLAY, solid(STAINED_CLAY, LIGHT_GRAY)),
                               solid(STONE, POLISHED_ANDESITE)), 1),
        "wall": HULL_WALL,
        "wallEnabled": True,
        "fill": HULL_WALL,
        "rim": top(team_tint(WOOL, solid(STAINED_CLAY, LIGHT_GRAY)), 1),
        "rimEdges": "void",
    },
    # the lit seams: an electric field's thin branching filaments, glowstone in the middle of a ramp
    # of white clay. It is the one pattern that draws a line without an author drawing one
    "seam": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(electric(702, 11, [
            solid(STAINED_CLAY, GRAY),
            solid(STAINED_CLAY, LIGHT_GRAY),
            solid(QUARTZ),
            solid(SEA_LANTERN),
            solid(GLOWSTONE),
        ], octaves=4), 2),
        "wall": HULL_WALL,
        "wallEnabled": True,
        "fill": HULL_WALL,
        "rim": top(solid(QUARTZ), 1),
        "rimEdges": "void",
    },
    # the walkway: a checker two blocks on a side, which is a grating and not a pattern anyone would
    # mistake for ground
    "grating": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(checker(2, solid(STONE, POLISHED_DIORITE), solid(STONE_BRICK)), 1),
        "wall": HULL_WALL,
        "wallEnabled": True,
        "fill": HULL_WALL,
        "rim": top(solid(IRON_BLOCK), 1),
        "rimEdges": "void",
    },
    # the burnt deck: where the yard was cut apart. Nether brick, coal and cracked brick in a noise
    # field, and it is the only ground here that is not a colour somebody chose
    "scorch": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(noise(703, 8, [
            solid(COAL_BLOCK),
            solid(NETHER_BRICK),
            solid(STONE_BRICK, CRACKED_BRICK),
            solid(STONE, ANDESITE),
        ], octaves=4), 2),
        "wall": HULL_WALL,
        "wallEnabled": True,
        "fill": HULL_WALL,
        "rim": top(solid(NETHER_BRICK), 1),
        "rimEdges": "void",
    },
    # the gantries and masts, which are made things and never ground
    "strut": {
        "bedrock": {"relative": False, "value": 1},
        "wallOnTerrainFaces": True,
        "surface": top(wall_frame(solid(IRON_BLOCK), solid(STONE_BRICK, CHISELLED_BRICK)), 3),
        "wall": wall_frame(solid(IRON_BLOCK), solid(STONE_BRICK, CHISELLED_BRICK)),
        "wallEnabled": True,
        "fill": solid(STONE_BRICK),
        "rim": top(solid(IRON_BLOCK), 1),
        "rimEdges": "void",
    },
}




# ── relief ──────────────────────────────────────────────────────────────────────
# A deck is level, and a broken deck is level in pieces. So the marks pin five flats and there are
# **no pushes at all** — the only ground on this board that is not level is the four courses the
# berth's shelf stands above the deck, and the ramps that step down off it.
#
# That is the opposite choice from the three boards before, and it is deliberate: a push is applied
# after the marks, so a dish inside a pinned pad drops whatever is pinned there, and on a board this
# densely built there is nowhere a dish can go that nothing is standing in. A hull is machined, not
# weathered, and the interest here is the plates rather than the terrain.
mark_rng = random.Random(4411)

#   berthpad  x -13..13   z  -98..-82  h 24  the spawn bay's shelf, four courses over the deck
#   hubflat   x -18..18   z  -78..-52  h 20  the deck behind the neck
#   armflat   x -58..-22  z  -73..-52  h 20  each arm out to its vault's own floor, and its mirror
#   neckflat  x -18..18   z  -48..-37  h 20  the frontline
BERTHPAD = lobed_box(-13, -98, 13, -82, 6, 0.02, mark_rng)
HUBFLAT = lobed_box(-18, -78, 18, -52, 6, 0.02, mark_rng)
ARMFLAT_W = lobed_box(-58, -73, -22, -52, 6, 0.02, mark_rng)
ARMFLAT_E = lobed_box(22, -73, 58, -52, 6, 0.02, mark_rng)
NECKFLAT = lobed_box(-18, -48, 18, -37, 6, 0.02, mark_rng)

TEAM_MARKS = [
    {"id": "edge", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "berthpad", "kind": "area", "ring": BERTHPAD, "h": 24},
    {"id": "hubflat", "kind": "area", "ring": HUBFLAT, "h": SURFACE},
    # both arms are stated, not one mirrored: `rot_180` maps a west mark onto the *other* team's east
    # side, so a west-only mark would leave one arm a side unpinned
    {"id": "armflat-w", "kind": "area", "ring": ARMFLAT_W, "h": SURFACE},
    {"id": "armflat-e", "kind": "area", "ring": ARMFLAT_E, "h": SURFACE},
    {"id": "neckflat", "kind": "area", "ring": NECKFLAT, "h": SURFACE},
    # the three ways down off the berth's shelf: one to each arm and one to the neck
    {"id": "ramp-w", "kind": "line",
     "points": [[-8, -82], [-13, -80], [-16, -77], [-18, -74], [-20, -70]],
     "h": [24, 23, 22, 21, SURFACE], "r": 5},
    {"id": "ramp-e", "kind": "line",
     "points": [[8, -82], [13, -80], [16, -77], [18, -74], [20, -70]],
     "h": [24, 23, 22, 21, SURFACE], "r": 5},
    {"id": "ramp-mid", "kind": "line",
     "points": [[0, -82], [0, -80], [0, -78], [0, -76], [0, -72]],
     "h": [24, 23, 22, 21, SURFACE], "r": 4},
]

SPINE_MARKS = [
    {"id": "spine-edge", "kind": "rim", "h": SURFACE, "depth": 1},
    {"id": "spine-flat", "kind": "area",
     "ring": lobed_box(-27, -12, 27, 12, 6, 0.02, mark_rng), "h": SURFACE},
]

# `reach: 0` is unlimited, so a mark reaches as far as it needs and the solver reconciles the flats
# between them. `amplitude: 1` is the whole grain: one course of wobble is the difference between
# level and machined.
RELIEF = {
    "team": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "plain",
             "grain": {"seed": 4412, "scale": 26, "amplitude": 1},
             "marks": TEAM_MARKS, "pushes": []},
    "neutral": {"base": SURFACE, "reach": 0, "step": 1, "stairs": True, "landform": "plain",
                "grain": {"seed": 4413, "scale": 22, "amplitude": 1},
                "marks": SPINE_MARKS, "pushes": []},
}
# ── the erected plates: catwalks ────────────────────────────────────────────────
def plate(shape_id, min_x, min_z, max_x, max_z, absolute_top, theme):
    """A slab of deck standing at a stated absolute top, sheer on every side.

    `override` writes over whatever the relief solved, `height_mode: level` stands it at its own
    `base_height` rather than reading the ground, and `relief_scope: exclude` takes its footprint out
    of the group's solve so the surrounding deck is not dragged up to meet it.
    """
    return {"id": shape_id, "type": "rectangle", "operation": "add", "override": True,
            "min_x": min_x, "min_z": min_z, "max_x": max_x, "max_z": max_z,
            "floor": 0, "base_height": absolute_top, "height_mode": "level", "skirt": 0,
            "relief_scope": "exclude", "theme": theme}



# ── the made things: masts and solar wings ──────────────────────────────────────
def mast(name, cx, cz, height, seed):
    """A lattice mast: a thin square tower with a wider collar at its head.

    `made` rather than terrain for the reason every standing thing on these boards is: the build
    ceiling is the tallest *terrain* column plus twenty, and a made layer is out of that reckoning —
    so a forty-course mast does not hand the whole yard a ceiling above its own head.
    """
    rng = random.Random(seed)
    return [
        {"id": f"{name}-shaft", "name": f"{name} shaft", "base_y": 0,
         "kind": "made", "part_of": name, "seat": "ground",
         "shapes": [{"id": f"{name}-s0", "type": "rectangle", "operation": "add",
                     "min_x": cx - 2, "min_z": cz - 2, "max_x": cx + 2, "max_z": cz + 2,
                     "floor": 0, "base_height": height, "height_mode": "level", "skirt": 0,
                     "theme": "strut"}],
         "groups": [{"id": f"{name}-s0-g", "name": name, "mirrors": True,
                     "shapeIds": [f"{name}-s0"]}]},
        {"id": f"{name}-head", "name": f"{name} head", "base_y": height,
         "kind": "made", "part_of": name, "seat": "ground",
         "shapes": [{"id": f"{name}-h0", "type": "rectangle", "operation": "add",
                     "min_x": cx - 4 + rng.randint(0, 0), "min_z": cz - 4,
                     "max_x": cx + 4, "max_z": cz + 4,
                     "floor": 0, "base_height": 2, "height_mode": "level", "skirt": 0,
                     "theme": "strut"}],
         "groups": [{"id": f"{name}-h0-g", "name": name, "mirrors": True,
                     "shapeIds": [f"{name}-h0"]}]},
    ]


def wing(name, cx, cz, base_y, span, seed):
    """A solar wing: three flat panels on a spar, hanging out over the void.

    It hangs beyond the coast on purpose. Every projective read on this studio takes the topmost
    solid block and a made layer is solid, so a panel over walkable deck reports a barrier no player
    will ever meet. Height does not fix that at any altitude; being off every walkable column does.
    """
    rng = random.Random(seed)
    panels = []
    for index in range(3):
        offset = (index - 1) * (span + 3)
        panels.append({"id": f"{name}-{index}", "type": "rectangle", "operation": "add",
                       "min_x": cx - span // 2, "min_z": cz + offset - 4,
                       "max_x": cx + span // 2, "max_z": cz + offset + 4,
                       "floor": 0, "base_height": 2, "height_mode": "level", "skirt": 0,
                       "theme": "seam" if index == 1 else "plate"})
    spar = {"id": f"{name}-spar", "type": "rectangle", "operation": "add",
            "min_x": cx - 1, "min_z": cz - (span + 8), "max_x": cx + 1,
            "max_z": cz + (span + 8),
            "floor": 0, "base_height": 2, "height_mode": "level", "skirt": 0,
            "theme": "strut"}
    shapes = panels + [spar]
    return [{"id": name, "name": name, "base_y": base_y + rng.randint(0, 0),
             "kind": "made", "part_of": name, "shapes": shapes,
             "groups": [{"id": f"{name}-g", "name": name, "mirrors": True,
                         "shapeIds": [shape["id"] for shape in shapes]}]}]


# ── the buildings ───────────────────────────────────────────────────────────────
def plain_surface():
    return {"field": None, "border": None, "borderWidth": 1, "inlay": None,
            "inlayInset": 2, "isPlain": True}


def no_gable_windows():
    return {"form": "none", "block": GLASS_PANE, "hostBlock": -1, "hostData": 0,
            "data": 0, "sill": 2, "width": 1, "height": 1, "spacing": 3}


def berth_style():
    """The berth: the spawn bay. Iron over a quartz plinth, chiselled corner posts, an open lid.

    `hole: True` is what makes it a bay rather than a shed — a spawn a player drops into.
    """
    return {
        "foundation": {
            "plate": {"stack": bands((solid(QUARTZ), 1), (solid(IRON_BLOCK), 1),
                                     (solid(STONE_BRICK), 1)), "extent": 3},
            "surface": plain_surface(),
            "footing": solid(STONE_BRICK, CHISELLED_BRICK),
        },
        "roof": {
            "form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": False, "hole": True,
            "body": solid(IRON_BLOCK),
            "verge": solid(STONE_BRICK, CHISELLED_BRICK),
            "gable": solid(QUARTZ),
            "gableWindows": no_gable_windows(),
        },
        "wall": {"stack": bands((solid(QUARTZ), 2), (solid(STAINED_CLAY, LIGHT_GRAY), 1),
                                (solid(IRON_BLOCK), 4)), "extent": 7},
        "post": solid(STONE_BRICK, CHISELLED_BRICK),
        "windows": {"form": "pane", "block": STAINED_GLASS, "hostBlock": -1, "hostData": 0,
                    "data": LIGHT_BLUE, "sill": 3, "width": 2, "height": 2, "spacing": 3},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": STONE_BRICK_STAIRS, "fill": "upperSlab",
                             "fillBlock": STONE_SLAB, "fillData": STONE_BRICK_SLAB},
                    "width": 2, "height": 3},
    }


def vault_style():
    """The wool room: a quartz shell with a lit band and a flat iron lid.

    It is the one building on the board whose interior is what the map is played for, so the walls
    are the pale material and the band at eye height is the lit one — a room a player can find from
    across the deck.
    """
    walls = {"stack": bands((solid(STONE_BRICK, CHISELLED_BRICK), 2),
                            (solid(SEA_LANTERN), 1),
                            (solid(QUARTZ), 4)), "extent": 7}
    return {
        "foundation": {
            "plate": {"stack": bands((solid(QUARTZ), 1), (solid(STONE_BRICK), 1)), "extent": 2},
            "surface": plain_surface(),
            "footing": solid(QUARTZ),
        },
        "roof": {
            "form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": False, "hole": False,
            "body": solid(IRON_BLOCK),
            "verge": solid(STONE_BRICK, CHISELLED_BRICK),
            "gable": solid(QUARTZ),
            "gableWindows": no_gable_windows(),
        },
        "wall": walls,
        "post": solid(STONE_BRICK, CHISELLED_BRICK),
        "windows": {"form": "pane", "block": STAINED_GLASS, "hostBlock": -1, "hostData": 0,
                    "data": CYAN, "sill": 2, "width": 1, "height": 2, "spacing": 2},
        "storeys": [],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": QUARTZ_STAIRS, "fill": "upperSlab",
                             "fillBlock": STONE_SLAB, "fillData": QUARTZ_SLAB_D},
                    "width": 2, "height": 3},
    }


def shed_style():
    """A cargo shed: two storeys of grey clay banded in iron, flat lid, no posts.

    The `deck` of the upper storey is a bare material and not a band stack: it is one course, one
    owner, and handing it a `{stack, extent}` is a 500 whose only diagnostic is in the server log.
    """
    walls = {"stack": bands((solid(STAINED_CLAY, GRAY), 2), (solid(IRON_BLOCK), 1),
                            (solid(STAINED_CLAY, LIGHT_GRAY), 2)), "extent": 5}
    upper = {"clear": 3, "wall": walls, "post": solid(STONE_BRICK, CHISELLED_BRICK),
             "windows": {"form": "pane", "block": STAINED_GLASS, "hostBlock": -1, "hostData": 0,
                         "data": GRAY, "sill": 1, "width": 1, "height": 2, "spacing": 2},
             "surface": plain_surface(),
             "deck": solid(STONE_BRICK), "headroom": 3}
    return {
        "foundation": {
            "plate": {"stack": bands((solid(STONE_BRICK), 1), (solid(STONE_BRICK), 1)),
                      "extent": 2},
            "surface": plain_surface(),
            "footing": solid(STONE_BRICK),
        },
        "roof": {
            "form": "flat", "pitch": 1, "slab": -1, "slabData": 0, "overhang": 1,
            "ridgeCap": False, "hole": False,
            "body": solid(STAINED_CLAY, GRAY),
            "verge": solid(IRON_BLOCK),
            "gable": solid(STAINED_CLAY, GRAY),
            "gableWindows": no_gable_windows(),
        },
        "wall": walls,
        "post": solid(STONE_BRICK, CHISELLED_BRICK),
        "windows": {"form": "pane", "block": STAINED_GLASS, "hostBlock": -1, "hostData": 0,
                    "data": GRAY, "sill": 2, "width": 1, "height": 2, "spacing": 2},
        "storeys": [upper],
        "porch": None,
        "front": None,
        "beams": {"block": -1, "data": 0, "reach": 1, "any": False},
        "doorway": {"door": "air",
                    "head": {"form": "arched", "block": STONE_BRICK_STAIRS, "fill": "upperSlab",
                             "fillBlock": STONE_SLAB, "fillData": STONE_BRICK_SLAB},
                    "width": 2, "height": 3},
    }


# ── the copied bodies: what a station has instead of trees ──────────────────────
def crate_stack(rng, wide, high):
    """A stack of cargo crates, and it is a `tree`-kind prop because a copied body is the one recipe
    that writes an arbitrary block.

    Nothing on this board grows, so nothing on it is a tree. What a deck is dressed with is what was
    left standing on it, and the recipes that place a thing on the ground are the tree recipes.
    """
    cells = {}
    for course in range(high):
        span = max(1, wide - course)
        for dx in range(span):
            for dz in range(span):
                if rng.random() < 0.18 and course == high - 1:
                    continue
                block, data = ((STAINED_CLAY, ORANGE) if (dx + dz + course) % 3 == 0
                               else (STAINED_CLAY, GRAY) if (dx + dz) % 2 else (IRON_BLOCK, 0))
                cells[(dx, course, dz)] = (block, data)
    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def dish(rng, radius, mast_height):
    """A dish on a short mast: a bowl of quartz stairs on a chiselled stalk, lit at the focus."""
    cells = {}
    for course in range(mast_height):
        cells[(0, course, 0)] = (STONE_BRICK, CHISELLED_BRICK)
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            distance = abs(dx) + abs(dz)
            if distance > radius:
                continue
            lift = mast_height + (0 if distance < radius else 1)
            cells[(dx, lift, dz)] = (QUARTZ, 0) if distance else (SEA_LANTERN, 0)
    cells[(0, mast_height + 2, 0)] = (GLOWSTONE, 0)
    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def conduit(rng, length, axis_x):
    """A run of pipe lying on the deck, with a valve collar a third of the way along.

    The blocks are all axis-free, so nothing here needs the face-pair trick a vine needed: the orbit
    turns a log's axis and a stair's facing and leaves the rest alone, and none of these is either.
    """
    cells = {}
    for step in range(length):
        position = (step, 0, 0) if axis_x else (0, 0, step)
        cells[position] = (STAINED_CLAY, LIGHT_GRAY)
        if step == length // 3:
            for lift in range(2):
                collar = (step, lift, 0) if axis_x else (0, lift, step)
                cells[collar] = (IRON_BLOCK, 0)
    return [[x, y, z, block, data] for (x, y, z), (block, data) in sorted(cells.items())]


def debris(rng, spots):
    """Torn plate: a flat scatter of cracked brick and coal, one course, on the deck."""
    return [[x, 0, z, *(rng.choice([(STONE_BRICK, CRACKED_BRICK), (COAL_BLOCK, 0),
                                    (STONE, ANDESITE)]))]
            for x, z in spots]


body_rng = random.Random(4211)

STYLES = {
    "berth": {"kind": "house", "shell": berth_style()},
    "vault": {"kind": "house", "shell": vault_style()},
    "shed": {"kind": "house", "shell": shed_style()},
    "crate-1": {"kind": "tree", "form": "copied", "body": crate_stack(body_rng, 3, 3)},
    "crate-2": {"kind": "tree", "form": "copied", "body": crate_stack(body_rng, 2, 4)},
    "crate-3": {"kind": "tree", "form": "copied", "body": crate_stack(body_rng, 4, 2)},
    "dish-1": {"kind": "tree", "form": "copied", "body": dish(body_rng, 3, 4)},
    "dish-2": {"kind": "tree", "form": "copied", "body": dish(body_rng, 2, 6)},
    "conduit-x": {"kind": "tree", "form": "copied", "body": conduit(body_rng, 9, True)},
    "conduit-z": {"kind": "tree", "form": "copied", "body": conduit(body_rng, 9, False)},
    "debris-1": {"kind": "tree", "form": "copied",
                 "body": debris(body_rng, [(0, 0), (2, 1), (1, 3), (3, 2), (4, 0), (2, 4)])},
}




ADD_SHAPES = [
    # one high catwalk over each arm's back half: an attacker holds it and drops six courses onto the
    # arm, which is a drop taken freely and a climb that has to be placed for. The asymmetry is the
    # whole point of a high approach to a wool.
    plate("walk-w", -38, -72, -26, -66, 26, "grating"),
    plate("walk-e", 26, -72, 38, -66, 26, "grating"),
    # and the cut across the neck, level with the deck so it is a colour rather than an obstacle
    plate("cut-w", -18, -40, -6, -37, SURFACE, "scorch"),
    plate("cut-e", 6, -40, 18, -37, SURFACE, "scorch"),
]


ADD_LAYERS = (
    # one mast on each arm, standing on the catwalk it rises through, and one on the gantry. A made
    # layer is out of the build-ceiling reckoning — the ceiling is the tallest *terrain* column plus
    # twenty — so a forty-course mast does not hand the yard a ceiling above its own head.
    mast("mast-w", -32, -70, 26, 61)
    + mast("mast-e", 32, -70, 30, 62)
    + mast("mast-mid", -24, -10, 34, 65)
    # the solar wings, hanging over the void between each arm and the gantry. They are out there for
    # a measurement reason and not a picture one: every projective read takes the topmost solid block
    # and a made layer is solid, so a panel over walkable deck reports a barrier no player will meet.
    + wing("wing-w", -40, -34, 42, 10, 71)
    + wing("wing-e", 40, -34, 48, 10, 72)
    + wing("wing-fw", -48, -20, 52, 8, 73)
    + wing("wing-fe", 48, -20, 56, 8, 74)
)


# ── the dressing ────────────────────────────────────────────────────────────────
# The walkway's own paving: a voronoi of two plates, so the line reads as laid rather than worn
WALK_PAVE = voronoi(711, 4,
                    (solid(QUARTZ), 1),
                    (solid(STONE, POLISHED_DIORITE), 2),
                    (solid(STAINED_CLAY, LIGHT_GRAY), 1))

PROPS = []

# the walkways: the berth's own door out along each arm to its vault, and one down the middle to the
# neck. Each arm leg runs down the arm's centre in z, which is what leaves the arm's front strip
# clear for props — a `route` stroke wants five and a half blocks off its centreline, and an arm
# twenty-five deep has room for exactly one line and one row of things beside it.
PROPS.append({"id": "walk-w", "kind": "stroke", "seed": 41, "radius": 2.5, "style": "solid",
              "coverage": 1.0, "route": True, "pave": WALK_PAVE,
              "points": [[-8, -82], [-13, -78], [-17, -73], [-21, -67], [-28, -63], [-36, -62],
                         [-44, -62]]})
PROPS.append({"id": "walk-e", "kind": "stroke", "seed": 42, "radius": 2.5, "style": "solid",
              "coverage": 1.0, "route": True, "pave": WALK_PAVE,
              "points": [[8, -82], [13, -78], [17, -73], [21, -67], [28, -63], [36, -62],
                         [44, -62]]})
PROPS.append({"id": "walk-neck", "kind": "stroke", "seed": 43, "radius": 2.5, "style": "solid",
              "coverage": 1.0, "route": True, "pave": WALK_PAVE,
              "points": [[0, -82], [0, -74], [0, -64], [0, -54], [0, -44], [0, -37]]})
PROPS.append({"id": "walk-spine", "kind": "stroke", "seed": 44, "radius": 2.5, "style": "solid",
              "coverage": 1.0, "route": True, "pave": WALK_PAVE,
              "points": [[0, -13], [0, -4], [0, 4], [0, 13]]})

# the sheds: two on the neck, either side of the causeway, and one on the gantry
PROPS.append({"id": "shed-w", "kind": "house", "seed": 441,
              "wings": [{"corners": [[-16, -46], [-10, -41]]}], "front": "posX",
              "style": "shed"})
PROPS.append({"id": "shed-e", "kind": "house", "seed": 442,
              "wings": [{"corners": [[10, -46], [16, -41]]}], "front": "negX",
              "style": "shed"})
PROPS.append({"id": "shed-mid", "kind": "house", "seed": 443,
              "wings": [{"corners": [[-12, -6], [-4, 1]]}], "front": "posZ",
              "style": "shed"})

# what a deck is dressed with. Every one is a copied body, because nothing on a station grows and a
# copied body is the one recipe that writes an arbitrary block. All of them sit at |z| > 35, so none
# can meet its own rot_180 image — which is what makes a dock affordable where the gantry is not.
#
# Six, and it was eight. The berth is nothing but ground `DR-KEEP` holds clear for a spawn, the hub's
# back corners are inside the spline the berth's own walkway overshoots into (`DR-ROAD`, three blocks
# either side of a road), and the arm's front strip is the debris pile's. A deck this densely walked
# has six places for a thing to stand, and the answer to the seventh is not to move it again.
DOCK_DRESS = [
    ("crate-hw", "crate-3", -16, -57),
    ("crate-he", "crate-3", 16, -57),
    ("dish-w", "dish-1", -34, -54),
    ("dish-e", "dish-2", 34, -54),
    ("scrap-w", "debris-1", -26, -58),
    ("scrap-e", "debris-1", 26, -58),
]
for index, (name, style, x, z) in enumerate(DOCK_DRESS):
    PROPS.append({"id": name, "kind": "tree", "seed": 3100 + index * 7,
                  "x": x, "z": z, "style": style})

# the gantry carries four, and four is the count rather than eight: a stated prop is two footprints,
# and `opus5-quiverstone` measured that a landmass this size cannot place the sixth clear of the
# fifth's image. Every pair here, and every pair of images, is fourteen blocks apart or more.
SPINE_DRESS = [("dish-mid", "dish-1", -24, 4),
               ("pipe-mid", "conduit-x", 14, -12)]
for index, (name, style, x, z) in enumerate(SPINE_DRESS):
    PROPS.append({"id": name, "kind": "tree", "seed": 3200 + index * 11,
                  "x": x, "z": z, "style": style})


# ── the paint, as patches ───────────────────────────────────────────────────────
def patch(shape_id, ring, theme):
    """A splotch: an ordinary one-course add, so a taller add keeps the height and the smallest
    shape keeps the colour."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
            "vertices": ring, "theme": theme}


paint_rng = random.Random(4511)

# `livery` sits round each berth and down each arm, which is where a dock's own colours belong: it is
# one material reading its cell's owner, so both docks are painted with the same theme and each comes
# out its own. The gantry is never painted with it — a neutral cell falls back to the grey and the
# point of the material is lost.
PAINT = [
    patch("livery-berth", on_dock(lobed_ring(0, -90, 12, 7, 13, 0.10, paint_rng)), "livery"),
    patch("livery-w", on_dock(lobed_ring(-30, -62, 11, 9, 11, 0.14, paint_rng)), "livery"),
    patch("livery-e", on_dock(lobed_ring(30, -62, 11, 9, 11, 0.14, paint_rng)), "livery"),
    # the lit seams: an electric field's filaments, laid where the deck was welded back together
    patch("seam-hub", on_dock(lobed_ring(0, -64, 16, 11, 13, 0.12, paint_rng)), "seam"),
    patch("seam-mid", on_spine(lobed_ring(0, 0, 22, 8, 13, 0.10, paint_rng)), "seam"),
    # and the burn, across the neck where the yard was cut apart, and at the gantry's own ends
    patch("scorch-neck", on_dock(lobed_ring(0, -43, 16, 5, 11, 0.16, paint_rng)), "scorch"),
    patch("scorch-mid-w", on_spine(lobed_ring(-21, 0, 6, 9, 11, 0.16, paint_rng)), "scorch"),
    patch("scorch-mid-e", on_spine(lobed_ring(21, 0, 6, 9, 11, 0.16, paint_rng)), "scorch"),
    # the grating: each walkway's own band, wider than the stroke laid on it
    patch("grate-w", on_dock(lobed_ring(-32, -63, 12, 4, 11, 0.12, paint_rng)), "grating"),
    patch("grate-e", on_dock(lobed_ring(32, -63, 12, 4, 11, 0.12, paint_rng)), "grating"),
    patch("grate-neck", on_dock(lobed_ring(0, -74, 4, 11, 11, 0.12, paint_rng)), "grating"),
]


FINISH = {
    "themeById": {},
    # a hull's edge is cut, not weathered, so the coasts bend by three and no more
    "bendShapes": {"arm-e-20": {"k": 0.12, "wander": 3, "step": 16, "seed": 7},
                   "spine-20": {"k": 0.10, "wander": 2, "step": 12, "seed": 9}},
    "addShapes": ADD_SHAPES + PAINT,
    "addLayers": ADD_LAYERS,
    "relief": RELIEF,
    "themes": THEMES,
    "mapTheme": "plate",
    # desert with hill specks: no rain on a hull, no snow to bury the paint, and a two-value field so
    # the sky is not one flat colour. The board's colour is stated in blocks, so a biome that
    # re-tinted anything would be arguing with the paint.
    "biome": {"kind": "noise", "seed": 23, "scale": 34, "octaves": 2, "stops": [2, 2, 3, 2]},
    # `cage` is the wool room's shell and `spawn` the berth's — the two rooms the studio stamps
    # itself from the plan's pieces rather than from a prop
    "roomStyles": {"spawn": berth_style(), "cage": vault_style()},
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
    copied = sum(1 for prop in PROPS if prop["kind"] == "tree")
    print(f"{SLUG}: {len(PLAN['pieces'])} pieces · {len(ADD_SHAPES)} plates · {len(PAINT)} patches · "
          f"{len(ADD_LAYERS)} made layers · {len(THEMES)} themes · "
          f"{len(PROPS)} props ({copied} copied bodies) · {len(STYLES)} recipes")


if __name__ == "__main__":
    main()
