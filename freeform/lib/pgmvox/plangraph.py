"""Walking the plan: the graph of how a player moves over a raster, shortest routes, arrival times per team, and
every jump the plan allows.

Moves, with their costs in blocks walked:

    walk    to a neighbouring walkable cell at most one higher (1, or 1.2 up a step); down any drop up to
            `max_drop` (a drop of more than three costs fall damage, `drop_cost` a block)
    jump    a running jump over a gap of one to `max_gap` cells to a walkable cell at most one higher, over
            cells that are not walls and not floor at the height a player would walk on (gap + 1)
    extra   anything the board adds: pads (see pad_edges), ladders, tunnels, portals, each an edge with a tag

    G = graph(R, walk_kinds={"floor", "stair", "hill"}, wall_kinds={"wall"})
    D, prev = dijkstra(G, starts)
    cost, tags = route(D, prev, cells)            # the cheapest of a target's cells and the moves to it
    arrivals(G, {"red": [...], "blue": [...]}, targets)

The jump rule is move.jump_reach's, the same rule the built-world walk uses, so the plan and the built world
agree about the same gap.
"""
import heapq
import math
from dataclasses import dataclass

import numpy as np

from .move import fly, jump_reach


@dataclass
class PlanRules:
    max_drop: int | None = None          # None: any drop
    drop_cost: float = 0.0               # extra cost a block for a drop beyond three
    jumps: bool = True
    max_gap: float = 3.0
    step_up_cost: float = 1.2
    diagonals: bool = False              # step corner to corner where both cells it cuts past are walkable


def jumps(R, walk_kinds, wall_kinds=(), max_gap=3.0):
    """Every jump the raster allows, in any direction: from a walkable cell to another whose nearest edge is one
    to max_gap cells away, landing no more than one higher, over cells that are neither wall nor floor at the
    height a player would walk on. Returns [((x, z), (x, z), gap)].

    Worked one offset at a time over the whole raster at once (the jump's reach for each rise is solved once),
    so a board of a few hundred blocks a side takes about a second rather than a minute."""
    walk = R.mask(*walk_kinds)
    wall = R.mask(*wall_kinds) if wall_kinds else np.zeros_like(walk)
    H = R.H
    nx, nz = walk.shape
    reach = {dh: jump_reach(dh) - 0.6 for dh in range(-64, 2)}
    out = []
    r = int(math.ceil(max_gap)) + 1
    for di in range(-r, r + 1):
        for dj in range(-r, r + 1):
            gap = math.hypot(max(0, abs(di) - 1), max(0, abs(dj) - 1))
            if gap < 1 or gap > max_gap:
                continue
            n = max(abs(di), abs(dj)) * 3
            over = sorted({(int(round(di * s / n)), int(round(dj * s / n))) for s in range(1, n)} - {(0, 0), (di, dj)})
            if not over:
                continue
            i0, i1 = max(0, -di), min(nx, nx - di)                 # sources whose landing is on the raster
            j0, j1 = max(0, -dj), min(nz, nz - dj)
            if i0 >= i1 or j0 >= j1:
                continue
            src = walk[i0:i1, j0:j1]
            dst = walk[i0 + di:i1 + di, j0 + dj:j1 + dj]
            h0 = H[i0:i1, j0:j1]
            h1 = H[i0 + di:i1 + di, j0 + dj:j1 + dj]
            dh = h1 - h0
            ok = src & dst & (dh <= 1)
            ok &= gap <= np.vectorize(lambda v: reach.get(int(v), reach[-64]))(np.clip(dh, -64, 1))
            low = np.minimum(h0, h1) - 1
            for oi, oj in over:                                  # nothing in the way: no wall, no floor to walk on
                w_ = wall[i0 + oi:i1 + oi, j0 + oj:j1 + oj]
                f_ = walk[i0 + oi:i1 + oi, j0 + oj:j1 + oj] & (H[i0 + oi:i1 + oi, j0 + oj:j1 + oj] >= low)
                ok &= ~(w_ | f_)
            for a, b in np.argwhere(ok):
                i, k = int(a) + i0, int(b) + j0
                out.append(((R.x_min + i, R.z_min + k), (R.x_min + i + di, R.z_min + k + dj), round(gap, 1)))
    return out


def node(R, x, z, storey=0):
    """A cell's node: (x, z) on the ground storey, (x, z, n) on storey n."""
    x, z = int(x), int(z)
    return (x, z) if storey == 0 else (x, z, int(storey))


def walkable(R, walk_kinds):
    """Per storey, the cells a player can stand on: a walkable kind with two blocks of air over its floor, so
    the ground under a storey that hangs too low is not walked."""
    levels = R.storeys
    out = []
    for s, L in enumerate(levels):
        w = L.mask(*[k for k in walk_kinds if k in L.kinds]) & L.has()
        for t, U in enumerate(levels):
            if t != s:
                w &= ~(U.has() & (U.H > L.H) & (U.H - L.H < 3))
        out.append(w)
    return out


def graph(R, walk_kinds, wall_kinds=(), rules=None, extra=(), bridge=None, bridge_tag="bridge"):
    """Edges {node: [(node, cost, tag)]} over the raster and its storeys. A step to a neighbouring column lands
    on the highest floor there no more than one up, if that floor is walkable; a floor at head height blocks
    it. So a player walks on and off a roof at its own height, drops off its edge, and climbs onto it from a
    floor one below. Jumps are taken on the ground storey only. extra is [(a, b, cost, tag)].

    With rules.diagonals a player also steps corner to corner, so distances are the octile ones a capture
    board's targets are set against rather than four-way. `bridge` is a mask of cells a player crosses by
    building (a capture board's build zones, a wall built over), joined to their eight neighbours at any height
    and tagged `bridge_tag`; `measure` says how much of a route was built."""
    rules = rules or PlanRules()
    levels = R.storeys
    walk = walkable(R, walk_kinds)
    has = [L.has() for L in levels]
    edges = {}

    def add(a, b, c, tag):
        edges.setdefault(a, []).append((b, c, tag))
    for s, L in enumerate(levels):
        for i, j in np.argwhere(walk[s]):
            h = int(L.H[i, j])
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + di, j + dj
                if not (0 <= a < R.nx and 0 <= b < R.nz):
                    continue
                floors = [(int(U.H[a, b]), t) for t, U in enumerate(levels) if has[t][a, b]]
                if any(fh == h + 2 for fh, _ in floors):
                    continue                                     # a floor at head height
                under = [(fh, t) for fh, t in floors if fh <= h + 1]
                if not under:
                    continue
                fh, t = max(under)
                if not walk[t][a, b]:
                    continue
                dh = fh - h
                if rules.max_drop is not None and -dh > rules.max_drop:
                    continue
                cost = rules.step_up_cost if dh == 1 else 1 + max(0, -dh - 3) * rules.drop_cost
                add(node(R, R.x_min + i, R.z_min + j, s), node(R, R.x_min + a, R.z_min + b, t), cost,
                    "walk" if dh >= -3 else f"drop {-dh}")
    ground = walk[0]
    if rules.diagonals:                                          # corner to corner, both cut corners walkable
        for i, j in np.argwhere(ground):
            for di, dj in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                a, b = i + di, j + dj
                if not (0 <= a < R.nx and 0 <= b < R.nz) or not (ground[a, b] and ground[i + di, j]
                                                                  and ground[i, j + dj]):
                    continue
                hs = (R.H[i, j], R.H[a, b], R.H[i + di, j], R.H[i, j + dj])
                if max(hs) - min(hs) > 1:
                    continue
                add(node(R, R.x_min + i, R.z_min + j), node(R, R.x_min + a, R.z_min + b), math.sqrt(2), "walk")
    if bridge is not None:                                       # cells crossed by building, at any height
        for i, j in np.argwhere(bridge):
            p = node(R, R.x_min + i, R.z_min + j)
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    a, b = i + di, j + dj
                    if (di, dj) == (0, 0) or not (0 <= a < R.nx and 0 <= b < R.nz):
                        continue
                    if not (bridge[a, b] or ground[a, b]):
                        continue
                    if di and dj and not ((bridge[i + di, j] or ground[i + di, j]) and
                                          (bridge[i, j + dj] or ground[i, j + dj])):
                        continue
                    q = node(R, R.x_min + a, R.z_min + b)
                    c = math.sqrt(2) if di and dj else 1.0
                    add(q, p, c, bridge_tag)                     # onto the built cell
                    if not bridge[a, b]:
                        add(p, q, c, bridge_tag)                 # and off it onto the floor
    if rules.jumps:
        for a, b, g in jumps(R, walk_kinds, wall_kinds, rules.max_gap):
            add(a, b, g + 1, f"jump {g}")
    for a, b, c, tag in extra:
        add(a, b, c, tag)
    return edges


def measure(D, prev, edges, cells):
    """The cheapest of a set of target cells, and how its cost divides by the kind of move: (cost,
    {tag: amount}, path), or (math.inf, {}, []) if none is reached. "79, 22 of it bridged" is
    measure(...)[1]["bridge"]."""
    got = [c for c in cells if c in D]
    if not got:
        return math.inf, {}, []
    c = min(got, key=D.get)
    p = path(prev, c)
    by = {}
    for u, v in zip(p, p[1:]):
        tag = prev[v][1]
        amount = min(cost for w, cost, t in edges[u] if w == v and t == tag)
        by[tag] = by.get(tag, 0.0) + amount
    return D[c], by, p


def dijkstra(edges, starts):
    """Cheapest cost to every node from any of the starts, and the move that reached it."""
    D, prev = {}, {}
    h = []
    for s in starts:
        D[s] = 0.0
        h.append((0.0, s))
    heapq.heapify(h)
    while h:
        d, u = heapq.heappop(h)
        if d > D.get(u, math.inf):
            continue
        for v, c, tag in edges.get(u, []):
            if d + c < D.get(v, math.inf):
                D[v] = d + c
                prev[v] = (u, tag)
                heapq.heappush(h, (d + c, v))
    return D, prev


def route(D, prev, cells):
    """The cheapest of a set of target cells: (cost, [the moves other than plain walking, in order]), or
    (math.inf, []) if none is reached, as dijkstra's distances read for an unreached cell."""
    reached = [c for c in cells if c in D]
    if not reached:
        return math.inf, []
    c = min(reached, key=lambda c: D[c])
    tags, u = [], c
    while u in prev:
        u, tag = prev[u]
        if tag != "walk" and (not tags or tags[-1] != tag):
            tags.append(tag)
    return D[c], list(reversed(tags))


def path(prev, cell):
    """The cells of the route to `cell`, start first."""
    out = [cell]
    while out[-1] in prev:
        out.append(prev[out[-1]][0])
    return list(reversed(out))


def arrivals(edges, spawns_by_team, targets):
    """For every team and every named target, the cheapest cost from the team's spawns: {target: {team: cost}},
    math.inf where unreached. A target is a list of cells, the same for every team, or a dict {team: cells} when
    each team has its own (its own wool room, the enemy's monument: the image of the other team's). A fair
    symmetric board shows the same numbers for both teams."""
    out = {name: {} for name in targets}
    for team, spawns in spawns_by_team.items():
        D, prev = dijkstra(edges, spawns)
        for name, cells in targets.items():
            out[name][team] = route(D, prev, cells[team] if isinstance(cells, dict) else cells)[0]
    return out


def pad_edges(R, pads, solid_kinds, ticks=200):
    """Edges for launch pads: pads = [(name, [(x, z)...], y, (vx, vy, vz))], y the pad's floor. Each pad cell
    flies with move.fly over the raster and lands on the first column it comes down onto; a column of a solid
    kind higher than the flight is a wall it stops against. Returns (extra edges, landings by name)."""
    solid = R.mask(*solid_kinds)
    edges, landings = [], {}
    for name, cells, y, v in pads:
        cx = sum(c[0] for c in cells) / len(cells) + 0.5
        cz = sum(c[1] for c in cells) / len(cells) + 0.5

        def land(t, x, yy, z, prev_y):
            gx, gz = math.floor(x), math.floor(z)
            if not R.inside(gx, gz):
                return dict(t=t, hit="off the plan")
            floor = R.h(gx, gz) + 1
            i, j = R.ix(gx), R.iz(gz)
            if solid[i, j] and yy < floor:
                return dict(t=t, x=x, z=z, cell=(gx, gz), hit="wall")
            if yy <= floor <= prev_y + 1e-9 and yy < prev_y:
                return dict(t=t, x=x, z=z, y=floor, cell=(gx, gz), hit=R.kind(gx, gz))
            return None
        L, p = fly((cx, y + 1.0, cz), v, land, ticks)
        landings[name] = dict(L or {}, apex=max(q[2] for q in p))
        if L and "cell" in L and L["hit"] != "wall":
            for c in cells:
                edges.append((tuple(c), L["cell"], L["t"] / 5.0, f"pad {name}"))
    return edges, landings
