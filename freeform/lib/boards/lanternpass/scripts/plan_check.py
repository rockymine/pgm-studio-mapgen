"""Check Lantern Pass's plan before anything is built: what the shooters see, and what it costs a runner to cross.

1. SIGHT. For every cell of the lane a runner can stand on, the share of the places a shooter can stand that
   see the runner's body or head: the inner edge of either walkway, within forty blocks along it, a ray from the
   shooter's eye that no solid column, no stall, no bamboo stalk and no awning or roof cuts. Water hides all but
   a swimmer's head. A cell seen from one window is nearly hidden; one seen from everywhere is a quay.
2. ROUTES. The lane walked from the boathouse's door to the bell: a step at most one up, any drop, a sprint jump
   over up to three blocks of void or water with at most one up, swimming and wading slower than walking; a
   swimmer climbs out onto a deck a block over the water. Two routes for
   each section: the fastest, and the safest, which pays up to four blocks more for every block, by how much of the walkways see it. And
   the gorge's three crossings, each forced.

Seconds are blocks over 6.7, a sprint with Speed I.

    python3 plan_check.py
"""
import heapq

import numpy as np

import plan as P

R = P.build()
H, K, T, C = R.H, R.K, R.T, R.C
HW = P.walkway_heights(R)
WALKK = {P.KINDS[k] for k in P.WALK}
SPEED = 6.7
RANGE = 40
LX0, LX1 = P.LANE


def walkable(i, j):
    return 0 <= i < P.NX and 0 <= j < P.NZ and K[i, j] in WALKK and P.LANE[0] <= i + P.X_MIN <= P.LANE[1]


def target_heights(i, j):
    if K[i, j] == P.KINDS["water"]:
        return [H[i, j] + 2.6]                                  # a swimmer shows his head
    return [H[i, j] + 1.0, H[i, j] + 1.6]


def sight():
    """vis[i, j]: True where a shooter can see a runner standing on the cell."""
    vis = np.zeros((P.NX, P.NZ))
    eyes = []
    for side, (x0, x1) in P.WALKS.items():
        xe = (x1 if side == "left" else x0) + 0.5               # the inner edge
        for z in range(P.Z_MIN + 2, P.Z_MAX - 1):
            eyes.append((xe, HW[P.iz(z)] + 1.62, z + 0.5))
    eyes = np.array(eyes)
    S = np.linspace(0.02, 0.98, 90)[None, :]
    for i in range(P.NX):
        for j in range(P.NZ):
            if not walkable(i, j):
                continue
            tx, tz = i + P.X_MIN + 0.5, j + P.Z_MIN + 0.5
            near = eyes[np.abs(eyes[:, 2] - tz) <= RANGE]
            seen = np.zeros(len(near), bool)
            for ty in target_heights(i, j):
                ex, ey, ez = near[:, 0:1], near[:, 1:2], near[:, 2:3]
                px, py, pz = ex + (tx - ex) * S, ey + (ty - ey) * S, ez + (tz - ez) * S
                ci = np.floor(px).astype(int) - P.X_MIN
                cj = np.floor(pz).astype(int) - P.Z_MIN
                ok = (ci >= 0) & (ci < P.NX) & (cj >= 0) & (cj < P.NZ)
                ci, cj = np.clip(ci, 0, P.NX - 1), np.clip(cj, 0, P.NZ - 1)
                own = (ci == i) & (cj == j)
                top = T[ci, cj]
                can = C[ci, cj]
                block = ok & ~own & ((py < top + 1) | ((can >= 0) & (py >= can) & (py < can + 1)))
                seen |= ~block.any(axis=1)
            vis[i, j] = seen.mean()
    return vis


def eff(i, j):
    """The height a player is at on a cell: a swimmer is at the water's surface, two over its bed."""
    return H[i, j] + (2 if K[i, j] == P.KINDS["water"] else 0)


def graph():
    E = {}

    def add(a, b, w):
        E.setdefault(a, []).append((b, w))
    for i in range(P.NX):
        for j in range(P.NZ):
            if not walkable(i, j):
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = i + di, j + dj
                if walkable(p, q) and eff(p, q) - eff(i, j) <= 1:
                    k = P.KN[K[p, q]]
                    add((i, j), (p, q), 2.5 if k == "water" else 1.4 if k == "paddy" else 1.0)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):        # a sprint jump over void
                for n in (2, 3, 4):
                    for side in (-1, 0, 1):
                        p, q = i + di * n + dj * side, j + dj * n + di * side
                        if not walkable(p, q) or eff(p, q) - eff(i, j) > 1 or K[p, q] == P.KINDS["water"]:
                            continue
                        mid = [(i + di * m + (dj * side if m > n // 2 else 0), j + dj * m + (di * side if m > n // 2 else 0))
                               for m in range(1, n)]
                        if all(K[a, b] in (P.KINDS["void"], P.KINDS["water"]) for a, b in mid
                               if 0 <= a < P.NX and 0 <= b < P.NZ):
                            add((i, j), (p, q), n + 1.0)
    return E


def dijkstra(E, starts, vis, k_exposed):
    D, prev = {}, {}
    h = []
    for s in starts:
        D[s] = 0.0
        h.append((0.0, s))
    heapq.heapify(h)
    while h:
        d, u = heapq.heappop(h)
        if d > D.get(u, 1e18):
            continue
        for v, w in E.get(u, []):
            nd = d + w * (1 + k_exposed * vis[v])
            if nd < D.get(v, 1e18):
                D[v] = nd
                prev[v] = u
                heapq.heappush(h, (nd, v))
    return D, prev


def path_to(D, prev, goals):
    g = min(goals, key=lambda c: D.get(c, 1e18))
    if g not in D:
        return None
    out = [g]
    while out[-1] in prev:
        out.append(prev[out[-1]])
    return out[::-1]


def cells(x0, x1, z0, z1):
    return [(P.ix(x), P.iz(z)) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) if walkable(P.ix(x), P.iz(z))]


def steps(path):
    """Blocks travelled along a path, a jump counting its length, and blocks in sight, weighted by how much of
    the walkways see each."""
    n, seen = 0.0, 0.0
    for a, b in zip(path, path[1:]):
        L = abs(a[0] - b[0]) + abs(a[1] - b[1])
        n += L
        seen += L * VIS[b]
    return n, seen


def by_section(path):
    out = {}
    for a, b in zip(path, path[1:]):
        z = b[1] + P.Z_MIN
        sec = next(s for s in P.SECTIONS if s[2] <= z <= s[3])[0]
        L = abs(a[0] - b[0]) + abs(a[1] - b[1])
        n, s = out.get(sec, (0.0, 0.0))
        out[sec] = (n + L, s + L * VIS[b])
    return out


VIS = sight()


def main():
    out = []
    E = graph()
    start = cells(P.SPAWN_GATE[0], P.SPAWN_GATE[1], 5, 5)
    bx0, bx1, bz0, bz1 = P.BELL["box"]
    goal = cells(bx0, bx1, bz0, bz1)
    routes = {}
    for name, k in (("fastest", 0.0), ("safest", 4.0)):
        D, prev = dijkstra(E, start, VIS, k)
        routes[name] = path_to(D, prev, goal)
    out.append("section          sight  fastest: blocks, in sight (s)       safest: blocks, in sight (s)")
    fs, ss = by_section(routes["fastest"]), by_section(routes["safest"])
    for key, name, z0, z1 in P.SECTIONS[1:]:
        cs = cells(LX0, LX1, z0, z1)
        open_ = np.mean([VIS[c] for c in cs]) if cs else 0      # the section's mean sight
        f, s = fs.get(key, (0, 0)), ss.get(key, (0, 0))
        out.append(f"{key} {name:<14} {open_:4.0%}   {f[0]:4.0f}, {f[1]:4.0f} ({f[1] / SPEED:4.1f})"
                   f"                {s[0]:4.0f}, {s[1]:4.0f} ({s[1] / SPEED:4.1f})")
    for name in ("fastest", "safest"):
        n, s = steps(routes[name])
        out.append(f"the {name} route, door to bell: {n:.0f} blocks, {n / SPEED:.0f} s; in sight {s:.0f} blocks, {s / SPEED:.0f} s")
    # the gorge's three crossings, each forced through a cell on it
    D0, p0 = dijkstra(E, start, VIS, 0.0)
    Dg, pg = dijkstra(E, goal, VIS, 0.0)
    near = cells(LX0, LX1, 231, 231) + cells(LX0, LX1, 226, 226)
    ways = []
    for name, via in (("the rope bridge", (P.ROPE["x0"], 250)), ("the pillars", (P.PILLARS[4][0], P.PILLARS[4][1])),
                      ("the arch", (P.ARCH["x0"] + 1, 250))):
        v = (P.ix(via[0]), P.iz(via[1]))
        a = path_to(D0, p0, [v])
        b = path_to(Dg, pg, [v])
        seg = [c for c in a + b[::-1][1:] if 226 <= c[1] + P.Z_MIN <= 275]
        n, s = steps(seg)
        ways.append(f"{name} {n:.0f} blocks, {s:.0f} in sight ({s / max(n, 1):.0%})")
    out.append("the gorge, from the bamboo's head to the stair's foot: " + "; ".join(ways))
    reach = dijkstra(E, start, VIS, 0.0)[0]
    out.append(f"the bell reached from the door: {'yes' if any(g in reach for g in goal) else 'NO'}; "
               f"lane cells a runner can stand on that the door does not reach: "
               f"{sum(1 for i in range(P.NX) for j in range(P.NZ) if walkable(i, j) and (i, j) not in reach and P.iz(5) <= j)}")
    print("\n".join(out))
    return out, routes


if __name__ == "__main__":
    main()
