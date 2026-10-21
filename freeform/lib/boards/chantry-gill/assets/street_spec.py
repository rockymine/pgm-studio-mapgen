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
for k in ("fell-cottage", "fell-cottage-dark"):
    styles[k].update(stack={"block": "COBBLE", "base": "COBBLE_STAIRS"}, chimney="COBBLE", joists_along=True,
                     chimney_top=["IRON_BARS", ["SLAB", 0], ["STAINED_GLASS", 7], ["STAINED_GLASS", 8]])
SMOKE = styles["fell-cottage"]["chimney_top"]
QUOINS = [["STONE", 5], ["STONE", 6]]
COURSES = ["COBBLE", ["COBBLE", ["STONE", 5]], ["STONE", 5], [["STONE", 5], ["STONEBRICK", 0]], ["STONEBRICK", 0]]

MAIN = [[50, -2], [49, 14], [51, 26], [52, 38], [51, 52], [53, 64], [54, 86]]
LANE = [[60, 36], [72, 31], [86, 28], [98, 26]]
SQUARE = [[42, 30], [60, 28], [66, 36], [63, 47], [44, 48], [40, 40]]
ground = [
    {"id": "sheet", "op": "outline", "box": [0, -4, 129, 89]},
    {"id": "fell", "op": "base", "height": 40, "terms": [{"ramp": {"along": "z", "from": 0, "to": 84, "rise": 5}}],
     "note": "the ground rising five blocks from the north gate to the south"},
    {"id": "square-level", "op": "level", "mode": "set", "top": "median", "inner": 1.0, "outer": 1.6,
     "areas": [{"polygon": SQUARE}], "note": "the square laid level, eased into the street"},
    {"id": "main-street", "op": "path", "line": MAIN, "width": 4, "max_grade": 0.15},
    {"id": "lane", "op": "path", "line": LANE, "width": 3, "max_grade": 0.2}]


def house(id_, at, heading, L, W, n, style, door, **kw):
    return dict(id=id_, op="house", at=at, heading=heading, L=L, W=W, storeys=n, style=style, door=door, **kw)


build = [
    {"id": "street-pave", "op": "paving", "area": {"line": {"near": "main-street", "width": 4}}, "cell": 1,
     "blocks": ["GRAVEL", ["STONE", 5], "COBBLE"], "seed": 2, "note": "a third each of gravel, andesite and cobble"},
    {"id": "lane-pave", "op": "paving", "area": {"line": {"near": "lane", "width": 3}}, "cell": 1,
     "blocks": ["GRAVEL", ["STONE", 5], "COBBLE"], "seed": 3},
    {"id": "square-pave", "op": "paving", "area": {"polygon": SQUARE}, "cell": 3,
     "blocks": [["STONEBRICK", 0], ["STONE", 6], ["STONE", 5], ["STONE", 0]], "seed": 4,
     "note": "a quarter each, in cells of three"},
    # the chapel on the square's west side, its tower at the north end with its door east onto the square
    house("nave", [32, 40], 90, 15, 9, 1, "chapel-stone", 0, storey=6, chimney=False),
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
    house("lane-1", [72, 22], -15, 9, 6, 2, "fell-cottage", 1),
    house("lane-2", [86, 18], 0, 9, 6, 1, "fell-cottage-dark", 1),
]
# the byre at the lane's end, south of it: door north onto the lane, stalls south onto its pen
dx, dz, dy = 60, 20, 3                     # the byre's floor stands at 43 here, three over the sheet's
for L in town["build"]:
    if L["id"] in ("byre", "byre-stalls", "byre-lean-to", "pen", "pen-gate"):
        L = json.loads(json.dumps(L))
        if "at" in L:
            L["at"] = [L["at"][0] + dx, L["at"][1] + dz]
        for b in L.get("boxes", []):
            x0, y0, z0, x1, y1, z1 = b["box"]
            b["box"] = [x0 + dx, y0 + dy, z0 + dz, x1 + dx, y1 + dy, z1 + dz]
        if "line" in L:
            L["line"] = [[x + dx, z + dz] for x, z in L["line"]]
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
    {"id": "gardens", "op": "small_trees", "at": [[33, 14], [35, 60], [69, 56], [71, 68], [38, 73]], "seed": 6},
    {"id": "roses", "op": "blocks", "boxes": [F(55, 0, 9, 55, 0, 9, "AIR")]},
    {"id": "flower-field", "op": "flowers", "area": {"polygon": [[100, 52], [114, 49], [124, 56], [118, 68], [102, 66]],
     "rough": {"amp": 0.08, "cell": 4, "seed": 3}},
     "flowers": [["FLOWER", 0], ["DANDELION", 0], ["FLOWER", 3], ["FLOWER", 8], ["FLOWER", 2]], "rows": 2},
    {"id": "byre-field", "op": "field", "rect": [100, 30, 120, 46], "crops": [["WHEAT", 7], ["CARROTS", 7], ["POTATOES", 7]],
     "rows": 6, "ditch": 3, "fence": "w", "scarecrows": [[110, 30]]},
]
WALLS = [[[54, -1], [76, 4], [96, 14], [99, 22]],
         [[99, 31], [100, 42], [92, 62], [74, 80], [58, 84]],
         [[49, 84], [30, 78], [18, 58], [17, 32], [22, 10], [45, -1]]]
for n, line in enumerate(WALLS):
    build += [
        {"id": f"wall-{n}", "op": "wall", "line": line, "width": 3, "height": 5, "crown": "follow", "courses": COURSES,
         "step_slab": ["SLAB", 5]},
        {"id": f"parapet-{n}", "op": "wall", "line": line, "offset": -1.4, "height": 6, "crown": "follow",
         "courses": COURSES, "crenel": ["SLAB", 5], "step_slab": ["SLAB", 5]}]
for n, (at, door) in enumerate((([96, 14], "s"), ([92, 62], "n"), ([18, 58], "e"), ([22, 10], "e"))):
    build.append({"id": f"tower-{n}", "op": "round_tower", "at": at, "half": 4, "height": 13, "wall": ["STONEBRICK", 0],
                  "door": door, "crenel": ["SLAB", 5], "quoins": QUOINS, "string": ["STONE", 6], "plinth": "COBBLE",
                  "floor": ["PLANKS", 1]})
doc = {"document": "layers", "version": "draft-1",
       "board": {"name": "Chantry Gill street", "x": [0, 129], "z": [-4, 89], "floor": 40, "height": 84, "seed": 3},
       "styles": styles, "fields": {"pen": {"fbm": {"cell": 3, "octaves": 2, "seed": 5}}},
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
