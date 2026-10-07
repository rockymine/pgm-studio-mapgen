#!/usr/bin/env python3
"""Rustwater Vale — an autumn river valley, two banks, one slow river, a watermill and a millstone a side.

Identity: two hillsides face each other across a river; each team's spawn sits on a shelf high on its own
valley side, its Millstone stands on a terrace below and to the east of it, and its watermill stands at the water.
The plan is three overlapping ranges of one height that step eastward toward the river, so the two banks only
overlap in the middle and the valley bends; every landform is authored in the relief.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import showcase  # noqa: E402

SLUG = "sonnet55b-rustwater"

# ---------------------------------------------------------------- the plan (cells of 4 blocks, team 0 north)
plan = {
  "plan": 2,
  "meta": {"name": "Rustwater Vale", "authors": ["Sonnet 5.5"]},
  "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20},
  "pieces": [
    {"id": "ridge", "rect": [-8, -29, 17, 9]},
    {"id": "slope", "rect": [-6, -20, 18, 9]},
    {"id": "bank",  "rect": [-6, -11, 20, 8]},
  ],
  "zones": [{"id": "river-gap", "rect": [-13, -3, 26, 6]}],
  "placements": {
    "spawns": [{"id": "spawn", "piece": "ridge", "at": [12, 24], "facing": "back",
                "footprint": [5, 17, 14, 14]}],
    "destroyables": [{"id": "millstone", "piece": "slope", "at": [40, 14], "style": "cube-3",
                      "materials": "gold block", "float": 3, "name": "Millstone"}],
  },
}

# ---------------------------------------------------------------- shapes of ground
def ring(cx, cz, rx, rz, n=12, wob=0.0, ph=0.0):
    return [[round(cx + rx*math.cos(2*math.pi*i/n + ph)*(1 + wob*math.sin(3*i + ph))),
             round(cz + rz*math.sin(2*math.pi*i/n + ph)*(1 + wob*math.cos(2*i)))] for i in range(n)]

LAND = [[-30,-110],[-12,-117],[4,-116],[16,-113],[24,-105],[32,-96],[38,-88],[44,-78],[46,-64],[40,-54],
        [34,-44],[30,-30],[30,-12],[20,-12],[0,-12],[-14,-12],[-24,-12],[-26,-26],[-22,-40],
        [-27,-56],[-25,-72],[-31,-85],[-35,-98]]

# ---------------------------------------------------------------- the relief: a stair of terraces to a ridge
def mk(i, kind, **kw):
    return {"id": i, "kind": kind, **kw}

relief = {"team": {"base": 20, "reach": 0, "step": 1, "landform": "hills",
  "grain": {"amplitude": 0.8, "scale": 9, "seed": 11},
  "marks": [
    mk("river-floor", "line", r=10, tread=7, points=[[-20,-24],[8,-22],[40,-27]], h=[14,14,14]),
    mk("mill-yard", "area", h=14, bevel=2, ring=ring(-4, -28, 17, 9, 10, 0.05)),
    mk("lower-shelf", "area", h=19, bevel=2, ring=ring(0, -48, 22, 10, 12, 0.07, 0.4)),
    mk("goal-terrace", "area", h=26, bevel=2, ring=ring(15, -66, 15, 11, 12, 0.06)),
    mk("barn-yard", "area", h=33, bevel=3, ring=ring(-1, -98, 9, 8, 10, 0.05)),
    mk("spawn-shelf", "area", h=32, bevel=2, ring=ring(-20, -92, 26, 15, 14, 0.07)),
    mk("back-ridge", "line", r=9, tread=3, points=[[-24,-112],[0,-114],[24,-111]], h=[40,42,39]),
  ],
  "pushes": [
    {"id": "east-fell", "ring": ring(37, -90, 6, 9, 9, 0.1), "amount": 9, "falloff": 15, "crown": 0.3,
     "roughness": 0.3, "seed": 3},
  ]}}

# ---------------------------------------------------------------- the paint: one ground, its slope bands
SOLID = lambda i, d=0: {"kind": "solid", "id": i, "data": d} if d else {"kind": "solid", "id": i}
GRASS, DIRT, COARSE, PODZOL = SOLID(2), SOLID(3), SOLID(3, 1), SOLID(3, 2)
STONE, ANDESITE, COBBLE = SOLID(1), SOLID(1, 5), SOLID(4)

def stack(*bands, ending="repeat"):
    return {"ending": ending, "bands": [{"thickness": t, "material": m} for m, t in bands]}

def layered(axis, *bands, ending="repeat", **words):
    return {"kind": "layered", "axis": axis, "stack": stack(*bands, ending=ending), **words}

def over_soil(top, under=DIRT):
    return layered("depth", (top, 1), (under, 2), ending="handOver")

def noise(stops, scale=3, seed=1, octaves=2, rise=0):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": octaves, "stops": stops}

def cell(palette, size=3, seed=1, jitter=1, warp=1, rise=0):
    d = {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp, "palette": palette}
    if rise: d["rise"] = rise
    return d

# meadow: leaf-littered grass (podzol inset at the ends of the stop list, the main set in the middle)
MEADOW = noise([PODZOL, GRASS, GRASS, PODZOL], scale=2, seed=4)
BARE = cell([DIRT, COARSE], size=4, seed=9)          # the worn shoulder, dirt and coarse dirt as one ground
ROCK = cell([STONE, ANDESITE, STONE, COBBLE], size=4, seed=2)

def theme(surface, wall, fill, rim=None, rim_edges="void", depth=3):
    t = {"bedrock": {"relative": False, "value": 1}, "rimEdges": rim_edges,
         "rim": {"enabled": rim is not None, "depth": 1, "material": rim or STONE},
         "surface": {"enabled": True, "depth": depth, "material": surface},
         "wallEnabled": True, "wallOnTerrainFaces": True, "wall": wall, "fill": fill}
    return t

STRATA = layered("height", (cell([STONE, ANDESITE], size=6, seed=3, rise=4), 4),
                 (cell([ANDESITE, STONE, COBBLE], size=6, seed=5, rise=4), 4), ending="repeat", follow=100, reach=16)
FILL = cell([STONE, ANDESITE, STONE], size=7, seed=6, rise=5)

SLOPE_STACK = layered("slope", (over_soil(MEADOW), 34), (over_soil(BARE), 10), (over_soil(ROCK, STONE), 46))

# built ground: the mill yard and the terraces' paving, four blocks of one warm tone a quarter each
POLISHED = SOLID(1, 6)
BRICK = SOLID(98)
PAVE = cell([BRICK, POLISHED, ANDESITE, STONE], size=3, seed=8)

themes = {
  "vale":  theme(SLOPE_STACK, STRATA, FILL),
  "yard":  theme(PAVE, STRATA, FILL, rim=None),
}

# ---------------------------------------------------------------- dressing
T = showcase.trees()
styles = {
  "oak-8":    T["oak-8"]["style"],
  "oak-6":    T["oak-6"]["style"],
  "birch-3":  T["birch-3"]["style"],
  "birch-5":  T["birch-5"]["style"],
  "mill":     {"library": "dark-oak-quay-warehouse", "kind": "house"},
  "cottage":  {"library": "hay-roofed-stone-and-dark-oak-house", "kind": "house"},
  "barn":     {"library": "hay-roofed-stone-and-dark-oak-house", "kind": "house"},
  "rock-a":   {"kind": "boulder", "form": "round", "size": 2.5, "mossy": False,
               "rock": {"kind": "cell", "seed": 14, "cellSize": 2, "jitter": 1, "warp": 1,
                        "palette": [{"kind": "solid", "id": 1}, {"kind": "solid", "id": 1, "data": 5},
                                    {"kind": "solid", "id": 1}, {"kind": "solid", "id": 4}]}},
}
STONE_RECIPE = None

def house(i, style, corners, front, seed):
    return {"id": i, "kind": "house", "layer": "ground", "seed": seed, "front": front, "style": style,
            "wings": [{"corners": corners, "spec": {"ridge": "alongX"}}]}

def tree(i, style, x, z, seed):
    return {"id": i, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}

props = [
  {"id": "river", "kind": "fluid", "layer": "ground", "shape": "channel", "form": "stream",
   "points": [[-26,-20],[-6,-19.5],[14,-21],[24,-26]], "radius": 5, "depth": 2, "level": 13,
   "shore": 3, "shoreWander": True, "edge": 1.5,
   "bank": cell([SOLID(13), SOLID(12), COARSE], size=3, seed=12)},
  house("mill", "mill", [[-12,-34],[-3,-28]], "negZ", 101),
  house("cottage", "cottage", [[-14,-54],[-5,-47]], "posZ", 102),
  house("barn", "barn", [[-6,-102],[3,-95]], "posZ", 103),
  tree("t1", "oak-8", -10, -66, 201), tree("t3", "oak-6", -21, -38, 203),
  tree("t5", "birch-5", 28, -50, 205), tree("t6", "oak-8", 25, -36, 206),
]


# ---------------------------------------------------------------- the cellar under the lower shelf
def sink(i, x0, z0, x1, z1, floor):
    return {"id": i, "type": "rectangle", "operation": "add", "height_mode": "sink", "base_height": floor,
            "skirt": 0, "theme": "yard", "group": "team", "layer": "ground",
            "min_x": x0, "min_z": z0, "max_x": x1, "max_z": z1}

cellar = [sink("cellar-pit", 0, -52, 10, -44, 7)]
for k in range(6):                      # a flight of six sunk treads, two blocks deep and one high, rising east
    cellar.append(sink(f"cellar-step-{k+1}", 10 + 2*k, -51, 12 + 2*k, -45, 6 - k))
roof_layer = {"id": "cellar-roof", "name": "cellar-roof", "base_y": 20,
              "shapes": [{"id": "cellar-lid", "type": "rectangle", "operation": "add", "floor": 0,
                          "base_height": 1, "theme": "yard", "min_x": -1, "min_z": -53, "max_x": 8, "max_z": -43}],
              "groups": [{"id": "cellar-roof", "mirrors": True, "shapeIds": ["cellar-lid"]}]}

# ---------------------------------------------------------------- paths: where the players go
WARM = cell([SOLID(3, 1), SOLID(5, 1), SOLID(13)], size=3, seed=21)
def path(i, pts, seed, radius=2.5):
    return {"id": i, "kind": "stroke", "layer": "ground", "points": pts, "radius": radius, "style": "solid",
            "claimsGround": True, "seed": seed, "wander": 2.5, "wanderLength": 14, "pave": WARM}
props += [
  path("way-spawn-goal", [[-20,-84],[-13,-78],[-3,-73],[6,-68]], 31),
  path("way-goal-mill", [[10,-60],[3,-53],[-2,-44],[-8,-37]], 32),
  path("way-mill-yard", [[-8,-34],[-8,-30]], 33),
  {"id": "meadow", "kind": "flora", "layer": "ground",
   "points": [[-30,-110],[30,-110],[44,-78],[46,-64],[30,-30],[20,-13],[-24,-14],[-26,-56],[-31,-85]],
   "spec": {"coverage": 0.28, "scale": 6, "octaves": 2, "fernShare": 0.15, "flowerShare": 0.12,
            "flowerScale": 5, "tallShare": 0.06}},
]

refinement = {
  "authors": [{"name": "Sonnet 5.5", "contribution": "map"}], "created": "2026-10-07",
  "biome": {"kind": "solid", "id": 37},
  "shapePropsById": {"bank-20": {"vertices": LAND, "theme": "vale"}},
  "relief": relief,
  "roomStyles": {"spawn": {"library": "hay-roofed-stone-and-dark-oak-house"}},
  "themes": themes, "mapTheme": "vale",
  "addShapes": cellar, "addLayers": [roof_layer],
  "dressing": {"styles": styles, "props": props},
}

if __name__ == "__main__":
    json.dump(plan, open(os.path.join(HERE, SLUG + ".plan.json"), "w"), indent=1)
    json.dump(refinement, open(os.path.join(HERE, SLUG + ".refinement.json"), "w"), indent=1)
