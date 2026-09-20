"""Nine lanes, each climbing the same eight blocks a different way.

A composed lane arrives flat, and giving it height is a choice between **tiers** rather than between
tricks. The plan says what ground is where and at what surface; the layout draws shapes on it; the relief
solves a field under all of them; a layer puts a second storey over the lot. Every tier can raise a lane
and they cost different things, which is what this card measures.

Each panel is the same lane — **12 blocks wide, 48 long**, its foot at surface 9 and its head eight blocks
up at 17 — so the only difference between two panels is the instrument. The reads are taken down the same
centreline on every one of them.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cards import SOLID, MOOR, grid  # noqa: E402

FOOT, HEAD = 9, 17          # the lane's two surfaces: base_height, so the top blocks are y8 and y16
WIDE, LONG = 12, 48         # every lane, every panel
COL_X, ROW_Z = grid(3, 4, panel_w=WIDE, panel_d=LONG, gap=28)
ARM = 36                    # how far the L's arm reaches east of its stem

PANELS = ["piece-steps", "piece-treads", "tilted",
          "plates", "raise-ridge", "raise-sheer",
          "marks", "push", "deck",
          "raise-on-an-l"]


def centre(name):
    index = PANELS.index(name)
    return COL_X[index % 3], ROW_Z[index // 3]


def box(shape_id, cx, cz, width, depth, base_height, floor=0, **words):
    """One rectangle of ground, centred on the panel's own x and a stated z."""
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": floor,
           "base_height": base_height,
           "min_x": round(cx - width / 2), "max_x": round(cx + width / 2),
           "min_z": round(cz - depth / 2), "max_z": round(cz + depth / 2)}
    out.update(words)
    return out


def quad(shape_id, cx, z0, z1, base_height, **words):
    """The same cross-band as a POLYGON. `SK22` refuses anchor heights on a rectangle — a rectangle states
    its bounds rather than the points a height is stated at — so anything that tilts is drawn as its four
    corners, north-west first and clockwise."""
    out = {"id": shape_id, "type": "polygon", "operation": "add", "floor": 0,
           "base_height": base_height,
           "vertices": [[round(cx - WIDE / 2), round(z0)], [round(cx + WIDE / 2), round(z0)],
                        [round(cx + WIDE / 2), round(z1)], [round(cx - WIDE / 2), round(z1)]]}
    out.update(words)
    return out


def band(shape_id, cx, z0, z1, base_height, **words):
    """A cross-band of the lane, from z0 to z1 along it."""
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": 0,
           "base_height": base_height,
           "min_x": round(cx - WIDE / 2), "max_x": round(cx + WIDE / 2),
           "min_z": round(z0), "max_z": round(z1)}
    out.update(words)
    return out


def lane(name):
    """One panel's shapes and its relief marks, as (shapes, marks)."""
    cx, cz = centre(name)
    z0, z1 = cz - LONG / 2, cz + LONG / 2
    shapes, marks = [], []

    if name == "piece-steps":
        # What a plan compiles to when five pieces step by 2. A piece is one height, so the lane is a run
        # of polygons — and `EL1` calls a land seam of 2 un-walkable, which is the tier's own gate saying so.
        for index, height in enumerate(range(FOOT, HEAD + 1, 2)):
            shapes.append(band(f"{name}-{index}", cx, z0 + index * 9.6, z0 + (index + 1) * 9.6, height))

    elif name == "piece-treads":
        # The same tier cut finer: nine pieces for eight blocks, every seam a single course.
        for index, height in enumerate(range(FOOT, HEAD + 1)):
            shapes.append(band(f"{name}-{index}", cx, z0 + index * (LONG / 9),
                               z0 + (index + 1) * (LONG / 9), height))

    elif name == "tilted":
        # One shape, four anchors. The climb is continuous and the plan tier cannot see it at all.
        # An anchor is the shape's own thickness at that vertex, not an offset from `base_height`, so a
        # lane climbing 9 to 17 states 9, 9, 17, 17 and the base height is what an unanchored corner takes.
        shapes.append(quad(name, cx, cz - LONG / 2, cz + LONG / 2, FOOT,
                           anchor_heights=[FOOT, FOOT, HEAD, HEAD]))

    elif name == "plates":
        # Ground at the foot all the way, with eight override plates stepping up it. A plate is a thing
        # standing ON ground rather than ground, which is what the transect under it says.
        shapes.append(box(f"{name}-ground", cx, cz, WIDE, LONG, FOOT))
        for index in range(1, HEAD - FOOT + 1):
            shapes.append(band(f"{name}-{index}", cx, z0 + index * (LONG / 9),
                               z1, FOOT + index, override=True))

    elif name in ("raise-ridge", "raise-sheer"):
        # One erected shelf over the lane's far half. `skirt` is the whole difference: at the lift it is
        # walked onto from any side, at 0 it is a monument with a sheer face.
        # A raise states its lift as `base_height` — the top stands that far over whatever ground the
        # footprint covers — and `skirt` is how far in from the outline it grades back down to it.
        # A skirt is paid out of the shape's own top from every side at once, so on a lane 12 wide the
        # most it can afford is 5 — anything over half the narrow dimension leaves no top at all.
        skirt = 5 if name == "raise-ridge" else 0
        shapes.append(box(f"{name}-ground", cx, cz, WIDE, LONG, FOOT))
        # No `override`: an override add is a privileged SET and wins the column whatever its height, so a
        # shelf written as one replaces the ground under it instead of standing on it. A plain add taller
        # than the ground is what stands on it.
        shapes.append(quad(f"{name}-shelf", cx, cz, z1, HEAD - FOOT,
                           height_mode="raise", skirt=skirt))

    elif name == "marks":
        # Ground at one height, and the relief does the climbing: two area marks with the lane's middle
        # left unpinned, so the relaxation grades between them.
        shapes.append(box(name, cx, cz, WIDE, LONG, FOOT))
        marks = [{"id": f"{name}-foot", "kind": "area", "h": FOOT - 1, "bevel": 0,
                  "ring": [[cx - WIDE / 2, z0], [cx + WIDE / 2, z0],
                           [cx + WIDE / 2, z0 + 10], [cx - WIDE / 2, z0 + 10]]},
                 {"id": f"{name}-head", "kind": "area", "h": HEAD - 1, "bevel": 0,
                  "ring": [[cx - WIDE / 2, z1 - 10], [cx + WIDE / 2, z1 - 10],
                           [cx + WIDE / 2, z1], [cx - WIDE / 2, z1]]}]

    elif name == "push":
        # The other relief answer: a landform lifting the head of the lane, graded back over its falloff.
        shapes.append(box(name, cx, cz, WIDE, LONG, FOOT))
        marks = [{"id": f"{name}-rise", "kind": "push", "amount": HEAD - FOOT, "falloff": 16, "crown": 0,
                  "roughness": 0, "seed": 1,
                  "ring": [[cx - WIDE / 2 - 4, z1 - 14], [cx + WIDE / 2 + 4, z1 - 14],
                           [cx + WIDE / 2 + 4, z1 + 4], [cx - WIDE / 2 - 4, z1 + 4]]}]

    elif name == "raise-on-an-l":
        # The same raise on a lane that turns. A skirt is measured in from the OUTLINE, so at the arm's
        # outside corner it comes in from one edge and at the inside corner from two at once.
        ground = {"id": f"{name}-ground", "type": "polygon", "operation": "add", "floor": 0,
                  "base_height": FOOT,
                  "vertices": [[round(cx - WIDE / 2), round(z0)], [round(cx + WIDE / 2), round(z0)],
                               [round(cx + WIDE / 2), round(z1 - WIDE)],
                               [round(cx + WIDE / 2 + ARM), round(z1 - WIDE)],
                               [round(cx + WIDE / 2 + ARM), round(z1)], [round(cx - WIDE / 2), round(z1)]]}
        shelf = {"id": f"{name}-shelf", "type": "polygon", "operation": "add", "floor": 0,
                 "base_height": HEAD - FOOT, "height_mode": "raise", "skirt": 5,
                 "vertices": [[round(cx - WIDE / 2), round(cz)], [round(cx + WIDE / 2), round(cz)],
                              [round(cx + WIDE / 2), round(z1 - WIDE)],
                              [round(cx + WIDE / 2 + ARM), round(z1 - WIDE)],
                              [round(cx + WIDE / 2 + ARM), round(z1)], [round(cx - WIDE / 2), round(z1)]]}
        shapes += [ground, shelf]

    elif name == "deck":
        # The tier that does not raise the lane: the lane stays at its foot and a storey crosses over it.
        shapes.append(box(name, cx, cz, WIDE, LONG, FOOT))

    return shapes, marks


shapes, groups, marks = [], [], []
for name in PANELS:
    panel_shapes, panel_marks = lane(name)
    shapes += panel_shapes
    marks += panel_marks
    groups.append({"id": name, "name": name, "mirrors": False,
                   "shapeIds": [shape["id"] for shape in panel_shapes]})

# The deck's own layer: a storey at the head's height over the far half of the lane, on four legs, with
# three clear under it. A layer is one span a column, so the legs stop at the deck rather than passing it.
deck_x, deck_z = centre("deck")
deck_z0, deck_z1 = deck_z, deck_z + LONG / 2
DECK_FLOOR = HEAD - 1                                   # the deck's slab, one below the head's top block
legs = [(deck_x - WIDE / 2, deck_x - WIDE / 2 + 2, deck_z0, deck_z0 + 2),
        (deck_x + WIDE / 2 - 2, deck_x + WIDE / 2, deck_z0, deck_z0 + 2),
        (deck_x - WIDE / 2, deck_x - WIDE / 2 + 2, deck_z1 - 2, deck_z1),
        (deck_x + WIDE / 2 - 2, deck_x + WIDE / 2, deck_z1 - 2, deck_z1)]
STONE = {"kind": "cell", "cellSize": 4, "rise": 2, "palette": [SOLID(98), SOLID(98, 1), SOLID(1, 6)]}
deck_layers = []
for tier, (rects, floor, thickness) in enumerate((
        (legs, FOOT - 1, DECK_FLOOR - FOOT + 1),
        ([(deck_x - WIDE / 2, deck_x + WIDE / 2, deck_z0, deck_z1)], DECK_FLOOR, 1))):
    drawn = [{"id": f"deck-tier{tier}-{index}", "type": "rectangle", "operation": "add",
              "floor": round(floor), "base_height": round(thickness), "material": STONE,
              "min_x": round(a), "max_x": round(b), "min_z": round(c), "max_z": round(d)}
             for index, (a, b, c, d) in enumerate(rects)]
    deck_layers.append({"id": f"deck-tier{tier}", "name": f"deck tier {tier}", "base_y": 0, "kind": "made",
                        "part_of": "deck-over", "layout": {"shapes": drawn, "groups": [
                            {"id": f"deck-tier{tier}", "name": "the deck over the lane", "mirrors": False,
                             "shapeIds": [shape["id"] for shape in drawn]}]}})

layout = {
    "setup": {"bbox": {"min_x": min(COL_X) - WIDE, "max_x": max(COL_X) + WIDE,
                       "min_z": min(ROW_Z) - LONG, "max_z": max(ROW_Z) + LONG},
              "center": {"cx": 0, "cz": 0}, "mirror_mode": "none"},
    "themes": {"moor": MOOR},
    "mapTheme": "moor",
    # A relief is keyed by GROUP, so only the two panels that want one carry one: the seven others have no
    # entry at all and come out exactly as they were drawn.
    "relief": {
        "marks": {"base": FOOT - 1, "reach": 0, "step": 1, "pushes": [],
                  "marks": [dict(mark) for mark in marks if mark["id"].startswith("marks-")]},
        "push": {"base": FOOT - 1, "reach": 0, "step": 1, "marks": [],
                 "pushes": [{k: v for k, v in mark.items() if k != "kind"}
                            for mark in marks if mark["id"].startswith("push-")]}},
    "layers": [{"id": "ground", "name": "Ground", "base_y": 0,
                "layout": {"shapes": shapes, "groups": groups}}] + deck_layers,
}

if __name__ == "__main__":
    json.dump(layout, open(os.path.join(HERE, "raising-a-lane.layout.json"), "w"), indent=1)
    print(f"{len(PANELS)} panels, {len(shapes)} ground shapes, {len(deck_layers)} made layer(s)")
    for name in PANELS:
        x, z = centre(name)
        print(f"  {name:16s} centre x{x:5d} z{z:5d}   foot z{round(z - LONG / 2):5d}  head z{round(z + LONG / 2):5d}")
