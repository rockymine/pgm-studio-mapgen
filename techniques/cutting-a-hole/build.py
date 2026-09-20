"""Seven islands, each stating the same negative space a different way.

A subtract is how a board says where ground is *not*. It is the one instrument that removes rather than
moves — relief grades a surface, a subtract deletes the column — and it is what a compile writes when a plan
leaves a gap between its pieces. Beside it sits the override add, which is the only add that can stand over
a cut, and the only one that wins a column it is too short to have earned.

Every panel is one island 68 x 52 at surface 9, so the only thing that differs between two panels is the
instrument drawn on it.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cards import SOLID, MOOR, grid  # noqa: E402

FLOOR, TOP = 0, 9           # the island: floor 0, nine courses, standing surface 9
ISLE_W, ISLE_D = 68, 52
COL_X, ROW_Z = grid(4, 2, panel_w=ISLE_W, panel_d=ISLE_D, gap=20)

PANELS = ["a-hole", "height-not-read", "a-lid", "a-room",
          "override-wins", "the-taller-wins", "a-declared-void"]

STONE = {"kind": "cell", "cellSize": 4, "rise": 2, "palette": [SOLID(98), SOLID(98, 1), SOLID(1, 6)]}


def centre(name):
    index = PANELS.index(name)
    return COL_X[index % 4], ROW_Z[index // 4]


def isle(name):
    """The island's own bounds."""
    cx, cz = centre(name)
    return cx - ISLE_W // 2, cx + ISLE_W // 2, cz - ISLE_D // 2, cz + ISLE_D // 2


def rect(shape_id, bounds, floor, height, operation="add", override=False, material=None):
    x0, x1, z0, z1 = bounds
    drawn = {"id": shape_id, "type": "rectangle", "operation": operation,
             "floor": round(floor), "base_height": round(height),
             "min_x": round(x0), "max_x": round(x1), "min_z": round(z0), "max_z": round(z1)}
    if override:
        drawn["override"] = True
    if material:
        drawn["material"] = material
    return drawn


shapes, groups = [], []
for name in PANELS:
    x0, x1, z0, z1 = isle(name)
    cx, cz = centre(name)
    drawn = [rect(f"{name}-ground", (x0, x1, z0, z1), FLOOR, TOP)]

    if name == "a-hole":
        # One cut through the island. Nothing states a depth, because a subtract has none to state.
        drawn.append(rect(f"{name}-cut", (cx - 10, cx + 10, cz - 10, cz + 10), FLOOR, 4, "subtract"))

    elif name == "height-not-read":
        # The same footprint twice at two wildly different heights. The columns come out identical.
        drawn += [rect(f"{name}-thin", (cx - 24, cx - 6, cz - 10, cz + 10), FLOOR, 1, "subtract"),
                  rect(f"{name}-tall", (cx + 6, cx + 24, cz - 10, cz + 10), FLOOR, 40, "subtract")]

    elif name == "a-lid":
        # An override add whose FLOOR stands above the cut's floor: the column's one span moves up and the
        # void stays open under it. This is a deck over a hole, not a filled hole.
        drawn += [rect(f"{name}-cut", (cx - 12, cx + 12, cz - 12, cz + 12), FLOOR, 6, "subtract"),
                  rect(f"{name}-deck", (cx - 12, cx + 12, cz - 12, cz + 12), 6, 3, override=True,
                       material=STONE)]

    elif name == "a-room":
        # A floor and a ceiling either side of a stated void. The subtract carries the courses the room is,
        # the floor's top stops at its floor and the ceiling's floor starts at its top — which is what SK13
        # asks for. The ceiling is on a layer of its own because a layer holds one span a column: drawn
        # beside the floor it would simply take the column off it, being the taller of the two.
        drawn += [rect(f"{name}-void", (cx - 12, cx + 12, cz - 12, cz + 12), 3, 5, "subtract"),
                  rect(f"{name}-floor", (cx - 12, cx + 12, cz - 12, cz + 12), FLOOR, 3, override=True,
                       material=STONE)]

    elif name == "override-wins":
        # An override add four courses tall on ground nine courses tall. It is shorter and it still takes
        # the column, because the set it belongs to is resolved after the ordinary adds.
        drawn.append(rect(f"{name}-plate", (cx - 12, cx + 12, cz - 12, cz + 12), FLOOR, 4, override=True,
                          material=STONE))

    elif name == "the-taller-wins":
        # Two override adds on one footprint. Within the privileged set the taller surface wins and document
        # order decides nothing, so the second — written first here — is not what stands.
        drawn += [rect(f"{name}-high", (cx - 12, cx + 12, cz - 12, cz + 12), FLOOR, 14, override=True,
                       material=STONE),
                  rect(f"{name}-low", (cx - 12, cx + 12, cz - 12, cz + 12), FLOOR, 4, override=True,
                       material=SOLID(155))]

    elif name == "a-declared-void":
        # What a compile writes. `PlanVoids.Declare` names every gap between pieces a `void-N` buffer and
        # the compiler emits it as this: a polygon subtract carrying an id, a type, an operation and its
        # vertices, and no floor and no height at all.
        drawn.append({"id": "void-1-cut", "type": "polygon", "operation": "subtract",
                      "vertices": [[cx - 12, cz - 12], [cx + 12, cz - 12],
                                   [cx + 12, cz + 12], [cx - 12, cz + 12]]})

    shapes += drawn
    groups.append({"id": name, "name": name, "mirrors": False,
                   "shapeIds": [shape["id"] for shape in drawn]})

# The room's ceiling, on the second layer its own floor cannot share.
CEILING_X, CEILING_Z = centre("a-room")
ceiling = rect("a-room-ceiling", (CEILING_X - 12, CEILING_X + 12, CEILING_Z - 12, CEILING_Z + 12),
               8, 2, material=STONE)
ceiling_layer = {"id": "a-room-ceiling", "name": "the room's ceiling", "base_y": 0, "kind": "made",
                 "part_of": "a-room", "layout": {"shapes": [ceiling], "groups": [
                     {"id": "a-room-ceiling", "name": "the room's ceiling", "mirrors": False,
                      "shapeIds": ["a-room-ceiling"]}]}}

layout = {
    "setup": {"bbox": {"min_x": min(COL_X) - ISLE_W, "max_x": max(COL_X) + ISLE_W,
                       "min_z": min(ROW_Z) - ISLE_D, "max_z": max(ROW_Z) + ISLE_D},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR},
    "mapTheme": "moor",
    "relief": {},
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}, ceiling_layer],
}

if __name__ == "__main__":
    json.dump(layout, open(os.path.join(HERE, "cutting-a-hole.layout.json"), "w"), indent=1)
    print(f"{len(PANELS)} panels, {len(shapes)} shapes on the ground layer, one made layer")
    for name in PANELS:
        print(f"  {name:18s} island x{isle(name)[0]:5d}..{isle(name)[1]:<5d} "
              f"z{isle(name)[2]:5d}..{isle(name)[3]:<5d}")
