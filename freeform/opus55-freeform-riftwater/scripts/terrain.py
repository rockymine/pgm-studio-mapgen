"""The land: the height field, the river and the pond, the rift face and the island's underside, the rock,
the soil and the paint — everything that is grown rather than built.

Works on the red half (x < 0) only; gen.py mirrors the finished half onto blue.
"""
import numpy as np
from scipy import ndimage

import plan as P
from mc import B
from noise import fbm, smoothstep, spline, polyline_distance

POND_LEVEL = 48
RIVER_LEVEL = 45
WEIR_X = -66


class Land:
    """The half-board's grids, indexed [ix, iz] with ix = x - X_MIN, iz = z - Z_MIN, for x < 0 only."""

    def __init__(self):
        self.x0, self.z0 = P.X_MIN, P.Z_MIN
        self.nx, self.nz = -P.X_MIN, P.Z_MAX - P.Z_MIN + 1
        xs = np.arange(self.x0, 0)
        zs = np.arange(self.z0, P.Z_MAX + 1)
        self.X, self.Z = np.meshgrid(xs, zs, indexing="ij")
        self.shape = self.X.shape

    def ix(self, x):
        return x - self.x0

    def iz(self, z):
        return z - self.z0


def river_course():
    pts = dict((p["key"], p) for p in P.PLACES)["river"]["line"]
    return spline(pts, 0.5)


def river_z_of_x(course):
    xs = np.array([p[0] for p in course])
    zs = np.array([p[1] for p in course])
    order = np.argsort(xs)
    return lambda x: np.interp(x, xs[order], zs[order])


def build_heights(L: Land):
    X, Z = L.X.astype(float), L.Z.astype(float)
    sh = L.shape
    n_small = fbm(sh, 12, 3, seed=11)
    n_big = fbm(sh, 40, 3, seed=12)

    # --- the land's outline ---------------------------------------------------------------------------
    # the rift's lip: ragged everywhere, bitten into bays where nothing stands, held straight under the
    # town's houses and at the two places a thing meets it (the Old Bridge, the falls)
    zz = np.arange(L.z0, P.Z_MAX + 1)
    edge_n = fbm((sh[1],), 10, 2, seed=21)
    bays = 4.5 * (0.5 + 0.5 * fbm((sh[1],), 22, 2, seed=25))
    hold = np.maximum.reduce([np.exp(-((zz + 45) / 16.0) ** 4), np.exp(-((zz - 1) / 6.0) ** 4)])
    rift_edge = -11 + np.round(edge_n * 1.2).clip(-1, 0) - np.round(bays * (1 - hold))
    land = X <= rift_edge[None, :]
    inset_w = (2 + 4 * fbm((sh[1],), 16, 2, seed=22)).clip(0, 6)
    inset_n = (2 + 5 * fbm((sh[0],), 16, 2, seed=23)).clip(0, 7)
    inset_s = (2 + 5 * fbm((sh[0],), 16, 2, seed=24)).clip(0, 7)
    land &= X >= P.X_MIN + inset_w[None, :]
    land &= Z >= P.Z_MIN + inset_n[:, None]
    land &= Z <= P.Z_MAX - inset_s[:, None]

    # --- the open ground ------------------------------------------------------------------------------
    course = river_course()
    zr = river_z_of_x(course)(X)                      # river centreline z at each x
    north = Z < zr
    # town bluff: 51 by the rift, 52 toward the square
    h_n = 51 + 1.0 * smoothstep(-30, -70, X) + 2.0 * smoothstep(-74, -96, X)
    # fields and village: 47 by the river, rising to the south and toward the ridge
    h_s = 47.2 + 1.8 * smoothstep(25, 80, Z) + 4.5 * smoothstep(-64, -98, X)
    h = np.where(north, h_n, h_s)
    # blend the seam over the pond end, where there is no river to separate the two
    west = smoothstep(-70, -80, X)
    h_w = 52.5 + 2.5 * smoothstep(-80, -98, X) - 1.5 * smoothstep(-10, 30, Z) + 1.0 * smoothstep(30, 60, Z)
    h = h * (1 - west) + h_w * west
    h += 0.8 * n_small + 1.2 * n_big

    # --- the river valley -------------------------------------------------------------------------
    d_r, along = polyline_distance(X, Z, course)
    in_reach = X > -75
    w = 3.0 + 0.6 * smoothstep(-60, -15, X)
    level = np.where(X < WEIR_X, POND_LEVEL, RIVER_LEVEL)
    # north side: a bluff, 6 blocks up over about 7; south side: a gentle bank over about 14
    rise_n = smoothstep(w, w + 7, d_r)
    rise_s = smoothstep(w, w + 14, d_r)
    bank = np.where(north, level + 1 + (h - level - 1) * rise_n, level + 1.3 + (h - level - 1.3) * rise_s)
    h = np.where(in_reach, np.minimum(h, bank), h)
    channel = in_reach & (d_r <= w)
    bed = level - 1 - 2.2 * (1 - (d_r / w) ** 2)

    # --- the mill pond -----------------------------------------------------------------------------
    px_, pz_ = -84, 20
    pn = fbm(sh, 8, 2, seed=31)
    pr = np.hypot((X - px_) / 12.5, (Z - pz_) / 9.5) + 0.12 * pn
    # the tongue of land: a spit from the south-west shore
    spit, _ = polyline_distance(X, Z, [(-92, 30), (-86, 24), (-83, 21)])
    pond = (pr < 1.0) & ~(spit < 1.6)
    shore = smoothstep(1.0, 1.5, pr)
    h = np.where(pr < 1.5, np.minimum(h, POND_LEVEL + 1 + (h - POND_LEVEL - 1) * shore), h)
    h = np.where(spit < 1.6, np.maximum(h, POND_LEVEL + 1), h)
    pond_bed = POND_LEVEL - 1 - 3.5 * (1 - pr.clip(0, 1) ** 2)

    # --- the ridge, its spurs, crags and steps ----------------------------------------------------------
    # the main ridge's foot wanders; two spurs reach east along the board's north and south edges
    foot = -100 + 4 * fbm((sh[1],), 24, 2, seed=40)[None, :]
    spur_n, _ = polyline_distance(X, Z, [(-114, -68), (-98, -74), (-82, -80)])
    spur_s, _ = polyline_distance(X, Z, [(-114, 70), (-100, 76), (-88, 82)])
    crest = 73 + 5 * fbm((sh[1],), 30, 2, seed=41)[None, :] + 4 * np.exp(-((Z + 72) / 18) ** 2)
    t = smoothstep(foot, foot - 15, X)
    ridge_n = fbm(sh, 10, 3, seed=42)
    crag = 1 - np.abs(fbm(sh, 7, 2, seed=43))           # ridged: sharp lines where the noise crosses zero
    ridge = h + (crest - h).clip(0) * t + t * (2.5 * ridge_n + 4 * smoothstep(0.75, 0.95, crag))
    # spurs: lower arms of the ridge, each with its own crest falling eastward
    for d, (cz, top) in ((spur_n, (-74, 66)), (spur_s, (78, 63))):
        arm = top - 0.25 * np.abs(X + 100) + 2 * ridge_n
        k = smoothstep(14, 3, d)
        ridge = np.maximum(ridge, h + (arm - h).clip(0) * k)
    # ground climbs in steps: pull the ridge half way toward 3-block terraces
    stepped = np.floor(ridge / 3) * 3 + 3 * smoothstep(0.3, 0.7, (ridge / 3) % 1)
    ridge = ridge + 0.55 * (stepped - ridge) * smoothstep(0.15, 0.5, t + 0.0 * ridge)
    h = np.where(ridge > h, ridge, h)
    # the far side of the ridge falls away toward the board edge
    h -= 7 * smoothstep(-114, -120, X)

    # --- the spawn shoulder: a lower spur at the ridge's foot, its top levelled for the watch house -----
    sn = fbm(sh, 6, 2, seed=44)
    sd = np.hypot((X + 97) / 12.0, (Z + 7) / 9.5) + 0.12 * sn
    terrace_y = 59
    k = smoothstep(1.0, 1.55, sd)
    shoulder = terrace_y * (1 - k) + np.minimum(h, terrace_y) * k
    h = np.where(sd < 1.55, np.maximum(np.where(sd < 1.0, terrace_y, h), shoulder), h)
    h = np.where(sd < 1.0, terrace_y, h)

    # --- the square and the green: level where the monuments stand -----------------------------------
    for (mx, mz), lvl, r in (((-66, -44), 52, 11), ((-66, 48), 50, 9)):
        d = np.hypot(X - mx, Z - mz)
        k = smoothstep(r, r + 8, d)
        h = np.where(d < r + 8, lvl * (1 - k) + h * k, h)

    # --- Lone Oak Knoll ---------------------------------------------------------------------------
    d = np.hypot((X + 22) / 1.0, (Z - 74) / 1.25)
    h += 6.5 * np.exp(-(d / 8.0) ** 2)

    H = np.round(h).astype(int)
    water = np.zeros(sh, dtype=int)                     # water surface y, 0 where dry
    bed_i = H.copy()
    water[channel] = level[channel]
    bed_i[channel] = np.floor(bed[channel]).astype(int)
    water[pond] = POND_LEVEL
    bed_i[pond] = np.floor(pond_bed[pond]).astype(int)
    # the outlet: the river must leave the pond without a dam between them
    outlet = (np.hypot(X + 74, Z - 22) < 4) & (d_r < w + 0.5)
    water[outlet] = POND_LEVEL
    bed_i[outlet] = np.minimum(bed_i[outlet], POND_LEVEL - 2)
    # the wet columns' ground is their bed
    H = np.where(water > 0, np.minimum(bed_i, water - 1), H)
    H = np.where(land, H, -1)
    water = np.where(land, water, 0)

    L.H, L.water, L.land, L.north = H, water, land, north
    L.d_river, L.zr = d_r, zr
    L.course = course
    return L


def build_underside(L: Land):
    """The island's bottom: sheer under the rift for about 30 blocks, tapering everywhere else."""
    land = L.land
    void = ~land
    # distance to the rift edge vs to the board's outer edge
    rift_side = np.zeros_like(land)
    rift_side[-1:, :] = True                             # the x = -1 column is rift
    outer = void & ~(L.X > -14)
    d_outer = ndimage.distance_transform_edt(~outer)
    d_rift = ndimage.distance_transform_edt(~(void & (L.X > -14)))
    n = fbm(L.shape, 9, 3, seed=51)
    thick_outer = 4 + 0.9 * d_outer + 4 * n
    thick_rift = 26 + 1.2 * d_rift + 4 * n
    thick = np.minimum(thick_outer, thick_rift)
    bottom = np.maximum(L.H - thick, 4 + 3 * fbm(L.shape, 16, 2, seed=52)).round().astype(int)
    L.bottom = np.where(land, bottom, 0)
    return L


def slope_deg(H, land):
    Hf = np.where(land, H, np.nan).astype(float)
    # worst step to a 4-neighbour, read over a 2-block window as the painter would
    gx = np.abs(np.roll(Hf, -1, 0) - np.roll(Hf, 1, 0)) / 2
    gz = np.abs(np.roll(Hf, -1, 1) - np.roll(Hf, 1, 1)) / 2
    g = np.nan_to_num(np.hypot(gx, gz), nan=0)
    return np.degrees(np.arctan(g))


def write_land(w, L: Land, seed=7):
    """Write rock, soil and paint for every land column into the world."""
    rng = np.random.default_rng(seed)
    H, bottom, water, land = L.H, L.bottom, L.water, L.land
    ang = slope_deg(H, land)
    L.angle = ang
    sh = L.shape
    patch = fbm(sh, 5, 2, seed=61)       # five-block patches
    patch2 = fbm(sh, 4, 2, seed=62)
    cellr = rng.random(sh)
    # 3-D rock: stone with andesite bodies, cobble flecks; strata that follow the ground
    ys = np.arange(w.sy)
    rock3 = None
    for ix in range(L.nx):
        x = L.x0 + ix
        wx = x - w.x0
        for iz in range(L.nz):
            if not land[ix, iz]:
                continue
            z = L.z0 + iz
            wz = z - w.z0
            top, bot = H[ix, iz], bottom[ix, iz]
            if top < 0:
                continue
            col_id = w.ids[wx, :, wz]
            col_d = w.dat[wx, :, wz]
            col_id[bot:top + 1] = B.STONE
            col_d[bot:top + 1] = 0
            # strata: andesite beds following the ground, broken by patch noise
            depth = top - ys[bot:top + 1]
            bed = ((depth + int(3 * patch2[ix, iz])) % 9) < 3
            col_d[bot:top + 1][bed & (patch[ix, iz] > -0.2)] = 5
            a = ang[ix, iz]
            wet = water[ix, iz] > 0
            if wet:
                # river and pond bed: gravel and sand, clay in the still pond
                r = cellr[ix, iz]
                if L.X[ix, iz] < -74 or water[ix, iz] == 48:
                    col_id[top], col_d[top] = (B.CLAY, 0) if r < 0.3 else ((B.SAND, 0) if r < 0.6 else (B.DIRT, 0))
                else:
                    col_id[top], col_d[top] = (B.GRAVEL, 0) if r < 0.55 else ((B.SAND, 0) if r < 0.8 else (B.STONE, 5))
                col_id[top + 1:water[ix, iz] + 1] = B.WATER
                col_d[top + 1:water[ix, iz] + 1] = 0
                continue
            if a < 38:
                soil = 3 if a < 25 else 2
                col_id[top - soil:top] = B.DIRT
                col_d[top - soil:top] = np.where(rng.random(soil) < 0.35, 1, 0)
                col_id[top], col_d[top] = B.GRASS, 0
                # worn edge: where the ground turns steep, coarse dirt shows in patches
                if a > 33 and patch[ix, iz] > 0.35:
                    col_id[top], col_d[top] = B.DIRT, 1
            elif a < 55:
                col_id[top - 1:top] = B.DIRT
                pv = patch[ix, iz]
                if pv > 0.15:
                    col_id[top], col_d[top] = B.GRASS, 0
                elif pv > -0.25:
                    col_id[top], col_d[top] = B.STONE, 5 if cellr[ix, iz] < 0.5 else 0
                else:
                    col_id[top], col_d[top] = B.DIRT, 1
            else:
                r = cellr[ix, iz]
                col_id[top], col_d[top] = (B.STONE, 0) if r < 0.45 else ((B.STONE, 5) if r < 0.8 else (B.COBBLE, 0))
            # a sandy lip where grass meets the river
            if not wet and L.d_river[ix, iz] < 5.2 and L.X[ix, iz] > -75 and top <= RIVER_LEVEL + 2 and a < 38:
                col_id[top], col_d[top] = (B.SAND, 0) if patch2[ix, iz] > -0.1 else (B.GRAVEL, 0)
    return L


def in_polygon(X, Z, poly):
    """Even-odd point-in-polygon over grids."""
    inside = np.zeros(X.shape, bool)
    n = len(poly)
    for i in range(n):
        (x1, z1), (x2, z2) = poly[i], poly[(i + 1) % n]
        cond = (z1 > Z) != (z2 > Z)
        xint = (x2 - x1) * (Z - z1) / ((z2 - z1) if z2 != z1 else 1e-9) + x1
        inside ^= cond & (X < xint)
    return inside


def write_falls(w, L: Land):
    """The river spills over the lip: falling water down the rift face, into the void."""
    for iz in range(L.nz):
        wet = np.nonzero(L.water[:, iz] > 0)[0]
        if len(wet) == 0:
            continue
        ix = wet.max()
        x = L.x0 + ix
        if x < -14:
            continue
        z = L.z0 + iz
        lvl = L.water[ix, iz]
        for xx in range(x + 1, -9):
            for y in range(8, lvl + 1):
                if w.id(xx, y, z) == 0:
                    w.set(xx, y, z, B.WATER_FLOW, 8)
    L.falls_x = -10


def paint_biomes(w, L: Land):
    woods = {p["key"]: p for p in P.PLACES}
    forest = in_polygon(L.X, L.Z, woods["north_wood"]["poly"]) | (L.X < -100)
    b = np.where(forest, 4, 1)
    b = np.where(L.water > 0, 7, b)
    # blend: the client blends grass colour, so a ragged edge is enough
    w.biome[:L.nx, :] = b
    L.forest = forest
