"""Abbeymoor's surface and what stands on it (red's half; the half turn carries it to blue's): the paint of the moor, the bog, the
roads and the nave; the water; the abbey's ruined walls, its dais and the monuments' dressing; the houses; the Standing Stones, the peat
cuttings, the drystone walls, the orchards, the boulders; the cuts into the rim.

Every prop has a reason beside it. Nothing stands within six of a monument but ground, and no tree stands on a road, a green, the bog or the hill.
A house's windows keep two blocks clear of its door.
"""
import numpy as np

import crypt
import land
import plan as P
from pgmvox import B, noise, props, trees
from pgmvox import build as BLD
from pgmvox import terrain as T
from pgmvox.orient import door as door_data, stair as stair_data
from pgmvox.shapes import polyline


def cellpick(x, z, choices, size=3, salt=0):
    k = ((x // size) * 73856093 ^ (z // size) * 19349663 ^ salt * 83492791) & 0xFFFF
    return choices[k % len(choices)]


FLAGS = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONEBRICK, 2)]
ROAD = [(B.DIRT, 1), (B.DIRT, 1), (B.DIRT, 1), (B.DIRT, 0), (B.GRAVEL, 0)]       # a trodden track: coarse dirt, plain dirt, a little gravel

# heather, podzol and worn ground are shapes: (cx, cz, rx, rz, what), red's half (z < 0) and drawn once; the image comes with the turn
PATCHES = [(-12, -100, 9, 6, "heather"), (-60, -110, 10, 7, "heather"), (-68, -80, 8, 10, "heather"), (-20, -52, 12, 5, "heather"),
           (70, -100, 8, 8, "heather"), (80, -60, 8, 12, "heather"), (-80, -40, 8, 8, "heather"), (50, -26, 10, 6, "heather"),
           (-74, -60, 5, 4, "podzol"), (46, -102, 6, 4, "podzol"), (-52, -100, 6, 4, "podzol"), (60, -76, 6, 5, "podzol"),
           (18, -108, 4, 4, "dirt"), (-34, -100, 4, 3, "dirt"), (74, -30, 6, 4, "dirt"), (-86, -20, 6, 5, "podzol")]


# the bog's outliers: peat ground in irregular shapes round the moor and through the middle, (cx, cz, rx, rz, tilt); drawn once, red's half
PEAT = [(-60, -20, 9, 5, 0.5), (-46, -8, 7, 4, -0.4), (-84, -26, 6, 4, 0.2), (-30, -48, 8, 4, 0.0), (-12, -36, 5, 3, 0.7), (14, -22, 7, 3, -0.3),
        (40, -16, 8, 4, 0.4), (62, -8, 6, 4, -0.5), (82, -14, 5, 5, 0.0), (28, -40, 5, 3, 0.3), (-70, -50, 6, 4, 0.6), (-26, -64, 4, 3, 0.0),
        (74, -48, 6, 3, -0.2), (-90, -70, 4, 5, 0.0), (52, -34, 4, 3, 0.5)]


def in_peat(x, z, wobble):
    for cx, cz, rx, rz, tilt in PEAT:
        u, v = x - cx, z - cz
        a, b = u * np.cos(tilt) + v * np.sin(tilt), -u * np.sin(tilt) + v * np.cos(tilt)
        if (a / rx) ** 2 + (b / rz) ** 2 <= 1 + 0.5 * wobble:
            return True
    return False


def patch_of(x, z):
    for cx, cz, rx, rz, what in PATCHES:
        if ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2 <= 1:
            return what
    return None


def surface(w, R, deg, r, stats):
    """The top of every column by what it is: flagstones in the nave, gravel and coarse dirt on the roads, clean turf on the green and
    the orchards, the bog's dark ground (coarse dirt, podzol, a little clay by the pools), heather (mycelium with allium), podzol and
    worn dirt as shapes on the moor, grass elsewhere, and bare rock past the angle where soil holds."""
    X, Z = w.grid()
    names = {i: k for k, i in R.kinds.items()}
    grain = noise.fbm((w.sx, w.sz), 5, 2, seed=44)
    wetness = noise.fbm((w.sx, w.sz), 9, 2, seed=45)
    main, lobe = land.bog_field(X, Z)
    bogish = (main < 0.78) | (lobe < 0.7)
    n = dict(heather=0, flags=0, bog=0, road=0)
    for i, k in np.argwhere(P.LAND & (Z < 0)):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(P.H[i, k])
        kind = names[int(R.K[i, k])]
        if kind in ("water", "hole", "wall", "room", "door", "ruin", "stair"):
            continue
        d = deg[i, k]
        top, soil = (B.GRASS, 0), (B.DIRT, 0)
        if kind == "nave":
            top, soil = cellpick(x, z, FLAGS, salt=4), (B.STONEBRICK, 0)
            n["flags"] += 1
        elif kind == "road":
            top, soil = cellpick(x, z, ROAD, salt=3), (B.DIRT, 1)
            n["road"] += 1
        elif kind == "boardwalk":
            top, soil = (B.PLANKS, 1), (B.DIRT, 1)
        elif kind == "peat":
            top, soil = (B.DIRT, 1), (B.DIRT, 1)
        elif kind in ("green", "orchard"):
            pass
        elif d > 44:
            top, soil = ((B.STONE, 0) if (x + z) % 3 else (B.STONE, 5)), (B.STONE, 0)
        elif d > 34:
            top, soil = ((B.STONE, 5) if grain[i, k] > 0 else (B.GRASS, 0)), (B.DIRT, 0)
        elif bogish[i, k] and h <= P.BOG + 3:
            c = grain[i, k]
            top = (B.DIRT, 1) if c < 0.15 else (B.DIRT, 2) if c < 0.55 else (B.DIRT, 0)
            soil = (B.DIRT, 1)
            n["bog"] += 1
        elif in_peat(x, z, wetness[i, k]) and h <= P.BOG + 8:
            c = grain[i, k]
            top = (B.DIRT, 1) if c < 0.1 else (B.DIRT, 2) if c < 0.5 else (B.DIRT, 0)
            soil = (B.DIRT, 1)
            n["bog"] += 1
        else:
            what = patch_of(x, z)
            if what == "heather":
                top, soil = (B.MYCELIUM, 0), (B.DIRT, 2)
                n["heather"] += 1
            elif what == "podzol":
                top, soil = (B.DIRT, 2), (B.DIRT, 2)
            elif what == "dirt" or (grain[i, k] > 0.62):
                top, soil = (B.DIRT, 1), (B.DIRT, 1)
        w.set(x, h, z, *top)
        w.set(x, h - 1, z, *soil)
        w.set(x, h - 2, z, *soil)
    stats["paint"] = n


def water(w, stats):
    """Water in every wet column from the bed's top to the surface land.py left: the pools, the beck."""
    X, Z = w.grid()
    n = 0
    for i, k in np.argwhere(P.WET):
        x, z = int(X[i, k]), int(Z[i, k])
        if z >= 0:
            continue
        top = int(max(P.H[i, k], 0))
        surf = P.BOG
        for wat in P.WATERS:
            if wat.mask[i, k]:
                surf = int(wat.surface[i, k])
        for y in range(top + 1, surf + 1):
            w.set(x, y, z, B.WATER)
            n += 1
        if surf >= top:
            w.set(x, top, z, B.SAND if (x + z) % 3 == 0 else B.CLAY)
    stats["water"] = n


# ---- houses ------------------------------------------------------------------------------------------------------
def clear_windows(L, margin=2.6):
    base = BLD.window_rhythm()

    def f(run, span, t, storey):
        if span == L and abs(run - span / 2) < margin:
            return False
        return base(run, span, t, storey)
    return f


def clay_style(walls, roof=(B.PLANKS, 5), stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR, window=(B.PANE, 0), post=1):
    """Clay or brick walls in a spruce frame, a stone course at the foot (see rebase)."""
    return dict(ground=walls, upper=walls, post=post, gable=walls[0], floor=(B.PLANKS, 1), roof=roof, stair=stair, slab=slab, door=door,
                window=window, chimney=(B.COBBLE, 0))


LIME_WASH = [(B.STAINED_CLAY, 0), (B.STAINED_CLAY, 0), (B.STAINED_CLAY, 8)]
OCHRE = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 4), (B.STAINED_CLAY, 1)]
BRICK_RED = [(B.BRICK, 0), (B.BRICK, 0), (B.BRICK, 0), (B.STAINED_CLAY, 14)]
TERRACOTTA = [(B.HARDENED_CLAY, 0), (B.HARDENED_CLAY, 0), (B.STAINED_CLAY, 1)]
UMBER = [(B.STAINED_CLAY, 12), (B.STAINED_CLAY, 12), (B.HARDENED_CLAY, 0)]
SLATE_ROOF = dict(roof=(B.STONEBRICK, 0), stair=B.STONEBRICK_STAIRS, slab=(B.SLAB, 5))
STYLE_TIMBER = dict(ground=[(B.PLANKS, 1)], upper=[(B.PLANKS, 1)], post=1, gable=(B.PLANKS, 1), floor=(B.PLANKS, 1), roof=(B.PLANKS, 5),
                    stair=B.DARK_OAK_STAIRS, slab=(B.WOOD_SLAB, 5), door=B.SPRUCE_DOOR, window=(B.PANE, 0))
STYLES = {"farmhouse": (clay_style(LIME_WASH), 1, 4), "farm-barn": (STYLE_TIMBER, 1, 5), "c1": (clay_style(OCHRE), 1, 4),
          "c2": (clay_style(BRICK_RED), 1, 4), "c3": (clay_style(TERRACOTTA, **SLATE_ROOF), 1, 4), "c4": (clay_style(LIME_WASH), 1, 4),
          "inn": (clay_style(UMBER, roof=(B.BRICK, 0), stair=B.BRICK_STAIRS, slab=(B.SLAB, 4), door=B.DARK_OAK_DOOR), 2, 4),
          "tithe": (clay_style(OCHRE, door=B.DARK_OAK_DOOR, **SLATE_ROOF), 1, 7),
          "f1": (clay_style(TERRACOTTA), 1, 4), "f2": (clay_style(LIME_WASH), 1, 4), "f3": (clay_style(UMBER, **SLATE_ROOF), 1, 4)}
FOOT = [(B.COBBLE, 0), (B.STONE, 5), (B.STONEBRICK, 0)]
WALL_BLOCKS = {B.BRICK, B.STAINED_CLAY, B.HARDENED_CLAY}


def rebase(w, res, floor, r):
    """A stone course at the foot of a clay or brick house: the first course of wall, but for the door and the windows."""
    for x, z in res["footprint"]:
        if w.id(x, floor + 1, z) in WALL_BLOCKS:
            w.set(x, floor + 1, z, *FOOT[int(r.integers(len(FOOT)))])


def houses(w, r, stats):
    ground = lambda x, z: P.g(x, z)                                          # noqa: E731
    out = {}
    for key, hs in P.houses().items():
        key_, cx, cz, heading, L, W, door, name = hs["spec"]
        style, storeys, storey = STYLES[key]
        h = BLD.House(cx=cx, cz=cz, heading=heading, L=L, W=W, floor=hs["floor"], storeys=storeys, storey=storey, style=style, door=door,
                      roof="gable", pitch=2 if key == "tithe" else 1, overhang=1, chimney=key in ("c1", "c2", "c3", "c4", "inn", "farmhouse", "f1", "f3"),
                      windows=clear_windows(L))
        res = BLD.house(w, h, ground, r)
        if style is not STYLE_TIMBER:
            rebase(w, res, hs["floor"], r)
        if (res["door"][0], res["door"][1]) != hs["door"]:
            raise RuntimeError(f"{key}: the library put the door at {res['door'][:2]}, the plan says {hs['door']}")
        out[key] = res
    stats["houses"] = len(out)
    return out


# ---- the abbey ---------------------------------------------------------------------------------------------------
def abbey(w, r, stats):
    """The nave: walls one block thick on the plan's ring, ragged at two to five high, buttresses every six, a pointed window every five
    (a gap three wide and five high), the doors the plan names open to the ground; the tower stump at the north-west corner, twelve
    high and broken; the west gable standing; rubble; the dais and its plinth under Monument A."""
    x0, z0, x1, z1 = P.NAVE
    f = P.PLATEAU
    n1 = noise.fbm((w.sx, w.sz), 4, 2, seed=61)
    doors = [d for _, d in P.NAVE_DOORS]
    def in_door(x, z):
        return any(a <= x <= c and b <= z <= d for a, b, c, d in doors)
    for x in range(x0, x2 := x1 + 1):
        for z in range(z0, z1 + 1):
            ring = x in (x0, x1) or z in (z0, z1)
            if not ring or in_door(x, z):
                continue
            i, k = x - w.x0, z - w.z0
            height = 4 + int(2.2 * n1[i, k]) + (2 if (x - x0) % 6 == 0 or (z - z0) % 6 == 0 else 0)
            if x == x0:
                height = 9                                                   # the west gable
            if x == x1:
                height = 2 + int(1.5 * (n1[i, k] + 1))                       # the east end, fallen
            window = (z in (z0, z1) and (x - x0) % 5 == 2 and 3 <= x - x0 <= 22) or (x == x0 and z in range(z0 + 5, z0 + 8))
            for y in range(f + 1, f + 1 + height):
                if window and f + 3 <= y <= f + 7 and not (abs(((x - x0) % 5) - 2) + (y - f - 3) * 0 > 1):
                    continue
                c = r.random()
                w.set(x, y, z, *((B.STONEBRICK, 0) if c < 0.5 else (B.STONEBRICK, 2) if c < 0.7 else (B.STONEBRICK, 1) if c < 0.85 else (B.COBBLE, 0)))
    # the tower stump: a hollow square of walls, twelve high at the corner and broken lower
    tx0, tz0, tx1, tz1 = P.TOWER
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            if x in (tx0, tx1) or z in (tz0, tz1):
                hgt = 12 - int(5 * abs(n1[x - w.x0, z - w.z0]) + 3 * ((x + z) % 2)) if (x, z) != (tx0, tz0) else 12
                for y in range(f + 1, f + 1 + hgt):
                    c = r.random()
                    w.set(x, y, z, *((B.STONEBRICK, 0) if c < 0.55 else (B.STONEBRICK, 2) if c < 0.8 else (B.COBBLE, 0)))
            else:
                for y in range(f + 1, f + 14):
                    w.set(x, y, z, B.AIR)
    # the dais and its plinth: three courses of stone brick under Monument A, five clear round it
    cx, cz = P.A_CENTRE
    for k, half in enumerate((3, 2, 1)):
        for dx in range(-half, half + 1):
            for dz in range(-half, half + 1):
                w.set(cx + dx, f + 1 + k, cz + dz, B.STONEBRICK, 3 if (dx == 0 and dz == 0) else 0)
    # rubble in the nave and outside it: fallen stones, one to three high
    for _ in range(40):
        x = int(r.integers(x0 + 2, x1 - 2))
        z = int(r.integers(z0 + 2, z1 - 2))
        if abs(x - cx) < 6 and abs(z - cz) < 6:
            continue
        if P.SLOT[0] - 1 <= x <= P.SLOT[2] + 1 and P.SLOT[1] - 2 <= z <= P.SLOT[3] + 2:
            continue
        for y in range(f + 1, f + 1 + int(r.integers(1, 3))):
            w.set(x, y, z, *((B.COBBLE, 0) if r.random() < 0.6 else (B.STONEBRICK, 2)))
    stats["abbey"] = "walls, tower, dais"


def gatehouse(w, r):
    """The Gatehouse: a ruined arch on the Monks' Way at the hill's foot, two piers and a lintel half fallen."""
    gx, gz = P.GATE
    y = P.g(gx, gz)
    for dx in (-3, 3):
        for yy in range(y + 1, y + 7):
            w.set(gx + dx, yy, gz, *((B.STONEBRICK, 0) if r.random() < 0.7 else (B.STONEBRICK, 2)))
            w.set(gx + dx, yy, gz + 1, *((B.STONEBRICK, 0) if r.random() < 0.7 else (B.COBBLE, 0)))
    for dx in range(-3, 1):
        w.set(gx + dx, y + 7, gz, B.STONEBRICK, 3)
    w.set(gx + 1, y + 6, gz, B.STONEBRICK_STAIRS, stair_data("w"))


def monuments(w, r):
    """Round each cube: a ring of stone brick flush with the ground (A is on its dais), four banners of its team's colour at five blocks,
    two lamps. No tree, wall or house within the five."""
    for (cx, cz), dais in ((P.A_CENTRE, True), (P.B_CENTRE, False)):
        y = P.g(cx, cz)
        if not dais:
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    if max(abs(dx), abs(dz)) in (2, 3):
                        w.set(cx + dx, y, cz + dz, *cellpick(cx + dx, cz + dz, FLAGS, 2, 5))
        for sx, sz in ((-7, -7), (7, -7), (-7, 7), (7, 7)):
            by = P.g(cx + sx, cz + sz)
            for yy in range(by + 1, by + 6):
                w.set(cx + sx, yy, cz + sz, B.FENCE, 0)
            w.banner(cx + sx, by + 6, cz + sz, 1, rot=0)
        for sx in (-7, 7):
            props.lamp(w, cx + sx, P.g(cx + sx, cz), cz, height=2)


# ---- the bog, the stones, the walls --------------------------------------------------------------------------------
def standing_stones(w, r, stats):
    """The Standing Stones: twelve in a ring of twelve about the bog's middle, each two by one at the foot and four to six high, tapered,
    leaning in a block at the top; and an avenue of pairs along the boardwalk. Red's half only: the turn carries the rest."""
    n = 0
    cx = cz = -0.5
    pts = []
    for k in range(12):
        a = k * np.pi / 6 + 0.13
        pts.append((int(round(cx + 12 * np.cos(a))), int(round(cz + 12 * np.sin(a))), int(r.integers(4, 7))))
    for z in range(-28, -4, 8):
        pts.append((-6, z, 4)), pts.append((5, z, 4))
    for sx, sz, hgt in pts:
        if sz >= 0 or P.WET[sx - P.X_MIN, sz - P.Z_MIN]:
            continue
        y = P.g(sx, sz)
        for dy in range(1, hgt + 1):
            for dx in range(2 if dy < hgt - 1 else 1):
                w.set(sx + dx, y + dy, sz, *((B.STONE, 0) if r.random() < 0.55 else (B.STONE, 5) if r.random() < 0.7 else (B.COBBLE, 0)))
        w.set(sx, y + hgt, sz + (1 if sz % 2 else -1), B.STONE, 0)
        n += 1
    stats["stones"] = n


def peat_cuttings(w, r):
    """The peat cuttings: three trenches a block deep and three wide, a drying stack of coarse dirt two high along each, and a plank hut's
    worth of cover at the end: where the bog's north shore is dug."""
    for x0, z0, x1, z1 in P.CUTTINGS:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                y = P.g(x, z)
                w.set(x, y, z, B.DIRT, 1)
                w.set(x, y - 1, z, B.DIRT, 1)
        for x in range(x0 + 1, x1 - 1, 5):
            for dz in (-2, 3):
                y = P.g(x, z0)
                for dx in range(3):
                    for hgt in (1, 2):
                        w.set(x + dx, y + hgt, z0 + dz, B.DIRT, 1)


def walls_along(w, pts, gaps=(), block=(B.COBBLE_WALL, 0), moss=0.2, r=None):
    """A drystone wall one block thick along a polyline, a gap where `gaps` says (a gate)."""
    from pgmvox.shapes import walk_cells
    cells = walk_cells([(int(round(x)), int(round(z))) for x, z in pts])
    for x, z in cells:
        if any(abs(x - gx) <= 1 and abs(z - gz) <= 1 for gx, gz in gaps) or not P.LAND[x - P.X_MIN, z - P.Z_MIN] or P.WET[x - P.X_MIN, z - P.Z_MIN]:
            continue
        y = P.g(x, z)
        if w.id(x, y + 1, z) != B.AIR:
            continue
        w.set(x, y + 1, z, B.COBBLE_WALL, 1 if (r is not None and r.random() < moss) else 0)


def fold_and_fields(w, r):
    """The sheepfold: a ring of drystone round (-22, -112), a gate toward the spawn; a field wall along the Drove Road both sides, with
    gaps; the farm's three plots with haystacks."""
    cx, cz, rad = P.FOLD
    ring = [(cx + rad * np.cos(a), cz + rad * np.sin(a)) for a in np.linspace(0, 2 * np.pi, 60)]
    walls_along(w, ring + ring[:1], gaps=[(cx + rad, cz)], r=r)
    for side in (-1, 1):
        pts = [(x + side * 5, z) for x, z in P.ROADS["Drove Road"]]
        walls_along(w, pts, gaps=[(pts[1][0], pts[1][1]), (pts[3][0], pts[3][1])], r=r)
    # the haystacks by the hay barn: three blocks of hay, two high
    for sx, sz in ((14, -110), (16, -108), (12, -106)):
        y = P.g(sx, sz)
        for dy in (1, 2):
            w.set(sx, y + dy, sz, B.HAY, 0)
            w.set(sx + 1, y + dy, sz, B.HAY, 0)


def well(w):
    """The well on the green's west edge: a ring of cobble one high, water inside it, a roof post pair."""
    x, z = 22, -74
    y = P.g(x, z)
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            if (dx, dz) == (0, 0):
                w.set(x, y, z, B.COBBLE, 0)
                w.set(x, y + 1, z, B.WATER)
            else:
                w.set(x + dx, y + 1, z + dz, B.COBBLE, 0)
    for dx in (-1, 1):
        for dy in (2, 3):
            w.set(x + dx, y + dy, z, B.FENCE, 0)
    for dx in (-1, 0, 1):
        w.set(x + dx, y + 4, z, B.WOOD_SLAB, 1)


# ---- trees and ground cover -----------------------------------------------------------------------------------------
def orchards(w, R, r, stats):
    """The orchards: small oaks and olives seven apart in rows, each plot's rows true to its edge, none within four of a road or six of a cube."""
    lib = trees.library()
    by = trees.kinds(lib)
    n = 0
    from scipy import ndimage
    near_road = ndimage.binary_dilation(R.mask("road", "boardwalk"), structure=np.ones((3, 3), bool), iterations=6)
    for name, (x0, z0, x1, z1) in P.ORCHARDS:
        for gx in range(x0 + 2, x1 - 1, 8):
            for gz in range(z0 + 2, z1 - 1, 8):
                x, z = gx + int(r.integers(-1, 2)), gz + int(r.integers(-1, 2))
                if R.kind(x, z) not in ("orchard",) or min(abs(x - P.B_CENTRE[0]), abs(z - P.B_CENTRE[1])) < 8:
                    continue
                if near_road[x - P.X_MIN, z - P.Z_MIN]:
                    continue
                pool = [t for t in by["tiny-oak"] + by["small-olive"] if t.crown <= 5]
                t = pool[int(r.integers(len(pool)))]
                if trees.plant(w, x, z, t, turn=int(r.integers(4))):
                    n += 1
    stats["orchard trees"] = n


def boulder(w, sx, sz, r):
    y = P.g(sx, sz)
    s = int(r.integers(2, 4))
    for dx in range(s):
        for dz in range(s):
            hgt = max(1, s - 1 - (abs(dx - 1) + abs(dz - 1)) // 2)
            for dy in range(1, hgt + 1):
                w.set(sx + dx, y + dy, sz + dz, *((B.STONE, 0) if r.random() < 0.5 else (B.STONE, 5)))


def boulders(w, R, r, stats):
    """Boulders and rock: the original spots, then forty more drawn from the moor's ground, ten or more apart, on the hill's skirts, the
    heather and the bog's edge: never on a road, the green, water, within eight of a monument or four of a house, and never in a lane."""
    from scipy import ndimage
    n = 0
    spots = [(-66, -96), (-70, -60), (-58, -40), (-86, -88), (-24, -96), (-10, -120), (52, -100), (62, -90), (78, -76), (74, -40),
             (60, -34), (-72, -20), (-46, -28), (-30, -100), (-8, -64), (4, -58), (40, -100), (70, -110), (-84, -110), (86, -18)]
    houses = np.zeros(P.H.shape, bool)
    for hs in P.houses().values():
        for x, z in hs["cells"]:
            houses[x - P.X_MIN, z - P.Z_MIN] = True
    near_house = ndimage.binary_dilation(houses, iterations=4)
    near_road = ndimage.binary_dilation(R.mask("road", "boardwalk", "green"), iterations=2)
    X, Z = w.grid()
    ok = P.LAND & (Z < -3) & R.mask("ground") & ~near_house & ~near_road & ~P.WET & (P.H > P.BOG)
    for cx, cz in (P.A_CENTRE, P.B_CENTRE):
        ok &= np.hypot(X - cx, Z - cz) > 10
    cand = np.argwhere(ok)
    r.shuffle(cand)
    for i, k in cand:
        if len(spots) >= 20 + 40:
            break
        x, z = int(X[i, k]), int(Z[i, k])
        if all((x - sx) ** 2 + (z - sz) ** 2 >= 100 for sx, sz in spots):
            spots.append((x, z))
    for sx, sz in spots:
        if not R.inside(sx, sz) or R.kind(sx, sz) in ("water", "road", "green", "wall", "void", "room", "door"):
            continue
        boulder(w, sx, sz, r)
        n += 1
    stats["boulders"] = n


def moor_trees(w, R, r, stats):
    """Copses on the moor: twelve clumps of small oaks, birches, olives and spruces, each within eight of a centre drawn from the open
    ground, never on a road, the green, the bog, the hill or within eight of a monument; their crowns never reach a road (four clear)."""
    from scipy import ndimage
    lib = trees.library()
    by = trees.kinds(lib)
    by = {k: [t for t in v if t.crown <= 6] for k, v in by.items() if k in ("tiny-oak", "birch", "small-olive", "tiny-spruce")}
    by = {k: v for k, v in by.items() if v}
    weights = {k: {"tiny-oak": 4, "birch": 2, "small-olive": 2, "tiny-spruce": 1}[k] for k in by}
    X, Z = w.grid()
    deg = T_slope()
    near_road = ndimage.binary_dilation(R.mask("road", "boardwalk", "green", "door", "peat"), iterations=7)
    near_house = np.zeros(P.H.shape, bool)
    for hs in P.houses().values():
        for x, z in hs["cells"]:
            near_house[x - P.X_MIN, z - P.Z_MIN] = True
    near_house = ndimage.binary_dilation(near_house, iterations=5)
    base = P.LAND & (Z < -3) & R.mask("ground") & ~near_road & ~near_house & ~ndimage.binary_dilation(P.WET, iterations=3) & (P.H > P.BOG + 1) & (deg < 25)
    for cx, cz in (P.A_CENTRE, P.B_CENTRE):
        base &= np.hypot(X - cx, Z - cz) > 12
    base &= np.hypot(X - P.A_CENTRE[0], Z - P.A_CENTRE[1]) > 38                       # not on the hill
    cand = np.argwhere(base)
    r.shuffle(cand)
    centres = []
    for i, k in cand:
        c = (int(X[i, k]), int(Z[i, k]))
        if all((c[0] - a) ** 2 + (c[1] - b) ** 2 >= 18 ** 2 for a, b in centres):
            centres.append(c)
        if len(centres) >= 12:
            break
    planted = []
    n = 0
    ok = lambda x, z, t: w.id(x, P.g(x, z), z) in (B.GRASS, B.MYCELIUM) and not near_road[x - P.X_MIN, z - P.Z_MIN]        # noqa: E731
    for cx, cz in centres:
        zone = base & (np.hypot(X - cx, Z - cz) <= 8)
        n += trees.scatter(w, zone, by, weights, r, spacing=1.5, tries=40, planted=planted, ok=ok)
    stats["moor trees"] = n


def T_slope():
    return T.slope_deg(P.H, P.LAND)


def cover(w, R, r, stats):
    """Ground cover: allium on the heather, ferns and tall grass on the moor's turf, none within five of a cube, none on a road."""
    X, Z = w.grid()
    n = 0
    for i, k in np.argwhere(P.LAND & (Z < 0)):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(P.H[i, k])
        if w.id(x, h, z) not in (B.GRASS, B.MYCELIUM, B.DIRT) or w.id(x, h + 1, z) != B.AIR:
            continue
        if min(abs(x - P.A_CENTRE[0]), abs(z - P.A_CENTRE[1])) < 6 or min(abs(x - P.B_CENTRE[0]), abs(z - P.B_CENTRE[1])) < 6:
            continue
        c = r.random()
        if w.id(x, h, z) == B.MYCELIUM:
            if c < 0.18:
                w.set(x, h + 1, z, B.FLOWER, 2)
                n += 1
        elif w.id(x, h, z) == B.GRASS:
            if c < 0.07:
                w.set(x, h + 1, z, B.TALLGRASS, 2 if r.random() < 0.5 else 1)
                n += 1
    stats["cover"] = n


def rim(w, r, stats):
    """The island's rim: vines hung on the cliff's faces, a few, so the bare rock carries something; the skirt's ledges are forms.skirt's."""
    X, Z = w.grid()
    from pgmvox.shapes import edge_depth
    ed = edge_depth(P.LAND)
    n = 0
    for i, k in np.argwhere(P.LAND & (ed == 0) & (Z < 0)):
        if r.random() > 0.07:
            continue
        x, z, h = int(X[i, k]), int(Z[i, k]), int(P.H[i, k])
        for dx, dz, bit in ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1)):
            if not P.LAND[i + dx, k + dz] if 0 <= i + dx < P.LAND.shape[0] and 0 <= k + dz < P.LAND.shape[1] else True:
                for y in range(h - 2, h - 2 - int(r.integers(3, 9)), -1):
                    if w.id(x + dx, y, z + dz) == B.AIR and w.id(x, y, z) != B.AIR:
                        w.set(x + dx, y, z + dz, B.VINE, bit)
                        n += 1
                break
    stats["rim vines"] = n


def lamps(w):
    for x, z in ((24, -78), (36, -76), (24, -64), (36, -62), (8, -96), (-2, -108), (30, -42)):
        props.lamp(w, x, P.g(x, z), z, height=2)


def spawn(w, r):
    """The spawn's iron (a cube of three, mined and grown back) and the fold's trough."""
    x0, z0 = -14, -106
    y = P.g(x0, z0)
    for dx in range(3):
        for dy in range(3):
            for dz in range(3):
                w.set(x0 + dx, y + 1 + dy, z0 + dz, B.IRON_ORE, 0)


def everything(w, R, deg, O, stats):
    r = noise_rng("dress")
    houses(w, r, stats)
    abbey(w, r, stats)
    gatehouse(w, r)
    monuments(w, r)
    standing_stones(w, r, stats)
    peat_cuttings(w, r)
    fold_and_fields(w, r)
    well(w)
    orchards(w, R, r, stats)
    moor_trees(w, R, r, stats)
    boulders(w, R, r, stats)
    cover(w, R, r, stats)
    rim(w, r, stats)
    lamps(w)
    spawn(w, r)
    crypt.finish(w, stats)
    steps_on_slopes(w)


def steps_on_slopes(w):
    """The Hill Track's and the Monks' Way's climbs take a stair wherever the ground rises a block (route.steps)."""
    from pgmvox import route as RT
    for name in ("Hill Track", "Monks' Way"):
        RT.steps(w, P.H, P.X, P.Z, P.ROADS[name], block=B.COBBLE_STAIRS, width=2)


def noise_rng(name):
    from pgmvox import rng
    return rng(P.BOARD, name)
