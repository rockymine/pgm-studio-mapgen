#!/usr/bin/env python3
"""Quadrangle -- a FOUR-TEAM CTW board, adapted from a composed two-team unit.

`GET /api/compose` answers 400 for `rot_90` and for `teams=4`, so the composer is what refuses four
teams; the plan tier does not. What is composed here is the *arrangement*: the unit is the ring hub
of `GET /api/compose?players=30&symmetry=rot_180&seed=7` -- hub `ring` with a yard in the middle,
frontline `none`, wools `i`/`i`, score 1.881, 56 land cells, the smallest two-team board in the
first two hundred seeds -- reshaped to fit a quadrant and then fanned with `globals.symmetry:
"rot_90"`, which `Symmetry.Order` reads as 4.

    four walled quadrangles set corner to corner round a crossed court, each with a cloistered
    yard in the middle of it and two faces to defend instead of one.

What the adaptation took:

  * the unit had to fit a QUADRANT before the symmetry was flipped, not after. Seed 7's unit spans
    x -35..30 by z 10..60 about the origin; fanned four ways as drawn it walks through its own
    images. Redrawn inside x 10..80, z 10..90 -- strictly inside the +x/+z quadrant -- the four
    images tile the plane and never touch.
  * a ring hub has a yard, and a yard in a composed plan is a hole the compiler cuts as a
    `subtract`. It is kept: a colonnade of twelve pillars stands round it on the ring itself, so
    the quadrangle has a cloister and the hole is what the cloister is round.
  * the composer emits one zone, a mid band between two fanned images. Four teams need a shape that
    reaches all four, and `rot_90` maps a cross onto itself: one zone, x -10..10 by z -60..60,
    fans into the crossed court the whole board is fought over.
  * DESTROY OBJECTIVES ARE ORDER-2 ONLY, so this is CTW and carries no destroyable and no core.
  * each quadrant's two outer sides are a terrace three courses over its court, carrying a
    crenellated curtain and an angle tower; the two flights down into the court are the only walks.

Run: python3 specs/opus5-quadrangle/build-spec.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "tools", "sculpt")))
import props

SLUG = "opus5-quadrangle"
CELL = 5
COURT, TERRACE = 11, 14
COURT_Y, TERRACE_Y = COURT, TERRACE
S, T = COURT, TERRACE

pieces=[]
def P(pid, role, x, z, w, h, surface=S, **kw):
    pieces.append(dict(id=pid, role=role, rect=[x,z,w,h], surface=surface, **kw))
P("corner-sw","piece",2,2,3,3,T)      # x 10..25 z 10..25
P("frontline-s","piece",5,2,6,2,T)    # x 25..55 z 10..20
P("frontline-w","piece",2,5,3,7,T)    # x 10..25 z 25..60
P("hub-s","piece",5,4,6,2)            # x 25..55 z 20..30
P("hub-w","piece",5,6,2,4)            # x 25..35 z 30..50
P("hub-e","piece",9,6,2,4)            # x 45..55 z 30..50
P("hub-n","piece",5,10,6,2)           # x 25..55 z 50..60
P("spawn-t1","piece",11,11,2,2)       # x 55..65 z 55..65
P("spawn-room","spawn",13,11,2,2)     # x 65..75 z 55..65
P("wool-a-app","piece",6,12,4,2)      # x 30..50 z 60..70
P("wool-a-neck","piece",10,12,1,2)    # x 50..55 z 60..70
P("wool-a-s","piece",6,14,5,1)        # x 30..55 z 70..75

P("wool-a-room","wool-room",6,15,2,2) # x 30..40 z 75..85
P("wool-a-w","piece",5,15,1,2)        # x 25..30 z 75..85
P("wool-a-e","piece",8,15,1,2)        # x 40..45 z 75..85
P("wool-a-n","piece",5,17,4,1)        # x 25..45 z 85..90
P("wool-b-app","piece",11,6,2,4)      # x 55..65 z 30..50
P("wool-b-room","wool-room",13,7,2,2) # x 65..75 z 35..45
P("wool-b-s","piece",13,5,3,2)        # x 65..80 z 25..35
P("wool-b-n","piece",13,9,3,1)        # x 65..80 z 45..50
P("wool-b-e","piece",15,7,1,2)        # x 75..80 z 35..45

plan = {
    "plan": 2,
    "meta": {"name": "Quadrangle"},
    "globals": {"cell": CELL, "symmetry": "rot_90", "maxPlayers": 20, "surface": COURT,
                "observerY": 60},
    "pieces": pieces,
    # one zone, and rot_90 maps it onto itself: the arm x -10..10 fans into a cross whose four
    # quadrants are the four teams' ground
    "zones": [{"id": "cross", "rect": [-2, -12, 4, 24], "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [5, 7], "facing": "left"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [{"a": "wool-a-app", "b": "hub-n"}, {"a": "wool-b-app", "b": "hub-e"}],
    "boxes": [],
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as out:
    json.dump(plan, out, indent=1)
print("wrote the plan")

# ── materials: pale ground, dark masonry, one accent ─────────────────────────────────────────────
def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
SAND, SANDSTONE, SMOOTH_SS, CHIS_SS = solid(12), solid(24), solid(24, 2), solid(24, 1)
STONE, COBBLE, ANDESITE = solid(1), solid(4), solid(1, 5)
STONEBRICK, CHIS_BRICK, GRAVEL = solid(98), solid(98, 3), solid(13)
DARK_LOG = solid(162, 1)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver", beyond=None):
    out = {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}
    if beyond is not None: out["beyond"] = beyond
    return out

ROCK_BODY = {"kind": "voronoi", "seed": 81, "cellSize": 11, "rise": 4, "bands": [
    {"depth": 1, "material": COBBLE}, {"depth": 2, "material": ANDESITE},
    {"depth": 1, "material": SANDSTONE}]}

VELD = layered([(1, cell_(82, 9, [GRASS, SAND])), (2, DIRT), (2, SANDSTONE)])
SCALD = layered([(1, cell_(83, 7, [COARSE, SAND])), (2, DIRT), (2, SANDSTONE)])
BLUFF = layered([(2, cell_(84, 6, [SANDSTONE, STONE])), (4, SANDSTONE)], beyond=SANDSTONE)
COURT_SURFACE = layered([(14, VELD), (14, SCALD), (62, BLUFF)], axis="slope", ending="repeat")

ASHLAR = cell_(85, 4, [SMOOTH_SS, SANDSTONE], rise=2)
SETTS = cell_(86, 5, [ANDESITE, STONEBRICK], rise=3)
MADE = cell_(87, 4, [ANDESITE, STONEBRICK], rise=3)
STEPS = cell_(88, 4, [STONEBRICK, COBBLE], rise=2)

themes = {
    "court": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": SANDSTONE},
        "surface": {"enabled": True, "depth": 5, "material": COURT_SURFACE},
        "wall": layered([(1, SAND), (2, SANDSTONE), (5, STONE)], beyond=ANDESITE),
        "wallEnabled": True,
        "fill": ROCK_BODY,
    },
    # the rampart, and the one place on the board a teamTint reads as ownership: four quadrants,
    # four landmasses, four colours, and a player reads whose wall they are under from the court.
    "rampart": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": CHIS_BRICK},
        "surface": {"enabled": True, "depth": 2, "material": SETTS},
        "wallEnabled": True,
        "wall": {"kind": "wallDiagonal", "slope": 2, "runs": [
            {"material": ANDESITE, "width": 4},
            {"material": {"kind": "teamTint", "blockId": 159, "neutral": solid(159, 8)}, "width": 1},
            {"material": STONEBRICK, "width": 3},
            {"material": COBBLE, "width": 2}]},
        "fill": ROCK_BODY,
    },
    # the cloister's floor, flagged rather than grown: the one splotch on the board, and it is
    # where the colonnade stands
    "cloister": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": CHIS_SS},
        "surface": {"enabled": True, "depth": 2, "material": ASHLAR},
        "wall": layered([(2, SANDSTONE), (3, SMOOTH_SS)], beyond=SANDSTONE),
        "wallEnabled": True,
        "fill": ROCK_BODY,
    },
}

# ── reshaping the compiled outlines ──────────────────────────────────────────────────────────────
COURT_SHAPE, TERRACE_SHAPE = "corner-sw-11", "corner-sw-14"

TERRACE_RING = [[10, 10], [55, 10], [55, 20], [25, 20], [25, 60], [10, 60]]
COURT_RING = [[25, 20], [55, 20], [55, 30], [65, 30], [65, 25], [80, 25], [80, 50], [55, 50],
              [55, 55], [75, 55], [75, 65], [55, 65], [55, 75], [45, 75], [45, 90], [25, 90],
              [25, 75], [30, 75], [30, 60], [25, 60]]

terrace_edits = [
    # the outer angle chamfered first, so the quadrangle turns its corner on a bevel rather than a
    # point. It goes first because an insert shifts every index after it and the two notches below
    # are stated against the ring this leaves.
    {"index": 0, "x": 10, "z": 16}, {"after": 0, "x": 16, "z": 10},
    # a re-entrant in each inner lip, cut to exactly the flight that fills it: the two ways down
    # off the rampart into the court, and the only ones
    {"after": 3, "x": 42, "z": 20}, {"after": 4, "x": 42, "z": 16},
    {"after": 5, "x": 34, "z": 16}, {"after": 6, "x": 34, "z": 20},
    {"after": 8, "x": 25, "z": 34}, {"after": 9, "x": 21, "z": 34},
    {"after": 10, "x": 21, "z": 42}, {"after": 11, "x": 25, "z": 42},
]
court_edits = [
    # the court's own outer corners taken in. Every move is INWARD; a corner pushed out over void
    # builds a stub at the shape's own floor and nothing declines it.
    {"index": 5, "x": 77, "z": 27}, {"index": 6, "x": 77, "z": 48},
    {"index": 14, "x": 43, "z": 88}, {"index": 15, "x": 27, "z": 88},
    # and a bite out of the long back edge, so the court is not a staircase of rectangles
    {"after": 11, "x": 51, "z": 69},
]

def simulate(ring, ops):
    ring = [list(p) for p in ring]
    for op in ops:
        if "remove" in op: ring.pop(op["remove"])
        elif "index" in op: ring[op["index"]] = [op["x"], op["z"]]
        else: ring.insert(op["after"] + 1, [op["x"], op["z"]])
    return ring

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
def flight(fid, ring, low, high, material=None):
    return {"id": fid, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": material or STEPS,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}

add_shapes = [
    # the two ways down off the rampart, each filling the re-entrant cut for it: twelve blocks of
    # run for three courses
    flight("stair-south", [(34, 28), (42, 28), (42, 16), (34, 16)], COURT, TERRACE),
    flight("stair-west", [(30, 34), (30, 42), (18, 42), (18, 34)], COURT, TERRACE),
    # the cloister's floor: a RING, drawn as one even-odd annulus rather than a disc, because the
    # yard inside it is the compiled subtract and SK13 refuses any add that puts ground back there
    {"id": "cloister-floor", "type": "polygon", "operation": "add", "group": "team",
     "base_height": COURT, "theme": "cloister",
     "vertices": [[round(x, 1), round(z, 1)] for x, z in props.annulus(40, 40, 17, 17, 5)]},
]

def lobe(cx, cz, radii, turn=0.0):
    import math
    n = len(radii)
    return [[round(cx + r * math.cos(turn + 2 * math.pi * i / n), 1),
             round(cz + r * math.sin(turn + 2 * math.pi * i / n), 1)]
            for i, r in enumerate(radii)]

relief = {"team": {
    "base": COURT, "step": 1, "reach": 16, "landform": "rolling",
    "grain": {"amplitude": 2, "scale": 15, "seed": 31},
    "marks": [
        # the cloister's own pad, flat and stated flat: twelve pillars state an absolute floor and
        # ground solved under them either buries them or leaves them on air
        {"id": "cloister-pad", "kind": "area", "h": COURT,
         "ring": lobe(40, 40, [15, 14, 15, 14, 15, 14, 15, 14])},
        # the court's own shape, outside the cloister's reach
        {"id": "hollow", "kind": "point", "at": [30, 56], "r": 4, "h": COURT - 2, "tread": 3},
        {"id": "rise", "kind": "point", "at": [51, 24], "r": 4, "h": COURT + 2, "tread": 3},
        {"id": "brae", "kind": "point", "at": [33, 82], "r": 4, "h": COURT + 2, "tread": 3},
        {"id": "sike", "kind": "point", "at": [73, 28], "r": 3, "h": COURT - 2, "tread": 2},
    ],
    "pushes": [
        # the swell across the back of the court. Ring 7 plus falloff 6 reaches thirteen blocks
        # from (48, 72); the wool room's own pad is fifteen away, so the push never lifts the
        # ground the room lays its plinth on. Gradients agree -- 3 over 6 against 3 over 6 (RL6).
        {"id": "swell", "ring": lobe(48, 72, [7, 6, 7, 6, 7, 6, 7, 6]),
         "amount": 3, "falloff": 6, "crown": 3, "roughness": 1.2, "seed": 9},
    ],
}}

# ── the structures ───────────────────────────────────────────────────────────────────────────────
def made(layers, part, material):
    out = []
    for layer in (layers if isinstance(layers, list) else [layers]):
        inner = layer.pop("layout")
        layer["shapes"], layer["groups"] = inner["shapes"], inner["groups"]
        layer["kind"], layer["part_of"] = "made", part
        for shape in layer["shapes"]:
            shape.pop("theme", None)
            shape["material"] = material
        out.append(layer)
    return out

structures = []
# the curtain along both outer lips, stopping short of the chamfered angle
structures += made(props.crenellated_wall("curtain-s", 16, 10, 55, 12, 1, TERRACE_Y, 4, None,
                                          merlon=3, crenel=2, parapet=2, name="South curtain"),
                   "quadrangle", MADE)
structures += made(props.crenellated_wall("curtain-w", 10, 16, 12, 60, 1, TERRACE_Y, 4, None,
                                          merlon=3, crenel=2, parapet=2, name="West curtain"),
                   "quadrangle", MADE)
# the angle tower, inside the bevel where the two curtains turn
structures += made(props.drum_tower("angle-tower", 19, 19, 4, 1, TERRACE_Y, 14, None, merlons=8,
                                    parapet=3, name="Angle tower"), "quadrangle", MADE)
# and the cloister: twelve pillars on the ring round the yard, which is the one form on these four
# boards that is neither a wall nor a tower
structures += made(props.colonnade("cloister", 40, 40, 12, 12, 1.5, COURT_Y, 7, None,
                                   name="The cloister"), "quadrangle", MADE)

# ── dressing ─────────────────────────────────────────────────────────────────────────────────────
ROAD_PAVE = cell_(89, 4, [GRAVEL, COARSE, SANDSTONE])
props_list = [
    {"id": "way", "kind": "stroke", "seed": 71, "radius": 2.5, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": ROAD_PAVE,
     "points": [[66, 60], [58, 56], [50, 54], [40, 55], [30, 52], [27, 44], [28, 36]]},
    {"id": "sward", "kind": "flora", "seed": 9,
     "points": [[25, 20], [80, 25], [75, 65], [45, 90], [25, 90], [25, 60]],
     "spec": {"coverage": 0.18, "scale": 15, "octaves": 3, "fernShare": 0.06,
              "flowerShare": 0.05, "flowerScale": 20, "tallShare": 0.02}},
]
# two rocks and three thorns, every one of them on a cell `sketch/seats` and
# `loop.py --candidates` answered for -- on a board this tightly claimed, a guess is a decline
for i, (bx, bz, form, size) in enumerate([(50, 22, "angular", 3), (61, 31, "round", 2)]):
    props_list.append({"id": f"crag-{i}", "kind": "boulder", "x": bx, "z": bz, "form": form,
                       "size": size, "mossy": False, "rock": ANDESITE if i % 2 else STONE,
                       "seed": 90 + i})
for i, (tx, tz, sp, h) in enumerate([(47, 36, "oak", 8), (61, 46, "oak", 9), (30, 31, "oak", 7)]):
    props_list.append({"id": f"thorn-{i}", "kind": "tree", "x": tx, "z": tz, "form": "Template",
                       "species": sp, "height": h, "seed": 95 + i})

# NO BUILDING. A quadrant unit is built from ranges ten blocks deep, and `DR-PASS` wants eight
# blocks of passable ground along a building's whole side: a five-deep house in a ten-deep range
# leaves four, and `sketch/seats` offers the seat anyway because the roof reaches a block past the
# walls it was asked about. The quadrangle's architecture is its curtain, its angle tower and its
# cloister, which are made layers and are not judged by that rule.

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-16",
    "voidEnforcement": True,
    "mapTheme": "court",
    "themes": themes,
    "biome": {"kind": "solid", "id": 35},
    "themeById": {COURT_SHAPE: "court", TERRACE_SHAPE: "rampart"},
    "shapePropsById": {TERRACE_SHAPE: {"relief_scope": "exclude"}},
    "editShapes": {TERRACE_SHAPE: terrace_edits, COURT_SHAPE: court_edits},
    "addShapes": add_shapes,
    "addLayers": structures,
    "relief": relief,
    "roomStyles": {"spawn": "@sb-blockhouse", "wool": "@showcase-cage"},
    "dressing": {"props": props_list},
}

with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as out:
    json.dump(finish, out, indent=1)
print("wrote the finish:", len(structures), "made layers,", len(add_shapes), "shapes,",
      len(props_list), "props")
