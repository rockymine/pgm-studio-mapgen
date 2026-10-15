"""Walk Riad's plan before anything is built.

Two storeys: the ground raster and, over it, the arcade roofs and the spawn decks. The moves:

  - a step to a neighbour at most one block higher (a jump, or a stair); a drop of any height, one way,
    into water at no cost and onto ground at the price the fall costs;
  - water swum at half speed, and left onto ground one block over its surface;
  - a ladder climbed from its foot to its top, and the Cistern's water columns swum up from under their cages;
  - a jump across a gap of one to three blocks to a surface at most one block higher. The checker finds every
    such jump the plan allows, so a jump nobody planned shows up in its list;
  - from a roof, a drop off its edge; from a spawn deck, a drop through the hole into the pool.

It prints the jumps, a check that every stair is met head-on, every walk from a spawn to each post and between
the posts, the ground the carrier is allowed, and what can be seen from each post.

    python3 plan_check.py
"""
import heapq
import math
from collections import deque

import numpy as np

import plan as P

R = P.build()
H, K, U, UK = R.H, R.K, R.U, R.UK
KN = {v: k for k, v in P.KINDS.items()}
WALKK = {P.KINDS[k] for k in P.WALK}
WATER = P.KINDS["water"]


def inside(i, j):
    return 0 <= i < P.NX and 0 <= j < P.NZ


def kind(i, j):
    return KN[K[i, j]]


def stands(i, j):
    """A ground cell a player can be in: a floor of any walkable kind, water, a ladder or a water column."""
    return inside(i, j) and (K[i, j] in WALKK or K[i, j] in (WATER, P.KINDS["ladder"], P.KINDS["swim"]))


def c(x, z):
    return (P.ix(x), P.iz(z), 0)


def fall_cost(d, into_water):
    if into_water or d <= 3:
        return 1.0
    return 1.0 + (d - 3) * 2.0          # a heart is worth a few blocks of walking


def jump_surfaces():
    """Every surface open to the sky a player can stand on, and its height: ground cells with no roof over them,
    the roofs, and the posts."""
    S = {}
    for i in range(P.NX):
        for j in range(P.NZ):
            if K[i, j] in WALKK and U[i, j] < 0:
                S[(i, j, 0)] = H[i, j]
            if UK[i, j] == P.UKINDS["roof"]:
                S[(i, j, 1)] = U[i, j]
    return S


def top_at(i, j):
    """The highest thing in a column a jump would have to clear: the ground's top, or a roof's."""
    if not inside(i, j):
        return -99
    t = H[i, j] if K[i, j] != P.KINDS["void"] else -99
    if U[i, j] >= 0:
        t = max(t, U[i, j])
    return t


def jumps():
    S = jump_surfaces()
    out = []
    for (i, j, l), h0 in S.items():
        for di in range(-4, 5):
            for dj in range(-4, 5):
                gap = math.hypot(max(0, abs(di) - 1), max(0, abs(dj) - 1))
                if gap < 1 or gap > 3.0:
                    continue
                for l2 in (0, 1):
                    t = (i + di, j + dj, l2)
                    if t not in S or S[t] - h0 > 1:
                        continue
                    lo = min(h0, S[t])
                    n = max(abs(di), abs(dj)) * 3
                    over = set()
                    for s in range(1, n):
                        p = int(round(i + di * s / n)); q = int(round(j + dj * s / n))
                        if (p, q) not in ((i, j), (t[0], t[1])):
                            over.add((p, q))
                    if not over or any(top_at(p, q) >= lo - 1 for p, q in over):
                        continue
                    out.append(((i, j, l), t, round(gap, 1)))
    return out


def graph(use_jumps=True):
    E = {}

    def add(a, b, w, tag="walk"):
        E.setdefault(a, []).append((b, w, tag))
    ladder, swim = P.KINDS["ladder"], P.KINDS["swim"]
    for i in range(P.NX):
        for j in range(P.NZ):
            if not stands(i, j):
                continue
            a = (i, j, 0)
            ka = K[i, j]
            ha = H[i, j]
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = i + di, j + dj
                if not stands(p, q):
                    continue
                kb, hb = K[p, q], H[p, q]
                if kb == swim:
                    continue                                   # entered only from under its cage, below
                if kb == ladder:
                    if ha <= P.G + 1:
                        add(a, (p, q, 0), 1 + (hb - P.G) * 1.8, "ladder")
                    continue
                if ka == ladder:
                    if hb <= ha:
                        add(a, (p, q, 0), 1)                   # off the top of the ladder
                    if hb <= P.G + 1:
                        add(a, (p, q, 0), 1 + (ha - P.G) * 0.5)   # or back down it
                    continue
                if ka == swim:
                    if hb <= ha and kb != WATER:
                        add(a, (p, q, 0), 1)                   # out of the column onto the tower
                    continue
                dh = hb - ha
                w = 2.0 if kb == WATER else (1.0 if dh <= 0 else 1.2)
                if dh <= 1:
                    tag = "walk" if dh >= -3 else f"drop {-dh}"
                    add(a, (p, q, 0), w if dh >= -3 else fall_cost(-dh, kb == WATER), tag)
            # off the tower or a post into the pool: any drop into water
    # the Cistern's water columns: dived into from the pool beside their cages, swum up to the tower's top
    for i in range(P.NX):
        for j in range(P.NZ):
            if K[i, j] != swim:
                continue
            for di in range(-2, 3):
                for dj in range(-2, 3):
                    p, q = i + di, j + dj
                    if inside(p, q) and K[p, q] == WATER and abs(di) + abs(dj) <= 2:
                        add((p, q, 0), (i, j, 0), 3 + (H[i, j] - P.CISTERN["water"]) * 1.5, "swim up")
    # drops from the tower and the porch into the pool: every cell of a post or floor next to water
    for i in range(P.NX):
        for j in range(P.NZ):
            if K[i, j] in WALKK:
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    p, q = i + di, j + dj
                    if inside(p, q) and K[p, q] == WATER and H[p, q] < H[i, j] - 1:
                        add((i, j, 0), (p, q, 0), 1, f"drop {H[i, j] - H[p, q]} into water")
    # the upper storey: walk on a roof, drop off its edge; the deck drops through its hole into the pool
    for i in range(P.NX):
        for j in range(P.NZ):
            if U[i, j] < 0:
                continue
            a = (i, j, 1)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = i + di, j + dj
                if not inside(p, q):
                    continue
                if U[p, q] >= 0 and abs(U[p, q] - U[i, j]) <= 1:
                    add(a, (p, q, 1), 1)
                elif U[p, q] < 0 and stands(p, q) and H[p, q] < U[i, j]:
                    d = U[i, j] - H[p, q]
                    add(a, (p, q, 0), fall_cost(d, K[p, q] == WATER), f"drop {d}" + (" into water" if K[p, q] == WATER else ""))
    J = jumps() if use_jumps else []
    for a, b, g in J:
        add(a, b, g + 1, f"jump {g}")
    return E, J


def dijkstra(E, start):
    D, prev = {start: 0.0}, {}
    h = [(0.0, start)]
    while h:
        d, u = heapq.heappop(h)
        if d > D.get(u, 1e18):
            continue
        for v, w, tag in E.get(u, []):
            if d + w < D.get(v, 1e18):
                D[v] = d + w
                prev[v] = (u, tag)
                heapq.heappush(h, (d + w, v))
    return D, prev


def path_tags(prev, u):
    tags = []
    while u in prev:
        u, tag = prev[u]
        if tag != "walk" and (not tags or tags[-1] != tag):
            tags.append(tag)
    return list(reversed(tags))


def post_cell(post):
    x, y, z = post["at"]
    return c(math.floor(x), math.floor(z))


def spawn_node(team):
    x, y, z, _ = P.SPAWNS[team]
    return (P.ix(math.floor(x)), P.iz(math.floor(z)), 1)


def walk_near(E, a, b, limit=10):
    seen = {a: 0}
    dq = deque([a])
    while dq:
        u = dq.popleft()
        if seen[u] >= limit:
            continue
        for v, w, tag in E.get(u, []):
            if tag.startswith("jump"):
                continue
            if v == b:
                return True
            if v not in seen:
                seen[v] = seen[u] + 1
                dq.append(v)
    return False


def landings():
    """Every flight must be met head-on: two cells before its foot at the level it starts from, and two past its
    top at the level it arrives at, in line with it."""
    bad = []
    for (x, z), r in R.stair.items():
        dx, dz = {"+x": (1, 0), "-x": (-1, 0), "+z": (0, 1), "-z": (0, -1)}[r]
        h = H[P.ix(x), P.iz(z)]
        for sign, want in ((-1, -1), (1, 0)):
            nx, nz = x + sign * dx, z + sign * dz
            if R.stair.get((nx, nz)) == r:
                continue
            for k in (1, 2):
                i, j = P.ix(x + sign * dx * k), P.iz(z + sign * dz * k)
                if not stands(i, j) or H[i, j] != h + want:
                    bad.append((x, z, r, "foot" if sign < 0 else "top"))
                    break
    return bad


def sight(a, b, eye=1.6):
    """Whether a player standing at a sees a player standing at b, over the raster: a column's top or a roof
    in the line's way blocks it."""
    (xa, ya, za), (xb, yb, zb) = a, b
    ya += eye; yb += 1.0
    n = int(max(abs(xb - xa), abs(zb - za)) * 4) + 1
    for s in range(1, n):
        t = s / n
        x, y, z = xa + (xb - xa) * t, ya + (yb - ya) * t, za + (zb - za) * t
        i, j = P.ix(math.floor(x)), P.iz(math.floor(z))
        if not inside(i, j):
            continue
        k = K[i, j]
        if k in (P.KINDS["wall"], P.KINDS["hedge"], P.KINDS["column"], P.KINDS["cage"], P.KINDS["post"]) and H[i, j] + 1 > y:
            if (math.floor(x), math.floor(z)) not in ((math.floor(xa), math.floor(za)), (math.floor(xb), math.floor(zb))):
                return False
        if U[i, j] >= 0 and U[i, j] <= y <= U[i, j] + 1:
            return False
    return True


def main():
    out = []
    E, J = graph()
    # the jumps that are routes: their two ends are not already a few steps apart on foot
    real = [(a, b, g) for a, b, g in J if not walk_near(E, a, b)]
    seen = set()
    out.append("jumps the plan allows (edge gap 1..3 in any direction, no more than 1 up), shortcuts only:")
    for a, b, g in sorted(real, key=lambda t: (t[0][1], t[0][0])):
        ha = U[a[0], a[1]] if a[2] else H[a[0], a[1]]
        hb = U[b[0], b[1]] if b[2] else H[b[0], b[1]]
        key = (ha, hb, round(g))
        tagged = (kind(a[0], a[1]) if not a[2] else "roof", kind(b[0], b[1]) if not b[2] else "roof")
        k2 = (tagged, ha, hb, (a[1] + P.Z_MIN) // 6, (a[0] + P.X_MIN) // 6)
        if k2 in seen:
            continue
        seen.add(k2)
        out.append(f"   {tagged[0]} ({a[0] + P.X_MIN},{a[1] + P.Z_MIN}) y{ha} -> {tagged[1]} ({b[0] + P.X_MIN},{b[1] + P.Z_MIN}) y{hb}, gap {g}")
    L = landings()
    out.append(f"stair ends without two cells of landing in line: {len(L)}")
    for x, z, r, end in L:
        out.append(f"   ({x},{z}) rising {r}: its {end}")
    # from each spawn to each post
    for team in ("red", "blue"):
        D, prev = dijkstra(E, spawn_node(team))
        parts = []
        for post in P.POSTS:
            u = post_cell(post)
            d = D.get(u)
            parts.append(f"{post['key']} {d:.0f} ({', '.join(path_tags(prev, u))})" if d is not None else f"{post['key']} UNREACHABLE")
        out.append(f"{team} spawn: " + "; ".join(parts))
    for post in P.POSTS:
        D, prev = dijkstra(E, post_cell(post))
        parts = []
        for other in P.POSTS:
            if other is post:
                continue
            u = post_cell(other)
            d = D.get(u)
            parts.append(f"{other['key']} {d:.0f} ({', '.join(path_tags(prev, u))})" if d is not None else f"{other['key']} UNREACHABLE")
        out.append(f"from {post['key']}: " + "; ".join(parts))
    # the reach of each spawn, and the carrier's ground
    D, _ = dijkstra(E, spawn_node("blue"))
    ground = [u for u in D if u[2] == 0 and K[u[0], u[1]] in WALKK]
    carrier = [u for u in ground if abs(u[1] + P.Z_MIN) < P.CARRIER_LINE and K[u[0], u[1]] != P.KINDS["spawn"]]
    out.append(f"blue spawn reaches {len(ground)} ground cells; the carrier is allowed {len(carrier)} of them (|z| < {P.CARRIER_LINE})")
    standing = [(x + 0.5, P.G + 1, z + 0.5) for x in range(-36, 37, 3) for z in range(17, 32, 3)]
    # what each post sees: the far spawn's pool and doors, and how much of the carrier's ground
    for post in P.POSTS:
        x, y, z = post["at"]
        eye = (x, y, z)
        pool = [(px + 0.5, P.G + 1, pz + 0.5) for px in (-2, 0, 2) for pz in (47, 49, 51)]
        doors = [(-10.5, P.G + 1, 52.5), (10.5, P.G + 1, 52.5)]
        seen_pool = sum(sight(eye, p) for p in pool)
        seen_doors = sum(sight(eye, p) for p in doors)
        out.append(f"{post['key']} post: sees {seen_pool}/9 of blue's pool, {seen_doors}/2 of its doors, "
                   f"{sum(sight(eye, p) for p in standing)}/{len(standing)} points of blue's gardens")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
