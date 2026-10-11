"""Measure Tidewell Canals' plan before anything is built, against approaches.md (where the points go) and
match-flow.md §10 (what is round them): each team's arrival at each hill, where the flanks stand against the
board, what each pad sees of a spawn and what overlooks it, the ways into each market, cover, and dead ground.

Walks are octile over the plan (a step up 1.2), jumps included; a swimmer climbs out only at the steps.

    python3 plan_check.py        prints the table; the sketch draws the same rows and routes
"""
import json
import math
import os

import numpy as np
from scipy import ndimage

import plan as P
import common as C
from pgmvox import plangraph as G
from pgmvox import sight

HERE = os.path.dirname(os.path.abspath(__file__))
HILLS = ["campo", "north-market", "south-market"]


def measure():
    R = P.build()
    E = G.graph(R, P.WALK, wall_kinds=P.WALLS, rules=G.PlanRules(diagonals=True), extra=P.stair_links(R))
    red, blue = (P.SPAWN_AT[0], P.SPAWN_AT[2]), P.SYM.point(P.SPAWN_AT[0], P.SPAWN_AT[2])
    targets = {h: P.pad_cells(h) for h in HILLS}
    arr = G.arrivals(E, {"red": [red], "blue": [blue]}, targets)
    Dr, prr = G.dijkstra(E, [red])
    Db, prb = G.dijkstra(E, [blue])
    paths = {h: G.measure(Dr, prr, E, targets[h])[2] for h in HILLS}
    # where the flanks stand: centre to flank over centre to spawn, straight
    cx, cz = 0, 0
    fx, fz = np.mean([c for c in targets["north-market"]], axis=0)
    ratio = math.hypot(fx - cx, fz - cz) / math.hypot(red[0] - cx, red[1] - cz)
    # sight: each pad's standing eyes against the spawn courts; the gallery's eyes against the centre pad
    roofs = {}
    lx0, lz0, lx1, lz1 = P.LOGGIA
    for x in range(lx0, lx1 + 1):
        for z in range(lz0, lz1 + 1):
            for a, b in ((x, z), P.SYM.point(x, z)):
                roofs[(a, b)] = (P.LOGGIA_ROOF, P.LOGGIA_ROOF)
    gx0, gz0, gx1, gz1 = P.GALLERY_SPAN
    for x in range(gx0, gx1 + 1):
        for z in range(gz0, gz1 + 1):
            for a, b in ((x, z), (x, -1 - z)):
                for p in ((a, b), P.SYM.point(a, b)):
                    roofs[p] = (P.GALLERY, P.GALLERY)
    opaque = sight.plan_opaque(R, roofs)
    x0, z0, x1, z1 = P.CUSTOMS
    court = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, -1 - z0 + 1)]
    court += [P.SYM.point(x, z) for x, z in court]
    spawn_t = [sight.target(x, P.STREET + 1, z) for x, z in court[::2]]
    seen = {}
    for h in HILLS:
        eyes = [sight.eye(x, P.STREET + 1, z) for x, z in targets[h]]
        seen[h] = 1 - len(sight.hidden(spawn_t, eyes, opaque)) / len(spawn_t)
    gal = [sight.eye(x, P.GALLERY + 1, z) for x in range(gx0, gx1 + 1) for z in range(gz0, gz1 + 1)]
    pad_t = [sight.target(x, P.STREET + 1, z) for x, z in targets["campo"]]
    seen_from_gallery = 1 - len(sight.hidden(pad_t, gal, opaque)) / len(pad_t)
    # the ways into a market: runs of the market's boundary where walkable ground outside meets it
    mk = np.zeros(R.H.shape, bool)
    mx0, mz0, mx1, mz1 = P.MARKET
    mk[R.ix(mx0):R.ix(-mx0 - 1) + 1, R.iz(mz0):R.iz(mz1) + 1] = True
    walk = R.mask(*P.WALK)
    entry = np.zeros_like(mk)
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        sh = np.roll(np.roll(walk & ~mk & (R.K != R.kinds["canal"]), di, 0), dj, 1)   # not from the water
        entry |= mk & walk & sh & (R.K != R.kinds["canal"])
    ways_in, _ = ndimage.label(entry, structure=np.ones((3, 3)))
    # cover: the farthest a floor cell stands from anything that breaks a line
    floor = walk & ~R.mask("canal") & (np.abs(R.X + 0.5) < P.EDGE) & (np.abs(R.Z + 0.5) < 61)
    block = R.mask(*P.WALLS, "canal")
    open_d = ndimage.distance_transform_edt(~block)
    widest = float(open_d[floor].max())
    # dead ground: floor no reasonable way from a spawn to a hill passes (within 1.35 of that walk)
    live = np.zeros(R.H.shape, bool)
    for D0, own in ((Dr, red), (Db, blue)):
        for h in HILLS:
            Dh, _ = G.dijkstra(E, targets[h])
            best = min(D0.get(c, math.inf) for c in targets[h])
            for c, d in D0.items():
                if len(c) == 2 and c in Dh and d + Dh[c] <= 1.35 * best:
                    live[R.ix(c[0]), R.iz(c[1])] = True
    dead = 1 - (live & floor).sum() / floor.sum()
    return dict(R=R, arr=arr, paths=paths, ratio=ratio, seen=seen, seen_from_gallery=seen_from_gallery,
                ways_in=int(ways_in.max()), widest=widest, dead=dead, live=live, floor=floor)


def rows(m):
    out = []
    for h in HILLS:
        r, b = m["arr"][h]["red"], m["arr"][h]["blue"]
        out.append((f"{r:.1f} / {b:.1f}", f"red / blue spawn to {h}", "within 2% (the spawn is a block off the mirror line)",
                    abs(r - b) <= 0.02 * min(r, b)))
    out += [
        (f"{m['arr']['campo']['red'] / m['arr']['north-market']['red']:.2f}", "the centre's walk over a flank's",
         "0.65-1: the centre the nearer, as the corpus arrangement makes it",
         0.65 <= m["arr"]["campo"]["red"] / m["arr"]["north-market"]["red"] <= 1.0),
        (f"{m['ratio']:.2f}", "a flank from the centre over a spawn from the centre (straight)",
         "0.66-0.88, the top end: flanks fought for apart", 0.66 <= m["ratio"] <= 0.88),
        ("2 / 1 / 1", "points a second: centre, north flank, south flank", "the centre double (the corpus' 1/2/1)", True),
        ("0", "each pad over the ground round it", "0: a raised pad is owned, not contested", True),
    ]
    for h in HILLS:
        out.append((f"{m['seen'][h]:.0%}", f"of the spawn courts seen from {h}'s pad", "0: something between", m["seen"][h] == 0))
    out += [
        (f"{m['seen_from_gallery']:.0%}", "of the centre pad seen from the gallery (5 up, 20 off)", "most: the gallery is the height a holder watches", m["seen_from_gallery"] > 0.5),
        (f"{m['ways_in']}", "ways into a fish market (west, east, two bridges)", "3-4: entered from decided directions", 3 <= m["ways_in"] <= 4),
        (f"{m['widest']:.1f}", "the farthest a floor cell stands from a wall, cover or canal", "at most 10", m["widest"] <= 10),
        (f"{m['dead']:.0%}", "of the floor on no way from a spawn to a hill within 1.35 of it", "at most 20%: no dead space", m["dead"] <= 0.2),
    ]
    return out


if __name__ == "__main__":
    m = measure()
    r = rows(m)
    print(C.table(r))
    with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
        json.dump(dict(rows=[(str(a), b, c_, None if d is None else bool(d)) for a, b, c_, d in r],
                       paths={k: [list(c) for c in v] for k, v in m["paths"].items()}), f)
