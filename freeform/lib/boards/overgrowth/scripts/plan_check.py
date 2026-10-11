"""Measure Overgrowth's plan before anything is built: the walk between the spawns by each of its lanes (centre over the
tiers, centre through the tunnel, the north terrace, the south terrace, the valley's flanks), the ways out of a court,
the longest clear line of sight a player stands in, what the high places can see of the courts, and the cover.

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


def route_via(E, start, via, end):
    pts = [start] + via + [end]
    cost, path = 0.0, []
    for a, b in zip(pts, pts[1:]):
        D, prev = G.dijkstra(E, [a])
        if b not in D:
            return None, []
        cost += D[b]
        path += G.path(prev, b)
    return cost, path


def clear_lines(R, cap=90):
    """For every walkable ground cell, the longest straight run (16 headings) a player could be shot along before
    something in the plan stands in the way: a cover, a wall, a tower, the rim, or ground three or more over the
    cell's own. Returns the array of longest runs and the walkable mask."""
    walk = R.mask(*[k for k in P.WALK if k in R.kinds]) & ~R.mask("tier2", "tier3", "tier4") & ~R.mask("stair")
    block = R.mask("cover", "wall", "tower", "rim")
    H = R.H
    nx, nz = H.shape
    I, K = np.meshgrid(np.arange(nx), np.arange(nz), indexing="ij")
    best = np.zeros(H.shape, int)
    runs = np.zeros(H.shape, int)
    longer = np.zeros(H.shape, int)
    for a in range(16):
        dx, dz = math.cos(a * math.pi / 8), math.sin(a * math.pi / 8)
        alive = np.ones(H.shape, bool)
        run = np.zeros(H.shape, int)
        for s in range(1, cap):
            ii = np.clip(np.round(I + dx * s).astype(int), 0, nx - 1)
            kk = np.clip(np.round(K + dz * s).astype(int), 0, nz - 1)
            blocked = block[ii, kk] | (H[ii, kk] >= H + 3)
            alive &= ~blocked
            run += alive
        best = np.maximum(best, run)
        runs += run
        longer += run > 40
    return best, walk, runs / 16.0, longer / 16.0


def measure():
    R = P.build()
    E = G.graph(R, P.WALK, rules=G.PlanRules(jumps=False, diagonals=True), extra=P.links())
    D, prev = G.dijkstra(E, [RED_SPAWN])
    shortest = D.get(BLUE_SPAWN)
    lanes = {
        "centre, over the tiers": [(-30, 0), (-20, 0), (0, 0), (19, 0), (30, 0)],
        "centre, through the tunnel": [(-24, -8), (-16, -8, 1), (15, -8, 1), (24, -8)],
        "north terrace": [(-44, -24), (-44, -33), (-30, -42), (30, -42), (43, -33), (43, -24)],
        "south terrace": [(-44, 23), (-44, 32), (-30, 41), (30, 41), (43, 32), (43, 23)],
        "valley, north flank": [(-30, -20), (30, -20)],
        "valley, south flank": [(-30, 19), (30, 19)],
    }
    out = {}
    for name, via in lanes.items():
        c, path = route_via(E, RED_SPAWN, via, BLUE_SPAWN)
        out[name] = dict(cost=c, path=[p[:2] for p in path])
    # a lane's own ways out: the court's three gates each reach the valley
    gates = {}
    for side, x0, z0, x1, z1 in P.GATES:
        c = ((x0 + x1) // 2, (z0 + z1) // 2)
        gates[side] = D.get(c)
    best, walk, mean, share = clear_lines(R)
    sel = walk & (R.Z < 0) & ~R.mask("court", "gate") & (R.X < 0)
    vals, means, shares = best[sel], mean[sel], share[sel]
    # sight: the high places over the courts
    roofs = {}
    for i, k in np.argwhere(R.mask("wall", "tower", "rim")):
        x, z = int(R.X[i, k]), int(R.Z[i, k])
        roofs[(x, z)] = _roof(R, x, z)
    opaque = sight.plan_opaque(R, roofs)
    seen = {}
    eyes = {"the ziggurat's top": [sight.eye(x, 74, z) for x in (-6, 6) for z in (-4, 4)],
            "a watchtower's platform": [sight.eye(-34, P.TOWER_TOP + 1, -41)]}
    court = [(x, z) for x in range(P.COURT[0] + 1, P.COURT[2]) for z in range(P.COURT[1] + 1, P.COURT[3]) if (x + z) % 2 == 0]
    targets = [sight.target(x, P.COURT_Y + 1, z) for x, z in court]
    for name, es in eyes.items():
        seen[name] = 1 - len(sight.hidden(targets, es, opaque)) / len(targets)
    near_cover = _cover_share(R)
    return dict(shortest=shortest, lanes=out, gates=gates, lines=vals, means=means, shares=shares, seen=seen, cover=near_cover, R=R)


def _roof(R, x, z):
    """Solid bands over the raster for the walls, towers and rim: the court's four, a tower's fourteen."""
    k = R.kind(x, z)
    h = R.h(x, z)
    if k == "wall":
        return (h + 1, h + 6)
    if k == "tower":
        return (h + 1, h + 14)
    if k == "rim":
        return (h + 1, h + 8)
    return None


def _cover_share(R):
    from scipy import ndimage
    cov = R.mask("cover", "wall", "tower") & (R.Z < 0)
    near = ndimage.binary_dilation(cov, iterations=5)
    play = R.mask("valley", "bank", "strip", "ford", "tier1") & (R.Z < 0) & (R.X < 0)
    return float((near & play).sum() / play.sum())


def rows(m):
    r = []
    s = m["shortest"]
    r.append((f"{s:.0f}", "spawn to the enemy spawn, shortest", "100-150", 100 <= s <= 150))
    costs = []
    for name, d in m["lanes"].items():
        c = d["cost"]
        costs.append(c)
        r.append(("not reached" if c is None else f"{c:.0f}", f"spawn to spawn by the {name}",
                  "within 1.5 of the shortest", c is not None and c <= 1.5 * s))
    r.append((", ".join(f"{k} {v:.0f}" for k, v in m["gates"].items()), "walk from the spawn to each gate of its court",
              "all reached, 8-30 (the baffles cost a detour)", all(v is not None and 8 <= v <= 30 for v in m["gates"].values())))
    v = m["lines"]
    mean, share = m["means"], m["shares"]
    r.append((f"{int(v.max())}", "the longest clear line of sight from any ground cell, any heading", "information", None))
    r.append((f"{mean.mean():.0f} / {np.percentile(mean, 90):.0f}", "mean clear run over sixteen headings: average / 90th percentile cell",
              "at most 30 / 45", mean.mean() <= 30 and np.percentile(mean, 90) <= 45))
    r.append((f"{share.mean():.0%}", "of cell-headings with a clear run past 40", "at most 20%", share.mean() <= 0.20))
    for name, share in m["seen"].items():
        r.append((f"{share:.0%}", f"of red's court floor seen from {name}", "at most 8%: the gates' throats only", share <= 0.08))
    r.append((f"{m['cover']:.0%}", "of red's open ground within five of a cover", "at least 45%", m["cover"] >= 0.45))
    return [(v, w_, t, None if ok is None else bool(ok)) for v, w_, t, ok in r]


def save(m, rows_, path):
    with open(path, "w") as f:
        json.dump(dict(rows=rows_, paths={k: [list(c) for c in v["path"]] for k, v in m["lanes"].items()}), f)


if __name__ == "__main__":
    m = measure()
    rs = rows(m)
    save(m, rs, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "plan-check.json"))
    for v, what, target, ok in rs:
        print(f"{'  ' if ok or ok is None else '! '}{str(v):>22}  {what}  (target {target})")
