"""Measure the plan before anything is built: walk its land and check the numbers capture boards are held to.

The land is the plan's pieces on red's half and their half-turn on blue's. A walk is octile: a step to a
neighbour costs 1, a diagonal 1.41. A walk may cross a build zone (not the band) by bridging it, block for
block; the bridged blocks are counted on their own, so "64 (13 bridged)" is 51 walked and 13 built.

    python3 plan_check.py            prints the table PLAN.md quotes
"""
import heapq
import math

import numpy as np

import geometry as G
import plan as P


def grid():
    xs = np.arange(P.X_MIN, P.X_MAX + 1); zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    land = np.zeros(X.shape, bool)
    owner = np.full(X.shape, "", object)
    for p in P.PIECES + [P.BELL_ROCK]:
        for poly, team in ((p["poly"], "red"), ([P.rot(x, z) for x, z in p["poly"]], "blue")):
            m = G.inside(X + 0.0, Z + 0.0, poly)
            if "hole" in p:
                hole = p["hole"] if team == "red" else [P.rot(x, z) for x, z in p["hole"]]
                m &= ~G.inside(X + 0.0, Z + 0.0, hole)
            land |= m
            owner = np.where(m, p["key"] + ":" + team, owner)
    band = G.inside(X + 0.0, Z + 0.0, P.BAND)
    zone = np.zeros(X.shape, bool)
    for z in P.BUILD_ZONES:
        if z["key"] != "band":
            for poly in (z["poly"], [P.rot(x, q) for x, q in z["poly"]]):
                zone |= G.inside(X + 0.0, Z + 0.0, poly)
    zone &= ~land
    return X, Z, land, owner, band, zone


STEPS = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.41), (1, -1, 1.41), (-1, 1, 1.41), (-1, -1, 1.41)]


def walk(land, zone, starts):
    """Octile distance over land and build zones from a set of (ix, iz) starts, and the blocks bridged on the way."""
    ok = land | zone
    D = np.full(land.shape, np.inf)
    Bn = np.zeros(land.shape)
    h = []
    for s in starts:
        D[s] = 0
        h.append((0.0, 0.0, s))
    heapq.heapify(h)
    while h:
        d, b, (i, k) = heapq.heappop(h)
        if d > D[i, k]:
            continue
        for di, dk, c in STEPS:
            a, e = i + di, k + dk
            if 0 <= a < ok.shape[0] and 0 <= e < ok.shape[1] and ok[a, e]:
                if di and dk and not (ok[i + di, k] and ok[i, k + dk]):
                    continue
                nb = b + (c if zone[a, e] else 0)
                if d + c < D[a, e] - 1e-9 or (abs(d + c - D[a, e]) < 1e-9 and nb < Bn[a, e]):
                    D[a, e] = d + c
                    Bn[a, e] = nb
                    heapq.heappush(h, (d + c, nb, (a, e)))
    return D, Bn


def cells_of(owner, key):
    return list(zip(*np.nonzero(owner == key)))


def gap(X, Z, owner, a, b):
    ca, cb = cells_of(owner, a + ":red"), cells_of(owner, b + ":red")
    return min(math.hypot(X[p] - X[q], Z[p] - Z[q]) for p in ca for q in cb) - 1


def main():
    X, Z, land, owner, band, zone = grid()
    ix0, iz0 = -P.X_MIN, -P.Z_MIN
    sp = (int(round(P.SPAWN_POINT[0] - 0.5)) + ix0, int(round(P.SPAWN_POINT[2] - 0.5)) + iz0)
    D_sp, B_sp = walk(land, zone, [sp])
    band_red = [tuple(c) for c in np.argwhere(band & (Z == -11))]
    D_bd, B_bd = walk(land & ~band, zone, band_red)
    out = []

    def to(D, B, key):
        cs = cells_of(owner, key + ":red")
        c = min(cs, key=lambda c: D[c])
        return D[c], B[c]

    def fmt(d, b):
        return f"{d:.0f}" + (f" ({b:.0f} bridged)" if b > 0.5 else "")
    front = [tuple(c) for c in np.argwhere(land & (Z == -12))]
    sp_band = min(D_sp[c] for c in front) + 1
    walked_sp, _ = walk(land, np.zeros_like(zone), [sp])
    s_store, s_pillar = to(D_sp, B_sp, "store"), to(D_sp, B_sp, "pillar")
    b_store, b_pillar = to(D_bd, B_bd, "store"), to(D_bd, B_bd, "pillar")
    out.append(("spawn to the band (SP10, at least 55)", f"{sp_band:.0f}"))
    out.append(("spawn to the Tea Store (WL9)", fmt(*s_store)))
    out.append(("spawn to the Tea Store, walked only", f"{min(walked_sp[c] for c in cells_of(owner, 'store:red')):.0f}"))
    out.append(("spawn to the Pillar (WL9)", fmt(*s_pillar)))
    out.append(("ratio of the two (WL9, ideal 1)", f"{max(s_store[0], s_pillar[0]) / min(s_store[0], s_pillar[0]):.2f}"))
    out.append(("band to the Tea Store, shortest (WL10e, at least 59)", fmt(*b_store)))
    out.append(("band to the Pillar, shortest (WL10e, at least 59)", fmt(*b_pillar)))
    # the same two from the band, kept to land and the hub: the way that is walked, not built
    land_only, _ = walk(land & ~band, np.zeros_like(zone), band_red)
    out.append(("band to the Tea Store, walked only", f"{min(land_only[c] for c in cells_of(owner, 'store:red')):.0f}"))
    wx0, wz0 = P.WOOLS[0]["at"]; wx1, wz1 = P.WOOLS[1]["at"]
    out.append(("Pillar to Tea Store, straight (WL7, 46 to 143)", f"{math.hypot(wx1 - wx0, wz1 - wz0):.0f}"))
    out.append(("Pillar to the Arms and the Long Terrace (WL20, at least 12)",
                ", ".join(f"{gap(X, Z, owner, 'pillar', k):.0f}" for k in ("f-west", "f-east", "f-stem"))))
    zmin = lambda poly: min(q[1] for q in poly) + 0.5
    zmax = lambda poly: max(q[1] for q in poly) - 0.5
    piece = {p["key"]: p for p in P.PIECES}
    drying = piece["drying"]["poly"]
    out.append(("the Store Road alone, its last junction to the room", f"{zmin(drying) - zmax(piece['store']['poly']) - 1:.0f}"))
    hole = next(p for p in P.PIECES if p["key"] == "hub")["hole"]
    out.append(("the Tea Court's sinkhole (LN6, at least 12)", f"{hole[1][0] - hole[0][0]:.0f} by {hole[2][1] - hole[1][1]:.0f}"))
    out.append(("the void inside the Store's F (LN6, at least 12)", f"{zmin(piece['rows']['poly']) - zmax(drying) - 1:.0f}"))
    out.append(("the void between the Stairs (WL12, at least 16)", f"{gap(X, Z, owner, 'leg-w', 'leg-e'):.0f}"))
    out.append(("the void from the spawn to the Near Arm", f"{gap(X, Z, owner, 'sp-front', 'f-east'):.0f}"))
    out.append(("the Mist Steps' gaps", ", ".join(f"{gap(X, Z, owner, a, b):.0f}" for a, b in
                                               (("w-1", "w-2"), ("w-1", "w-3"), ("w-3", "f-stem"), ("w-4", "f-stem")))))
    out.append(("the Tea Steps' gaps", ", ".join(f"{gap(X, Z, owner, a, b):.0f}" for a, b in (("e-1", "e-2"), ("e-2", "road")))))
    out.append(("land on red's half, in blocks", f"{int((land & (Z < 0)).sum())}"))
    w_ = max(len(a) for a, b in out)
    for a, b in out:
        print(f"{a:<{w_}}  {b}")
    return out


if __name__ == "__main__":
    main()
