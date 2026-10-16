"""What hangs beyond the playable ground: icicles and ember drips under the islands, seams down their outer cliffs,
floating shards in the bays, and the dead trees on the crags."""
import math

import numpy as np

import land as LD
from pgmvox import B
from pgmvox.geom.shapes import boundary
from pgmvox.scenery import trees as TR


def hangings(w, ctx, rng):
    """Icicles in the north, ember drips in the south: columns hung from the underside's outermost ring."""
    land, H, bottom, ed = ctx["land"], ctx["H"], ctx["bottom"], ctx["ed"]
    X, Z = ctx["X"], ctx["Z"]
    rim = (ed <= 2) & land & ~ctx["rift"]
    n = 0
    for i, k in np.argwhere(rim):
        if rng.random() > 0.16:
            continue
        z = int(Z[i, k])
        y0 = int(bottom[i, k])
        length = int(rng.integers(3, 12))
        for j in range(1, length + 1):
            y = y0 - j
            if y < 8:
                break
            if z < 0:
                blk = (B.PACKED_ICE, 0) if j < length - 1 or rng.random() < 0.5 else (B.ICE, 0)
            else:
                blk = (B.STAINED_CLAY, 1) if j < length else (B.GLOWSTONE, 0)
            w.ids[i, y, k], w.dat[i, y, k] = blk
        n += 1
    return n


def seams(w, ctx, rng):
    """Vertical streaks down the outer cliffs: frozen falls in the north, seams of ember in the south."""
    land, H, bottom, ed = ctx["land"], ctx["H"], ctx["bottom"], ctx["ed"]
    X, Z = ctx["X"], ctx["Z"]
    edge = boundary(land) & ~ctx["rift"] & (ed <= 0)
    cols = np.argwhere(edge)
    rng.shuffle(cols)
    n, taken = 0, []
    for i, k in cols:
        if any(abs(i - a) + abs(k - b) < 9 for a, b in taken):
            continue
        taken.append((i, k))
        z = int(Z[i, k])
        for di in range(-1, 2):
            for dk in range(-1, 2):
                a, b = i + di, k + dk
                if not (0 <= a < LD.SX and 0 <= b < LD.SZ) or not edge[a, b]:
                    continue
                for y in range(int(bottom[a, b]), int(H[a, b]) - 1):
                    if z < 0:
                        blk = (B.PACKED_ICE, 0) if (a + y) % 3 else (B.ICE, 0)
                    else:
                        blk = (B.STAINED_CLAY, 1) if (a + y) % 4 else (B.GLOWSTONE, 0)
                    w.ids[a, y, b], w.dat[a, y, b] = blk
        n += 1
        if n >= 22:
            break
    return n


def shard(w, x, z, y, r, south, rng):
    """A floating rock: a lens of the half's rock, its top in the half's ground, one tree on it."""
    for dx in range(-r - 2, r + 3):
        for dz in range(-r - 2, r + 3):
            d = math.hypot(dx, dz) / (r + 0.3)
            if d > 1.0:
                continue
            depth = int(round((1 - d) ** 0.9 * r * 1.7)) + 1
            for j in range(depth):
                yy = y - j
                if south:
                    blk = (B.HARDENED_CLAY, 0) if j % 4 else (B.STAINED_CLAY, 12)
                else:
                    blk = (B.STONE, 0) if j % 5 else (B.PACKED_ICE, 0)
                w.set(x + dx, yy, z + dz, *blk)
            w.set(x + dx, y + 1, z + dz, *((B.GRASS, 0) if south else (B.SNOW, 0)))
            w.set(x + dx, y, z + dz, *((B.DIRT, 1) if south else (B.STONE, 0)))


SHARDS = [(-60, -30, 66, 4), (-59, -72, 70, 5), (62, -29, 62, 3), (60, -86, 68, 4), (-48, -96, 64, 3), (66, -62, 64, 3)]


def shards(w, ctx, rng):
    from flora import autumn_oak, spruce
    for x, z, y, r in SHARDS:
        for south in (False, True):
            px, pz = (-1 - x, -1 - z) if south else (x, z)
            if not (LD.X0 + 3 <= px < LD.X0 + LD.SX - 3 and LD.Z0 + 3 <= pz < LD.Z0 + LD.SZ - 3):
                continue
            if ctx["land"][px - LD.X0, pz - LD.Z0]:
                continue
            shard(w, px, pz, y, r, south, rng)
            if r >= 4:
                (autumn_oak if south else spruce)(w, px, pz, y + 1, 5 if south else 7, rng) if south else \
                    spruce(w, px, pz, y + 1, 7, rng)


def dead_trees(w, ctx, rng):
    """Bare trees on the crags: frost-killed spruce in the north, charred dark oak in the south."""
    from flora import sites
    H, land, Z, X = ctx["H"], ctx["land"], ctx["Z"], ctx["X"]
    m = land & (Z < -76) & (ctx["deg"] < 40) & (ctx["ed"] > 3) & ~((X > -8) & (X < 34)) & (H > 60)
    pts = sites(ctx, rng, m, 8, 11, [])
    for x, z in pts:
        g = int(H[x - w.x0, z - w.z0])
        h = int(rng.integers(5, 9))
        TR.dead_tree(w, x, g, z, rng, h, log=B.LOG, kind=1)
        TR.dead_tree(w, -1 - x, g, -1 - z, rng, h, log=B.LOG2, kind=1)
    return len(pts)


def lavafalls(w, ctx, rng):
    """Where the rift ends at the board's edge the lava is dammed, and the dam's outer face carries a fall of lava set
    solid: orange clay streaked with ember, hanging down the cliff into the void."""
    land, rift, ed, bottom = ctx["land"], ctx["rift"], ctx["ed"], ctx["bottom"]
    n = 0
    for i, k in np.argwhere(rift & (ed <= 0)):
        for di, dk in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, k + dk
            if not (0 <= a < LD.SX and 0 <= b < LD.SZ) or land[a, b]:
                continue
            length = 14 + int(rng.integers(0, 12)) + 4 * int(abs(k - LD.SZ // 2) < 6)
            top = LD.LAVA + 1
            for j in range(length):
                y = top - j
                if y < 10:
                    break
                w.ids[a, y, b], w.dat[a, y, b] = ((B.STAINED_CLAY, 1) if j % 4 else (B.GLOWSTONE, 0))
            n += 1
    return n
