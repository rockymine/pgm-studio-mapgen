#!/usr/bin/env python3
"""Sallyport -- a composed bar hub taken over as a rampart with a postern and a detached outwork.

Composed from `GET /api/compose?players=30&symmetry=rot_180&seed=66` -- hub `bar` (one 10x6 piece),
frontline `single` (two steps), wools `i`/`l`, score 1.392, 138 land cells, 110 x 170 blocks.
Rebuilt round one idea:

    a team that has to bridge to its own wool defends a different board from one that can walk
    to it, and the rampart in front is what it walks out through.

What the composer gave and what was done with it:

  * the hub bar was cut in two across its width. Its front ten cells are a terrace three courses
    over the moor, and the rampart -- a crenellated curtain with two drum towers -- stands on the
    terrace's lip. Between the towers the curtain stops: that gap is the sally port, and the
    flight that fills it is the only walk between the terrace and the ground in front of it.
  * the near wool was taken off the team's landmass entirely. It stands on an outwork over a
    twenty-block strait, and the only way on is `team-bridge`, a build zone whose every interfacing
    component touches one team's islands and nobody else's -- `CT4`'s team transient-link, which
    the composer models on no board it makes (it emits exactly one zone, the mid band).
  * the deep wool keeps the composer's place and its approach carries the plan's bedrock wall.
  * the lopsided wool is NOT closed on this board, and the reason is geometric rather than lazy:
    the spawn hangs off one corner of the team's half, and the locus of points equidistant from
    both spawns is the perpendicular bisector of the line between them, which for a corner spawn
    runs outside the half. What is done instead is to make the near wool cost a bridge.

Run: python3 specs/opus5-sallyport/build-spec.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "tools", "sculpt")))
import props

SLUG = "opus5-sallyport"
CELL = 5
MOOR, CRAG, TERRACE = 11, 13, 14
MOOR_Y, CRAG_Y, TERRACE_Y = MOOR, CRAG, TERRACE

pieces = []
def P(pid, role, x, z, w, h, surface, **kw):
    pieces.append(dict(id=pid, role=role, rect=[x, z, w, h], surface=surface, **kw))

# the hub, cut across into a moor body and a raised front terrace
P("hub-back", "piece", -3, 9, 10, 4, MOOR)          # x -15..35 z 45..65
P("hub-front", "piece", -3, 7, 10, 2, TERRACE)      # x -15..35 z 35..45
# the composed frontline, unchanged
P("frontline-t1", "piece", -3, 4, 10, 3, MOOR)      # x -15..35 z 20..35
P("frontline-t2", "piece", -3, 2, 7, 2, MOOR)       # x -15..20 z 10..20
# the spawn, moved five blocks back so it hangs off the moor rather than across the terrace's seam
P("spawn-t1", "piece", 7, 9, 2, 3, MOOR)            # x  35..45 z 45..60
P("spawn-room", "spawn", 9, 9, 2, 3, MOOR)          # x  45..55 z 45..60

# the deep wool: the composer's `l`, with a garth built round the room and one seam to the hub
P("wool-a-t1", "piece", -2, 13, 2, 2, MOOR)         # x -10..0   z 65..75   the one seam -- WALLED
P("wool-a-t2", "piece", -3, 15, 3, 2, MOOR)         # x -15..0   z 75..85
P("wool-a-room", "wool-room", -5, 15, 2, 2, MOOR)   # x -25..-15 z 75..85
P("wool-a-w", "piece", -6, 15, 1, 2, MOOR)          # x -30..-25 z 75..85
P("wool-a-n", "piece", -6, 17, 4, 1, MOOR)          # x -30..-10 z 85..90
P("wool-a-s", "piece", -6, 14, 4, 1, MOOR)          # x -30..-10 z 70..75

# the outwork: the near wool, off the team's landmass, over a twenty-block strait
P("outwork", "piece", -9, 9, 2, 2, CRAG)            # x -45..-35 z 45..55
P("wool-b-room", "wool-room", -11, 9, 2, 2, CRAG)   # x -55..-45 z 45..55
P("outwork-n", "piece", -11, 11, 4, 1, CRAG)        # x -55..-35 z 55..60
P("outwork-s", "piece", -11, 8, 4, 1, CRAG)         # x -55..-35 z 40..45
P("outwork-w", "piece", -12, 9, 1, 2, CRAG)         # x -60..-55 z 45..55

plan = {
    "plan": 2,
    "meta": {"name": "Sallyport"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 30, "surface": MOOR,
                "observerY": 58},
    "pieces": pieces,
    "zones": [{"id": "mid-band", "rect": [-4, -2, 8, 4], "holes": []},
              # the intra-team build zone. Both of its interfacing components -- the hub's west
              # flank and the outwork's east face -- are this team's own islands, which is what
              # makes it a team transient-link (CT4) rather than a mid stone.
              {"id": "team-bridge", "rect": [-7, 9, 4, 2], "holes": []}],   # x -35..-15 z 45..55
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [7, 7], "facing": "left"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    "walls": [{"a": "wool-a-t1", "b": "hub-back"}],
    "boxes": [],
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as out:
    json.dump(plan, out, indent=1)
print("wrote the plan")

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE, PODZOL = solid(2), solid(3), solid(3, 1), solid(3, 2)
STONE, COBBLE, ANDESITE, MOSSY = solid(1), solid(4), solid(1, 5), solid(48)
GRAVEL, BRICK, STONEBRICK, CHIS_BRICK = solid(13), solid(45), solid(98), solid(98, 3)
SPRUCE, SPRUCE_LOG = solid(5, 1), solid(17, 1)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver", beyond=None):
    out = {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}
    if beyond is not None: out["beyond"] = beyond
    return out

ROCK_BODY = {"kind": "voronoi", "seed": 61, "cellSize": 11, "rise": 4, "bands": [
    {"depth": 1, "material": COBBLE}, {"depth": 2, "material": ANDESITE},
    {"depth": 1, "material": STONE}]}

PEAT = layered([(1, cell_(62, 9, [PODZOL, GRASS])), (2, DIRT), (2, COARSE)])
SCAR = layered([(1, cell_(63, 7, [COARSE, GRAVEL])), (2, DIRT), (2, STONE)])
GRIT = layered([(2, cell_(64, 6, [STONE, ANDESITE])), (4, STONE)], beyond=STONE)
MOOR_SURFACE = layered([(14, PEAT), (14, SCAR), (62, GRIT)], axis="slope", ending="repeat")

SETTS = cell_(65, 5, [COBBLE, ANDESITE], rise=3)
SCREE = cell_(66, 6, [STONE, GRAVEL], rise=3)
MADE = cell_(67, 4, [COBBLE, BRICK], rise=3)
STEPS = cell_(68, 4, [COBBLE, ANDESITE], rise=2)

themes = {
    "moor": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": GRAVEL},
        "surface": {"enabled": True, "depth": 5, "material": MOOR_SURFACE},
        "wall": layered([(1, COARSE), (2, GRAVEL), (5, STONE)], beyond=ANDESITE),
        "wallEnabled": True,
        "fill": ROCK_BODY,
    },
    # the terrace. Its face is what the rampart stands on and is the one surface on the board that
    # wants a wallDiagonal: the runs shear by height so they climb the batter, and one of them is a
    # teamTint -- each fort is its own island, so each wears its garrison's colour.
    "works": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": MOSSY},
        "surface": {"enabled": True, "depth": 2, "material": SETTS},
        "wallEnabled": True,
        "wall": {"kind": "wallDiagonal", "slope": 2, "runs": [
            {"material": BRICK, "width": 3},
            {"material": {"kind": "teamTint", "blockId": 159, "neutral": solid(159, 7)}, "width": 1},
            {"material": COBBLE, "width": 3},
            {"material": ANDESITE, "width": 2}]},
        "fill": ROCK_BODY,
    },
    # the outwork is bare rock: nobody made it and nobody lives on it
    "crag": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": STONE},
        "surface": {"enabled": True, "depth": 3, "material": SCREE},
        "wall": layered([(2, STONE), (3, ANDESITE), (4, COBBLE)], beyond=STONE),
        "wallEnabled": True,
        "fill": ROCK_BODY,
    },
}

# ── reshaping the compiled outlines ──────────────────────────────────────────────────────────────
MOOR_SHAPE, FRONT_SHAPE = "frontline-t1-11", "frontline-t1-11-2"
TERRACE_SHAPE, OUTWORK_SHAPE = "frontline-t1-14", "outwork-13"

moor_edits = [
    # a bay eaten into the hub's north edge between the spawn spur and the wool lane
    {"after": 8, "x": 24, "z": 61}, {"after": 9, "x": 13, "z": 63},
    # the wool garth's two west corners chamfered in
    {"index": 0, "x": -27, "z": 73}, {"index": 15, "x": -27, "z": 87},
]
front_edits = [
    # the frontline's own shore, where the crossing lands: three points pulled back off a ruled
    # line. Nothing on the z=35 edge moves -- that edge is flush against the terrace.
    {"after": 5, "x": -8, "z": 14}, {"after": 6, "x": 1, "z": 12}, {"after": 7, "x": 11, "z": 15},
    {"index": 0, "x": 18, "z": 13},
]
terrace_edits = [
    # the sally port's re-entrant on the front, cut to exactly the flight that fills it
    {"after": 0, "x": -5, "z": 35}, {"after": 1, "x": -5, "z": 39},
    {"after": 2, "x": 5, "z": 39}, {"after": 3, "x": 5, "z": 35},
    # and a second on the back, for the ramp the garrison comes UP by. The terrace's back seam is
    # a three-course drop as much as its front is: without this the only walk onto the rampart is
    # the attackers' own stair, which is the wrong way round.
    {"after": 6, "x": 34, "z": 45}, {"after": 7, "x": 34, "z": 41},
    {"after": 8, "x": 26, "z": 41}, {"after": 9, "x": 26, "z": 45},
]

def simulate(ring, ops):
    ring = [list(p) for p in ring]
    for op in ops:
        if "remove" in op: ring.pop(op["remove"])
        elif "index" in op: ring[op["index"]] = [op["x"], op["z"]]
        else: ring.insert(op["after"] + 1, [op["x"], op["z"]])
    return ring

MOOR_RING = [[-30, 70], [-10, 70], [-10, 65], [-15, 65], [-15, 45], [55, 45], [55, 60], [35, 60],
             [35, 65], [0, 65], [0, 85], [-10, 85], [-10, 90], [-30, 90]]
FRONT_RING = [[20, 10], [20, 20], [35, 20], [35, 35], [-15, 35], [-15, 10]]
TERRACE_RING = [[-15, 35], [35, 35], [35, 45], [-15, 45]]

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
def flight(fid, ring, low, high, material=None):
    return {"id": fid, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": material or STEPS,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}

DYKE = cell_(72, 4, [COBBLE, STONE], rise=2)

add_shapes = [
    # a drystone dyke across the moor, drawn as a POLYLINE: the rasterizer splines its points --
    # centripetal Catmull-Rom, eight samples a segment -- before offsetting the band, so four
    # clicked points come out as a wall that flows rather than as a chain of chords. Two courses
    # proud of whatever ground it crosses, which is a scramble rather than a barrier: it is a field
    # wall, and it breaks the sightline down the moor without closing it.
    {"id": "dyke", "type": "polyline", "operation": "add", "override": True, "keepClear": True,
     "group": "team", "vertices": [[6, 52], [16, 56], [26, 55], [34, 60]],
     "radius": 1.2, "stroke_edge": "rough", "stroke_seed": 7,
     "floor": 0, "base_height": 2, "skirt": 0, "height_mode": "raise", "material": DYKE},
    # the sally port itself: eight blocks of run for three courses, set into the terrace's own
    # re-entrant so the stair is IN the rampart rather than leaning on it
    flight("sally-stair", [(-5, 31), (5, 31), (5, 39), (-5, 39)], MOOR, TERRACE),
    # and the garrison's own ramp up the terrace's back, where the way out of the spawn meets it
    flight("terrace-ramp", [(26, 49), (34, 49), (34, 41), (26, 41)], MOOR, TERRACE),
]

def lobe(cx, cz, radii, turn=0.0):
    import math
    n = len(radii)
    return [[round(cx + r * math.cos(turn + 2 * math.pi * i / n), 1),
             round(cz + r * math.sin(turn + 2 * math.pi * i / n), 1)]
            for i, r in enumerate(radii)]

relief = {"team": {
    "base": MOOR, "step": 1, "reach": 18, "landform": "rolling",
    "grain": {"amplitude": 2, "scale": 16, "seed": 21},
    "marks": [
        # the barrow's own pad. A made thing states an absolute floor, so the ground under one is
        # stated rather than solved -- otherwise it floats or is buried and nothing reports either.
        {"id": "barrow-pad", "kind": "area", "h": MOOR,
         "ring": lobe(10, 56, [10, 8, 9, 8, 10, 8, 9, 8])},
        # the ground at the foot of the sally port, so the first tread is not met as a drop
        {"id": "sally-foot", "kind": "area", "h": MOOR,
         "ring": lobe(0, 28, [13, 10, 12, 8, 13, 10, 12, 8])},
        # the moor's own shape: a peat hollow behind the terrace, a howe on the east flank, a brae
        # out at the wool garth. Each carries a tread because each would otherwise meet the ground
        # beside it on a wall; the two pads above carry none, because they are meant to be flat to
        # their edge (RL5).
        {"id": "moss", "kind": "point", "at": [-6, 55], "r": 6, "h": MOOR - 2, "tread": 4},
        {"id": "howe", "kind": "point", "at": [30, 68], "r": 5, "h": MOOR + 3, "tread": 3},
        {"id": "brae", "kind": "point", "at": [-26, 80], "r": 5, "h": MOOR + 3, "tread": 3},
    ],
    "pushes": [
        # the rigg across the east half of the ground in front of the rampart, which is what stops
        # the approach being one flat sheet under fire from the wall. Ring 10 plus falloff 6 reaches
        # sixteen blocks from (20, 20); the sally port's foot is 22.8 away, so the stair's first
        # tread is met on the flat it was anchored to. Its gradients agree -- 3 over 6 against
        # 3 over 8 (RL6).
        {"id": "rigg", "ring": lobe(20, 20, [10, 8, 9, 7, 10, 8, 9, 7]),
         "amount": 3, "falloff": 6, "crown": 3, "roughness": 1.3, "seed": 5},
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
# the rampart: two runs of crenellated curtain along the terrace's lip, stopping either side of
# the sally port, so the gap between them is the gate and the flight is what fills it
for pid, x0, x1 in (("rampart-west", -15, -6), ("rampart-east", 6, 35)):
    structures += made(props.crenellated_wall(pid, x0, 35, x1, 37, 1, TERRACE_Y, 4, None,
                                              merlon=3, crenel=2, parapet=2, name=f"Rampart {pid}"),
                       "rampart", MADE)
# a drum tower each side of the gate, standing on the terrace behind the curtain
structures += made(props.drum_tower("gate-tower-w", -9, 41, 3, 1, TERRACE_Y, 12, None, merlons=7,
                                    parapet=3, name="West gate tower"), "rampart", MADE)
structures += made(props.drum_tower("gate-tower-e", 9, 41, 3, 1, TERRACE_Y, 12, None, merlons=7,
                                    parapet=3, name="East gate tower"), "rampart", MADE)
# the barrow on the moor behind it: a stepped mound, which is the one landmark on this board that
# is neither a wall nor a tower
structures += made(props.ziggurat("barrow", 10, 56, 6, MOOR_Y, 3, 2, 2, None, name="The barrow"),
                   "barrow", cell_(69, 5, [COARSE, STONE], rise=2))
# the outwork's curtain, in two runs with the bridge's landing left open between them
for pid, z0, z1 in (("outwork-wall-s", 40, 48), ("outwork-wall-n", 52, 60)):
    structures += made(props.crenellated_wall(pid, -36, z0, -34, z1, 1, CRAG_Y, 4, None,
                                              merlon=3, crenel=2, parapet=2, name=f"Outwork {pid}"),
                       "outwork", MADE)

# ── dressing ─────────────────────────────────────────────────────────────────────────────────────
ROAD_PAVE = cell_(70, 4, [GRAVEL, COARSE, COBBLE])
props_list = [
    # out of the spawn, west along the moor, and out through the sally port
    {"id": "way", "kind": "stroke", "seed": 71, "radius": 2.5, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": ROAD_PAVE,
     "points": [[46, 52], [38, 51], [30, 48], [30, 42], [16, 40], [2, 40], [0, 33]]},
    {"id": "sward", "kind": "flora", "seed": 9,
     "points": [[-15, 10], [35, 10], [55, 45], [55, 60], [0, 90], [-30, 90], [-30, 60]],
     "spec": {"coverage": 0.2, "scale": 15, "octaves": 3, "fernShare": 0.3,
              "flowerShare": 0.02, "flowerScale": 18, "tallShare": 0.03}},
]
# two clints, each on a cell `loop.py --candidates` answered for rather than on a guess
for i, (bx, bz, form, size) in enumerate([(22, 58, "round", 2), (-10, 58, "angular", 3)]):
    props_list.append({"id": f"clint-{i}", "kind": "boulder", "x": bx, "z": bz, "form": form,
                       "size": size, "mossy": i % 2 == 0, "rock": ANDESITE if i % 2 else STONE,
                       "seed": 90 + i})
for i, (tx, tz, sp, h) in enumerate([(-3, 58, "spruce", 8), (32, 60, "spruce", 11)]):
    props_list.append({"id": f"fir-{i}", "kind": "tree", "x": tx, "z": tz, "form": "Template",
                       "species": sp, "height": h, "seed": 95 + i})

# Two buildings, one style family, differing in proportion rather than in material -- which is
# what makes two buildings a row rather than a swatch. Both stand where `sketch/seats` answered
# forwards for a 9x6 footprint: the watch house on the terrace behind the rampart's east run, and
# a steading out in the approach, which is the only cover on the ground the assault crosses.
props_list.append({"id": "watch-house", "kind": "house", "seed": 41, "front": "negZ",
                   "style": "@talltimber-store", "wings": [{"corners": [[-15, 47], [-6, 52]]}]})
props_list.append({"id": "steading", "kind": "house", "seed": 42, "front": "posZ",
                   "style": "@talltimber-cottage", "wings": [{"corners": [[-14, 23], [-6, 28]]}]})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-16",
    "voidEnforcement": True,
    "mapTheme": "moor",
    "themes": themes,
    "biome": {"kind": "solid", "id": 32},
    "themeById": {MOOR_SHAPE: "moor", FRONT_SHAPE: "moor", TERRACE_SHAPE: "works",
                  OUTWORK_SHAPE: "crag"},
    # the terrace and the outwork are out of the solve, so each meets the moor at a face
    "shapePropsById": {TERRACE_SHAPE: {"relief_scope": "exclude"},
                       OUTWORK_SHAPE: {"relief_scope": "exclude"}},
    "editShapes": {MOOR_SHAPE: moor_edits, FRONT_SHAPE: front_edits,
                   TERRACE_SHAPE: terrace_edits},
    # the outwork is the one ring on the board whose every edge is over void, so a bend can only
    # make it read more like a crag and less like a rectangle
    "bendShapes": {OUTWORK_SHAPE: {"k": 0.22, "wander": 3, "step": 6, "seed": 5, "side": "in"}},
    "addShapes": add_shapes,
    "addLayers": structures,
    "relief": relief,
    "roomStyles": {"spawn": "@hb-spawn", "wool": "@ow-cage"},
    "dressing": {"props": props_list},
}

with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as out:
    json.dump(finish, out, indent=1)
print("wrote the finish:", len(structures), "made layers,", len(add_shapes), "shapes,",
      len(props_list), "props")
