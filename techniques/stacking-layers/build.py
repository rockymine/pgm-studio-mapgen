"""Writes stacking-layers.layout.json — six galleries, each a stack of thin layers you can see into.

A layer is a slab keeping one span per column, so a cell may be on several and the air between them is the
feature. Here the document's stack IS the structure: a court, a layer holding a back wall and a colonnade,
and a roof over them. Every gallery is open to the south, so what the layers made is read off the board
itself rather than off an x-ray.

Row 1 is one gallery at three headrooms — four courses, one course, and a roof set one too low, which is
`SK10`. Row 2 is the stair onto a roof and a gallery stacked on a gallery.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, grid

PANEL_W, PANEL_D = 64, 44
HALF = PANEL_W / 2
COL_X, ROW_Z = grid(3, 2, PANEL_W, PANEL_D)

COURT_TOP = 14   # the court's base_height: its top block is y13, and a layer resting on it has base_y 14

# Not the slope axis. A board finished by its angle is a landform; a gallery is finished by what it is made
# of, so every stack here is a depth stack and the court's `fill` is a third block on purpose — it is what
# lets a covered column be told from an open one at a glance.
COURT = {
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(24)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": SOLID(24, 2), "fill": SOLID(1),
    "surface": {"enabled": True, "depth": 2,
                "material": depth_stack((SOLID(24), 1), (SOLID(24, 1), 1))},
}
MASONRY = {   # the walls and the colonnade
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(98)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": SOLID(98), "fill": SOLID(98),
    "surface": {"enabled": True, "depth": 1, "material": SOLID(98, 1)},
}
PAVING = {    # the gallery's own floor, marked with a shape rather than a stroke
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(1, 6)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": SOLID(1, 6), "fill": SOLID(1),
    "surface": {"enabled": True, "depth": 1, "material": SOLID(1, 6)},
}
DECK = {      # every roof and every intermediate floor
    "bedrock": {"relative": False, "value": 1},
    "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(5, 1)},
    "wallEnabled": True, "wallOnTerrainFaces": True,
    "wall": SOLID(98), "fill": SOLID(98),
    "surface": {"enabled": True, "depth": 1, "material": SOLID(5, 1)},
}


def rect(shape_id, min_x, min_z, max_x, max_z, **words):
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": 0,
           "min_x": min_x, "min_z": min_z, "max_x": max_x, "max_z": max_z}
    out.update(words)
    return out


def masonry(name, cx, cz, courses):
    """One layer holding the gallery's walls: a back wall along the north and an end wall at each end.

    The gallery is open on its south and east sides, the two the camera looks into, and eight cells deep
    against four courses of headroom: a 2:1 isometric sees about two cells in for every course of height,
    so a deeper gallery is a roof with a shadow under it and has to be x-rayed to be read at all."""
    return [rect(f"back-{name}", cx - HALF + 4, cz - 10, cx + HALF - 4, cz - 6,
                 base_height=courses, theme="masonry"),
            rect(f"west-{name}", cx - HALF + 4, cz - 10, cx - HALF + 8, cz,
                 base_height=courses, theme="masonry")]


def roof(name, cx, cz):
    return [rect(f"roof-{name}", cx - HALF + 3, cz - 11, cx + HALF - 3, cz,
                 base_height=1, theme="deck")]


def stair(name, cx, cz, z_near):
    """A flight on the COURT's own layer, climbing from the court to the roof's own course.
    `height_mode: "level"` with `anchor_heights` is a tilted plane, one world height per vertex."""
    return {"id": f"stair-{name}", "type": "polygon", "operation": "add", "floor": 0,
            "base_height": 20, "height_mode": "level", "skirt": 0, "theme": "court",
            "vertices": [[cx + 4, cz + 18], [cx + 20, cz + 18],
                         [cx + 20, cz + z_near], [cx + 4, cz + z_near]],
            "anchor_heights": [COURT_TOP, COURT_TOP, 20, 20]}


# (name, column, row, the storeys over the court, the stair's north edge or None).
# A storey is (wall base_y, wall courses, roof base_y).
PANELS = [
    ("open",        0, 0, [(14, 5, 19)], None),
    ("low",         1, 0, [(14, 1, 15)], None),
    ("driven",      2, 0, [(14, 5, 18)], None),
    ("stair-meets", 0, 1, [(14, 5, 19)], 0),
    ("stair-short", 1, 1, [(14, 5, 19)], 1),
    ("two-storeys", 2, 1, [(14, 5, 19), (20, 5, 25)], None),
]

court_shapes, court_groups, slabs = [], [], []
for name, col, row, storeys, stair_to in PANELS:
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    ids = [f"court-{name}", f"paving-{name}"]
    court_shapes.append(rect(f"court-{name}", x0, z0, x0 + PANEL_W, z0 + PANEL_D,
                             base_height=COURT_TOP, theme="court"))
    # The gallery's floor, stated as a shape of the court's own courses carrying a different theme. A
    # stroke ignores `layer` and would come back on the roof; a shape's theme scope resolves per layer and
    # lands where it is drawn.
    court_shapes.append(rect(f"paving-{name}", cx - HALF + 8, cz - 6, cx + HALF - 4, cz,
                             base_height=COURT_TOP, theme="paving"))
    if stair_to is not None:
        court_shapes.append(stair(name, cx, cz, stair_to))
        ids.append(f"stair-{name}")
    court_groups.append({"id": f"court-{name}", "name": name, "mirrors": False, "shapeIds": ids})
    for storey, (wall_at, courses, roof_at) in enumerate(storeys):
        tag = f"{name}-{storey}" if len(storeys) > 1 else name
        slabs.append((f"walls-{tag}", wall_at, masonry(tag, cx, cz, courses)))
        slabs.append((f"roof-{tag}", roof_at, roof(tag, cx, cz)))

layers = [{"id": "court", "name": "Court", "base_y": 0,
           "layout": {"shapes": court_shapes, "groups": court_groups}}]
layers += [{"id": layer_id, "name": layer_id, "base_y": base_y,
            "layout": {"shapes": shapes,
                       "groups": [{"id": layer_id, "name": layer_id, "mirrors": False,
                                   "shapeIds": [s["id"] for s in shapes]}]}}
           for layer_id, base_y, shapes in sorted(slabs, key=lambda slab: slab[1])]

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"court": COURT, "masonry": MASONRY, "paving": PAVING, "deck": DECK},
    "mapTheme": "court",
    "relief": {},
    "layers": layers,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stacking-layers.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(layers)} layers -> {out}")
for layer in layers:
    print(f"  {layer['id']:18s} base_y {layer['base_y']:3}  {len(layer['layout']['shapes'])} shape(s)")
