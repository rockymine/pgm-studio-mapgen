"""Generate Hoarfrost Reach from the plan: red's half (z < 0) is built, then mirrored across the band
(orient.turn_world, z' = -1 - z); the wools and monuments are stamped on both halves from their objects; the pack
ice and the open leads between its floes are laid over both halves with no symmetry.

Every headland is its plan floor at its height, exactly, so the gaps the plan measured are the gaps in the world.
Each stands on rock in beds of packed ice, snow, andesite and stone, a block of snow over it; the bedrock course five
under every floor; and below it a root of ice, fluted and drawn out into icicles, no lower than y 50.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np
from scipy import ndimage

import plan as P
from pgmvox import B, World, rng
from pgmvox import build as BLD
from pgmvox import facade as F
from pgmvox import noise, props, trees
from pgmvox import terrain as T
from pgmvox.orient import door as door_data, stair as stair_data, turn_world
from pgmvox.shapes import edge_depth

SY = 128
ROOT_FLOOR = 52


def red_cols(w):
    _, Z = w.grid()
    return Z < 0


def world_arrays(w, R):
    """The plan raster as world-shaped arrays: floor, land, kind."""
    floor = R.H.copy()
    land = ~R.mask("void")
    gb = R.mask("gbridge")                           # the glacier bridge is a deck laid by hand over the shelf
    land[gb] = P.piece_mask(R, "icefall")[gb]
    floor[gb] = P.PIECE["icefall"][4]
    return floor, land


def strata():
    return T.Strata([((B.PACKED_ICE, 0), 3, 3), ((B.SNOW, 0), 2, 2), ((B.STONE, 0), 1.5, 3), ((B.STONE, 5), 1.5, 3),
                     ((B.STAINED_CLAY, 3), 0.5, 1)], seed=21, start=0)


def islands(w, R, beds, offset, r):
    floor, land = world_arrays(w, R)
    red = red_cols(w)
    land_r = land & red
    ed = edge_depth(land_r)
    root = T.root_depth(land_r, cone=3.4, power=0.85, rough=0.4, flutes=3.5, spires=14, seed=11)
    cap = np.maximum(floor - P.FOUNDATION - ROOT_FLOOR, 1)
    root = np.minimum(root, cap)
    fill = T.beds(beds, offset, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.05), ((B.PACKED_ICE, 0), (B.ICE, 0), 0.06)], seed=6)

    def paint(k, x, z):
        c = r.random()
        if k <= 2:
            return (B.STONE, 5) if c < 0.5 else (B.STONE, 0)
        return (B.PACKED_ICE, 0) if c < 0.62 else (B.ICE, 0) if c < 0.78 else (B.SNOW, 0) if c < 0.92 else (B.STONE, 5)
    for h in np.unique(floor[land_r]):
        m = land_r & (floor == h)
        T.lay(w, np.where(m, h, 0), mask=m, top=lambda deg, hh: (B.SNOW, 0), under=(B.SNOW, 0), dirt_depth=1,
              bands=fill, from_y=int(h) - 5)
        T.underside(w, m, int(h) - 5, depth=root, rng=r, jitter=1, paint=paint)
    X, Z = w.grid()
    for i, k in np.argwhere(land_r):                           # the course, and frost on the rim's faces
        x, z, h = int(X[i, k]), int(Z[i, k]), int(floor[i, k])
        if ed[i, k] > 0:
            w.set(x, h - P.FOUNDATION, z, B.BEDROCK)
        else:
            for y in range(h - 5, h - 1):
                if r.random() < 0.15:
                    w.set(x, y, z, B.PACKED_ICE)
    return land_r, floor


def surface(w, R, land_r, floor, r):
    """Frozen puddles, a few stones and gravel on the snow; planked causeways and bridges with their rails."""
    X, Z = w.grid()
    patch = noise.fbm((w.sx, w.sz), 6, 2, seed=33)
    plain = np.isin(R.K, [R.kinds[k] for k in ("skald", "strand", "front", "leg-w", "leg-e", "icefall", "lighthouse", "floe-1", "floe-2", "hall", "glacier")])
    for i, k in np.argwhere(land_r & plain):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(floor[i, k])
        c = r.random()
        if patch[i, k] > 0.35 and c < 0.7:
            w.set(x, h, z, B.PACKED_ICE)
        elif c < 0.03:
            w.set(x, h, z, B.STONE, 5)
        elif c < 0.05:
            w.set(x, h, z, B.GRAVEL)
    decks = ("cause-w", "cause-e", "bridge-w", "bridge-e")
    for i, k in np.argwhere(land_r & np.isin(R.K, [R.kinds[k_] for k_ in decks])):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(floor[i, k])
        w.set(x, h, z, B.PLANKS, 1)
        n = [(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        for nx, nz in n:
            ni, nk = nx - w.x0, nz - w.z0
            if not (0 <= ni < w.sx and 0 <= nk < w.sz) or not land_r[ni, nk]:
                w.set(x, h + 1, z, B.SPRUCE_FENCE, 0)
                break


def flights(w, R, r):
    """The skald's two flights down to the strand, and the Glacier Stair: stairs laid on the plan's cells, the mass
    under each filled with ice, the air over it cleared."""
    X, Z = w.grid()
    for i, k in np.argwhere(R.mask("stair") & (Z < 0)):
        x, z, y = int(X[i, k]), int(Z[i, k]), int(R.H[i, k])
        glacier = x >= 50
        rises = R.stair.get((x, z), "n")
        base = (B.QUARTZ_STAIRS if glacier else B.STONEBRICK_STAIRS)
        for yy in range(y - 6, y):
            if w.id(x, yy, z) in (B.AIR, B.SNOW):
                w.set(x, yy, z, *((B.PACKED_ICE, 0) if glacier else (B.STONEBRICK, 0)))
        w.set(x, y, z, base, stair_data(rises))
        for yy in range(y + 1, y + 5):
            w.set(x, yy, z, B.AIR)
        w.set(x, y - 1, z, *((B.PACKED_ICE, 0) if glacier else (B.STONEBRICK, 0)))
    glacier_bridge(w)


def glacier_bridge(w):
    """The Glacier Bridge: a quartz deck at the hall's floor from the top of the four steps to the landing, seven
    clear across between low walls, on packed-ice piers every six blocks over the shelf. The steps carry on
    from the plan's flight; the span over the 3 blocks of void is the deck alone."""
    g = P.GLACIER
    shelf = P.PIECE["icefall"][4]
    for z in range(-51, -67, -1):
        for x in range(g["x0"], g["x1"] + 1):
            edge = x in (g["x0"], g["x1"])
            w.set(x, P.HALL_Y, z, *((B.QUARTZ, 1) if edge else (B.QUARTZ, 0)))
            w.set(x, P.HALL_Y - 1, z, B.AIR)
            for y in range(P.HALL_Y + 1, P.HALL_Y + 5):
                w.set(x, y, z, B.AIR)
        for x in (g["x0"], g["x1"]):
            w.set(x, P.HALL_Y + 1, z, B.COBBLE_WALL, 0)
        if (z + 51) % 6 == 0 and z >= -62:
            for x in (g["x0"], g["x1"]):
                for y in range(shelf + 1, P.HALL_Y):
                    w.set(x, y, z, B.PACKED_ICE, 0)


def houses(w, R, r):
    ground_at = lambda x, z: int(R.H[x - R.x_min, z - R.z_min])      # noqa: E731
    for key, b in P.houses().items():
        res = BLD.house(w, b["house"], ground_at, r)
        if key == "skald-hall":
            skald_interior(w, b, res)
        else:
            x0, z0, x1, z1 = b["spec"]["rect"]
            for dx in range(x0 + 1, x1):                              # nets and racks beside the shed
                w.set(dx, b["floor"] + 1, z1 + 2, B.FENCE, 0) if dx % 2 == 0 else None


def skald_interior(w, b, res):
    """The hall: a bench along the north wall, a hearth at each end, lanterns. The floor between the doorway and the
    spawn is left clear: the long fenced tables the first build set across it made every spawn walk round them."""
    x0, z0, x1, z1 = b["spec"]["rect"]
    f = b["floor"]
    cz = (z0 + z1) // 2
    for x in range(x0 + 4, x1 - 3):
        w.set(x, f + 1, z0 + 1, B.WOOD_SLAB, 1)                  # a bench of half slabs, stepped over, not walked round
    for x, z in ((x0 + 1, cz), (x1 - 1, cz)):
        for dy in range(1, 4):
            w.set(x, f + dy, z, B.COBBLE, 0)
        w.set(x, f + 1, z, B.FURNACE, 5 if x < 0 else 4)
    for x in range(x0 + 4, x1 - 3, 4):
        w.set(x, f + 5, cz, B.GLOWSTONE, 0)
    w.chest(x0 + 2, f + 1, z0 + 1, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:cooked_beef", 32, 0)], 3)
    w.chest(x1 - 2, f + 1, z0 + 1, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:arrow", 32, 0)], 3)


def monuments_lawn(w, r):
    """The monument slots on the skald's lawn: a stone ring round each, lamps, so a player finds them."""
    for sx in (-16, 16):
        sz = -80
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if max(abs(dx), abs(dz)) == 2:
                    w.set(sx + dx, 75, sz + dz, B.STONEBRICK, 3 if (dx + dz) % 2 else 0)
        props.brazier(w, sx - 3, 75, sz - 3, post=(B.SPRUCE_FENCE, 0), base=(B.COBBLE_WALL, 0))
        props.brazier(w, sx + 3, 75, sz - 3, post=(B.SPRUCE_FENCE, 0), base=(B.COBBLE_WALL, 0))


def strand(w, R, r):
    """The strand: lamps, cairns, a ring of packed ice round the pond; the breakwater's cover (crates and walls)."""
    cx, cz, rad = P.HOLE
    for a in range(0, 360, 12):
        x, z = int(round(cx + (rad + 1.2) * np.cos(np.radians(a)))), int(round(cz + (rad + 1.2) * np.sin(np.radians(a))))
        if w.id(x, 72, z) not in (B.AIR,):
            w.set(x, 72, z, B.PACKED_ICE, 0)
            if a % 36 == 0:
                w.set(x, 73, z, B.SNOW, 0)
    for x, z in ((-36, -60), (-12, -60), (12, -60), (36, -60), (-36, -46), (-24, -46), (24, -46), (36, -46)):
        props.lamp(w, x, 72, z, height=2, post=(B.SPRUCE_FENCE, 0), light=(B.SEA_LANTERN, 0), cap=None)
    for x, z in ((-20, -50), (22, -57), (-6, -46), (8, -60)):
        props.rubble(w, x, 72, z, r, r=1.5, blocks=((B.COBBLE, 0), (B.STONE, 5), (B.SNOW, 0)))
    # cover on the breakwater: small crates (2 x 2 x 2) and larger walls (6 x 1 x 3)
    for x in (-26, -8, 10, 26):
        for dx in (0, 1):
            for dz in (0, 1):
                for dy in (1, 2):
                    w.set(x + dx, 70 + dy, -33 + dz, B.PLANKS, 1)
        w.set(x, 73, -33, B.SNOW_LAYER, 0)
    for x0, z0 in ((-35, -24), (31, -24)):
        for dx in range(6 if x0 < 0 else 5):
            for dy in (1, 2, 3):
                w.set(x0 + dx if x0 < 0 else x0 + dx, 70 + dy, z0, B.STONEBRICK, 0 if dy < 3 else 3)
    # a rail along the breakwater's outer edge
    BLD.parapet(w, {(x, -36) for x in range(-36, 37)} | {(x, -28) for x in range(-36, 37)}, 71, (B.SPRUCE_FENCE, 0))


def lighthouse(w, R, r):
    """The tower: striped walls, a ladder up with a hatch in every floor, a glazed room under a lantern roof, a
    gallery round the room; the doorway on the east."""
    x0, z0, x1, z1 = P.TOWER
    base, top = 72, P.ROOM_Y
    lx, lz = P.TOWER_LADDER
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            for y in range(base - 4, base + 1):
                w.set(x, y, z, B.STONEBRICK, 0)
            for y in range(base + 1, top + 8):
                t = y - base
                if edge:
                    if y <= top:
                        stripe = (t // 4) % 2 == 0
                        blk = (B.STAINED_CLAY, 14) if stripe else (B.STAINED_CLAY, 0)
                        if corner:
                            blk = (B.STONEBRICK, 0)
                        elif t % 6 == 3 and ((x + z) % 2 == 0) and not stripe is None and y < top - 1:
                            blk = (B.IRON_BARS, 0)
                        w.set(x, y, z, *blk)
                    elif y <= top + 5:
                        w.set(x, y, z, *((B.STONEBRICK, 0) if corner else (B.STAINED_GLASS, 3)))
                    else:
                        w.set(x, y, z, B.AIR)
                else:
                    w.set(x, y, z, B.AIR)
            if not edge:
                for t in range(5, top - base, 5):
                    w.set(x, base + t, z, B.PLANKS, 1)
                w.set(x, top, z, B.PLANKS, 1)                    # the room's floor, at ROOM_Y
    for t in range(5, top - base, 5):
        w.set(lx, base + t, lz, B.AIR)                            # a hatch over the ladder
    w.set(lx, top, lz, B.AIR)
    for y in range(base + 1, top + 2):
        w.set(lx, y, lz, B.LADDER, 2)                            # on the south wall: facing north
    # the roof: quartz over the room, a lantern at its heart
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            edge = x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1)
            w.set(x, top + 6, z, *((B.QUARTZ, 0) if not edge else (B.SLAB, 7)))
    cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
    for y in range(top + 7, top + 10):
        w.set(cx, y, cz, B.GLASS if y < top + 9 else B.SEA_LANTERN, 0)
    for dx in (-1, 1):
        for dz in (-1, 1):
            w.set(cx + dx, top + 7, cz + dz, B.QUARTZ_STAIRS, 0)
    w.set(cx, top + 7, cz, B.SEA_LANTERN, 0)
    # the gallery: a ring of slabs at the room's floor, a rail of bars
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1, z1 + 2):
            if x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1):
                w.set(x, top, z, B.SLAB, 7)
                w.set(x, top + 1, z, B.IRON_BARS, 0)
    # the door and a short flight of steps out of it
    dx_, dz_ = P.TOWER_DOOR
    w.set(dx_, 73, dz_, B.SPRUCE_DOOR, door_data("e"))
    w.set(dx_, 74, dz_, B.SPRUCE_DOOR, door_data("e", upper=True))
    # the wool's pedestal in the room
    wx, wy, wz = (x0 + x1) // 2, top + 1, (z0 + z1) // 2
    w.set(wx, top, wz, B.QUARTZ, 1)
    props.wool_chests(w, (x0 + 1, z0 + 1, x1 - 1, z1 - 1), top, "e")     # the corners: clear of the ladder, wool and door


def ice_hall(w, R, r):
    """The Ice Hall: packed-ice walls with blue glass bands, a floor of tiled blue and white clay, sea lanterns in
    a packed-ice ceiling, a doorway on the south toward the landing."""
    x0, z0, x1, z1 = P.HALL_BOX
    f = P.HALL_Y
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            w.set(x, f, z, *((B.PACKED_ICE, 0) if edge else ((B.STAINED_CLAY, 3) if (x + z) % 2 == 0 else (B.STAINED_CLAY, 0))))
            for y in range(f + 1, f + 8):
                if edge:
                    band = y in (f + 3, f + 4) and (x + z) % 4 in (1, 2)
                    w.set(x, y, z, *((B.STAINED_GLASS, 3) if band else (B.PACKED_ICE, 0)))
                else:
                    w.set(x, y, z, B.AIR)
            w.set(x, f + 8, z, *((B.SEA_LANTERN, 0) if (not edge and x % 4 == 0 and z % 4 == 0) else (B.PACKED_ICE, 0)))
    dx = (x0 + x1) // 2
    for ddx in (-1, 0, 1):
        for y in (f + 1, f + 2, f + 3):
            w.set(dx + ddx, y, z1, B.AIR)
    props.wool_chests(w, (x0 + 1, z0 + 1, x1 - 1, z1 - 1), f, "s")        # the corners: clear of the wool and the doorway
    # pillars of ice, two on each side, for cover inside
    for px, pz in ((x0 + 4, z0 + 4), (x1 - 4, z0 + 4), (x0 + 4, z1 - 4), (x1 - 4, z1 - 4)):
        for y in range(f + 1, f + 8):
            w.set(px, y, pz, *((B.PACKED_ICE, 0) if y < f + 7 else (B.SEA_LANTERN, 0)))


def forest(w, R, land_r, floor, r):
    """Spruces on the skald's wings, the strand's far corners, the lighthouse stack and the icefall shelf's flanks,
    crowns apart; snow on every crown."""
    lib = trees.library()
    by = trees.kinds(lib)
    X, Z = w.grid()
    zone = np.zeros(X.shape, bool)
    for key, box in (("skald", None),):
        zone |= (R.K == R.kinds["skald"]) & (Z < 0)
    keep_off = np.zeros(X.shape, bool)
    hx0, hz0, hx1, hz1 = P.HALL_SKALD
    keep_off |= (X >= hx0 - 4) & (X <= hx1 + 4) & (Z >= hz0 - 4) & (Z <= P.HALL_SKALD[3] + 14)
    keep_off |= (X >= -12) & (X <= 12) & (Z >= -72)
    zone &= ~keep_off
    inner = ndimage.binary_erosion(zone, iterations=3)
    zone &= inner
    for key in ("lighthouse", "icefall"):
        zone |= ndimage.binary_erosion((R.K == R.kinds[key]) & (Z < 0), iterations=2)
    zone[(X >= -84) & (X <= -66) & (Z >= -60) & (Z <= -50)] = False        # the tower's foot and the door
    zone[(X >= 56) & (X <= 68)] = False                                       # the stair's foot
    placed = []
    n = trees.scatter(w, zone, by_kind=dict(tall=by["tall-spruce"], tiny=by["tiny-spruce"], pine=by["large-pine"]),
                      weights={"tall": 0.3, "tiny": 0.5, "pine": 0.2}, rng=r, spacing=0.9, tries=2500, planted=placed) \
        if False else None
    kinds = [by["tall-spruce"], by["tiny-spruce"], by["large-pine"]]
    cells = np.argwhere(zone)
    order = r.permutation(len(cells))
    count = 0
    for j in order:
        if count >= 70:
            break
        i, k = cells[j]
        x, z = int(X[i, k]), int(Z[i, k])
        if any(np.hypot(x - a, z - b) < 5.5 for a, b, _ in placed):
            continue
        kind = kinds[int(r.choice(3, p=[0.3, 0.5, 0.2]))]
        t = kind[int(r.integers(len(kind)))]
        if trees.plant(w, x, z, t, turn=int(r.integers(4))):
            placed.append((x, z, t))
            count += 1
    # snow on the crowns
    ids = w.ids
    for x, z, t in placed:
        for dx in range(-t.crown, t.crown + 1):
            for dz in range(-t.crown, t.crown + 1):
                i, k = x + dx - w.x0, z + dz - w.z0
                if not (0 <= i < w.sx and 0 <= k < w.sz):
                    continue
                col = ids[i, :, k]
                ys = np.nonzero(np.isin(col, (B.LEAVES, B.LEAVES2)))[0]
                if len(ys):
                    y = int(ys.max())
                    if col[y + 1] == 0 and r.random() < 0.7:
                        w.set(w.x0 + i, y + 1, w.z0 + k, B.SNOW_LAYER, 0)
    return count


def build_zone_marks(w, R):
    """Block 36 at y 0 under every column a player may build in: land and build zones, both halves."""
    cols = ~R.mask("void") | P.zone_mask(R)
    w.ids[:, 0, :][cols] = 36
    return int(cols.sum())


def make():
    R = P.build()
    O = P.objectives()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    t0 = time.time()
    r = rng(P.BOARD, "rock")
    beds = strata()
    offset = T.bed_offset((w.sx, w.sz), dip=(0.0, 0.0), fold=3, cell=14, seed=13)
    land_r, floor = islands(w, R, beds, offset, r)
    surface(w, R, land_r, floor, rng(P.BOARD, "surface"))
    flights(w, R, rng(P.BOARD, "flights"))
    houses(w, R, rng(P.BOARD, "houses"))
    monuments_lawn(w, rng(P.BOARD, "lawn"))
    strand(w, R, rng(P.BOARD, "strand"))
    lighthouse(w, R, rng(P.BOARD, "lighthouse"))
    ice_hall(w, R, rng(P.BOARD, "hall"))
    n_trees = forest(w, R, land_r, floor, rng(P.BOARD, "forest"))
    n_marked = build_zone_marks(w, R)
    turn_world(w, "mirror_z", red_cols(w), recolour={(B.CARPET, 14): (B.CARPET, 11), (B.STAINED_CLAY, 14): (B.STAINED_CLAY, 11)})
    O.stamp(w)
    before = int((w.ids == B.PACKED_ICE).sum())
    T.cloud_deck(w, P.SEA_Y, seed=50, cell=18, puff=4, breaks=-0.08, materials=((B.PACKED_ICE, 0), (B.SNOW, 0)))
    n_sea = int((w.ids == B.PACKED_ICE).sum()) - before
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose], w.dat[:, 1:, :][loose] = B.STONE, 5
    w.biome[:, :] = 12
    return w, dict(trees=n_trees, marked=n_marked, sea=n_sea)


if __name__ == "__main__":
    t0 = time.time()
    w, n = make()
    w.save(sys.argv[1], "Hoarfrost Reach", P.OBSERVER_AT)
    print(f"generated in {time.time() - t0:.0f}s: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}")
