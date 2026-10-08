"""Generate Gullhaven from the plan: every column built to the floor the checker walked, its top by what kind
of ground it is, then what stands on it — the closed houses, the lighthouse, the mill, the chapel's ruin, the
caves carved under the Headland, the bridges, the piers and boats, the cover and the trees.

    python3 gen.py <build-dir>
"""
import math
import random
import sys
import time

import numpy as np

import house
import plan as P
from geometry import polyline
from mc import World, B

R = P.build()
K = P.KINDS
KN = {v: k for k, v in K.items()}
G = R.G
BASE_Y = 6
SEA_FLOOR = 13
rng = random.Random(5)

STONE, ANDESITE, POL_ANDESITE, DIORITE = (B.STONE, 0), (B.STONE, 5), (B.STONE, 6), (B.STONE, 3)
COBBLE, MOSSY_COBBLE = (B.COBBLE, 0), (B.MOSSY, 0)
SBRICK, MOSSY_BRICK, CRACKED_BRICK = (B.STONEBRICK, 0), (B.STONEBRICK, 1), (B.STONEBRICK, 2)
GRAVEL, SAND, SANDSTONE, DIRT, COARSE = (B.GRAVEL, 0), (B.SAND, 0), (B.SANDSTONE, 0), (B.DIRT, 0), (B.DIRT, 1)
GRASS = (B.GRASS, 0)
SPRUCE, SPRUCE_LOG, OAK_LOG = (B.PLANKS, 1), (B.LOG, 1), (B.LOG, 0)
COBBLE_STAIRS, BRICK_STAIRS = 67, 109
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def kind(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return "sea"
    return KN[R.K[i, j]]


def g(x, z):
    i, j = P.ix(x), P.iz(z)
    if not (0 <= i < P.NX and 0 <= j < P.NZ):
        return P.SEA
    return int(G[i, j])


def pick(choices, weights):
    return rng.choices(choices, weights)[0]


def strata(y):
    """The island's rock in its cliffs: stone, with courses of andesite and a seam of gravelly coarse dirt."""
    if y % 7 == 3:
        return ANDESITE
    if y % 11 == 6:
        return DIORITE
    return STONE


TOWN_KINDS = ("street",)


def top_block(x, z, k, h):
    if k == "grass":
        return GRASS
    if k == "beach":
        return SAND
    if k == "street":
        return pick([SBRICK, COBBLE, ANDESITE, MOSSY_BRICK, GRAVEL], [45, 20, 15, 10, 10])
    if k == "quay":
        edge = any(kind(x + dx, z + dz) == "sea" for dx, dz in N4)
        return SPRUCE if edge else pick([SBRICK, CRACKED_BRICK, COBBLE], [60, 20, 20])
    if k == "ravine":
        return pick([GRAVEL, COARSE, STONE, MOSSY_COBBLE], [40, 30, 20, 10])
    if k == "ramp":
        town = any(kind(x + dx, z + dz) in ("street", "quay") for dx in (-3, 0, 3) for dz in (-3, 0, 3))
        return SBRICK if town else GRAVEL
    return GRASS


def stair_dir(x, z, h):
    """If this ramp cell is a step up from a ramp neighbour one lower, the way a player climbs onto it."""
    for (dx, dz), d in zip(N4, (1, 0, 3, 2)):
        if kind(x + dx, z + dz) == "ramp" and g(x + dx, z + dz) == h - 1:
            return d
    return None


# ---- the ground -------------------------------------------------------------------------------------------
def columns(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            k, h = KN[R.K[i, j]], int(G[i, j])
            if k == "sea":
                for y in range(BASE_Y, SEA_FLOOR):
                    w.set(x, y, z, *STONE)
                w.set(x, SEA_FLOOR, z, *(GRAVEL if (x * 3 + z * 7) % 5 == 0 else SAND))
                for y in range(SEA_FLOOR + 1, P.SEA + 1):
                    w.set(x, y, z, B.WATER)
                continue
            if k == "pier":
                for y in range(BASE_Y, SEA_FLOOR + 1):
                    w.set(x, y, z, *STONE)
                for y in range(SEA_FLOOR + 1, P.SEA + 1):
                    w.set(x, y, z, B.WATER)
                if (z % 4 == 0) and (x in (26, 27, 35, 36)):
                    for y in range(SEA_FLOOR + 1, h):
                        w.set(x, y, z, *SPRUCE_LOG)
                w.set(x, h, z, *SPRUCE)
                continue
            if k == "stream":
                for y in range(BASE_Y, h):
                    w.set(x, y, z, *strata(y))
                w.set(x, h - 1, z, *GRAVEL)
                w.set(x, h, z, B.WATER)
                continue
            low = min([g(x + dx, z + dz) for dx, dz in N4 if kind(x + dx, z + dz) != "sea"] + [h])
            for y in range(BASE_Y, h + 1):
                w.set(x, y, z, *strata(y))
            if k in ("street", "quay") or (k == "ramp" and top_block(x, z, k, h) == SBRICK):
                # a terrace's retaining wall where the ground falls away to lower ground: stone brick, mossy
                # toward its foot; where it falls to the sea, a sea wall five courses deep on the rock
                for y in range(max(low, BASE_Y), h):
                    w.set(x, y, z, *(MOSSY_BRICK if y < low + 2 or rng.random() < 0.15 else SBRICK))
                if any(kind(x + dx, z + dz) == "sea" for dx in (-1, 0, 1) for dz in (-1, 0, 1)) and h - P.SEA > 4:
                    for y in range(max(h - 6, P.SEA + 1), h):
                        w.set(x, y, z, *(MOSSY_BRICK if y < h - 4 or rng.random() < 0.2 else SBRICK))
            elif k == "beach":
                for y in range(h - 3, h):
                    w.set(x, y, z, *SANDSTONE)
            else:
                cliff = h - low >= 3
                for y in range(h - (1 if cliff else 3), h):
                    w.set(x, y, z, *DIRT)
            t = top_block(x, z, k, h)
            sd = stair_dir(x, z, h) if k == "ramp" else None
            if sd is not None:
                w.set(x, h, z, BRICK_STAIRS if t == SBRICK else COBBLE_STAIRS, sd)
            else:
                w.set(x, h, z, *t)


NATURAL = ("grass", "beach", "ravine", "stream")


def cliffs(w):
    """Break the cliffs. Three things, none of which a player can climb:

    - the face: level by level, rock within a block or three of the open air is cut away where a noise that
      changes with height says so — notches, ledges, overhangs — never in the top two courses, so the edge a
      player walks to stays where the plan put it, and never within three blocks of the town, the quay or a
      building, which stand on whole rock behind a sea wall;
    - the foot: below every cliff that stands over the sea or the beach, a slope of fallen rock rising toward
      the face, two and a half blocks up for every block in, its top four under the cliff's edge, so no step
      of it is a block high and it is never a way up;
    - sea stacks off the Headland, the Cove and the town.

    The terraces' walls between the town's levels keep their built stone brick, and where the town stands over
    the sea it stands on a sea wall of stone brick six courses deep."""
    from scipy import ndimage
    from noise import fbm
    shape = (P.NX, P.NZ)
    a, b, c = fbm(shape, 7, 3, seed=31), fbm(shape, 5, 2, seed=32), fbm(shape, 11, 2, seed=33)
    Gi = G.astype(int)
    land = ~np.isin(R.K, [K["sea"], K["pier"]])
    natural = np.isin(R.K, [K[k] for k in NATURAL])
    built = np.isin(R.K, [K["street"], K["quay"], K["ramp"]])
    sea = R.K == K["sea"]
    # nothing is cut within three blocks of the town, the quay or anything built on the ground
    standing = np.isin(R.K, [K["house"], K["landmark"]]) | built
    keep = ndimage.binary_dilation(standing, iterations=3)
    # the face
    for y in range(SEA_FLOOR + 1, int(Gi.max()) + 1):
        solid = (Gi >= y) & land
        n3 = a * math.cos(y * 0.55) + b * math.sin(y * 0.8 + 1.0) + 0.5 * c
        din = ndimage.distance_transform_edt(solid)
        depth = np.clip((n3 - 0.05) * 5.0, 0, 3.2)
        cut = solid & (din <= depth) & (depth > 0.3) & natural & ~keep & (y <= Gi - 2)
        for i, j in zip(*np.nonzero(cut)):
            x, z = i + P.X_MIN, j + P.Z_MIN
            if w.id(x, y, z) not in (B.AIR, B.WATER):
                w.set(x, y, z, B.WATER if y <= P.SEA else B.AIR)
    # the foot: for every sea or beach column near a cliff, the height of the nearest cliff top and how far
    land_top = np.where(land & (Gi >= P.SEA + 6), Gi, 0)
    d, (ii, jj) = ndimage.distance_transform_edt(land_top == 0, return_indices=True)
    scale = 1.0 + 0.6 * c
    for i in range(P.NX):
        for j in range(P.NZ):
            k = KN[R.K[i, j]]
            if k not in ("sea", "beach") or d[i, j] > 7 or d[i, j] < 1:
                continue
            ht = int(land_top[ii[i, j], jj[i, j]])
            top = int(math.floor(ht - 4 - 2.5 * (d[i, j] - 1) * scale[i, j] + 1.2 * a[i, j]))
            x, z = i + P.X_MIN, j + P.Z_MIN
            base = SEA_FLOOR if k == "sea" else int(Gi[i, j])
            if top <= base:
                continue
            for y in range(base + 1, top + 1):
                w.set(x, y, z, *pick([STONE, ANDESITE, MOSSY_COBBLE, COBBLE, GRAVEL], [45, 25, 12, 10, 8]))
            if top > P.SEA and rng.random() < 0.15:
                w.set(x, top + 1, z, *MOSSY_COBBLE)
    # sea stacks
    for cx, cz, r, top in ((-54, -40, 1.8, 31), (-30, -49, 1.4, 26), (-55, 28, 1.6, 27), (52, -38, 1.5, 24)):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            for z in range(int(cz - r) - 1, int(cz + r) + 2):
                for y in range(SEA_FLOOR, top + 1):
                    rr = r * (1.0 - 0.35 * (y - SEA_FLOOR) / (top - SEA_FLOOR)) + 0.4 * math.sin(y * 1.3 + x)
                    if (x - cx) ** 2 + (z - cz) ** 2 <= rr * rr and kind(x, z) == "sea":
                        w.set(x, y, z, *(GRASS if y == top else strata(y)))


def sea_near(i, j):
    return any(0 <= i + a < P.NX and 0 <= j + b < P.NZ and R.K[i + a, j + b] == K["sea"]
               for a in (-3, 0, 3) for b in (-3, 0, 3))


def houses(w):
    for n, hs in enumerate(P.HOUSES):
        spec = dict(hs)
        spec["floor"] = g(int(hs["cx"]), int(hs["cz"]))
        spec["door"] = 1 if n % 2 else -1
        spec["jetty"] = hs.get("storeys", 1) >= 2 and hs.get("style") == "town"
        house.build(w, spec, ground_at=lambda x, z: g(x, z), rng=np.random.default_rng(n + 3))


def disc_cells(cx, cz, r):
    return [(x, z) for x in range(int(cx - r) - 1, int(cx + r) + 2) for z in range(int(cz - r) - 1, int(cz + r) + 2)
            if (x + 0.5 - cx - 0.5) ** 2 + (z + 0.5 - cz - 0.5) ** 2 <= r * r]


def lighthouse(w):
    """White and red in bands, a door that does not open, a gallery, a lantern of glass round glowstone."""
    cx, cz = -42, -38
    base = g(cx, cz)
    top = base + 20
    for x, z in disc_cells(cx, cz, 3.5):
        rim = (x - cx) ** 2 + (z - cz) ** 2 > 2.2 ** 2
        for y in range(base - 2, top + 1):
            if rim or y in (base, top):
                band = ((y - base) // 4) % 2
                w.set(x, y, z, *((B.WOOL, 14) if band else (B.QUARTZ, 0)))
            else:
                w.set(x, y, z, B.AIR)
    for y in (base + 5, base + 10, base + 15):
        w.set(cx + 3, y, cz, B.PANE)
        w.set(cx - 3, y, cz, B.PANE)
    w.set(cx, base + 1, cz + 3, B.SPRUCE_DOOR, 1)
    w.set(cx, base + 2, cz + 3, B.SPRUCE_DOOR, 8)
    for x, z in disc_cells(cx, cz, 4.6):
        w.set(x, top, z, *SBRICK)
        if (x - cx) ** 2 + (z - cz) ** 2 > 3.6 ** 2:
            w.set(x, top + 1, z, B.IRON_BARS)
    for x, z in disc_cells(cx, cz, 2.2):
        edge = (x - cx) ** 2 + (z - cz) ** 2 > 1.2 ** 2
        for y in range(top + 1, top + 4):
            w.set(x, y, z, *((B.GLASS, 0) if edge else (B.GLOWSTONE, 0)))
        w.set(x, top + 4, z, *(B.WOOL, 14))
    w.set(cx, top + 5, cz, B.WOOL, 14)


def mill(w):
    """A stone tower mill, a cone of spruce, four sails of white wool on its south face."""
    cx, cz = -30, 26
    base = g(cx, cz)
    top = base + 11
    for x, z in disc_cells(cx, cz, 3.0):
        for y in range(base - 2, top + 1):
            w.set(x, y, z, *(COBBLE if y % 3 else STONE))
    for k, y in enumerate(range(top + 1, top + 5)):
        for x, z in disc_cells(cx, cz, 3.2 - k * 0.9):
            w.set(x, y, z, *SPRUCE)
    hz = cz + 4
    hy = top - 1
    w.set(cx, hy, cz + 3, *SPRUCE_LOG)
    for d in range(1, 7):
        for (ax, ay) in ((d, 0), (-d, 0), (0, d), (0, -d)):
            w.set(cx + ax, hy + ay, hz, B.FENCE)
            if d >= 2:
                ox, oy = (0, 1) if ay == 0 else (1, 0)
                w.set(cx + ax + ox * (1 if ax >= 0 else -1), hy + ay + oy * (1 if ay >= 0 else -1), hz, B.WOOL, 0)
    w.set(cx, base + 1, cz - 3, B.SPRUCE_DOOR, 3)
    w.set(cx, base + 2, cz - 3, B.SPRUCE_DOOR, 8)


def chapel(w):
    """The chapel's ruin: walls of mossy and cracked stone brick two high with gaps, the west gable standing
    to its window, a floor of broken tiles, and the crypt's shaft with its ladder."""
    x0, x1, z0, z1 = P.CHAPEL["box"]
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            f = g(x, z)
            edge = x in (x0, x1) or z in (z0, z1)
            w.set(x, f, z, *pick([SBRICK, MOSSY_BRICK, CRACKED_BRICK, GRASS], [30, 25, 25, 20]))
            if not edge:
                continue
            gap = (x in (x0 + 4,) and z == z1) or (z == z1 - 4 and x == x1) or rng.random() < 0.18
            if gap:
                continue
            hgt = 2 if x != x0 else (6 if abs(z - (z0 + z1) / 2) < 3 else 3)
            if x == x0 and abs(z - (z0 + z1) / 2) < 1:
                hgt = 6
            for y in range(f + 1, f + 1 + hgt):
                win = x == x0 and abs(z - (z0 + z1) / 2) < 1 and f + 3 <= y <= f + 5
                if not win:
                    w.set(x, y, z, *pick([MOSSY_BRICK, CRACKED_BRICK, SBRICK], [40, 30, 30]))


def carve_line(w, pts, half=1.6, head=3, floor_block=GRAVEL):
    """A tunnel: discs along the polyline of (x, z, floor), air `head` high over a floor; where the ground is
    only a little over it, the cut opens to the sky."""
    for (ax, az, ay), (bx, bz, by) in zip(pts, pts[1:]):
        n = int(max(abs(bx - ax), abs(bz - az), abs(by - ay)) * 3) + 1
        for s in range(n + 1):
            t = s / n
            cx, cz, cy = ax + (bx - ax) * t, az + (bz - az) * t, ay + (by - ay) * t
            fy = int(round(cy))
            for x in range(int(cx - half) - 1, int(cx + half) + 2):
                for z in range(int(cz - half) - 1, int(cz + half) + 2):
                    if (x + 0.5 - cx) ** 2 + (z + 0.5 - cz) ** 2 > half * half:
                        continue
                    ground = g(x, z)
                    roof = fy + head if ground - (fy + head) > 1 else max(ground, fy + head)
                    for y in range(fy + 1, roof + 1):
                        w.set(x, y, z, B.AIR)
                    w.set(x, fy, z, *floor_block)


def caves(w):
    """The grotto, its pool and its lights; the four tunnels; the crypt's ladder; glowstone along the walls."""
    x0, x1, z0, z1 = P.GROTTO["box"]
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            cxn, czn = (x - (x0 + x1) / 2) / ((x1 - x0) / 2 + 1), (z - (z0 + z1) / 2) / ((z1 - z0) / 2 + 1)
            r = cxn * cxn + czn * czn
            if r > 1.05:
                continue
            ceil = P.GROTTO["ceil"] - int(r * 3) - (1 if (x * 5 + z * 3) % 7 == 0 else 0)
            for y in range(P.GROTTO["floor"] + 1, ceil + 1):
                w.set(x, y, z, B.AIR)
            w.set(x, P.GROTTO["floor"], z, *pick([STONE, GRAVEL, MOSSY_COBBLE], [50, 30, 20]))
            if (x + z) % 6 == 0 and r < 0.8:
                w.set(x, ceil + 1, z, B.GLOWSTONE)
    for x in range(-35, -32):                       # the pool, one deep
        for z in range(-25, -22):
            w.set(x, P.GROTTO["floor"], z, B.WATER)
            w.set(x, P.GROTTO["floor"] - 1, z, *(B.SAND, 0))
    for t in P.TUNNELS:
        pts = t["pts"]
        if t.get("ladder"):
            (sx, sz, top), (_, _, bot) = pts[0], pts[1]
            for y in range(bot + 1, top + 1):
                w.set(sx, y, sz, B.LADDER, 3)
                w.set(sx + 1, y, sz, B.AIR)
                w.set(sx, y, sz - 1, *MOSSY_BRICK)
            w.set(sx, top, sz, B.LADDER, 3)
            carve_line(w, pts[1:], half=1.4)
        else:
            carve_line(w, pts)
        for (ax, az, ay), (bx, bz, by) in zip(pts, pts[1:]):
            L = math.dist((ax, az), (bx, bz))
            for s in np.arange(3, L, 7):
                t_ = s / L
                cx, cz, cy = ax + (bx - ax) * t_, az + (bz - az) * t_, ay + (by - ay) * t_
                nx, nz = -(bz - az) / L, (bx - ax) / L
                gx, gz = int(round(cx + nx * 2.4)), int(round(cz + nz * 2.4))
                if w.id(gx, int(cy) + 2, gz) not in (B.AIR, B.WATER) and g(gx, gz) > int(cy) + 4:
                    w.set(gx, int(cy) + 2, gz, B.GLOWSTONE)


def bridges(w):
    """Spruce decks on log trestles, fenced both sides; a step in the deck is a stair."""
    for br in P.BRIDGES:
        d, along = polyline(P.XS, P.ZS, br["pts"])
        for i in range(P.NX):
            for j in range(P.NZ):
                x, z = i + P.X_MIN, j + P.Z_MIN
                u = R.U[i, j]
                if d[i, j] > br["half"] + 1.0:
                    continue                                # another bridge's cell, or no bridge's
                if u >= 0:
                    sd = None
                    for (dx, dz), dd in zip(N4, (1, 0, 3, 2)):
                        p, q = i + dx, j + dz
                        if 0 <= p < P.NX and 0 <= q < P.NZ and R.U[p, q] == u - 1:
                            sd = dd
                    w.set(x, u, z, *((134, sd) if sd is not None else SPRUCE))
                    if (int(along[i, j]) % 4 == 0) and d[i, j] > 0.4:
                        bottom = SEA_FLOOR if KN[R.K[i, j]] == "sea" else int(G[i, j])
                        for y in range(bottom + 1, u):
                            w.set(x, y, z, *SPRUCE_LOG)
                elif br["half"] < d[i, j] <= br["half"] + 1.0 and along[i, j] > 1 and \
                        KN[R.K[i, j]] in br["over"]:
                    near = [R.U[i + a, j + b] for a, b in N4 if 0 <= i + a < P.NX and 0 <= j + b < P.NZ and R.U[i + a, j + b] >= 0]
                    if near:
                        w.set(x, max(near) + 1, z, B.SPRUCE_FENCE)


def cover(w):
    """What stands on the ground to be stood behind: hedgerows of leaves, dry-stone walls, the standing stones,
    rocks on the grass, crates and barrels in the town and on the quay, driftwood on the beach."""
    hedge = np.zeros((P.NX, P.NZ), bool)
    for line in P.HEDGES:
        d, _ = polyline(P.XS, P.ZS, line)
        hedge |= d < 0.75
    wall = np.zeros((P.NX, P.NZ), bool)
    for line in P.WALLS:
        d, _ = polyline(P.XS, P.ZS, line)
        wall |= d < 0.75
    stones = set(P.STONES)
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.K[i, j] != K["cover"]:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            f = g(x, z)
            tall = int(R.H[i, j]) - f
            base = kind_under(x, z)
            for y in range(f + 1, f + 1 + tall):
                if hedge[i, j]:
                    b = (B.LEAVES, 4)
                elif wall[i, j]:
                    b = pick([COBBLE, MOSSY_COBBLE], [60, 40])
                elif (x, z) in stones:
                    b = pick([STONE, ANDESITE], [60, 40])
                elif base in ("street", "quay", "ramp"):
                    b = pick([OAK_LOG, (B.HAY, 0), SPRUCE, (B.LOG, 13)], [30, 30, 20, 20])
                elif base == "beach":
                    b = (B.LOG, 4) if y == f + 1 else (B.AIR, 0)
                else:
                    b = pick([STONE, ANDESITE, MOSSY_COBBLE, COBBLE], [40, 30, 20, 10])
                w.set(x, y, z, *b)
            if (x, z) not in stones and not hedge[i, j] and not wall[i, j] and base == "grass":
                for dx, dz in N4:                          # a rock: a low shoulder of stone round it
                    if kind(x + dx, z + dz) == "grass" and rng.random() < 0.5:
                        w.set(x + dx, g(x + dx, z + dz) + 1, z + dz, *pick([STONE, ANDESITE, MOSSY_COBBLE], [50, 30, 20]))


def kind_under(x, z):
    """The ground's kind beneath a cover cell: the commonest kind among its neighbours."""
    ks = [kind(x + dx, z + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)]
    ks = [k for k in ks if k not in ("cover", "tree", "house", "landmark")]
    return max(set(ks), key=ks.count) if ks else "grass"


def tree(w, x, y, z, sort):
    r = random.Random(x * 1009 + z)
    if sort == "spruce":
        t = r.randint(6, 8)
        for yy in range(y + 1, y + t + 1):
            w.set(x, yy, z, B.LOG, 1)
        for k, yy in enumerate(range(y + t, y + 2, -1)):
            rad = [0, 1, 1, 2, 1, 2, 2][min(k, 6)]
            for dx in range(-rad, rad + 1):
                for dz in range(-rad, rad + 1):
                    if abs(dx) + abs(dz) <= rad + (1 if rad == 2 else 0) and (dx, dz) != (0, 0) and w.id(x + dx, yy, z + dz) == B.AIR:
                        w.set(x + dx, yy, z + dz, B.LEAVES, 5)
        w.set(x, y + t + 1, z, B.LEAVES, 5)
        return
    t = r.randint(5, 6)
    top = y + t
    for yy in range(y + 1, top + 1):
        w.set(x, yy, z, *OAK_LOG)
    for yy in (top - 2, top - 1):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if abs(dx) == 2 and abs(dz) == 2 and r.random() < 0.6:
                    continue
                if (dx, dz) != (0, 0) and w.id(x + dx, yy, z + dz) == B.AIR:
                    w.set(x + dx, yy, z + dz, B.LEAVES, 4)
    for yy in (top, top + 1):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if abs(dx) == 1 and abs(dz) == 1 and (yy == top + 1 or r.random() < 0.5):
                    continue
                if w.id(x + dx, yy, z + dz) == B.AIR:
                    w.set(x + dx, yy, z + dz, B.LEAVES, 4)


def trees(w):
    for x, z in P.TREES:
        sort = "spruce" if g(x, z) >= 38 or (x + z) % 3 == 0 else "oak"
        tree(w, x, g(x, z), z, sort)


def boats(w):
    """Two boats moored in the basin, hulls of spruce at the water's surface."""
    for cx, cz, along_x in ((31, 26, False), (40, 34, False)):
        for k in range(-3, 4):
            for o in (-1, 0, 1):
                x, z = (cx + o, cz + k) if not along_x else (cx + k, cz + o)
                if abs(k) == 3 and o != 0:
                    continue
                w.set(x, P.SEA, z, *SPRUCE)
                if o != 0 or abs(k) == 3:
                    w.set(x, P.SEA + 1, z, B.WOOD_SLAB, 1)
        w.set(cx, P.SEA + 1, cz, B.FENCE)
        w.set(cx, P.SEA + 2, cz, B.FENCE)
        w.set(cx, P.SEA + 3, cz, B.WOOL, 0)


def flowers(w):
    for i in range(P.NX):
        for j in range(P.NZ):
            if R.K[i, j] != K["grass"]:
                continue
            x, z = i + P.X_MIN, j + P.Z_MIN
            y = g(x, z)
            if w.get(x, y, z) != GRASS or w.id(x, y + 1, z) != B.AIR:
                continue
            r = rng.random()
            if r < 0.10:
                w.set(x, y + 1, z, B.TALLGRASS, 2 if y >= 38 else 1)
            elif r < 0.115:
                w.set(x, y + 1, z, B.FLOWER, rng.choice((0, 3, 8)))
            elif r < 0.12:
                w.set(x, y + 1, z, B.DANDELION)


def make():
    w = World(P.X_MIN, P.Z_MIN, P.NX, P.NZ, sy=72)
    columns(w)
    cliffs(w)
    caves(w)
    chapel(w)
    houses(w)
    lighthouse(w)
    mill(w)
    bridges(w)
    cover(w)
    trees(w)
    boats(w)
    flowers(w)
    w.biome[:, :] = 1
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Gullhaven", (0, 60, 0))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
