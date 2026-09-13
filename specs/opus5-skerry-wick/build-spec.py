#!/usr/bin/env python3
"""Skerry Wick — wool carried between islands, and every route is a crossing.

The board in one sentence: a wool board of bare skerries over void, where a
team's two wool rooms stand on two separate islands at two different depths,
so an attack cannot take both on one bridge and has to choose which sea to
cross first.

The proportions are the composer's rather than mine. GET /api/compose
?players=24&symmetry=rot_180&wools=i answers a team unit of 105 land cells
at cell 5 — hub 44, frontline 32, two wools 20, spawn 9 — against a budget
of 171, which is about a third land. A wool board is HALF VOID and the
fill-ratio term under G8 holds it to [0.201, 0.542].

The shape that gets there is not symmetry about the centre line. The unit is
drawn OFFSET to the west, so its own rot_180 image takes the east of the far
half and the two interlock: every row of the board is about half land, and a
unit drawn symmetric about x = 0 fills its own bounding rectangle and cannot
reach the band at any size.
"""
import json, os, math

D = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-skerry-wick"
CELL = 5

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

GRASS       = solid(2, 0)
DIRT        = solid(3, 0)
COARSE_DIRT = solid(3, 1)
PODZOL      = solid(3, 2)
STONE       = solid(1, 0)
ANDESITE    = solid(1, 5)
DIORITE     = solid(1, 3)
GRANITE     = solid(1, 1)
COBBLE      = solid(4, 0)
MOSSY_COBBLE= solid(48, 0)
GRAVEL      = solid(13, 0)
STONE_BRICK = solid(98, 0)
DARK_PLANK  = solid(5, 5)
DARK_LOG    = solid(17, 5)
SPRUCE_LOG  = solid(17, 1)

def depth_stack(*pairs, beyond=STONE):
    return {"kind": "layered", "axis": "depth", "beyond": beyond,
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in pairs]}}

def slope_stack(*bands):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}

def ring(cx, cz, r, n=11, wobble=0.0, seed=1):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + wobble * math.sin(seed * 1.7 + i * 2.3))
        out.append([round(cx + rr * math.cos(a)), round(cz + rr * math.sin(a))])
    return out

# ---------------------------------------------------------------- the plan
# One team's unit, offset west. Land cells: home 40, hub ring 32, two holms
# 2x16, spawn 8 = 112, against the composer's 105 for this player count.
plan = {
    "plan": 2,
    "meta": {"name": "Skerry Wick"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12,
                "surface": 14, "observerY": 44},
    "pieces": [
        # The home island at the back, carrying the spawn.
        {"id": "home",  "role": "piece", "rect": [-11, -20, 8, 5]},
        {"id": "spawn", "role": "spawn", "rect": [-9, -19, 5, 2]},
        # The two wool holms. They are on two different seas — one in the
        # hub's lee, one out on the open flank — rather than at two different
        # DEPTHS, because WL9 holds the two wools to within 1.232x of each
        # other's walk from the spawn and a near/far pair cannot be that.
        # Each holm is four cells to the room's two, so the room has ordinary
        # ground on all four sides: a wool room's foundation is bedrock to y0
        # and beside void it builds as a cliff nothing drew.
        {"id": "holm-far",  "role": "piece", "rect": [-11, -12, 4, 4]},
        {"id": "holm-near", "role": "piece", "rect": [0, -13, 4, 4]},
        # A reef between the home island and the hub. Without it those two
        # face each other across 45 blocks with nothing in between, and G5
        # reads the hop it would take rather than the route round.
        {"id": "reef", "role": "piece", "rect": [-7, -11, 4, 2]},
        # The forward body, and the only piece either team contests.
        {"id": "hub", "role": "piece", "rect": [-7, -6, 8, 4]},
    ],
    "zones": [
        # Every gap is 10 to 20 blocks — G5's hop band — so each is a bridge
        # somebody pays for rather than a jump or a swim.
        {"id": "wick", "rect": [-7, -2, 14, 4], "holes": []},
        {"id": "reaches", "rect": [-11, -15, 15, 9], "holes": []},
    ],
    "placements": {
        "spawns": [
            # The door sits east in its own island, which is what makes the
            # two wool walks the same length: WL9 holds them to within
            # 1.232x, and a spawn at the island's west end put one wool at
            # 41 blocks and the other at 57.
            {"id": "spawn-1", "piece": "spawn", "at": [22, 5], "facing": "back",
             "footprint": [4, 1, 16, 8]},
        ],
        "wools": [
            # at and footprint are BLOCKS from the piece's minimum corner.
            {"id": "wool-far", "piece": "holm-far", "at": [10, 10],
             "footprint": [5, 5, 10, 10]},
            {"id": "wool-near", "piece": "holm-near", "at": [10, 10],
             "footprint": [5, 5, 10, 10]},
        ],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [], "boxes": [],
}

# ------------------------------------------------------------ relief marks
# An island board's relief is small on purpose: every island is ground a
# player fights on, and a wool room seats on an absolute plinth. The two
# holms are pinned dead flat; the hub is the one piece that is shaped.
relief_team = {
    "base": 14,
    "reach": 0,
    "step": 1,
    "landform": "rolling",
    "grain": {"amplitude": 1.2, "scale": 18, "seed": 19},
    "marks": [
        {"id": "holm-far-pad", "kind": "area", "h": 15, "bevel": 2,
         "ring": ring(-45, -50, 12, 9, 0.10, 3)},
        {"id": "holm-near-pad", "kind": "area", "h": 15, "bevel": 2,
         "ring": ring(10, -55, 12, 9, 0.10, 5)},
        {"id": "home-pad", "kind": "area", "h": 16, "bevel": 3,
         "ring": ring(-35, -88, 20, 11, 0.12, 7)},
        {"id": "reef-pad", "kind": "area", "h": 13, "bevel": 2,
         "ring": ring(-25, -48, 10, 9, 0.14, 9)},
    ],
    "pushes": [
        # The hub's knoll, which is the high ground both teams want.
        # amount/falloff 4/8 = 0.5 a block against crown/half 7/14 = 0.5.
        # The half-width is the RING's, not a number of your choosing: at
        # r14 a crown of 7 spreads over 14, and the skirt has to be set to
        # match it or the ground steps at the push's own outline.
        {"id": "hub-knoll", "amount": 4, "falloff": 8, "crown": 7,
         "roughness": 3, "seed": 11, "ring": ring(-15, -20, 14, 11, 0.12, 2)},
    ],
}

# ---------------------------------------------------------------- themes
skerry_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    # The rim is OFF even here. It belongs on a made edge, and every edge on
    # this board is a coast the relief solved.
    "rim": {"enabled": False, "depth": 1, "material": STONE},
    "surface": {"enabled": True, "depth": 4, "material": slope_stack(
        (depth_stack((GRASS, 1), (DIRT, 2), beyond=STONE), 20),
        (depth_stack((PODZOL, 1), (COARSE_DIRT, 2), beyond=STONE), 22),
        (depth_stack((STONE, 2), (ANDESITE, 2), beyond=STONE), 48),
    )},
    "wall": {"kind": "wallRun", "runs": [
        {"material": STONE, "width": 4},
        {"material": ANDESITE, "width": 1},
        {"material": DIORITE, "width": 2},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 13, "cellSize": 13, "rise": 6,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": GRANITE, "depth": 1}]},
}

strand_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (GRAVEL, 1), (COBBLE, 1), (STONE, 1), beyond=STONE)},
    "wall": {"kind": "wallRun", "runs": [
        {"material": COBBLE, "width": 2},
        {"material": MOSSY_COBBLE, "width": 1},
        {"material": STONE, "width": 3},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 23, "cellSize": 12, "rise": 6,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": ANDESITE, "depth": 1}]},
}

works_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "boundary",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONE_BRICK},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (STONE_BRICK, 1), (COBBLE, 2), beyond=STONE)},
    # A made face is striped along its perimeter and sheared by height, which
    # is the one surface on a board nothing sampled from the plane can reach.
    "wall": {"kind": "wallDiagonal", "slope": 2, "runs": [
        {"material": COBBLE, "width": 3},
        {"material": STONE_BRICK, "width": 1},
        {"material": MOSSY_COBBLE, "width": 1},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 29, "cellSize": 12, "rise": 7,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": COBBLE, "depth": 1}]},
}

def patch(pid, pts, theme):
    """A paint patch states a height_mode or it never owns a cell."""
    return {"id": pid, "type": "polygon", "operation": "add",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "vertices": pts, "theme": theme}

patches = [
    patch("quay-far",  ring(-45, -50, 9, 9, 0.15, 2), "works"),
    patch("quay-near", ring(10, -55, 9, 9, 0.15, 4), "works"),
    patch("strand-hub", ring(-15, -20, 10, 10, 0.2, 6), "strand"),
    patch("strand-home", ring(-35, -80, 11, 9, 0.2, 8), "strand"),
]

# ------------------------------------------------------------------ shells
def shell(wall_a, wall_b, post, roof_body):
    return {
        "foundation": {
            "plate": {"stack": {"bands": [{"material": wall_a, "thickness": 1}],
                                "ending": "repeat"}, "extent": 2},
            "surface": {"field": None, "border": None, "borderWidth": 1,
                        "inlay": None, "inlayInset": 2, "isPlain": True},
            # No footing. Over a plate of one course it is a rim round a
            # building with no foundation to speak of, and it reads as noise.
            "footing": None,
        },
        "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0,
                 "overhang": 1, "ridgeCap": True, "hole": False,
                 "body": roof_body, "verge": solid(5, 5), "gable": solid(5, 5),
                 "gableWindows": {"form": "none", "block": 102, "hostBlock": -1,
                                  "hostData": 0, "data": 0, "sill": 2,
                                  "width": 2, "height": 2, "spacing": 3}},
        "wall": {"stack": {"bands": [
            {"material": wall_a, "thickness": 2},
            {"material": wall_b, "thickness": 4},
        ], "ending": "repeat"}, "extent": 6},
        "post": post,
        "windows": {"form": "arched", "block": 134, "hostBlock": 5,
                    "hostData": 1, "data": 0, "sill": 4, "width": 2,
                    "height": 2, "spacing": 2},
        "storeys": [], "porch": None, "front": None,
        "beams": {"block": 17, "data": 5, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "arched", "block": 134,
                    "fill": "upperSlab", "fillBlock": 126, "fillData": 1},
                    "width": 3, "height": 4},
    }

# The key is `wool`, not `cage`. A key SketchRoomStyles does not know is
# dropped in silence on the whole-layout write this driver uses -- 200,
# pre-flight OPEN, and the room builds as the built-in bedrock box.
room_styles = {
    "wool":  shell(STONE_BRICK, DARK_PLANK, DARK_LOG, DARK_PLANK),
    "spawn": shell(COBBLE, DARK_PLANK, SPRUCE_LOG, DARK_PLANK),
}

# `cell` takes `palette`, and `jitter` and `warp` are required. `entries` is
# not a field the studio reads, so a pattern stating it is dropped inside the
# snapshot in silence and renders as a flat swatch.
PAVE = {"kind": "cell", "seed": 5, "cellSize": 9, "jitter": 3,
        "warp": 2, "rise": 4, "palette": [GRAVEL, ANDESITE, COBBLE]}

dressing_props = [
    {"id": "hub-track", "kind": "stroke", "style": "solid", "claimsGround": True,
     "radius": 2, "seed": 7, "pave": PAVE,
     "points": [[-32, -16], [-20, -22], [-8, -18], [2, -14]]},
    # Each of these stands where loop.py --candidates said it would. The two
    # holms are wool-room keep-out from edge to edge -- a 20-block holm round
    # a 10-block room leaves no cell a prop may have -- so everything is on
    # the home island or on the reef, which is also where a player walks.
    {"id": "sea-stack-0", "kind": "boulder", "x": -24, "z": -50, "seed": 51, "radius": 3},
    {"id": "pine-0", "kind": "tree", "x": -52, "z": -78, "species": "spruce",
     "height": 11, "seed": 61},
    {"id": "pine-1", "kind": "tree", "x": -46, "z": -79, "species": "spruce",
     "height": 13, "seed": 62},
    {"id": "isle-cover", "kind": "flora", "seed": 9,
     "points": [[-55, -100], [20, -100], [20, -40], [-55, -40]],
     "spec": {"coverage": 0.2, "scale": 22, "octaves": 2, "fernShare": 0.4,
              "flowerShare": 0.04, "flowerScale": 13, "tallShare": 0.04}},
]

finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"skerry": skerry_theme, "strand": strand_theme,
               "works": works_theme},
    "mapTheme": "skerry",
    "addShapes": patches,
    "relief": {"team": relief_team},
    # Taiga: the grass and leaves on these islands take their colour from the
    # biome byte and nothing else on the board does, so it is a palette
    # decision rather than a line added at the end.
    "biome": {"kind": "solid", "biome": 5},
    "roomStyles": room_styles,
    "dressing": {"styles": {}, "props": dressing_props},
}

with open(os.path.join(D, f"{SLUG}.plan.json"), "w") as fh:
    json.dump(plan, fh, indent=1)
with open(os.path.join(D, f"{SLUG}.finish.json"), "w") as fh:
    json.dump(finish, fh, indent=1)
print(f"wrote {SLUG}")
