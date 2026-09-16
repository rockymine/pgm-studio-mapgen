#!/usr/bin/env python3
"""Revetment -- a composed double-hole hub taken over as a hillfort.

Composed from `GET /api/compose?players=30&symmetry=rot_180&seed=2` -- hub `double-hole`, frontline
`bar`, wools `i`/`i`, card score 0.278, 118 land cells. Rebuilt round one idea:

    the fort is made ground and the field in front of it is grown ground, and the six-course
    revetment between them is the board.

What the composer gave and what was done with it:

  * every piece got a `surface`, so the flat plan stops compiling to one merged polygon and a
    subtract. Two tiers only: the meadow at 11 and the fort platform at 17.
  * the two holes the `double-hole` hub rings are kept as holes -- they are wells in the fort's
    floor, railed round rather than filled.
  * the hub was trimmed on its east side (t5, t6, t7 each lose a cell) so the fort is symmetric
    about x=0, and the spawn was moved off the composed west flank into the fort's back centre.
    That is what fixes the lopsided wool: with a flank spawn the two wools cannot be equidistant
    from their own spawn AND from the attacking one, and the composer resolves the tension in
    favour of defence. On the axis both readings are 1.000 by construction.
  * the two `i` wools are re-hung as walled wards on the fort's shoulders, each entered through
    exactly one gate, and each gate carries the plan's bedrock approach wall (`walls`, which the
    composer emits empty on every board it makes).
  * the frontline was widened from 6 cells to 10 and is the only ground the relief touches.

Run: python3 specs/opus5-revetment/build-spec.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "tools", "sculpt")))
import props

SLUG = "opus5-revetment"
CELL = 5
MEADOW, FORT = 11, 17
FORT_Y = FORT                      # the course a made thing standing on the platform floors at

pieces = []
def P(pid, role, x, z, w, h, surface):
    pieces.append({"id": pid, "role": role, "rect": [x, z, w, h], "surface": surface})

# ── the fort: the composed hub, its east arm cut back a cell so the work is symmetric ────────────
P("hub-t1", "piece", -5, 11, 7, 2, FORT)          # x -25..10  z 55..65
P("hub-t2", "piece", -5, 7, 7, 2, FORT)           # x -25..10  z 35..45
P("hub-t3", "piece", -5, 9, 2, 2, FORT)           # x -25..-15 z 45..55
P("hub-t4", "piece", 0, 9, 2, 2, FORT)            # x   0..10  z 45..55
P("hub-t5", "piece", 2, 11, 3, 2, FORT)           # x  10..25  z 55..65  (was 4 cells)
P("hub-t6", "piece", 2, 7, 3, 2, FORT)            # x  10..25  z 35..45  (was 4 cells)
P("hub-t7", "piece", 4, 9, 1, 2, FORT)            # x  20..25  z 45..55  (was 2 cells)
# the two wells the hub rings: x -15..0 and x 10..20, both z 45..55

# ── the spawn, moved from the composed west spur to the back of the fort ─────────────────────────
P("spawn-t1", "piece", -2, 13, 4, 2, FORT)        # x -10..10  z 65..75
P("spawn-room", "spawn", -2, 15, 4, 2, FORT)      # x -10..10  z 75..85

# ── the west ward: one gate, and the wool room walled inside it ──────────────────────────────────
P("ward-w-gate", "piece", -7, 7, 2, 6, FORT)      # x -35..-25 z 35..65  the gate court
P("ward-w-s", "piece", -10, 8, 3, 1, FORT)        # x -50..-35 z 40..45
P("wool-a-room", "wool-room", -9, 9, 2, 2, FORT)  # x -45..-35 z 45..55
P("ward-w-w", "piece", -10, 9, 1, 2, FORT)        # x -50..-45 z 45..55
P("ward-w-n", "piece", -10, 11, 3, 1, FORT)       # x -50..-35 z 55..60

# ── the east ward ────────────────────────────────────────────────────────────────────────────────
P("ward-e-gate", "piece", 5, 7, 2, 6, FORT)       # x  25..35  z 35..65
P("ward-e-s", "piece", 7, 8, 3, 1, FORT)          # x  35..50  z 40..45
P("wool-b-room", "wool-room", 7, 9, 2, 2, FORT)   # x  35..45  z 45..55
P("ward-e-e", "piece", 9, 9, 1, 2, FORT)          # x  45..50  z 45..55
P("ward-e-n", "piece", 7, 11, 3, 1, FORT)         # x  35..50  z 55..60

# ── the meadow the assault crosses ───────────────────────────────────────────────────────────────
P("frontline-t1", "piece", -5, 2, 10, 5, MEADOW)  # x -25..25  z 10..35

plan = {
    "plan": 2,
    "meta": {"name": "Revetment"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 30, "surface": MEADOW,
                "observerY": 58},
    "pieces": pieces,
    "zones": [{"id": "mid-band", "rect": [-5, -2, 10, 4], "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [10, 5], "facing": "front"}],
        "wools": [{"id": "wool-1", "piece": "wool-a-room", "at": [5, 5]},
                  {"id": "wool-2", "piece": "wool-b-room", "at": [5, 5]}],
        "iron": [], "destroyables": [], "cores": [],
    },
    # Each ward faces the fort along three seams. Two of the three carry the bedrock curtain and
    # the middle one is left open: that seam is the gate, and the gatehouse is built on it.
    "walls": [{"a": "ward-w-gate", "b": "hub-t2"}, {"a": "ward-w-gate", "b": "hub-t1"},
              {"a": "ward-e-gate", "b": "hub-t6"}, {"a": "ward-e-gate", "b": "hub-t5"}],
    "boxes": [],
}

with open(os.path.join(HERE, f"{SLUG}.plan.json"), "w") as out:
    json.dump(plan, out, indent=1)
print("wrote the plan")

# ── materials ────────────────────────────────────────────────────────────────────────────────────
def solid(i, d=0): return {"kind": "solid", "id": i, "data": d}

STONE, GRASS, DIRT, COBBLE = solid(1), solid(2), solid(3), solid(4)
COARSE, ANDESITE, DIORITE = solid(3, 1), solid(1, 5), solid(1, 3)
GRAVEL, SAND, SANDSTONE, SMOOTH_SS = solid(13), solid(12), solid(24), solid(24, 2)
STONEBRICK, CHISELLED, MOSSY_BRICK = solid(98), solid(98, 3), solid(98, 1)
OAK_LOG, DARKOAK = solid(17, 0), solid(5, 5)

def cell_(seed, size, palette, rise=0, jitter=2, warp=2):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}

def stack(bands, ending="handOver"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for t, m in bands]}

def layered(bands, axis="depth", ending="handOver", beyond=None):
    out = {"kind": "layered", "axis": axis, "stack": stack(bands, ending)}
    if beyond is not None: out["beyond"] = beyond
    return out

# the body of the rock nobody sees until a face is cut: a voronoi, in stone, in the fill, with the
# ground the board is made of written LAST so it takes the cell interiors
ROCK_BODY = {"kind": "voronoi", "seed": 31, "cellSize": 11, "rise": 4, "bands": [
    {"depth": 1, "material": COBBLE}, {"depth": 2, "material": ANDESITE},
    {"depth": 1, "material": STONE}]}

TURF = layered([(1, GRASS), (2, DIRT), (1, COARSE)])
BROW = layered([(1, COARSE), (2, DIRT), (1, SANDSTONE)])
SCARP = layered([(2, SANDSTONE), (3, STONE), (4, ANDESITE)], beyond=STONE)
# the ground is finished by its ANGLE. The cuts are re-set from `incline` after the first build.
LEA_SURFACE = layered([(14, TURF), (14, BROW), (62, SCARP)], axis="slope", ending="repeat")

SETTS = cell_(41, 5, [STONEBRICK, ANDESITE], rise=3)
YARD = cell_(42, 6, [GRAVEL, ANDESITE], rise=2)
MADE = cell_(43, 4, [STONEBRICK, ANDESITE], rise=3)
STEPS = cell_(44, 4, [COBBLE, ANDESITE], rise=2)

themes = {
    # the grown ground: one theme, banded by slope, with its own rock in the fill
    "lea": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": SANDSTONE},
        "surface": {"enabled": True, "depth": 4, "material": LEA_SURFACE},
        "wall": layered([(1, COARSE), (2, SANDSTONE), (5, STONE)], beyond=ANDESITE),
        "wallEnabled": True,
        "fill": ROCK_BODY,
    },
    # the made ground. Its face is the revetment and is the whole point of the board, so it is
    # STRIPED rather than sampled: a wallDiagonal shears its runs by height so they climb the wall
    # at a batter, and one run is a teamTint -- each fort is its own island, so each wears its
    # garrison's colour and a player reads whose wall they are under from the far bank.
    "revet": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": CHISELLED},
        "surface": {"enabled": True, "depth": 2, "material": SETTS},
        "wallEnabled": True,
        "wall": {"kind": "wallDiagonal", "slope": 2, "runs": [
            {"material": STONEBRICK, "width": 4},
            {"material": {"kind": "teamTint", "blockId": 159, "neutral": solid(159, 8)}, "width": 1},
            {"material": COBBLE, "width": 3},
            {"material": ANDESITE, "width": 2},
        ]},
        "fill": ROCK_BODY,
    },
    # the two ward courts: a beaten yard rather than laid setts, so the wool's enclosure reads as
    # a different place from the fort it hangs off
    "garth": {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "drop", "wallOnTerrainFaces": True,
        "rim": {"enabled": True, "depth": 1, "material": COBBLE},
        "surface": {"enabled": True, "depth": 2, "material": YARD},
        "wallEnabled": True,
        "wall": {"kind": "wallRun", "runs": [
            {"material": STONEBRICK, "width": 3}, {"material": COBBLE, "width": 2},
            {"material": ANDESITE, "width": 1}]},
        "fill": ROCK_BODY,
    },
}

# ── reshaping the two compiled outlines, one vertex at a time ────────────────────────────────────
# The compiler emits the whole fort as one sixteen-vertex polygon and the meadow as a rectangle.
# Neither is a shape; both are the staircase of the plan's rectangles. These are the edits, in the
# order the driver replays them, and `simulate` below prints what they come to so a fold is caught
# before the board is stored rather than after.
FORT_SHAPE, LEA_SHAPE = "frontline-t1-17", "frontline-t1-11"

fort_edits = [
    # the west stair's re-entrant: ten wide, six deep, exactly the flight that fills it
    {"after": 2, "x": -18, "z": 35}, {"after": 3, "x": -18, "z": 39},
    {"after": 4, "x": -8, "z": 39}, {"after": 5, "x": -8, "z": 35},
    # the bastion between the two stairs: a salient pushed six blocks out over the meadow, so the
    # wall is not one line and the ground under it is enfiladed from both sides
    {"after": 6, "x": -6, "z": 35}, {"after": 7, "x": -3, "z": 29},
    {"after": 8, "x": 3, "z": 29}, {"after": 9, "x": 6, "z": 35},
    # the east stair's re-entrant
    {"after": 10, "x": 14, "z": 35}, {"after": 11, "x": 14, "z": 39},
    {"after": 12, "x": 24, "z": 39}, {"after": 13, "x": 24, "z": 35},
    # the four outer corners of the two wards chamfered in, so a ward reads as a bastion rather
    # than as a box. Every one of these moves INWARD; a corner pushed out would hang over void.
    {"index": 0, "x": -47, "z": 43}, {"index": 17, "x": 47, "z": 43},
    {"index": 18, "x": 47, "z": 57}, {"index": 27, "x": -47, "z": 57},
]

lea_edits = [
    # the meadow's front, where the crossing lands: five points pulled north so the shore is not a
    # ruled line. Nothing on the z=35 edge moves -- that edge is flush against the revetment.
    {"after": 0, "x": -16, "z": 14}, {"after": 1, "x": -7, "z": 11},
    {"after": 2, "x": 2, "z": 15}, {"after": 3, "x": 11, "z": 12},
    {"after": 4, "x": 18, "z": 16},
    # the two flanks, eaten into
    {"after": 6, "x": 21, "z": 20}, {"after": 7, "x": 24, "z": 28},
    {"after": 10, "x": -23, "z": 27}, {"after": 11, "x": -20, "z": 19},
]

def simulate(ring, ops):
    ring = [list(p) for p in ring]
    for op in ops:
        if "remove" in op: ring.pop(op["remove"])
        elif "index" in op: ring[op["index"]] = [op["x"], op["z"]]
        else: ring.insert(op["after"] + 1, [op["x"], op["z"]])
    return ring

FORT_RING = [[-50, 40], [-35, 40], [-35, 35], [35, 35], [35, 40], [50, 40], [50, 60], [35, 60],
             [35, 65], [10, 65], [10, 85], [-10, 85], [-10, 65], [-35, 65], [-35, 60], [-50, 60]]
LEA_RING = [[-25, 10], [25, 10], [25, 35], [-25, 35]]

# ── what the plan cannot state ───────────────────────────────────────────────────────────────────
def flight(fid, ring, low, high, material=None):
    """A stair is a thing somebody built, so it carries a MATERIAL rather than a theme, states its
    two ends and nothing between them, and runs at least twice its rise."""
    return {"id": fid, "type": "polygon", "operation": "add", "override": True, "keepClear": True,
            "group": "team", "floor": 0, "base_height": high, "material": material or STEPS,
            "height_mode": "level", "skirt": 0,
            "vertices": [[x, z] for x, z in ring],
            "anchor_heights": [low, low, high, high]}

def patch(pid, ring, theme, height):
    """A splotch: a theme stated on a shape, seated at exactly the ground it lies on, carrying no
    relief_scope -- a scope is a statement about height and would pin the ring rigid."""
    return {"id": pid, "type": "polygon", "operation": "add", "group": "team",
            "base_height": height, "theme": theme,
            "vertices": [[x, z] for x, z in ring]}

add_shapes = [
    # the two flights, each set INTO the wall in its own re-entrant: fourteen blocks of run for six
    # courses of rise, and the re-entrant is cut to exactly their width.
    flight("stair-west", [(-18, 26), (-8, 26), (-8, 39), (-18, 39)], MEADOW, FORT),
    flight("stair-east", [(14, 26), (24, 26), (24, 39), (14, 39)], MEADOW, FORT),
    # the two ward courts, painted as yards rather than as the fort's laid setts
    patch("garth-w", [(-47, 43), (-36, 41), (-26, 44), (-26, 56), (-36, 59), (-47, 57)],
          "garth", FORT),
    patch("garth-e", [(47, 43), (36, 41), (26, 44), (26, 56), (36, 59), (47, 57)], "garth", FORT),
]

# ── the relief: the meadow, and nothing else ─────────────────────────────────────────────────────
# The fort is `exclude`, so it is out of the solve entirely and the two grounds meet at a face
# rather than being graded into each other. That face is the revetment and the stairs are the join.
def lobe(cx, cz, radii, turn=0.0):
    import math
    n = len(radii)
    return [[round(cx + r * math.cos(turn + 2 * math.pi * i / n), 1),
             round(cz + r * math.sin(turn + 2 * math.pi * i / n), 1)]
            for i, r in enumerate(radii)]

relief = {"team": {
    "base": MEADOW, "step": 1, "reach": 18, "landform": "plain",
    "grain": {"amplitude": 1, "scale": 15, "seed": 6},
    "marks": [
        # the meadow is ground to FIGHT on, so most of it is stated flat and stated once. A board
        # whose every mark carries a tread is a board of shoulders with nowhere to stand (RL5); the
        # face this board is about is the revetment, and the revetment is not in the relief at all.
        {"id": "apron", "kind": "area", "h": MEADOW - 1,
         "ring": lobe(-1, 19, [23, 19, 22, 13, 21, 19, 23, 13])},
        # two knolls in the corners the stairs do not reach, and a bench between the bastion and
        # the east stair. Nothing is pinned across a flight's foot: a stair states its own two ends
        # and the ground beside it has to arrive at the lower one, or the foot is a pit.
        {"id": "knoll-west", "kind": "point", "at": [-22, 30], "r": 5, "h": MEADOW + 3},
        {"id": "knoll-east", "kind": "point", "at": [23, 21], "r": 4, "h": MEADOW + 1,
         "tread": 3},
        {"id": "bench", "kind": "area", "h": MEADOW + 1,
         "ring": lobe(16, 31, [6, 4, 5, 4, 6, 4, 5, 4])},
        # dead ground at the bastion's east flank, where nobody on the parapet can see down
        {"id": "sump", "kind": "point", "at": [7, 32], "r": 4, "h": MEADOW - 1, "tread": 3},
    ],
    "pushes": [
        # the knowe in front of the bastion: the one landform on the board, and what breaks the
        # sightline from the parapet down to the crossing. A push is applied AFTER every
        # constraint, so its skirt has to clear both stair feet or it lifts the ground beside a
        # flight and puts a drop into the first tread -- measured at (-13, 27), a four-block one,
        # on an earlier build. Its two gradients agree: 2 over 8 up the skirt against 2 over 9 to
        # the crest, which is what makes it a swell and not a step with a hill on it (RL6).
        {"id": "knowe", "ring": lobe(0, 15, [11, 9, 10, 8, 11, 9, 10, 8]),
         "amount": 2, "falloff": 8, "crown": 2, "roughness": 1.2, "seed": 4},
    ],
}}

# ── the structures: layers, not block soup ───────────────────────────────────────────────────────
# Every one of these is circles, polygons and rectangles on a layer of its own, `kind: "made"` so
# SK10's pair walk and SK11's reachability walk leave them alone, and `part_of` so the storey strip
# groups them as one thing.
def made(layers, part):
    out = []
    for layer in (layers if isinstance(layers, list) else [layers]):
        inner = layer.pop("layout")
        layer["shapes"], layer["groups"] = inner["shapes"], inner["groups"]
        layer["kind"], layer["part_of"] = "made", part
        for shape in layer["shapes"]:
            shape.pop("theme", None)
            shape["material"] = MADE
        out.append(layer)
    return out

structures = []
# the parapet along the fort's south lip, in four runs with the two stair mouths left open
# the runs stop short of x -26..-24 and 24..26: the plan's own bedrock curtains stand in those
# columns, and a made thing sharing a course with one interleaves with it (SK18)
for pid, x0, x1 in (("par-west", -35, -27), ("par-gate", -23, -18), ("par-mid", 6, 14),
                    ("par-east", 27, 35)):
    structures += made(props.crenellated_wall(pid, x0, 35, x1, 37, 1, FORT_Y, 3, None,
                                              merlon=3, crenel=2, parapet=2, name=f"Parapet {pid}"),
                       "revetment")
# the bastion's own breastwork, out on the salient
structures += made(props.crenellated_wall("par-bastion", -3, 30, 3, 32, 1, FORT_Y, 3, None,
                                          merlon=2, crenel=2, parapet=2, name="Bastion breastwork"),
                   "revetment")
# two drum towers flanking the west stair's head, and a slim turret over the east one
structures += made(props.drum_tower("tower-wl", -21, 38, 3, 2, FORT_Y, 11, None, merlons=7,
                                    parapet=3, inner_floor=None, name="West gate tower"), "revetment")
structures += made(props.drum_tower("tower-wr", -4, 38, 4, 2, FORT_Y, 11, None, merlons=8,
                                    parapet=3, inner_floor=None, name="West gate tower, east side"),
                   "revetment")
structures += made(props.tapered_tower("turret-east", 30, 38, 4, 2, 2, FORT_Y, 15, None,
                                       name="East turret"), "revetment")
# one tower in each ward, on opposite sides of its gate: the plan is symmetric because that is what
# the two raids' balance needs, and the board is not
structures += made(props.drum_tower("tower-ward-w", -31, 58, 4, 2, FORT_Y, 13, None, merlons=9,
                                    parapet=3, inner_floor=None, name="West ward tower"), "revetment")
structures += made(props.drum_tower("tower-ward-e", 31, 42, 4, 2, FORT_Y, 13, None, merlons=9,
                                    parapet=3, inner_floor=None, name="East ward tower"), "revetment")

# the two wells the composed hub rings, railed rather than filled. A rail is drawn as the
# COMPLEMENT of the shaft -- four bars standing on the land round it -- because SK13 reads the
# compiled subtract as the board's negative space and refuses any add that puts ground back.
rail = props.LayerBuilder("well-rails", name="Well rails", base_y=0, mirrors=True, tag="rail")
for (wx0, wz0, wx1, wz1) in ((-15, 45, 0, 55), (10, 45, 20, 55)):
    rail.rect(wx0 - 1, wz0 - 1, wx1 + 1, wz0, FORT_Y, 2, None)
    rail.rect(wx0 - 1, wz1, wx1 + 1, wz1 + 1, FORT_Y, 2, None)
    rail.rect(wx0 - 1, wz0, wx0, wz1, FORT_Y, 2, None)
    rail.rect(wx1, wz0, wx1 + 1, wz1, FORT_Y, 2, None)
structures += made(rail.done(), "revetment")

# ── dressing ─────────────────────────────────────────────────────────────────────────────────────
ROAD_PAVE = cell_(45, 4, [GRAVEL, ANDESITE, COBBLE])   # a way is three blocks a reader cannot quite tell apart
props_list = [
    # the fort's own circulation, drawn before the scenery: out of the spawn door and round the two
    # wells to each ward's gate, which are the only two seams in the curtain. A stroke repaints the
    # top course and adds no cell, so it says where players walk without moving any ground.
    {"id": "way-west", "kind": "stroke", "seed": 61, "radius": 2.5, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": ROAD_PAVE,
     "points": [[0, 78], [0, 68], [-6, 62], [-16, 57], [-26, 52], [-33, 50]]},
    {"id": "way-east", "kind": "stroke", "seed": 62, "radius": 2.5, "style": "solid",
     "coverage": 1.0, "claimsGround": True, "pave": ROAD_PAVE,
     "points": [[0, 72], [7, 65], [17, 59], [26, 54], [33, 50]]},
    # ground cover over the whole meadow, as one shape and two small numbers: the patchiness is the
    # density field's job and a high coverage is a board whose slope banding cannot be read
    {"id": "sward", "kind": "flora", "seed": 9,
     "points": [[-25, 10], [25, 10], [25, 35], [-25, 35]],
     "spec": {"coverage": 0.22, "scale": 14, "octaves": 3, "fernShare": 0.14,
              "flowerShare": 0.05, "flowerScale": 18, "tallShare": 0.03}},
]
# rock fallen off the face, at the foot of the wall and nowhere else -- stone, cobble, andesite
for i, (bx, bz, form, size) in enumerate([(-16, 19, "angular", 2), (-3, 21, "angular", 3),
                                          (9, 31, "round", 2), (14, 20, "angular", 2)]):
    props_list.append({"id": f"spall-{i}", "kind": "boulder", "x": bx, "z": bz, "form": form,
                       "size": size, "mossy": i % 2 == 0, "rock": ANDESITE if i % 2 else STONE,
                       "seed": 80 + i})
# thorns, and only where nobody walks: the dead ground under the west wall, the lee of the
# bastion, and the shore the crossing lands on
for i, (tx, tz, sp, h) in enumerate([(-22, 32, "oak", 8), (12, 30, "birch", 9), (-6, 18, "oak", 7)]):
    props_list.append({"id": f"thorn-{i}", "kind": "tree", "x": tx, "z": tz, "form": "Template",
                       "species": sp, "height": h, "seed": 90 + i})

# the one building on the board, and it is not made of what it stands on: a timber byre standing
# out on the meadow, halfway across the ground an assault has to cross, where `sketch/seats` says a
# 7x5 footprint may stand. It is cover in the open, which is the only reason to put a building
# there -- the fort's own front range is full of the fort's own structures and has no room for one.
props_list.append({"id": "byre", "kind": "house", "seed": 51, "front": "negZ",
                   "style": "@talltimber-store", "wings": [{"corners": [[3, 24], [9, 28]]}]})

finish = {
    "authors": ["Opus 5"],
    "created": "2026-09-15",
    "voidEnforcement": True,
    "mapTheme": "lea",
    "themes": themes,
    "themeById": {LEA_SHAPE: "lea", FORT_SHAPE: "revet"},
    # the fort is taken out of the relief solve, which is what makes the revetment a FACE rather
    # than a graded shoulder, and what puts the stairs somewhere
    "shapePropsById": {FORT_SHAPE: {"relief_scope": "exclude"}},
    "editShapes": {FORT_SHAPE: fort_edits, LEA_SHAPE: lea_edits},
    "addShapes": add_shapes,
    "addLayers": structures,
    "relief": relief,
    "roomStyles": {"spawn": "@sb-spawn", "wool": "@ow-cage"},
    "dressing": {"props": props_list},
}

with open(os.path.join(HERE, f"{SLUG}.finish.json"), "w") as out:
    json.dump(finish, out, indent=1)
print("wrote the finish:", len(structures), "made layers,", len(add_shapes), "shapes,",
      len(props_list), "props")
