"""Measure Cinderfall's plan before anything is built: each team's walk to red's core, the ratio of the two, the five
approaches (each from the enemy spawn, by its own way, with the bearing it arrives from), how exposed the core is,
what stands within four blocks of it, and the grades of the roads.

    python3 plan_check.py            prints the table; the sketch draws the same rows (renders/plan-check.json)
"""
import json
import math
import os

import numpy as np

import plan as P
from pgmvox import plangraph as G
from pgmvox import shapes, sight

RED_SPAWN = (P.SPAWN[0], P.SPAWN[2])
BLUE_SPAWN = tuple(int(v) for v in P.SYM.point(*RED_SPAWN))
CORE = P.CORE_AT


def ring_cells(R):
    return [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(R.mask("plinth")) if R.X[i, k] < 0]


def bearing(p, c):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])) % 360


def diff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def approach(E, D_from, prev_from, wps, ring, R):
    """The path from a spawn to the ring by way of waypoints (cells, in order); cost and cells."""
    cost, cells, start = 0.0, [], None
    return None


def route_via(E, start, via, ring):
    """Cheapest walk start -> each via cell in turn -> the ring. Returns (cost, path, tags)."""
    pts = [start] + via
    cost, path, tags = 0.0, [], []
    for a, b in zip(pts, pts[1:]):
        D, prev = G.dijkstra(E, [a])
        if b not in D:
            return None, [], []
        cost += D[b]
        path += G.path(prev, b)
    D, prev = G.dijkstra(E, [pts[-1]])
    best = min((c for c in ring if c in D), key=D.get, default=None)
    if best is None:
        return None, path, []
    c, moves = G.route(D, prev, [best])
    return cost + D[best], path + G.path(prev, best)[1:], moves


def measure():
    R = P.build()
    E = G.graph(R, P.WALK, rules=G.PlanRules(jumps=False, diagonals=True), extra=P.links())
    ring = ring_cells(R)
    Dr, pr = G.dijkstra(E, [RED_SPAWN])
    Db, pb = G.dijkstra(E, [BLUE_SPAWN])
    own = min(Dr[c] for c in ring if c in Dr)
    enemy = min(Db[c] for c in ring if c in Db)
    cx, cz = CORE
    # the core's angle off the line between the spawns, measured from red's spawn
    a1 = bearing(CORE, RED_SPAWN)
    a2 = bearing(BLUE_SPAWN, RED_SPAWN)
    off = diff(a1, a2)

    # the five approaches, from blue's spawn, each by its waypoints (red's coordinates)
    ledge = (cx, -33)
    pit = tuple(int(v) for v in P.PIT[0])
    ways = {
        "around (the open ash)": ([(-36, -4)], "road"),
        "above (the Slag Ridge)": ([(-30, -37), (-48, -37), (cx, -33)], "ridge"),
        "below (the vent tube)": ([pit, (P.VENT[0][0], P.VENT[0][2], 1), (P.VENT[-1][0], P.VENT[-1][2], 1)], "tube"),
        "through (the Foundry Row)": ([(-46, 15), (-46, 4)], "row"),
        "unseen (the Charred Wood)": ([(-30, -24)], "wood"),
    }
    out = {}
    for name, (via, _) in ways.items():
        if name.startswith("above"):
            cost, path, moves = route_via(E, BLUE_SPAWN, via, [ledge])
            cost_ring = cost
        else:
            cost, path, moves = route_via(E, BLUE_SPAWN, via, ring)
        brg = None
        if path:
            brg = bearing(ledge, CORE) if name.startswith("above") else bearing([p for p in path if math.hypot(p[0] - cx, p[1] - cz) > 9][-1][:2], CORE)
        out[name] = dict(cost=cost, path=[p[:2] for p in path], bearing=brg, tube=any(m == "tube" for m in (moves or [])) or
                         any(len(p) == 3 for p in path))
    # above: the ledge to the core, across and down
    top_y = P.at(P.land(), cx, -33)
    ledge_gap = math.hypot(0, -33 - (cz - 2.5)) if False else abs(-33 - cz) - 3
    ledge_drop = top_y - (P.PLINTH_Y + P.FLOAT + 2)

    # what the core sees: ground within 6..24 of it seen from the top of its casing
    opaque = sight.plan_opaque(R)
    eye = sight.eye(cx, P.PLINTH_Y + P.FLOAT + 5, cz)
    targets = []
    for i, k in np.argwhere(R.mask("ground", "road", "track", "plinth", "wood", "steep", "ridge") & (R.X < 0)):
        x, z = int(R.X[i, k]), int(R.Z[i, k])
        d = math.hypot(x - cx, z - cz)
        if 6 <= d <= 24 and (x + z) % 2 == 0:
            targets.append(sight.target(x, int(R.H[i, k]) + 1, z))
    seen = 1 - len(sight.hidden(targets, [eye], opaque)) / len(targets)

    # what stands within four blocks of the casing
    near = [(x, z) for key, b in P.houses().items() for (x, z) in b["cells"]
            if math.hypot(max(0, abs(x - cx) - 2.5), max(0, abs(z - cz) - 2.5)) < 4.5]
    clear = min((math.hypot(max(0, abs(x - cx) - 2), max(0, abs(z - cz) - 2)) for key, b in P.houses().items()
                 for (x, z) in b["cells"]), default=99)

    # the tube: the walk through it, pit to blowhole
    Dp, pp = G.dijkstra(E, [(P.VENT[0][0], P.VENT[0][2], 1)])
    tube_len = Dp.get((P.VENT[-1][0], P.VENT[-1][2], 1))
    # the roads' steepest grade
    L = P.land()
    grades = {}
    for rt in L.routes:
        s, p = rt["profile"]
        g = np.abs(np.diff(p)) / np.maximum(np.diff(s), 1e-6)
        grades[rt["name"]] = float(g.max())
    on_road = 0
    roadm = np.zeros(L.H.shape, bool)
    for mk in L.road_on.values():
        roadm |= mk
    for key, b in P.houses().items():
        on_road += sum(1 for x, z in b["cells"] if roadm[x - P.X_MIN, z - P.Z_MIN])
    beacon = (-48, -37)
    to_beacon = Dr.get(beacon)
    caldera = dict(rim=int(L.H[(L.X == -1) & (L.Z == -28)].max()), floor=int(L.H[(L.X == -12) & (L.Z == -1)].max()))
    return dict(R=R, own=own, enemy=enemy, off=off, ways=out, seen=seen, clear=clear, tube=tube_len, grades=grades,
                ledge_gap=ledge_gap, ledge_drop=ledge_drop, to_beacon=to_beacon, caldera=caldera, near=near, on_road=on_road)


def rows(m):
    r = []
    ratio = m["enemy"] / m["own"]
    r.append((f"{m['own']:.0f}", "red spawn to red's core plinth", "25-50 (near its own spawn)", 25 <= m["own"] <= 50))
    r.append((f"{m['enemy']:.0f}", "blue spawn to red's core plinth", "at least 3 times the walk home", ratio >= 3))
    r.append((f"{ratio:.2f}", "ratio of the two walks", "3.0-4.5 (goal rule)", 3.0 <= ratio <= 4.5))
    r.append((f"{m['off']:.0f} deg", "the core's angle off the spawn-to-spawn line", "20-76 (corpus quartiles)",
              20 <= m["off"] <= 76))
    bs = []
    for name, d in m["ways"].items():
        c = d["cost"]
        r.append(("not reached" if c is None else f"{c:.0f}", f"blue spawn to the core by the way {name}",
                  "reached", c is not None))
        if d["bearing"] is not None:
            bs.append((name, d["bearing"]))
    gaps = [diff(a[1], b[1]) for i, a in enumerate(bs) for b in bs[i + 1:]]
    r.append((", ".join(f"{n.split(' ')[0]} {b:.0f}" for n, b in bs), "bearings the five ways arrive from (deg)",
              "all pairs at least 40 apart", min(gaps) >= 40 if gaps else False))
    r.append((f"{m['ledge_gap']:.0f} across, {m['ledge_drop']:.0f} down", "the ridge's ledge to the core's casing",
              "a bridge to build: 12-24 across", 12 <= m["ledge_gap"] <= 24))
    r.append((f"{m['seen']:.0%}", "of the ground 6-24 out seen from atop the core", "at least 60% (exposed)",
              m["seen"] >= 0.6))
    r.append((f"{m['clear']:.1f}", "nearest building to the casing, blocks", "at least 4", m["clear"] >= 4))
    r.append(("none" if m["tube"] is None else f"{m['tube']:.0f}", "the vent tube, pit mouth to blowhole mouth",
              "reached, 35-60", m["tube"] is not None and 35 <= m["tube"] <= 60))
    r.append(("none" if m["to_beacon"] is None else f"{m['to_beacon']:.0f}", "red spawn to the beacon on the ridge",
              "at most 70", m["to_beacon"] is not None and m["to_beacon"] <= 70))
    g = max(m["grades"].values())
    r.append((f"{g:.2f}", "steepest graded road, blocks up per block", "at most 0.6", g <= 0.61))
    r.append((f"{m['caldera']['rim'] - m['caldera']['floor']}", "the caldera, the north rim over the basin floor",
              "6-20", 6 <= m["caldera"]["rim"] - m["caldera"]["floor"] <= 20))
    r.append((m["on_road"], "building cells standing on a road or track", "0", m["on_road"] == 0))
    return r


def save(m, rows_, path):
    with open(path, "w") as f:
        json.dump(dict(rows=rows_, paths={k: [list(c) for c in v["path"]] for k, v in m["ways"].items()}), f)


if __name__ == "__main__":
    m = measure()
    rs = rows(m)
    save(m, rs, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "plan-check.json"))
    for v, what, target, ok in rs:
        print(f"{'  ' if ok else '! '}{str(v):>16}  {what}  (target {target})")
