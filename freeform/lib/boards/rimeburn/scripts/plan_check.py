"""Check Rimeburn's plan before a block is written: each team's walks to its own goals and the enemy's, the
studio's goal rules against them, the bridging the seam asks, and the ground nobody can reach.

    GO4  a goal's own spawn is 40 to 90 blocks of walk away
    GO1  the nearest enemy spawn is 3 to 4 times the walk to its own
    GO3  a spawn reaches an enemy goal in 85 to 150
"""
import json
import math
import os

import numpy as np

import plan as P
from pgmvox.plan import graph as G
from pgmvox.play.objectives import Core, Destroyable, Spawn

R = P.build()
SEAM = R.mask("seam")
E = G.graph(R, P.WALK, wall_kinds={"wall"}, rules=G.PlanRules(diagonals=True), bridge=SEAM,
            extra=P.vent_extra(R))
O = P.objectives()
spawns = {s.team: [(s.at[0], s.at[2])] for s in O.of(Spawn)}
goals = [g for g in O.items if isinstance(g, (Core, Destroyable))]
D = {t: G.dijkstra(E, cells) for t, cells in spawns.items()}

rows = []


def row(value, what, target, ok):
    rows.append((value, what, target, ok))
    mark = "" if ok is None else ("ok" if ok else "MISS")
    print(f"{value:>10}  {what:<58} {target:<16} {mark}")


print("Rimeburn plan check\n")
for g in goals:
    cells = P.goal_cells(g.box)
    own = g.team
    enemy = P.TEAMS.other(own)
    d_own, by_own, _ = G.measure(*D[own], E, cells)
    d_en, by_en, _ = G.measure(*D[enemy], E, cells)
    bridged = by_en.get("bridge", 0)
    row(f"{d_own:.0f}", f"{g.name}: walk from its own spawn", "GO4 40-90", 40 <= d_own <= 90)
    row(f"{d_en:.0f}", f"{g.name}: walk from the enemy spawn ({bridged:.0f} bridged)", "GO3 85-150",
        85 <= d_en <= 150)
    row(f"{d_en / d_own:.2f}", f"{g.name}: enemy walk over own", "GO1 3-4", 3 <= d_en / d_own <= 4)
    sx, sz = spawns[own][0]
    ex, ez = spawns[enemy][0]
    gx, gz = g.box.centre()
    a = math.degrees(abs(math.atan2(gx - sx, gz - sz) - math.atan2(ex - sx, ez - sz)))
    a = min(a, 360 - a)
    row(f"{a:.0f}", f"{g.name}: degrees off the line between the spawns", "corpus median 42", a >= 25)

# the same walks for both teams, by symmetry
for g in goals[::2]:
    other = [h for h in goals if h is not g and type(h) is type(g)][0]
    a = G.measure(*D[g.team], E, P.goal_cells(g.box))[0]
    b = G.measure(*D[other.team], E, P.goal_cells(other.box))[0]
    row(f"{abs(a - b):.1f}", f"{type(g).__name__}: Frost's walk less Ember's to their own", "0", abs(a - b) < 0.5)

# the crossings: the shortest bridge from one land to the other, and at the Thaw
land = R.mask("ground", "water", "stair")
X, Z = R.X, R.Z
north = land & (Z < 0) & (Z > -40) & ~((abs(X) < 24) & (abs(Z) < 12))
south = land & (Z >= 0) & (Z < 40) & ~((abs(X) < 24) & (abs(Z) < 12))
thaw = land & (abs(X) < 24) & (abs(Z) < 12)


def gap(a, b):
    pa = np.argwhere(a)
    pb = np.argwhere(b)
    best = math.inf
    for i, k in pa[:: 3]:
        d = np.hypot(pb[:, 0] - i, pb[:, 1] - k).min()
        best = min(best, d)
    return best - 1


g1 = gap(north, south)
g2 = gap(north, thaw)
row(f"{g1:.0f}", "the narrowest bridge straight across the seam", "at least 16", g1 >= 16)
row(f"{g2:.0f}", "the narrowest bridge from a land to the Thaw", "8 to 16", 8 <= g2 <= 16)

# every dry column reached from a spawn
Dn, _ = D["frost-team"]
reached = np.zeros(R.H.shape, bool)
for node_ in Dn:
    x, z = node_[0], node_[1]
    reached[R.ix(x), R.iz(z)] = True
walkable = R.mask(*P.WALK) & (R.H < 56)              # the Rimewall's crest above 56 frames the board, unplayed
cut = int((walkable & ~reached).sum())
row(f"{100 * cut / walkable.sum():.1f}%", "ground under y 56 no spawn reaches", "at most 2%", cut / walkable.sum() <= 0.02)
row(int(land.sum()), "columns of land", "less than 20,000 (void board)", land.sum() < 20000)

os.makedirs(os.path.join("..", "renders"), exist_ok=True)
with open(os.path.join("..", "renders", "plan-check.json"), "w") as f:
    json.dump([[str(v), w, t, None if o is None else bool(o)] for v, w, t, o in rows], f, indent=1)
