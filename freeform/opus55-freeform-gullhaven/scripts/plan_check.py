"""Walk Gullhaven's plan before anything is built, and read it the way a free-for-all is played.

The moves: a step to a neighbour at most one block higher; a drop of any height (fall damage is off); the
bridge's deck walked over the Ravine; the caves as edges between their mouths and the grotto, the crypt's
ladder both ways. Water is swum at half speed and left one block up.

What it prints:
  - whether every spawn reaches every other, and how much of the island a player can stand on;
  - for every spawn, the walk to its nearest neighbour and how many other spawns it can see;
  - the open ground: how far each walkable cell is from the nearest thing to stand behind;
  - the longest clear sightline on the island, which on a one-shot map is the one that matters.

    python3 plan_check.py
"""
import heapq
import math

import numpy as np
from scipy import ndimage

import plan as P

R = P.build()
H, K, U = R.H, R.K, R.U
KN = {v: k for k, v in P.KINDS.items()}
WALKK = {P.KINDS[k] for k in P.WALK}
BLOCKS = {P.KINDS[k] for k in ("house", "landmark", "cover", "tree")}


def inside(i, j):
    return 0 <= i < P.NX and 0 <= j < P.NZ


def walkable(i, j):
    return inside(i, j) and K[i, j] in WALKK


def node(x, z):
    return (P.ix(x), P.iz(z))


def graph():
    E = {}

    def add(a, b, w, tag="walk"):
        E.setdefault(a, []).append((b, w, tag))
    for i in range(P.NX):
        for j in range(P.NZ):
            if not walkable(i, j):
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = i + di, j + dj
                if not walkable(p, q):
                    continue
                dh = H[p, q] - H[i, j]
                if dh <= 1:
                    add((i, j), (p, q), 1.0 if dh <= 0 else 1.2, "walk" if dh >= -3 else "drop")
            if U[i, j] >= 0:                                   # the bridge: its own layer over the Ravine
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    p, q = i + di, j + dj
                    if not inside(p, q):
                        continue
                    if U[p, q] >= 0 and abs(U[p, q] - U[i, j]) <= 1:
                        add((i, j, 1), (p, q, 1), 1.0)
                    elif U[p, q] < 0 and walkable(p, q) and abs(H[p, q] - U[i, j]) <= 1:
                        add((i, j, 1), (p, q), 1.0)
                        add((p, q), (i, j, 1), 1.0)
    for t in P.TUNNELS:
        pts = t["pts"]
        L = sum(math.dist(a[:2], b[:2]) + abs(a[2] - b[2]) * (1.5 if t.get("ladder") else 0.4) for a, b in zip(pts, pts[1:]))
        A, B = node(*t["a"]), (-1, -1)
        add(A, B, L, t["key"])
        add(B, A, L, t["key"])
    return E


def dijkstra(E, start):
    D = {start: 0.0}
    h = [(0.0, start)]
    while h:
        d, u = heapq.heappop(h)
        if d > D.get(u, 1e18):
            continue
        for v, w, tag in E.get(u, []):
            if d + w < D.get(v, 1e18):
                D[v] = d + w
                heapq.heappush(h, (d + w, v))
    return D


def spawn_nodes():
    out = [(f"({x},{z})", node(x, z), (x + 0.5, H[P.ix(x), P.iz(z)] + 1, z + 0.5)) for x, z, _ in P.SPAWNS]
    out += [(f"cave ({x},{z})", (-1, -1), (x + 0.5, y + 1, z + 0.5)) for x, z, _, y in P.CAVE_SPAWNS]
    return out


def top(i, j):
    t = H[i, j] if K[i, j] != P.KINDS["sea"] else P.SEA
    return max(t, U[i, j])


def sight(a, b, eye=1.6):
    """Whether a player at a sees a player at b: no column's top in the way of the line between their eyes."""
    (xa, ya, za), (xb, yb, zb) = a, b
    ya += eye; yb += eye
    n = int(max(abs(xb - xa), abs(zb - za)) * 3) + 1
    for s in range(1, n):
        t = s / n
        x, y, z = xa + (xb - xa) * t, ya + (yb - ya) * t, za + (zb - za) * t
        i, j = P.ix(math.floor(x)), P.iz(math.floor(z))
        if inside(i, j) and top(i, j) + 1 > y:
            return False
    return True


def openness():
    """For every walkable cell, the distance to the nearest thing a player can stand behind: a house, a
    landmark, cover, a tree, or ground two or more blocks higher next to it (a cliff, a terrace's wall)."""
    blocker = np.isin(K, list(BLOCKS))
    Hp = np.pad(H, 1, mode="edge")
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb = Hp[1 + di:1 + di + P.NX, 1 + dj:1 + dj + P.NZ]
        blocker |= (nb >= H + 2) & np.isin(K, list(WALKK))
    d = ndimage.distance_transform_edt(~blocker)
    out = np.where(np.isin(K, list(WALKK)), d, -1.0)
    return out


def main():
    out = []
    E = graph()
    S = spawn_nodes()
    D0 = dijkstra(E, S[0][1])
    walk_cells = [u for u in D0 if len(u) == 2 and u != (-1, -1) and walkable(*u)]
    total = int(np.isin(K, list(WALKK)).sum())
    out.append(f"{len(S)} spawns; the first reaches {len(walk_cells)} of the {total} walkable cells, and "
               f"{sum(1 for _, n, _ in S if n in D0)} of the spawns")
    near, seen = [], []
    for name, n, eye in S:
        D = dijkstra(E, n)
        others = [(D.get(m, 1e9), nm) for nm, m, _ in S if m != n]
        d, nm = min(others)
        vis = sum(1 for nm2, m, e2 in S if m != n and math.dist(eye, e2) < 60 and sight(eye, e2))
        near.append(d)
        seen.append(vis)
        out.append(f"   spawn {name:>14} y{int(eye[1]) - 1}: nearest spawn {d:.0f} on foot ({nm}); sees {vis} other spawns within 60")
    out.append(f"nearest-neighbour walk between spawns: min {min(near):.0f}, median {np.median(near):.0f}, max {max(near):.0f}; "
               f"spawns seen from a spawn: median {np.median(seen):.0f}, max {max(seen)}")
    o = openness()
    w = o[o >= 0]
    out.append(f"open ground: {np.mean(w > 6) * 100:.0f}% of walkable cells are more than 6 from anything to stand behind, "
               f"{np.mean(w > 10) * 100:.0f}% more than 10; the farthest is {w.max():.0f}")
    # the longest clear sightline between two standing points on a grid of the island
    pts = [(x + 0.5, H[P.ix(x), P.iz(z)] + 1, z + 0.5) for x in range(P.X_MIN, P.X_MAX + 1, 4)
           for z in range(P.Z_MIN, P.Z_MAX + 1, 4) if walkable(P.ix(x), P.iz(z))]
    best = (0, None, None)
    rng = np.random.default_rng(3)
    for k in rng.choice(len(pts), size=min(220, len(pts)), replace=False):
        a = pts[k]
        for b in pts:
            dd = math.dist(a, b)
            if dd > best[0] and sight(a, b):
                best = (dd, a, b)
    a, b = best[1], best[2]
    out.append(f"longest clear sightline found: {best[0]:.0f} blocks, ({a[0]:.0f},{a[1]:.0f},{a[2]:.0f}) to ({b[0]:.0f},{b[1]:.0f},{b[2]:.0f})")
    print("\n".join(out))
    return out, o


if __name__ == "__main__":
    main()
