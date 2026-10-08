"""Measure Tamarisk Wash's plan before anything is built: each team's walk to each of red's two monuments and the
ratio of the two, the approaches to each (each from blue's spawn, by its own way, with the bearing it arrives
from), how exposed each monument is, what stands within four blocks of it, the wash's crossings and the grades.

    python3 plan_check.py            prints the table; the sketch draws the same rows (renders/plan-check.json)
"""
import json
import math
import os

import numpy as np

import plan as P
from pgmvox import plangraph as G
from pgmvox import sight

RED_SPAWN = (P.SPAWN[0], P.SPAWN[2])
BLUE_SPAWN = tuple(int(v) for v in P.SYM.point(*RED_SPAWN))
A = P.OBELISK_AT
B_ = P.STONE_AT


def bearing(p, c):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])) % 360


def diff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def ring(R, c, r, kinds):
    return [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(R.mask(*kinds))
            if math.hypot(R.X[i, k] - c[0], R.Z[i, k] - c[1]) <= r]


def route_via(E, start, via, targets):
    pts = [start] + via
    cost, path = 0.0, []
    for a, b in zip(pts, pts[1:]):
        D, prev = G.dijkstra(E, [a])
        if b not in D:
            return None, []
        cost += D[b]
        path += G.path(prev, b)
    D, prev = G.dijkstra(E, [pts[-1]])
    best = min((c for c in targets if c in D), key=D.get, default=None)
    if best is None:
        return None, path
    return cost + D[best], path + G.path(prev, best)[1:]


def measure():
    R = P.build()
    L = P.land()
    E = G.graph(R, P.WALK, rules=G.PlanRules(jumps=False, diagonals=True), extra=P.links())
    ringA = ring(R, A, 4, ["mesa", "stair"])
    ringB = ring(R, B_, 5, ["square"])
    Dr, pr = G.dijkstra(E, [RED_SPAWN])
    Db, pb = G.dijkstra(E, [BLUE_SPAWN])
    cost = lambda D, ring_: min((D[c] for c in ring_ if c in D), default=None)           # noqa: E731
    own_a, own_b = cost(Dr, ringA), cost(Dr, ringB)
    en_a, en_b = cost(Db, ringA), cost(Db, ringB)
    waysA = {
        "steps (the south face)": ([(A[0], A[1] + 14)], "steps"),
        "mine (below, ladder to the top)": ([(P.MINE[0][0], P.MINE[0][2]), (P.MINE[0][0], P.MINE[0][2], 1),
                                            (-68, -34, 1), (-64, -32, 1), (-64, -29, 1),
                                            (P.MINE[-1][0], P.MINE[-1][2], 1), P.MINE_SHAFT], "mine"),
        "arch (above, from the stepped rock)": ([P.ARCH[0] + (1,), P.ARCH[-1] + (1,)], "arch"),
    }
    sx0, sz0, sx1, sz1 = P.SERAI
    roof = (sx0 + 12, sz0 + 1, 1)
    waysB = {
        "lanes (through the Souk)": ([(-54, 15)], "lanes"),
        "roofs (above, over the caravanserai)": ([(sx1 - 1, sz0 + 1, 1), roof], "roofs"),
        "qanat (below, up the well)": ([(P.QANAT[0][0], P.QANAT[0][2]), (P.QANAT[0][0], P.QANAT[0][2], 1),
                                       (P.CISTERN[0] + 2, P.CISTERN[2], 1), (P.WELL[0], P.WELL[1], 1),
                                       (P.WELL[0], P.WELL[1])], "qanat"),
        "grove (unseen, from the oasis)": ([(-53, 46)], "grove"),
    }
    out = {}
    for goal, ways, ringG, c in (("Obelisk", waysA, ringA, A), ("Sunstone", waysB, ringB, B_)):
        for name, (via, _) in ways.items():
            cst, path = route_via(E, BLUE_SPAWN, via, ringG)
            ground = [p for p in path if len(p) == 2]            # where a player stands on the surface
            d12 = [math.hypot(p[0] - c[0], p[1] - c[1]) > 12 for p in ground]
            last_out = max((j for j, o in enumerate(d12) if o), default=-1) if ground else -1
            brg = bearing(ground[min(last_out + 1, len(ground) - 1)], c) if ground else None
            out[f"{goal}: {name}"] = dict(goal=goal, cost=cst, path=[p[:2] for p in path], bearing=brg)
    # what each monument sees
    opaque = sight.plan_opaque(R)
    seen = {}
    for goal, c, y in (("Obelisk", A, P.TABLE_TOP + 6), ("Sunstone", B_, P.PLATEAU + 5)):
        eye = sight.eye(c[0], y, c[1])
        targets = []
        for i, k in np.argwhere(R.mask("sand", "road", "lane", "square", "yard", "mesa", "grove", "steep") & (R.X < 0)):
            x, z = int(R.X[i, k]), int(R.Z[i, k])
            d = math.hypot(x - c[0], z - c[1])
            if 6 <= d <= 24 and (x + z) % 2 == 0:
                targets.append(sight.target(x, int(R.H[i, k]) + 1, z))
        seen[goal] = 1 - len(sight.hidden(targets, [eye], opaque)) / max(1, len(targets))
    clear = {}
    for goal, c in (("Obelisk", A), ("Sunstone", B_)):
        clear[goal] = min((math.hypot(max(0, abs(x - c[0]) - 0.5), max(0, abs(z - c[1]) - 0.5))
                           for b in P.houses().values() for (x, z) in b["cells"]), default=99)
    # the wash: the walk across it, and the aqueduct's gap
    ax1 = P.ARCADE[2]
    gap = 2 * (-1 - ax1)
    cross = None
    Dn, pn = G.dijkstra(E, [(-24, -8)])
    for c_ in ((23, -8),):
        cross = Dn.get(c_)
    tube = G.dijkstra(E, [(P.QANAT[0][0], P.QANAT[0][2], 1)])[0].get((P.WELL[0], P.WELL[1], 1))
    grades = {}
    for rt in L.routes:
        s, p = rt["profile"]
        grades[rt["name"]] = float(np.max(np.abs(np.diff(p)) / np.maximum(np.diff(s), 1e-6)))
    onroad = 0
    roadm = np.zeros(L.H.shape, bool)
    for mk in L.road_on.values():
        roadm |= mk
    for key, b in P.houses().items():
        onroad += sum(1 for x, z in b["cells"] if roadm[x - P.X_MIN, z - P.Z_MIN])
    return dict(own=(own_a, own_b), enemy=(en_a, en_b), ways=out, seen=seen, clear=clear, gap=gap, cross=cross,
                tube=tube, grades=grades, onroad=onroad)


def rows(m):
    r = []
    names = ("Obelisk", "Sunstone")
    for i, n in enumerate(names):
        o, e = m["own"][i], m["enemy"][i]
        r.append((f"{o:.0f}", f"red spawn to red's {n}", "20-80" if i == 0 else "20-60", 20 <= o <= (80 if i == 0 else 60)))
        r.append((f"{e:.0f}", f"blue spawn to red's {n}", "reached", e is not None))
        r.append((f"{e / o:.2f}", f"ratio of the two walks to the {n}", "at least 2.5 (goal rule)", e / o >= 2.5))
    for goal in names:
        bs = []
        for name, d in m["ways"].items():
            if d["goal"] != goal:
                continue
            c = d["cost"]
            r.append(("not reached" if c is None else f"{c:.0f}", f"blue spawn to the {name}", "reached", c is not None))
            if d["bearing"] is not None:
                bs.append((name.split(":")[1].strip().split(" ")[0], d["bearing"]))
        gaps = [diff(a[1], b[1]) for i, a in enumerate(bs) for b in bs[i + 1:]]
        r.append((", ".join(f"{n} {b:.0f}" for n, b in bs), f"bearings the ways onto the {goal} arrive from (deg)",
                  "all pairs at least 40 apart", bool(gaps) and min(gaps) >= 40))
    for goal in names:
        r.append((f"{m['seen'][goal]:.0%}", f"of the ground 6-24 out seen from the {goal}", "at least 50% (exposed)",
                  m["seen"][goal] >= 0.5))
        r.append((f"{m['clear'][goal]:.1f}", f"nearest building to the {goal}, blocks", "at least 4", m["clear"][goal] >= 4))
    r.append((m["gap"], "blocks of air between the aqueduct's two halves", "8-12 (a bridge to build)",
              8 <= m["gap"] <= 12))
    r.append(("none" if m["cross"] is None else f"{m['cross']:.0f}", "walk across the wash by the north ghats, rim to rim",
              "reached, 45-90", m["cross"] is not None and 45 <= m["cross"] <= 90))
    r.append(("none" if m["tube"] is None else f"{m['tube']:.0f}", "the qanat, mouth in the wash to the well's foot",
              "reached, 45-75", m["tube"] is not None and 45 <= m["tube"] <= 75))
    g = max(m["grades"].values())
    r.append((f"{g:.2f}", "steepest graded road, blocks up per block", "at most 0.6", g <= 0.61))
    r.append((m["onroad"], "building cells standing on a road or lane", "0", m["onroad"] == 0))
    return r


def save(m, rows_, path):
    with open(path, "w") as f:
        json.dump(dict(rows=rows_, paths={k: [list(c) for c in v["path"]] for k, v in m["ways"].items()}), f)


if __name__ == "__main__":
    m = measure()
    rs = rows(m)
    save(m, rs, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "plan-check.json"))
    for v, what, target, ok in rs:
        print(f"{'  ' if ok else '! '}{str(v):>20}  {what}  (target {target})")
