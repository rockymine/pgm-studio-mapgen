"""The ground of Hollowcrown, built from the plan's polygons and polylines.

Heights first, over the whole board from red's definitions, made symmetric by the half-turn:
  the vale rising from the river to the mountain's foot; the mountain rising from its foot polygon to its
  summit polygons, rough on its middle slopes and laid in ledges; the Wend's legs cut into the valley face as
  shelves with walls between; the other routes cut into the slope or carried on an embankment; the river with
  its banks cut steep on the outside of each bend and lying low on the inside; the tarn and the brook with
  its two falls, each shelving to its shore.
Then voxels for red's half: rock, soil, paint by slope and by place, the water, the cavern and its lake,
the tunnels.
"""
import math

import numpy as np

import geometry as G
import plan as P
from mc import B
from noise import fbm, smoothstep

RNG = np.random.default_rng(2024)


class Field:
    def __init__(self):
        self.x0, self.z0 = P.X_MIN, P.Z_MIN
        self.nx, self.nz = P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1
        xs = np.arange(P.X_MIN, P.X_MAX + 1); zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
        self.X, self.Z = np.meshgrid(xs, zs, indexing="ij")
        self.shape = self.X.shape
        self.red = self.X < 0

    def sym(self, a):
        return np.where(self.red, a, a[::-1, ::-1])

    def at(self, a, x, z):
        return a[x - self.x0, z - self.z0]


def route_y(pts, s):
    """The y a route is graded to at arc length s (linear between its bends)."""
    acc = 0.0
    for i in range(len(pts) - 1):
        (ax, az, ay), (bx, bz, by) = pts[i], pts[i + 1]
        L = math.hypot(bx - ax, bz - az)
        if s <= acc + L or i == len(pts) - 2:
            t = min(max((s - acc) / L, 0), 1) if L else 0
            return ay + (by - ay) * t
        acc += L
    return pts[-1][2]


def route_field(F, pts):
    d, s = G.polyline(F.X, F.Z, [(x, z) for x, z, y in pts])
    ys = np.vectorize(lambda v: route_y(pts, v))(s)
    return d, s, ys


def brook_level(s):
    """Millbrook's water at arc length s: level between bends, except where a bend drops more than two
    blocks, which is a fall: the upper level holds to a third of the way, then the lower."""
    pts = P.BROOK
    acc = 0.0
    for i in range(len(pts) - 1):
        (ax, az, ay), (bx, bz, by) = pts[i], pts[i + 1]
        L = math.hypot(bx - ax, bz - az)
        if s <= acc + L or i == len(pts) - 2:
            t = min(max((s - acc) / L, 0), 1) if L else 0
            if ay - by > 2:
                return ay if t < 0.34 else by
            return round(ay + (by - ay) * t)
        acc += L
    return pts[-1][2]


def build(F):
    X, Z = F.X.astype(float), F.Z.astype(float)
    sh = F.shape
    rough = fbm(sh, 11, 3, seed=1)
    ridges = 1 - np.abs(fbm(sh, 17, 3, seed=2))
    small = fbm(sh, 5, 2, seed=3)
    broad = fbm(sh, 30, 2, seed=4)

    # ---- the vale: from the river's banks up to the mountain's foot ----------------------------------------
    rx = np.vectorize(P.river_x)(Z)
    across = X - rx                                    # signed distance across the river
    dr = np.abs(across)
    vale = P.PLAIN_Y + (P.FOOT_Y - P.PLAIN_Y) * smoothstep(9, 28, dr) + 0.7 * broad + 0.3 * small

    # ---- the mountain: max over summits of a rise from the foot to the summit's height ---------------------
    din = np.maximum(-G.signed_distance(X, Z, P.FOOT), 0)
    mount = np.full(sh, -1.0)
    for s in P.SUMMITS:
        dk = np.maximum(G.signed_distance(X, Z, s["poly"]), 0)
        t = din / (din + dk + 1e-6)
        g = t ** 1.15
        hk = P.FOOT_Y + (s["y"] - P.FOOT_Y) * g
        mount = np.maximum(mount, hk)
    t_mid = np.clip(mount - P.FOOT_Y, 0, 60) / 60
    mid = 4 * t_mid * (1 - t_mid)                     # 1 on the middle slopes, 0 at the foot and the top
    mount = mount + mid * (5 * rough + 4 * (ridges - 0.5))
    # ledges: the slope laid in benches of five with steep risers, half strength
    q = mount / 5.0
    benched = (np.floor(q) + smoothstep(0.55, 1.0, q - np.floor(q))) * 5.0
    mount = mount + 0.55 * mid * (benched - mount)
    foot_blend = smoothstep(0, 6, din)
    h = np.where(din > 0, vale * (1 - foot_blend) + np.maximum(mount, vale) * foot_blend, vale)
    # the summits are level, a block of roughness at most
    for s in P.SUMMITS:
        inn = G.inside(X, Z, s["poly"])
        h = np.where(inn, s["y"] + np.round(0.6 * small), h)

    # ---- the town: each block of Wendholm takes the height of the Wend where it is nearest -------------------
    wd, ws, wy = route_field(F, P.WEND)
    town_sd = G.signed_distance(X, Z, P.TOWN)
    shelf = np.round(wy)
    kt = smoothstep(0, 4, town_sd)                     # 0 inside the town, 1 four blocks out
    h = np.where(town_sd < 4, shelf * (1 - kt) + h * kt, h)
    market = G.inside(X, Z, P.MARKET)
    h = np.where(market, P.MARKET_Y, h)
    # the drop between two shelves is laid in ledges three high rather than one wall: the higher shelf gives
    # way a block at a time, never on the road itself
    keep = (wd < 3.0) | market | (town_sd >= 0)
    hr = np.round(h)
    for _ in range(5):
        lowest = np.minimum.reduce([np.roll(hr, sft, ax) for ax in (0, 1) for sft in (1, -1)])
        hr = np.where(keep, hr, np.minimum(hr, lowest + 3))
    h = np.where(town_sd < 0, hr, h)

    # ---- the other routes: cut into the slope, or carried on an embankment --------------------------------
    corridors = np.full(sh, np.inf)
    for r in P.ROUTES:
        if r["name"] == "the Wend":
            continue
        d, s, ys = route_field(F, r["pts"])
        core = r["half"] + 0.6
        cut = ys + (h - ys) * smoothstep(core, core + 3, d)
        fill = np.maximum(h, ys - 1.5 * (d - core))
        shaped = np.where(d <= core, ys, np.where(h > ys, cut, fill))
        h = np.where(d < core + 6, shaped, h)
        corridors = np.minimum(corridors, d - core)
    # the Wend's own corridor outside the town (its foot in the vale)
    h = np.where((wd < 2.6) & (town_sd >= 0), wy, h)

    # ---- the tarn: a basin in the shoulder, shelving from its shore ---------------------------------------
    tsd = G.signed_distance(X, Z, P.TARN) + 1.2 * small
    tarn = tsd < 0
    shore_t = (tsd >= 0) & (tsd < 6)
    h = np.where(shore_t, P.TARN_Y + 1 + (np.maximum(h, P.TARN_Y + 1) - P.TARN_Y - 1) * smoothstep(0, 6, tsd), h)
    h = np.where(tarn, P.TARN_Y - 1 - 5 * smoothstep(0, 8, -tsd) + 0.6 * small, h)

    # ---- Millbrook: a channel cut to its water, two falls, a pool under each, banks one above the water -----
    bd, bs = G.polyline(X, Z, [(x, z) for x, z, y in P.BROOK])
    blev = np.vectorize(brook_level)(bs)
    bw = 1.4 + 0.5 * small
    brook = bd < bw
    pools = np.zeros(sh, bool)
    for (fx, fz), nxt in zip(P.FALLS, (2, 7)):
        px_, pz_, py_ = P.BROOK[nxt]
        pd = np.hypot(X - (fx + 2.5), Z - (fz + 0.5)) + 0.8 * small
        pool = pd < 4.2
        pools |= pool
        blev = np.where(pool, py_, blev)
        h = np.where(pool, py_ - 1 - 2.5 * smoothstep(0, 4.2, 4.2 - pd), h)
        ring = (pd >= 4.2) & (pd < 8)
        h = np.where(ring, np.minimum(np.maximum(h, py_ + 1), py_ + 1 + (h - py_ - 1) * smoothstep(4.2, 8, pd)), h)
    bank = (bd >= bw) & (bd < bw + 4) & ~pools
    h = np.where(bank, np.maximum(blev + 1, blev + 1 + (h - blev - 1) * smoothstep(bw, bw + 4, bd)), h)
    h = np.where(brook & ~pools, blev - 1 - (bd < 0.7), h)
    water_b = (brook | pools) & (din > -200)

    # ---- the river: shelving bed, steep outer banks, low inner bars -----------------------------------------
    zs = Z[0, :]
    xr = np.array([P.river_x(z) for z in zs])
    curv = np.gradient(np.gradient(xr))                # x''(z)
    outer_sign = -np.sign(curv)[None, :] * np.ones(sh)
    bend = np.clip(np.abs(curv)[None, :] / (np.abs(curv).max() + 1e-9), 0, 1) * np.ones(sh)
    side = np.sign(across)
    outer = side == outer_sign
    w = P.RIVER_HALF + 1.2 * fbm(sh, 9, 2, seed=8)
    river = dr < w
    # deepest toward the outside of the bend
    shift = 0.35 * w * outer_sign * bend
    an = np.clip(np.abs(across - shift) / w, 0, 1.4)
    bed = P.WATER_Y - 1 - 3.5 * np.clip(1 - an ** 2, 0, 1) + 0.6 * small
    band = np.where(outer, 2.0 + 1.5 * (1 - bend), 4.0 + 4.0 * bend)
    bankr = (dr >= w) & (dr < w + band + 2)
    edge = P.WATER_Y + np.where(outer, 1.0, 0.0)       # the inside of a bend lies flush with the water
    h = np.where(bankr, edge + (h - edge) * smoothstep(w, w + band, dr), h)
    h = np.where(river, bed, h)
    # fords: the bed raised to a block under the water across a band
    ford = np.zeros(sh, bool)
    for fz in P.FORDS:
        f = (np.abs(Z - fz) <= 2) & river
        ford |= f
        h = np.where(f, np.maximum(h, P.WATER_Y - 1), h)

    # ---- the board is the half-turn of red's half ----------------------------------------------------------
    H = F.sym(np.round(h).astype(int))
    F.H = H
    F.river = F.sym(river)
    F.ford = F.sym(ford)
    F.outer = F.sym(outer)
    F.across = F.sym(dr)
    F.tarn = F.sym(tarn)
    F.brook = F.sym(water_b)
    F.blev = F.sym(np.round(blev).astype(int))
    F.pools = F.sym(pools)
    F.town = F.sym(town_sd < 0)
    F.market = F.sym(market)
    F.corr = F.sym(corridors)
    F.wend = F.sym(wd)
    F.wend_y = F.sym(np.round(wy).astype(int))
    F.mount = F.sym(din > 0)
    F.water_any = F.river | F.tarn | F.brook
    F.underhall = F.sym(G.signed_distance(X, Z, P.UNDERHALL) + 2.5 * fbm(sh, 6, 2, seed=30))
    F.mere = F.sym(G.signed_distance(X, Z, P.DEEPMERE) + 1.0 * small)
    F.lowergate = F.sym(G.signed_distance(X, Z, P.LOWER_GATE))
    F.small = small
    F.ceil_n = fbm(sh, 7, 2, seed=31)
    return F


def slope_deg(H):
    Hf = H.astype(float)
    gx = np.abs(np.roll(Hf, -1, 0) - np.roll(Hf, 1, 0)) / 2
    gz = np.abs(np.roll(Hf, -1, 1) - np.roll(Hf, 1, 1)) / 2
    return np.degrees(np.arctan(np.hypot(gx, gz)))


def write(w, F):
    """Rock and soil, then the top painted by what the place is and how steep it lies."""
    H = F.H
    ang = slope_deg(H)
    F.angle = ang
    # how much higher the highest neighbour is: cliffs above, and the scree at their feet
    up = np.maximum.reduce([np.roll(H, s, a) for a in (0, 1) for s in (1, -1)]) - H
    down = H - np.minimum.reduce([np.roll(H, s, a) for a in (0, 1) for s in (1, -1)])
    patch = fbm(F.shape, 4, 2, seed=40)
    mat = fbm(F.shape, 6, 2, seed=41)
    r = RNG.random(F.shape)
    path_mix = RNG.random(F.shape)
    road = F.wend < 2.6
    for ix in range(F.nx):
        x = F.x0 + ix
        for iz in range(F.nz):
            if not F.red[ix, iz]:
                continue
            z = F.z0 + iz
            ci = w.ids[x - w.x0, :, z - w.z0]
            cd = w.dat[x - w.x0, :, z - w.z0]
            top = int(H[ix, iz])
            ci[2:top + 1] = B.STONE
            ys = np.arange(2, top + 1)
            cd[2:top + 1] = np.where((ys + int(3 * patch[ix, iz])) % 11 < 2, 5, np.where((ys + 5) % 17 == 0, 1, 0))
            a = ang[ix, iz]
            soil = 3 if a < 35 else (1 if a < 50 else 0)
            if soil:
                ci[top - soil:top] = B.DIRT
                cd[top - soil:top] = 0
            q = r[ix, iz]
            # --- water and its edges -------------------------------------------------------------
            if F.river[ix, iz]:
                an = F.across[ix, iz]
                ci[top] = B.SAND if (q < 0.35 and top >= P.WATER_Y - 2) else (B.CLAY if q < 0.55 and top >= P.WATER_Y - 2
                                                                              else B.GRAVEL if q < 0.8 else B.DIRT)
                cd[top] = 0
                ci[top + 1:P.WATER_Y + 1] = B.WATER
                cd[top + 1:P.WATER_Y + 1] = 0
                if F.ford[ix, iz] and (x + z) % 2 == 0:
                    ci[P.WATER_Y], cd[P.WATER_Y] = B.STONE, 0
                    ci[P.WATER_Y + 1], cd[P.WATER_Y + 1] = B.SLAB, 0
                continue
            if F.tarn[ix, iz]:
                ci[top], cd[top] = (B.GRAVEL, 0) if q < 0.5 else ((B.CLAY, 0) if q < 0.75 else (B.DIRT, 0))
                ci[top + 1:P.TARN_Y + 1] = B.WATER
                cd[top + 1:P.TARN_Y + 1] = 0
                continue
            if F.brook[ix, iz]:
                lv = int(F.blev[ix, iz])
                ci[top], cd[top] = (B.GRAVEL, 0) if q < 0.6 else ((B.STONE, 0) if q < 0.8 else (B.MOSSY, 0))
                ci[top + 1:lv + 1] = B.WATER
                cd[top + 1:lv + 1] = 0
                continue
            near_water = top <= P.WATER_Y + 2 and F.across[ix, iz] < P.RIVER_HALF + 10
            # --- built ground ----------------------------------------------------------------------
            if F.market[ix, iz]:
                ci[top], cd[top] = ((B.STONE, 6) if (x + 2 * z) % 5 == 0 else (B.STONEBRICK, 0) if q < 0.5 else (B.STONE, 5))
                continue
            if road[ix, iz] and F.town[ix, iz] or (road[ix, iz] and top > P.FOOT_Y):
                m = path_mix[ix, iz]
                ci[top], cd[top] = (B.GRAVEL, 0) if m < 0.34 else ((B.COBBLE, 0) if m < 0.67 else (B.STONE, 5))
                continue
            if F.corr[ix, iz] < 0.01:
                m = path_mix[ix, iz]
                ci[top], cd[top] = (B.DIRT, 1) if m < 0.34 else ((B.GRAVEL, 0) if m < 0.67 else (B.STONE, 5))
                continue
            if F.town[ix, iz] and down[ix, iz] >= 3:
                # a retaining wall: the face of the shelf is masonry
                for yy in range(max(2, top - int(down[ix, iz]) + 1), top + 1):
                    ci[yy], cd[yy] = (B.STONEBRICK, 1 if r[ix, iz] < 0.25 else 2 if r[ix, iz] < 0.4 else 0)
                continue
            # --- the shores: sand and gravel on the inside of a bend, cut earth on the outside -----------
            if near_water:
                outer = F.outer[ix, iz]
                if top <= P.WATER_Y:
                    ci[top], cd[top] = (B.SAND, 0) if q < 0.6 else (B.GRAVEL, 0)
                elif outer:
                    ci[top], cd[top] = (B.GRASS, 0)
                    ci[top - 1], cd[top - 1] = (B.DIRT, 1)
                else:
                    ci[top], cd[top] = (B.SAND, 0) if q < 0.3 else ((B.GRAVEL, 0) if q < 0.45 else (B.GRASS, 0))
                continue
            # --- the mountain and the vale by slope, in patches rather than speckle -------------------
            m = mat[ix, iz]
            if a < 38:
                ci[top], cd[top] = (B.GRASS, 0)
                if m < -0.62:
                    ci[top], cd[top] = (B.DIRT, 1)
                if up[ix, iz] >= 4 and a < 25 and m > 0.2:
                    ci[top], cd[top] = (B.GRAVEL, 0)      # scree at the foot of a cliff
            elif a < 56:
                ci[top], cd[top] = (B.GRASS, 0) if m > -0.05 else ((B.STONE, 5) if m > -0.35 else (B.STONE, 0))
            else:
                ci[top], cd[top] = (B.STONE, 5) if m > 0.15 else ((B.STONE, 0) if m > -0.5 else (B.COBBLE, 0))
    caverns(w, F)


def caverns(w, F):
    """Underhall: the cavern under the mountain, floor 20, a vault rising to 22 blocks over it, never nearer
    the surface than ten; Deepmere shelving in its west; the Lower Gate; the tunnels."""
    sd = F.underhall
    for ix in range(F.nx):
        x = F.x0 + ix
        for iz in range(F.nz):
            if not F.red[ix, iz]:
                continue
            z = F.z0 + iz
            s = sd[ix, iz]
            g = F.lowergate[ix, iz]
            if s >= 0 and g >= 0:
                continue
            surf = int(F.H[ix, iz])
            if s < 0:
                depth_in = -s
                floor = P.HALL_FLOOR + (1 if F.ceil_n[ix, iz] > 0.45 else 0)
                vault = floor + 6 + 16 * smoothstep(0, 14, depth_in) + 3 * F.ceil_n[ix, iz]
            else:
                floor = P.HALL_FLOOR + 1
                vault = floor + 7 - 2 * smoothstep(-4, 0, g)
            vault = int(min(vault, surf - 10))
            m = F.mere[ix, iz]
            col_i = w.ids[x - w.x0, :, z - w.z0]
            col_d = w.dat[x - w.x0, :, z - w.z0]
            if s < 0 and m < 0:
                bed = int(round(P.MERE_Y - 1 - 6 * smoothstep(0, 9, -m)))
                col_i[bed + 1:vault + 1] = B.AIR
                col_i[bed + 1:P.MERE_Y + 1] = B.WATER
                col_d[bed + 1:P.MERE_Y + 1] = 0
                q = RNG.random()
                col_i[bed], col_d[bed] = (B.GRAVEL, 0) if q < 0.45 else ((B.CLAY, 0) if q < 0.75 else (B.STONE, 5))
                continue
            if s < 0 and m < 4:
                floor = int(round(P.MERE_Y + smoothstep(0, 4, m)))       # the shore shelves to the water
            col_i[floor + 1:vault + 1] = B.AIR
            q = RNG.random()
            if s < 0 and m < 4:
                col_i[floor], col_d[floor] = (B.GRAVEL, 0) if q < 0.5 else ((B.CLAY, 0) if q < 0.7 else (B.SAND, 0))
            else:
                col_i[floor], col_d[floor] = (B.STONE, 0) if q < 0.4 else ((B.STONE, 5) if q < 0.7 else ((B.GRAVEL, 0) if q < 0.85 else (B.COBBLE, 0)))
            F.cave_floor[(x, z)] = floor
    tunnels(w, F)


def tunnels(w, F):
    for t in P.TUNNELS:
        if t["height"] == 0:
            continue
        pts = t["pts"]
        cells = G.walk_cells([(x, z) for x, z, y in pts])
        L = G.length([(x, z) for x, z, y in pts])
        n = len(cells)
        for k, (cx, cz) in enumerate(cells):
            y = int(round(route_y(pts, L * k / max(1, n - 1))))
            for dx in range(-t["half"] - 1, t["half"] + 2):
                for dz in range(-t["half"] - 1, t["half"] + 2):
                    X, Z = cx + dx, cz + dz
                    if X >= 0:
                        continue
                    if max(abs(dx), abs(dz)) > t["half"]:
                        continue
                    for yy in range(y + 1, y + t["height"] + 1):
                        if w.id(X, yy, Z) not in (B.WATER,):
                            w.set(X, yy, Z, B.AIR)
                    if w.id(X, y, Z) == B.AIR:
                        w.set(X, y, Z, B.STONE)
                    F.tunnel_floor[(X, Z)] = min(F.tunnel_floor.get((X, Z), 999), y)
            F.tunnel_cells.append((cx, cz, y, t["name"]))


def paint_biomes(w, F):
    w.biome[:, :] = np.where(F.river, 7, np.where(F.mount, 4, 1)).astype(np.uint8)   # river, forest, plains
