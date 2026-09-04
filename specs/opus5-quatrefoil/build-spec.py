#!/usr/bin/env python3
"""Quatrefoil — a four-team capture board on one rot_90 island.

Four wooded corner quarters, four pale sand spits on the axes, and a high angular keep in the middle
that every route crosses and nobody owns. The quarters are natural: a mossy grey-green moor over
coffee-dark earth, rolled by pushes rather than pinned by marks. The keep is made: a stepped platform
of pale courses with a prismarine band through its face, a ramp up each side, and planted beds and
trees that let it go green at the edges.

Writes <slug>.plan.json and <slug>.finish.json beside this file. Nothing here reads a built world.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SLUG = "opus5-quatrefoil"
CELL = 2

# ── the palette ───────────────────────────────────────────────────────────────────────────────────
# Five colours, each read off `GET /api/terrain/blocks` for the nearest block that is ground rather
# than a stated shade — stained clay, wool and glass are shade rows and never terrain.
#   muted teal  #ABC4AB  mossy cobblestone #6e7b62 · mossy stone brick #74796a · prismarine brick #63a08f
#   camel       #A39171  coarse dirt #7e5a3c · birch planks #c4b078 · brown mushroom block #bfaf95
#   pale oak    #DCC9B6  mushroom stem #cbc4ab · smooth sandstone #d8cea0 · sandstone #d9cfa1
#   grey        #727D71  mossy cobblestone · cobblestone #7a7a7a · stone #7e7e7e · stone brick
#   coffee bean #6D4C3D  podzol #5d421f · spruce planks #725430 · dark oak planks #422b14
MOSS      = {"kind": "solid", "id": 48,  "data": 0}
MOSSBRICK = {"kind": "solid", "id": 98,  "data": 1}
COBBLE    = {"kind": "solid", "id": 4,   "data": 0}
STONE     = {"kind": "solid", "id": 1,   "data": 0}
ANDESITE  = {"kind": "solid", "id": 1,   "data": 5}
BRICK     = {"kind": "solid", "id": 98,  "data": 0}
CHISELLED = {"kind": "solid", "id": 98,  "data": 3}
COARSE    = {"kind": "solid", "id": 3,   "data": 1}
DIRT      = {"kind": "solid", "id": 3,   "data": 0}
PODZOL    = {"kind": "solid", "id": 3,   "data": 2}
GRAVEL    = {"kind": "solid", "id": 13,  "data": 0}
SANDSTONE = {"kind": "solid", "id": 24,  "data": 0}
SMOOTH    = {"kind": "solid", "id": 24,  "data": 2}
SAND      = {"kind": "solid", "id": 12,  "data": 0}
STEM      = {"kind": "solid", "id": 99,  "data": 15}
PRISM     = {"kind": "solid", "id": 168, "data": 1}
DARKPRISM = {"kind": "solid", "id": 168, "data": 2}

# ── heights ───────────────────────────────────────────────────────────────────────────────────────
# One concentric rise from the corner spawns inward. Every LAND seam steps by a single block, so no
# seam wants a ramp; the one stated step is the keep's own wall, and that is a carved flight.
H_YARD, H_MARCH, H_SHELF, H_ROOM = 8, 9, 10, 11
H_SPIT_OUT, H_SPIT_MID, H_SPIT_IN = 7, 8, 9
H_APRON, H_KEEP = 13, 18
H_TIER1, H_TIER2, H_TIER3 = 19, 20, 21

# ── the plan ──────────────────────────────────────────────────────────────────────────────────────
# The authored unit is the north-west quarter, the west spit and the keep; rot_90 fans it four ways.
PIECES = [
    # the quarter — a spawn compound, the protection region standing in the middle of its own yard,
    # because a 40-block region is a field of immunity a team cannot be fought out of (ST10)
    ("spawn",        "spawn",     [-48, -48, 10, 10], H_YARD),
    ("yard-e",       "piece",     [-38, -48, 10, 10], H_YARD),
    ("yard-s",       "piece",     [-48, -38, 20, 10], H_YARD),
    # the two marches out of the compound, one to each spit
    ("march-s",      "piece",     [-45, -28, 13, 15], H_MARCH),
    ("march-e",      "piece",     [-28, -45, 15, 13], H_MARCH),
    # the shelf the wool room stands on — ground on all four sides, or the room's bedrock plinth
    # stands in the open
    ("wool-app-w",   "piece",     [-32, -25,  7, 10], H_SHELF),
    ("wool-app-n",   "piece",     [-25, -32, 10,  7], H_SHELF),
    ("wool",         "wool-room", [-25, -25, 10, 10], H_ROOM),
    ("wool-ledge-e", "piece",     [-15, -25,  3, 10], H_SHELF),
    ("wool-ledge-s", "piece",     [-25, -15, 13,  3], H_SHELF),
    # the west spit, on the axis of symmetry
    ("arm-outer",    "piece",     [-49,  -5,  4, 10], H_SPIT_OUT),
    ("arm-mid",      "piece",     [-45,  -5, 13, 10], H_SPIT_MID),
    ("arm-inner",    "piece",     [-32,  -5,  8, 10], H_SPIT_IN),
    ("keep-apron",   "piece",     [-18,  -5,  8, 10], H_APRON),
    # the keep, its own image under rot_90
    ("keep",         "piece",     [-10, -10, 20, 20], H_KEEP),
]

ZONES = [
    # the spit crossing: one region lapping the spit and both quarter gaps either side of it
    ("bz-arm",   [-45, -13, 13, 26]),
    # the spit's inner hop onto the keep apron
    ("bz-cross", [-26,  -5, 11, 10]),
    # the raid: apron down into the next quarter's wool shelf
    ("bz-raid",  [-18, -12,  7,  7]),
]


def plan():
    return {
        "plan": 2,
        "meta": {"name": "Quatrefoil"},
        "globals": {"cell": CELL, "symmetry": "rot_90", "maxPlayers": 12,
                    "surface": 9, "observerY": 38},
        "pieces": [{"id": i, "role": r, "rect": rect, "surface": s} for i, r, rect, s in PIECES],
        "zones": [{"id": i, "rect": rect, "holes": []} for i, rect in ZONES],
        "placements": {
            # no footprint on either room: WX1's default follows the facing, and a stated one does not
            "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [10, 12], "facing": "back"}],
            "wools":  [{"id": "wool-1", "piece": "wool", "at": [10, 10]}],
            "iron":   [{"id": "iron-1", "piece": "spawn", "at": [10.5, 18.5]}],
            "destroyables": [], "cores": [],
        },
        "walls": [], "boxes": [],
    }


# ── themes ────────────────────────────────────────────────────────────────────────────────────────
def cell_pattern(seed, size, palette, rise=None, jitter=60, warp=2):
    out = {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
           "palette": palette}
    if rise is not None:
        out["rise"] = rise
    return out


def layered(bands, beyond):
    return {"kind": "layered", "axis": "depth", "beyond": beyond,
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def theme(surface_bands, wall_bands, fill, rim=None, rim_edges="void", depth=4):
    out = {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": rim_edges,
        "wallOnTerrainFaces": True,
        "rim": {"enabled": rim is not None, "depth": 1, "material": rim or COBBLE},
        "surface": {"enabled": True, "depth": depth,
                    "material": layered(surface_bands, wall_bands[-1][0])},
        "wall": layered(wall_bands[:-1], wall_bands[-1][0]),
        "wallEnabled": True,
        "fill": fill,
    }
    return out


THEMES = {
    # the quarters: a mossy grey-green turf over coffee-dark earth. Two materials in the top course,
    # not a family — the mottle is moss against bare earth and nothing else.
    "moor": theme(
        surface_bands=[(cell_pattern(11, 9, [MOSS, MOSS, COARSE]), 1), (DIRT, 2), (COARSE, 1)],
        wall_bands=[(MOSS, 1), (COARSE, 2), (DIRT, 2), (STONE, 4), (ANDESITE, 1)],
        fill=cell_pattern(21, 9, [STONE, STONE, ANDESITE], rise=5)),
    # the patches worn into it: bare earth under the trees, and the trodden ground along a route
    "brake": theme(
        surface_bands=[(cell_pattern(13, 7, [PODZOL, COARSE]), 1), (DIRT, 2)],
        wall_bands=[(PODZOL, 1), (COARSE, 2), (STONE, 4), (ANDESITE, 1)],
        fill=cell_pattern(21, 9, [STONE, STONE, ANDESITE], rise=5), depth=3),
    # the four spits: pale sand, the board's own rim, and the one ground that is not the moor
    "strand": theme(
        surface_bands=[(cell_pattern(17, 11, [SANDSTONE, SANDSTONE, SAND, GRAVEL]), 1), (SANDSTONE, 2)],
        wall_bands=[(SANDSTONE, 1), (SMOOTH, 3), (SANDSTONE, 4), (STONE, 1)],
        fill=cell_pattern(23, 11, [SMOOTH, SANDSTONE], rise=5), depth=3),
    # the keep: made, and made of something the ground is not. Courses rather than a field — a
    # chiselled kerb on every drop, a paved deck, and a prismarine band through the face.
    "keep": theme(
        surface_bands=[({"kind": "checker", "size": 4, "even": SMOOTH, "odd": SANDSTONE}, 1),
                       (BRICK, 1), (STONE, 1)],
        wall_bands=[(CHISELLED, 1), (SMOOTH, 2), (PRISM, 1), (BRICK, 4), (ANDESITE, 1)],
        fill=cell_pattern(31, 9, [BRICK, STONE], rise=5),
        rim=CHISELLED, rim_edges="drop", depth=3),
}


# ── rings ─────────────────────────────────────────────────────────────────────────────────────────
def lobed(cx, cz, rx, rz, points=11, wobble=0.16, phase=0.0):
    """A closed ring that is not a rectangle. An `area` mark's ring is a shape, and a rectangle
    builds a mesa with sheer sides that reads in the heightmap as a literal square."""
    ring = []
    for i in range(points):
        a = 2 * math.pi * i / points + phase
        r = 1.0 + wobble * math.sin(3 * a + phase * 2.3) + 0.5 * wobble * math.sin(5 * a + 1.1)
        ring.append([round(cx + rx * r * math.cos(a), 1), round(cz + rz * r * math.sin(a), 1)])
    return ring


def catmull(ring, divisor=6.0):
    """Catmull-Rom handles over a closed ring — tangent-continuous at every vertex, which a
    per-edge bulge is not: that recipe is right for one corner and draws a gear round a ring."""
    n = len(ring)
    controls = {}
    for i in range(n):
        p0, p1, p2 = ring[(i - 1) % n], ring[i], ring[(i + 1) % n]
        tx, tz = (p2[0] - p0[0]) / divisor, (p2[1] - p0[1]) / divisor
        controls[str(i)] = {"in": [round(p1[0] - tx, 2), round(p1[1] - tz, 2)],
                            "out": [round(p1[0] + tx, 2), round(p1[1] + tz, 2)]}
    return controls


# ── the relief ────────────────────────────────────────────────────────────────────────────────────
# A mark is a constraint honoured exactly; only ground a player has to arrive at is pinned. Every
# landform is a push, because a mark with a radius builds a drum and not a hill.
RELIEF = {
    "team": {
        "base": 9, "reach": 0, "step": 1, "stairs": True,
        "grain": {"amplitude": 1.4, "scale": 23, "seed": 7},
        "marks": [
            # the ground outside the spawn door, so the egress is level whatever the pushes do
            {"id": "door-apron", "kind": "area", "h": 8,
             "ring": lobed(-84, -70, 13, 8, points=9, wobble=0.12)},
        ],
        "pushes": [
            # the bank at the team's back — the map's own corner, behind the compound. Its skirt is
            # kept off the spawn piece: a push is applied after every constraint, so a skirt across
            # the room lifts the pad the room is stamped on.
            {"id": "bank-w", "ring": lobed(-91, -66, 5, 8, points=11, wobble=0.10),
             "amounts": [5, 6, 6, 5, 5, 5, 6, 6, 5, 5, 5], "crown": 2, "falloff": 7,
             "roughness": 1, "seed": 41},
            {"id": "bank-n", "ring": lobed(-66, -91, 8, 5, points=11, wobble=0.10, phase=0.6),
             "amounts": [5, 6, 6, 5, 5, 5, 6, 6, 5, 5, 5], "crown": 2, "falloff": 7,
             "roughness": 1, "seed": 43},
            # the south march carries a swell and the east march a dell, so a team's two ways out of
            # its own compound are a high road and a low one
            # A range is a wall unless its two gradients agree: 5 over a 11-block skirt is 0.45 a block
            # outside the ring, and a crown of 3 over the ring's ~8-block half-width is 0.37 inside it.
            {"id": "swell-south", "ring": lobed(-78, -45, 9, 8, points=13, wobble=0.10),
             "amounts": [5, 5, 6, 6, 5, 5, 5, 5, 6, 6, 5, 5, 5], "crown": 3, "falloff": 11,
             "roughness": 1, "seed": 17},
            # The same shape dished: a negative crown makes a corrie of the ring rather than a dome.
            {"id": "dell-east", "ring": lobed(-45, -78, 9, 8, points=13, wobble=0.10, phase=0.7),
             "amounts": [3, 3, 2, 2, 3, 3, 3, 2, 2, 3, 3, 3, 3], "crown": -4, "falloff": 10,
             "roughness": 1, "seed": 23},
            # the spit is crowned down its middle, so it reads as a bar of sand rather than a deck
            {"id": "spit-crown",
             "ring": [[-96, -3], [-74, -4], [-56, -3], [-52, 0], [-56, 3], [-74, 4], [-96, 3],
                      [-98, 0]],
             "amounts": [4, 5, 5, 4, 4, 5, 5, 4], "crown": 2, "falloff": 8, "roughness": 1,
             "seed": 29},
            # a knap on the wool shelf's outer shoulder, so the raid landing is overlooked
            {"id": "shelf-knap", "ring": lobed(-58, -58, 6, 6, points=9, wobble=0.18),
             "amounts": [3, 3, 4, 3, 3, 3, 4, 3, 3], "crown": 2, "falloff": 6, "roughness": 1,
             "seed": 37},
        ],
    }
}


# ── authored shapes ───────────────────────────────────────────────────────────────────────────────
def brush(shape_id, ring, theme_name, divisor=6.0):
    """A paint patch on solved ground: an ordinary one-course add, never an override. Paint scopes to
    the smallest shape over a cell so the patch wins the colour, and the taller add wins the column
    so it can never lower what it is painted on."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0, "base_height": 1,
            "vertices": ring, "controls": catmull(ring, divisor), "theme": theme_name}


def slab(shape_id, x0, z0, x1, z1, height, theme_name):
    """A made terrace: flat, sheer, and out of the elevation model."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0,
            "base_height": height, "skirt": 0, "relief_scope": "exclude", "theme": theme_name,
            "vertices": [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]}


def bay(shape_id, ring):
    """A bite out of the coast. A subtract beats every add on its layer, so one is drawn only on an
    outer edge — never across a seam a player walks or a face a build zone docks."""
    return {"id": shape_id, "type": "polygon", "operation": "subtract", "floor": 0,
            "vertices": ring, "controls": catmull(ring, 5.0)}


ADD_SHAPES = [
    # ── the keep: a stepped platform, four ramps, four corner bastions ───────────────────────────
    # the ramp up each face — 5 courses over 16 blocks, which is a course every third block and a
    # walk that costs nothing either way. A rise wants twice its run before it stops building treads
    # of two.
    {"id": "keep-ramp", "type": "polygon", "operation": "add", "floor": 0, "base_height": H_APRON,
     "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "theme": "keep",
     "vertices": [[-36, -5], [-20, -5], [-20, 5], [-36, 5]],
     "anchor_heights": [H_APRON, H_KEEP, H_KEEP, H_APRON]},
    # three concentric terraces, each a single walkable riser over the one below
    slab("keep-t1", -14, -14, 14, 14, H_TIER1, "keep"),
    slab("keep-t2", -8, -8, 8, 8, H_TIER2, "keep"),
    slab("keep-t3", -3, -3, 3, 3, H_TIER3, "keep"),
    # a bastion on each corner of the deck, one riser up — cover on a platform that is otherwise a
    # table, and the shape that makes the keep read as built from across the board
    slab("keep-bastion", -19, -19, -12, -12, H_TIER2, "keep"),
    # ── what lets the keep go green ──────────────────────────────────────────────────────────────
    # planted beds cut into the deck, in the ground's own earth, so the flora overlay has soil to
    # take. A bed is an ordinary one-course add and is safe over excluded ground.
    brush("keep-bed-w", lobed(-17, -10, 3, 4, points=8, wobble=0.14), "brake"),
    brush("keep-bed-n", lobed(-10, -17, 4, 3, points=8, wobble=0.14, phase=0.8), "brake"),
    # ── the quarters: patches of bare earth worn into the moor ───────────────────────────────────
    brush("brake-march-s", lobed(-80, -40, 9, 8, points=11, wobble=0.22), "brake"),
    brush("brake-march-e", lobed(-40, -80, 8, 9, points=11, wobble=0.22, phase=0.9), "brake"),
    brush("brake-yard", lobed(-70, -66, 8, 6, points=9, wobble=0.25, phase=1.7), "brake"),
    brush("brake-shelf", lobed(-38, -38, 6, 6, points=9, wobble=0.2, phase=2.4), "brake"),
    brush("dune-w", lobed(-82, 3, 9, 4, points=11, wobble=0.2, phase=1.2), "moor"),
    brush("dune-e", lobed(-59, -4, 7, 4, points=11, wobble=0.2, phase=2.8), "moor"),
    # ── the coast: three bites, all on outer edges, none on a seam or a crossing face ────────────
    bay("bay-yard-w", [[-99, -74], [-93, -71], [-92, -62], [-97, -59], [-101, -66]]),
    bay("bay-yard-n", [[-74, -99], [-71, -93], [-62, -92], [-59, -97], [-66, -101]]),
    bay("bay-march-w", [[-93, -50], [-87, -47], [-88, -39], [-93, -36], [-97, -43]]),
    bay("bay-march-n", [[-50, -93], [-47, -87], [-39, -88], [-36, -93], [-43, -97]]),
    bay("bay-cape", [[-101, -6], [-96, -4], [-95, 2], [-99, 5], [-103, 0]]),
]


# ── dressing ──────────────────────────────────────────────────────────────────────────────────────
DRESSING = {"props": [
    # the route out of each spawn door, across both marches to the wool shelf. A seam and a route
    # want `worn`, which is the one style that spends its coverage on a scatter; `rough` fills its
    # band solid and turns a track into a stripe.
    {"id": "track-south", "kind": "stroke", "seed": 70, "style": "worn", "coverage": 0.85,
     "radius": 2, "claimsGround": True,
     "points": [[-86, -77], [-86, -66], [-86, -56], [-85, -46], [-79, -37], [-69, -34], [-59, -33]],
     "pave": cell_pattern(83, 4, [GRAVEL, COARSE, COBBLE, GRAVEL], jitter=100, warp=0)},
    {"id": "track-east", "kind": "stroke", "seed": 71, "style": "worn", "coverage": 0.8,
     "radius": 2, "claimsGround": True,
     "points": [[-84, -75], [-72, -72], [-60, -71], [-50, -74], [-44, -78], [-39, -69], [-36, -59]],
     "pave": cell_pattern(84, 4, [GRAVEL, COARSE, COBBLE, GRAVEL], jitter=100, warp=0)},
    # the trodden crest of each spit — the lane every crossing runs along
    {"id": "spit-lane", "kind": "stroke", "seed": 72, "style": "worn", "coverage": 0.7,
     "radius": 3, "claimsGround": True,
     "points": [[-97, 1], [-86, -2], [-74, 1], [-62, -1], [-50, 0]],
     "pave": cell_pattern(85, 5, [GRAVEL, SANDSTONE, SAND, GRAVEL], jitter=100, warp=0)},
    {"id": "flora-spit", "kind": "flora", "seed": 254,
     "points": [[-98, -10], [-48, -10], [-48, 10], [-98, 10]],
     "spec": {"coverage": 0.3, "scale": 11, "octaves": 3, "fernShare": 0.2,
              "flowerShare": 0.04, "flowerScale": 15, "tallShare": 0.18}},
    # one lookout on the swell, timber against a mossy ground — a building is never the ground it
    # stands on
    {"id": "lookout", "kind": "house", "seed": 100, "front": "posZ", "style": "@wh-shed",
     "points": [[-80, -48], [-72, -40]]},
    # the wood on the dell's far shoulder, and singles on the swell
    {"id": "flora-marches", "kind": "flora", "seed": 250,
     "points": [[-88, -54], [-66, -54], [-66, -28], [-88, -28]],
     "spec": {"coverage": 0.34, "scale": 14, "octaves": 3, "fernShare": 0.45,
              "flowerShare": 0.06, "flowerScale": 19, "tallShare": 0.1}},
    {"id": "flora-dell", "kind": "flora", "seed": 251,
     "points": [[-54, -88], [-28, -88], [-28, -66], [-54, -66]],
     "spec": {"coverage": 0.38, "scale": 14, "octaves": 3, "fernShare": 0.5,
              "flowerShare": 0.08, "flowerScale": 19, "tallShare": 0.12}},
    # the keep's beds, where the deck was opened to the earth
    {"id": "flora-keep-w", "kind": "flora", "seed": 252,
     "points": [[-21, -15], [-13, -15], [-13, -5], [-21, -5]],
     "spec": {"coverage": 0.55, "scale": 7, "octaves": 2, "fernShare": 0.4,
              "flowerShare": 0.3, "flowerScale": 9, "tallShare": 0.1}},
    {"id": "flora-keep-n", "kind": "flora", "seed": 253,
     "points": [[-15, -21], [-5, -21], [-5, -13], [-15, -13]],
     "spec": {"coverage": 0.55, "scale": 7, "octaves": 2, "fernShare": 0.4,
              "flowerShare": 0.3, "flowerScale": 9, "tallShare": 0.1}},
]}

# the wood: birch on the swell, spruce round the dell, one pair of small birches in the keep's beds
TREES = [
    ("t-swell-1", -88, -32, "birch", 11), ("t-swell-2", -82, -32, "birch", 9),
    ("t-swell-3", -70, -52, "birch", 12), ("t-swell-4", -85, -31, "spruce", 10),
    ("t-dell-1", -32, -88, "spruce", 12), ("t-dell-2", -32, -82, "spruce", 10),
    ("t-dell-3", -48, -66, "spruce", 13), ("t-dell-4", -31, -85, "birch", 9),
    ("t-yard-1", -72, -64, "spruce", 11), ("t-yard-2", -64, -64, "spruce", 11),
    ("t-shelf-1", -70, -30, "birch", 9), ("t-shelf-2", -30, -70, "birch", 9),
    ("t-keep-w", -17, -10, "birch", 6), ("t-keep-n", -10, -17, "birch", 6),
    ("t-spit-1", -86, 6, "birch", 8), ("t-spit-2", -58, 7, "birch", 7),
]
for i, (tid, tx, tz, species, height) in enumerate(TREES):
    DRESSING["props"].append({"id": tid, "kind": "tree", "seed": 200 + i, "x": tx, "z": tz,
                              "form": "template", "species": species, "height": height})

# erratics: mossy at the keep's foot, where the made thing meets the ground it stands on, and a few
# out on the moor
BOULDERS = [
    ("b-keep-w", -33, -8, "angular", 3, True, MOSS),
    ("b-moor-1", -66, -42, "outcrop", 4, True, ANDESITE),
    ("b-moor-2", -54, -82, "outcrop", 4, True, ANDESITE),
    ("b-moor-3", -74, -30, "round", 3, True, STONE),
    ("b-moor-4", -30, -74, "round", 3, True, STONE),
    ("b-spit-1", -88, -8, "angular", 3, False, SANDSTONE),
    ("b-spit-2", -72, 7, "angular", 4, False, SANDSTONE),
    ("b-spit-3", -55, -7, "round", 3, False, SANDSTONE),
    ("b-spit-4", -80, -7, "round", 3, False, SANDSTONE),
]
for i, (bid, bx, bz, form, size, mossy, rock) in enumerate(BOULDERS):
    DRESSING["props"].append({"id": bid, "kind": "boulder", "seed": 300 + i, "x": bx, "z": bz,
                              "form": form, "size": size, "mossy": mossy, "rock": rock})


def finish():
    return {
        "authors": ["Opus 5"],
        "created": "2026-09-03",
        "roomStyles": {"spawn": "@hb-spawn", "cage": "@hb-cage"},
        "themes": THEMES,
        "mapTheme": "moor",
        # keyed on the compiled ids, because two pieces at one height fuse into one shape and a
        # height key cannot tell them apart
        "themeById": {
            "march-e-8": "moor",     # the spawn compound
            "march-e-9": "moor",     # march-s
            "march-e-9-2": "moor",     # march-e
            "march-e-10": "moor",     # the wool shelf, all four sides of the room
            "march-e-11": "moor",     # the room's own ground
            "arm-inner-7": "strand",   # the spit, outer
            "arm-inner-8": "strand",   # the spit, middle
            "arm-inner-9": "strand",   # the spit, inner
            "keep-13": "keep",     # the apron is the keep's own landing, not the spit's end
            "keep-18": "keep",     # the keep
        },
        "shapePropsById": {
            # the room and its shelf are pads, each one riser over the one it is reached from
            "march-e-10": {"relief_scope": "hold"},
            "march-e-11": {"relief_scope": "hold"},
            # the apron and the keep are made: out of the elevation model, flat and sheer
            "keep-13": {"relief_scope": "exclude"},
            "keep-18": {"relief_scope": "exclude"},
        },
        "relief": RELIEF,
        "addShapes": ADD_SHAPES,
        "dressing": DRESSING,
    }


def main():
    with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as f:
        json.dump(plan(), f, indent=1)
    with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as f:
        json.dump(finish(), f, indent=1)
    print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")


if __name__ == "__main__":
    main()
