"""Everything somebody built: Gilt — its false-front Main Street, the adobe quarter, the plaza round the
spring, the chapel, the water tower — the tipple and the bench tram with its trestle over the Wash, the Mule
Trail cut into the wall, the headframe over the Throat, Fort Ochre, the Rancho, the windmills, the ladders up
the buttes.

Two built families, per the plan: timber (spruce posts, oak plank walls, spruce false fronts, dark oak roofs)
and adobe (smooth sandstone walls, sandstone courses, spruce vigas, flat roofs with parapets).
"""
import numpy as np

import plan as P
from mc import B
from noise import spline

RNG = np.random.default_rng(909)
HARD = [(B.GRAVEL, 0), (B.DIRT, 1), (B.HARDENED_CLAY, 0)]     # Gilt's streets: packed earth and gravel
TRACK = [(B.DIRT, 1), (B.DIRT, 0), (B.GRAVEL, 0)]              # tracks on the mesa
PAVE = [(B.SANDSTONE, 2), (B.SANDSTONE, 0), (B.STAINED_CLAY, 0), (B.HARDENED_CLAY, 0)]   # the plaza
RECORDS = []


def H(L, x, z):
    return int(L.H[x - L.x0, z - L.z0])


def set_ground(w, L, x, z, y, mat=None):
    ix, iz = x - L.x0, z - L.z0
    if not (0 <= ix < L.nx and 0 <= iz < L.nz) or not L.land[ix, iz] or L.water[ix, iz]:
        return
    old = int(L.H[ix, iz])
    for yy in range(y + 1, max(old, y) + 4):
        if w.id(x, yy, z) not in (B.AIR, B.LOG, B.LOG2, B.PLANKS, B.SANDSTONE, B.OBSIDIAN):
            w.set(x, yy, z, B.AIR)
    for yy in range(min(old, y), y):
        if w.id(x, yy, z) == B.AIR:
            w.set(x, yy, z, B.STAINED_CLAY, 1)
    if mat:
        w.set(x, y, z, *mat)
    elif w.id(x, y, z) == B.AIR:
        w.set(x, y, z, B.STAINED_CLAY, 1)
    L.H[ix, iz] = y


def claim(L, name, box):
    """Record what stands where, and note anything it overlaps: two things in one place is a mistake."""
    a0, b0, a1, b1 = box
    for other, (c0, d0, c1, d1) in L.things:
        if a0 <= c1 and c0 <= a1 and b0 <= d1 and d0 <= b1:
            L.conflicts.append((name, other, box))
    L.things.append((name, box))


def site(w, L, x0, z0, x1, z1, y, margin=1, name="building"):
    for x in range(x0 - margin, x1 + margin + 1):
        for z in range(z0 - margin, z1 + margin + 1):
            if any(a <= x <= c and b <= z <= d for a, b, c, d in L.footprints):
                continue
            set_ground(w, L, x, z, y, None if (x0 <= x <= x1 and z0 <= z <= z1) else None)
    L.footprints.append((x0, z0, x1, z1))
    claim(L, name, (x0, z0, x1, z1))


def floor_of(L, x0, z0, x1, z1):
    return int(np.median(L.H[x0 - L.x0:x1 - L.x0 + 1, z0 - L.z0:z1 - L.z0 + 1]))


def door(w, x, y, z, side, block=B.SPRUCE_DOOR):
    f = {"e": 0, "s": 1, "w": 2, "n": 3}[side]
    w.set(x, y + 1, z, block, f)
    w.set(x, y + 2, z, block, 8)


def out_of(side):
    return {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[side]


def gable(w, x0, z0, x1, z1, y, along_x, stair, gable_mat, ridge):
    """A gable roof whose eaves overhang by one; the verge (stairs) is never the gable's block."""
    if along_x:
        a0, a1, b0, b1, lo, hi = x0 - 1, x1 + 1, z0 - 1, z1 + 1, 2, 3
    else:
        a0, a1, b0, b1, lo, hi = z0 - 1, z1 + 1, x0 - 1, x1 + 1, 0, 1
    k = 0
    while b0 + k <= b1 - k:
        yy = y + k
        for a in range(a0, a1 + 1):
            for b, s in ((b0 + k, lo), (b1 - k, hi)):
                X, Z = (a, b) if along_x else (b, a)
                if b0 + k == b1 - k:
                    w.set(X, yy, Z, *ridge)
                else:
                    w.set(X, yy, Z, stair, s)
        for b in range(b0 + k + 1, b1 - k):
            for a in ((x0, x1) if along_x else (z0, z1)):
                X, Z = (a, b) if along_x else (b, a)
                w.set(X, yy, Z, *gable_mat)
        k += 1
    return y + k


# ---- the timber family -------------------------------------------------------------------------
def false_front(w, L, x0, z0, x1, z1, front, storeys=1, name=None, kind="store", walls=(B.PLANKS, 0)):
    """A frontier store: plank walls between spruce posts, a gable roof running back from the street, a
    square false front standing over it, a boardwalk porch under a one-block roof, a sign on the front."""
    y = floor_of(L, x0, z0, x1, z1)
    site(w, L, x0, z0, x1, z1, y, name=kind)
    top = y + 4 * storeys
    corners = {(x0, z0), (x0, z1), (x1, z0), (x1, z1)}
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            yy = y - 1
            while yy > 0 and w.id(x, yy, z) == B.AIR:
                w.set(x, yy, z, B.STAINED_CLAY, 1); yy -= 1
            w.set(x, y, z, B.PLANKS, 1)
            edge = x in (x0, x1) or z in (z0, z1)
            for yy in range(y + 1, top + 1):
                if not edge:
                    w.set(x, yy, z, B.PLANKS, 1) if (yy - y) % 4 == 0 else w.set(x, yy, z, B.AIR)
                elif (x, z) in corners:
                    w.set(x, yy, z, B.LOG, 1)
                elif (yy - y) % 4 == 0:
                    run_x = z in (z0, z1)
                    w.set(x, yy, z, B.LOG, 1 | (4 if run_x else 8))     # the laid course at each seam
                else:
                    w.set(x, yy, z, *walls)
    along_x = front in "ns"           # the ridge runs back from the street
    ridge_along_x = not along_x
    gable(w, x0, z0, x1, z1, top + 1, ridge_along_x, B.DARK_OAK_STAIRS, (B.PLANKS, 1), (B.WOOD_SLAB, 5))
    # windows on every storey of the front and sides
    fx, fz = out_of(front)
    for s in range(storeys):
        wy = y + 2 + 4 * s
        if front in "ns":
            zf = z0 if front == "n" else z1
            for x in range(x0 + 1, x1, 2):
                if x != (x0 + x1) // 2 or s > 0:
                    w.set(x, wy, zf, B.PANE)
                    if s > 0:
                        w.set(x, wy + 1, zf, B.PANE)
        else:
            xf = x0 if front == "w" else x1
            for z in range(z0 + 1, z1, 2):
                if z != (z0 + z1) // 2 or s > 0:
                    w.set(xf, wy, z, B.PANE)
                    if s > 0:
                        w.set(xf, wy + 1, z, B.PANE)
    # the false front: the street wall carried up square past the roof, capped with a slab course
    rise = (z1 - z0 if front in "ns" else x1 - x0) // 2 + 3
    for k in range(1, rise + 1):
        cap = k == rise
        if front in "ns":
            zf = (z0 if front == "n" else z1) + fz
            for x in range(x0, x1 + 1):
                w.set(x, top + k, zf - fz, *((B.WOOD_SLAB, 1) if cap else (B.PLANKS, 1)))
        else:
            xf = (x0 if front == "w" else x1) + fx
            for z in range(z0, z1 + 1):
                w.set(xf - fx, top + k, z, *((B.WOOD_SLAB, 1) if cap else (B.PLANKS, 1)))
    # door in the middle of the front, porch and boardwalk two deep in front of it
    if front in "ns":
        dx, dz = (x0 + x1) // 2, (z0 if front == "n" else z1)
    else:
        dx, dz = (x0 if front == "w" else x1), (z0 + z1) // 2
    door(w, dx, y, dz, front)
    for k in (1, 2):
        span = range(x0, x1 + 1) if front in "ns" else range(z0, z1 + 1)
        for a in span:
            X, Z = (a, dz + fz * k) if front in "ns" else (dx + fx * k, a)
            set_ground(w, L, X, Z, y, (B.WOOD_SLAB, 1 | 8) if True else None)
            for yy in range(y + 1, y + 4):
                w.set(X, yy, Z, B.AIR)
            if k == 2 and (a - (x0 if front in "ns" else z0)) % 3 == 0:
                w.set(X, y + 1, Z, B.SPRUCE_FENCE); w.set(X, y + 2, Z, B.SPRUCE_FENCE)
            if k == 2 and (a - (x0 if front in "ns" else z0)) % 3 != 0 and kind != "saloon":
                pass
            w.set(X, y + 3, Z, B.WOOD_SLAB, 5)
    # the sign over the door
    if name:
        sx, sz = dx + fx, dz + fz
        w.sign(sx, y + 3 - 0, sz, [name[0], name[1] if len(name) > 1 else "", "", ""],
               wall_facing={"n": 2, "s": 3, "w": 4, "e": 5}[front]) if False else None
        w.set(dx + fx * 0, top - 1 if storeys > 1 else y + 3, dz, *((B.LOG, 1)))
        hx, hz = dx + fx, dz + fz
        w.sign(hx, top + 2, hz if front in "ew" else hz, name + [""] * (4 - len(name)),
               wall_facing={"n": 2, "s": 3, "w": 4, "e": 5}[front])
    furnish(w, x0, z0, x1, z1, y, kind, front)
    rec = dict(x0=x0, z0=z0, x1=x1, z1=z1, floor=y, kind=kind, front=front, door=(dx, dz), storeys=storeys)
    RECORDS.append(rec)
    return rec


def furnish(w, x0, z0, x1, z1, y, kind, front):
    ix0, iz0, ix1, iz1 = x0 + 1, z0 + 1, x1 - 1, z1 - 1

    def put(x, z, b, d=0, dy=1):
        if w.id(x, y + dy, z) == B.AIR:
            w.set(x, y + dy, z, b, d)
    if kind == "saloon":
        for x in range(ix0 + 1, ix1):
            put(x, iz1 if front != "s" else iz0, B.PLANKS, 5)          # the bar
        for x, z in ((ix0 + 1, (iz0 + iz1) // 2), (ix1 - 1, (iz0 + iz1) // 2 + 1)):
            put(x, z, B.FENCE); put(x, z, B.PLATE_WOOD, 0, 2)
        put(ix0, iz0, B.CHEST, 2)
    elif kind in ("store", "assay", "bank", "hotel", "house"):
        for z in range(iz0, iz1 + 1):
            if (z + x0) % 2:
                put(ix0, z, B.BOOKSHELF if kind == "bank" else B.CHEST, 4 if kind != "bank" else 0)
        put(ix1, iz1, B.CRAFTING)
        if kind == "assay":
            put(ix1, iz0, B.FURNACE, 4); put(ix1 - 1, iz0, B.CAULDRON); put(ix1 - 2, iz0, B.ANVIL)
        if kind == "bank":
            put(ix1, iz0, B.IRON_BLOCK); put(ix1, iz0 + 1, B.GOLD_BLOCK)
    for s_y in (y + 3,):
        mx, mz = (ix0 + ix1) // 2, (iz0 + iz1) // 2
        if w.id(ix0, s_y, mz) == B.AIR:
            w.set(ix0, s_y, mz, B.TORCH, 1)


# ---- the adobe family -------------------------------------------------------------------------
def adobe(w, L, x0, z0, x1, z1, door_side, storeys=1, kind="house", upper=None, name=None):
    """Adobe: smooth sandstone walls on a sandstone course, a flat roof behind a parapet, spruce vigas
    whose sawn ends stand out of the walls under it, shuttered windows. `upper` is a smaller box set back on
    the roof for a second storey, reached by a ladder on the roof terrace."""
    y = floor_of(L, x0, z0, x1, z1)
    site(w, L, x0, z0, x1, z1, y, name="adobe " + kind)

    def box(a0, c0, a1, c1, fy, ht, vigas=True):
        for x in range(a0, a1 + 1):
            for z in range(c0, c1 + 1):
                edge = x in (a0, a1) or z in (c0, c1)
                yy = fy - 1
                while yy > 0 and w.id(x, yy, z) == B.AIR:
                    w.set(x, yy, z, B.STAINED_CLAY, 1); yy -= 1
                if fy == y:
                    w.set(x, fy, z, *((B.SANDSTONE, 0) if edge else (B.PLANKS, 1)))
                for k in range(1, ht + 1):
                    if edge:
                        w.set(x, fy + k, z, *((B.SANDSTONE, 0) if k == 1 else (B.SANDSTONE, 2)))
                    else:
                        w.set(x, fy + k, z, B.AIR)
                # the roof and its parapet, with gaps for the rain
                w.set(x, fy + ht + 1, z, *((B.SANDSTONE, 2) if edge else (B.HARDENED_CLAY, 0)))
                if edge and (x + z) % 5:
                    w.set(x, fy + ht + 2, z, B.SANDSTONE, 2)
        if vigas:
            vy = fy + ht
            for x in range(a0 + 1, a1, 2):
                for z, dz in ((c0 - 1, -1), (c1 + 1, 1)):
                    if w.id(x, vy, z) == B.AIR:
                        w.set(x, vy, z, B.LOG, 1 | 8)       # sawn end out of the wall
        # windows with shutters
        wy = fy + 2
        for x in range(a0 + 2, a1 - 1, 3):
            for z in (c0, c1):
                w.set(x, wy, z, B.PANE)
        for z in range(c0 + 2, c1 - 1, 3):
            for x in (a0, a1):
                w.set(x, wy, z, B.PANE)

    box(x0, z0, x1, z1, y, 3)
    if door_side in "ns":
        dx, dz = (x0 + x1) // 2, (z0 if door_side == "n" else z1)
    else:
        dx, dz = (x0 if door_side == "w" else x1), (z0 + z1) // 2
    door(w, dx, y, dz, door_side)
    top = y + 4
    if upper:
        ua0, uc0, ua1, uc1 = upper
        box(ua0, uc0, ua1, uc1, top, 3)
        # a ladder from the terrace to the upper roof
        lx, lz = ua0 - 1, uc0 + 1
        if w.id(lx, top + 1, lz) == B.AIR:
            for k in range(1, 5):
                w.set(lx, top + k, lz, B.LADDER, 4)
        top = top + 4
    # a ladder up the outside to the roof terrace, on the wall opposite the door
    opp = {"n": "s", "s": "n", "e": "w", "w": "e"}[door_side]
    ox, oz = out_of(opp)
    if opp in "ns":
        lx, lz = x0 + 1, (z0 if opp == "n" else z1) + oz
    else:
        lx, lz = (x0 if opp == "w" else x1) + ox, z0 + 1
    for k in range(1, 6):
        if w.id(lx, y + k, lz) == B.AIR:
            w.set(lx, y + k, lz, B.LADDER, {"n": 2, "s": 3, "w": 4, "e": 5}[opp])
    w.set(x0 + 1, y + 1, z0 + 1, B.CRAFTING) if kind == "house" else None
    if w.id(x1 - 1, y + 1, z1 - 1) == B.AIR:
        w.set(x1 - 1, y + 1, z1 - 1, B.BED, 2); w.set(x1 - 1, y + 1, z1 - 2, B.BED, 2 | 8)
    if w.id(x0 + 1, y + 3, (z0 + z1) // 2) == B.AIR:
        w.set(x0 + 1, y + 3, (z0 + z1) // 2, B.TORCH, 1)
    if name:
        fx, fz = out_of(door_side)
        sx, sz = dx + (1 if door_side in "ns" else 0) + fx, dz + (1 if door_side in "ew" else 0) + fz
        w.sign(sx, y + 2, sz - fz + fz, name + [""] * (4 - len(name)),
               wall_facing={"n": 2, "s": 3, "w": 4, "e": 5}[door_side]) if w.id(sx, y + 2, sz) == B.AIR else None
    rec = dict(x0=x0, z0=z0, x1=x1, z1=z1, floor=y, kind=kind, front=door_side, door=(dx, dz), storeys=2 if upper else 1)
    RECORDS.append(rec)
    return rec


def chapel(w, L, x0, z0, x1, z1):
    """The mission chapel: an adobe nave with a stepped bell gable over its door, the bell in its arch."""
    rec = adobe(w, L, x0, z0, x1, z1, "e", kind="chapel")
    y = rec["floor"]
    # raise the nave walls and give it a bell gable on the door front
    zc = (z0 + z1) // 2
    for k, half in enumerate((3, 3, 2, 2, 1, 1, 0)):
        for z in range(zc - half, zc + half + 1):
            w.set(x1, y + 6 + k, z, B.SANDSTONE, 2)
    for yy in (y + 9, y + 10):
        w.set(x1, yy, zc, B.AIR)
    w.set(x1, y + 11, zc, B.SANDSTONE, 2)
    w.set(x1, y + 10, zc, B.FENCE); w.set(x1, y + 9, zc, B.GOLD_BLOCK)
    # pews and the altar
    for x in range(x0 + 3, x1 - 1, 2):
        for z in (zc - 2, zc - 1, zc + 1, zc + 2):
            if w.id(x, y + 1, z) == B.AIR:
                w.set(x, y + 1, z, B.SPRUCE_STAIRS, 1)
    w.set(x0 + 1, y + 1, zc, B.QUARTZ); w.set(x0 + 1, y + 2, zc, B.TORCH, 5)
    return rec


def water_tower(w, L, cx, cz):
    """A round plank tank on four dark oak legs with a ladder: the tallest thing in town, a perch over the
    spring and the arch's shadow."""
    g = H(L, cx, cz)
    claim(L, "water tower", (cx - 6, cz - 6, cx + 6, cz + 6))
    legs = [(cx - 3, cz - 3), (cx + 3, cz - 3), (cx - 3, cz + 3), (cx + 3, cz + 3)]
    top = g + 11
    for lx, lz in legs:
        for y in range(g + 1, top):
            w.set(lx, y, lz, B.LOG2, 1)
    for y in (g + 5, top - 1):
        for d in range(-3, 4):
            for (X, Z, ax) in ((cx + d, cz - 3, 4), (cx + d, cz + 3, 4), (cx - 3, cz + d, 8), (cx + 3, cz + d, 8)):
                w.set(X, y, Z, B.LOG2, 1 | ax)
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            d = np.hypot(x - cx, z - cz)
            if d <= 4.3:
                w.set(x, top, z, B.PLANKS, 1)
                for y in range(top + 1, top + 6):
                    if d > 3.3:
                        w.set(x, y, z, B.PLANKS, 1 if (y - top) % 3 else 5)     # hoops
                    else:
                        w.set(x, y, z, B.WATER if y < top + 5 else B.AIR)
            if 3.3 < d <= 4.3:
                w.set(x, top + 6, z, B.DARK_OAK_STAIRS, 0)
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            if np.hypot(x - cx, z - cz) <= 3.3:
                w.set(x, top + 6, z, B.WOOD_SLAB, 5)
    # ladder up the west leg's inside to a walkway round the tank
    for y in range(g + 1, top + 6):
        w.set(cx - 5, y, cz, B.LADDER, 4) if False else None
    for y in range(g + 1, top):
        w.set(cx - 4, y, cz, B.LOG2, 1)
        w.set(cx - 5, y, cz, B.LADDER, 4)
    for x in range(cx - 6, cx + 7):
        for z in range(cz - 6, cz + 7):
            d = np.hypot(x - cx, z - cz)
            if 4.3 < d <= 5.6 and w.id(x, top, z) == B.AIR:
                w.set(x, top, z, B.WOOD_SLAB, 1 | 8)
                if d > 5.0:
                    w.set(x, top + 1, z, B.SPRUCE_FENCE)
    w.set(cx - 5, top + 1, cz, B.AIR)
    return top


def spring(w, L):
    """Gilt Spring: a round pool with a sandstone kerb, gaps where the creek leaves, a pump and benches; the
    plaza round it paved in sandstone and clay."""
    cx, cz = -0.5, -0.5
    for x in range(-14, 0):
        for z in range(-13, 13):
            d = np.hypot(x - cx, z - cz)
            ix, iz = x - L.x0, z - L.z0
            if L.water[ix, iz]:
                continue
            if d < 12.5:
                m = PAVE[((x // 2) * 3 + (z // 2) * 5) % 4]
                set_ground(w, L, x, z, P.FLOOR_Y, m)
    for x in range(-8, 0):
        for z in range(-8, 8):
            d = np.hypot(x - cx, z - cz)
            if 5.2 <= d < 6.3:
                ix, iz = x - L.x0, z - L.z0
                if L.creek[ix, iz] or abs(x - P.canyon_x(z)) < 2.2:
                    continue
                w.set(x, P.FLOOR_Y + 1, z, B.SLAB, 1)
    # a pump with its trough, benches facing the water
    w.set(-9, P.FLOOR_Y + 1, -4, B.COBBLE_WALL); w.set(-9, P.FLOOR_Y + 2, -4, B.LEVER, 5)
    w.set(-9, P.FLOOR_Y + 1, -3, B.CAULDRON, 3)
    for z in (2, 3, 4):
        w.set(-11, P.FLOOR_Y + 1, z, B.SPRUCE_STAIRS, 0)


# ---- tracks, trails and the tram ---------------------------------------------------------------
def pave(w, L, pts, width, mats, flatten=2):
    sp = spline(pts, 0.5)
    hs = np.array([H(L, int(round(x)), int(round(z))) for x, z in sp], float)
    k = 8
    sm = np.convolve(np.pad(hs, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="same")[k:-k]
    done = set()
    r = width / 2.0
    for (x, z), y in zip(sp, sm):
        for dx in range(-int(r) - 1, int(r) + 2):
            for dz in range(-int(r) - 1, int(r) + 2):
                X, Z = int(round(x + dx)), int(round(z + dz))
                if (X, Z) in done or np.hypot(X - x, Z - z) > r or X >= 0:
                    continue
                ix, iz = X - L.x0, Z - L.z0
                if not (0 <= ix < L.nx and 0 <= iz < L.nz) or not L.land[ix, iz] or L.water[ix, iz]:
                    continue
                if any(a <= X <= c and b <= Z <= d for a, b, c, d in L.footprints):
                    continue
                g = H(L, X, Z)
                if w.id(X, g + 1, Z) not in (B.AIR, B.TALLGRASS, B.DEADBUSH):
                    continue
                done.add((X, Z))
                ty = int(round(y))
                if abs(ty - g) > flatten:
                    ty = g + int(np.sign(ty - g)) * flatten
                set_ground(w, L, X, Z, ty, mats[RNG.integers(len(mats))])


def rail_path(cells):
    """Data values for a 4-connected run of rail cells: straight, curved where it turns."""
    out = []
    for i, (x, y, z) in enumerate(cells):
        nb = []
        for j in (i - 1, i + 1):
            if 0 <= j < len(cells):
                nb.append((cells[j][0] - x, cells[j][2] - z))
        dirs = set()
        for dx, dz in nb:
            dirs.add("e" if dx > 0 else "w" if dx < 0 else "s" if dz > 0 else "n")
        if dirs <= {"n", "s"}:
            d = 0
        elif dirs <= {"e", "w"}:
            d = 1
        elif dirs == {"s", "e"}:
            d = 6
        elif dirs == {"s", "w"}:
            d = 7
        elif dirs == {"n", "w"}:
            d = 8
        else:
            d = 9
        out.append((x, y, z, d))
    return out


def tram(w, L):
    """The tram on the bench: from the adit's mouth south past the arch's foot to the tipple's head, across
    the Wash on its trestle, to the South Drift. Rails run on the bench's ground; on the trestle, on its deck."""
    z_start = -33
    z_end = L.drift_mouth[2]
    cells = []
    px = None
    for z in range(z_start, z_end + 1):
        x = int(round(P.bench_x(z)))
        if px is not None and x != px:
            step = 1 if x > px else -1
            for xx in range(px + step, x + step, step):
                cells.append((xx, None, z - 1 if xx != x else z))
            if cells[-1][0] == x and cells[-1][2] == z:
                px = x
                continue
        cells.append((x, None, z))
        px = x
    # dedupe while keeping 4-connection
    seen, run = set(), []
    for c in cells:
        if (c[0], c[2]) not in seen:
            seen.add((c[0], c[2])); run.append(c)
    trestle_cells = []
    placed = []
    for x, _, z in run:
        g = H(L, x, z)
        wash = L.wash_mask[x - L.x0, z - L.z0] or g < P.BENCH_Y - 2
        y = P.BENCH_Y if not wash else P.BENCH_Y
        if wash:
            trestle_cells.append((x, z))
        placed.append((x, y + 1, z))
    for x, y, z, d in rail_path(placed):
        if w.id(x, y - 1, z) == B.AIR:
            w.set(x, y - 1, z, B.PLANKS, 5)
        if w.id(x, y, z) in (B.AIR, B.TALLGRASS, B.DEADBUSH):
            w.set(x, y, z, B.RAIL, d)
            for yy in (y + 1, y + 2):
                if w.id(x, yy, z) not in (B.AIR,):
                    w.set(x, yy, z, B.AIR)
    trestle(w, L, trestle_cells)
    L.tram = placed


def trestle(w, L, cells):
    """Timber bents under the tram wherever the bench is broken — across the Wash — a deck three wide,
    a fence along both sides."""
    for i, (x, z) in enumerate(cells):
        for dx in (-1, 0, 1):
            w.set(x + dx, P.BENCH_Y, z, B.PLANKS, 5)
        w.set(x - 2, P.BENCH_Y + 1, z, B.DARK_OAK_FENCE); w.set(x + 2, P.BENCH_Y + 1, z, B.DARK_OAK_FENCE)
        w.set(x - 2, P.BENCH_Y, z, B.LOG2, 1 | 8); w.set(x + 2, P.BENCH_Y, z, B.LOG2, 1 | 8)
        if i % 4 == 0:
            for dx in (-2, 2):
                g = H(L, x + dx, z)
                for y in range(g, P.BENCH_Y):
                    w.set(x + dx, y, z, B.LOG2, 1)
            # cross bracing
            for k, y in enumerate(range(P.BENCH_Y - 1, P.BENCH_Y - 9, -3)):
                for dx in (-1, 0, 1):
                    if w.id(x + dx, y, z) == B.AIR:
                        w.set(x + dx, y, z, B.LOG2, 1 | 4)


def tipple(w, L):
    """The tipple: a timber tower from the canyon floor to the tram at the bench's edge, with a stair
    inside — the way up from the Adobe Quarter — and an ore chute down to a bin on the street."""
    z = 26
    xb = int(round(P.bench_x(z)))
    x_edge = int(round(P.canyon_x(z) - P.FLOOR_HALF))          # the lower cliff's foot
    x0, x1 = x_edge - 1, x_edge + 4
    z0, z1 = z - 3, z + 3
    gy = P.FLOOR_Y
    top = P.BENCH_Y
    for x in range(x0, x1 + 1):
        for zz in range(z0, z1 + 1):
            edge_x, edge_z = x in (x0, x1), zz in (z0, z1)
            for y in range(gy + 1, top + 4):
                w.set(x, y, zz, B.AIR)
            if edge_x and edge_z:
                for y in range(gy - 1, top + 4):
                    w.set(x, y, zz, B.LOG2, 1)
    for y in range(gy + 4, top + 4, 4):
        for x in range(x0, x1 + 1):
            for zz in (z0, z1):
                w.set(x, y, zz, B.LOG2, 1 | 4)
        for zz in range(z0, z1 + 1):
            for x in (x0, x1):
                w.set(x, y, zz, B.LOG2, 1 | 8)
    claim(L, "tipple", (x0, z0, x1, z1))
    claim(L, "tipple chute and bin", (x1 + 1, z - 1, x1 + 13, z + 1))
    # the stair: a switchback of spruce stairs up the inside, landings at each turn
    y = gy
    xa, xb2 = x0 + 1, x1 - 1
    zz = z0 + 1
    going = 1
    while y < top:
        for i in range(xb2 - xa + 1):
            x = xa + i if going > 0 else xb2 - i
            y += 1
            if y > top:
                break
            for dz in (0, 1):
                w.set(x, y, zz + dz, B.SPRUCE_STAIRS, 0 if going > 0 else 1)
                for yy in range(y - 1, gy, -1):
                    pass
            if y >= top:
                break
        # landing and turn
        zz = z1 - 2 if zz == z0 + 1 else z0 + 1
        going = -going
        if y < top:
            for x in (xb2 if going < 0 else xa,):
                for dz in (0, 1):
                    w.set(x, y, zz + dz, B.PLANKS, 5)
    # the top floor joining the bench, and the chute: slabs down to an ore bin on the street
    for x in range(x0, x1 + 1):
        for zz2 in range(z0, z1 + 1):
            if w.id(x, top, zz2) == B.AIR:
                w.set(x, top, zz2, B.PLANKS, 5)
    for x in range(x0 - 3, x0 + 1):
        for zz2 in range(z0 + 1, z1):
            if w.id(x, top, zz2) == B.AIR or x >= x0:
                w.set(x, top, zz2, B.PLANKS, 5)
            for yy in range(top + 1, top + 3):
                if w.id(x, yy, zz2) not in (B.AIR,):
                    w.set(x, yy, zz2, B.AIR)
    for k in range(10):
        cx = x1 + 1 + k
        cy = top - 1 - k
        if cy <= gy + 2:
            break
        w.set(cx, cy, z, B.WOOD_SLAB, 5 | 8)
        w.set(cx, cy, z - 1, B.DARK_OAK_FENCE); w.set(cx, cy, z + 1, B.DARK_OAK_FENCE)
    bx = x1 + 11
    for x in range(bx, bx + 3):
        for zz2 in (z - 1, z, z + 1):
            edge = x in (bx, bx + 2) or zz2 in (z - 1, z + 1)
            w.set(x, gy + 1, zz2, *((B.PLANKS, 5) if edge else (B.GOLD_ORE, 0)))
    # the tipple's doorway on the street side, and an opening onto the bench
    for y in (gy + 1, gy + 2):
        w.set(x1, y, z, B.AIR); w.set(x1, y, z + 1, B.AIR)
    L.footprints.append((x0, z0, x1, z1))


def mule_trail(w, L):
    """Stairs cut into the canyon wall: up the lower cliff from Main Street to the bench, along the bench,
    up the upper cliff to the rim among the Needles. Red sandstone stairs, a fence on the open side."""
    def flight(z_start, y_start, y_end, x_of, dirz):
        z = z_start
        y = y_start
        while y < y_end:
            x = int(round(x_of(z)))
            for dx in (0, -1):
                X = x + dx
                for yy in range(y + 1, y + 5):
                    w.set(X, yy, z, B.AIR)
                w.set(X, y, z, B.RED_SANDSTONE, 0)
                w.set(X, y + 1, z, B.RED_SANDSTONE_STAIRS if hasattr(B, "RED_SANDSTONE_STAIRS") else 180, 3 if dirz < 0 else 2)
                for yy in range(y - 6, y):
                    if w.id(X, yy, z) == B.AIR:
                        w.set(X, yy, z, B.STAINED_CLAY, 1)
                L.H[X - L.x0, z - L.z0] = y + 1
            w.set(x + 1, y + 2, z, B.DARK_OAK_FENCE) if w.id(x + 1, y + 1, z) == B.AIR else None
            y += 1
            z += dirz
        return z
    # lower flight: from the floor at the wall's foot, climbing north into a notch in the cliff
    z0 = -50
    lower_x = lambda z: P.canyon_x(z) - P.FLOOR_HALF - 1.5
    zt = flight(z0, P.FLOOR_Y, P.BENCH_Y, lower_x, -1)
    # upper flight: from the bench's back, climbing north to the rim
    upper_x = lambda z: P.canyon_x(z) - P.FLOOR_HALF - P.LOWER_CLIFF - P.BENCH_WIDTH - 1.5
    flight(zt - 4, P.BENCH_Y, P.PLATEAU_Y, upper_x, -1)


def ladder_up(w, L, x_from, z, rise=8):
    """A ladder up the first rock face met walking west from x_from along z: placed in the last low column,
    against the face, from its ground to the top of the rock."""
    x = x_from
    while x > L.x0 + 1 and H(L, x - 1, z) - H(L, x, z) < rise:
        x -= 1
    # the ladder stands on the tier below; the rock face is the next column west
    g, top = H(L, x, z), H(L, x - 1, z)
    for y in range(g + 1, top + 1):
        w.set(x, y, z, B.LADDER, 5)
    return (x, z, g, top)


# ---- the mesa top -------------------------------------------------------------------------------
def headframe(w, L):
    sx, sz = (-78, -30)
    g = L.shaft_top
    top = g + 14
    for dx, dz in ((-3, -3), (-3, 3), (3, -3), (3, 3)):
        for y in range(g + 1, top + 1):
            k = (y - g) // 6
            w.set(sx + dx - int(np.sign(dx)) * k, y, sz + dz - int(np.sign(dz)) * k, B.LOG2, 1)
    for y in (g + 5, g + 10, top):
        k = (y - g) // 6
        r = 3 - k
        for d in range(-r, r + 1):
            for (X, Z, ax) in ((sx + d, sz - r, 4), (sx + d, sz + r, 4), (sx - r, sz + d, 8), (sx + r, sz + d, 8)):
                w.set(X, y, Z, B.LOG2, 1 | ax)
    cy = top + 3
    for a in np.linspace(0, 2 * np.pi, 48, endpoint=False):
        w.set(sx + int(round(2.6 * np.cos(a))), cy + int(round(2.6 * np.sin(a))), sz, B.PLANKS, 5)
    for d in (-2, -1, 1, 2):
        w.set(sx + d, cy, sz, B.DARK_OAK_FENCE); w.set(sx, cy + d, sz, B.DARK_OAK_FENCE)
    w.set(sx, cy, sz, B.LOG2, 1 | 8)
    for y in range(top + 1, cy):
        w.set(sx, y, sz, B.DARK_OAK_FENCE)
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            if max(abs(dx), abs(dz)) >= 2:
                set_ground(w, L, sx + dx, sz + dz, g, (B.PLANKS, 5))
    L.footprints.append((sx - 3, sz - 3, sx + 3, sz + 3))
    claim(L, "headframe", (sx - 3, sz - 3, sx + 3, sz + 3))


def windmill(w, L, x, z, height=12):
    """A farm windmill: a lattice tower, a wheel of blades facing east, a tail vane."""
    g = H(L, x, z)
    for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        for y in range(g + 1, g + height):
            w.set(x + dx, y, z + dz, B.SPRUCE_FENCE)
    for y in range(g + 3, g + height, 3):
        for dx in (-1, 0, 1):
            w.set(x + dx, y, z - 1, B.SPRUCE_FENCE); w.set(x + dx, y, z + 1, B.SPRUCE_FENCE)
    top = g + height
    w.set(x, top, z, B.LOG2, 1)
    for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        for rr in (1, 2, 3):
            w.set(x + 1, top + int(round(rr * np.sin(a))), z + int(round(rr * np.cos(a))), B.WOOD_SLAB, 1 if rr < 3 else 9)
    for k in range(1, 4):
        w.set(x - k, top, z, B.SPRUCE_FENCE)
    w.set(x - 4, top, z, B.PLANKS, 1); w.set(x - 4, top + 1, z, B.PLANKS, 1)
    L.footprints.append((x - 1, z - 1, x + 1, z + 1))
    claim(L, "windmill", (x - 4, z - 1, x + 1, z + 1))


def tank(w, L, x, z, r=3.5):
    """A stock tank: a ring of stone with water in it."""
    g = H(L, x, z)
    claim(L, "stock tank", (int(x - r - 1), int(z - r - 1), int(x + r + 1), int(z + r + 1)))
    for X in range(int(x - r - 1), int(x + r + 2)):
        for Z in range(int(z - r - 1), int(z + r + 2)):
            d = np.hypot(X - x, Z - z)
            if d < r:
                w.set(X, g, Z, B.WATER)
                w.set(X, g + 1, Z, B.AIR)
            elif d < r + 1:
                w.set(X, g + 1, Z, B.COBBLE_WALL)


def fort(w, L):
    """Fort Ochre: an adobe compound on the upper tier, its back to High Butte; a two-storey quarters on
    the west wall, a watchtower in the north-east corner, the gate east onto Fort Road, red flying."""
    x0, z0, x1, z1 = -113, -8, -97, 16
    y = P.PLATEAU_Y + 1 + 6
    y = floor_of(L, x0, z0, x1, z1)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            set_ground(w, L, x, z, y, PAVE[(x * 7 + z * 3) % 4] if not (x in (x0, x1) or z in (z0, z1)) else (B.SANDSTONE, 0))
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                for k in range(1, 5):
                    w.set(x, y + k, z, B.SANDSTONE, 2 if k > 1 else 0)
                if (x + z) % 2 == 0:
                    w.set(x, y + 5, z, B.SANDSTONE, 2)
    # the gate: a timber lintel over a four-wide opening
    for z in range(2, 7):
        for k in range(1, 4):
            w.set(x1, y + k, z, B.AIR)
        w.set(x1, y + 4, z, B.LOG, 1 | 8)
    for z in (1, 7):
        for k in range(1, 6):
            w.set(x1, y + k, z, B.LOG, 1)
    # a walk along the inside of the walls, a ladder up to it
    for x in range(x0 + 1, x1):
        for z in (z0 + 1, z1 - 1):
            w.set(x, y + 3, z, B.WOOD_SLAB, 1 | 8)
    for z in range(z0 + 1, z1):
        w.set(x0 + 1, y + 3, z, B.WOOD_SLAB, 1 | 8)
    for k in range(1, 4):
        w.set(x1 - 2, y + k, z0 + 2, B.LADDER, 3) if False else None
    L.footprints.append((x0, z0, x1, z1))
    claim(L, "fort walls", (x0, z0, x1, z1))
    L.things.pop()   # the fort's own buildings stand inside its walls by design
    q = adobe(w, L, x0 + 2, z0 + 2, x0 + 8, z1 - 2, "e", kind="quarters", upper=(x0 + 2, z0 + 2, x0 + 6, z0 + 9))
    # the watchtower
    tx0, tz0 = x1 - 5, z0 + 1
    for x in range(tx0, tx0 + 4):
        for z in range(tz0, tz0 + 4):
            corner = x in (tx0, tx0 + 3) and z in (tz0, tz0 + 3)
            for k in range(1, 15):
                if corner:
                    w.set(x, y + k, z, B.LOG, 1)
            if not corner:
                w.set(x, y + 9, z, B.PLANKS, 1)
                w.set(x, y + 14, z, B.PLANKS, 1)
    for k in range(1, 10):
        w.set(tx0 + 1, y + k, tz0 + 4, B.LADDER, 3) if False else None
    for k in range(1, 9):
        w.set(tx0 + 1, y + k, tz0 + 1, B.LADDER, 3)
    w.set(tx0 + 1, y + 9, tz0 + 1, B.LADDER, 3)
    for x in range(tx0, tx0 + 4):
        for z in (tz0, tz0 + 3):
            w.set(x, y + 10, z, B.SPRUCE_FENCE)
    for z in range(tz0, tz0 + 4):
        for x in (tx0, tx0 + 3):
            w.set(x, y + 10, z, B.SPRUCE_FENCE)
    w.set(tx0 + 1, y + 10, tz0, B.AIR)
    # the flag
    for k in range(15, 22):
        w.set(tx0 + 3, y + k, tz0 + 3, B.SPRUCE_FENCE)
    for k in range(19, 22):
        for d in (1, 2, 3):
            w.set(tx0 + 3, y + k, tz0 + 3 + d, B.WOOL, 14)
    # a wagon in the yard, a well
    wx, wz = x1 - 7, z1 - 3
    for dx in range(0, 4):
        w.set(wx + dx, y + 2, wz, B.WOOD_SLAB, 1)
        w.set(wx + dx, y + 3, wz - 1, B.WOOL, 0); w.set(wx + dx, y + 3, wz + 1, B.WOOL, 0)
        w.set(wx + dx, y + 4, wz, B.WOOL, 0)
    for dx in (0, 3):
        w.set(wx + dx, y + 1, wz - 1, B.LOG, 4); w.set(wx + dx, y + 1, wz + 1, B.LOG, 4)
    L.fort_floor = y
    return q


def rancho(w, L):
    cx, cz = -104, 74
    adobe(w, L, cx - 6, cz - 4, cx + 2, cz + 3, "e", kind="house", upper=(cx - 6, cz - 4, cx - 2, cz))
    # the barn
    false_front(w, L, cx - 6, cz + 8, cx + 1, cz + 15, "e", storeys=1, name=None, kind="barn", walls=(B.PLANKS, 5))
    # the corral
    # the corral on the house's west side, away from the scarp's edge, its gate toward the house
    c0, c1, d0, d1 = cx - 18, cx - 8, cz - 8, cz + 4
    claim(L, "corral", (c0, d0, c1, d1))
    for x in range(c0, c1 + 1):
        for z in range(d0, d1 + 1):
            if x in (c0, c1) or z in (d0, d1):
                if not (x == c1 and abs(z - (d0 + d1) // 2) <= 1):
                    w.set(x, H(L, x, z) + 1, z, B.FENCE)
    windmill(w, L, cx - 8, cz - 12, 11)
    tank(w, L, cx - 8, cz - 17, 2.5)


def build(w, L):
    L.footprints = []
    L.things = []
    L.conflicts = []
    RECORDS.clear()
    claim(L, "Gilt Spring plaza", (-12, -11, -1, 10))
    spring(w, L)
    # Main Street: west row with its backs to the cliff, east row between the street and the creek
    west = [(-90, 7, 2, "hotel", ["Grand", "Hotel"]), (-81, 6, 1, "store", ["General", "Store"]),
            (-72, 5, 1, "house", None), (-64, 7, 2, "saloon", ["Saloon"]), (-54, 6, 1, "assay", ["Assay", "Office"]),
            (-45, 6, 1, "store", ["Feed &", "Seed"]), (-36, 8, 2, "bank", ["Bank of", "Gilt"])]
    for z0, depth, storeys, kind, name in west:
        zc = z0 + depth // 2
        xs = int(round(P.canyon_x(zc) - 12)) - 3      # the street's west kerb
        false_front(w, L, xs - 8, z0, xs, z0 + depth, "e", storeys, name, kind)
    east = [(-86, 6, 1, "house", None), (-70, 7, 1, "store", ["Barber"]), (-58, 6, 2, "hotel", ["Rooms"]),
            (-44, 6, 1, "store", ["Sheriff"])]
    for z0, depth, storeys, kind, name in east:
        zc = z0 + depth // 2
        xs = int(round(P.canyon_x(zc) - 12)) + 3      # the street's east kerb
        xe = int(round(P.canyon_x(zc) - 3.8))
        if xe - xs < 4:
            continue
        false_front(w, L, xs, z0, min(xs + 6, xe), z0 + depth, "w", storeys, name, kind)
    # the Adobe Quarter, south of the spring
    for (x0, z0, x1, z1, side, up) in ((-19, 12, -13, 18, "e", None),
                                       (-7, 18, -2, 24, "w", None), (-19, 33, -13, 39, "e", None),
                                       (-6, 30, -1, 37, "w", (-4, 30, -1, 33)), (-24, 60, -18, 67, "e", None),
                                       (-8, 64, -2, 70, "w", None), (-23, 74, -16, 81, "e", (-23, 74, -19, 77)),
                                       (-8, 80, -2, 86, "w", None)):
        adobe(w, L, x0, z0, x1, z1, side, upper=up)
    chapel(w, L, -10, 42, -2, 49)
    L.tower_top = water_tower(w, L, -19, -14)
    tipple(w, L)
    mule_trail(w, L)
    tram(w, L)
    headframe(w, L)
    fort(w, L)
    rancho(w, L)
    windmill(w, L, -84, -62, 12)
    tank(w, L, -82, -54, 3.5)
    # ladders up the buttes
    # ladders up each tier of High Butte and Table Rock, one above the other
    for name, (xf, z) in (("butte_ladder", (-100, 22)), ("table_ladder", (-60, 86))):
        steps = []
        for _ in range(3):
            x, zz, g, top = ladder_up(w, L, xf, z, rise=4)
            steps.append((x, g, top))
            xf = x - 1
            if H(L, xf - 3, z) <= top + 1:
                break
        setattr(L, name, steps)
    for r in P.ROUTES:
        mats = {"street": HARD, "road": TRACK, "track": TRACK}[r["kind"]]
        pave(w, L, r["pts"], {"street": 5, "road": 3, "track": 2}[r["kind"]], mats)
    L.records = RECORDS
