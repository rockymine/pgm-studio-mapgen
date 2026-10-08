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

import kit
import plan as P
from pgmvox import B, World, rng
from pgmvox import build as BLD
from pgmvox import route
from pgmvox import terrain as T
from pgmvox import under as U
from pgmvox.noise import fbm
from pgmvox.orient import turn_world

SY = 128
PALETTE_ASH = ((B.STAINED_CLAY, 7), (B.GRAVEL, 0), (B.STAINED_CLAY, 8), (B.STONE, 5))


def red_cols(w):
    X, _ = w.grid()
    return X < 0


def lay_ground(w, L):
    """Rock, soil and the painted top over red's land; the underside cleared below each column's bottom."""
    X, Z = w.grid()
    H = L.H.copy()
    red = red_cols(w) & L.land
    rock = T.Strata([((B.STONE, 5), 3, 5), ((B.STONE, 0), 1.6, 3), ((B.STAINED_CLAY, 15), 1.6, 2),
                     ((B.STAINED_CLAY, 7), 2, 3), ((B.COAL_BLOCK, 0), 0.5, 1), ((B.STAINED_CLAY, 14), 0.25, 1)],
                    length=90, seed=5, start=-300)
    deg = T.lay(w, H, red, top=T.by_angle([(22, (B.STAINED_CLAY, 7)), (45, (B.STONE, 5)), (90, (B.STONE, 0))]),
                bands=T.beds(rock, H, flecks=[((B.STONE, 5), (B.COBBLE, 0), 0.05), ((B.STONE, 0), (B.GRAVEL, 0), 0.02)],
                             seed=3),
                under=(B.STAINED_CLAY, 7), from_y=3, soil=((20, 2), (30, 1)))
    r = rng(P.BOARD, "ground")
    sh = (w.sx, w.sz)
    patch, cell = fbm(sh, 7, 2, seed=61), r.random(sh)
    rr = np.hypot(X + 0.5, Z + 0.5)
    for i, k in np.argwhere(red):
        top = int(H[i, k])
        w.ids[i, :max(0, int(L.bottom[i, k])), k] = 0
        w.dat[i, :max(0, int(L.bottom[i, k])), k] = 0
        if L.lava[i, k]:
            continue
        a = int(deg[i, k])
        c, pv = cell[i, k], patch[i, k]
        d = rr[i, k]
        if a <= 22:
            if pv > 0.25:
                blk = (B.STAINED_CLAY, 15) if c < 0.88 else (B.STAINED_CLAY, 7)          # burnt ground
            elif pv < -0.25:
                blk = (B.STONE, 5) if c < 0.88 else (B.GRAVEL, 0)
            else:
                blk = (B.STAINED_CLAY, 7) if c < 0.86 else (B.GRAVEL, 0) if c < 0.95 else (B.STAINED_CLAY, 8)
            w.ids[i, top, k], w.dat[i, top, k] = blk
        elif a <= 45:
            blk = (B.STONE, 5) if c < 0.5 else (B.COBBLE, 0) if c < 0.75 else (B.STAINED_CLAY, 15) if pv > 0.2 else (B.STONE, 0)
            w.ids[i, top, k], w.dat[i, top, k] = blk
        else:
            blk = (B.STONE, 0) if c < 0.4 else (B.STONE, 5) if c < 0.7 else (B.STAINED_CLAY, 15) if c < 0.85 else (B.COBBLE, 0)
            w.ids[i, top, k], w.dat[i, top, k] = blk
        # round the lake: obsidian and netherrack on the shore, cracks that glow, ash beyond it
        if 8.6 < d <= 11.5 and a <= 45:
            w.ids[i, top, k], w.dat[i, top, k] = (B.OBSIDIAN, 0) if c < 0.45 else (B.NETHERRACK, 0)
        elif 11.5 < d <= 24 and a <= 40 and pv > 0.4:
            w.ids[i, top, k], w.dat[i, top, k] = (B.NETHERRACK, 0)
            if c < 0.05:
                w.ids[i, top, k], w.dat[i, top, k] = (B.GLOWSTONE, 0)
    w.biome[:, :] = 2
    return deg


def lava_lake(w, L):
    """The lake: lava from its bed to the surface, an obsidian bed, a glowing floor."""
    red = red_cols(w) & L.land & L.lava
    for i, k in np.argwhere(red):
        top = int(L.H[i, k])
        w.ids[i, top, k], w.dat[i, top, k] = B.OBSIDIAN, 0
        w.ids[i, top + 1:P.LAVA_Y + 1, k] = B.LAVA
        w.dat[i, top + 1:P.LAVA_Y + 1, k] = 0
    # the east half of the lake is blue's image of the west half: the lake straddles the seam, so draw it whole
    X, Z = w.grid()
    for i, k in np.argwhere(L.lava & (X >= 0) & L.land):
        top = int(L.H[i, k])
        w.ids[i, top, k], w.dat[i, top, k] = B.OBSIDIAN, 0
        w.ids[i, top + 1:P.LAVA_Y + 1, k] = B.LAVA
        w.dat[i, top + 1:P.LAVA_Y + 1, k] = 0


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


def beacon(w, L):
    x0, z0, x1, z1 = P.BEACON
    kit.tower(w, x0, z0, x1, z1, P.BEACON_Y, 12, rng=rng(P.BOARD, "beacon"), door_side="s", ladder_on="n")


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
    pts = kit.scatter_points(ok, 70, 3.6, r, X, Z)
    for x, z in pts:
        y = int(L.H[x - w.x0, z - w.z0])
        kit.dead_tree(w, x, y, z, r, int(r.integers(5, 10)))
    n = 0
    for x, z in kit.scatter_points(ok, 60, 2.5, r, X, Z, taken=pts):
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
    for x, z in kit.scatter_points(free, 40, 5, r, X, Z):
        y = int(L.H[x - w.x0, z - w.z0])
        kit.rubble(w, x, y, z, r, r=float(r.uniform(1.2, 2.4)))
    for x, z in kit.scatter_points(free, 80, 3, r, X, Z):
        y = int(L.H[x - w.x0, z - w.z0])
        if w.id(x, y + 1, z) == B.AIR:
            w.set(x, y + 1, z, B.DEADBUSH, 0)
    # lamps along the roads, braziers at the plinth's door
    for rt in L.routes:
        if rt["kind"] == "road":
            H = np.where(L.land, L.H, 0)
            kit.lamps(w, [tuple(p) for p in rt["line"]], H, X, Z, every=14, side=3.2)
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
        kit.brazier(w, -65, yy, dz)


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
    n_tube = tube(w, L)
    clear_pits(w, L)
    roads(w, L)
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
