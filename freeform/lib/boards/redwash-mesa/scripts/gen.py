"""Generate Redwash Mesa from the plan: red's half (x < 0) is built and mirrored onto blue's, then the objectives are
stamped for both teams from their objects.

The look, decided in the report's plan section and made here:
    ground   badlands: red sand, orange clay and red sandstone, with coarse dirt ringed by hardened clay as patches
    cliffs   mesa banding at fixed heights: hardened clay with orange, yellow, white, brown and thin red beds
    built    pale: smooth sandstone adobe with dark oak vigas, sandstone stairs and trails
    accent   cyan clay window frames and doors' trim, the pool's water, the team banners

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
from pgmvox import props, route
from pgmvox.orient import turn_world
from pgmvox.shapes import edge_depth
from pgmvox.terrain import Strata, beds, by_angle, lay

t0 = time.time()
L = P.land()
w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=100)
X, Z = w.grid()
MESA = 37
HC, ORANGE, RSAND, RSS = (B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 1), (B.SAND, 1), (B.RED_SANDSTONE, 0)
GROUND = [(B.DIRT, 1), HC, RSAND, RSAND, ORANGE, RSS]           # coarse dirt ringed by clay, inside the orange
WASH = [RSAND, RSAND, RSS, HC]
TRAIL = [(B.SANDSTONE, 0), (B.SANDSTONE, 2), (B.PLANKS, 2)]
PLAZA = [(B.SANDSTONE, 2), (B.SANDSTONE, 0), RSS, HC]


def grid(a, fill):
    out = np.full((w.sx, w.sz), fill, dtype=np.asarray(a).dtype)
    out[:a.shape[0], :] = a
    return out


H = grid(L.H, -1)
land = grid(L.land, False)
water = grid(L.water, 0)
bottom = grid(L.bottom, 0)

# ---- the ground: banded cliffs, an orange ground with inset patches ---------------------------------------------
bands = Strata([(HC, 0.32, 4), (ORANGE, 0.2, 3), ((B.STAINED_CLAY, 4), 0.12, 2), ((B.STAINED_CLAY, 0), 0.1, 2),
                ((B.STAINED_CLAY, 12), 0.14, 2), ((B.STAINED_CLAY, 14), 0.06, 1), ((B.STAINED_CLAY, 8), 0.06, 1)],
               length=100, seed=9, start=0)
deg = lay(w, H, land, top=by_angle([(90, ORANGE)]), under=RSS, bands=beds(bands, None, seed=2), from_y=4,
          soil=((30, 2), (40, 1)), bottom=bottom)
g = C.grain((w.sx, w.sz), 91)
g2 = C.grain((w.sx, w.sz), 92)
wash = grid(L.wash, False)
plaza = grid(L.plaza, False)
for i, k in np.argwhere(land):
    x, z, top = int(X[i, k]), int(Z[i, k]), int(H[i, k])
    if water[i, k] > 0:
        w.set(x, top, z, *(RSAND if g[i, k] > 0 else (B.CLAY, 0)))
        w.set(x, top - 1, z, *RSS)
        for y in range(top + 1, water[i, k] + 1):
            w.set(x, y, z, B.WATER)
        continue
    if deg[i, k] > 40:
        continue                                               # the bands show on the faces
    if plaza[i, k]:
        blk = C.cell_pick(x, z, PLAZA, 3, 5)
    elif wash[i, k]:
        blk = C.set_paint(WASH, g[i, k], 0)
    elif deg[i, k] > 28:
        blk = C.cell_pick(x, z, [HC, ORANGE, HC], 2, 1)
    elif g2[i, k] > 0.55 and not wash[i, k]:
        blk = (B.GRASS, 0)                                     # mesa grass in clumps on the flats
    else:
        blk = C.set_paint(GROUND, g[i, k], 0)
    w.set(x, top, z, *blk)
    if blk == RSAND:
        w.set(x, top - 1, z, *RSS)                             # red sand always over something it holds on
w.biome[:, :] = MESA
print(f"ground {time.time() - t0:.1f}s")

# ---- the stairs cut into the cliffs ------------------------------------------------------------------------
for (fx, fz), rises, n in (P.LADDER, P.HEAD, P.BENCH_STAIR):
    if (fx, fz) == P.HEAD[0]:
        sz, y0 = fz + n - 1, P.SHELF - n + 1                   # rising north, built from its foot on the floor
    elif rises == "s":
        sz, y0 = fz, P.at(L, fx, fz - 1) + 1
    else:
        sz, y0 = fz, P.SHELF + 1
    sx = fx - 1 if rises == "n" else fx + 1                    # build.stairs widens to the right of the climb
    dz = -1 if rises == "n" else 1
    for kk in range(n):
        for x in (fx - 1, fx, fx + 1):
            z = sz + dz * kk
            for y in range(y0 + kk + 1, P.MAX_BUILD):
                w.set(x, y, z, B.AIR)                          # the cut, open to the sky
    BLD.stairs(w, sx, sz, rises, y0, n, B.SANDSTONE_STAIRS, width=3, under=(B.SANDSTONE, 2))
    for kk in range(n):                                        # a low parapet where the cut is open
        for x in (fx - 2, fx + 2):
            z = sz + dz * kk
            if w.id(x, y0 + kk, z) == B.AIR and w.id(x, y0 + kk - 1, z) != B.AIR:
                w.set(x, y0 + kk, z, B.SANDSTONE, 2)

# ---- the trails and the plaza -----------------------------------------------------------------------------
hs = P.houses()
keep = np.zeros((w.sx, w.sz), bool)
for b in hs.values():
    for x, z in b["cells"]:
        keep[x - w.x0, z - w.z0] = True
keep |= plaza
for n, r in enumerate(L.routes):
    route.pave(w, w.heightmap(), X, Z, r["line"], width=r["width"], surface=tuple(TRAIL), weights=(0.45, 0.35, 0.2),
               keep=keep, seed=n, clear=3)
print(f"stairs and trails {time.time() - t0:.1f}s")

# ---- the houses: adobe with vigas; the cliff house cut into its cliff ---------------------------------------------
for key, b in hs.items():
    BLD.site(w, b["cells"], b["floor"], lambda x, z: w.top(x, z), margin=1, fill=RSS, top=ORANGE)
for key, b in hs.items():
    out = BLD.house(w, b["house"], ground_at=lambda x, z: w.top(x, z), rng=rng(P.BOARD, f"house {key}"))
    if out["door"][:2] != b["door"]:
        raise RuntimeError(f"{key}: the library put the door at {out['door'][:2]}, the plan at {b['door']}")
    eave = b["floor"] + 4 * b["house"].storeys
    cells = set(b["cells"])
    for x, z in BLD.edge_cells(cells):                         # vigas: beam ends through the parapet's foot
        for ddx, ddz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ox, oz = x + ddx, z + ddz
            if (ox, oz) not in cells and (x * 7 + z * 3) % 3 == 0 and w.id(ox, eave, oz) == B.AIR:
                w.set(ox, eave, oz, B.LOG2, 1 | (4 if ddx else 8))
    for x, z in BLD.edge_cells(cells):                         # cyan frames round the windows
        for y in range(b["floor"] + 1, eave):
            if w.id(x, y, z) == B.STAINED_PANE:
                for yy in (y - 1, y + 1):
                    if w.id(x, yy, z) == B.SANDSTONE:
                        w.set(x, yy, z, B.STAINED_CLAY, 9)
cliff = hs["cliff"]
for x in range(min(c[0] for c in cliff["cells"]) + 1, max(c[0] for c in cliff["cells"]), 3):
    w.banner(x, cliff["floor"] + 6, max(c[1] for c in cliff["cells"]) + 1, 1, wall_facing=3)

# the town's market along the north houses' fronts, kept nine blocks off the monument
props.stalls(w, [(x, 25) for x in range(-66, -57)], P.at(L, -62, 25), "s", every=4, awnings=(1, 9, 4))

# ---- the Silver Drift and its shaft, with a hoist frame on the Table ----------------------------------------------
line = P.mine_line()
U.gallery(w, line, rng(P.BOARD, "drift"), timber=(B.LOG2, 1), fence=(B.DARK_OAK_FENCE, 0), stair=B.DARK_OAK_STAIRS,
          torches=7, ore=(B.GOLD_ORE, 0))

# U.gallery carves each cell's three-by-three-by-three before it floors, so a cell one up from the last has lost the
# floor under it, and a rise's stair faced whichever axis the diagonal step favoured. The drift is mended here so a
# run down it is level or on a stair: floor under every cell, every stair climbing the way the line goes, the
# timber sets' fences (they narrowed three blocks to one) and the pockets the carve spilled into the walls taken out.
DRIFT_FLOOR = ((B.GRAVEL, 0), (B.STONE, 0), (B.STONE, 5))
r_drift = rng(P.BOARD, "drift floor")
sx_, sy_, sz_ = line[-1]                                       # the shaft's five by five, lined after this: its
for i, (x, y, z) in enumerate(line):                           # fences are its walls' footing, so they stay
    rises = i + 1 < len(line) and line[i + 1][1] > y
    in_shaft = abs(z - sz_) <= 2
    for dx in (-1, 0, 1):
        if w.id(x + dx, y - 1, z) in (B.AIR, B.DARK_OAK_STAIRS):
            w.set(x + dx, y - 1, z, *DRIFT_FLOOR[int(r_drift.integers(len(DRIFT_FLOOR)))])
        if w.id(x + dx, y, z) == B.DARK_OAK_STAIRS or (w.id(x + dx, y, z) == B.DARK_OAK_FENCE and not in_shaft):
            w.set(x + dx, y, z, B.AIR)
        if w.id(x + dx, y + 1, z) == B.DARK_OAK_FENCE and not in_shaft:
            w.set(x + dx, y + 1, z, B.AIR)
        if rises:
            w.set(x + dx, y, z, B.DARK_OAK_STAIRS, 3)           # rising north, the way the line runs
    if 6 <= i < len(line) - 4:
        for dx in (-3, -2, 2, 3):
            for dy in range(-1, 3):
                if w.id(x + dx, y + dy, z) == B.AIR:
                    w.set(x + dx, y + dy, z, B.STONE)
ex, ey, ez = line[-1]
U.shaft(w, ex, ez, ey - 1, P.TABLE, wall=(B.PLANKS, 5), post=(B.LOG2, 1), ladder_on="s")
for y in range(ey - 1, P.TABLE + 1):                           # the shaft leaves its foot open where the drift's carve
    if w.id(ex, y, ez + 2) in (B.AIR, B.DARK_OAK_FENCE):       # reached it: the wall behind the ladder is made good
        w.set(ex, y, ez + 2, B.PLANKS, 5)
for dx in (-2, 2):                                             # the hoist: two posts, a beam, a slab roof
    for dz in (-2, 2):
        for y in range(P.TABLE + 1, P.TABLE + 5):
            w.set(ex + dx, y, ez + dz, B.DARK_OAK_FENCE)
for dx in range(-2, 3):
    for dz in range(-2, 3):
        w.set(ex + dx, P.TABLE + 5, ez + dz, B.WOOD_SLAB, 5)
mx, my, mz = line[0]
for y in range(my, my + 4):                                    # the portal's timbers in the canyon wall
    for dx in (-2, 2):
        if w.id(mx + dx, y, mz) != B.AIR:
            w.set(mx + dx, y, mz, B.LOG2, 1)
for dx in range(-2, 3):
    w.set(mx + dx, my + 3, mz, B.LOG2, 1 | 4)

# ---- junipers, dry growth ------------------------------------------------------------------------------------
lib = T.kinds(T.library())
inland = edge_depth(land) >= 2
over_land = lambda x, z: w.x0 <= x < w.x0 + w.sx and w.z0 <= z < w.z0 + w.sz and bool(inland[x - w.x0, z - w.z0])  # noqa: E731
clear = keep.copy()
for r in L.routes:
    clear |= np.asarray(route.footprint(X, Z, r["line"], r["width"] + 4), bool)
mon = [P.MONUMENTS[k][0] for k in P.MONUMENTS]
far = np.min([np.hypot(X - x, Z - z) for x, z in mon], axis=0) > 8
zone = grid(L.junipers, False) & ~clear & (deg < 25) & far
planted = []
n_j = T.scatter(w, zone, lib, {"olive": 0.7, "small-olive": 0.3}, rng(P.BOARD, "junipers"), spacing=1.0, tries=500,
                planted=planted, allowed=over_land)
bench = grid(L.bench, False) & ~clear & (deg < 25) & far & (np.hypot(X + 60, Z - 50) < 14)
n_b = T.scatter(w, bench, lib, {"small-olive": 1.0}, rng(P.BOARD, "bench"), spacing=1.4, tries=80, planted=planted,
                allowed=over_land)
r_ = rng(P.BOARD, "growth")
for i, k in np.argwhere(land & (deg < 25) & ~clear & far):
    x, z, top = int(X[i, k]), int(Z[i, k]), int(H[i, k])
    if w.id(x, top + 1, z) != B.AIR or w.id(x, top, z) not in (B.SAND, B.STAINED_CLAY, B.HARDENED_CLAY, B.GRASS):
        continue
    c = r_.random()
    if c < 0.012:
        w.set(x, top + 1, z, B.DEADBUSH)
    elif c < 0.016 and w.id(x, top, z) == B.SAND:
        for y in range(top + 1, top + 1 + int(r_.integers(1, 4))):
            w.set(x, y, z, B.CACTUS)
    elif c < 0.03 and w.id(x, top, z) == B.GRASS:
        w.set(x, top + 1, z, B.TALLGRASS, 1)
print(f"houses, drift and growth {time.time() - t0:.1f}s: {n_j} junipers, {n_b} on the Bench")

# ---- blue's half, the objectives, save --------------------------------------------------------------------------
turn_world(w, "mirror_x", X < 0, recolour={(B.WOOL, 14): (B.WOOL, 11)}, banners={1: 4})
O = P.objectives()
O.stamp(w)
w.save(sys.argv[1], "Redwash Mesa", (0, 90, 0))
print(f"saved {time.time() - t0:.1f}s: {int(np.count_nonzero(w.ids))} blocks, {len(w.tiles)} tile entities")
