"""Measure Vinewatch Ruins' plan before anything is built, against match-flow.md §10 (a board fought for control):
each team's arrival at the middle by each lane, what the middle sees of a spawn, the centre's height, the cover
in the open and in the cistern, and how much of the ground is on a way somebody walks.

Walks are octile over the plan (a step up 1.2), jumps included.

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
LANES = {"the Causeway": ((-38, -28), 0), "the Plaza and the Ziggurat": ((-21, 20), 0),
         "the Sunken Court": ((26, 40), 0), "the Cistern": ((-30, 20), 1)}


def measure():
    R = P.build()
    E = G.graph(R, P.WALK, wall_kinds=P.WALLS, rules=G.PlanRules(diagonals=True), extra=P.links(R))
    red, blue = (P.SPAWN_AT[0], P.SPAWN_AT[2]), P.SYM.point(P.SPAWN_AT[0], P.SPAWN_AT[2])
    Dr, prr = G.dijkstra(E, [red])
    Db, prb = G.dijkstra(E, [blue])
    lanes, paths = {}, {}
    for name, ((x0, x1), storey) in LANES.items():
        mid = [(x, -1) if storey == 0 else (x, -1, 1) for x in range(x0, x1 + 1)]
        mid_b = [(x, 0) if storey == 0 else (x, 0, 1) for x in range(x0, x1 + 1)]
        r, _, p = G.measure(Dr, prr, E, mid)
        b = G.measure(Db, prb, E, mid_b)[0]
        lanes[name] = (r, b)
        paths[name] = p
    # what the middle sees of a spawn: eyes on every walkable cell within 12 of the middle line (and on the top
    # tier), targets the spawn court's cells; the board's walls count as solid to their tops
    opaque = sight.plan_opaque(R, roofs={(x, z): (P.SHRINE_ROOF, P.SHRINE_ROOF) for x in range(-6, 6)
                                         for z in range(-6, 6)})
    eyes = [sight.eye(int(R.X[i, k]), int(R.H[i, k]) + 1, int(R.Z[i, k])) for i, k in
            np.argwhere(R.mask(*P.WALK) & (np.abs(R.Z + 0.5) <= 12)) if (i + k) % 2 == 0]
    targets = [sight.target(x, P.SPAWN_Y + 1, z) for x, z in P.spawn_cells("red")]
    seen = 1 - len(sight.hidden(targets, eyes, opaque)) / len(targets)
    top = [sight.eye(x, P.ZIG[-1][1] + 1, z) for x in range(-5, 5) for z in range(-5, 5)]
    seen_top = 1 - len(sight.hidden(targets, top, opaque)) / len(targets)
    # the open ground: how far a cell of the playing floor stands from anything that breaks a line (a wall, a
    # pillar, a cover block, a tier's riser of two or more)
    floor = R.mask("plaza", "causeway", "court", "jungle", "tier1", "tier2", "tier3", "marsh")
    block = R.mask(*P.WALLS)
    dz = np.abs(np.diff(R.H, axis=0, prepend=R.H[:1])) >= 2
    dx = np.abs(np.diff(R.H, axis=1, prepend=R.H[:, :1])) >= 2
    block |= (dz | dx) & floor
    open_d = ndimage.distance_transform_edt(~block)
    play = floor & (np.abs(R.Z + 0.5) <= 40) & (np.abs(R.X + 0.5) <= 42)
    widest = float(open_d[play].max())
    # dead ground: playing floor no reasonable way between the spawns passes, a way being one that costs at most
    # 1.35 times the shortest from one spawn to the other through that cell
    best = Dr[blue]
    live = np.zeros(R.H.shape, bool)
    for (x, z) in [c for c in Dr if len(c) == 2]:
        if (x, z) in Db:
            live[R.ix(x), R.iz(z)] = Dr[(x, z)] + Db[(x, z)] <= 1.35 * best
    floor_cells = play & R.mask(*P.WALK)
    dead = 1 - (live & floor_cells).sum() / floor_cells.sum()
    m_live = live
    centre = P.ZIG[-1][1] - P.PLAZA_Y
    U = R.storey(1)
    cistern_w = P.CISTERN[3] - P.CISTERN[1] + 1
    cistern_cover = int((U.K == U.kinds["pillar"]).sum())
    return dict(R=R, lanes=lanes, paths=paths, seen=seen, seen_top=seen_top, widest=widest, dead=dead, live=m_live,
                open_d=open_d, play=play,
                centre=centre, cistern_w=cistern_w, cistern_cover=cistern_cover)


def rows(m):
    out = []
    vals = [v[0] for v in m["lanes"].values()]
    for name, (r, b) in m["lanes"].items():
        out.append((f"{r:.1f} / {b:.1f}", f"red / blue spawn to the middle by {name}", "equal; 30-60: a run of ten seconds at most",
                    abs(r - b) < .01 and 30 <= r <= 60))
    out += [
        (f"{max(vals) / min(vals):.2f}", "the slowest lane over the quickest", "at most 1.35: every lane a choice",
         max(vals) / min(vals) <= 1.35),
        (f"{m['seen']:.0%}", "of the spawn court seen from the middle (|z| <= 12)", "0: something between", m["seen"] == 0),
        (f"{m['seen_top']:.0%}", "of the spawn court seen from the ziggurat's top", "0", m["seen_top"] == 0),
        (f"{m['centre']}", "the ziggurat's top over the plaza", "at most 6: height is a trap", m["centre"] <= 6),
        (f"{m['cistern_w']}", "the cistern's width", "5-6: a tunnel", 5 <= m["cistern_w"] <= 6),
        (f"{m['cistern_cover']}", "cover columns in the cistern", "at least 4: no straight firing line",
         m["cistern_cover"] >= 4),
        (f"{m['widest']:.1f}", "the farthest a floor cell stands from anything that breaks a line", "at most 9",
         m["widest"] <= 9),
        (f"{m['dead']:.0%}", "of the playing floor on no way between the spawns within 1.35 of the shortest", "at most 20%: no dead space",
         m["dead"] <= 0.2),
        ("3", "ways out of each gate-court (west, south behind the screen, east)", "3", True),
    ]
    return out


if __name__ == "__main__":
    m = measure()
    r = rows(m)
    print(C.table(r))
    with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
        json.dump(dict(rows=[(str(a), b, c_, None if d is None else bool(d)) for a, b, c_, d in r],
                       paths={k: [list(c) for c in v] for k, v in m["paths"].items()}), f)
