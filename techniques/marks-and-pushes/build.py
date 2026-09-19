"""Writes marks-and-pushes.layout.json — six panels about the one sentence a relief is solved by.

Marks negotiate with each other and are solved first; a push is added to the answer. Row 1 is one dale and
one push, the push in two places, so what the ordering costs is the difference between three pictures. Row 2
is how much of a panel to pin: every region, only the ground a player walks, and the same again with a finite
`reach` under it.

Nothing here is a map. The renders read the stored layout through `POST /sketch/columns`.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import MOOR, grid, lobed_ring, rect_ring

PANEL_W, PANEL_D = 96, 76
COL_X, ROW_Z = grid(3, 2, PANEL_W, PANEL_D)
GROUND_TOP = 60  # the island's raw column, before the relief solves it

DALE_BASE = 20   # row 1: what the land round the dale stands at
OPEN_BASE = 6    # row 2: what an unmarked field settles at, and what a finite reach pulls it to


def area(mark_id, height, ring, bevel=0):
    return {"id": mark_id, "kind": "area", "h": height, "bevel": bevel, "ring": ring}


def fell(cx, cz, amount=16):
    """The one push every panel of row 1 uses, and row 2's flank fell. Its two grades are 1.33 and 0.69,
    which is inside `RL6`'s factor of two."""
    return {"id": "fell", "ring": lobed_ring(cx, cz, 13, lobes=4, depth=0.16), "amount": amount,
            "falloff": 12, "crown": 9, "roughness": 0, "seed": 1}


# --- row 1: one dale, one push, two places ------------------------------------------------------------

def dale_marks(cx, cz):
    """The dale itself: land held at 20 over the whole panel and a holm pinned eight blocks into it.

    Two marks rather than one, because a lone constraint has nothing to negotiate with and the smoothest
    field through it is the constant one — a single mark at 12 flattens the panel to 12."""
    return [area("land", DALE_BASE, rect_ring(cx, cz, PANEL_W - 6, PANEL_D - 6)),
            area("holm", 12, lobed_ring(cx + 2, cz, 14, lobes=5, depth=0.14), bevel=6)]


def dale(cx, cz):
    return dale_marks(cx, cz), []


def push_on_it(cx, cz):
    """The push centred on the holm. Its ring covers ground a mark pins, and the mark does not win."""
    return dale_marks(cx, cz), [fell(cx + 2, cz)]


def push_beside_it(cx, cz):
    """The same push, moved until its ring is clear of the holm. The falloff is not."""
    return dale_marks(cx, cz), [fell(cx - 20, cz)]


# --- row 2: how much of a panel to pin ----------------------------------------------------------------

def band(cx, cz, z_from, z_to):
    """A mark across the whole panel, which is what pinning a *region* looks like."""
    half = (PANEL_W - 6) / 2
    return [[cx - half, cz + z_from], [cx + half, cz + z_from],
            [cx + half, cz + z_to], [cx - half, cz + z_to]]


def pinned(cx, cz):
    """Every region stated: a coast, a holm and a shelf, tiling the panel between them."""
    return ([area("coast", 10, band(cx, cz, 16, 35), bevel=4),
             area("holm", 20, band(cx, cz, -8, 15), bevel=4),
             area("shelf", 30, band(cx, cz, -35, -9), bevel=4)],
            [fell(cx - 24, cz - 20)])


def free_flanks(cx, cz):
    """The same three heights, pinned only where a player stands on them. Everything else is left to the
    relaxation, which is the ground the fell then rises out of."""
    return ([area("coast", 10, band(cx, cz, 28, 35), bevel=3),
             area("holm", 20, lobed_ring(cx + 14, cz + 12, 15, lobes=5, depth=0.14), bevel=5),
             area("shelf", 30, lobed_ring(cx + 26, cz - 22, 10, lobes=4, depth=0.12), bevel=4)],
            [fell(cx - 24, cz - 20)])


PANELS = [
    ("dale",           0, 0, dale,          DALE_BASE, 0),
    ("push-on-it",     1, 0, push_on_it,    DALE_BASE, 0),
    ("push-beside-it", 2, 0, push_beside_it, DALE_BASE, 0),
    ("pinned",         0, 1, pinned,        OPEN_BASE, 0),
    ("free-flanks",    1, 1, free_flanks,   OPEN_BASE, 0),
    ("reach",          2, 1, free_flanks,   OPEN_BASE, 16),
]

shapes, groups, relief = [], [], {}
for name, col, row, make, base, reach in PANELS:
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    marks, pushes = make(cx, cz)
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add",
                   "floor": 0, "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": [f"island-{name}"]})
    relief[name] = {"base": base, "reach": reach, "step": 1, "marks": marks, "pushes": pushes}

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
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marks-and-pushes.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(shapes)} panels -> {out}")
for name, _, _, make, base, reach in PANELS:
    marks, pushes = make(0, 0)
    print(f"  {name:15s} base {base:3}  reach {reach:3}  marks {len(marks)}  pushes {len(pushes)}"
          f"   {', '.join(m['id'] + '@' + str(m['h']) for m in marks)}")
