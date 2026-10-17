"""Check Sixes and Sevens' plan: every walk the studio's goal rules measure, against its band, for Red (Blue's
are the same by the half turn), walked on the snow without building.

    GO4  monument to its own spawn            40 to 90
    GO1  to the enemy spawn over to its own    3 to 4
    GO2  a team's two monuments apart         35 to 65
    GO3  a monument to every enemy monument   85 to 150
"""
from plan import PUMP, REACTOR, SPAWN, WALK, WALLS, build
from pgmvox.plan import graph as G

R = build()
E = G.graph(R, WALK, WALLS, rules=G.PlanRules(diagonals=True))
sym = R.symmetry.point
SITES = {"red reactor": REACTOR, "red pump": PUMP, "blue reactor": sym(*REACTOR), "blue pump": sym(*PUMP)}
SITES = {k: (int(v[0]), int(v[1])) for k, v in SITES.items()}
RED, BLUE = SPAWN, tuple(int(v) for v in sym(*SPAWN))


def walk(a, b):
    D, _ = G.dijkstra(E, [a])
    return D.get(b, float("inf"))


def rows():
    out = []
    for name in ("red reactor", "red pump"):
        own, enemy = walk(RED, SITES[name]), walk(BLUE, SITES[name])
        out.append((f"{own:.0f}", f"{name} to Red's spawn", "40 to 90", 40 <= own <= 90))
        out.append((f"{enemy / own:.2f}", f"{name}: Blue's spawn over Red's", "3 to 4", 3 <= enemy / own <= 4))
    d = walk(SITES["red reactor"], SITES["red pump"])
    out.append((f"{d:.0f}", "red reactor to red pump", "35 to 65", 35 <= d <= 65))
    for a in ("red reactor", "red pump"):
        for b in ("blue reactor", "blue pump"):
            d = walk(SITES[a], SITES[b])
            out.append((f"{d:.0f}", f"{a} to {b}", "85 to 150", 85 <= d <= 150))
    return out


if __name__ == "__main__":
    for value, what, target, ok in rows():
        print(f"{'ok  ' if ok else 'MISS'} {value:>6}  {what}  (target {target})")
