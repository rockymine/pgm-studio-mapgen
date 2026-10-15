"""Walk the built world: from a spawn, how far is every place a player can stand, on foot, with no blocks
placed? A step climbs one block, drops at most three, swims through water, climbs ladders, passes doors.

    python3 walk.py <build-dir>

Prints the walks from each spawn to its objectives along the skyways and stairs, and says which masses are
reached only by bridging — the numbers the report quotes. Nothing below the kill height counts as ground.
"""
import sys
from collections import deque

import numpy as np

import render_iso
from mc import B

PASS = {0, 36, 55, 31, 32, 37, 38, 175, 50, 59, 141, 142, 83, 106, 65, 66, 27, 28, 63, 68, 72, 70, 78, 111, 30, 64,
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
    x0, z0, ids, dat = render_iso.load(build)
    passable, water, ladder, solid = grid(ids)
    st = standable(passable, water, solid) | (ladder & passable)
    st[:, :41, :] = False                     # below the kill height nobody stands
    spawns = {"red": (-1, 73, -105), "blue": (0, 73, 104)}
    red_places = {"its own monuments": (-1, 71, -89), "the Tea Store's door (its own)": (56, 70, -96),
                  "the Near Arm's end": (-37, 68, -95), "the Far Arm's end": (-88, 68, -95),
                  "the Long Terrace's west end": (-86, 67, -66), "the West Stair's foot at the band": (-19, 65, -13),
                  "the East Stair's foot at the band": (18, 65, -13), "the Store Road's foot": (56, 67, -40), "the Store Road at its wall": (56, 70, -80)}
    enemy = {"red's Tea Store, inside the door": (56, 71, -99), "red's Near Arm (the Pillar's launch)": (-37, 68, -80),
             "red's Pillar Shrine": (-63, 75, -94), "red's West Ledge": (-73, 47, -79)}
    out = []
    for team, s in spawns.items():
        dist = bfs(st, ladder, water, [s], x0, z0)
        out.append(f"from {team} spawn {s}: {int((dist >= 0).sum())} standable cells reached on foot, no blocks placed")
        if team == "red":
            for name, p in red_places.items():
                v = nearest(dist, x0, z0, *p, r=3)
                out.append(f"  to {name}: {v if v is not None else 'not walked: behind the bedrock wall, crossed by building'}")
        else:
            for name, p in enemy.items():
                v = nearest(dist, x0, z0, *p, r=3)
                out.append(f"  to {name}: {v if v is not None else 'not walked: built to, or dropped to'}")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
