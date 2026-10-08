"""Walk Saltgate's plan stage by stage, before anything is built.

At each stage the gates of the stages already done are open and the rest are shut; the defenders' postern is
open to them alone. The moves: a step at most one up, a drop of any height (more than three costs health), the
siege ladders climbed from the beach to the wall walk, the walk over the gate's passage, the culvert under the
wall. For every stage it reports how far each team's current spawn is from each objective, and for the
attackers the length of each way in, so a stage's balance is read before it is built.

    python3 plan_check.py
"""
import heapq
import math

import numpy as np

import plan as P

R = P.build()
H, K, U = R.H, R.K, R.U
KN = {v: k for k, v in P.KINDS.items()}
WALKK = {P.KINDS[k] for k in P.WALK}
POSTERN = {(x, z) for x in (36, 37, -38, -37) for z in (23, 24, 25)}
ORDER = ["warmup", "A", "B", "C"]


def inside(i, j):
    return 0 <= i < P.NX and 0 <= j < P.NZ


def walkable(i, j, done, team):
    if not inside(i, j):
        return False
    x, z = i + P.X_MIN, j + P.Z_MIN
    if (x, z) in POSTERN and team != "defenders":
        return False
    if K[i, j] == P.KINDS["gate"]:
        return R.gate[(x, z)] in done
    return K[i, j] in WALKK


def node(x, z, layer=0):
    return (P.ix(x), P.iz(z), layer)


def graph(done, team, ladders=True, culvert=True, gate_passage=True):
    E = {}

    def add(a, b, w, tag="walk"):
        E.setdefault(a, []).append((b, w, tag))
    for i in range(P.NX):
        for j in range(P.NZ):
            if not walkable(i, j, done, team):
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            if not gate_passage and -3 <= x <= 2 and -31 <= z <= -29:
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = i + di, j + dj
                if not walkable(p, q, done, team):
                    continue
                if not gate_passage and -3 <= p + P.X_MIN <= 2 and -31 <= q + P.Z_MIN <= -29:
                    continue
                dh = H[p, q] - H[i, j]
                if dh <= 1:
                    w = 1.0 if dh <= 0 else 1.2
                    if dh < -3:
                        w += (-dh - 3) * 2.0
                    add((i, j, 0), (p, q, 0), w, "walk" if dh >= -3 else "drop")
    # the walk over the gate's passage, joined to the wall walk either side
    for i in range(P.NX):
        for j in range(P.NZ):
            if U[i, j] < 0:
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = i + di, j + dj
                if not inside(p, q):
                    continue
                if U[p, q] >= 0:
                    add((i, j, 1), (p, q, 1), 1.0)
                elif K[p, q] == P.KINDS["rampart"] and H[p, q] == U[i, j]:
                    add((i, j, 1), (p, q, 0), 1.0)
                    add((p, q, 0), (i, j, 1), 1.0)
    if ladders:
        for (x, z) in [(x, z) for x in range(P.X_MIN, P.X_MAX + 1) for z in range(P.Z_MIN, P.Z_MAX + 1)
                       if K[P.ix(x), P.iz(z)] == P.KINDS["ladder"]]:
            foot, top = node(x, z - 1), node(x, z + 1)               # from the beach to the wall walk
            add(foot, top, 1 + (H[P.ix(x), P.iz(z)] - H[foot[0], foot[1]]) * 1.8, "ladder")
            add(top, foot, 4, "ladder down")
    if culvert:
        c = P.CULVERT
        L = sum(math.dist(a[:2], b[:2]) + abs(a[2] - b[2]) * 0.4 for a, b in zip(c["pts"], c["pts"][1:]))
        add(node(*c["a"]), node(*c["b"]), L, "culvert")
        add(node(*c["b"]), node(*c["a"]), L, "culvert")
    return E


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


def to_box(D, box):
    x0, x1, z0, z1 = box
    ds = [D.get(node(x, z), 1e18) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
    m = min(ds)
    return None if m >= 1e17 else m


def to_point(D, x, z, r=2):
    return to_box(D, (x - r, x + r, z - r, z + r))


def spawn(team, stage):
    x, y, z, _ = P.SPAWNS[team][stage]
    return node(int(math.floor(x)), int(math.floor(z)))


def fmt(v):
    return "UNREACHABLE" if v is None else f"{v:.0f}"


def landings():
    bad = []
    for (x, z), r in R.stair.items():
        dx, dz = {"+x": (1, 0), "-x": (-1, 0), "+z": (0, 1), "-z": (0, -1)}[r]
        h = H[P.ix(x), P.iz(z)]
        for sign, want in ((-1, -1), (1, 0)):
            if R.stair.get((x + sign * dx, z + sign * dz)) == r:
                continue
            for k in (1, 2):
                i, j = P.ix(x + sign * dx * k), P.iz(z + sign * dz * k)
                ok = inside(i, j) and (K[i, j] in WALKK or K[i, j] == P.KINDS["gate"]) and H[i, j] == h + want
                if not ok:
                    bad.append((x, z, r, "foot" if sign < 0 else "top"))
                    break
    return bad


def main():
    out = []
    L = landings()
    out.append(f"stair ends without two cells of landing in line: {len(L)}" + (f" {L[:6]}" if L else ""))
    # stage A: the Sea Gate
    done = {"warmup"}
    E = graph(done, "attackers")
    D, _ = dijkstra(E, spawn("attackers", "1"))
    a = to_box(D, P.CONTROL["box"])
    ways = []
    for name, kw in (("the gate", dict(ladders=False, culvert=False)), ("the ladders", dict(culvert=False, gate_passage=False)),
                     ("the culvert", dict(ladders=False, gate_passage=False))):
        Dw, _ = dijkstra(graph(done, "attackers", **kw), spawn("attackers", "1"))
        ways.append(f"{name} {fmt(to_box(Dw, P.CONTROL['box']))}")
    Dd, _ = dijkstra(graph(done, "defenders"), spawn("defenders", "1"))
    out.append(f"A, the Sea Gate: attackers {fmt(a)} from the flagship ({', '.join(ways)}); defenders {fmt(to_box(Dd, P.CONTROL['box']))}")
    out.append(f"   before the warmup ends the attackers reach it: {fmt(to_box(dijkstra(graph(set(), 'attackers'), spawn('attackers', '1'))[0], P.CONTROL['box']))}")
    pre = dijkstra(graph(done, "attackers"), spawn("attackers", "1"))[0]
    out.append("   the magazines before A falls, to the attackers: " +
               ", ".join(f"{m['key']} {fmt(to_point(pre, m['monument'][0], m['monument'][2], 1))}" for m in P.MAGAZINES))
    # stage B: the Powder Stores
    done = {"warmup", "A"}
    Da, _ = dijkstra(graph(done, "attackers"), spawn("attackers", "2"))
    Dd, _ = dijkstra(graph(done, "defenders"), spawn("defenders", "2"))
    out.append("B, the Powder Stores: " + "; ".join(
        f"{m['key']}: attackers {fmt(to_point(Da, m['monument'][0], m['monument'][2], 1))}, defenders {fmt(to_point(Dd, m['monument'][0], m['monument'][2], 1))}"
        for m in P.MAGAZINES))
    wx, wy, wz = P.WOOL["at"]
    out.append(f"   the banner before B falls, to the attackers: {fmt(to_point(Da, wx, wz, 1))}")
    # stage C: the Banner
    done = {"warmup", "A", "B"}
    Ea = graph(done, "attackers")
    Da, _ = dijkstra(Ea, spawn("attackers", "3"))
    Dw, _ = dijkstra(Ea, node(wx, wz))
    mx, my, mz = P.WOOL["monument"]
    Dd, _ = dijkstra(graph(done, "defenders"), spawn("defenders", "3"))
    out.append(f"C, the Banner: attackers {fmt(to_point(Da, wx, wz, 1))} to it; the carry to the Sea Gate {fmt(to_point(Dw, mx, mz, 1))}; "
               f"defenders {fmt(to_point(Dd, wx, wz, 1))} to it, {fmt(to_point(Dd, mx, mz, 1))} to the Sea Gate")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
