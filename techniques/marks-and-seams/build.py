"""Writes marks-and-seams.layout.json — twelve panels on what two marks do to the ground they share.

A mark states a height over a patch of the footprint and the relaxation solves the smoothest surface that
satisfies all of them. Two marks never negotiate: each pins its own cells, and what happens between them is
decided entirely by how much ground neither one claimed.

Row 1 is one pair of pads — a low one and a high one — meeting four ways. Row 2 is the mark that states a
step on purpose, and three that state nothing anybody can see. Row 3 is what the shape of a mark does to the
field around it.
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import grid, lobed_ring, moor, round_ring

PANEL_W, PANEL_D = 96, 76
COL_X, ROW_Z = grid(4, 3, PANEL_W, PANEL_D)
GROUND_TOP = 40
LOW, HIGH = 8, 20

# Where the ground theme's slope bands cut, read off this board's own `incline`.
MOOR = moor(grass_to=35, dirt_to=55)


def area(mark_id, height, ring, bevel=0):
    return {"id": mark_id, "kind": "area", "h": height, "bevel": bevel, "ring": ring}


def zband(cx, z_from, z_to, inset=4):
    """A band across the panel between two z. A ring covers the cells whose CENTRES fall inside it, so two
    bands stated to share their boundary coordinate leave no cell between them and two stated one apart
    leave one — which is the whole of row 1."""
    half = PANEL_W / 2 - inset
    return [[cx - half, z_from], [cx + half, z_from], [cx + half, z_to], [cx - half, z_to]]


def pads(cx, cz, z0, gap=0, bevel=0):
    """A low pad in the north half and a high one in the south, with `gap` cells of unpinned ground between
    them. The two pads never move; only what is between them does."""
    seam = cz
    return [area("low", LOW, zband(cx, z0 + 8, seam - gap)),
            area("high", HIGH, zband(cx, seam, z0 + PANEL_D - 8), bevel=bevel)]


PANELS = ["butted", "one-apart", "gapped", "bevelled",
          "a-scarp", "bevel-too-wide", "off-the-land", "half-off",
          "one-height", "a-summit", "a-plateau", "facing"]

shapes, groups, relief = [], [], {}
for index, name in enumerate(PANELS):
    col, row = index % 4, index // 4
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": [f"island-{name}"]})

    if name == "butted":
        marks = pads(cx, cz, z0)
    elif name == "one-apart":
        marks = pads(cx, cz, z0, gap=1)
    elif name == "gapped":
        marks = pads(cx, cz, z0, gap=10)
    elif name == "bevelled":
        marks = pads(cx, cz, z0, bevel=6)
    elif name == "a-scarp":
        # One mark instead of two: a scarp states both sides and the face between them, so the step is
        # authored rather than left over. `face` is how far the drop runs across and `band` how far either
        # side is held before the surface is free again.
        marks = [{"id": "brink", "kind": "scarp", "high": HIGH, "low": LOW, "face": 2, "band": 14,
                  "points": [[x0 + 6, cz], [x0 + PANEL_W - 6, cz]]}]
    elif name == "bevel-too-wide":
        # A bevel is paid for out of the mark's own floor from every side at once, so a nine-cell band at
        # bevel 5 has no floor left. It pins nothing and is NOT silent: its ring does cover cells.
        marks = [area("low", LOW, zband(cx, z0 + 8, cz)),
                 area("crest", HIGH, zband(cx, cz + 10, cz + 19), bevel=5)]
    elif name == "off-the-land":
        # A ring drawn wholly off the footprint pins nothing at all, which IS what `silentMarks` is for.
        marks = [area("low", LOW, zband(cx, z0 + 8, cz)),
                 area("high", HIGH, zband(cx, cz, z0 + PANEL_D - 8)),
                 area("elsewhere", 30, round_ring(cx, z0 - 40, 12))]
    elif name == "half-off":
        # A ridge traced past the coast pins the coastal strip at its own heights and leaves its crest off
        # the map — a mountainside cut through rather than ground decaying to base. Nothing reports it.
        marks = [{"id": "ridge", "kind": "line", "r": 14, "h": [LOW, 34],
                  "points": [[cx, z0 + 12], [cx, z0 + PANEL_D + 26]]}]
    elif name == "one-height":
        marks = [area("plateau", 30, lobed_ring(cx, cz, 20, lobes=5, depth=0.14))]
    elif name == "a-summit":
        marks = [{"id": "summit", "kind": "point", "at": [cx, cz], "h": 30, "r": 6}]
    elif name == "a-plateau":
        marks = [area("plateau", 30, lobed_ring(cx, cz, 20, lobes=5, depth=0.14))]
    else:  # facing
        marks = [area("north", 30, zband(cx, z0 + 6, z0 + 18)),
                 area("south", LOW, zband(cx, z0 + PANEL_D - 18, z0 + PANEL_D - 6))]

    for mark in marks:
        mark["id"] = f"{mark['id']}-{name}"
    # `reach` is how far a mark's influence travels before the field falls back to `base`. Zero is
    # unlimited, so a group whose marks all state one height comes out at that height everywhere: a
    # landform needs something to fall to, and the fall is either `reach` or a second mark.
    reach = 24 if name in ("a-summit", "a-plateau") else 0
    relief[name] = {"base": LOW, "reach": reach, "step": 1, "marks": marks, "pushes": []}

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 10, "max_x": COL_X[-1] + PANEL_W + 10,
                       "min_z": ROW_Z[0] - 10, "max_z": ROW_Z[-1] + PANEL_D + 10},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR},
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marks-and-seams.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels -> {out}")
for index, name in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    kinds = " ".join(f"{m['kind']}:{m['id'].split('-')[0]}" for m in relief[name]["marks"])
    print(f"  {name:15s} at x{x0:5d} z{z0:5d}  {kinds}")
