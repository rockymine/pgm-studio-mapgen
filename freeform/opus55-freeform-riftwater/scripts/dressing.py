"""Planting and props: the woods (rockymine's oaks and birches, planted whole), the ground cover, the wheat
field with its scarecrow and hay cart, the barn, the jetty and the rowboat, the Cutting's stumps and log
piles, the square's stalls and the street lamps, the village gardens, the spring off the ridge.

Nothing is scattered: every placement below says where and why, and a tree is refused anywhere it would
stand on a path, in a building, over the rift's lip or within reach of a monument.
"""
import json
import os

import numpy as np

import plan as P
from mc import B
from house import house
from noise import fbm, polyline_distance
from terrain import in_polygon

RNG = np.random.default_rng(777)
HERE = os.path.dirname(os.path.abspath(__file__))
TREES = json.load(open(os.path.join(HERE, "trees.json")))
NATURAL_TOP = {B.GRASS, B.DIRT}


def H(L, x, z):
    return int(L.H[x - L.x0, z - L.z0])


def route_distance(L):
    d = np.full(L.shape, np.inf)
    for r in P.ROUTES:
        dd, _ = polyline_distance(L.X, L.Z, r["pts"])
        d = np.minimum(d, dd - {"street": 2.5, "lane": 1.5, "path": 1.0}[r["kind"]])
    return d


def built_mask(w, L):
    """Columns whose ground is not grass or dirt, or that have something standing on them already."""
    m = np.zeros(L.shape, bool)
    for ix in range(L.nx):
        x = L.x0 + ix
        for iz in range(L.nz):
            if not L.land[ix, iz]:
                m[ix, iz] = True
                continue
            z = L.z0 + iz
            h = L.H[ix, iz]
            col = w.ids[x - w.x0, h:h + 30, z - w.z0]
            if int(col[0]) not in NATURAL_TOP or np.any((col[1:] != 0) & (col[1:] != B.TALLGRASS)):
                m[ix, iz] = True
    return m


def plant(w, L, x, z, tree, turn=0):
    """Plant a tree whole with its foot on the ground at (x, z), turned by quarter turns. Refuse if any of
    its blocks would land in something that is not air or plant."""
    g = H(L, x, z)
    cells = []
    for dx, dy, dz, i, d in tree["blocks"]:
        for _ in range(turn):
            dx, dz = -dz, dx
        X, Y, Z = x + dx, g + 1 + dy, z + dz
        if not w.inside(X, Y, Z) or X >= -1:
            return False
        cur = w.id(X, Y, Z)
        if cur in (B.GRASS, B.DIRT, B.STONE, B.COBBLE, B.GRAVEL):
            continue            # a crown on a hillside meets the hill: the hill wins, the tree still stands
        if cur not in (B.AIR, B.TALLGRASS, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT, B.LEAVES, B.LEAVES2):
            return False
        cells.append((X, Y, Z, i, d))
    for X, Y, Z, i, d in cells:
        # turned logs keep their sawn ends pointing the right way
        if i in (17, 162) and turn % 2 == 1 and (d & 12) in (4, 8):
            d = (d & 3) | (12 - (d & 12))
        if w.id(X, Y, Z) in (B.LEAVES, B.LEAVES2) and i in (18, 161):
            continue
        w.set(X, Y, Z, i, d)
    if w.id(x, g, z) == B.GRASS:
        w.set(x, g, z, B.DIRT)
    return True


def forest(w, L, zone, kinds, weights, spacing=1.0, tries=4000, extra_ok=None, seed=0):
    """Fill a zone with trees whose trunks stand at least their two crowns' worth apart."""
    rng = np.random.default_rng(seed)
    pts = np.argwhere(zone)
    rng.shuffle(pts)
    planted = L.trees
    n = 0
    for ix, iz in pts[:tries]:
        x, z = L.x0 + ix, L.z0 + iz
        if L.blocked[ix, iz]:
            continue
        if extra_ok is not None and not extra_ok(x, z):
            continue
        kind = rng.choice(kinds, p=weights)
        t = TREES[kind][rng.integers(len(TREES[kind]))]
        c = t["crown"] * 0.5
        if any(np.hypot(x - px, z - pz) < (c + pc) * spacing for px, pz, pc in planted):
            continue
        if L.route_d[ix, iz] < 3 or L.mon_d[ix, iz] < 4 + t["crown"]:
            continue
        if plant(w, L, x, z, t, int(rng.integers(4))):
            planted.append((x, z, c))
            n += 1
    return n


def cover(w, L):
    """Grass, ferns and flowers on grass with nothing on it: sparse on the open ground, fuller in the woods,
    flowers in drifts rather than confetti."""
    dens = fbm(L.shape, 9, 2, seed=81)
    flowers = fbm(L.shape, 14, 2, seed=82)
    ftype = fbm(L.shape, 30, 1, seed=83)
    for ix in range(L.nx):
        for iz in range(L.nz):
            if not L.land[ix, iz]:
                continue
            x, z = L.x0 + ix, L.z0 + iz
            g = L.H[ix, iz]
            if w.id(x, g, z) != B.GRASS or w.id(x, g + 1, z) != B.AIR:
                continue
            if L.mon_d[ix, iz] < 2:
                continue
            wood = L.forest[ix, iz]
            p = (0.30 if wood else 0.07) * (0.6 + dens[ix, iz])
            r = RNG.random()
            if flowers[ix, iz] > 0.58 and not wood and r < 0.3:
                t = ftype[ix, iz]
                kind = (B.DANDELION, 0) if t < -0.3 else (B.FLOWER, 3) if t < 0.0 else (B.FLOWER, 8) if t < 0.3 else (B.FLOWER, 0)
                w.set(x, g + 1, z, *kind)
            elif r < p:
                if wood and RNG.random() < 0.45:
                    w.set(x, g + 1, z, B.TALLGRASS, 2)
                elif RNG.random() < 0.06 and w.id(x, g + 2, z) == B.AIR and L.route_d[ix, iz] > 3:
                    w.set(x, g + 1, z, B.DOUBLE_PLANT, 2); w.set(x, g + 2, z, B.DOUBLE_PLANT, 10)
                else:
                    w.set(x, g + 1, z, B.TALLGRASS, 1)


# ---- the farm ---------------------------------------------------------------------------------------------
FIELD = (-50, 45, -31, 69)


def wheat_field(w, L):
    """Strips of wheat, carrots and potatoes on farmland, watered by ditches every ninth row, fenced on the
    village side; the scarecrow stands in the middle of it, the hay cart at its foot."""
    x0, z0, x1, z1 = FIELD
    base = int(np.median(L.H[x0 - L.x0:x1 - L.x0 + 1, z0 - L.z0:z1 - L.z0 + 1]))
    crops = [(B.WHEAT, 7), (B.WHEAT, 7), (B.WHEAT, 6), (B.CARROTS, 7), (B.WHEAT, 7), (B.POTATOES, 7)]
    for z in range(z0, z1 + 1):
        strip = (z - z0) // 9
        ditch = (z - z0) % 9 == 4
        crop = crops[strip % len(crops)]
        for x in range(x0, x1 + 1):
            ix, iz = x - L.x0, z - L.z0
            if not L.land[ix, iz] or L.water[ix, iz]:
                continue
            g = L.H[ix, iz]
            # the field is a tilted plane: each strip level, one step between strips at most
            y = base + int(round((z - (z0 + z1) / 2) * 0.06))
            for yy in range(y + 1, g + 3):
                w.set(x, yy, z, B.AIR)
            for yy in range(min(g, y) - 2, y):
                w.set(x, yy, z, B.DIRT)
            if ditch and x0 < x < x1:
                w.set(x, y, z, B.WATER)
                w.set(x, y - 1, z, B.DIRT)
            elif x in (x0, x1) or z in (z0, z1):
                w.set(x, y, z, B.GRASS)
            else:
                w.set(x, y, z, B.FARMLAND, 7)
                c = crop
                if c[0] == B.WHEAT and RNG.random() < 0.15:
                    c = (B.WHEAT, int(RNG.integers(4, 8)))
                w.set(x, y + 1, z, *c)
            L.H[ix, iz] = y
    # a fence along the field's west side, toward the green and the village, with a gate
    for z in range(z0, z1 + 1):
        y = L.H[x0 - L.x0, z - L.z0]
        if z == (z0 + z1) // 2:
            w.set(x0, y + 1, z, B.FENCE_GATE, 1)
        else:
            w.set(x0, y + 1, z, B.FENCE)
    # the scarecrow: fence legs, a hay-bale body with fence arms, a pumpkin head, facing the rift
    sx, sz = (x0 + x1) // 2 + 1, (z0 + z1) // 2 - 3
    y = L.H[sx - L.x0, sz - L.z0]
    w.set(sx, y + 1, sz, B.FENCE)
    w.set(sx, y + 2, sz, B.FENCE)
    w.set(sx, y + 3, sz, B.HAY, 0)
    w.set(sx, y + 3, sz - 1, B.FENCE); w.set(sx, y + 3, sz + 1, B.FENCE)
    w.set(sx, y + 4, sz, B.PUMPKIN, 3)
    L.field = FIELD
    L.scarecrow = (sx, y + 1, sz)


def hay_cart(w, L, x, z):
    """A two-wheeled cart piled with hay, its shafts down: log wheels show their sawn ends as the rims."""
    g = H(L, x, z)
    for dz in (0, 1, 2):
        for dx in (0, 1):
            w.set(x + dx, g + 2, z + dz, B.WOOD_SLAB, 1)
            w.set(x + dx, g + 3, z + dz, B.HAY, 8)
    w.set(x, g + 4, z + 1, B.HAY, 8)
    w.set(x - 1, g + 1, z + 1, B.LOG2, 1 | 4); w.set(x + 2, g + 1, z + 1, B.LOG2, 1 | 4)
    w.set(x, g + 1, z + 1, B.DARK_OAK_FENCE); w.set(x + 1, g + 1, z + 1, B.DARK_OAK_FENCE)
    w.set(x, g + 1, z - 1, B.SPRUCE_FENCE); w.set(x + 1, g + 1, z - 1, B.SPRUCE_FENCE)
    w.set(x, g + 2, z - 1, B.WOOD_SLAB, 1); w.set(x + 1, g + 2, z - 1, B.WOOD_SLAB, 1)


def haystacks(w, L, pts):
    for x, z in pts:
        g = H(L, x, z)
        for dx in (0, 1):
            for dz in (0, 1):
                w.set(x + dx, g + 1, z + dz, B.HAY, 0 if (dx + dz) % 2 else 4)
        w.set(x, g + 2, z, B.HAY, 8)


def barn(w, L):
    rec = house(w, L, -67, 64, -59, 73, storeys=2, style="village", door="e", kind="barn", along_x=False,
                chimney=False)
    f = rec["floor"]
    # a wide door: open the middle of the east wall, two blocks high
    for z in range(67, 71):
        for y in (f + 1, f + 2, f + 3):
            w.set(-59, y, z, B.AIR)
    for z in range(65, 73):
        for x in range(-66, -61):
            if (x + z) % 3 == 0:
                w.set(x, f + 1, z, B.HAY, 0)
    return rec


# ---- the pond --------------------------------------------------------------------------------------------
def jetty_and_boat(w, L):
    """A plank jetty off the end of the spit, and the rowboat tied to it."""
    for z in range(16, 21):
        for x in (-83, -82):
            w.set(x, 49, z, B.PLANKS, 1)
        if z % 2 == 0:
            for x in (-84, -81):
                w.set(x, 49, z, B.SPRUCE_FENCE) if z == 16 else None
            w.set(-83, 48, z, B.LOG, 1); w.set(-83, 47, z, B.LOG, 1)
    w.set(-84, 50, 16, B.SPRUCE_FENCE)
    # the rowboat: a hull of spruce stairs and slabs floating on the pond, oars of fence
    bx, bz = -79, 13
    y = 48
    for dz in range(0, 5):
        for dx in (0, 1):
            if dz in (0, 4):
                w.set(bx + dx, y, bz + dz, B.SPRUCE_STAIRS, 2 if dz == 4 else 3)
            else:
                w.set(bx + dx, y, bz + dz, B.WOOD_SLAB, 1 | 8)
    w.set(bx - 1, y, bz + 2, B.SPRUCE_FENCE); w.set(bx + 2, y, bz + 2, B.SPRUCE_FENCE)
    # lily pads in the still corners, reeds where the shore is sand
    for _ in range(60):
        x = int(RNG.integers(-96, -71)); z = int(RNG.integers(10, 31))
        ix, iz = x - L.x0, z - L.z0
        if L.water[ix, iz] == 48 and w.id(x, 49, z) == B.AIR and w.id(x, 48, z) == B.WATER:
            near_shore = any(L.water[ix + a, iz + b] == 0 for a in (-2, 0, 2) for b in (-2, 0, 2))
            if near_shore:
                w.set(x, 49, z, B.LILY)
    for ix in range(L.nx):
        for iz in range(L.nz):
            if L.water[ix, iz] or not L.land[ix, iz]:
                continue
            x, z = L.x0 + ix, L.z0 + iz
            if not (-98 < x < -66 and 6 < z < 34):
                continue
            g = L.H[ix, iz]
            if w.id(x, g, z) in (B.GRASS, B.SAND, B.DIRT) and w.id(x, g + 1, z) == B.AIR and g == 49:
                if any(L.water[ix + a, iz + b] == 48 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) and RNG.random() < 0.35:
                    for k in range(1, 2 + int(RNG.integers(0, 2))):
                        w.set(x, g + k, z, B.REEDS)


def spring(w, L):
    """The river's source: water breaking out of a cleft in the ridge and falling into the pond."""
    z = 21
    x_src = -99
    g = H(L, x_src, z)
    for x in range(x_src, -95):
        top = H(L, x, z)
        if x == x_src:
            w.set(x, g, z, B.WATER)
            w.set(x, g + 1, z, B.AIR)
            continue
        for y in range(49, top + 1):
            w.set(x, y, z, B.AIR)
        for y in range(49, g):
            if x == x_src + 1:
                w.set(x, y, z, B.WATER_FLOW, 8)
        w.set(x, 48, z, B.STONE, 5)
    # mossy rocks beside the cleft
    for dz in (-1, 1):
        for y in range(48, g + 1):
            if w.id(x_src + 1, y, z + dz) in (B.AIR, B.GRASS, B.DIRT):
                w.set(x_src + 1, y, z + dz, B.MOSSY if RNG.random() < 0.4 else B.COBBLE)


# ---- the Cutting -----------------------------------------------------------------------------------------
def cutting(w, L):
    """Where the south wood was felled for the mine's props: stumps, log piles, a sawhorse, a sledge."""
    cx, cz = -110, 68
    rng = np.random.default_rng(5)
    for _ in range(14):
        a = rng.uniform(0, 2 * np.pi); r = rng.uniform(2, 8)
        x, z = int(cx + r * np.cos(a)), int(cz + r * np.sin(a))
        g = H(L, x, z)
        if w.id(x, g, z) not in NATURAL_TOP or w.id(x, g + 1, z) not in (B.AIR, B.TALLGRASS):
            continue
        sp = 2 if rng.random() < 0.35 else 0
        w.set(x, g + 1, z, B.LOG, sp | 0)
        if rng.random() < 0.3:
            w.set(x, g + 2, z, B.WOOD_SLAB, sp)
    # log piles: logs laid along x, three, two, one
    for px, pz in ((-106, 63), (-113, 73)):
        g = H(L, px, pz)
        for layer, n in enumerate((3, 2, 1)):
            for k in range(n):
                for dx in range(4):
                    w.set(px + dx, g + 1 + layer, pz + k + layer // 2 + (layer % 2) * 0, B.LOG, 4 | (2 if (k + layer) % 3 == 0 else 0))
    # a sawhorse with a log on it
    g = H(L, -109, 70)
    w.set(-110, g + 1, 70, B.SPRUCE_FENCE); w.set(-107, g + 1, 70, B.SPRUCE_FENCE)
    for x in range(-111, -105):
        w.set(x, g + 2, 70, B.LOG, 4)
    # sawdust and bark underfoot
    for _ in range(40):
        a = RNG.uniform(0, 2 * np.pi); r = RNG.uniform(0, 7)
        x, z = int(cx + r * np.cos(a)), int(cz + r * np.sin(a))
        g = H(L, x, z)
        if w.id(x, g, z) == B.GRASS:
            w.set(x, g, z, B.DIRT, 1 if RNG.random() < 0.5 else 0)
            if w.id(x, g + 1, z) in (B.TALLGRASS, B.FLOWER):
                w.set(x, g + 1, z, B.AIR)


# ---- the town's furniture ---------------------------------------------------------------------------------
def stalls(w, L):
    """Market stalls along the square's west edge, well back from the monument: fence posts, a wool awning."""
    x0, z0, x1, z1, y = L.square
    for i, z in enumerate(range(z0 + 3, z1 - 2, 5)):
        x = x0 + 1
        colour = (14, 4, 11, 13)[i % 4]
        for dz in (0, 2):
            for yy in (1, 2):
                w.set(x, y + yy, z + dz, B.FENCE)
                w.set(x + 2, y + yy, z + dz, B.FENCE)
        for dx in range(0, 3):
            for dz in range(0, 3):
                w.set(x + dx, y + 3, z + dz, B.WOOL if (dx + i) % 2 else B.WOOL, colour if dx != 1 else 0)
        w.set(x + 2, y + 1, z + 1, B.WOOD_SLAB, 1 | 8)
        w.set(x + 1, y + 1, z + 1, B.CHEST, 5)
        w.set(x + 2, y + 2, z + 1, B.PUMPKIN if i % 2 else B.MELON, 3)


def lamps(w, L, pts, every=10):
    """A lamp post every so often along a street: a fence post carrying a lantern of glowstone."""
    from noise import spline
    sp = spline(pts, 1.0)
    for i in range(every // 2, len(sp), every):
        x, z = int(round(sp[i][0])), int(round(sp[i][1]))
        for off in (3, -3):
            X, Z = x, z + off
            g = H(L, X, Z)
            if w.id(X, g + 1, Z) == B.AIR and w.id(X, g, Z) not in (B.WATER,):
                for yy in (1, 2, 3):
                    w.set(X, g + yy, Z, B.FENCE)
                w.set(X, g + 4, Z, B.GLOWSTONE)
                w.set(X, g + 5, Z, B.WOOD_SLAB, 5)
                break


def gardens(w, L):
    """A vegetable patch fenced behind each Ironhollow cottage, on its back (west) side."""
    for rec in L.records:
        if rec.get("style") != "village" or rec.get("kind") not in ("cottage", "house"):
            continue
        if rec["x0"] < -100 or rec["z0"] < 30:
            continue
        x1 = rec["x0"] - 2
        x0 = x1 - 3
        z0, z1 = rec["z0"], rec["z1"]
        y = rec["floor"]
        if any(w.id(x, H(L, x, z) + 1, z) not in (B.AIR, B.TALLGRASS, B.FLOWER) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)):
            continue
        for x in range(x0 - 1, x1 + 2):
            for z in range(z0 - 1, z1 + 2):
                g = H(L, x, z)
                if abs(g - y) > 1:
                    continue
                if x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1):
                    w.set(x, g + 1, z, B.SPRUCE_FENCE)
                else:
                    w.set(x, g, z, B.FARMLAND, 7)
                    w.set(x, g + 1, z, B.CARROTS if (z % 2) else B.POTATOES, 7)
        # a water source in the middle keeps it from drying out
        mx, mz = (x0 + x1) // 2, (z0 + z1) // 2
        w.set(mx, H(L, mx, mz), mz, B.WATER)
        w.set(mx, H(L, mx, mz) + 1, mz, B.AIR)


def benches(w, L):
    """Two benches facing the falls on the Falls Walk, where somebody would sit and look."""
    for x, z in ((-20, 12), (-24, 13)):
        g = H(L, x, z)
        if w.id(x, g + 1, z) == B.AIR:
            w.set(x, g + 1, z, B.SPRUCE_STAIRS, 3)


def build(w, L):
    L.route_d = route_distance(L)
    mons = list(P.MONUMENTS.values())
    L.mon_d = np.min([np.hypot(L.X - mx, L.Z - mz) for mx, mz in mons], axis=0)
    wheat_field(w, L)
    barn(w, L)
    haystacks(w, L, [(-56, 76), (-53, 73)])
    hay_cart(w, L, -45, 72)
    jetty_and_boat(w, L)
    spring(w, L)
    cutting(w, L)
    stalls(w, L)
    for r in P.ROUTES:
        if r["kind"] == "street":
            lamps(w, L, r["pts"])
    gardens(w, L)
    benches(w, L)
    # where a tree may stand
    bm = built_mask(w, L)
    edge = ~L.land
    from scipy import ndimage
    edge_d = ndimage.distance_transform_edt(~edge)
    L.blocked = bm | (edge_d < 4)
    L.trees = []
    woods = in_polygon(L.X, L.Z, dict((p["key"], p) for p in P.PLACES)["north_wood"]["poly"])
    ridge = (L.X < -101) & ~((L.X > -110) & (L.Z > -18) & (L.Z < 6))
    south_wood = (L.X < -98) & (L.Z > 36) & (np.hypot(L.X + 110, L.Z - 68) > 9)
    n = forest(w, L, woods & ~ridge, ["oak", "birch", "tiny-oak"], [0.22, 0.43, 0.35], spacing=0.85, seed=1)
    n += forest(w, L, ridge & ~south_wood, ["birch", "oak", "tiny-oak"], [0.45, 0.2, 0.35], spacing=0.85, seed=2)
    n += forest(w, L, south_wood, ["oak", "birch", "tiny-oak"], [0.25, 0.4, 0.35], spacing=0.85, seed=3)
    # the clearing's edge: a ring of young trees where the felling stopped
    ring = (np.abs(np.hypot(L.X + 110, L.Z - 68) - 11) < 2)
    n += forest(w, L, ring, ["tiny-oak", "birch"], [0.6, 0.4], spacing=0.8, seed=4)
    # Lone Oak Knoll: the one big oak on its top
    plant(w, L, -22, 74, TREES["big-oak"][1], 1)
    L.trees.append((-22, 74, 7))
    # single trees placed for a reason: one by the inn's yard, one in the chapel's garth, two by the mill,
    # birches along the field bank between the bridge and the falls, oaks shading the village well and green
    for (x, z, kind, i) in ((-22, -24, "tiny-oak", 2), (-36, -84, "oak", 6), (-70, 4, "birch", 3),
                            (-54, 2, "tiny-oak", 5), (-28, 20, "birch", 1), (-20, 24, "birch", 4),
                            (-44, 18, "birch", 7), (-91, 47, "tiny-oak", 0), (-68, 78, "oak", 8),
                            (-90, 80, "tiny-oak", 3), (-70, -24, "tiny-oak", 6), (-80, -36, "oak", 7),
                            (-82, 30, "birch", 2), (-62, -84, "birch", 5)):
        t = TREES[kind][i % len(TREES[kind])]
        ix, iz = x - L.x0, z - L.z0
        if L.mon_d[ix, iz] < 4 + t["crown"] or L.blocked[ix, iz]:
            continue
        if plant(w, L, x, z, t, i % 4):
            L.trees.append((x, z, t["crown"] * 0.6))
            n += 1
    print(f"  planted {n} trees")
    cover(w, L)
