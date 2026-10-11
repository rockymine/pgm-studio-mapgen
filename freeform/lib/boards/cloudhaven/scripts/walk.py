"""Walk the built world: from a spawn, how far is every place a player can stand, on foot, with no blocks
placed? A step climbs one block, drops at most three, swims through water, climbs ladders, passes doors.

    python3 walk.py <build-dir>

Prints the walks from each spawn to each monument and to the islands, ships and rocks between — the numbers
the report quotes. Water here only falls, so nobody swims.
"""
import sys
from collections import deque

import numpy as np

import render_iso
from mc import B

PASS = {0, 31, 32, 37, 38, 175, 50, 59, 141, 142, 83, 106, 65, 66, 27, 28, 63, 68, 72, 70, 78, 111, 30, 64,
        193, 194, 195, 196, 197, 171, 6, 39, 40, 8, 9, 69, 77, 143, 131, 132}
WATER = {8, 9}


def grid(ids):
    passable = np.isin(ids, list(PASS))
    water = np.isin(ids, list(WATER))
    ladder = ids == B.LADDER
    solid = ~passable
    return passable, water, ladder, solid


def standable(passable, water, solid):
    """A cell a player can occupy: two passable cells high, with solid ground or water under or in it."""
    sx, sy, sz = passable.shape
    st = np.zeros_like(passable)
    st[:, 1:-1, :] = passable[:, 1:-1, :] & passable[:, 2:, :] & (solid[:, :-2, :] | water[:, 1:-1, :] | water[:, :-2, :])
    return st


def bfs(st, ladder, water, start, x0, z0):
    sx, sy, sz = st.shape
    dist = np.full(st.shape, -1, np.int32)
    q = deque()
    for (x, y, z) in start:
        i = (x - x0, y, z - z0)
        if st[i]:
            dist[i] = 0
            q.append(i)
    while q:
        x, y, z = q.popleft()
        d = dist[x, y, z] + 1
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if not (0 <= nx < sx and 0 <= nz < sz):
                continue
            for dy in (0, 1, -1, -2, -3):
                ny = y + dy
                if not (1 <= ny < sy - 1):
                    continue
                if st[nx, ny, nz] and dist[nx, ny, nz] < 0:
                    # a climb needs headroom over where you stand
                    if dy == 1 and not st[x, y, z] | True:
                        continue
                    dist[nx, ny, nz] = d
                    q.append((nx, ny, nz))
                    break
                if dy == 0 and st[nx, ny, nz]:
                    break
        # ladders and water lift a player straight up
        for dy in (1, -1):
            ny = y + dy
            if 1 <= ny < sy - 1 and (ladder[x, ny, z] or ladder[x, y, z] or water[x, ny, z]) and st[x, ny, z] | ladder[x, ny, z]:
                if dist[x, ny, z] < 0:
                    dist[x, ny, z] = d
                    q.append((x, ny, z))
    return dist


def nearest(dist, x0, z0, x, y, z, r=3):
    best = None
    for dx in range(-r, r + 1):
        for dz in range(-r, r + 1):
            for dy in range(-4, 2):
                i = (x + dx - x0, y + dy, z + dz - z0)
                if 0 <= i[0] < dist.shape[0] and 0 <= i[2] < dist.shape[2] and dist[i] >= 0:
                    if best is None or dist[i] < best:
                        best = int(dist[i])
    return best


def main(build):
    import plan as P
    x0, z0, ids, dat = render_iso.load(build)
    passable, water, ladder, solid = grid(ids)
    st = standable(passable, np.zeros_like(water), solid) | (ladder & passable)
    H = np.load(f"{build}/heights.npy")

    def at(key, dy=1):
        x, z = [i for i in P.ISLANDS if i["key"] == key][0]["at"]
        return (x, int(H[x - x0, z - z0]) + dy, z)
    spawns = {"red": (-110, 94, 0), "blue": (109, 94, -1)}
    goals = {"red monument A (Lantern Isle)": (-72, 80, -60), "red monument B (the Gardens)": (-71, 60, 59),
             "blue monument A": (71, 80, 59), "blue monument B": (70, 60, -60)}
    places = {"Windmill Isle": at("windmill"), "Sentinel Rock": at("sentinel"), "Port Aerie": at("port"),
              "Gate Rock": at("gate"), "the Concord's deck": (-12, 75, -1), "the Concord's far end": (14, 75, -1),
              "the Albatross's deck": (-40, 73, -27), "Cloudstep": at("cloudstep"), "North Reach": at("northreach"),
              "Fernrock": at("fernrock"), "South Reach": at("southreach")}
    out = []
    for team, s in spawns.items():
        dist = bfs(st, ladder, np.zeros_like(water), [s], x0, z0)
        out.append(f"from {team} spawn {s}: {int((dist >= 0).sum())} standable cells reached on foot")
        for name, m in goals.items():
            out.append(f"  to {name}: {nearest(dist, x0, z0, *m, r=4)}")
        if team == "red":
            for name, p in places.items():
                out.append(f"  to {name}: {nearest(dist, x0, z0, *p, r=4)}")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
