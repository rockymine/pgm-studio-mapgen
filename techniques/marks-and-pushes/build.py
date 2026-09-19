"""Writes marks-and-pushes.layout.json — six panels about the one sentence a relief is solved by.

Marks negotiate with each other and are solved first; a push is added to the answer. Row 1 is one dale and
one push, the push in two places, so what the ordering costs is the difference between three pictures. Row 2
is how much of a panel to pin: every region, only the ground a player walks, and the same again with a finite
`reach` under it.

Nothing here is a map. The renders read the stored layout through `POST /sketch/columns`.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import grid, lobed_ring, moor

PANEL_W, PANEL_D = 120, 96
COL_X, ROW_Z = grid(3, 2, PANEL_W, PANEL_D)

# Cut against this board's own `incline`, which holds 30% of its ground between 10 and 19 degrees and
# almost none above 50: banding at the cards' usual 15 and 40 would stripe every gentle flank row by row
# and leave the fell no scree at all.
MOOR = moor(grass_to=25, dirt_to=45)
GROUND_TOP = 60  # the island's raw column, before the relief solves it

DALE_BASE = 18   # row 1: what the field settles toward between the brae and the strand
OPEN_BASE = 6    # row 2: what an unmarked field settles at, and what a finite reach pulls it to


def area(mark_id, height, ring, bevel=0):
    return {"id": mark_id, "kind": "area", "h": height, "bevel": bevel, "ring": ring}


def fell(cx, cz, amount=12):
    """The one push every panel but the first uses, identical in all five.

    A nominal skirt of 0.55 blocks a cell, because the read's figure is an average and the smoothstep it
    eases with is half again as steep at its middle: 0.55 peaks at 0.82, which is 39 degrees and scree. A
    skirt the read calls 1.3 peaks at 2.0 — 63 degrees — and the slope stack paints the whole landform as
    crag whatever it was meant to be.

    `crown` 0, so the lift inside the ring is the same number everywhere and the summit is the ground plus
    twelve. A crown would add most where the ground is lowest, which on this card would cancel the very
    thing the first row is about."""
    return {"id": "fell", "ring": lobed_ring(cx, cz, 13, lobes=4, depth=0.16), "amount": amount,
            "falloff": 22, "crown": 0, "roughness": 0, "seed": 1}


# --- row 1: one dale, one push, two places ------------------------------------------------------------

def dale_marks(cx, cz):
    """The hillside: a brae pinned at 30 along the north edge, a strand at 14 along the south, and a holm
    at 10 cut into the fall between them.

    Three marks rather than one, because a lone constraint has nothing to negotiate with and the smoothest
    field through it is the constant one. Two of them long and facing each other rather than three small
    ones scattered, because a field pinned only in patches relaxes into fans radiating from each patch,
    while a field pinned along two opposite edges relaxes into the ramp between them.

    Neither band carries a `bevel`. A bevel is paid for out of the mark's own floor from every side at
    once, so a nine-cell band with a bevel of four pins nothing at all and the read does not call it
    silent — the panel simply comes out at whatever else is speaking."""
    return [area("brae", 30, band(cx, cz, -47, -38)),
            area("strand", 14, band(cx, cz, 38, 47)),
            area("holm", 10, lobed_ring(cx + 8, cz, 13, lobes=5, depth=0.14), bevel=5)]


def dale(cx, cz):
    return dale_marks(cx, cz), []


def push_on_it(cx, cz):
    """The push centred on the holm. Its ring covers ground a mark pins, and the mark does not win."""
    return dale_marks(cx, cz), [fell(cx + 8, cz)]


def push_beside_it(cx, cz):
    """The same push, moved until its ring is clear of the holm. The falloff is not."""
    return dale_marks(cx, cz), [fell(cx - 24, cz)]


# --- row 2: how much of a panel to pin ----------------------------------------------------------------

def band(cx, cz, z_from, z_to):
    """A mark across the whole panel: the shape a boundary condition takes, and the shape pinning a whole
    *region* takes."""
    half = (PANEL_W - 6) / 2
    return [[cx - half, cz + z_from], [cx + half, cz + z_from],
            [cx + half, cz + z_to], [cx - half, cz + z_to]]


def pinned(cx, cz):
    """Every region stated: a coast, a holm and a shelf, tiling the panel between them."""
    return ([area("coast", 10, band(cx, cz, 20, 47), bevel=5),
             area("holm", 20, band(cx, cz, -10, 19), bevel=5),
             area("shelf", 30, band(cx, cz, -47, -11), bevel=5)],
            [fell(cx - 26, cz - 6)])


def free_flanks(cx, cz):
    """The same three heights, pinned only where a player stands on them. Everything else is left to the
    relaxation, which is the ground the fell then rises out of."""
    return ([area("coast", 10, band(cx, cz, 38, 47)),
             area("holm", 20, lobed_ring(cx + 20, cz + 16, 17, lobes=5, depth=0.14), bevel=5),
             area("shelf", 30, lobed_ring(cx + 34, cz - 24, 11, lobes=4, depth=0.12), bevel=4)],
            [fell(cx - 26, cz - 6)])


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
