"""Writes made-ground.layout.json — eight panels, one hillside and one piece on it, eight ways.

A shape is either part of the ground or standing in it, and the document says which with one of two
fields that are alternatives rather than a pair. Row 1 is `relief_scope`, which says how a shape that IS
ground takes part in the solve. Row 2 is `height_mode`, which says the shape stands OUT of the field and
is applied over ground the relief has already made — and the last panel of it states both, to show what
happens to the one that is ignored.

Every panel carries the same hillside and the same 34x26 piece in the same place, so the difference
between two panels is the words on the piece.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import grid, moor

PANEL_W, PANEL_D = 96, 76
COL_X, ROW_Z = grid(4, 2, PANEL_W, PANEL_D)

MOOR = moor(grass_to=25, dirt_to=45)

BRAE, STRAND = 26, 10   # the hillside the piece meets, north edge to south
BASE = 18               # what the field settles toward between them
TOP = 24                # the height the piece states, two-thirds of the way up the fall
GROUND_TOP = 44         # the island's raw column, before the relief solves it

PIECE_W, PIECE_D = 34, 26

# What each panel writes on the piece, and nothing else changes.
PANELS = [
    ("inherit",    0, 0, {}),
    ("hold",       1, 0, {"relief_scope": "hold"}),
    ("follow",     2, 0, {"relief_scope": "follow"}),
    ("exclude",    3, 0, {"relief_scope": "exclude"}),
    ("sheer",      0, 1, {"height_mode": "level", "skirt": 0}),
    ("skirt-6",    1, 1, {"height_mode": "level", "skirt": 6}),
    ("skirt-14",   2, 1, {"height_mode": "level", "skirt": 14}),
    ("both-words", 3, 1, {"height_mode": "level", "skirt": 0, "relief_scope": "hold"}),
]


def band(cx, cz, z_from, z_to):
    half = (PANEL_W - 6) / 2
    return [[cx - half, cz + z_from], [cx + half, cz + z_from],
            [cx + half, cz + z_to], [cx - half, cz + z_to]]


shapes, groups, relief = [], [], {}
for name, col, row, words in PANELS:
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add",
                   "floor": 0, "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    piece = {"id": f"piece-{name}", "type": "rectangle", "operation": "add", "floor": 0,
             "base_height": TOP, "theme": "moor",
             "min_x": cx - PIECE_W / 2, "min_z": cz - PIECE_D / 2,
             "max_x": cx + PIECE_W / 2, "max_z": cz + PIECE_D / 2}
    piece.update(words)
    shapes.append(piece)
    groups.append({"id": name, "name": name, "mirrors": False,
                   "shapeIds": [f"island-{name}", f"piece-{name}"]})
    relief[name] = {"base": BASE, "reach": 0, "step": 1, "pushes": [],
                    "marks": [{"id": "brae", "kind": "area", "h": BRAE, "bevel": 0,
                               "ring": band(cx, cz, -37, -30)},
                              {"id": "strand", "kind": "area", "h": STRAND, "bevel": 0,
                               "ring": band(cx, cz, 30, 37)}]}

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR},
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "made-ground.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, hillside {BRAE} -> {STRAND}, piece at {TOP} -> {out}")
for name, col, row, words in PANELS:
    print(f"  {name:11s} {json.dumps(words)}")
