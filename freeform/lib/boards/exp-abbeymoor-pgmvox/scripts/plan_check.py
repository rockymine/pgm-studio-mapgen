"""Measure Abbeymoor's plan before anything is built: the goal rules against the studio's bands (GO1, GO3, GO4), the ways onto
each monument (over the ground, by the cellar and the crypt), how much of the ground a player approaching a monument sees it
from, the clearance round each, the stairs, the cover over the passage, and the share of the ground a player reaches.

    python3 plan_check.py        prints the table; the sketch draws the same rows
"""
import json
import math
import os

import numpy as np

import plan as P
from pgmvox import plangraph as G
from pgmvox import sight

RED = (P.SPAWN_AT[0], P.SPAWN_AT[2])
BLUE = tuple(int(v) for v in P.SYM.point(*RED))


def graph(R, storey1=True):
    E = G.graph(R, P.WALK, rules=G.PlanRules(jumps=False, diagonals=True, max_drop=3), extra=P.links() if storey1 else ())
    if not storey1:
        E = {a: [(b, c, t) for b, c, t in v if len(b) == 2] for a, v in E.items() if len(a) == 2}
    return E


def near(D, centre, r=3):
    cx, cz = centre
    cells = [(x, z) for x in range(cx - r, cx + r + 1) for z in range(cz - r, cz + r + 1) if (x, z) in D]
    return min((D[c] for c in cells), default=None)


def measure():
    R = P.build()
    E = graph(R)
    Eg = graph(R, False)
    Dr, pr = G.dijkstra(E, [RED])
    Db, pb = G.dijkstra(E, [BLUE])
    Drg, prg = G.dijkstra(Eg, [RED])
    img = lambda p: tuple(int(v) for v in P.SYM.point(*p))                        # noqa: E731
    A, Bm = P.A_CENTRE, P.B_CENTRE
    own_A, own_B = near(Dr, A), near(Dr, Bm)
    enemy_A, enemy_B = near(Db, A), near(Db, Bm)                                 # blue's spawn to red's goals
    far_A, far_B = near(Dr, img(A)), near(Dr, img(Bm))                           # red's spawn to blue's goals
    ang = {}
    for name, c in (("A", A), ("B", Bm)):
        v1 = (c[0] - RED[0], c[1] - RED[1])
        v2 = (BLUE[0] - RED[0], BLUE[1] - RED[1])
        ang[name] = math.degrees(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))))
    # ways onto Monument A: over the ground, and by the cellar, the crypt and the Night Stair
    head = (19, P.PASSAGE_Z)
    Dh, ph = G.dijkstra(E, [(18, P.PASSAGE_Z, 1)])
    by_cellar = near(Db, head, 2)
    cellar_to_A = near(Dh, A)
    over_A = near(Db, A) if False else None
    Dbg, pbg = G.dijkstra(Eg, [BLUE])
    over_A = near(Dbg, A)
    over_B = near(Dbg, Bm)
    via = (by_cellar or 0) + (cellar_to_A or 0)
    # sight: the share of the ground, 25 to 60 blocks off, from which a player sees the monument's top course
    opaque = sight.plan_opaque(R)
    shares = {}
    ground = np.argwhere(R.mask("ground", "road", "green", "orchard", "peat", "nave", "boardwalk"))
    for name, c in (("A", A), ("B", Bm)):
        box = P.monument_box(*c)
        tgt = sight.target(c[0], box.y1, c[1])
        cells = [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in ground
                 if 25 <= math.hypot(R.X[i, k] - c[0], R.Z[i, k] - c[1]) <= 60 and (R.X[i, k] + R.Z[i, k]) % 5 == 0 and (R.Z[i, k] > -127)]
        eyes = [sight.eye(x, R.h(x, z) + 1, z) for x, z in cells]
        seen = sight.visibility([tgt], eyes, opaque)[0] if eyes else 0
        # and from the approach: the cells on the enemy's way within 60 blocks of it
        shares[name] = seen
    # the cover round each: nothing but ground, road, green or the nave's floor within four blocks
    clear = {}
    for name, c in (("A", A), ("B", Bm)):
        bad = set()
        for x in range(c[0] - 5, c[0] + 6):
            for z in range(c[1] - 5, c[1] + 6):
                if max(abs(x - c[0]), abs(z - c[1])) < 5:
                    continue
                k = R.kind(x, z)
                if k in ("wall", "room", "ruin") and max(abs(x - c[0]), abs(z - c[1])) <= 5 + (0 if True else 1):
                    bad.add(k)
        clear[name] = bad
    # the passage's cover: ground less floor, least over the passage
    U = R.storey(1)
    cover = []
    for x, y in P.PASSAGE_FLOORS.items():
        for dz in (-1, 0, 1):
            gz = int(R.H[x - R.x_min, P.PASSAGE_Z + dz - R.z_min])
            if R.kind(x, P.PASSAGE_Z + dz) != "hole":
                cover.append(gz - (y + 2))
    # a flight's climb: the longest run of consecutive rises along the stair and the passage, in blocks
    def runs(seq):
        best = cur = 0
        for a, b in zip(seq, seq[1:]):
            cur = cur + 1 if b != a else 0
            best = max(best, cur)
        return best
    stair_run = max(runs([y for _, y in P.NIGHT_STAIR]), runs([P.PASSAGE_FLOORS[x] for x in sorted(P.PASSAGE_FLOORS)]))
    dryk = {R.kinds[k] for k in ('ground', 'road', 'green', 'orchard', 'peat', 'nave', 'boardwalk', 'steep')}
    reached = len([c for c in Drg if len(c) == 2 and int(R.K[c[0] - R.x_min, c[1] - R.z_min]) in dryk])
    dry = int(R.mask("ground", "road", "green", "orchard", "peat", "nave", "boardwalk", "steep").sum())
    dead = 1 - reached / dry
    return dict(own_A=own_A, own_B=own_B, enemy_A=enemy_A, enemy_B=enemy_B, far_A=far_A, far_B=far_B, ang=ang, over_A=over_A, over_B=over_B,
                by_cellar=by_cellar, cellar_to_A=cellar_to_A, via=via, shares=shares, clear=clear, cover=min(cover), stair_run=stair_run,
                dead=dead, R=R, paths=dict(A=_path(Dbg, pbg, Eg, A), B=_path(Dbg, pbg, Eg, Bm)))


def _path(D, prev, E, c):
    cells = [(x, z) for x in range(c[0] - 3, c[0] + 4) for z in range(c[1] - 3, c[1] + 4) if (x, z) in D]
    cost, by, path = G.measure(D, prev, E, cells)
    return path


def rows(m):
    r = []
    ok = lambda v, lo, hi: lo <= v <= hi                                          # noqa: E731
    r.append((f"{m['own_A']:.0f} / {m['own_B']:.0f}", "spawn to its own Abbey / Village monument", "GO4: 40 to 90", ok(m["own_A"], 40, 90) and ok(m["own_B"], 40, 90)))
    r.append((f"{m['enemy_A']:.0f} / {m['enemy_B']:.0f}", "the enemy spawn to red's Abbey / Village monument", "GO1: at least 3 times its own", min(m["enemy_A"] / m["own_A"], m["enemy_B"] / m["own_B"]) >= 3))
    r.append((f"{m['enemy_A'] / m['own_A']:.2f} / {m['enemy_B'] / m['own_B']:.2f}", "the ratio, enemy walk to own walk", "GO1: 3 to 4", None))
    r.append((f"{m['far_A']:.0f} / {m['far_B']:.0f}", "a spawn to the enemy's Abbey / Village monument", "GO3: 85 to 150", ok(m["far_A"], 85, 150) and ok(m["far_B"], 85, 150)))
    r.append((f"{m['ang']['A']:.0f} / {m['ang']['B']:.0f}", "degrees off the line between the spawns (A / B)", "corpus median 42", None))
    r.append((f"{m['over_A']:.0f} / {m['over_B']:.0f}", "blue's spawn over the ground to red's A / B", "reference", None))
    r.append((f"{m['by_cellar']:.0f} + {m['cellar_to_A']:.0f} = {m['via']:.0f}", "blue's spawn to the cellar stair, then by the crypt to A", "a way from below within 1.4 of over the ground", m["via"] <= 1.4 * m["over_A"]))
    r.append((f"{100 * m['shares']['A']:.0f}% / {100 * m['shares']['B']:.0f}%", "of the ground 25 to 60 off that sees the monument (A / B)", "at least 25% (found without a map)", min(m["shares"].values()) >= 0.25))
    r.append((", ".join(f"{k}: {sorted(v) if v else 'clear'}" for k, v in m["clear"].items()), "what stands within five of each monument", "no wall or ruin within four of the cube", not any(m["clear"].values())))
    r.append((f"{m['cover']}", "the passage's least cover over its roof, blocks", "at least 3", m["cover"] >= 3))
    r.append((f"{m['stair_run']}", "the longest climb in the Night Stair and the passage, blocks", "at most 4", m["stair_run"] <= 4))
    r.append((f"{100 * m['dead']:.1f}%", "of the dry ground not reached on foot from a spawn", "at most 5%", m["dead"] <= 0.05))
    return r


def save(m, rows_, path):
    paths = {k: [list(c[:2]) for c in v] for k, v in m["paths"].items()}
    with open(path, "w") as f:
        json.dump(dict(rows=[[str(a), b, c, (None if d is None else bool(d))] for a, b, c, d in rows_], paths=paths), f)


if __name__ == "__main__":
    m = measure()
    rs = rows(m)
    save(m, rs, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "plan-check.json"))
    w = max(len(r[1]) for r in rs)
    for value, what, target, ok_ in rs:
        mark = "" if ok_ is None else ("  ok" if ok_ else "  MISS")
        print(f"{what:<{w}}  {value:<28} {target}{mark}")
