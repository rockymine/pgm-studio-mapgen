"""Dungeon and bunker layouts. Each is laid out on a grid, one level at a time: every cell rock, room, corridor or
door, with a ceiling height per cell, and then carved out of solid rock. Measured for play: rooms, loops, dead ends,
the longest straight sightline and the longest walk between two points.

    dungeon      rooms of many shapes in a split plan, corridors between neighbours, extra links for loops
    caverns      grown caves, joined by tunnels, a great hall with a pillar of rock left in it
    crypt        four-fold: a rotunda, a ring gallery, spokes, burial niches and corner chapels
    descent      two dungeon levels over each other, stairwells between them and an atrium through both
    bunker       blast doors, a chicane entrance under a firing slit, dog-leg corridors, barracks, command,
                 generator hall, air shafts and a long escape tunnel
    line         a fortress line: a long gallery with a rail, branches climbing to casemates at the surface

    python3 dungeons.py [name ...]      # renders into ../renders/layouts
"""
import os
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import B, World                                                   # noqa: E402
from pgmvox.geom import noise                                                 # noqa: E402
from pgmvox.read import render                                                # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "layouts")
N = 160
ROCK, ROOM, CORR, DOOR, STAIR, PILLAR = 0, 1, 2, 3, 4, 5
SURFACE = 52


class Level:
    def __init__(self, floor):
        self.kind = np.zeros((N, N), np.int8)
        self.height = np.zeros((N, N), np.int8)
        self.floor = floor
        self.rooms = []

    def room(self, mask, h=5):
        self.kind[mask & (self.kind != DOOR)] = ROOM
        self.height[mask] = np.maximum(self.height[mask], h)
        self.rooms.append(mask)

    def corridor(self, mask, h=3):
        free = mask & (self.kind == ROCK)
        self.kind[free] = CORR
        self.height[mask] = np.maximum(self.height[mask], h)


I, K = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")


def rect(x0, z0, x1, z1):
    return (I >= x0) & (I <= x1) & (K >= z0) & (K <= z1)


def disc(cx, cz, r):
    return np.hypot(I - cx, K - cz) <= r


def lpath(a, b, width, rng, bend=None):
    """An L-shaped corridor from a to b, `width` wide, turning first along x or z."""
    (ax, az), (bx, bz) = a, b
    first_x = rng.random() < 0.5 if bend is None else bend
    h = (width - 1) // 2, width // 2
    if first_x:
        return rect(min(ax, bx) - h[0], az - h[0], max(ax, bx) + h[1], az + h[1]) | \
            rect(bx - h[0], min(az, bz) - h[0], bx + h[1], max(az, bz) + h[1])
    return rect(ax - h[0], min(az, bz) - h[0], ax + h[1], max(az, bz) + h[1]) | \
        rect(min(ax, bx) - h[0], bz - h[0], max(ax, bx) + h[1], bz + h[1])


def shaped_room(x0, z0, x1, z1, rng):
    """A room in a box: a plain hall, a round chamber, a cross, a pillared hall or an L, chosen at random."""
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    w, d = x1 - x0, z1 - z0
    kind = rng.choice(["hall", "round", "cross", "pillars", "ell"], p=[0.3, 0.2, 0.15, 0.2, 0.15])
    if kind == "round":
        return disc(cx, cz, min(w, d) / 2), kind
    if kind == "cross":
        return rect(x0, cz - d / 5, x1, cz + d / 5) | rect(cx - w / 5, z0, cx + w / 5, z1), kind
    if kind == "ell":
        return rect(x0, z0, x1, cz) | rect(x0, z0, cx, z1), kind
    m = rect(x0, z0, x1, z1)
    if kind == "pillars" and w >= 9 and d >= 9:
        piers = ((I - x0) % 4 == 2) & ((K - z0) % 4 == 2) & rect(x0 + 2, z0 + 2, x1 - 2, z1 - 2)
        return m, piers
    return m, kind


def bsp(box, rng, min_size=22, out=None):
    out = [] if out is None else out
    x0, z0, x1, z1 = box
    w, d = x1 - x0, z1 - z0
    if max(w, d) < min_size * 2 or (max(w, d) < min_size * 2.6 and rng.random() < 0.3):
        out.append(box)
        return out
    if w > d:
        s = int(rng.uniform(x0 + min_size, x1 - min_size))
        bsp((x0, z0, s, z1), rng, min_size, out); bsp((s, z0, x1, z1), rng, min_size, out)
    else:
        s = int(rng.uniform(z0 + min_size, z1 - min_size))
        bsp((x0, z0, x1, s), rng, min_size, out); bsp((x0, s, x1, z1), rng, min_size, out)
    return out


def dungeon_level(lv, rng, box=(4, 4, N - 5, N - 5), loops=4):
    leaves = bsp(box, rng)
    centres = []
    for x0, z0, x1, z1 in leaves:
        w, d = x1 - x0, z1 - z0
        rw, rd = int(rng.uniform(0.5, 0.85) * w), int(rng.uniform(0.5, 0.85) * d)
        rx0 = int(rng.uniform(x0 + 3, x1 - 3 - rw)) if x1 - 3 - rw > x0 + 3 else x0 + 3
        rz0 = int(rng.uniform(z0 + 3, z1 - 3 - rd)) if z1 - 3 - rd > z0 + 3 else z0 + 3
        m, kind = shaped_room(rx0, rz0, rx0 + rw, rz0 + rd, rng)
        piers = kind if not isinstance(kind, str) else None
        lv.room(m, h=7 if piers is not None or kind == "round" else 5)
        if piers is not None:
            lv.kind[piers] = PILLAR
        centres.append((rx0 + rw // 2, rz0 + rd // 2))
    # a spanning tree by nearest neighbours, then extra links for loops
    pts = np.array(centres)
    joined, edges = {0}, []
    while len(joined) < len(pts):
        best = None
        for a in joined:
            for b in range(len(pts)):
                if b in joined:
                    continue
                dd = np.hypot(*(pts[a] - pts[b]))
                if best is None or dd < best[0]:
                    best = (dd, a, b)
        edges.append(best[1:]); joined.add(best[2])
    pairs = sorted(((np.hypot(*(pts[a] - pts[b])), a, b) for a in range(len(pts)) for b in range(a + 1, len(pts))))
    extra = [p for p in pairs if (p[1], p[2]) not in edges and (p[2], p[1]) not in edges][:loops * 3]
    for _, a, b in [extra[k] for k in rng.choice(len(extra), size=min(loops, len(extra)), replace=False)]:
        edges.append((a, b))
    for a, b in edges:
        lv.corridor(lpath(tuple(pts[a]), tuple(pts[b]), int(rng.choice([2, 3, 3])), rng))
    return centres


def doors(lv):
    """A door wherever a corridor meets a room."""
    room = lv.kind == ROOM
    near = ndimage.binary_dilation(room, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)) & (lv.kind == CORR)
    lab, n = ndimage.label(near)
    for k in range(1, n + 1):                                              # a door is a corridor's mouth, not a run
        cells = lab == k                                                   # of corridor along a room's side
        if cells.sum() <= 4:
            lv.kind[cells] = DOOR
            lv.height[cells] = 3


# --- the layouts ----------------------------------------------------------------------------------------------------

def dungeon():
    rng = np.random.default_rng(3)
    lv = Level(20)
    dungeon_level(lv, rng, loops=5)
    doors(lv)
    return [lv], None


def caverns():
    rng = np.random.default_rng(5)
    lv = Level(20)
    cave = (rng.random((N, N)) < 0.56) | ~rect(3, 3, N - 4, N - 4)
    for _ in range(5):
        n = ndimage.convolve(cave.astype(int), np.ones((3, 3)), mode="constant", cval=1)
        cave = n >= 5
    cave = ndimage.binary_closing(cave, iterations=1) | cave
    open_ = ~cave
    open_ |= (np.hypot((I - 80) / 30, (K - 82) / 22) + 0.12 * noise.fbm((N, N), 10, 2, seed=6)) < 1   # the great hall
    open_ &= ~(np.hypot(I - 84, K - 80) < 5 + 1.5 * noise.fbm((N, N), 4, 1, seed=7))                   # its pillar
    lab, n = ndimage.label(open_)
    sizes = ndimage.sum(open_, lab, range(1, n + 1))
    keep = [k + 1 for k in np.argsort(sizes)[::-1][:8] if sizes[k] > 60]
    open_ = np.isin(lab, keep)
    lab, n = ndimage.label(open_)
    cents = ndimage.center_of_mass(open_, lab, range(1, n + 1))
    main = int(np.argmax(ndimage.sum(open_, lab, range(1, n + 1))))
    for k, c in enumerate(cents):                                          # a wandering tunnel from each to the main
        if k == main:
            continue
        p = np.array(c, float)
        goal = np.array(cents[main], float)
        for _ in range(400):
            step = (goal - p) / max(np.linalg.norm(goal - p), 1) + rng.normal(0, 0.7, 2)
            p = p + step / max(np.linalg.norm(step), 1e-6)
            i, j = int(p[0]), int(p[1])
            open_[max(i - 1, 0):i + 2, max(j - 1, 0):j + 2] = True
            if np.linalg.norm(goal - p) < 3:
                break
    dist = ndimage.distance_transform_edt(open_)
    lv.kind[open_] = ROOM
    lv.height[open_] = np.clip(2 + dist[open_] * 1.1 + 2 * noise.fbm((N, N), 12, 2, seed=8)[open_], 3, 14).astype(np.int8)
    return [lv], None


def crypt():
    lv = Level(20)
    c = (N - 1) / 2
    r = np.hypot(I - c, K - c)
    th = np.arctan2(K - c, I - c)
    lv.room(r <= 13, h=9)                                                 # the rotunda
    lv.room((r <= 15) & (np.abs(np.sin(2 * th)) > 0.96) & (r > 12), h=5)   # four apses
    lv.corridor((r >= 40) & (r <= 43), h=5)                                # the ring gallery
    for a in range(4):                                                     # spokes, each a dog-leg past a pillar
        ang = a * np.pi / 2
        u = (I - c) * np.cos(ang) + (K - c) * np.sin(ang)
        v = -(I - c) * np.sin(ang) + (K - c) * np.cos(ang)
        lv.corridor((u > 12) & (u < 42) & (np.abs(v) <= 1.5), h=4)
        lv.room((u > 24) & (u < 30) & (np.abs(v) <= 4.5) & ~((u > 26) & (u < 28) & (np.abs(v) <= 0.5)), h=5)
        # niches along the outer side of the ring
        for t in np.linspace(0.2, 1.37, 6):
            na = ang + t - 0.08
            nx, nz = c + 45.5 * np.cos(na), c + 45.5 * np.sin(na)
            lv.room(np.hypot(I - nx, K - nz) <= 1.7, h=3)
        # a chapel at each diagonal, off the ring by a short passage
        ca = ang + np.pi / 4
        px, pz = c + 60 * np.cos(ca), c + 60 * np.sin(ca)
        lv.room(np.hypot(I - px, K - pz) <= 9, h=7)
        uu = (I - c) * np.cos(ca) + (K - c) * np.sin(ca)
        vv = -(I - c) * np.sin(ca) + (K - c) * np.cos(ca)
        lv.corridor((uu > 42) & (uu < 52) & (np.abs(vv) <= 1), h=3)
        # and an outer passage linking neighbouring chapels, for a second loop
        lv.corridor((r >= 66) & (r <= 67.5) & (np.abs(np.angle(np.exp(1j * (th - ca)))) < 0.9), h=3)
    doors(lv)
    return [lv], None


def descent():
    rng = np.random.default_rng(11)
    upper, lower = Level(32), Level(18)
    dungeon_level(upper, np.random.default_rng(12), loops=3)
    dungeon_level(lower, np.random.default_rng(13), loops=4)
    atrium = disc(80, 80, 12)
    for lv in (upper, lower):
        lv.kind[disc(80, 80, 20)] = ROCK                                   # a clear ring of rock round the atrium
        lv.height[disc(80, 80, 20)] = 0
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):                    # four passages out from it
            lv.corridor(lpath((80 + 15 * dx, 80 + 15 * dz), (80 + 34 * dx, 80 + 34 * dz), 3, rng, bend=dx != 0), h=3)
    upper.room(disc(80, 80, 16) & ~disc(80, 80, 12), h=5)                   # the gallery round the atrium
    lower.room(disc(80, 80, 14), h=19)                                    # the atrium's floor, open to the gallery
    stairs = []
    for (sx, sz), goal in (((30, 40), (80, 46)), ((128, 120), (80, 114))):   # two stairwells, a flight of 14 down
        run = rect(sx, sz, sx + 2, sz + 13)
        for lv in (upper, lower):
            lv.kind[run] = STAIR
            lv.height[run] = 4
        upper.corridor(lpath((sx + 1, sz), goal, 3, rng), h=3)
        lower.corridor(lpath((sx + 1, sz + 13), goal, 3, rng), h=3)
        stairs.append((sx, sz))
    for lv in (upper, lower):
        doors(lv)
    return [lower, upper], stairs


def bunker():
    lv = Level(20)
    T = lambda m, h=3: lv.corridor(m, h)                                  # noqa: E731
    # the spine, dog-legged so no straight sightline runs its length
    for a, b in [((14, 80), (50, 80)), ((50, 80), (50, 70)), ((50, 70), (100, 70)), ((100, 70), (100, 82)), ((100, 82), (146, 82))]:
        T(rect(min(a[0], b[0]) - 1, min(a[1], b[1]) - 1, max(a[0], b[0]) + 1, max(a[1], b[1]) + 1))
    # the entrance from the west: a chicane under a guard room's firing slit, then a blast door
    for a, b in [((2, 40), (14, 40)), ((14, 40), (14, 50)), ((14, 50), (6, 50)), ((6, 50), (6, 60)), ((6, 60), (14, 60)), ((14, 60), (14, 80))]:
        T(rect(min(a[0], b[0]) - 1, min(a[1], b[1]) - 1, max(a[0], b[0]) + 1, max(a[1], b[1]) + 1))
    lv.room(rect(18, 44, 26, 56), h=4)                                    # the guard room
    T(rect(21, 57, 22, 72)); T(rect(21, 71, 48, 72))                      # its own way in, from the spine side
    lv.kind[rect(16, 50, 17, 50)] = DOOR                                   # its slit onto the chicane (a gap a block high)
    lv.height[rect(16, 50, 17, 50)] = 1
    lv.kind[rect(13, 76, 15, 76)] = DOOR                                   # the blast door
    # barracks: a side corridor with cells either side
    T(rect(30, 84, 32, 120))
    for z in range(88, 120, 8):
        lv.room(rect(22, z, 28, z + 5), h=4); lv.room(rect(34, z, 40, z + 5), h=4)
        T(rect(29, z + 2, 29, z + 3)); T(rect(33, z + 2, 33, z + 3))        # a doorway into each cell
    # command centre: a hall with a raised dais, off the spine by a short dog-leg
    T(rect(74, 56, 76, 68)); T(rect(66, 54, 76, 56))
    lv.room(rect(56, 30, 92, 54), h=6)
    # generator hall and stores to the east
    T(rect(120, 84, 122, 100)); lv.room(rect(108, 100, 140, 124), h=8)
    T(rect(124, 60, 126, 80)); lv.room(rect(116, 40, 136, 60), h=5)
    # the escape tunnel: long, winding, a single width, out to the north-east
    lv.corridor(rect(136, 40, 140, 41), h=3)
    for a, b in [((140, 40), (140, 20)), ((140, 20), (110, 20)), ((110, 20), (110, 8)), ((110, 8), (150, 8))]:
        lv.corridor(rect(min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])), h=3)
    doors(lv)
    shafts = [(24, 50), (74, 42), (124, 112), (150, 8)]                    # air shafts and the escape hatch
    return [lv], shafts


def line():
    lv = Level(14)
    lv.corridor(rect(6, 76, 153, 80), h=5)                                # the main gallery
    lv.corridor(rect(6, 78, 153, 78), h=5)
    blocks = []
    for k, x in enumerate((24, 58, 96, 132)):                              # branches to the combat blocks
        zt = 30 if k % 2 == 0 else 128
        lv.corridor(rect(x - 1, min(zt, 76), x + 1, max(zt, 80)), h=3)
        lv.room(rect(x - 7, zt - 6, x + 7, zt + 6), h=6)                    # the block's base: a shaft climbs from here
        blocks.append((x, zt))
        lv.room(rect(x + 6, 83, x + 14, 92), h=4)                            # a magazine beside each branch
        lv.corridor(rect(x + 9, 81, x + 10, 82), h=3)
    lv.room(rect(70, 86, 90, 100), h=6)                                    # the barracks under the line
    lv.corridor(rect(79, 81, 81, 85), h=3)
    for x0, z in ((6, 78), (153, 78)):                                     # entrances at both ends, ramps up
        blocks.append((x0, z))
    doors(lv)
    return [lv], blocks


STUDIES = [dungeon, caverns, crypt, descent, bunker, line]


# --- measuring -------------------------------------------------------------------------------------------------------

def thin(mask):
    """Zhang-Suen thinning: a mask cut down to lines one cell wide."""
    m = np.pad(mask.astype(np.uint8), 1)
    while True:
        changed = False
        for step in (0, 1):
            P = [np.roll(np.roll(m, -dy, 0), -dx, 1) for dy, dx in
                 ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))]
            Bn = sum(P)
            A = sum(((P[i] == 0) & (P[(i + 1) % 8] == 1)) for i in range(8))
            c1 = (P[0] * P[2] * P[4] == 0) if step == 0 else (P[0] * P[2] * P[6] == 0)
            c2 = (P[2] * P[4] * P[6] == 0) if step == 0 else (P[0] * P[4] * P[6] == 0)
            rm = (m == 1) & (Bn >= 2) & (Bn <= 6) & (A == 1) & c1 & c2
            if rm.any():
                m[rm] = 0
                changed = True
        if not changed:
            return m[1:-1, 1:-1].astype(bool)


def measure(levels):
    walk = [(lv.kind != ROCK) & (lv.kind != PILLAR) for lv in levels]
    holes = 0
    for w in walk:
        lab, n = ndimage.label(~w, structure=np.ones((3, 3)))
        edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        holes += sum(1 for k in range(1, n + 1) if k not in edge and sizes[k - 1] >= 30)   # a pillar is no loop
    dead = 0
    for w in walk:
        sk = thin(w)
        nb = ndimage.convolve(sk.astype(int), np.ones((3, 3)), mode="constant") - sk
        dead += int((sk & (nb == 1)).sum())
    sight = 0
    for w in walk:
        for arr in (w, w.T):
            for row in arr:
                run = best = 0
                for v in row:
                    run = run + 1 if v else 0
                    best = max(best, run)
                sight = max(sight, best)
    # the longest walk: BFS from a far point twice, on the first level
    w = walk[0]
    start = tuple(np.argwhere(w)[0])
    def bfs(s):
        dist = np.full(w.shape, -1); dist[s] = 0; q = deque([s]); last = s
        while q:
            p = q.popleft(); last = p
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (p[0] + d[0], p[1] + d[1])
                if 0 <= n[0] < N and 0 <= n[1] < N and w[n] and dist[n] < 0:
                    dist[n] = dist[p] + 1; q.append(n)
        return last, dist
    far, _ = bfs(start)
    far2, dist = bfs(far)
    rooms = sum(int(ndimage.label(lv.kind == ROOM)[1]) for lv in levels)
    return dict(rooms=rooms, loops=holes, dead_ends=dead, sightline=sight, longest_walk=int(dist[far2]),
                open_cells=int(sum(w.sum() for w in walk)))


# --- building and drawing --------------------------------------------------------------------------------------------

def build(levels, extra):
    w = World(-N // 2, -N // 2, N, N, sy=64)
    w.ids[:, :SURFACE + 1, :] = B.WOOL
    w.dat[:, :SURFACE + 1, :] = 7
    w.dat[:, SURFACE, :] = 0                                               # the surface, pale
    ys = np.arange(64)[None, :, None]
    for lv in levels:
        open3 = ((lv.kind != ROCK) & (lv.kind != PILLAR))[:, None, :] & (ys > lv.floor) & (ys <= lv.floor + lv.height[:, None, :])
        w.ids[open3] = 0
        floor = ((lv.kind != ROCK) & (lv.kind != PILLAR))[:, None, :] & (ys == lv.floor)
        w.dat[floor] = 0
        w.dat[floor & (lv.kind == DOOR)[:, None, :]] = 12
        w.dat[floor & (lv.kind == STAIR)[:, None, :]] = 1
    air = w.ids == 0
    wall = (w.ids != 0) & ndimage.binary_dilation(air, np.ones((3, 1, 3)).astype(bool)) & (ys < SURFACE)
    w.dat[wall & (w.dat == 7)] = 8
    return w


def plan(levels, extra, title, out, scale=5):
    from pgmvox.core import blocks as K_
    tiles = []
    for lv in levels:
        img = np.zeros((N, N, 3), float)
        img[:] = (70, 72, 78)
        open_ = (lv.kind != ROCK) & (lv.kind != PILLAR)
        wall = ndimage.binary_dilation(open_, np.ones((3, 3))) & ~open_
        img[wall] = (30, 30, 34)
        tone = 245.0 - np.clip(lv.height.astype(float), 0, 14) * 5
        img[open_] = np.stack([tone, tone - 3, tone - 10], -1)[open_]
        img[lv.kind == DOOR] = (176, 110, 60)
        img[lv.kind == STAIR] = (200, 80, 80)
        im = Image.fromarray(img.astype(np.uint8).transpose(1, 0, 2)).resize((N * scale, N * scale), Image.NEAREST)
        d = ImageDraw.Draw(im)
        for x in range(0, N, 10):
            d.line([(x * scale, N * scale - 6), (x * scale, N * scale)], fill=(200, 200, 200))
        d.text((8, 6), f"{title}  floor y {lv.floor}  (north up; a tick every 10 blocks; paler = higher ceiling; "
                       f"brown door, red stair)", fill=(255, 255, 255))
        if extra:
            for ex, ez in extra:
                d.ellipse([ex * scale - 7, ez * scale - 7, ex * scale + 7, ez * scale + 7], outline=(90, 200, 255), width=3)
        tiles.append(im)
    W = sum(t.width for t in tiles) + 10 * (len(tiles) - 1)
    sheet = Image.new("RGB", (W, tiles[0].height), (20, 20, 24))
    x = 0
    for t in tiles:
        sheet.paste(t, (x, 0)); x += t.width + 10
    sheet.save(out)


def main(names):
    os.makedirs(OUT, exist_ok=True)
    for f in STUDIES:
        n = f.__name__
        if names and n not in names:
            continue
        levels, extra = f()
        m = measure(levels)
        plan(levels, extra, n, f"{OUT}/{n}-plan.png")
        w = build(levels, extra)
        for k, lv in enumerate(levels):
            tag = "" if len(levels) == 1 else f"-level{k}"
            render.iso(w.ids, w.dat, w.x0, w.z0, f"{OUT}/{n}{tag}-cut.png", 3, "se", ymin=lv.floor - 2, ymax=lv.floor + 3)
            render.trim(f"{OUT}/{n}{tag}-cut.png")
        print(f"{n:8s} " + "  ".join(f"{k} {v}" for k, v in m.items()))


if __name__ == "__main__":
    main(sys.argv[1:])
