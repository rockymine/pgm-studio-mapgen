"""sonnet55-ember-reach — an autumn river valley, destroy-the-monument, 16 a side.

Writes the plan and the refinement beside this file. Run by tools/drive.py first.
Team 0 is the north bank (z < 0); rot_180 fans it onto the south bank.
Block ids are the studio's legacy ids: 2 grass, 3 dirt (3:1 coarse, 3:2 podzol), 1 stone (1:1 granite,
1:2 polished granite, 1:5 andesite), 4 cobble, 12 sand, 13 gravel, 24 sandstone, 5:1 spruce planks.
"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sonnet55-ember-reach"

# ── plan: the arrangement and nothing else ─────────────────────────────────────────────────────────
plan = {
  "plan": 2,
  "meta": {"name": "Ember Reach", "authors": ["Sonnet 5.5"]},
  "globals": {"cell": 4, "symmetry": "rot_180", "maxPlayers": 16, "surface": 20},
  "pieces": [
    {"id": "hall", "role": "spawn", "rect": [-3, -28, 6, 5], "surface": 20},
    {"id": "bank", "rect": [-11, -23, 22, 19], "surface": 20},
  ],
  "zones": [{"id": "river", "rect": [-11, -4, 22, 8]}],
  "placements": {
    "spawns": [{"id": "s0", "piece": "hall", "at": [12, 10], "facing": "back", "footprint": [2, 1, 20, 14]}],
    "destroyables": [{"id": "d0", "piece": "bank", "at": [30, 32], "style": "pillar-3",
                      "materials": "obsidian", "float": 4, "name": "Monument"}],
  },
  "walls": [],
}

S = lambda i, d=0: {"kind": "solid", "id": i, "data": d}
def stack(*bands, axis=None):
    out = {"kind": "layered", "stack": {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}}
    if axis: out["axis"] = axis
    return out
def cell(palette, size=3, seed=1, jitter=55, warp=1, rise=0):
    return {"kind": "cell", "seed": seed, "cellSize": size, "jitter": jitter, "warp": warp, "palette": palette, "rise": rise}
def noise(stops, scale=2, seed=1):
    return {"kind": "noise", "seed": seed, "scale": scale, "octaves": 2, "stops": stops}

# ── the paint: three families ──────────────────────────────────────────────────────────────────────
# ground  = russet turf (grass under Mesa's brown tint, podzol, dirt, coarse dirt)
# built   = granite, brick, dark-oak and hay (warm, and never the turf's own tones)
# accent  = the orange of the hay roofs and a little brick; no other
TURF = noise([S(3, 2), S(2), S(2), S(3, 1)], scale=2, seed=11)        # patches of podzol / coarse dirt in grass
BANK = cell([S(3), S(3, 1)], size=3, seed=12)                         # dirt and coarse dirt, half and half
ROCK = cell([S(1), S(1, 5), S(1), S(1, 5), S(4)], size=3, seed=13)    # stone and andesite, cobble 20%
VALLEY = {
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": S(1)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": cell([S(1), S(1, 5), S(1)], size=4, seed=14, rise=2), "fill": S(1),
    "surface": {"enabled": True, "depth": 3, "material": {
        "kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
            {"thickness": 46, "material": stack((TURF, 1), (S(3), 2))},
            {"thickness": 12, "material": stack((BANK, 1), (S(3), 2))},
            {"thickness": 32, "material": stack((ROCK, 3))}]}}},
}
BED = {
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": S(12)},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": S(24), "fill": S(24),
    "surface": {"enabled": True, "depth": 2, "material": stack((cell([S(3, 1), S(12), S(24)], size=3, seed=15), 1), (S(24), 1))},
}
YARD = {   # laid ground at the mills: granite, polished granite and andesite, a quarter each (+ granite)
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": S(1, 1)},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": S(1, 1), "fill": S(1),
    "surface": {"enabled": True, "depth": 1, "material": cell([S(1, 1), S(1, 2), S(1, 5), S(1, 1)], size=3, seed=16)},
}
THEMES = {"valley": VALLEY, "bed": BED, "yard": YARD}

# ── the relief: valley floor pinned, flanks and ground between left to the solver ─────────────────────
def rect(x0, z0, x1, z1): return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]
RELIEF = {"base": 20, "reach": 0, "step": 1, "landform": "rolling", "grain": {"amplitude": 1.6, "scale": 16, "seed": 9},
  "marks": [
    {"id": "hall-pad", "kind": "area", "h": 20, "bevel": 0, "ring": rect(-14, -110, 14, -90)},
    {"id": "monument-yard", "kind": "area", "h": 20, "bevel": 3, "ring": rect(-26, -72, 0, -48)},
    # the bank eases to the river's edge: a line of 14 along the water, lofting to the base behind it
    {"id": "waterside", "kind": "line", "points": [[-46, -17], [46, -17]], "h": [14, 14], "r": 24, "tread": 2},
    # the mill's pad, flat at the bank's own height
    {"id": "house-pad", "kind": "area", "h": 17, "bevel": 3, "ring": rect(-30, -48, -10, -32)},
    {"id": "mill-pad", "kind": "area", "h": 14, "bevel": 2, "ring": rect(4, -36, 28, -19)},
  ],
  "pushes": [
    # the valley's two sides: ground that rises toward the flanks and leaves the lane between them alone
    {"id": "west-side", "ring": rect(-52, -88, -38, -30), "amount": 9, "falloff": 14, "crown": 4, "roughness": 1, "seed": 3},
    {"id": "east-side", "ring": rect(38, -86, 52, -32), "amount": 8, "falloff": 14, "crown": 4, "roughness": 1, "seed": 4},
    # behind the spawn, the head of the valley
    {"id": "head-west", "ring": rect(-52, -112, -16, -94), "amount": 7, "falloff": 12, "crown": 3, "roughness": 1, "seed": 5},
    {"id": "head-east", "ring": rect(16, -112, 52, -94), "amount": 7, "falloff": 12, "crown": 3, "roughness": 1, "seed": 6},
    ],
}

def S_(i, **kw): d = {"id": i}; d.update(kw); return d

add_shapes = [
  # the river: ground of its own below the banks, and the water stands over it
  S_("riverbed", type="rectangle", operation="add", floor=0, base_height=4, theme="bed",
     min_x=-44, min_z=-16, max_x=44, max_z=16, group="river"),
  # the undercroft: a dugout five deep, roofed in turf, and a stair of dug steps down to it
  S_("cellar-floor", type="rectangle", operation="add", height_mode="sink", skirt=0, floor=0, base_height=5,
     theme="yard", keepClear=True, min_x=-30, min_z=-86, max_x=-20, max_z=-74),
] + [
  S_(f"cellar-step-{k}", type="rectangle", operation="add", height_mode="sink", skirt=0, floor=0,
     base_height=5 - k, theme="yard", keepClear=True,
     min_x=-20 + 2 * k, min_z=-82, max_x=-18 + 2 * k, max_z=-78)
  for k in range(5)
] + [
  S_("mill-yard", type="polygon", operation="add", floor=0, base_height=14, theme="yard",
     vertices=[[6, -34], [26, -34], [26, -21], [6, -21]], group="team"),
]
add_layers = [
  {"id": "cellar-roof", "name": "Cellar roof", "base_y": 21, "kind": "made", "part_of": "undercroft",
   "shapes": [S_("cellar-roof-slab", type="rectangle", operation="add", floor=0, base_height=1, theme="valley",
                 min_x=-31, min_z=-87, max_x=-19, max_z=-73)],
   "groups": [{"id": "cellar-roof", "name": "Cellar roof", "mirrors": True, "shapeIds": ["cellar-roof-slab"]}]},
]

# ── dressing ──────────────────────────────────────────────────────────────────────────────────────
HOUSE = lambda lib, shell=None: {"kind": "house", "library": lib} if not shell else {"kind": "house", "library": lib, "shell": shell}
STYLES = {
  "mill": {"kind": "house", "library": "dark-oak-quay-warehouse"},
  "farm": {"kind": "house", "library": "hay-roofed-stone-and-dark-oak-house"},
  "oak-9": {"kind": "tree", "form": "template", "species": "oak", "height": 9},
  "oak-13": {"kind": "tree", "form": "template", "species": "oak", "height": 13},
  "rock": {"kind": "boulder", "form": "round", "size": 3, "mossy": False,
           "rock": {"kind": "turbulence", "seed": 21, "scale": 3, "octaves": 3, "rise": 3,
                    "stops": [S(1), S(1, 5), S(4), S(1, 5)]}},
}
def wing(x0, z0, x1, z1, **spec): return {"corners": [[x0, z0], [x1, z1]], "spec": spec}
def house(i, style, wings, front, seed): return {"id": i, "kind": "house", "layer": "ground", "seed": seed, "front": front, "style": style, "wings": wings}
def tree(i, x, z, style="oak-9"): return {"id": i, "kind": "tree", "seed": 300 + abs(x * 7 + z), "x": x, "z": z, "style": style}
def rock(i, x, z): return {"id": i, "kind": "boulder", "seed": 500 + abs(x * 5 + z), "x": x, "z": z, "style": "rock"}

props = [
  # the watermill on the bank: a long hall over the water's edge and a taller wing at its back
  house("watermill", "mill", [wing(8, -33, 23, -26, ridge="alongX", storeysHigh=1),
                              wing(8, -25, 15, -20, ridge="alongZ", storeysHigh=0)], "posZ", 31),
  # the miller's house, up the lane toward the monument, and a granary the same house taller
  house("millers-house", "farm", [wing(-29, -44, -17, -35, ridge="alongX")], "posX", 32),
  house("granary", "farm", [wing(6, -76, 15, -66, ridge="alongZ", storeysHigh=1)], "negX", 33),
  # trees: a few on the valley's sides and along the water, never in the lane or at the goal
  tree("t1", -44, -64, "oak-13"), tree("t2", -41, -52), tree("t3", -40, -78, "oak-13"),
  tree("t4", 43, -62, "oak-13"), tree("t5", 41, -48), tree("t6", 40, -76),
  tree("t7", -28, -22), tree("t8", 38, -22, "oak-13"), tree("t9", -34, -92), tree("t10", 26, -88),
  rock("r1", -20, -40), rock("r2", 4, -70), rock("r3", 20, -78),
  # the road: spawn door -> monument -> mill, and the lane's own loop to the miller's house
  {"id": "road-spawn", "kind": "stroke", "seed": 41, "radius": 2, "style": "solid", "claimsGround": True,
   "wander": 2, "wanderLength": 14,
   "pave": cell([S(13), S(1, 5), S(4)], size=3, seed=17),
   "points": [[0, -90], [-4, -82], [-10, -72], [-14, -64]]},
  {"id": "road-mill", "kind": "stroke", "seed": 42, "radius": 2, "style": "solid", "claimsGround": True,
   "wander": 2, "wanderLength": 14,
   "pave": cell([S(13), S(1, 5), S(4)], size=3, seed=17),
   "points": [[-10, -52], [-2, -44], [4, -36], [10, -31]]},
  {"id": "road-house", "kind": "stroke", "seed": 43, "radius": 2, "style": "solid", "claimsGround": True,
   "wander": 2, "wanderLength": 14,
   "pave": cell([S(13), S(1, 5), S(4)], size=3, seed=17),
   "points": [[-14, -56], [-11, -50], [-11, -42], [-14, -38]]},
  {"id": "ground-cover", "kind": "flora", "seed": 61, "points": [[-44, -108], [44, -108], [44, -18], [-44, -18]],
   "spec": {"coverage": 0.32, "scale": 8, "octaves": 3, "fernShare": 0.35, "flowerShare": 0.05, "flowerScale": 12, "tallShare": 0.03}},
  # the river itself: a pool over the bed, ringed past the edge so the water meets the void
  {"id": "river", "kind": "fluid", "layer": "ground", "shape": "pool", "form": "natural", "seed": 71,
   "points": [[-48, -16], [48, -16], [48, 16], [-48, 16]], "radius": 6, "depth": 3, "level": 8, "shore": 0,
   "edge": 0, "bank": cell([S(3, 1), S(12), S(24)], size=3, seed=15), "fluid": "water"},
]

refinement = {
  "authors": ["Sonnet 5.5"], "created": "2026-10-07",
  "themes": THEMES, "mapTheme": "valley",
  "roomStyles": {"spawn": {"library": "stone-and-spruce-barn"}},
  "themeById": {},
  "biome": {"kind": "solid", "id": 37},
  "relief": {"team": RELIEF},
  "addShapes": add_shapes, "addLayers": add_layers,
  "dressing": {"styles": STYLES, "props": props},
}

json.dump(plan, open(f"{HERE}/{SLUG}.plan.json", "w"), indent=1)
json.dump(refinement, open(f"{HERE}/{SLUG}.refinement.json", "w"), indent=1)
