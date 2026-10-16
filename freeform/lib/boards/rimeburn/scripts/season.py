"""The two seasons. Frost's half is laid as winter; Ember's is the same ground and the same buildings re-seasoned
block by block into the last of autumn, then each half gets the trees and the dressing only its season has.

    ground      snow -> Mesa grass (olive-brown under the biome); packed-ice patches -> podzol, leaf litter;
                scree gravel -> coarse dirt; ice -> water; snow layers gone, but above y 58 the snow stays: the
                first of the winter on Ember's peaks
    paths       andesite, cobble, polished andesite -> coarse dirt, dirt, spruce planks
    buildings   spruce walls -> acacia, spruce posts -> dark oak, dark oak roofs -> nether brick, sea lanterns ->
                glowstone; the stone-brick foot, the quartz and the packed ice of the shrine stay as they are
    trees       Frost: spruces with snow on their boughs; Ember: oaks whose crowns turn brown, orange and red
"""
import math

import numpy as np

import land as LD
from pgmvox import B
from pgmvox.core.orient import turn_world
from pgmvox.scenery import trees as TR

FROST_BIOME = 12            # Ice Plains: grass and leaves #80b497 / #60a17b, the cold that agrees with snow
EMBER_BIOME = 37            # Mesa: grass #90814d, leaves #9e814d, the brown that meets podzol as one floor

TERRAIN = {(B.SNOW, 0): (B.GRASS, 0), (B.PACKED_ICE, 0): (B.DIRT, 2), (B.GRAVEL, 0): (B.DIRT, 1),
           (B.ICE, 0): (B.WATER, 0)}
PATH = {(B.STONE, 5): (B.DIRT, 1), (B.COBBLE, 0): (B.DIRT, 0), (B.STONE, 6): (B.PLANKS, 1)}
MADE = {B.DARK_OAK_STAIRS: B.NETHER_STAIRS, B.SPRUCE_STAIRS: B.DARK_OAK_STAIRS, B.SPRUCE_FENCE: B.DARK_OAK_FENCE,
        B.SPRUCE_DOOR: B.DARK_OAK_DOOR}
MADE_DATA = {(B.PLANKS, 1): (B.PLANKS, 4), (B.PLANKS, 5): (B.NETHER_BRICK, 0), (B.WOOD_SLAB, 5): (B.SLAB, 6),
             (B.WOOD_SLAB, 1): (B.WOOD_SLAB, 5), (B.SEA_LANTERN, 0): (B.GLOWSTONE, 0)}


def reseason(w, made, path, snow_line=58):
    """Turn Frost's half of `w` (z < 0) into Ember's in place: `made` is a boolean volume of what was built,
    `path` a column mask of the paths."""
    nz = -LD.Z0                                         # columns z0 .. -1
    ids, dat = w.ids[:, :, :nz], w.dat[:, :, :nz]
    mk = made[:, :, :nz]
    ys = np.arange(w.sy)[None, :, None]
    terrain = ~mk
    # the paths: the top of each path column
    top = w.heightmap()[:, :nz]
    for (a, ad), (b, bd) in PATH.items():
        m = (ids == a) & (dat == ad) & terrain & path[:, None, :nz] & (ys == top[:, None, :])
        ids[m], dat[m] = b, bd
    for (a, ad), (b, bd) in TERRAIN.items():
        m = (ids == a) & (dat == ad) & terrain
        if a == B.SNOW:
            m &= ys < snow_line
        ids[m], dat[m] = b, bd
    m = (ids == B.SNOW_LAYER) & (ys < snow_line + 1)
    ids[m], dat[m] = B.AIR, 0
    for a, b in MADE.items():
        m = (ids == a) & mk
        ids[m] = b
    m = (ids == B.LOG) & ((dat & 3) == 1) & mk
    ids[m] = B.LOG2
    dat[m] = (dat[m] & 12) | 1
    for (a, ad), (b, bd) in MADE_DATA.items():
        m = (ids == a) & (dat == ad) & mk
        ids[m], dat[m] = b, bd


def carry(w, made, path):
    """Ember's half: a copy of `w` re-seasoned and turned onto the south. `w` itself is changed only south of the
    middle."""
    import copy
    w2 = copy.deepcopy(w)
    reseason(w2, made, path)
    turn_world(w2, "half", lambda x, z: z < 0)
    nz = -LD.Z0
    w.ids[:, :, nz:] = w2.ids[:, :, nz:]
    w.dat[:, :, nz:] = w2.dat[:, :, nz:]
    w.biome[:, :nz] = FROST_BIOME
    w.biome[:, nz:] = EMBER_BIOME


# ---- the trees ------------------------------------------------------------------------------------------------
# Frost's sites; Ember plants at each one's image. (x, z, kind) with kind "tall" or "small".
SITES = [
    (-54, -79, "tall"), (-49, -87, "small"), (-58, -70, "tall"), (-46, -78, "small"), (-56, -61, "small"),
    (-42, -88, "tall"), (-60, -86, "small"),                                    # the Rimewood, west of the hollow
    (16, -92, "tall"), (25, -88, "small"), (-14, -91, "small"),                 # under the Rimewall
    (52, -77, "tall"), (57, -66, "small"), (46, -83, "small"), (58, -84, "tall"),   # behind the shelf
    (12, -50, "small"), (27, -51, "tall"),                                      # the Tarn's north shore
    (59, -40, "small"), (36, -30, "small"),                                     # by Rimecroft
    (-57, -46, "small"), (-58, -32, "tall"),                                    # the west headland, past the Anvil
]
THROUGH = TR.PLANTS | {B.SNOW_LAYER}
GIVES = TR.GIVES_WAY | {B.SNOW}


def _clump(x, y, z, seed, cell=2):
    h = ((x + 999) // cell * 73856093) ^ ((y + 999) // cell * 19349663) ^ ((z + 999) // cell * 83492791) ^ seed
    return (h & 0xffff) / 65535.0


def plant_trees(w, ok, rng):
    """Each site takes a tree of its kind in both halves; where one will not stand whole (a crown into rock or off
    the board's edge) another of the kind, another turn, or a spot a block or three off is tried."""
    lib = TR.kinds(TR.library())
    stood = []

    def one(x, z, group, through, gives, after, ember):
        for attempt in range(16):
            ox, oz = (0, 0) if attempt == 0 else (int(rng.integers(-3, 4)), int(rng.integers(-3, 4)))
            px, pz = x + ox, z + oz
            if not ok(*(LD.SYM.point(px, pz) if ember else (px, pz))):
                continue
            t = group[int(rng.integers(len(group)))]
            if TR.plant(w, px, pz, t, int(rng.integers(4)), through=through, gives_way=gives):
                after(px, pz, t)
                return (px, pz, t.name)
        return None

    for x, z, kind in SITES:
        frost = lib["tall-spruce" if kind == "tall" else "tiny-spruce"]
        ember = lib["dense-oak" if kind == "tall" else "tiny-oak"]
        got = one(x, z, frost, THROUGH, GIVES, lambda px, pz, t: frost_tree(w, px, pz, t.crown + 1, rng), False)
        if got:
            stood.append((*got, "frost"))
        ex, ez = LD.SYM.point(x, z)
        maple = rng.random() < 0.45
        got = one(ex, ez, ember, TR.PLANTS, GIVES,
                  lambda px, pz, t: ember_tree(w, px, pz, t.crown + 1, rng, maple), True)
        if got:
            stood.append((*got, "ember"))
    return stood


def _box(w, x, z, r):
    for X in range(x - r, x + r + 1):
        for Z in range(z - r, z + r + 1):
            if w.inside(X, 0, Z):
                yield X, Z


def frost_tree(w, x, z, r, rng):
    """A spruce: acacia trunk to spruce, birch leaves to spruce leaves, and snow lying on the boughs."""
    for X, Z in _box(w, x, z, r):
        col = w.ids[X - w.x0, :, Z - w.z0]
        dcol = w.dat[X - w.x0, :, Z - w.z0]
        for y in np.nonzero((col == B.LOG2) | (col == B.LEAVES))[0]:
            if col[y] == B.LOG2:
                col[y], dcol[y] = B.LOG, 1 | (dcol[y] & 12)
            else:
                col[y], dcol[y] = B.LEAVES, 1 | 4
        for y in np.nonzero(col == B.LEAVES)[0]:
            if y + 1 < w.sy and col[y + 1] == B.AIR and rng.random() < 0.8:
                col[y + 1], dcol[y + 1] = B.SNOW_LAYER, 0


def ember_tree(w, x, z, r, rng, maple):
    """An oak in autumn: its leaves the biome's brown, clumps turned orange, and in a maple red as well."""
    seed = int(rng.integers(1 << 16))
    for X, Z in _box(w, x, z, r):
        col = w.ids[X - w.x0, :, Z - w.z0]
        dcol = w.dat[X - w.x0, :, Z - w.z0]
        for y in np.nonzero(col == B.LEAVES)[0]:
            c = 0.6 * _clump(X, y, Z, seed, 1) + 0.4 * _clump(X, y, Z, seed + 3, 3)
            if maple:
                blk = (B.WOOL, 14) if c < 0.36 else (B.WOOL, 1) if c < 0.55 else (B.LEAVES, 4)
            else:
                blk = (B.WOOL, 1) if c < 0.3 else (B.LEAVES, 4)
            col[y], dcol[y] = blk
    # the leaves it has dropped: litter on the grass under its crown, and the freshest fallen in drifts on top
    for X, Z in _box(w, x, z, r + 1):
        d = math.hypot(X - x, Z - z)
        if d > r + 0.5:
            continue
        y = w.top(X, Z)
        if y <= 0 or w.id(X, y, Z) != B.GRASS or w.id(X, y + 1, Z) != B.AIR:
            continue
        c = _clump(X, 0, Z, seed + 7, 2)
        if d < r * 0.8 and c < 0.4:
            w.set(X, y, Z, B.DIRT, 2)
        elif c > 0.55 and rng.random() < 0.7:
            w.set(X, y + 1, Z, B.CARPET, 14 if maple and c > 0.8 else 1 if c > 0.68 else 12)


# ---- each season's dressing -------------------------------------------------------------------------------------
def dress_frost(w, made, warm, H):
    """Snow lying on every flat built top in Frost's half above the ground: roofs, walls' caps, the deck; the yards
    and floors people walk stay swept."""
    nz = -LD.Z0
    top = w.heightmap()
    for i in range(w.sx):
        for k in range(nz):
            y = int(top[i, k])
            if y <= H[i, k] + 1 or y + 1 >= w.sy or not made[i, y, k] or warm[i, k]:
                continue
            b, d = int(w.ids[i, y, k]), int(w.dat[i, y, k])
            if b in (B.PLANKS, B.STONEBRICK, B.COBBLE, B.STONE, B.LOG) and w.ids[i, y + 1, k] == B.AIR:
                w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.SNOW_LAYER, 0


def dress_ember(w, keep_clear, rng):
    """Ember's meadow: flowers of the season in drifts (orange and red tulips, poppies), ferns and short grass, kept
    low and off the paths and the goals; and pumpkins by the byre at Embercroft."""
    from pgmvox.geom import noise
    nz = -LD.Z0
    drift = noise.fbm((w.sx, w.sz), 6, 2, seed=LD.SEED + 40)
    fern = noise.fbm((w.sx, w.sz), 4, 2, seed=LD.SEED + 41)
    top = w.heightmap()
    flowers = [(B.FLOWER, 5), (B.FLOWER, 4), (B.FLOWER, 0), (B.FLOWER, 5)]
    for i in range(w.sx):
        for k in range(nz, w.sz):
            y = int(top[i, k])
            x, z = i + w.x0, k + w.z0
            if y <= 0 or w.ids[i, y, k] != B.GRASS or w.ids[i, y + 1, k] != B.AIR or (x, z) in keep_clear:
                continue
            r = rng.random()
            if drift[i, k] > 0.35 and r < 0.4:
                w.ids[i, y + 1, k], w.dat[i, y + 1, k] = flowers[int(rng.integers(len(flowers)))]
            elif fern[i, k] > 0.3 and r < 0.18:
                w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.TALLGRASS, 2
            elif r < 0.07:
                w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.TALLGRASS, 1


def ember_falls(w, frost_cells):
    """Ember's Rime Falls is not frozen: the notch's ice turned to water, so the burn comes down the Rimewall in
    steps of still pools."""
    top = max(y for x, y, z in frost_cells)
    for x, y, z in frost_cells:
        ex, ez = LD.SYM.point(x, z)
        if w.id(ex, y, ez) == B.ICE:
            w.set(ex, y, ez, *((B.WATER, 0) if y == top else (B.WATER_FLOW, 8)))


def thaw_line(w, made):
    """On the Thaw the seasons do not meet on a ruled line: the edge between snow and autumn wanders across the
    island, snow lying a few blocks into Ember's half and grass showing a few blocks into Frost's."""
    from pgmvox.geom import noise
    f = noise.fbm((w.sx, w.sz), 7, 2, seed=LD.SEED + 50)
    top = w.heightmap()
    for i in range(w.sx):
        for k in range(w.sz):
            x, z = i + w.x0, k + w.z0
            if abs(x) > 24 or abs(z + 0.5) > 12:
                continue
            y = int(top[i, k])
            if y <= 0 or made[i, y, k]:
                continue
            ember = (z + 0.5) + 4.5 * f[i, k] > 0
            b = int(w.ids[i, y, k])
            if ember and b == B.SNOW:
                w.ids[i, y, k], w.dat[i, y, k] = B.GRASS, 0
                if w.ids[i, y + 1, k] == B.SNOW_LAYER:
                    w.ids[i, y + 1, k] = B.AIR
            elif not ember and b == B.GRASS:
                w.ids[i, y, k], w.dat[i, y, k] = B.SNOW, 0
                if w.ids[i, y + 1, k] == B.AIR:
                    w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.SNOW_LAYER, 0


def croft_yard(w, rng):
    """By each byre: hay stacked against its wall; at Embercroft, pumpkins ripe in the stubble beside it."""
    bx, bz = 50, -36
    for dx, dz, h in ((0, 0, 2), (1, 0, 1), (0, 1, 1)):
        for side in (False, True):
            x, z = (bx + dx, bz + dz) if not side else LD.SYM.point(bx + dx, bz + dz)
            y = w.top(x, z)
            for k in range(1, h + 1):
                w.set(x, y + k, z, B.HAY, 0)
            if not side:
                w.set(x, y + h + 1, z, B.SNOW_LAYER, 0)
    px, pz = LD.SYM.point(56, -40)
    for dx in range(-3, 4):
        for dz in range(-2, 3):
            if rng.random() < 0.35:
                y = w.top(px + dx, pz + dz)
                if w.id(px + dx, y, pz + dz) in (B.GRASS, B.DIRT) and w.id(px + dx, y + 1, pz + dz) in (0, B.TALLGRASS, B.FLOWER):
                    w.set(px + dx, y, pz + dz, B.DIRT, 1)
                    w.set(px + dx, y + 1, pz + dz, B.PUMPKIN, int(rng.integers(4)))
