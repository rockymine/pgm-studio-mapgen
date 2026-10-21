"""Write town.layers.json: the town's pieces on one sheet, each where it can be looked at.

    the byre      spruce roof in a dark oak verge and two bands, three stalls under a lean-to, its pen
    the market    three stalls with striped wool roofs
    the lamps     a torch on a cobble wall on polished andesite; a redstone lamp under a daylight sensor
    the wall      a bending curtain three thick, a walk two wide behind a crenellated parapet, two round towers
    the greenery  a cottage garden behind a fence, a hedge, a bush against a wall, flowers under a window
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda x0, y0, z0, x1, y1, z1, b: {"box": [x0, y0, z0, x1, y1, z1], "block": b}       # noqa: E731
houses = json.load(open(os.path.join(HERE, "buildings.layers.json")))
styles = {k: houses["styles"][k] for k in ("fell-cottage", "byre")}
styles["byre"] = dict(styles["byre"], verge={"roof": ["PLANKS", 5], "slab": ["WOOD_SLAB", 5]}, roof_bands=2)

build = [
    {"id": "byre", "op": "house", "at": [20, 20], "heading": 0, "L": 13, "W": 7, "storeys": 2, "style": "byre",
     "door": -1, "chimney": False},
    {"id": "byre-stalls", "op": "blocks", "boxes": [
        F(15, 41, 23, 17, 43, 23, "AIR"), F(19, 41, 23, 21, 43, 23, "AIR"), F(23, 41, 23, 25, 43, 23, "AIR"),
        F(18, 41, 23, 18, 43, 23, ["LOG", 0]), F(22, 41, 23, 22, 43, 23, ["LOG", 0]),
        F(18, 41, 18, 18, 41, 22, "FENCE"), F(22, 41, 18, 22, 41, 22, "FENCE"),
        F(15, 41, 18, 16, 41, 18, "HAY"), F(20, 41, 18, 20, 41, 18, "HAY"), F(24, 41, 18, 25, 41, 18, "HAY"),
        F(19, 46, 23, 20, 47, 23, "AIR"), F(19, 45, 22, 20, 45, 22, "HAY")]},
    {"id": "byre-lean-to", "op": "blocks", "boxes": [
        F(14, 41, 26, 14, 43, 26, ["LOG", 0]), F(18, 41, 26, 18, 43, 26, ["LOG", 0]),
        F(22, 41, 26, 22, 43, 26, ["LOG", 0]), F(26, 41, 26, 26, 43, 26, ["LOG", 0]),
        F(15, 43, 26, 17, 43, 26, ["LOG", 4]), F(19, 43, 26, 21, 43, 26, ["LOG", 4]), F(23, 43, 26, 25, 43, 26, ["LOG", 4]),
        F(13, 45, 24, 27, 45, 24, ["WOOD_SLAB", 1]), F(13, 44, 25, 27, 44, 25, ["WOOD_SLAB", 9]),
        F(13, 44, 26, 27, 44, 26, ["WOOD_SLAB", 1]), F(13, 43, 27, 27, 43, 27, ["WOOD_SLAB", 9])],
     "note": "three deep at the main roof's half-block pitch, its eave a row of upper slabs"},
    {"id": "pen", "op": "wall", "line": [[14, 29], [14, 37], [26, 37], [26, 29]], "height": 1, "blocks": ["FENCE"]},
    {"id": "pen-gate", "op": "blocks", "boxes": [F(20, 41, 37, 20, 41, 37, ["FENCE_GATE", 0])]},
    {"id": "stall-a", "op": "stall", "at": [44, 22], "facing": "s", "colours": [14, 0], "counter_stair": "SPRUCE_STAIRS", "post": ["LOG", 1], "banners": True, "sides": True},
    {"id": "stall-b", "op": "stall", "at": [52, 22], "facing": "s", "colours": [11, 0], "post": ["LOG", 1], "banners": True, "sides": True},
    {"id": "stall-c", "op": "stall", "at": [60, 22], "facing": "s", "colours": [4, 13], "post": ["LOG", 1], "banners": True, "sides": True,
     "goods": [["HAY", 0], ["PUMPKIN", 3], ["HAY", 0]]},
    {"id": "lamp-torch", "op": "posts", "at": [[70, 18], [70, 26]], "stack": [["STONE", 6], "COBBLE_WALL", ["TORCH", 5]]},
    {"id": "lamp-redstone", "op": "posts", "at": [[76, 18], [76, 26]],
     "stack": [["STONE", 6], "COBBLE_WALL", "COBBLE_WALL", "REDSTONE_LAMP", [151, 0]]},
    {"id": "garden-bush", "op": "blocks", "boxes": [F(94, 41, 16, 96, 42, 17, ["LEAVES", 4]), F(95, 43, 16, 95, 43, 16, ["LEAVES", 4])]},
    {"id": "orchard", "op": "small_trees", "at": [[90, 22], [100, 17]], "seed": 4},
    {"id": "flower-field", "op": "flowers", "area": {"polygon": [[106, 30], [120, 27], [133, 33], [129, 44], [110, 42]],
     "rough": {"amp": 0.08, "cell": 4, "seed": 3}},
     "flowers": [["FLOWER", 0], ["DANDELION", 0], ["FLOWER", 3], ["FLOWER", 8], ["FLOWER", 2]], "along": "x", "rows": 2,
     "note": "a field of flowers in the open, two rows a kind, every cell of it planted"},
    {"id": "hedge", "op": "hedge", "line": [[60, 32], [70, 30], [80, 34], [90, 31]], "seed": 2, "grass": True},
    {"id": "cottage", "op": "house", "at": [116, 20], "heading": 0, "L": 9, "W": 6, "storeys": 2, "style": "fell-cottage",
     "door": 1},
    {"id": "cottage-green", "op": "blocks", "boxes": [
        F(112, 41, 24, 113, 41, 24, ["DOUBLE_PLANT", 4]), F(112, 42, 24, 113, 42, 24, ["DOUBLE_PLANT", 8]),
        F(119, 41, 24, 120, 41, 24, ["LEAVES", 4]), F(121, 41, 23, 121, 41, 23, ["FLOWER", 1])]},
]
wall = [[10, 60], [40, 52], [70, 56], [100, 50], [130, 58]]
COURSES = ["COBBLE", ["COBBLE", ["STONE", 5]], ["STONE", 5], [["STONE", 5], ["STONEBRICK", 0]], ["STONEBRICK", 0]]
build += [
    {"id": "town-wall", "op": "wall", "line": wall, "width": 3, "height": 5, "crown": "follow",
     "courses": COURSES, "step_slab": ["SLAB", 5], "note": "the curtain, cobble at its foot into brick, its walk on top"},
    {"id": "parapet", "op": "wall", "line": wall, "offset": 1.4, "height": 6, "crown": "follow",
     "courses": COURSES, "crenel": ["SLAB", 5], "step_slab": ["SLAB", 5],
     "note": "a parapet on the outer edge, its crenels slabs"}]
for (cx, cz), a, b in (((40, 52), wall[0], wall[2]), ((100, 50), wall[2], wall[4])):
    ang = lambda p: math.degrees(math.atan2(p[1] - cz, p[0] - cx))                       # noqa: E731
    build.append({"id": f"tower-{cx}", "op": "round_tower", "at": [cx, cz], "half": 4, "height": 13, "openings_from": "floor",
                  "wall": ["STONEBRICK", 0], "door": "n", "crenel": ["SLAB", 5],
                  "openings": [[ang(a), 5], [ang(b), 5]], "floor": ["PLANKS", 1]})
doc = {"document": "layers", "version": "draft-1",
       "board": {"name": "Chantry Gill town pieces", "x": [0, 139], "z": [0, 69], "floor": 40, "height": 80, "seed": 3},
       "styles": styles, "fields": {"pen": {"fbm": {"cell": 3, "octaves": 2, "seed": 5}}},
       "ground": [{"id": "sheet", "op": "outline", "box": [0, 0, 139, 69]}, {"id": "sheet-floor", "op": "base", "height": 40},
                  {"id": "rise", "op": "mound", "mode": "lift", "rise": 4, "power": 1.5,
                   "areas": [{"ellipse": {"at": [72, 58], "rx": 40, "rz": 14}}], "note": "a swell the wall climbs over"}],
       "paint": [{"block": ["DIRT", 1], "area": {"rect": [15, 30, 25, 36]}, "noise": {"field": "pen", "lo": 0}},
                 {"block": ["DIRT", 0], "area": {"rect": [15, 30, 25, 36]}}],
       "build": build,
       "dress": []}
json.dump(doc, open(os.path.join(HERE, "town.layers.json"), "w"), indent=1)
