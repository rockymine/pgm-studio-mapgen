"""The land and the sea: the crescent and the islands with their rock and snow, the seabed and its shelves,
the sea ice with its open leads, the lake held high in the south-west horn, the Beacon's stack, the
pressure ridges, and the frame of pack ice at the board's edge.

Fields are computed over the whole board from red's definitions and made symmetric under the half-turn;
voxels are written for red's half only and turned onto blue by gen.py.
"""
import numpy as np
from scipy import ndimage

import plan_v1_frozen_sea as P
from mc import B
from noise import fbm, smoothstep, polyline_distance

RNG = np.random.default_rng(1212)


class Field:
    def __init__(self):
        self.x0, self.z0 = P.X_MIN, P.Z_MIN
        self.nx, self.nz = P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1
        xs = np.arange(P.X_MIN, P.X_MAX + 1); zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
        self.X, self.Z = np.meshgrid(xs, zs, indexing="ij")
        self.shape = self.X.shape
        self.red = (self.X + self.Z < -1) | ((self.X + self.Z == -1) & (self.X <= -1))

    def sym(self, a):
        """Red's values, turned onto blue's half."""
        return np.where(self.red, a, a[::-1, ::-1])


def spine_fields(F):
    """For the crescent: how far inside it each cell is (s: 1 on the spine, 0 at the shore), and where along
    it (t: 0 at the north-east tip, 1 at the south-west tip)."""
    X, Z = F.X.astype(float), F.Z.astype(float)
    best = np.full(F.shape, np.inf)
    s = np.full(F.shape, -9.0)
    t = np.zeros(F.shape)
    total = sum(np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(P.SPINE[:-1], P.SPINE[1:]))
    acc = 0.0
    for (ax, az, aw), (bx, bz, bw) in zip(P.SPINE[:-1], P.SPINE[1:]):
        L = np.hypot(bx - ax, bz - az)
        d, along = polyline_distance(X, Z, [(ax, az), (bx, bz)])
        u = along / L
        wid = aw + (bw - aw) * u
        si = 1 - d / wid
        m = si > s
        s = np.where(m, si, s)
        t = np.where(m, (acc + along) / total, t)
        acc += L
    return s, t


def build(F):
    X, Z = F.X.astype(float), F.Z.astype(float)
    sh = F.shape
    n_out = fbm(sh, 7, 3, seed=1)
    n_rock = fbm(sh, 9, 3, seed=2)
    crag = 1 - np.abs(fbm(sh, 6, 2, seed=3))
    s, t = spine_fields(F)
    s = s + 0.22 * n_out                                # coves and points, not a smooth outline
    land = s > 0
    # how high the crescent stands along its length: a rock ridge at the north-east horn, the crags in the
    # corner, the lake's horn in the south-west
    peak = np.interp(t, [0.0, 0.08, 0.3, 0.48, 0.55, 0.7, 0.85, 1.0], [11, 14, 12, 27, 27, 13, 14, 7])
    core = smoothstep(0.0, 0.8, s) ** 0.8
    rough = smoothstep(0.35, 0.55, peak / 27.0)          # the crags only where the island stands high
    h = P.SEA_ICE_Y + 1 + core * peak * (0.85 + 0.15 * n_rock) + core * 7 * rough * smoothstep(0.72, 0.95, crag)
    # benches: the land climbs in steps, and snow lies on every step
    stepped = np.floor(h / 4) * 4 + 4 * smoothstep(0.55, 0.9, (h / 4) % 1)
    h = h + 0.6 * (stepped - h) * core

    # --- the other islands ---------------------------------------------------------------------
    for isl in P.ISLANDS:
        (cx, cz), (rx, rz), pk = isl["at"], isl["r"], isl["peak"]
        d = np.hypot((X - cx) / rx, (Z - cz) / rz) + 0.18 * n_out
        si = 1 - d
        inside = si > 0
        hi = P.SEA_ICE_Y + 1 + smoothstep(0.0, 0.6, si) * pk * (0.7 + 0.3 * n_rock) + 3 * smoothstep(0.75, 0.95, crag) * smoothstep(0, 0.4, si)
        h = np.where(inside & (~land | (hi > h)), np.maximum(hi, np.where(land, h, 0)), h)
        land |= inside
    # the Beacon's stack: a sheer column of rock off the north-east horn
    bx, bz = P.BEACON
    ds = np.hypot(X - bx, Z - bz) + 0.25 * n_out
    stack = ds < 4.6
    h = np.where(stack, 60, h)
    land |= stack

    # --- the spawn's shelf and the village's slope ---------------------------------------------------
    hx, _, hz = P.SPAWN[0], 0, P.SPAWN[2]
    d = np.hypot(X - hx, Z - hz)
    k = smoothstep(9, 15, d)
    h = np.where(d < 15, 63 * (1 - k) + np.maximum(h, 63 - 4) * k, h)
    vx, vz = dict((p["key"], p) for p in P.PLACES)["village"]["at"]
    d = np.hypot(X - vx, Z - vz)
    k = smoothstep(8, 16, d)
    gentle = P.SEA_ICE_Y + 2 + 0.25 * np.maximum(0, (-(X + Z) - 86))   # rising away from the bay
    h = np.where(land & (d < 16), gentle * (1 - k) + h * k, h)

    # --- Kaldvatn, held high in the south-west horn, its rim, its islet, its lip toward the bay ---------
    mx, mz = P.MONUMENT
    dl = np.hypot((X - mx) / 1.0, (Z - mz) / 1.15) + 0.6 * fbm(sh, 5, 2, seed=4)
    lake = dl < 10
    # the horn rises into a broad shoulder that holds the lake: no ring wall, a slope falling away on all sides
    rim = (dl >= 10) & (dl < 26) & land
    rim_h = P.LAKE_Y + 2 + 1.5 * n_rock - 0.55 * np.maximum(0, dl - 11)
    h = np.where(rim, np.maximum(h, rim_h), h)
    h = np.where(lake, P.LAKE_Y - 1 - 3 * (1 - dl / 10), h)
    islet = np.hypot(X - mx, Z - mz) < 3.2
    h = np.where(islet, P.LAKE_Y + 2, h)
    land |= rim | lake
    # the lip: a notch on the bay side where the fall leaves the lake
    lip_dir = np.array([1.0, 0.35]); lip_dir /= np.linalg.norm(lip_dir)
    along = (X - mx) * lip_dir[0] + (Z - mz) * lip_dir[1]
    across = -(X - mx) * lip_dir[1] + (Z - mz) * lip_dir[0]
    lip = (np.abs(across) < 1.6) & (along > 9) & (along < 15)
    h = np.where(lip & land, P.LAKE_Y, h)
    F.lip = (mx + 15 * lip_dir[0], mz + 15 * lip_dir[1])

    H = np.round(h).astype(int)
    H = np.where(land, H, -1)
    H = F.sym(H)
    land = F.sym(land)
    lake = F.sym(lake)
    islet = F.sym(islet)

    # --- the sea: a seabed that shelves up to the shores; sea ice; the leads -------------------------
    dist = ndimage.distance_transform_edt(~land)
    seabed = np.round(P.SEA_FLOOR + 14 * np.exp(-dist / 6.0) + 2 * fbm(sh, 10, 2, seed=5)).astype(int)
    seabed = F.sym(np.minimum(seabed, P.SEA_ICE_Y - 2))
    u = X - Z
    wander = 6.0 * np.sin(u * 2 * np.pi / 90.0) + 2.5 * np.sin(u * 2 * np.pi / 37.0)   # odd in u: the half-turn keeps it
    lead = np.abs(X + Z + 1 - wander) < 5.5 + 1.2 * fbm(sh, 9, 2, seed=6)
    for (tx, tz) in ((-3, -72), (bx, bz), (-72, -4)):
        lead |= np.hypot(X - tx, Z - tz) < 13 + 2 * fbm(sh, 6, 2, seed=7)
    lead = F.sym(lead | lead[::-1, ::-1]) & ~land
    # the board is a band along the spawn-to-spawn diagonal: the far north-east and south-west corners are
    # cut away, the cut ragged; |x - z| is unchanged by the half-turn, so the cut is too
    cut = P.BAND + 4 * fbm(sh, 14, 2, seed=10)
    cut = F.sym(cut)
    inside = np.abs(X - Z) < cut
    # the frame: pack ice heaved up along the board's edge, square sides and cut sides alike
    edge = np.minimum.reduce([X - P.X_MIN, P.X_MAX - X, Z - P.Z_MIN, P.Z_MAX - Z,
                              (cut - np.abs(X - Z)) / np.sqrt(2)]).astype(float)
    frame_w = 4 + 2.5 * fbm(sh, 8, 2, seed=8)
    frame = F.sym(edge < frame_w) & ~land
    frame_h = F.sym(np.round(P.SEA_ICE_Y + 1 + 5 * np.clip(1 - edge / np.maximum(frame_w, 1), 0, 1) * (0.5 + 0.5 * fbm(sh, 3, 2, seed=9)))).astype(int)

    H = np.where(inside, H, -1)
    land &= inside
    F.inside = inside
    F.H, F.land, F.lake, F.islet, F.seabed, F.lead, F.frame, F.frame_h = H, land, lake, islet, seabed, lead, frame, frame_h
    F.s, F.t = s, t
    return F


def slope_deg(H, land):
    Hf = np.where(land, H, np.nan).astype(float)
    gx = np.abs(np.roll(Hf, -1, 0) - np.roll(Hf, 1, 0)) / 2
    gz = np.abs(np.roll(Hf, -1, 1) - np.roll(Hf, 1, 1)) / 2
    return np.degrees(np.arctan(np.nan_to_num(np.hypot(gx, gz), nan=0)))


def write(w, F):
    """Rock below, stone and andesite in beds; on the flats grass under snow; bare rock where it is steep;
    gravel scree at the foot of the crags; the sea, its ice, its leads and its frame."""
    H, land = F.H, F.land
    ang = slope_deg(H, land)
    Hf = H.astype(int)
    flatn = sum((np.abs(np.roll(Hf, s, a) - Hf) <= 1).astype(int) for a in (0, 1) for s in (1, -1))
    ang = np.where((flatn >= 3) & (ang < 60), np.minimum(ang, 30), ang)
    F.angle = ang
    patch = fbm(F.shape, 4, 2, seed=20)
    drift = fbm(F.shape, 7, 2, seed=21)
    r = RNG.random(F.shape)
    for ix in range(F.nx):
        x = F.x0 + ix
        for iz in range(F.nz):
            if not F.red[ix, iz] or not F.inside[ix, iz]:
                continue
            z = F.z0 + iz
            wx, wz = x - w.x0, z - w.z0
            ci = w.ids[wx, :, wz]
            cd = w.dat[wx, :, wz]
            if land[ix, iz]:
                top = int(H[ix, iz])
                ci[4:top + 1] = B.STONE
                cd[4:top + 1] = np.where((np.arange(4, top + 1) + int(3 * patch[ix, iz])) % 7 < 2, 5, 0)
                a = ang[ix, iz]
                if F.lake[ix, iz]:
                    ci[top] = B.GRAVEL if r[ix, iz] < 0.5 else B.DIRT
                    for y in range(top + 1, P.LAKE_Y):
                        ci[y] = B.WATER
                    ci[P.LAKE_Y] = B.ICE
                    cd[top:P.LAKE_Y + 1] = 0
                    continue
                if a < 34:
                    ci[top - 2:top] = B.DIRT
                    cd[top - 2:top] = 0
                    ci[top], cd[top] = B.GRASS, 0
                    # snow lies on the flats, deeper in the drifts
                    depth = 0 if drift[ix, iz] < 0.2 else 1
                    ci[top + 1], cd[top + 1] = B.SNOW_LAYER, depth
                elif a < 52:
                    ci[top], cd[top] = (B.STONE, 0) if r[ix, iz] < 0.4 else ((B.STONE, 5) if r[ix, iz] < 0.75 else (B.COBBLE, 0))
                    if patch[ix, iz] > 0.25:
                        ci[top + 1], cd[top + 1] = B.SNOW_LAYER, 0
                else:
                    ci[top], cd[top] = (B.STONE, 0) if r[ix, iz] < 0.5 else ((B.STONE, 5) if r[ix, iz] < 0.85 else (B.COBBLE, 0))
                # scree: gravel where the ground at a crag's foot is low and near steep rock
                if a < 34 and top <= P.SEA_ICE_Y + 4 and patch[ix, iz] < -0.45:
                    ci[top], cd[top] = B.GRAVEL, 0
                # the very tops of the crags: snow, packed
                if top >= 76 and a < 45:
                    ci[top], cd[top] = B.SNOW, 0
                    ci[top + 1] = B.AIR
                continue
            # the sea
            bed = int(F.seabed[ix, iz])
            ci[4:bed + 1] = B.STONE
            ci[bed] = B.GRAVEL if r[ix, iz] < 0.5 else (B.SAND if r[ix, iz] < 0.8 else B.CLAY)
            ci[bed + 1:P.SEA_ICE_Y + 1] = B.WATER
            cd[bed + 1:P.SEA_ICE_Y + 1] = 0
            if F.frame[ix, iz]:
                for y in range(bed + 1, int(F.frame_h[ix, iz]) + 1):
                    ci[y], cd[y] = B.PACKED_ICE, 0
                continue
            if not F.lead[ix, iz]:
                ci[P.SEA_ICE_Y], cd[P.SEA_ICE_Y] = B.ICE, 0
                if drift[ix, iz] > 0.35 and r[ix, iz] < 0.6:
                    ci[P.SEA_ICE_Y + 1], cd[P.SEA_ICE_Y + 1] = B.SNOW_LAYER, 0


def pressure_ridges(w, F):
    """Ridges of broken ice heaved up across the sea ice: packed ice and ice slabs in a jagged line, one to
    three high, with gaps — the only cover on the open ice."""
    rng = np.random.default_rng(33)
    lines = [[(-30, -56), (-20, -52), (-10, -46), (-2, -44)],
             [(-50, -12), (-44, -20), (-36, -26)],
             [(-12, -28), (-6, -22), (-2, -14)],
             [(14, -64), (22, -58), (26, -50)],
             [(-60, 2), (-54, 10), (-44, 14)]]
    from noise import spline
    for pts in lines:
        for i, (x, z) in enumerate(spline(pts, 0.5)):
            if i % 9 in (0, 1):
                continue                                    # gaps to run through
            for dx in (0, 1):
                X_, Z_ = int(round(x)) + dx, int(round(z))
                ix, iz = X_ - F.x0, Z_ - F.z0
                if not (0 <= ix < F.nx and 0 <= iz < F.nz) or not F.red[ix, iz]:
                    continue
                if F.land[ix, iz] or F.lead[ix, iz] or F.frame[ix, iz]:
                    continue
                hgt = 1 + int(rng.integers(0, 3))
                for y in range(P.SEA_ICE_Y + 1, P.SEA_ICE_Y + 1 + hgt):
                    w.set(X_, y, Z_, B.PACKED_ICE if rng.random() < 0.7 else B.ICE)


def paint_biomes(w, F):
    b = np.where(F.land, 30, 10).astype(np.uint8)       # cold taiga on land, frozen ocean on the sea
    w.biome[:, :] = b
