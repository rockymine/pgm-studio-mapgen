"""Generate Vinewatch Ruins from the plan: red's half (z < 0) is built and mirrored onto blue's, then the middle
(the plaza, the ziggurat and the cistern, which lie on the axis) is built over both, then the spawns are stamped.

The look, decided in the report's plan section and made here:
    built    a pale temple: polished diorite, diorite and quartz, a quarter each in cells of three; quartz pillars
    ground   jungle: grass with worn dirt and coarse dirt, a marsh of mud and pools; the bowl's rim in stone
    green    jungle trees in the thicket and on the rim, vines on the walls, ferns kept low
    accent   gold on the shrine's lid, glowstone in the cistern, the teams' banners

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
import common as C
from pgmvox import B, World, rng
from pgmvox import trees as T
from pgmvox.noise import fbm
from pgmvox.orient import stair as stair_data, turn_world

t0 = time.time()
R = P.build()
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=96)
X, Z = w.grid()
r_ = rng(P.BOARD, "ruins")
PALE = [(B.STONE, 4), (B.STONE, 3), (B.QUARTZ, 0), (B.STONE, 4)]
WALL = [(B.STONE, 4), (B.STONE, 4), (B.STONE, 3), (B.STONEBRICK, 1)]     # mossy brick faintly, as the ruling allows
JUNGLE = 21
g = C.grain((w.sx, w.sz), 31)
rim_n = fbm((w.sx, w.sz), 9, 3, seed=32)


def kind(x, z):
    return R.kind(x, z)


def in_red(x, z):
    return z < 0


# ---- the ground: the bowl, its rim, the floors ---------------------------------------------------------------
for i, k in np.argwhere(np.ones((w.sx, w.sz), bool)):
    x, z = int(X[i, k]), int(Z[i, k])
    kd, h = kind(x, z), R.h(x, z)
    if kd == "rim":
        top = 52 + int(6 * (0.5 + 0.5 * rim_n[i, k])) + min(8, max(0, 3 * (min(abs(x + 0.5) - 44, 0) * 0)))
        w.column(x, z, 1, top - 1, B.STONE)
        w.set(x, top, z, *((B.GRASS, 0) if rim_n[i, k] > -0.2 else (B.STONE, 5)))
        continue
    base = 41 if kd in ("thicket", "wall", "cover", "pillar") else h
    w.column(x, z, 1, base - 3, B.STONE)
    w.column(x, z, base - 2, base - 1, B.DIRT)
    if kd in ("jungle", "thicket", "wall", "cover", "pillar"):
        top = (B.DIRT, 1) if g[i, k] > 0.75 else (B.GRASS, 0)
        w.set(x, base, z, *top)
    elif kd == "marsh":
        pool = g[i, k] < -0.35 and abs(x + 41) > 2 or (abs(z + 0.5) > 4 and g[i, k] < -0.6)
        if pool and not (-43 <= x <= -38 and -4 <= z <= 3):
            w.set(x, base - 1, z, B.DIRT); w.set(x, base, z, B.WATER)
            if r_.random() < 0.15:
                w.set(x, base + 1, z, B.LILY)
        else:
            w.set(x, base, z, *((B.DIRT, 1) if g[i, k] > 0.2 else (B.GRASS, 0)))
    else:
        w.column(x, z, base - 2, base - 1, B.STONE)
        w.set(x, base, z, *C.cell_pick(x, z, PALE, 3, 1))
print(f"ground {time.time() - t0:.1f}s")

# ---- the made things on red's half: walls, cover, pillars, the court's sides, the stairs -----------------------------
for i, k in np.argwhere(Z < 0):
    x, z = int(X[i, k]), int(Z[i, k])
    kd, h = kind(x, z), R.h(x, z)
    if kd == "wall":
        for y in range(42 if h < P.SPAWN_Y + 3 else 41, h + 1):
            w.set(x, y, z, *C.cell_pick(x, y * 7 + z, WALL, 2, 3))
        w.set(x, h, z, B.STONE, 4)
    elif kd == "cover":
        floor = max(R.h(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if R.kind(x + dx, z + dz) in P.WALK)
        for y in range(floor + 1, floor + 3):
            w.set(x, y, z, B.STONE, 3)
        w.set(x, floor + 3, z, B.QUARTZ, 1)                    # chiselled quartz cap: a ruined plinth
    elif kd == "pillar":
        floor = max([R.h(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
                     if R.kind(x + dx, z + dz) in P.WALK] or [41])
        for y in range(floor + 1, floor + 6):
            w.set(x, y, z, B.QUARTZ, 2)
    elif kd == "court":
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):      # the court's sides: a revetment of pale stone
            nk = R.kind(x + dx, z + dz)
            if nk not in ("court", "stair") and nk in P.WALK:
                for y in range(h + 1, R.h(x + dx, z + dz) + 1):
                    w.set(x + dx, y, z + dz, *C.cell_pick(x + dx, y, WALL, 2, 4))
    if kd == "causeway" and R.kind(x, z) == "causeway":
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):      # the causeway's sides
            if R.kind(x + dx, z + dz) == "marsh":
                for y in range(37, h):
                    w.set(x, y, z, *C.cell_pick(x, y, WALL, 2, 5))
for (x, z), rises in R.stair.items():
    if z < 0 and R.kind(x, z) == "stair" and abs(x) < 30 or (z < 0 and R.kind(x, z) == "stair" and x >= 30):
        y = R.h(x, z)
        for yy in range(y + 1, y + 5):
            if w.id(x, yy, z) not in (B.AIR,) and yy <= 46:
                w.set(x, yy, z, B.AIR)
        w.set(x, y, z, B.QUARTZ_STAIRS, stair_data(rises))
        w.column(x, z, y - 3, y - 1, B.STONE, 3)
# the gate-court: banners on its back wall, a canopy of slabs over the back row
x0, z0, x1, z1 = P.SPAWN_COURT
for x in range(x0, x1 + 1):
    for z in range(z0, z0 + 3):
        w.set(x, P.SPAWN_Y + 5, z, B.SLAB, 7)                      # quartz slab (6 is nether brick)
for x in (x0 + 2, (x0 + x1) // 2, x1 - 2):
    w.banner(x, P.SPAWN_Y + 3, z0, 1, wall_facing=3)
print(f"red's ruins {time.time() - t0:.1f}s")

# ---- the thicket and the rim: jungle trees; vines on the walls ---------------------------------------------------
lib = T.kinds(T.library())
planted = []
thicket = np.vectorize(lambda x, z: kind(x, z) == "thicket")(X, Z) & (Z < 0)
n_t = T.scatter(w, thicket, lib, {"jungle": 0.7, "dense-oak": 0.3}, rng(P.BOARD, "thicket"), spacing=0.7, tries=400,
                planted=planted, allowed=lambda x, z: kind(x, z) in ("thicket", "rim") and z < 0)
for i, k in np.argwhere(thicket):                               # the thicket's floor: leaves, so it reads as wood
    x, z = int(X[i, k]), int(Z[i, k])
    if w.id(x, 42, z) == B.AIR and r_.random() < 0.45:
        w.set(x, 42, z, B.LEAVES, 3 | 4)
        if r_.random() < 0.4 and w.id(x, 43, z) == B.AIR:
            w.set(x, 43, z, B.LEAVES, 3 | 4)
rim = np.vectorize(lambda x, z: kind(x, z) == "rim")(X, Z) & (Z < 0) & (np.abs(X + 0.5) < 46)
n_r = T.scatter(w, rim, lib, {"jungle": 1.0}, rng(P.BOARD, "rim"), spacing=0.9, tries=300, planted=planted)
for i, k in np.argwhere(Z < 0):                                 # vines on the walls' faces, now and then
    x, z = int(X[i, k]), int(Z[i, k])
    if kind(x, z) != "wall":
        continue
    for (dx, dz), bit in (((0, 1), 4), ((0, -1), 1), ((1, 0), 2), ((-1, 0), 8)):
        if R.kind(x + dx, z + dz) in P.WALK and r_.random() < 0.3:
            for y in range(R.h(x, z) - 1, R.h(x, z) - 1 - int(r_.integers(1, 4)), -1):
                if w.id(x + dx, y, z + dz) == B.AIR:
                    w.set(x + dx, y, z + dz, B.VINE, bit)
for i, k in np.argwhere((Z < 0) & (g < -0.5)):                    # ferns on the jungle floor, low, few
    x, z = int(X[i, k]), int(Z[i, k])
    if kind(x, z) == "jungle" and w.id(x, 42, z) == B.AIR and r_.random() < 0.25:
        w.set(x, 42, z, B.TALLGRASS, 2)
print(f"green {time.time() - t0:.1f}s: {n_t} in the thicket, {n_r} on the rim")

turn_world(w, "mirror_z", Z < 0, banners={1: 4})

# ---- the middle, on the axis: the ziggurat, its lid and the cistern -------------------------------------------------
for half, h in P.ZIG:
    for x in range(-half, half):
        for z in range(-half, half):
            w.column(x, z, 38, h - 1, B.QUARTZ, 0)
            w.set(x, h, z, *C.cell_pick(x, z, PALE, 3, 2))
    for x in range(-half, half):                                # each tier's riser trimmed in chiselled quartz
        for z in (-half, half - 1):
            w.set(x, h - 1, z, B.QUARTZ, 1)
    for z in range(-half, half):
        for x in (-half, half - 1):
            w.set(x, h - 1, z, B.QUARTZ, 1)
for (x, z), rises in R.stair.items():                           # the ziggurat's stairs, both faces
    if R.kind(x, z) == "stair" and abs(x) <= 1 and abs(z + 0.5) <= 14:
        w.set(x, R.h(x, z), z, B.QUARTZ_STAIRS, stair_data(rises))
for x, z in ((-5, -5), (4, -5), (-5, 4), (4, 4)):
    for y in range(47, P.SHRINE_ROOF):
        w.set(x, y, z, B.QUARTZ, 2)
for x in range(-6, 6):
    for z in range(-6, 6):
        edge = x in (-6, 5) or z in (-6, 5)
        w.set(x, P.SHRINE_ROOF, z, *((B.GOLD_BLOCK, 0) if edge and (x + z) % 2 else (B.SLAB, 7)))
# the cistern: carved under the plaza and the ziggurat, stone brick, a pool in the hall, lamps
U = R.storey(1)
for i, k in np.argwhere(U.has()):
    x, z = int(X[i, k]), int(Z[i, k])
    if U.kind(x, z) == "pillar":
        w.column(x, z, P.CISTERN_Y, P.CISTERN_Y + 4, B.STONEBRICK, 3)
        continue
    hall = -6 <= x <= 5 and -7 <= z <= 6
    top = P.CISTERN_Y + (5 if hall else 3)
    for y in range(P.CISTERN_Y + 1, top + 1):
        w.set(x, y, z, B.AIR)
    w.set(x, P.CISTERN_Y, z, *((B.STONEBRICK, 0) if (x + z) % 5 else (B.STONEBRICK, 1)))
    w.set(x, top + 1, z, B.STONEBRICK)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx_, nz_ = x + dx, z + dz
        if not (U.inside(nx_, nz_) and U.has()[U.ix(nx_), U.iz(nz_)]):
            for y in range(P.CISTERN_Y, top + 2):
                if w.id(nx_, y, nz_) != B.AIR or R.kind(nx_, nz_) != "stair":
                    w.set(nx_, y, nz_, B.STONEBRICK, 0 if (y + nx_) % 4 else 1)
    if hall and abs(x + 0.5) <= 2 and abs(z + 0.5) <= 2:
        w.set(x, P.CISTERN_Y, z, B.WATER)                       # the cistern's pool, a block deep
    if not hall and x % 8 == 0 and z in (-3, 2):
        w.set(x, top, z, B.GLOWSTONE)
for x, z in ((-6, -7), (5, -7), (-6, 6), (5, 6)):
    w.set(x, P.CISTERN_Y + 5, z, B.GLOWSTONE)
for (x, z), rises in R.stair.items():                           # the stairwells: open over, walled round
    if R.kind(x, z) == "stair" and abs(z + 0.5) <= 2 and abs(x) >= 24:
        y = R.h(x, z)
        for yy in range(y + 1, 46):
            w.set(x, yy, z, B.AIR)
        w.set(x, y, z, B.STONEBRICK_STAIRS, stair_data(rises))
        for dz in (-3, 2):
            for yy in range(y - 1, max(y + 4, 42)):
                w.set(x, yy, dz, B.STONEBRICK)
w.biome[:, :] = JUNGLE
O = P.objectives()
O.stamp(w)
w.save(sys.argv[1], "Vinewatch Ruins", (0, 70, 0))
print(f"saved {time.time() - t0:.1f}s: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
