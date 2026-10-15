"""The walk over built blocks (from Gullhaven): from a spawn, how far is every place a player can stand, on foot, with no blocks
placed? A step climbs one block; a player drops off any edge, three blocks at no cost, five at the price of a
heart, any height into water; swims, and is lifted by water and ladders.

    python3 walk.py <build-dir>

Checks every spawn point stands on ground with headroom, that every spawn reaches every other, and the walks
to the island's places.
"""
import sys
from collections import deque

import numpy as np

import render_iso
from mc import B

# doors are not passable: no block is used on this board, so a door stays shut
PASS = {0, 36, 55, 31, 32, 37, 38, 175, 50, 59, 141, 142, 83, 106, 65, 66, 27, 28, 63, 68, 72, 70, 78, 111, 30,
        171, 6, 39, 40, 8, 9, 69, 77, 143, 131, 132, 176, 177}
WATER = {8, 9}


def grid(ids):
    passable = np.isin(ids, list(PASS))
    water = np.isin(ids, list(WATER))
    ladder = ids == B.LADDER
    solid = ~passable
    return passable, water, ladder, solid


def standable(passable, water, solid):
    """A cell a player can occupy: two passable cells high, with solid ground or water under or in it."""
    st = np.zeros_like(passable)
    st[:, 1:-1, :] = passable[:, 1:-1, :] & passable[:, 2:, :] & (solid[:, :-2, :] | water[:, 1:-1, :] | water[:, :-2, :])
    return st


JUMPS = [(dx, dz) for dx in range(-4, 5) for dz in range(-4, 5)
         if 1 <= ((max(abs(dx) - 1, 0)) ** 2 + (max(abs(dz) - 1, 0)) ** 2) ** 0.5 <= 3]


def bfs(st, ladder, water, passable, start, x0, z0, jumps=False):
    sx, sy, sz = st.shape
    dist = np.full(st.shape, -1, np.int32)
    q = deque()
    for (x, y, z) in start:
        i = (x - x0, y, z - z0)
        if st[i]:
            dist[i] = 0
            q.append(i)

    def push(i, d):
        if dist[i] < 0:
            dist[i] = d
            q.append(i)
    while q:
        x, y, z = q.popleft()
        d = dist[x, y, z] + 1
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if not (0 <= nx < sx and 0 <= nz < sz):
                continue
            if y + 1 < sy - 1 and st[nx, y + 1, nz] and passable[x, y + 2, z]:
                push((nx, y + 1, nz), d)                     # a step up, with headroom to jump
            if st[nx, y, nz]:
                push((nx, y, nz), d)
                continue
            if not (passable[nx, y, nz] and passable[nx, y + 1, nz]):
                continue
            for ny in range(y - 1, 0, -1):                   # off the edge: fall to whatever is below
                if not passable[nx, ny, nz]:
                    break
                if st[nx, ny, nz]:
                    push((nx, ny, nz), d)                    # fall damage is off: any drop
                    break
        if jumps:                                            # a running jump over a gap of one to three, at most one up
            for dx, dz in JUMPS:
                nx, nz = x + dx, z + dz
                if not (0 <= nx < sx and 0 <= nz < sz) or y + 3 >= sy:
                    continue
                n = max(abs(dx), abs(dz)) * 3
                line = {(x + round(dx * s / n), z + round(dz * s / n)) for s in range(1, n)} - {(x, z), (nx, nz)}
                if not line or any(st[a, y, b] or st[a, y + 1, b] for a, b in line):
                    continue                                 # not a gap: the ground runs on
                if not all(passable[a, y + 1, b] and passable[a, y + 2, b] for a, b in line):
                    continue
                for ny in (y + 1, y):
                    if st[nx, ny, nz]:
                        push((nx, ny, nz), d + max(abs(dx), abs(dz)))
                        break
        for dy in (1, -1):                                   # ladders and water lift a player straight up
            ny = y + dy
            if 1 <= ny < sy - 1 and (ladder[x, ny, z] or ladder[x, y, z] or water[x, ny, z]) and (st[x, ny, z] or ladder[x, ny, z]):
                push((x, ny, z), d)
    return dist


def nearest(dist, x0, z0, x, y, z, r=1):
    best = None
    for dx in range(-r, r + 1):
        for dz in range(-r, r + 1):
            for dy in range(-1, 2):
                i = (x + dx - x0, y + dy, z + dz - z0)
                if 0 <= i[0] < dist.shape[0] and 0 <= i[2] < dist.shape[2] and dist[i] >= 0:
                    if best is None or dist[i] < best:
                        best = int(dist[i])
    return best


