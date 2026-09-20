#!/usr/bin/env python3
"""Portway -- a composed twin frontline taken over as a breached rampart with a pier in the water.

Composed from `GET /api/compose?players=30&symmetry=mirror_z&seed=2` -- hub `bar` (one 9x6 piece),
frontline `twin` with an eight-cell hole between its prongs, wools `i`/`i`, score 0.000, 123 land
cells, 85 x 170 blocks. Rebuilt round one idea:

    the front is a built rampart with a hole punched through it that nobody can close, and the
    crossing is made at a stone pier standing in the middle of the gap.

What the composer gave and what was done with it:

  * the `twin` frontline's own hole is kept and is the board's subject. The two prongs are raised
    four courses into stone bastions; the notch between them is void from the mid band to the
    apron, so the middle of the rampart is a breach and the fight funnels either side of it.
  * the composer places no middle island on any board. `zones` takes more than one entry, so the
    mid band is four zones with a `pier` piece seated in the hole they leave -- a neutral stone
    stump two courses over the heath, ten blocks from each front, with a beacon on it.
  * the spawn was moved ten blocks west and the two wools re-hung. The composed board walks 153
    blocks to one wool and 138 to the other; on this one the far pair is 1.07 apart and the two
    raids are at different depths rather than mirror images.
  * each wool ward hangs off the hub on exactly one twenty-block seam, and both seams carry the
    plan's bedrock approach wall -- which the composer emits as `"walls": []` on every board.
  * a gatehouse of two drum towers, an arch and two crenellated curtains closes the hub's front
    across its whole width, with two-block slips at the ends so nothing is sealed.

Run: python3 specs/opus5-portway/build-spec.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "tools", "sculpt")))
import props

SLUG = "opus5-portway"
CELL = 5
HEATH, PIER, DECK = 12, 14, 16
HEATH_Y, PIER_Y, DECK_Y = HEATH, PIER, DECK

pieces = []
def P(pid, role, x, z, w, h, surface, **kw):
    pieces.append(dict(id=pid, role=role, rect=[x, z, w, h], surface=surface, **kw))

# the hub: the composed nine-by-six bar, untouched
P("hub-t1", "piece", -4, 8, 9, 6, HEATH)            # x -20..25  z 40..70
# the frontline: the composed twin, its apron left as heath and its two prongs raised into bastions
P("frontline-t1", "piece", -4, 5, 9, 3, HEATH)      # x -20..25  z 25..40
P("frontline-t2", "piece", -4, 3, 3, 2, DECK)       # x -20..-5  z 15..25
P("frontline-t3", "piece", 2, 3, 3, 2, DECK)        # x  10..25  z 15..25
#   and between them the breach: x -5..10, z 15..25, void, and kept void.  Three equal
#   thirds across the front: bastion, breach, bastion, each fifteen blocks (FR9 reads a front
#   narrower than fifteen as a funnel)

# the mid: a pier the composer would not have put there, seated in the hole the four zones leave
P("pier", "piece", -1, -1, 3, 2, PIER, mirrors=False)   # x  -5..10  z -5..5

# the spawn, ten blocks west of where the composer hung it, which is what squares the two raids
P("spawn-t1", "piece", -1, 14, 3, 2, HEATH)         # x  -5..10  z 70..80
P("spawn-room", "spawn", -1, 16, 3, 2, HEATH)       # x  -5..10  z 80..90

# the west ward, deep behind the hub
P("wool-a-app", "piece", -6, 9, 2, 4, HEATH)        # x -30..-20 z 45..65   the one seam, walled
P("wool-a-room", "wool-room", -8, 10, 2, 2, HEATH)  # x -40..-30 z 50..60
P("wool-a-n", "piece", -9, 12, 3, 1, HEATH)         # x -45..-30 z 60..65
P("wool-a-s", "piece", -9, 9, 3, 1, HEATH)          # x -45..-30 z 45..50
P("wool-a-w", "piece", -9, 10, 1, 2, HEATH)         # x -45..-40 z 50..60

# the east ward, forward of it: the same walk, ten blocks nearer the front
P("wool-b-app", "piece", 5, 8, 2, 4, HEATH)         # x  25..35  z 40..60   the one seam, walled
P("wool-b-room", "wool-room", 7, 8, 2, 2, HEATH)    # x  35..45  z 40..50
P("wool-b-n", "piece", 7, 10, 3, 1, HEATH)          # x  35..50  z 50..55
P("wool-b-e", "piece", 9, 8, 1, 2, HEATH)           # x  45..50  z 40..50
P("wool-b-s", "piece", 7, 7, 3, 1, HEATH)           # x  35..50  z 35..40

plan = {
    "plan": 2,
    "meta": {"name": "Portway"},
    "globals": {"cell": CELL, "symmetry": "mirror_z", "maxPlayers": 30, "surface": HEATH,
                "observerY": 58},
    "pieces": pieces,
    # four zones rather than the composer's one, because the pier stands in the middle of them
    "zones": [{"id": "mid-n", "rect": [-4, 1, 9, 2], "holes": []},      # x -20..25 z  5..15
              {"id": "mid-w", "rect": [-4, -1, 3, 2], "holes": []},     # x -20..-5  z -5..5
              {"id": "mid-e", "rect": [2, -1, 3, 2], "holes": []}],     # x  10..25  z -5..5
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [7, 8], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [{"a": "wool-a-app", "b": "hub-t1"}, {"a": "wool-b-app", "b": "hub-t1"}],
    "boxes": [],
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as out:
    json.dump(plan, out, indent=1)
print("wrote the plan")

# ── materials: three tone families, and the ground is the warm one ───────────────────────────────
def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}

RED_SAND, RED_SS, SMOOTH_RED = solid(12, 1), solid(179), solid(179, 2)
HARDCLAY, ORANGE_CLAY, BROWN_CLAY = solid(172), solid(159, 1), solid(159, 12)
COARSE, GRAVEL = solid(3, 1), solid(13)
SANDSTONE, SMOOTH_SS, CHIS_SS = solid(24), solid(24, 2), solid(24, 1)
STONE, COBBLE, ANDESITE, STONEBRICK, CHIS_BRICK = solid(1), solid(4), solid(1, 5), solid(98), solid(98, 3)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver", beyond=None):
    out = {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}
    if beyond is not None: out["beyond"] = beyond
    return out

CLAY_BODY = {"kind": "voronoi", "seed": 23, "cellSize": 12, "rise": 4, "bands": [
    {"depth": 1, "material": BROWN_CLAY}, {"depth": 2, "material": ORANGE_CLAY},
    {"depth": 1, "material": HARDCLAY}]}
ROCK_BODY = {"kind": "voronoi", "seed": 24, "cellSize": 9, "rise": 3, "bands": [
    {"depth": 1, "material": COBBLE}, {"depth": 2, "material": ANDESITE},
    {"depth": 1, "material": STONE}]}

DUST = layered([(1, cell_(31, 8, [RED_SAND, HARDCLAY])), (2, HARDCLAY), (2, ORANGE_CLAY)])
SCALD = layered([(1, COARSE), (2, HARDCLAY), (2, ORANGE_CLAY)])
BADLAND = layered([(2, RED_SS), (3, HARDCLAY), (3, ORANGE_CLAY)], beyond=ORANGE_CLAY)
HEATH_SURFACE = layered([(14, DUST), (14, SCALD), (62, BADLAND)], axis="slope", ending="repeat")

MASONRY = cell_(33, 5, [SANDSTONE, SMOOTH_SS], rise=3)
SETT = cell_(34, 4, [STONEBRICK, COBBLE], rise=2)
MADE_PALE = cell_(35, 4, [SANDSTONE, SMOOTH_SS], rise=3)
MADE_GREY = cell_(36, 4, [STONEBRICK, ANDESITE], rise=3)
STEPS = cell_(37, 4, [SANDSTONE, CHIS_SS], rise=2)

themes = {
    "heath": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": RED_SS},
        "surface": {"enabled": True, "depth": 5, "material": HEATH_SURFACE},
        "wall": layered([(1, RED_SAND), (2, RED_SS), (4, HARDCLAY)], beyond=ORANGE_CLAY),
        "wallEnabled": True,
        "fill": CLAY_BODY,
    },
    # the two bastions. Their face is a sawn one, so it is a wallRun -- stripes that wrap the
    # perimeter and stand upright, against the heath's bedded strata beside them.
    "works": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": CHIS_SS},
        "surface": {"enabled": True, "depth": 2, "material": MASONRY},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": SMOOTH_SS, "width": 3}, {"material": SANDSTONE, "width": 2},
            {"material": CHIS_SS, "width": 1}, {"material": RED_SS, "width": 1}]},
        "fill": CLAY_BODY,
    },
    # the pier is nobody's, and it is the one grey thing on a red board
    "pier": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": CHIS_BRICK},
        "surface": {"enabled": True, "depth": 2, "material": SETT},
        "wallEnabled": True,
        "wall": layered([(2, COBBLE), (3, STONE), (5, ANDESITE)], beyond=STONE),
        "fill": ROCK_BODY,
    },
}

# ── reshaping the compiled outlines, one vertex at a time ────────────────────────────────────────
HEATH_SHAPE, WEST_BASTION, EAST_BASTION, PIER_SHAPE = (
    "frontline-t1-12", "frontline-t1-16", "frontline-t1-16-2", "pier-14")

# the heath ring the compiler emits, for the simulation below
HEATH_RING = [[-45, 45], [-20, 45], [-20, 25], [25, 25], [25, 40], [35, 40], [35, 35], [50, 35],
              [50, 55], [35, 55], [35, 60], [25, 60], [25, 70], [10, 70], [10, 90], [-5, 90],
              [-5, 70], [-20, 70], [-20, 65], [-45, 65]]

heath_edits = [
    # a bay eaten out of the west flank, pinching the neck between the hub's front and the west
    # ward's approach. It stops north of z 39 -- the west flight's foot is at z 25..35 and a ring
    # pulled in over it would leave the first tread hanging over void.
    {"after": 1, "x": -13, "z": 43}, {"after": 2, "x": -16, "z": 39},
    # the two wards' outer corners chamfered. Every move here is INWARD: a corner pushed out hangs
    # over sea and builds a stub at the shape's own floor, which nothing declines.
    {"index": 0, "x": -42, "z": 48}, {"index": 21, "x": -42, "z": 62},
    {"index": 9, "x": 47, "z": 38}, {"index": 10, "x": 47, "z": 52},
]

# the bastions: outer corner battered, and a notch cut into each breach cheek, so the breach reads
# as something knocked through rather than as the gap left between two boxes
west_edits = [{"index": 0, "x": -18, "z": 17},
              {"after": 1, "x": -5, "z": 18}, {"after": 2, "x": -8, "z": 18},
              {"after": 3, "x": -8, "z": 22}, {"after": 4, "x": -5, "z": 22}]
east_edits = [{"index": 1, "x": 22, "z": 17},
              {"after": 3, "x": 10, "z": 22}, {"after": 4, "x": 13, "z": 22},
              {"after": 5, "x": 13, "z": 18}, {"after": 6, "x": 10, "z": 18}]

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
            "anchor_heights": [high, high, low, low]}

CAUSEY = cell_(39, 4, [SMOOTH_SS, SANDSTONE], rise=2)

add_shapes = [
    # the portway itself, drawn as a POLYLINE: the rasterizer splines its four points before
    # offsetting the band, so it comes out as a road that flows rather than as a chain of chords.
    # One course proud of the heath, out of the gate's arch and down to the lip of the breach.
    {"id": "causey", "type": "polyline", "operation": "add", "override": True, "keepClear": True,
     "group": "team", "vertices": [[2, 46], [1, 38], [3, 31], [2, 26]],
     "radius": 2.0, "stroke_edge": "solid", "stroke_seed": 4,
     "floor": 0, "base_height": 1, "skirt": 0, "height_mode": "raise", "material": CAUSEY},
    # one flight onto each bastion, ten blocks of run for four courses, cut into the apron behind
    # it rather than leaning on the bastion's face
    flight("stair-west", [(-18, 25), (-12, 25), (-12, 35), (-18, 35)], HEATH, DECK),
    flight("stair-east", [(14, 25), (20, 25), (20, 35), (14, 35)], HEATH, DECK),
]

# ── the relief: the heath, and not the made ground on it ─────────────────────────────────────────
def lobe(cx, cz, radii, turn=0.0):
    import math
    n = len(radii)
    return [[round(cx + r * math.cos(turn + 2 * 3.141592653589793 * i / n), 1),
             round(cz + r * math.sin(turn + 2 * 3.141592653589793 * i / n), 1)]
            for i, r in enumerate(radii)]

relief = {"team": {
    "base": HEATH, "step": 1, "reach": 16, "landform": "plain",
    "grain": {"amplitude": 2, "scale": 17, "seed": 11},
    "marks": [
        # the ground the gatehouse stands on is flat, and stated so, and no wider than the
        # gatehouse. A made thing states an absolute floor; ground solved under one either buries
        # it or leaves it standing on air, and nothing downstream reports either. Everything
        # outside this ring is the solver's -- a mark on every region is a table with bumps on it.
        {"id": "gate-flat", "kind": "area", "h": HEATH,
         "ring": [[-23, 31], [-10, 30], [6, 31], [21, 31], [26, 37], [25, 46],
                  [12, 48], [-2, 47], [-15, 48], [-23, 42]]},
        # the hub's back, either side of the lane out of the spawn
        {"id": "dell", "kind": "point", "at": [-13, 57], "r": 6, "h": HEATH - 2, "tread": 4},
        {"id": "knap", "kind": "point", "at": [18, 62], "r": 5, "h": HEATH + 2, "tread": 3},
        # each ward gets a brae at its far corner and a dip at its neck, and neither stands on the
        # wool room's own pad -- the pad is pinned flat by the compiler and a mark over it fights
        # the plinth the room lays.
        {"id": "brae-west", "kind": "point", "at": [-43, 47], "r": 4, "h": HEATH + 3, "tread": 3},
        {"id": "sike-west", "kind": "point", "at": [-24, 63], "r": 4, "h": HEATH - 2, "tread": 3},
        {"id": "brae-east", "kind": "point", "at": [47, 37], "r": 4, "h": HEATH + 3, "tread": 3},
        {"id": "sike-east", "kind": "point", "at": [28, 56], "r": 4, "h": HEATH - 2, "tread": 3},
    ],
    "pushes": [
        # the rigg behind the hub, west of the lane out of the spawn. Ring 7 plus falloff 6 reaches
        # thirteen blocks, and the gate's flat ends at z 48, so the skirt never lifts the ground the
        # gatehouse was floored to. Its gradients agree -- 3 over 6 up the skirt against 3 over 6
        # to the crest (RL6).
        {"id": "rigg", "ring": lobe(-8, 63, [7, 6, 7, 5, 7, 6, 7, 5]),
         "amount": 3, "falloff": 6, "crown": 3, "roughness": 1.2, "seed": 7},
    ],
}}

# ── the structures: layers, not block soup ───────────────────────────────────────────────────────
def made(layers, part, material, mirrors=True):
    out = []
    for layer in (layers if isinstance(layers, list) else [layers]):
        inner = layer.pop("layout")
        layer["shapes"], layer["groups"] = inner["shapes"], inner["groups"]
        # A structure standing inside one team's ground is that team's, so it fans with the board:
        # the rasterizer copies a group's shapes onto every orbit axis only where the group says it
        # mirrors, and a landmark seated on the symmetry centre is what turns that off.
        for group in layer["groups"]:
            group["mirrors"] = mirrors
        layer["kind"], layer["part_of"] = "made", part
        for shape in layer["shapes"]:
            shape.pop("theme", None)
            shape["material"] = material
        out.append(layer)
    return out

structures = []
# The gatehouse: two drum towers, an arch between them and a crenellated curtain each side, closing
# the hub's whole front but for a two-block slip at either end -- a wall with one gate is a gate,
# a wall with no way round it is a board that cannot be walked.
structures += made(props.gatehouse("gate", 2.5, 42, 20, HEATH_Y, None, wing=5, wall_height=9,
                                   tower_radius=5, tower_height=15, mirrors=True),
                   "portway", MADE_PALE)
# the battlement along each bastion's lip, and a return down each cheek of the breach
for pid, x0, z0, x1, z1 in (("bat-west", -20, 15, -5, 17), ("bat-east", 10, 15, 25, 17),
                            ("cheek-west", -7, 17, -5, 25), ("cheek-east", 10, 17, 12, 25)):
    structures += made(props.crenellated_wall(pid, x0, z0, x1, z1, 1, DECK_Y, 3, None,
                                              merlon=3, crenel=2, parapet=2, name=f"Battlement {pid}"),
                       "portway", MADE_PALE)
# a drum tower at each bastion's outer corner, where the rampart turns
structures += made(props.drum_tower("tower-west", -16, 21, 3, 1, DECK_Y, 10, None, merlons=7,
                                    parapet=3, name="West bastion tower"), "portway", MADE_PALE)
structures += made(props.drum_tower("tower-east", 21, 21, 3, 1, DECK_Y, 10, None, merlons=7,
                                    parapet=3, name="East bastion tower"), "portway", MADE_PALE)
# and the beacon on the pier, which is the only made thing on the board that belongs to nobody
structures += made(props.drum_tower("beacon", 2, 0, 4, 1, PIER_Y, 12, None, merlons=8, parapet=3,
                                    inner_floor=None, mirrors=False, name="The beacon"),
                   "portway", MADE_GREY, mirrors=False)

# ── dressing ─────────────────────────────────────────────────────────────────────────────────────
ROAD_PAVE = cell_(38, 4, [GRAVEL, COARSE, HARDCLAY])
props_list = [
    # the way out of the spawn, through the gate's arch, to the lip of the breach
    {"id": "way", "kind": "stroke", "seed": 71, "radius": 2.5, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": ROAD_PAVE,
     "points": [[2, 82], [2, 72], [2, 62], [2, 50]]},
    {"id": "sward", "kind": "flora", "seed": 9,
     "points": [[-20, 25], [25, 25], [25, 70], [-20, 70]],
     "spec": {"coverage": 0.14, "scale": 16, "octaves": 3, "fernShare": 0.05,
              "flowerShare": 0.02, "flowerScale": 20, "tallShare": 0.02}},
]
# three rocks, each on ground `loop.py --candidates` answered for rather than on a guess
for i, (bx, bz, form, size) in enumerate([(13, 55, "round", 2), (20, 52, "angular", 3)]):
    props_list.append({"id": f"crag-{i}", "kind": "boulder", "x": bx, "z": bz, "form": form,
                       "size": size, "mossy": False, "rock": ANDESITE if i % 2 else STONE,
                       "seed": 90 + i})
for i, (tx, tz, sp, h) in enumerate([(-11, 60, "oak", 7), (-14, 58, "oak", 6), (14, 62, "oak", 8)]):
    props_list.append({"id": f"scrub-{i}", "kind": "tree", "x": tx, "z": tz, "form": "Template",
                       "species": sp, "height": h, "seed": 95 + i})

# the one building on the board, in the lee of the gatehouse where `sketch/seats` answered for a
# 9x6 footprint. Timber over a red heath under pale sandstone: three families, and the building is
# made of none of the ground's.
props_list.append({"id": "bastle", "kind": "house", "seed": 51, "front": "negZ",
                   "style": "@talltimber-cottage", "wings": [{"corners": [[-13, 48], [-5, 53]]}]})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-16",
    "voidEnforcement": True,
    "mapTheme": "heath",
    "themes": themes,
    "biome": {"kind": "solid", "id": 37},
    "themeById": {HEATH_SHAPE: "heath", WEST_BASTION: "works", EAST_BASTION: "works",
                  PIER_SHAPE: "pier"},
    # the bastions and the pier are out of the relief solve, so each meets the heath at a face and
    # the pier stands on vertical sides. `exclude` is the only scope that does that.
    "shapePropsById": {WEST_BASTION: {"relief_scope": "exclude"},
                       EAST_BASTION: {"relief_scope": "exclude"},
                       PIER_SHAPE: {"relief_scope": "exclude"}},
    "editShapes": {HEATH_SHAPE: heath_edits, WEST_BASTION: west_edits, EAST_BASTION: east_edits},
    # the pier's own outline roughened: it is the one ring on the board whose every edge is over
    # water, so a bend can only make it read more like a stump and less like a rectangle
    "bendShapes": {PIER_SHAPE: {"k": 0.2, "wander": 2, "step": 5, "seed": 3, "side": "in"}},
    "addShapes": add_shapes,
    "addLayers": structures,
    "relief": relief,
    "roomStyles": {"spawn": "@rk-spawn", "wool": "@desert-house"},
    "dressing": {"props": props_list},
}

with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as out:
    json.dump(finish, out, indent=1)
print("wrote the finish:", len(structures), "made layers,", len(add_shapes), "shapes,",
      len(props_list), "props")
