#!/usr/bin/env python3
"""Slatefold — a capture-the-wool board for two teams of twelve: a slate-quarrying hamlet on two terraced
hillsides that face each other across the void. Written for the experiment (exp-slatefold-studio).

Unit = team 0 on the north (z < 0); rot_180 fans the south hillside. Terraces from the void back, across the
whole width: yard 14 (a flooded quarry at the front)  ->  mid 22 (the two wool rooms at its two ends, a minehead
between)  ->  upper 30 (spawn, hall, cottages, the headframe).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "exp-slatefold-studio"
C = 4  # blocks per cell


def cells(x0, z0, x1, z1):
    assert all(v % C == 0 for v in (x0, z0, x1, z1)), (x0, z0, x1, z1)
    return [x0 // C, z0 // C, (x1 - x0) // C, (z1 - z0) // C]


X0, X1, Z0, Z1 = -48, 48, -112, -16
YARD, MID, UPPER, BENCH, SLOPE = 14, 22, 30, 40, 26

ROOMS = {
    "spawn":   ("spawn",     (-16, -112, 12, -92), UPPER),
    "kiln":    ("wool-room", (-48, -80, -28, -60), MID),
    "winding": ("wool-room", (32, -80, 48, -56), MID),
}


def surface_at(x, z):
    """The height the plan states for the ground at a cell: the tier it belongs to."""
    return UPPER if z < -88 else MID if z < -52 else YARD


def tile(bounds, holes):
    x0, z0, x1, z1 = bounds
    grid = {}
    for z in range(z0, z1, C):
        for x in range(x0, x1, C):
            if not any(h[0] <= x < h[2] and h[1] <= z < h[3] for h in holes):
                grid[(x, z)] = surface_at(x, z)
    used, out = set(), []
    for z in range(z0, z1, C):
        for x in range(x0, x1, C):
            if (x, z) in grid and (x, z) not in used:
                v = grid[(x, z)]
                xe = x
                while (xe + C, z) in grid and (xe + C, z) not in used and grid[(xe + C, z)] == v:
                    xe += C
                ze = z
                while all((xx, ze + C) in grid and (xx, ze + C) not in used and grid[(xx, ze + C)] == v
                          for xx in range(x, xe + C, C)):
                    ze += C
                for zz in range(z, ze + C, C):
                    for xx in range(x, xe + C, C):
                        used.add((xx, zz))
                out.append(((x, z, xe + C, ze + C), v))
    return out


pieces = []
for pid, (role, r, surf) in ROOMS.items():
    pieces.append({"id": pid, "role": role, "rect": cells(*r), "surface": surf})
for i, (r, v) in enumerate(tile((X0, Z0, X1, Z1), [r for _, r, _ in ROOMS.values()])):
    pieces.append({"id": f"ground-{i + 1}", "role": "piece", "rect": cells(*r), "surface": v})

plan = {
    "plan": 2,
    "meta": {"name": "Slatefold"},
    "globals": {"cell": C, "symmetry": "rot_180", "maxPlayers": 12, "surface": MID},
    "pieces": pieces,
    "zones": [{"id": "strait", "rect": cells(-40, -16, 40, 16)}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn", "at": [16, 8], "facing": "back",
                    "footprint": [7, 1, 20, 15]}],
        "iron": [{"id": "iron-1", "piece": "spawn", "at": [1.5, 4.5]}],
        "wools": [{"id": "wool-kiln", "piece": "kiln", "at": [10, 10], "footprint": [3, 3, 14, 14]},
                  {"id": "wool-winding", "piece": "winding", "at": [8, 12], "footprint": [3, 7, 10, 10]}],
    },
}


# ── materials ────────────────────────────────────────────────────────────────────────
import sys
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import showcase  # noqa: E402

TREES = showcase.trees()


def S(i, d=0):
    return {"kind": "solid", "id": i, "data": d}


STONE, ANDESITE, POLISHED, COBBLE, MOSSY = S(1), S(1, 5), S(1, 6), S(4), S(48)
GRASS, DIRT, COARSE, GRAVEL = S(2), S(3), S(3, 1), S(13)


def cell(seed, size, palette, jitter=60, warp=3, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp,
            "palette": palette, "rise": rise}


def noise(seed, scale, stops, octaves=2, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops, "rise": rise}


def depth_stack(*bands):
    return {"kind": "layered", "axis": "depth",
            "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def slope_stack(*bands):
    return {"kind": "layered", "axis": "slope",
            "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}


def strata():
    """Slate beds that follow the land: dark andesite and stone beds, a thin cobble bed."""
    beds = [(ANDESITE, 3), (STONE, 2), (POLISHED, 1), (ANDESITE, 2), (STONE, 3), (POLISHED, 2), (ANDESITE, 1),
            (STONE, 1), (COBBLE, 1), (ANDESITE, 3), (STONE, 2), (POLISHED, 1)]
    return {"kind": "layered", "axis": "height", "from": -10, "follow": 100, "reach": 16, "beyond": STONE,
            "stack": {"ending": "handOver", "bands": [{"material": m, "thickness": t} for m, t in beds]}}


ROCK = cell(11, 4, [STONE, ANDESITE, POLISHED, STONE, COBBLE, ANDESITE], jitter=70, warp=4)
FLOOR = cell(12, 3, [ANDESITE, STONE, POLISHED, GRAVEL, ANDESITE, STONE], jitter=60, warp=3)
TIPS = cell(16, 3, [STONE, ANDESITE, POLISHED, STONE, GRAVEL, COBBLE], jitter=80, warp=3)
HARD_PATH = cell(17, 3, [GRAVEL, ANDESITE, COBBLE], jitter=40, warp=2)

# grass to 36 degrees, a worn shoulder of dirt and coarse dirt to 46, then slate
HILL_TOP = slope_stack(
    (depth_stack((GRASS, 1), (DIRT, 2)), 32),
    (depth_stack((cell(13, 3, [DIRT, COARSE, DIRT, COARSE]), 1), (DIRT, 2)), 8),
    (ROCK, 50))


def theme(top, depth=3, rim=True):
    return {
        "rimEdges": "void",
        "rim": {"material": cell(14, 3, [ANDESITE, STONE, POLISHED]), "depth": 1, "enabled": rim},
        "surface": {"material": top, "depth": depth, "enabled": True},
        "wall": strata(), "wallEnabled": True,
        "fill": strata(),
    }


themes = {
    "hill": theme(HILL_TOP),
    "quarry": theme(FLOOR, 2),
    "spoil": theme(TIPS, 3),
    "moss": theme(slope_stack(
        (depth_stack((noise(18, 3, [MOSSY, GRASS, GRASS, MOSSY]), 1), (DIRT, 2)), 32),
        (depth_stack((cell(13, 3, [DIRT, COARSE, DIRT, COARSE]), 1), (DIRT, 2)), 8),
        (ROCK, 50))),
}


# ── relief ───────────────────────────────────────────────────────────────────────────
def rect_ring(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def blob(cx, cz, rx, rz, n=10, turn=0.0):
    import math
    return [[round(cx + rx * math.cos(2 * math.pi * k / n + turn), 1),
             round(cz + rz * math.sin(2 * math.pi * k / n + turn), 1)] for k in range(n)]


def grown(ring, by):
    import math
    cx = sum(p[0] for p in ring) / len(ring)
    cz = sum(p[1] for p in ring) / len(ring)
    return [[round(x + (x - cx) / math.hypot(x - cx, z - cz) * by), round(z + (z - cz) / math.hypot(x - cx, z - cz) * by)]
            for x, z in ring]


PIT = blob(-3, -31, 14, 7, 14, 0.2)


marks = [
    {"id": "yard", "kind": "area", "ring": rect_ring(-48, -46, 48, -16), "h": YARD},
    # the flooded quarry: a hollow with its bank, the water standing in it (a fluid prop of the same outline grown by the bank)
    {"id": "pit", "kind": "area", "ring": PIT, "h": 8, "bevel": 4},
    {"id": "upper", "kind": "area", "ring": rect_ring(-48, -112, 48, -88), "h": UPPER},
    {"id": "s-upper-mid", "kind": "scarp", "points": [[48, -84], [-48, -84]], "high": UPPER, "low": MID,
     "face": 4, "band": 4},
    {"id": "mid", "kind": "area", "ring": rect_ring(-48, -80, 48, -56), "h": MID},
    {"id": "s-mid-yard", "kind": "scarp", "points": [[48, -52], [-48, -52]], "high": MID, "low": YARD,
     "face": 4, "band": 4},
    # the cart ramps that cross the banks: one pair in the middle, one pair to the winding house's end
    {"id": "ramp-yard-mid", "kind": "line", "r": 4, "tread": 2, "points": [[-4, -44], [-4, -60]], "h": [YARD, MID]},
    {"id": "ramp-yard-mid-e", "kind": "line", "r": 4, "tread": 2, "points": [[26, -44], [26, -60]], "h": [YARD, MID]},
    {"id": "ramp-mid-upper-w", "kind": "line", "r": 4, "tread": 2, "points": [[-16, -78], [-16, -94]],
     "h": [MID, UPPER]},
    {"id": "ramp-mid-upper-e", "kind": "line", "r": 4, "tread": 2, "points": [[26, -78], [26, -94]],
     "h": [MID, UPPER]},
]
relief = {"team": {"base": YARD, "reach": 30, "marks": marks, "pushes": []}}


# ── added ground: worn quarry floor, spoil tips ──────────────────────────────────────
def poly(sid, pts, **fields):
    return {"id": sid, "type": "polygon", "operation": "add", "vertices": pts, "floor": 0, "layer": "ground",
            "group": "team", **fields}


def rectpoly(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


shapes = [
    poly("quarry-floor", blob(-3, -31, 22, 12, 14), base_height=1, theme="quarry"),
    poly("tip-1", blob(-26, -22, 6, 5, 9, 0.3), base_height=5, height_mode="raise", skirt=4, theme="spoil"),
    poly("tip-2", blob(20, -42, 7, 5, 9, 0.9), base_height=6, height_mode="raise", skirt=4, theme="spoil"),
    poly("tip-3", blob(38, -44, 5, 4, 8, 0.1), base_height=4, height_mode="raise", skirt=3, theme="spoil"),
    # the landing stage: ground out over the void where the bridge starts, at the middle of the zone
    poly("pier", rectpoly(-4, -17, 4, -11), base_height=YARD, theme="quarry"),
    # moss on the benches
    poly("moss-upper", blob(-46, -88, 3, 3, 9, 0.2), base_height=1, height_mode="sink", theme="moss"),
    poly("moss-bench", blob(22, -95, 6, 5, 9, 0.5), base_height=1, height_mode="sink", theme="moss"),
    poly("moss-mid", blob(-22, -66, 8, 4, 10, 0.4), base_height=1, height_mode="sink", theme="moss"),
]


# ── made things: the headframe over the winding house, the kiln stack, the posts that mark the build zone ──
def box(sid, x0, z0, x1, z1, floor, height, material):
    return {"id": sid, "type": "rectangle", "operation": "add", "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1,
            "floor": floor, "base_height": height, "material": material}


LOG = S(162, 1)
PLANK = S(5, 5)
BRICK = S(45)
SBRICK = S(98)
GLOW = S(89)


def made_layer(layer_id, part, base_y, shapes_):
    """One slab of a made thing: a layer keeps one span a column, so a post and the beam on its top are two."""
    return {"id": layer_id, "name": layer_id, "base_y": base_y, "kind": "made", "part_of": part, "seat": "ground",
            "shapes": shapes_, "groups": [{"id": layer_id, "name": layer_id, "mirrors": True,
                                           "shapeIds": [x["id"] for x in shapes_]}]}


def ring(sid, x0, z0, x1, z1, material, floor=0):
    return [box(f"{sid}-n", x0, z0, x1, z0 + 1, floor, 1, material), box(f"{sid}-s", x0, z1 - 1, x1, z1, floor, 1, material),
            box(f"{sid}-w", x0, z0 + 1, x0 + 1, z1 - 1, floor, 1, material),
            box(f"{sid}-e", x1 - 1, z0 + 1, x1, z1 - 1, floor, 1, material)]


HX, HZ = 40, -110  # the headframe's north-west corner
posts = [box(f"hf-post-{i}", HX + dx, HZ + dz, HX + dx + 2, HZ + dz + 2, 0, 13, LOG)
         for i, (dx, dz) in enumerate([(0, 0), (4, 0), (0, 4), (4, 4)])]
layers = [
    made_layer("hf-posts", "headframe", 0, posts),
    made_layer("hf-low", "headframe", 6, ring("hf-low", HX, HZ, HX + 6, HZ + 6, PLANK)),
    made_layer("hf-top", "headframe", 13, ring("hf-top", HX, HZ, HX + 6, HZ + 6, PLANK)),
    made_layer("hf-sheave", "headframe", 14, [box("hf-sheave", HX + 2, HZ + 2, HX + 4, HZ + 4, 0, 2, SBRICK)]),
    made_layer("stack", "kiln-stack", 0, [box("stack-shaft", -26, -59, -23, -56, 0, 16, BRICK)]),
]
def disc(sid, cx, cz, r, floor, height, material):
    return {"id": sid, "type": "circle", "operation": "add", "center_x": cx, "center_z": cz, "radius": r,
            "floor": floor, "base_height": height, "material": material}


for k, (cx, cz) in enumerate([(-24, -69), (-9, -68)]):
    layers += [made_layer(f"bottle-{k}-a", f"bottle-{k}", 0, [disc(f"bottle-{k}-a", cx, cz, 3.5, 0, 5, BRICK)]),
               made_layer(f"bottle-{k}-b", f"bottle-{k}", 5, [disc(f"bottle-{k}-b", cx, cz, 3, 0, 4, BRICK)]),
               made_layer(f"bottle-{k}-c", f"bottle-{k}", 9, [disc(f"bottle-{k}-c", cx, cz, 2, 0, 3, SBRICK)])]
for i, (px, pz) in enumerate([(-42, -19), (40, -19)]):
    layers += [made_layer(f"lip-post-{i}", f"lip-{i}", 0, [box(f"lip-{i}-post", px, pz, px + 2, pz + 2, 0, 7, LOG)]),
               made_layer(f"lip-lamp-{i}", f"lip-{i}", 7, [box(f"lip-{i}-lamp", px, pz, px + 2, pz + 2, 0, 1, GLOW)])]

# ── dressing ─────────────────────────────────────────────────────────────────────────
SPRUCE = TREES["tiny-spruce-3"]["style"]
SPRUCE2 = TREES["tiny-spruce-1"]["style"]
BIRCH = TREES["birch-9"]["style"]
ROCKSTYLE = {"kind": "boulder", "form": "angular", "size": 4, "rock": cell(53, 4, [STONE, ANDESITE, COBBLE, STONE], 2, 3),
             "mossy": False}
OUTCROP = {"kind": "boulder", "form": "outcrop", "size": 5, "rock": cell(54, 4, [STONE, ANDESITE, COBBLE, STONE], 2, 3),
           "mossy": False}

styles = {
    "spruce": SPRUCE, "spruce-b": SPRUCE2, "birch": BIRCH, "rock": ROCKSTYLE, "outcrop": OUTCROP,
    "cottage": {"library": "dark-oak-roofed-stone-cottage", "kind": "house"},
    "cottage-b": {"library": "spruce-roofed-stone-cottage", "kind": "house"},
    "rubble": {"library": "rubble-and-spruce-house", "kind": "house"},
    "minehead": {"library": "stone-timber-minehead", "kind": "house"},
    "barn": {"library": "stone-and-spruce-barn", "kind": "house"},
    "longhouse": {"library": "spruce-roofed-stone-longhouse", "kind": "house"},
}


def house(pid, style, x0, z0, x1, z1, front="posZ", ridge=None):
    spec = {"ridge": ridge} if ridge else {}
    return {"id": pid, "kind": "house", "layer": "ground", "seed": 5, "front": front, "style": style,
            "wings": [{"corners": [[x0, z0], [x1, z1]], "spec": spec}]}


def stroke(pid, pts, radius=2, wander=1.5, claims=True):
    return {"id": pid, "kind": "stroke", "layer": "ground", "seed": 3, "points": pts, "radius": radius,
            "style": "solid", "pave": HARD_PATH, "claimsGround": claims, "wander": wander, "wanderLength": 14}


def tree(pid, style, x, z):
    return {"id": pid, "kind": "tree", "layer": "ground", "seed": 7, "x": x, "z": z, "style": style}


def boulder(pid, style, x, z):
    return {"id": pid, "kind": "boulder", "layer": "ground", "seed": 9, "x": x, "z": z, "style": style}


props = [
    # the cart road and the lanes (circulation before scenery)
    stroke("road-lip-pit", [[0, -13], [0, -21], [20, -24], [20, -38], [8, -47], [-4, -47], [-4, -60]], 2),
    stroke("road-yard-e", [[20, -38], [24, -42], [26, -44], [26, -60]], 2),
    stroke("lane-mid", [[-30, -62], [-4, -62], [10, -62], [26, -62], [34, -62]], 2),
    stroke("road-upper", [[-16, -62], [-16, -80], [-16, -94], [-14, -98]], 2),
    stroke("road-upper-e", [[26, -62], [26, -80], [26, -94], [30, -98]], 2),
    stroke("road-tarn", [[-16, -94], [-24, -98], [-33, -97], [-40, -101]], 2),
    stroke("road-headframe", [[30, -98], [40, -100], [44, -104]], 2, 0.5),
    # the minehead on the mid terrace between the wool rooms; the cottages on the upper terrace beside the spawn
    house("mine", "minehead", -2, -71, 10, -65),
    house("cot-1", "cottage", 22, -110, 30, -104),
    house("cot-2", "cottage-b", -43, -42, -35, -36),
    house("shed-1", "barn", 26, -34, 38, -26),
    house("hall", "barn", -47, -111, -37, -103),
    # trees: two species, a few, to the outside
    tree("t3", "birch", 40, -93),
    tree("t4", "spruce", 46, -34), tree("t5", "birch", 42, -22), tree("t6", "spruce-b", -45, -90),
    # rock
    boulder("b1", "rock", -40, -93), boulder("b3", "rock", -22, -49),
    {"id": "quarry-lake", "kind": "fluid", "layer": "ground", "seed": 5, "shape": "basin", "level": 11,
     "points": grown(PIT, 4), "radius": 2, "depth": 3, "fluid": "water", "shore": 1},
    {"id": "tarn", "kind": "fluid", "layer": "ground", "seed": 4, "shape": "pool", "points": blob(-36, -94, 4, 3, 10),
     "radius": 2, "depth": 3, "fluid": "water", "shore": 2},
    
    {"id": "cover", "kind": "flora", "layer": "ground", "seed": 11,
     "points": [[-48, -112], [48, -112], [48, -16], [-48, -16]],
     "spec": {"coverage": 0.22, "scale": 9, "octaves": 2, "fernShare": 0.2, "flowerShare": 0.12,
              "flowerScale": 6, "tallShare": 0.04}},
]

refinement = {
    "created": "2026-10-10",
    "authors": [{"name": "Sonnet 5.5", "contribution": "Plan, ground, paint, dressing"}],
    "themes": themes, "mapTheme": "hill",
    "relief": relief,
    "addShapes": shapes,
    "addLayers": layers,
    "biome": {"kind": "solid", "biome": 3},
    "roomStyles": {"wool": {"library": "brick-townhouse"}, "spawn": {"library": "spruce-roofed-stone-longhouse"}},
    "dressing": {"styles": styles, "props": props},
}

if __name__ == "__main__":
    json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
    json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)
    print("pieces", len(pieces), "props", len(props))
