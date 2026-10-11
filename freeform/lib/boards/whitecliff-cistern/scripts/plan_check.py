"""Measure Whitecliff Cistern's plan before anything is built: each spawn's walk to each of the three hills (the same
for both by the mirror), the ways onto each hill and the bearing each arrives from, how high each pad stands over
the ground round it, how far the flanks stand out, what each hill sees of a spawn, the longest runs of clear sight,
the cover, and the share of the town no route to a hill passes through.

    python3 plan_check.py            prints the table; the sketch draws the same rows (renders/plan-check.json)
"""
import json
import math
import os

import numpy as np

import plan as P
from pgmvox import plangraph as G
from pgmvox import sight

RED_SPAWN = (P.SPAWN_AT[0], P.SPAWN_AT[2])
BLUE_SPAWN = tuple(int(v) for v in P.SYM.point(*RED_SPAWN))
CENTRES = {"cistern": (-0.5, -0.5), "garden": (-0.5, -42.5), "boatyard": (-0.5, 42.5)}


def pad_cells(R, key):
    box = [b for k, n, b, p in P.HILLS if k == key][0]
    if key == "cistern":
        return [(x, z, 1) for x in range(box.x0, box.x1 + 1) for z in range(box.z0, box.z1 + 1)]
    return [(x, z) for x in range(box.x0, box.x1 + 1) for z in range(box.z0, box.z1 + 1)]


def bearing(p, c):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])) % 360


def diff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


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


WAYS = {
    "cistern": {
        "north-west stairwell": [(-6, -9), (-6, -4, 1)], "north-east stairwell": [(5, -9), (5, -4, 1)],
        "south-west stairwell": [(-6, 8), (-6, 3, 1)], "south-east stairwell": [(5, 8), (5, 3, 1)],
        "the oculus (a drop)": [(-3, 0)], "the west undercroft": [(-41, -1), (-40, -1, 1), (-26, -1, 1)],
        "the east undercroft": [(40, -1), (39, -1, 1), (25, -1, 1)]},
    "garden": {"the west gate": [(-21, -40), (-14, -40)], "the east gate": [(20, -40), (13, -40)],
               "the steps from the north plaza": [(0, -31), (0, -34)]},
    "boatyard": {"the west ramp": [(-19, 40), (-14, 40)], "the east ramp": [(18, 40), (13, 40)],
                 "the steps from the south plaza": [(0, 31), (0, 36)]},
}


def clear_lines(R, cap=80):
    walk = R.mask(*[k for k in P.WALK if k in R.kinds]) & ~R.mask("stair", "vault", "tunnel", "roof")
    block = R.mask("cover", "wall", "house")
    H = R.H
    nx, nz = H.shape
    I, K = np.meshgrid(np.arange(nx), np.arange(nz), indexing="ij")
    runs = np.zeros(H.shape, int)
    longer = np.zeros(H.shape, int)
    best = np.zeros(H.shape, int)
    for a in range(16):
        dx, dz = math.cos(a * math.pi / 8), math.sin(a * math.pi / 8)
        alive = np.ones(H.shape, bool)
        run = np.zeros(H.shape, int)
        for s in range(1, cap):
            ii = np.clip(np.round(I + dx * s).astype(int), 0, nx - 1)
            kk = np.clip(np.round(K + dz * s).astype(int), 0, nz - 1)
            alive &= ~(block[ii, kk] | (H[ii, kk] >= H + 3) | (R.K[ii, kk] == R.kinds["void"]) & (H[ii, kk] == 0) & False)
            run += alive
        runs += run
        longer += run > 35
        best = np.maximum(best, run)
    return best, walk, runs / 16.0, longer / 16.0


def measure():
    R = P.build()
    E = G.graph(R, P.WALK, rules=G.PlanRules(jumps=False, diagonals=True, max_drop=None, drop_cost=1.5))
    Dr, pr = G.dijkstra(E, [RED_SPAWN])
    walks, ways = {}, {}
    for hill in P.HILLS:
        key = hill[0]
        cells = pad_cells(R, key)
        walks[key] = min((Dr[c] for c in cells if c in Dr), default=None)
        for name, via in WAYS[key].items():
            c, path = route_via(E, RED_SPAWN, via, cells)
            cc = CENTRES[key]
            out_ = [j for j, p in enumerate(path) if math.hypot(p[0] - cc[0], p[1] - cc[1]) > 9]
            brg = bearing(path[min(out_[-1] + 1, len(path) - 1)][:2], cc) if out_ else None
            ways[(key, name)] = dict(cost=c, path=[p[:2] for p in path], bearing=brg)
    # pads against the ground round them
    over = {}
    for key, name, box, pts in P.HILLS:
        cc = CENTRES[key]
        near = [R.h(x, z) for x in range(int(cc[0]) - 12, int(cc[0]) + 13) for z in range(int(cc[1]) - 12, int(cc[1]) + 13)
                if R.inside(x, z) and R.kind(x, z) in ("street", "plaza", "ring", "yard", "court", "garden", "dock", "quay")]
        over[key] = box.y0 - float(np.median(near))
    # what each hill sees of a spawn's floor
    roofs = {}
    for i, k in np.argwhere(R.mask("wall")):
        x, z = int(R.X[i, k]), int(R.Z[i, k])
        roofs[(x, z)] = (R.h(x, z) + 1, R.h(x, z) + 6)
    for i, k in np.argwhere(R.mask("house")):
        x, z = int(R.X[i, k]), int(R.Z[i, k])
        roofs[(x, z)] = (R.h(x, z) + 1, R.h(x, z) + 8)
    opaque = sight.plan_opaque(R, roofs)
    quay = [(x, z) for x in range(-57, -48) for z in range(-8, 8) if (x + z) % 2 == 0]
    targets = [sight.target(x, P.QUAY + 1, z) for x, z in quay]
    seen = {}
    for key, name, box, pts in P.HILLS:
        cc = CENTRES[key]
        eyes = [sight.eye(int(cc[0]) + dx, box.y0 + 1, int(cc[1]) + dz) for dx in (-2, 2) for dz in (-2, 2)]
        seen[key] = 1 - len(sight.hidden(targets, eyes, opaque)) / len(targets)
    # the rooftops: what the roofs see of the quay
    roof_eyes = [sight.eye(x, P.ROOF + 1, z) for x in (-39, -30) for z in (-20, -6, 5, 17)]
    seen["the rooftops"] = 1 - len(sight.hidden(targets, roof_eyes, opaque)) / len(targets)
    best, walk, mean, share = clear_lines(R)
    sel = walk & (R.X < 0)
    # dead ground: cells on no corridor (within 6 of a shortest route) between a spawn and a hill
    Dh = {}
    for key, *_ in P.HILLS:
        Dh[key] = G.dijkstra(E, pad_cells(R, key))[0]
    Db_, _ = G.dijkstra(E, [BLUE_SPAWN])
    on = set()
    for key, *_ in P.HILLS:
        for Ds in (Dr, Db_):
            best_ = min(Ds[c] for c in pad_cells(R, key) if c in Ds)
            for n, d in Ds.items():
                if len(n) == 2 and n in Dh[key] and d + Dh[key][n] <= best_ + 8:
                    on.add(n)
    walkable = [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(R.mask(*[k for k in P.WALK if k in R.kinds]) & (R.X < 0)
                                                                         & ~R.mask("vault", "tunnel", "roof"))]
    dead = 1 - sum(1 for c in walkable if c in on) / len(walkable)
    from scipy import ndimage
    cov = R.mask("cover", "wall", "house") & (R.X < 0)
    near = ndimage.binary_dilation(cov, iterations=5)
    play = R.mask("street", "plaza", "ring", "yard", "court", "garden", "dock") & (R.X < 0)
    cover = float((near & play).sum() / play.sum())
    return dict(walks=walks, ways=ways, over=over, seen=seen, means=mean[sel], shares=share[sel], best=best[sel],
                dead=dead, cover=cover, R=R)


def rows(m):
    r = []
    w = m["walks"]
    for key, name, box, pts in P.HILLS:
        r.append((f"{w[key]:.0f}", f"each spawn to {name}, by the shortest way (equal for both by the mirror)",
                  "reached", w[key] is not None))
    r.append((f"{w['garden'] / w['cistern']:.2f} / {w['boatyard'] / w['cistern']:.2f}", "the flanks' walk over the middle's",
              "at most 1.6", max(w["garden"], w["boatyard"]) / w["cistern"] <= 1.6))
    d = [math.hypot(c[0] - (-0.5), c[1] - (-0.5)) for c in (CENTRES["garden"], CENTRES["boatyard"])]
    sp = math.hypot(P.SPAWN_AT[0] + 0.5, P.SPAWN_AT[2] + 0.5)
    r.append((f"{d[0] / sp:.2f} / {d[1] / sp:.2f}", "a flank's distance from the middle over a spawn's",
              "0.52-0.88 (corpus quartiles), at the top", all(0.52 <= v <= 0.88 for v in (d[0] / sp, d[1] / sp))))
    for key, name, box, pts in P.HILLS:
        bs = []
        for (k, way), v in m["ways"].items():
            if k != key:
                continue
            c = v["cost"]
            r.append(("not reached" if c is None else f"{c:.0f}", f"the way onto {name}: {way}", "reached", c is not None))
            if v["bearing"] is not None:
                bs.append((way, v["bearing"]))
        sectors = {int(b // 45) for _, b in bs}
        need = 4 if key == "cistern" else 3
        r.append((", ".join(f"{b:.0f}" for _, b in bs), f"bearings the ways onto {name} arrive from (deg); {len(sectors)} of 8 sectors",
                  f"at least {need} of the eight 45-degree sectors", len(sectors) >= need))
    r.append((", ".join(f"{k} {v:+.0f}" for k, v in m["over"].items()), "each pad's floor over the median ground within 12",
              "at most +2 (no raised pad)", all(v <= 2 for v in m["over"].values())))
    r.append((", ".join(f"{k} {v:.0%}" for k, v in m["seen"].items()), "of a spawn's floor seen from each hill and from the roofs",
              "0% from the hills; at most 8% from the roofs",
              all(m["seen"][k] == 0 for k in ("cistern", "garden", "boatyard")) and m["seen"]["the rooftops"] <= 0.08))
    mean, share = m["means"], m["shares"]
    r.append((f"{int(m['best'].max())}", "the longest clear line of sight from any ground cell, any heading", "information", None))
    r.append((f"{mean.mean():.0f} / {np.percentile(mean, 90):.0f}", "mean clear run over sixteen headings: average / 90th percentile cell",
              "at most 22 / 38", mean.mean() <= 22 and np.percentile(mean, 90) <= 38))
    r.append((f"{share.mean():.0%}", "of cell-headings with a clear run past 35", "at most 12%", share.mean() <= 0.12))
    r.append((f"{m['dead']:.0%}", "of red's walkable ground on no corridor from a spawn to a hill", "at most 25% (a capture board: little dead space)",
              m["dead"] <= 0.25))
    r.append((f"{m['cover']:.0%}", "of red's open ground within five of a cover", "at least 55%", m["cover"] >= 0.55))
    r.append(("2 / 1 / 1", "points a second: the Cistern, the Garden, the Boatyard", "the middle pays double", True))
    return [(v, w_, t, None if ok is None else bool(ok)) for v, w_, t, ok in r]


def save(m, rows_, path):
    with open(path, "w") as f:
        json.dump(dict(rows=rows_, paths={f"{k[0]}: {k[1]}": [list(c) for c in v["path"]] for k, v in m["ways"].items()}), f)


if __name__ == "__main__":
    m = measure()
    rs = rows(m)
    save(m, rs, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "plan-check.json"))
    for v, what, target, ok in rs:
        print(f"{'  ' if ok or ok is None else '! '}{str(v):>30}  {what}  (target {target})")
