"""Millrace, revamped in the studio — the author's re-theming of opus5-millrace restated as documents.

The world at maps/rockymine-ruediger-millrace was made by hand over the studio's build of opus5-millrace,
with WorldEdit and Arceon. review/fable-millrace-revamp.md is the measured account of what changed; this is
that account written back as the three documents the studio builds from, over the original's own layout so
the terrain, the water, the walls and the boulders stay where the author kept them.

    python3 specs/fable-millrace-revamp/build.py
    python3 tools/drive.py specs/fable-millrace-revamp "Millrace" --out maps/fable-millrace-revamp
"""
import json, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, f"{ROOT}/tools/sculpt")
from layers import compile_layers, stats

SRC = f"{ROOT}/specs/opus5-millrace/opus5-millrace"
OUT = f"{ROOT}/specs/fable-millrace-revamp/fable-millrace-revamp"
plan = json.load(open(f"{SRC}.plan.json"))
layout = json.load(open(f"{SRC}.layout.json"))
intent = json.load(open(f"{SRC}.intent.json"))
BODIES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trees.json")))
MODELS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

# ── materials ────────────────────────────────────────────────────────────────────────────────────────
def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
def noise(stops, scale, seed, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 3, "stops": stops, "rise": rise}
def turb(stops, scale, seed, rise=0):
    return {"kind": "turbulence", "seed": seed, "scale": scale, "octaves": 3, "stops": stops, "rise": rise}
def cell(palette, size, seed, jitter=2, warp=1, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp, "palette": palette, "rise": rise}
def layered(bands):
    """A depth stack: (material, thickness) from the top down; past the last band the fill takes over."""
    return {"kind": "layered", "axis": "depth",
            "stack": {"bands": [{"material": m, "thickness": t} for m, t in bands], "ending": "handOver"}}

STONE, ANDESITE, POLISHED, COBBLE, MOSSY = solid(1), solid(1, 5), solid(1, 6), solid(4), solid(48)
EMERALD_ORE, CYAN_CLAY, PRISMARINE, GRAVEL = solid(129), solid(159, 9), solid(168), solid(13)
GRASS, DIRT, COARSE, PODZOL, SPRUCE_PLANK = solid(2), solid(3), solid(3, 1), solid(3, 2), solid(5, 1)
GRANITE, POLISHED_GRANITE, JUNGLE_PLANK = solid(1, 1), solid(1, 2), solid(5, 3)
SBRICK, MOSSY_B, CRACKED = solid(98), solid(98, 1), solid(98, 2)
DSLAB, SMOOTH_DSLAB, LIGHT_GRAY_WOOL = solid(43), solid(43, 8), solid(35, 8)
WHITE_G, PLANK_S = solid(95, 0), solid(5, 1)

# The stone body: cells nine blocks across and four tall, each cell one turbulent mix of two or three of the
# six stones — the author's placeholder-and-replace sequence (#vor[7] then #turb[5] inside it) stated as one
# nested pattern. `rise` is what makes a pattern a volume; without it a cell runs the whole height of a cliff,
# and a cell as tall as it is wide still reads as a column on a cut face — the author's blobs are wider than
# tall, so the cells are.
BODY = cell([
    turb([ANDESITE, POLISHED], 7, 71, rise=4),
    turb([STONE, ANDESITE], 7, 72, rise=4),
    turb([MOSSY, STONE, MOSSY], 7, 73, rise=4),
    cell([EMERALD_ORE, POLISHED, MOSSY, ANDESITE], 5, 74, rise=4),
    cell([CYAN_CLAY, STONE, ANDESITE], 5, 75, rise=4),
    turb([POLISHED, MOSSY], 7, 76, rise=4),
], 9, 70, rise=5)
# Three courses of earth under every soil surface: coarse dirt, spruce planks and dirt.
EARTH = noise([COARSE, COARSE, COARSE, SPRUCE_PLANK, SPRUCE_PLANK, DIRT], 4, 80, rise=8)
# The surfaces: the moor's grass with dirt and podzol in it, the wold's dirt with grass specks, the holm's
# podzol, and the race bed under the water.
MOOR_TOP = noise([GRASS, GRASS, GRASS, COARSE, GRASS, DIRT, COARSE, PODZOL], 4, 81)
WOLD_TOP = noise([COARSE, DIRT, COARSE, GRASS, PODZOL, COARSE, DIRT, GRASS], 4, 82)
HOLM_TOP = noise([PODZOL, COARSE, PODZOL, GRASS, COARSE, DIRT], 4, 83)
BED_TOP = noise([COARSE, SPRUCE_PLANK, COARSE, GRAVEL, SPRUCE_PLANK, MOSSY, ANDESITE, PRISMARINE], 4, 84)
QUAY = cell([DSLAB, DSLAB, SMOOTH_DSLAB, LIGHT_GRAY_WOOL, DSLAB], 4, 90, rise=4)
MASONRY_SURF = noise([SBRICK, MOSSY_B], 11, 41); MASONRY_FILL = noise([SBRICK, CRACKED], 11, 42)

def theme(surface, wall, fill, depth):
    return {"bedrock": {"relative": False, "value": 1}, "wallOnTerrainFaces": False,
            "surface": {"enabled": True, "depth": depth, "material": surface},
            "wall": wall, "wallEnabled": True, "fill": fill,
            "rim": {"enabled": False, "depth": 1, "material": STONE}, "rimEdges": "boundary"}
def ground(top): return theme(layered([(top, 1), (EARTH, 3)]), BODY, BODY, 4)
def flat(b): return theme(b, b, b, 1)

THEMES = {
    "moor": ground(MOOR_TOP), "wold": ground(WOLD_TOP), "holm": ground(HOLM_TOP),
    "bed": theme(layered([(BED_TOP, 1), (EARTH, 2)]), BODY, BODY, 3),
    "quay": theme(QUAY, QUAY, QUAY, 1),
    "masonry": theme(MASONRY_SURF, MASONRY_FILL, MASONRY_FILL, 1),
    "timber": flat(PLANK_S), "cloud": flat(WHITE_G),
}

# ── the ground: the original's shapes, re-themed ────────────────────────────────────────────────────
ground_layer = layout["layers"][0]
RETHEME = {"s0": "bed", "s1": "moor", "s2": "wold", "s3": "holm",
           "wall-s": "quay", "wall-n-w": "quay", "wall-n-e": "quay"}
for shape in ground_layer["layout"]["shapes"]:
    if shape["id"] in RETHEME: shape["theme"] = RETHEME[shape["id"]]
    elif shape.get("theme") in ("stone-pale", "worn"): shape["theme"] = "masonry"
# The clouds and the bridges stay; the diorite statue and the lighter go — the author replaced both.
layout["layers"] = [layer for layer in layout["layers"]
                    if not (layer.get("part_of") in ("statue", "lighter"))]
layout["themes"], layout["mapTheme"] = THEMES, "moor"
# The biome: forest, jungle, beach and birch forest in cells, which is what tints the leaves four ways.
layout["biome"] = {"kind": "cell", "seed": 8, "cellSize": 12, "jitter": 3, "palette": [4, 21, 16, 4, 27, 4, 21, 27]}

# ── the made things, cut out of the author's world ──────────────────────────────────────────────────
def model(name, drop=lambda x, y, z, i, d: False, recolour=None, turn=None):
    rows = json.load(open(f"{MODELS}/{name}.json"))
    out = {}
    for x, y, z, i, d in rows:
        if drop(x, y, z, i, d): continue
        if recolour: i, d = recolour(i, d)
        if turn: x, z = turn(x, z)
        out[(x, y, z)] = f"m-{i}-{d}"
    return out

def made(name, voxels, mirrors, seat=None):
    layers = compile_layers(voxels, prefix=name + "-", layer_prefix=f"{name}-L", mirrors=mirrors,
                            group_name=name, part_of=name, seat=seat)
    for key in {m for m in voxels.values()}:
        _, i, d = key.split("-"); THEMES[key] = flat(solid(int(i), int(d)))
    st = stats(voxels, layers)
    print(f"  {name:14} {st['blocks']:5} blocks  {st['layers']:2} layers  {st['shapes']:4} shapes")
    return layers

TEAM_SWAP = {(35, 14): (35, 11), (35, 11): (35, 14), (159, 14): (159, 11), (159, 11): (159, 14)}
def blue(i, d): return TEAM_SWAP.get((i, d), (i, d))

# The observer platform is the studio's own stamp at (0, 70, 0): the basket keeps its walls and gives up
# the six-by-six the platform and its boards stand in.
balloon = model("balloon", drop=lambda x, y, z, i, d: -3 <= x <= 2 and -3 <= z <= 2 and 67 <= y <= 71)
extra = []
extra += made("balloon", balloon, mirrors=False)
extra += made("statue-red", model("statue"), mirrors=False)
extra += made("statue-blue", model("statue", recolour=blue, turn=lambda x, z: (-x, -z)), mirrors=False)
extra += made("tug", model("boat"), mirrors=True)
extra += made("beacon-front", model("beacon"), mirrors=True)
extra += made("beacon-back", model("beacon", turn=lambda x, z: (x + 75, z + 80)), mirrors=True)
layout["layers"] += extra

# ── dressing ─────────────────────────────────────────────────────────────────────────────────────────
S0 = [[-132, 49], [-125, 35], [-82, 43], [-46, 30], [-15, 35], [-7, 54], [-15, 70], [-40, 62], [-90, 76], [-108, 73], [-125, 70]]
MOOR = [[-113, 95], [-108, 73], [-90, 76], [-40, 62], [1, 75], [13, 96], [5, 120], [-34, 131], [-68, 122], [-105, 120]]
WOLD = [[-122, 15], [-115, 0], [-89, -20], [-65, -2], [-33, 6], [-15, 35], [-46, 30], [-82, 43], [-125, 35]]
HOLM = [[-70, -75], [-30, -75], [-25, -45], [-45, -32], [-70, -45]]

STYLE = json.load(open(f"{ROOT}/tools/styles/17h-croft.json"))
def repaint(style, swap):
    def walk(n):
        if isinstance(n, dict):
            if n.get("kind") == "solid" and (n.get("id"), n.get("data", 0)) in swap:
                n["id"], n["data"] = swap[(n["id"], n.get("data", 0))]; return
            for v in n.values(): walk(v)
        elif isinstance(n, list):
            for v in n: walk(v)
    copy = json.loads(json.dumps(style)); walk(copy); return copy
VARIANT = repaint(STYLE, {(4, 0): (1, 5), (98, 0): (1, 0), (98, 1): (1, 5)})
layout["roomStyles"] = {"spawn": json.load(open(f"{ROOT}/tools/styles/showcase-hall.json"))}

styles = {}
for key, tree in BODIES.items():
    styles[key] = {"kind": "tree", "form": "copied", "body": tree["body"]}
styles["erratic"] = {"kind": "boulder", "form": "angular", "size": 6, "mossy": True,
                     "rock": noise([MOSSY, MOSSY, PRISMARINE, PRISMARINE, COBBLE, EMERALD_ORE, ANDESITE], 3, 51, rise=3)}
styles["bed-rock"] = {"kind": "boulder", "form": "round", "size": 5, "mossy": True,
                      "rock": noise([MOSSY, PRISMARINE, COBBLE, EMERALD_ORE], 3, 52, rise=3)}
styles["shelf"] = {"kind": "boulder", "form": "outcrop", "size": 7, "mossy": True,
                   "rock": noise([MOSSY, PRISMARINE, COBBLE, MOSSY, EMERALD_ORE], 3, 53, rise=3)}
styles["croft"] = {"kind": "house", "shell": STYLE}
styles["croft-grey"] = {"kind": "house", "shell": VARIANT}

def tree(pid, x, z, style): return {"id": pid, "kind": "tree", "seed": abs(x * 31 + z * 17) % 9973, "layer": "ground", "x": x, "z": z, "style": style}
def boulder(pid, x, z, style): return {"id": pid, "kind": "boulder", "seed": abs(x * 11 + z * 5) % 9973, "layer": "ground", "x": x, "z": z, "style": style}
def house(pid, x0, z0, x1, z1, style, front):
    return {"id": pid, "kind": "house", "seed": abs(x0 * 7 + z0 * 13) % 9973, "layer": "ground",
            "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}
def road(pid, points, seed):
    return {"id": pid, "kind": "stroke", "seed": seed, "layer": "ground", "points": points, "radius": 2.5,
            "style": "rough", "coverage": 0.8, "claimsGround": True,
            "pave": noise([GRANITE, POLISHED_GRANITE, JUNGLE_PLANK, GRANITE], 4, 60 + seed)}
def meadow(pid, ring, seed):
    return {"id": pid, "kind": "flora", "seed": seed, "layer": "ground", "points": ring,
            "spec": {"coverage": 0.92, "scale": 6, "octaves": 3, "fernShare": 0.5, "flowerShare": 0.02,
                     "flowerScale": 18, "tallShare": 0.03}}

# The trees stand where the author stood them, each wearing the showcase tree the author copied there.
OAKS = [(-62, 80, "oak-dense-2"), (-21, 83, "oak-dense-3"), (-106, 86, "oak-dense-1"), (-51, 112, "oak-dense-7"),
        (-40, 114, "oak-dense-6"), (-30, 117, "oak-dense-8"), (-16, 118, "oak-dense-4"), (-52, 122, "oak-dense-9"),
        (-39, 124, "oak-dense-5"), (-69, 88, "oak-dense-5")]
FIRS = [(-100, -7, "fir-tall-6"), (-63, 2, "fir-tall-5"), (-37, 9, "fir-small-5"), (-32, 18, "fir-small-4"),
        (-101, 28, "fir-tall-8"), (-86, 35, "fir-tall-7"), (-52, -67, "fir-tall-6"), (-35, -67, "fir-tall-7"),
        (-65, -43, "fir-small-1"), (-32, -36, "fir-small-2"), (-115, 7, "fir-small-2"), (-119, 30, "fir-small-1"),
        (-27, 27, "fir-small-5")]
# No rock stands in the race: the water prop claims its whole bed and the quay walls keep their band clear,
# so every boulder brushed into the bed by hand is a boulder the studio refuses (review/fable-millrace-revamp.md).
BOULDERS = [("erratic-round", -10, 80, "erratic"), ("erratic-broken", -76, 86, "erratic"), ("erratic-shelf", -56, 93, "shelf"),
            ("erratic-cairn", -6, 115, "bed-rock"), ("erratic-crag", -60, 12, "erratic"), ("erratic-cobble", -118, 23, "bed-rock"),
            ("erratic-ledge", -35, -54, "shelf"), ("erratic-stack", -66, -54, "bed-rock")]

props = [
    {"id": "race-water", "kind": "water", "seed": 7, "layer": "ground", "shape": "pool", "points": S0,
     "radius": 26, "depth": 10, "shore": 1, "shoreWander": False, "edge": 0.6, "level": 25, "bank": GRAVEL},
    # The spawn quarter: the crofts moved back and west, the way the author moved them, held to the studio's
    # footprint cap where the author's halls exceed it.
    house("croft-west", -108, 101, -97, 113, "croft", "posX"),
    house("croft-east", -81, 99, -70, 110, "croft-grey", "negZ"),
    house("hall-back", -90, 114, -75, 122, "croft", "negZ"),
    house("croft-fell", -93, -13, -86, -7, "croft", "posZ"),
    house("croft-bank", -37, 69, -27, 78, "croft-grey", "posZ"),
    # The roads, laid in the author's granite and jungle plank
    road("road-stair", [[-88, 82], [-75, 78], [-60, 70], [-50, 66]], 1),
    road("road-south", [[-50, 27], [-62, 21], [-74, 18]], 2),
    road("road-holm", [[-48, 6], [-48, -18], [-49, -32]], 3),
    road("road-island", [[-48, -44], [-44, -54]], 4),
    road("road-back", [[-82, 96], [-58, 100], [-34, 104], [-20, 96]], 5),
    meadow("meadow-moor", MOOR, 11), meadow("meadow-wold", WOLD, 12), meadow("meadow-holm", HOLM, 13),
]
props += [tree(f"oak-{n}", x, z, style) for n, (x, z, style) in enumerate(OAKS)]
props += [tree(f"fir-{n}", x, z, style) for n, (x, z, style) in enumerate(FIRS)]
props += [boulder(pid, x, z, style) for pid, x, z, style in BOULDERS]
layout["dressing"] = {"props": props, "styles": styles}

# ── the play ─────────────────────────────────────────────────────────────────────────────────────────
intent["maxPlayers"] = 56
intent["observer"] = {"point": {"x": 0, "y": 70, "z": 0}, "yaw": 0}
for spawn in intent["spawns"]:
    sign = 1 if spawn["team"] == "blue" else -1
    # The whole terrace is the author's protection; the studio holds a protection to 20 x 30, so this is the
    # hall and the ground in front of it.
    spawn["protection"] = [{"minX": min(sign * 100, sign * 80), "maxX": max(sign * 100, sign * 80),
                            "minZ": min(-sign * 96, -sign * 125), "maxZ": max(-sign * 96, -sign * 125)}]
    spawn["iron"] = [{"x": sign * 78, "z": -sign * 116}, {"x": sign * 82, "z": -sign * 116}]
intent.setdefault("meta", {}).update({
    "name": "Millrace", "created": "2026-09-02",
    "authors": [
        {"name": "rockymine", "uuid": "fe3608b7-d105-4029-8800-34b3147065b6", "contribution": "layout, terrain, block palette, beautification"},
        {"name": "Ruediger_LP", "uuid": "e2d2c2c6-cea9-4510-9ab2-a091b5605b30", "contribution": "interior design, houses, beautification"},
        {"name": "Opus 5", "contribution": "layout composition, initial draft, sculptures, bridges"},
        {"name": "Fable 5.1", "contribution": "the revamp restated in the studio"},
    ]})
plan["meta"]["name"] = "Millrace"
# The plan is re-planned from, so it states the current form: marker offsets in blocks from the piece corner.
if plan.get("plan", 1) < 2:
    cell_size = plan["globals"]["cell"]
    for group in plan["placements"].values():
        for marker in group:
            marker["at"] = [marker["at"][0] * cell_size, marker["at"][1] * cell_size]
    plan["plan"] = 2

json.dump(plan, open(OUT + ".plan.json", "w"), indent=1)
json.dump(layout, open(OUT + ".layout.json", "w"), indent=1)
json.dump(intent, open(OUT + ".intent.json", "w"), indent=1)
print(f"wrote {len(layout['layers'])} layers, {len(ground_layer['layout']['shapes'])} ground shapes, "
      f"{len(props)} props over {len(styles)} recipes")
