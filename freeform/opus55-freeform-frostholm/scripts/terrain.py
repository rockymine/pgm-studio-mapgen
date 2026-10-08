"""The land (second version): a winter landscape that is mostly land — rolling snowfields, rock outcrops,
crags in the corners, a lake in a hollow — cut across by narrow straits, frozen in stretches.

Fields are computed over the whole board from red's definitions and made symmetric under the half-turn;
voxels are written for red's half only and turned onto blue by gen.py.
"""
import numpy as np

import plan as P
from mc import B
from noise import fbm, smoothstep

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
        return np.where(self.red, a, a[::-1, ::-1])


def strait_fields(F):
    """Distance across each strait (signed, in blocks), its width there, and whether it is frozen."""
    X, Z = F.X.astype(float), F.Z.astype(float)
    U = X - Z
    out = {}
    for k, s in enumerate(P.STRAITS):
        wv = np.vectorize(lambda u: P.wander(u, s["key"]))(U)
        across = (X + Z - s["c"] - wv) / np.sqrt(2)
        width = s["w"] + 1.2 * fbm(F.shape, 11, 2, seed=100 + k)
        frozen = np.zeros(F.shape, bool)
        for a, b in s["ice"]:
            frozen |= (U > a) & (U < b)
        out[s["key"]] = (across, width, frozen)
    return out


def build(F):
    X, Z = F.X.astype(float), F.Z.astype(float)
    sh = F.shape
    hills = fbm(sh, 34, 3, seed=1)
    small = fbm(sh, 9, 3, seed=2)
    crag = 1 - np.abs(fbm(sh, 13, 2, seed=3))
    outcrop = fbm(sh, 13, 2, seed=4)
    s_along = (X + Z) / 2.0                         # -89 at red's corner, 0 at the centre
    # rolling snowfields, higher toward each home corner
    h = P.LAND_Y + 3 + 5 * hills + 1.2 * small + 10 * smoothstep(-55, -85, s_along) * (0.6 + 0.4 * hills)
    # rock outcrops standing out of the fields: ridged crests, a few blocks high
    rocks = smoothstep(0.86, 0.97, crag) * (3 + 5 * smoothstep(0.0, 0.6, outcrop)) * (outcrop > -0.1)
    h += rocks
    # the crags in the corner behind the spawn
    cx, cz = dict((p["key"], p) for p in P.PLACES)["crags"]["at"]
    dc = np.hypot(X - cx, Z - cz)
    h += 16 * np.exp(-(dc / 13.0) ** 2) * (0.75 + 0.5 * crag)

    # --- the straits: the land falls to the water in banks ----------------------------------------
    st = strait_fields(F)
    water = np.zeros(sh, bool)
    ice = np.zeros(sh, bool)
    for key, (across, width, frozen) in st.items():
        a = np.abs(across)
        if "end" in P.STRAITS[[s["key"] for s in P.STRAITS].index(key)]:
            # a fjord: it narrows to nothing where it ends inland
            end = P.STRAITS[[s["key"] for s in P.STRAITS].index(key)]["end"]
            U = X - Z
            width = width * smoothstep(end, end + 22, U)
        if key == "midsund":
            # the lead opens into a pool round Tingholm at the centre, so the islet stands in water
            Uc = X - Z
            width = width + 7.5 * np.exp(-(Uc / 16.0) ** 2)
        wet = a < width
        bank = smoothstep(width, width + 7 + 3 * small, a)
        h = np.where(a < width + 10, P.WATER_Y + 1 + (h - P.WATER_Y - 1) * bank, h)
        water |= wet
        ice |= wet & frozen
    # Tingholm: a rock islet in Midsund at the centre
    dt = np.hypot(X + 0.5, Z + 0.5) + 0.4 * small
    islet = dt < 6.5
    h = np.where(islet, P.WATER_Y + 3 + 3 * np.clip(1 - dt / 6.5, 0, 1) + rocks * 0.5, h)
    water &= ~islet

    # --- the lake in its hollow, and Holmstein on its shore ---------------------------------------
    lx, lz = P.LAKE
    dl = np.hypot(X - lx, (Z - lz) / 1.3) + 1.2 * fbm(sh, 6, 2, seed=5)
    lake_level = P.LAND_Y + 1
    hollow = smoothstep(8.5, 18, dl)
    h = np.where(dl < 18, lake_level + 1 + (np.maximum(h, lake_level + 2) - lake_level - 1) * hollow, h)
    lake = dl < 8.5
    lake_floor = lake_level - 2 - 3 * np.clip(1 - dl / 8.5, 0, 1)
    h = np.where(lake, lake_floor, h)
    mx, mz = P.MONUMENT
    dk = np.hypot(X - mx, Z - mz) + 0.5 * small
    knoll = 7 * np.clip(1 - dk / 7.0, 0, 1) ** 0.7
    h = np.where(dk < 7, np.maximum(h, lake_level + 2 + knoll), h)
    h = np.where(dk < 2.2, lake_level + 8, h)       # the knoll's flat crown where the monument floats

    # --- level ground for the hall, the village, the Beacon ------------------------------------------
    for (fx, fz, r) in ((P.SPAWN[0], P.SPAWN[1], 10), (P.BEACON[0], P.BEACON[1], 7), (-16, -14, 12)):
        d = np.hypot(X - fx, Z - fz)
        level = float(np.median(h[(d < r) & ~water]))
        k = smoothstep(r, r + 6, d)
        h = np.where((d < r + 6) & ~water, level * (1 - k) + h * k, h)

    # the board: the band along the diagonal, a ragged cut; the square's edges are the board's too
    cut = F.sym(P.BAND + 4 * fbm(sh, 14, 2, seed=10))
    inside = np.abs(X - Z) < cut

    H = np.round(h).astype(int)
    H = F.sym(H)
    water = F.sym(water); ice = F.sym(ice); lake = F.sym(lake); islet = F.sym(islet)
    seabed = P.WATER_Y - 3 - 4 * np.clip(1 - np.abs(st["midsund"][0]) / 6, 0, 1) \
        - 3 * np.clip(1 - np.abs(st["ravnsund"][0]) / 6, 0, 1) + small
    seabed = F.sym(np.round(seabed).astype(int))
    H = np.where(water, seabed, H)
    H = np.where(inside, H, -1)
    F.H, F.water, F.ice, F.lake, F.islet, F.inside = H, water & inside, ice & inside, lake & inside, islet, inside
    F.lake_level = lake_level
    F.straits = st
    return F


def slope_deg(H, ok):
    Hf = np.where(ok, H, np.nan).astype(float)
    gx = np.abs(np.roll(Hf, -1, 0) - np.roll(Hf, 1, 0)) / 2
    gz = np.abs(np.roll(Hf, -1, 1) - np.roll(Hf, 1, 1)) / 2
    return np.degrees(np.arctan(np.nan_to_num(np.hypot(gx, gz), nan=0)))


def write(w, F):
    """Stone below in beds; grass under snow on the flats and gentle slopes; bare rock where it is steep;
    gravel and stones on the strait shores; water and ice in the straits and the lake."""
    H = F.H
    ok = F.inside
    ang = slope_deg(H, ok & ~F.water)
    Hf = H.astype(int)
    flatn = sum((np.abs(np.roll(Hf, s, a) - Hf) <= 1).astype(int) for a in (0, 1) for s in (1, -1))
    ang = np.where((flatn >= 3) & (ang < 60), np.minimum(ang, 28), ang)
    F.angle = ang
    patch = fbm(F.shape, 4, 2, seed=20)
    drift = fbm(F.shape, 7, 2, seed=21)
    r = RNG.random(F.shape)
    for ix in range(F.nx):
        x = F.x0 + ix
        for iz in range(F.nz):
            if not F.red[ix, iz] or not ok[ix, iz]:
                continue
            z = F.z0 + iz
            ci = w.ids[x - w.x0, :, z - w.z0]
            cd = w.dat[x - w.x0, :, z - w.z0]
            top = int(H[ix, iz])
            ci[20:top + 1] = B.STONE
            cd[20:top + 1] = np.where((np.arange(20, top + 1) + int(3 * patch[ix, iz])) % 7 < 2, 5, 0)
            if F.water[ix, iz]:
                ci[top], cd[top] = (B.GRAVEL, 0) if r[ix, iz] < 0.55 else ((B.SAND, 0) if r[ix, iz] < 0.8 else (B.STONE, 5))
                ci[top + 1:P.WATER_Y + 1] = B.WATER
                cd[top + 1:P.WATER_Y + 1] = 0
                if F.ice[ix, iz]:
                    ci[P.WATER_Y] = B.ICE
                continue
            a = ang[ix, iz]
            if F.lake[ix, iz]:
                ci[top], cd[top] = B.GRAVEL, 0
                ci[top + 1:F.lake_level + 1] = B.WATER
                ci[F.lake_level] = B.ICE
                cd[top + 1:F.lake_level + 1] = 0
                continue
            if a < 36:
                ci[top - 3:top] = B.DIRT
                cd[top - 3:top] = 0
                ci[top], cd[top] = B.GRASS, 0
                # snow on the ground, deeper in the drifts; podzol where the wind has scoured it bare
                if patch[ix, iz] > -0.55:
                    ci[top + 1], cd[top + 1] = B.SNOW_LAYER, 0 if drift[ix, iz] < 0.25 else 1
                else:
                    ci[top], cd[top] = B.DIRT, 2
            else:
                ci[top], cd[top] = (B.STONE, 0) if r[ix, iz] < 0.45 else ((B.STONE, 5) if r[ix, iz] < 0.82 else (B.COBBLE, 0))
                if a < 50 and patch[ix, iz] > 0.3:
                    ci[top + 1], cd[top + 1] = B.SNOW_LAYER, 0
            # the strait shores: gravel and stones
            if top <= P.WATER_Y + 1 and a < 36:
                ci[top], cd[top] = (B.GRAVEL, 0) if r[ix, iz] < 0.6 else (B.STONE, 5)
            if top >= 74 and a < 45:
                ci[top], cd[top] = B.SNOW, 0
                ci[top + 1] = B.AIR


def paint_biomes(w, F):
    w.biome[:, :] = np.where(F.water, 11, 30).astype(np.uint8)   # cold taiga on land, frozen river in the straits
