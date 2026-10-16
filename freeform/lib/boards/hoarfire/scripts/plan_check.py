"""Check Hoarfire's plan before a block is written: each team's walk from its spawn to its own goals and to the
enemy's (the Rift crossed by building, the Ice Cave walked), the ratios a destroy board is held to, the Rift's
narrowest crossing, the widest jump, and that every place is reached.

    python3 plan_check.py > ../renders/plan-check.txt
"""
import math

import numpy as np

import plan as P
from pgmvox.plan import graph as G

R = P.build()
E = G.graph(R, P.WALK, wall_kinds={"wall"}, rules=G.PlanRules(diagonals=True, max_drop=6, drop_cost=2.0),
            bridge=P.rift_mask(R), extra=P.cave_edges())
J = G.jumps(R, P.WALK, {"wall"})
SPAWNS = {"red": [(P.SPAWN_AT[0], P.SPAWN_AT[2])], "blue": [P.SYM.point(P.SPAWN_AT[0], P.SPAWN_AT[2])]}


def around(box, r):
    cells = []
    for x in range(box.x0 - r, box.x1 + r + 1):
        for z in range(box.z0 - r, box.z1 + r + 1):
            if R.inside(x, z) and R.kind(x, z) in P.WALK:
                cells.append((x, z))
    return cells


def image(cells):
    return [P.SYM.point(x, z) for x, z in cells]


MON = around(P.MONUMENT_BOX, 2)
CORE = around(P.CORE_BOX, 3)
D = {t: G.dijkstra(E, s) for t, s in SPAWNS.items()}


def walk(team, cells):
    return G.measure(*D[team], E, cells)


rows = []


def row(value, what, target, ok):
    rows.append((value, what, target, ok))
    mark = "" if ok is None else ("ok" if ok else "MISS")
    print(f"{value:>10}  {what:<58} {target:<22} {mark}")


print("Hoarfire plan check (plan walk: octile steps, the Rift bridged at a block a block, drops over six refused)")
print()
for team, own, other in (("red", lambda c: c, image), ("blue", image, lambda c: c)):
    m_own, _, _ = walk(team, own(MON))
    c_own, _, _ = walk(team, own(CORE))
    enemy = "blue" if team == "red" else "red"
    m_enemy, mb, _ = walk(enemy, own(MON))
    c_enemy, cb, _ = walk(enemy, own(CORE))
    row(f"{m_own:.0f}", f"{team}: own spawn to its Rime Monument", "40 to 90", 40 <= m_own <= 90)
    row(f"{c_own:.0f}", f"{team}: own spawn to its Ember Core", "40 to 90", 40 <= c_own <= 90)
    row(f"{m_enemy:.0f}", f"{team}'s monument from the enemy spawn ({mb.get('bridge', 0):.0f} bridged)", "", None)
    row(f"{c_enemy:.0f}", f"{team}'s core from the enemy spawn ({cb.get('bridge', 0):.0f} bridged)", "", None)
    row(f"{m_enemy / m_own:.2f}", f"{team}: monument, enemy walk / own walk", "2.5 to 4", 2.5 <= m_enemy / m_own <= 4)
    row(f"{c_enemy / c_own:.2f}", f"{team}: core, enemy walk / own walk", "2.5 to 4", 2.5 <= c_enemy / c_own <= 4)
# goal to goal across the Rift
Dm = G.dijkstra(E, MON)
mc, _, _ = G.measure(*Dm, E, image(CORE))
mm, _, _ = G.measure(*Dm, E, image(MON))
Dc = G.dijkstra(E, CORE)
cc, _, _ = G.measure(*Dc, E, image(CORE))
row(f"{min(mc, mm, cc):.0f}", "nearest enemy goal from a goal", "85 to 150", 85 <= min(mc, mm, cc) <= 150)
# the Rift: the narrowest crossing, the void a player must build
rift = R.mask("rift")
red_land = (R.Z < 0) & ~rift & (R.K != R.kinds["void"])
blue_land = (R.Z >= 0) & ~rift & (R.K != R.kinds["void"])
islet = np.zeros(rift.shape, bool)
for (cx, cz), rx, rz, _, _ in P.land.ISLETS:
    islet |= (np.abs(R.X - cx) <= rx + 1) & (np.abs(R.Z - cz) <= rz + 1) & ~rift & (R.K != R.kinds["void"])
red_land &= ~islet
blue_land &= ~islet
narrow = math.inf
xs = range(P.X_MIN, P.X_MAX + 1)
for x in xs:
    zr = [z for z in range(-20, 0) if red_land[x - P.X_MIN, z - P.Z_MIN]]
    zb = [z for z in range(0, 20) if blue_land[x - P.X_MIN, z - P.Z_MIN]]
    if zr and zb:
        narrow = min(narrow, min(zb) - max(zr) - 1)
row(narrow, "the Rift's narrowest void, shore to shore", "16 or more", narrow >= 16)
isl_gap = math.inf
for x in xs:
    col = [z for z in range(-20, 0) if red_land[x - P.X_MIN, z - P.Z_MIN]]
    il = [z for z in range(-12, 12) if islet[x - P.X_MIN, z - P.Z_MIN]]
    if col and il:
        isl_gap = min(isl_gap, min(il) - max(col) - 1)
row(isl_gap, "void from a shore to an islet", "5 or more (no jump)", isl_gap >= 5)
widest = max((gp for *_, gp in J), default=0)
row(f"{widest}", "the widest jump the plan allows", "at most 3", widest <= 3)
across = [j for j in J if (j[0][1] < -1) != (j[1][1] < -1)]
row(len(across), "jumps across the Rift", "none", len(across) == 0)
# every place reached from Rowan's spawn
Dr = D["red"][0]
missing = [n for n, (x, z) in P.PLACES if z < 0 and not any(math.hypot(x - a, z - b) <= 4 for a, b in Dr if len((a, b)) == 2)]
row(len(missing), "Rowan's places not reached on foot or by building", "none" if not missing else ", ".join(missing),
    not missing)
