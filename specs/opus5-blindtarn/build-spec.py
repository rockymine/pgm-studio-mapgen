#!/usr/bin/env python3
"""Blind Tarn — a frozen corrie is the middle, and every attack crosses it.

The board in one sentence: a destroy board whose no-man's-land is a corrie —
a bowl with a frozen tarn in the bottom — so an attack goes DOWN into the
open, across or round the ice, and up the far side under everything on the
rim, and each team's monument stands on the outer slope beyond it.

It was drawn as a capture board and could not be one: `MapIntent` carries
wools, destroyables, cores and modes, and no control point of any kind.
`controlPoint` has no occurrence in the whole API surface, and MapParser
lists `control-points` among the elements the studio refuses to read. The
driver's own `controlPoints` finish key writes into `intent.controlPoints`,
which nothing consumes — RQ3 naming it unread is the only report of it.

The relief is four instruments and each does what only it can:

  push, NEGATIVE crown   dishes the ring instead of doming it. This is the
                         corrie, and nothing else in the studio makes one.
  push, positive crown   the headwall behind it, so the rim is not level
  area marks             the aprons and shoulders a player stands on, all of
                         them OUTSIDE the corrie push: a push is added to the
                         surface the marks solved, so a mark under one moves
  height_mode raise      the moraine bar. Erected shapes are applied over the
                         solved ground, AFTER the pushes, so this is the one
                         way to state a height inside a push and keep it.
"""
import json, os, math

D = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-blindtarn"
CELL = 4

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

SNOW        = solid(80, 0)
ICE         = solid(79, 0)
PACKED_ICE  = solid(174, 0)
GRASS       = solid(2, 0)
DIRT        = solid(3, 0)
COARSE_DIRT = solid(3, 1)
PODZOL      = solid(3, 2)
STONE       = solid(1, 0)
ANDESITE    = solid(1, 5)
DIORITE     = solid(1, 3)
GRANITE     = solid(1, 1)
COBBLE      = solid(4, 0)
GRAVEL      = solid(13, 0)
STONE_BRICK = solid(98, 0)
SPRUCE_PLANK = solid(5, 1)
SPRUCE_LOG   = solid(17, 1)

def depth_stack(*pairs, beyond=STONE):
    return {"kind": "layered", "axis": "depth", "beyond": beyond,
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in pairs]}}

def slope_stack(*bands):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}

def ring(cx, cz, r, n=12, wobble=0.0, seed=1):
    """A lobed ring. An area mark's ring is a SHAPE, and a four-vertex
    rectangle builds a mesa with literal square sides."""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + wobble * math.sin(seed * 1.7 + i * 2.3))
        out.append([round(cx + rr * math.cos(a)), round(cz + rr * math.sin(a))])
    return out

TARN_LEVEL = 9

# ---------------------------------------------------------------- the plan
plan = {
    "plan": 2,
    "meta": {"name": "Blind Tarn"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 14,
                "surface": 24, "observerY": 62},
    "pieces": [
        # One piece, authored across the axis: its own rot_180 image overlaps
        # it through the middle, so the board is ONE landmass. A capture board
        # wants contested ground in the middle, not a strait.
        {"id": "fell",  "role": "piece", "rect": [-10, -24, 20, 26]},
        {"id": "spawn", "role": "spawn", "rect": [-3, -24, 6, 3]},
    ],
    "zones": [],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn", "at": [12, 6], "facing": "back",
             "footprint": [5, 2, 14, 8]},
        ],
        "wools": [], "iron": [], "cores": [],
        "destroyables": [
            # Beyond the corrie's rim on the outer slope, and a long way off
            # the centre line: with both monuments near the middle every
            # journey ran down the same corridor and the corrie's two flanks
            # were 9,000 dead cells. Out here the two roads diverge and each
            # flank is on one of them. at: BLOCKS from the
            # piece's minimum corner (-52, -96).
            {"id": "destroyable-1", "piece": "fell", "at": [12, 40],
             "style": "pillar-3", "materials": "obsidian", "float": 4,
             "name": "Tarnstone"},
        ],
    },
    "walls": [], "boxes": [],
}

# ------------------------------------------------------------ relief marks
relief_team = {
    "base": 24,
    "reach": 0,
    "step": 1,
    "landform": "hills",
    "grain": {"amplitude": 1.1, "scale": 26, "seed": 23},
    "marks": [
        # Only ground a player stands on is pinned, and all of it is outside
        # the corrie push. A board with a mark on every region is a table with
        # bumps on it however tall the bumps are; the flanks carry none.
        # One of each: the group is fanned, so its rot_180 image is stated
        # for free. A mark drawn at the image's own coordinates pins nothing
        # (RL4) and the surface is what it would have been without it.
        # RL5 is the fault of grading everything: a board of nothing but
        # shoulders reads walkable and has no flat to fight on. These four
        # are the flats, and all of them sit OUTSIDE the corrie push.
        {"id": "goal-shelf-w", "kind": "area", "h": 26, "bevel": 4,
         "ring": ring(-28, -56, 13, 11, 0.16, 5)},
        {"id": "spawn-apron", "kind": "area", "h": 24, "bevel": 3,
         "ring": ring(0, -84, 16, 9, 0.12, 3)},
    ],
    "pushes": [
        # THE CORRIE. amount lifts the rim four; crown -20 drops the middle
        # twenty below it. Skirt 6/14 = 0.43 a block against crown 20/32 =
        # 0.63 — 1.45x apart, which is inside what RL6 calls a step.
        {"id": "corrie", "amount": 6, "falloff": 14, "crown": -20,
         "roughness": 5, "seed": 11, "ring": ring(0, 0, 32, 14, 0.10, 2)},
        # The headwall behind it, on the far side from nobody: it makes the
        # rim unequal, so the two shoulders are not the same shoulder twice.
        {"id": "headwall", "amount": 11, "falloff": 10, "crown": 9,
         "roughness": 4, "seed": 13,
         "ring": [[-40, -66], [-16, -62], [10, -64], [34, -61], [46, -66],
                  [44, -52], [22, -49], [-4, -51], [-28, -49], [-42, -53]]},
    ],
}

# --------------------------------------------------- the bar, and the water
# An erected shape is applied over the ground the relief solved — after the
# pushes — so it is the only way to state a height INSIDE a push and keep it.
# `raise` reads the median of the ground under its own footprint, so this
# stands six over whatever the corrie settles at, which is above the water.
moraine = {
    "id": "moraine", "type": "polygon", "operation": "add",
    "height_mode": "raise", "base_height": 6, "skirt": 5, "floor": 0,
    "vertices": [[-20, 4], [-8, -3], [8, -4], [20, 2], [19, 10],
                 [6, 12], [-8, 10], [-19, 11]],
    "theme": "tarn",
}
# Two necks joining the bar to the rim, so the middle point is come at from
# two sides and neither is the other. skirt >= the lift is what makes an
# erected shape a landform a player strolls up rather than a standing stone.
neck_w = {
    "id": "neck-w", "type": "polygon", "operation": "add",
    "height_mode": "raise", "base_height": 5, "skirt": 7, "floor": 0,
    "vertices": [[-33, 3], [-19, 3], [-18, 12], [-32, 14]],
    "theme": "tarn",
}
# ONE dry way onto the bar, not two. The other side is waded, which is slow
# and in the open, so the two approaches to the middle cost different things.
neck_e = None

# The tarn itself. A sink is applied over the ground the relief solved, like a
# raise, so it is the one instrument that can cut a LEVEL floor inside a push
# — and level is what a frozen lake is. It is ice rather than a water prop
# because a pool takes the lowest surface its body crosses as its line and
# empties every column above it, so water drawn on a dish digs a shaft
# whatever depth is asked for (DR-BANK), and because a board this cold has a
# tarn you walk on.
tarn_pan = {
    "id": "tarn-pan", "type": "polygon", "operation": "add",
    # A raise of ZERO, not a sink. Both flatten to the median of the ground
    # under them, and both are applied after the pushes — but a sink with a
    # narrow skirt cuts sheer faces, and at the bottom of a bowl that is a
    # thirteen-block pit you drop into and cannot climb out of. A flush raise
    # with a wide skirt is the same flat floor with an edge that eases.
    "height_mode": "raise", "base_height": 0, "skirt": 12, "floor": 0,
    "vertices": ring(0, 0, 24, 12, 0.10, 6),
    "theme": "ice",
}

# ---------------------------------------------------------------- themes
fell_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    # The rim is off: this ground is relief-solved, and a rim caps every fall
    # with a band, which turns a corrie into contour lines.
    "rim": {"enabled": False, "depth": 1, "material": STONE},
    # Finished by angle. Snow lies on the flat, grass on the shoulder, and
    # neither lies on a forty-five degree face — the slope axis is the only
    # thing on the board that knows the difference. Snow sits straight on the
    # soil: a surfacing block is one course and has to be the top of its
    # stack, so grass under snow is PT1 and a refusal.
    "surface": {"enabled": True, "depth": 4, "material": slope_stack(
        (depth_stack((SNOW, 1), (DIRT, 3), beyond=STONE), 22),
        (depth_stack((GRASS, 1), (COARSE_DIRT, 2), beyond=STONE), 20),
        (depth_stack((STONE, 2), (ANDESITE, 2), beyond=STONE), 48),
    )},
    "wall": {"kind": "wallRun", "runs": [
        {"material": STONE, "width": 4},
        {"material": ANDESITE, "width": 1},
        {"material": DIORITE, "width": 2},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 29, "cellSize": 14, "rise": 6,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": GRANITE, "depth": 1}]},
}

# The bar and the shore: what the ice leaves behind, which is gravel and rock
# and no snow at all, because it is under water half the year.
tarn_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (GRAVEL, 1), (COBBLE, 1), (STONE, 1), beyond=STONE)},
    "wall": {"kind": "wallRun", "runs": [
        {"material": COBBLE, "width": 2},
        {"material": GRAVEL, "width": 1},
        {"material": STONE, "width": 3},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 31, "cellSize": 12, "rise": 6,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": ANDESITE, "depth": 1}]},
}

crag_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": ANDESITE},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (STONE, 1), (ANDESITE, 2), beyond=STONE)},
    # A cliff is what the wall bucket paints, so the strata live here — and in
    # the fill, or the face bands at the top and is plain the whole way down.
    "wall": {"kind": "wallRun", "runs": [
        {"material": STONE, "width": 3},
        {"material": DIORITE, "width": 1},
        {"material": ANDESITE, "width": 2},
        {"material": GRANITE, "width": 1},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "layered", "axis": "depth", "beyond": STONE,
             "stack": {"ending": "repeat", "bands": [
                 {"material": STONE, "thickness": 3},
                 {"material": DIORITE, "thickness": 1},
                 {"material": STONE, "thickness": 2},
                 {"material": ANDESITE, "thickness": 1},
             ]}},
}


# The ice. One material, laid flat, and no field sampled over it: a frozen
# tarn is the one surface on this board that is genuinely uniform.
ice_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": SNOW},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (ICE, 1), (PACKED_ICE, 2), beyond=STONE)},
    "wall": {"kind": "wallRun", "runs": [
        {"material": PACKED_ICE, "width": 3},
        {"material": STONE, "width": 2},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 37, "cellSize": 12, "rise": 6,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": ANDESITE, "depth": 1}]},
}

def patch(pid, pts, theme):
    """A paint patch has to declare a height_mode or it never owns a cell:
    a scoping shape wins only where its own top equals the tallest top there,
    and a shape that states a height_mode is `standing` and always a
    candidate. `raise` of zero sits flush at the median ground under it."""
    return {"id": pid, "type": "polygon", "operation": "add",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "vertices": pts, "theme": theme}

patches = [
    patch("headwall-face", ring(2, -48, 22, 11, 0.18, 9), "crag"),
    patch("shore-w", ring(-27, 7, 12, 10, 0.16, 4), "tarn"),
    patch("shore-e", ring(27, -7, 12, 10, 0.16, 6), "tarn"),
]

spawn_style = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": STONE_BRICK, "thickness": 1}],
                            "ending": "repeat"}, "extent": 2},
        "surface": {"field": None, "border": None, "borderWidth": 1,
                    "inlay": None, "inlayInset": 2, "isPlain": True},
        "footing": None,
    },
    "roof": {"form": "gable", "pitch": 1, "slab": -1, "slabData": 0,
             "overhang": 1, "ridgeCap": True, "hole": False,
             "body": SPRUCE_PLANK, "verge": solid(5, 5), "gable": solid(5, 5),
             "gableWindows": {"form": "none", "block": 102, "hostBlock": -1,
                              "hostData": 0, "data": 0, "sill": 2, "width": 2,
                              "height": 2, "spacing": 3}},
    "wall": {"stack": {"bands": [
        {"material": STONE_BRICK, "thickness": 2},
        {"material": SPRUCE_PLANK, "thickness": 4},
    ], "ending": "repeat"}, "extent": 6},
    "post": SPRUCE_LOG,
    "windows": {"form": "arched", "block": 134, "hostBlock": 5, "hostData": 1,
                "data": 0, "sill": 4, "width": 2, "height": 2, "spacing": 2},
    "storeys": [], "porch": None, "front": None,
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air", "head": {"form": "arched", "block": 134,
                "fill": "upperSlab", "fillBlock": 126, "fillData": 1},
                "width": 3, "height": 4},
}

PAVE = {"kind": "cell", "seed": 17, "cellSize": 9, "entries": [
    {"material": GRAVEL}, {"material": ANDESITE}, {"material": COBBLE}]}

dressing_props = [
    # The tarn. It states its own level rather than taking the lowest surface
    # it finds: the corrie's floor is a dish and not a pan, so water left to
    # find a level would stand in a puddle at the very bottom.
    {"id": "corrie-road", "kind": "stroke", "style": "solid",
     "claimsGround": True, "radius": 2, "seed": 8, "pave": PAVE,
     "points": [[0, -82], [-10, -70], [-22, -58], [-28, -44], [-26, -28]]},
    {"id": "erratic-0", "kind": "boulder", "x": -31, "z": -14, "seed": 41, "radius": 3},
    {"id": "erratic-1", "kind": "boulder", "x": 30, "z": 26, "seed": 42, "radius": 3},
    {"id": "erratic-2", "kind": "boulder", "x": -8, "z": -64, "seed": 43, "radius": 2},
]

finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"fell": fell_theme, "tarn": tarn_theme, "crag": crag_theme,
               "ice": ice_theme},
    "mapTheme": "fell",
    "addShapes": [tarn_pan, moraine, neck_w] + patches,
    "relief": {"team": relief_team},
    # Ice plains: snow and ice are BLOCKS, so a snowfield on Plains has a
    # summer meadow running through it. This biome tints grass #80b497, which
    # is what makes the two agree.
    "biome": {"kind": "solid", "biome": 12},
    "roomStyles": {"spawn": spawn_style},
    "dressing": {"styles": {}, "props": dressing_props},
}

with open(os.path.join(D, f"{SLUG}.plan.json"), "w") as fh:
    json.dump(plan, fh, indent=1)
with open(os.path.join(D, f"{SLUG}.finish.json"), "w") as fh:
    json.dump(finish, fh, indent=1)
print(f"wrote {SLUG}")
