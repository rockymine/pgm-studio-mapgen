"""Read a plan drawn in the studio's planner (plan version 2) as a pgmvox.brittle blueprint of cells.

    plan = studioplan.load("plan.json")                  # GET /api/map/<slug>/plan, saved beside the board
    unit = studioplan.unit(plan, lift=6, under={(-2, -3)})  # {(cx, cz): Cell}, the one team's part as drawn
    cells, team = brittle.fan(unit)                      # all four, by the plan's rot_90
    studioplan.placement(plan, "spawns")                 # [(x, y, z) where it stands, (x0, z0, x1, z1) its footprint]

The planner is read as the author used it, overlaps and all:

    a piece      flat ground at its surface, or the plan's; a later piece lies over an earlier one
    spawn        the keep; wool-room: flat ground the wool's room stands on
    stair...     a piece whose id begins "stair" is a stair cell, climbing from the lower of its two neighbours across
                 it to the higher, one level of three; its own surface is not read
    double...    a piece whose id begins "double" is stacked: a deck at its surface; the cells named in `under` are
                 open beneath it, a lower floor eight down (pgmvox.brittle.DECK)
    a zone       where no piece lies, a build zone: a zone whose id begins "water" is water ground; any other is
                 bare, block 36 under it and cobwebs along its outline where it faces the void

A cell rect [x, z, w, h] covers blocks [x * cell, (x + w) * cell) on each axis about the symmetry's centre, which
is the world's origin, so the plan's cells are pgmvox.brittle's. `lift` raises every height by that many blocks,
for a plan drawn low enough that a cap would reach the floor of the world.
"""
import json

from .brittle import OPP, Cell

STEP = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}


def load(path):
    with open(path) as f:
        return json.load(f)


def _cells(rect):
    x, z, w, h = rect
    return [(a, b) for a in range(x, x + w) for b in range(z, z + h)]


def unit(plan, lift=0, under=()):
    """The one team's part as a blueprint: {(cx, cz): Cell}. `under` names the cells of stacked pieces that are open
    beneath their decks, which the planner does not draw."""
    g = plan["globals"]
    assert g.get("cell", 5) == 5, "pgmvox.brittle's cells are five blocks"
    base = g.get("surface", 9)
    out, stairs = {}, []
    for p in plan["pieces"]:
        y = p.get("surface", base) + lift
        pid = p["id"]
        for c in _cells(p["rect"]):
            if pid.startswith("stair"):
                stairs.append(c)
            elif pid.startswith("double"):
                out[c] = Cell("stacked", y, name=pid, under=c in under)
            elif p.get("role") == "spawn":
                out[c] = Cell("keep", y, name=pid)
            else:
                out[c] = Cell("flat", y, name=pid)
    for z in plan.get("zones", []):
        for c in _cells(z["rect"]):
            if c not in out and c not in stairs:
                out[c] = Cell("water" if z["id"].startswith("water") else "gap", name=z["id"])
    for c in stairs:
        out[c] = _stair(out, c)
    stray = [c for c in under if not (c in out and out[c].kind == "stacked")]
    assert not stray, f"under cells outside every double... piece: {stray}"
    return out


def _stair(cells, c):
    """A stair cell's rise: across it, from a neighbour three lower to the neighbour on the far side; the deck of
    a stacked neighbour is its height."""
    for d, (dx, dz) in STEP.items():
        hi, lo = cells.get((c[0] + dx, c[1] + dz)), cells.get((c[0] - dx, c[1] - dz))
        if hi and lo and hi.y is not None and lo.y is not None and hi.y - lo.y == 3:
            return Cell("stair", lo.y, rises=d, name="stair")
    raise ValueError(f"stair cell {c}: no neighbour three lower across it from one three higher")


def placement(plan, kind, lift=0):
    """The plan's spawns, wools, iron ... of one kind: [((x, y, z) where it stands, (x0, z0, x1, z1) its footprint
    in blocks, its record)], each `at` and footprint counted from its piece's corner, y its piece's surface."""
    g = plan["globals"]
    pieces = {p["id"]: p for p in plan["pieces"]}
    out = []
    for m in plan["placements"].get(kind, []):
        p = pieces[m["piece"]]
        px, pz = p["rect"][0] * g.get("cell", 5), p["rect"][1] * g.get("cell", 5)
        y = p.get("surface", g.get("surface", 9)) + lift
        ax, az = m["at"]
        fp = m.get("footprint")
        box = (px + fp[0], pz + fp[1], px + fp[0] + fp[2] - 1, pz + fp[1] + fp[3] - 1) if fp else None
        out.append(((int(px + ax), y, int(pz + az)), box, m))
    return out


FACING = {"left": "w", "right": "e", "front": "n", "back": "s"}          # the planner: front is -Z, left is -X


def facing(m):
    """A placement's facing as a side, n e s w, where the planner names one."""
    f = m.get("facing")
    return FACING.get(f.split("-")[0], None) if f else None


__all__ = ["load", "unit", "placement", "facing", "OPP"]
