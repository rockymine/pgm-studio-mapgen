"""Routes over ground: where a road or a path goes, and laying it.

    way = find(H, X, Z, (-86, 30), (60, -55), max_grade=1 / 7, water=river.mask)    # cells, start first
    pts = smooth(simplify(way))                                                    # a polyline to grade along
    H, level, spans = landform.grade(H, X, Z, pts, width=4, max_grade=1 / 7, water=river.mask)
    ...lay the terrain...
    pave(w, H, X, Z, pts, width=4, water=river.mask)       # the surface, and a bridge over each span
    steps(w, H, X, Z, pts)                                 # a footpath's stairs where it climbs a block at once

    roads = network(H, X, Z, {"harbour": (...), "village": (...), "pass": (...)}, max_grade=1 / 7)

**A route is found, not drawn.** `find` is a least-cost search over nodes a few blocks apart, up to 48 headings out
of each, so a line can run at a shallow angle across a steep slope.
A step costs its length, more for the grade it climbs, steeply more past `max_grade`, and more for a turn, so a
route that cannot go straight up a slope runs across it in long legs and turns about in hairpins: the switchbacks
come out of the cost, not out of a drawing. Water costs `bridge` a block (or is refused with bridge=None) and an
`avoid` mask is refused.

**A network reuses its roads.** `network` joins places one at a time, nearest first, each to the nearest cell of
the roads already laid, where a step costs `reuse` of its length, so a village gets one road with branches rather
than a road to each place.

The studio's routes are strokes an author drags over finished ground. These are found over the ground and graded
into it, the two halves a stroke cannot do.
"""
import heapq
import math

import numpy as np

from .blocks import B
from .orient import stair as stair_data
from .shapes import polyline

def _moves(reach):
    """Every heading out of a node to another `reach` nodes away at most, each once (no multiples)."""
    return [(dx, dz) for dx in range(-reach, reach + 1) for dz in range(-reach, reach + 1)
            if (dx, dz) != (0, 0) and math.gcd(abs(dx), abs(dz)) == 1]


def _index(X, Z, p):
    return int(round(p[0] - X[0, 0])), int(round(p[1] - Z[0, 0]))


def find(H, X, Z, start, goal, max_grade=0.15, cell=3, reach=4, turn=6.0, climb=2.0, steep=40.0, water=None,
         bridge=6.0, avoid=None, prefer=None, reuse=0.35, goals=None):
    """The cheapest route from start to goal (world (x, z)), or to the nearest cell of `goals` (a mask): a list of
    world points, start first, through nodes `cell` blocks apart. Returns None when nothing reaches.

    Out of each node a route may head to any node up to `reach` away (48 headings at a reach of 4, enough to cross
    a 1 in 2 slope at 1 in 8). A step costs its length, more for the grade it climbs and for the ground it rises
    and falls over on the way, steeply more for a grade past `max_grade`, and `turn` for a turn about, less for a
    smaller one: so a route that cannot climb straight runs long legs joined by hairpins rather than zig-zagging.
    Water costs `bridge` a block, or is refused with bridge=None; `avoid` is refused; ground in `prefer` (roads
    already laid) costs `reuse` of what it would."""
    sx, sz = H.shape
    xs, zs = np.arange(0, sx, cell), np.arange(0, sz, cell)
    nx, nz = len(xs), len(zs)
    moves = _moves(reach)
    heading = [math.atan2(dz, dx) for dx, dz in moves]

    def node(p):
        i, k = _index(X, Z, p)
        return int(np.clip(round(i / cell), 0, nx - 1)), int(np.clip(round(k / cell), 0, nz - 1))

    def at(n):
        return min(xs[n[0]], sx - 1), min(zs[n[1]], sz - 1)

    cache = {}

    def edge(n, m):
        key = (n, m)
        if key in cache:
            return cache[key]
        dx, dz = moves[m]
        o = (n[0] + dx, n[1] + dz)
        if not (0 <= o[0] < nx and 0 <= o[1] < nz):
            cache[key] = None
            return None
        (ai, ak), (bi, bk) = at(n), at(o)
        L = math.hypot(bi - ai, bk - ak)
        k = max(2, int(L) + 1)
        ii = np.round(np.linspace(ai, bi, k)).astype(int)
        kk = np.round(np.linspace(ak, bk, k)).astype(int)
        if avoid is not None and avoid[ii, kk].any():
            cache[key] = None
            return None
        h = H[ii, kk].astype(float)
        wet = water[ii, kk] if water is not None else np.zeros(k, bool)
        if wet.any() and bridge is None:
            cache[key] = None
            return None
        dry = ~wet
        c = L * (1 + (bridge - 1) * wet.mean()) if wet.any() else L
        if dry.sum() >= 2:
            hd = h[dry]
            g = abs(hd[-1] - hd[0]) / L
            rough = float(np.abs(np.diff(hd)).sum()) - abs(hd[-1] - hd[0])
            c += L * climb * g + climb * rough
            if g > max_grade:
                c += L * steep * (g - max_grade) / max_grade
        if prefer is not None and prefer[ii, kk].mean() > 0.5:
            c *= reuse
        cache[key] = (o, c)
        return cache[key]

    s = node(start)
    if goals is None:
        gnode = node(goal)
        is_goal = lambda n: n == gnode                                    # noqa: E731
        hfun = lambda n: math.hypot(*np.subtract(at(n), at(gnode))) * (reuse if prefer is not None else 1.0)  # noqa: E731
    else:
        gn = {(int(round(i / cell)), int(round(k / cell))) for i, k in np.argwhere(goals)}
        gn = {(min(i, nx - 1), min(k, nz - 1)) for i, k in gn}
        is_goal = lambda n: n in gn                                       # noqa: E731
        hfun = lambda n: 0.0                                              # noqa: E731
    D = {(s, -1): 0.0}
    prev = {}
    heap = [(hfun(s), 0.0, s, -1)]
    end = None
    while heap:
        _, d, n, came = heapq.heappop(heap)
        if d > D.get((n, came), math.inf):
            continue
        if is_goal(n):
            end = (n, came)
            break
        for m in range(len(moves)):
            e = edge(n, m)
            if e is None:
                continue
            o, c = e
            if came >= 0:
                a = abs((heading[m] - heading[came] + math.pi) % (2 * math.pi) - math.pi)
                c += turn * (a / math.pi) ** 2
            nd = d + c
            if nd < D.get((o, m), math.inf):
                D[(o, m)] = nd
                prev[(o, m)] = (n, came)
                heapq.heappush(heap, (nd + hfun(o), nd, o, m))
    if end is None:
        return None
    path = [end]
    while path[-1] in prev:
        path.append(prev[path[-1]])
    path.reverse()
    x0, z0 = int(X[0, 0]), int(Z[0, 0])
    pts = [(x0 + at(n)[0], z0 + at(n)[1]) for n, _ in path]
    pts[0] = tuple(start)
    if goal is not None and goals is None:
        pts[-1] = tuple(goal)
    return pts


def simplify(pts, tolerance=1.5):
    """Fewer points on the same line (Ramer-Douglas-Peucker): a route's cells to the bends that matter."""
    pts = [tuple(map(float, p)) for p in pts]
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0]), np.array(pts[-1])
    ab = b - a
    n = np.hypot(*ab) or 1e-9
    d = [abs(ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])) / n for p in pts[1:-1]]
    j = int(np.argmax(d)) + 1
    if d[j - 1] <= tolerance:
        return [pts[0], pts[-1]]
    return simplify(pts[:j + 1], tolerance)[:-1] + simplify(pts[j:], tolerance)


def smooth(pts, rounds=2):
    """Corners cut (Chaikin), so a switchback turns in an arc rather than a point; the ends stay where they were."""
    pts = [tuple(map(float, p)) for p in pts]
    for _ in range(rounds):
        if len(pts) < 3:
            break
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            out += [(0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]),
                    (0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1])]
        out.append(pts[-1])
        pts = out
    return pts


def network(H, X, Z, places, order=None, width=4, **kw):
    """Join named places, (x, z) each, with roads: the first is the root, then each place in `order` (default:
    nearest to the network first) is joined to the nearest cell of the roads already found. Returns
    {name: cells} for each new branch and the mask of every road cell."""
    names = list(places)
    root = names[0]
    roads = np.zeros(H.shape, bool)
    i, k = _index(X, Z, places[root])
    roads[i, k] = True
    branches = {}
    todo = list(order or names[1:])
    while todo:
        if order is None:
            have = np.argwhere(roads)
            todo.sort(key=lambda n: np.min(np.hypot(have[:, 0] - _index(X, Z, places[n])[0],
                                                    have[:, 1] - _index(X, Z, places[n])[1])))
        name = todo.pop(0)
        cells = find(H, X, Z, places[name], None, goals=roads, prefer=roads, **kw)
        if cells is None:
            branches[name] = None
            continue
        branches[name] = cells
        d, _ = polyline(X, Z, cells if len(cells) > 1 else cells * 2)
        roads |= d <= max(0.5, width / 2 - 0.5)
    return branches, roads


def footprint(X, Z, pts, width):
    """The columns a route of this width covers: what a later route's grading keeps off."""
    d, _ = polyline(X, Z, pts)
    return d <= width / 2


def grades(H, X, Z, cells):
    """The grade of every leg of a route over the ground as it stands, end to end: rise over run, unsigned."""
    out = [0.0]
    for p, q in zip(cells, cells[1:]):
        a, b = _index(X, Z, p), _index(X, Z, q)
        out.append(abs(float(H[b]) - float(H[a])) / math.hypot(q[0] - p[0], q[1] - p[1]))
    return out


# ---- laying a route into the world -----------------------------------------------------------------------
def pave(w, H, X, Z, pts, width=4, surface=((B.GRAVEL, 0), (B.DIRT, 1), (B.COBBLE, 0)), weights=(0.6, 0.3, 0.1),
         water=None, deck=(B.PLANKS, 1), rail=(B.FENCE, 0), clear=3, seed=0, level=None):
    """Lay a route's surface: every column within width / 2 of the line takes a block from `surface` (by
    `weights`) with `clear` blocks of air over it; over water the route is a bridge, a deck of `deck` at
    level(s) (the graded level, or the banks' height) with a rail each side. Returns the bridge cells."""
    rng = np.random.default_rng(seed)
    d, s = polyline(X, Z, pts)
    on = d <= width / 2
    edge = on & (d > width / 2 - 1)
    p = np.array(weights, float) / sum(weights)
    bridge = []
    for i, k in np.argwhere(on):
        x, z, y = int(X[i, k]), int(Z[i, k]), int(H[i, k])
        if water is not None and water[i, k]:
            yd = int(round(level(s[i, k]))) if level else y + 2
            w.set(x, yd, z, *deck)
            if edge[i, k] and rail:
                w.set(x, yd + 1, z, *rail)
            bridge.append((x, yd, z))
            continue
        w.set(x, y, z, *surface[int(rng.choice(len(surface), p=p))])
        for yy in range(y + 1, y + 1 + clear):
            if w.id(x, yy, z) not in (B.WATER, B.WATER_FLOW):
                w.set(x, yy, z, B.AIR)
    return bridge


def steps(w, H, X, Z, pts, block=B.COBBLE_STAIRS, width=1):
    """A footpath's steps: walking the line cell by cell, wherever the ground rises a block at once, a stair
    climbing that way, as wide as the path. Returns how many were laid."""
    from .shapes import walk_cells
    cells = walk_cells([(int(round(x)), int(round(z))) for x, z in pts])
    n = 0
    for (ax, az), (bx, bz) in zip(cells, cells[1:]):
        a, b = _index(X, Z, (ax, az)), _index(X, Z, (bx, bz))
        if not (0 <= b[0] < H.shape[0] and 0 <= b[1] < H.shape[1]):
            continue
        dh = int(H[b]) - int(H[a])
        dx, dz = bx - ax, bz - az
        if abs(dh) != 1 or abs(dx) + abs(dz) != 1:
            continue
        up, at = ((dx, dz), (bx, bz, int(H[b]))) if dh > 0 else ((-dx, -dz), (ax, az, int(H[a])))
        for j in range(-(width // 2), width - width // 2):
            x, z = at[0] + j * abs(dz), at[1] + j * abs(dx)                 # widened across the climb
            w.set(x, at[2], z, block, stair_data(up))
            n += 1
    return n
