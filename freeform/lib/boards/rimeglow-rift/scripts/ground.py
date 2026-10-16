"""Rimeglow Rift's ground laid in blocks: rock in beds that follow the season, the top painted by slope and by
winter, the lava in the rift, the underside, the roads."""
import numpy as np

import land as LD
from pgmvox import B
from pgmvox.geom import noise
from pgmvox.geom.shapes import distance_in, edge_depth
from pgmvox.surface import terrain as T

SNOWB, PACKED, ICEB = (B.SNOW, 0), (B.PACKED_ICE, 0), (B.ICE, 0)
AND = (B.STONE, 5)
STONE = (B.STONE, 0)
GRAN = (B.STONE, 1)
PGRAN = (B.STONE, 2)

# ---- the beds -------------------------------------------------------------------------------------------------
# winter rock: grey beds with bands of packed ice and drifted snow, as a glacier's cut face shows them
WINTER_BEDS = [STONE, AND, PACKED, STONE, STONE, SNOWB, AND, PACKED, PACKED, STONE, AND, (B.COBBLE, 0)]
# autumn rock: the mesa's own banding, hardened clay and the stained clays of one family
AUTUMN_BEDS = [(B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 1), (B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 12),
               (B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 4), (B.HARDENED_CLAY, 0),
               (B.STAINED_CLAY, 12), (B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 14), (B.HARDENED_CLAY, 0)]


def bed_layers(seed, n=160):
    """Two bed lists as arrays of thickness-expanded indices: bed k at height y."""
    rng = np.random.default_rng(seed)
    idx, last = [], -1
    while len(idx) < n:
        k = int(rng.integers(0, 12))
        if k == last:
            continue
        last = k
        idx += [k] * int(rng.integers(1, 4))
    return np.array(idx[:n])


def season(X, Z, H, land):
    """Winter, 0 to 1: the north is winter, the south autumn, and each bank thaws or frosts toward the rift. High
    ground wears snow whatever the half, and the line between the two is bitten by noise so it is never ruled."""
    V = Z + 0.5
    d = np.abs(V)
    north = 0.5 + 0.5 * LD.sstep(16, 48, d)
    south = 0.42 * (1 - LD.sstep(14, 46, d))
    base = np.where(V < 0, north, south)
    cap = 0.5 * LD.sstep(72, 86, H) * (V > 0)
    n = noise.fbm(X.shape, 13, 3, seed=31) * 0.42 + noise.fbm(X.shape, 5, 2, seed=32) * 0.12
    return np.clip(base + cap + n, 0, 1)


def build(w, ctx_seed=1):
    X, Z, H0, cd = LD.ground()
    H1, laid_n, paths = LD.graded(H0, X, Z)
    half = LD.SZ // 2
    H = np.round(H1).astype(int)
    H[:, half:] = LD.turned(H)[:, half:]
    laid = laid_n.copy()
    laid[:, half:] = LD.turned(laid_n)[:, half:]
    shelf = (cd >= 0) & (cd < LD.SHELF_W) & (np.abs(X + 0.5) < LD.SHELF_X)
    laid |= shelf
    flow = LD.flow_mask(X, Z) & ~laid
    land = LD.land_mask(X, Z)
    rift = (cd < 0) & land
    ed = edge_depth(land, "euclid")

    # the dams: the rift's floor lifts to a lip where the land ends, so the lava cannot run off the board
    dam = rift & (ed < 3)
    H = np.where(dam, LD.LAVA + 2, H)
    H = np.where(land, H, 0)

    deg = T.slope_deg(H, land)
    deg = T.ledge_angle(H, deg, land)
    S = season(X, Z, H, land)
    winter = S >= 0.5
    # patches of ground, each a low-frequency field: one tone with the other sets inset in it
    g1 = noise.fbm(X.shape, 6, 2, seed=41) * 1.4
    g2 = noise.fbm(X.shape, 10, 3, seed=42) * 1.3
    hashf = ((X * 73856093) ^ (Z * 19349663)) & 1023

    bedA = bed_layers(7)
    bedW = bed_layers(8)
    depth_cone = T.root_depth(land, cone=3.0, power=0.78, rough=0.45, flutes=5.0, flute_cell=6, spires=16.0,
                              spire_cell=12, cap=60, seed=9)
    bottom = np.maximum(13, H - np.maximum(depth_cone, 3) - 3)

    jn = noise.fbm(X.shape, 9, 2, seed=51) * 0.6
    cells = np.argwhere(land)
    for i, k in cells:
        h = int(H[i, k])
        if h <= 0:
            continue
        lo = int(bottom[i, k])
        x, z = int(X[i, k]), int(Z[i, k])
        s = S[i, k]
        wint = bool(winter[i, k])
        dg = int(deg[i, k])
        # rock, by bed: the season at each course decides which set of beds shows, so the thaw line runs through the
        # rock as a ragged edge rather than one ruled one
        ys = np.arange(lo, h)
        rock_s = float(np.clip(0.5 + (0.62 if z < 0 else -0.62) + jn[i, k] * 0.9, 0, 1))
        tilt = int(0.06 * x - 0.04 * z)

        def bed(y):
            band = y + tilt
            bj = (((band // 3) * 2654435761) >> 9) % 100 / 100.0 - 0.5     # one draw per bed, so a bed is one set
            if rock_s + bj * 0.5 >= 0.5:
                return WINTER_BEDS[bedW[band % 160]]
            return AUTUMN_BEDS[bedA[band % 160]]
        for y in ys:
            w.ids[i, y, k], w.dat[i, y, k] = bed(y)
        if rift[i, k]:
            continue
        top = surface(i, k, x, z, h, dg, s, wint, g1[i, k], g2[i, k], hashf[i, k], laid[i, k], bed)
        if flow[i, k] and dg < 50:
            top = flow_block(x, z, g1[i, k], g2[i, k], hashf[i, k])
        # soil courses under the top where the ground is gentle
        sd = int(T.soil_depth(np.array([dg]))[0])
        for j in range(1, sd + 1):
            if h - j >= lo:
                w.ids[i, h - j, k], w.dat[i, h - j, k] = soil(wint, j, hashf[i, k])
        w.ids[i, h, k], w.dat[i, h, k] = top
    return dict(X=X, Z=Z, H=H, deg=deg, S=S, land=land, rift=rift, cd=cd, laid=laid, paths=paths, ed=ed,
                bottom=bottom, g1=g1, g2=g2)


def noise_at(y, i, k):
    return 0.0


def soil(wint, j, hv):
    if wint:
        return (B.DIRT, 1) if j == 1 else STONE
    return ((B.DIRT, 1) if (j + hv) % 2 else (B.DIRT, 0))


def surface(i, k, x, z, h, dg, s, wint, g1, g2, hv, on_road, bed):
    if on_road:
        return road_block(x, z, wint)
    if wint:
        if dg > 46:
            return bed(h)
        if dg > 32:
            return (AND, STONE, SNOWB, SNOWB, PACKED)[hv % 5]
        if g2 < -0.5:
            return PACKED
        return SNOWB
    if dg > 42:
        return bed(h)
    if dg > 33:
        return ((B.SAND, 1), (B.HARDENED_CLAY, 0), (B.SAND, 1), (B.STAINED_CLAY, 1), (B.DIRT, 1))[hv % 5]
    if g2 > 0.5:
        return (B.DIRT, 2)
    if g1 < -0.6:
        return (B.DIRT, 1)
    return (B.GRASS, 0)


def road_block(x, z, wint):
    """A road is a made thing and is paved by hue: cold hard stone in the north, granite and brick in the south."""
    cell = ((x // 3) * 7 + (z // 3) * 13 + ((x * 3 + z * 5) % 7 == 0)) % 3
    if wint:
        return ((B.GRAVEL, 0), AND, (B.COBBLE, 0))[cell]
    return ((B.DIRT, 1), (B.DIRT, 2), (B.PLANKS, 5))[cell]


def flow_block(x, z, g1, g2, hv):
    """The glacier's tongue: packed ice in sheets, clear ice in the seams. The cooled lava's: grey and black clay, orange
    clay in the cracks and an ember in some of them."""
    if z < 0:
        return (B.ICE, 0) if g1 > 0.45 else (SNOWB if g2 > 0.5 else PACKED)
    if g1 > 0.45:
        return (B.STAINED_CLAY, 1) if hv % 6 else (B.GLOWSTONE, 0)
    return (B.STAINED_CLAY, 15) if g2 > 0.1 else (B.STAINED_CLAY, 7)
