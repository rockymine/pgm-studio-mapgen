"""A goal's approach laid underground: each part of an `approach.Approach` a chamber cut into rock, the chain stepping
down from its host to its room, the voids the form leaves cut as shafts to the void, its defence walls in bedrock.

    a = approach.emit("donut", depth=3, reach=2)
    got = lay(w, a, at=(x, z), top=60, cell=7, drop=6, rng=rng)
    got["room"], got["host"], got["walls"], got["floors"]

**The approach turns on its side by giving every part a floor.** The host's floor is `top`; walking from the host
to the room, each part after the entry stands `drop` blocks lower than the one before, and a part a player walks
along (a run, a bar, a leg) ramps from the floor it is entered at to its own, a block a step. The room is level.
So the form's plan is kept, its ways in are the same ways, and the climb out with a goal is a climb.

**What the form leaves empty is cut to the void.** A donut's hole, the bay of a U, H or scythe and the gap of a
clamp are shafts from the chambers' floors down through the bottom of the world: in plan they are what they were,
voids, and since they are no build zone a player crosses them at no height. The rock round the chambers is the
rest of the map; a board that lets only its kit's blocks be broken (`Build(only=...)`) keeps every way in a door.

**A chamber is cut, not built.** Its floor is level or ramped a block a step with a stair on every step, its
roof six or seven over the floor, and the rock is left standing on every edge it shares with no other part. An
edge that looks onto a shaft is open over a parapet: the void is seen and shot across, and not crossed.
"""
import math

import numpy as np

from pgmvox.core.blocks import B
from pgmvox.core.orient import stair as stair_data
from pgmvox.plan import approach as AP


def _order(a):
    """The parts in walking order from the host: each part's distance from the entry, by the cells it shares."""
    cells = a.cells()
    dist = {c: 0 for c in a.entry}
    todo = list(a.entry)
    while todo:
        nxt = []
        for c in todo:
            for n in AP._neighbours(c, cells):
                if n not in dist:
                    dist[n] = dist[c] + 1
                    nxt.append(n)
        todo = nxt
    return dist


def floors(a, top, drop):
    """Each corridor cell's floor: the host's `top` at the entry, falling `drop` a part along the shortest walk to
    each cell's part, ramped through a walking part from the part before it; the room level at the bottom."""
    dist = _order(a)
    depth_of = {}
    for k, p in enumerate(a.parts):
        cs = p.cells()
        depth_of[k] = min(dist[c] for c in cs)
    rank = {k: r for r, k in enumerate(sorted(depth_of, key=lambda k: (depth_of[k], k)))}
    level = {}
    steps = sorted(set(depth_of.values()))
    for k in depth_of:
        level[k] = top - drop * steps.index(depth_of[k])
    room_k = len(a.parts) - 1                                     # the room is level with the part it is entered from
    level[room_k] = min(v for k, v in level.items() if k != room_k) if len(level) > 1 else level[room_k]
    out = {}
    for k, p in enumerate(a.parts):
        for c in p.cells():
            out[c] = level[k]
    return out, level, rank


def _bays(a):
    """Empty cells the form walls on three sides or more within three cells: the bays and holes its voids are."""
    cells, host = a.cells(), a.host()
    out = set(AP.holes(cells | host))
    i0, i1 = min(c[0] for c in cells), max(c[0] for c in cells)
    j0, j1 = min(c[1] for c in cells), max(c[1] for c in cells)
    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            c = (i, j)
            if c in cells or c in host:
                continue
            walled = sum(1 for d in AP.DIRS if any((c[0] + k * d[0], c[1] + k * d[1]) in cells for k in range(1, 4)))
            if walled >= 3:
                out.add(c)
    return out


def lay(w, a, at, top, cell=7, drop=6, rng=None, height=6, floor_block=(B.STONE, 5), stair=B.COBBLE_STAIRS,
        parapet=(B.COBBLE_WALL, 0), wall_block=(B.BEDROCK, 0), shafts=True, walls=True):
    """Lay approach `a` with corridor cell (0, 0)'s corner at `at` (x, z), its host's floor at `top`, each cell
    `cell` blocks square, each part after the entry `drop` lower. Returns each cell's floor, the shafts cut, the
    walls laid and where everything is, for `centre`."""
    rng = rng or np.random.default_rng(0)
    x0, z0 = at
    cfloor, _, _ = floors(a, top, drop)
    host = a.host()
    cells = a.cells()
    every = dict(cfloor)
    for c in host:
        every[c] = top
    dist = _order(a)
    void = _bays(a) if shafts else set()
    ground = cells | host

    def box(c):
        return x0 + c[0] * cell, z0 + c[1] * cell
    for c, f in every.items():
        bx, bz = box(c)
        near = {(n[0] - c[0], n[1] - c[1]): n for n in AP._neighbours(c, ground)}
        prev = [n for n in near.values() if n in host or dist.get(n, 99) < dist.get(c, 0)]
        src = max(prev, key=lambda n: every[n]) if prev and c not in a.room and c not in host else None
        rise = every[src] - f if src is not None else 0
        d = (src[0] - c[0], src[1] - c[1]) if src is not None else None
        for u in range(cell):
            for v in range(cell):
                x, z = bx + u, bz + v
                side = (-1, 0) if u == 0 else (1, 0) if u == cell - 1 else None
                side_z = (0, -1) if v == 0 else (0, 1) if v == cell - 1 else None
                shut = (side and side not in near) or (side_z and side_z not in near)
                looks = [s for s in (side, side_z) if s and s not in near and (c[0] + s[0], c[1] + s[1]) in void
                         and rise == 0]                            # a ramp's parapet would be a stair onto a wall
                if shut and not looks:
                    continue                                       # the rock between this chamber and the next
                t = 0
                if rise > 0:                                       # how far in from the edge it is entered by
                    t = {(1, 0): cell - 1 - u, (-1, 0): u, (0, 1): cell - 1 - v, (0, -1): v}[d]
                fy = f + max(0, rise - math.ceil(rise * (t + 1) / cell)) if rise > 0 else f
                h = height + (1 if 0 < u < cell - 1 and 0 < v < cell - 1 and rng.random() < 0.4 else 0)
                w.set(x, fy, z, *floor_block)
                for y in range(fy + 1, fy + 1 + h):
                    w.set(x, y, z, B.AIR)
                if looks:                                          # a parapet over a shaft, two high so nobody climbs
                    w.set(x, fy + 1, z, *parapet)                  # it onto a wall: seen across, not crossed
                    w.set(x, fy + 2, z, *parapet)
                elif rise > 0 and t > 0:
                    back = f + max(0, rise - math.ceil(rise * t / cell))
                    if back > fy:                                  # a stair where the ramp steps down
                        w.set(x, fy + 1, z, stair, stair_data((d[0], d[1])))
    out_shafts = sorted(void)
    for c in out_shafts:
        bx, bz = box(c)
        near = [every[n] for n in AP._neighbours(c, ground)]
        lo = (max(near) if near else top) + height
        for u in range(cell):
            for v in range(cell):
                for y in range(0, lo):
                    w.set(bx + u, y, bz + v, B.AIR)
    out_walls = []
    if walls:
        for e in AP.walls(a):
            p, q = sorted(tuple(e))
            fy = max(every[p], every[q])
            bx, bz = box(q)
            along_x = p[1] == q[1]
            for k in range(cell):
                x, z = (bx, bz + k) if along_x else (bx + k, bz)
                y = fy + 1
                while y > 1 and w.id(x, y - 1, z) == B.AIR:          # down to the floor where the ramp has fallen
                    y -= 1
                for yy in range(y, y + 2):
                    if w.id(x, yy, z) in (B.AIR, B.COBBLE_STAIRS):
                        w.set(x, yy, z, *wall_block)
            out_walls.append((p, q))
    return {"room": sorted(a.room), "host": sorted(host), "floors": every, "shafts": out_shafts, "walls": out_walls,
            "cell": cell, "at": at}


def centre(got, c):
    """The middle of corridor cell c at its floor, as feet."""
    x0, z0 = got["at"]
    n = got["cell"]
    return x0 + c[0] * n + n // 2, got["floors"][c] + 1, z0 + c[1] * n + n // 2
