"""Check Copperline's plan before anything is built: the rails as PGM will read them, and each leg walked.

1. THE TRACK. The rails are laid from the plan's waypoints and each leg is traced from its start the way PGM's
   Track does (`track.py`). The trace must be exactly the leg as planned: the same cells in the same order, no
   shorter (a break) and no longer (running on into the next leg).
2. THE LEGS. For each leg, with the gates of the legs already done open, the walk from each team's spawn to the
   leg's cart and to its end; and for the attackers, the length of each way to the end, forced through a point
   or a connector on that way. Moves: a step at most one up, a drop of any height (more than three costs
   health), a swim along the river, the connectors. A team never walks through the other's spawn room.

    python3 plan_check.py
"""
import heapq
import math

import plan as P
import track as T

R = P.build()
H, K, U = R.H, R.K, R.U
WALKK = {P.KINDS[k] for k in P.WALK}
ORDER = ["warmup", "A", "B", "C"]
SPAWN_ROOMS = {"attackers": ["engine-shed", "station", "depot"], "defenders": ["office", "bunkhouse", "lamp-room"]}


def rails():
    out = {}
    for leg in P.LEGS:
        for x, z, h, d in P.lay(leg):
            assert (x, h + 1, z) not in out
            out[(x, h + 1, z)] = d
    return out


def start(leg):
    x, z, h = leg["pts"][0]
    return (x, h + 1, z)


def check_track():
    out = []
    rs = rails()
    for leg in P.LEGS:
        want = [(x, h + 1, z) for x, z, h, d in P.lay(leg)]
        got = T.trace(rs, start(leg))
        kinds = [rs[p] for p in got]
        n_slope = sum(2 <= d <= 5 for d in kinds)
        n_curve = sum(d >= 6 for d in kinds)
        ok = "as planned" if got == want else f"NOT AS PLANNED: traced {len(got)}, planned {len(want)}, first difference at " \
            f"{next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), min(len(got), len(want)))}"
        e = got[-1]
        out.append(f"leg {leg['key']}, {leg['name']}: {len(got)} rails from {got[0]} to {e}, {n_curve} curves, {n_slope} sloped, "
                   f"climbs {e[1] - got[0][1]}; {ok}")
    for x, y, z in rs:                                            # every rail stands on its cell's ground
        if U[P.ix(x), P.iz(z)] >= 0:
            assert U[P.ix(x), P.iz(z)] == y - 1, (x, y, z)
        else:
            assert H[P.ix(x), P.iz(z)] == y - 1, (x, y, z, H[P.ix(x), P.iz(z)])
    return out


def inside(i, j):
    return 0 <= i < P.NX and 0 <= j < P.NZ


def blocked_rooms(team):
    other = "defenders" if team == "attackers" else "attackers"
    cells = set()
    for name in SPAWN_ROOMS[other]:
        x0, x1, z0, z1 = P.BUILDINGS[name]["box"]
        cells |= {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}
    return cells


def graph(done, team):
    E = {}
    bad = blocked_rooms(team)

    def add(a, b, w):
        E.setdefault(a, []).append((b, w))

    def walkable(i, j):
        if not inside(i, j):
            return False
        x, z = i + P.X_MIN, j + P.Z_MIN
        if (x, z) in bad:
            return False
        if K[i, j] == P.KINDS["gate"]:
            return R.gate[(x, z)] in done
        return K[i, j] in WALKK

    for i in range(P.NX):
        for j in range(P.NZ):
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p, q = i + di, j + dj
                if not inside(p, q):
                    continue
                if walkable(i, j) and walkable(p, q):
                    dh = H[p, q] - H[i, j]
                    if dh <= 1:
                        add((i, j, 0), (p, q, 0), 1.0 + (0.2 if dh > 0 else 0) + max(0, -dh - 3) * 2.0
                            + (0.6 if K[p, q] == P.KINDS["river"] else 0))
                if U[i, j] >= 0:
                    if U[p, q] >= 0:
                        add((i, j, 1), (p, q, 1), 1.0)
                    elif walkable(p, q) and abs(H[p, q] - U[i, j]) <= 1:
                        add((i, j, 1), (p, q, 0), 1.0)
                        add((p, q, 0), (i, j, 1), 1.0)
    for name, way, a, b, L in P.CONNECTORS:
        add(node(*a), node(*b), L)
        add(node(*b), node(*a), L)
    return E


def node(x, z, layer=0):
    return (P.ix(x), P.iz(z), layer)


def dijkstra(E, s):
    D = {s: 0.0}
    h = [(0.0, s)]
    while h:
        d, u = heapq.heappop(h)
        if d > D.get(u, 1e18):
            continue
        for v, w in E.get(u, []):
            if d + w < D.get(v, 1e18):
                D[v] = d + w
                heapq.heappush(h, (d + w, v))
    return D


def near(D, x, z, r=2, layers=(0, 1)):
    ds = [D.get((P.ix(a), P.iz(b), l), 1e18) for a in range(x - r, x + r + 1) for b in range(z - r, z + r + 1)
          for l in layers if inside(P.ix(a), P.iz(b))]
    m = min(ds)
    return None if m >= 1e17 else m


def spawn(team, stage):
    x, y, z, _ = P.SPAWNS[team][stage]
    return node(int(math.floor(x)), int(math.floor(z)))


def fmt(v):
    return "UNREACHABLE" if v is None else f"{v:.0f}"


# the ways forward on each leg: (name, approach, via point (x, z, layer) or a connector's name)
WAYS = {
    "A": [("Main Street", "through", (8, 45, 0)), ("the back alley", "through", (-6, 45, 0)),
          ("the slag heap", "above", (34, 36, 0))],
    "B": [("the trestle", "through", (16, -12, 1)), ("the riverbed", "below", "the north ladder"),
          ("the footbridge", "around", (-25, -12, 1))],
    "C": [("the shelf", "through", (0, -38, 0)), ("the gantry", "above", "the gantry"),
          ("the adit", "below", "the adit"), ("the east ramp", "around", (28, -45, 0))],
}

# the places that look down on each leg's track: (name, (x, z, layer))
VANTAGE = {
    "A": [("the slag heap's top", (34, 36, 0)), ("the station platforms", (-17, 20, 0))],
    "B": [("the north bank over the trestle", (24, -24, 0)), ("the trestle's far end", (16, -19, 1))],
    "C": [("the mine yard over the shelf", (0, -42, 0)), ("the gantry's foot in the yard", (4, -51, 0))],
}


def main():
    out = check_track()
    for n, leg in enumerate(P.LEGS):
        stage = str(n + 1)
        done = set(ORDER[:n + 1])
        cells = P.lay(leg)
        sx, sz, _, _ = cells[0]
        ex, ez, _, _ = cells[-1]
        Ea, Ed = graph(done, "attackers"), graph(done, "defenders")
        Da, Dd = dijkstra(Ea, spawn("attackers", stage)), dijkstra(Ed, spawn("defenders", stage))
        out.append(f"leg {leg['key']}: attackers {fmt(near(Da, sx, sz))} to the cart, {fmt(near(Da, ex, ez))} to the end; "
                   f"defenders {fmt(near(Dd, sx, sz))} to the cart, {fmt(near(Dd, ex, ez))} to the end")
        Dend = dijkstra(Ea, node(ex, ez))
        ways = []
        for name, kind, via in WAYS[leg["key"]]:
            if isinstance(via, str):
                c = next(c for c in P.CONNECTORS if c[0] == via)
                a, b = node(*c[2]), node(*c[3])
                d = min(Da.get(a, 1e18) + c[4] + Dend.get(b, 1e18), Da.get(b, 1e18) + c[4] + Dend.get(a, 1e18))
            else:
                v = node(*via)
                d = Da.get(v, 1e18) + Dend.get(v, 1e18)
            ways.append(f"{name} ({kind}) {fmt(None if d >= 1e17 else d)}")
        out.append("   the ways to the end: " + ", ".join(ways))
        vs = []
        for name, (x, z, l) in VANTAGE[leg["key"]]:
            vs.append(f"{name}: attackers {fmt(near(Da, x, z, 1, (l,)))}, defenders {fmt(near(Dd, x, z, 1, (l,)))}")
        out.append("   the high ground: " + "; ".join(vs))
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main()
