"""The land: the canyon's cross-section with its two cliffs and the bench between them, the Wash climbing to
the mesa top, the buttes and the Needles, the spring and its creek, the clay strata, the island's underside,
the Sky Arch, and the ground's paint.

Works on the red half (x < 0) only; gen.py turns the finished half onto blue.
"""
import numpy as np
from scipy import ndimage

import plan as P
from mc import B
from noise import fbm, smoothstep, polyline_distance

RNG = np.random.default_rng(2024)


class Land:
    """The half-board's grids, indexed [ix, iz] with ix = x - X_MIN, iz = z - Z_MIN, for x < 0 only."""

    def __init__(self):
        self.x0, self.z0 = P.X_MIN, P.Z_MIN
        self.nx, self.nz = -P.X_MIN, P.Z_MAX - P.Z_MIN + 1
        xs = np.arange(self.x0, 0)
        zs = np.arange(self.z0, P.Z_MAX + 1)
        self.X, self.Z = np.meshgrid(xs, zs, indexing="ij")
        self.shape = self.X.shape


def wash_line(x):
    return 51 + 4.0 * np.sin(x / 10.0)


def wash_floor(x):
    """The Wash climbs from the canyon floor at its mouth to the mesa top at its head, in a smooth grade."""
    t = np.clip((-x - 24) / (100 - 24), 0, 1)
    return P.FLOOR_Y + (P.PLATEAU_Y - P.FLOOR_Y) * t


def butte(h, X, Z, cx, cz, rx, rz, top, seed, tier=6):
    """A flat-topped butte: sheer sides, a ragged outline, a lower tier round its foot."""
    n = fbm(X.shape, 6, 2, seed=seed)
    d = np.hypot((X - cx) / rx, (Z - cz) / rz) + 0.12 * n
    h = np.where(d < 1.0, np.maximum(h, top), h)
    h = np.where((d >= 1.0) & (d < 1.25), np.maximum(h, top - tier), h)
    return h


def spires(h, X, Z, sites, base_seed):
    """Spires and hoodoos: each a column of clay rising out of the plateau, pointed or capped."""
    for k, (sx, sz, r, height, kind) in enumerate(sites):
        d = np.hypot(X - sx, Z - sz)
        if kind == "needle":
            prof = np.clip(1 - (d / r) ** 1.3, 0, 1)
        else:
            prof = np.clip(1 - (d / r) ** 5, 0, 1)
        base = h[int(sx - P.X_MIN), int(sz - P.Z_MIN)]
        h = np.where(prof > 0.02, np.maximum(h, base + height * prof), h)
    return h


def needle_sites():
    rng = np.random.default_rng(31)
    poly = dict((p["key"], p) for p in P.PLACES)["needles"]["poly"]
    xs = [q[0] for q in poly]; zs = [q[1] for q in poly]
    sites = []
    for _ in range(400):
        x = rng.uniform(min(xs) + 2, max(xs) - 2); z = rng.uniform(min(zs) + 3, max(zs) - 2)
        r = rng.uniform(1.6, 3.4)
        if any(np.hypot(x - a, z - b) < r + c + 2.5 for a, b, c, _, _ in sites):
            continue
        # keep the Needles Path and the Mule Trail's head walkable
        path = [(-56, -64), (-52, -76), (-50, -78)]
        if min(np.hypot(x - a, z - b) for a, b in path) < r + 3:
            continue
        sites.append((x, z, r, rng.uniform(8, 22), "needle" if rng.random() < 0.7 else "hoodoo"))
        if len(sites) >= 26:
            break
    # a few hoodoos standing alone elsewhere, where the rim looks out
    sites += [(-50, 22, 2.5, 11, "hoodoo"), (-56, 40, 2.0, 9, "needle"), (-48, 66, 2.8, 14, "hoodoo"),
              (-118, -60, 3.0, 12, "hoodoo"), (-74, 30, 1.8, 8, "needle"), (-112, 46, 2.4, 10, "hoodoo"),
              (-90, 98 - 6, 2.2, 9, "needle")]
    return sites


def build_heights(L: Land):
    X, Z = L.X.astype(float), L.Z.astype(float)
    sh = L.shape
    zs = np.arange(L.z0, P.Z_MAX + 1).astype(float)
    cx = np.array([P.canyon_x(z) for z in zs])[None, :]
    d = cx - X                                         # distance west of the canyon's centreline
    n1 = fbm((sh[1],), 9, 3, seed=1)[None, :]
    n2 = fbm((sh[1],), 11, 3, seed=2)[None, :]
    n3 = fbm((sh[1],), 14, 2, seed=3)[None, :]
    floor_edge = P.FLOOR_HALF + 2.6 * n1
    bench0 = floor_edge + P.LOWER_CLIFF
    bench1 = bench0 + P.BENCH_WIDTH + 2.0 * n2
    rim = bench1 + P.UPPER_CLIFF + 1.5 * n3
    small = fbm(sh, 8, 2, seed=4)
    roll = fbm(sh, 40, 2, seed=5)

    floor = P.FLOOR_Y + 0.5 * small
    # talus: the floor climbs a little against the foot of the wall
    talus = 3.0 * smoothstep(floor_edge - 5, floor_edge, d) * (0.6 + 0.4 * fbm(sh, 5, 2, seed=6))
    h = floor + talus
    jag = 1.2 * fbm(sh, 3, 2, seed=7)                   # cliffs are ragged, not ruled
    lower = P.FLOOR_Y + (P.BENCH_Y - P.FLOOR_Y) * smoothstep(floor_edge + jag, bench0 + jag, d)
    h = np.where(d >= floor_edge + jag, np.maximum(h, lower), h)
    bench = P.BENCH_Y + 0.4 * small
    h = np.where(d >= bench0 + jag, bench, h)
    upper = P.BENCH_Y + (P.PLATEAU_Y - P.BENCH_Y) * smoothstep(bench1 + jag, rim + jag, d)
    h = np.where(d >= bench1 + jag, upper, h)
    plateau = P.PLATEAU_Y + 1.6 * roll + 2.5 * smoothstep(-80, -118, X) + 0.4 * small
    h = np.where(d >= rim + jag, plateau, h)
    L.d, L.floor_edge, L.bench0, L.bench1, L.rim = d, floor_edge, bench0, bench1, rim

    # --- the scarp: the back of the mesa stands a tier higher, with gullies where the roads go down -------
    sc = -96 + 4 * fbm((sh[1],), 18, 2, seed=9)[None, :]
    step = 6 * smoothstep(sc + 1.5, sc - 1.5, X)
    gully = np.zeros(sh)
    for gz, gw in ((0, 4), (34, 4), (-40, 4)):
        gully = np.maximum(gully, smoothstep(gw + 3, gw, np.abs(Z - gz)))
    step = step * (1 - gully) + gully * 6 * smoothstep(sc + 12, sc - 12, X)
    h = np.where(d >= rim + jag, h + step, h)

    # --- the Wash: a side canyon from the floor to the mesa top --------------------------------------
    zw = wash_line(X)
    hw = 7.5 - 3.0 * smoothstep(-26, -100, X)
    dz = np.abs(Z - zw) + 0.8 * fbm(sh, 5, 2, seed=8)
    wf = wash_floor(X) + 0.4 * small
    inwash = (X < -18) & (X > -104)
    wall = smoothstep(hw, hw + 2.5, dz)
    h = np.where(inwash & (dz < hw + 2.5), np.minimum(h, wf * (1 - wall) + h * wall), h)
    L.wash_mask = inwash & (dz < hw)

    # --- buttes, the Needles, hoodoos ---------------------------------------------------------------
    h = butte(h, X, Z, -125, 0, 9, 24, P.PLATEAU_Y + 20, seed=40)
    h = butte(h, X, Z, -80, 86, 7, 6, P.PLATEAU_Y + 12, seed=41, tier=5)
    L.spires = needle_sites()
    h = spires(h, X, Z, L.spires, 50)

    # --- level ground where things are built ----------------------------------------------------
    for (fx, fz, r, y) in ((-108, 4, 14, P.PLATEAU_Y + 1), (-104, 74, 12, None), (-78, -30, 6, None)):
        dd = np.hypot(X - fx, Z - fz)
        lvl = y if y is not None else float(np.median(h[(dd < r)]))
        k = smoothstep(r, r + 6, dd)
        h = np.where(dd < r + 6, lvl * (1 - k) + h * k, h)

    # --- the spring and the creek ---------------------------------------------------------------
    dc = np.abs(X - cx)
    creek = (dc < 1.7) & (d < floor_edge)
    spring = np.hypot(X + 0.5, Z + 0.5) < 5.2
    H = np.round(h).astype(int)
    water = np.zeros(sh, int)
    water[creek] = P.CREEK_Y
    water[spring] = P.FLOOR_Y
    H = np.where(creek, P.CREEK_Y - 2 + (dc > 1.0), H)
    H = np.where(spring, P.FLOOR_Y - 3, H)
    # banks: the floor eases down to the water
    bank = (dc < 3.5) & ~creek & ~spring & (d < floor_edge)
    H = np.where(bank, np.minimum(H, P.FLOOR_Y), H)

    # --- the island's outline -----------------------------------------------------------------
    inset_w = (2 + 3 * fbm((sh[1],), 16, 2, seed=60)).clip(0, 6)[None, :]
    inset_n = (2 + 4 * fbm((sh[0],), 16, 2, seed=61)).clip(0, 7)[:, None]
    inset_s = (2 + 4 * fbm((sh[0],), 16, 2, seed=62)).clip(0, 7)[:, None]
    land = (X >= P.X_MIN + inset_w) & (Z >= P.Z_MIN + inset_n) & (Z <= P.Z_MAX - inset_s)
    # the creek runs to the very edge at both ends, so it can fall off
    land |= creek & (Z > P.Z_MIN) & (Z < P.Z_MAX)
    H = np.where(land, H, -1)
    water = np.where(land, water, 0)
    L.H, L.water, L.land, L.cx = H, water, land, cx
    L.creek, L.spring = creek & land, spring
    return L


def build_underside(L: Land):
    void = ~L.land
    de = ndimage.distance_transform_edt(~void)
    n = fbm(L.shape, 9, 3, seed=70)
    thick = 4 + 1.1 * de + 4 * n
    bottom = np.maximum(L.H - thick, 5 + 3 * fbm(L.shape, 16, 2, seed=71)).round().astype(int)
    L.bottom = np.where(L.land, bottom, 0)
    return L


# ---- the strata --------------------------------------------------------------------------------------
def band_table():
    """Horizontal clay beds by height: hardened clay the commonest, orange and yellow and white and light grey
    and brown between, red only ever one block thick."""
    rng = np.random.default_rng(77)
    seq = []
    choices = [(B.HARDENED_CLAY, 0, 3), (B.STAINED_CLAY, 1, 3), (B.STAINED_CLAY, 4, 2), (B.STAINED_CLAY, 0, 2),
               (B.STAINED_CLAY, 8, 2), (B.STAINED_CLAY, 12, 2), (B.STAINED_CLAY, 14, 1)]
    weights = np.array([0.3, 0.22, 0.12, 0.1, 0.1, 0.12, 0.04])
    while len(seq) < 140:
        i = rng.choice(len(choices), p=weights / weights.sum())
        bid, dv, tmax = choices[i]
        t = 1 if dv == 14 else int(rng.integers(1, tmax + 1))
        if seq and seq[-1] == (bid, dv):
            continue
        seq += [(bid, dv)] * t
    return seq


BANDS = band_table()
STONE_TOP = 28


def rock_at(y, off):
    yy = y + off
    if yy < STONE_TOP:
        return (B.STONE, 0)
    return BANDS[min(len(BANDS) - 1, max(0, yy - STONE_TOP))]


def slope_deg(H, land):
    Hf = np.where(land, H, np.nan).astype(float)
    gx = np.abs(np.roll(Hf, -1, 0) - np.roll(Hf, 1, 0)) / 2
    gz = np.abs(np.roll(Hf, -1, 1) - np.roll(Hf, 1, 1)) / 2
    return np.degrees(np.arctan(np.nan_to_num(np.hypot(gx, gz), nan=0)))


def write_land(w, L: Land):
    """Rock in beds, soil on the flats, the paint by angle: the beds show wherever the ground is steep."""
    H, bottom, water, land = L.H, L.bottom, L.water, L.land
    ang = slope_deg(H, land)
    Hf = H.astype(int)
    flatn = sum((np.abs(np.roll(Hf, s, a) - Hf) <= 1).astype(int) for a in (0, 1) for s in (1, -1))
    ang = np.where((flatn >= 3) & (ang < 60), np.minimum(ang, 30), ang)
    L.angle = ang
    sh = L.shape
    off = np.round(1.6 * fbm(sh, 30, 2, seed=80)).astype(int)     # beds undulate a little
    patch = fbm(sh, 5, 2, seed=81)                                # five-block patches
    q = np.quantile(patch[land], [0.16, 0.27])
    r = RNG.random(sh)
    stone3 = fbm(sh, 6, 2, seed=82)
    for ix in range(L.nx):
        x = L.x0 + ix
        wx = x - w.x0
        for iz in range(L.nz):
            if not land[ix, iz]:
                continue
            z = L.z0 + iz
            wz = z - w.z0
            top, bot = int(H[ix, iz]), int(bottom[ix, iz])
            col_i = w.ids[wx, :, wz]
            col_d = w.dat[wx, :, wz]
            o = int(off[ix, iz])
            for y in range(bot, top + 1):
                bid, dv = rock_at(y, o)
                if bid == B.STONE and stone3[ix, iz] > 0.2 and (y % 5) < 2:
                    dv = 5
                col_i[y], col_d[y] = bid, dv
            if water[ix, iz]:
                col_i[top], col_d[top] = (B.GRAVEL, 0) if r[ix, iz] < 0.5 else (B.SAND, 0) if r[ix, iz] < 0.8 else (B.CLAY, 0)
                col_i[top + 1:water[ix, iz] + 1] = B.WATER
                col_d[top + 1:water[ix, iz] + 1] = 0
                continue
            a = ang[ix, iz]
            if a >= 40:
                continue                      # the bed shows: banded faces
            on_floor = L.d[ix, iz] < L.floor_edge[0, iz] and top <= P.FLOOR_Y + 3
            near_water = np.abs(L.X[ix, iz] - L.cx[0, iz]) < 6 and on_floor
            pv = patch[ix, iz]
            rr = r[ix, iz]
            if near_water:
                # the creek's banks: grass on dirt, the board's green
                col_i[top - 2:top] = B.DIRT
                col_d[top - 2:top] = 0
                col_i[top], col_d[top] = (B.GRASS, 0) if rr < 0.8 else (B.DIRT, 1)
                continue
            if pv < q[0]:
                # a patch of soil: dirt and coarse dirt half and half, grass on some of it
                col_i[top - 1], col_d[top - 1] = B.DIRT, 0
                col_i[top], col_d[top] = (B.GRASS, 0) if rr < 0.4 else ((B.DIRT, 1) if rr < 0.7 else (B.DIRT, 0))
            elif pv < q[1]:
                col_i[top], col_d[top] = B.HARDENED_CLAY, 0          # the ring of hardened clay round it
            else:
                # the orange ground: red sand with orange clay, red sandstone flecks; never sand over air
                col_i[top - 1], col_d[top - 1] = B.STAINED_CLAY, 1
                col_i[top], col_d[top] = (B.SAND, 1) if rr < 0.5 else ((B.STAINED_CLAY, 1) if rr < 0.85 else (B.RED_SANDSTONE, 0))
    return L


def write_falls(w, L: Land):
    """The creek leaves the board at both ends, pouring off the island's edge into the void."""
    for ix in range(L.nx):
        col = np.nonzero(L.creek[ix, :])[0]
        if len(col) == 0:
            continue
        x = L.x0 + ix
        z_end = L.z0 + col.min()
        for zz in range(z_end - 1, max(P.Z_MIN - 1, z_end - 3), -1):
            if w.inside(x, 0, zz):
                for y in range(8, P.CREEK_Y + 1):
                    if w.id(x, y, zz) == B.AIR:
                        w.set(x, y, zz, B.WATER_FLOW, 8)
                break


def sky_arch(w, L: Land):
    """A natural arch rim to rim across the canyon at z = -3..2, its deck a little over the plateau, its
    underside a long curve, ragged at its edges, banded through like the cliffs it was cut from."""
    z0, z1 = -3, 2
    L.arch_top = {}
    xs = range(-60, 0)
    for x in xs:
        t = abs(x + 0.5) / abs(P.rim_x(0) + 0.5)   # 0 at the centre, 1 at the rims
        if t > 1.08:
            continue
        deck = int(round(P.PLATEAU_Y + 2 - 2 * t * t))
        # thin at the crown, thickening toward the rims where it grows out of the walls
        under = int(round(deck - 4 - 18 * t * t))
        for z in range(z0 - 1, z1 + 2):
            edge = z in (z0 - 1, z1 + 1)
            if edge and RNG.random() < 0.6:
                continue
            top = deck - (1 if edge else 0)
            bot = under + (1 if edge else 0)
            ix, iz = x - L.x0, z - L.z0
            g = L.H[ix, iz] if L.land[ix, iz] else -1
            for y in range(max(bot, 0), top + 1):
                if y <= g:
                    continue
                w.set(x, y, z, *rock_at(y, 0))
            # its deck is weathered ground
            if not edge:
                w.set(x, top, z, *((B.HARDENED_CLAY, 0) if (x * 3 + z) % 4 else (B.STAINED_CLAY, 1)))
            # the ground under the arch stays the ground: the arch is a second storey, recorded apart
            if not edge:
                L.arch_top[(x, z)] = top
    L.arch = (z0, z1)


def paint_biomes(w, L: Land, green):
    """Mesa everywhere, Plains where something grows green: the creek banks and the groves."""
    b = np.full(L.shape, 37, np.uint8)
    b = np.where(green, 1, b)
    w.biome[:L.nx, :] = b
