"""Walk the built world: from a spawn, how far is every place a player can stand, on foot, with no blocks
placed? A step climbs one block; a player drops off any edge, three blocks at no cost, five at the price of a
heart, any height into water; swims, and is lifted by water and ladders.

    python3 walk.py <build-dir>

Prints the walks from each spawn to the three posts and the places on the way, and checks that nobody on the
ground can get back up into a spawn.
"""
import sys
from collections import deque

import numpy as np

import render_iso
from mc import B

PASS = {0, 36, 55, 31, 32, 37, 38, 175, 50, 59, 141, 142, 83, 106, 65, 66, 27, 28, 63, 68, 72, 70, 78, 111, 30, 64,
        193, 194, 195, 196, 197, 171, 6, 39, 40, 8, 9, 69, 77, 143, 131, 132, 176, 177}
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
                    if y - ny <= 5 or water[nx, ny, nz] or water[nx, ny - 1, nz]:
                        push((nx, ny, nz), d)
                    break
        if jumps:                                            # a running jump over a gap of one to three, at most one up
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                for g in (2, 3, 4):
                    nx, nz = x + dx * g, z + dz * g
                    if not (0 <= nx < sx and 0 <= nz < sz) or y + 3 >= sy:
                        continue
                    clear = all(passable[x + dx * k, y + 1, z + dz * k] and passable[x + dx * k, y + 2, z + dz * k]
                                for k in range(1, g))
                    if not clear:
                        break
                    for ny in (y + 1, y):
                        if st[nx, ny, nz] and not st[x + dx, y, z + dz]:
                            push((nx, ny, nz), d + g)
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


def main(build):
    x0, z0, ids, dat = render_iso.load(build)
    passable, water, ladder, solid = grid(ids)
    st = standable(passable, water, solid) | (ladder & passable)
    spawns = {"red": (0, 33, -55), "blue": (0, 33, 55)}
    places = [("the Cistern's top, the post", (0, 25, 0)), ("the Mirador's pad, the post", (-42, 25, 0)),
              ("the Minaret's top, the post", (30, 26, 0)), ("the Mirador's porch", (-25, 25, 0)),
              ("the pool under the spawn", (0, 18, 49)), ("the canal's head at the court", (5, 21, 17)),
              ("the arcade roof's north end", (11, 25, 18)), ("the west garden's kiosk", (-25, 21, 22))]
    out = []
    for team, s in spawns.items():
        dist = bfs(st, ladder, water, passable, [s], x0, z0)
        out.append(f"from {team} spawn {s}: {int((dist >= 0).sum())} standable cells reached on foot, no jumps")
        for name, (x, y, z) in places:
            if team == "red" and z:
                z = -z
            v = nearest(dist, x0, z0, x, y, z)
            out.append(f"  to {name}: {v if v is not None else 'NOT REACHED on foot'}")
    dist = bfs(st, ladder, water, passable, [spawns["blue"]], x0, z0, jumps=True)
    v = nearest(dist, x0, z0, 11, 25, 18)
    out.append(f"blue spawn, with running jumps: the arcade roof's north end {v if v is not None else 'NOT REACHED'}, "
               f"{int((dist >= 0).sum())} cells in all")
    for name, (x, y, z) in places[:3]:
        dist = bfs(st, ladder, water, passable, [(x, y, z)], x0, z0)
        parts = []
        for other, p in places[:3]:
            if other != name:
                v = nearest(dist, x0, z0, *p)
                parts.append(f"{other.split(',')[0]} {v if v is not None else 'not on foot'}")
        out.append(f"from {name.split(',')[0]}: " + "; ".join(parts))
    # can anyone on the ground get back up into a spawn room?
    dist = bfs(st, ladder, water, passable, [(25, 21, 0)], x0, z0)
    for team, s in spawns.items():
        v = nearest(dist, x0, z0, *s, r=3)
        out.append(f"from the ground into {team}'s spawn room: {'REACHED in ' + str(v) if v is not None else 'not reachable'}")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
