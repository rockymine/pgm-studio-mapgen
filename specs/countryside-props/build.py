"""Countryside's hand-built props, rebuilt in the studio as made things and labelled as rebuilds.

Every prop was cut out of the original world (`tools/lift.py`, one voxel model each, in `models/`) and is
compiled to sketch layers by run index (`tools/sculpt/layers.py`), one block a theme. Each stands on a pad of its
own except the two the author built floating in the void, which float here too.

    python3 specs/countryside-props/build.py            # write the layout and intent beside this file
    python3 specs/countryside-props/build.py --store    # ... and store them as the map `countryside-props`
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "sculpt"))

import board                                    # noqa: E402
from layers import compile_layers, stats        # noqa: E402

SLUG = "countryside-props"
NAME = "Countryside props (rebuilt)"
SOURCE = "alphaboy98yt-4"
GROUND_TOP = 6                                  # the original ground's top block, so no model is moved in y
PAD_MARGIN = 3
GAP = 4
ROW_LIMIT = 64                                  # blocks of pad per row before the next row starts

AUTHORS = [
    {"name": "Alphaboy98yt", "uuid": "1af9f952-e33e-42a5-8e1e-296757747fdc", "role": "author",
     "contribution": "built every prop shown, for Countryside"},
    {"name": "Claude Code", "role": "contributor",
     "contribution": "rebuilt the props from the original world as studio layers"},
]

# key, what it is, where the original stands (x, z) on the east half of Countryside, floats in the void
PROPS = [
    ("barn-spawn", "Spawn barn: red clay and wool walls, mushroom-stem posts, soul-sand roof, doors, interior", (4, 260), False),
    ("barn-wool", "Wool barn: loft chests, interior doors, floating wool pad over the roof", (4, 233), False),
    ("tractor-module", "Tractor on its road through the field: coal wheels, dropper grille, lever exhaust", (60, 227), False),
    ("wheat-field", "Wheat field: farmland bed, slab edging, trapdoor ends, water beside it", (18, 260), False),
    ("bench", "Bench: four slabs with wall-sign backs", (128, 236), False),
    ("barrel-trough", "Barrel with tripwire-hook taps and a water trough", (125, 239), False),
    ("supply-wall", "Supply wall with a chest, buttons at the ends, bedrock below", (132, 225), False),
    ("wool-room-line", "Wool room line: redstone on a bedrock wall", (139, 225), False),
    ("hand-fence", "Small hand-built fence", (114, 192), False),
    ("pothole-path", "Path with potholes (rings of stairs)", (127, 199), False),
    ("frontline-detail", "Frontline edge detail: slabs and a wheat patch", (110, 198), False),
    ("bush-a", "Bush batch with leaves and fences", (129, 211), False),
    ("bush-b", "Bush batch with leaves and fences", (128, 194), False),
    ("cart", "Small cart with a hay bale", (92, 264), False),
    ("scarecrow", "Scarecrow", (88, 225), False),
    ("windmill", "Thin windmill with two crates of crafting tables", (121, 193), False),
    ("water-tower", "Water tower", (83, 265), False),
    ("fence-prop", "Fence prop floating in the void", (126, 255), True),
    ("bow-spam-blocker", "Bow-spam blocker: glass wall with barrier above, in the void", (135, 212), True),
]

# lift.py drops water; these are the water blocks of each box, in the original's coordinates.
WATER = {
    "wheat-field": [(16, 7, 259), (16, 7, 260)],
    "tractor-module": [(64, 6, 231)],
    "barn-spawn": [(-2, 9, 257), (-1, 9, 257)],
    "barrel-trough": [(123, 8, 238), (124, 8, 238), (125, 8, 238)],
    "water-tower": [(83, 8, 265)],
}


def solid(block, data=0):
    return {"kind": "solid", "id": block, "data": data}


def ground_theme():
    """The island's side pattern: grass, coarse dirt, one stripe of spruce planks, a stone, gravel, andesite and
    coal mix, and bedrock under it, courses fixed to world Y so every pad's edge reads the same."""
    mix = {"kind": "cell", "cellSize": 3, "rise": 2,
           "palette": [solid(1), solid(13), solid(1, 5), solid(1), solid(16)]}
    wall = {"kind": "layered", "axis": "height", "from": 0, "stack": {"ending": "repeat", "bands": [
        {"material": solid(7), "thickness": 1},
        {"material": mix, "thickness": 3},
        {"material": solid(5, 1), "thickness": 1},
        {"material": solid(3, 1), "thickness": 1}]}}
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
            "rim": {"enabled": True, "depth": 1, "material": solid(2)},
            "surface": {"enabled": True, "depth": 1, "material": solid(2)},
            "wall": wall, "wallEnabled": True, "wallOnTerrainFaces": True, "fill": mix}


SURFACING = {2, 60, 110}                        # blocks that only ever cap a column; a thick run of one is refused
SURFACING_DATA = {(3, 2)}


def block_theme(block, data):
    if block in SURFACING or (block, data) in SURFACING_DATA:
        # One course of the surfacing block over dirt: the first band of a layered pattern, which is the one
        # shape PT1 accepts, and what a run of one course draws wherever another layer stands on it.
        skin = {"kind": "layered", "stack": {"ending": "repeat", "bands": [
            {"material": solid(block, data), "thickness": 1}, {"material": solid(3, 0), "thickness": 1}]}}
        return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "boundary", "wallOnTerrainFaces": True,
                "rim": {"enabled": True, "depth": 1, "material": solid(block, data)},
                "surface": {"enabled": True, "depth": 1, "material": solid(block, data)},
                "wall": skin, "wallEnabled": True, "fill": skin}
    return board.solid(block, data)


def model(key):
    rows = json.load(open(os.path.join(HERE, "models", f"{key}.json")))
    rows = rows if isinstance(rows, list) else rows["blocks"]
    voxels = {(x, y, z): (b, d) for x, y, z, b, d in rows}
    for cell in WATER.get(key, []):
        voxels[cell] = (9, 0)
    return voxels


def bounds(voxels):
    xs, zs = [c[0] for c in voxels], [c[2] for c in voxels]
    return min(xs), min(zs), max(xs), max(zs)


EXPECTED = {}                                   # prop key -> {(x, y, z): (block, data)} as placed, for read-back checks


def build():
    themes = {"ground": ground_theme()}
    pad_shapes, layers, rows, table = [], [], [], []
    cursor_x, cursor_z, row_depth = 0, 0, 0
    for key, title, (ox, oz), floats in PROPS:
        voxels = model(key)
        x0, z0, x1, z1 = bounds(voxels)
        width, depth = x1 - x0 + 1, z1 - z0 + 1
        if cursor_x and cursor_x + width + 2 * PAD_MARGIN > ROW_LIMIT:
            cursor_x, cursor_z, row_depth = 0, cursor_z + row_depth + GAP, 0
        pad_x, pad_z = cursor_x, cursor_z
        tx, tz = pad_x + PAD_MARGIN - x0, pad_z + PAD_MARGIN - z0
        placed = {(x + tx, y, z + tz): m for (x, y, z), m in voxels.items()}
        EXPECTED[key] = placed
        for (b, d) in set(placed.values()):
            themes.setdefault(f"m{b}-{d}", block_theme(b, d))
        label = f"REBUILT · {title} — original at {ox}, {oz} in Countryside ({SOURCE})"
        made = compile_layers({c: f"m{b}-{d}" for c, (b, d) in placed.items()}, prefix=f"{key}-",
                              layer_prefix=f"{key}-L", mirrors=False, group_name=label, part_of=key)
        layers.extend(made)
        if not floats:
            pad_shapes.append({"id": f"pad-{key}", "type": "rectangle", "operation": "add", "floor": 0,
                               "base_height": GROUND_TOP + 1, "theme": "ground",
                               "min_x": pad_x, "min_z": pad_z,
                               "max_x": pad_x + width + 2 * PAD_MARGIN, "max_z": pad_z + depth + 2 * PAD_MARGIN})
        row = stats(placed, made)
        row.update(key=key, title=title, origin=(ox, oz), floats=floats,
                   at=(min(c[0] for c in placed), min(c[1] for c in placed), min(c[2] for c in placed),
                       max(c[0] for c in placed), max(c[1] for c in placed), max(c[2] for c in placed)))
        table.append(row)
        cursor_x += width + 2 * PAD_MARGIN + GAP
        row_depth = max(row_depth, depth + 2 * PAD_MARGIN)

    # the visitors' pad, west of the first row
    pad_shapes.append({"id": "pad-visitors", "type": "rectangle", "operation": "add", "floor": 0,
                       "base_height": GROUND_TOP + 1, "theme": "ground",
                       "min_x": -22, "min_z": -2, "max_x": -6, "max_z": 14})
    ground = {"id": "ground", "name": "Ground", "base_y": 0,
              "layout": {"shapes": pad_shapes, "groups": [{"id": "pads", "name": "Pads", "mirrors": False,
                                                           "shapeIds": [s["id"] for s in pad_shapes]}]}}
    document = board.layout([ground] + layers, themes, map_theme="ground", mirror="none", room_styles=None)
    return document, table


if __name__ == "__main__":
    document, table = build()
    intent = board.intent(NAME, created="2026-10-06", spawn=(-14, GROUND_TOP + 1, 6), observer=(30, 40, 30))
    json.dump(document, open(os.path.join(HERE, f"{SLUG}.layout.json"), "w"))
    json.dump(intent, open(os.path.join(HERE, f"{SLUG}.intent.json"), "w"), indent=1)
    print(f"{'prop':<18}{'blocks':>7}{'layers':>7}{'shapes':>7}   placed at (x0,y0,z0)-(x1,y1,z1)")
    for row in table:
        print(f"{row['key']:<18}{row['blocks']:>7}{row['layers']:>7}{row['shapes']:>7}   {row['at']}"
              f"{'  floats' if row['floats'] else ''}")
    print(f"{len(document['layers'])} layers, {len(document['themes'])} themes")
    if "--store" in sys.argv:
        print(board.API)
        board.call("PUT", f"/map/{SLUG}/source",
                   {"layout": document, "intent": intent, "name": NAME,
                    "refinement": {"authors": AUTHORS, "created": "2026-10-06"}})
