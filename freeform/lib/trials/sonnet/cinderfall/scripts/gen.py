"""Generate Cinderfall from the plan: red's half (x < 0) is built, then turned half a circle onto blue's
(orient.turn_world); the cores are stamped on both halves from their objects.

The ground is the plan's heightfield, exactly, so the walks the plan measured are the walks in the world. Rock in
dark beds that follow the surface, a top painted by slope (ash flats, andesite on the slopes, bare stone on the
cliffs), netherrack and obsidian about the lava lake, the vent tube carved under the plain, the roads laid and
the buildings, the dead wood and the dressing on top.

    python3 gen.py <build-dir>
"""
import sys
import time

import numpy as np

import plan as P
from pgmvox import B, World, rng
from pgmvox import props, shapes, trees
from pgmvox import build as BLD
from pgmvox import forms, route
from pgmvox import terrain as T
from pgmvox import under as U
from pgmvox.noise import fbm
from pgmvox.orient import turn_world

SY = 128
PALETTE_ASH = ((B.STAINED_CLAY, 7), (B.GRAVEL, 0), (B.STAINED_CLAY, 8), (B.STONE, 5))


def red_cols(w):
    X, _ = w.grid()
    return X < 0


# The rock is bedded like a mesa's: bands of burnt clay, orange, brown, red, yellow and white between the black, with
# andesite, granite and coarse dirt among them, so a cliff reads as strata and not as a grey wall.
BEDS = ((B.STAINED_CLAY, 15), 1.5, 3), ((B.STAINED_CLAY, 14), 1.2, 2), ((B.STAINED_CLAY, 1), 1.2, 2), \
    ((B.STAINED_CLAY, 12), 1.5, 3), ((B.HARDENED_CLAY, 0), 1.0, 2), ((B.STONE, 5), 1.5, 3), ((B.STONE, 1), 1.0, 2), \
    ((B.STAINED_CLAY, 4), 0.5, 1), ((B.STAINED_CLAY, 0), 0.4, 1), ((B.STAINED_CLAY, 7), 0.9, 2), ((B.DIRT, 1), 0.5, 1), \
    ((B.COAL_BLOCK, 0), 0.4, 1)
SHORE = ((B.NETHERRACK, 0), (B.STONE, 1), (B.STAINED_CLAY, 14), (B.OBSIDIAN, 0), (B.STAINED_CLAY, 15))


def pick(c, table):
    """A block from (weight, block) rows by a uniform draw c."""
    t = 0.0
    for wt, blk in table:
        t += wt
        if c < t:
            return blk
    return table[-1][1]


GROUND_ASH = ((0.50, (B.STAINED_CLAY, 7)), (0.18, (B.STAINED_CLAY, 15)), (0.10, (B.GRAVEL, 0)), (0.10, (B.STONE, 5)),
              (0.12, (B.STAINED_CLAY, 8)))
GROUND_RED = ((0.38, (B.STAINED_CLAY, 14)), (0.22, (B.STAINED_CLAY, 1)), (0.14, (B.HARDENED_CLAY, 0)),
              (0.10, (B.NETHERRACK, 0)), (0.10, (B.STONE, 1)), (0.06, (B.SAND, 1)))
GROUND_BROWN = ((0.36, (B.STAINED_CLAY, 12)), (0.24, (B.DIRT, 1)), (0.14, (B.STONE, 1)), (0.10, (B.STONE, 5)),
                (0.10, (B.STAINED_CLAY, 4)), (0.06, (B.STAINED_CLAY, 1)))


def lay_ground(w, L):
    """Rock, soil and the painted top over red's land; the underside cleared below each column's bottom."""
    X, Z = w.grid()
    H = L.H.copy()
    red = red_cols(w) & L.land
    rock = T.Strata(list(BEDS), length=70, seed=5, start=-300)
    offset = T.bed_offset((w.sx, w.sz), dip=(0.02, 0.05), fold=2.2, cell=26, seed=8)
    bands = T.beds(rock, offset, flecks=[((B.STONE, 5), (B.COBBLE, 0), 0.05), ((B.STONE, 0), (B.GRAVEL, 0), 0.02)],
                   seed=3)
    deg = T.lay(w, H, red, top=T.by_angle([(22, (B.STAINED_CLAY, 7)), (45, (B.STONE, 5)), (90, (B.STONE, 0))]),
                bands=bands, under=(B.STAINED_CLAY, 7), from_y=3, soil=((20, 2), (30, 1)))
    r = rng(P.BOARD, "ground")
    sh = (w.sx, w.sz)
    patch, cell = fbm(sh, 7, 2, seed=61), r.random(sh)
    zone = fbm(sh, 22, 2, seed=77)
    rav = L.rav
    for i, k in np.argwhere(red):
        top = int(H[i, k])
        w.ids[i, :max(0, int(L.bottom[i, k])), k] = 0
        w.dat[i, :max(0, int(L.bottom[i, k])), k] = 0
        if L.lava[i, k] or L.pit[i, k]:
            continue
        a = int(deg[i, k])
        c, pv, zn = cell[i, k], patch[i, k], zone[i, k]
        shore = rav["c1"][i, k] - 0.5 <= rav["c"][i, k] < rav["c2"][i, k] + 0.5 and L.land[i, k]
        if shore:
            w.ids[i, top, k], w.dat[i, top, k] = pick(c, tuple((1 / len(SHORE), b) for b in SHORE))
            continue
        if a > 45:
            w.ids[i, top, k], w.dat[i, top, k] = bands(i, k, [top])[0]    # the beds show on the faces, to the lip
            continue
        if a <= 22:
            if pv > 0.25:
                blk = (B.STAINED_CLAY, 15) if c < 0.7 else (B.STAINED_CLAY, 12) if c < 0.9 else (B.NETHERRACK, 0)
            elif zn > 0.15:
                blk = pick(c, GROUND_RED)
            elif zn < -0.15:
                blk = pick(c, GROUND_BROWN)
            elif pv < -0.25:
                blk = (B.STONE, 5) if c < 0.5 else (B.STONE, 1) if c < 0.8 else (B.DIRT, 1)
            else:
                blk = pick(c, GROUND_ASH)
            w.ids[i, top, k], w.dat[i, top, k] = blk
        else:
            if c < 0.55:
                w.ids[i, top, k], w.dat[i, top, k] = bands(i, k, [top])[0]   # a bed shows through the slope
                continue
            blk = (B.STONE, 5) if c < 0.7 else (B.STONE, 1) if c < 0.8 else (B.COBBLE, 0) if c < 0.9 else (B.STAINED_CLAY, 14)
            w.ids[i, top, k], w.dat[i, top, k] = blk
        # cracks that glow, where the ground is burnt
        if 14 < np.hypot(X[i, k] + 0.5, Z[i, k] + 0.5) <= 30 and a <= 40 and pv > 0.4:
            w.ids[i, top, k], w.dat[i, top, k] = (B.NETHERRACK, 0)
            if c < 0.05:
                w.ids[i, top, k], w.dat[i, top, k] = (B.GLOWSTONE, 0)
    w.biome[:, :] = 2
    return deg


def lava_lake(w, L):
    """The ravine's lava, bed to surface over an obsidian floor, and the pit under the core, lined in obsidian."""
    X, Z = w.grid()
    for i, k in np.argwhere(L.lava & L.land):
        top = int(L.H[i, k])
        w.ids[i, top, k], w.dat[i, top, k] = B.OBSIDIAN, 0
        w.ids[i, top + 1:P.LAVA_Y + 1, k] = B.LAVA
        w.dat[i, top + 1:P.LAVA_Y + 1, k] = 0
    cx, cz = P.CORE_AT
    for i, k in np.argwhere(L.pit & (X < 0)):
        w.ids[i, P.PIT_BED, k], w.dat[i, P.PIT_BED, k] = B.OBSIDIAN, 0
        w.ids[i, P.PIT_BED + 1:P.PIT_LAVA_Y + 1, k] = B.LAVA
        w.dat[i, P.PIT_BED + 1:P.PIT_LAVA_Y + 1, k] = 0
    for x in range(cx - 6, cx + 7):                                      # the pit's lining: a ring of obsidian, solid to the rim
        for z in range(cz - 6, cz + 7):
            d = np.hypot(x - cx, z - cz)
            if P.PIT_R < d <= P.PIT_R + 1.3:
                for y in range(P.PIT_BED, P.PLINTH_Y):
                    w.set(x, y, z, B.OBSIDIAN, 0)


def tube(w, L):
    """The vent tube under the plain: carved with the library's tunnel, finished as cave."""
    ground = L.H
    red = lambda x, y, z: x >= 0                                  # noqa: E731  (blue's half is the turn's)
    n, floor = U.tunnel(w, P.VENT, ground=None, keep=red)
    box = (-62, -18, -4, 20, 44, 62)
    U.dress_cave(w, box, rng(P.BOARD, "cave"), ground=lambda x, z: int(L.H[x - w.x0, z - w.z0]) if L.land[x - w.x0, z - w.z0] else None,
                 keep=red, floors=((B.GRAVEL, 0), (B.STONE, 5), (B.STAINED_CLAY, 15), (B.COBBLE, 0)),
                 mushrooms=0.0, stalactites=0.06, ores=260, stalagmites=500,
                 ore_blocks=((B.COAL_ORE, 0.6), (B.IRON_ORE, 0.25), (B.REDSTONE_ORE, 0.15)))
    # lights in the walls: a glowstone every few blocks along the tube, set in the rock beside the floor
    r = rng(P.BOARD, "tubelights")
    for x, fy, z, rad in P.VENT[1:-1]:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            bx, bz = x + dx * int(rad + 1), z + dz * int(rad + 1)
            for y in range(fy + 1, fy + 4):
                if w.id(bx, y, bz) in (B.STONE, B.STAINED_CLAY, B.COBBLE, B.COAL_BLOCK) and w.id(bx - dx, y, bz - dz) == B.AIR:
                    w.set(bx, y, bz, B.GLOWSTONE, 0)
                    break
            else:
                continue
            break
    return n


def roads(w, L):
    """The roads and tracks laid on the graded ground; red's half only (the turn copies them)."""
    X, Z = w.grid()
    H = np.where(L.land, L.H, 0)
    for rt in L.routes:
        surf = ((B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 12), (B.COBBLE, 0), (B.GRAVEL, 0)) if rt["kind"] == "road" else \
               ((B.STAINED_CLAY, 12), (B.GRAVEL, 0), (B.HARDENED_CLAY, 0), (B.STONE, 5))
        wts = (0.45, 0.25, 0.2, 0.1) if rt["kind"] == "road" else (0.4, 0.3, 0.2, 0.1)
        keep = L.lava | (X >= 0)
        route.pave(w, H, X, Z, rt["pts"] if False else [tuple(p) for p in rt["line"]], width=rt["width"], surface=surf,
                   weights=wts, water=None, clear=3, seed=len(rt["name"]), keep=keep)
        # steps where the road climbs a block at once
        route.steps(w, H, X, Z, [tuple(p) for p in rt["line"]], block=B.COBBLE_STAIRS, width=min(rt["width"], 3)) \
            if rt["kind"] == "road" and rt["grade"] > 0.4 else None


def clear_pits(w, L):
    """The funnels: rubble steps of andesite and cobble, the tube's mouth black with soot."""
    r = rng(P.BOARD, "funnel")
    for m in L.funnels:
        for i, k in np.argwhere(m & (np.arange(w.sx)[:, None] + w.x0 < 0)):
            top = int(L.H[i, k])
            c = r.random()
            w.ids[i, top, k], w.dat[i, top, k] = ((B.STAINED_CLAY, 15) if c < 0.4 else (B.STONE, 5) if c < 0.7
                                                  else (B.COBBLE, 0))


def houses(w, L):
    """Red's buildings from the plan: a level site, the library's house, then parapets, stacks and the yard."""
    r = rng(P.BOARD, "houses")
    ground_at = lambda x, z: P.at(L, x, z)                          # noqa: E731
    out = {}
    for key, b in P.houses().items():
        if key == "beacon":
            continue
        cells = b["cells"]
        BLD.site(w, cells, b["floor"], ground_at, margin=2, fill=(B.STONE, 5), top=(B.STAINED_CLAY, 7),
                 under=(B.STAINED_CLAY, 7), clear=14)
        res = BLD.house(w, b["house"], ground_at, r)
        out[key] = res
        st = b["spec"]["style"]
        if st in ("foundry", "hold"):
            BLD.parapet(w, cells, res["eave"] + 1, (B.STONEBRICK, 0) if st == "foundry" else (B.NETHER_BRICK, 0),
                        crenel=(B.COBBLE_WALL, 0) if st == "hold" else None)
        if st == "foundry":
            xs = [c[0] for c in cells]; zs = [c[1] for c in cells]
            sx, sz = min(xs) + 2, max(zs) - 2                       # a stack at one corner, four courses over the roof
            for y in range(res["eave"] + 1, res["eave"] + 8):
                for dx in (0, 1):
                    for dz in (0, 1):
                        w.set(sx + dx, y, sz + dz, B.STONEBRICK, 0)
            w.set(sx, res["eave"] + 8, sz, B.NETHER_FENCE, 0)
            w.set(sx + 1, res["eave"] + 8, sz, B.GLOWSTONE, 0)
    return out


def stack_rock(y, b):
    """The beds of a stack, by height: the same colours the cliffs wear, tilted a little by the bulge."""
    seq = ((B.STAINED_CLAY, 15), (B.STAINED_CLAY, 14), (B.STAINED_CLAY, 1), (B.STAINED_CLAY, 12), (B.HARDENED_CLAY, 0),
           (B.STONE, 5), (B.STAINED_CLAY, 4), (B.STAINED_CLAY, 12), (B.STONE, 1), (B.STAINED_CLAY, 7))
    return seq[(y + int(3 * b)) // 3 % len(seq)]


def stacks(w, L):
    """Rock stacks standing in the ravine and on its shore, and the keystone in mid-channel: rings tapering up from
    the bed with a ledge every seven courses, the beds running round them, a cap of andesite to stand on."""
    r = rng(P.BOARD, "stacks")
    through = (B.AIR, B.LAVA, B.LAVA_FLOW)
    n = 0
    items = [(x, z, rad, top) for x, z, rad, top, _ in P.STACKS] + [(-1, -1, 4.6, P.BRIDGE_Y)]
    for j, (x, z, rad, top) in enumerate(items):
        ground = int(L.H[x - w.x0, z - w.z0])
        n += forms.tower(w, x, z, ground - 2, top, rad, stack_rock, r, taper=(1.15, 0.72), ledge_every=7, ledge=0.7,
                         bulge=1.0, cell=4, seed=90 + j, through=through, crown=(B.STONE, 5), crown_r=0.8, vines=0)
    return n


def bridge(w, L):
    """The Slag Bridge: a four-wide deck of nether brick between obsidian edges from the rim pad to the keystone, level
    with the plain, on two obsidian piers; a brazier at the head. Red's span only: the half turn lays blue's."""
    y = P.BRIDGE_Y
    x0, x1 = P.BRIDGE_X[0], -1
    z0, z1 = P.BRIDGE_Z
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = z in (z0, z1)
            for yy in range(y + 1, y + 5):
                if w.id(x, yy, z) != B.AIR:
                    w.set(x, yy, z, B.AIR)
            w.set(x, y, z, *((B.OBSIDIAN, 0) if edge else (B.NETHER_BRICK, 0)))
            if w.id(x, y - 1, z) == B.AIR or w.id(x, y - 1, z) == B.LAVA:
                w.set(x, y - 1, z, *((B.OBSIDIAN, 0) if edge else (B.STONEBRICK, 0)))
    for px in (x0 + 4, x0 + 8):
        for pz in (z0 + 1, z0 + 2):
            yy = y - 2
            while yy > 2 and w.id(px, yy, pz) in (B.AIR, B.LAVA, B.LAVA_FLOW):
                w.set(px, yy, pz, B.OBSIDIAN, 0)
                yy -= 1
    props.brazier(w, x0 + 1, y, z0 - 1)
    props.brazier(w, x0 + 1, y, z1 + 1)


def beacon(w, L):
    x0, z0, x1, z1 = P.BEACON
    forms.masonry_tower(w, x0, z0, x1, z1, P.BEACON_Y, 12, rng=rng(P.BOARD, "beacon"), door_side="s", ladder_on="n")


def plinth(w, L):
    """The core's footing: rings of obsidian, netherrack, black clay and polished andesite round the foot, the
    four braziers' lights flush with the ground (cover keeps four blocks off the casing, so nothing stands up)."""
    cx, cz = P.CORE_AT
    for x in range(cx - 8, cx + 9):
        for z in range(cz - 8, cz + 9):
            d = np.hypot(x - cx, z - cz)
            if d > 7.5:
                continue
            blk = (B.OBSIDIAN, 0) if d <= 2.8 else (B.NETHERRACK, 0) if d <= 4.4 else (B.STAINED_CLAY, 15) if d <= 5.8 \
                else (B.STONE, 6)
            if abs(x - cx) <= 1 and abs(abs(z - cz) - 6) <= 0 or abs(z - cz) <= 1 and abs(abs(x - cx) - 6) <= 0:
                blk = (B.GLOWSTONE, 0)
            if d <= P.PIT_R:                                   # the pit: lava to three under the rim, air over it
                for y in range(P.PIT_LAVA_Y + 1, P.PLINTH_Y + 4):
                    w.set(x, y, z, B.AIR)
                continue
            w.set(x, P.PLINTH_Y, z, *blk)
            for y in range(P.PLINTH_Y + 1, P.PLINTH_Y + 4):
                w.set(x, y, z, B.AIR)


def wood(w, L):
    """The Charred Wood: dead trees apart, dead bushes, stumps and a fallen log or two."""
    r = rng(P.BOARD, "wood")
    X, Z = w.grid()
    red = (X < 0) & L.wood
    road = np.zeros(X.shape, bool)
    for m in L.road_on.values():
        road |= m
    from scipy import ndimage
    road = ndimage.binary_dilation(road, iterations=2)
    cx, cz = P.CORE_AT
    ok = red & ~road & (np.hypot(X - cx, Z - cz) > 12) & (L.slope < 30)
    pts = shapes.scatter_points(ok, 70, 3.6, r, X, Z)
    for x, z in pts:
        y = int(L.H[x - w.x0, z - w.z0])
        trees.dead_tree(w, x, y, z, r, int(r.integers(5, 10)))
    n = 0
    for x, z in shapes.scatter_points(ok, 60, 2.5, r, X, Z, taken=pts):
        y = int(L.H[x - w.x0, z - w.z0])
        if r.random() < 0.6:
            w.set(x, y + 1, z, B.DEADBUSH, 0)
        else:
            w.set(x, y + 1, z, B.LOG2, 1)                          # a stump
            if r.random() < 0.4:
                w.set(x, y + 2, z, B.LOG2, 1)
        n += 1
    return len(pts), n


def dressing(w, L):
    """Everything else: dead bushes and rubble on the ash, braziers at the road's bends, lamps along the roads,
    a forge yard, the iron outcrop, slag cones with ore in them."""
    r = rng(P.BOARD, "dress")
    X, Z = w.grid()
    cx, cz = P.CORE_AT
    road = np.zeros(X.shape, bool)
    for m in L.road_on.values():
        road |= m
    from scipy import ndimage
    near_road = ndimage.binary_dilation(road, iterations=2)
    house_cells = set()
    for b in P.houses().values():
        house_cells |= {(x, z) for x, z in b["cells"]}
    hmask = np.zeros(X.shape, bool)
    for x, z in house_cells:
        hmask[x - w.x0, z - w.z0] = True
    hmask = ndimage.binary_dilation(hmask, iterations=3)
    free = (X < 0) & L.land & ~near_road & ~hmask & ~L.lava & ~L.wood & (np.hypot(X - cx, Z - cz) > 12) & (L.slope < 35)
    for x, z in shapes.scatter_points(free, 40, 5, r, X, Z):
        y = int(L.H[x - w.x0, z - w.z0])
        props.rubble(w, x, y, z, r, r=float(r.uniform(1.2, 2.4)), supported=False)
    for x, z in shapes.scatter_points(free, 80, 3, r, X, Z):
        y = int(L.H[x - w.x0, z - w.z0])
        if w.id(x, y + 1, z) == B.AIR:
            w.set(x, y + 1, z, B.DEADBUSH, 0)
    # lamps along the roads, braziers at the plinth's door
    for rt in L.routes:
        if rt["kind"] == "road":
            H = np.where(L.land, L.H, 0)
            props.lamps(w, [tuple(p) for p in rt["line"]], H, X, Z, every=14, side=3.2)
    # the foundry yard: an anvil, furnaces, a crucible and a stack of iron by the smelter
    sm = P.houses()["smelter"]
    x1 = max(c[0] for c in sm["cells"]) + 2
    yy = P.at(L, x1, 12)
    w.set(x1, yy + 1, 11, B.ANVIL, 0)
    w.set(x1, yy + 1, 13, B.CAULDRON, 0)
    for dz in (9, 15):
        w.set(x1 + 1, yy + 1, dz, B.FURNACE, 5)
    for k in range(3):
        w.set(x1 + 2, yy + 1 + k, 12, B.IRON_BLOCK if k < 2 else B.COAL_BLOCK, 0)
    # the iron outcrop behind the hold (minable inside the spawn area)
    for dx, dz in ((0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (1, 2)):
        x, z = -77 + dx, 24 + dz
        y = P.at(L, x, z)
        w.set(x, y, z, B.IRON_ORE, 0)
        w.set(x, y + 1, z, B.IRON_ORE, 0) if (dx + dz) % 2 == 0 else None
    # the hold's yard: a lamp at each step of its terrace
    for dz in (7, 17):
        yy = P.at(L, -65, dz)
        props.brazier(w, -65, yy, dz)


def hold_interior(w, L):
    """The Ember Hold's hall: a carpet runner, glowstone in the ceiling, chests of the spawn kit."""
    b = P.houses()["hold"]
    f = b["floor"]
    xs = [c[0] for c in b["cells"]]; zs = [c[1] for c in b["cells"]]
    for z in range(min(zs) + 2, max(zs) - 1):
        for x in range(min(xs) + 2, max(xs) - 1):
            if abs(z - (min(zs) + max(zs)) // 2) <= 1:
                w.set(x, f + 1, z, B.CARPET, 14)
    cx, cz = (min(xs) + max(xs)) // 2, (min(zs) + max(zs)) // 2
    for dx, dz in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        w.set(cx + dx, f + 4, cz + dz, B.GLOWSTONE, 0)
    w.chest(min(xs) + 2, f + 1, min(zs) + 2, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:cooked_beef", 32, 0)], 5)
    w.chest(min(xs) + 2, f + 1, max(zs) - 2, [(0, "minecraft:golden_apple", 4, 0), (1, "minecraft:arrow", 32, 0)], 5)


def make():
    L = P.land()
    w = World(P.X_MIN, P.Z_MIN, P.X_MAX - P.X_MIN + 1, P.Z_MAX - P.Z_MIN + 1, sy=SY)
    t0 = time.time()
    lay_ground(w, L)
    lava_lake(w, L)
    n_stacks = stacks(w, L)
    n_tube = tube(w, L)
    clear_pits(w, L)
    roads(w, L)
    bridge(w, L)
    houses(w, L)
    beacon(w, L)
    plinth(w, L)
    hold_interior(w, L)
    n_trees, n_small = wood(w, L)
    dressing(w, L)
    # the stairs at the doors: nothing laid; the raster's doors open onto the roads
    # blue's half: red's turned half a circle, with the hold's carpet recoloured blue
    turn_world(w, "half", red_cols(w), recolour={(B.CARPET, 14): (B.CARPET, 11)})
    P.objectives().stamp(w)
    # nothing stands off the island: a roof's overhang or a site's margin past the edge is cut
    off = ~L.land
    w.ids.swapaxes(1, 2)[off] = 0
    w.dat.swapaxes(1, 2)[off] = 0
    # the build area: block 36 under every land column, so the void filter lets players build on the island only
    X, Z = w.grid()
    w.ids[:, 0, :][L.land] = 36
    # what the turn must not leave: gravel hung over air (the undercuts)
    loose = (w.ids[:, 1:, :] == B.GRAVEL) & (w.ids[:, :-1, :] == B.AIR)
    w.ids[:, 1:, :][loose], w.dat[:, 1:, :][loose] = B.STONE, 5
    print(f"generated in {time.time() - t0:.0f}s: tube {n_tube} blocks, {n_trees} dead trees, {n_small} bushes and stumps")
    return w


if __name__ == "__main__":
    w = make()
    w.save(sys.argv[1], "Cinderfall", (0, 90, 0))
    print(f"build height {P.MAX_BUILD}, kill below {P.KILL_Y}, {int(np.count_nonzero(w.ids))} blocks")
