"""Walk the plan before anything is built, and tune the jump pads.

The raster's moves: a step to a neighbour that is at most one block higher (a jump, or a stair); a drop of any
height to a lower neighbour, one way (more than three costs health); water entered from anywhere and left only
by a ladder; a jump across a gap of one to three blocks to a floor at most one block higher, which the checker
finds wherever the raster allows it, so a jump nobody planned shows up in its list. Then the plan's special
edges: the tunnel, and each pad's landing, simulated in 1.8's player physics.

    python3 plan_check.py        prints the jumps found, the pads' flights, and the routes to each hill
"""
import heapq
import math

import numpy as np

import plan_v2 as P
from pad import fly

R = P.build()
H, K = R.H, R.K
WALK = {P.KINDS[k] for k in ("floor", "stair", "pad", "hill", "spawn")}
LADDER = P.KINDS["ladder"]
WATER = P.KINDS["water"]


def walkable(i, j):
    return 0 <= i < P.NX and 0 <= j < P.NZ and K[i, j] in WALK


def land_of_pad(pad, v=None):
    """Simulate a pad's flight and say where it comes down: the first column it falls onto whose floor is under
    the player's feet, or the wall it hits."""
    x0, x1, z0, z1, y = pad["cells"]
    px, pz = (x0 + x1 + 1) / 2, (z0 + z1 + 1) / 2
    t, *_ , apex, path = fly((px, y + 1.0, pz), v or pad["v"], None, 120)
    prev_y = y + 1.0
    for t, x, yy, z in path[1:]:
        i, j = P.ix(math.floor(x)), P.iz(math.floor(z))
        if not (0 <= i < P.NX and 0 <= j < P.NZ):
            return None
        floor = H[i, j] + 1
        if K[i, j] == P.KINDS["wall"] and yy < P.WALL_Y + 1:
            return dict(t=t, x=x, z=z, y=yy, apex=apex, hit="wall")
        if yy <= floor and prev_y >= floor - 0.01 or (yy <= floor and K[i, j] == WATER):
            return dict(t=t, x=x, z=z, y=floor, apex=apex, hit=["wall", "floor", "water", "stair", "ladder", "pad", "hill", "spawn"][K[i, j]],
                        cell=(i, j), dist=math.hypot(x - px, z - pz))
        prev_y = yy
    return None


def tune(pad, target, rng=np.random.default_rng(1)):
    """Search velocities for one that lands within a block of the target (x, z) on walkable floor."""
    best = None
    x0, x1, z0, z1, y = pad["cells"]
    for vy in np.arange(0.6, 2.01, 0.05):
        for vh in np.arange(0.4, 3.0, 0.05):
            px, pz = (x0 + x1 + 1) / 2, (z0 + z1 + 1) / 2
            ang = math.atan2(target[1] - pz, target[0] - px)
            v = (round(vh * math.cos(ang), 2), round(vy, 2), round(vh * math.sin(ang), 2))
            L = land_of_pad(pad, v)
            if not L or L["hit"] not in ("floor", "hill", "stair"):
                continue
            err = math.hypot(L["x"] - target[0], L["z"] - target[1])
            score = err + 0.05 * L["apex"]
            if best is None or score < best[0]:
                best = (score, v, L)
    return best


def jumps():
    """Every gap of 1..3 blocks across which a player lands no more than a block higher."""
    out = []
    for i in range(P.NX):
        for j in range(P.NZ):
            if not walkable(i, j):
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                for g in (1, 2, 3):
                    a, b = i + di * (g + 1), j + dj * (g + 1)
                    if not walkable(a, b):
                        continue
                    mid = [(i + di * s, j + dj * s) for s in range(1, g + 1)]
                    if all(K[p, q] == P.KINDS["stair"] for p, q in mid):
                        continue                    # across a stairwell cut into a floor: a hop, not a route
                    if all(not walkable(p, q) or H[p, q] <= min(H[i, j], H[a, b]) - 2 for p, q in mid) and \
                            all(K[p, q] != P.KINDS["wall"] for p, q in mid) and H[a, b] - H[i, j] <= 1 and \
                            not any(walkable(p, q) and H[p, q] >= H[i, j] - 1 for p, q in mid):
                        out.append(((i, j), (a, b), g))
                        break
    return out


def graph(use_tunnel=True, use_pads=True, use_jumps=True, use_drops=True):
    J = jumps() if use_jumps else []
    edges = {}

    def add(a, b, c, tag):
        edges.setdefault(a, []).append((b, c, tag))
    for i in range(P.NX):
        for j in range(P.NZ):
            if K[i, j] == LADDER:                       # climbed out onto the Ledge beside it
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if walkable(i + di, j + dj) and H[i + di, j + dj] == 16:
                        add((i, j), (i + di, j + dj), 6, "ladder")
                continue
            if not (walkable(i, j) or K[i, j] == WATER):
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + di, j + dj
                if not (0 <= a < P.NX and 0 <= b < P.NZ):
                    continue
                if K[i, j] == WATER:
                    if K[a, b] == WATER or K[a, b] == P.KINDS["ladder"]:
                        add((i, j), (a, b), 1.5, "swim")
                    continue
                if K[a, b] == WATER:
                    add((i, j), (a, b), 1, "fall into the pool")
                    continue
                if K[a, b] == LADDER:
                    continue
                if not walkable(a, b):
                    continue
                dh = H[a, b] - H[i, j]
                if dh <= 1 and (dh >= -3 or use_drops):
                    add((i, j), (a, b), 1 if dh <= 0 else 1.2, "walk" if dh >= -3 else f"drop {-dh}")
    for (a, b, g) in J:
        add(a, b, g + 1, f"jump {g}")
    if use_pads:
        for pad in P.PADS:
            L = land_of_pad(pad)
            if L and "cell" in L:
                x0, x1, z0, z1, y = pad["cells"]
                for x in range(x0, x1 + 1):
                    for z in range(z0, z1 + 1):
                        for (px, pz) in ((x, z), P.rot(x, z)):
                            pass
                # the pad and its turned twin
                for twin in (False, True):
                    cells = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
                    li, lj = L["cell"]
                    if twin:
                        cells = [P.rot(x, z) for x, z in cells]
                        lx, lz = P.rot(li + P.X_MIN, lj + P.Z_MIN)
                        li, lj = P.ix(lx), P.iz(lz)
                    for x, z in cells:
                        add((P.ix(x), P.iz(z)), (li, lj), L["t"] / 5.0, f"pad {pad['key']}")
    if use_tunnel:
        for t in P.TUNNELS:
            pts = t["pts"]
            L = sum(math.dist(p[:2], q[:2]) + abs(p[2] - q[2]) * 0.4 for p, q in zip(pts, pts[1:]))
            for twin in (False, True):
                a_, b_ = (t["a"], t["b"]) if not twin else (P.rot(*t["a"]), P.rot(*t["b"]))
                A, B = (P.ix(a_[0]), P.iz(a_[1])), (P.ix(b_[0]), P.iz(b_[1]))
                add(A, B, L, t["key"])
                add(B, A, L, t["key"])
    return edges, J


def dijkstra(edges, start):
    D = {start: 0.0}
    prev = {}
    h = [(0.0, start)]
    while h:
        d, u = heapq.heappop(h)
        if d > D.get(u, 1e18):
            continue
        for v, c, tag in edges.get(u, []):
            if d + c < D.get(v, 1e18):
                D[v] = d + c
                prev[v] = (u, tag)
                heapq.heappush(h, (d + c, v))
    return D, prev


def to_hill(D, prev, hill):
    x0, x1, z0, z1 = hill["box"]
    cells = [(P.ix(x), P.iz(z)) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
    c = min(cells, key=lambda c: D.get(c, 1e18))
    if c not in D:
        return None, []
    tags, u = [], c
    while u in prev:
        u, tag = prev[u]
        if not tags or tags[-1] != tag:
            tags.append(tag)
    return D[c], [t for t in reversed(tags) if t != "walk"]


def main():
    out = []
    # the pads: tune each, then report where it lands
    targets = {"mid-north": (-13.5, -29.5), "ledge-rim": (-40.5, -37.5)}
    for pad in P.PADS:
        L = land_of_pad(pad)
        out.append(f"pad {pad['key']}: velocity {pad['v']} -> lands on the {L['hit']} at ({L['x']:.1f}, {L['z']:.1f}) y {L['y']:.0f}, "
                   f"{L['dist']:.1f} out after {L['t']} ticks, apex {L['apex']:.1f}")
    J = jumps()
    out.append(f"jumps the raster allows (gap 1..3, landing no more than 1 up): {len(J)}")
    seen = set()
    for (a, b, g) in J:
        key = (min(a, b), max(a, b))
        if key in seen:
            continue
        seen.add(key)
        (i, j), (p, q) = a, b
        out.append(f"   ({i + P.X_MIN},{j + P.Z_MIN}) y{H[i, j]} -> ({p + P.X_MIN},{q + P.Z_MIN}) y{H[p, q]}, gap {g}")
    sp = (P.ix(int(math.floor(P.SPAWN_POINT[0]))), P.iz(int(math.floor(P.SPAWN_POINT[2]))))
    for label, kw in (("every route", {}), ("no tunnel", dict(use_tunnel=False)), ("no pads", dict(use_pads=False)),
                      ("no jumps", dict(use_jumps=False)), ("walking only", dict(use_tunnel=False, use_pads=False, use_jumps=False))):
        E, _ = graph(**kw)
        D, prev = dijkstra(E, sp)
        parts = []
        for hill in P.HILLS:
            d, tags = to_hill(D, prev, hill)
            parts.append(f"{hill['key']} {d:.0f}" + (f" ({', '.join(tags)})" if tags else "") if d is not None else f"{hill['key']} unreachable")
        out.append(f"red spawn, {label}: " + "; ".join(parts))
    # from the Middle to each side hill, and between the side hills
    E, _ = graph()
    for a in P.HILLS:
        x0, x1, z0, z1 = a["box"]
        D, prev = dijkstra(E, (P.ix((x0 + x1) // 2), P.iz((z0 + z1) // 2)))
        parts = []
        for b in P.HILLS:
            if b is a:
                continue
            d, tags = to_hill(D, prev, b)
            parts.append(f"{b['key']} {d:.0f}" + (f" ({', '.join(tags)})" if tags else ""))
        out.append(f"from {a['key']}: " + "; ".join(parts))
    # each named route on its own: the walk through its waypoints, each leg the shortest on the full graph
    E, _ = graph()
    def cell(x, z):
        return (P.ix(x), P.iz(z))
    for name, pts, why in ROUTES:
        total, ok = 0.0, True
        for a_, b_ in zip(pts, pts[1:]):
            D, _ = dijkstra(E, cell(*a_))
            d = D.get(cell(*b_))
            if d is None:
                ok = False
                break
            total += d
        out.append(f"route {name}: {total:.0f}" if ok else f"route {name}: BROKEN")
    print("\n".join(out))
    return out


# the named routes, red's, as waypoints the walk must pass through (blue's are the same turned)
ROUTES = [
    ("main lane, spawn to the Middle", [(-50, -1), (-44, -1), (-36, -1), (-29, -1), (-12, -1), (-1, -1)], ""),
    ("Bench round to the North hill, in by the side stair", [(-50, -1), (-44, -1), (-37, -1), (-37, -31), (-9, -31), (-8, -27), (-4, -28)], ""),
    ("Bench round to the South hill, up its front stair", [(-50, -1), (-44, -1), (-37, -1), (-37, 28), (-10, 26), (-1, 20), (-1, 30)], ""),
    ("spawn tunnel to the Ledge, up the North hill's front stair", [(-50, -1), (-29, -21), (-1, -20), (-1, -30)], ""),
    ("Rim to the North hill, dropping on it", [(-50, -1), (-45, -7), (-41, -37), (-1, -35), (-1, -30)], ""),
    ("spawn tunnel, Ledge pad to the Rim, drop on the North hill", [(-50, -1), (-28, -24), (-40, -37), (-1, -35), (-1, -30)], ""),
    ("spawn tunnel, Ledge, parkour onto the Middle", [(-50, -1), (-29, -21), (-1, -20), (-1, -9), (-1, -1)], ""),
    ("Middle to the North hill by the pad and the side stair", [(-1, -1), (-8, -8), (-13, -29), (-9, -31), (-8, -27), (-4, -28)], ""),
    ("Middle to the North hill through the Spring", [(-1, -1), (8, -6), (6, -20), (6, -25), (-1, -21), (-1, -30)], ""),
    ("North hill back to the Middle by the parkour", [(-1, -30), (-1, -20), (-1, -9), (-1, -1)], ""),
    ("North hill back to the Middle through the Spring", [(-1, -30), (-1, -21), (6, -25), (6, -20), (8, -6), (-1, -1)], ""),
]


if __name__ == "__main__":
    main()
