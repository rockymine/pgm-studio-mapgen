"""Small built things every board of this set wanted and the library does not have: Poisson scatter of points over a
mask, dead and live trees from a few blocks, rubble, braziers, a masonry tower with a ladder and a crown, a row of
lamps along a route, a plank bridge. Written here first; a thing written by a second board belongs in pgmvox
(see the friction log in REPORT.md).
"""
import math

import numpy as np

import plan  # noqa: F401  (puts the library on the path)
from pgmvox import B
from pgmvox.orient import ladder as ladder_data, stair as stair_data, vec


def scatter_points(mask, n, min_d, rng, X, Z, taken=()):
    """Up to n points (x, z) over the cells of a mask, none nearer than min_d to another or to `taken`."""
    cells = np.argwhere(mask)
    order = rng.permutation(len(cells))
    pts = list(taken)
    out = []
    for j in order:
        i, k = cells[j]
        p = (int(X[i, k]), int(Z[i, k]))
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) >= min_d for q in pts):
            pts.append(p)
            out.append(p)
            if len(out) >= n:
                break
    return out


def log_axis(kind, direction):
    """A LOG/LOG2 data value lying along a direction (dx, dz): bit 4 along x, 8 along z."""
    return kind | (4 if abs(direction[0]) >= abs(direction[1]) else 8)


def dead_tree(w, x, y, z, rng, h, log=B.LOG2, kind=1):
    """A bare tree: a trunk h high from the ground at y, three to five arms leaning out of its upper half, each
    ending in a stub. No leaves."""
    for k in range(1, h + 1):
        w.set(x, y + k, z, log, kind)
    n = int(rng.integers(3, 6))
    for _ in range(n):
        a = rng.uniform(0, 2 * math.pi)
        dx, dz = round(math.cos(a)), round(math.sin(a))
        if (dx, dz) == (0, 0):
            dx = 1
        y0 = y + int(rng.integers(max(2, h // 2), h))
        L = int(rng.integers(2, 4))
        for s in range(1, L + 1):
            bx, bz, by = x + dx * s, z + dz * s, y0 + (s // 2)
            if w.id(bx, by, bz) in (B.AIR, B.TALLGRASS, B.DEADBUSH):
                w.set(bx, by, bz, log, log_axis(kind, (dx, dz)) if s < L else kind)
        if rng.random() < 0.5:
            w.set(x + dx * L, y0 + L // 2 + 1, z + dz * L, log, kind)


def rubble(w, x, y, z, rng, r=1.6, blocks=((B.STONE, 5), (B.COBBLE, 0), (B.STONE, 0), (B.GRAVEL, 0))):
    """A heap of loose stone: a low blob on the ground at y."""
    R = int(math.ceil(r))
    for dx in range(-R, R + 1):
        for dz in range(-R, R + 1):
            d = math.hypot(dx, dz) + rng.uniform(-0.4, 0.4)
            if d <= r:
                top = int(round((r - d) * 0.9)) + (1 if rng.random() < 0.5 else 0)
                for k in range(1, max(1, top) + 1):
                    if w.id(x + dx, y + k, z + dz) in (B.AIR, B.TALLGRASS, B.DEADBUSH) and \
                            w.id(x + dx, y + k - 1, z + dz) not in (B.AIR, B.TALLGRASS, B.DEADBUSH, B.WATER):
                        w.set(x + dx, y + k, z + dz, *blocks[int(rng.integers(len(blocks)))])


def brazier(w, x, y, z, post=(B.NETHER_FENCE, 0), light=(B.GLOWSTONE, 0), height=2, base=(B.COBBLE_WALL, 0)):
    """A post on a stone footing, a light on top."""
    w.set(x, y + 1, z, *base)
    for k in range(2, height + 1):
        w.set(x, y + k, z, *post)
    w.set(x, y + height + 1, z, *light)


def tower(w, x0, z0, x1, z1, y0, height, wall=((B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 2)),
          corner=(B.STONEBRICK, 3), floor=(B.PLANKS, 5), slit=(B.IRON_BARS, 0), door=B.DARK_OAK_DOOR, door_side="s",
          crown=(B.STONEBRICK, 0), crenel=(B.COBBLE_WALL, 0), light=(B.GLOWSTONE, 0), rng=None, ladder_on="n"):
    """A hollow masonry tower: walls from y0 + 1 to y0 + height, a floor every five courses, a ladder up the inside
    of one wall, iron-barred slits on every face, a door at the foot, a crenellated crown with a light in it."""
    rng = rng or np.random.default_rng(1)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            cornerp = x in (x0, x1) and z in (z0, z1)
            for y in range(y0 - 3, y0 + 1):
                w.set(x, y, z, B.STONEBRICK, 0)
            for y in range(y0 + 1, y0 + height + 1):
                if cornerp:
                    w.set(x, y, z, *corner)
                elif edge:
                    t = y - y0
                    if t % 5 in (3, 4) and ((x - x0 + z - z0) % 3 == 1) and t > 2:
                        w.set(x, y, z, *slit)
                    else:
                        w.set(x, y, z, *wall[int(rng.integers(len(wall)))])
                else:
                    w.set(x, y, z, B.AIR)
            if not edge:
                w.set(x, y0, z, *floor)
                for t in range(5, height, 5):
                    w.set(x, y0 + t, z, *floor)
                w.set(x, y0 + height, z, *floor)
    # the ladder on the inside of the wall at `ladder_on`
    lx = (x0 + x1) // 2
    lz = (z0 + z1) // 2
    px, pz = {"n": (lx, z0 + 1), "s": (lx, z1 - 1), "w": (x0 + 1, lz), "e": (x1 - 1, lz)}[ladder_on]
    face = {"n": "s", "s": "n", "w": "e", "e": "w"}[ladder_on]
    for y in range(y0 + 1, y0 + height + 1):
        w.set(px, y, pz, B.LADDER, ladder_data(ladder_on))
    for t in range(5, height + 1, 5):                 # a hatch in each floor over the ladder
        w.set(px, y0 + t, pz, B.LADDER, ladder_data(ladder_on))
    # the door
    dx_, dz_ = {"n": ((x0 + x1) // 2, z0), "s": ((x0 + x1) // 2, z1), "w": (x0, (z0 + z1) // 2),
                "e": (x1, (z0 + z1) // 2)}[door_side]
    from pgmvox.orient import door as door_data
    w.set(dx_, y0 + 1, dz_, door, door_data(door_side))
    w.set(dx_, y0 + 2, dz_, door, door_data(door_side, upper=True))
    # the crown: a parapet round, crenels every other block, a light in the middle
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                w.set(x, y0 + height + 1, z, *crown)
                if (x + z) % 2 == 0:
                    w.set(x, y0 + height + 2, z, *crenel)
    cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
    w.set(cx, y0 + height + 1, cz, B.NETHER_FENCE, 0)
    w.set(cx, y0 + height + 2, cz, *light)
    return (px, pz)


def lamps(w, line, H, X, Z, every=12, post=(B.NETHER_FENCE, 0), light=(B.GLOWSTONE, 0), height=2, side=3.0, start=6):
    """Lamp posts beside a route every so many blocks, alternating sides. `line` is the route's polyline."""
    from pgmvox.shapes import point_at
    from pgmvox import shapes
    total = shapes.length(line)
    s, n = start, 0
    out = []
    while s < total:
        (px, pz), (hx, hz) = point_at(line, s)
        nx, nz = -hz, hx
        sg = 1 if n % 2 == 0 else -1
        x, z = int(round(px + sg * side * nx)), int(round(pz + sg * side * nz))
        i, k = x - int(X[0, 0]), z - int(Z[0, 0])
        if 0 <= i < H.shape[0] and 0 <= k < H.shape[1] and H[i, k] > 0:
            y = int(H[i, k])
            for t in range(1, height + 1):
                w.set(x, y + t, z, *post)
            w.set(x, y + height + 1, z, *light)
            out.append((x, z))
        s += every
        n += 1
    return out
