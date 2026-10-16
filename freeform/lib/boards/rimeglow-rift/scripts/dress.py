"""The finishing of the ground: lamps along the roads, rock fallen below the cliffs, drifts in the lee, spires on the
crags and the ground cover of each half. Every piece is placed for a reason stated beside it."""
import math

import numpy as np
from scipy import ndimage

import land as LD
from pgmvox import B
from pgmvox.built import props as PR
from pgmvox.geom import noise
from pgmvox.geom.shapes import distance_in
import flora as FL


def lamps(w, ctx):
    """A lamp every fourteen blocks along each road, alternating sides: the roads are how a player finds the way at
    night, and each half lights its own with its own light."""
    H, X, Z = ctx["H"], ctx["X"], ctx["Z"]
    n = 0
    for name, pts in ctx["paths"].items():
        if name.startswith("ramp"):
            continue
        for south in (False, True):
            path = [(-1 - x, -1 - z) for x, z in pts] if south else pts
            post, light = ((B.NETHER_FENCE, 0), (B.GLOWSTONE, 0)) if south else ((B.SPRUCE_FENCE, 0), (B.SEA_LANTERN, 0))
            n += len(PR.lamps(w, path, H, X, Z, every=14, post=post, light=light, height=2, side=3.2, start=7))
    return n


def rockfall(w, ctx, rng):
    """Boulders where a cliff has shed them: at the foot of a steep face, on gentle ground, one family of rock a half."""
    H, deg, land, X, Z = ctx["H"], ctx["deg"], ctx["land"], ctx["X"], ctx["Z"]
    relief = ndimage.maximum_filter(H, size=9) - ndimage.minimum_filter(H, size=9)
    foot = land & (deg < 22) & (relief > 7) & ~ctx["laid"] & (Z < -14) & ~ctx["rift"] & (ctx["ed"] > 3)
    foot &= ~LD.mere_mask(X, Z)
    foot &= ~((X > -8) & (X < 34) & (Z < -58))
    foot &= ~(np.hypot(X - 46, Z + 48) < 14)
    spots = FL.sites(ctx, rng, foot, 20, 9, [])
    n = 0
    for x, z in spots:
        g = int(H[x - w.x0, z - w.z0])
        r = int(rng.integers(1, 3))
        FL.boulder(w, x, z, g + 1, r, rng, ((B.STONE, 5), (B.STONE, 0), (B.STONE, 5), (B.COBBLE, 0)))
        if rng.random() < 0.5:
            w.set(x, g + 1 + 2 * r, z, B.SNOW_LAYER, 1) if w.id(x, g + 1 + 2 * r, z) == 0 else None
        # the south image: the same fall in the south's rock, hardened clay and granite
        nx, nz = -1 - x, -1 - z
        FL.boulder(w, nx, nz, g + 1, r, rng, ((B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 12), (B.HARDENED_CLAY, 0), (B.STONE, 1)))
        n += 1
    return n


def drifts(w, ctx):
    """Snow settled in the lee: layers a block thick on the snow's gentle ground, thickest where the wind dropped it,
    never on a road or beside a lamp."""
    H, deg, land, X, Z, S = ctx["H"], ctx["deg"], ctx["land"], ctx["X"], ctx["Z"], ctx["S"]
    lee = noise.fbm(X.shape, 11, 3, seed=91)
    ok = land & (S >= 0.55) & (deg < 25) & ~ctx["laid"] & ~ctx["rift"] & (ctx["ed"] > 1)
    n = 0
    for i, k in np.argwhere(ok & (lee > 0.18)):
        x, z = int(X[i, k]), int(Z[i, k])
        h = int(H[i, k])
        if w.ids[i, h, k] == B.SNOW and w.ids[i, h + 1, k] == 0:
            w.ids[i, h + 1, k] = B.SNOW_LAYER
            w.dat[i, h + 1, k] = 1 if lee[i, k] < 0.4 else 2
            n += 1
    return n


def spire(w, x, z, y0, h, r, rng, blocks, lean=(0, 0)):
    """A spire: stacked rings narrowing to a point, leaning a little."""
    for k in range(h):
        rr = r * (1 - k / (h + 1)) ** 0.8
        cx, cz = x + int(round(lean[0] * k / h)), z + int(round(lean[1] * k / h))
        R = int(math.ceil(rr))
        for dx in range(-R, R + 1):
            for dz in range(-R, R + 1):
                if math.hypot(dx, dz) <= rr + 0.2:
                    w.set(cx + dx, y0 + k, cz + dz, *blocks[int(rng.integers(len(blocks)))])


def spires(w, ctx, rng):
    """Crystal spires of ice on the north highland's crags and charred spires of clay on the south's: the two edges of
    the board read from the rift as one skyline of two materials."""
    H, land, X, Z = ctx["H"], ctx["land"], ctx["X"], ctx["Z"]
    crag = land & (Z < -78) & (ctx["ed"] > 2) & ~((X > -8) & (X < 34)) & (H > 62)
    sp = FL.sites(ctx, rng, crag, 9, 8, [])
    for x, z in sp:
        g = int(H[x - w.x0, z - w.z0])
        h = int(rng.integers(6, 13))
        lean = (int(rng.integers(-2, 3)), int(rng.integers(-2, 3)))
        spire(w, x, z, g + 1, h, 1.8, rng, ((B.PACKED_ICE, 0), (B.PACKED_ICE, 0), (B.ICE, 0)), lean)
        spire(w, -1 - x, -1 - z, g + 1, h, 1.8, rng,
              ((B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 12), (B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 1)),
              (-lean[0], -lean[1]))
    return len(sp)


def cover(w, ctx, rng):
    """Ground cover, kept thin so a player reads the ground: dead bushes and tall grass on the autumn half's gentle
    ground, away from roads, and a few ferns where the snow thins."""
    H, deg, land, X, Z, S = ctx["H"], ctx["deg"], ctx["land"], ctx["X"], ctx["Z"], ctx["S"]
    near_road = ndimage.binary_dilation(ctx["laid"], iterations=2)
    ok = land & (deg < 20) & ~near_road & ~ctx["rift"] & (ctx["ed"] > 1) & (S < 0.5)
    field = noise.fbm(X.shape, 7, 2, seed=92)
    n = 0
    for i, k in np.argwhere(ok & (field > 0.25)):
        h = int(H[i, k])
        if w.ids[i, h, k] == B.GRASS and w.ids[i, h + 1, k] == 0 and rng.random() < 0.32:
            w.ids[i, h + 1, k] = B.TALLGRASS if rng.random() < 0.75 else B.DEADBUSH
            w.dat[i, h + 1, k] = 1 if w.ids[i, h + 1, k] == B.TALLGRASS else 0
            n += 1
    return n


def steps(w, ctx):
    """A stair on every one-block rise along each road, the full width of the way: cobble in the north, dark oak in the
    south, so a climb on a road is a flight and not a jump."""
    from pgmvox.routes import route as R
    H, X, Z = ctx["H"], ctx["X"], ctx["Z"]
    n = 0
    for name, pts in ctx["paths"].items():
        for south in (False, True):
            path = [(-1 - x, -1 - z) for x, z in pts] if south else pts
            block = B.DARK_OAK_STAIRS if south else B.COBBLE_STAIRS
            width = 3 if name.startswith("ramp") else 4
            n += R.steps(w, H, X, Z, path, block=block, width=width)
    return n
