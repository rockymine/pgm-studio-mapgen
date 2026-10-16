"""The rift: a river of lava between the two halves, its floor, its dams at the ends, its shelves and stepping
stones."""
import numpy as np

import land as LD
from pgmvox import B


def lava(w, ctx):
    H, rift, ed = ctx["H"], ctx["rift"], ctx["ed"]
    X, Z = ctx["X"], ctx["Z"]
    n = 0
    for i, k in np.argwhere(rift):
        h = int(H[i, k])
        dam = ed[i, k] < 3
        if dam:
            for y in range(int(ctx["bottom"][i, k]), h + 1):
                w.ids[i, y, k], w.dat[i, y, k] = ((B.OBSIDIAN, 0), (B.COAL_BLOCK, 0))[int((i + k + y) % 3 == 0)]
            continue
        w.ids[i, h, k], w.dat[i, h, k] = B.OBSIDIAN, 0
        for y in range(h + 1, LD.LAVA + 1):
            w.ids[i, y, k], w.dat[i, y, k] = B.LAVA, 0
        n += 1
    return n


def stones(w, ctx):
    """Two crossings of the lava on foot: pillars of obsidian two above the lava, a jump apart, and a lit post at
    each landing."""
    for xc in (-20, 20):
        u = xc + 0.5
        c = float(LD.centre(u))
        hw = float(LD.half_width(u))
        zs = np.arange(c - hw + 1.2, c + hw - 0.5, 3.6)
        for z0 in zs:
            for dx in range(-1, 2):
                for dz in range(-1, 2):
                    x, z = xc + dx, int(round(z0 - 0.5)) + dz
                    for y in range(LD.FLOOR + 1, LD.SHELF_Y):
                        w.set(x, y, z, B.OBSIDIAN, 0)
                    w.set(x, LD.SHELF_Y - 1, z, (B.OBSIDIAN, 0)[0], 0)
        # the landing posts, on the ledge at either end
    return len(zs)


def streaks(w, ctx, seed=4):
    """Frozen falls down the north wall and seams of ember down the south one: the top two blocks of the wall's
    columns in a narrow strip, which is the whole of a stepped face."""
    rng = np.random.default_rng(seed)
    H, cd, X, Z = ctx["H"], ctx["cd"], ctx["X"], ctx["Z"]
    land = ctx["land"]
    n = 0
    for x0 in (-52, -43, -33, -24, -15, -6, 7, 16, 25, 36, 45, 53):
        width = int(rng.integers(2, 4))
        for x in range(x0, x0 + width):
            for z in range(-30, 30):
                i, k = x - LD.X0, z - LD.Z0
                if not land[i, k] or cd[i, k] <= LD.SHELF_W or cd[i, k] > 9.8 or ctx["laid"][i, k]:
                    continue
                north = z < 0
                h = int(H[i, k])
                for y in (h, h - 1):
                    if north:
                        w.ids[i, y, k], w.dat[i, y, k] = ((B.PACKED_ICE, 0) if (x + y) % 3 else (B.ICE, 0))
                    else:
                        w.ids[i, y, k], w.dat[i, y, k] = ((B.STAINED_CLAY, 1) if (x + y) % 3 else (B.GLOWSTONE, 0))
                n += 1
    return n
