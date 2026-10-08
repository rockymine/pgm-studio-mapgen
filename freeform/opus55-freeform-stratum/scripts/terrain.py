"""The land under Stratum, painted rather than played: rolling hills laid in swathes of colour that run across
the board like brushstrokes, a lake under the middle shelving to its shores, woods; and the city's own
geometry stuck into it — a monolith driven in at a slant, an obelisk fallen across a field, a cube half sunk in
the lake, a ring tipped on a hill, a slab lying askew.
Then the cloud sea between the land and the city: glass, thick where it gathers, broken where it does not.

Heights are computed over the whole board and made symmetric by the mirror; voxels are written for red's half.
"""
import math

import numpy as np

import geometry as G
import plan as P
from mc import B
from noise import fbm, smoothstep

RNG = np.random.default_rng(808)


class Field:
    def __init__(self):
        self.x0, self.z0 = P.X_MIN, P.Z_MIN
        self.nx, self.nz = P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1
        xs = np.arange(P.X_MIN, P.X_MAX + 1); zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
        self.X, self.Z = np.meshgrid(xs, zs, indexing="ij")
        self.shape = self.X.shape
        self.red = self.X < 0

    def sym(self, a):
        return np.where(self.red, a, a[::-1, :])


def build(F):
    X, Z = F.X.astype(float), F.Z.astype(float)
    sh = F.shape
    hills = fbm(sh, 38, 3, seed=1)
    roll = fbm(sh, 14, 2, seed=2)
    h = 22 + 9 * hills + 3.5 * roll + 6 * smoothstep(40, 95, np.abs(X + 0.5))   # the land rises to the edges
    # the lake under the middle, a basin shelving to its shore
    sd = G.signed_distance(X, Z, P.LAKE) + 1.5 * fbm(sh, 7, 2, seed=3)
    lake = sd < 0
    shore = (sd >= 0) & (sd < 10)
    h = np.where(shore, P.LAKE_Y + 1 + (np.maximum(h, P.LAKE_Y + 1) - P.LAKE_Y - 1) * smoothstep(0, 10, sd), h)
    h = np.where(lake, P.LAKE_Y - 1 - 5 * smoothstep(0, 9, -sd), h)
    F.H = F.sym(np.round(h).astype(int))
    F.lake = F.sym(lake)
    F.shore = F.sym(shore)
    F.sd = F.sym(sd)
    # the swathes: bands of colour across the board, bent by the hills, like strokes of a brush
    stroke = np.sin((X * 0.55 + Z) / 7.5 + 3.0 * fbm(sh, 24, 2, seed=4))
    F.stroke = F.sym(stroke)
    F.band = F.sym(np.floor((X * 0.55 + Z) / (7.5 * math.pi) + 0.5 * fbm(sh, 24, 2, seed=4)).astype(int) % 6)
    F.wood = F.sym(fbm(sh, 13, 2, seed=5))
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
    ang = slope(F.H)
    F.angle = ang
    r = RNG.random(F.shape)
    for ix in range(F.nx):
        x = F.x0 + ix
        if x >= 0:
            continue
        for iz in range(F.nz):
            z = F.z0 + iz
            top = int(F.H[ix, iz])
            ci = w.ids[x - w.x0, :, z - w.z0]
            cd = w.dat[x - w.x0, :, z - w.z0]
            ci[1:top + 1] = B.STONE
            cd[1:top + 1] = 0
            ci[top - 3:top] = B.DIRT
            cd[top - 3:top] = 0
            q = r[ix, iz]
            if F.lake[ix, iz]:
                ci[top], cd[top] = (B.SAND, 0) if q < 0.3 else ((B.CLAY, 0) if q < 0.6 else (B.GRAVEL, 0))
                ci[top + 1:P.LAKE_Y + 1] = B.WATER
                cd[top + 1:P.LAKE_Y + 1] = 0
                continue
            if F.shore[ix, iz] and top <= P.LAKE_Y + 1:
                ci[top], cd[top] = (B.SAND, 0) if q < 0.6 else (B.GRAVEL, 0)
                if q > 0.8 and F.sd[ix, iz] < 2:
                    for k in range(1, 3):
                        ci[top + k], cd[top + k] = B.REEDS, 0
                continue
            if ang[ix, iz] > 48:
                ci[top], cd[top] = (B.STONE, 0) if q < 0.6 else (B.STONE, 5)
                continue
            ground, grows, dens = SWATHES[int(F.band[ix, iz])]
            ci[top], cd[top] = ground
            # thickest in the middle of a stroke, thinning to its edges
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


def fragments(w, F):
    """The city's pieces in the land. Each is concrete, in courses of four, with an orange band and a dark
    one laid in its own frame, so a band runs round a tipped monolith at its tipped angle."""
    for f in P.FRAGMENTS:
        x, z = f["at"]
        w_, h_, d_ = f["size"]
        g = int(F.H[x - F.x0, z - F.z0])
        sink = {"monolith": 0.30, "fallen-obelisk": 0.35, "sunk-cube": 0.5, "ring": 0.25, "slab": 0.4}[f["kind"]]
        base = P.LAKE_Y if f["kind"] == "sunk-cube" else g
        cy = base + h_ / 2 * (1 - 2 * sink) if f["tilt"] < 45 else base + (w_ / 2) * (1 - 2 * sink)
        for (X, Y, Z, u, ly, lz) in box_voxels(x, cy, z, w_, h_, d_, f["yaw"], f["tilt"]):
            if X >= 0 or Y < 1:
                continue
            if f["kind"] == "ring" and abs(u) < w_ / 2 - 4 and abs(ly) < h_ / 2 - 4:
                continue
            band = (ly + h_ / 2)
            if abs(band - h_ * 0.7) < 0.6:
                blk = (B.STAINED_CLAY, 1)
            elif abs(band - h_ * 0.7) < 1.6:
                blk = (B.STAINED_CLAY, 7)
            elif int(band) % 4 == 0:
                blk = (B.STONE, 6)
            else:
                blk = (B.STONE, 0)
            if w.id(X, Y, Z) in (B.AIR, B.WATER, B.TALLGRASS, B.FLOWER, B.DANDELION, B.DIRT, B.GRASS, B.STONE, B.SAND,
                                 B.GRAVEL, B.CLAY, B.REEDS):
                w.set(X, Y, Z, *blk)
        F.fragment_at.append((x, z, f["kind"]))


def clouds(w, F):
    """The cloud sea: where a noise field gathers above a threshold there is cloud, thicker where it gathers
    more, its underside light grey, its top white, its edge plain glass; where it does not, the land shows."""
    sh = F.shape
    gather = F.sym(fbm(sh, 16, 3, seed=50) + 0.35 * fbm(sh, 5, 2, seed=51))
    base = F.sym(P.CLOUD_Y[0] + 3 + 2.5 * fbm(sh, 20, 2, seed=52))
    n = 0
    for ix in range(F.nx):
        x = F.x0 + ix
        if x >= 0:
            continue
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
