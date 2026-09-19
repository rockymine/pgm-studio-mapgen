"""Writes painting-a-patch.layout.json — eight panels asking one question of one shape: does it own the
paint it carries?

Every panel is the same island — a plain at 8 with one hill pushed up on its east side — and the same
lobed outline drawn on it carrying the same scree theme. What changes between two panels is only what
that shape says about its own height, which is the whole of what decides whether any of its paint lands.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import SOLID, depth_stack, grid, lobed_ring, moor

PANEL_W, PANEL_D = 64, 60
COL_X, ROW_Z = grid(4, 2, PANEL_W, PANEL_D)
GROUND_TOP = 12          # the island's own drawn thickness, which is the top every patch is tested against
PLAIN = 8

# Where the ground theme's slope bands cut, read off this board's own `incline`.
GRASS_TO, DIRT_TO = 60, 75
GROUND = moor(GRASS_TO, DIRT_TO)


def scree():
    """The patch's theme: the moor with a drift of scree for a surface, everything under it unchanged. One
    paint over all eight panels, so a panel that differs in its picture differs in what its shape said."""
    theme = json.loads(json.dumps(GROUND))
    theme["surface"]["material"] = depth_stack((SOLID(13), 1), (SOLID(3, 1), 2))
    return theme


# The eight statements, in the order the card reads them. `patch` is what the shape carrying the theme says
# about its own height; `where` is which outline it is drawn on; a panel needing a second shape says so by
# its `where`. Row 1 asks whether the patch owns any paint at all; row 2 asks what owning it costs the
# ground underneath.
PANELS = [
    ("says-nothing",   "flat",  {"operation": "add"}),
    ("one-short",      "flat",  {"operation": "add", "base_height": GROUND_TOP - 1}),
    ("level-with-it",  "flat",  {"operation": "add", "base_height": GROUND_TOP}),
    ("override-thin",  "flat",  {"operation": "add", "base_height": 1, "override": True}),
    ("raise-flush",    "flat",  {"operation": "add", "height_mode": "raise",
                                 "base_height": 0, "skirt": 0}),
    ("across-a-slope", "flank", {"operation": "add", "height_mode": "raise",
                                 "base_height": 0, "skirt": 0}),
    ("over-excluded",  "shelf", {"operation": "add", "base_height": 1, "override": True}),
    ("over-the-void",  "coast", {"operation": "add", "base_height": GROUND_TOP}),
]

THEMES = {"moor": GROUND}
shapes, groups, relief = [], [], {}
for index, (name, where, patch) in enumerate(PANELS):
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
    members.append(f"patch-{name}")
    shapes.append({"id": f"patch-{name}", "type": "polygon", "floor": 0,
                   "vertices": ring, "theme": f"scree-{name}", **patch})

    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": members})
    # One hill on the east half of every panel, so each has a summit, a flank and a plain. A crown on a
    # round ring climbs to the middle rather than holding the ring's level, and 10 over a falloff of 13 is
    # a flank of 0.77 blocks a cell — ground a patch can be drawn across without it being a cliff.
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "marks": [], "pushes": [
        {"id": "hill", "ring": lobed_ring(cx + 14, cz, 9, lobes=5, depth=0.20),
         "amount": 10, "falloff": 13, "crown": 8, "roughness": 0, "seed": 3}]}

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": THEMES,
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "painting-a-patch.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(PANELS)} panels, {len(THEMES)} themes -> {out}")
for index, (name, where, patch) in enumerate(PANELS):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    said = " ".join(f"{k}={v}" for k, v in patch.items() if k != "operation")
    print(f"  {name:14s} on {where:6s} at x{x0:5d} z{z0:5d}  {said}")
