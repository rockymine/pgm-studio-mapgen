"""The land under Stratum, painted rather than played, and drawn once over the whole board: nobody plays on
it, so it keeps no symmetry. The city above is mirrored; the land below is wild.

Rolling hills laid in swathes of colour that run across the board like brushstrokes; a river winding in
from the west into a lake off the middle and out again to the east, its banks shelving; a mesa in the
north-east whose cliffs show their strata in coloured clay; a crater in the south-west; and the city's own
geometry stuck into it all where it fell — a monolith driven in at a slant, an obelisk fallen into the crater,
a yellow cube half sunk in the lake, a lime ring tipped on a hill, a magenta cube on its corner, a glyph
tablet standing in a field, a fallen gate, a stump, a stand of broken columns.
Then the cloud sea between the land and the city: glass, thick where it gathers, broken where it does not.
"""
import math

import numpy as np

import facade as Fa
import geometry as G
import plan as P
from mc import B
from noise import fbm, smoothstep

RNG = np.random.default_rng(808)
STRATA = [(B.STAINED_CLAY, 1), (B.STAINED_CLAY, 4), (B.STAINED_CLAY, 0), (B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 6),
          (B.STAINED_CLAY, 12), (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 8), (B.STAINED_CLAY, 4), (B.STAINED_CLAY, 0)]


class Field:
    def __init__(self):
        self.x0, self.z0 = P.X_MIN, P.Z_MIN
        self.nx, self.nz = P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1
        xs = np.arange(P.X_MIN, P.X_MAX + 1); zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
        self.X, self.Z = np.meshgrid(xs, zs, indexing="ij")
        self.shape = self.X.shape
        self.red = self.X < 0


def build(F):
    X, Z = F.X.astype(float), F.Z.astype(float)
    sh = F.shape
    hills = fbm(sh, 38, 3, seed=1)
    roll = fbm(sh, 14, 2, seed=2)
    h = 23 + 9 * hills + 3.5 * roll
    # the mesa: a table at 40 with stepped cliffs
    msd = G.signed_distance(X, Z, P.MESA) + 3 * fbm(sh, 9, 2, seed=6)
    mesa_h = P.MESA_Y - 4 * np.floor(smoothstep(-1, 9, msd) * 4)          # terraces four high down its cliffs
    h = np.where(msd < 9, np.maximum(h, mesa_h - 2 * smoothstep(6, 9, msd) * (mesa_h - h).clip(0)), h)
    F.mesa = msd < 9
    # the crater
    cx, cz = P.CRATER["at"]
    dc = np.hypot(X - cx, Z - cz) + 1.2 * roll
    r = P.CRATER["r"]
    h = np.where(dc < r, h - 9 * (1 - (dc / r) ** 2), h)
    h = np.where((dc >= r) & (dc < r + 5), h + 3 * (1 - np.abs(dc - r - 1.5) / 3.5).clip(0), h)
    # the river: a channel to the lake's level, its banks shelving over six blocks
    river = np.zeros(sh, bool)
    for pts in (P.RIVER_IN, P.RIVER_OUT):
        d, _ = G.polyline(X, Z, pts)
        wv = 3.2 + 1.2 * fbm(sh, 8, 2, seed=7)
        river |= d < wv
        bank = (d >= wv) & (d < wv + 7)
        h = np.where(bank, P.LAKE_Y + 1 + (np.maximum(h, P.LAKE_Y + 1) - P.LAKE_Y - 1) * smoothstep(wv, wv + 7, d), h)
        h = np.where(d < wv, P.LAKE_Y - 1 - 2 * np.clip(1 - d / wv, 0, 1), h)
    # the lake, shelving to its shore
    sd = G.signed_distance(X, Z, P.LAKE) + 1.5 * fbm(sh, 7, 2, seed=3)
    lake = sd < 0
    shore = (sd >= 0) & (sd < 10)
    h = np.where(shore, P.LAKE_Y + 1 + (np.maximum(h, P.LAKE_Y + 1) - P.LAKE_Y - 1) * smoothstep(0, 10, sd), h)
    h = np.where(lake, P.LAKE_Y - 1 - 5 * smoothstep(0, 9, -sd), h)
    F.H = np.round(h).astype(int)
    F.water = lake | river
    F.lake = F.water
    F.shore = (shore | (~F.water & (np.minimum.reduce([G.polyline(X, Z, pts)[0] for pts in (P.RIVER_IN, P.RIVER_OUT)]) < 9))) & ~F.mesa
    F.sd = np.where(lake, sd, -1.0)
    stroke = np.sin((X * 0.55 + Z) / 7.5 + 3.0 * fbm(sh, 24, 2, seed=4))
    F.stroke = stroke
    F.band = np.floor((X * 0.55 + Z) / (7.5 * math.pi) + 0.5 * fbm(sh, 24, 2, seed=4)).astype(int) % 6
    F.wood = fbm(sh, 13, 2, seed=5)
    F.strata_off = np.round(2 * fbm(sh, 18, 2, seed=8)).astype(int)
    return F


def slope(H):
    Hf = H.astype(float)
    gx = np.abs(np.roll(Hf, -1, 0) - np.roll(Hf, 1, 0)) / 2
    gz = np.abs(np.roll(Hf, -1, 1) - np.roll(Hf, 1, 1)) / 2
    return np.degrees(np.arctan(np.hypot(gx, gz)))


# what each swathe is laid with: ground, then what grows on it and how thickly
SWATHES = [
    ((B.GRASS, 0), [(B.FLOWER, 0)], 0.35),            # poppies
    ((B.GRASS, 0), [(B.TALLGRASS, 1)], 0.5),          # long grass
    ((B.DIRT, 2), [(B.TALLGRASS, 2)], 0.15),          # podzol and ferns
    ((B.GRASS, 0), [(B.DANDELION, 0)], 0.35),         # dandelions
    ((B.GRASS, 0), [(B.FLOWER, 2), (B.FLOWER, 1)], 0.3),   # allium and orchid
    ((B.DIRT, 1), [(B.TALLGRASS, 1)], 0.1),           # coarse earth
]


def write(w, F):
    """The whole board's land. A column under the mesa is laid in strata of coloured clay from the valley's
    floor up, so wherever a cliff cuts it the bands show."""
    ang = slope(F.H)
    F.angle = ang
    r = RNG.random(F.shape)
    for ix in range(F.nx):
        x = F.x0 + ix
        for iz in range(F.nz):
            z = F.z0 + iz
            top = int(F.H[ix, iz])
            ci = w.ids[x - w.x0, :, z - w.z0]
            cd = w.dat[x - w.x0, :, z - w.z0]
            ci[1:top + 1] = B.STONE
            cd[1:top + 1] = 0
            q = r[ix, iz]
            if F.mesa[ix, iz]:
                off = int(F.strata_off[ix, iz])
                for y in range(18, top + 1):
                    blk = STRATA[((y + off) // 2) % len(STRATA)]
                    ci[y], cd[y] = blk
                if ang[ix, iz] < 40:
                    ci[top], cd[top] = (B.DIRT, 1) if q < 0.4 else (B.GRASS, 0)
                    if q > 0.93:
                        ci[top + 1], cd[top + 1] = B.DEADBUSH, 0
                continue
            ci[top - 3:top] = B.DIRT
            cd[top - 3:top] = 0
            if F.water[ix, iz]:
                ci[top], cd[top] = (B.SAND, 0) if q < 0.3 else ((B.CLAY, 0) if q < 0.6 else (B.GRAVEL, 0))
                ci[top + 1:P.LAKE_Y + 1] = B.WATER
                cd[top + 1:P.LAKE_Y + 1] = 0
                continue
            if F.shore[ix, iz] and top <= P.LAKE_Y + 1:
                ci[top], cd[top] = (B.SAND, 0) if q < 0.6 else (B.GRAVEL, 0)
                if q > 0.8:
                    for k in range(1, 3):
                        ci[top + k], cd[top + k] = B.REEDS, 0
                continue
            if ang[ix, iz] > 48:
                ci[top], cd[top] = (B.STONE, 0) if q < 0.6 else (B.STONE, 5)
                continue
            ground, grows, dens = SWATHES[int(F.band[ix, iz])]
            ci[top], cd[top] = ground
            k = abs(F.stroke[ix, iz])
            if q < dens * (0.4 + 0.8 * k):
                g = grows[int(q * 100) % len(grows)]
                ci[top + 1], cd[top + 1] = g


def box_voxels(cx, cy, cz, w_, h_, d_, yaw, tilt):
    """The blocks of a box w by h by d, turned by yaw about the vertical and tipped by tilt about its own
    x axis: for each block in reach, its centre taken back into the box's frame and tested."""
    cyw, syw = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    ct, st = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    R = int(math.ceil(math.sqrt(w_ * w_ + h_ * h_ + d_ * d_) / 2)) + 1
    out = []
    for x in range(int(cx) - R, int(cx) + R + 1):
        for y in range(int(cy) - R, int(cy) + R + 1):
            for z in range(int(cz) - R, int(cz) + R + 1):
                dx, dy, dz = x - cx, y - cy, z - cz
                u = dx * cyw + dz * syw                     # undo the yaw
                v = -dx * syw + dz * cyw
                ly = dy * ct + v * st                       # undo the tilt about the box's x axis
                lz = -dy * st + v * ct
                if abs(u) <= w_ / 2 and abs(ly) <= h_ / 2 and abs(lz) <= d_ / 2:
                    out.append((x, y, z, u, ly, lz))
    return out


SOFT_GROUND = (B.AIR, B.WATER, B.TALLGRASS, B.FLOWER, B.DANDELION, B.DIRT, B.GRASS, B.STONE, B.SAND, B.GRAVEL,
               B.CLAY, B.REEDS, B.STAINED_CLAY, B.HARDENED_CLAY, B.DEADBUSH)


def paint_block(f, u, ly, lz, w_, h_, d_):
    kind, col = f["paint"]
    band = ly + h_ / 2
    if kind == "solid":
        return (B.STONE, 6) if int(band) % 4 == 0 else (B.WOOL, col)
    if kind == "glyph":
        # a glyph scaled over the tablet's front face, set in colour
        if ly > h_ / 2 - 1.0:
            g = Fa.GLYPHS["eye"]
            c = int((u + w_ / 2) / w_ * 5.0)
            r_ = int((lz + d_ / 2) / d_ * 5.0)
            if 0 <= c < 5 and 0 <= r_ < 5 and g[r_][c] == "#":
                return (B.WOOL, col)
        return Fa.SMOOTH
    if abs(band - h_ * 0.7) < 0.6:
        return (B.WOOL, col)
    if abs(band - h_ * 0.7) < 1.6:
        return (B.STAINED_CLAY, 7)
    return (B.STONE, 6) if int(band) % 4 == 0 else (B.STONE, 0)


def fragments(w, F):
    """The city's pieces in the land, each sunk to its own depth, each painted: a band of colour in its own
    frame, solid colour with dark courses, or a glyph across its face."""
    for f in P.FRAGMENTS:
        x, z = f["at"]
        w_, h_, d_ = f["size"]
        g = int(F.H[x - F.x0, z - F.z0])
        if f["kind"] == "columns":
            # a stand of broken columns: five, of different heights, one fallen
            for k, (dx, dz, hh, tilt) in enumerate(((0, 0, 18, 0), (5, 3, 11, 0), (-4, 5, 14, 0), (3, -6, 7, 0), (-7, -3, 16, 74))):
                g2 = int(F.H[x + dx - F.x0, z + dz - F.z0])
                cy = g2 + hh / 2 - 2 if tilt == 0 else g2 + 1
                for (X, Y, Z, u, ly, lz) in box_voxels(x + dx, cy, z + dz, w_, hh, d_, 15 * k, tilt):
                    if 1 <= Y < P.CLOUD_Y[0] - 1 and w.id(X, Y, Z) in SOFT_GROUND:
                        w.set(X, Y, Z, *paint_block(f, u, ly, lz, w_, hh, d_))
            F.fragment_at.append((x, z, f["kind"]))
            continue
        sink = {"monolith": 0.30, "fallen-obelisk": 0.35, "sunk-cube": 0.5, "ring": 0.25, "slab": 0.4, "cube": 0.2,
                "tablet": 0.15, "gate": 0.2, "stump": 0.3}[f["kind"]]
        base = P.LAKE_Y if f["kind"] == "sunk-cube" else g
        extent = h_ if f["tilt"] < 45 else max(w_, d_)
        cy = base + extent / 2 * (1 - 2 * sink)
        for (X, Y, Z, u, ly, lz) in box_voxels(x, cy, z, w_, h_, d_, f["yaw"], f["tilt"]):
            if not (1 <= Y < P.CLOUD_Y[0] - 1):
                continue
            if f["kind"] in ("ring", "gate") and abs(u) < w_ / 2 - 4 and abs(ly) < h_ / 2 - 4:
                continue
            if w.id(X, Y, Z) in SOFT_GROUND:
                w.set(X, Y, Z, *paint_block(f, u, ly, lz, w_, h_, d_))
        F.fragment_at.append((x, z, f["kind"]))


def clouds(w, F):
    """The cloud sea, over the whole board and as unsymmetric as the land: where a noise field gathers above a
    threshold there is cloud, thicker where it gathers more, its underside light grey, its top white, its edge
    plain glass; where it does not, the land shows."""
    sh = F.shape
    gather = fbm(sh, 16, 3, seed=50) + 0.35 * fbm(sh, 5, 2, seed=51)
    base = P.CLOUD_Y[0] + 3 + 2.5 * fbm(sh, 20, 2, seed=52)
    n = 0
    for ix in range(F.nx):
        x = F.x0 + ix
        for iz in range(F.nz):
            gv = gather[ix, iz]
            if gv < 0.12:
                continue
            z = F.z0 + iz
            thick = min(8, (gv - 0.12) * 22)
            b = base[ix, iz]
            lo, hi = int(round(b - thick * 0.35)), int(round(b + thick * 0.65))
            lo, hi = max(lo, P.CLOUD_Y[0]), min(hi, P.CLOUD_Y[1])
            rim = gv < 0.19
            for y in range(lo, hi + 1):
                if w.id(x, y, z) != B.AIR:
                    continue
                if rim:
                    if (x + y + z) % 2 == 0:
                        w.set(x, y, z, B.GLASS)
                elif y == lo:
                    w.set(x, y, z, 95, 8)
                else:
                    w.set(x, y, z, 95, 0)
                n += 1
    return n
