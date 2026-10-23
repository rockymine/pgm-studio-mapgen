"""Write street.layers.json: the settlement put together, on ground that rises gently to the south.

    the street    from the north gate past the inn, through the square, up to the south gate, a lane east off
                  the square to the byre and the east gate; laid in cells of gravel, andesite and cobble
    the square    paved in stone bricks and three andesites, a quarter each; the monument in its open west half,
                  the chapel on its west side (its tower door onto the square), three stalls along its east edge
    the houses    long side to the street and door onto it, never nearer than three blocks roof to roof
    the wall      three runs between the gates, cobble into brick, four towers at its bends
    the green     small oaks in back gardens, a hedge down the lane, roses at doors, a flower field outside
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda x0, y0, z0, x1, y1, z1, b: {"box": [x0, y0, z0, x1, y1, z1], "block": b}       # noqa: E731
town = json.load(open(os.path.join(HERE, "town.layers.json")))
bld = json.load(open(os.path.join(HERE, "buildings.layers.json")))
styles = {k: bld["styles"][k] for k in ("fell-cottage", "fell-cottage-dark", "chapel-stone", "byre")} \
    if "fell-cottage-dark" in bld["styles"] else {}
hs = json.load(open(os.path.join(HERE, "houses.layers.json")))["styles"]
styles["fell-cottage"], styles["fell-cottage-dark"] = hs["fell-cottage"], hs["fell-cottage-dark"]
for k in ("chapel-stone", "byre"):
    styles[k] = town["styles"].get(k, bld["styles"][k])
for k in ("fell-cottage", "fell-cottage-dark", "chapel-stone", "byre"):
    styles[k]["ridge_slab"] = True
styles["byre"] = {k: v for k, v in styles["byre"].items() if k not in ("verge", "roof_bands", "slab_roof")}
styles["byre"].update(roof=["PLANKS", 5], stair="DARK_OAK_STAIRS", slab=["WOOD_SLAB", 5])
for k in ("fell-cottage", "fell-cottage-dark"):
    styles[k]["plinth"] = "COBBLE"
for k in ("fell-cottage", "fell-cottage-dark"):
    styles[k].update(stack={"block": "COBBLE", "base": "COBBLE_STAIRS"}, chimney="COBBLE", joists_along=True,
                     chimney_top=["IRON_BARS", ["SLAB", 0], ["STAINED_GLASS", 7], ["STAINED_GLASS", 8]])
SMOKE = styles["fell-cottage"]["chimney_top"]
QUOINS = [["STONE", 5], ["STONE", 6]]
COURSES = ["COBBLE", ["COBBLE", ["STONE", 5]], ["STONE", 5], [["STONE", 5], ["STONEBRICK", 0]], ["STONEBRICK", 0]]

MAIN = [[50, -2], [49, 14], [51, 26], [52, 38], [51, 52], [53, 64], [54, 86]]
LANE = [[60, 36], [72, 31], [86, 28], [98, 26], [110, 30], [118, 34]]
FIELD = [[116, 12], [140, 18], [142, 40], [122, 46], [114, 30]]
SQUARE = [[42, 30], [60, 28], [66, 36], [63, 47], [44, 48], [40, 40]]
ground = [
    {"id": "sheet", "op": "outline", "box": [0, -4, 149, 89]},
    {"id": "fell", "op": "base", "height": 40,
     "terms": [{"tilt": {"dx": 0.025, "dz": 0.045}}, {"gauss": {"at": [96, 92], "r": 46, "rise": 5}},
               {"noise": {"field": "small", "rise": 0.9}}, {"noise": {"field": "big", "rise": 1.6}}],
     "note": "the ground rising toward the south-east, a swell under its corner, rolling"},
    {"id": "square-level", "op": "level", "mode": "set", "top": "median", "inner": 1.0, "outer": 1.6,
     "areas": [{"polygon": SQUARE}], "note": "the square laid level, eased into the street"},
    {"id": "field-level", "op": "level", "mode": "set", "top": "median", "inner": 1.0, "outer": 1.5,
     "areas": [{"polygon": FIELD}], "note": "the field laid level, so its ditches hold their water"},
    {"id": "main-street", "op": "path", "line": MAIN, "width": 4, "max_grade": 0.15},
    {"id": "lane", "op": "path", "line": LANE, "width": 3, "max_grade": 0.2}]


WALK = {"blocks": [["DIRT", 1], "GRAVEL", ["DIRT", 0]], "leaves": ["LEAVES", 4], "side": "left", "gaps": 0.25}


def house(id_, at, heading, L, W, n, style, door, to="main-street", **kw):
    walk = {} if to is None else {"walk": dict(WALK, to=to)}
    return dict(id=id_, op="house", at=at, heading=heading, L=L, W=W, storeys=n, style=style, door=door, **walk, **kw)


build = [
    {"id": "street-pave", "op": "paving", "area": {"line": {"near": "main-street", "width": 4}}, "cell": 1,
     "blocks": ["GRAVEL", ["STONE", 5], "COBBLE"], "seed": 2, "note": "a third each of gravel, andesite and cobble"},
    {"id": "lane-pave", "op": "paving", "area": {"line": {"near": "lane", "width": 3}}, "cell": 1,
     "blocks": ["GRAVEL", ["STONE", 5], "COBBLE"], "seed": 3},
    {"id": "square-pave", "op": "paving", "area": {"polygon": SQUARE}, "cell": 3,
     "blocks": [["STONEBRICK", 0], ["STONE", 6], ["STONE", 5], ["STONE", 0]], "seed": 4,
     "note": "a quarter each, in cells of three"},
    # the chapel on the square's west side, its tower at the north end with its door east onto the square
    house("nave", [32, 40], 90, 15, 9, 1, "chapel-stone", 0, to=None, storey=6, chimney=False),
    {"id": "chapel-tower", "op": "round_tower", "at": [32, 30], "half": 2, "cut": False, "height": 15,
     "wall": ["STONEBRICK", 0], "quoins": QUOINS, "string": ["STONE", 6], "plinth": "COBBLE", "crenel": ["SLAB", 5],
     "door": "e", "floor": ["PLANKS", 1]},
    {"id": "chapel-door", "op": "blocks", "boxes": [F(32, 43, 32, 32, 44, 33, "AIR")],
     "note": "the way from the tower into the nave, two high through both walls"},
    # east of the street: door west (heading 90, door 1); west of it: door east (door -1)
    house("inn", [58, 12], 90, 13, 7, 2, "fell-cottage", 1, jetty=True, note="the inn by the north gate"),
    house("cooper", [41, 13], 90, 9, 6, 2, "fell-cottage-dark", -1),
    house("east-row-1", [60, 55], 90, 9, 6, 2, "fell-cottage", 1),
    house("east-row-2", [62, 70], 90, 9, 6, 1, "fell-cottage-dark", 1),
    house("west-row-1", [43, 57], 90, 9, 6, 2, "fell-cottage", -1),
    house("west-row-2", [45, 71], 90, 11, 7, 2, "fell-cottage-dark", -1, jetty=True),
    # the lane: houses on its north side face south onto it, one turned with it
    house("lane-1", [72, 22], -15, 9, 6, 2, "fell-cottage", 1, to="lane"),
    house("lane-2", [86, 18], 0, 9, 6, 1, "fell-cottage-dark", 1, to="lane"),
]
# the byre at the lane's end, south of it: door north onto the lane, stalls south onto its pen
dx, dz, dy = 60, 20, 0
for L in town["build"]:
    if L["id"] in ("byre", "byre-stalls", "byre-lean-to", "pen", "pen-gate"):
        L = json.loads(json.dumps(L))
        if "at" in L:
            L["at"] = [L["at"][0] + dx, L["at"][1] + dz]
        if L["id"] == "byre":
            L["walk"] = dict(WALK, to="lane")
        if L["op"] == "blocks" and L["id"] != "pen-gate":
            L["rel"] = "byre"                    # its heights over the byre's floor, which stood at 40 on its sheet
        for b in L.get("boxes", []):
            x0, y0, z0, x1, y1, z1 = b["box"]
            dy = -40 if L.get("rel") else 0
            b["box"] = [x0 + dx, y0 + dy, z0 + dz, x1 + dx, y1 + dy, z1 + dz]
        if "line" in L:
            L["line"] = [[x + dx, z + dz] for x, z in L["line"]]
        if L["id"] == "pen-gate":
            L = {"id": "pen-gate", "op": "posts", "at": [[80, 57]], "stack": [["FENCE_GATE", 0]]}
        build.append(L)
build += [
    {"id": "stall-a", "op": "stall", "at": [62, 32], "facing": "w", "colours": [14, 0], "post": ["DARK_OAK_FENCE", 0],
     "foot": ["LOG2", 1], "counter_stair": "SPRUCE_STAIRS", "banners": True, "sides": True},
    {"id": "stall-b", "op": "stall", "at": [62, 40], "facing": "w", "colours": [11, 0], "post": ["DARK_OAK_FENCE", 0],
     "foot": ["LOG2", 1], "counter_stair": "SPRUCE_STAIRS", "banners": True, "sides": True},
    {"id": "stall-c", "op": "stall", "at": [54, 46], "facing": "n", "colours": [4, 13], "post": ["DARK_OAK_FENCE", 0],
     "foot": ["LOG2", 1], "counter_stair": "SPRUCE_STAIRS", "banners": True, "sides": True,
     "goods": [["HAY", 0], ["PUMPKIN", 3], ["HAY", 0]]},
    {"id": "monument", "op": "posts", "at": [[45, 39]], "stack": ["AIR", "AIR", "AIR", "OBSIDIAN", "OBSIDIAN", "OBSIDIAN"],
     "note": "the monument, three of obsidian floating three over the square"},
    {"id": "street-lamps", "op": "posts", "at": [[46, 6], [53, 20], [47, 31], [57, 50], [48, 62], [57, 76]],
     "stack": [["STONE", 6], "COBBLE_WALL", ["TORCH", 5]]},
    {"id": "square-lamps", "op": "posts", "at": [[43, 33], [59, 44]],
     "stack": [["STONE", 6], "COBBLE_WALL", "COBBLE_WALL", "REDSTONE_LAMP", [151, 0]]},
    {"id": "lane-hedge", "op": "hedge", "line": [[68, 34], [80, 32], [90, 31]], "offset": 0, "seed": 5, "grass": True,
     "note": "the hedge along the lane's south side, between it and the byre's yard"},
    {"id": "gardens", "op": "small_trees", "at": [[33, 14], [69, 56], [71, 68], [38, 74]], "seed": 6},
    {"id": "orchard", "op": "small_trees", "seed": 7, "note": "the open ground where the wall has fallen, planted",
     "at": [[12, 40], [8, 52], [14, 64], [22, 72], [10, 76], [28, 84], [64, 84], [76, 78], [86, 72], [96, 70]]},
    {"id": "graveyard-wall", "op": "wall", "line": [[39, 51], [39, 49], [25, 49], [25, 60], [39, 60], [39, 55]],
     "height": 1, "blocks": ["COBBLE_WALL"], "note": "a low wall round the churchyard, its gate onto the street"},
    {"id": "graves", "op": "graves", "facing": "e", "seed": 8, "flowered": 0.45,
     "flowers": [["FLOWER", 0], ["FLOWER", 3], ["DANDELION", 0], ["FLOWER", 8]],
     "at": [[x, z] for z in (51, 53, 55, 57) for x in (27, 31, 35)][:-1],
     "note": "headstones of polished andesite under a slab, the grave in coarse dirt before each, flowers on some"},
    {"id": "roses", "op": "blocks", "boxes": [F(55, 0, 9, 55, 0, 9, "AIR")]},
    {"id": "flower-field", "op": "flowers", "angle": -24, "rows": 2,
     "area": {"polygon": [[104, 74], [122, 66], [136, 74], [130, 88], [110, 88]], "rough": {"amp": 0.08, "cell": 4, "seed": 3}},
     "flowers": [["FLOWER", 0], ["DANDELION", 0], ["FLOWER", 3], ["FLOWER", 8], ["FLOWER", 2]],
     "note": "a meadow of flowers down the slope south-east of the town, its rows across the fall"},
    {"id": "byre-field", "op": "crops", "angle": 18, "rows": 6, "ditch": 3, "seed": 9,
     "area": {"polygon": FIELD},
     "crops": [["WHEAT", 7], ["CARROTS", 7], ["POTATOES", 7]], "scarecrows": [[130, 20]],
     "note": "the byre's field out past the east gate, the lane running on to it, its strips turned with the hill"},
]
# the wall faces the way an enemy comes, north and east, and has fallen down the town's flanks
WALLS = [([[54, -1], [76, 4], [96, 14], [99, 22]], None, -1.4),
         ([[99, 31], [100, 42], [92, 62], [80, 74]], [22, 52, 4], -1.4),
         ([[45, -1], [22, 10], [17, 32], [18, 54]], [34, 66, 5], 1.4)]
for n, (line, ruin, out) in enumerate(WALLS):
    r = {"ruin": ruin} if ruin else {}
    build += [
        {"id": f"wall-{n}", "op": "wall", "line": line, "width": 3, "height": 5, "crown": "follow", "courses": COURSES,
         "step_slab": ["SLAB", 5], **r},
        {"id": f"parapet-{n}", "op": "wall", "line": line, "offset": out, "height": 6, "crown": "follow",
         "courses": COURSES, "crenel": ["SLAB", 5], "step_slab": ["SLAB", 5], **r}]
import math
for n, (at, door, a, b) in enumerate((([96, 14], "s", [76, 4], [99, 22]), ([22, 10], "e", [45, -1], [17, 32]))):
    ang = lambda p: math.degrees(math.atan2(p[1] - at[1], p[0] - at[0]))                   # noqa: E731
    build.append({"id": f"tower-{n}", "op": "round_tower", "at": at, "half": 3, "height": 10, "wall": ["STONEBRICK", 0],
                  "openings": [[ang(a), 5], [ang(b), 5]], "openings_from": "floor",
                  "door": door, "crenel": ["SLAB", 5], "quoins": QUOINS, "string": ["STONE", 6], "plinth": "COBBLE",
                  "floor": ["PLANKS", 1]})
doc = {"document": "layers", "version": "draft-1",
       "board": {"name": "Chantry Gill street", "x": [0, 149], "z": [-4, 89], "floor": 40, "height": 84, "seed": 3},
       "styles": styles, "fields": {"pen": {"fbm": {"cell": 3, "octaves": 2, "seed": 5}},
                                    "small": {"fbm": {"cell": 10, "octaves": 3, "seed": 1}},
                                    "big": {"fbm": {"cell": 32, "octaves": 3, "seed": 2}}},
       "ground": ground,
       "paint": [{"block": ["DIRT", 1], "area": {"rect": [75, 50, 85, 56]}, "noise": {"field": "pen", "lo": 0}},
                 {"block": ["DIRT", 0], "area": {"rect": [75, 50, 85, 56]}}],
       "carve": [{"id": "crypt", "op": "rooms", "seed": 11,
                  "rooms": [{"id": "crypt", "rect": [29, 34, 35, 46], "floor": 30, "h": 5}],
                  "lining": {"wall": [[["STONEBRICK", 0], 6], [["STONEBRICK", 2], 1]],
                             "floor": [[["STONEBRICK", 0], 1], [["STONE", 6], 1], [["STONE", 5], 1], [["STONE", 0], 1]],
                             "ceiling": "STONEBRICK"}, "light": {"y": 2}},
                 {"id": "crypt-shaft", "op": "shaft", "at": [33, 44], "bottom": 30, "top": "ground", "ladder_on": "s",
                  "wall": ["STONEBRICK", 0], "post": ["STONEBRICK", 0]}],
       "build": [L for L in build if L["id"] != "roses"]}
json.dump(doc, open(os.path.join(HERE, "street.layers.json"), "w"), indent=1)
