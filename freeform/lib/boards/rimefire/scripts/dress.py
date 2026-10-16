"""Ground cover and growth for both skins.

Warm ground grows the autumn wood: oak, birch and dark oak with their crowns turned to the colours of a dying year, a
litter of fallen leaves under them and dead bushes on the poor ground. Cold ground grows spruce and pine with snow
lying on the boughs, ferns beneath, and drifts. Where the skins meet, both grow, each at half the density.
"""
import os

import numpy as np

os.environ.setdefault("PGM_STUDIO_ROOT", "/home/user/pgm-studio")

from pgmvox import B, rng
from pgmvox.geom import noise, shapes
from pgmvox.scenery import trees as T

import land as LND

LEAVES = (B.LEAVES, B.LEAVES2)
GIVE = T.GIVES_WAY | {B.SNOW, B.PACKED_ICE, B.STAINED_CLAY, B.HARDENED_CLAY, B.RED_SANDSTONE, B.SAND, B.CARPET}
HUES = [(None, 0.16), ((B.STAINED_CLAY, 1), 0.28), ((B.STAINED_CLAY, 4), 0.24), ((B.STAINED_CLAY, 14), 0.16),
        ((B.HARDENED_CLAY, 0), 0.16)]


def claim_mask(g, claims, pad=0):
    m = np.zeros(g["H"].shape, bool)
    for name, x0, z0, x1, z1 in claims:
        m[max(0, x0 - pad - LND.X0):x1 + pad - LND.X0 + 1, max(0, z0 - pad - LND.Z0):z1 + pad - LND.Z0 + 1] = True
    return m


def open_ground(g, claims, skins_ok=None):
    """Columns a tree may stand in: land, gentle, off the seam, off every road, off every claim, and off the ground a
    crossing's landings and the contested hilltops keep clear."""
    H = g["H"]
    land = g["land"]
    from pgmvox.surface import terrain as TR
    deg = TR.slope_deg(H, land)
    ok = land & (deg < 40) & ~g["seam"]
    X, Z = g["X"], g["Z"]
    ok &= ~(np.abs(Z - LND.centre(X)) < 20)                                    # the seam's rims are kept open
    ok &= ~claim_mask(g, claims, 3)
    ok &= ~shapes_dilate(g["laid"], 2)
    ok &= H > 44
    return ok


def shapes_dilate(mask, r):
    from scipy import ndimage
    return ndimage.binary_dilation(mask, iterations=r)


def hue_for(r):
    x, acc = r.random(), 0.0
    for blk, p in HUES:
        acc += p
        if x < acc:
            return blk
    return None


def snow_the_boughs(w, x, z, reach, r):
    """A layer of snow on the leaves of a spruce that have air above them."""
    for xx in range(x - reach, x + reach + 1):
        for zz in range(z - reach, z + reach + 1):
            for yy in range(w.sy - 2, 40, -1):
                if w.id(xx, yy, zz) in LEAVES:
                    if w.id(xx, yy + 1, zz) == B.AIR and r.random() < 0.7:
                        w.set(xx, yy + 1, zz, B.SNOW_LAYER, 0)
                    break


def plant_wood(w, zone, by, weights, r, claimed, ok, warm, H, tries=5000, spacing=0.7, allow=None):
    n = 0
    X, Z = w.grid()
    names = list(weights)
    p = np.array([weights[k] for k in names], float)
    p /= p.sum()
    cells = np.argwhere(zone)
    r.shuffle(cells)
    for i, k in cells[:tries]:
        x, z = int(X[i, k]), int(Z[i, k])
        group = by[names[int(r.choice(len(names), p=p))]]
        t = group[int(r.integers(len(group)))]
        c = t.crown * 0.5
        if any((x - px) ** 2 + (z - pz) ** 2 < ((c + pc) * spacing) ** 2 for px, pz, pc in claimed):
            continue
        if not ok(x, z, t):
            continue
        if T.plant(w, x, z, t, int(r.integers(4)), allowed=lambda xx, zz: bool(allow[xx - w.x0, zz - w.z0]),
                   through=T.PLANTS | {B.SNOW_LAYER}, gives_way=GIVE):
            claimed.append((x, z, c))
            reach = t.crown + 1
            if warm:
                hue = hue_for(r)
                if hue is not None:
                    for xx in range(x - reach, x + reach + 1):
                        for zz in range(z - reach, z + reach + 1):
                            y0 = int(H[x - w.x0, z - w.z0])
                            for yy in range(y0, min(w.sy, y0 + t.height + 4)):
                                if w.id(xx, yy, zz) in LEAVES and r.random() < 0.82:
                                    w.set(xx, yy, zz, *hue)
            else:
                snow_the_boughs(w, x, z, reach, r)
            n += 1
    return n


def forest(w, g, f, skins, claims):
    lib = T.library()
    by = T.kinds(lib)
    r = rng("rimefire", "forest")
    ok_ground = open_ground(g, claims)
    shape = g["H"].shape
    grove = noise.fbm(shape, 24, 3, seed=91)
    glade = noise.fbm(shape, 11, 2, seed=92)
    cold = skins == 2
    dust = skins == 1
    warm = skins == 0
    planted = []
    n = {}
    # keep the spawn plateaus and the hilltops open: sight lines are the game there
    X, Z = g["X"], g["Z"]
    open_top = np.zeros(shape, bool)
    for at, rad in ((LND.SPAWN, 17), (LND.turn(*LND.SPAWN), 17), (LND.OVERLOOK, 14), (LND.turn(*LND.OVERLOOK), 14),
                    (LND.FURNACE, 16), (LND.turn(*LND.FURNACE), 16)):
        open_top |= np.hypot(X - at[0], Z - at[1]) < rad
    ok_ground &= ~open_top
    loose = g["land"] & ~open_top & ~claim_mask(g, claims, 1) & ~g["seam"] & ~(np.abs(Z - LND.centre(X)) < 20)
    groves = ok_ground & (grove > -0.12) & (glade > -0.6)
    groves |= ok_ground & warm & (grove > -0.75) & (glade > -0.8)
    groves |= ok_ground & cold & (grove > -0.45) & (glade > -0.7)
    strays = ok_ground & (grove > -0.6) & ~groves

    def clear(x, z, t):
        return True

    oak = {"oak": 0.20, "birch": 0.34, "dense-oak": 0.10, "dark-oak": 0.08, "tiny-oak": 0.26, "large-oak": 0.02}
    pine = {"tall-spruce": 0.30, "tiny-spruce": 0.52, "large-pine": 0.18}
    n["autumn grove"] = plant_wood(w, groves & (warm | (dust & (glade > 0))), by, oak, r, planted, clear, True, g["H"], 9000, 0.6, allow=loose)
    n["spruce grove"] = plant_wood(w, groves & (cold | (dust & (glade <= 0))), by, pine, r, planted, clear, False, g["H"], 6000, allow=loose)
    n["autumn stray"] = plant_wood(w, strays & (warm | dust), by, {"oak": 0.4, "birch": 0.4, "tiny-oak": 0.2}, r, planted,
                                   clear, True, g["H"], 900, 1.9, allow=loose)
    n["spruce stray"] = plant_wood(w, strays & (cold | dust), by, {"tiny-spruce": 0.6, "tall-spruce": 0.4}, r, planted,
                                   clear, False, g["H"], 900, 1.9, allow=loose)
    return n, planted


LITTER = [(B.CARPET, 1), (B.CARPET, 14), (B.CARPET, 4), (B.CARPET, 12), (B.CARPET, 1)]


def litter(w, g, skins, planted):
    """Fallen leaves in carpet under and between the warm trees: every tree throws a drift on the ground around its foot."""
    r = rng("rimefire", "litter")
    n = 0
    H = g["H"]
    for x, z, c in planted:
        i, k = x - LND.X0, z - LND.Z0
        if skins[i, k] == 2:
            continue
        reach = int(c + 2.6)
        for _ in range(int(6 + 3 * c)):
            a = r.uniform(0, 2 * np.pi)
            d = r.uniform(1.2, reach + 1)
            xx, zz = int(round(x + d * np.cos(a))), int(round(z + d * np.sin(a)))
            ii, kk = xx - LND.X0, zz - LND.Z0
            if not (0 <= ii < H.shape[0] and 0 <= kk < H.shape[1]) or skins[ii, kk] == 2 or g["laid"][ii, kk]:
                continue
            y = w.top(xx, zz)
            if y > 0 and w.id(xx, y, zz) in (B.GRASS, B.DIRT) and w.id(xx, y + 1, zz) == B.AIR:
                w.set(xx, y + 1, zz, *LITTER[int(r.integers(len(LITTER)))])
                n += 1
    return n


def cover(w, g, f, skins, claims):
    """Small growth: dead bushes and tall grass on warm ground, ferns on cold, mushrooms in the shade of the groves."""
    r = rng("rimefire", "cover")
    H, land = g["H"], g["land"]
    ok = open_ground(g, claims) & ~g["laid"]
    n = {"deadbush": 0, "grass": 0, "fern": 0}
    X, Z = g["X"], g["Z"]
    cells = np.argwhere(ok)
    for i, k in cells[r.permutation(len(cells))][:9000]:
        x, z = int(X[i, k]), int(Z[i, k])
        y = int(H[i, k])
        top = w.id(x, y, z)
        if w.id(x, y + 1, z) != B.AIR:
            continue
        s = skins[i, k]
        roll = r.random()
        if s == 0 and top in (B.GRASS, B.DIRT):
            if top == B.DIRT and roll < 0.10:
                w.set(x, y + 1, z, B.DEADBUSH, 0)
                n["deadbush"] += 1
            elif top == B.GRASS and roll < 0.16:
                w.set(x, y + 1, z, B.TALLGRASS, 1)
                n["grass"] += 1
        elif s == 1 and top in (B.GRASS, B.DIRT) and roll < 0.05:
            w.set(x, y + 1, z, B.TALLGRASS, 2)
            n["fern"] += 1
    return n


def shrubs(w, g, skins, claims, planted, count=420):
    """Low growth under and between the trees: a shrub is a clump of one to four leaf blocks a block off the ground, in
    autumn colours over warm ground and spruce green with snow on it over cold."""
    r = rng("rimefire", "shrubs")
    H = g["H"]
    X, Z = g["X"], g["Z"]
    ok = open_ground(g, claims) & ~shapes_dilate(g["laid"], 1)
    cells = np.argwhere(ok)
    cells = cells[r.permutation(len(cells))]
    n = 0
    for i, k in cells:
        if n >= count:
            break
        x, z = int(X[i, k]), int(Z[i, k])
        if any((x - px) ** 2 + (z - pz) ** 2 < 4 for px, pz, pc in planted):
            continue
        y = int(H[i, k])
        if w.id(x, y + 1, z) != B.AIR:
            continue
        s = skins[i, k]
        cold = s == 2 or (s == 1 and r.random() < 0.5)
        size = int(r.integers(1, 5))
        spots = [(0, 0)] + [(int(r.integers(-1, 2)), int(r.integers(-1, 2))) for _ in range(size - 1)]
        hue = None if cold else hue_for(r)
        for dx, dz in set(spots):
            xx, zz = x + dx, z + dz
            ii, kk = xx - LND.X0, zz - LND.Z0
            if not (0 <= ii < H.shape[0] and 0 <= kk < H.shape[1]) or not ok[ii, kk]:
                continue
            gy = int(H[ii, kk])
            if abs(gy - y) > 1 or w.id(xx, gy + 1, zz) != B.AIR:
                continue
            if cold:
                w.set(xx, gy + 1, zz, B.LEAVES, 1 | 4)
                w.set(xx, gy + 2, zz, B.SNOW_LAYER, 0)
            elif hue is None:
                w.set(xx, gy + 1, zz, B.LEAVES, 4)
            else:
                w.set(xx, gy + 1, zz, *hue)
        n += 1
    return n


def features(w, g, skins, claims, planted):
    """Things that belong to one ground: on the cold, boulders under a cap of snow, bare spruce trunks and drifts lee of
    the rock; on the warm, fallen logs and rust-coloured boulders of banded clay."""
    from pgmvox.built import props
    r = rng("rimefire", "features")
    H = g["H"]
    X, Z = g["X"], g["Z"]
    ok = open_ground(g, claims) & ~shapes_dilate(g["laid"], 2)
    cells = np.argwhere(ok)
    cells = cells[r.permutation(len(cells))]
    n = {"boulder": 0, "bare trunk": 0, "drift": 0, "fallen log": 0, "rust boulder": 0}
    want = {"boulder": 34, "bare trunk": 26, "drift": 60, "fallen log": 26, "rust boulder": 26}
    for i, k in cells:
        if all(n[a] >= want[a] for a in n):
            break
        x, z = int(X[i, k]), int(Z[i, k])
        if any((x - px) ** 2 + (z - pz) ** 2 < 9 for px, pz, pc in planted):
            continue
        y = int(H[i, k])
        if w.id(x, y + 1, z) != B.AIR:
            continue
        s = skins[i, k]
        if s == 2:
            roll = r.random()
            if roll < 0.35 and n["boulder"] < want["boulder"]:
                props.rubble(w, x, y, z, r, r=float(r.uniform(1.4, 2.6)), blocks=((B.STONE, 5), (B.STONE, 6), (B.COBBLE, 0), (B.STONE, 5)))
                for dx in range(-3, 4):
                    for dz in range(-3, 4):
                        top = w.top(x + dx, z + dz)
                        if top > y and w.id(x + dx, top, z + dz) in (B.STONE, B.COBBLE) and w.id(x + dx, top + 1, z + dz) == B.AIR:
                            w.set(x + dx, top + 1, z + dz, B.SNOW_LAYER, int(r.integers(0, 2)))
                n["boulder"] += 1
            elif roll < 0.55 and n["bare trunk"] < want["bare trunk"]:
                from pgmvox.scenery.trees import dead_tree
                dead_tree(w, x, y, z, r, int(r.integers(6, 11)), log=B.LOG, kind=1)
                n["bare trunk"] += 1
            elif n["drift"] < want["drift"]:
                for _ in range(int(r.integers(5, 12))):
                    dx, dz = int(r.integers(-3, 4)), int(r.integers(-3, 4))
                    xx, zz = x + dx, z + dz
                    ii, kk = xx - LND.X0, zz - LND.Z0
                    if not ok[ii, kk]:
                        continue
                    gy = int(H[ii, kk])
                    if w.id(xx, gy, zz) in (B.SNOW, B.PACKED_ICE) and w.id(xx, gy + 1, zz) == B.AIR:
                        w.set(xx, gy + 1, zz, B.SNOW_LAYER, int(r.integers(1, 4)))
                n["drift"] += 1
        elif s == 0:
            roll = r.random()
            if roll < 0.3 and n["fallen log"] < want["fallen log"]:
                along_x = r.random() < 0.5
                ln = int(r.integers(4, 8))
                for j in range(ln):
                    xx, zz = (x + j, z) if along_x else (x, z + j)
                    ii, kk = xx - LND.X0, zz - LND.Z0
                    if not ok[ii, kk]:
                        break
                    gy = int(H[ii, kk])
                    if abs(gy - y) <= 1 and w.id(xx, gy + 1, zz) == B.AIR:
                        w.set(xx, gy + 1, zz, B.LOG2, 1 | (4 if along_x else 8))
                n["fallen log"] += 1
            elif roll < 0.6 and n["rust boulder"] < want["rust boulder"]:
                props.rubble(w, x, y, z, r, r=float(r.uniform(1.3, 2.4)),
                             blocks=((B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 12), (B.STONE, 1), (B.HARDENED_CLAY, 0)))
                n["rust boulder"] += 1
    return n
