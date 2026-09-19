"""Writes water.layout.json — eight panels of water asked for eight ways.

Water cannot drape on a slope the way gravel can, so a body of water is not a finish over the ground but a
shape taken out of it: a carved bed under a level fill. Row 1 is the four things that shape can be — a
beach, a pond, a canal against a stream, and a basin dug in the sketch and filled by a stated line. Row 2
is the four surprises: a pan drawn bigger than its water, the same pan drawn right, a deck that dries a
beck out, and the two channels that carry it under.
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, grid, lobed_ring, moor

PANEL_W, PANEL_D = 96, 76
COL_X, ROW_Z = grid(5, 2, PANEL_W, PANEL_D)
MOOR = moor(grass_to=25, dirt_to=45)
GROUND_TOP = 40

PLANK = {   # the bridge, so it can be told from the grass it crosses
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(5, 1)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": SOLID(98), "fill": SOLID(98),
    "surface": {"enabled": True, "depth": 1, "material": SOLID(5, 1)},
}

SAND = {"kind": "solid", "id": 12, "data": 0}
GRAVEL_BANK = {"kind": "voronoi", "seed": 5, "cellSize": 5, "bands": [
    {"material": {"kind": "solid", "id": 13, "data": 0}, "thickness": 2},
    {"material": {"kind": "solid", "id": 3, "data": 1}, "thickness": 1},
    {"material": SAND, "thickness": 1}]}


def area(mark_id, height, ring, bevel=0):
    return {"id": mark_id, "kind": "area", "h": height, "bevel": bevel, "ring": ring}


def band(cx, cz, z_from, z_to, inset=3):
    half = PANEL_W / 2 - inset
    return [[cx - half, cz + z_from], [cx + half, cz + z_from],
            [cx + half, cz + z_to], [cx - half, cz + z_to]]


def box(cx, cz, width, depth):
    return [[cx - width / 2, cz - depth / 2], [cx + width / 2, cz - depth / 2],
            [cx + width / 2, cz + depth / 2], [cx - width / 2, cz + depth / 2]]


def water(prop_id, shape, points, **words):
    out = {"id": prop_id, "kind": "water", "shape": shape, "points": points,
           "radius": 3, "depth": 2, "form": "canal", "edge": 0.8,
           "shore": 2, "shoreWander": True, "seed": 7, "bank": GRAVEL_BANK}
    out.update(words)
    return out


# Each panel: the relief its ground is solved to, any shape it cuts, and the water drawn on it.
def beach(cx, cz):
    """A pool against a bank that shelves. `shore` is how wide a beach the water meets the land through,
    and `shoreWander` opens and closes it along the run so the strand is ragged rather than ruled."""
    return ([area("fell", 30, band(cx, cz, -35, -26)), area("strand", 17, band(cx, cz, 10, 35))],
            [], [water("bay", "pool", box(cx, cz + 23, 70, 22), level=16, radius=8, depth=4,
                       form="natural", shore=5, edge=2)])


def pond(cx, cz):
    """A pool with no `level`: the line is the lowest surface it crosses, which is a pond cut into ground
    that was already there."""
    return ([area("land", 22, band(cx, cz, -35, 35))],
            [], [water("tarn", "pool", lobed_ring(cx, cz, 17, lobes=5, depth=0.18),
                       radius=6, depth=3, form="natural", shore=3, edge=2)])


def no_shore(cx, cz):
    """The same pond with `shore` 0: the water meets the grass at its own edge and there is no beach at
    all. `shore` is how wide a band of the bank material the water meets the land through."""
    return ([area("land", 22, band(cx, cz, -35, 35))],
            [], [water("tarn", "pool", lobed_ring(cx, cz, 17, lobes=5, depth=0.18),
                       radius=6, depth=3, form="natural", shore=0, edge=2)])


def two_forms(cx, cz):
    """The same radius and depth drawn twice: a canal holds its width the whole way, a stream pinches and
    swells on a beat down its arc and runs shallower throughout."""
    return ([area("holm", 20, band(cx, cz, -35, 35))], [],
            [water("cut", "channel", [[cx - 42, cz - 16], [cx + 42, cz - 16]], radius=4, depth=3),
             water("beck", "channel", [[cx - 42, cz + 16], [cx + 42, cz + 16]], radius=4, depth=3,
                   form="stream", edge=1.5, shore=3)])


def basin(cx, cz):
    """The pool's shape taken out of the ground with a `sink` shape, and the water stated at a `level`.
    Dug ground has no surface up at the line for a derived one to find, so a basin can only be filled by
    saying where the water stands."""
    return ([area("quay", 22, band(cx, cz, -35, 35))],
            [{"id": "dock", "type": "rectangle", "operation": "add", "floor": 0, "base_height": 8,
              "height_mode": "sink", "skirt": 0, "theme": "moor",
              "min_x": cx - 30, "min_z": cz - 16, "max_x": cx + 30, "max_z": cz + 16}],
            [water("dock-water", "pool", box(cx, cz, 60, 32), level=20, radius=4, depth=1, shore=0)])


def pan_too_big(cx, cz):
    """An `area` mark drawn at the size of the *hollow* rather than the size of the water: everything the
    mark levelled stands at the water line, wet or not."""
    return ([area("land", 20, band(cx, cz, -35, 35)), area("pan", 14, box(cx, cz, 68, 44), bevel=6)],
            [], [water("sump", "pool", lobed_ring(cx, cz, 10, lobes=5, depth=0.16),
                       radius=5, depth=3, form="natural", shore=2, edge=1.5)])


def pan_fits(cx, cz):
    """The same water with the mark drawn at its own size, and the floor around it left to the solve."""
    return ([area("land", 20, band(cx, cz, -35, 35)),
             area("pan", 14, lobed_ring(cx, cz, 14, lobes=5, depth=0.16), bevel=6)],
            [], [water("sump", "pool", lobed_ring(cx, cz, 10, lobes=5, depth=0.16),
                       radius=5, depth=3, form="natural", shore=2, edge=1.5)])


def under_a_bridge(cx, cz, split=False):
    """A beck across level ground with a deck thrown over it. The channel's line is the lowest surface its
    band crosses — the open holm at 20 — and every column over that line inside the band is emptied down
    to it, the deck's own columns included. Two channels stopping at the deck's edges leave it standing."""
    marks = [area("holm", 20, band(cx, cz, -35, 35))]
    if not split:
        return marks, [], [water("beck", "channel", [[cx, cz - 32], [cx, cz + 32]],
                                 radius=4, depth=3, form="stream", shore=3, edge=1.5)]
    return marks, [], [water("beck-north", "channel", [[cx, cz - 32], [cx, cz - 11]],
                             radius=4, depth=3, form="stream", shore=3, edge=1.5),
                       water("beck-south", "channel", [[cx, cz + 11], [cx, cz + 32]],
                             radius=4, depth=3, form="stream", shore=3, edge=1.5)]


def down_a_hill(cx, cz):
    """The same channel run down a fall instead of across the level. The line is still the lowest surface
    the band crosses, which is now the foot of the hill, and every column over it is emptied down to it:
    `DR-BANK`, and a trench where a beck was drawn."""
    return ([area("head", 30, band(cx, cz, -35, -26)), area("foot", 16, band(cx, cz, 26, 35))], [],
            [water("beck", "channel", [[cx, cz - 32], [cx, cz + 32]],
                   radius=4, depth=3, form="stream", shore=3, edge=1.5)])


PANELS = [
    ("beach", 0, 0, beach), ("pond", 1, 0, pond), ("no-shore", 2, 0, no_shore),
    ("two-forms", 3, 0, two_forms), ("basin", 4, 0, basin),
    ("pan-too-big", 0, 1, pan_too_big), ("pan-fits", 1, 1, pan_fits), ("down-a-hill", 2, 1, down_a_hill),
    ("one-channel", 3, 1, under_a_bridge),
    ("two-channels", 4, 1, lambda cx, cz: under_a_bridge(cx, cz, split=True)),
]

shapes, groups, relief, props = [], [], {}, []
deck_layer = []
for name, col, row, make in PANELS:
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    marks, cut, water_props = make(cx, cz)
    ids = [f"island-{name}"]
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    for extra in cut:
        shapes.append(extra)
        ids.append(extra["id"])
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": ids})
    relief[name] = {"base": 18, "reach": 0, "step": 1, "marks": marks, "pushes": []}
    for prop in water_props:
        prop["id"] = f"{name}-{prop['id']}"   # a prop id is the handle a decline names
    props += water_props
    if name in ("one-channel", "two-channels"):
        deck_layer.append({"id": f"deck-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                           "base_height": 1, "theme": "plank",
                           "min_x": cx - 24, "min_z": cz - 6, "max_x": cx + 24, "max_z": cz + 6})

layers = [{"id": "ground", "name": "Ground", "base_y": 0,
           "layout": {"shapes": shapes, "groups": groups}},
          {"id": "deck", "name": "Deck", "base_y": 25,
           "layout": {"shapes": deck_layer,
                      "groups": [{"id": "deck", "name": "deck", "mirrors": False,
                                  "shapeIds": [s["id"] for s in deck_layer]}]}}]

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR, "plank": PLANK},
    "mapTheme": "moor",
    "relief": relief,
    "layers": layers,
    "dressing": {"props": props},
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "water.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(props)} water prop(s) -> {out}")
for prop in props:
    print(f"  {prop['id']:12s} {prop['shape']:8s} {prop['form']:8s} r={prop['radius']} "
          f"depth={prop['depth']} shore={prop['shore']} level={prop.get('level')}")
