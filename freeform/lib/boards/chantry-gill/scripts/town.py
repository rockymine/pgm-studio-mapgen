"""Chantry Gill's town and everything made on the fell and the Scar, as layer-document layers in blue's half.

    ground()     the ways graded into the ground: the street, the lane, the brig road, the back road, the bench path,
                 the square levelled
    carve()      the crypt under the chapel and the adit from the shelter under the gill into it, a ladder up
    build()      paving, houses, the chapel, the byre, stalls, lamps, the wall at the front, the spawn's hall
    dress()      gardens, orchards, a copse on the edge bench, boulders, flowers, a field
    STYLES       the house styles, from the asset sheets
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
F = lambda x0, y0, z0, x1, y1, z1, b: {"box": [x0, y0, z0, x1, y1, z1], "block": b}      # noqa: E731

_hs = json.load(open(os.path.join(ASSETS, "houses.layers.json")))["styles"]
_bs = json.load(open(os.path.join(ASSETS, "buildings.layers.json")))["styles"]
SMOKE = ["IRON_BARS", ["SLAB", 0], ["STAINED_GLASS", 7], ["STAINED_GLASS", 8]]
STYLES = {k: dict(_hs[k], stack={"block": "COBBLE", "base": "COBBLE_STAIRS"}, chimney="COBBLE", plinth="COBBLE",
                  joists_along=True, chimney_top=SMOKE, ridge_slab=True) for k in ("fell-cottage", "fell-cottage-dark")}
STYLES["chapel-stone"] = dict(_bs["chapel-stone"], ridge_slab=True)
STYLES["byre"] = {k: v for k, v in _bs["byre"].items() if k not in ("verge", "roof_bands", "slab_roof")}
STYLES["byre"].update(roof=["PLANKS", 5], stair="DARK_OAK_STAIRS", slab=["WOOD_SLAB", 5], ridge_slab=True)
QUOINS = [["STONE", 5], ["STONE", 6]]
COURSES = ["COBBLE", ["COBBLE", ["STONE", 5]], ["STONE", 5], [["STONE", 5], ["STONEBRICK", 0]], ["STONEBRICK", 0]]
PAVE = ["GRAVEL", ["STONE", 5], "COBBLE"]

MAIN = [[-6, 12], [-8, 30], [-11, 44], [-13, 50]]
SOUTH = [[-6, 64], [-4, 74], [0, 84], [4, 92]]
SQUARE = [[-24, 48], [-6, 46], [0, 54], [-2, 64], [-20, 66], [-27, 58]]
LANE = [[-25, 56], [-36, 50], [-44, 46]]
BRIG_ROAD = [[-1, 52], [12, 46], [22, 40], [28, 38]]
FAR_ROAD = [[41, 38], [48, 42], [52, 52], [54, 64], [53, 74]]
BACK_ROAD = [[6, 94], [18, 93], [30, 92]]
FIELD = [[-58, 22], [-34, 18], [-28, 30], [-46, 36], [-60, 32]]
TOWN_MONUMENT, SCAR_MONUMENT = (-14, 57), (54, 82)


def ground():
    return [
        {"id": "square-level", "op": "level", "mode": "set", "top": "median", "inner": 1.0, "outer": 1.6,
         "areas": [{"polygon": SQUARE}], "note": "the market square laid level"},
        {"id": "field-level", "op": "level", "mode": "set", "top": "median", "inner": 1.0, "outer": 1.5,
         "areas": [{"polygon": FIELD}], "note": "the field laid level for its ditches"},
        {"id": "main-street", "op": "path", "line": MAIN, "width": 4, "max_grade": 0.15},
        {"id": "south-street", "op": "path", "line": SOUTH, "width": 4, "max_grade": 0.15},
        {"id": "lane", "op": "path", "line": LANE, "width": 3, "max_grade": 0.2},
        {"id": "brig-road", "op": "path", "line": BRIG_ROAD, "width": 3, "max_grade": 0.2},
        {"id": "far-road", "op": "path", "line": FAR_ROAD, "width": 3, "max_grade": 0.45,
         "note": "from the brig's east end round the tarn and up onto the bench"},
        {"id": "back-road", "op": "path", "line": BACK_ROAD, "width": 3, "max_grade": 0.2,
         "note": "from the spawn to the timber bridge"},
    ]


def carve():
    return [
        {"id": "crypt", "op": "rooms", "seed": 11,
         "rooms": [{"id": "crypt", "rect": [-14, 70, -3, 78], "floor": 33, "h": 5},
                   {"id": "adit-end", "rect": [4, 71, 8, 77], "floor": 33, "h": 4}],
         "halls": [{"from": "crypt", "to": "adit-end", "via": "x", "width": 3, "h": 4}],
         "lining": {"wall": [[["STONEBRICK", 0], 6], [["STONEBRICK", 2], 1]],
                    "floor": [[["STONEBRICK", 0], 1], [["STONE", 6], 1], [["STONE", 5], 1], [["STONE", 0], 1]],
                    "ceiling": "STONEBRICK"}, "light": {"y": 2},
         "props": [F(-13, 33, 71, -12, 33, 72, ["STONEBRICK", 3]), F(-13, 34, 71, -12, 34, 72, ["SLAB", 5]),
                   F(-13, 33, 76, -12, 33, 77, ["STONEBRICK", 3]), F(-13, 34, 76, -12, 34, 77, ["SLAB", 5])],
         "note": "the chantry's crypt under the nave, two tombs; a hall east to where the miners broke in"},
        {"id": "crypt-ladder", "op": "shaft", "at": [-5, 74], "bottom": 33, "top": "ground", "ladder_on": "s",
         "wall": ["STONEBRICK", 0], "post": ["STONEBRICK", 0], "note": "the ladder from the crypt up into the nave"},
        {"id": "adit", "op": "tunnel", "breach": True, "cover": 3,
         "pts": [[41, 35, 75, 2.0], [37, 32, 75, 2.0], [33, 27, 76, 2.0], [24, 26, 75, 2.0], [14, 29, 74, 2.0],
                 [6, 33, 74, 2.0]],
         "dress": {"seed": 23, "ores": 60, "stalagmites": 40},
         "note": "the old adit from the shelter under the gill into the crypt's end"},
    ]


def house(id_, at, heading, L, W, n, style, door, to="main-street", **kw):
    walk = {} if to is None else {"walk": {"to": to, "blocks": [["DIRT", 1], "GRAVEL", ["DIRT", 0]]}}
    return dict(id=id_, op="house", at=at, heading=heading, L=L, W=W, storeys=n, style=style, door=door, **walk, **kw)


def build():
    b = [
        {"id": "street-pave", "op": "paving", "area": {"line": {"near": "main-street", "width": 4}}, "cell": 1, "blocks": PAVE},
        {"id": "south-pave", "op": "paving", "area": {"line": {"near": "south-street", "width": 4}}, "cell": 1, "blocks": PAVE},
        {"id": "lane-pave", "op": "paving", "area": {"line": {"near": "lane", "width": 3}}, "cell": 1, "blocks": PAVE, "seed": 3},
        {"id": "brig-pave", "op": "paving", "area": {"line": {"near": "brig-road", "width": 3}}, "cell": 1, "blocks": PAVE, "seed": 4},
        {"id": "far-pave", "op": "paving", "area": {"line": {"near": "far-road", "width": 3}}, "cell": 1,
         "blocks": [["DIRT", 1], "GRAVEL", ["STONE", 5]], "seed": 5},
        {"id": "back-pave", "op": "paving", "area": {"line": {"near": "back-road", "width": 3}}, "cell": 1,
         "blocks": [["DIRT", 1], "GRAVEL", ["DIRT", 0]], "seed": 6},
        {"id": "square-pave", "op": "paving", "area": {"polygon": SQUARE}, "cell": 3,
         "blocks": [["STONEBRICK", 0], ["STONE", 6], ["STONE", 5], ["STONE", 0]], "seed": 7},
        # the chapel south-east of the square, its tower at the west end, entered through the tower
        house("nave", [-6, 74], 0, 15, 9, 1, "chapel-stone", 0, to=None, storey=6, chimney=False),
        {"id": "chapel-tower", "op": "round_tower", "at": [-16, 74], "half": 2, "cut": False, "height": 15,
         "wall": ["STONEBRICK", 0], "quoins": QUOINS, "string": ["STONE", 6], "plinth": "COBBLE",
         "crenel": ["SLAB", 5], "door": "n", "floor": ["PLANKS", 1]},
        {"id": "chapel-way", "op": "blocks", "rel": "nave", "boxes": [F(-14, 1, 74, -13, 2, 74, "AIR")],
         "note": "the way from the tower into the nave"},
        {"id": "crypt-hatch", "op": "blocks", "rel": "nave",
         "boxes": [F(-5, -10, 75, -5, 0, 75, ["LADDER", 2]), F(-5, -11, 76, -5, -8, 76, ["STONEBRICK", 0]),
                   F(-6, 1, 74, -6, 1, 76, "SPRUCE_FENCE"), F(-4, 1, 74, -4, 1, 76, "SPRUCE_FENCE"),
                   F(-5, 1, 76, -5, 1, 76, "SPRUCE_FENCE")],
         "note": "the ladder carried up through the nave's floor, railed on three sides"},
        {"id": "graveyard-wall", "op": "wall", "line": [[-14, 80], [-14, 88], [2, 88], [2, 80]], "height": 1,
         "blocks": ["COBBLE_WALL"], "note": "a low wall round the churchyard south of the chapel"},
        {"id": "graves", "op": "graves", "facing": "e", "seed": 8, "flowered": 0.45,
         "flowers": [["FLOWER", 0], ["FLOWER", 3], ["DANDELION", 0], ["FLOWER", 8]],
         "at": [[x, z] for z in (82, 84, 86) for x in (-12, -8, -4)]},
        # houses on the street: long side and door to it, three blocks between roofs
        house("inn", [6, 24], 90, 13, 7, 2, "fell-cottage", 1, jetty=True),
        house("cooper", [-21, 22], 90, 9, 6, 2, "fell-cottage-dark", -1),
        house("west-1", [-23, 38], 90, 9, 6, 1, "fell-cottage", -1),
        house("east-1", [4, 40], 90, 9, 6, 2, "fell-cottage-dark", 1),
        house("square-east", [10, 58], 90, 11, 7, 2, "fell-cottage", 1, to="brig-road", jetty=True),
        house("square-west", [-36, 60], 90, 9, 6, 2, "fell-cottage-dark", -1, to="lane"),
        house("south-west", [-24, 80], 0, 9, 6, 2, "fell-cottage", -1, to="south-street"),
        house("south-east", [12, 78], 90, 9, 6, 1, "fell-cottage-dark", 1, to="south-street"),
        house("lane-1", [-36, 42], 15, 9, 6, 2, "fell-cottage", 1, to="lane"),
        # the spawn's hall, its door north to the spawn
        house("hall", [4, 104], 0, 13, 7, 2, "fell-cottage-dark", -1, to=None, jetty=True),
        house("byre", [-50, 40], 0, 13, 7, 2, "byre", -1, to="lane", chimney=False),
        {"id": "stall-a", "op": "stall", "at": [-3, 52], "facing": "w", "colours": [14, 0], "post": ["DARK_OAK_FENCE", 0],
         "foot": ["LOG2", 1], "counter_stair": "SPRUCE_STAIRS", "banners": True, "sides": True},
        {"id": "stall-b", "op": "stall", "at": [-4, 60], "facing": "w", "colours": [11, 0], "post": ["DARK_OAK_FENCE", 0],
         "foot": ["LOG2", 1], "counter_stair": "SPRUCE_STAIRS", "banners": True, "sides": True},
        {"id": "stall-c", "op": "stall", "at": [-22, 62], "facing": "n", "colours": [4, 13], "post": ["DARK_OAK_FENCE", 0],
         "foot": ["LOG2", 1], "counter_stair": "SPRUCE_STAIRS", "banners": True, "sides": True,
         "goods": [["HAY", 0], ["PUMPKIN", 3], ["HAY", 0]]},
        {"id": "street-lamps", "op": "posts", "stack": [["STONE", 6], "COBBLE_WALL", ["TORCH", 5]],
         "at": [[-10, 20], [-4, 34], [-15, 44], [-2, 68], [4, 82], [-28, 52], [16, 46], [24, 36]]},
        {"id": "square-lamps", "op": "posts", "stack": [["STONE", 6], "COBBLE_WALL", "COBBLE_WALL", "REDSTONE_LAMP", [151, 0]],
         "at": [[-22, 50], [-1, 63]]},
        # the wall across the town's front, its gate on the street, broken toward the west
        {"id": "front-wall-e", "op": "wall", "line": [[-1, 16], [12, 15], [22, 19]], "width": 3, "height": 5,
         "crown": "follow", "courses": COURSES, "step_slab": ["SLAB", 5]},
        {"id": "front-parapet-e", "op": "wall", "line": [[-1, 16], [12, 15], [22, 19]], "offset": 1.4, "height": 6,
         "crown": "follow", "courses": COURSES, "crenel": ["SLAB", 5], "step_slab": ["SLAB", 5]},
        {"id": "front-wall-w", "op": "wall", "line": [[-12, 17], [-26, 15], [-40, 18]], "width": 3, "height": 5,
         "crown": "follow", "courses": COURSES, "step_slab": ["SLAB", 5], "ruin": [6, 28, 3]},
        {"id": "front-parapet-w", "op": "wall", "line": [[-12, 17], [-26, 15], [-40, 18]], "offset": -1.4, "height": 6,
         "crown": "follow", "courses": COURSES, "crenel": ["SLAB", 5], "step_slab": ["SLAB", 5], "ruin": [6, 28, 3]},
        {"id": "gate-tower", "op": "round_tower", "at": [24, 22], "half": 3, "height": 10, "wall": ["STONEBRICK", 0],
         "door": "s", "crenel": ["SLAB", 5], "quoins": QUOINS, "string": ["STONE", 6], "plinth": "COBBLE",
         "floor": ["PLANKS", 1], "openings": [[200, 5]], "openings_from": "floor"},
        {"id": "byre-field", "op": "crops", "angle": 14, "rows": 6, "ditch": 3, "seed": 9, "area": {"polygon": FIELD},
         "crops": [["WHEAT", 7], ["CARROTS", 7], ["POTATOES", 7]], "scarecrows": [[-44, 26]]},
        {"id": "flower-meadow", "op": "flowers", "angle": -20, "rows": 2,
         "area": {"polygon": [[-36, 70], [-26, 68], [-24, 78], [-30, 86], [-40, 82]], "rough": {"amp": 0.08, "cell": 4, "seed": 3}},
         "flowers": [["FLOWER", 0], ["DANDELION", 0], ["FLOWER", 3], ["FLOWER", 8], ["FLOWER", 2]]},
        {"id": "gardens", "op": "small_trees", "seed": 6,
         "at": [[14, 30], [-30, 30], [16, 66], [-44, 66], [-30, 92], [20, 84], [-12, 94]]},
        {"id": "erratics", "op": "boulders", "seed": 17, "sink": 0.3, "rough": 0.5,
         "at": [[-30, 104, 3.2, {"rz": 2.4, "angle": 20}], [-60, 72, 2.6], [64, 40, 2.4], [70, 70, 3.4, {"rz": 2.6, "angle": -30}],
                [20, 104, 2.2], [-16, 30, 1.8], [44, 56, 2.0]],
         "note": "erratics on the fell and the Scar, one rock each"},
    ]
    return b


def dress():
    return [
        {"id": "edge-copse", "op": "trees", "on": "ground", "area": {"polygon": [[-66, 54], [-52, 52], [-46, 62], [-54, 72], [-66, 68]]},
         "kinds": {"oak": 3, "birch": 1}, "tries": 30, "seed": 4, "spacing": 1.8, "note": "a copse on the edge bench"},
        {"id": "scar-trees", "op": "trees", "on": "ground", "area": {"polygon": [[60, 56], [76, 50], [80, 70], [70, 90], [62, 80]]},
         "kinds": {"oak": 2, "birch": 1}, "tries": 16, "seed": 5, "spacing": 2.2, "note": "a few trees on the plateau"},
        {"id": "knott-trees", "op": "trees", "on": "ground", "area": {"polygon": [[-40, 90], [-22, 88], [-14, 98], [-30, 104]]},
         "kinds": {"oak": 1}, "tries": 8, "seed": 6, "spacing": 2.4, "note": "oaks on the knott's foot"},
    ]


SPAWN = (4, 46, 95)
