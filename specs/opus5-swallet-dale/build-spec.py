#!/usr/bin/env python3
"""Swallet Dale — the monument is inside the rock, and the way in is a gallery.

The board in one sentence: a destroy board on a limestone dale where each
team's monument stands in a chamber inside a crag, and the crag has three
ways into it — a drift, an adit and a hole in its roof.

Crossing the strait is only the first half of an attack; the second half is
getting inside, and the crag's roof is ground you can hold without it helping
you at all.

The stack, bottom-up. Every storey is an absolute span, so the ground under
the crag is pinned flat by an `area` mark — a made thing cannot be seated on
a relief, and one course of drift would bury it.

  ground   y0..y12   the dale. Its surface IS the gallery floor.
  workings y13..y20  the crag's rock, drawn as the COMPLEMENT of the corridors
  roof     y18..y20  the crag's lid, drawn as rectangles AROUND the chamber
  crown    y21..y23  the taller lid over the chamber, with the swallet in it

Nothing here is cut with a `subtract`: SK13 reads one as the board's negative
space and refuses any add that fills it, on any layer. The corridors are the
rock that was not drawn, and the holes are the rectangles left out.
"""
import json, os

D = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-swallet-dale"
CELL = 4

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

GRASS        = solid(2, 0)
DIRT         = solid(3, 0)
COARSE_DIRT  = solid(3, 1)
PODZOL       = solid(3, 2)
STONE        = solid(1, 0)
GRANITE      = solid(1, 1)
ANDESITE     = solid(1, 5)
DIORITE      = solid(1, 3)
COBBLE       = solid(4, 0)
MOSSY_COBBLE = solid(48, 0)
GRAVEL       = solid(13, 0)
STONE_BRICK  = solid(98, 0)
MOSSY_BRICK  = solid(98, 1)
SPRUCE_PLANK = solid(5, 1)
SPRUCE_LOG   = solid(17, 1)
DARK_OAK_LOG = solid(17, 5)
COAL_ORE     = solid(16, 0)

def depth_stack(*pairs, beyond=STONE):
    return {"kind": "layered", "axis": "depth", "beyond": beyond,
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in pairs]}}

def slope_stack(*bands):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}

# ===================================================== the workings, by plan
# The crag's footprint and the corridors cut through it. Everything about the
# gallery is stated ONCE, here, as air; the rock is derived from it below, so
# a corridor moved never leaves a wall behind.
CRAG = (-28, -86, 20, -42)          # min_x, min_z, max_x, max_z

CHAMBER  = (-20, -76, -2, -56)      # the room the monument stands in
WEST_DRIFT = (-28, -66, -18, -60)   # opens on the crag's west face
EAST_ADIT  = (-2, -68, 20, -62)     # opens on the east face
SOUTH_ADIT = (-10, -58, -4, -42)    # opens on the south face, toward the strait
SWALLET_SPUR = (-4, -52, 10, -46)   # runs under the hole in the roof
SWALLET  = (-16, -68, -10, -62)      # the hole itself, cut in the crown
# Every strip the swallet leaves in the crown is at least four blocks wide.
# Thinner and SK23 fires: no column has ground on all eight sides, so every
# one of them is an edge, only the rim and wall buckets paint it, and the
# theme's surface appears nowhere on the shape at all.

VOIDS = [CHAMBER, WEST_DRIFT, EAST_ADIT, SOUTH_ADIT, SWALLET_SPUR]

def complement(outer, holes):
    """The rectangles of `outer` that no hole covers, as a grid sweep.

    Authoring arithmetic, not a read of anything built: the corridors are the
    statement and the rock is what is left, so the two can never disagree.
    Among the shapes of one layer the TALLER add wins the column outright, so
    a wall that crossed a corridor would seal it whatever the document order.
    """
    x0, z0, x1, z1 = outer
    xs = sorted({x0, x1} | {v for h in holes for v in (h[0], h[2])
                            if x0 < v < x1})
    zs = sorted({z0, z1} | {v for h in holes for v in (h[1], h[3])
                            if z0 < v < z1})
    out = []
    for i in range(len(xs) - 1):
        for j in range(len(zs) - 1):
            cx, cz = (xs[i] + xs[i + 1]) / 2, (zs[j] + zs[j + 1]) / 2
            if any(h[0] < cx < h[2] and h[1] < cz < h[3] for h in holes):
                continue
            out.append((xs[i], zs[j], xs[i + 1], zs[j + 1]))
    return out

def rect(rid, r, floor, height, theme=None, layer_material=None):
    s = {"id": rid, "type": "rectangle", "operation": "add",
         "min_x": r[0], "min_z": r[1], "max_x": r[2], "max_z": r[3],
         "floor": floor, "base_height": height}
    if theme:
        s["theme"] = theme
    if layer_material:
        s["material"] = layer_material
    return s

# The rock between the dale floor and the lid: the crag minus every corridor.
workings = [rect(f"rock-{i}", r, 13, 5, theme="crag")
            for i, r in enumerate(complement(CRAG, VOIDS))]

# The lid over everything except the chamber, which gets a taller one.
roof = [rect(f"roof-{i}", r, 18, 3, theme="crag")
        for i, r in enumerate(complement(CRAG, [CHAMBER]))]

# The crown over the chamber, with the swallet left out of it.
# Two courses, not three: the swallet is cut in the crown, so the crown has
# to be ground a player can get onto from the roof around it. At three it
# stood a barrier over the roof and the third way in was unreachable.
crown = [rect(f"crown-{i}", r, 21, 2, theme="crag")
         for i, r in enumerate(complement(CHAMBER, [SWALLET]))]

# ---------------------------------------------------------------- the plan
plan = {
    "plan": 2,
    "meta": {"name": "Swallet Dale"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12,
                "surface": 12, "observerY": 46},
    "pieces": [
        {"id": "dale",  "role": "piece", "rect": [-10, -27, 20, 23]},
        {"id": "spawn", "role": "spawn", "rect": [2, -30, 6, 3]},
    ],
    "zones": [
        {"id": "strait", "rect": [-10, -4, 20, 8], "holes": []},
    ],
    "placements": {
        "spawns": [
            {"id": "spawn-1", "piece": "spawn", "at": [12, 6], "facing": "back",
             "footprint": [5, 2, 14, 8]},
        ],
        "wools": [], "iron": [], "cores": [],
        "destroyables": [
            # `layer` is the whole of what puts this in the dark. A goal naming
            # none resolves against SurfaceTop — the HIGHEST layer — so this
            # one would stand on the crag's roof with nothing declined.
            {"id": "destroyable-1", "piece": "dale", "at": [34, 38],
             "layer": "ground", "style": "pillar-3", "materials": "obsidian",
             "float": 4, "name": "Swallet"},
        ],
    },
    "walls": [], "boxes": [],
}

# ------------------------------------------------------------ relief marks
relief_team = {
    "base": 12,
    "reach": 0,
    "step": 1,
    "landform": "rolling",
    "grain": {"amplitude": 1.4, "scale": 23, "seed": 17},
    "marks": [
        # The crag's floor, pinned dead flat and a little wider than the crag.
        # Every shape above states an absolute floor, so ground the relief
        # moved under them would bury the drift or leave it in the air.
        {"id": "crag-floor", "kind": "area", "h": 12, "bevel": 2,
         "ring": [[-34, -92], [26, -92], [26, -36], [-34, -36]]},
        # The dale in front of the crag, which is the ground an attack crosses.
        {"id": "dale-floor", "kind": "area", "h": 12, "bevel": 5,
         "ring": [[-38, -36], [-16, -34], [4, -36], [24, -34], [38, -36],
                  [36, -18], [12, -16], [-12, -18], [-36, -17]]},
        {"id": "spawn-apron", "kind": "area", "h": 12, "bevel": 3,
         "ring": [[2, -120], [34, -120], [36, -104], [20, -101], [4, -104]]},
    ],
    "pushes": [
        # The fell shoulders either side of the dale. amount/falloff 12/10 =
        # 1.2 a block against crown/half 10/9 = 1.1 — the two gradients agree,
        # so each reads as a hillside rather than a wall with a hill on top.
        # Both stop well clear of the crag: a push is added to the surface the
        # marks solved, and a skirt reaching the crag would tilt its floor.
        {"id": "fell-w", "amount": 10, "falloff": 8, "crown": 5,
         "roughness": 4, "seed": 3,
         "ring": [[-40, -104], [-37, -86], [-39, -64], [-37, -44],
                  [-40, -30], [-52, -34], [-54, -70], [-50, -100]]},
        {"id": "fell-e", "amount": 10, "falloff": 8, "crown": 5,
         "roughness": 4, "seed": 5,
         "ring": [[40, -104], [37, -86], [39, -64], [37, -44],
                  [40, -30], [52, -34], [54, -70], [50, -100]]},
    ],
}

# ------------------------------------------------------ the way onto the top
# The crag's roof is ground, so it needs a way up that is not the gallery.
# Run 18 for a rise of 9 is the two-to-one a stair meant to be climbed wants.
roof_ramp = {
    "id": "roof-ramp", "type": "polygon", "operation": "add", "override": True,
    "keepClear": True, "height_mode": "level", "skirt": 0, "floor": 0,
    # It runs two blocks INTO the crag's own footprint. Stopped at the face it
    # eased back into the ground over its last column and left a five-block
    # barrier onto a roof it was drawn to reach; overlapping the two footprints
    # is the whole of the fix, and skirt 0 is what stops the easing.
    "vertices": [[-30, -104], [-18, -104], [-18, -84], [-30, -84]],
    "anchor_heights": [12, 12, 21, 21],
    "material": STONE_BRICK,
}

# The gallery floor is the dale's own surface with a crag over it, so it is a
# COVERED column: one column resolves one band stack, and ground under a slab
# falls inside the `fill` band — no turf, no rim, no wall, whatever its theme
# says about a surface. These patches are here for their fill, which is what
# puts stone and coal in a mine floor instead of the dale's own rock.
def floor_patch(pid, r):
    return {"id": pid, "type": "rectangle", "operation": "add",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "min_x": r[0], "min_z": r[1], "max_x": r[2], "max_z": r[3],
            "theme": "gallery"}

gallery_floors = [floor_patch(f"floor-{i}", r) for i, r in enumerate(VOIDS)]

# ---------------------------------------------------------------- themes
dale_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": STONE},
    # Finished by angle, not by height: one stack takes the pasture, the
    # shoulder and the bare face of the same fell.
    "surface": {"enabled": True, "depth": 4, "material": slope_stack(
        (depth_stack((GRASS, 1), (DIRT, 2), beyond=STONE), 20),
        (depth_stack((COARSE_DIRT, 1), (DIRT, 2), beyond=STONE), 20),
        (depth_stack((STONE, 2), (ANDESITE, 2), beyond=STONE), 50),
    )},
    "wall": {"kind": "wallRun", "runs": [
        {"material": STONE, "width": 4},
        {"material": ANDESITE, "width": 1},
        {"material": GRANITE, "width": 2},
    ]},
    "wallEnabled": True,
    # A voronoi belongs in the fill and is made of stone: it is the body of
    # the rock nobody sees until a face is cut, and cells wider than they are
    # tall keep a cut face reading as blobs rather than as vertical posts.
    "fill": {"kind": "voronoi", "seed": 19, "cellSize": 13, "rise": 6,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": ANDESITE, "depth": 1}]},
}

# The crag: its faces are the point, so the strata go in `wall` AND `fill`.
# A stack stated only in `surface` bands the top four courses and leaves the
# whole face plain.
crag_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "drop",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": ANDESITE},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (STONE, 1), (ANDESITE, 2), beyond=STONE)},
    "wall": {"kind": "wallRun", "runs": [
        {"material": STONE, "width": 3},
        {"material": ANDESITE, "width": 1},
        {"material": GRANITE, "width": 2},
        {"material": DIORITE, "width": 1},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "layered", "axis": "depth", "beyond": STONE,
             "stack": {"ending": "repeat", "bands": [
                 {"material": STONE, "thickness": 3},
                 {"material": GRANITE, "thickness": 1},
                 {"material": STONE, "thickness": 2},
                 {"material": ANDESITE, "thickness": 1},
             ]}},
}

# The gallery. Nothing sampled: a worked passage is courses, not a field.
gallery_theme = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": COBBLE},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (GRAVEL, 1), (COBBLE, 1), (STONE, 1), beyond=STONE)},
    "wall": {"kind": "wallRun", "runs": [
        {"material": COBBLE, "width": 2},
        {"material": MOSSY_COBBLE, "width": 1},
        {"material": STONE, "width": 3},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 7, "cellSize": 11, "rise": 5,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": COAL_ORE, "depth": 1}]},
}

# --------------------------------------------------------------- the shell
# Forked from the shipped `longhouse`. The footing goes: it is the course
# ringing a DEEP plate one block proud, and over the one-course plate a board
# gives it, it is a rim round a building rather than masonry.
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
    "post": DARK_OAK_LOG,
    "windows": {"form": "arched", "block": 134, "hostBlock": 5, "hostData": 1,
                "data": 0, "sill": 4, "width": 2, "height": 2, "spacing": 2},
    "storeys": [], "porch": None, "front": None,
    "beams": {"block": 17, "data": 5, "reach": 1, "any": True},
    "doorway": {"door": "air", "head": {"form": "arched", "block": 134,
                "fill": "upperSlab", "fillBlock": 126, "fillData": 1},
                "width": 3, "height": 4},
}

# ---------------------------------------------------------------- dressing
PAVE = {"kind": "cell", "seed": 13, "cellSize": 9, "entries": [
    {"material": GRAVEL}, {"material": ANDESITE}, {"material": COBBLE}]}

dressing_props = [
    # The road off the spawn to the crag's south adit — the way the board is
    # meant to be walked, drawn rather than left to be guessed.
    {"id": "dale-road", "kind": "stroke", "style": "solid", "claimsGround": True,
     "radius": 2, "seed": 6, "pave": PAVE,
     "points": [[14, -110], [6, -96], [-2, -80], [-6, -62], [-7, -48]]},
    # Spoil off the workings, at the mouth of each way in and nowhere else.
    {"id": "spoil-w", "kind": "boulder", "x": -34, "z": -63, "seed": 31, "radius": 3},
    {"id": "spoil-e", "kind": "boulder", "x": 26,  "z": -65, "seed": 32, "radius": 3},
    {"id": "spoil-s", "kind": "boulder", "x": -14, "z": -38, "seed": 33, "radius": 2},
    {"id": "dale-cover", "kind": "flora", "seed": 4,
     "points": [[-36, -34], [36, -34], [36, -18], [0, -16], [-36, -18]],
     "spec": {"coverage": 0.22, "scale": 24, "octaves": 2, "fernShare": 0.35,
              "flowerShare": 0.06, "flowerScale": 15, "tallShare": 0.05}},
]

# ---------------------------------------------------------------- finish
finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"dale": dale_theme, "crag": crag_theme, "gallery": gallery_theme},
    "mapTheme": "dale",
    "addShapes": [roof_ramp] + gallery_floors,
    "relief": {"team": relief_team},
    # The stack is written bottom-up or the lower storeys are painted by the
    # upper ones: the painter walks layers in document order and each pass
    # paints its layer's whole column from the bedrock course up.
    #
    # All three carry kind "made". The crag stands ON the dale rather than
    # being a storey of it, and the word is what keeps the stacking rules off
    # it: SK10's pair walk reads a solid mass sinking into ground as a lost
    # gap, and SK11's reachability walk reads its roof as standable ground
    # somebody forgot a stair to. `part_of` names the one thing the three
    # slices belong to.
    "addLayers": [
        {"id": "workings", "kind": "made", "part_of": "crag", "name": "Workings", "base_y": 0,
         "shapes": workings, "groups": [{"id": "workings", "shapeIds":
                                         [s["id"] for s in workings]}]},
        {"id": "roof", "kind": "made", "part_of": "crag", "name": "Crag roof", "base_y": 0,
         "shapes": roof, "groups": [{"id": "roof", "shapeIds":
                                     [s["id"] for s in roof]}]},
        {"id": "crown", "kind": "made", "part_of": "crag", "name": "Crown", "base_y": 0,
         "shapes": crown, "groups": [{"id": "crown", "shapeIds":
                                      [s["id"] for s in crown]}]},
    ],
    "biome": {"kind": "solid", "biome": 3},
    "roomStyles": {"spawn": spawn_style},
    "dressing": {"styles": {}, "props": dressing_props},
}

with open(os.path.join(D, f"{SLUG}.plan.json"), "w") as fh:
    json.dump(plan, fh, indent=1)
with open(os.path.join(D, f"{SLUG}.finish.json"), "w") as fh:
    json.dump(finish, fh, indent=1)
print(f"wrote {SLUG}: {len(workings)} rock, {len(roof)} roof, {len(crown)} crown")
