"""Check Riftwater's plan before anything is built: each team's walk to its own two monuments (the same for both,
or the board is unfair), the cave's three ways up from the mouth behind the falls, the mine from the spawn, the
three rift crossings' gaps, and what stands on what.

    python3 plan_check.py            # prints the table the sketch draws
"""
import math

import numpy as np

import plan as P
from pgmvox import plangraph as G
from pgmvox import shapes
from pgmvox.build import Claims

RED_SPAWN = (P.SPAWN[0], P.SPAWN[2])
BLUE_SPAWN = P.SYM.point(*RED_SPAWN)


def ring(x, z, r=2):
    """The cells a player breaks a floating monument from: within r of it."""
    return [(x + dx, z + dz) for dx in range(-r, r + 1) for dz in range(-r, r + 1) if (dx, dz) != (0, 0)]


def targets():
    out = {}
    for key, ((x, z), _, name) in P.MONUMENTS.items():
        out[f"red {key}"] = ring(x, z)
        out[f"blue {key}"] = ring(*P.SYM.point(x, z))
    return out


def rift_gaps(R):
    """The air a team bridges at each z: from red's last floor (ground or deck) to blue's first, the narrowest
    at the Old Bridge, the falls and the south fields."""
    gaps = {}
    for z in range(R.z_min, R.z_max + 1):
        last = None
        for x in range(-1, R.x_min - 1, -1):
            if any(U.has()[U.ix(x), U.iz(z)] and U.kind(x, z) not in ("void", "none", "cave") for U in R.storeys):
                last = x
                break
        if last is not None:
            gaps[z] = 2 * (-1 - last)                  # the mirror's first floor is at -1 - last
    return gaps


def cost(c):
    """plangraph.route and arrivals answer None for a target nobody reaches; the table wants infinity."""
    return math.inf if c is None else c


def measure():
    R = P.build()
    E = G.graph(R, P.WALK, rules=G.PlanRules(jumps=False), extra=P.links())
    T = targets()
    arr = {t: {k: cost(v) for k, v in d.items()}
           for t, d in G.arrivals(E, {"red": [RED_SPAWN], "blue": [BLUE_SPAWN]}, T).items()}
    D, prev = G.dijkstra(E, [RED_SPAWN])
    paths = {}
    for key in P.MONUMENTS:
        best = min((c for c in T[f"red {key}"] if c in D), key=D.get)
        paths[key] = G.path(prev, best)
    # the underground: from the ledge behind the falls
    mouth = (-11, 6, 1)
    Dm, prevm = G.dijkstra(E, [mouth])
    sink = [(x, z) for x in range(-52, -47) for z in range(36, 41)]
    cellar = [(x, z, 1) for x in range(-54, -49) for z in range(-36, -31)]
    brk = [(-57, 37, 1), (-58, 37, 1), (-58, 38, 1)]
    adit = [(-104, 3), (-104, 4), (-103, 3), (-105, 3)]
    under = {"sinkhole": cost(G.route(Dm, prevm, sink)[0]), "gaol cellar": cost(G.route(Dm, prevm, cellar)[0]),
             "mine breakthrough": cost(G.route(Dm, prevm, brk)[0]), "spawn, by the mine": Dm.get(RED_SPAWN, math.inf)}
    adit_walk = cost(G.route(D, prev, adit)[0])
    cave_path = G.path(prevm, min((c for c in sink if c in Dm), key=Dm.get)) if any(c in Dm for c in sink) else []
    # the crossings
    gaps = rift_gaps(R)
    crossings = {"Old Bridge": min(gaps.get(z, 99) for z in range(-46, -41)),
                 "the falls": min(gaps.get(z, 99) for z in range(-3, 4)),
                 "the south fields": min(gaps.get(z, 99) for z in range(55, 85))}
    # what stands where: buildings, towers and roads on the ground, none on another
    C = Claims()
    for key, b in P.houses().items():
        C.claim(key, b["cells"])
    for name, x0, z0, x1, z1, _ in P.TOWERS:
        C.claim(name, {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)})
    L = P.land()
    for r in L.routes:
        d, _ = shapes.polyline(L.X.astype(float), L.Z.astype(float), r["line"])
        C.claim(r["name"], {(int(L.X[i, k]), int(L.Z[i, k])) for i, k in np.argwhere(d <= r["width"] / 2 - 0.5)})
    overlaps = [o for o in C.overlaps() if not ({o[1], o[2]} & {r["name"] for r in L.routes} and
                                               {o[1], o[2]} <= {r["name"] for r in L.routes})]
    house_on_road = [o for o in overlaps if (o[1] in P.houses() or o[2] in P.houses())]
    return dict(R=R, E=E, arr=arr, paths=paths, under=under, adit=adit_walk, crossings=crossings, gaps=gaps,
                overlaps=house_on_road, cave_path=cave_path, D=D)


def rows(m):
    a = m["arr"]
    out = []
    for key in P.MONUMENTS:
        r, b = a[f"red {key}"]["red"], a[f"blue {key}"]["blue"]
        out.append((f"{r:.1f}", f"red spawn to its {key} monument", "40-90, equal to blue's", 40 <= r <= 90 and abs(r - b) < 0.01))
        out.append((f"{b:.1f}", f"blue spawn to its {key} monument", "the mirror of red's", abs(r - b) < 0.01))
        e = a[f"red {key}"]["blue"]
        out.append(("none" if math.isinf(e) else f"{e:.0f}", f"blue to red's {key} monument on foot", "none: the rift is bridged", math.isinf(e)))
    out.append((f"{m['adit']:.0f}", "spawn to the mine adit", "at most 35", m["adit"] <= 35))
    for k, v in m["under"].items():
        tgt = "reached" if k != "spawn, by the mine" else "reached (the defenders' way in)"
        out.append(("none" if math.isinf(v) else f"{v:.0f}", f"falls cave mouth to {k}", tgt, not math.isinf(v)))
    for k, v in m["crossings"].items():
        out.append((v, f"blocks to bridge at {k}", "8-24", 8 <= v <= 24))
    out.append((len(m["overlaps"]), "buildings standing on a road or another building", "0", not m["overlaps"]))
    return out


if __name__ == "__main__":
    m = measure()
    for v, what, target, ok in rows(m):
        print(f"{'  ' if ok or ok is None else '! '}{str(v):>8}  {what}  (target {target})")
    for o in m["overlaps"]:
        print("   overlap:", o)
