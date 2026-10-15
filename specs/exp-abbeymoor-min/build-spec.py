"""Abbeymoor, destroy the monument -- the plan and the refinement it is driven with.

A high heather moor split by a black peat bog. Each team holds the hill of a ruined abbey with a crypt under
it, and an orchard village in the hollow below; the bog between has a stone ring and two causeways.
Blocks everywhere unless a name says cells. x runs red (west, negative) to blue (east); z is north-south.
The red half is authored and rot_180 fans the blue one.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.basename(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "tools"))
CELL = 4

# ---------------------------------------------------------------- the plan
def piece(pid, x, z, w, h, surface=None, role="piece"):
    p = {"id": pid, "role": role, "rect": [x, z, w, h]}
    if surface is not None:
        p["surface"] = surface
    return p

SPAWN_AT = (-112, 4)
ABBEY_STONE = (-74, -30)      # the abbey monument, in the nave's open east end
MARKET_CROSS = (-60, 28)      # the village monument, on the green

plan = {
    "plan": 2,
    "meta": {"name": "Abbeymoor"},
    "globals": {"cell": CELL, "symmetry": "rot_180", "maxPlayers": 16, "surface": 22},
    "pieces": [
        piece("moor-n", -35, -13, 26, 11),
        piece("moor-s", -35, 4, 26, 9),
        piece("moor-m", -26, -2, 17, 6),
        piece("spawn", -31, -2, 5, 6, role="spawn"),
        piece("bog", -9, -13, 18, 26, surface=18),
    ],
    "zones": [],
    "placements": {
        "spawns": [{"id": "red-spawn", "piece": "spawn", "at": [10, 12], "facing": "right", "footprint": [1, 1, 18, 22]}],
        "destroyables": [
            {"id": "abbey-stone", "piece": "", "at": list(ABBEY_STONE), "style": "pillar-3",
             "materials": "obsidian", "float": 4, "name": "Abbey Stone"},
            {"id": "market-cross", "piece": "", "at": list(MARKET_CROSS), "style": "cube-3",
             "materials": "gold block", "float": 4, "name": "Market Cross"},
        ],
    },
    "walls": [],
}

# ---------------------------------------------------------------- materials
def S(block, data=0): return {"kind": "solid", "id": block, "data": data}
def depth(*bands): return {"kind": "layered", "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}
def cell(size, palette, seed=1, jitter=1, warp=1, rise=0): return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp, "palette": palette, "rise": rise}
def noise(scale, stops, seed=1, octaves=2): return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops}

STONE, ANDESITE, GRANITE, POLISHED = S(1), S(1, 5), S(1, 1), S(1, 6)
COBBLE, MOSSCOBBLE = S(4), S(48)
GRASS, DIRT, COARSE, PODZOL = S(2), S(3), S(3, 1), S(3, 2)
BRICK, MOSSBRICK, CRACKBRICK = S(98), S(98, 1), S(98, 2)
GRAVEL, PLANKS_SPRUCE = S(13), S(5, 1)

# strata follow the ground: stone with andesite bands and a thin cobble accent, laid so a cliff reads as beds
STRATA = {"kind": "layered", "axis": "height", "from": 0, "follow": 100, "reach": 16, "stack": {"ending": "repeat", "bands": [
    {"material": cell(3, [STONE, STONE, ANDESITE], seed=61, rise=1), "thickness": 4},
    {"material": cell(3, [ANDESITE, POLISHED, ANDESITE, STONE], seed=62, rise=1), "thickness": 2},
    {"material": cell(3, [STONE, GRANITE, STONE, ANDESITE], seed=63, rise=1), "thickness": 3},
    {"material": cell(2, [COBBLE, ANDESITE, COBBLE, STONE], seed=64, rise=1), "thickness": 1},
    {"material": cell(3, [ANDESITE, STONE, ANDESITE], seed=65, rise=1), "thickness": 3}]}}
# a rock is a set: stone and andesite with cobblestone as the accent (at most a third)
ROCK = cell(3, [STONE, ANDESITE, STONE, COBBLE], seed=3)
SOIL = depth((cell(2, [DIRT, COARSE], seed=5), 1), (DIRT, 2))   # a worn dirt, half and half

def moor_theme(grass_to=40, dirt_to=55, flat=None):
    turf = flat or noise(3, [PODZOL, GRASS, GRASS, GRASS, GRASS, COARSE], seed=11)
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "rim": {"enabled": False, "depth": 1, "material": STONE},
        "wallEnabled": True, "wallOnTerrainFaces": True,
        "wall": STRATA, "fill": STRATA,
        "surface": {"enabled": True, "depth": 3, "material": {
            "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
                {"thickness": grass_to, "material": depth((turf, 1), (COARSE, 1), (DIRT, 1))},
                {"thickness": dirt_to - grass_to, "material": SOIL},
                {"thickness": 90 - dirt_to, "material": depth((ROCK, 3))}]}}},
    }

def bog_theme():
    peat = noise(3, [COARSE, PODZOL, PODZOL, DIRT, COARSE], seed=21)
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "rim": {"enabled": False, "depth": 1, "material": STONE},
        "wallEnabled": True, "wallOnTerrainFaces": True,
        "wall": STRATA, "fill": STRATA,
        "surface": {"enabled": True, "depth": 3, "material": {
            "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
                {"thickness": 36, "material": depth((peat, 1), (COARSE, 2))},
                {"thickness": 14, "material": SOIL},
                {"thickness": 40, "material": depth((ROCK, 3))}]}}},
    }

HEATH_FLAT = noise(3, [COARSE, PODZOL, GRASS, GRASS, PODZOL, COARSE], seed=13)
RUIN_SET = cell(3, [BRICK, POLISHED, ANDESITE, BRICK], seed=31)
def ruin_theme():
    ruin_wall = cell(2, [BRICK, BRICK, ANDESITE, MOSSBRICK, BRICK], seed=33, rise=2)
    return {
        "bedrock": {"relative": False, "value": 1},
        "rimEdges": "void", "rim": {"enabled": False, "depth": 1, "material": BRICK},
        "wallEnabled": True, "wallOnTerrainFaces": True,
        "wall": ruin_wall, "fill": cell(3, [STONE, ANDESITE, COBBLE, BRICK], seed=35, rise=2),
        "surface": {"enabled": True, "depth": 1, "material": RUIN_SET},
    }

STREET = cell(3, [DIRT, COARSE, PLANKS_SPRUCE], seed=41)
CAUSEWAY = cell(3, [GRAVEL, ANDESITE, COBBLE], seed=43)

# ---------------------------------------------------------------- relief
def lobed(cx, cz, rx, rz, lobes=5, depth=0.14, points=36, phase=0.0):
    out = []
    for k in range(points):
        a = 2 * math.pi * k / points
        f = 1 + depth * math.cos(lobes * a + phase)
        out.append([round(cx + rx * f * math.cos(a), 1), round(cz + rz * f * math.sin(a), 1)])
    return out

def area(mark_id, h, ring, bevel=0):
    return {"id": mark_id, "kind": "area", "h": h, "bevel": bevel, "ring": ring}

def line(mark_id, points, h, r=4, tread=2):
    return {"id": mark_id, "kind": "line", "points": points, "h": h, "r": r, "tread": tread}

ABBEY_HILL = (-84, -28)
VILLAGE = (-62, 26)
CAUSEWAY_VILLAGE = [[-46, 34], [-36, 26], [-26, 16], [-14, 8], [-4, 2], [0, 0]]
CAUSEWAY_ABBEY = [[-54, -28], [-46, -20], [-38, -14], [-24, -8], [-12, -3], [0, 0]]

marks = [
    area("bog-floor", 18, lobed(0, 0, 27, 38, lobes=3, depth=0.07)),
    area("spawn-pad", 22, [[-128, -12], [-100, -12], [-100, 20], [-128, 20]]),
    area("village-hollow", 20, lobed(VILLAGE[0], VILLAGE[1], 19, 16, lobes=4, depth=0.1), bevel=4),
    line("causeway-village", CAUSEWAY_VILLAGE, 20, r=4, tread=2),
    line("causeway-abbey", CAUSEWAY_ABBEY, 20, r=4, tread=2),
    area("hummock-a", 20, lobed(-16, -28, 7, 5, lobes=3, depth=0.15), bevel=2),
    area("hummock-b", 20, lobed(-8, 30, 6, 5, lobes=3, depth=0.15, phase=1), bevel=2),
    area("hummock-c", 20, lobed(-6, -16, 4.5, 3.5, lobes=3, depth=0.15, phase=2), bevel=1),
]
pushes = [
    {"id": "abbey-hill", "ring": lobed(ABBEY_HILL[0], ABBEY_HILL[1], 15, 12, lobes=4, depth=0.16),
     "amount": 13, "falloff": 26, "crown": 4, "roughness": 1, "seed": 4},
    {"id": "spawn-ridge", "ring": lobed(-134, 2, 8, 10, lobes=3, depth=0.15),
     "amount": 7, "falloff": 12, "crown": 3, "roughness": 1, "seed": 6},
    {"id": "tor", "ring": lobed(-50, -44, 6, 5, lobes=3, depth=0.2),
     "amount": 9, "falloff": 12, "crown": 4, "roughness": 1, "seed": 8},
    {"id": "swell-south", "ring": lobed(-110, 40, 10, 8, lobes=3, depth=0.2),
     "amount": 3, "falloff": 16, "crown": 0, "roughness": 0, "seed": 12},
    {"id": "swell-north", "ring": lobed(-118, -42, 10, 8, lobes=3, depth=0.2),
     "amount": 3, "falloff": 16, "crown": 0, "roughness": 0, "seed": 13},
]
relief = {"team": {"base": 22, "reach": 0, "step": 1, "marks": marks, "pushes": pushes,
                   "grain": {"amplitude": 1.2, "scale": 9, "seed": 17}}}

# ---------------------------------------------------------------- the board's outline (red half; rot_180 draws the rest)
MOOR_RING = [[-136, -40], [-124, -50], [-104, -51], [-84, -48], [-62, -50], [-46, -48], [-36, -46],
             [-36, 46], [-48, 50], [-68, 49], [-90, 51], [-110, 49], [-126, 48], [-138, 38],
             [-142, 26], [-143, 8], [-142, -10], [-141, -26]]
BOG_RING = [[-36, -46], [-18, -42], [0, -37], [18, -40], [36, -46],
            [36, 46], [18, 42], [0, 37], [-18, 40], [-36, 46]]

# ---------------------------------------------------------------- the abbey: ruin on the hill, crypt under it
CREST = 35     # the abbey hill's plateau, read back from a transect

def block(shape_id, x0, z0, x1, z1, top, theme="ruin", keep=True, floor=0):
    s = {"id": shape_id, "type": "rectangle", "operation": "add", "override": True, "floor": floor,
         "base_height": top - floor, "height_mode": "level", "skirt": 0, "theme": theme,
         "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}
    if keep:
        s["keepClear"] = True
    return s

def subtract(shape_id, x0, z0, x1, z1):
    return {"id": shape_id, "type": "rectangle", "operation": "subtract", "floor": 0,
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}

SOFFIT = 32            # the crypt's ceiling course; the roof over it is SOFFIT..CREST
FLOOR_TOP = 27         # crypt layer slab thickness: floor course is y26
shapes = []
# the nave floor is level ground at the plateau height, cut around the stair well and the lane roof
shapes += [block("nave-floor-w", -104, -36, -82, -22, CREST, theme="moor", keep=False),
           block("nave-floor-e", -82, -32, -68, -22, CREST, theme="moor", keep=False),
           block("nave-floor-nstrip", -82, -36, -68, -35, CREST, theme="moor", keep=False)]
# walls: ragged courses along the nave, a tower stump at the south-west, the west gable
for sid, x0, x1, top in [("nw1", -104, -94, 3), ("nw2", -90, -80, 5), ("nw3", -76, -66, 2)]:
    shapes.append(block("nave-n-" + sid, x0, -38, x1, -36, CREST + top))
for sid, x0, x1, top in [("sw1", -100, -94, 4), ("sw2", -92, -84, 2), ("sw3", -80, -70, 5)]:
    shapes.append(block("nave-s-" + sid, x0, -22, x1, -20, CREST + top))
shapes.append(block("gable-w", -106, -38, -104, -20, CREST + 7))
shapes.append(block("tower-stump", -106, -26, -100, -20, CREST + 10))
for i, px in enumerate([-96, -90, -84]):    # piers stand over the crypt roof, so they start at its soffit
    shapes.append(block(f"pier-n{i}", px, -33, px + 1, -32, CREST + (4 if i % 2 else 2), floor=SOFFIT))
    shapes.append(block(f"pier-s{i}", px, -26, px + 1, -25, CREST + (3 if i % 2 else 5), floor=SOFFIT))
# crypt roof, lane roof, and the two cuts: the stair well in the nave and the open lane to the east flank
shapes += [block("crypt-roof", -98, -35, -82, -24, CREST, floor=SOFFIT),
           block("lane-roof", -82, -30, -68, -27, CREST, floor=SOFFIT),
           subtract("stair-well", -82, -35, -64, -32),
           subtract("lane-cut", -68, -30, -50, -27)]

# the standing stones of the bog: eight in a ring of radius 15, four authored and four fanned
for i, (ang, top) in enumerate(zip([25, 70, 115, 160], [28, 30, 27, 29])):
    cx, cz = 15 * math.cos(math.radians(ang)), 15 * math.sin(math.radians(ang))
    shapes.append(block(f"stone-{i}", round(cx) - 1, round(cz) - 1, round(cx) + 1, round(cz) + 1, top))
# gate stones where the village causeway leaves the moor, a sheepfold, peat stacks, a well
shapes += [block("gatestone-a", -49, 30, -47, 32, 27), block("gatestone-b", -45, 36, -43, 38, 28)]
for sid, x0, z0, x1, z1 in [("fold-n", -126, -38, -114, -37), ("fold-s", -126, -30, -118, -29),
                            ("fold-w", -126, -38, -125, -29), ("fold-e", -114, -38, -113, -33)]:
    shapes.append(block(sid, x0, z0, x1, z1, 26))
for sid, x0, z0, x1, z1 in [("peat-1", -46, -46, -40, -44), ("peat-2", -46, -43, -40, -41), ("peat-3", -39, -46, -35, -44)]:
    shapes.append(block(sid, x0, z0, x1, z1, 26, theme="bog", keep=True))
shapes += [block("well-rim", -63, 22, -59, 24, 22, keep=True)]

# patches of rough heath: shapes carrying their own theme, drawn at the island's own raw height
def patch(pid, cx, cz, rx, rz, theme="heath", lobes=4, phase=0.0):
    return {"id": pid, "type": "polygon", "operation": "add", "floor": 0, "base_height": 22, "theme": theme,
            "vertices": lobed(cx, cz, rx, rz, lobes=lobes, depth=0.22, points=18, phase=phase)}
patches = [patch("heath-north", -108, -26, 15, 10), patch("heath-ridge", -131, 18, 9, 11, phase=1),
           patch("heath-south", -102, 36, 13, 8, phase=2), patch("heath-tor", -64, -50, 8, 3, lobes=3)]

# the crypt storey: floor slab, pillars, tombs, the lane floor and the nine steps up the stair well
crypt = [
    {"id": "crypt-floor", "type": "rectangle", "operation": "add", "floor": 0, "base_height": FLOOR_TOP,
     "theme": "ruin", "min_x": -98, "min_z": -35, "max_x": -82, "max_z": -24},
    {"id": "lane-floor", "type": "rectangle", "operation": "add", "floor": 0, "base_height": FLOOR_TOP,
     "theme": "ruin", "min_x": -82, "min_z": -30, "max_x": -54, "max_z": -27},
    {"id": "lane-apron-1", "type": "rectangle", "operation": "add", "floor": 0, "base_height": FLOOR_TOP - 1,
     "theme": "ruin", "min_x": -54, "min_z": -30, "max_x": -52, "max_z": -27},
    {"id": "lane-apron-2", "type": "rectangle", "operation": "add", "floor": 0, "base_height": FLOOR_TOP - 2,
     "theme": "ruin", "min_x": -52, "min_z": -30, "max_x": -50, "max_z": -27},
]
for i, (px, pz) in enumerate([(-94, -32), (-94, -27), (-88, -32), (-88, -27)]):
    crypt.append({"id": f"crypt-pillar-{i}", "type": "rectangle", "operation": "add", "floor": 0,
                  "base_height": SOFFIT, "theme": "ruin", "min_x": px, "min_z": pz, "max_x": px + 1, "max_z": pz + 1})
for i, (tx, tz) in enumerate([(-97, -34), (-97, -25)]):
    crypt.append({"id": f"tomb-{i}", "type": "rectangle", "operation": "add", "floor": 0, "base_height": FLOOR_TOP + 1,
                  "theme": "ruin", "min_x": tx, "min_z": tz, "max_x": tx + 4, "max_z": tz + 1})
# lamps: a glowstone column at each end wall of the chamber, since a shape can carry one material and the light with it
for i, (lx, lz) in enumerate([(-98, -35), (-98, -25), (-91, -35), (-91, -25)]):
    crypt.append({"id": f"lamp-{i}", "type": "rectangle", "operation": "add", "floor": 0, "base_height": FLOOR_TOP + 2,
                  "material": {"kind": "solid", "id": 89, "data": 0}, "min_x": lx, "min_z": lz, "max_x": lx + 1, "max_z": lz + 1})
# eight rises in two flights of four with a landing between: a step is two blocks long, the landing is four
cursor = -82
for k in range(1, 9):
    run = 4 if k == 4 else 2
    crypt.append({"id": f"step-{k}", "type": "rectangle", "operation": "add", "floor": 0, "base_height": FLOOR_TOP + k,
                  "theme": "ruin", "min_x": cursor, "min_z": -35, "max_x": cursor + run, "max_z": -32})
    cursor += run
crypt_layer = {"id": "crypt", "name": "Crypt", "base_y": 0, "below": True, "shapes": crypt,
               "groups": [{"id": "crypt", "name": "crypt", "mirrors": True, "shapeIds": [c["id"] for c in crypt]}]}

# ---------------------------------------------------------------- dressing
from showcase import trees as studio_trees
LIB = studio_trees()
STYLES = {
    "orchard-oak": LIB["tiny-oak-3"]["style"],
    "hawthorn": LIB["olive-6"]["style"],
    "outcrop": {"kind": "boulder", "form": "round", "size": 3, "mossy": False, "rock": ROCK},
    "cottage": {"library": "spruce-roofed-white-clay-cottage", "kind": "house"},
}

def tree(pid, x, z, style):
    return {"id": pid, "kind": "tree", "layer": "ground", "seed": 100 + abs(x * 7 + z), "x": x, "z": z, "style": style}

def boulder(pid, x, z):
    return {"id": pid, "kind": "boulder", "layer": "ground", "seed": 200 + abs(x * 3 + z), "x": x, "z": z, "style": "outcrop"}

def house(pid, x0, z0, x1, z1, front, ridge):
    return {"id": pid, "kind": "house", "layer": "ground", "seed": 5, "front": front, "style": "cottage",
            "wings": [{"corners": [[x0, z0], [x1, z1]], "spec": {"ridge": ridge}}]}

def road(pid, points, pave, radius=2, wander=2, claims=True):
    return {"id": pid, "kind": "stroke", "layer": "ground", "seed": 7, "points": points, "radius": radius,
            "style": "solid", "claimsGround": claims, "pave": pave, "wander": wander, "wanderLength": 14}

props = [
    road("spawn-street", [[-103, 4], [-94, 12], [-86, 18], [-78, 19], [-70, 20], [-64, 25], [-60, 28]], STREET, radius=2),
    road("fold-path", [[-110, -9], [-112, -18], [-114, -28]], STREET, radius=1.5),
    road("hill-path", [[-62, 22], [-61, 12], [-62, 0], [-66, -10], [-68, -18], [-66, -26]], STREET, radius=1.5),
    road("tor-path", [[-66, -32], [-60, -38], [-54, -42]], STREET, radius=1.5),
    road("peat-path", [[-52, -42], [-46, -38], [-44, -32]], STREET, radius=1.5),
    road("causeway-village", CAUSEWAY_VILLAGE, CAUSEWAY, radius=2, wander=1),
    road("causeway-abbey", CAUSEWAY_ABBEY, CAUSEWAY, radius=2, wander=1),
]
props += [
    house("cott-1", -80, 22, -72, 28, "posX", "alongZ"),
    house("cott-2", -74, 8, -66, 13, "posZ", "alongX"),
    house("cott-3", -50, 10, -42, 15, "posZ", "alongX"),
    house("cott-4", -74, 38, -66, 43, "negZ", "alongX"),
    house("cott-5", -54, 32, -49, 36, "negX", "alongZ"),
    house("cott-6", -46, -36, -38, -31, "posX", "alongZ"),
]
# the orchard: a lattice of small oaks west and south of the cottages
for r, z in enumerate([32, 40, 47]):
    for c, x in enumerate([-100, -92, -84]):
        props.append(tree(f"orchard-w-{r}-{c}", x, z, "orchard-oak"))
for c, x in enumerate([-62, -54]):
    props.append(tree(f"orchard-s-{c}", x, 47, "orchard-oak"))
props += [tree("haw-a", -16, -28, "hawthorn"), tree("haw-b", -8, 30, "hawthorn"),
          tree("haw-spawn-1", -137, -4, "hawthorn"), tree("haw-spawn-2", -136, 14, "hawthorn")]
props += [boulder("rock-tor-1", -54, -45), boulder("rock-tor-2", -45, -41),
          boulder("rock-abbey-1", -64, -44), boulder("rock-abbey-2", -118, -44),
          boulder("rock-ridge", -130, 24), boulder("rock-south", -108, 45)]
def pool(pid, ring):
    return {"id": pid, "kind": "fluid", "shape": "pool", "layer": "ground", "points": ring, "radius": 2,
            "depth": 2, "form": "natural", "edge": 1.5, "shore": 1, "shoreWander": True, "seed": 3, "level": 17,
            "bank": cell(3, [COARSE, PODZOL, DIRT], seed=51)}
props += [pool("tarn-north", lobed(-14, -18, 8, 5, lobes=3, depth=0.2)),
          pool("tarn-south", lobed(-24, 33, 6, 4, lobes=3, depth=0.2, phase=1)),
          pool("tarn-mid", lobed(-6, 20, 5, 4, lobes=3, depth=0.2, phase=2))]
props.append({"id": "heather", "kind": "flora", "layer": "ground", "seed": 77,
              "points": [[-140, -50], [140, -50], [140, 50], [-140, 50]],
              "spec": {"coverage": 0.28, "scale": 6, "octaves": 3, "fernShare": 0.35, "flowerShare": 0.3,
                       "flowerScale": 12, "tallShare": 0.02, "mushroomShare": 0.3}})

refinement = {
    "themes": {"moor": moor_theme(), "heath": moor_theme(flat=HEATH_FLAT), "bog": bog_theme(), "ruin": ruin_theme()},
    "mapTheme": "moor",
    "themeById": {"bog-22": "moor", "bog-18": "bog"},
    "shapePropsById": {"bog-22": {"vertices": MOOR_RING}, "bog-18": {"vertices": BOG_RING}},
    "bendShapes": {"bog-22": {"tension": 0.22, "wander": 3, "step": 10, "seed": 5, "side": "out"},
                   "bog-18": {"tension": 0.22, "wander": 2, "step": 12, "seed": 9, "side": "out"}},
    "biome": {"kind": "solid", "id": 6},
    "relief": relief,
    "addLayers": [crypt_layer],
    "addShapes": [dict(s, layer="ground", group="team") for s in shapes + patches],
    "roomStyles": {"spawn": {"library": "spruce-roofed-stone-longhouse"}},
    "dressing": {"styles": STYLES, "props": props},
    "authors": ["Claude Sonnet 5.5"],
    "created": "2026-10-10",
}

if __name__ == "__main__":
    json.dump(plan, open(f"{HERE}/{BASE}.plan.json", "w"), indent=1)
    json.dump(refinement, open(f"{HERE}/{BASE}.refinement.json", "w"), indent=1)
    print(f"plan {len(plan['pieces'])} pieces; refinement: {len(shapes)} ground shapes, {len(crypt)} crypt shapes, {len(props)} props")
