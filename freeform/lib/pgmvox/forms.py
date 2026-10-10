"""Forms: scenery built in three dimensions, block by block, where a heightfield cannot say it.

    tower(w, cx, cz, 28, 90, r=5, rock=lambda y, b: beds(y + int(4 * b)), rng=r, tree=pine)
    skirt(w, land, floor, rock=beds, rng=r)        # karst faces under a floating floor's rim
    root_vines(w, land, floor, bottom, rng=r)      # vines hanging from the tips of the roots

**A tower is a stack of rings, and its rings are what make it read as built.** Each course is a disc whose radius
tapers from `taper[0]` to `taper[1]` of r up the tower; every `ledge_every` blocks a course juts out `ledge`
further, a ring of ledges round the stack; and every disc's edge is pushed in or out by three-dimensional noise,
so the faces bulge between the ledges. Rock laid by height shows its beds as courses round it.

A heightfield spire has none of this: one surface, its sides a single slope, no ledge and nothing overhanging.
The karst towers were drawn this way and a spire in their place read as plain terrain, so the recipe is kept here.

**A skirt turns a floating floor's box sides into a cliff,** never touching the walked top: rock bulges out under
the rim in ledges no higher than two under the floor, is cut back under it where the noise is low, carries moss,
and grass grows on its ledges.
"""
import numpy as np
from scipy import ndimage

from . import noise
from .blocks import B
from .shapes import distance_in, edge_depth

SIDES = ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1))       # (dx, dz, the vine bit that hangs it on the block back)


def tower(w, cx, cz, y0, top, r, rock, rng, taper=(1.15, 0.70), ledge_every=9, ledge=0.8, bulge=1.4, cell=4,
          seed=0, through=(B.AIR, B.STAINED_GLASS, B.GLASS), crown=(B.GRASS, 0), crown_r=0.7, tree=None, vines=6):
    """A tower from y0 to top round (cx, cz), radius r at its foot. rock(y, b) gives the block at height y, where b
    is the bulge there (a tilt for the beds). It is written only into blocks in `through`, so it rises through
    mist without cutting islands. The crown is `crown` out to crown_r of r, with tree(w, x, y, z, rng) on it;
    `vines` is the number of vine strings a block of radius, hung down the faces. Returns the blocks laid."""
    R0 = int(r * max(taper) + ledge + bulge + 2)
    span = top - y0 + 1
    field = noise.fbm((2 * R0 + 1, span, 2 * R0 + 1), cell, 2, seed=seed)
    n = 0
    for y in range(y0, top + 1):
        t = (y - y0) / max(1, top - y0)
        rr = r * (taper[0] + (taper[1] - taper[0]) * t) + (ledge if (y % ledge_every) == 0 else 0)
        for dx in range(-R0, R0 + 1):
            for dz in range(-R0, R0 + 1):
                b = field[dx + R0, y - y0, dz + R0]
                if dx * dx + dz * dz <= (rr + bulge * b) ** 2:
                    x, z = cx + dx, cz + dz
                    if w.inside(x, y, z) and w.id(x, y, z) in through:
                        w.set(x, y, z, *rock(y, b))
                        n += 1
    cr = int(r * crown_r)
    for dx in range(-cr, cr + 1):
        for dz in range(-cr, cr + 1):
            if dx * dx + dz * dz <= cr * cr and w.inside(cx + dx, top, cz + dz) and w.id(cx + dx, top, cz + dz) != 0 \
                    and w.id(cx + dx, top + 1, cz + dz) == B.AIR:
                w.set(cx + dx, top, cz + dz, *crown)
    if tree:
        tree(w, cx, top, cz, rng)
    for _ in range(int(r * vines)):                               # strings of vine down the faces
        a = rng.uniform(0, 2 * np.pi)
        ya = int(rng.integers(min(y0 + 12, top - 3), top - 2)) if top - 2 > y0 + 12 else top - 3
        for y in range(ya, ya - int(rng.integers(3, 12)), -1):
            for rad in range(R0 + 1, 0, -1):
                x, z = cx + int(round(rad * np.cos(a))), cz + int(round(rad * np.sin(a)))
                if not w.inside(x, y, z) or w.id(x, y, z) != B.AIR:
                    continue
                hung = False
                for dx, dz, bit in ((1, 0, 8), (-1, 0, 2), (0, 1, 1), (0, -1, 4)):
                    if w.inside(x + dx, y, z + dz) and w.id(x + dx, y, z + dz) not in (B.AIR, B.VINE) + through:
                        w.set(x, y, z, B.VINE, bit)
                        hung = True
                        break
                if hung:
                    break
    return n


def skirt(w, land, floor, rock, rng, bulge=None, reach=(0.05, 0.3), moss=0.12, grass=0.5, undercut=-0.25,
          keep=None, seed=15):
    """Karst faces under the rim of floating floors (land: a world-grid mask; floor: each column's floor y).
    Outside the rim, where the bulge noise is high, rock juts out a block or two as ledges, their tops no higher
    than floor - 2 (so the walked edge and the plan's gaps are untouched), with `moss` of it mossy and grass on
    `grass` of the ledges; on the rim, where the noise is under `undercut`, the face is cut back from floor - 5
    to floor - 3. `keep` is a mask of rim cells never undercut (a wool room's wall, a pillar)."""
    near = distance_in(~land, "euclid")
    Hn = ndimage.maximum_filter(np.where(land, floor, -1), size=5)
    b = noise.fbm(land.shape, 5, 2, seed=seed) if bulge is None else bulge
    X, Z = w.grid()
    n = 0
    for i, k in np.argwhere(~land & (near <= 2.2) & (Hn >= 0)):
        v = b[i, k]
        if near[i, k] > (v > reach[0]) + (v > reach[1]):
            continue
        x, z, h = int(X[i, k]), int(Z[i, k]), int(Hn[i, k])
        top = h - 2 - int(near[i, k]) - (1 if v < 0.2 else 0)
        bot = h - 6 - int(4 * max(0, v)) - int(rng.integers(0, 3))
        for y in range(bot, top + 1):
            w.set(x, y, z, *((B.MOSSY, 0) if rng.random() < moss else rock(y)))
            n += 1
        if rng.random() < grass and w.id(x, top + 1, z) == B.AIR:
            w.set(x, top + 1, z, B.TALLGRASS, 2 if rng.random() < 0.5 else 1)
    rim = land & (edge_depth(land) == 0) & (b < undercut)
    if keep is not None:
        rim &= ~keep
    for i, k in np.argwhere(rim):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(floor[i, k])
        for y in range(h - 5, h - 2):
            w.set(x, y, z, B.AIR)
    return n


def root_vines(w, land, floor, bottom, rng, chance=0.05, under=9, length=(3, 10), keep=None):
    """Vines hanging from the lower part of floating roots: on each side of a land column, with `chance`, a string
    starting a few blocks above the root's tip (bottom: each column's lowest y) and never higher than `under`
    below the floor, hung on the root wherever it has a face. They trail below the islands, where nobody reaches
    them from a floor."""
    X, Z = w.grid()
    cells = land if keep is None else land & ~keep
    n = 0
    for i, k in np.argwhere(cells):
        x, z, h, lo = int(X[i, k]), int(Z[i, k]), int(floor[i, k]), int(bottom[i, k])
        for dx, dz, bit in SIDES:
            if rng.random() > chance:
                continue
            top = min(h - under, lo + int(rng.integers(3, 12)))
            for y in range(top, max(lo, top - int(rng.integers(*length))), -1):
                if w.id(x, y, z) not in (B.AIR, B.VINE) and w.inside(x + dx, y, z + dz) \
                        and w.id(x + dx, y, z + dz) == B.AIR:
                    w.set(x + dx, y, z + dz, B.VINE, bit)
                    n += 1
    return n
