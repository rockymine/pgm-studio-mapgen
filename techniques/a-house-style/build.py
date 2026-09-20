"""Writes a-house-style.layout.json — twelve pads, one plan, and one knob of the style changed on each.

`techniques/a-house-and-its-wings` varies the PLAN and holds the style still. This card does the other
half: every pad carries the same 12 x 8 rectangle at the same place, and what differs between two of them
is one field of the `HouseStyle` the prop names. So a form, a pitch, an overhang, a window or a storey is
read as itself rather than as part of a building somebody designed.

The base is `bothy`, taken whole from `specs/opus5-glassmere` and shared with the wings card, so the two
read against one another.
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cards import SOLID, depth_stack, grid, moor  # noqa: E402

PANEL_W, PANEL_D = 56, 48
COL_X, ROW_Z = grid(4, 3, PANEL_W, PANEL_D)
GROUND_TOP = 20
PLAIN = 8
HALL_W, HALL_D = 12, 8            # the one rectangle every pad carries

MOOR = moor(grass_to=35, dirt_to=55)
YARD = {
    "bedrock": {"relative": False, "value": 1}, "rimEdges": "void",
    "rim": {"enabled": False, "depth": 1, "material": SOLID(1)},
    "wallEnabled": True, "wallOnTerrainFaces": True, "wall": SOLID(1), "fill": SOLID(1),
    "surface": {"enabled": True, "depth": 3, "material": depth_stack((SOLID(13), 1), (SOLID(3, 1), 2))},
}
BOTHY = json.load(open(os.path.join(os.path.dirname(HERE), "a-house-and-its-wings", "bothy.style.json")))


def styled(**changes):
    """The base style with one thing changed. `changes` are dotted paths into `shell`, so the panel's own
    name says which field it is about and the rest is held identical."""
    out = copy.deepcopy(BOTHY)
    for path, value in changes.items():
        *walk, leaf = path.split("__")
        target = out["shell"]
        for step in walk:
            target = target[step]
        target[leaf] = value
    return out


# One knob a panel, and the panel is named for it. Row 1 is the six roof forms; row 2 is what the roof
# states about itself beside its form; row 3 is the wall, the openings and the second storey.
PANELS = {
    "gable":        {},                                    # the base, unchanged
    "flat":         {"roof__form": "flat"},
    "hip":          {"roof__form": "hip"},
    "gambrel":      {"roof__form": "gambrel"},
    "shed":         {"roof__form": "shed"},
    "saltbox":      {"roof__form": "saltbox"},
    "pitch-1":      {"roof__pitch": 1},
    "overhang-3":   {"roof__overhang": 3},
    "windows-none": {"windows__form": "none"},
    # `HS1`: an `arched` window is turned by a stair's own facing, so its block has to BE a stair.
    # The form and the block are one decision rather than two.
    "windows-arched": {"windows__form": "arched", "windows__block": 134},
    "no-beams":     {"beams__any": False},
    "one-storey":   {"storeys": BOTHY["shell"]["storeys"][:1]},
}
ORDER = list(PANELS)


def centre(name):
    index = ORDER.index(name)
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    return x0 + PANEL_W // 2, z0 + PANEL_D // 2


shapes, groups, relief, props, styles = [], [], {}, [], {}
for index, name in enumerate(ORDER):
    x0, z0 = COL_X[index % 4], ROW_Z[index // 4]
    cx, cz = centre(name)
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    shapes.append({"id": f"yard-{name}", "type": "rectangle", "operation": "add", "floor": 0,
                   "base_height": GROUND_TOP, "theme": "yard",
                   "min_x": cx - 12, "min_z": cz - 10, "max_x": cx + 12, "max_z": cz + 12})
    groups.append({"id": name, "name": name, "mirrors": False,
                   "shapeIds": [f"island-{name}", f"yard-{name}"]})
    relief[name] = {"base": PLAIN, "reach": 0, "step": 1, "marks": [], "pushes": []}
    styles[name] = styled(**PANELS[name])
    hx, hz = cx - HALL_W // 2, cz - HALL_D // 2
    props.append({"id": name, "kind": "house", "layer": "ground", "seed": 5, "front": "negZ",
                  "style": name,
                  "wings": [{"corners": [[hx, hz], [hx + HALL_W - 1, hz + HALL_D - 1]],
                             "spec": {"ridge": "alongX"}}]})

layout = {
    "setup": {"bbox": {"min_x": COL_X[0] - 8, "max_x": COL_X[-1] + PANEL_W + 8,
                       "min_z": ROW_Z[0] - 8, "max_z": ROW_Z[-1] + PANEL_D + 8},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR, "yard": YARD},
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}],
    "dressing": {"styles": styles, "props": props},
}

if __name__ == "__main__":
    json.dump(layout, open(os.path.join(HERE, "a-house-style.layout.json"), "w"), indent=1)
    print(f"{len(ORDER)} panels, one {HALL_W} x {HALL_D} rectangle each, {len(styles)} styles")
    for name in ORDER:
        said = ", ".join(f"{k.replace('__', '.')} = {json.dumps(v)[:40]}" for k, v in PANELS[name].items())
        print(f"  {name:16s} at {centre(name)}  {said or 'the base, unchanged'}")
