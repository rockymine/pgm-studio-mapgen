"""Seven L-shaped lanes, each climbing the same eight blocks a different way.

A composed lane bends. A wool approach is an L, a hub arm turns into its spawn, and the instruments that
raise ground do not all survive the corner — which is the whole reason the lane here is an L rather than a
bar. Every panel is the same shape: a stem **12 wide** running 40 north, a **12 x 12** corner at its head,
and an arm **36** east of that. The foot is at surface 9 and the head eight blocks up at 17.

The climb is stated in nine steps where an instrument steps at all: three up the stem, one on the corner,
five along the arm. The reads are taken along the same path on every panel — up the stem, round the corner,
out to the end of the arm.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cards import SOLID, MOOR, grid  # noqa: E402

FOOT, HEAD = 9, 17
WIDE = 12                   # every leg of every L
STEM, ARM = 40, 36          # the stem runs north, the arm east off its head
COL_X, ROW_Z = grid(4, 2, panel_w=WIDE + ARM, panel_d=STEM, gap=26)

PANELS = ["piece-steps", "piece-treads", "tilted", "plates", "marks", "push", "deck"]

# Where each step falls along the path: three on the stem, one on the corner, five on the arm. A plan piece
# is a rectangle, so the corner is a piece of its own — that is what a bend costs at this tier.
STEM_STEPS, ARM_STEPS = 3, 5


def centre(name):
    index = PANELS.index(name)
    return COL_X[index % 4], ROW_Z[index // 4]


def limits(name):
    """The L's own coordinates: the stem's x span, the corner, and how far the arm reaches."""
    cx, cz = centre(name)
    x0, x1 = round(cx - (WIDE + ARM) / 2), round(cx - (WIDE + ARM) / 2) + WIDE
    z0, z1 = round(cz - STEM / 2), round(cz + STEM / 2)
    return x0, x1, z0, z1                       # stem x0..x1, lane z0..z1, corner is x0..x1 by z1-WIDE..z1


def outline(name):
    """The L as one ring: up the stem's west side, round the arm, and back along the south."""
    x0, x1, z0, z1 = limits(name)
    return [[x0, z0], [x1, z0], [x1, z1 - WIDE], [x1 + ARM, z1 - WIDE], [x1 + ARM, z1], [x0, z1]]


def rect(shape_id, x0, x1, z0, z1, base_height, **words):
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": 0,
           "base_height": base_height,
           "min_x": round(x0), "max_x": round(x1), "min_z": round(z0), "max_z": round(z1)}
    out.update(words)
    return out


def ground(name, **words):
    """The whole L at one height, as a polygon."""
    x0, x1, z0, z1 = limits(name)
    out = {"id": f"{name}-ground", "type": "polygon", "operation": "add", "floor": 0,
           "base_height": FOOT, "vertices": outline(name)}
    out.update(words)
    return out


def steps(name, heights, **words):
    """One rectangle a step, following the path: z-bands up the stem, the corner square, x-bands out the
    arm. A step across a bend is a rectangle either way, so the corner takes one of its own."""
    x0, x1, z0, z1 = limits(name)
    stem_end = z1 - WIDE
    drawn, index = [], 0
    stem_run = (stem_end - z0) / STEM_STEPS
    for step in range(STEM_STEPS):
        drawn.append(rect(f"{name}-{index}", x0, x1, z0 + step * stem_run, z0 + (step + 1) * stem_run,
                          heights[index], **words))
        index += 1
    drawn.append(rect(f"{name}-{index}", x0, x1, stem_end, z1, heights[index], **words))
    index += 1
    arm_run = ARM / ARM_STEPS
    for step in range(ARM_STEPS):
        drawn.append(rect(f"{name}-{index}", x1 + step * arm_run, x1 + (step + 1) * arm_run,
                          z1 - WIDE, z1, heights[index], **words))
        index += 1
    return drawn


def lane(name):
    """One panel's shapes and its relief marks."""
    x0, x1, z0, z1 = limits(name)
    shapes, marks, pushes = [], [], []

    if name == "piece-steps":
        # Five heights for eight blocks: the coarse plan, where every seam is a step of 2.
        heights = [FOOT, FOOT, FOOT + 2, FOOT + 4, FOOT + 4, FOOT + 6, FOOT + 6, HEAD, HEAD]
        shapes = steps(name, heights)

    elif name == "piece-treads":
        # Nine heights for eight blocks: one course a seam, the whole way round the bend.
        shapes = steps(name, list(range(FOOT, HEAD + 1)))

    elif name == "tilted":
        # One polygon and six anchors, one per vertex of the L. A tilt is a plane and a plane has one
        # gradient, so what the corner does with two directions of climb is the panel's question.
        corners = outline(name)
        shapes = [{"id": name, "type": "polygon", "operation": "add", "floor": 0, "base_height": FOOT,
                   "vertices": corners,
                   "anchor_heights": [FOOT, FOOT, HEAD - 3, HEAD, HEAD, FOOT + 3]}]

    elif name == "plates":
        # The lane left at its foot with nine override plates stepping over it, which is the same staircase
        # drawn at the layout tier — and an override add replaces the column it lands on.
        shapes = [ground(name)] + steps(name, list(range(FOOT, HEAD + 1)), override=True)

    elif name == "marks":
        # The relief grades it: the foot pinned at the foot, the arm's end pinned at the head, and
        # everything between — the stem, the corner and most of the arm — left to the relaxation.
        shapes = [ground(name)]
        marks = [{"id": f"{name}-foot", "kind": "area", "h": FOOT - 1, "bevel": 0,
                  "ring": [[x0, z0], [x1, z0], [x1, z0 + 8], [x0, z0 + 8]]},
                 {"id": f"{name}-head", "kind": "area", "h": HEAD - 1, "bevel": 0,
                  "ring": [[x1 + ARM - 8, z1 - WIDE], [x1 + ARM, z1 - WIDE],
                           [x1 + ARM, z1], [x1 + ARM - 8, z1]]}]

    elif name == "push":
        # A landform at the arm's end, graded back over its falloff. A push's skirt is radial, so what it
        # does to a bend is not what it does to a bar.
        shapes = [ground(name)]
        pushes = [{"id": f"{name}-rise", "amount": HEAD - FOOT, "falloff": 22, "crown": 0,
                   "roughness": 0, "seed": 1,
                   "ring": [[x1 + ARM - 14, z1 - WIDE], [x1 + ARM + 2, z1 - WIDE],
                            [x1 + ARM + 2, z1], [x1 + ARM - 14, z1]]}]

    elif name == "deck":
        # The tier that leaves the lane alone: the L stays at its foot and a storey crosses its corner.
        shapes = [ground(name)]

    return shapes, marks, pushes


shapes, groups, relief = [], [], {}
for name in PANELS:
    panel_shapes, panel_marks, panel_pushes = lane(name)
    shapes += panel_shapes
    groups.append({"id": name, "name": name, "mirrors": False,
                   "shapeIds": [shape["id"] for shape in panel_shapes]})
    if panel_marks or panel_pushes:
        relief[name] = {"base": FOOT - 1, "reach": 0, "step": 1,
                        "marks": panel_marks, "pushes": panel_pushes}

# The deck: a storey at the head's height over the corner and the first of the arm, on four legs. A layer is
# one span a column, so the legs stop at the deck rather than passing through it.
dx0, dx1, dz0, dz1 = limits("deck")
DECK = (dx0, dx1 + 16, dz1 - WIDE, dz1)                 # over the corner and 16 blocks of the arm
STONE = {"kind": "cell", "cellSize": 4, "rise": 2, "palette": [SOLID(98), SOLID(98, 1), SOLID(1, 6)]}
legs = [(DECK[0], DECK[0] + 2, DECK[2], DECK[2] + 2), (DECK[1] - 2, DECK[1], DECK[2], DECK[2] + 2),
        (DECK[0], DECK[0] + 2, DECK[3] - 2, DECK[3]), (DECK[1] - 2, DECK[1], DECK[3] - 2, DECK[3])]
deck_layers = []
for tier, (rects, floor, thickness) in enumerate(((legs, FOOT - 1, HEAD - FOOT), ([DECK], HEAD - 1, 1))):
    drawn = [{"id": f"deck-tier{tier}-{index}", "type": "rectangle", "operation": "add",
              "floor": round(floor), "base_height": round(thickness), "material": STONE,
              "min_x": round(a), "max_x": round(b), "min_z": round(c), "max_z": round(d)}
             for index, (a, b, c, d) in enumerate(rects)]
    deck_layers.append({"id": f"deck-tier{tier}", "name": f"deck tier {tier}", "base_y": 0, "kind": "made",
                        "part_of": "deck-over", "layout": {"shapes": drawn, "groups": [
                            {"id": f"deck-tier{tier}", "name": "the deck over the corner", "mirrors": False,
                             "shapeIds": [shape["id"] for shape in drawn]}]}})

layout = {
    "setup": {"bbox": {"min_x": min(COL_X) - WIDE - ARM, "max_x": max(COL_X) + WIDE + ARM,
                       "min_z": min(ROW_Z) - STEM, "max_z": max(ROW_Z) + STEM},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR},
    "mapTheme": "moor",
    "relief": relief,
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}] + deck_layers,
}


def path(name):
    """The line every read is taken along: up the stem, round the corner, out to the arm's end."""
    x0, x1, z0, z1 = limits(name)
    middle_x, middle_z = round((x0 + x1) / 2), round(z1 - WIDE / 2)
    return [(middle_x, z0), (middle_x, middle_z), (x1 + ARM - 1, middle_z)]


if __name__ == "__main__":
    json.dump(layout, open(os.path.join(HERE, "raising-a-lane.layout.json"), "w"), indent=1)
    print(f"{len(PANELS)} panels, {len(shapes)} ground shapes, {len(deck_layers)} made layer(s)")
    for name in PANELS:
        x0, x1, z0, z1 = limits(name)
        print(f"  {name:14s} stem x{x0:5d}..{x1:<5d} z{z0:5d}..{z1:<5d} arm to x{x1 + ARM:5d}")
