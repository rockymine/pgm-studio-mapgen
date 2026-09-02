"""Mossgill — one moor split by a beck in a gill, on half of Millrace's box, in Millrace's revamp palette.

A 130 × 120 destroy board, `rot_180`. Each team spawns on a crag in its own corner, walks down over a brow
onto an apron where its monument stands inside a low sheepfold, and the moor falls from there to a beck cut
through the middle on a shallow diagonal, crossed once by a plank bridge between two quays. Everything the
Millrace revamp taught is in the finish: the six-stone body as a volume of cells wider than tall, three
courses of earth as a volume, the author's copied trees, granite roads, ferns on the grass, four biomes.

    python3 specs/fable-mossgill/build.py
    python3 tools/drive.py specs/fable-mossgill "Mossgill" --out maps/fable-mossgill
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BODIES = json.load(open(f"{ROOT}/specs/fable-millrace-revamp/trees.json"))

# ── the plan ──────────────────────────────────────────────────────────────────────────────────────────
GOAL = [-29, -28]
plan = {
    "plan": 2,
    "meta": {"name": "Mossgill"},
    "globals": {"cell": 5, "symmetry": "rot_180", "maxPlayers": 24, "surface": 14},
    "pieces": [
        {"id": "crag", "role": "spawn", "rect": [-13, -12, 4, 4], "surface": 27},
        {"id": "brow", "role": "piece", "rect": [-9, -12, 5, 4], "surface": 22},
        {"id": "apron", "role": "piece", "rect": [-13, -8, 11, 4], "surface": 20},
        {"id": "bank", "role": "piece", "rect": [-13, -4, 13, 4], "surface": 14},
        {"id": "shoulder", "role": "piece", "rect": [0, -4, 9, 4], "surface": 14},
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "crag", "at": [10, 10], "facing": "right"}],
        "wools": [], "iron": [], "cores": [],
        "destroyables": [{"id": "destroyable-1", "at": GOAL, "style": "pillar-3",
                          "materials": "obsidian", "float": 4, "name": "Fold Monument"}],
    },
    "walls": [], "boxes": [],
}

# ── materials ─────────────────────────────────────────────────────────────────────────────────────────
def solid(b, d=0): return {"kind": "solid", "id": b, "data": d}
def noise(stops, scale, seed, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 3, "stops": stops, "rise": rise}
def turb(stops, scale, seed, rise=0):
    return {"kind": "turbulence", "seed": seed, "scale": scale, "octaves": 3, "stops": stops, "rise": rise}
def cell(palette, size, seed, jitter=2, warp=1, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp, "palette": palette, "rise": rise}
def layered(bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"bands": [{"material": m, "thickness": t} for m, t in bands], "ending": "handOver"}}
def voronoi(bands, size, seed):
    return {"kind": "voronoi", "seed": seed, "cellSize": size, "rise": 0,
            "bands": [{"material": m, "depth": d} for m, d in bands]}

STONE, ANDESITE, POLISHED, COBBLE, MOSSY = solid(1), solid(1, 5), solid(1, 6), solid(4), solid(48)
EMERALD_ORE, CYAN_CLAY, PRISMARINE, GRAVEL, SAND = solid(129), solid(159, 9), solid(168), solid(13), solid(12)
GRASS, DIRT, COARSE, PODZOL, SPRUCE_PLANK = solid(2), solid(3), solid(3, 1), solid(3, 2), solid(5, 1)
GRANITE, POLISHED_GRANITE, JUNGLE_PLANK = solid(1, 1), solid(1, 2), solid(5, 3)
DSLAB, SMOOTH_DSLAB, LIGHT_GRAY_WOOL = solid(43), solid(43, 8), solid(35, 8)
PLANK_S, PLANK_D = solid(5, 1), solid(5, 5)

# The six-stone body: cells nine across and four tall, each a turbulent mix. A pattern is a plane until it
# states a rise (TP15), and a cell as tall as it is wide reads as a column on a cut; the author's blobs are
# wider than tall, so the cells are.
BODY = cell([
    turb([ANDESITE, POLISHED], 6, 71, rise=3),
    turb([STONE, ANDESITE], 6, 72, rise=3),
    turb([MOSSY, STONE, MOSSY], 6, 73, rise=3),
    cell([EMERALD_ORE, POLISHED, MOSSY, ANDESITE], 5, 74, rise=3),
    cell([CYAN_CLAY, STONE, ANDESITE], 5, 75, rise=3),
    turb([POLISHED, MOSSY], 6, 76, rise=3),
], 9, 70, rise=4)
EARTH = noise([COARSE, COARSE, COARSE, SPRUCE_PLANK, SPRUCE_PLANK, DIRT], 4, 80, rise=6)
BANK_TOP = noise([GRASS, GRASS, GRASS, COARSE, GRASS, DIRT, COARSE, PODZOL], 4, 81)
APRON_TOP = noise([GRASS, GRASS, COARSE, GRASS, GRASS, PODZOL, DIRT, GRASS], 4, 82)
BROW_TOP = noise([COARSE, PODZOL, COARSE, GRASS, DIRT, COARSE, PODZOL], 4, 83)
CRAG_TOP = noise([PODZOL, COARSE, PODZOL, COARSE, DIRT, GRASS, COARSE], 4, 84)
BED_TOP = noise([COARSE, SPRUCE_PLANK, COARSE, GRAVEL, SPRUCE_PLANK, MOSSY, ANDESITE, PRISMARINE], 4, 85)
QUAY = cell([DSLAB, DSLAB, SMOOTH_DSLAB, LIGHT_GRAY_WOOL, DSLAB], 4, 90, rise=4)

def theme(surface, wall, fill, depth):
    return {"bedrock": {"relative": False, "value": 1}, "wallOnTerrainFaces": False,
            "surface": {"enabled": True, "depth": depth, "material": surface},
            "wall": wall, "wallEnabled": True, "fill": fill,
            "rim": {"enabled": False, "depth": 1, "material": STONE}, "rimEdges": "boundary"}
def ground(top): return theme(layered([(top, 1), (EARTH, 3)]), BODY, BODY, 4)
def flat(b): return theme(b, b, b, 1)

THEMES = {
    "bank": ground(BANK_TOP), "apron": ground(APRON_TOP), "brow": ground(BROW_TOP), "crag": ground(CRAG_TOP),
    "bed": theme(layered([(BED_TOP, 1), (EARTH, 2)]), BODY, BODY, 3),
    "quay": theme(QUAY, QUAY, QUAY, 1), "timber": flat(PLANK_S), "dark-timber": flat(PLANK_D),
}

# ── the ground: the beck's line, its lips, the fold, the quays and the bridge ─────────────────────────
def beck_z(x): return x * 0.125                 # the beck runs from (-64, -8) to (64, 8), through the centre
BECK = [[x, round(beck_z(x), 1)] for x in range(-64, 65, 8)]
def lip(offset, x0, x1, step=8):
    return [[x, round(beck_z(x) + offset, 1)] for x in range(x0, x1 + 1, step)]

def path_shape(sid, pts, radius, floor, height, th, seed=7, level=True, keep=True):
    shape = {"id": sid, "type": "path", "operation": "add", "override": True, "keepClear": keep,
             "vertices": pts, "radius": radius, "path_edge": "solid", "path_seed": seed,
             "floor": floor, "base_height": height, "skirt": 0, "relief_scope": "exclude", "theme": th}
    if level: shape["height_mode"] = "level"
    return shape

def arc(cx, cz, r, a0, a1, step=10):
    return [[round(cx + r * math.cos(math.radians(a)), 1), round(cz + r * math.sin(math.radians(a)), 1)]
            for a in range(a0, a1 + 1, step)]

# A strip along the beck the width of its gill, at the bank's own height: no geometry of its own, only the
# bed theme scoped to it — the smaller shape wins a contested cell's paint.
BED_RING = [[x, round(beck_z(x) - 7, 1)] for x in range(-66, 67, 11)] + \
           [[x, round(beck_z(x) + 7, 1)] for x in range(66, -67, -11)]
add_shapes = [
    {"id": "beck-bed", "type": "polygon", "operation": "add", "override": False, "keepClear": False,
     "vertices": BED_RING, "floor": 0, "base_height": 14, "theme": "bed"},
    # The sheepfold: two arcs of quay wall round the monument, open east and west, two courses over the apron.
    path_shape("fold-n", arc(GOAL[0], GOAL[1], 6, 200, 340), 1.0, 19, 3, "quay", seed=11),
    path_shape("fold-s", arc(GOAL[0], GOAL[1], 6, 20, 160), 1.0, 19, 3, "quay", seed=12),
    # The quays: a parapet along each lip of the beck at the crossing, one course over the bank.
    path_shape("quay-n", lip(-6, -16, 16, 8), 1.0, 8, 7, "quay", seed=13),
]

# The plank bridge, on its own layer over the beck: its own image, so it does not mirror.
bridge = {"id": "spans", "name": "spans", "base_y": 0, "layout": {
    "shapes": [
        {"id": "deck", "type": "rectangle", "operation": "add", "override": True, "keepClear": True,
         "min_x": -3, "max_x": 3, "min_z": -9, "max_z": 9, "floor": 13, "base_height": 1,
         "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "theme": "timber"},
        {"id": "rail-w", "type": "rectangle", "operation": "add", "override": True, "keepClear": True,
         "min_x": -4, "max_x": -3, "min_z": -9, "max_z": 9, "floor": 13, "base_height": 2,
         "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "theme": "dark-timber"},
        {"id": "rail-e", "type": "rectangle", "operation": "add", "override": True, "keepClear": True,
         "min_x": 3, "max_x": 4, "min_z": -9, "max_z": 9, "floor": 13, "base_height": 2,
         "height_mode": "level", "skirt": 0, "relief_scope": "exclude", "theme": "dark-timber"},
    ],
    "groups": [{"id": "spans-body", "name": "spans", "mirrors": False, "shapeIds": ["deck", "rail-w", "rail-e"]}]}}

def ring(cx, cz, rx, rz, n=9):
    return [[round(cx + rx * math.cos(2 * math.pi * i / n)), round(cz + rz * math.sin(2 * math.pi * i / n))]
            for i in range(n)]

relief = {"team": {
    "base": 14, "reach": 18, "step": 1, "stairs": True, "landform": "moor",
    "grain": {"amplitude": 1.0, "scale": 16, "seed": 5},
    "marks": [
        {"id": "apron", "kind": "area", "h": 20, "ring": [[-66, -41], [-9, -41], [-9, -19], [-66, -19]]},
        {"id": "brow", "kind": "area", "h": 22, "ring": [[-46, -61], [-19, -61], [-19, -39], [-46, -39]]},
        {"id": "crag", "kind": "area", "h": 27, "ring": [[-66, -61], [-44, -61], [-44, -39], [-66, -39]]},
        # the beck: a gill cut eight courses into the bank, sheer on both lips
        {"id": "beck", "kind": "line", "width": 9, "points": BECK, "h": [6] * len(BECK)},
        {"id": "lip-n", "kind": "scarp", "points": lip(-6, -60, 60, 12), "high": 14, "low": 7, "face": 3, "band": 5},
    ],
    "pushes": [
        {"id": "knoll", "ring": ring(-30, -11, 13, 6), "amount": 4, "falloff": 10, "roughness": 0.4, "crown": 2, "seed": 7},
        {"id": "moss-bank", "ring": ring(-58, -30, 8, 9), "amount": 3, "falloff": 9, "roughness": 0.35, "crown": 2, "seed": 8},
        {"id": "shoulder-rise", "ring": ring(30, -12, 12, 6), "amount": 3, "falloff": 9, "roughness": 0.4, "crown": 2, "seed": 9},
    ],
}}

# ── dressing ──────────────────────────────────────────────────────────────────────────────────────────
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

styles = {key: {"kind": "tree", "form": "copied", "body": tree["body"]} for key, tree in BODIES.items()}
styles["erratic"] = {"kind": "boulder", "form": "angular", "size": 5, "mossy": True,
                     "rock": noise([MOSSY, MOSSY, PRISMARINE, PRISMARINE, COBBLE, EMERALD_ORE, ANDESITE], 3, 51, rise=3)}
styles["shelf"] = {"kind": "boulder", "form": "outcrop", "size": 6, "mossy": True,
                   "rock": noise([MOSSY, PRISMARINE, COBBLE, MOSSY, EMERALD_ORE], 3, 53, rise=3)}
styles["croft"] = {"kind": "house", "shell": STYLE}
styles["croft-grey"] = {"kind": "house", "shell": VARIANT}

def tree(pid, x, z, style): return {"id": pid, "kind": "tree", "seed": abs(x * 31 + z * 17) % 9973, "x": x, "z": z, "style": style}
def boulder(pid, x, z, style): return {"id": pid, "kind": "boulder", "seed": abs(x * 11 + z * 5) % 9973, "x": x, "z": z, "style": style}
def house(pid, x0, z0, x1, z1, style, front):
    return {"id": pid, "kind": "house", "seed": abs(x0 * 7 + z0 * 13) % 9973,
            "wings": [{"corners": [[x0, z0], [x1, z1]]}], "front": front, "style": style}
def road(pid, points, seed):
    return {"id": pid, "kind": "stroke", "seed": seed, "points": points, "radius": 2.5, "style": "rough",
            "coverage": 0.8, "route": True, "pave": noise([GRANITE, POLISHED_GRANITE, JUNGLE_PLANK, GRANITE], 4, 60 + seed)}
def meadow(pid, ring_, seed):
    return {"id": pid, "kind": "flora", "seed": seed, "points": ring_,
            "spec": {"coverage": 0.88, "scale": 6, "octaves": 3, "fernShare": 0.5, "flowerShare": 0.03,
                     "flowerScale": 18, "tallShare": 0.03}}

# Every prop keeps 21 blocks off the monument (OB19) and off the spawn's own ground.
TREES = [
    # the crag and the brow: the tall acacia-and-birch conifers on earth
    (-61, -58, "fir-tall-5"), (-48, -59, "fir-tall-7"), (-38, -57, "fir-tall-6"), (-24, -55, "fir-tall-8"),
    (-22, -45, "fir-tall-5"), (-42, -43, "fir-small-4"),
    # the apron ends and the bank: the dense oaks on grass
    (-62, -23, "oak-dense-2"), (-8, -22, "oak-dense-4"), (-4, -36, "oak-dense-7"),
    (-42, -8, "oak-dense-1"), (-24, -5, "oak-dense-3"), (-58, -9, "oak-dense-5"),
    # the shoulder across the beck
    (12, -15, "oak-dense-6"), (28, -7, "oak-dense-9"), (41, -16, "oak-dense-8"),
    # small firs along the gill's lips
    (-13, -17, "fir-small-1"), (22, -18, "fir-small-2"), (38, -6, "fir-small-5"), (-52, -18, "fir-small-4"),
]
BOULDERS = [("stone-1", -20, -13, "erratic"), ("stone-2", 18, -6, "shelf"), ("stone-3", -62, -3, "erratic"),
            ("stone-4", 40, -11, "erratic"), ("stone-5", -63, -33, "shelf")]
props = [
    {"id": "beck", "kind": "water", "seed": 1, "shape": "channel", "form": "natural", "radius": 4, "depth": 2,
     "edge": 0.8, "shore": 2, "shoreWander": True, "points": BECK,
     "bank": voronoi([(GRAVEL, 1), (COARSE, 1), (SAND, 1)], 5, 6)},
    house("bothy", -64, -39, -55, -31, "croft", "posX"),
    house("barn", -54, -16, -45, -9, "croft-grey", "negZ"),
    road("road-crag", [[-44, -50], [-35, -47], [-32, -40], [-36, -34]], 1),
    road("road-beck", [[-26, -25], [-16, -15], [-5, -10], [0, -8]], 2),
    road("road-bank", [[-34, -22], [-46, -18], [-56, -12], [-62, -6]], 3),
    meadow("meadow-apron", [[-66, -41], [-9, -41], [-9, -19], [-66, -19]], 11),
    meadow("meadow-bank", [[-66, -21], [46, -21], [46, -6], [-66, -6]], 12),
    meadow("meadow-brow", [[-46, -61], [-19, -61], [-19, -39], [-46, -39]], 13),
]
props += [tree(f"tree-{n}", x, z, style) for n, (x, z, style) in enumerate(TREES)]
props += [boulder(pid, x, z, style) for pid, x, z, style in BOULDERS]

finish = {
    "themeByHeight": {"14": "bank", "20": "apron", "22": "brow", "27": "crag"},
    "bendShapes": {"s0": {"k": 0.2, "wander": 3, "step": 9, "seed": 5}, "s1": {"k": 0.18, "wander": 2, "step": 9, "seed": 6}},
    "addShapes": add_shapes,
    "addLayers": [bridge],
    "relief": relief,
    "themes": THEMES, "mapTheme": "bank",
    "biome": {"kind": "cell", "seed": 8, "cellSize": 12, "jitter": 3, "palette": [4, 21, 16, 4, 27, 4, 21, 27]},
    "roomStyles": {"spawn": "@17h-hall"},
    "dressing": {"props": props, "styles": styles},
    "authors": [
        {"name": "Fable 5.1", "contribution": "layout, terrain, roads, composition"},
        {"name": "rockymine", "uuid": "fe3608b7-d105-4029-8800-34b3147065b6", "contribution": "the trees, and the palette the map is themed in"},
    ],
    "created": "2026-09-02",
}
json.dump(plan, open(f"{HERE}/fable-mossgill.plan.json", "w"), indent=1)
json.dump(finish, open(f"{HERE}/fable-mossgill.finish.json", "w"), indent=1)
print(f"wrote the plan ({len(plan['pieces'])} pieces) and the finish ({len(props)} props over {len(styles)} recipes, "
      f"{len(add_shapes)} added shapes, {len(relief['team']['marks'])} marks, {len(relief['team']['pushes'])} pushes)")
