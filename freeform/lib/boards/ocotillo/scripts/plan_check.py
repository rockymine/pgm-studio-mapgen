"""Check Ocotillo's blueprint against its own rules, then measure it.

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


def level_of(c):
    k, lv, d, _ = C.get(c, ("void", None, None, None))
    if k == "stair":
        return None
    return lv if k in ("flat", "keep", "tower", "stacked") else None


# ---- the rules ---------------------------------------------------------------------------------------------
bad_stairs = []
for c, (k, lv, d, _) in C.items():
    if k != "stair":
        continue
    dx, dz = P.STEP[d]
    lo, hi = level_of((c[0] - dx, c[1] - dz)), level_of((c[0] + dx, c[1] + dz))
    if lo is None or hi is None or hi != lo + 1:
        bad_stairs.append((c, lo, hi))


def runs():
    """The longest straight run, in cells, of flat ground at one level (keep and tower floors included)."""
    longest, where = 0, None
    for (cx, cz), (k, lv, _, _) in C.items():
        if k not in ("flat", "keep", "tower"):
            continue
        for dx, dz in ((1, 0), (0, 1)):
            n = 1
            while C.get((cx + dx * n, cz + dz * n), ("",))[0] in ("flat", "keep", "tower") and \
                    C[(cx + dx * n, cz + dz * n)][1] == lv:
                n += 1
            if n > longest:
                longest, where = n, (cx, cz)
    return longest, where


longest, longest_at = runs()
flat_cells = {c for c, v in C.items() if v[0] == "flat"}
sand = sum(1 for c in flat_cells if T[c] == "sand")
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
def room(i):
    x0, z0, x1, z1 = P.tower_box(i)
    return [(x, z) for x in range(x0 + 2, x1 - 1) for z in range(z0 + 2, z1 - 1)]


def reach(D, prev, cells):
    cost, by, path = G.measure(D, prev, E, cells)
    return cost, by.get("bridge", 0.0), path


dais = [(x, z) for x in range(-5, 5) for z in range(-5, 5)]
rows, paths, fair = [], {}, []
names = ["its own", "blue's, its neighbour clockwise", "green's, opposite", "yellow's, its neighbour anticlockwise"]
for team in range(4):
    D, prev = G.dijkstra(E, [spawns[team]])
    got = []
    for j in range(4):
        cost, built, path = reach(D, prev, room((team + j) % 4))
        got.append((round(cost, 1), round(built, 1)))
        if team == 0:
            paths[f"wool{j}"] = path
    cost, built, path = reach(D, prev, dais)
    got.append((round(cost, 1), round(built, 1)))
    if team == 0:
        paths["dais"] = path
    fair.append(got)
same = all(f == fair[0] for f in fair)

for j in range(4):
    cost, built = fair[0][j]
    if j == 0:
        rows.append((f"{cost}", "spawn to its own wool room, the defender's walk", "short: under 40", cost < 40))
    else:
        rows.append((f"{cost}, {built} built", f"spawn to {names[j]} wool room",
                     "46 to 143, the corpus's wool range", 46 <= cost <= 143))
rows.append((f"{fair[0][4][0]}, {fair[0][4][1]} built", "spawn to the dais in the middle", "", True))
rows.append(("yes" if same else "NO", "every team's numbers the same, by the quarter turns", "yes", same))
rows.append((f"{len(bad_stairs)}", "stairs that do not climb one level from low side to high", "0",
             not bad_stairs))
rows.append((f"{longest} cells, {longest * P.CELL} blocks", "the longest straight run at one level",
             "3 cells, 15 blocks", longest <= 3))
rows.append((f"{sand} sand, {inlay} inlay", "flat cells by theme (one cell wide: sand)", "", True))
rows.append((f"{unreached}", "floors not reached from red's spawn, walking and building", "0", unreached == 0))

w = max(len(r[0]) for r in rows)
for v, what, target, ok in rows:
    print(f"{what:<62} {v:<{w}}  {target:<38} {'ok' if ok else 'NO'}")
if bad_stairs:
    print("bad stairs:", bad_stairs[:8])
if longest > 3:
    print("longest run starts at cell", longest_at)
with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
    json.dump({"rows": rows, "paths": {k: [list(p)[:2] for p in v] for k, v in paths.items()}}, f)
