"""The islands: each a disc of grass with a ragged outline and a gentle dome, over a cone of rock that hangs
beneath it and drips into spikes. Debris rocks are the same thing small. Vines trail off the rims, and
water falls off Highmoor and the Gardens into the void.

Fields are computed for red's islands only (all at x < 0) and written for red's half; gen.py turns them
onto blue.
"""
import numpy as np

import plan as P
from mc import B
from noise import fbm

RNG = np.random.default_rng(3131)


class Field:
    def __init__(self):
        self.x0, self.z0 = P.X_MIN, P.Z_MIN
        self.nx, self.nz = P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1
        xs = np.arange(P.X_MIN, P.X_MAX + 1); zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
        self.X, self.Z = np.meshgrid(xs, zs, indexing="ij")
        self.shape = self.X.shape
        self.red = self.X < 0


def outline(rng, r, rag):
    """A ragged radius as a function of angle: a few low harmonics with random phases."""
    ks = [(k, rng.uniform(0, 2 * np.pi), rng.uniform(0.4, 1.0) / k ** 0.7) for k in (2, 3, 5, 7)]
    norm = sum(a for _, _, a in ks)

    def rr(theta):
        return r * (1 + rag * sum(a * np.sin(k * theta + p) for k, p, a in ks) / norm)
    return rr


def build(F):
    X, Z = F.X.astype(float), F.Z.astype(float)
    H = np.full(F.shape, -1, int)       # the grass
    Bot = np.full(F.shape, -1, int)     # the lowest rock
    key = np.full(F.shape, "", object)
    small = fbm(F.shape, 6, 2, seed=1)
    spikes = fbm(F.shape, 3, 2, seed=2)
    lumpy = fbm(F.shape, 9, 2, seed=3)
    rocks = [(i["key"], i["at"], i["r"], i["top"], i["deep"], i["rag"]) for i in P.ISLANDS]
    rocks += [(f"debris{k}", (x, z), r, y, 1.8, 0.3) for k, (x, z, y, r) in enumerate(P.DEBRIS)]
    F.edge = {}
    for n, (k, (cx, cz), r, top, deep, rag) in enumerate(rocks):
        rng = np.random.default_rng(100 + n)
        rr = outline(rng, r, rag)
        d = np.hypot(X - cx, Z - cz)
        th = np.arctan2(Z - cz, X - cx)
        R = rr(th)
        t = d / R
        inside = (t < 1) & (X < 0)
        dome = 1.6 * np.clip(1 - t ** 2, 0, 1) * min(1.0, r / 8)
        h = top + dome + 0.9 * small - 1.0 * (t > 0.86)
        depth = 2 + deep * r * (1 - np.clip(t, 0, 1)) ** 0.75 * (0.75 + 0.5 * lumpy)
        depth = depth + np.where(spikes > 0.35, 6 * (spikes - 0.35) / 0.65 * r / 6, 0) * (t < 0.85)
        hh = np.round(h).astype(int)
        bb = np.round(h - depth).astype(int)
        H = np.where(inside, hh, H)
        Bot = np.where(inside, bb, Bot)
        key = np.where(inside, k, key)
    F.H, F.B, F.key = H, Bot, key
    F.land = H > 0
    return F


def write(w, F):
    """Stone from the bottom up in streaks of granite and andesite, dirt under the grass, then vines
    trailing off the hanging rock and water falling off two rims."""
    streak = fbm(F.shape, 5, 2, seed=7)
    r = RNG.random(F.shape)
    for ix in range(F.nx):
        for iz in range(F.nz):
            if not F.land[ix, iz]:
                continue
            x, z = F.x0 + ix, F.z0 + iz
            top, bot = int(F.H[ix, iz]), int(F.B[ix, iz])
            ci = w.ids[x - w.x0, :, z - w.z0]
            cd = w.dat[x - w.x0, :, z - w.z0]
            ys = np.arange(bot, top + 1)
            ci[bot:top + 1] = B.STONE
            band = (ys + int(4 * streak[ix, iz])) % 9
            cd[bot:top + 1] = np.where(band < 2, 1, np.where(band < 4, 5, 0))
            ci[max(bot, top - 3):top] = B.DIRT
            cd[max(bot, top - 3):top] = 0
            ci[top], cd[top] = B.GRASS, 0
            if r[ix, iz] < 0.12:
                ci[top + 1], cd[top + 1] = B.TALLGRASS, 1
            elif r[ix, iz] < 0.135:
                ci[top + 1], cd[top + 1] = (B.FLOWER, int(RNG.choice([0, 3, 8, 1]))) if r[ix, iz] < 0.128 else (B.DANDELION, 0)
    vines(w, F)


def vines(w, F):
    """Vines on the hanging rock's outer faces, trailing down a few blocks from where they catch."""
    sides = ((0, 1, 1), (-1, 0, 2), (0, -1, 4), (1, 0, 8))      # the neighbour the vine hangs on, and its bit
    rng = np.random.default_rng(55)
    for ix in range(1, F.nx - 1):
        for iz in range(1, F.nz - 1):
            if F.land[ix, iz] or not F.red[ix, iz]:
                continue
            x, z = F.x0 + ix, F.z0 + iz
            for dx, dz, bit in sides:
                jx, jz = ix + dx, iz + dz
                if not F.land[jx, jz] or rng.random() > 0.22:
                    continue
                top = int(F.H[jx, jz])
                y = top - 1 - int(rng.integers(0, 3))
                n = int(rng.integers(2, 9))
                for k in range(n):
                    yy = y - k
                    if w.id(x, yy, z) != B.AIR:
                        break
                    w.set(x, yy, z, B.VINE, bit)
                break


def waterfall(w, F, x, z, drop=46):
    """A spring at the rim of an island and the water falling off it: a source in a notch in the grass, and
    a falling column over the edge into the void, which simply ends."""
    ix, iz = x - F.x0, z - F.z0
    top = int(F.H[ix, iz])
    # walk outward along the steepest way off the island to the first air column
    best = None
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for k in range(1, 16):
            jx, jz = ix + dx * k, iz + dz * k
            if not F.land[jx, jz]:
                if best is None or k < best[2]:
                    best = (dx, dz, k)
                break
    dx, dz, k = best
    for i in range(0, k):
        X, Z = x + dx * i, z + dz * i
        top = int(F.H[X - F.x0, Z - F.z0]) if i else top
        w.set(X, top, Z, B.WATER, 0)
        w.set(X, top + 1, Z, B.AIR)
        for sx, sz in ((dz, dx), (-dz, -dx)):
            if w.id(X + sx, top, Z + sz) in (B.GRASS, B.DIRT):
                w.set(X + sx, top, Z + sz, B.MOSSY)
    X, Z = x + dx * k, z + dz * k
    for y in range(top - drop, top + 1):
        if w.id(X, y, Z) == B.AIR or w.id(X, y, Z) == B.VINE:
            w.set(X, y, Z, B.WATER_FLOW, 8)
    return (X, Z)


def paint_biomes(w, F):
    w.biome[:, :] = 1
