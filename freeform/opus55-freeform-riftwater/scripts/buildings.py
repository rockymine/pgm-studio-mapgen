"""Everything somebody built: the market town and its streets, the gaol over the cellar, the chapel, the
inn, Ironhollow's cottages and headframe and smithy, the watch house at the spawn, the mill with its wheel
and weir, the outlet footbridge, the stone bridge, the Old Bridge's broken stub, and the monuments.
"""
import numpy as np

import plan as P
from mc import B
from house import house, site, furnish, STYLES
from noise import spline

RNG = np.random.default_rng(4242)

# ---- materials laid rather than grown (see WHAT-A-BOARD-IS-MADE-OF: paths are three of one tone) -------
HARD = [(B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0)]                 # town streets
SOFT = [(B.DIRT, 1), (B.DIRT, 0), (B.GRAVEL, 0)]                    # village lanes, field roads
FOREST = [(B.DIRT, 2), (B.DIRT, 1), (B.DIRT, 0)]                    # forest paths: podzol, coarse, dirt
FLOOR = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]  # the square: a built floor
MONUMENT_BLOCK = B.OBSIDIAN

RECORDS = []


def H(L, x, z):
    return int(L.H[x - L.x0, z - L.z0])


def set_ground(w, L, x, z, y, mat):
    """Make (x, z)'s ground exactly y with `mat` on top, cutting or filling the column."""
    ix, iz = x - L.x0, z - L.z0
    if not (0 <= ix < L.nx and 0 <= iz < L.nz) or not L.land[ix, iz] or L.water[ix, iz] > 0:
        return
    old = int(L.H[ix, iz])
    if y < old:
        for yy in range(y + 1, old + 1):
            w.set(x, yy, z, B.AIR)
    for yy in range(min(old, y), y):
        if w.id(x, yy, z) in (B.AIR, B.GRASS):
            w.set(x, yy, z, B.DIRT)
    # clear plants standing on it
    for yy in range(y + 1, y + 3):
        if w.id(x, yy, z) in (B.TALLGRASS, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT):
            w.set(x, yy, z, B.AIR)
    w.set(x, y, z, *mat)
    L.H[ix, iz] = y


def pave(w, L, pts, width, mats, cell=1, flatten=2, keep_built=True, wander=0.0):
    """Lay a path along a spline through pts: `width` blocks wide, its ground eased to a smoothed centreline
    height (no more than `flatten` from where it was), a third each of three blocks."""
    sp = spline(pts, 0.5)
    if wander:
        sp = [(x + wander * np.sin(i / 9.0), z + wander * np.cos(i / 11.0)) for i, (x, z) in enumerate(sp)]
    hs = np.array([H(L, int(round(x)), int(round(z))) for x, z in sp], float)
    k = 9
    pad = np.pad(hs, k, mode="edge")
    sm = np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="same")[k:-k]
    done = set()
    r = width / 2.0
    for (x, z), y in zip(sp, sm):
        for dx in range(-int(r) - 1, int(r) + 2):
            for dz in range(-int(r) - 1, int(r) + 2):
                X, Z = int(round(x + dx)), int(round(z + dz))
                if (X, Z) in done or np.hypot(X - x, Z - z) > r:
                    continue
                ix, iz = X - L.x0, Z - L.z0
                if not (0 <= ix < L.nx and 0 <= iz < L.nz) or not L.land[ix, iz] or L.water[ix, iz] > 0:
                    continue
                top_id = w.id(X, H(L, X, Z), Z)
                if keep_built and top_id not in (B.GRASS, B.DIRT, B.STONE, B.GRAVEL, B.SAND, B.COBBLE):
                    continue
                if w.id(X, H(L, X, Z) + 1, Z) not in (B.AIR, B.TALLGRASS, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT):
                    continue
                done.add((X, Z))
                old = H(L, X, Z)
                ty = int(round(y))
                if abs(ty - old) > flatten:
                    ty = old + int(np.sign(ty - old)) * flatten
                m = mats[RNG.integers(len(mats))] if cell == 1 else mats[((X // cell) * 7 + (Z // cell) * 13) % len(mats)]
                set_ground(w, L, X, Z, ty, m)
    return sp


def path_to_door(w, L, rec, mats):
    """A short paved run from a door's step to wherever the nearest paving is."""
    ox, oz = rec["out"]
    dx, dz = ox - rec["door"][0], oz - rec["door"][1]
    for i in range(0, 6):
        X, Z = ox + dx * i, oz + dz * i
        y = H(L, X, Z)
        top = w.id(X, y, Z)
        if i > 0 and (top, w.get(X, y, Z)[1]) in [m for m in mats] + HARD + SOFT and top != B.DIRT:
            break
        for k in (-1, 0, 1) if i > 0 else (0,):
            XX, ZZ = X + (k if dz else 0), Z + (k if dx else 0)
            if w.id(XX, H(L, XX, ZZ) + 1, ZZ) == B.AIR:
                set_ground(w, L, XX, ZZ, min(rec["floor"], H(L, XX, ZZ)) if i > 0 else rec["floor"], mats[RNG.integers(len(mats))])


# ---------------------------------------------------------------------------------------------------------
def square(w, L):
    """Market Square: a level built floor, a stone kerb, the monument standing open in the middle."""
    x0, z0, x1, z1 = -76, -53, -57, -35
    y = 52
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            # rounded corners
            cx = max(x0 + 3 - x, 0, x - (x1 - 3)); cz = max(z0 + 3 - z, 0, z - (z1 - 3))
            if np.hypot(cx, cz) > 3.2:
                continue
            m = FLOOR[((x // 3) * 5 + (z // 3) * 3 + (x * z) % 2) % 4]
            set_ground(w, L, x, z, y, m)
    L.square = (x0, z0, x1, z1, y)


def monument(w, L, x, z, ground):
    """The destroyable: two obsidian blocks stacked, floating two over the ground, as PGM monuments do."""
    base = ground + 2
    w.set(x, base, z, MONUMENT_BLOCK)
    w.set(x, base + 1, z, MONUMENT_BLOCK)
    return (x, base, z)


# ---------------------------------------------------------------------------------------------------------
def town(w, L):
    recs = []
    T = lambda *a, **k: recs.append(house(w, L, *a, style=k.pop("style", "town"), **k))
    # the town hall closes the square's north side
    T(-74, -64, -59, -56, storeys=2, door="s", kind="hall", floor_y=52)
    # Main Street, north side
    T(-54, -56, -48, -48, storeys=2, door="s", kind="house")
    T(-46, -55, -41, -48, storeys=3, door="s", kind="shop")
    T(-36, -56, -29, -48, storeys=2, door="s", kind="house")
    T(-27, -54, -22, -48, storeys=2, door="s", kind="bakery")
    T(-20, -55, -15, -48, storeys=2, door="s", kind="house")
    # Main Street, south side
    T(-37, -40, -30, -33, storeys=2, door="n", kind="house")
    T(-27, -40, -21, -34, storeys=2, door="n", kind="shop")
    T(-18, -40, -14, -35, storeys=1, door="n", kind="house")
    # the gaol, on the square's south-east corner, over the cellar
    T(-56, -38, -48, -30, storeys=2, door="w", kind="gaol", floor_y=52, style="stone")
    # Bridge Street
    T(-49, -26, -43, -19, storeys=2, door="e", kind="house")
    T(-48, -15, -43, -11, storeys=1, door="e", kind="house")
    T(-33, -28, -24, -17, storeys=2, door="w", kind="inn")
    # North Lane
    T(-34, -78, -28, -70, storeys=2, door="s", kind="house")
    T(-24, -80, -18, -73, storeys=2, door="s", kind="house")
    T(-69, -80, -61, -72, storeys=1, door="s", kind="shop")
    return recs


def gaol_stair(w, L):
    """A ladder from the gaol's floor down into the cellar's north-east corner."""
    x, z = -50, -36
    for y in range(43, 53):
        w.set(x, y, z, B.AIR)
        w.set(x, y, z + 1, B.STONEBRICK, 0) if y < 52 else None
        w.set(x, y, z, B.LADDER, 2)
    w.set(x, 53, z, B.AIR)
    w.set(x, 54, z, B.AIR)


def chapel(w, L):
    """A stone nave with a belfry tower at its west end: the tallest thing in town, laddered to the bells."""
    rec = house(w, L, -50, -80, -38, -71, storeys=2, style="stone", door="s", kind="chapel",
                chimney=False, along_x=True)
    f = rec["floor"]
    dy = f - 52
    # pews and an altar
    for x in range(-48, -41, 2):
        for z in (-77, -76, -74, -73):
            w.set(x, 53 + dy, z, B.SPRUCE_STAIRS, 0)
    w.set(-40, 53 + dy, -76, B.QUARTZ); w.set(-40, 53 + dy, -75, B.QUARTZ); w.set(-40, 54 + dy, -76, B.TORCH, 5)
    # the upper floor is a gallery: open the middle so the nave is tall
    for x in range(-48, -40):
        for z in range(-78, -72):
            w.set(x, 56 + dy, z, B.AIR)
    # tall windows
    for x in (-47, -44, -41):
        for z in (-80, -71):
            for y in range(54 + dy, 59 + dy):
                w.set(x, y, z, B.PANE)
    # the tower
    tx0, tz0, tx1, tz1 = -55, -79, -51, -73
    site(w, L, tx0, tz0, tx1, tz1, f)
    top = f + 20
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            edge = x in (tx0, tx1) or z in (tz0, tz1)
            for y in range(f, top + 1):
                if edge:
                    corner = x in (tx0, tx1) and z in (tz0, tz1)
                    w.set(x, y, z, *((B.STONE, 6) if corner else (B.STONEBRICK, 0)))
                else:
                    w.set(x, y, z, B.AIR if y > f else B.PLANKS, 5)
    # belfry openings near the top, and the bell
    for y in (top - 4, top - 3, top - 2):
        for d in (-1, 0, 1):
            w.set(tx0 + 2 + d, y, tz0, B.AIR); w.set(tx0 + 2 + d, y, tz1, B.AIR)
            w.set(tx0, y, tz0 + 3 + d, B.AIR); w.set(tx1, y, tz0 + 3 + d, B.AIR)
    for x in range(tx0 + 1, tx1):
        for z in range(tz0 + 1, tz1):
            w.set(x, top - 5, z, B.PLANKS, 5)
    w.set(tx0 + 2, top - 1, tz0 + 3, B.FENCE)
    w.set(tx0 + 2, top - 2, tz0 + 3, B.GOLD_BLOCK)
    # a ladder up the inside, a hatch in the belfry floor
    for y in range(f + 1, top - 4):
        w.set(tx0 + 1, y, tz0 + 1, B.LADDER, 3)
    w.set(tx0 + 1, top - 5, tz0 + 1, B.LADDER, 3)
    # door from the nave into the tower, and from the lane
    for y in (f + 1, f + 2):
        w.set(tx1, y, -76, B.AIR)
        w.set(tx0 + 2, y, tz1, B.AIR)
    w.set(tx0 + 2, f + 1, tz1, B.DARK_OAK_DOOR, 1); w.set(tx0 + 2, f + 2, tz1, B.DARK_OAK_DOOR, 8)
    # the spire: a pyramid of dark oak stairs
    for k in range(4):
        for x in range(tx0 - 1 + k, tx1 + 2 - k):
            for z in range(tz0 - 1 + k, tz1 + 2 - k):
                edge = x in (tx0 - 1 + k, tx1 + 1 - k) or z in (tz0 - 1 + k, tz1 + 1 - k)
                if edge:
                    w.set(x, top + 1 + k, z, B.PLANKS, 5)
    w.set(tx0 + 2, top + 5, tz0 + 3, B.FENCE); w.set(tx0 + 2, top + 6, tz0 + 3, B.FENCE)
    rec["tower_top"] = top
    return rec


def inn_sign(w, L, inn):
    w.sign(-34, inn["floor"] + 2, -21, ["The Falls Inn", "", "rooms & ale", ""], wall_facing=4)


# ---------------------------------------------------------------------------------------------------------
def village(w, L):
    recs = []
    V = lambda *a, **k: recs.append(house(w, L, *a, style=k.pop("style", "village"), **k))
    V(-98, 38, -92, 44, storeys=1, door="e", kind="cottage")
    main = house(w, L, -99, 49, -92, 55, storeys=2, style="village", door="e", kind="house")
    recs.append(main)
    # a low wing against the tall house: one storey, its ridge across the main ridge
    recs.append(house(w, L, -98, 46, -93, 48, storeys=1, style="village", door="e", kind="none", along_x=True,
                      floor_y=main["floor"], chimney=False, windows=True))
    V(-97, 61, -91, 68, storeys=1, door="e", kind="cottage", along_x=False)
    big = house(w, L, -90, 71, -82, 76, storeys=2, style="village", door="n", kind="house")
    recs.append(big)
    recs.append(house(w, L, -95, 72, -91, 76, storeys=1, style="village", door="n", kind="none", along_x=False,
                      floor_y=big["floor"], chimney=True))
    V(-79, 69, -74, 75, storeys=1, door="n", kind="cottage", along_x=False)
    eng = house(w, L, -80, 49, -75, 55, storeys=1, style="stone", door="w", kind="engine", chimney=False)
    recs.append(eng)
    # the engine house's stack: the tallest made thing in Ironhollow after the headframe
    f = eng["floor"]
    for y in range(f + 1, f + 19):
        for dx in (0, 1):
            for dz in (0, 1):
                w.set(-74 + dx, y, 50 + dz, B.BRICK)
    for dx in (-1, 0, 1, 2):
        for dz in (-1, 0, 1, 2):
            if dx in (-1, 2) or dz in (-1, 2):
                w.set(-74 + dx, f + 18, 50 + dz, B.BRICK)
    w.set(-74, f + 18, 50, B.AIR); w.set(-73, f + 18, 51, B.AIR)
    smith = house(w, L, -78, 59, -72, 64, storeys=1, style="village", door="w", kind="smithy")
    # the forge is open on its lane side: take out the wall between the posts
    for z in range(60, 64):
        for y in range(smith["floor"] + 1, smith["floor"] + 4):
            w.set(-78, y, z, B.AIR)
    f = smith["floor"]
    w.set(-75, f + 1, 61, B.ANVIL, 0)
    w.set(-73, f + 1, 60, B.FURNACE, 4); w.set(-73, f + 1, 61, B.FURNACE, 4)
    w.set(-73, f + 1, 63, B.CAULDRON, 3)
    w.set(-74, f + 1, 63, B.CHEST, 2)
    recs.append(smith)
    return recs


def well(w, L, x, z):
    y = H(L, x, z)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            set_ground(w, L, x + dx, z + dz, y, (B.COBBLE, 0))
            if dx or dz:
                w.set(x + dx, y + 1, z + dz, B.COBBLE_WALL)
    for yy in range(y - 6, y + 1):
        w.set(x, yy, z, B.WATER if yy < y else B.WATER)
    for dx, dz in ((-1, -1), (1, 1)):
        w.set(x + dx, y + 2, z + dz, B.SPRUCE_FENCE)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(x + dx, y + 3, z + dz, B.WOOD_SLAB, 1)
    w.set(x, y + 2, z, B.SPRUCE_FENCE)


def headframe(w, L):
    """The winding tower over the shaft: four spruce legs braced to a head, a wheel at the top."""
    sx, sz = -84, 56
    g = L.shaft_top
    # collar: a plank floor round the shaft mouth, the shaft itself open with its ladder
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            if max(abs(dx), abs(dz)) >= 2:
                set_ground(w, L, sx + dx, sz + dz, g, (B.PLANKS, 1))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(sx + dx, g, sz + dz, B.AIR)
    w.set(sx, g, sz + 1, B.LADDER, 2)
    top = g + 17
    for dx, dz in ((-3, -3), (-3, 3), (3, -3), (3, 3)):
        for y in range(g + 1, top + 1):
            # legs lean in: step in by one every five blocks
            k = (y - g) // 6
            lx = sx + dx - int(np.sign(dx)) * k
            lz = sz + dz - int(np.sign(dz)) * k
            w.set(lx, y, lz, B.LOG, 1)
    # braces and the head frame
    for y in (g + 5, g + 10, top):
        k = (y - g) // 6
        r = 3 - k
        for d in range(-r, r + 1):
            for (X, Z, ax) in ((sx + d, sz - r, 4), (sx + d, sz + r, 4), (sx - r, sz + d, 8), (sx + r, sz + d, 8)):
                w.set(X, y, Z, B.LOG, 1 | ax)
    # the winding wheel: a ring of dark oak in the x-y plane over the shaft
    cy = top + 3
    for a in np.linspace(0, 2 * np.pi, 48, endpoint=False):
        X = sx + int(round(2.6 * np.cos(a))); Y = cy + int(round(2.6 * np.sin(a)))
        w.set(X, Y, sz, B.PLANKS, 5)
    for d in (-2, -1, 1, 2):
        w.set(sx + d, cy, sz, B.DARK_OAK_FENCE); w.set(sx, cy + d, sz, B.DARK_OAK_FENCE)
    w.set(sx, cy, sz, B.LOG2, 1 | 8)
    for y in range(top + 1, cy):
        w.set(sx, y, sz, B.DARK_OAK_FENCE)
    # a platform at the head with a ladder up one leg
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(sx + dx, top, sz + dz, B.PLANKS, 1)
    leg_x = sx - 3 + (top - g) // 6
    for y in range(g + 1, top):
        k = (y - g) // 6
        w.set(sx - 2 + k, y, sz - 3 + k + 1, B.LADDER, 3) if False else None
    # a ladder up a post of its own on the north side, so it has something to hang on
    for y in range(g + 1, top):
        w.set(sx - 1, y, sz - 3, B.LOG, 1)
        w.set(sx - 1, y, sz - 2, B.LADDER, 3)
    w.set(sx - 1, top, sz - 2, B.AIR)
    # ore cart track from the collar to the bin, an ore pile
    for x in range(sx + 4, sx + 9):
        if w.id(x, H(L, x, sz) + 1, sz) == B.AIR:
            w.set(x, H(L, x, sz) + 1, sz, B.RAIL, 1)
    return top


def spoil_heap(w, L, cx, cz, r=7, h=6):
    for x in range(cx - r - 1, cx + r + 2):
        for z in range(cz - r - 1, cz + r + 2):
            d = np.hypot((x - cx) / r, (z - cz) / (r * 0.8))
            if d >= 1:
                continue
            ix, iz = x - L.x0, z - L.z0
            if not (0 <= ix < L.nx and 0 <= iz < L.nz) or not L.land[ix, iz]:
                continue
            y0 = H(L, x, z)
            top = y0 + int(round(h * (1 - d ** 1.6)))
            for y in range(y0 + 1, top + 1):
                r_ = RNG.random()
                w.set(x, y, z, *((B.GRAVEL, 0) if r_ < 0.5 else (B.COBBLE, 0) if r_ < 0.75 else (B.STONE, 5)))
            L.H[ix, iz] = top


# ---------------------------------------------------------------------------------------------------------
def watch_house(w, L):
    """Red's spawn: a framed house on the terrace with a stone tower at its back corner."""
    main = house(w, L, -102, -11, -94, -3, storeys=2, style="town", door="e", kind="spawnhall", floor_y=59)
    tower = house(w, L, -107, -10, -102, -4, storeys=4, style="stone", door="e", kind="none", floor_y=59,
                  chimney=False, along_x=False)
    # a doorway from the house into the tower on each floor
    for s in range(2):
        for y in (60 + 4 * s, 61 + 4 * s):
            w.set(-102, y, -7, B.AIR)
    # team colour: wool hung from the tower's top
    for z in range(-10, -3):
        if z % 2 == 0:
            for y in range(73, 75):
                w.set(-108, y, z, B.WOOL, 14)
    # the terrace: a stone floor in front of the door with a low wall along its edge, steps down east
    for x in range(-93, -85):
        for z in range(-12, -1):
            set_ground(w, L, x, z, 59, FLOOR[(x * 3 + z * 5) % 4])
    for z in range(-12, -1):
        if z not in (-8, -7, -6):
            w.set(-85, 60, z, B.COBBLE_WALL)
    for x in range(-93, -85):
        w.set(x, 60, -13, B.COBBLE_WALL); w.set(x, 60, -1, B.COBBLE_WALL)
    # stairs down from the terrace to the lane
    for i, x in enumerate(range(-84, -77)):
        y = 59 - i
        g = H(L, x, -7)
        if y <= g:
            break
        for z in (-8, -7, -6):
            for yy in range(min(g, y) - 1, y):
                w.set(x, yy, z, B.STONE, 0)
            w.set(x, y, z, B.STONEBRICK_STAIRS, 1)
            for yy in range(y + 1, y + 4):
                w.set(x, yy, z, B.AIR)
            L.H[x - L.x0, z - L.z0] = y
    return main, tower


def hut(w, L):
    rec = house(w, L, -107, -67, -102, -62, storeys=1, style="village", door="e", kind="cottage")
    f = rec["floor"]
    w.chest(-103, f + 1, -63, [(0, "minecraft:arrow", 24, 0), (1, "minecraft:cooked_beef", 6, 0),
                               (2, "minecraft:log", 16, 0), (13, "minecraft:iron_axe", 1, 0)], facing=2)
    # chopping block and woodpile by the door
    g = H(L, -100, -64)
    w.set(-100, g + 1, -63, B.LOG, 0)
    for z in (-67, -66, -65):
        for y in (1, 2):
            w.set(-101, g + y, z, B.LOG, 4)
    return rec


def mill(w, L):
    """The watermill on the north bank, its wheel turning in a race cut beside the river, and the weir."""
    rec = house(w, L, -67, 1, -58, 7, storeys=2, style="stone", upper_style="village", door="n", kind="mill",
                along_x=True)
    f = rec["floor"]
    # the race: water at river level in a cut along the mill's south wall, opening into the river downstream
    for x in range(-68, -53):
        for z in (9, 10, 11):
            g = H(L, x, z)
            for y in range(42, max(g, 46) + 4):
                w.set(x, y, z, B.AIR)
            w.set(x, 41, z, B.GRAVEL)
            for y in range(42, 46):
                w.set(x, y, z, B.WATER)
            L.H[x - L.x0, z - L.z0] = 41
            L.water[x - L.x0, z - L.z0] = 45
        for z in (8, 12):
            g = H(L, x, z)
            if g > 46:
                for y in range(41, g + 1):
                    w.set(x, y, z, B.STONEBRICK, 0)
    # the wheel in the race: a dark oak rim and paddles round a log axle that runs into the mill
    cx, cy = -62, 46
    for a in np.linspace(0, 2 * np.pi, 64, endpoint=False):
        for rr in (4.0, 4.6):
            X = cx + int(round(rr * np.cos(a))); Y = cy + int(round(rr * np.sin(a)))
            w.set(X, Y, 10, B.PLANKS, 5)
    for a in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        for rr in np.arange(1, 4, 0.5):
            X = cx + int(round(rr * np.cos(a))); Y = cy + int(round(rr * np.sin(a)))
            w.set(X, Y, 10, B.LOG2, 1 | 12)
    for z in range(8, 12):
        w.set(cx, cy, z, B.LOG2, 1 | 8)
    # the weir: a stone sill across the river where the pond reach drops to the river reach
    zr = L.zr[-67 - L.x0, :]
    zc = int(round(L.zr[-67 - L.x0, 0]))
    for z in range(zc - 5, zc + 6):
        ix, iz = -67 - L.x0, z - L.z0
        if L.water[ix, iz] > 0 or abs(z - zc) <= 3:
            for y in range(L.H[ix, iz], 48):
                w.set(-67, y, z, B.STONEBRICK, 0)
            w.set(-67, 48, z, B.WATER)
            w.set(-66, 47, z, B.WATER_FLOW, 8) if w.id(-66, 47, z) == B.AIR else None
            w.set(-66, 46, z, B.WATER_FLOW, 8) if w.id(-66, 46, z) == B.AIR else None
    # sacks and a millstone inside
    w.set(-60, f + 1, 3, B.DSLAB, 0); w.set(-60, f + 2, 3, B.SLAB, 0)
    for x in (-65, -64):
        w.set(x, f + 1, 2, B.HAY, 0)
    return rec


def footbridge(w, L):
    """A timber trestle bridge over the pond's outlet: the quick way from the spawn to the green."""
    x0, x1 = -72, -68
    z0, z1 = 12, 27
    deck = 50
    for z in range(z0, z1 + 1):
        # the deck eases down to the south bank
        y = deck if z < 22 else deck - (z - 21) // 2
        for x in range(x0, x1 + 1):
            if x in (x0, x1):
                w.set(x, y + 1, z, B.SPRUCE_FENCE)
                if z % 4 == 0:
                    w.set(x, y + 2, z, B.TORCH, 5) if z in (16, 24) else None
            w.set(x, y, z, B.PLANKS if x not in (x0, x1) else B.LOG, 1 if x not in (x0, x1) else 1 | 8)
            for yy in range(y + 1, y + 4):
                if x not in (x0, x1) and w.id(x, yy, z) not in (B.AIR,):
                    w.set(x, yy, z, B.AIR)
        if z % 4 == 2:
            for x in (x0, x1):
                g = H(L, x, z)
                for yy in range(g - 2, y):
                    w.set(x, yy, z, B.LOG, 1)
    # open the ends onto the lane
    for x in range(x0 + 1, x1):
        for z in (z0, z1):
            pass


def stone_bridge(w, L):
    """A hump-backed stone bridge: one arch over the river, its deck climbing from the field bank to a crown
    over the water and easing onto the town bluff, stepped with stairs so it walks rather than jumps."""
    x0, x1 = -38, -34
    zN, zS = -10, 14
    zc, half = 3, 6.5
    yN = int(np.median([H(L, x, zN - 1) for x in range(x0, x1 + 1)]))
    yS = int(np.median([H(L, x, zS + 1) for x in range(x0, x1 + 1)]))
    crown = max(yN, yS) + 1
    def deck_y(z):
        if z <= 1:
            return int(round(yN + (crown - yN) * (z - zN) / (1 - zN)))
        return int(round(crown - (crown - yS) * (z - 1) / (zS - 1)))
    for z in range(zN, zS + 1):
        dy = deck_y(z)
        prev, nxt = deck_y(z - 1), deck_y(z + 1)
        t = (z - zc) / half
        soffit = int(round(45 + 5.2 * np.sqrt(1 - t * t))) if abs(t) < 1 else None
        for x in range(x0, x1 + 1):
            ix, iz = x - L.x0, z - L.z0
            ground = int(L.H[ix, iz])
            lo = (soffit + 1) if soffit is not None else min(ground, dy) - 1
            for y in range(lo, dy):
                ring = soffit is not None and y == soffit + 1
                keystone = ring and abs(z - zc) < 1
                w.set(x, y, z, B.STONEBRICK, 3 if keystone else (0 if (y * 3 + z) % 9 else 2))
            if soffit is not None:
                for y in range(46, soffit + 1):
                    w.set(x, y, z, B.AIR)
            # the deck: a stair where it climbs toward the crown, a built floor where it is level
            if nxt > dy and z < 1:
                w.set(x, dy + 1, z, B.STONEBRICK_STAIRS, 2)
                w.set(x, dy, z, B.STONEBRICK, 0)
            elif prev > dy and z > 1:
                w.set(x, dy + 1, z, B.STONEBRICK_STAIRS, 3)
                w.set(x, dy, z, B.STONEBRICK, 0)
            else:
                w.set(x, dy, z, *FLOOR[(x + z) % 4])
            for y in range(dy + 2 if (nxt > dy and z < 1) or (prev > dy and z > 1) else dy + 1, dy + 5):
                if x not in (x0, x1):
                    w.set(x, y, z, B.AIR)
            if x in (x0, x1):
                top = dy + 1 if not ((nxt > dy and z < 1) or (prev > dy and z > 1)) else dy + 2
                w.set(x, top, z, B.STONEBRICK, 0)
                w.set(x, top + 1, z, B.SLAB, 5)
                for y in range(top + 2, top + 4):
                    w.set(x, y, z, B.AIR)
            L.H[ix, iz] = max(L.H[ix, iz], dy + (1 if (nxt > dy and z < 1) or (prev > dy and z > 1) else 0))
    # cutwaters at the arch's feet and lamps at its ends
    for pz in (zc - 7, zc + 7):
        for x in (x0 - 1, x1 + 1):
            g = int(L.H[x - L.x0, pz - L.z0])
            for y in range(min(g, 44), 49):
                w.set(x, y, pz, B.STONEBRICK, 0)
            w.set(x, 49, pz, B.SLAB, 5)
    for z, x in ((zN, x0), (zN, x1), (zS, x0), (zS, x1)):
        y = deck_y(z) + 2
        w.set(x, y, z, B.STONEBRICK, 0); w.set(x, y + 1, z, B.FENCE); w.set(x, y + 2, z, B.GLOWSTONE)


def old_bridge(w, L):
    """The Old Bridge's stub: Main Street carried out over the rift on a half-arch springing from the rift
    face, broken off where the middle span fell. The deck runs out six blocks; the arch ring curls up under
    it from ten blocks down the face; the break is ragged, its parapet gone first."""
    zc = -44
    face = -12
    deck = H(L, -15, -44)
    end = -5
    rng = np.random.default_rng(17)
    for x in range(face - 3, end + 1):
        out = x - face                        # 0 at the face, 7 at the end
        for z in range(zc - 3, zc + 4):
            edge = abs(z - zc) == 3
            k = (x - face) / (end - face)
            # ragged break: the last blocks survive by chance, less near the parapet
            if x >= end - 1 and rng.random() < (0.45 if x == end else 0.2) + (0.3 if edge else 0):
                continue
            soffit = int(round(deck - 2 - 9 * (1 - k) ** 2)) if x >= face else deck - 12
            ring = soffit
            for y in range(soffit, deck):
                if x < face and w.id(x, y, z) not in (B.AIR,):
                    continue
                w.set(x, y, z, B.STONEBRICK, 0 if (y + z + x) % 5 else 2)
            if x >= face:
                w.set(x, ring, z, B.STONEBRICK, 3 if (z == zc and x == face + 3) else 0)
            if edge:
                # the parapet, broken first at the end
                if not (x >= end - 2 and rng.random() < 0.6):
                    w.set(x, deck, z, B.STONEBRICK, 0)
                    w.set(x, deck + 1, z, B.SLAB, 5)
            else:
                w.set(x, deck, z, *FLOOR[(x * 7 + z * 3) % 4])
                for y in range(deck + 1, deck + 4):
                    if x >= face - 1:
                        w.set(x, y, z, B.AIR)
    # what hangs from the break: iron ties and a fallen voussoir caught on them
    for z in (zc - 1, zc + 1):
        for y in range(deck - 4, deck):
            w.set(end + 1, y, z, B.IRON_BARS)
    w.set(end + 1, deck - 5, zc - 1, B.STONEBRICK, 2)
    # lamps at the bridge head, on the land
    for z in (zc - 3, zc + 3):
        g = H(L, face - 2, z)
        w.set(face - 2, deck + 1, z, B.STONEBRICK, 0)
        w.set(face - 2, deck + 2, z, B.FENCE); w.set(face - 2, deck + 3, z, B.GLOWSTONE)


def build(w, L):
    square(w, L)
    recs = town(w, L)
    gaol_stair(w, L)
    recs.append(chapel(w, L))
    inn_sign(w, L, [r for r in recs if r['kind'] == 'inn'][0])
    recs += village(w, L)
    well(w, L, -87, 46)
    L.headframe_top = headframe(w, L)
    spoil_heap(w, L, -101, 79)
    recs += list(watch_house(w, L))
    recs.append(hut(w, L))
    recs.append(mill(w, L))
    footbridge(w, L)
    stone_bridge(w, L)
    old_bridge(w, L)
    # streets and lanes, after the houses so they run to the doors
    for r in P.ROUTES:
        mats = {"street": HARD, "lane": SOFT, "path": FOREST}[r["kind"]]
        width = {"street": 5, "lane": 3, "path": 2}[r["kind"]]
        pave(w, L, r["pts"], width, mats, wander=1.2 if r["kind"] != "street" else 0.0)
    for rec in recs:
        if rec.get("kind") in ("none", "chapel"):
            continue
        mats = HARD if rec["style"] in ("town", "stone") and rec["x0"] > -80 and rec["z0"] < 0 else SOFT
        path_to_door(w, L, rec, mats)
    # monuments last, over the finished ground
    L.monuments = {}
    for key, (mx, mz) in P.MONUMENTS.items():
        g = H(L, mx, mz)
        L.monuments[key] = monument(w, L, mx, mz, g)
    L.records = recs
