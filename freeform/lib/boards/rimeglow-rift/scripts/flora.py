"""What grows on the ground: spruce in the north and autumn oak in the south, each half's wood drawn once on the north
half's sites and written twice, with the species traded on the banks of the rift where fire and ice meet."""
import math

import numpy as np
from scipy import ndimage

import land as LD
from pgmvox import B
from pgmvox.scenery import trees as TR

CLAY_ORANGE, CLAY_RED, CLAY_YELLOW, CLAY_BROWN = (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 14), (B.STAINED_CLAY, 4), (B.STAINED_CLAY, 12)
CROWNS = {                                   # one dominant colour and a second, by tree
    "ember": (CLAY_ORANGE, CLAY_RED),
    "gold": (CLAY_YELLOW, CLAY_ORANGE),
    "crimson": (CLAY_RED, CLAY_ORANGE),
    "rust": (CLAY_ORANGE, CLAY_BROWN),
}
LITTER = {"ember": (1, 14), "gold": (4, 1), "crimson": (14, 12), "rust": (1, 12)}      # carpet colours


def _free(w, x, y, z):
    return w.id(x, y, z) in (B.AIR, B.TALLGRASS, B.SNOW_LAYER, B.DEADBUSH, B.CARPET)


def spruce(w, x, z, y0, h, rng, radius=3):
    """A spruce: a trunk of spruce log, tiers of needles widening down, snow settled on the tiers' tops."""
    for y in range(y0 + 1, y0 + h + 1):
        w.set(x, y, z, B.LOG, 1)
    top = y0 + h
    for j in range(0, h - 1):
        y = top - j
        r = min(radius, (j + 1) // 2 + (1 if j > 0 else 0))
        if j == 0:
            r = 0
        if j % 2 == 1 and j > 2:
            r = max(1, r - 1)
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) == r and abs(dz) == r and r >= 2:
                    continue
                if (dx or dz or j == 0) and _free(w, x + dx, y, z + dz):
                    w.set(x + dx, y, z + dz, B.LEAVES, 5)
                elif dx == 0 and dz == 0:
                    pass
    w.set(x, top + 1, z, B.LEAVES, 5)
    for dx in range(-radius - 1, radius + 2):
        for dz in range(-radius - 1, radius + 2):
            for y in range(y0 + 3, top + 2):
                if w.id(x + dx, y, z + dz) == B.LEAVES and w.id(x + dx, y + 1, z + dz) == B.AIR \
                        and rng.random() < 0.55:
                    w.set(x + dx, y + 1, z + dz, B.SNOW_LAYER, int(rng.integers(0, 2)))


def autumn_oak(w, x, z, y0, h, rng, tone="ember", rx=None):
    """An autumn oak: a bent trunk, a crown of leaf with its outer shell in the tree's own colours, and the leaves it
    has dropped lying round its foot as carpet."""
    a, b = CROWNS[tone]
    rx = rx or (3.0 + rng.random() * 1.6)
    ry = rx * (0.72 + 0.2 * rng.random())
    lean = rng.integers(-1, 2, 2)
    cx, cz = x, z
    for k in range(1, h + 1):
        if k == h // 2 + 1:
            cx, cz = x + int(lean[0]), z + int(lean[1])
        w.set(cx if k > h // 2 else x, y0 + k, cz if k > h // 2 else z, B.LOG, 0)
    cy = y0 + h + 1
    for dx in range(-int(rx) - 2, int(rx) + 3):
        for dy in range(-int(ry) - 2, int(ry) + 3):
            for dz in range(-int(rx) - 2, int(rx) + 3):
                d = (dx / rx) ** 2 + (dy / ry) ** 2 + (dz / rx) ** 2
                if d <= 1.0 + 0.3 * (rng.random() - 0.5) and _free(w, cx + dx, cy + dy, cz + dz):
                    if d > 0.42 and rng.random() < 0.62:
                        blk = a if rng.random() < 0.8 else b
                    else:
                        blk = (B.LEAVES, 4)
                    w.set(cx + dx, cy + dy, cz + dz, *blk)
    litter = LITTER[tone]
    for dx in range(-5, 6):
        for dz in range(-5, 6):
            r = math.hypot(dx, dz)
            if 1.5 < r < 4.8 and rng.random() < 0.42:
                gx, gz = x + dx, z + dz
                gy = w.top(gx, gz)
                if gy > 0 and w.id(gx, gy, gz) in (B.GRASS, B.DIRT, B.SAND, B.HARDENED_CLAY, B.STAINED_CLAY) \
                        and w.id(gx, gy + 1, gz) == B.AIR:
                    w.set(gx, gy + 1, gz, B.CARPET, litter[int(rng.integers(0, 2))])


def needle_floor(w, x, z, rng):
    """Podzol under a spruce: the forest floor where needles lie, showing through the snow."""
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if math.hypot(dx, dz) < 2.4 and rng.random() < 0.7:
                gy = w.top(x + dx, z + dz)
                if gy > 0 and w.id(x + dx, gy, z + dz) in (B.SNOW, B.GRASS, B.DIRT):
                    w.set(x + dx, gy, z + dz, B.DIRT, 2)


def boulder(w, x, z, y0, r, rng, blocks):
    """One rock: an ellipsoid sunk into the ground, drawn from one family."""
    for dx in range(-r - 1, r + 2):
        for dz in range(-r - 1, r + 2):
            for dy in range(-1, r + 1):
                d = (dx / (r + 0.2)) ** 2 + (dy / max(1.0, r * 0.7)) ** 2 + (dz / (r + 0.2)) ** 2
                if d <= 1.0 + 0.25 * (rng.random() - 0.5):
                    y = y0 + dy
                    if _free(w, x + dx, y, z + dz) or (dy < 0):
                        w.set(x + dx, y, z + dz, *blocks[int(rng.integers(0, len(blocks)))])


def sites(ctx, rng, mask, n, spacing, taken):
    """Up to n points over a mask, none nearer than `spacing` to each other or to `taken`."""
    cells = np.argwhere(mask)
    rng.shuffle(cells)
    out = []
    pts = list(taken)
    for i, k in cells:
        p = (i + LD.X0, k + LD.Z0)
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= spacing ** 2 for q in pts):
            out.append(p)
            pts.append(p)
            if len(out) >= n:
                break
    return out


def masks(ctx, structures):
    """Where a tree may stand in the north half: ground that is gentle, off every road and building."""
    X, Z, H, deg, land, laid = ctx["X"], ctx["Z"], ctx["H"], ctx["deg"], ctx["land"], ctx["laid"]
    near_road = ndimage.binary_dilation(laid, iterations=2)
    ok = land & (deg < 44) & ~near_road & (Z < -12) & ~ctx["rift"] & (ctx["ed"] > 2)
    ok &= structures
    return ok
