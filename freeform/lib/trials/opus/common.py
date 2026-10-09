"""What the five trial boards each needed and the library does not hold, written once here so the boards share it.

Each piece is a library candidate; the boards' reports and SUMMARY.md say which and why. A board's scripts import
this module after `plan.py` has put `freeform/lib` and this folder on the path.

    full(red, op)            a half-board array completed by its image (half turn or a mirror)
    image_box(sym, x0, z0, x1, z1)   a rectangle's image under a Symmetry, as corners again
    gaps(R, axis, ...)       the void a team bridges across a seam, at each row
    via(E, starts, waypoint, targets)  the cheapest walk that passes a waypoint: an approach measured by its way
    set_paint(...)           a ground painted as a set of one tone with inset patches (the look ruling's recipe)
    cell_pick(...)           a built floor or path: even shares of three or four blocks in cells of about three
    kit(doc)                 the kit every board here gives
    table(rows)              the plan check's rows printed with value, measurement, target and a mark
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (LIB, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402

from pgmvox import B  # noqa: E402
from pgmvox import plangraph as G  # noqa: E402
from pgmvox.mapxml import E, item  # noqa: E402
from pgmvox.noise import fbm  # noqa: E402


# ---- symmetry ----------------------------------------------------------------------------------------------
def full(red, op):
    """A red-half array (red is the low half along the turned axis: x < 0 for "half" and "mirror_x", z < 0 for
    "mirror_z") completed by its image about the default axis between blocks -1 and 0."""
    if op == "mirror_x":
        return np.concatenate([red, red[::-1]], axis=0)
    if op == "mirror_z":
        return np.concatenate([red, red[:, ::-1]], axis=1)
    if op == "half":
        return np.concatenate([red, red[::-1, ::-1]], axis=0)
    raise ValueError(op)


def image_box(sym, x0, z0, x1, z1):
    """A rectangle of whole blocks carried through a Symmetry: (x0, z0, x1, z1) sorted."""
    a, b = sym.point(x0, z0), sym.point(x1, z1)
    return min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])


# ---- plan measures -----------------------------------------------------------------------------------------
def gaps(land, xs, zs, axis="x"):
    """The void a team bridges across a seam: for each row (z when the seam runs along z), the run of void
    between the last land before the middle and the first after it. land is a full-board mask [i, k]."""
    out = {}
    if axis == "x":
        mid = land.shape[0] // 2
        for k, z in enumerate(zs):
            left = np.nonzero(land[:mid, k])[0]
            right = np.nonzero(land[mid:, k])[0]
            if len(left) and len(right):
                out[int(z)] = int(mid + right[0] - left[-1] - 1)
    else:
        mid = land.shape[1] // 2
        for i, x in enumerate(xs):
            top = np.nonzero(land[i, :mid])[0]
            bot = np.nonzero(land[i, mid:])[0]
            if len(top) and len(bot):
                out[int(x)] = int(mid + bot[0] - top[-1] - 1)
    return out


def finite(v):
    return v is not None and not math.isinf(v)


def via(E, starts, waypoint, targets):
    """The cheapest walk from the starts to the targets that passes through the waypoint cells: an approach
    measured by the way it comes. Returns (cost, path) or (inf, [])."""
    D, prev = G.dijkstra(E, starts)
    reach = [c for c in waypoint if c in D]
    if not reach:
        return math.inf, []
    w = min(reach, key=D.get)
    D2, prev2 = G.dijkstra(E, [w])
    got = [c for c in targets if c in D2]
    if not got:
        return math.inf, []
    t = min(got, key=D2.get)
    return D[w] + D2[t], G.path(prev, w) + G.path(prev2, t)[1:]


def ring(box_cells, r=1, keep=None):
    """The cells within r of a footprint and not on it: where a player stands to break a goal."""
    cells = set(box_cells)
    out = set()
    for x, z in cells:
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                c = (x + dx, z + dz)
                if c not in cells and (keep is None or keep(*c)):
                    out.add(c)
    return sorted(out)


def table(rows):
    """Print the check: the value, what it measures, the target, and a mark where it misses."""
    w = max(len(r[1]) for r in rows)
    lines = []
    for value, what, target, ok in rows:
        mark = "" if ok is None else ("  ok" if ok else "  MISS")
        lines.append(f"{what:<{w}}  {str(value):<26} {target}{mark}")
    return "\n".join(lines)


# ---- paint -------------------------------------------------------------------------------------------------
def cell_pick(x, z, blocks, size=3, seed=0):
    """A built floor or a path: even shares of the blocks, one block over a cell of about `size` (the look
    ruling's `cell`), not a speckle."""
    cx, cz = math.floor(x / size), math.floor(z / size)
    h = (cx * 73856093) ^ (cz * 19349663) ^ (seed * 83492791)
    jitter = ((x * 31 + z * 17 + seed) % 7 == 0)                 # the odd block off its cell, so cells read worn
    return blocks[(h + (x if jitter else 0)) % len(blocks)]


def set_paint(stops, field, v):
    """A noise stop list: equal bands of the field's value, so the middle stops make the main ground and the
    end stops the patches inside it (`[patch, main, main, patch2]`). field is about -1..1."""
    n = len(stops)
    k = int(np.clip((v + 0.8) / 1.6 * n, 0, n - 1))
    return stops[k]


def grain(shape, seed, cell=3):
    """Ground noise with patches about five blocks across: two octaves at a small cell."""
    return fbm(shape, cell, 2, seed=seed) * 1.4


# ---- map.xml -----------------------------------------------------------------------------------------------
def kit(d, wood=64, extra=()):
    """The kit every board here gives: sword, bow, pickaxe, axe, wood, the team's clay, a golden apple, water,
    food, arrows, leather in team colour with iron chest."""
    return d.kit("spawn-kit",
                 item("iron sword", 0, unbreakable=True), item("bow", 1, enchant=[("infinity", 1)], unbreakable=True),
                 item("iron pickaxe", 2, enchant=[("efficiency", 1)], unbreakable=True),
                 item("iron axe", 3, unbreakable=True), item("wood", 4, wood),
                 item("stained clay", 5, 48, team_color=True), item("golden apple", 6), item("water bucket", 7),
                 item("cooked beef", 8, 16), item("arrow", 28), *extra,
                 item("leather helmet", unbreakable=True, team_color=True, tag="helmet"),
                 item("iron chestplate", unbreakable=True, tag="chestplate"),
                 item("chainmail leggings", unbreakable=True, tag="leggings"),
                 item("leather boots", unbreakable=True, team_color=True, tag="boots"))


def build_only_over(d, region_el, message):
    """Blocks may be placed over the void only inside a region: the not-void filter applied outside it."""
    d.filter("not-void", E("not", E("void")))
    d.region("not-build-area", E("negative", region_el))
    d.apply(block_place="not-void", region="not-build-area", message=message)


# ---- blocks the boards share ---------------------------------------------------------------------------------
STONE_SET = ((B.STONE, 0), (B.STONE, 5), (B.STONE, 0), (B.COBBLE, 0))      # stony ground, cobble a quarter
