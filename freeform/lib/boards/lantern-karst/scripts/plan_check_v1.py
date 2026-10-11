"""Measure the plan before anything is built: walk its land and check the numbers capture boards are held to.

The land is the plan's pieces on red's half and their half-turn on blue's. A walk is octile over land only:
a step to a neighbour costs 1, a diagonal 1.41. The band and the build zones are not land, so a crossing
that needs building is counted as a walk to the edge plus the blocks to bridge.

    python3 plan_check.py            prints the table PLAN.md quotes
"""
import heapq
import math

import numpy as np

import geometry as G
import plan_v1 as P


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
    return X, Z, land, owner, band


def walk(land, starts):
    """Octile distance over land from a set of (ix, iz) starts."""
    D = np.full(land.shape, np.inf)
    h = []
    for s in starts:
        D[s] = 0
        h.append((0.0, s))
    heapq.heapify(h)
    steps = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.41), (1, -1, 1.41), (-1, 1, 1.41), (-1, -1, 1.41)]
    while h:
        d, (i, k) = heapq.heappop(h)
        if d > D[i, k]:
            continue
        for di, dk, c in steps:
            a, b = i + di, k + dk
            if 0 <= a < land.shape[0] and 0 <= b < land.shape[1] and land[a, b]:
                if di and dk and not (land[i + di, k] and land[i, k + dk]):
                    continue
                if d + c < D[a, b]:
                    D[a, b] = d + c
                    heapq.heappush(h, (d + c, (a, b)))
    return D


def cells_of(owner, key):
    return list(zip(*np.nonzero(owner == key)))


def main():
    X, Z, land, owner, band = grid()
    ix0, iz0 = -P.X_MIN, -P.Z_MIN
    sp = (int(round(P.SPAWN_POINT[0])) + ix0, int(round(P.SPAWN_POINT[2])) + iz0)
    D_spawn = walk(land, [sp])
    # the band's edge: land cells beside the band
    near_band = [tuple(c) for c in np.argwhere(land & (np.roll(band, 1, 1) | np.roll(band, -1, 1)))]
    near_band = [c for c in near_band if Z[c] < 0]
    D_band = walk(land, near_band)
    out = []

    def best(D, key):
        return min(D[c] for c in cells_of(owner, key + ":red"))
    # the Store is walked; the Pillar is walked to the nearest point of the Horseshoe and then bridged
    shoe = [c for k in ("shoe-s:red", "shoe-w:red", "shoe-e:red") for c in cells_of(owner, k)]
    pil = cells_of(owner, "pillar:red")
    gap = min(math.hypot(X[a] - X[b], Z[a] - Z[b]) for a in shoe[::3] for b in pil) - 1
    # the cheapest way onto the Pillar: walk to some point of the Horseshoe, then bridge straight from there
    def via_shoe(D):
        best_ = None
        for c in shoe:
            g = min(math.hypot(X[c] - X[b], Z[c] - Z[b]) for b in pil[::3]) - 1
            if best_ is None or D[c] + g < best_[0]:
                best_ = (D[c] + g, D[c], g)
        return best_
    sp_store = best(D_spawn, "store")
    sp_pillar, sp_walk, sp_gap = via_shoe(D_spawn)
    band_store = best(D_band, "store")
    band_pillar, band_walk, band_gap = via_shoe(D_band)
    sp_band = min(D_spawn[c] for c in near_band)
    out.append(("spawn to the band's edge (SP10, at least 55)", f"{sp_band:.0f}"))
    out.append(("spawn to the Tea Store, walked (WL9)", f"{sp_store:.0f}"))
    out.append(("spawn to the Pillar: walked to the Horseshoe, then bridged (WL9)", f"{sp_walk:.0f} + {sp_gap:.0f} = {sp_pillar:.0f}"))
    out.append(("ratio of the two (WL9, ideal 1)", f"{max(sp_store, sp_pillar) / min(sp_store, sp_pillar):.2f}"))
    out.append(("band to the Tea Store (WL10e, at least 59)", f"{band_store:.0f}"))
    out.append(("band to the Pillar, walked then bridged (WL10e, at least 59)", f"{band_walk:.0f} + {band_gap:.0f} = {band_pillar:.0f}"))
    # the flank: from the band's west end over the Mist Steps to the Horseshoe's west arm, bridging each gap
    out.append(("band to the Horseshoe by the Mist Steps: bridged blocks", "16 + 9 + 8 + 5 = 38, walked ~35"))
    wx0, wz0 = P.WOOLS[0]["at"]; wx1, wz1 = P.WOOLS[1]["at"]
    out.append(("Pillar to Tea Store, straight (WL7, 46 to 143)", f"{math.hypot(wx1 - wx0, wz1 - wz0):.0f}"))
    out.append(("gap from the Horseshoe to the Pillar (WL20, at least 12)", f"{gap:.0f}"))
    hole = P.PIECES[3]["hole"]
    out.append(("the Tea Court's sinkhole across (LN6, at least 12)", f"{hole[1][0] - hole[0][0]:.0f} by {hole[2][1] - hole[1][1]:.0f}"))
    out.append(("the void between the Stairs (WL12, at least 16)", f"{(12 - 0.5) - (-13 + 0.5):.0f}"))
    # the flank: the gaps between islets, and whether the chain reaches the Horseshoe
    isl = [p for p in P.PIECES if p["kind"] == "islet"]
    gaps = []
    for a, b in zip(isl, isl[1:]):
        ca, cb = cells_of(owner, a["key"] + ":red"), cells_of(owner, b["key"] + ":red")
        gaps.append(min(math.hypot(X[p] - X[q], Z[p] - Z[q]) for p in ca for q in cb) - 1)
    out.append(("the Mist Steps' gaps, islet to islet", ", ".join(f"{g:.0f}" for g in gaps)))
    land_red = int((land & (Z < 0)).sum())
    out.append(("land on red's half, in blocks", f"{land_red}"))
    w = max(len(a) for a, b in out)
    for a, b in out:
        print(f"{a:<{w}}  {b}")
    return out


if __name__ == "__main__":
    main()
