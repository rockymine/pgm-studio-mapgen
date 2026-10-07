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
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))
import props as sculpt  # noqa: E402

SLUG = "sonnet55b-rustwater"

# ---------------------------------------------------------------- the plan (cells of 4 blocks, team 0 north)
plan = {
  "plan": 2,
  "meta": {"name": "Rustwater Vale", "authors": ["Sonnet 5.5"]},
  "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20},
  "pieces": [
    {"id": "ridge", "rect": [-8, -29, 9, 9]},
    {"id": "fell",  "rect": [1, -29, 8, 9]},
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
    mk("watch-pad", "area", h=30, bevel=0, ring=ring(29, -92, 5, 5, 10)),
    mk("glade", "area", h=26, bevel=2, ring=ring(-14, -66, 7, 6, 10, 0.05)),
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

# made ground and made things each take a theme of their own: a tower is a thing somebody built
RUIN_WALL = cell([BRICK, BRICK, ANDESITE, COBBLE, SOLID(98, 2)], size=3, seed=15, rise=3)
PLANKS = cell([SOLID(5, 1), SOLID(5, 0), SOLID(5, 1)], size=3, seed=16, rise=2)
DRYSTONE = cell([COBBLE, ANDESITE, STONE, COBBLE], size=3, seed=17, rise=2)

def whole(material):
    return theme(material, material, material, depth=1)

themes = {
  "vale":     theme(SLOPE_STACK, STRATA, FILL),
  "yard":     theme(PAVE, STRATA, FILL),
  "ruin":     theme(PAVE, RUIN_WALL, RUIN_WALL, depth=1),
  "plank":    whole(PLANKS),
  "drystone": whole(DRYSTONE),
  "litter":   theme(layered("depth", (noise([PODZOL, COARSE, PODZOL, GRASS, PODZOL], scale=2, seed=24), 1), (DIRT, 2),
                            ending="handOver"), STRATA, FILL),
}

# ---------------------------------------------------------------- the places, planned before anything is placed
# team 0 (north); every one is fanned onto team 1 by the rot_180 orbit.
#   The Ridge        back of the board: a crest at y38..42 that curves east and becomes the fell above the goal.
#                    Walked by a ridge path from the barn yard to the Watch; scree, boulders and old oaks on its flank.
#   The Watch        a ruined round tower on the fell's crest at (29,-92), y38: the high ground over the Millstone.
#   Spawn Shelf      hall and barn at the back, a haystack yard, the lane down to the goal.
#   Millstone Terrace  the exposed goal, an open flat with the Watch above it, Haldenwood beside it, the cellar below it.
#   Haldenwood       the autumn wood on the west flank with a woodcutters' glade: hut, stumps and log piles.
#   Hamlet           the lower shelf: the cottage and the root cellar, lanes to the glade, the terrace and the mill.
#   Millrace         the valley floor: mill, miller's house, an orchard, ploughed fields behind a dry-stone wall.
#   The River        a footbridge from the mill yard to the water's edge, a jetty and a moored boat.
T = showcase.trees()
styles = {
  "oak-8":    T["oak-8"]["style"],
  "oak-6":    T["oak-6"]["style"],
  "oak-9":    T["oak-9"]["style"],
  "birch-3":  T["birch-3"]["style"],
  "birch-5":  T["birch-5"]["style"],
  "tiny-oak": T["tiny-oak-3"]["style"],
  "mill":     {"library": "dark-oak-quay-warehouse", "kind": "house"},
  "cottage":  {"library": "dark-oak-roofed-rubble-cottage", "kind": "house"},
  "barn":     {"library": "hay-gambrel-barn", "kind": "house"},
  "rock-a":   {"kind": "boulder", "form": "round", "size": 2.5, "mossy": False,
               "rock": cell([STONE, ANDESITE, STONE, COBBLE], size=2, seed=14)},
  "scree":    {"kind": "boulder", "form": "round", "size": 1.6, "mossy": False,
               "rock": cell([STONE, ANDESITE, COBBLE], size=2, seed=18)},
  "stump":    {"kind": "boulder", "form": "round", "size": 1.2, "mossy": False, "rock": SOLID(17)},
  "logpile":  {"kind": "boulder", "form": "round", "size": 2.0, "mossy": False,
               "rock": cell([SOLID(17), SOLID(17, 1), SOLID(17)], size=2, seed=19)},
  "pumpkin":  {"kind": "boulder", "form": "round", "size": 0.7, "mossy": False, "rock": SOLID(86)},
  "haystack": {"kind": "boulder", "form": "round", "size": 1.9, "mossy": False, "rock": SOLID(170)},
}

def house(i, style, corners, front, seed, ridge="alongX"):
    return {"id": i, "kind": "house", "layer": "ground", "seed": seed, "front": front, "style": style,
            "wings": [{"corners": corners, "spec": {"ridge": ridge}}]}

def tree(i, style, x, z, seed):
    return {"id": i, "kind": "tree", "seed": seed, "x": x, "z": z, "style": style}

def rock(i, style, x, z, seed):
    return {"id": i, "kind": "boulder", "seed": seed, "x": x, "z": z, "style": style}

props = [
  {"id": "river", "kind": "fluid", "layer": "ground", "shape": "channel", "form": "stream",
   "points": [[-26,-20],[-6,-19.5],[14,-21],[24,-26]], "radius": 5, "depth": 2, "level": 13,
   "shore": 3, "shoreWander": True, "edge": 1.5,
   "bank": cell([SOLID(13), SOLID(12), COARSE], size=3, seed=12)},
  # buildings: one row of rubble cottages, one mill, one barn
  house("mill", "mill", [[-12,-34],[-3,-28]], "negZ", 101),
  house("cottage", "cottage", [[-14,-54],[-5,-47]], "posZ", 102),
  house("barn", "barn", [[-6,-102],[3,-95]], "posZ", 103),
  house("miller", "cottage", [[5,-37],[12,-32]], "negZ", 104),
]

# ---- paths: every route a player or a villager takes; hard ground, so gravel, andesite and cobblestone
HARD = cell([SOLID(13), ANDESITE, COBBLE], size=3, seed=21)
def path(i, pts, seed, radius=2.2, wander=2.0):
    return {"id": i, "kind": "stroke", "layer": "ground", "points": pts, "radius": radius, "style": "solid",
            "claimsGround": True, "seed": seed, "wander": wander, "wanderLength": 14, "pave": HARD}
props += [
  path("way-hall-goal",   [[-20,-84],[-13,-78],[-3,-73],[6,-68]], 31),
  path("way-hall-barn",   [[-18,-86],[-10,-90],[-3,-92.5]], 32),
  path("way-ridge",       [[-3,-92.5],[5,-93],[12,-96],[18,-97],[23,-95],[26,-93]], 33, radius=1.8),
  path("way-watch-goal",  [[28,-88],[30,-82],[29,-75],[26,-68]], 34, radius=1.8),
  path("way-goal-hamlet", [[10,-60],[6,-54],[1,-48],[-4,-44],[-9,-43.5]], 35),
  path("way-hamlet-mill", [[-9,-43.5],[-8,-40],[-8,-37]], 36, wander=1.5),
  path("way-cellar",      [[2,-52],[10,-52],[21,-49]], 37, radius=1.8, wander=1.0),
  path("way-glade",       [[-6,-75],[-6,-70],[-9,-67],[-12,-66.5]], 38, radius=1.8, wander=1.0),
  path("way-glade-low",   [[-9,-67],[-8,-62],[-6,-57]], 42, radius=1.8, wander=1.0),
  path("way-miller",      [[-8,-37],[0,-38.5],[7,-38.5]], 39, radius=1.8, wander=1.0),
  path("way-fields",      [[7,-38.5],[16,-39],[27,-39]], 40, radius=1.6, wander=1.0),
  path("way-bridge",      [[-8,-37],[-13,-33],[-12,-27],[-9,-26]], 41, radius=1.8, wander=1.0),
]

# ---- ploughed fields behind the mill, and the wall that keeps the sheep out of them
TILL_A = cell([COARSE, DIRT, COARSE], size=2, seed=22)
TILL_B = cell([PODZOL, COARSE, DIRT], size=2, seed=23)
for k, (zc, pv) in enumerate([(-33.5, TILL_A), (-30.5, TILL_B), (-27.5, TILL_A)]):
    props.append({"id": f"furrow-{k}", "kind": "stroke", "layer": "ground", "points": [[16,zc],[22,zc+0.4],[28,zc]],
                  "radius": 1.0, "style": "solid", "claimsGround": True, "seed": 50 + k, "pave": pv})

# ---- the wood, the glade, the orchard and the hill; each tree stands for a reason
props += [
  # Haldenwood, west flank, closing the terrace's west side
  tree("w1", "oak-8", -24, -60, 301),
  # the orchard on the valley floor, west of the mill
  tree("o1", "tiny-oak", -19, -36, 311), tree("o2", "tiny-oak", -18, -28, 312),
  # old oaks on the ridge, and one beside the Watch
  tree("r1", "oak-8", 8, -111, 321), tree("r2", "oak-9", 20, -104, 322), tree("r6", "birch-3", 20, -91, 326),
  # banks
  tree("b1", "oak-6", 25, -42, 331),
  # the woodcutters' glade: stumps where trees were taken, logs stacked by the hut
  rock("s1", "stump", -10, -62, 341), rock("s2", "stump", -9, -69, 342), rock("s3", "stump", -13, -58, 343),
  rock("s4", "stump", -8, -64, 344), rock("lp1", "logpile", -18, -64, 345), rock("lp2", "logpile", -19, -45.5 if False else -57, 346),
  # the pumpkin patch between the furrows
  rock("p1", "pumpkin", 18, -32, 371), rock("p2", "pumpkin", 22, -32, 372), rock("p3", "pumpkin", 26, -32, 373),
  rock("p4", "pumpkin", 20, -29, 374),
  # haystacks in the barn yard
  rock("h1", "haystack", 7, -102, 351), rock("h2", "haystack", 8, -99, 352),
  # the ridge's rock: scree under the Watch and boulders on the crest
  rock("k1", "rock-a", 14, -108, 361), rock("k2", "rock-a", 24, -100, 362), rock("k3", "scree", 24, -82, 363),
  rock("k4", "scree", 31, -78, 364),
  {"id": "watch-chest", "kind": "chest", "x": 29, "z": -91, "y": 40, "facing": "posZ",
   "items": [{"item": "golden apple", "count": 2}, {"item": "arrow", "count": 16}]},
  {"id": "meadow", "kind": "flora", "layer": "ground",
   "points": [[-30,-110],[30,-110],[44,-78],[46,-64],[30,-30],[20,-13],[-24,-14],[-26,-56],[-31,-85]],
   "spec": {"coverage": 0.2, "scale": 6, "octaves": 2, "fernShare": 0.12, "flowerShare": 0.1,
            "flowerScale": 5, "tallShare": 0.05}},
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

# ---------------------------------------------------------------- dry-stone walls on the flat valley floor
def wall(i, pts):
    return {"id": i, "type": "polyline", "operation": "add", "vertices": pts, "radius": 0.7,
            "stroke_edge": "solid", "height_mode": "raise", "base_height": 2, "skirt": 0,
            "theme": "drystone", "keepClear": True, "group": "team", "layer": "ground"}

def patch(i, cx, cz, rx, rz, h, seed=0):
    return {"id": i, "type": "polygon", "operation": "add", "vertices": ring(cx, cz, rx, rz, 12, 0.18, seed),
            "base_height": h, "theme": "litter", "group": "team", "layer": "ground"}

litter = [patch("litter-glade", -14, -66, 6.5, 5.5, 26, 0.3), patch("litter-orchard", -18, -32, 7, 7, 14, 0.9)]
walls = [wall("field-wall-n", [[14,-36.5],[22,-37],[29,-36.5]]), wall("field-wall-e", [[29,-36.5],[29.5,-31],[29,-26]])]

# ---------------------------------------------------------------- made things: the Watch, the footbridge, the boat
L = sculpt.LayerBuilder
watch_shaft = sculpt.ring_wall("watch", 29, -92, 3.7, 1.4, 0, 7, "ruin", doors=((180, 2.2),), inner_floor="ruin",
                               points=40, base_y=39, name="Watch")
crown = L("watch-crown", name="Watch crown", base_y=39)
for i in range(5):
    a0 = 2*math.pi*(i + 0.15)/5 + math.pi/5      # five merlons, none over the doorway at 180°
    a1 = a0 + math.pi/6
    arc = [(29 + 4.0*math.cos(a), -92 + 4.0*math.sin(a)) for a in (a0 + (a1 - a0)*k/4 for k in range(5))]
    arc += [(29 + 2.3*math.cos(a), -92 + 2.3*math.sin(a)) for a in (a1 - (a1 - a0)*k/4 for k in range(5))]
    crown.poly(arc, 7, 2, "ruin")

bridge = L("footbridge", name="Footbridge", base_y=14)
bridge.rect(-10, -27, -8, -12.5, 0, 1, "plank", keepClear=False)
bridge.rect(-11, -27, -10, -12.5, 0, 2, "plank", keepClear=False)
bridge.rect(-8, -27, -7, -12.5, 0, 2, "plank", keepClear=False)
jetty = L("jetty", name="Jetty and boat", base_y=14)
jetty.rect(-21, -27, -19, -21, 0, 1, "plank", keepClear=False)
jetty.rect(-17, -23, -13, -22, 0, 1, "plank", keepClear=False)            # the boat's bottom
jetty.rect(-17, -24, -13, -23, 0, 2, "plank", keepClear=False)            # its two sides
jetty.rect(-17, -22, -13, -21, 0, 2, "plank", keepClear=False)
jetty.rect(-18, -24, -17, -21, 0, 2, "plank", keepClear=False)            # its stem

def flat(layer):
    if "layout" not in layer:
        return layer
    out = {"id": layer["id"], "name": layer["name"], "base_y": layer["base_y"],
           "shapes": layer["layout"]["shapes"], "groups": layer["layout"]["groups"]}
    if layer["id"].startswith("watch"):          # a landmark standing in the hill: no gap to lose, no stair forgotten
        out.update({"kind": "made", "part_of": "ground"})
    return out

refinement_layers = sorted([flat(x) for x in [roof_layer, watch_shaft, crown.done(), bridge.done(), jetty.done()]],
                           key=lambda l: l["base_y"])

refinement = {
  "authors": [{"name": "Sonnet 5.5", "contribution": "map"}], "created": "2026-10-07",
  "biome": {"kind": "solid", "id": 37},
  "shapePropsById": {"bank-20": {"vertices": LAND, "theme": "vale"}},
  "relief": relief,
  "roomStyles": {"spawn": {"library": "dark-oak-roofed-rubble-cottage"}},
  "themes": themes, "mapTheme": "vale",
  "addShapes": cellar + walls + litter, "addLayers": refinement_layers,
  "dressing": {"styles": styles, "props": props},
}

if __name__ == "__main__":
    json.dump(plan, open(os.path.join(HERE, SLUG + ".plan.json"), "w"), indent=1)
    json.dump(refinement, open(os.path.join(HERE, SLUG + ".refinement.json"), "w"), indent=1)
