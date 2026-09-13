#!/usr/bin/env python3
"""Ruddle Brink — one continuous red scarp, broken in exactly three places.

Writes opus5-ruddle-brink.plan.json and opus5-ruddle-brink.finish.json.

The board in one sentence: a core board where each team holds a low red bench
under its own cliff, and the face above that bench is broken in three places —
a scree, a cut road and a long ramp — which are the only ways onto the plateau.

Geometry, in blocks:
  plateau  z -100..-74  y23      the defenders' ground, spawn at the back
  face     z  -78..-72           the scarp: high 23, low 12, six blocks across
  bench    z  -72..-12  y12      the fighting ground, the core stands on it
  void     z  -12..+12           the strait, crossed by a build zone

The face is climbed in exactly three places, and no two cost the same thing:
a scree the relief leaves unpinned at the west end, and two ramps somebody
built — embankments standing on the bench and climbing north into the face,
so each spends ten blocks of cliff rather than the twenty-two its run needs.
"""
import json, os

D = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus5-ruddle-brink"
CELL = 4

# ---------------------------------------------------------------- materials
def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

RED_SANDSTONE   = solid(179, 0)
RED_SS_SMOOTH   = solid(179, 2)
RED_SS_CHISEL   = solid(179, 1)
RED_SAND        = solid(12, 1)
CLAY_ORANGE     = solid(159, 1)
CLAY_RED        = solid(159, 14)
CLAY_BROWN      = solid(159, 12)
HARDENED_CLAY   = solid(172, 0)
SANDSTONE       = solid(24, 0)
SS_SMOOTH       = solid(24, 2)
SS_CHISEL       = solid(24, 1)
GRAVEL          = solid(13, 0)
ANDESITE        = solid(1, 5)
COBBLE          = solid(4, 0)
STONE           = solid(1, 0)
SPRUCE_PLANK    = solid(5, 1)
SPRUCE_LOG      = solid(17, 1)

def depth_stack(*pairs, beyond=None):
    """A depth-axis stack: (material, courses) top-down, then `beyond` below."""
    return {"kind": "layered", "axis": "depth",
            "beyond": beyond or RED_SANDSTONE,
            "stack": {"ending": "handOver",
                      "bands": [{"material": m, "thickness": t} for m, t in pairs]}}

def slope_stack(*bands):
    """A slope-axis stack: (material, degrees) from flat to sheer."""
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}}

# ---------------------------------------------------------------- the plan
plan = {
    "plan": 2,
    "meta": {"name": "Ruddle Brink"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 12,
                "surface": 23, "observerY": 48},
    "pieces": [
        # One piece for the whole team half. The two tiers are the relief's
        # job, not the plan's — a piece states arrangement, not landform.
        # Two pieces, one landmass: the brow is the full width of the board and
        # the bench under it is not, so the cliff runs out over void at both
        # ends as a headland and the bench has no corner a journey never reaches.
        {"id": "brow",  "role": "piece", "rect": [-11, -25, 22, 7], "surface": 23},
        {"id": "bench", "role": "piece", "rect": [-9, -18, 18, 15], "surface": 12},
        # The spawn sits off the centre line, so a team's own walk to its core
        # runs diagonally and sweeps ground a centred one would leave dead.
        {"id": "spawn", "role": "spawn", "rect": [0, -25, 6, 3], "surface": 23},
    ],
    "zones": [
        # The strait. The two halves are joined by build zone over void and
        # by nothing else: a crossing an attacker pays for.
        {"id": "strait", "rect": [-9, -3, 18, 6], "holes": []},
    ],
    "placements": {
        "spawns": [
            # at: BLOCKS from the piece's minimum corner (-12, -120).
            {"id": "spawn-1", "piece": "spawn", "at": [12, 6], "facing": "back",
             "footprint": [5, 2, 14, 8]},
        ],
        "wools": [], "iron": [], "destroyables": [],
        "cores": [
            # at: BLOCKS from the bench's minimum corner (-36, -72) — measured
            # against /plan/inspect, whatever the field description says.
            # World (-14, -66): off the centre line, so both flanks are walked.
            # The piece is named so /plan/inspect can walk GO1's ratio at all.
            {"id": "core-1", "piece": "bench", "at": [14, 10],
             "lava": 3, "lavaHeight": 3, "float": 6, "leak": 5},
        ],
    },
    "walls": [], "boxes": [],
}

# ------------------------------------------------------------ relief marks
# The plateau pad, notched back at x -50..-36 so the west break has twenty
# blocks of unpinned ground to fall through instead of six. Its ring is a
# lobed polygon and not a rectangle: a four-vertex area mark builds a mesa
# with literal square sides.
plateau_ring = [
    [-44, -100], [-22, -102], [2, -100], [26, -101], [44, -100],
    [44, -76], [34, -74], [16, -76], [-6, -74], [-18, -76],
    [-20, -92], [-34, -92], [-36, -75], [-42, -76],
]
# The bench pad. It reaches north into the scree window so the two pads face
# each other across twenty blocks of free ground rather than across the face.
bench_ring = [
    [-36, -70], [-34, -71], [-20, -71], [-7, -70], [6, -71], [22, -70],
    [33, -71], [36, -70], [36, -18], [20, -14], [0, -17], [-20, -14],
    [-36, -18],
]

SCARP_Z = -75
def scarp(idx, x_from, x_to):
    """A segment of the lip. Traced east to west, so the high band — the
    plateau — lands on the -z side, which is where the defenders are."""
    return {"id": f"lip-{idx}", "kind": "scarp",
            "points": [[x_from, SCARP_Z], [x_to, SCARP_Z]],
            "high": 23, "low": 12, "face": 2, "band": 7}

relief_team = {
    "base": 12,
    "reach": 0,
    "step": 1,
    "landform": "rolling",
    "grain": {"amplitude": 1.6, "scale": 21, "seed": 41},
    "marks": [
        {"id": "plateau-pad", "kind": "area", "h": 23, "bevel": 3, "ring": plateau_ring},
        {"id": "bench-pad",   "kind": "area", "h": 12, "bevel": 4, "ring": bench_ring},
        # Two segments, one gap. The gap is the scree; the other two ways up
        # are built, and stand against an unbroken face.
        scarp(1,  44, -20),
        scarp(2, -34, -44),
    ],
    "pushes": [
        # Two shoulders flanking the spawn rather than one ridge across it.
        # A push is added to the surface the marks solved, so a skirt that
        # reaches the lip grades the lip: both of these stop at z -88 with a
        # falloff of 6, which dies at -82, six blocks clear of the face.
        # amount/falloff 7/6 = 1.17 a block against crown/half 5/5 = 1.0 —
        # the two gradients agree, so each reads as a hillside, not a wall.
        {"id": "shoulder-w", "amount": 7, "falloff": 6, "crown": 5,
         "roughness": 3, "seed": 7,
         "ring": [[-42, -100], [-34, -98], [-26, -100], [-26, -90],
                  [-34, -88], [-42, -90]]},
        {"id": "shoulder-e", "amount": 7, "falloff": 6, "crown": 5,
         "roughness": 3, "seed": 11,
         "ring": [[26, -100], [34, -98], [42, -100], [42, -90],
                  [34, -88], [26, -90]]},
    ],
}

# ------------------------------------------------------- the two built ways
# A flight is made, so it is one material the whole way up and it keeps the
# dressing off. Each runs at least twice its rise (11), and each climbs in z
# as an embankment standing on the bench — which is what lets a way up spend
# ten blocks of cliff instead of the twenty-two its run would need along it.
cut_road = {
    "id": "cut-road", "type": "polygon", "operation": "add", "override": True,
    "keepClear": True, "height_mode": "level", "skirt": 2, "floor": 0,
    "vertices": [[-7, -52], [6, -52], [6, -76], [-7, -76]],
    "anchor_heights": [12, 12, 23, 23],
    "material": SS_SMOOTH,
}
long_ramp = {
    "id": "long-ramp", "type": "polygon", "operation": "add", "override": True,
    "keepClear": True, "height_mode": "level", "skirt": 2, "floor": 0,
    "vertices": [[22, -46], [33, -46], [33, -76], [22, -76]],
    "anchor_heights": [12, 12, 23, 23],
    "material": SS_SMOOTH,
}
# Talus under the scree and at each ramp's foot — splotches, drawn, not
# sampled: where two grounds meet the edge is a shape.
def patch(pid, pts, theme):
    """A paint patch states a height_mode, and that is the whole of why it
    paints. ShapeScopeOwners gives a cell to the smallest shape whose own top
    EQUALS the tallest top there -- so a one-course add at bedrock, with or
    without `override`, is never a candidate and paints nothing at all, in
    silence. A shape declaring level/raise/sink is `standing` instead, and a
    standing shape is always a candidate whatever its height. `raise` of zero
    sits flush at the median ground under the patch, which is why each of
    these is drawn on flat ground: on a slope it would read as a plate."""
    return {"id": pid, "type": "polygon", "operation": "add",
            "height_mode": "raise", "base_height": 0, "skirt": 0,
            "vertices": pts, "theme": theme}

def talus(idx, pts):
    return patch(f"talus-{idx}", pts, "scree")

talus_shapes = [
    # Scree at the foot of the face, under the one way up the relief left
    # unpinned, and a fan at the toe of each built ramp.
    talus(1, [[-34, -66], [-29, -56], [-17, -54], [-14, -62], [-21, -67]]),
    talus(2, [[-12, -50], [-2, -44], [10, -47], [11, -54], [-6, -55]]),
    talus(3, [[19, -44], [29, -38], [36, -42], [35, -48], [23, -49]]),
    # The made ground: the apron a spawn stands on and the heads of the two
    # ways up, which is where the work on this cliff was done.
    patch("apron", [[2, -99], [22, -99], [24, -89], [16, -86],
                    [4, -87], [0, -92]], "works"),
    patch("head-cut", [[-9, -84], [8, -84], [9, -79], [-8, -79]], "works"),
    patch("head-ramp", [[20, -84], [35, -84], [35, -79], [21, -79]], "works"),
]

# ---------------------------------------------------------------- themes
brink = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "boundary",
    "wallOnTerrainFaces": True,
    # The rim is off: this ground is relief-solved, and a rim caps every fall
    # with a band and turns a hillside into contour lines.
    "rim": {"enabled": False, "depth": 1, "material": RED_SS_SMOOTH},
    "surface": {"enabled": True, "depth": 4, "material": slope_stack(
        # flat: wind-blown sand over rock
        (depth_stack((RED_SAND, 1), (CLAY_ORANGE, 2), beyond=RED_SANDSTONE), 18),
        # shoulder: the sand thins and the clay shows
        (depth_stack((CLAY_ORANGE, 1), (CLAY_RED, 2), beyond=RED_SANDSTONE), 22),
        # face: bare rock, which is what a scarp is
        (depth_stack((RED_SANDSTONE, 2), (RED_SS_SMOOTH, 2), beyond=RED_SANDSTONE), 50),
    )},
    # A cliff is what the wall bucket paints, so the strata go here — and in
    # the fill, or the face is banded at the top and plain all the way down.
    "wall": {"kind": "wallRun", "runs": [
        {"material": RED_SANDSTONE, "width": 4},
        {"material": CLAY_RED, "width": 1},
        {"material": RED_SS_SMOOTH, "width": 3},
        {"material": CLAY_BROWN, "width": 1},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 23, "cellSize": 13, "rise": 7,
             "bands": [{"material": RED_SANDSTONE, "depth": 2},
                       {"material": HARDENED_CLAY, "depth": 1}]},
}
scree = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": GRAVEL},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (GRAVEL, 1), (ANDESITE, 2), beyond=RED_SANDSTONE)},
    "wall": {"kind": "wallRun", "runs": [
        {"material": ANDESITE, "width": 3},
        {"material": GRAVEL, "width": 1},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 5, "cellSize": 11, "rise": 6,
             "bands": [{"material": STONE, "depth": 2},
                       {"material": ANDESITE, "depth": 1}]},
}
works = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "boundary",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": SS_CHISEL},
    "surface": {"enabled": True, "depth": 3, "material": depth_stack(
        (SS_SMOOTH, 1), (SANDSTONE, 2), beyond=SANDSTONE)},
    # A made face is striped along its perimeter and sheared by height.
    "wall": {"kind": "wallDiagonal", "slope": 2, "runs": [
        {"material": SANDSTONE, "width": 3},
        {"material": SS_CHISEL, "width": 1},
        {"material": SS_SMOOTH, "width": 2},
    ]},
    "wallEnabled": True,
    "fill": {"kind": "voronoi", "seed": 11, "cellSize": 12, "rise": 7,
             "bands": [{"material": SANDSTONE, "depth": 2},
                       {"material": STONE, "depth": 1}]},
}

# ------------------------------------------------------------- spawn shell
# Forked from the shipped `longhouse`: the timber stays, the footing goes
# (a footing over a one-course plate is a rim round a building), and the
# walls leave the ground's family — red rock outside, spruce and pale
# sandstone in the hall.
spawn_style = {
    "foundation": {
        "plate": {"stack": {"bands": [{"material": SS_SMOOTH, "thickness": 1}],
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
        {"material": SS_SMOOTH, "thickness": 2},
        {"material": SPRUCE_PLANK, "thickness": 4},
    ], "ending": "repeat"}, "extent": 6},
    "post": SPRUCE_LOG,
    "windows": {"form": "arched", "block": 134, "hostBlock": 5, "hostData": 1,
                "data": 0, "sill": 4, "width": 2, "height": 2, "spacing": 2},
    "storeys": [],
    "porch": None, "front": None,
    "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
    "doorway": {"door": "air", "head": {"form": "arched", "block": 134,
                "fill": "upperSlab", "fillBlock": 126, "fillData": 1},
                "width": 3, "height": 4},
}


# ---------------------------------------------------------------- dressing
# Nothing is scattered. Every prop answers "why here": the road is the reason
# the cut is made, the cot is what watches it, the rock is what came off the
# face, and the cover is one shape over the whole bench.
COARSE_DIRT = solid(3, 1)

# A gate cot at the head of the cut road — pale timber and sandstone, which is
# the built family and not the red the ground is made of.
cot_style = {
    "kind": "house",
    "shell": {
        "foundation": {
            "plate": {"stack": {"bands": [{"material": SANDSTONE, "thickness": 1}],
                                "ending": "repeat"}, "extent": 1},
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
            {"material": SS_SMOOTH, "thickness": 2},
            {"material": SPRUCE_PLANK, "thickness": 3},
        ], "ending": "repeat"}, "extent": 5},
        "post": SPRUCE_LOG,
        "windows": {"form": "arched", "block": 134, "hostBlock": 5, "hostData": 1,
                    "data": 0, "sill": 3, "width": 1, "height": 2, "spacing": 3},
        "storeys": [], "porch": None, "front": None,
        "beams": {"block": 17, "data": 1, "reach": 1, "any": True},
        "doorway": {"door": "air", "head": {"form": "arched", "block": 134,
                    "fill": "upperSlab", "fillBlock": 126, "fillData": 1},
                    "width": 2, "height": 3},
    },
}

# A path is solid and three colours a reader cannot quite tell apart.
PAVE = {"kind": "cell", "seed": 31, "cellSize": 9, "entries": [
    {"material": SANDSTONE}, {"material": SS_SMOOTH}, {"material": HARDENED_CLAY}]}

dressing_props = [
    # The made road: spawn door, down the cut, out to the core's ground.
    {"id": "haul-road", "kind": "stroke", "style": "solid", "claimsGround": True,
     "radius": 2, "seed": 4, "pave": PAVE,
     "points": [[12, -92], [6, -84], [0, -76], [-2, -62], [-14, -58], [-22, -60]]},
    # The cot that watches the head of the long ramp. It stands east of the
    # spawn door's approach, which is the ground DR-KEEP holds and the only
    # place on this brow a building may not go.
    {"id": "gate-cot", "kind": "house", "seed": 11, "front": "posZ",
     "style": "cot", "wings": [{"corners": [[24, -87], [32, -80]]}]},
    # Rock off the face, on the talus fans and nowhere else.
    # Every one of these was probed with loop.py --candidates before it was
    # written down: OB19's ring round the core is wider than it sounds, and
    # both ramps hold their own ground.
    {"id": "spall-0", "kind": "boulder", "x": -34, "z": -58, "seed": 21, "radius": 3},
    {"id": "spall-1", "kind": "boulder", "x": -32, "z": -48, "seed": 22, "radius": 2},
    {"id": "spall-2", "kind": "boulder", "x": -12, "z": -44, "seed": 23, "radius": 2},
    {"id": "spall-3", "kind": "boulder", "x": 16,  "z": -40, "seed": 24, "radius": 3},
    {"id": "spall-4", "kind": "boulder", "x": 30,  "z": -30, "seed": 25, "radius": 2},
    # Cover is one shape over the whole bench, and the field does the patchiness.
    # Both gameplay numbers stay low: high coverage is ground a player cannot
    # read, and tall grass is cover nobody authored in front of an objective.
    {"id": "bench-cover", "kind": "flora", "seed": 9,
     "points": [[-36, -70], [36, -70], [36, -16], [0, -14], [-36, -18]],
     "spec": {"coverage": 0.18, "scale": 26, "octaves": 2, "fernShare": 0.25,
              "flowerShare": 0.05, "flowerScale": 14, "tallShare": 0.04}},
]

# ---------------------------------------------------------------- finish
finish = {
    "created": "2026-09-12",
    "authors": ["Opus 5"],
    "themes": {"brink": brink, "scree": scree, "works": works},
    "mapTheme": "brink",
    "addShapes": [cut_road, long_ramp] + talus_shapes,
    "bendShapes": {"bench-12": {"k": 0.20, "wander": 3, "step": 9, "seed": 5}},
    "relief": {"team": relief_team},
    "roomStyles": {"spawn": spawn_style},
    # Mesa, so the biome comes to meet the ground: its grass tint is #90814d,
    # which reads as one dry floor beside red rock where Plains' #91bd59 would
    # read as neither. A tinted block's family is the biome's to decide.
    "biome": {"kind": "solid", "biome": 37},
    "dressing": {"styles": {"cot": cot_style}, "props": dressing_props},
}

with open(os.path.join(D, f"{SLUG}.plan.json"), "w") as fh:
    json.dump(plan, fh, indent=1)
with open(os.path.join(D, f"{SLUG}.finish.json"), "w") as fh:
    json.dump(finish, fh, indent=1)
print(f"wrote {SLUG}.plan.json and {SLUG}.finish.json")
