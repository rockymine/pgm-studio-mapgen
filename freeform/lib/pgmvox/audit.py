"""Footing: the blocks that would fall or pop off when the world loads.

    footing(w, box=None)  -> [(x, y, z, why)]

Sand, gravel and anvils over air fall. Torches, ladders, wall signs, wall banners, buttons and levers hang on the
block their data names, and pop off when it is air or something they cannot hang on (another passable block).
A board runs this over its whole world before writing it; the plot kit ran it over each plot.
"""
import numpy as np

from . import blocks as K
from .blocks import B

# (id) -> {data: (dx, dy, dz) to the block holding it}
_WALL = {2: (0, 0, 1), 3: (0, 0, -1), 4: (1, 0, 0), 5: (-1, 0, 0)}
_TORCH = {1: (-1, 0, 0), 2: (1, 0, 0), 3: (0, 0, -1), 4: (0, 0, 1), 5: (0, -1, 0)}
_BUTTON = {1: (-1, 0, 0), 2: (1, 0, 0), 3: (0, 0, -1), 4: (0, 0, 1)}
HANGS = {
    B.LADDER: _WALL, B.WALL_SIGN: _WALL, B.WALL_BANNER: _WALL,
    B.TORCH: _TORCH, B.REDSTONE_TORCH: _TORCH, 75: _TORCH,
    B.BUTTON_STONE: _BUTTON, B.BUTTON_WOOD: _BUTTON, B.LEVER: {**_BUTTON, 5: (0, -1, 0), 6: (0, -1, 0)},
}
STANDS = {B.SIGN_POST, B.BANNER, B.FLOWER_POT, B.CARPET, B.RAIL, B.RAIL_POWERED, B.RAIL_DETECTOR,
          B.RAIL_ACTIVATOR, B.PLATE_STONE, B.PLATE_WOOD, B.REDSTONE_WIRE, B.SNOW_LAYER} | K.DOORS


def footing(w, box=None):
    """Every block in the world (or in box = (x0, y0, z0, x1, y1, z1)) that falls or has nothing to hang on."""
    out = []
    ids, dat = w.ids, w.dat
    if box:
        x0, y0, z0, x1, y1, z1 = box
        sl = (slice(x0 - w.x0, x1 - w.x0 + 1), slice(y0, y1 + 1), slice(z0 - w.z0, z1 - w.z0 + 1))
        off = (x0 - w.x0, y0, z0 - w.z0)
    else:
        sl = (slice(None),) * 3
        off = (0, 0, 0)
    sub = ids[sl]
    interesting = np.isin(sub, sorted(K.GRAVITY | set(HANGS) | STANDS))
    passable = K.mask(ids, K.PASSABLE)
    for i, y, k in np.argwhere(interesting):
        a, b, c = i + off[0], y + off[1], k + off[2]
        bid, d = int(ids[a, b, c]), int(dat[a, b, c])
        x, z, b = int(a + w.x0), int(c + w.z0), int(b)
        if bid in K.GRAVITY:
            if b > 0 and ids[a, b - 1, c] == 0:
                out.append((x, b, z, f"block {bid} over air: it falls"))
            continue
        if bid in HANGS:
            on = HANGS[bid].get(d & 7)
            if on is None:
                out.append((x, b, z, f"block {bid} with data {d} faces nowhere"))
                continue
        else:
            on = (0, -1, 0)
            if bid in K.DOORS and d & 8:
                continue                                         # an upper door half stands on its lower half
        ha, hb, hc = a + on[0], b + on[1], c + on[2]
        if not (0 <= ha < w.sx and 0 <= hb < w.sy and 0 <= hc < w.sz) or passable[ha, hb, hc]:
            out.append((x, b, z, f"block {bid} hangs on nothing: it pops off"))
    return out
