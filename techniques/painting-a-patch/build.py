"""Writes painting-a-patch.layout.json — twelve panels asking one question of one shape: whose surface does
a cell wear?

Every panel is the same island — a plain at 8 with one hill pushed up on its east side — and the same
lobed outline drawn on it carrying the same scree theme. What changes between two panels is what that
shape says about its own height, and which layer it is drawn on. Both decide the same thing: whether the
shape forms the surface of the cells it covers, which is the whole of whether any of its paint lands.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, grid, lobed_ring, moor

PANEL_W, PANEL_D = 64, 60
COL_X, ROW_Z = grid(4, 3, PANEL_W, PANEL_D)
GROUND_TOP = 12          # the island's own drawn thickness, which is the top every patch is tested against
PLAIN = 8

# Where the ground theme's slope bands cut, read off this board's own `incline`.
GRASS_TO, DIRT_TO = 60, 75
GROUND = moor(GRASS_TO, DIRT_TO)


def scree():
    """The patch's theme: the moor with a drift of scree for a surface, everything under it unchanged. One
    paint over all twelve panels, so a panel that differs in its picture differs in what its shape said."""
    theme = json.loads(json.dumps(GROUND))
    theme["surface"]["material"] = depth_stack((SOLID(13), 1), (SOLID(3, 1), 2))
    return theme


# The twelve statements, in the order the card reads them. `patch` is what the shape carrying the theme says
# about its own height; `where` is which outline it is drawn on; a panel needing a second shape says so by
# its `where`. `layer` moves the patch off the ground layer onto one of its own, stating that layer's
# `base_y` and whether its group carries a relief.
#
# Row 1 asks whether the patch owns any paint at all. Row 2 asks what owning it costs the ground
# underneath. Row 3 asks the same two questions of a patch that is not on the ground layer at all.
PANELS = [
    ("says-nothing",   "flat",  {"operation": "add"}, None),
    ("one-short",      "flat",  {"operation": "add", "base_height": GROUND_TOP - 1}, None),
    ("level-with-it",  "flat",  {"operation": "add", "base_height": GROUND_TOP}, None),
    ("override-thin",  "flat",  {"operation": "add", "base_height": 1, "override": True}, None),
    ("raise-flush",    "flat",  {"operation": "add", "height_mode": "raise",
                                 "base_height": 0, "skirt": 0}, None),
    ("across-a-slope", "flank", {"operation": "add", "height_mode": "raise",
                                 "base_height": 0, "skirt": 0}, None),
    ("over-excluded",  "shelf", {"operation": "add", "base_height": 1, "override": True}, None),
    ("over-the-void",  "coast", {"operation": "add", "base_height": GROUND_TOP}, None),
    # A second layer keeps its own span per column and its own owner per cell, so a patch on one is not a
    # patch: it is a slab standing at whatever height the layer and the shape between them state.
    ("on-a-layer",     "flat",  {"operation": "add", "base_height": GROUND_TOP}, {"base_y": 0}),
    ("layer-on-a-hill", "flank", {"operation": "add", "base_height": GROUND_TOP}, {"base_y": 0}),
    ("layer-on-top",   "flat",  {"operation": "add", "base_height": 1}, {"base_y": PLAIN}),
    ("layer-solved",   "flank", {"operation": "add", "base_height": GROUND_TOP},
                                {"base_y": 0, "relief": True}),
]

THEMES = {"moor": GROUND}
shapes, groups, relief, over_layers = [], [], {}, []
for index, (name, where, patch, layer) in enumerate(PANELS):
    col, row = index % 4, index // 4
    x0, z0 = COL_X[col], ROW_Z[row]
    cx, cz = x0 + PANEL_W / 2, z0 + PANEL_D / 2
    THEMES[f"scree-{name}"] = scree()

    island = f"island-{name}"
    shapes.append({"id": island, "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    members = [island]

    # A low table the relief never solves: `exclude` takes its cells out of the group's footprint, so
    # nothing writes a solved height back over them and the merged raw column is what is built. It states
    # one course and comes out at the island's twelve, because the merge keeps the taller of the two.
    if where == "shelf":
        members.append(f"shelf-{name}")
        shapes.append({"id": f"shelf-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                       "base_height": 1, "relief_scope": "exclude", "theme": "moor",
                       "min_x": cx - 26, "min_z": cz - 19, "max_x": cx + 2, "max_z": cz + 19})

    ring = {"flat":  lobed_ring(cx - 15, cz, 9, lobes=4, depth=0.20),
            "shelf": lobed_ring(cx - 12, cz, 8, lobes=4, depth=0.20),
            "flank": lobed_ring(cx + 14, cz + 13, 9, lobes=4, depth=0.20),
            "coast": lobed_ring(cx - 15, z0 + 4, 9, lobes=4, depth=0.20)}[where]
    drawn = {"id": f"patch-{name}", "type": "polygon", "floor": 0,
             "vertices": ring, "theme": f"scree-{name}", **patch}
    if layer is None:
        members.append(f"patch-{name}")
        shapes.append(drawn)
    else:
        over_layers.append({"id": f"over-{name}", "name": f"Over {name}", "base_y": layer["base_y"],
                            "layout": {"shapes": [drawn],
                                       "groups": [{"id": f"over-{name}", "name": f"over-{name}",
                                                   "mirrors": False, "shapeIds": [f"patch-{name}"]}]}})

    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": members})
    # One hill on the east half of every panel, so each has a summit, a flank and a plain. A crown on a
    # round ring climbs to the middle rather than holding the ring's level, and 10 over a falloff of 13 is
    # a flank of 0.77 blocks a cell — ground a patch can be drawn across without it being a cliff.
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "marks": [], "pushes": [
        {"id": "hill", "ring": lobed_ring(cx + 14, cz, 9, lobes=5, depth=0.20),
         "amount": 10, "falloff": 13, "crown": 8, "roughness": 0, "seed": 3}]}
    # The same field again, for the one panel that asks what it costs to make a second layer follow the
    # terrain: the only way is to state the ground's relief a second time, over the patch's own group.
    if layer and layer.get("relief"):
        relief[f"over-{name}"] = json.loads(json.dumps(relief[name]))

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": THEMES,
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}]
              # Ordered by base_y, because the list order and the base_y order stating different things
              # about which layer is on top is `SK20`.
              + sorted(over_layers, key=lambda over: over["base_y"]),
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "painting-a-patch.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(THEMES)} themes, {1 + len(over_layers)} layers -> {out}")
for index, (name, where, patch, layer) in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    said = " ".join(f"{k}={v}" for k, v in patch.items() if k != "operation")
    on = "ground" if layer is None else f"over-{name} (base_y {layer['base_y']})"
    print(f"  {name:15s} on {where:6s} at x{x0:5d} z{z0:5d}  [{on}]  {said}")
