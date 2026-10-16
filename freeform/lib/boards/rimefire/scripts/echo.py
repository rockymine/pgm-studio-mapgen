"""The fire half's built things, turned half round the board onto the ice half in the ice half's materials.

Everything a place builder writes north of the board's middle is recorded as a change to the world; `mirror_changes`
carries each changed block to its half turn, turns its data (stairs, doors, logs, banners) and swaps its material
through `ICE`, so one builder makes both halves and the two are the same bones in two skins.
"""
import numpy as np

from pgmvox import B
from pgmvox.core.orient import data_table

H = 8                                    # a slab's top bit

# (id, data or None for any) -> (id, data or None for unchanged); the first key that matches wins
ICE = {
    (B.ACACIA_STAIRS, None): (B.DARK_OAK_STAIRS, None),
    (B.ACACIA_FENCE, None): (B.DARK_OAK_FENCE, None),
    (B.ACACIA_DOOR, None): (B.SPRUCE_DOOR, None),
    (B.PLANKS, 4): (B.PLANKS, 5),
    (B.WOOD_SLAB, 4): (B.WOOD_SLAB, 5), (B.WOOD_SLAB, 12): (B.WOOD_SLAB, 13),
    (B.RED_SANDSTONE, 0): (B.QUARTZ, 0), (B.RED_SANDSTONE, 1): (B.QUARTZ, 1), (B.RED_SANDSTONE, 2): (B.QUARTZ, 0),
    (B.RED_SANDSTONE_STAIRS, None): (B.QUARTZ_STAIRS, None),
    (B.RED_SANDSTONE_SLAB, 0): (B.SLAB, 7), (B.RED_SANDSTONE_SLAB, 8): (B.SLAB, 15),
    (B.NETHER_BRICK, None): (B.PRISMARINE, 1),
    (B.NETHER_STAIRS, None): (B.STONEBRICK_STAIRS, None),
    (B.NETHER_FENCE, None): (B.SPRUCE_FENCE, 0),
    (B.GLOWSTONE, None): (B.SEA_LANTERN, 0),
    (B.JACK, None): (B.SEA_LANTERN, 0),
    (B.NETHERRACK, None): (B.PACKED_ICE, 0),
    (B.LAVA, None): (B.ICE, 0), (B.LAVA_FLOW, None): (B.ICE, 0),
    (B.FIRE, None): (B.SEA_LANTERN, 0),
    (B.HAY, None): (B.SNOW, 0),
    (B.PUMPKIN, None): (B.SNOW, 0),
    (B.STAINED_CLAY, 1): (B.STAINED_CLAY, 3), (B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11),
    (B.COAL_BLOCK, None): (B.STONE, 6),
    (B.STAINED_GLASS, 1): (B.STAINED_GLASS, 3),
    (B.STONE, 1): (B.STONE, 5), (B.STONE, 2): (B.STONE, 6), (B.BRICK, None): (B.STONEBRICK, 0),
    (B.DIRT, 2): (B.SNOW, 0), (B.DIRT, 1): (B.GRAVEL, 0),
    (B.HARDENED_CLAY, None): (B.PACKED_ICE, 0), (B.STAINED_CLAY, 12): (B.PACKED_ICE, 0),
    (B.WATER, None): (B.ICE, 0), (B.WATER_FLOW, None): (B.ICE, 0),
    (B.WOOL, 1): (B.WOOL, 3), (B.WOOL, 14): (B.WOOL, 11), (B.WOOL, 4): (B.WOOL, 0),
}
BANNERS = {1: 4, 14: 12, 11: 6}          # red -> blue, orange -> light blue


def _map(ids, dat, table):
    ids = ids.copy()
    dat = dat.copy()
    out_i, out_d = ids.copy(), dat.copy()
    done = np.zeros(ids.shape, bool)
    for (a, ad), (b, bd) in table.items():
        m = (ids == a) & ~done
        if ad is not None:
            m &= dat == ad
        out_i[m] = b
        if bd is not None:
            out_d[m] = bd
        done |= m
    return out_i, out_d


def mirror_changes(w, before_ids, before_dat, tiles_from, palette=ICE):
    """Carry every block changed since `before` in the north half (z < -0.5) to its half turn. Returns how many."""
    changed = (w.ids != before_ids) | (w.dat != before_dat)
    zs = np.arange(w.z0, w.z0 + w.sz)
    changed &= (zs < -0.5)[None, None, :]
    xi, yi, zi = np.nonzero(changed)
    ids, dat = w.ids[xi, yi, zi], w.dat[xi, yi, zi]
    table = data_table("half")
    dat = table[ids, dat & 15]
    nid, nd = _map(ids, dat, palette)
    ix = (-1 - (xi + w.x0)) - w.x0
    iz = (-1 - (zi + w.z0)) - w.z0
    ok = (ix >= 0) & (ix < w.sx) & (iz >= 0) & (iz < w.sz)
    w.ids[ix[ok], yi[ok], iz[ok]] = nid[ok]
    w.dat[ix[ok], yi[ok], iz[ok]] = nd[ok]
    for te in list(w.tiles[tiles_from:]):
        m = dict(te)
        m["x"], m["z"] = -1 - te["x"], -1 - te["z"]
        if te.get("kind") == "Banner":
            m["base"] = BANNERS.get(te["base"], te["base"])
            m["patterns"] = [dict(p, color=BANNERS.get(p["color"], p["color"])) for p in te.get("patterns", [])]
        w.tiles.append(m)
    return int(ok.sum())
