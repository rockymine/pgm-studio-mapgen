"""Emberfrost's plan, measured before a block is built: the walk over the planned ground (a climb of one a step, a drop of three, the gorge crossed
by its three spans and its two scree ways, water and lava not walked), from each spawn to each core, against the targets the plan states.

    python3 plan_check.py > renders/plan-check.txt
"""
import heapq
import math

import numpy as np

import plan as P
import land

H, LAND = P.H.copy(), P.LAND
X, Z = P.X, P.Z
xs, zs = X + 0.5, Z + 0.5
az = np.abs(zs)
walkable = LAND.copy()
walkable &= ~((az < 9.5) & (H < land.LIQUID + 1) & (np.abs(xs) > 3.5))              # the river and the lava
walkable &= ~(land.lake_distance(X, Z) < 0.97) | (H > land.LAKE_ICE - 1) | True       # the Mirror is frozen: walked
for xc, half, deck in ((-41, 2, 65), (0, 3, 64), (40, 2, 64)):                       # a span: a deck over the gorge, both halves
    for x in range(xc - half, xc + half + 1):
        for z in range(-14, 14):
            i, k = x - P.X_MIN, z - P.Z_MIN
            H[i, k] = deck
            walkable[i, k] = True
for x in range(-3, 4):                                                               # the bar under the Cinder Span
    for z in range(-5, 6):
        H[x - P.X_MIN, z - P.Z_MIN] = land.LIQUID + 1
        walkable[x - P.X_MIN, z - P.Z_MIN] = True


def dijkstra(start):
    dist = {start: 0.0}
    heap = [(0.0, start)]
    while heap:
        d, (i, k) = heapq.heappop(heap)
        if d > dist[(i, k)]:
            continue
        for di in (-1, 0, 1):
            for dk in (-1, 0, 1):
                if (di, dk) == (0, 0):
                    continue
                a, b = i + di, k + dk
                if not (0 <= a < H.shape[0] and 0 <= b < H.shape[1]) or not walkable[a, b]:
                    continue
                if H[a, b] - H[i, k] > 1 or H[i, k] - H[a, b] > 3:
                    continue
                nd = d + math.hypot(di, dk)
                if nd < dist.get((a, b), 1e9):
                    dist[(a, b)] = nd
                    heapq.heappush(heap, (nd, (a, b)))
    return dist


def cell(x, z):
    return (x - P.X_MIN, z - P.Z_MIN)


spawn_r = cell(P.SPAWN_AT[0], P.SPAWN_AT[2])
spawn_b = cell(P.SPAWN_AT[0], -1 - P.SPAWN_AT[2])
dr, db = dijkstra(spawn_r), dijkstra(spawn_b)
rows = []


def near(dist, x, z, r=5):
    best = None
    for dx in range(-r, r + 1):
        for dz in range(-r, r + 1):
            c = cell(x + dx, z + dz)
            if c in dist and math.hypot(dx, dz) >= 4 and (best is None or dist[c] < best):
                best = dist[c]
    return best


print("measurement                                         value   target")
for name, (x, z) in (("Rime Core", P.RIME), ("Forge Core", P.FORGE)):
    own = near(dr, x, z)
    enemy = near(dr, x, -1 - z)
    to_enemy_spawn = dijkstra(cell(x, z)).get(spawn_b)
    to_own_spawn = own
    ratio = to_enemy_spawn / to_own_spawn if to_enemy_spawn and to_own_spawn else float("nan")
    print(f"red spawn to red {name:11s}                        {own:6.0f}   40 to 90")
    print(f"red spawn to blue {name:10s}                       {enemy:6.0f}   85 to 150")
    print(f"red {name:11s} to blue spawn / to red spawn           {ratio:6.2f}   3 to 4")
reached = sum(1 for c in dr if walkable[c])
print(f"land cells reached from red's spawn: {reached} of {int(LAND.sum())}                 all")
print(f"board: {LAND.shape[0]} by {LAND.shape[1]}, land {100 * LAND.mean():.0f}% of it                       at most 150 by 200")
