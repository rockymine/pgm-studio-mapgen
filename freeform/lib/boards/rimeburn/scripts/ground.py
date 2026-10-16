"""Rimeburn's ground laid as Frost's: rock in beds, soil by slope, and a top chosen by the angle of the ground,
then by place. The Ember half is this same ground re-seasoned (season.py), so everything here is winter.

    the top, flat to steep    snow (packed ice inset in patches) < 26 deg < bare rock and scree < 40 deg < the beds
    the Hearth Hollow         thawed: wet litter of podzol and coarse dirt, no snow, the fire's warmth
    a path                    andesite, cobblestone and polished andesite, a third each (season.py warms it)
    the water                 ice at its surface over still water and a clay bed
"""
import numpy as np

import land as LD
from pgmvox import B
from pgmvox.geom import noise
from pgmvox.geom import shapes
from pgmvox.surface import terrain as T

ROCK_BEDS = [(B.STONE, 0), (B.STONE, 0), (B.STONE, 5), (B.STONE, 0), (B.STONE, 5), (B.STONE, 5), (B.COBBLE, 0),
             (B.STONE, 0), (B.STONE, 5), (B.STONE, 0)]
PATH = [(B.STONE, 5), (B.COBBLE, 0), (B.STONE, 6)]
SNOW_LINE_EMBER = 58          # above this the Ember half keeps its snow: the first of the winter on its peaks


def path_mask(X, Z, paths, width=3.2, seed=0):
    """Every path's band, wandering a little between its points, Frost's half then its image."""
    m = np.zeros(X.shape, bool)
    for k, pts in enumerate(paths.values()):
        fine = []
        for (ax, az), (bx, bz) in zip(pts, pts[1:]):
            n = max(2, int(np.hypot(bx - ax, bz - az) // 2))
            for t in np.linspace(0, 1, n, endpoint=False):
                fine.append((ax + (bx - ax) * t, az + (bz - az) * t))
        fine.append(pts[-1])
        fine = np.array(fine)
        wob = noise.fbm((len(fine),), 7, 2, seed=seed + k) * 1.6
        dx = np.gradient(fine[:, 0]); dz = np.gradient(fine[:, 1])
        ln = np.hypot(dx, dz) + 1e-9
        ease = np.minimum(1, np.minimum(np.arange(len(fine)), np.arange(len(fine))[::-1]) / 4)
        fine[:, 0] += -dz / ln * wob * ease
        fine[:, 1] += dx / ln * wob * ease
        d, _ = shapes.polyline(X, Z, [tuple(p) for p in fine])
        m |= d <= width / 2
    m &= Z < 0
    return LD.SYM.field(m, keep=Z < 0).astype(bool)


def lay(w, X, Z, H, land, water, surface, paths, ramps):
    """Lay every column of the board as Frost's ground. Returns the slope read and the masks the later stages
    paint by: {"path", "hollow", "patch"}."""
    deg = T.slope_deg(np.where(land, H, H.min()), land)
    sx, sz = H.shape
    n_bed = T.bed_offset(H.shape, dip=(0.03, 0.05), fold=2.0, cell=30, seed=LD.SEED + 20,
                         drape=(np.where(land, H, 36), 0.35, 10))
    rough = 3.0 * noise.fbm(H.shape, 10, 3, seed=LD.SEED + 21)
    pad = 6                                             # the board's edge is void too, not more rock
    top_p = np.pad(np.where(land, H, 0).astype(float), pad)
    land_p = np.pad(land, pad)
    bottom = T.island_bottom(top_p, land_p, np.zeros_like(land_p), taper=(4, 0.85), rough=np.pad(rough, pad),
                             floor=6)[pad:-pad, pad:-pad]
    # the rock under the Vent runs deep, a buttress the passage is cut through, its mouth a hole in the cliff
    dv, _ = shapes.polyline(X, Z, [(x, z) for x, y, z in LD.VENT])
    bottom = np.where(dv < 6, np.minimum(bottom, 22 + (dv * 1.5).astype(int)), bottom)
    patch_field = noise.fbm(H.shape, 5, 3, seed=LD.SEED + 22)
    fleck = noise.fbm(H.shape, 3, 2, seed=LD.SEED + 23)
    hollow_d = np.hypot(X - LD.HEARTH[0], Z - LD.HEARTH[1]) * (1 + 0.1 * noise.fbm(H.shape, 6, 2, seed=LD.SEED + 24))
    hollow = (hollow_d < 13.5) & land
    hollow = LD.SYM.field(hollow & (Z < 0), keep=Z < 0).astype(bool)
    path = path_mask(X, Z, paths) & land & ~water
    rampm = np.zeros_like(land)
    for m in ramps.values():
        rampm |= m
    patch = (patch_field > 0.42) & ~hollow & ~path
    rng = np.random.default_rng(LD.SEED + 25)
    for i in range(sx):
        for k in range(sz):
            if not land[i, k]:
                continue
            h = int(H[i, k])
            b = int(min(bottom[i, k], h - 2))
            dg = int(deg[i, k])
            soil = 0 if dg > 40 else 1 if dg > 32 else 3
            for y in range(b, h - soil + 1):
                blk = ROCK_BEDS[(y + int(n_bed[i, k])) // 2 % len(ROCK_BEDS)]
                if blk == (B.STONE, 0) and fleck[i, k] > 0.55 and (y % 3 == 0):
                    blk = (B.COBBLE, 0)
                w.ids[i, y, k], w.dat[i, y, k] = blk
            for y in range(h - soil + 1, h):
                w.ids[i, y, k], w.dat[i, y, k] = (B.DIRT, 0) if (y + i + k) % 3 else (B.DIRT, 1)
            if water[i, k] and int(surface[i, k]) - h <= 3:
                s = max(int(surface[i, k]), h + 1)
                w.ids[i, h, k], w.dat[i, h, k] = B.CLAY, 0
                for y in range(h + 1, s):
                    w.ids[i, y, k], w.dat[i, y, k] = B.WATER, 0
                w.ids[i, max(s, h + 1), k], w.dat[i, max(s, h + 1), k] = B.ICE, 0
                continue
            if rampm[i, k]:
                top = (B.STONE, 5)
            elif path[i, k]:
                top = PATH[int(rng.integers(3))]
            elif hollow[i, k] and dg <= 40:
                top = (B.DIRT, 2) if (patch_field[i, k] + 0.3 * fleck[i, k]) > -0.05 else (B.DIRT, 1)
            elif dg > 40:
                top = ROCK_BEDS[(h + int(n_bed[i, k])) // 2 % len(ROCK_BEDS)]
            elif dg > 32:
                top = [(B.STONE, 0), (B.STONE, 5), (B.GRAVEL, 0)][int(rng.integers(3))] if fleck[i, k] < 0.3 \
                    else (B.STONE, 5)
            elif patch[i, k]:
                top = (B.PACKED_ICE, 0)
            else:
                top = (B.SNOW, 0)
            w.ids[i, h, k], w.dat[i, h, k] = top
            if top == (B.SNOW, 0) or (top[0] in (B.STONE, B.GRAVEL) and dg <= 32 and fleck[i, k] < -0.2):
                w.ids[i, h + 1, k], w.dat[i, h + 1, k] = B.SNOW_LAYER, 0
    weirs(w, H, land, water, surface)
    return deg, {"path": path, "hollow": hollow, "patch": patch, "ramp": rampm}


def weirs(w, H, land, water, surface):
    """Where the burn steps down, the lower cell takes a sill of stones up to the higher water's surface, so no
    water stands against air: riffle stones at every fall."""
    stones = [(B.STONE, 5), (B.COBBLE, 0), (B.STONE, 0)]
    wet = water & land & (surface - H <= 3)
    eff = np.maximum(surface, H + 1)
    for i, k in np.argwhere(wet):
        s = int(eff[i, k])
        for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, k + dk
            if not (0 <= a < H.shape[0] and 0 <= b < H.shape[1]) or not land[a, b]:
                continue
            lo = int(eff[a, b]) if wet[a, b] else int(H[a, b])
            if lo >= s:
                continue
            for y in range(lo + 1, s + 1):
                w.ids[a, y, b], w.dat[a, y, b] = stones[(a * 7 + b * 3 + y) % 3]
