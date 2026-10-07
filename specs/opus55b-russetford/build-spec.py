#!/usr/bin/env python3
"""Russetford — an autumn river valley, destroy the monument, 16 a side.

`composition.md` beside this file is the drawing this script builds: the zones, what each is for and how a
player goes between them. Team 0 holds the north bank (z < 0); rot_180 about the origin fans the south.
Writes opus55b-russetford.plan.json and opus55b-russetford.refinement.json beside itself.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "opus55b-russetford"
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))

# ---- heights (blocks) -------------------------------------------------------------------------
WATER = 20          # the river's line, and the leat's
FLATS = 21          # the holm and the beach the water meets
FARM_Y = 40         # the spawn farm's knoll
GREEN_Y = 32        # the village green, where the monument stands
VILLAGE_Y = 24      # the village street
ORCHARD_Y = 28      # the orchard's foot, over the cut bank

# ---- the plan ---------------------------------------------------------------------------------
# One valley crossing the axis: the north bank is authored, its image is the south bank, and the river runs
# over the seam. Nothing is void inside the board, so nothing needs a build zone.
plan = {
    "plan": 2,
    "meta": {"name": "Russetford", "authors": ["Opus 5.5"]},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 24},
    "pieces": [
        {"id": "ridge",     "rect": [-16, -24, 32, 3]},
        {"id": "westfarm",  "rect": [-16, -21, 6, 4]},
        {"id": "eastfarm",  "rect": [-6, -21, 22, 4]},
        {"id": "valley",    "rect": [-16, -17, 32, 17]},
        {"id": "spawn-room", "role": "spawn", "rect": [-10, -21, 4, 4], "surface": FARM_Y},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [8, 8], "facing": "back"}],
        "destroyables": [{"id": "monument", "piece": "", "at": [4, -56], "style": "pillar-3", "float": 4}],
    },
}

# ---- helpers ----------------------------------------------------------------------------------
def rect_ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]

def disc(cx, cz, r, n=12, wob=0.0, seed=0):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + wob * math.sin(3 * a + seed))
        out.append([round(cx + rr * math.cos(a), 1), round(cz + rr * math.sin(a), 1)])
    return out

def B(i, d=0): return {"kind": "solid", "id": i, "data": d}

def layered(axis, *bands, ending="repeat"):
    return {"kind": "layered", "axis": axis,
            "stack": {"ending": ending, "bands": [{"material": m, "thickness": t} for m, t in bands]}}

def over_soil(top, under=None):
    return layered("depth", (top, 1), (under or B(3), 2), ending="handOver")

def noise(stops, scale=2, seed=1, rise=None):
    out = {"kind": "noise", "seed": seed, "scale": scale, "octaves": 2, "stops": stops}
    if rise: out["rise"] = rise
    return out

def cell(palette, size=2, seed=1, rise=None):
    out = {"kind": "cell", "seed": seed, "cellSize": size, "palette": palette}
    if rise: out["rise"] = rise
    return out

def made_layer(lid, name, shapes, part_of=None, mirrors=True, seat=None):
    layer = {"id": lid, "name": name, "base_y": 0, "kind": "made", "shapes": shapes,
             "groups": [{"id": lid, "name": name, "mirrors": mirrors, "shapeIds": [s["id"] for s in shapes]}]}
    if part_of: layer["part_of"] = part_of
    if seat: layer["seat"] = seat
    return layer

def box(sid, x0, z0, x1, z1, floor, height, material):
    return {"id": sid, "type": "rectangle", "operation": "add", "min_x": x0, "min_z": z0,
            "max_x": x1, "max_z": z1, "floor": floor, "base_height": height, "material": material}

# ---- materials --------------------------------------------------------------------------------
GRASS, DIRT, COARSE, PODZOL = B(2), B(3), B(3, 1), B(3, 2)
STONE, ANDESITE, COBBLE, GRAVEL = B(1), B(1, 5), B(4), B(13)
SAND, SANDSTONE, FARMLAND = B(12), B(24), B(60)
SPRUCE_PLANK, DARKOAK_PLANK, OAK_PLANK = B(5, 1), B(5, 5), B(5, 0)
STONEBRICK, MOSSY_COBBLE = B(98), B(48)

ROCK = noise([ANDESITE, STONE, STONE, COBBLE], scale=2, seed=4)
WALLROCK = dict(ROCK, rise=3)
EARTH = cell([DIRT, COARSE], size=2, seed=2)
FILL = cell([STONE, STONE, ANDESITE], size=5, seed=9, rise=4)

def theme(flat, cut_grass=30, cut_earth=12, steep=None):
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void",
        "rim": {"enabled": False, "depth": 1, "material": STONE},
        "surface": {"enabled": True, "depth": 3, "material": layered(
            "slope", (over_soil(flat), cut_grass), (over_soil(EARTH), cut_earth),
            (over_soil(steep or ROCK, STONE), 90 - cut_grass - cut_earth))},
        "wallEnabled": True, "wallOnTerrainFaces": True, "wall": WALLROCK,
        "fill": FILL,
    }

# ---- the river, the leat and the cave ---------------------------------------------------------
# The Russet's centreline, the north half from the origin west; its image is the east half. The S is
# point-symmetric by itself, so each bank gets one outer bend (a cut cliff) and one inner bend (a beach).
RIVER = [[0, 0], [-14, -9], [-28, -13], [-42, -9], [-56, 0], [-70, 6]]
RIVER_R = 6
# the leat, cut from the river upstream of the village, run past the mill and back
LEAT = [[63, -6], [56, -20], [20, -20], [22, -10], [26, 8]]
# the cave: a mouth in the cut bank at water level, a drive under the orchard, a chamber under the green
CAVE = [[-31, -18], [-26, -18], [-23, -30], [-13, -39], [-3, -47], [-3, -60], [-11, -60], [-11, -50],
        [-18, -42], [-29, -33]]
CAVE_FLOOR = FLATS           # the floor's top course is the flats' own level
CAVE_ROOF = FLATS + 4        # three courses of headroom

# ---- relief -----------------------------------------------------------------------------------
relief = {"*": {
    "base": 26, "reach": 0, "step": 1,
    "marks": [
        # the river flats on the inner bend, the holm under the village
        {"id": "holm", "kind": "area", "h": FLATS, "ring": [[14, -17], [62, -17], [64, -8], [44, 2], [28, 4],
                                                              [16, -2]]},
        # the bridgehead the lane comes down to
        {"id": "bridgehead", "kind": "area", "h": 23, "ring": rect_ring(-6, -17, 7, -9)},
        # the orchard's foot, standing over the river's outer bend so the carve leaves a cut bank
        {"id": "orchard-foot", "kind": "area", "h": ORCHARD_Y,
         "ring": [[-64, -24], [-50, -16], [-36, -21], [-20, -20], [-12, -18], [-14, -26], [-64, -32]]},
        # the fields beside the farm, and the farm's knoll
        {"id": "fields", "kind": "area", "h": 37, "ring": rect_ring(-64, -66, -52, -50)},
        {"id": "farm", "kind": "area", "h": FARM_Y, "bevel": 3,
         "ring": [[-46, -88], [-4, -88], [-4, -74], [-20, -64], [-46, -64]]},
        # the ridge behind the farm, and the saddle between it and the hanger
        {"id": "ridge", "kind": "line", "r": 4, "points": [[-64, -94], [-34, -95], [-6, -93]], "h": [50, 48, 44]},
        # the green's knoll, the village street and the mill yard
        {"id": "green", "kind": "area", "h": GREEN_Y, "ring": disc(4, -56, 9)},
        {"id": "village", "kind": "area", "h": VILLAGE_Y, "ring": [[16, -58], [60, -58], [60, -41], [16, -41]]},
        {"id": "millyard", "kind": "area", "h": 22, "ring": rect_ring(18, -37, 56, -25)},
        # the hanger: a summit the solver grades down to the village, the saddle and the edge
        {"id": "hanger", "kind": "area", "h": 42, "ring": disc(50, -86, 7, wob=0.15, seed=1)},
    ],
    "pushes": [
    ],
}}

# ---- themes -----------------------------------------------------------------------------------
THEMES = {
    "valley": theme(GRASS),
    "beach":  theme(noise([SAND, GRAVEL, GRAVEL, ANDESITE], scale=2, seed=6), cut_grass=24, cut_earth=10),
    "wood":   theme(noise([GRASS, PODZOL, PODZOL, COARSE], scale=2, seed=8), cut_grass=42, cut_earth=10),
}

# ---- shapes on the ground ---------------------------------------------------------------------
add_shapes = [
    {"id": "cave-roof", "type": "polygon", "operation": "add", "override": True,
     "floor": CAVE_ROOF, "vertices": CAVE},
]
add_layers = [
    {"id": "cave", "name": "Cave", "base_y": 0, "below": True,
     "shapes": [{"id": "cave-floor", "type": "polygon", "operation": "add", "floor": 0,
                 "base_height": CAVE_FLOOR + 1, "material": FILL, "vertices": CAVE}],
     "groups": [{"id": "cave", "name": "cave", "mirrors": True, "shapeIds": ["cave-floor"]}]},
]

# the bridge: a stone arch over the middle, drawn whole on the axis and kept off the fan
bridge = []
for z in range(-12, 12):
    t = abs(z + 0.5) / 12.0                       # 0 at the crown, 1 at the abutments
    under = 21 + int(round(3 * math.sqrt(max(0.0, 1 - t * t))))
    deck = 25
    bridge.append(box(f"arch-{z + 12}", -2, z, 2, z + 1, under, deck - under, STONEBRICK))
    for px in (-3, 2):                            # the parapets
        bridge.append(box(f"parapet-{px}-{z + 12}", px, z, px + 1, z + 1, under, deck + 1 - under, COBBLE))
add_layers.append(made_layer("bridge", "Russet bridge", bridge, part_of="bridge", mirrors=False))

# the waterwheel: a slatted disc standing in the leat against the mill's south wall
WHEEL_X, WHEEL_Y, WHEEL_R = 36, 21, 5
PADDLES = {"kind": "checker", "size": 1, "even": DARKOAK_PLANK, "odd": SPRUCE_PLANK}
wheel = []
for dx in range(-WHEEL_R, WHEEL_R + 1):
    h = int(math.floor(math.sqrt(WHEEL_R * WHEEL_R - dx * dx) + 0.4))
    wheel.append(box(f"wheel-{dx + WHEEL_R}", WHEEL_X + dx, -22, WHEEL_X + dx + 1, -20, WHEEL_Y - h, 2 * h + 1,
                     PADDLES))
wheel.append(box("axle", WHEEL_X, -27, WHEEL_X + 1, -22, WHEEL_Y, 1, B(162, 9)))
add_layers.append(made_layer("wheel", "Mill wheel", wheel, part_of="mill-wheel"))

# two footbridges off the holm over the leat
foot = []
for i, (x0, x1) in enumerate(((22, 25), (44, 47))):
    foot.append(box(f"foot-{i}", x0, -25, x1, -16, 21, 1, SPRUCE_PLANK))
add_layers.append(made_layer("footbridges", "Footbridges", foot, part_of="footbridges"))

# ---- the dressing: what each zone holds --------------------------------------------------------
import showcase
TREES = showcase.trees()
STYLES = {
    "oak": TREES["oak-3"]["style"], "oak-b": TREES["oak-6"]["style"],
    "oak-large": TREES["large-oak-1"]["style"],
    "fruit": TREES["tiny-oak-1"]["style"], "fruit-b": TREES["tiny-oak-5"]["style"],
    "cottage": {"library": "spruce-roofed-white-clay-cottage", "kind": "house"},
    "stonecot": {"library": "brick-roofed-stone-cottage", "kind": "house"},
    "mill": {"library": "spruce-roofed-stone-longhouse", "kind": "house"},
    "barn": {"library": "hay-gambrel-barn", "kind": "house"},
}

def tree(tid, x, z, style="oak"):
    return {"id": tid, "kind": "tree", "style": style, "x": x, "z": z, "layer": "ground"}

def house(hid, style, front, *wings, seed=1):
    out = {"id": hid, "kind": "house", "layer": "ground", "seed": seed, "front": front, "style": style,
           "wings": [{"corners": [list(a), list(b)], "spec": dict(spec)} for a, b, spec in wings]}
    return out

# a lane of one brown: leaf-strewn podzol, coarse dirt and boards, a third each
LANE = cell([PODZOL, COARSE, SPRUCE_PLANK], size=1, seed=11)
def lane(pid, pts, radius=1.5, wander=3):
    return {"id": pid, "kind": "stroke", "points": pts, "radius": radius, "style": "solid", "pave": LANE,
            "claimsGround": True, "wander": wander, "wanderLength": 14, "seed": len(pid)}

props = [
    # -- the farm: the spawn farmhouse (the room), its barn across the yard
    house("barn", "barn", "posZ", ((-16, -86), (-7, -76), {"ridge": "alongZ"}), seed=2),
    # -- the village: cottages along the street, the miller's house and the mill on the leat
    house("cottage-1", "cottage", "posZ", ((18, -54), (25, -48), {"ridge": "alongX"}), seed=3),
    house("cottage-2", "stonecot", "posZ", ((32, -55), (40, -49), {"ridge": "alongX"}), seed=4),
    house("cottage-3", "cottage", "posZ", ((47, -54), (54, -47), {"ridge": "alongZ"}), seed=5),
    house("mill", "mill", "negZ", ((31, -36), (43, -28), {"ridge": "alongX"}), seed=7),
    house("miller", "stonecot", "negZ", ((49, -37), (55, -31), {"ridge": "alongX"}), seed=6),
    # -- the orchard: fruit trees in a quincunx on the slope over the cut bank
    *[tree(f"fruit-{i}", x, z, "fruit" if i % 2 else "fruit-b") for i, (x, z) in enumerate(
        [(-60, -28), (-48, -28), (-36, -28), (-54, -40), (-42, -40), (-48, -51), (-36, -51)])],
    # -- the ridge wood behind the farm, either side of the spawn's back
    tree("ridge-1", -62, -74, "oak-large"), tree("ridge-2", -14, -90, "oak-b"), tree("ridge-3", -2, -86),
    # -- the hanger: oaks on its skirt round the tower, its west edge toward the green
    tree("hanger-1", 28, -72), tree("hanger-2", 42, -62, "oak-b"), tree("hanger-3", 60, -66),
    tree("hanger-4", 36, -94, "oak-large"), tree("hanger-5", 62, -92, "oak-b"),
    # -- a tree by the bridgehead and one on the holm
    tree("holm-1", 54, -12, "oak-b"),
    # -- the lanes: spawn to green, green to bridge, the village street up to the tower, the mill lanes,
    #    the farm down through the orchard to the cliff, the farm across the saddle to the hanger
    lane("spawn-lane", [[-32, -66], [-22, -62], [-10, -60], [-5, -57]]),
    lane("bridge-lane", [[4, -46], [3, -36], [1, -24], [0, -13]]),
    lane("street", [[13, -50], [20, -43], [34, -44], [46, -43], [60, -46]], radius=2),
    lane("tower-lane", [[60, -46], [62, -58], [56, -70], [50, -74]]),
    lane("mill-lane-w", [[23, -43], [24, -38], [23.5, -27], [23.5, -16]], wander=1),
    lane("mill-lane-e", [[45.5, -43], [45.5, -38], [45.5, -27], [45.5, -16]], radius=1, wander=0),
    lane("orchard-lane", [[-36, -66], [-32, -56], [-30, -44], [-28, -32], [-27, -24]]),
    lane("saddle-lane", [[-8, -72], [4, -78], [18, -80], [30, -82], [42, -78]]),
    # -- ground cover over the whole bank, wheat on the field
    {"id": "flora", "kind": "flora", "layer": "ground", "seed": 13,
     "points": [[-64, -96], [64, -96], [64, 0], [-64, 0]],
     "spec": {"coverage": 0.2, "scale": 6, "octaves": 2, "fernShare": 0.3, "flowerShare": 0.03,
              "flowerScale": 10, "tallShare": 0.03, "cropShare": 0.9, "crops": ["wheat", "potatoes"],
              "ripeness": 0.85, "lilyShare": 0.08}},
]

# the field: farmland the flora sows, hedged
add_shapes.append({"id": "field", "type": "polygon", "operation": "add", "theme": "field", "floor": 0,
                   "base_height": 24, "vertices": rect_ring(-63, -65, -53, -51)})
# the holm's point bar, gravel and sand where the river drops it
add_shapes.append({"id": "point-bar", "type": "polygon", "operation": "add", "theme": "beach", "floor": 0,
                   "base_height": 24, "vertices": [[24, -6], [40, -10], [56, -6], [46, 2], [30, 4]]})
# the leaf floor under the hanger's oaks
add_shapes.append({"id": "hanger-floor", "type": "polygon", "operation": "add", "theme": "wood", "floor": 0,
                   "base_height": 24, "vertices": [[22, -60], [40, -58], [64, -60], [64, -94], [24, -94]]})
THEMES["field"] = theme(FARMLAND, cut_grass=40, cut_earth=10)

# walls and hedges laid over the ground: the hedges round the field, dry-stone walls on the saddle
HEDGE = B(18, 4)                     # oak leaves that never decay
DRYSTONE = cell([MOSSY_COBBLE, COBBLE, COBBLE, STONE], size=2, seed=12, rise=1)
def laid(sid, pts, material, height=1, radius=0.5):
    return {"id": sid, "type": "polyline", "operation": "add", "vertices": pts, "radius": radius,
            "height_mode": "drape", "base_height": height, "material": material, "keepClear": True,
            "stroke_edge": "solid"}
add_shapes += [
    laid("hedge-field", [[-64, -50], [-64, -66], [-52, -66], [-52, -54]], HEDGE, 2),
    laid("wall-saddle-1", [[-2, -66], [6, -72], [14, -70], [22, -64]], DRYSTONE),
    laid("wall-saddle-2", [[0, -90], [10, -86], [22, -88], [26, -94]], DRYSTONE),
    laid("wall-green", [[14, -40], [8, -44]], DRYSTONE),
    # the bridge lane runs between hedges, with gaps where the field gates are
    laid("hedge-lane-w1", [[-3, -42], [-4, -33]], HEDGE, 2), laid("hedge-lane-w2", [[-4, -28], [-5, -18]], HEDGE, 2),
    laid("hedge-lane-e1", [[8, -42], [7, -34]], HEDGE, 2), laid("hedge-lane-e2", [[6, -29], [6, -18]], HEDGE, 2),
    # a hedge across the meadow between the lane and the orchard, the line the west bank is held on
    laid("hedge-meadow", [[-24, -48], [-16, -44], [-10, -40]], HEDGE, 2),
    # the cottage gardens behind the north row, fenced
    laid("garden-1", [[17, -55], [17, -60], [26, -60], [26, -55]], B(85), 1),
    laid("garden-2", [[31, -56], [31, -60], [41, -60], [41, -56]], B(85), 1),
]

# the ruined tower on the hanger's top, seated on the ground under it
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "sculpt"))
import props as sculpt
def as_added(layer, kind="made", part_of=None, seat=None):
    out = {"id": layer["id"], "name": layer["name"], "base_y": layer["base_y"], "kind": kind,
           "shapes": layer["layout"]["shapes"], "groups": layer["layout"]["groups"]}
    for sh in out["shapes"]:
        sh.pop("theme", None)
        sh["material"] = cell([MOSSY_COBBLE, STONEBRICK, COBBLE, STONEBRICK], size=2, seed=21, rise=1)
    if part_of: out["part_of"] = part_of
    if seat: out["seat"] = seat
    return out
for layer in sculpt.drum_tower("tower", 50, -86, 4, 1, 50, 8, "ruin", merlons=6, parapet=2):
    add_layers.append(as_added(layer, part_of="tower", seat="ground"))

# the cave mouth's timbers, in the cut bank at the water's edge
POST, LINTEL = B(162, 1), B(162, 5)
add_layers.append(made_layer("cave-mouth", "Cave mouth", [
    box("mouth-post-w", -31, -21, -30, -20, CAVE_FLOOR + 1, 3, POST),
    box("mouth-post-e", -27, -21, -26, -20, CAVE_FLOOR + 1, 3, POST),
    box("mouth-lintel", -30, -21, -27, -20, CAVE_FLOOR + 3, 1, LINTEL)], part_of="cave-mouth"))
# pumpkins in the gardens
pumpkins = [box(f"pumpkin-{i}", x, z, x + 1, z + 1, 0, 1, B(86, i % 4)) for i, (x, z) in enumerate(
    [(19, -58), (22, -57), (24, -59), (33, -58), (36, -57), (39, -59), (35, -59)])]
add_layers.append(made_layer("pumpkins", "Pumpkin patch", pumpkins, part_of="pumpkins", seat="ground"))

# the village well, in the gap between the cottages and the street
WG = 24
well = [made_layer("well-curb", "Well curb", [box(f"curb-{i}", x, z, x + 1, z + 1, WG, 1, COBBLE)
                                              for i, (x, z) in enumerate([(42, -51), (43, -51), (44, -51), (42, -50),
                                                                          (44, -50), (42, -49), (43, -49), (44, -49)])]
                    + [box("well-water", 43, -50, 44, -49, WG - 2, 3, B(9))], part_of="well", seat="ground"),
        made_layer("well-posts", "Well posts", [box("post-a", 42, -50, 43, -49, WG + 1, 2, B(85)),
                                                box("post-b", 44, -50, 45, -49, WG + 1, 2, B(85))],
                   part_of="well", seat="ground"),
        made_layer("well-roof", "Well roof", [box("well-roof", 41, -51, 46, -48, WG + 3, 1, B(126, 1))],
                   part_of="well", seat="ground")]
add_layers += well

# hay in the farm yard and a log pile at the woodcutter's clearing
HAY, LOG = B(170), B(17, 4)
yard = [box("hay-1", -22, -70, -20, -68, FARM_Y, 2, HAY), box("hay-2", -19, -70, -18, -68, FARM_Y, 1, HAY),
        box("hay-3", -12, -72, -10, -71, FARM_Y, 1, HAY)]
add_layers.append(made_layer("hayyard", "Hay yard", yard, part_of="hayyard", seat="ground"))
logs = [box("logs-1", 34, -76, 38, -74, 0, 2, LOG), box("logs-2", 35, -74, 38, -73, 0, 1, LOG),
        box("stump-1", 38, -70, 39, -69, 0, 1, B(17, 0)), box("stump-2", 32, -69, 33, -68, 0, 1, B(17, 0))]
add_layers.append(made_layer("woodpile", "Woodcutter's clearing", logs, part_of="woodpile", seat="ground"))

# ---- the refinement ---------------------------------------------------------------------------
refinement = {
    "relief": relief,
    "biome": {"kind": "noise", "seed": 3, "scale": 40, "octaves": 2, "stops": [1, 35, 37, 37, 35, 1]},
    "themes": THEMES,
    "mapTheme": "valley",
    "addShapes": add_shapes,
    "addLayers": add_layers,
    "roomStyles": {"spawn": {"library": "spruce-roofed-white-clay-cottage"}},
    "dressing": {"styles": STYLES, "props": props + [
        {"id": "river", "kind": "fluid", "layer": "ground", "shape": "channel", "form": "natural",
         "points": RIVER, "radius": RIVER_R, "depth": 3, "level": WATER, "shore": 0, "edge": 0, "seed": 7,
         "bank": noise([SAND, GRAVEL, GRAVEL, ANDESITE], scale=2, seed=6)},
        {"id": "leat", "kind": "fluid", "layer": "ground", "shape": "channel", "form": "canal",
         "points": LEAT, "radius": 2, "depth": 2, "level": WATER, "shore": 0, "edge": 0, "seed": 9,
         "bank": GRAVEL},
    ]},
    "authors": ["Opus 5.5"],
    "created": "2026-10-07",
}

for name, doc in (("plan", plan), ("refinement", refinement)):
    with open(os.path.join(HERE, f"{SLUG}.{name}.json"), "w") as f:
        json.dump(doc, f, indent=1)
print("wrote", SLUG)
