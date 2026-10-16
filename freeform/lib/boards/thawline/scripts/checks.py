"""The measurements Thawline's plan is held to, made once for the checker and the sketch: each team's walks to its
own goals and the enemy's (building across the rift counted as walking), the goal rules the studio holds a destroy
board to (GO1 the enemy spawn three to four times as far as the own; GO4 the own spawn 40 to 90 away; GO3 an enemy
goal 85 to 150 from a spawn), how far each goal stands off the line between the spawns, the Thawline's widths, and
the dry ground nobody can reach."""
import math
from functools import lru_cache

import numpy as np

import plan as P
from pgmvox.plan import graph as G

SPAWN_F = (P.SPAWN_AT[0], P.SPAWN_AT[2])
SPAWN_E = P.SYM.point(*SPAWN_F)
SPAWNS = {"frost": [SPAWN_F], "ember": [SPAWN_E]}


def under(box, pad=0):
    return [(x, z) for x in range(box.x0 - pad, box.x1 + pad + 1) for z in range(box.z0 - pad, box.z1 + pad + 1)]


def image(cells):
    return [P.SYM.point(x, z) for x, z in cells]


TARGETS = {"frost core": under(P.CORE_BOX), "frost lantern": [c for c in under(P.LANTERN_BOX, 2)
                                                            if c != (P.LANTERN_BOX.x0, P.LANTERN_BOX.z0)]}
TARGETS["ember core"] = image(TARGETS["frost core"])
TARGETS["ember lantern"] = image(TARGETS["frost lantern"])


@lru_cache(maxsize=1)
def graph():
    R = P.build()
    return R, G.graph(R, P.WALK, rules=G.PlanRules(diagonals=True), bridge=P.RIFT)


@lru_cache(maxsize=1)
def dists():
    R, E = graph()
    return {t: G.dijkstra(E, s) for t, s in SPAWNS.items()}


def walk(team, target):
    R, E = graph()
    D, prev = dists()[team]
    cost, by, path = G.measure(D, prev, E, TARGETS[target])
    return cost, by.get("bridge", 0.0), path


def measure():
    """Every measurement as (value, what, target, passed) rows, and the routes the sketch draws."""
    rows, routes = [], {}
    for goal in ("core", "lantern"):
        own, _, p_own = walk("frost", f"frost {goal}")
        enemy, built, p_enemy = walk("ember", f"frost {goal}")
        own_e, _, _ = walk("ember", f"ember {goal}")
        enemy_e, _, _ = walk("frost", f"ember {goal}")
        routes[f"frost to its {goal}"] = p_own
        routes[f"ember to Frost's {goal}"] = p_enemy
        name = "Heart" if goal == "core" else "Lantern"
        rows += [(f"{own:.0f}", f"Frost's spawn to the Frost {name} (GO4)", "40 to 90", 40 <= own <= 90),
                 (f"{enemy:.0f}", f"Ember's spawn to the Frost {name}, {built:.0f} built (GO3)", "85 to 150",
                  85 <= enemy <= 150),
                 (f"{enemy / own:.2f}", f"the Frost {name}'s walks, enemy over own (GO1)", "3 to 4", 3 <= enemy / own <= 4),
                 (f"{own_e:.0f} / {enemy_e:.0f}", f"Ember's twin walks to the Ember {name}", "the same", abs(own - own_e) < 0.5
                  and abs(enemy - enemy_e) < 0.5)]
    for name, (gx, gz) in (("Heart", P.land.KETTLE), ("Lantern", P.land.GREEN)):
        a = abs(math.degrees(math.atan2(gx - SPAWN_F[0], gz - SPAWN_F[1])))
        rows.append((f"{a:.0f}", f"degrees the {name} stands off the line between the spawns", "30 to 60 (corpus 42)",
                     30 <= a <= 60))
    widths = [int(n) for n in (P.RIFT & ~P.STACK).sum(axis=1) if n]
    rows.append((f"{min(widths)} to {max(widths)}", "the Thawline's width, lip to lip, away from the Stack",
                 "at least 7: no jump crosses it", min(widths) >= 7))
    col = P.LAND[-P.X_MIN]
    zs = P.Z[-P.X_MIN]
    stack_z = zs[P.STACK[-P.X_MIN]]
    lip = max(int(z) for z, l_ in zip(zs, col) if l_ and z < stack_z.min())
    gap = int(stack_z.min() - lip - 1)
    rows.append((gap, "the gap from a lip to the Stack, at x 0", "4 to 6: bridged, never jumped", 4 <= gap <= 6))
    R, E = graph()
    D, _ = dists()["frost"]
    reach = np.zeros(P.H.shape, bool)
    for k in D:
        if len(k) == 2:
            reach[k[0] - P.X_MIN, k[1] - P.Z_MIN] = True
    steep = R.mask("steep") & P.LAND
    dry = P.LAND & ~P.WET & ~steep
    behind = np.abs(P.Z + 0.5) > 78
    miss = dry & ~reach
    front = miss & ~behind
    rows.append((f"{100 * miss.sum() / dry.sum():.1f}%", "dry walkable ground not reached from a spawn",
                 "only the Glacier and its spurs, behind the spawns", front.sum() == 0))
    rows.append((int(P.LAND.sum()), "columns of land (the rift and the void not counted)", "under 24,000 (150 by 200 "
                 "less the void)", P.LAND.sum() < 24000))
    return rows, routes
