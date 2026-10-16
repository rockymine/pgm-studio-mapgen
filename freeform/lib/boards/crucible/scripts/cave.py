"""Crucible's two caves: the lava tube from the sinkhole to the casting pit's floor, its walls glazed black, and the
flank cave from the west spur down to the cold store, cut through the beds with a chamber halfway.

    cave.build(w, C) after the foundry is carved, so a cave never cuts a lined wall it does not mean to
"""
import numpy as np

import palette as P
import plan as PL
from pgmvox import B
from pgmvox.volume import under


def _floor_fn(pts):
    import math
    from pgmvox.geom.shapes import nearest_on
    arc = np.concatenate([[0], np.cumsum([math.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts, pts[1:])])])
    plan = [(p[0], p[2]) for p in pts]

    def floor(x, z):
        return int(round(np.interp(nearest_on(plan, x, z)[1], arc, [p[1] for p in pts])))
    return floor


def glaze(w, box, floor_fn, seed):
    """Every rock face of the air in `box` (x0, x1, y0, y1, z0, z1) laid in the basalt set, the floor in rubble."""
    x0, x1, y0, y1, z0, z1 = box
    rng = np.random.default_rng(seed)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for y in range(y0, y1 + 1):
                if w.id(x, y, z) != B.AIR:
                    continue
                for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    a, b, c = x + dx, y + dy, z + dz
                    i = w.id(a, b, c)
                    if i in (B.STONE, B.COBBLE, B.STAINED_CLAY, B.NETHERRACK, B.COAL_BLOCK):
                        name = "rubble" if dy == -1 else "basalt"
                        ids, dat = P.pick(name, np.array([rng.random()]))
                        w.set(a, b, c, int(ids[0]), int(dat[0]))


def build(w, C):
    keep = None
    high = None
    # the lava tube: no cover kept, so it opens into the sinkhole and onto the pit's floor
    under.tunnel(w, PL.TUBE, ground=high, cover=0, keep=keep)
    xs = [p[0] for p in PL.TUBE]
    zs = [p[2] for p in PL.TUBE]
    glaze(w, (min(xs) - 4, max(xs) + 2, 37, 46, min(zs) - 4, max(zs) + 4), _floor_fn(PL.TUBE), 21)
    # the flank cave: from the spur's face into the mountain, down to the cold store's west wall
    under.tunnel(w, PL.FLANK, ground=high, cover=0, keep=keep)
    for cx, fy, cz, rx, h, rz in PL.CAVE_CHAMBERS:
        under.chamber(w, cx, fy, cz, rx, h, rz, ground=high, cover=0, keep=keep)
    # the cave's floor: rubble laid on whatever the beds left, so the way reads underfoot
    fl = _floor_fn(PL.FLANK)
    rng = np.random.default_rng(23)
    xs = [p[0] for p in PL.FLANK]
    zs = [p[2] for p in PL.FLANK]
    for x in range(min(xs) - 6, max(xs) + 6):
        for z in range(min(zs) - 6, max(zs) + 6):
            f = fl(x, z)
            for y in (f, f + 1):
                if w.id(x, y, z) == B.AIR and w.id(x, y - 1, z) not in (B.AIR, B.WATER) and not C.is_air(x, y, z):
                    ids, dat = P.pick("haul", np.array([rng.random()]))
                    w.set(x, y - 1, z, int(ids[0]), int(dat[0]))
                    break
