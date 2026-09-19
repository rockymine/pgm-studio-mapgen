"""Writes pushes.layout.json — eight panels, each an island carrying one push or a few, and nothing else.

Row 1 is one push, four outlines: what a ring's shape does to the landform that comes out of it, which is
the card's whole argument. Row 2 is pushes against each other — stacked, overlapped, a negative one cut
into a positive one — and, last, the one arrangement the relief read refuses to like.

The knobs are all four a push has: `amount` is the lift inside the ring, `falloff` the width of the skirt
outside it, `crown` a second lift toward the shape's own middle, and `amounts` one lift per position round
the ring in place of the single one.
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cards import MOOR, grid, lobed_ring, rect_ring, round_ring, turned

PANEL_W, PANEL_D = 96, 76
COL_X, ROW_Z = grid(4, 2, PANEL_W, PANEL_D)

GROUND = 8       # what an unmarked field settles at: the plain every panel's push rises out of
GROUND_TOP = 52  # the island's raw column, before the relief solves it


def panels():
    """Every panel as (name, column, row, [push, ...]), the pushes in the order the solver adds them."""
    for name, col, row, make in [
        ("plateau",  0, 0, plateau), ("dome",    1, 0, dome),
        ("ridge",    2, 0, ridge),   ("amounts", 3, 0, amounts),
        ("stack",    0, 1, stack),   ("overlap", 1, 1, overlap),
        ("crater",   2, 1, crater),  ("disagree", 3, 1, disagree),
    ]:
        cx, cz = COL_X[col] + PANEL_W / 2, ROW_Z[row] + PANEL_D / 2
        yield name, col, row, make(cx, cz)


# --- row 1: one push, four outlines -------------------------------------------------------------------

def plateau(cx, cz):
    """No crown, so the lift is flat from the outline inward: a mesa, and the default a push is."""
    return [{"id": "mesa", "ring": lobed_ring(cx, cz, 19, lobes=5, depth=0.18),
             "amount": 22, "falloff": 14, "crown": 0}]


def dome(cx, cz):
    """A crown on a round ring climbs to the one point furthest from the outline: a hill."""
    return [{"id": "fell", "ring": round_ring(cx, cz, 20),
             "amount": 16, "falloff": 14, "crown": 14}]


def ridge(cx, cz):
    """The same crown on a long thin ring, whose furthest-from-the-outline set is a LINE: a crest."""
    return [{"id": "edge", "ring": turned(rect_ring(cx, cz, 68, 12), cx, cz),
             "amount": 16, "falloff": 12, "crown": 6}]


def amounts(cx, cz):
    """One lift per position round the ring, stated as a function of position ALONG the form: a spur that
    falls from one end to the other.

    Every interior cell takes the amount of its nearest ring point, so a ring of few points cuts the
    landform into that many wedges with a step down the middle of each seam. Two things remove it — enough
    points that neighbouring positions differ by little, and a form long enough that the two sides facing
    each other across the middle state the same lift."""
    points = 40
    lifts = [round(16 + 10 * math.cos(2 * math.pi * k / points), 2) for k in range(points)]
    return [{"id": "spur", "ring": round_ring(cx, cz, 28, points=points, squash=13 / 28),
             "amounts": lifts, "amount": max(lifts), "falloff": 14, "crown": 0}]


# --- row 2: pushes against each other -----------------------------------------------------------------

def stack(cx, cz):
    """Three pushes on one another. The solver adds every push into one lift field, so a smaller ring
    inside a larger one is a terrace on it rather than a replacement for it."""
    return [{"id": "massif", "ring": turned(rect_ring(cx, cz, 54, 38), cx, cz),
             "amount": 10, "falloff": 13, "crown": 0},
            {"id": "bench", "ring": turned(rect_ring(cx, cz, 36, 26), cx, cz),
             "amount": 8, "falloff": 9, "crown": 0},
            {"id": "tor", "ring": turned(rect_ring(cx, cz, 18, 12), cx, cz),
             "amount": 6, "falloff": 5, "crown": 4}]


def overlap(cx, cz):
    """Two rings crossing. Addition is addition wherever the two reach, so the ground between them is
    higher than either states and the crossing is the two together."""
    return [{"id": "west", "ring": round_ring(cx - 10, cz, 16), "amount": 14, "falloff": 12, "crown": 0},
            {"id": "east", "ring": round_ring(cx + 10, cz, 16), "amount": 14, "falloff": 12, "crown": 0}]


def crater(cx, cz):
    """A negative push inside a positive one: the hill is cut after it is raised, because both are one
    sum and the order they are written in changes nothing."""
    return [{"id": "cone", "ring": round_ring(cx, cz, 22), "amount": 20, "falloff": 14, "crown": 0},
            {"id": "caldera", "ring": round_ring(cx, cz, 11), "amount": -14, "falloff": 5, "crown": 0}]


def disagree(cx, cz):
    """A skirt at 3.0 blocks a cell against a crown at 0.4: the two rates meet at the ring's own outline,
    which is where the ground steps. This is the panel `RL6` is about."""
    return [{"id": "stack-of-two", "ring": round_ring(cx, cz, 19),
             "amount": 24, "falloff": 8, "crown": 8}]


shapes, groups, relief = [], [], {}
for name, col, row, pushes in panels():
    x0, z0 = COL_X[col], ROW_Z[row]
    shapes.append({"id": f"island-{name}", "type": "rectangle", "operation": "add",
                   "floor": 0, "base_height": GROUND_TOP, "theme": "moor",
                   "min_x": x0, "min_z": z0, "max_x": x0 + PANEL_W, "max_z": z0 + PANEL_D})
    groups.append({"id": name, "name": name, "mirrors": False, "shapeIds": [f"island-{name}"]})
    relief[name] = {"base": GROUND, "reach": 0, "step": 1, "marks": [],
                    "pushes": [dict(p, roughness=0, seed=1) for p in pushes]}

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

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pushes.layout.json")
json.dump(layout, open(out, "w"), indent=1)
print(f"{len(shapes)} panels, plain at {GROUND} -> {out}")
for name, _, _, pushes in panels():
    for p in pushes:
        lift = max(p.get("amounts") or [p["amount"]], key=abs)
        print(f"  {name:9s} {p['id']:13s} amount {lift:+4} falloff {p['falloff']:3}"
              f"  crown {p['crown']:+3}   skirt {abs(lift) / max(0.5, p['falloff']):.2f}")
