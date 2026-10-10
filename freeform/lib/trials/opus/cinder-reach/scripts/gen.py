"""Generate Cinder Reach from the plan: red's half (x < 0) is built and turned half a circle onto blue's, then the
objectives are stamped for both teams from their objects.

The look, decided in PLAN.md's last section and made here:
    ground   an ash field: grey stained clay with black clay in five-block patches, grass inset only where water or
             the hamlet makes it (biome savanna, so its grass sits yellow-green beside the ash); over it patches ten
             to thirty blocks across of six-sided dark oak logs, soul sand and coarse dirt, lava pools sunk and
             rimmed, and dead trees
    rock     stone and andesite in beds following the surface, cobble a quarter, black clay as thin beds; the island's
             stone is banded with andesite, cobble, mossy cobble, coarse dirt, gravel and ore, and hangs stalactites
    built    warm: brick ground storeys, spruce upper and dark oak roofs; granite and brick roads and terrace
    accent   lava in the ember pools and the core, glowstone in the lamps, the teams' banners

    python3 gen.py <build-dir>
"""
import math
import sys
import time

import numpy as np
from scipy import ndimage

import plan as P
import common as C
from pgmvox import B, World, rng
from pgmvox import build as BLD
from pgmvox import trees as T
from pgmvox import under as U
from pgmvox import route, props
from pgmvox import forms
from pgmvox.noise import fbm
from pgmvox.orient import ladder as ladder_data, stair as stair_data, turn_world
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


def blobs(seed, cell, cover):
    """Blob-shaped patches `cell` blocks across, covering about `cover` of the land: the high end of smooth noise."""
    f = fbm((w.sx, w.sz), cell, 2, seed=seed)
    return f > np.quantile(f[land], 1 - cover)


# the ash's colour comes in patches: six-sided dark oak logs, soul sand, coarse dirt. The first claim wins a cell.
PATCH = np.zeros((w.sx, w.sz), int)
for code, (seed, cell, cover) in {3: (71, 11, 0.12), 2: (72, 14, 0.11), 1: (73, 17, 0.12)}.items():
    PATCH[blobs(seed, cell, cover)] = code
LOGS6, SOUL, COARSE = (B.LOG2, 13), (B.SOUL_SAND, 0), (B.DIRT, 1)
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
        pk = PATCH[i, k]
        if pk == 1:                                             # a fallen-wood patch, coarse dirt showing through
            blk = LOGS6 if g2[i, k] < 0.75 else COARSE
        elif pk == 2:                                           # soul sand, coarse dirt at its fringe
            blk = SOUL if g2[i, k] < 0.8 else COARSE
        elif pk == 3:                                           # a coarse dirt patch with gravel flecks
            blk = COARSE if g2[i, k] < 0.5 else (B.GRAVEL, 0)
    w.set(x, top, z, *blk)
w.biome[:, :] = SAVANNA
print(f"ground {time.time() - t0:.1f}s")

# ---- the island's stone: beds, patches, ore, and stalactites under it ------------------------------------------------
# lay() left plain stone and andesite beds, so the faces and the underside read as grey. Over the red half (blue's is
# its turn) the body is re-laid: beds three thick that dip across the island, each of one of five stones; patches of
# cobble (a third of it mossy), andesite, coarse dirt and gravel from smooth 3D noise; ore on the exposed faces.
hx = -w.x0
Y3 = np.arange(w.sy)[None, :, None]
body = ((w.ids[:hx] == B.STONE) | (w.ids[:hx] == B.COBBLE))
tilt = 6 * fbm((hx, w.sz), 28, 2, seed=81)
bed = np.floor((Y3 + tilt[:, None, :]) / 3.0).astype(np.int64)
pickbed = ((bed * 73856093) ^ (bed * 19349663 >> 4)) % 100
thin = ((Y3 + (tilt[:, None, :] * 1.5).astype(np.int64)) % 13 == 0)                 # a one-block bed now and then
n_a = fbm((hx, w.sy, w.sz), 8, 3, seed=82)
n_b = fbm((hx, w.sy, w.sz), 6, 3, seed=83)
n_c = fbm((hx, w.sy, w.sz), 10, 2, seed=84)
new_id = np.full(body.shape, B.STONE, dtype=w.ids.dtype)
new_dat = np.zeros(body.shape, dtype=w.dat.dtype)


def put(mask, bid, d=0):
    new_id[mask] = bid
    new_dat[mask] = d


put(pickbed >= 30, B.STONE, 5)                                                       # andesite beds
put(pickbed >= 52, B.STONE, 0)
put(pickbed >= 66, B.COBBLE, 0)
put(pickbed >= 80, B.STONE, 6)                                                       # polished andesite
put(pickbed >= 92, B.STONE, 0)
put(thin & (pickbed % 3 == 0), B.DIRT, 1)                                            # a coarse dirt seam
put(thin & (pickbed % 3 == 1), B.MOSSY, 0)
put(n_a > 0.30, B.COBBLE, 0)                                                         # cobble patches
put((n_a > 0.42) & (n_c > 0.0), B.MOSSY, 0)                                          # mossy where they are thickest
put(n_b < -0.30, B.STONE, 5)                                                         # andesite patches
put(n_c > 0.46, B.DIRT, 1)                                                           # coarse dirt patches
below_solid = np.zeros(body.shape, bool)
below_solid[:, 1:, :] = w.ids[:hx, :-1, :] != 0
gravel = (n_c < -0.5) & below_solid                                                 # gravel only over something solid
put(gravel, B.GRAVEL, 0)
sel = body
w.ids[:hx][sel] = new_id[sel]
w.dat[:hx][sel] = new_dat[sel]
# ore on faces that see air, a speck of one to three blocks
air_ = (w.ids == 0)
seen = np.zeros(w.ids.shape, bool)
for ax in range(3):
    for sh_ in (1, -1):
        seen |= np.roll(air_, sh_, axis=ax)
seen = seen[:hx] & body & (w.ids[:hx] != B.GRAVEL)
ro = rng(P.BOARD, "ore")
spot = seen & (ro.random(seen.shape) < 0.014)
kind = ro.random(seen.shape)
for lo_, hi_, (oid, od) in ((0, .5, (B.COAL_ORE, 0)), (.5, .78, (B.IRON_ORE, 0)), (.78, .88, (B.GOLD_ORE, 0)),
                            (.88, .95, (B.REDSTONE_ORE, 0)), (.95, .99, (B.LAPIS_ORE, 0)), (.99, 1.01, (B.DIAMOND_ORE, 0))):
    m = spot & (kind >= lo_) & (kind < hi_)
    m |= np.roll(m, 1, axis=0) & body & (ro.random(m.shape) < 0.5)                  # a neighbour or two
    m |= np.roll(m, 1, axis=2) & body & (ro.random(m.shape) < 0.35)
    w.ids[:hx][m & body] = oid
    w.dat[:hx][m & body] = od
bottoms = np.where((w.ids != 0).any(axis=1), (w.ids != 0).argmax(axis=1), -1)         # each column's lowest solid y
rim_d = edge_depth(land)
rs = rng(P.BOARD, "stalactites")
n_st = 0
STAL = [(B.STONE, 0), (B.STONE, 5), (B.COBBLE, 0), (B.STONE, 5), (B.MOSSY, 0)]
for i, k in rs.permutation(np.argwhere(land[:hx] & (rim_d[:hx] <= 16) & (rim_d[:hx] >= 0))):
    if rs.random() > 0.045:
        continue
    cx_, cz_ = int(X[i, k]), int(Z[i, k])
    ln = int(rs.integers(4, 11))
    rad = 1.0 + ln / 4.5
    for di in range(-3, 4):
        for dk in range(-3, 4):
            d_ = math.hypot(di, dk)
            ii, kk = i + di, k + dk
            if d_ >= rad or not (0 <= ii < hx and 0 <= kk < w.sz) or not land[ii, kk]:
                continue
            lo = int(bottoms[ii, kk])
            n = int(round(ln * (1 - d_ / rad)))
            for j in range(1, n + 1):
                if lo - j < 1 or w.ids[ii, lo - j, kk] != 0:
                    break
                tip = j == n and rs.random() < 0.5                      # a mossy tip on half of them
                w.ids[ii, lo - j, kk], w.dat[ii, lo - j, kk] = STAL[-1] if tip else STAL[int(rs.integers(len(STAL) - 1))]
            n_st += 1
bottoms = np.where((w.ids != 0).any(axis=1), (w.ids != 0).argmax(axis=1), -1)
red_land = land & (X < 0)
n_vine = forms.root_vines(w, red_land, H, bottoms, rng(P.BOARD, "vines"), chance=0.07, under=6, length=(3, 8))
print(f"island stone {time.time() - t0:.1f}s: {int((w.ids[:hx] == B.COBBLE).sum())} cobble, "
      f"{int(((w.ids[:hx] == B.COAL_ORE) | (w.ids[:hx] == B.IRON_ORE)).sum())} coal and iron, {n_st} stalactite columns, "
      f"{n_vine} vines")

# ---- the platform under the casing: a pit in the bowl's floor, a stone brick floor three down, rock under it ----------
# The casing hangs four over the bowl's top. Under it the bowl is ordinary ground to the platform (no obsidian hull); a
# five-by-five pit three deep holds the platform, so lava falls onto it and leaks, and a stair on the north row climbs out.
cx, cz = P.CORE
top_pit = P.BOWL_Y
PLAT = [(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONE, 6), (B.STONEBRICK, 2)]
for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
        for y in range(P.VENT_BOTTOM + 1, top_pit + 1):
            w.set(x, y, z, B.AIR)
        edge = max(abs(x - cx), abs(z - cz)) == 2
        w.set(x, P.VENT_BOTTOM, z, *((B.STONEBRICK, 0) if edge else C.cell_pick(x, z, PLAT, 1, 4)))
for j, x in enumerate((cx, cx - 1, cx - 2)):
    z = cz - 2
    y = P.VENT_BOTTOM + 1 + j
    for yy in range(P.VENT_BOTTOM + 1, y):
        w.set(x, yy, z, B.STONEBRICK, 0)
    if j < 2:
        w.set(x, y, z, B.STONEBRICK_STAIRS, stair_data("w"))    # the stair rises westward
    else:
        w.set(x, y, z, *C.cell_pick(x, z, CINDER, 2, 3))        # the last cell is the bowl's floor again

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
# the carve cut under gravel the island's beds had laid over solid rock: a roof of it would fall, so it becomes andesite
for _ in range(6):
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == 0)
    if not loose.any():
        break
    w.ids[:, 1:, :][loose] = B.STONE
    w.dat[:, 1:, :][loose] = 5
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


# ---- more ember pools in the ash, and dead trees ---------------------------------------------------------------------
# Sites are the ash's flat ground kept off every road and path (seven blocks), off the buildings, the pond, the sinkhole,
# the tube, the cone round the core and the island's edge, so a pool or a trunk is never on a way a team walks.
near = lambda m: ndimage.distance_transform_edt(~m)                                  # noqa: E731
lane = np.zeros((w.sx, w.sz), bool)
for r in L.routes:
    lane |= np.asarray(route.footprint(X, Z, r["line"], r["width"]), bool)
tube_m = np.zeros((w.sx, w.sz), bool)
for (tx_, tz_), _ in P.tube_cells().items():
    if w.x0 <= tx_ < w.x0 + w.sx:
        tube_m[tx_ - w.x0, tz_ - w.z0] = True
level = (ndimage.maximum_filter(np.where(land, H, 0), size=9) - ndimage.minimum_filter(np.where(land, H, 999), size=9)) <= 3
site = (land & (X < -6) & (deg < 24) & level & (edge_depth(land) >= 7) & (near(lane) >= 7) & (near(keep) >= 9)
        & (near(grid(L.pond, False)) >= 6) & (near(grid(L.sink, False)) >= 8) & (near(tube_m) >= 6)
        & (np.hypot(X - cx, Z - cz) >= 24) & ~grid(L.wood, False) & (near(grid(L.wood, False)) >= 3))
rp = rng(P.BOARD, "pools")
RIM = [(B.OBSIDIAN, 0), (B.OBSIDIAN, 0), (B.COAL_BLOCK, 0), (B.COBBLE, 0), (B.STAINED_CLAY, 15)]
wob = fbm((w.sx, w.sz), 5, 2, seed=91)
taken = [(px, pz, pr + 4) for (px, pz), pr in P.POOLS]
more = []
for i, k in rp.permutation(np.argwhere(site)):
    x, z = int(X[i, k]), int(Z[i, k])
    r_pool = float(rp.uniform(2.3, 4.3))
    if any(math.hypot(x - a_, z - b_) < c_ + r_pool + 3 for a_, b_, c_ in taken):
        continue
    if site[max(0, i - 5):i + 6, max(0, k - 5):k + 6].mean() < 0.8:      # room for the pool and its rim
        continue
    taken.append((x, z, r_pool))
    more.append(((x, z), r_pool))
    if len(more) == 9:
        break
n_lava = 0
for (px, pz), pr in more:                                                           # sunk in the ash, rimmed, uneven
    for x in range(int(px - pr - 3), int(px + pr + 4)):
        for z in range(int(pz - pr - 3), int(pz + pr + 4)):
            i, k = x - w.x0, z - w.z0
            gy_ = hwall(x, z)
            if gy_ < 0 or not land[i, k]:
                continue
            d = math.hypot(x - px, z - pz) / (1 + 0.28 * wob[i, k])
            if d < pr:
                for y in range(gy_ - 1, gy_ + 3):
                    w.set(x, y, z, B.AIR)
                w.set(x, gy_ - 1, z, B.LAVA)
                w.set(x, gy_ - 2, z, B.LAVA)
                w.set(x, gy_ - 3, z, B.OBSIDIAN)
                n_lava += 1
            elif d < pr + 1.3:
                w.set(x, gy_, z, *RIM[int(rp.integers(len(RIM)))])
                w.set(x, gy_ - 1, z, B.OBSIDIAN)
                w.set(x, gy_ - 2, z, B.OBSIDIAN)
POOLED = P.POOLS + more


def dead_tree(x, z, r):
    """A bare trunk of dark oak or spruce with four or five limbs, each a run of lying logs that ends upturned; no
    leaves. Seated on the ground at (x, z); refuses itself if anything but air stands in a limb's way."""
    gy_ = w.top(x, z)
    dark = r.random() < 0.6
    trunk = (B.LOG2, 1) if dark else (B.LOG, 1)
    lying = lambda d, ax: (trunk[0], trunk[1] | (4 if ax == "x" else 8))             # noqa: E731
    h_ = int(r.integers(6, 11))
    for y in range(gy_ + 1, gy_ + h_ + 1):
        w.set(x, y, z, *trunk)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):                                # roots lying out from the foot
        if r.random() < 0.45 and w.id(x + dx, gy_ + 1, z + dz) == B.AIR and w.id(x + dx, gy_, z + dz) != B.AIR:
            w.set(x + dx, gy_ + 1, z + dz, *lying(None, "x" if dx else "z"))
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    r.shuffle(dirs)
    for n_, (dx, dz) in enumerate(dirs[:int(r.integers(3, 5))] + [dirs[0]]):
        y = gy_ + int(h_ * r.uniform(0.45, 0.85)) + n_ % 2
        run = int(r.integers(2, 4))
        for s_ in range(1, run + 1):
            bx, bz = x + dx * s_, z + dz * s_
            if w.id(bx, y, bz) == B.AIR:
                w.set(bx, y, bz, *lying(None, "x" if dx else "z"))
        ex, ez = x + dx * run, z + dz * run
        for up in range(1, int(r.integers(2, 4))):                                    # the limb turns up at its end
            if w.id(ex, y + up, ez) == B.AIR:
                w.set(ex, y + up, ez, *trunk)
        if run == 3 and r.random() < 0.6:                                             # a twig off the limb
            tx_, tz_ = x + dx * 2 + dz, z + dz * 2 + dx
            if w.id(tx_, y, tz_) == B.AIR:
                w.set(tx_, y, tz_, *lying(None, "z" if dx else "x"))
    return h_


rd = rng(P.BOARD, "dead trees")
near_pool = np.zeros((w.sx, w.sz), bool)
for (px, pz), pr in POOLED:
    near_pool |= np.hypot(X - px, Z - pz) < pr + 12
pool_m = np.zeros((w.sx, w.sz), bool)
for (px, pz), pr in POOLED:
    pool_m |= np.hypot(X - px, Z - pz) < pr + 3
tree_site = site & (near(pool_m) >= 4) & (X < -10)
dead = []
for want_pool, count in ((True, 3), (False, 7)):
    for i, k in rd.permutation(np.argwhere(tree_site & (near_pool if want_pool else ~near_pool))):
        x, z = int(X[i, k]), int(Z[i, k])
        if any(math.hypot(x - a_, z - b_) < 14 for a_, b_ in dead):
            continue
        dead_tree(x, z, rd)
        dead.append((x, z))
        if len(dead) >= count:
            break
print(f"pools and dead trees {time.time() - t0:.1f}s: {len(more)} new pools ({n_lava} lava columns), {len(dead)} dead trees")
print("  pools", [(p_[0], p_[1], round(r_, 1)) for p_, r_ in more])
print("  dead trees", dead)

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
