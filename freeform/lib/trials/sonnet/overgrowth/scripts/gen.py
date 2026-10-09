"""Generate Overgrowth from the plan: red's half (x < 0) is built, then mirrored across the ziggurat (orient.turn_world,
x' = -1 - x); the ziggurat itself is built whole and symmetric.

The ground is the plan's heightfield, exactly. Rock in beds of stone and mossy cobble, grass and podzol on the valley,
the stream's bed of gravel and clay, the terraces' moss. On it: the mossy ziggurat with its H of tunnels, its heart
ladders and its sun chamber; the two courts with their walls, gates and baffles; the cover; the four watchtowers; the
rope bridges; the perimeter wall; and the jungle, kept off every lane the plan walks.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np
from scipy import ndimage

import kit
import plan as P
from pgmvox import B, World, rng
from pgmvox import facade as F
from pgmvox import trees
from pgmvox import terrain as T
from pgmvox.noise import fbm
from pgmvox.orient import stair as stair_data, turn_world

SY = 128
MOSS = (B.STONEBRICK, 1)
BRICK = (B.STONEBRICK, 0)
CRACK = (B.STONEBRICK, 2)
CHISEL = (B.STONEBRICK, 3)


def red_cols(w):
    X, _ = w.grid()
    return X < 0


def stonework(r):
    """A random brick: mostly mossy, some plain, some cracked."""
    def f(x, y, z):
        c = r.random()
        return MOSS if c < 0.5 else BRICK if c < 0.8 else CRACK if c < 0.92 else (B.MOSSY, 0)
    return f


def lay_ground(w, L):
    X, Z = w.grid()
    H = L.H.copy()
    mask = np.ones(H.shape, bool)
    rock = T.Strata([((B.STONE, 0), 3, 4), ((B.STONE, 5), 1.5, 3), ((B.MOSSY, 0), 1.2, 2), ((B.DIRT, 0), 0.8, 2),
                     ((B.GRAVEL, 0), 0.5, 1)], length=120, seed=17, start=0)
    deg = T.lay(w, H, mask, top=T.by_angle([(30, (B.GRASS, 0)), (50, (B.DIRT, 1)), (90, (B.MOSSY, 0))]),
                bands=T.beds(rock, T.bed_offset(H.shape, fold=2, cell=20, seed=3), seed=2), from_y=1, soil=((30, 3), (45, 2), (60, 1)))
    r = rng(P.BOARD, "ground")
    patch, cell = fbm(H.shape, 7, 2, seed=61), r.random(H.shape)
    w.ids[:, 0, :] = B.BEDROCK
    for i, k in np.argwhere(mask):
        top = int(H[i, k])
        a = int(deg[i, k])
        c, pv = cell[i, k], patch[i, k]
        if L.water[i, k]:
            w.ids[i, top, k], w.dat[i, top, k] = (B.GRAVEL, 0) if c < 0.5 else (B.CLAY, 0)
            w.ids[i, top + 1:P.STREAM_Y + 2, k] = B.WATER
            w.dat[i, top + 1:P.STREAM_Y + 2, k] = 0
            continue
        if a <= 30:
            w.ids[i, top, k], w.dat[i, top, k] = ((B.DIRT, 2) if pv > 0.3 and c < 0.6 else (B.GRASS, 0)) if c > 0.04 else (B.DIRT, 1)
        if L.dz[i, k] > 29 and L.dz[i, k] < 34 and a > 10:
            w.ids[i, top, k], w.dat[i, top, k] = (B.MOSSY, 0) if c < 0.5 else (B.DIRT, 1)
    w.biome[:, :] = 21
    return deg


def block_for(kind, r):
    return {"crate": (B.PLANKS, 3), "wall": MOSS, "baffle": MOSS, "pillar": (B.MOSSY, 0), "statue": CHISEL}[kind]


def cover(w, R, L, r):
    """The plan's cover, built: crates of jungle planks, ruined walls with gaps in them, statues topped with gold,
    pillars of mossy cobble, baffles of mossy brick."""
    n = 0
    for c in P.COVER:
        x0, z0, x1, z1 = c["rect"]
        g = R.h(x0, z0) if c["kind"] != "baffle" else P.COURT_Y
        base = g
        top = g + c["h"] if c["kind"] != "baffle" else g + c["h"]
        # the plan's cover floor is ground + h; the ground under it is the column's own
        gx = int(L.H[x0 - w.x0, z0 - w.z0])
        if c["kind"] == "baffle":
            gx = P.COURT_Y
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(gx + 1, gx + c["h"] + 1):
                    if c["kind"] == "wall" and y > gx + 1 and r.random() < 0.18:
                        continue                                          # a ruined wall: gaps in its upper courses
                    if c["kind"] == "statue" and y == gx + c["h"]:
                        w.set(x, y, z, B.GOLD_BLOCK, 0)
                        continue
                    w.set(x, y, z, *(block_for(c["kind"], r) if c["kind"] != "baffle" else
                                     (MOSS if r.random() < 0.7 else CRACK)))
                n += 1
    return n


def tiers(w, R, L, r):
    """The ziggurat: four tiers of mossy brick poured over the valley, banded in chiselled brick and cyan clay, a
    parapet on none of them (the ledges are for walking), the H of tunnels, the chamber, the heart ladders."""
    base_y = P.VALLEY
    fn = stonework(r)
    for key, (x0, z0, x1, z1), y in P.TIERS:
        cells = {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}
        F.extrude(w, cells, base_y, y, base=fn, faces_=[F.band(2, 2, (B.STAINED_CLAY, 9), inset=True),
                                                        F.courses(3, CHISEL), F.glyph_row(max(0, y - base_y - 3), ["eye", "step", "sun"], (B.STAINED_CLAY, 4), spacing=9, min_run=9)])
        for x, z in cells:
            for yy in range(y + 1, y + 6):
                if w.id(x, yy, z) not in (B.AIR,):
                    w.set(x, yy, z, B.AIR)
    # the tunnels: air from the floor over, a pillar and a lamp every few blocks
    for x0, z0, x1, z1 in P.TUNNELS:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                for y in range(62, 65):
                    w.set(x, y, z, B.AIR)
                w.set(x, 61, z, *( (B.STONEBRICK, 0) if (x + z) % 2 else (B.STONEBRICK, 1)))
                w.set(x, 65, z, *BRICK)
    for x in range(-14, 15, 6):
        for z in (-10, -6, 5, 9):
            if (z in (-10, 9) or True) and not (-2 <= x <= 1):
                for y in range(62, 65):
                    w.set(x, y, z, *CHISEL if y == 62 else MOSS)
        for z in (-8, 7):
            w.set(x, 64, z, B.SEA_LANTERN, 0)
    for z in range(-9, 9, 5):
        w.set(-2, 64, z, B.SEA_LANTERN, 0)
        w.set(1, 64, z, B.SEA_LANTERN, 0)
    # the heart: two ladders from the H's crossing up the mass into the chamber
    for hx, face in ((0, "w"), (-1, "e")):
        sup = hx + (1 if face == "w" else -1)
        for y in range(62, 74):
            w.set(hx, y, 0, B.LADDER, 4 if face == "w" else 5)
            w.set(sup, y, 0, *CHISEL if y < 65 else MOSS)
            w.set(hx, y, 1, *MOSS) if y >= 65 else None
            w.set(hx, y, -1, *MOSS) if y >= 65 else None
    # the chamber: walls five high, a roof, four doors, a gold altar, cyan lamps
    x0, z0, x1, z1 = P.CHAMBER
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            for y in range(74, 79):
                w.set(x, y, z, *(fn(x, y, z) if ring else (B.AIR, 0)))
            w.set(x, 79, z, *( (B.SLAB, 5) if ring else (B.STONEBRICK, 3) if (x + z) % 2 else BRICK))
            if not ring:
                w.set(x, 73, z, *( (B.STAINED_CLAY, 9) if (x + z) % 3 == 0 else (B.STAINED_CLAY, 4)) )
    for bx0, bz0, bx1, bz1 in P.CHAMBER_DOORS:
        for x in range(bx0, bx1 + 1):
            for z in range(bz0, bz1 + 1):
                for y in (74, 75, 76):
                    w.set(x, y, z, B.AIR)
    w.set(0, 73, 0, B.AIR)
    w.set(-1, 73, 0, B.AIR)
    for x, z in ((-4, -2), (3, -2), (-4, 2), (3, 2)):
        w.set(x, 74, z, B.GOLD_BLOCK, 0)
        w.set(x, 75, z, B.SEA_LANTERN, 0)
    # the tiers' flights: stairs on the plan's cells
    for i, k in np.argwhere(R.mask("stair") & (np.abs(R.X + 0.5) < 22) & (np.abs(R.Z + 0.5) < 20)):
        x, z, y = int(R.X[i, k]), int(R.Z[i, k]), int(R.H[i, k])
        w.set(x, y, z, B.STONEBRICK_STAIRS, stair_data(R.stair.get((x, z), "e")))
        w.set(x, y - 1, z, *BRICK)
        for yy in range(y + 1, y + 4):
            w.set(x, yy, z, B.AIR)


def courts(w, R, L, r):
    """Red's court: the platform poured from the valley, a floor of tiles, walls six high with their gates, the
    baffles (built with the cover), braziers; the three flights down in mossy stairs."""
    cx0, cz0, cx1, cz1 = P.COURT
    fn = stonework(r)
    cells = {(x, z) for x in range(cx0, cx1 + 1) for z in range(cz0, cz1 + 1)}
    F.extrude(w, cells, P.VALLEY - 2, P.COURT_Y, base=fn, faces_=[F.courses(3, CHISEL), F.band(2, 2, (B.STAINED_CLAY, 9), inset=False)])
    gate_cells = set()
    for side, x0, z0, x1, z1 in P.GATES:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                gate_cells.add((x, z))
    for x, z in cells:
        edge = x in (cx0, cx1) or z in (cz0, cz1)
        if edge:
            for y in range(P.COURT_Y + 1, P.COURT_Y + 7):
                if (x, z) in gate_cells:
                    continue
                w.set(x, y, z, *(fn(x, y, z)))
            if (x, z) not in gate_cells:
                w.set(x, P.COURT_Y + 7, z, *( (B.SLAB, 5) if (x + z) % 2 else (B.AIR, 0)))
        else:
            for y in range(P.COURT_Y + 1, P.COURT_Y + 8):
                w.set(x, y, z, B.AIR)
    F.carpet(w, cx0 + 1, cz0 + 1, cx1 - 1, cz1 - 1, P.COURT_Y, F.first_of(
        F.border(1, (B.STAINED_CLAY, 9)), F.medallion(0.0, 0.2, (B.STAINED_CLAY, 4)), F.tiles(2, (B.STONEBRICK, 0), (B.STONEBRICK, 1)),
        default=(B.STONEBRICK, 1)))
    for x, z in ((cx0 + 2, cz0 + 2), (cx0 + 2, cz1 - 2), (cx1 - 3, cz0 + 2), (cx1 - 3, cz1 - 2)):
        kit.brazier(w, x, P.COURT_Y, z, post=(B.JUNGLE_FENCE, 0), light=(B.GLOWSTONE, 0), base=(B.COBBLE_WALL, 1))
    # the flights down from the gates: the plan's stair cells over red's court side
    for i, k in np.argwhere(R.mask("stair") & (R.X < -40)):
        x, z, y = int(R.X[i, k]), int(R.Z[i, k]), int(R.H[i, k])
        w.set(x, y, z, B.STONEBRICK_STAIRS, stair_data(R.stair.get((x, z), "w")))
        for yy in range(P.VALLEY - 1, y):
            w.set(x, yy, z, *MOSS)
        for yy in range(y + 1, y + 4):
            w.set(x, yy, z, B.AIR)
    # the spawn's chests
    w.chest(cx0 + 2, P.COURT_Y + 1, 0, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:cooked_beef", 32, 0)], 5)
    w.chest(cx0 + 2, P.COURT_Y + 1, 1, [(0, "minecraft:arrow", 32, 0), (1, "minecraft:golden_apple", 4, 0)], 5)


def towers(w, R, L, r):
    for (x0, z0, x1, z1) in P.TOWERS:
        south = z0 > 0
        kit.tower(w, x0, z0, x1, z1, P.TOWER_Y, P.TOWER_TOP - P.TOWER_Y,
                  wall=(MOSS, MOSS, BRICK, CRACK), corner=CHISEL, floor=(B.PLANKS, 3), slit=(B.IRON_BARS, 0),
                  door=B.JUNGLE_DOOR, door_side="n" if south else "s", crown=BRICK, crenel=(B.COBBLE_WALL, 1),
                  light=(B.SEA_LANTERN, 0), rng=r, ladder_on="s")


def bridges(w, R, L, r):
    for i, k in np.argwhere(R.mask("bridge") & (R.X < 0)):
        x, z, y = int(R.X[i, k]), int(R.Z[i, k]), int(R.H[i, k])
        w.set(x, y, z, B.PLANKS, 3)
        for yy in range(y + 1, y + 4):
            w.set(x, yy, z, B.AIR)
        left = R.kind(x - 1, z) != "bridge"
        right = R.kind(x + 1, z) != "bridge"
        if left or right:
            w.set(x, y + 1, z, B.JUNGLE_FENCE, 0)
        if (left or right) and (z % 6 == 0):
            w.set(x, y + 2, z, B.JUNGLE_FENCE, 0)
    # a post at each bridge end
    for bx in P.BRIDGES_X:
        for z in (26, 37, -27, -38):
            for dx in (-2, 2):
                y = int(R.H[bx + dx - R.x_min, z - R.z_min]) if R.inside(bx + dx, z) else 60
                for yy in range(y + 1, y + 4):
                    w.set(bx + dx, yy, z, B.LOG, 3)


def perimeter(w, L, r):
    """A temple wall round the board's edge, mossy and tall, so nobody walks off it: two courses thick."""
    X, Z = w.grid()
    edge = (X <= P.X_MIN + 1) | (X >= P.X_MAX - 1) | (Z <= P.Z_MIN + 1) | (Z >= P.Z_MAX - 1)
    fn = stonework(r)
    for i, k in np.argwhere(edge):
        top = int(L.H[i, k])
        for y in range(top - 2, top + 7):
            w.ids[i, y, k], w.dat[i, y, k] = fn(0, y, 0)
        if (i + k) % 2 == 0:
            w.ids[i, top + 7, k], w.dat[i, top + 7, k] = B.COBBLE_WALL, 1


def vines(w, L, r):
    """Vines on the mossy faces: every exposed vertical face of mossy brick takes a vine now and then, hanging two to
    six blocks."""
    n = 0
    ids = w.ids
    sides = ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1))             # (dx, dz, the vine's data: the face it hangs on)
    cols = np.argwhere((ids[:, 62:84, :] == B.STONEBRICK).any(axis=1))
    for i, k in cols:
        if r.random() > 0.35:
            continue
        for dx, dz, data in sides:
            ni, nk = i + dx, k + dz
            if not (0 <= ni < w.sx and 0 <= nk < w.sz) or r.random() > 0.35:
                continue
            ys = np.nonzero((ids[i, :, k] == B.STONEBRICK) & (ids[ni, :, nk] == 0))[0]
            if len(ys) == 0:
                continue
            top = int(ys.max())
            if top < 62:
                continue
            for y in range(top, max(top - int(r.integers(2, 7)), 61), -1):
                if ids[ni, y, nk] == 0 and ids[i, y, k] == B.STONEBRICK:
                    ids[ni, y, nk], w.dat[ni, y, nk] = B.VINE, {2: 8, 8: 2, 4: 1, 1: 4}[data] if False else (2 if dx == -1 else 8 if dx == 1 else 4 if dz == -1 else 1)
                    n += 1
    return n


def jungle(w, R, L, r):
    """Jungle trees, willows on the stream, bushes, ferns and flowers: kept off every lane and the plan's footprints."""
    lib = trees.library()
    by = trees.kinds(lib)
    X, Z = w.grid()
    red = X < 0
    off = np.zeros(X.shape, bool)
    off |= R.mask("court", "gate", "wall", "tower", "stair", "bridge", "cover", "ladder", "door", "chamber", "rim",
                  "tier1", "tier2", "tier3", "tier4", "tunnel")
    off = ndimage.binary_dilation(off, iterations=1)
    off |= L.water
    ok = red & ~off & (L.slope < 35)
    # lanes: a corridor four wide round each of the plan's routes
    check = __import__("json").load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "renders", "plan-check.json")))
    lane = np.zeros(X.shape, bool)
    for pts in check["paths"].values():
        for x, z in pts:
            if P.X_MIN <= x <= P.X_MAX and P.Z_MIN <= z <= P.Z_MAX:
                lane[x - w.x0, z - w.z0] = True
    lane = ndimage.binary_dilation(lane, iterations=2)
    ok &= ~lane
    kinds = [by["jungle"], by["dense-oak"], by["tiny-oak"], by["willow"]]
    cells = np.argwhere(ok)
    near_water = ndimage.binary_dilation(L.water, iterations=6)
    order = r.permutation(len(cells))
    placed = []
    for j in order:
        if len(placed) >= 160:
            break
        i, k = cells[j]
        x, z = int(X[i, k]), int(Z[i, k])
        wet = near_water[i, k]
        pick = 3 if wet and r.random() < 0.7 else int(r.choice(3, p=[0.12, 0.5, 0.38]))
        t = kinds[pick][int(r.integers(len(kinds[pick])))]
        if any(np.hypot(x - a, z - b) < 0.7 * (t.crown + tt.crown) for a, b, tt in placed):
            continue
        if trees.plant(w, x, z, t, turn=int(r.integers(4))):
            placed.append((x, z, t))
    n = 0
    free = ok & (w.ids[np.arange(w.sx)[:, None], np.minimum(L.H + 1, SY - 1), np.arange(w.sz)[None, :]] == 0)
    for i, k in np.argwhere(free):
        c = r.random()
        y = int(L.H[i, k])
        if w.ids[i, y, k] != B.GRASS:
            continue
        if c < 0.10:
            w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.TALLGRASS, 1 if r.random() < 0.6 else 2
        elif c < 0.12:
            w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.FLOWER, int(r.integers(0, 9))
        elif c < 0.135:
            for dx in (0, 1):
                for dz in (0, 1):
                    if i + dx < w.sx and k + dz < w.sz and w.ids[i + dx, y + 1, k + dz] == 0 and r.random() < 0.8:
                        w.ids[i + dx, y + 1, k + dz], w.dat[i + dx, y + 1, k + dz] = B.LEAVES, 3 | 4
        n += 1
    return len(placed)


def make():
    L = P.land()
    R = P.build()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    t0 = time.time()
    lay_ground(w, L)
    r = rng(P.BOARD, "build")
    tiers(w, R, L, r)
    courts(w, R, L, r)
    n_cover = cover(w, R, L, rng(P.BOARD, "cover"))
    towers(w, R, L, rng(P.BOARD, "towers"))
    bridges(w, R, L, r)
    n_trees = jungle(w, R, L, rng(P.BOARD, "jungle"))
    n_vines = vines(w, L, rng(P.BOARD, "vines"))
    # blue's half: red's mirrored; the ziggurat is its own image (both halves of it were drawn: copy red's over blue's)
    turn_world(w, "mirror_x", red_cols(w), recolour={(B.CARPET, 14): (B.CARPET, 11)})
    perimeter(w, L, rng(P.BOARD, "perimeter"))
    P.objectives().stamp(w)
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose], w.dat[:, 1:, :][loose] = B.STONE, 5
    return w, dict(cover=n_cover, trees=n_trees, vines=n_vines)


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Overgrowth", (0, 100, 0))
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {P.MAX_BUILD}")
