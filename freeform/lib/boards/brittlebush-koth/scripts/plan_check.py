"""Check Brittlebush KotH's blueprint against its own rules, then measure the walks to its hills.

The rules: every stair climbs one level from the cell on its low side to the cell on its high side; no flat piece
runs more than three cells, fifteen blocks, at one level; a piece one cell wide is sand and one with two cells by
two in it is inlay; every floor is reached from every spawn, walking and building over the gaps.

The walk is octile over the floors (a step up costs 1.2) and may cross a gap by building over it, block for block.
Every number is red's; the board is the same for every team by its quarter turns, and the check says so.

    python3 plan_check.py            prints the table, and writes plan-check.json beside it for the sketch
"""
import json
import math
import os

import plan as P  # noqa: F401  (puts the library on the path)

import numpy as np

from pgmvox import plangraph as G

HERE = os.path.dirname(os.path.abspath(__file__))
R = P.plan()
C = R.cells
T = R.themes


def levels_of(c):
    """The floors a cell offers: its level, and a stacked cell's underfloor one under it."""
    k, lv, d, _ = C.get(c, ("void", None, None, None))
    if k in ("flat", "keep", "tower"):
        return {lv}
    return {lv, lv - 1} if k == "stacked" else set()


# ---- the rules ---------------------------------------------------------------------------------------------
bad_stairs, narrow_stairs = [], []
for c, (k, lv, d, _) in C.items():
    if k != "stair":
        continue
    dx, dz = P.STEP[d]
    if lv not in levels_of((c[0] - dx, c[1] - dz)) or lv + 1 not in levels_of((c[0] + dx, c[1] + dz)):
        bad_stairs.append((c, d, lv))
    side = [(c[0] + dz, c[1] + dx), (c[0] - dz, c[1] - dx)]                # the cells beside it, across the rise
    if not any(C.get(s, ("",))[0] == "stair" and C[s][2] == d and C[s][1] == lv for s in side):
        narrow_stairs.append(c)


def runs():
    """The longest straight run, in cells, of flat ground at one level (the keep included; the tower is a
    building, not ground)."""
    longest, where = 0, None
    for (cx, cz), (k, lv, _, _) in C.items():
        if k not in ("flat", "keep"):
            continue
        for dx, dz in ((1, 0), (0, 1)):
            n = 1
            while C.get((cx + dx * n, cz + dz * n), ("",))[0] in ("flat", "keep") and \
                    C[(cx + dx * n, cz + dz * n)][1] == lv:
                n += 1
            if n > longest:
                longest, where = n, (cx, cz)
    return longest, where


longest, longest_at = runs()
flat_cells = {c for c, v in C.items() if v[0] == "flat"}
sand = sum(1 for c in flat_cells if T[c] == "sand")
narrow = [c for c in flat_cells if T[c] == "sand"]
inlay = sum(1 for c in flat_cells if T[c] == "inlay")

gap = R.mask("gap")
E = G.graph(R, P.WALK_KINDS, rules=G.PlanRules(jumps=False, diagonals=True), bridge=gap)
spawns = [P.spawn_cell(i) for i in range(4)]
D0, prev0 = G.dijkstra(E, [spawns[0]])
walk = G.walkable(R, P.WALK_KINDS)
unreached = 0
for s, L in enumerate(R.storeys):
    for i, k in np.argwhere(walk[s]):
        if G.node(R, R.X[i, k], R.Z[i, k], s) not in D0:
            unreached += 1


# ---- the numbers -------------------------------------------------------------------------------------------
E_foot = G.graph(R, P.WALK_KINDS, rules=G.PlanRules(jumps=False, diagonals=True))


def pad(box):
    x0, z0, x1, z1 = box
    return [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]


def near(pt, r=2):
    """The blocks within r of a point, the same on either side of it when it lies between two blocks."""
    def span(v):
        return range(math.floor(v) - r + 1, math.ceil(v) + r) if v != int(v) else range(int(v) - r, int(v) + r + 1)
    return [(a, b) for a in span(pt[0]) for b in span(pt[1])]


def reach(E, D, prev, cells):
    cost, by, path = G.measure(D, prev, E, cells)
    return round(cost, 1), round(by.get("bridge", 0.0), 1), path


hills = {hid: pad(box) for hid, _, box, _, _ in P.HILLS}
order = ["north", "east", "south", "west"]
rows, paths, fair = [], {}, []
for team in range(4):
    D, prev = G.dijkstra(E, [spawns[team]])
    Df, prevf = G.dijkstra(E_foot, [spawns[team]])
    near_two = [order[team], order[(team + 3) % 4]]                     # the borders either side of its quadrant
    far_two = [order[(team + 1) % 4], order[(team + 2) % 4]]
    got = {"centre": reach(E_foot, Df, prevf, hills["centre"])}
    for k, hid in enumerate(near_two + far_two):
        got[f"{'near' if k < 2 else 'far'}{k % 2}"] = reach(E_foot, Df, prevf, hills[hid])
    got["apples"] = reach(E, D, prev, [c for p in P.APPLES for c in near(p)])
    got["arrows"] = reach(E_foot, Df, prevf, [c for p in P.ARROWS for c in near(p)])
    if team == 0:
        paths = {k: v[2] for k, v in got.items()}
    fair.append({k: v[:2] for k, v in got.items()})
same = all(f == fair[0] for f in fair)
f = fair[0]
spawn_r = (spawns[0][0] ** 2 + spawns[0][1] ** 2) ** 0.5
hill_r = 58.5
rows += [
    (f"{f['centre'][0]}", "spawn to the middle hill, the Dais, on foot", "", f["centre"][0] < 1e9),
    (f"{f['near0'][0]}, {f['near1'][0]}", "spawn to the two border hills beside it, on foot", "the same",
     f["near0"][0] == f["near1"][0] < 1e9),
    (f"{f['far0'][0]}, {f['far1'][0]}", "spawn to the two border hills beyond, on foot", "", f["far0"][0] < 1e9),
    (f"{hill_r / spawn_r:.2f}", "a border hill's distance from the middle, over a spawn's",
     "0.52 to 0.99, the four-team corpus", 0.52 <= hill_r / spawn_r <= 0.99),
    (f"{f['apples'][0]}, {f['apples'][1]} built", "spawn to the nearest golden apples, on an inner island", "", True),
    (f"{f['arrows'][0]}", "spawn to the nearest arrows, on a landing, on foot", "", True),
    ("yes" if same else "NO", "every team's numbers the same, by the quarter turns", "yes", same),
    (f"{len(bad_stairs)}", "stairs that do not climb one level from low side to high", "0", not bad_stairs),
    (f"{len(narrow_stairs)}", "stairs narrower than two cells", "0", not narrow_stairs),
    (f"{longest} cells, {longest * P.CELL} blocks", "the longest straight run at one level", "3 cells, 15 blocks",
     longest <= 3),
    (f"{sand} sand, {inlay} inlay", "flat cells by theme (one cell wide: sand)", "", True),
    (f"{unreached}", "floors not reached from red's spawn, walking and building", "0", unreached == 0),
]
w = max(len(r[0]) for r in rows)
for v, what, target, ok in rows:
    print(f"{what:<62} {v:<{w}}  {target:<38} {'ok' if ok else 'NO'}")
if not same:
    for t, f_ in enumerate(fair):
        print("team", t, f_)
if bad_stairs:
    print("bad stairs:", bad_stairs[:8])
if narrow_stairs:
    print("narrow stairs:", narrow_stairs[:8])
if longest > 3:
    print("longest run starts at cell", longest_at)
with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
    json.dump({"rows": rows, "paths": {k: [list(p)[:2] for p in v] for k, v in paths.items()}}, f)
