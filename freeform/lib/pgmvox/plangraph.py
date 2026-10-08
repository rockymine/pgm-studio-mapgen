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


def jumps(R, walk_kinds, wall_kinds=(), max_gap=3.0):
    """Every jump the raster allows, in any direction: from a walkable cell to another whose nearest edge is one
    to max_gap cells away, landing no more than one higher, over cells that are neither wall nor floor at the
    height a player would walk on. Returns [((x, z), (x, z), gap)]."""
    walk = R.mask(*walk_kinds)
    wall = R.mask(*wall_kinds) if wall_kinds else np.zeros_like(walk)
    H = R.H
    out = []
    r = int(math.ceil(max_gap)) + 1
    for i, j in np.argwhere(walk):
        h0 = H[i, j]
        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):
                gap = math.hypot(max(0, abs(di) - 1), max(0, abs(dj) - 1))
                if gap < 1 or gap > max_gap:
                    continue
                a, b = i + di, j + dj
                if not (0 <= a < R.nx and 0 <= b < R.nz) or not walk[a, b] or H[a, b] - h0 > 1:
                    continue
                if gap > jump_reach(H[a, b] - h0) - 0.6:
                    continue
                n = max(abs(di), abs(dj)) * 3
                over = {(int(round(i + di * s / n)), int(round(j + dj * s / n))) for s in range(1, n)} - {(i, j), (a, b)}
                if not over:
                    continue
                if any(wall[p, q] or (walk[p, q] and H[p, q] >= min(h0, H[a, b]) - 1) for p, q in over):
                    continue
                out.append(((R.x_min + i, R.z_min + j), (R.x_min + a, R.z_min + b), round(gap, 1)))
    return out


def graph(R, walk_kinds, wall_kinds=(), rules=None, extra=()):
    """Edges {(x, z): [((x, z), cost, tag)]} over the raster. extra is [(a, b, cost, tag)]."""
    rules = rules or PlanRules()
    walk = R.mask(*walk_kinds)
    H = R.H
    edges = {}

    def add(a, b, c, tag):
        edges.setdefault(a, []).append((b, c, tag))
    for i, j in np.argwhere(walk):
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if not (0 <= a < R.nx and 0 <= b < R.nz) or not walk[a, b]:
                continue
            dh = int(H[a, b] - H[i, j])
            if dh > 1 or (rules.max_drop is not None and -dh > rules.max_drop):
                continue
            cost = rules.step_up_cost if dh == 1 else 1 + max(0, -dh - 3) * rules.drop_cost
            add((R.x_min + i, R.z_min + j), (R.x_min + a, R.z_min + b), cost, "walk" if dh >= -3 else f"drop {-dh}")
    if rules.jumps:
        for a, b, g in jumps(R, walk_kinds, wall_kinds, rules.max_gap):
            add(a, b, g + 1, f"jump {g}")
    for a, b, c, tag in extra:
        add(a, b, c, tag)
    return edges


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
    (None, []) if none is reached."""
    reached = [c for c in cells if c in D]
    if not reached:
        return None, []
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
    """For every team and every named target (a list of cells), the cheapest cost from the team's spawns:
    {target: {team: cost}}. A fair symmetric board shows the same numbers for both teams."""
    out = {name: {} for name in targets}
    for team, spawns in spawns_by_team.items():
        D, prev = dijkstra(edges, spawns)
        for name, cells in targets.items():
            out[name][team] = route(D, prev, cells)[0]
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
