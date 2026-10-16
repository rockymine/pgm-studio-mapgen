"""Thawline's trees and ground cover. A tree is placed in Frost's coordinates and planted on both halves, the same
cut turned half round, so the cover it gives is the same for both teams; only its wood and its leaves change.

Two kinds a half, by how deep into its half a tree stands:

    Frost, the back     spruce, dark, with snow lying on the crowns (past a depth of 0.5)
    Frost, the front    oak in its autumn colour, the first snow on the crowns
    Ember, the front    the same oaks, no snow; each crown rust, flame or copper (CROWNS)
    Ember, the back     larches: the spruce's own cut in gold, as a larch turns before it drops its needles

The woods, each with its reason (`SITES` names them):

    Rimewood        between the Kettle and the rift: cover to within twelve of the Kettle's rim, for the attack
    the groves      on the Glacier's spurs either side of the hall: they frame the spawn, nobody fights in them
    the Beckside    along the beck below the hamlet, where trees grow by water
    behind the green  three on its north side, between the green and the hall
    the crag's foot  a stand at Hoarcrag's foot, west of the Kettle
"""
import math

import numpy as np

import plan as P
from pgmvox import B
from pgmvox.geom import shapes
from pgmvox.scenery import trees as TR
from season import MESA, SAVANNA

# (name, polygon in Frost's coordinates, how many, least spacing in blocks)
SITES = [
    ("Rimewood", [(-62, -46), (-40, -46), (-35, -32), (-38, -16), (-61, -15)], 12, 8.0),
    ("west grove", [(-40, -96), (-17, -98), (-17, -82), (-28, -74), (-42, -80)], 7, 6.5),
    ("east grove", [(16, -98), (40, -96), (42, -80), (30, -74), (17, -82)], 7, 6.5),
    ("Beckside", [(36, -26), (58, -24), (56, -14), (40, -14)], 5, 7.0),
    ("behind the green", [(22, -72), (42, -72), (42, -67), (22, -67)], 3, 8.0),
    ("the crag's foot", [(-52, -78), (-40, -76), (-42, -68), (-52, -70)], 3, 7.0),
]
KEEP_OFF = 3.0
SOLID = TR.GIVES_WAY | {B.SNOW, B.PACKED_ICE, B.STONEBRICK, B.SANDSTONE, B.STAINED_CLAY, B.COAL_BLOCK, B.OBSIDIAN}              # a tree's trunk keeps this far from a road's middle line and from water


def library():
    lib = TR.library()
    by = TR.kinds(lib)
    return by


# the crowns: what a leaf block of the cut becomes, drawn per block. Autumn is the biome's brown leaves with wool in
# the colours the biome cannot give (orange, red, yellow, brown); a larch is Savanna's gold leaves flecked yellow.
CROWNS = {
    "spruce": [((B.LEAVES, 1 | 4), 1.0)],
    "rust": [((B.LEAVES, 0 | 4), 0.52), ((B.WOOL, 1), 0.24), ((B.WOOL, 14), 0.14), ((B.WOOL, 12), 0.10)],
    "flame": [((B.LEAVES, 0 | 4), 0.48), ((B.WOOL, 1), 0.34), ((B.WOOL, 4), 0.18)],
    "copper": [((B.LEAVES2, 1 | 4), 0.55), ((B.WOOL, 14), 0.2), ((B.WOOL, 1), 0.15), ((B.WOOL, 12), 0.10)],
    "larch": [((B.LEAVES, 0 | 4), 0.8), ((B.WOOL, 4), 0.13), ((B.WOOL, 1), 0.07)],
}


def remap(tree, wood, crown, rng):
    """A cut with its wood swapped (logs keep their axis bits) and every leaf drawn from the crown's recipe."""
    blocks, weights = zip(*CROWNS[crown])
    p = np.array(weights) / sum(weights)
    out = []
    for dx, dy, dz, i, d in tree.blocks:
        if i in (B.LOG, B.LOG2):
            i, d = wood[0], (d & 12) | wood[1]
        elif i in (B.LEAVES, B.LEAVES2):
            i, d = blocks[int(rng.choice(len(blocks), p=p))]
        elif i == B.PLANKS:
            i, d = B.PLANKS, 1 if wood == (B.LOG, 1) else 5
        elif i == B.WOOD_SLAB:
            i, d = B.WOOD_SLAB, 1 if wood == (B.LOG, 1) else 5
        out.append((dx, dy, dz, i, d))
    return TR.Tree(tree.name, tree.kind, tuple(out), tree.crown, tree.height)


def sites(rng):
    """Every tree's foot in Frost's coordinates with its wood's name: spaced in each wood, off the roads, the
    water and the made ground."""
    X, Z = P.X, P.Z
    roads = np.zeros(X.shape, bool)
    for pts in P.land.ROADS.values():
        roads |= shapes.polyline(X, Z, pts)[0] <= KEEP_OFF
    from pgmvox.geom.shapes import distance_in
    off_water = distance_in(~P.WET, "euclid") > KEEP_OFF
    off_made = distance_in(~P.MADE, "euclid") > 2
    inland = distance_in(P.LAND, "euclid") > 6
    from pgmvox.surface.terrain import slope_deg
    gentle = slope_deg(P.H, P.LAND) < 40
    out = []
    for name, poly, n, spacing in SITES:
        zone = shapes.inside(X, Z, poly) & P.LAND & ~roads & off_water & off_made & gentle & (Z < -12) & inland
        for x, z in shapes.scatter_points(zone, n, spacing, rng, X, Z, taken=[(a, b) for a, b, _ in out]):
            out.append((x, z, name))
    return out


def kind_for(depth, ember):
    if depth > 0.5:
        return "larch" if ember else "spruce"
    return "oak"


def on_land(ax, az):
    return P.X_MIN <= ax <= P.X_MAX and P.Z_MIN <= az <= P.Z_MAX and bool(P.LAND[ax - P.X_MIN, az - P.Z_MIN])


def fits(w, x, z, tree, turn, through):
    """Whether `plant` would stand the cut here, asked without writing: every block over land, in air, a plant or
    ground that gives way."""
    body = TR.turned(tree, turn)
    rest = min(b[1] for b in body)
    tops = [w.top(x + dx, z + dz) for dx, dy, dz, _, _ in body if dy == rest]
    if min(tops) < 0:
        return False
    base = min(tops) + 1 - rest
    for dx, dy, dz, _, _ in body:
        X_, Y_, Z_ = x + dx, base + dy, z + dz
        if not on_land(X_, Z_) or not w.inside(X_, Y_, Z_):
            return False
        cur = w.id(X_, Y_, Z_)
        if cur not in SOLID and cur not in through:
            return False
    return True


def plant_all(w, rng, depth):
    """Plant every site on both halves. Returns the planted [(x, z, crown, kind, side)] and the crown discs as a
    mask (the ground under them is leaf litter)."""
    by = library()
    spruce_cuts = by["tall-spruce"]
    oak_cuts = by["dense-oak"] + by["tiny-oak"]
    planted = []
    litter = np.zeros(P.H.shape, bool)
    gold = np.zeros(P.H.shape, bool)
    snowy = []
    through = TR.PLANTS | {B.SNOW_LAYER, B.DEADBUSH, B.WOOL}
    every = sites(rng)
    for x, z, name in every:
        i, k = x - P.X_MIN, z - P.Z_MIN
        dp = float(depth[i, k])
        fk, ek = kind_for(dp, False), kind_for(dp, True)
        cuts = spruce_cuts if fk == "spruce" else oak_cuts
        autumn = ("rust", "flame", "copper")[int(rng.integers(3))]
        seed = int(rng.integers(1 << 30))
        choice = None
        for _ in range(12):                              # a cut and a turn that stands on both halves
            cut = cuts[int(rng.integers(len(cuts)))]
            turn = int(rng.integers(4))
            if fits(w, x, z, cut, turn, through) and fits(w, -1 - x, -1 - z, cut, (turn + 2) % 4, through):
                choice = (cut, turn)
                break
        if choice is None:
            continue
        cut, turn = choice
        for ember, kind in ((False, fk), (True, ek)):
            leaf_rng = np.random.default_rng(seed + ember)
            if kind == "spruce":
                t = remap(cut, (B.LOG, 1), "spruce", leaf_rng)
            elif kind == "larch":
                t = remap(cut, (B.LOG, 1), "larch", leaf_rng)
            else:
                t = remap(cut, (B.LOG2, 1) if ember else (B.LOG, 0), autumn, leaf_rng)
            tx, tz = (-1 - x, -1 - z) if ember else (x, z)
            if TR.plant(w, tx, tz, t, (turn + 2) % 4 if ember else turn, through=through, gives_way=SOLID,
                        allowed=on_land):
                r = t.crown
                planted.append((tx, tz, r, kind, "ember" if ember else "frost"))
                disc = np.hypot(P.X - tx, P.Z - tz) <= max(2.0, r * 0.75)
                litter |= disc & P.LAND
                if ember and kind == "larch":
                    gold |= np.hypot(P.X - tx, P.Z - tz) <= r + 1
                if not ember:
                    snowy.append((tx, tz, r))
    return planted, litter, gold, snowy


def snow_on_crowns(w, snowy):
    """A layer of snow on the top leaf of every column of Frost's crowns."""
    n = 0
    for x0, z0, r in snowy:
        for x in range(x0 - r, x0 + r + 1):
            for z in range(z0 - r, z0 + r + 1):
                if not w.inside(x, 0, z):
                    continue
                i, k = x - w.x0, z - w.z0
                col = w.ids[i, :, k]
                ys = np.nonzero(col)[0]
                if not len(ys):
                    continue
                y = int(ys.max())
                if col[y] in (B.LEAVES, B.LEAVES2, B.WOOL) and y + 1 < w.sy:
                    w.set(x, y + 1, z, B.SNOW_LAYER, 0)
                    n += 1
    return n


def biome_tints(w, gold, depth):
    """Ember's gold crowns stand on Savanna, so their leaves take its gold; the rest of the autumn is Mesa's brown."""
    w.biome[gold & (P.Z >= 0)] = SAVANNA
    return int((gold & (P.Z >= 0)).sum())


def cover(w, rng, depth, litter):
    """Ground cover, sparse: bracken (fern, browned by the biome) and dead stalks on Ember's ground and Frost's
    front where no snow lies; mushrooms under Ember's oaks. Never on a road, a terrace or the rift's lip."""
    X, Z = P.X, P.Z
    roads = np.zeros(X.shape, bool)
    for pts in P.land.ROADS.values():
        roads |= shapes.polyline(X, Z, pts)[0] <= 2.5
    from pgmvox.geom.shapes import distance_in
    lip = distance_in(~P.RIFT, "euclid") <= 5
    field = np.abs(np.sin(X * 0.37 + Z * 0.11) + np.cos(Z * 0.29 - X * 0.07))
    n = 0
    for i, k in np.argwhere(P.LAND & ~P.WET & ~P.MADE & ~roads & ~lip):
        x, z = int(X[i, k]), int(Z[i, k])
        h = int(P.H[i, k])
        top = w.id(x, h, z)
        if w.id(x, h + 1, z) != 0:
            continue
        ember = z >= 0
        r = rng.random()
        if top == B.GRASS:
            if r < 0.05 * (field[i, k] > 0.9):
                w.set(x, h + 1, z, B.TALLGRASS, 2)
                n += 1
            elif r < 0.012:
                w.set(x, h + 1, z, B.TALLGRASS, 1)
                n += 1
        elif top == B.DIRT and litter[i, k] and ember:
            if r < 0.025:
                w.set(x, h + 1, z, B.BROWN_MUSHROOM if rng.random() < 0.6 else B.RED_MUSHROOM)
                n += 1
        elif top == B.DIRT and r < 0.015:
            w.set(x, h + 1, z, B.DEADBUSH)
            n += 1
    return n
