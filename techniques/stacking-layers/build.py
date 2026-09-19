"""Writes stacking-layers.layout.json — six panels about two solid spans in one column.

A layer is a slab keeping one span per column, so a cell may be on several and the air between them is the
feature. Row 1 is the gap and the two ways to lose it: four courses of air, one shared course, and two
courses driven into each other. Row 2 is getting onto a deck and what a third storey costs.

Every panel is a 96x76 court with a deck strip oversailing it. The court and the deck carry different
themes, and the court's `fill` is deliberately a different block from its surface, so that whether a
covered column keeps its own paint can be read off a single block.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, grid

PANEL_W, PANEL_D = 96, 76
COL_X, ROW_Z = grid(3, 2, PANEL_W, PANEL_D)

# A layer's SEGMENT top is `base_y + base_height` and its built top block is one lower, which is what puts
# the seam where it is: a deck at `base_y` 14 rests on a court whose top block is y13 and shares one course
# by the gate's arithmetic, and one lower than that is `SK10`.
COURT_TOP = 14   # the court's base_height: its top block is y13
DECK = 18        # the deck layer's base_y, four courses of air clear of the court
ROOF = 24        # the third storey of the last panel

# Not the slope axis. A board finished by its angle is a landform; a deck is finished by what it is made
# of, so both stacks are depth stacks and one course deep.
COURT = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(24)},
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "wall": SOLID(24, 2),                                   # smooth sandstone, the court's own edge
    "fill": SOLID(1),                                       # stone — what a covered column comes out as
    "surface": {"enabled": True, "depth": 2,
                "material": depth_stack((SOLID(24), 1), (SOLID(24, 1), 1))},
}
GANTRY = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(98)},
    "wallEnabled": True,
    "wallOnTerrainFaces": True,
    "wall": SOLID(98),                                      # stone brick, the deck's soffit and sides
    "fill": SOLID(98),
    "surface": {"enabled": True, "depth": 1, "material": SOLID(5, 1)},   # spruce planks
}


def rect(shape_id, cx, cz, width, depth, **words):
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": 0,
           "min_x": cx - width / 2, "min_z": cz - depth / 2,
           "max_x": cx + width / 2, "max_z": cz + depth / 2}
    out.update(words)
    return out


def causeway(shape_id, cx, cz, z_far, z_near):
    """A ramp on the COURT's own layer, climbing from the court at its south end to the deck's top at its
    north end. `height_mode: "level"` with `anchor_heights` is a tilted plane, one world height per vertex
    in the order they are drawn."""
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0,
            "base_height": DECK + 1, "height_mode": "level", "skirt": 0, "theme": "court",
            "vertices": [[cx - 12, cz + z_far], [cx + 12, cz + z_far],
                         [cx + 12, cz + z_near], [cx - 12, cz + z_near]],
            "anchor_heights": [COURT_TOP, COURT_TOP, DECK + 1, DECK + 1]}


# Every panel's court, and what stands over it. A deck is stated as (layer id, base_y, thickness, depth,
# z-offset); the layers are written in base_y order, which is the order the world builds them in.
PANELS = [
    ("air",           0, 0, [("air",   DECK,         1, 28,   0)], None),
    ("seam",          1, 0, [("seam",  COURT_TOP,     1, 28,  0)], None),
    ("driven",        2, 0, [("driven", COURT_TOP - 1, 1, 28, 0)], None),
    ("ramp-meets",    0, 1, [("meets", DECK,         1, 28,   0)], 14),
    ("ramp-short",    1, 1, [("short", DECK,         1, 28,   0)], 15),
    ("three-storeys", 2, 1, [("mezz",  DECK,         1, 28,   0),
                             ("roof",  ROOF,         1, 16, -12)], None),
]

court_shapes, court_groups, decks = [], [], []
for name, col, row, slabs, ramp_to in PANELS:
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    ids = [f"court-{name}"]
    court_shapes.append(rect(f"court-{name}", cx, cz, PANEL_W, PANEL_D,
                             base_height=COURT_TOP, theme="court"))
    if ramp_to is not None:
        court_shapes.append(causeway(f"causeway-{name}", cx, cz, 34, ramp_to))
        ids.append(f"causeway-{name}")
    court_groups.append({"id": f"court-{name}", "name": name, "mirrors": False, "shapeIds": ids})
    for layer_id, base_y, thickness, depth, offset in slabs:
        decks.append((layer_id, base_y, {
            "shapes": [rect(f"deck-{layer_id}", cx, cz + offset, PANEL_W + 8, depth,
                            base_height=thickness, theme="gantry")],
            "groups": [{"id": f"deck-{layer_id}", "name": layer_id, "mirrors": False,
                        "shapeIds": [f"deck-{layer_id}"]}]}))

layers = [{"id": "court", "name": "Court", "base_y": 0,
           "layout": {"shapes": court_shapes, "groups": court_groups}}]
layers += [{"id": layer_id, "name": layer_id, "base_y": base_y, "layout": layout}
           for layer_id, base_y, layout in sorted(decks, key=lambda slab: slab[1])]

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"court": COURT, "gantry": GANTRY},
    "mapTheme": "court",
    "relief": {},
    "layers": layers,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stacking-layers.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(layers)} layers -> {out}")
for layer in layers:
    print(f"  {layer['id']:8s} base_y {layer['base_y']:3}  "
          f"{len(layer['layout']['shapes'])} shape(s)")
