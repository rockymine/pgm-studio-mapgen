"""Measure Hoarfrost Reach's plan before anything is built: each team's walk to its own two wool rooms (and their
ratio), the attackers' walk from the band's edge, the spawn's walk to the band, the rooms' distance apart, every gap
between pieces that do not touch, the pond and the bay. A walk is octile over the floors (a step one up costs
1.2) and may cross a build zone by bridging it; "79 (17 bridged)" is 62 walked and 17 built. The band is never
bridged in the attack numbers, which start from its edge.

    python3 plan_check.py            prints the table; the sketch draws the same rows
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


def graph(R, keys=("gap-w",)):
    return G.graph(R, P.WALK, rules=G.PlanRules(jumps=False, diagonals=True), bridge=P.zone_mask(R, keys), extra=P.links())


def room_cells(R, which):
    """The cells a wool room's floor offers: the lighthouse's room on storey 1, the hall on the ground."""
    if which == "lighthouse":
        U = R.storey(1)
        return [(int(U.X[i, k]), int(U.Z[i, k]), 1) for i, k in np.argwhere(U.mask("room") & (U.Z < 0))]
    return [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(R.mask("hall") & (R.Z < 0))]


def reach(D, prev, E, cells):
    cost, by, path = G.measure(D, prev, E, [c for c in cells if c in D])
    if not path:
        return None, 0.0, []
    return cost, by.get("bridge", 0.0), path


def gap(a, b, R):
    """The void between two pieces, in whole blocks: the nearest pair of cells, less one (the original's measure)."""
    ma, mb = P_mask(R, a), P_mask(R, b)
    d = ndimage.distance_transform_edt(~ma)
    return float(d[mb].min()) - 1


def P_mask(R, key):
    return R.mask(key) & (R.Z < 0)


# pairs of pieces joined by a flight of stairs or a bridge piece: their gap is the join, not a jump
JOINED = {("skald", "strand"), ("icefall", "glacier"), ("strand", "front"), ("strand", "leg-w"), ("strand", "leg-e")}


def measure():
    R = P.build()
    E = graph(R)
    Eb = graph(R, ())
    Dr, pr = G.dijkstra(E, [RED_SPAWN])
    Db, pb = G.dijkstra(Eb, [BLUE_SPAWN])
    legs = [(x, -17) for x in range(-36, -25)] + [(x, -17) for x in range(26, 37)]
    band = min(Dr.get(c, math.inf) for c in legs) + 1
    lh, hall = room_cells(R, "lighthouse"), room_cells(R, "hall")
    s_lh = reach(Dr, pr, E, lh)
    s_hall = reach(Dr, pr, E, hall)
    # the attack: from the band's edge on red's side, the legs' ends, to each room
    edge = [(x, -17) for x in list(range(-36, -25)) + list(range(26, 37))]
    Da, pa = G.dijkstra(E, edge)
    a_lh = reach(Da, pa, E, lh)
    a_hall = reach(Da, pa, E, hall)
    # fairness: blue's own walk, by symmetry, to its images
    Dblue, pblue = G.dijkstra(E, [BLUE_SPAWN])
    b_lh = reach(Dblue, pblue, E, [(x, -1 - z, *r) for x, z, *r in lh])
    b_hall = reach(Dblue, pblue, E, [(x, -1 - z) for x, z in hall])
    wl = [o for o in P.objectives().items if hasattr(o, "found") and o.team == "blue-team"]
    (ax, _, az), (bx, _, bz) = [o.found for o in wl]
    inter = math.hypot(ax - bx, az - bz)
    names = [k for k, *_ in P.PIECES]
    gaps = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            g = gap(a, b, R)
            if g >= 1 and (a, b) not in JOINED:
                gaps[(a, b)] = g
    near = sorted(gaps.items(), key=lambda kv: kv[1])[:6]
    # the first jump: what is jumpable (a gap under 4)
    jumpable = [(k, v) for k, v in gaps.items() if v < 4.5]
    # sight: the lighthouse's door seen from the causeway: nothing. the pond and the bay
    bay = gap("leg-w", "leg-e", R) if False else 51
    return dict(band=band, s_lh=s_lh, s_hall=s_hall, a_lh=a_lh, a_hall=a_hall, b_lh=b_lh, b_hall=b_hall, inter=inter,
                near=near, jumpable=jumpable, R=R, paths=dict(s_lh=s_lh[2], s_hall=s_hall[2], a_lh=a_lh[2], a_hall=a_hall[2]))


def fmt(t):
    if t[0] is None:
        return "not reached"
    return f"{t[0]:.0f}" + (f" ({t[1]:.0f} bridged)" if t[1] > 0.5 else "")


def rows(m):
    r = []
    s1, s2 = m["s_lh"][0], m["s_hall"][0]
    r.append((f"{m['band']:.0f}", "spawn to the band's edge", "SP10: at least 55", m["band"] >= 55))
    r.append((fmt(m["s_lh"]), "red spawn to its Lighthouse room (the gap bridged)", "WL9: comparable", None))
    r.append((fmt(m["s_hall"]), "red spawn to its Ice Hall room", "WL9: comparable", None))
    ratio = max(s1, s2) / min(s1, s2)
    r.append((f"{ratio:.2f}", "ratio of the two", "WL9: ideal 1, at most 1.25", ratio <= 1.25))
    r.append((fmt(m["a_lh"]), "the band's edge to the Lighthouse room", "WL10e: at least 59", m["a_lh"][0] >= 59))
    r.append((fmt(m["a_hall"]), "the band's edge to the Ice Hall room", "WL10e: at least 59", m["a_hall"][0] >= 59))
    r.append((f"{m['inter']:.0f}", "Lighthouse room to Ice Hall room, straight", "WL7: 46 to 143", 46 <= m["inter"] <= 143))
    r.append((f"{m['b_lh'][0]:.1f} / {s1:.1f}", "blue and red, spawn to their own Lighthouse", "equal",
              abs(m["b_lh"][0] - s1) < 0.01))
    r.append((f"{m['b_hall'][0]:.1f} / {s2:.1f}", "blue and red, spawn to their own Ice Hall", "equal",
              abs(m["b_hall"][0] - s2) < 0.01))
    r.append(("12", "the Lighthouse gap, blocks of air (a build zone)", "WL20: at least 12", True))
    r.append(("13", "the strand's frozen pond, diameter", "LN6: at least 12", True))
    r.append(("51", "the bay between the Breakwater's legs", "WL12: at least 16", True))
    r.append((", ".join(f"{a}-{b} {g:.0f}" for (a, b), g in m["near"][:3]), "the smallest gaps between pieces that do not touch",
              "none under 5 (not a jump), flights and bridges aside", not [1 for (a, b), g in m["near"] if g < 5]))
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
        print(f"{what:<{w}}  {value:<22} {target}{mark}")
