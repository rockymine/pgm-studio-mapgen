"""Crucible's palette: the board's three tone families and the sets each one is laid with.

    ground   the slag plain and the mountain's ash: black and grey stained clay with coal, a dark scorched set;
             the cinder cone's scoria in netherrack and brown clay; the rock beds of every cut and cliff
    built    the foundries: stone brick and polished andesite, pilasters of smooth double slab stepped out,
             panels of nether brick sunk a block, an orange band inset at the lintels, iron where a thing is a machine
    accent   lava and its glow, the teams' glass, and the one cold room's quartz, prismarine and sea lanterns

A set is several blocks close in tone; `pick` draws one per block from a noise value in [0, 1), so a set is laid as
patches rather than as one block.
"""
import numpy as np
from scipy import ndimage

from pgmvox import B

SETS = {
    # ground
    "ash":      [((B.STAINED_CLAY, 15), 0.22), ((B.STAINED_CLAY, 7), 0.60), ((B.STAINED_CLAY, 12), 0.18)],
    "scoria":   [((B.NETHERRACK, 0), 0.30), ((B.STAINED_CLAY, 12), 0.40), ((B.STAINED_CLAY, 15), 0.30)],
    "basalt":   [((B.STAINED_CLAY, 15), 0.55), ((B.COAL_BLOCK, 0), 0.45)],
    "rubble":   [((B.STAINED_CLAY, 15), 0.35), ((B.STAINED_CLAY, 7), 0.40), ((B.COBBLE, 0), 0.25)],
    "rock":     [((B.STONE, 5), 0.55), ((B.STONE, 0), 0.30), ((B.COBBLE, 0), 0.15)],
    "slate":    [((B.STAINED_CLAY, 9), 0.85), ((B.STONE, 5), 0.15)],
    "tuff":     [((B.STAINED_CLAY, 7), 0.6), ((B.STAINED_CLAY, 12), 0.4)],
    "red":      [((B.NETHERRACK, 0), 0.6), ((B.HARDENED_CLAY, 0), 0.4)],
    "scorch":   [((B.OBSIDIAN, 0), 0.5), ((B.STAINED_CLAY, 15), 0.3), ((B.NETHERRACK, 0), 0.2)],
    "haul":     [((B.GRAVEL, 0), 1 / 3), ((B.STONE, 5), 1 / 3), ((B.COBBLE, 0), 1 / 3)],
    # built
    "floor":    [((B.STONEBRICK, 0), 0.25), ((B.STONE, 6), 0.25), ((B.STONE, 5), 0.25), ((B.STONE, 0), 0.25)],
    "deck":     [((B.DSLAB, 0), 0.5), ((B.STONE, 6), 0.5)],
}


def pick(name, u):
    """Blocks of set `name` for noise values u in [0, 1): (ids, data) arrays shaped like u."""
    members = SETS[name]
    w = np.cumsum([m[1] for m in members])
    w = w / w[-1]
    idx = np.searchsorted(w, np.clip(u, 0, 0.999999), side="right")
    ids = np.array([m[0][0] for m in members])[idx]
    dat = np.array([m[0][1] for m in members])[idx]
    return ids, dat


def uniform(a):
    """Noise values ranked to an even spread over [0, 1)."""
    flat = a.ravel()
    r = np.empty(flat.size)
    r[np.argsort(flat, kind="stable")] = np.arange(flat.size) / flat.size
    return r.reshape(a.shape)


def noise3(shape, cell, seed):
    """A smooth 3-D noise in [0, 1), patches about `cell` across (a number, or one a side: lenses in a bed are
    long across and short up)."""
    cells = cell if isinstance(cell, (tuple, list)) else (cell,) * 3
    rng = np.random.default_rng(seed)
    gs = [max(2, s // c + 3) for s, c in zip(shape, cells)]
    g = rng.uniform(0, 1, gs)
    up = ndimage.zoom(g, cells, order=1)
    return uniform(up[:shape[0], :shape[1], :shape[2]])


def noise2(shape, cell, seed):
    rng = np.random.default_rng(seed)
    gs = [max(2, s // cell + 3) for s in shape]
    g = rng.uniform(0, 1, gs)
    up = ndimage.zoom(g, [cell] * 2, order=1)
    return uniform(up[:shape[0], :shape[1]])


def cells(X, Z, size=2, seed=0):
    """A paving: one value a cell of `size`, the rows staggered, even shares over the set's members."""
    h = (np.floor((X + (np.floor_divide(Z, size) % 2) * (size // 2)) / size).astype(np.int64) * 73856093
         ^ np.floor_divide(Z, size).astype(np.int64) * 19349663 ^ seed * 83492791)
    return (h % 1000) / 1000.0
