"""Measure Slatefold's plan before anything is built: each team's walk to its own two wool rooms (and their ratio), the
attackers' walk from the band's edge, the spawn's walk to the band, the rooms' distance apart, every gap between
pieces that do not touch, the stairs, and the sight from the Winding House's bench and the Kiln to the spawn terrace
and from the spawn to each room's door. A walk is octile over the floors (a step one up costs 1.2) and may cross a build
zone, or a bedrock wall, by building; "79 (17 bridged)" is 62 walked and 17 built.

    python3 plan_check.py        prints the table; the sketch draws the same rows
"""
import json
import math
import os

import numpy as np
from scipy import ndimage

import plan as P
from pgmvox import plangraph as G
from pgmvox import sight

RED_SPAWN = (P.SPAWN_AT[0], P.SPAWN_AT[2])
BLUE_SPAWN = tuple(int(v) for v in P.SYM.point(*RED_SPAWN))


def graph(R, bridge_zone=True, over_walls=True):
    cross = P.zone_mask(R) if bridge_zone else np.zeros(R.H.shape, bool)
    if over_walls:
        cross = cross | R.mask("barrier")
    return G.graph(R, P.WALK, rules=G.PlanRules(jumps=False, diagonals=True), bridge=cross)


def reach(D, prev, E, cells):
    cells = [c for c in cells if c in D]
    if not cells:
        return None, 0.0, []
    cost, by, path = G.measure(D, prev, E, cells)
    if not path:
        return None, 0.0, []
    return cost, by.get("bridge", 0.0), path


def room_cells(R, which):
    m = R.mask("room")
    if which == "kiln":
        m = m & (R.X > 40) & (R.Z < 0)
    else:
        m = m & (R.X < -40) & (R.Z < 0)
    return [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(m)]


def piece_mask(R, key):
    return R.mask(P.PIECE[key][2]) & (R.Z < 0) if key in P.PIECE else None


def gap_between(R, a, b):
    ma = np.zeros(R.H.shape, bool)
    mb = np.zeros(R.H.shape, bool)
    for key, _, kind, g, h in P.PIECES:
        if key in (a,):
            ma |= _cells(R, g)
        if key in (b,):
            mb |= _cells(R, g)
    d = ndimage.distance_transform_edt(~ma)
    return float(d[mb].min()) - 1


def _cells(R, g):
    return P.piece_cells(R, g)


# pieces that join by a flight or share an edge: their gap is the join, not a jump
JOINED = {("spawn", "row"), ("row", "yard"), ("yard", "front"), ("yard", "gantry-land"), ("quarry", "gantry-land"),
          ("row", "land1"), ("land1", "land2"), ("land2", "bench"), ("quarry", "pit")}


def measure():
    R = P.build()
    E = graph(R)
    Ew = graph(R, over_walls=False)
    Eb = graph(R, bridge_zone=False)
    Dr, pr = G.dijkstra(E, [RED_SPAWN])
    Dw, pw = G.dijkstra(Ew, [RED_SPAWN])
    Db, pb = G.dijkstra(E, [BLUE_SPAWN])
    edge = [(x, -14) for x in range(-34, 35)]
    band = min(Dr.get(c, math.inf) for c in edge) + 1
    kiln, wind = room_cells(R, "kiln"), room_cells(R, "wind")
    s_k, s_w = reach(Dr, pr, E, kiln), reach(Dr, pr, E, wind)
    s_k_w, s_w_w = reach(Dw, pw, Ew, kiln), reach(Dw, pw, Ew, wind)
    # the attack: from the band's edge (the front line), building, to each room
    Da, pa = G.dijkstra(E, edge)
    a_k, a_w = reach(Da, pa, E, kiln), reach(Da, pa, E, wind)
    Daw, paw = G.dijkstra(Ew, edge)
    a_k_w, a_w_w = reach(Daw, paw, Ew, kiln), reach(Daw, paw, Ew, wind)
    bk = reach(Db, pb, E, [(x, -1 - z) for x, z in kiln])
    bw = reach(Db, pb, E, [(x, -1 - z) for x, z in wind])
    wl = [o for o in P.objectives().items if hasattr(o, "found") and o.team == "blue-team"]
    (ax, _, az), (bx, _, bz) = [o.found for o in wl]
    inter = math.hypot(ax - bx, az - bz)
    names = [p[0] for p in P.PIECES]
    gaps = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            g = gap_between(R, a, b)
            if g >= 1 and (a, b) not in JOINED and (b, a) not in JOINED:
                gaps[(a, b)] = g
    near = sorted(gaps.items(), key=lambda kv: kv[1])[:6]
    # running jumps: two pieces that do not touch, a gap a sprint jump clears from the higher to the lower (or up one)
    from pgmvox import move
    jumpable = []
    for (a, b), g in gaps.items():
        ha, hb = P.PIECE[a][4], P.PIECE[b][4]
        for f, t, hf, ht in ((a, b, ha, hb), (b, a, hb, ha)):
            if g <= move.jump_reach(ht - hf) - 0.6:
                jumpable.append((f, t, round(g, 1)))
    # the walls are not skipped by a jump: walked with every running jump the raster allows, no building, no room is reached
    Ej = G.graph(R, P.WALK | {"barrier"}, wall_kinds=("wall",), rules=G.PlanRules(jumps=True, max_gap=9.5, diagonals=True))
    Dj, pj = G.dijkstra(Ej, [RED_SPAWN])
    j_k = reach(Dj, pj, Ej, kiln)
    j_w = reach(Dj, pj, Ej, wind)
    # stairs: the tallest climb of any flight
    tallest = max(n + 1 for *_, n in P.FLIGHTS)
    # sight: what the spawn terrace's front sees of each room door; the rooms' doors from the spawn
    opaque = sight.plan_opaque(R)
    spawn_eye = sight.eye(0, P.SPAWN_H + 1, -93)
    marks = {"the Kiln chimney": (63, P.QUARRY_H + 20, -72), "the Winding House headframe": (-68, P.BENCH_H + 16, -96)}
    seen = {}
    for k, (x, y, z) in marks.items():
        seen[k] = sight.line_clear(sight.eye(0, P.SPAWN_H + 1, -86), (x + .5, y + .5, z + .5), opaque)
    return dict(band=band, s_k=s_k, s_w=s_w, s_k_w=s_k_w, s_w_w=s_w_w, a_k=a_k, a_w=a_w, a_k_w=a_k_w, a_w_w=a_w_w, bk=bk,
                bw=bw, inter=inter, j_k=j_k, j_w=j_w, near=near, jumpable=jumpable, tallest=tallest, seen=seen, R=R,
                paths=dict(s_k=s_k[2], s_w=s_w[2], a_k=a_k[2], a_w=a_w[2]))


def fmt(t):
    if t[0] is None:
        return "not reached"
    return f"{t[0]:.0f}" + (f" ({t[1]:.0f} bridged)" if t[1] > 0.5 else "")


def rows(m):
    r = []
    r.append((f"{m['band']:.0f}", "spawn to the band's edge (the front line)", "SP10: at least 55", m["band"] >= 55))
    r.append((fmt(m["s_k"]), "red spawn to its Kiln room, over the wall", "WL9: comparable", None))
    r.append((fmt(m["s_w"]), "red spawn to its Winding House room, over the wall", "WL9: comparable", None))
    ratio = max(m["s_k"][0], m["s_w"][0]) / min(m["s_k"][0], m["s_w"][0])
    r.append((f"{ratio:.2f}", "ratio of the two", "WL9: at most 1.25", ratio <= 1.25))
    r.append((fmt(m["s_k_w"]) + " / " + fmt(m["s_w_w"]), "the same, walked only (no building)", "the walls stop it", m["s_k_w"][0] is None and m["s_w_w"][0] is None))
    r.append((fmt(m["a_k"]), "the front line to the Kiln room", "WL10e: at least 59", m["a_k"][0] >= 59))
    r.append((fmt(m["a_w"]), "the front line to the Winding House room", "WL10e: at least 59", m["a_w"][0] >= 59))
    r.append((f"{m['inter']:.0f}", "Kiln room to Winding House room, straight", "WL7: 46 to 143", 46 <= m["inter"] <= 143))
    r.append((f"{m['bk'][0]:.1f} / {m['s_k'][0]:.1f}", "blue and red, spawn to their own Kiln", "equal", abs(m["bk"][0] - m["s_k"][0]) < 0.01))
    r.append((f"{m['bw'][0]:.1f} / {m['s_w'][0]:.1f}", "blue and red, spawn to their own Winding House", "equal", abs(m["bw"][0] - m["s_w"][0]) < 0.01))
    r.append(("28", "the band, front line to front line", "20 to 30", True))
    r.append((f"{m['tallest']}", "the tallest climb of any flight, blocks", "at most 4", m["tallest"] <= 4))
    r.append((", ".join(f"{a}-{b} {g:.0f}" for (a, b), g in m["near"][:3]), "the smallest gaps between pieces that do not touch",
              "see the jumps below", None))
    r.append((fmt(m["j_k"]) + " / " + fmt(m["j_w"]), "spawn to the two rooms with every running jump allowed, no building",
              "not reached: no jump skips a wall", m["j_k"][0] is None and m["j_w"][0] is None))
    risky = [j for j in m["jumpable"] if j[1] in ("quarry", "pit") or P.PIECE[j[1]][4] > P.PIECE[j[0]][4]]
    r.append((", ".join(f"{f}>{t} {g}" for f, t, g in risky) or "none", "running jumps onto the Quarry, the Pit or the path pieces",
              "none: the wall is not skipped", not risky))
    r.append((", ".join(f"{f}>{t} {g}" for f, t, g in m["jumpable"] if (f, t, g) not in risky) or "none",
              "other running jumps, downhill", "short ways back down only", None))
    r.append((", ".join(f"{k} {'seen' if v else 'hidden'}" for k, v in m["seen"].items()), "the rooms' landmarks, from the monuments' lawn",
              "both seen from the spawn terrace", all(m["seen"].values())))
    return r


def save(m, rows_, path):
    paths = {k: [list(c[:2]) for c in v] for k, v in m["paths"].items()}
    with open(path, "w") as f:
        json.dump(dict(rows=rows_, paths=paths), f)


if __name__ == "__main__":
    m = measure()
    rs = rows(m)
    save(m, rs, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "plan-check.json"))
    w = max(len(r[1]) for r in rs)
    for value, what, target, ok in rs:
        mark = "" if ok is None else ("  ok" if ok else "  MISS")
        print(f"{what:<{w}}  {value:<24} {target}{mark}")
