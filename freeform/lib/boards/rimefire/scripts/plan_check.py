"""Check Rimefire's plan before a block is written: each team's walk to each core, to the enemy spawn and over each
crossing, on the shaped ground with the bridges, against the goal rules' targets."""
import plan as PLAN
import planraster as PR
import land as LND
from pgmvox.plan import graph as G

R, g = PR.build()
E = PR.graph(R)
fx, fz = LND.FURNACE
SPAWN = {"fire": (PLAN.SPAWN_AT[0], PLAN.SPAWN_AT[2]), "ice": (-1 - PLAN.SPAWN_AT[0], -1 - PLAN.SPAWN_AT[2])}
GATE = {"fire": (fx - 10, fz), "ice": (-1 - (fx - 10), -1 - fz)}


def walk_to(frm, cells):
    D, prev = G.dijkstra(E, [frm])
    best = min((D[c] for c in cells if c in D), default=None)
    return best


def around(p, r=3):
    return [(p[0] + dx, p[1] + dz) for dx in range(-r, r + 1) for dz in range(-r, r + 1)]


rows = {}
for team in ("fire", "ice"):
    other = "ice" if team == "fire" else "fire"
    rows[f"{team} spawn to its own core's gate"] = walk_to(SPAWN[team], around(GATE[team]))
    rows[f"{team} spawn to the {other} core's gate"] = walk_to(SPAWN[team], around(GATE[other]))
    rows[f"{team} spawn to the {other} spawn"] = walk_to(SPAWN[team], around(SPAWN[other]))
    rows[f"{team} core gate to the {other} spawn"] = walk_to(GATE[team], around(SPAWN[other]))
for k, v in rows.items():
    print(f"{k}: {v if v is None else round(v)}")
own, enemy = rows["fire spawn to its own core's gate"], rows["fire spawn to the ice core's gate"]
print(f"enemy core / own core, from the spawn: {enemy / own:.2f}")
print(f"core gate to the enemy spawn / to its own spawn: {rows['fire core gate to the ice spawn'] / own:.2f}")
D, _ = G.dijkstra(E, [SPAWN["fire"]])
print("walkable columns reached from the fire spawn:", len(D), "of", int(sum((R.K == R.kinds[k]).sum() for k in PR.WALK)))
