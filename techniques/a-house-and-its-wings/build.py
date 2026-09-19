"""Writes a-house-and-its-wings.layout.json — twelve pads, one house style, and every way two rectangles of
one plan can meet.

A house is a prop stating a list of touching rectangles. Nothing in it is named by an author: which
rectangle is the hall and which the cross wing follows from the ridges and the edge they share, and five
`HJ` rules decide whether the pair is a building at all.

Row 1 is one hall and one wing at the SAME height, met three ways, against the lower wing the corpus
already has. Row 2 is what the ridges decide. Row 3 is the three ways two rectangles fail to be one plan,
and the U-plan an author actually wants. Row 4 is the other thing a wing states about itself: its own roof
form and its own pitch, so one building can carry two.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, grid, moor

PANEL_W, PANEL_D = 64, 56
COL_X, ROW_Z = grid(4, 4, PANEL_W, PANEL_D)
GROUND_TOP = 20
PLAIN = 8

MOOR = moor(grass_to=35, dirt_to=55)
YARD = {   # the pad each house stands on, so a footprint can be seen against the ground
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(1)},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": SOLID(1), "fill": SOLID(1),
    "surface": {"enabled": True, "depth": 3, "material": depth_stack((SOLID(13), 1), (SOLID(3, 1), 2))},
}
BOTHY = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bothy.style.json")))

# `HP3` caps a placed building at 192 blocks of footprint, so every plan here is drawn inside it: a hall
# of 96 leaves room for one cross wing of 48 or two of 40.
HALL_W, HALL_D = 12, 8       # the hall: a range with its ridge along x
WING_W, WING_D = 6, 8        # the cross wing: its ridge runs into the hall's long edge


def wing(x0, z0, width, depth, **spec):
    """One rectangle of a plan, as two opposite corners. `spec` is what it states about itself — its storey
    count, its ridge axis, and whether it projects."""
    return {"corners": [[x0, z0], [x0 + width - 1, z0 + depth - 1]],
            "spec": {k: v for k, v in spec.items() if v is not None}}


def plan(name, cx, cz):
    """The wings of one panel's house, in the panel's own coordinates. Every hall is the same rectangle at
    the same place; only what the second rectangle says, or where it sits, changes."""
    hx, hz = cx - HALL_W // 2, cz - 6
    hall = lambda **spec: wing(hx, hz, HALL_W, HALL_D, ridge="alongX", **spec)
    # The cross wing hangs off the hall's south edge, sharing the whole of its own north end with it.
    cross = lambda **spec: wing(cx - WING_W // 2, hz + HALL_D, WING_W, WING_D, ridge="alongZ", **spec)
    return {
        # Row 1 — the joint, at one height.
        "one-range":   [hall()],
        "marching":    [hall(), cross()],
        "projecting":  [hall(), cross(projects=True)],
        "lower-wing":  [hall(), cross(storeysHigh=1)],
        # Row 2 — what the ridges decide.
        "a-t-plan":    [hall(), wing(cx - 2, hz + HALL_D, 5, WING_D, ridge="alongZ"),
                        wing(cx - 2, hz - WING_D, 5, WING_D, ridge="alongZ")],
        "side-by-side": [wing(hx, hz, HALL_W, 7, ridge="alongX"),
                         wing(hx, hz + 7, HALL_W, 7, ridge="alongX")],
        "end-to-end":  [wing(hx, hz, HALL_W, 7, ridge="alongZ"),
                        wing(hx, hz + 7, HALL_W, 7, ridge="alongZ")],
        "wing-overtops": [wing(cx - 4, hz, 8, 8, ridge="alongX"),
                          wing(cx - 7, hz + 8, 14, 6, ridge="alongZ")],
        # Row 3 — the three ways two rectangles are not one plan, and the one an author wants.
        "overlapping": [hall(), wing(cx - WING_W // 2, hz + HALL_D - 3, WING_W, WING_D, ridge="alongZ")],
        "partial-edge": [hall(), wing(hx + HALL_W - 3, hz + HALL_D, WING_W, WING_D, ridge="alongZ")],
        "apart":       [hall(), wing(cx - WING_W // 2, hz + HALL_D + 4, WING_W, WING_D, ridge="alongZ")],
        "a-u-plan":    [hall(), wing(hx, hz + HALL_D, 5, WING_D, ridge="alongZ"),
                        wing(hx + HALL_W - 5, hz + HALL_D, 5, WING_D, ridge="alongZ")],
        # Row 4 — a wing states its own roof, so a plan can carry two forms. A lower wing running into a
        # flat-topped range meets a WALL rather than a roof, which is the case a gable hall cannot give.
        "flat-hall":   [hall(form="flat"), cross(form="gable", storeysHigh=1)],
        "flat-wing":   [hall(), cross(form="flat", storeysHigh=1)],
        "shed-wing":   [hall(), cross(form="shed", storeysHigh=1)],
        "shallow-wing": [hall(), cross(form="gable", pitch=1, storeysHigh=1)],
    }[name]


PANELS = ["one-range", "marching", "projecting", "lower-wing",
          "a-t-plan", "side-by-side", "end-to-end", "wing-overtops",
          "overlapping", "partial-edge", "apart", "a-u-plan",
          "flat-hall", "flat-wing", "shed-wing", "shallow-wing"]

shapes, groups, relief, props = [], [], {}, []
for index, name in enumerate(PANELS):
    col, row = index % 4, index // 4
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W // 2, z0 + PANEL_D // 2
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    # The yard: a paint patch at the island's own height, so a plan's footprint reads against the grass.
    shapes.append({"id": f"yard-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "yard",
                   "min_x": cx - 14, "min_z": cz - 12, "max_x": cx + 14, "max_z": cz + 14})
    groups.append({"id": name, "name": name, "mirrors": False,
                   "shapeIds": [f"island-{name}", f"yard-{name}"]})
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "marks": [], "pushes": []}
    props.append({"id": name, "kind": "house", "layer": "ground", "seed": 5, "front": "negZ",
                  "style": "bothy", "wings": plan(name, cx, cz)})

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR, "yard": YARD},
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
    "dressing": {"styles": {"bothy": BOTHY}, "props": props},
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a-house-and-its-wings.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels -> {out}")
for index, name in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    said = " + ".join(f"{w['corners'][0]}..{w['corners'][1]} {w['spec']}" for w in plan(
        name, x0 + PANEL_W // 2, z0 + PANEL_D // 2))
    print(f"  {name:14s} at x{x0:5d} z{z0:5d}  {said}")
