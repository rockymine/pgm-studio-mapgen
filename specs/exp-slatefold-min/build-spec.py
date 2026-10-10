"""Slatefold -- a capture-the-wool board for two teams of twelve: a slate-quarrying hamlet on two terraced
hillsides that face each other across the void. Writes exp-slatefold-min.plan.json and .refinement.json.

Team 0 stands on +z and is fanned by rot_180. Every height is a terrace: quarry floor 8, spoil shelf 12,
hamlet 13, spawn terrace and the high bench 18, with stairs of one-block treads between them.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "exp-slatefold-min"

def piece(pid, x, z, w, h, y, role="piece"):
    return {"id": pid, "role": role, "rect": [x, z, w, h], "surface": y}

QUARRY_Y, HAMLET_Y, HIGH_Y = 8, 12, 16

pieces = []
# quarry floor, the lowest ground, at the void's edge
pieces += [piece("quarry-main", -4, 4, 13, 5, QUARRY_Y),
           piece("quarry-east", 9, 7, 3, 2, QUARRY_Y),
           piece("kiln-room", 9, 4, 3, 3, QUARRY_Y, "wool-room"),
           piece("spoil-shelf", -8, 4, 4, 5, HAMLET_Y - 1)]
# the high bench along the west edge, ending at the watchtower
pieces += [piece("tower-room", -12, 4, 4, 3, HIGH_Y, "wool-room"),
           piece("bench", -12, 7, 4, 22, HIGH_Y)]
# the cart track: three treads from the quarry floor up to the hamlet, four risers
for i in range(3):
    pieces.append(piece(f"cart-{i}", 2, 9 + i, 4, 1, QUARRY_Y + 1 + i))
# the hamlet terrace
pieces += [piece("hamlet-a", -8, 9, 10, 4, HAMLET_Y),
           piece("hamlet-b", 6, 9, 6, 4, HAMLET_Y),
           piece("cart-head", 2, 12, 4, 1, HAMLET_Y),
           piece("hamlet-row", -8, 13, 20, 4, HAMLET_Y),
           piece("hamlet-top", -4, 17, 16, 3, HAMLET_Y),
           piece("scree-gully", -8, 20, 5, 4, HAMLET_Y)]
# the bench path: three treads rising west from the hamlet, then a landing on the bench
for i in range(3):
    pieces.append(piece(f"bench-stair-{i}", -5 - i, 17, 1, 3, HAMLET_Y + 1 + i))
pieces.append(piece("bench-landing", -8, 17, 1, 3, HIGH_Y))
# the spawn stair, three treads, then the spawn terrace
for i in range(3):
    pieces.append(piece(f"spawn-stair-{i}", -3, 20 + i, 6, 1, HAMLET_Y + 1 + i))
pieces += [piece("terrace-w", -8, 24, 5, 5, HIGH_Y),
           piece("terrace-e", 3, 24, 3, 5, HIGH_Y),
           piece("terrace-front", -3, 23, 6, 2, HIGH_Y),
           piece("spawn-room", -3, 25, 6, 4, HIGH_Y, "spawn")]

plan = {
    "plan": 2,
    "meta": {"name": "Slatefold", "notes": "Two terraced slate hillsides facing across the void."},
    "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 12, "surface": 13},
    "pieces": pieces,
    "zones": [{"id": "crossing", "rect": [-12, -4, 24, 8], "holes": []}],
    "placements": {
        "spawns": [{"id": "spawn-1", "piece": "spawn-room", "at": [12, 8], "facing": "front"}],
        "wools": [{"id": "wool-kiln", "piece": "kiln-room", "at": [8, 6]},
                  {"id": "wool-tower", "piece": "tower-room", "at": [8, 6]}],
        "iron": [], "destroyables": [], "cores": []},
    "walls": [],
}

def solid(i, d=0):
    return {"kind": "solid", "id": i, "data": d}

GRASS, DIRT, COARSE, STONE, ANDESITE, POLISHED, COBBLE = solid(2), solid(3), solid(3, 1), solid(1), solid(1, 5), solid(1, 6), solid(4)
GRAVEL, STONEBRICK = solid(13), solid(98)

def layered(axis, *bands, ending="repeat", **words):
    out = {"kind": "layered", "axis": axis,
           "stack": {"ending": ending, "bands": [{"thickness": t, "material": m} for m, t in bands]}}
    out.update(words)
    return out

def over(top, under=DIRT, depth=1):
    return layered("depth", (top, depth), (under, 2), ending="handOver")

# one rock under the whole board: beds that follow the ground, on the fill, the wall and the steepest slope band
STRATA = layered("height", (STONE, 3), (ANDESITE, 1), (POLISHED, 1), (STONE, 2), (ANDESITE, 2), (POLISHED, 1),
                 **{"from": 0, "follow": 100, "reach": 16})

def theme(surface, rim=ANDESITE):
    return {"bedrock": {"relative": False, "value": 1}, "fill": STRATA, "rimEdges": "void",
            "rim": {"enabled": True, "depth": 1, "material": rim},
            "wallEnabled": True, "wallOnTerrainFaces": True, "wall": STRATA,
            "surface": {"enabled": True, "depth": 3, "material": surface}}

def cell(seed, size, palette, jitter=55):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": 1, "rise": 0, "palette": palette}

def noise(seed, scale, stops):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 2, "stops": stops, "rise": 0}

# the hillside is turf over soil, soil and scree on the shoulders, rock on the faces: one stack read by slope
HILLSIDE = theme(layered("slope", (over(GRASS), 32), (over(noise(11, 2, [COARSE, DIRT, DIRT, COARSE])), 14), (STRATA, 44)))
# the quarry is bare slate: a stone/andesite ground with cobble as an end patch, then the beds
QUARRY = theme(layered("slope", (over(noise(21, 2, [COBBLE, ANDESITE, STONE, STONE, ANDESITE]), STONE), 40), (STRATA, 50)))
# a flight is laid, and is the same stone the whole way up
STEPS = theme(cell(31, 3, [STONEBRICK, POLISHED, ANDESITE, STONE]), rim=STONEBRICK)

STEP_IDS = ["bench-9", "bench-10", "bench-11", "bench-13", "bench-13-2", "bench-14", "bench-14-2", "bench-15", "bench-15-2"]
THEME_BY_ID = {"bench-8": "quarry", "bench-11-2": "quarry", "bench-12": "hillside", "bench-16": "hillside"}
THEME_BY_ID.update({i: "steps" for i in STEP_IDS})
ALL_IDS = list(THEME_BY_ID)

def ring(cx, cz, rx, rz, n=10, lobe=0.18, phase=0.0):
    import math
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n + phase
        f = 1 + lobe * math.sin(3 * a + phase * 5)
        out.append([round(cx + rx * f * math.cos(a)), round(cz + rz * f * math.sin(a))])
    return out

PUSHES = [
    # the quarry pit: a hollow in the floor the cart track descends into
    {"id": "pit", "ring": ring(8, 25, 11, 6, 10, 0.15, 0.4), "amount": -3, "falloff": 6, "crown": 0, "roughness": 0.3, "seed": 3},
    # spoil heaps: tipped slate on the shelf under the tower, and one on the floor
    {"id": "heap-shelf", "ring": ring(-24, 26, 5, 5, 8, 0.2, 0.2), "amount": 3, "falloff": 5, "crown": 2, "roughness": 0.4, "seed": 5},
    {"id": "heap-floor", "ring": ring(-10, 30, 3, 3, 8, 0.2, 1.0), "amount": 3, "falloff": 4, "crown": 1.5, "roughness": 0.4, "seed": 6},
]

PATH_SET = cell(41, 3, [GRAVEL, ANDESITE, COBBLE], jitter=55)
YARD_SET = cell(51, 3, [DIRT, COARSE], jitter=60)

def road(pid, seed, points, radius=2, wander=2, pave=PATH_SET, style="solid"):
    return {"id": pid, "kind": "stroke", "seed": seed, "radius": radius, "style": style, "claimsGround": True,
            "wander": wander, "wanderLength": 14, "pave": pave, "points": points}

def house(pid, seed, x0, z0, x1, z1, front, style="cottage"):
    return {"id": pid, "kind": "house", "layer": "ground", "seed": seed, "front": front, "style": style,
            "wings": [{"corners": [[x0, z0], [x1, z1]]}]}

def tree(pid, seed, x, z, style):
    return {"id": pid, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}

def rock(pid, seed, x, z, style):
    return {"id": pid, "kind": "boulder", "seed": seed, "x": x, "z": z, "style": style}

SLATE = {"kind": "turbulence", "seed": 8801, "scale": 3, "octaves": 3, "rise": 3,
         "stops": [ANDESITE, STONE, STONE, COBBLE]}

COTTAGE = json.load(open(os.path.join(HERE, "cottage.style.json")))
KILN_HOUSE = json.load(open(os.path.join(HERE, "kiln-house.style.json")))

DRESSING = {
    "styles": {
        "cottage": {"kind": "house", "shell": COTTAGE},
        "spruce-8": {"kind": "tree", "form": "template", "species": "spruce", "height": 8},
        "oak-6": {"kind": "tree", "form": "template", "species": "oak", "height": 6},
        "slate-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": False, "rock": SLATE},
        "slate-2": {"kind": "boulder", "form": "round", "size": 2, "mossy": False, "rock": SLATE},
    },
    "props": [
        # circulation: spawn stair foot -> the green -> the cart stair; the cart stair foot -> the quarry floor;
        # the green -> the east cottages; the green -> the bench stair; the bench path from the spawn terrace to the tower
        road("street", 9001, [[0, 79], [3, 72], [8, 64], [14, 58], [16, 53]]),
        road("cart-foot", 9002, [[16, 35], [17, 31], [22, 29], [30, 27], [35, 24]]),
        road("east-lane", 9003, [[16, 57], [24, 60], [34, 60], [42, 58]]),
        road("bench-approach", 9004, [[3, 72], [-6, 70], [-12, 72], [-15, 74]]),
        road("bench-path", 9005, [[-26, 106], [-35, 102], [-38, 92], [-37, 80], [-38, 66], [-37, 52], [-38, 40], [-39, 30]]),
        road("green", 9006, [[-4, 58], [8, 58]], radius=5, wander=0, pave=YARD_SET, style="worn"),
        # the hamlet: one style, four plots
        house("cottage-west", 9101, -28, 56, -18, 64, "posZ"),
        house("cottage-store", 9102, -10, 44, 2, 52, "posX"),
        house("cottage-east", 9103, 22, 66, 32, 74, "negZ"),
        house("cottage-yard", 9104, 27, 40, 37, 48, "posZ"),
        house("cottage-warden", 9105, -44, 98, -34, 108, "posX"),
        # cover: slate heaps' neighbours and a few rocks where a hill meets a wall
        rock("rock-shelf", 9201, -28, 34, "slate-3"), rock("rock-gully", 9202, -22, 88, "slate-2"),
        rock("rock-brink", 9203, 26, 33, "slate-2"), rock("rock-bench", 9204, -46, 86, "slate-3"),
        tree("spruce-bench-a", 9301, -45, 60, "spruce-8"), tree("spruce-bench-b", 9302, -45, 46, "spruce-8"),
        tree("spruce-hamlet-w", 9303, -30, 42, "spruce-8"), tree("spruce-hamlet-e", 9304, 41, 75, "spruce-8"),
        tree("spruce-terrace-w", 9305, -23, 112, "spruce-8"), tree("spruce-terrace-e", 9306, 29, 106, "spruce-8"),
        tree("oak-terrace", 9307, 30, 102, "oak-6"), tree("oak-hamlet", 9308, 40, 68, "oak-6"),
        {"id": "ground-cover", "kind": "flora", "seed": 9401,
         "points": [[-48, 16], [48, 16], [48, 116], [-48, 116]],
         "spec": {"coverage": 0.28, "scale": 6, "octaves": 3, "fernShare": 0.3, "flowerShare": 0.08,
                  "flowerScale": 14, "tallShare": 0.04}},
    ],
}

refinement = {
    "authors": ["Sonnet 5.5"], "created": "2026-10-10",
    "themes": {"hillside": HILLSIDE, "quarry": QUARRY, "steps": STEPS},
    "mapTheme": "hillside",
    "themeById": THEME_BY_ID,
    "editShapes": {
        # the hamlet's east and back coasts wander in a few blocks; the spawn terrace's two back corners are cut off
        "bench-12": [{"pulls": {"5": [[0.28, 3], [0.6, 1.5], [0.85, 3.5]], "6": [[0.12, 3], [0.3, 1.5], [0.5, 4]]}}],
        "bench-16": [{"after": 11, "x": 24, "z": 108}, {"index": 13, "x": 16, "z": 116},
                     {"after": 14, "x": -48, "z": 108}, {"index": 14, "x": -40, "z": 116},
                     {"pulls": {"13": [[0.8, 3]]}}],
    },
    "shapePropsById": {i: {"relief_scope": "hold"} for i in ALL_IDS},
    "relief": {"team": {"base": 13, "reach": 0, "step": 1, "marks": [], "pushes": PUSHES}},
    "biome": {"kind": "solid", "id": 3},
    "roomStyles": {"wool": KILN_HOUSE, "spawn": COTTAGE},
    "dressing": DRESSING,
}

def main():
    json.dump(plan, open(os.path.join(HERE, f"{SLUG}.plan.json"), "w"), indent=1)
    json.dump(refinement, open(os.path.join(HERE, f"{SLUG}.refinement.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
