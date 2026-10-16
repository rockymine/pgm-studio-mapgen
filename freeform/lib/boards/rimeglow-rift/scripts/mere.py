"""The two meres: a frozen one in the north and its half turn, a cooled lava lake in the south, each flat for the reason
it is flat, and what stands on them."""
import math

import numpy as np

import land as LD
from pgmvox import B
from pgmvox.geom import noise
from stamp import AIR, Stamp

LEVEL = LD.LAKE["level"]


def surface(w, ctx):
    X, Z, H = ctx["X"], ctx["Z"], ctx["H"]
    mask = LD.mere_mask(X, Z) & ctx["land"]
    crack = np.clip(1 - np.abs(noise.fbm(X.shape, 15, 3, seed=81)), 0, 1)
    patch = noise.fbm(X.shape, 9, 2, seed=82)
    n = 0
    for i, k in np.argwhere(mask):
        x, z = int(X[i, k]), int(Z[i, k])
        h = int(H[i, k])
        if z < 0:                                           # frozen: packed ice, in sheets of clear ice, cracked
            if crack[i, k] > 0.955:
                top, under = (B.ICE, 0), (B.PACKED_ICE, 0)
            elif patch[i, k] > 0.38:
                top, under = (B.SNOW, 0), (B.PACKED_ICE, 0)
            else:
                top, under = (B.PACKED_ICE, 0), (B.PACKED_ICE, 0)
        else:                                               # cooled: grey and black clay, orange in the cracks
            if crack[i, k] > 0.955:
                top, under = ((B.STAINED_CLAY, 1) if (x + z) % 5 else (B.GLOWSTONE, 0)), (B.STAINED_CLAY, 15)
            elif patch[i, k] > 0.38:
                top, under = ((B.SOUL_SAND, 0) if patch[i, k] > 0.55 else (B.COAL_BLOCK, 0)), (B.STAINED_CLAY, 15)
            else:
                top, under = ((B.STAINED_CLAY, 7) if (x // 2 + z // 2) % 3 else (B.STAINED_CLAY, 15)), (B.STAINED_CLAY, 15)
        w.ids[i, h, k], w.dat[i, h, k] = top
        for y in (h - 1, h - 2):
            w.ids[i, y, k], w.dat[i, y, k] = under
        for y in range(h + 1, h + 4):                       # clear whatever the paint left standing over it
            w.ids[i, y, k] = 0
            w.dat[i, y, k] = 0
        n += 1
    return n


def hut(S, x0, z0):
    """An ice-fishing hut: spruce, a slab roof, a door to the south, a hole in the ice inside it."""
    f = LEVEL
    for x in range(x0, x0 + 5):
        for z in range(z0, z0 + 4):
            edge = x in (x0, x0 + 4) or z in (z0, z0 + 3)
            S.set(x, f, z, "plank")
            for y in range(f + 1, f + 4):
                S.set(x, y, z, ("plank" if y != f + 3 else "log") if edge else AIR)
            S.set(x, f + 4, z, "roof_slab")
    for y in (f + 1, f + 2):
        S.set(x0 + 2, y, z0 + 3, AIR)
    S.door(x0 + 2, f + 1, z0 + 3, "s")
    S.set(x0 + 1, f + 2, z0, "pane"); S.set(x0 + 3, f + 2, z0, "pane")
    S.set(x0 + 1, f, z0 + 1, AIR); S.set(x0 + 1, f - 1, z0 + 1, (B.WATER, 0))      # the hole
    S.set(x0 + 3, f + 1, z0 + 1, "slab")
    S.torch(x0 + 2, f + 2, z0 + 1) if False else None
    S.set(x0 + 4 - 1, f + 3, z0 + 2, "light")
    for z in range(z0 - 1, z0 + 5):                                  # a roof of the eaves, with fish drying beneath
        S.set(x0 - 1, f + 4, z, "roof_slab") if False else None


def kiln(S, x0, z0):
    """A charcoal kiln: a beehive of nether brick and orange clay with a chimney and an arched mouth to the south."""
    f = LEVEL
    cx, cz = x0 + 2, z0 + 2
    for x in range(x0 - 1, x0 + 6):
        for z in range(z0 - 1, z0 + 6):
            r = math.hypot(x - cx, z - cz)
            for y in range(f, f + 6):
                ry = y - f
                lim = 3.4 - 0.65 * ry
                if r <= lim and r > lim - 1.3:
                    S.set(x, y, z, ("wall", "hot", "wall")[(x + z + y) % 3] if ry < 4 else "hot")
                elif r <= lim - 1.3:
                    S.set(x, y, z, AIR if ry > 0 else "wall")
    for y in range(f + 3, f + 9):
        S.set(cx, y, cz, "wall")
    S.set(cx, f + 9, cz, (B.NETHERRACK, 0))
    S.set(cx, f + 10, cz, (B.FIRE, 0))
    for y in (f + 1, f + 2):
        for x in (cx - 0, cx + 0):
            S.set(x, y, cz + 3, AIR)
            S.set(x, y, cz + 2, AIR)
    S.set(cx, f + 1, cz, (B.NETHERRACK, 0)); S.set(cx, f + 2, cz, (B.FIRE, 0))


def ridge(S, pts, rng):
    """A pressure ridge: a line of blocks one or two high with gaps, the heave where the ice (or the crust) buckled."""
    for (xa, za), (xb, zb) in zip(pts, pts[1:]):
        n = int(max(abs(xb - xa), abs(zb - za)))
        for s in range(n + 1):
            x = int(round(xa + (xb - xa) * s / max(n, 1)))
            z = int(round(za + (zb - za) * s / max(n, 1)))
            if (s % 9) in (4, 5):
                continue
            hgt = 1 + int(rng.integers(0, 2)) + (1 if s % 7 == 0 else 0)
            for y in range(LEVEL + 1, LEVEL + 1 + hgt):
                S.set(x, y, z, "pressure")
            if rng.random() < 0.4:
                S.set(x + 1, LEVEL + 1, z, "pressure")


def henge(S, cx, cz, rng):
    """Stones standing in a ring: tall, irregular, one capped, the mere's landmark."""
    for k in range(7):
        a = 2 * math.pi * k / 7 + 0.3
        x, z = int(round(cx + 7 * math.cos(a))), int(round(cz + 5.5 * math.sin(a)))
        hgt = int(rng.integers(4, 8))
        for y in range(LEVEL + 1, LEVEL + 1 + hgt):
            S.set(x, y, z, "menhir")
            if y < LEVEL + 1 + hgt - 2 and rng.random() < 0.6:
                S.set(x + 1, y, z, "menhir")
        S.set(x, LEVEL + hgt, z, "menhir")


def build(w, ctx):
    n = surface(w, ctx)
    rng = np.random.default_rng(8)
    for south in (False, True):
        S = Stamp(w, south)
        (kiln if south else hut)(S, -22, -48)
        (kiln if south else hut)(S, 4, -37)
        ridge(S, [(-30, -38), (-22, -34), (-12, -38), (-4, -32)], rng)
        ridge(S, [(-14, -52), (-6, -49), (4, -52), (12, -48)], rng)
        henge(S, -8, -42, rng)
    return n
