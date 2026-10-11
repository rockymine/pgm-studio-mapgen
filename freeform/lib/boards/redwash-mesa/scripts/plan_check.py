"""Measure Redwash Mesa's plan before anything is built: each monument's walks against the studio's goal rules, the
ways onto each and what they cost, the seam's widths at its three heights, the spawn's back, what stands near a
monument.

Walks are octile over the plan (a step up 1.2, a drop past three a block extra for the fall); the seam is crossed
by building, a block of bridge a block.

    python3 plan_check.py        prints the table; the sketch draws the same rows and routes
"""
import json
import math
import os

import numpy as np

import plan as P
import common as C
from pgmvox import plangraph as G

HERE = os.path.dirname(os.path.abspath(__file__))


def near(x, z, r, R, ok=None):
    return [(x + dx, z + dz) for dx in range(-r, r + 1) for dz in range(-r, r + 1)
            if math.hypot(dx, dz) <= r and R.inside(x + dx, z + dz) and (ok is None or ok(x + dx, z + dz))]


def measure():
    R = P.build()
    L = P.land()
    zone = P.zone(R)
    E = G.graph(R, P.WALK, rules=G.PlanRules(diagonals=True, drop_cost=1.0), bridge=zone, extra=P.links())
    red_sp = (P.SPAWN[0], P.SPAWN[2])
    blue_sp = P.SYM.point(*red_sp)
    Dr, prr = G.dijkstra(E, [red_sp])
    Db, prb = G.dijkstra(E, [blue_sp])
    walks, paths = {}, {}
    for key in P.MONUMENTS:
        own_r, _, p_own = G.measure(Dr, prr, E, P.monument_ring(key, "red"))
        own_b = G.measure(Db, prb, E, P.monument_ring(key, "blue"))[0]
        en_r, by, p_en = G.measure(Db, prb, E, P.monument_ring(key, "red"))
        en_b = G.measure(Dr, prr, E, P.monument_ring(key, "blue"))[0]
        walks[key] = dict(own=(own_r, own_b), enemy=(en_r, en_b), bridged=by.get("bridge", 0))
        paths[f"own {key}"], paths[f"enemy {key}"] = p_own, p_en

    walkable = lambda x, z: R.kind(x, z) in P.WALK                       # noqa: E731
    (px, pz), prx, prz, _ = P.POOL
    mine_mid = [(x, z, 1) for x, y, z in P.mine_line() if 8 <= z <= 12]
    ways = {
        "table": {
            "across the rim, north of the pool": near(px, pz - int(prz) - 3, 2, R, walkable),
            "across the rim, south of the pool": near(px, pz + int(prz) + 3, 2, R, walkable),
            "through the junipers": near(-46, -44, 3, R, walkable),
            "up the Silver Drift": mine_mid,
        },
        "wash": {
            "up the Wash through the Gate": near(-30, 28, 2, R, walkable),
            "off the Shelf, a drop of 11": near(-47, 15, 3, R, lambda x, z: R.h(x, z) == P.SHELF),
            "down the Bench stair": near(-38, 38, 1, R, lambda x, z: R.kind(x, z) == "stair"),
        },
    }
    approach = {}
    for key, ws in ways.items():
        for name, wp in ws.items():
            cost, path = C.via(E, [blue_sp], wp, P.monument_ring(key, "red"))
            at_b = min((Db[c] for c in wp if c in Db), default=math.inf)
            at_r = min((Dr[c] for c in wp if c in Dr), default=math.inf)
            approach[(key, name)] = (cost, path, at_b, at_r)

    gaps = C.gaps(R.K != R.kinds["void"], range(R.x_min, R.x_max + 1), range(R.z_min, R.z_max + 1), "x")
    gv = sorted(v for z, v in gaps.items() if abs(z + 0.5) <= 56)
    by_level = {}
    for name, z0, z1 in (("the Table", -50, 8), ("the Gate (the Wash)", 20, 34), ("the Bench", 44, 56)):
        vs = [gaps[z] for z in range(z0, z1 + 1) if z in gaps]
        by_level[name] = (min(vs), max(vs))
    angles = {}
    for key, ((x, z), _) in P.MONUMENTS.items():
        a = abs(math.degrees(math.atan2(z - red_sp[1], x - red_sp[0]) -
                             math.atan2(blue_sp[1] - red_sp[1], blue_sp[0] - red_sp[0])))
        angles[key] = min(a, 360 - a)
    back = max(R.h(x, z) for x, z in near(red_sp[0], red_sp[1], 20, R) if R.kind(x, z) not in ("void", "house"))
    behind = sum(1 for x in range(red_sp[0] - 1, R.x_min - 1, -1) if R.kind(x, red_sp[1]) != "void")

    def dmin(cells, key):
        (mx, mz), _ = P.MONUMENTS[key]
        return min((math.hypot(a - mx, b - mz) for a, b in cells), default=99)
    houses = [c for b in P.houses().values() for c in b["cells"]]
    jun = [(int(L.X[i, k]), int(L.Z[i, k])) for i, k in np.argwhere(L.junipers)]
    cover = {key: (dmin(houses, key), dmin(jun, key)) for key in P.MONUMENTS}
    apart = math.dist(*[m for m, _ in P.MONUMENTS.values()])
    return dict(R=R, walks=walks, paths=paths, approach=approach, gv=gv, by_level=by_level, angles=angles,
                back=back, behind=behind, cover=cover, apart=apart)


def rows(m):
    out = []
    for key, wk in m["walks"].items():
        o_r, o_b = wk["own"]
        e_r, e_b = wk["enemy"]
        out += [
            (f"{o_r:.1f} / {o_b:.1f}", f"spawn to its own {key} monument, red / blue", "GO4: 40-90, equal",
             40 <= o_r <= 90 and abs(o_r - o_b) < .01),
            (f"{e_r:.1f} / {e_b:.1f}", f"enemy spawn to the {key} monument ({wk['bridged']:.0f} bridged)",
             "GO3: 85-150, equal", 85 <= e_r <= 150 and abs(e_r - e_b) < .01),
            (f"{e_r / o_r:.2f}", f"   enemy over own, the {key} monument", "GO1: 3-4", 3 <= e_r / o_r <= 4),
            (f"{m['angles'][key]:.0f} deg", f"   the {key} monument off the line between the spawns", "20-60",
             20 <= m["angles"][key] <= 60),
        ]
    for key in m["walks"]:
        best = min(v[0] for (k, _), v in m["approach"].items() if k == key)
        for (k, name), (c, _, ab, ar) in m["approach"].items():
            if k != key:
                continue
            out.append((f"{c:.0f} (x{c / best:.2f})", f"blue onto red's {key} monument {name}",
                        "at most 1.3 x the shortest", c <= 1.3 * best))
            out.append((f"blue {ab:.0f}, red {ar:.0f}", "   who reaches that way's mouth first", "red first", ar < ab))
    for name, (lo, hi) in m["by_level"].items():
        out.append((f"{lo}-{hi}", f"the seam's void at {name}", "16-28", 16 <= lo and hi <= 28))
    out += [
        (f"{m['back'] - P.SHELF}", "ground over the spawn ledge within 20", "at least 8", m["back"] - P.SHELF >= 8),
        (f"{m['behind']}", "the spawn's own land behind it", "at least 8", m["behind"] >= 8),
    ]
    for key, (h, j) in m["cover"].items():
        out.append((f"{h:.1f}, {j:.1f}", f"nearest house, juniper ground to the {key} monument", "at least 4",
                    min(h, j) >= 4))
    out.append((f"{m['apart']:.0f}", "the two monuments apart (a north and a south)", "30-70", 30 <= m["apart"] <= 70))
    return out


if __name__ == "__main__":
    m = measure()
    r = rows(m)
    print(C.table(r))
    paths = dict(m["paths"])
    paths.update({f"{k} | {n}": v[1] for (k, n), v in m["approach"].items()})
    with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
        json.dump(dict(rows=[(str(a), b, c_, None if d is None else bool(d)) for a, b, c_, d in r],
                       paths={k: [list(c) for c in v] for k, v in paths.items()}), f)
