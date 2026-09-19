#!/usr/bin/env python3
"""Whitegape — a limestone gorge quarried from both rims.

Writes opus5-whitegape.plan.json and opus5-whitegape.finish.json for tools/drive.py.

The board in one sentence: two teams face each other across a 23-block chasm; each holds the
workings on its own rim, and its monument stands on the floor of its own quarry pit, reached by a
haul ramp from the spawn side and a tramway incline from the gorge side.

Everything here is measured in blocks unless the name says cells. The authored unit is team A, on
negative z; rot_180 fans it (image of (x, z) is (-x-1, -z-1)).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from sculpt import props as P  # noqa: E402

SLUG = "opus5-whitegape"
CELL = 4

# ── the five numbers ──────────────────────────────────────────────────────────────────────────────
# lane 176 blocks spawn to spawn; goal 42 along it from its own spawn; board 64 wide, 200 long,
# with a 23-block void gap down the middle. Solved against GO1 (3-4), GO3 (>=85), GO4 (>=40).
GOAL_XZ = (-9, -50)           # the monument, 9 blocks west of the centre line
LAND_Z = (-100, -13)          # team A's ground, inclusive
LAND_X = (-28, 27)            # 56 wide: 4,928 blocks a team, 246 a player at 20 (G8's own law)
BASE = 24                     # globals.surface — the moor's own level
SHELF = 25                    # the spawn shelf: one step over the moor, which is what SP8 allows
PAD = 22                      # the graded apron the quarry is cut into
LIP = 21                      # the moor at the gorge lip — the board falls toward the chasm
DOCK_TOP = 17                 # the loading dock, cut 4 below the lip
PIT_DEPTH = 11                # so the pit floor is PAD - 11 = 11

# ── blocks ────────────────────────────────────────────────────────────────────────────────────────
def solid(b, d=0):
    return {"kind": "solid", "id": b, "data": d}

STONE, ANDESITE, DIORITE = solid(1), solid(1, 5), solid(1, 3)
GRASS, DIRT, COARSE = solid(2), solid(3), solid(3, 1)
COBBLE, GRAVEL = solid(4), solid(13)
SPRUCE, SPRUCE_LOG = solid(5, 1), solid(17, 1)
BRICK, STONEBRICK = solid(45), solid(98)


def cell(palette, size, seed, jitter=25, warp=4, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter,
            "warp": warp, "palette": palette, "rise": rise}


def layered(bands, axis="depth", ending="handOver", beyond=None):
    m = {"kind": "layered", "axis": axis,
         "stack": {"ending": ending,
                   "bands": [{"material": mat, "thickness": t} for mat, t in bands]}}
    if beyond is not None:
        m["beyond"] = beyond
    return m


# The board's rock, stated once. Every cut on the map — the gorge walls, the quarry faces, the cut
# banks behind the dock — is the same beds in the same order, which is what makes them read as one
# limestone rather than as three separate decisions.
BEDS = layered([(STONE, 2), (DIORITE, 1), (STONE, 3), (ANDESITE, 1),
                (STONE, 4), (DIORITE, 2)], ending="repeat")
# The body nobody sees until a wall is cut: cells wider than tall, so a cut face reads as blobs
# rather than as vertical runs.
BODY = cell([STONE, ANDESITE, DIORITE], 9, 41, jitter=25, warp=4, rise=5)
# Three blocks a reader cannot quite tell apart, for ground somebody walks on and works.
# A rise, because this is also the whole material of the ramps and the flights, and PT4 refuses a
# fill sampled in the plane alone — it would stripe every cut face floor to sky.
HARDCORE = cell([GRAVEL, ANDESITE, COBBLE], 7, 47, jitter=30, warp=3, rise=4)

# ── themes ────────────────────────────────────────────────────────────────────────────────────────
# One ground, and two places that are genuinely made of something else.
FELL = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    # No rim: the gorge lip and the crag shoulders are ground a relief solved, and a rim caps every
    # fall with a band and turns a hillside into contour lines.
    "rim": {"enabled": False, "depth": 1, "material": COBBLE},
    # The ground is finished by its ANGLE. A limestone fell is meadow where it lies flat, worn
    # ground where it leans, and bare rock where it stands up.
    "surface": {"enabled": True, "depth": 3, "material": layered([
        (layered([(GRASS, 1), (COARSE, 1), (DIRT, 1)], beyond=STONE), 16),
        (layered([(cell([COARSE, GRAVEL], 9, 43), 1), (DIRT, 2)], beyond=STONE), 18),
        (layered([(cell([STONE, ANDESITE], 11, 45, rise=4), 2), (STONE, 1)], beyond=STONE), 56),
    ], axis="slope", ending="repeat", beyond=STONE)},
    "wall": BEDS,
    "wallEnabled": True,
    "fill": BODY,
}

# The pit: quarry spoil and swept rock, sharing the fell's beds on every face it cuts.
WORKS = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": COBBLE},
    "surface": {"enabled": True, "depth": 2, "material": layered([
        (HARDCORE, 1), (cell([STONE, GRAVEL], 9, 49, rise=3), 1)], beyond=STONE)},
    "wall": BEDS,
    "wallEnabled": True,
    "fill": BODY,
}

# The loading dock: made ground, so its face is coursed rather than bedded.
DOCK = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": True, "depth": 1, "material": STONEBRICK},
    "surface": {"enabled": True, "depth": 2, "material": layered([
        (cell([STONEBRICK, STONE, COBBLE], 9, 51, jitter=20, warp=3, rise=4), 1),
        (STONE, 1)], beyond=STONE)},
    "wall": {"kind": "wallRun", "runs": [
        {"material": STONEBRICK, "width": 5},
        {"material": STONE, "width": 3},
        {"material": COBBLE, "width": 2}]},
    "wallEnabled": True,
    "fill": cell([STONE, COBBLE], 9, 53, rise=5),
}

# The kiln. Brick, because a lime kiln is brick-lined and because nothing else on the board is —
# it is the one thing visible from the far rim and it may not be the ground it stands on.
KILN = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "wallOnTerrainFaces": True,
    "rim": {"enabled": False, "depth": 1, "material": BRICK},
    "surface": {"enabled": True, "depth": 2, "material": cell([BRICK, solid(172), BRICK], 6, 57,
                                                              jitter=20, warp=2, rise=4)},
    "wall": cell([BRICK, solid(172), BRICK], 6, 57, jitter=20, warp=2, rise=4),
    "wallEnabled": True,
    "fill": cell([BRICK, solid(172)], 6, 57, jitter=20, warp=2, rise=4),
}

THEMES = {"fell": FELL, "works": WORKS, "dock": DOCK, "kiln": KILN}

# ── the plan ──────────────────────────────────────────────────────────────────────────────────────
# Two pieces. The plan states the arrangement — the ground and the room the spawn stands in — and
# every landform below is relief or an authored shape.
# PL4 refuses two pieces that overlap at different surfaces, so the fell is tiled AROUND the
# spawn rather than drawn under it.
SPAWN_PIECE = [-5, -25, 4, 4]        # cells: blocks x -20..-5, z -100..-85
BUILD_ZONE = [-7, -6, 14, 12]        # cells: blocks x -28..27, z -24..23 — over the whole chasm

plan = {
    "plan": 2,
    "meta": {"name": "Whitegape"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 20,
                "surface": BASE, "observerY": 52},
    "pieces": [
        {"id": "fell", "role": "piece", "rect": [-7, -21, 14, 18], "surface": BASE},
        {"id": "fell-w", "role": "piece", "rect": [-7, -25, 2, 4], "surface": BASE},
        {"id": "fell-e", "role": "piece", "rect": [-1, -25, 8, 4], "surface": BASE},
        {"id": "head", "role": "spawn", "rect": SPAWN_PIECE, "surface": SHELF},
    ],
    "zones": [{"id": "chasm", "rect": BUILD_ZONE, "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "head", "at": [8, 8], "facing": "back",
                    "footprint": [3, 3, 10, 10]}],
        "wools": [], "iron": [], "cores": [],
        "destroyables": [{"id": "destroyable-1", "piece": "", "at": list(GOAL_XZ),
                          "style": "pillar-3", "materials": "obsidian", "float": 4,
                          "name": "The Whitegape Pillar"}],
    },
    "walls": [], "boxes": [],
}

# ── relief ────────────────────────────────────────────────────────────────────────────────────────
# Four marks and one push. Everything pinned is ground a player stands on and needs to be at a
# stated height: the spawn shelf, the graded apron the quarry is cut into, the moor along the lip,
# and the cart road between shelf and apron. The flanks carry no mark, so the solver makes them.
MARKS = [
    {"id": "shelf", "kind": "area", "h": SHELF, "bevel": 3, "ring": [
        [-27, -100], [-27, -88], [-22, -80], [-12, -78], [-2, -83], [-1, -96], [-3, -100]]},
    {"id": "pad", "kind": "area", "h": PAD, "bevel": 4, "ring": [
        [-27, -56], [-26, -72], [-14, -75], [-2, -72], [8, -64], [11, -50],
        [8, -36], [-2, -31], [-14, -33], [-24, -38], [-27, -46]]},
    {"id": "lipmoor", "kind": "area", "h": LIP, "bevel": 3, "ring": [
        [-28, -30], [-18, -32], [-5, -29], [7, -32], [19, -29], [27, -26],
        [27, -13], [14, -13], [0, -16], [-14, -13], [-28, -13], [-28, -22]]},
    {"id": "cartway", "kind": "line", "r": 6, "tread": 3,
     "points": [[-14, -82], [-20, -74], [-23, -66]], "h": [SHELF, 23, PAD]},
]

PUSHES = [
    # The knott: the east fell, the one landform the board has that nobody made. Its two gradients
    # agree — amount/falloff 5/14 outside (20°) against crown/half 4/8 inside (27°) — so it is a
    # hillside a player walks up and not a wall with a hill on top of it.
    {"id": "knott", "seed": 11, "roughness": 3, "falloff": 14, "crown": 4,
     "amounts": [3, 4, 5, 5, 4, 3, 4], "ring": [
         [17, -88], [25, -85], [27, -74], [26, -56], [21, -46], [16, -56], [15, -72]]},
]

RELIEF = {"*": {"base": BASE, "reach": 0, "step": 1,
                "grain": {"amplitude": 1.2, "scale": 16, "seed": 7},
                "marks": MARKS, "pushes": PUSHES}}

# ── the made ground ───────────────────────────────────────────────────────────────────────────────
ADD = []


def made(shape):
    ADD.append(shape)
    return shape


# The pit. A sink cuts sheer and leaves a flat floor; nested area marks would have built a funnel.
made({"id": "pit", "type": "polygon", "operation": "add", "theme": "works",
      "height_mode": "sink", "skirt": 1, "floor": 0, "base_height": PIT_DEPTH,
      "anchor_heights": [PIT_DEPTH] * 8,
      "vertices": [[-21, -56], [-19, -62], [-7, -63], [2, -58],
                   [3, -50], [-2, -44], [-12, -43], [-20, -48]]})

# The loading dock, cut 4 courses into the lip so whatever lands on it is below the defence. Its
# back edge is not a straight line: two bays are let into the moor, each sized to the flight in it.
made({"id": "dock", "type": "polygon", "operation": "add", "theme": "dock", "keepClear": True,
      "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
      "floor": 0, "base_height": DOCK_TOP + 1,
      "vertices": [[-14, -25], [-10, -25], [-10, -30], [-4, -30], [-4, -25],
                   [5, -25], [5, -31], [11, -31], [11, -25], [13, -25],
                   [13, -13], [-14, -13]]})


def flight(fid, verts, tops, material):
    """A flight is one polygon with a height per vertex. The run is at least twice the rise, which
    is what separates a stair from a wall."""
    return made({"id": fid, "type": "polygon", "operation": "add", "keepClear": True,
                 "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
                 "floor": 0, "base_height": max(tops), "material": material,
                 "vertices": verts, "anchor_heights": [t + 1 for t in tops]})


# Two flights out of the dock, one in each bay: 5 courses over 10 blocks of run.
flight("flight-w", [[-10, -40], [-4, -40], [-4, -30], [-10, -30]],
       [PAD, PAD, DOCK_TOP, DOCK_TOP], HARDCORE)
flight("flight-e", [[5, -41], [11, -41], [11, -31], [5, -31]],
       [PAD, PAD, DOCK_TOP, DOCK_TOP], HARDCORE)

# The haul ramp: out of the pit on the spawn side, 11 courses over 24 blocks of run.
flight("haul-ramp", [[-26, -70], [-20, -73], [-8, -52], [-14, -49]],
       [PAD, PAD, PAD - PIT_DEPTH, PAD - PIT_DEPTH], HARDCORE)
# The tramway incline: out of the pit on the gorge side, 10 courses over 28.
flight("tram-ramp", [[14, -27], [20, -24], [2, -49], [-4, -46]],
       [LIP, LIP, PAD - PIT_DEPTH, PAD - PIT_DEPTH], HARDCORE)

DRYSTONE = cell([COBBLE, STONE, ANDESITE], 3, 61, jitter=30, warp=2, rise=2)

# The quarry's boundary wall, above the pit's back face — what stops a man or a sheep walking into
# the hole, and what a defender at the head of the haul ramp stands behind.
made({"id": "pit-wall", "type": "polyline", "operation": "add", "keepClear": True,
      "stroke_edge": "solid", "radius": 1.5, "material": DRYSTONE,
      "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
      "floor": 0, "base_height": PAD + 3,
      "vertices": [[-13, -69], [-7, -67], [-1, -66], [2, -64]]})

# The dock's parapet, three blocks in from the void so there is a walkway outside it. Split, so the
# middle of the dock is open to the chasm — which is where a bridge wants to leave from.
for pid, pts in (("kerb-w", [[-13, -17], [-8, -18], [-4, -17]]),
                 ("kerb-e", [[3, -17], [8, -18], [12, -17]])):
    made({"id": pid, "type": "polyline", "operation": "add", "keepClear": True,
          "stroke_edge": "solid", "radius": 1.2, "material": STONEBRICK,
          "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
          "floor": 0, "base_height": DOCK_TOP + 3,
          "vertices": pts})

# ── the kiln ──────────────────────────────────────────────────────────────────────────────────────
# A tapered tower on the dock: the one thing on the board read from the far rim, and the reason the
# dock exists at all. mirrors=True, so each team gets its own.
kiln_layer = P.tapered_tower("kiln", -9, -20, 4.6, 3.2, 1, 0, 11, "kiln",
                             mirrors=True, name="The kiln")
LAYERS = [{"id": kiln_layer["id"], "name": kiln_layer["name"], "base_y": DOCK_TOP + 1,
           "kind": "made", "part_of": "kiln",
           "shapes": kiln_layer["layout"]["shapes"],
           "groups": kiln_layer["layout"]["groups"]}]

# ── buildings ─────────────────────────────────────────────────────────────────────────────────────
SHELL = json.load(open(os.path.join(ROOT, "tools", "styles", "showcase-hall.json")))


def stack(bands, extent):
    return {"stack": {"ending": "repeat",
                      "bands": [{"material": m, "thickness": t} for m, t in bands]}, "extent": extent}


# One built family: spruce over a brick plinth, spruce posts, spruce roof. Neither is the pale
# limestone under its feet, and the brick is the accent the kiln already wears.
SHELL["foundation"]["plate"] = stack([(BRICK, 1)], 1)
SHELL["foundation"]["footing"] = None
SHELL["post"] = SPRUCE_LOG
SHELL["wall"] = stack([(BRICK, 1), (SPRUCE, 4)], 5)
SHELL["roof"].update({"form": "gable", "pitch": 1, "slab": 126, "slabData": 1, "overhang": 1,
                      "ridgeCap": True, "body": SPRUCE, "verge": {"kind": "laidLog", "id": 17, "data": 1},
                      "gable": SPRUCE})
SHELL["beams"] = {"block": 17, "data": 1, "reach": 1, "any": False}
# A storey carries clear + 1 courses of wall, so each stack is sized to its own storey or the rest
# is truncated in silence.
SHELL["storeys"][0].update({
    "clear": 5, "post": SPRUCE_LOG,
    "wall": stack([(BRICK, 2), (SPRUCE, 3), ({"kind": "laidLog", "id": 17, "data": 1}, 1)], 5)})
SHELL["storeys"][1].update({
    "clear": 4, "post": SPRUCE_LOG,
    "wall": stack([(SPRUCE, 4), ({"kind": "laidLog", "id": 17, "data": 1}, 1)], 4)})

WORKS_SHELL = json.loads(json.dumps(SHELL))
WORKS_SHELL["storeys"] = [json.loads(json.dumps(SHELL["storeys"][0]))]

# ── dressing ──────────────────────────────────────────────────────────────────────────────────────
BODIES = json.load(open(os.path.join(ROOT, "specs", "fable-millrace-revamp", "trees.json")))
SCRUB = ["fir-small-1", "fir-small-2", "fir-small-3", "fir-small-4", "fir-small-5"]
SHELTER = ["oak-dense-1", "oak-dense-4"]

styles = {k: {"kind": "tree", "form": "copied", "body": BODIES[k]["body"]}
          for k in SCRUB + SHELTER}
styles["limestone"] = {"kind": "boulder", "form": "angular", "size": 6, "mossy": False,
                       "rock": {"kind": "noise", "seed": 71, "scale": 3, "octaves": 3, "rise": 2,
                                "stops": [STONE, COBBLE, ANDESITE, STONE]}}
styles["clint"] = {"kind": "boulder", "form": "outcrop", "size": 7, "mossy": False,
                   "rock": {"kind": "noise", "seed": 73, "scale": 3, "octaves": 3, "rise": 2,
                            "stops": [STONE, ANDESITE, COBBLE]}}
styles["works-shed"] = {"kind": "house", "shell": WORKS_SHELL}

props = []


def tree(pid, x, z, style):
    props.append({"id": pid, "kind": "tree", "seed": abs(x * 31 + z * 17) % 9973,
                  "x": x, "z": z, "style": style})


def boulder(pid, x, z, style):
    props.append({"id": pid, "kind": "boulder", "seed": abs(x * 11 + z * 5) % 9973,
                  "x": x, "z": z, "style": style})


def road(pid, pts, radius, seed):
    props.append({"id": pid, "kind": "stroke", "claimsGround": True, "radius": radius,
                  "seed": seed, "style": "solid", "points": pts, "pave": HARDCORE})


def house(pid, corners, seed, front):
    props.append({"id": pid, "kind": "house", "seed": seed, "front": front,
                  "wings": [{"corners": corners}], "style": "works-shed"})


# Three ways, each of them somewhere a load or a man actually went.
road("haul-road", [[-22, -71], [-17, -80], [-14, -88]], 3, 81)         # ramp head to the spawn
road("tramway", [[18, -24], [15, -28], [12, -33]], 2, 83)              # incline head to the east bay
road("lip-path", [[-16, -76], [-24, -58], [-26, -46], [-23, -38]], 2, 85)   # west flank, to the door

# The winding house, at the head of the haul ramp: the drum that hauled wagons out of the pit.
house("winding-house", [[-27, -82], [-20, -75]], 601, "posZ")
# The powder house: a magazine stands apart from the works, which is why it is out on the west
# flank on its own with a track running to its door and nothing else near it.
house("powder-house", [[-27, -36], [-20, -29]], 607, "negZ")

# Boulders where a limestone fell has them: broken off the knott's shoulder, and one pair on the
# bare pavement west of the cart road.
for i, (x, z, st) in enumerate([(4, -84, "clint"), (6, -70, "limestone"), (24, -88, "limestone"),
                                (21, -58, "clint")]):
    boulder(f"erratic-{i}", x, z, st)

# Scrub in the lee of the knott and a shelter belt behind the spawn hall. Nothing in the pit and
# nothing on the dock: a working floor is bare, and OB19 keeps 10 blocks round the goal clear.
for i, (x, z, st) in enumerate([
        (18, -34, SCRUB[0]), (22, -46, SCRUB[1]), (17, -44, SCRUB[2]), (24, -32, SCRUB[3]),
        (12, -52, SCRUB[4]), (2, -32, SCRUB[0]), (6, -58, SCRUB[1]),
        (-27, -66, SCRUB[2]), (-22, -24, SCRUB[3]), (-25, -16, SCRUB[4]),
        (16, -20, SCRUB[0]), (26, -68, SCRUB[1]), (12, -98, SHELTER[0]),
        (16, -92, SCRUB[2]), (20, -96, SCRUB[3]), (24, -76, SCRUB[4])]):
    tree(f"thorn-{i}", x, z, st)

# Ground cover over the whole half, not a patch of it — the density field is better at patchiness
# than a hand-drawn polygon. Both gameplay numbers stay low: tall grass is cover nobody authored.
props.append({"id": "fell-cover", "kind": "flora",
              "points": [[-28, -100], [27, -100], [27, -14], [-28, -14]],
              "spec": {"coverage": 0.28, "scale": 18, "octaves": 3, "fernShare": 0.25,
                       "flowerShare": 0.04, "flowerScale": 11, "tallShare": 0.12}})

# ── the finish ────────────────────────────────────────────────────────────────────────────────────
finish = {
    "created": "2026-09-18",
    "authors": ["Opus 5"],
    "themes": THEMES,
    "mapTheme": "fell",
    # Extreme hills tints grass #8ab689 — the pale grey-green a limestone fell has, against the
    # #91bd59 Plains would paint on the same blocks.
    "biome": {"kind": "solid", "id": 3},
    "relief": RELIEF,
    "addShapes": ADD,
    "addLayers": LAYERS,
    "roomStyles": {"spawn": SHELL},
    "dressing": {"styles": styles, "props": props},
}

for name, doc in ((f"{SLUG}.plan.json", plan), (f"{SLUG}.finish.json", finish)):
    with open(os.path.join(HERE, name), "w") as fh:
        json.dump(doc, fh, indent=1)
    print(f"wrote {name}  ({os.path.getsize(os.path.join(HERE, name)):,} bytes)")
