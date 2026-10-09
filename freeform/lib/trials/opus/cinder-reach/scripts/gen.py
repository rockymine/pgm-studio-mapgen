"""Generate Cinder Reach from the plan: red's half (x < 0) is built and turned half a circle onto blue's, then the
objectives are stamped for both teams from their objects.

The look, decided in PLAN.md's last section and made here:
    ground   an ash field: grey stained clay with black clay in five-block patches, grass inset only where water or
             the hamlet makes it (biome savanna, so its grass sits yellow-green beside the ash)
    rock     stone and andesite in beds following the surface, cobble a quarter, black clay as thin beds
    built    warm: brick ground storeys, spruce upper and dark oak roofs; granite and brick roads and terrace
    accent   lava in the ember pools and the core, glowstone in the lamps, the teams' banners

    python3 gen.py <build-dir>
"""
import math
import sys
import time

import numpy as np

import plan as P
import common as C
from pgmvox import B, World, rng
from pgmvox import build as BLD
from pgmvox import trees as T
from pgmvox import under as U
from pgmvox import route, props
from pgmvox.noise import fbm
from pgmvox.orient import ladder as ladder_data, turn_world
from pgmvox.shapes import edge_depth
from pgmvox.terrain import Strata, beds, by_angle, lay

t0 = time.time()
L = P.land()
R = P.build()
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=112)
X, Z = w.grid()
SAVANNA = 35
ASH = [(B.STAINED_CLAY, 15), (B.STAINED_CLAY, 7), (B.STAINED_CLAY, 7), (B.STAINED_CLAY, 8)]   # black and pale drifts in grey
ROCK = [(B.STONE, 0), (B.STONE, 5), (B.STONE, 0), (B.COBBLE, 0)]
CINDER = [(B.STAINED_CLAY, 15), (B.COAL_BLOCK, 0), (B.STAINED_CLAY, 15), (B.STAINED_CLAY, 7)]
WARM_PATH = [(B.STONE, 1), (B.STONE, 2), (B.BRICK, 0)]
WARM_FLOOR = [(B.STONE, 2), (B.STONE, 1), (B.BRICK, 0), (B.HARDENED_CLAY, 0)]


def grid(a, fill):
    out = np.full((w.sx, w.sz), fill, dtype=np.asarray(a).dtype)
    out[:a.shape[0], :] = a
    return out


H = grid(L.H, -1)
land = grid(L.land, False)
water = grid(L.water, 0)
bottom = grid(L.bottom, 0)


def hwall(x, z):
    return int(H[x - w.x0, z - w.z0])


# ---- the ground --------------------------------------------------------------------------------------------
rock = Strata([((B.STONE, 0), 0.45, 4), ((B.STONE, 5), 0.3, 3), ((B.STAINED_CLAY, 15), 0.1, 1),
               ((B.STONE, 6), 0.15, 2)], length=80, seed=5, start=-120)
deg = lay(w, H, land, top=by_angle([(90, (B.STAINED_CLAY, 7))]), under=(B.STAINED_CLAY, 7),
          bands=beds(rock, H, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.06)], seed=4), from_y=3,
          soil=((30, 2), (42, 1)))
g = C.grain((w.sx, w.sz), 61)
g2 = C.grain((w.sx, w.sz), 62)
pond_d = np.hypot((X - P.POND[0][0]) / P.POND[1], (Z - P.POND[0][1]) / P.POND[2])
hamlet = np.hypot((X + 73) / 13.0, (Z - 4) / 15.0) < 1.0
meadow = grid(L.wood, False) | (np.hypot((X + 26) / 16.0, (Z - 36) / 5.0) < 1.0)    # the wood floor, the shore under the Spine
r_ = rng(P.BOARD, "ground")
for i, k in np.argwhere(land):
    x, z, top = int(X[i, k]), int(Z[i, k]), int(H[i, k])
    w.ids[i, :max(0, bottom[i, k]), k] = 0
    w.dat[i, :max(0, bottom[i, k]), k] = 0
    if water[i, k] > 0:
        w.set(x, top, z, *((B.GRAVEL, 0) if g[i, k] > 0 else (B.CLAY, 0)))
        for y in range(top + 1, water[i, k] + 1):
            w.set(x, y, z, B.WATER)
        continue
    a = deg[i, k]
    if L.bowl[i, k] if i < L.bowl.shape[0] else False:
        blk = C.cell_pick(x, z, CINDER, 2, 3)
    elif a > 48:
        continue                                              # the beds show on the faces
    elif a > 32:
        blk = C.cell_pick(x, z, ROCK, 3, 1)
    elif (pond_d[i, k] < 1.9 or hamlet[i, k] or meadow[i, k]) and g2[i, k] > -0.45 and a < 25:
        blk = (B.DIRT, 1) if g2[i, k] > 0.75 else (B.GRASS, 0)   # grass where water, shade or the hamlet keeps it
    else:
        blk = C.set_paint(ASH, g[i, k], 0)
    w.set(x, top, z, *blk)
w.biome[:, :] = SAVANNA
print(f"ground {time.time() - t0:.1f}s")

# ---- the cone: its vent under the casing, lava's catch ----------------------------------------------------------
cx, cz = P.CORE
for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
        for y in range(P.VENT_BOTTOM + 1, P.BOWL_Y + 1):
            w.set(x, y, z, B.AIR)
        w.set(x, P.VENT_BOTTOM, z, B.OBSIDIAN)
for x in range(cx - 3, cx + 4):                                 # the vent's lip and walls in obsidian
    for z in range(cz - 3, cz + 4):
        if max(abs(x - cx), abs(z - cz)) == 3:
            for y in range(P.VENT_BOTTOM, P.BOWL_Y + 1):
                w.set(x, y, z, B.OBSIDIAN)

# ---- the tube and the sinkhole ---------------------------------------------------------------------------------
carved, floor = U.tunnel(w, P.TUBE, ground=H, cover=3)
U.dress_cave(w, (-40, -6, -4, 12, 38, 50), rng(P.BOARD, "tube"), ground=H, ores=60, stalagmites=120,
             floors=((B.STONE, 5), (B.GRAVEL, 0), (B.STONE, 0), (B.STAINED_CLAY, 15)))
(kx, kz), kr, kf = P.SINK
for i, k in np.argwhere(grid(L.sink, False)):                   # the rings: rock, the floor cinder
    x, z = int(X[i, k]), int(Z[i, k])
    w.set(x, int(H[i, k]), z, *C.cell_pick(x, z, ROCK if math.hypot(x - kx, z - kz) > 2 else CINDER, 2, 7))
for (x, z), y in P.tube_cells().items():                        # the tube opens through the sinkhole's rings
    if L.land[x - P.X_MIN, z - P.Z_MIN] and L.sink[x - P.X_MIN, z - P.Z_MIN]:
        for yy in range(y + 1, y + 4):
            w.set(x, yy, z, B.AIR)
        w.set(x, y, z, *C.cell_pick(x, z, CINDER, 2, 7))
print(f"tube {time.time() - t0:.1f}s: {carved} carved")

# ---- the roads and paths, the terrace ---------------------------------------------------------------------------
hs = P.houses()
keep = np.zeros((w.sx, w.sz), bool)
for b in hs.values():
    for x, z in b["cells"]:
        keep[x - w.x0, z - w.z0] = True
tx0, tz0, tx1, tz1 = P.TERRACE
keep[tx0 - w.x0:tx1 - w.x0 + 1, tz0 - w.z0:tz1 - w.z0 + 1] = True
for n, r in enumerate(L.routes):
    route.pave(w, w.heightmap(), X, Z, r["line"], width=r["width"], surface=tuple(WARM_PATH),
               weights=(0.4, 0.35, 0.25) if r["kind"] == "road" else (0.5, 0.4, 0.1), keep=keep, seed=n, clear=3)
for x in range(tx0, tx1 + 1):
    for z in range(tz0, tz1 + 1):
        w.set(x, P.TERRACE_Y, z, *C.cell_pick(x, z, WARM_FLOOR, 3, 2))
        for y in range(P.TERRACE_Y + 1, P.TERRACE_Y + 7):
            w.set(x, y, z, B.AIR)
        for y in range(max(3, hwall(x, z) - 1), P.TERRACE_Y):
            if w.id(x, y, z) == B.AIR:
                w.set(x, y, z, B.BRICK)
        edge = z in (tz0, tz1) or x == tx0
        if edge:
            w.set(x, P.TERRACE_Y + 1, z, *((B.BRICK, 0) if (x + z) % 4 else (B.FENCE, 0)))
for z in (tz0, tz1):                                            # lanterns on the terrace's corners
    for x in (tx0, tx1):
        w.set(x, P.TERRACE_Y + 2, z, B.FENCE); w.set(x, P.TERRACE_Y + 3, z, B.GLOWSTONE)
print(f"roads {time.time() - t0:.1f}s")

# ---- the buildings ---------------------------------------------------------------------------------------------
for key, b in hs.items():
    BLD.site(w, b["cells"], b["floor"], lambda x, z: w.top(x, z), margin=2, fill=(B.STONE, 0),
             top=(B.STAINED_CLAY, 7))
built = {}
for key, b in hs.items():
    built[key] = BLD.house(w, b["house"], ground_at=lambda x, z: w.top(x, z), rng=rng(P.BOARD, f"house {key}"))
    if built[key]["door"][:2] != b["door"]:
        raise RuntimeError(f"{key}: the library put the door at {built[key]['door'][:2]}, the plan at {b['door']}")
lodge = hs["lodge"]
lx = [c[0] for c in lodge["cells"]]
for x in range(min(lx) + 1, max(lx), 3):                        # the team's banners along the lodge's front
    w.banner(x, lodge["floor"] + 4, max(c[1] for c in lodge["cells"]) + 1, 1, wall_facing=3)

# ---- the hamlet's things: a well, a woodpile at the cutter's, a garden of wheat by the long house ---------------
x, z = -71, 3
y = hwall(x, z)
for dx in (-1, 0, 1):
    for dz in (-1, 0, 1):
        w.set(x + dx, y, z + dz, B.COBBLE)
        if dx or dz:
            w.set(x + dx, y + 1, z + dz, B.COBBLE_WALL)
        for yy in range(y + 2, y + 4):
            w.set(x + dx, yy, z + dz, B.AIR)
        w.set(x + dx, y + 3, z + dz, B.WOOD_SLAB, 5)
for yy in range(y - 5, y + 1):
    w.set(x, yy, z, B.WATER)
for dx, dz in ((-1, -1), (1, 1)):
    w.set(x + dx, y + 2, z + dz, B.DARK_OAK_FENCE)
cut = hs["cutter"]
for x in range(-69, -65):                                       # a pile of cut logs along the cutter's south side
    g_ = hwall(x, -5)
    w.set(x, g_ + 1, -5, B.LOG, 1 | 8 if x % 2 else 0 | 8)
    if x in (-68, -67):
        w.set(x, g_ + 2, -5, B.LOG, 0 | 8)
for x in range(-83, -79):                                       # the long house's plot: wheat behind a fence
    for z in range(20, 25):
        g_ = hwall(x, z)
        edge = x in (-83, -80) or z in (20, 24)
        if edge:
            w.set(x, g_ + 1, z, B.DARK_OAK_FENCE)
        else:
            w.set(x, g_, z, B.FARMLAND, 7); w.set(x, g_ + 1, z, B.WHEAT, 7)
w.set(-81, hwall(-81, 21), 21, B.WATER)
w.set(-81, hwall(-81, 21) + 1, 21, B.AIR)
for r in L.routes:                                              # lamps every twelve blocks along the roads
    if r["kind"] != "road":
        continue
    for j in range(6, len(r["line"]) - 3, 12):
        (x, z), (x2, z2) = r["line"][j], r["line"][j + 1]
        n = math.hypot(x2 - x, z2 - z) or 1
        px, pz = int(round(x - (z2 - z) / n * 3.5)), int(round(z + (x2 - x) / n * 3.5))
        if keep[px - w.x0, pz - w.z0] or math.hypot(px - cx, pz - cz) < 15 or px > -12:
            continue
        g_ = w.top(px, pz)
        if w.id(px, g_ + 1, pz) == B.AIR:
            props.lamp(w, px, g_ + 1, pz, post=(B.DARK_OAK_FENCE, 0))

# ---- the Cairn: a ruined watch tower on the tallest knoll, a ladder to its lookout -------------------------------
qx, qz = P.CAIRN
gy = hwall(qx, qz)
rr = rng(P.BOARD, "cairn")
for x in range(qx - 2, qx + 3):
    for z in range(qz - 2, qz + 3):
        ring_ = max(abs(x - qx), abs(z - qz)) == 2
        for y in range(gy - 2, gy + 1):
            w.set(x, y, z, B.STONEBRICK)
        if ring_:
            hgt = 9 if (x + z) % 3 else 11
            if x == qx + 2 and z > qz - 2:                      # the broken east face, open to the fissure
                hgt = 4 + int(rr.integers(0, 3))
            for y in range(gy + 1, gy + hgt):
                w.set(x, y, z, *((B.STONEBRICK, 2) if rr.random() < 0.25 else (B.STONEBRICK, 0)))
for y in (gy + 1, gy + 2):
    w.set(qx - 2, y, qz, B.AIR)                                  # its door, west, toward the path
for x in range(qx - 1, qx + 2):
    for z in range(qz - 1, qz + 2):
        w.set(x, gy + 7, z, B.WOOD_SLAB, 5 | 8)
w.set(qx - 1, gy + 7, qz - 1, B.AIR)
for y in range(gy + 1, gy + 8):
    w.set(qx - 1, y, qz - 1, B.LADDER, ladder_data("n"))

# ---- the ember pools at the wall's foot ----------------------------------------------------------------------
for (px, pz), pr in P.POOLS:
    for x in range(int(px - pr - 2), int(px + pr + 3)):
        for z in range(int(pz - pr - 2), int(pz + pr + 3)):
            d = math.hypot(x - px, z - pz)
            gy_ = hwall(x, z)
            if gy_ < 0:
                continue
            if d < pr:
                for y in range(gy_ - 1, gy_ + 2):
                    w.set(x, y, z, B.AIR)
                w.set(x, gy_ - 1, z, B.LAVA)
                w.set(x, gy_ - 2, z, B.OBSIDIAN)
            elif d < pr + 1.2:
                w.set(x, gy_, z, B.OBSIDIAN)
                w.set(x, gy_ - 1, z, B.OBSIDIAN)
                w.set(x, gy_ - 2, z, B.OBSIDIAN)


# ---- the Scorch Wood: acacia with a few olive, kept off the paths and the sinkhole's brink -----------------------
lib = T.kinds(T.library())
clear = np.zeros((w.sx, w.sz), bool)
for r in L.routes:
    clear |= np.asarray(route.footprint(X, Z, r["line"], r["width"] + 6), bool)
dk = np.hypot(X - kx, Z - kz)
inland = edge_depth(land) >= 2                                    # every block of a tree over land, a block in
over_land = lambda x, z: w.x0 <= x < w.x0 + w.sx and w.z0 <= z < w.z0 + w.sz and bool(inland[x - w.x0, z - w.z0])  # noqa: E731
woodzone = grid(L.wood, False) & ~clear & (dk > kr + 3) & (deg < 30) & inland
planted = []
n_wood = T.scatter(w, woodzone, lib, {"acacia": 0.8, "small-olive": 0.2}, rng(P.BOARD, "wood"), spacing=0.95,
                   tries=900, planted=planted, allowed=over_land)
spine = (grid(L.slope, 0) < 28) & inland & (np.hypot(X + 30, Z - 52) < 12) & ~clear
n_sp = T.scatter(w, spine, lib, {"acacia": 1.0}, rng(P.BOARD, "spine trees"), spacing=1.2, tries=60, planted=planted,
                allowed=over_land)
print(f"buildings and trees {time.time() - t0:.1f}s: {n_wood} in the wood, {n_sp} on the Spine")

# ---- blue's half, the objectives, save --------------------------------------------------------------------------
turn_world(w, "half", X < 0, recolour={(B.WOOL, 14): (B.WOOL, 11), (B.STAINED_GLASS, 14): (B.STAINED_GLASS, 11)},
           banners={1: 4})
O = P.objectives()
O.stamp(w)
w.save(sys.argv[1], "Cinder Reach", (0, 92, 0))
print(f"saved {time.time() - t0:.1f}s: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
