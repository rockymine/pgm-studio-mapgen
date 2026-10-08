"""Everything somebody built on red's half: Jarlshall, the Beacon with the core in its lantern, Holmstein's
stones and the monument, the ice-fishing huts on Kaldvatn, Skarvik — longhouses, the stave church, the
smithy, boathouses and a pier on Midsund, drying racks — the Old Bridge over Ravnsund, the whaler frozen in
the strait, Tingholm's ring, the ruined watchtower on Kraakodde, the sealers' hut, and the paths.

One built family: dark spruce timber on cobblestone, dark oak roofs, crossed boards at the gables. The
Beacon is the one thing of stone, striped brick and white.
"""
import numpy as np

import plan as P
from mc import B
from noise import spline

RNG = np.random.default_rng(808)
RECORDS = []
SOFT = (B.AIR, B.SNOW_LAYER, B.TALLGRASS, B.DOUBLE_PLANT)


def H(F, x, z):
    return int(F.H[x - F.x0, z - F.z0])


def claim(F, name, box):
    a0, b0, a1, b1 = box
    for other, (c0, d0, c1, d1) in F.things:
        if a0 <= c1 and c0 <= a1 and b0 <= d1 and d0 <= b1:
            F.conflicts.append((name, other, box))
    F.things.append((name, box))


def set_ground(w, F, x, z, y, mat=None):
    ix, iz = x - F.x0, z - F.z0
    if not (0 <= ix < F.nx and 0 <= iz < F.nz) or not F.inside[ix, iz] or F.water[ix, iz]:
        return
    old = int(F.H[ix, iz])
    for yy in range(y + 1, max(old, y) + 3):
        if w.id(x, yy, z) in (B.STONE, B.DIRT, B.GRASS, B.COBBLE, B.GRAVEL, B.SNOW, B.SNOW_LAYER, B.TALLGRASS):
            w.set(x, yy, z, B.AIR)
    for yy in range(min(old, y), y):
        if w.id(x, yy, z) == B.AIR or yy > old:
            w.set(x, yy, z, B.DIRT)
    if mat:
        w.set(x, y, z, *mat)
    elif w.id(x, y, z) in (B.AIR, B.SNOW_LAYER):
        w.set(x, y, z, B.GRASS)
    F.H[ix, iz] = y


def site(w, F, x0, z0, x1, z1, y, name, margin=1):
    for x in range(x0 - margin, x1 + margin + 1):
        for z in range(z0 - margin, z1 + margin + 1):
            if any(a <= x <= c and b <= z <= d for a, b, c, d in F.footprints):
                continue
            set_ground(w, F, x, z, y, None)
            if not (x0 <= x <= x1 and z0 <= z <= z1) and w.id(x, y + 1, z) == B.AIR:
                w.set(x, y + 1, z, B.SNOW_LAYER, 0)
    F.footprints.append((x0, z0, x1, z1))
    claim(F, name, (x0, z0, x1, z1))


def free_spot(F, cx, cz, wx, wz, max_r=14, relief=4, margin=2):
    """The nearest footprint of wx by wz to (cx, cz) that is on dry land, red's own, no steeper than `relief`
    across, and clear of everything already claimed by `margin` blocks. Searched in a widening spiral."""
    for r in range(0, max_r + 1):
        ring = [(dx, dz) for dx in range(-r, r + 1) for dz in range(-r, r + 1) if max(abs(dx), abs(dz)) == r]
        for dx, dz in ring:
            x0, z0 = cx + dx - wx // 2, cz + dz - wz // 2
            x1, z1 = x0 + wx - 1, z0 + wz - 1
            if not all(a + b < -1 for a, b in ((x0, z0), (x1, z0), (x0, z1), (x1, z1))):
                continue
            ix0, iz0 = x0 - F.x0, z0 - F.z0
            if ix0 < 0 or iz0 < 0 or x1 - F.x0 >= F.nx or z1 - F.z0 >= F.nz:
                continue
            sub = (slice(ix0 - margin, x1 - F.x0 + margin + 1), slice(iz0 - margin, z1 - F.z0 + margin + 1))
            if F.water[sub].any() or F.lake[sub].any() or not F.inside[sub].all():
                continue
            hh = F.H[ix0:x1 - F.x0 + 1, iz0:z1 - F.z0 + 1]
            if hh.max() - hh.min() > relief:
                continue
            box = (x0 - margin, z0 - margin, x1 + margin, z1 + margin)
            if any(a0 <= c1 and c0 <= a1 and b0 <= d1 and d0 <= b1
                   for _, (c0, d0, c1, d1) in F.things for (a0, b0, a1, b1) in (box,)):
                continue
            return x0, z0, x1, z1
    raise RuntimeError(f"no free {wx}x{wz} spot near {(cx, cz)}")


def floor_of(F, x0, z0, x1, z1):
    sub = F.H[x0 - F.x0:x1 - F.x0 + 1, z0 - F.z0:z1 - F.z0 + 1]
    return int(np.median(sub))


def door(w, x, y, z, side):
    w.set(x, y + 1, z, B.SPRUCE_DOOR, {"e": 0, "s": 1, "w": 2, "n": 3}[side])
    w.set(x, y + 2, z, B.SPRUCE_DOOR, 8)


def steep_roof(w, x0, z0, x1, z1, y, along_x, snow=True):
    """A steep roof of dark oak: two stairs up for every step in, its ridge capped in planks that carry snow,
    crossed boards standing over each gable."""
    if along_x:
        a0, a1, b0, b1, lo, hi = x0 - 1, x1 + 1, z0 - 1, z1 + 1, 2, 3
    else:
        a0, a1, b0, b1, lo, hi = z0 - 1, z1 + 1, x0 - 1, x1 + 1, 0, 1
    k = 0
    yy = y
    while b0 + k <= b1 - k:
        for rise in (0, 1):
            if b0 + k > b1 - k:
                break
            for a in range(a0, a1 + 1):
                for b, s in ((b0 + k, lo), (b1 - k, hi)):
                    X, Z = (a, b) if along_x else (b, a)
                    if b0 + k == b1 - k:
                        w.set(X, yy, Z, B.PLANKS, 5)
                        if snow:
                            w.set(X, yy + 1, Z, B.SNOW_LAYER, 0)
                    elif rise == 0:
                        w.set(X, yy, Z, B.DARK_OAK_STAIRS, s)
                    else:
                        w.set(X, yy, Z, B.PLANKS, 5)
            # gable infill between the two slopes, on both ends
            for b in range(b0 + k + 1, b1 - k):
                for a in ((x0, x1) if along_x else (z0, z1)):
                    X, Z = (a, b) if along_x else (b, a)
                    w.set(X, yy, Z, B.PLANKS, 1)
            yy += 1
        k += 1
    # crossed boards over each gable: the old dragon-head ends, in fence
    top = yy
    mid = (b0 + b1) // 2
    for a in (a0, a1):
        X, Z = (a, mid) if along_x else (mid, a)
        w.set(X, top - 1, Z, B.DARK_OAK_FENCE)
        w.set(X, top, Z, B.DARK_OAK_FENCE)
    return top


def longhouse(w, F, x0, z0, x1, z1, along_x, kind="house", doors=("s",), name=None, height=3):
    """A Norse longhouse: a cobblestone course, spruce log posts at the corners and every third block,
    spruce plank walls, a few small windows, a steep dark oak roof, crossed boards at the gables."""
    y = floor_of(F, x0, z0, x1, z1)
    site(w, F, x0, z0, x1, z1, y, kind)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            yy = y - 1
            while yy > 20 and w.id(x, yy, z) in (B.AIR, B.WATER, B.ICE, B.SNOW_LAYER):
                w.set(x, yy, z, B.COBBLE); yy -= 1
            edge = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            post = edge and (corner or ((x - x0) % 3 == 0 if z in (z0, z1) else (z - z0) % 3 == 0))
            w.set(x, y, z, *((B.COBBLE, 0) if edge else (B.PLANKS, 1)))
            for k in range(1, height + 1):
                if not edge:
                    w.set(x, y + k, z, B.AIR)
                elif post:
                    w.set(x, y + k, z, B.LOG, 1)
                elif k == 1:
                    w.set(x, y + k, z, B.COBBLE)
                else:
                    w.set(x, y + k, z, B.PLANKS, 1)
            if edge:
                run_x = z in (z0, z1)
                w.set(x, y + height + 1, z, *((B.LOG, 1) if corner else (B.LOG, 1 | (4 if run_x else 8))))
    # small windows high in the long walls
    for x in range(x0 + 2, x1 - 1, 4):
        for z in (z0, z1):
            if w.id(x, y + 2, z) == B.PLANKS:
                w.set(x, y + 2, z, B.PANE)
    for z in range(z0 + 2, z1 - 1, 4):
        for x in (x0, x1):
            if w.id(x, y + 2, z) == B.PLANKS:
                w.set(x, y + 2, z, B.PANE)
    top = steep_roof(w, x0, z0, x1, z1, y + height + 2, along_x)
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            w.set(x, y + height + 1, z, B.AIR)
    outs = []
    for side in doors:
        if side in "ns":
            dx, dz = (x0 + x1) // 2, (z0 if side == "n" else z1)
        else:
            dx, dz = (x0 if side == "w" else x1), (z0 + z1) // 2
        door(w, dx, y, dz, side)
        ox, oz = {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[side]
        for k in (1, 2):
            if w.id(dx + ox, y + k, dz + oz) not in (B.AIR,):
                w.set(dx + ox, y + k, dz + oz, B.AIR)
        outs.append((dx + ox, dz + oz))
    # the hearth in the middle of the floor, its smoke hole in the ridge
    hx, hz = (x0 + x1) // 2, (z0 + z1) // 2
    if kind in ("house", "hall"):
        for dx in (-1, 0, 1):
            w.set(hx + dx, y, hz, B.COBBLE)
        w.set(hx, y, hz, B.NETHERRACK); w.set(hx, y + 1, hz, B.AIR)
        w.set(hx - 1, y + 1, hz, B.COBBLE_WALL); w.set(hx + 1, y + 1, hz, B.COBBLE_WALL)
        # benches along the long walls
        for x in range(x0 + 1, x1):
            for z in ((z0 + 1, z1 - 1) if along_x else ()):
                if w.id(x, y + 1, z) == B.AIR and (x - x0) % 4 != 2:
                    w.set(x, y + 1, z, B.SPRUCE_STAIRS, 3 if z == z0 + 1 else 2)
        for z in range(z0 + 1, z1):
            for x in ((x0 + 1, x1 - 1) if not along_x else ()):
                if w.id(x, y + 1, z) == B.AIR and (z - z0) % 4 != 2:
                    w.set(x, y + 1, z, B.SPRUCE_STAIRS, 1 if x == x0 + 1 else 0)
    for (tx, tz, f) in ((x0 + 1, hz, 1), (x1 - 1, hz, 2)):
        if w.id(tx, y + 3, tz) == B.AIR:
            w.set(tx, y + 3, tz, B.TORCH, f)
    rec = dict(x0=x0, z0=z0, x1=x1, z1=z1, floor=y, kind=kind, outs=outs, top=top)
    RECORDS.append(rec)
    return rec


def stave_church(w, F, cx, cz):
    """A stave church: a nave in three stepped tiers of dark oak roof, crossed boards at every gable, a door
    to the south under a little porch."""
    x0, z0, x1, z1 = cx - 4, cz - 4, cx + 4, cz + 4
    y = floor_of(F, x0, z0, x1, z1)
    site(w, F, x0, z0, x1, z1, y, "stave church")
    tiers = [(4, 4), (3, 4), (2, 4), (1, 3)]
    base = y
    for i, (r, ht) in enumerate(tiers):
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                edge = abs(x - cx) == r or abs(z - cz) == r
                corner = abs(x - cx) == r and abs(z - cz) == r
                if i == 0:
                    w.set(x, base, z, *((B.COBBLE, 0) if edge else (B.PLANKS, 5)))
                for k in range(1, ht + 1):
                    if edge:
                        w.set(x, base + k, z, *((B.LOG2, 1) if corner else (B.PLANKS, 1)))
                    elif i == 0:
                        w.set(x, base + k, z, B.AIR)
        # the skirt roof round this tier: one ring of stairs out from the wall
        ry = base + ht + 1
        for x in range(cx - r - 1, cx + r + 2):
            for z in range(cz - r - 1, cz + r + 2):
                dxv, dzv = x - cx, z - cz
                if max(abs(dxv), abs(dzv)) == r + 1:
                    if abs(dxv) >= abs(dzv):
                        w.set(x, ry, z, B.DARK_OAK_STAIRS, 0 if dxv < 0 else 1)
                    else:
                        w.set(x, ry, z, B.DARK_OAK_STAIRS, 2 if dzv < 0 else 3)
                elif max(abs(dxv), abs(dzv)) <= r:
                    w.set(x, ry, z, B.PLANKS, 5)
        for (dx, dz) in ((r + 1, 0), (-r - 1, 0), (0, r + 1), (0, -r - 1)):
            w.set(cx + dx, ry + 1, cz + dz, B.DARK_OAK_FENCE)
        base = ry
    for k in range(1, 4):
        w.set(cx, base + k, cz, B.DARK_OAK_FENCE)
    w.set(cx - 1, base + 2, cz, B.DARK_OAK_FENCE); w.set(cx + 1, base + 2, cz, B.DARK_OAK_FENCE)
    door(w, cx, y, z1, "s")
    for k in (1, 2):
        w.set(cx, y + k, z1 + 1, B.AIR)
    for x in range(cx - 2, cx + 3):
        for z in (cz - 2, cz, cz + 2):
            if w.id(x, y + 1, z) == B.AIR and x != cx:
                w.set(x, y + 1, z, B.SPRUCE_STAIRS, 3)
    w.set(cx, y + 1, z0 + 1, B.QUARTZ); w.set(cx, y + 2, z0 + 1, B.TORCH, 5)
    RECORDS.append(dict(x0=x0, z0=z0, x1=x1, z1=z1, floor=y, kind="church", outs=[(cx, z1 + 1)], top=base))


def beacon(w, F):
    """The Beacon: a round tower striped in brick and white, a spiral stair up its inside wall round an open
    well, a gallery ringed by a parapet at the top, the lantern of glass over it and the core inside it.
    The core stands over the well's mouth: lava let into the well falls the tower's height — the leak."""
    cx, cz = P.BEACON
    g = H(F, cx, cz)
    claim(F, "the Beacon", (cx - 7, cz - 7, cx + 7, cz + 7))
    F.footprints.append((cx - 7, cz - 7, cx + 7, cz + 7))
    top = g + 20                        # the lantern's floor
    for x in range(cx - 7, cx + 8):
        for z in range(cz - 7, cz + 8):
            d = np.hypot(x - cx, z - cz)
            if d <= 5.5:
                set_ground(w, F, x, z, g, (B.STONEBRICK, 0))
            for y in range(g + 1, top + 1):
                if d <= 4.4:
                    if d > 3.4:
                        band = ((y - g) // 3) % 2
                        w.set(x, y, z, *((B.BRICK, 0) if band else (B.STONE, 4)))
                    else:
                        w.set(x, y, z, B.AIR)
            # the gallery and its parapet, drain gaps every few blocks
            if d <= 6.4:
                w.set(x, top, z, B.STONEBRICK, 0)
            if 5.6 < d <= 6.4:
                ang = np.degrees(np.arctan2(z - cz, x - cx)) % 45
                if ang > 6:
                    w.set(x, top + 1, z, B.STONEBRICK, 0)
                    w.set(x, top + 2, z, B.SLAB, 5)
    # the spiral stair, one step a block round the inside wall, landing under the lantern floor
    steps = []
    angle = 0.0
    y = g + 1
    while y < top:
        a = np.radians(angle)
        x = cx + int(round(2.6 * np.cos(a))); z = cz + int(round(2.6 * np.sin(a)))
        if (x, z) != (cx, cz) and (not steps or (x, z) != steps[-1][:2]):
            w.set(x, y, z, B.STONEBRICK, 0)
            steps.append((x, z, y))
            y += 1
        angle += 26
    # the hatch from the stair's head into the lantern: one open block in the floor
    hx, hz, hy = steps[-1]
    w.set(hx, top, hz, B.AIR)
    # the well: the open middle of the tower, its mouth under the core
    for y in range(g + 1, top):
        w.set(cx, y, cz, B.AIR)
    # the lantern: glass round the core, a dark oak cap
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            d = np.hypot(x - cx, z - cz)
            if 2.4 < d <= 3.4:
                for y in range(top + 1, top + 5):
                    w.set(x, y, z, B.PANE)
            if d <= 3.4:
                w.set(x, top + 5, z, B.STONEBRICK, 0)
    for k, r in enumerate((3.4, 2.4, 1.4, 0.5)):
        for x in range(cx - 4, cx + 5):
            for z in range(cz - 4, cz + 5):
                if np.hypot(x - cx, z - cz) <= r:
                    w.set(x, top + 6 + k, z, B.PLANKS, 5)
    w.set(cx, top + 10, cz, B.FENCE)
    # two openings from the lantern to the gallery
    for (dx, dz) in ((3, 0), (-3, 0)):
        for y in (top + 1, top + 2):
            w.set(cx + dx, y, cz + dz, B.AIR)
    # the core: obsidian round lava, its bottom over the well's mouth
    c0 = top + 1
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            for y in range(c0, c0 + 3):
                inner = (x, z, y) == (cx, cz, c0 + 1)
                w.set(x, y, z, B.LAVA if inner else B.OBSIDIAN)
    w.set(cx, top, cz, B.AIR)                     # the well's mouth, under the core
    # the door at the foot, facing the headland path
    for y in (g + 1, g + 2):
        w.set(cx - 4, y, cz, B.AIR); w.set(cx - 3, y, cz, B.AIR)
    w.set(cx - 4, g + 1, cz, B.SPRUCE_DOOR, 2); w.set(cx - 4, g + 2, cz, B.SPRUCE_DOOR, 8)
    F.core = dict(x0=cx - 1, x1=cx + 1, y0=c0, y1=c0 + 2, z0=cz - 1, z1=cz + 1)
    F.beacon_top = top


def holmstein(w, F):
    """The monument on the knoll's crown, two obsidian blocks floating; a ring of standing stones round the
    knoll's foot, well back from it."""
    mx, mz = P.MONUMENT
    g = H(F, mx, mz)
    w.set(mx, g + 3, mz, B.OBSIDIAN); w.set(mx, g + 4, mz, B.OBSIDIAN)
    F.monument = (mx, g + 3, mz)
    claim(F, "monument clearance", (mx - 4, mz - 4, mx + 4, mz + 4))
    for k in range(7):
        a = 2 * np.pi * k / 7 + 0.3
        sx, sz = int(round(mx + 7.5 * np.cos(a))), int(round(mz + 7.5 * np.sin(a)))
        gy = H(F, sx, sz)
        if F.lake[sx - F.x0, sz - F.z0] or F.water[sx - F.x0, sz - F.z0]:
            continue
        for y in range(gy + 1, gy + 3 + (k % 2)):
            w.set(sx, y, sz, B.STONE, 0 if y % 2 else 5)


def ice_hut(w, F, x, z):
    """An ice-fishing hut on the lake: a little spruce box on runners, a hole cut in the ice by its door."""
    y = F.lake_level
    for dx in range(0, 3):
        for dz in range(0, 4):
            edge = dx in (0, 2) or dz in (0, 3)
            for k in (1, 2):
                w.set(x + dx, y + k, z + dz, *((B.PLANKS, 1) if edge else (B.AIR, 0)))
            w.set(x + dx, y + 3, z + dz, B.WOOD_SLAB, 5)
    w.set(x + 1, y + 1, z + 3, B.AIR); w.set(x + 1, y + 2, z + 3, B.AIR)
    w.set(x + 1, y, z + 5, B.WATER)
    w.set(x + 1, y + 1, z + 1, B.SPRUCE_STAIRS, 2)
    claim(F, "ice hut", (x, z, x + 2, z + 5))


def bridge(w, F):
    """The Old Bridge: a timber trestle over Ravnsund's open water, along x, its deck a little arched,
    bents every four blocks into the strait's bed, a rail of fence."""
    bx, bz = dict((p["key"], p) for p in P.PLACES)["bridge"]["at"]
    # find the shores either side along x
    xs = [x for x in range(bx - 16, bx + 17) if not F.water[x - F.x0, bz - F.z0]]
    west = max(x for x in xs if x < bx)
    east = min(x for x in xs if x > bx)
    y0, y1 = H(F, west, bz), H(F, east, bz)
    n = east - west
    claim(F, "the Old Bridge", (west, bz - 2, east, bz + 2))
    for i, x in enumerate(range(west, east + 1)):
        t = i / max(1, n)
        deck = int(round(y0 + (y1 - y0) * t + 2.2 * np.sin(np.pi * t)))
        deck = max(deck, P.WATER_Y + 2)
        for dz in (-1, 0, 1):
            w.set(x, deck, bz + dz, B.PLANKS, 1)
            for k in (1, 2, 3):
                if w.id(x, deck + k, bz + dz) not in (B.AIR,):
                    w.set(x, deck + k, bz + dz, B.AIR)
        for dz in (-2, 2):
            w.set(x, deck, bz + dz, B.LOG, 1 | 4)
            w.set(x, deck + 1, bz + dz, B.SPRUCE_FENCE)
        if i % 4 == 0 and 0 < i < n:
            for dz in (-2, 2):
                yb = H(F, x, bz + dz)
                for y in range(yb + 1, deck):
                    w.set(x, y, bz + dz, B.LOG, 1)
            for y in range(P.WATER_Y + 1, deck, 3):
                for dz in (-1, 0, 1):
                    w.set(x, y, bz + dz, B.LOG, 1 | 8)
        F.H[x - F.x0, bz - F.z0] = max(F.H[x - F.x0, bz - F.z0], deck) if not F.water[x - F.x0, bz - F.z0] else F.H[x - F.x0, bz - F.z0]
    F.bridge = (west, east, bz)


def whaler(w, F):
    """A three-masted whaler frozen into Ravnsund's ice, lying along the strait (on the diagonal, not on the
    grid): a dark oak hull, a spruce deck under snow, three masts with furled sails, the stern cabin."""
    cx, cz = dict((p["key"], p) for p in P.PLACES)["whaler"]["at"]
    L = 22
    keel, deck = P.WATER_Y - 4, P.WATER_Y + 3
    ends = [(cx + a * 1 / np.sqrt(2), cz - a * 1 / np.sqrt(2)) for a in (-L / 2 - 1, L / 2 + 5)]
    claim(F, "the whaler", (int(min(e[0] for e in ends)) - 3, int(min(e[1] for e in ends)) - 3,
                            int(max(e[0] for e in ends)) + 3, int(max(e[1] for e in ends)) + 3))
    ax, az = 1 / np.sqrt(2), -1 / np.sqrt(2)          # along the strait
    bx, bz = 1 / np.sqrt(2), 1 / np.sqrt(2)           # across it

    def half_at(a):
        t = a / (L / 2)
        if abs(t) >= 1:
            return 0.0
        return 4.4 * np.sqrt(1 - t ** 2) if t < 0 else 4.4 * np.sqrt(max(0, 1 - t ** 1.6))
    for x in range(cx - 13, cx + 14):
        for z in range(cz - 13, cz + 14):
            a = (x - cx) * ax + (z - cz) * az
            b = (x - cx) * bx + (z - cz) * bz
            half = half_at(a)
            if half <= 0:
                continue
            for y in range(keel, deck + 1):
                hw = half * (0.45 + 0.55 * (y - keel) / (deck - keel)) + 0.3
                bb = b - (y - keel) * 0.1          # the list
                if abs(bb) > hw:
                    continue
                shell = abs(bb) > hw - 1.0 or y == keel
                if y == deck:
                    w.set(x, y, z, *((B.PLANKS, 5) if shell else (B.PLANKS, 1)))
                    if not shell and RNG.random() < 0.6:
                        w.set(x, y + 1, z, B.SNOW_LAYER, 0)
                    elif shell:
                        w.set(x, y + 1, z, B.DARK_OAK_FENCE)
                elif shell:
                    w.set(x, y, z, B.PLANKS, 5)
                else:
                    w.set(x, y, z, B.AIR)
            # ice heaved against the hull
            if half + 0.5 < abs(b) < half + 2.2 and w.id(x, P.WATER_Y, z) in (B.ICE, B.WATER) and RNG.random() < 0.5:
                w.set(x, P.WATER_Y + 1, z, B.PACKED_ICE)
    # masts with yards across the hull and the sails furled on them
    for (a, ht) in ((-6, 15), (0, 19), (6, 13)):
        mx, mz = int(round(cx + a * ax)), int(round(cz + a * az))
        for y in range(deck + 1, deck + ht):
            w.set(mx, y, mz, B.LOG, 1)
        for yy, span in ((deck + ht - 3, 3), (deck + ht - 8, 4)):
            for k in range(-span, span + 1):
                X, Z = int(round(mx + k * bx)), int(round(mz + k * bz))
                w.set(X, yy, Z, B.SPRUCE_FENCE)
                if abs(k) < span:
                    w.set(X, yy - 1, Z, B.WOOL, 0)
    # the bowsprit
    for k in range(1, 6):
        a = L / 2 + k * 0.9
        w.set(int(round(cx + a * ax)), deck + 1 + k // 2, int(round(cz + a * az)), B.SPRUCE_FENCE)
    # the stern cabin: a little planked box on the after deck, a chest inside
    sx, sz = int(round(cx - 8 * ax)), int(round(cz - 8 * az))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            for k in (1, 2):
                w.set(sx + dx, deck + k, sz + dz, *((B.PLANKS, 5) if (dx, dz) != (0, 0) else (B.AIR, 0)))
            w.set(sx + dx, deck + 3, sz + dz, B.WOOD_SLAB, 5)
    w.set(sx + 1, deck + 1, sz, B.AIR); w.set(sx + 1, deck + 2, sz, B.AIR)
    w.chest(sx, deck + 1, sz, [(0, "minecraft:arrow", 24, 0), (1, "minecraft:cooked_fish", 8, 0),
                               (13, "minecraft:iron_boots", 1, 0)], facing=5)
    # a gangplank down onto the ice off the side facing home
    for k in range(4):
        X, Z = int(round(cx - (2.5 + k) * bx)), int(round(cz - (2.5 + k) * bz))
        w.set(X, deck - k, Z, B.PLANKS, 1)
        for yy in (deck - k + 1, deck - k + 2):
            if w.id(X, yy, Z) not in (B.AIR,):
                w.set(X, yy, Z, B.AIR)


def boathouse(w, F, x0, z0, x1, z1, open_side):
    """A boathouse on the strait's shore, its water end open, a boat drawn up inside it."""
    rec = longhouse(w, F, x0, z0, x1, z1, along_x=open_side in "ew", kind="boathouse", doors=())
    y = rec["floor"]
    if open_side in "ns":
        zz = z0 if open_side == "n" else z1
        for x in range(x0 + 1, x1):
            for k in (1, 2, 3):
                w.set(x, y + k, zz, B.AIR)
    else:
        xx = x0 if open_side == "w" else x1
        for z in range(z0 + 1, z1):
            for k in (1, 2, 3):
                w.set(xx, y + k, z, B.AIR)
    # the boat: a little hull of stairs and slabs
    bx, bz = (x0 + x1) // 2, (z0 + z1) // 2
    for k in range(-2, 3):
        X, Z = (bx + k, bz) if open_side in "ew" else (bx, bz + k)
        w.set(X, y + 1, Z, B.WOOD_SLAB, 1)
    return rec


def racks(w, F, x, z, n=3, along_x=True):
    """Drying racks: frames of spruce for the stockfish, in a row."""
    g = H(F, x, z)
    for i in range(n):
        X, Z = (x + i * 3, z) if along_x else (x, z + i * 3)
        for dz in (0, 3):
            XX, ZZ = (X, Z + dz) if along_x else (X + dz, Z)
            gy = H(F, XX, ZZ)
            for y in range(gy + 1, gy + 4):
                w.set(XX, y, ZZ, B.SPRUCE_FENCE)
        for dz in range(0, 4):
            XX, ZZ = (X, Z + dz) if along_x else (X + dz, Z)
            w.set(XX, g + 3, ZZ, B.SPRUCE_FENCE)
    claim(F, "drying racks", (x, z, x + (3 * n if along_x else 3), z + (3 if along_x else 3 * n)))


def pier(w, F, x, z, length, dx, dz):
    """A pier of planks on log piles out into the strait."""
    g = H(F, x, z)
    y = max(g, P.WATER_Y + 1)
    for k in range(length):
        X, Z = x + dx * k, z + dz * k
        for s in (-1, 0, 1):
            XX, ZZ = (X, Z + s) if dx else (X + s, Z)
            w.set(XX, y, ZZ, B.PLANKS, 1)
            if k % 3 == 0 and s != 0:
                for yy in range(P.WATER_Y - 4, y):
                    if w.id(XX, yy, ZZ) in (B.WATER, B.ICE, B.AIR):
                        w.set(XX, yy, ZZ, B.LOG, 1)
    claim(F, "pier", (min(x, x + dx * length) - 1, min(z, z + dz * length) - 1, max(x, x + dx * length) + 1, max(z, z + dz * length) + 1))


def tingholm(w, F):
    """Tingholm: standing stones in a ring on the islet, a cairn in the middle. Red sets the stones on its half."""
    cx, cz = -0.5, -0.5
    for k in range(12):
        a = 2 * np.pi * k / 12
        sx, sz = int(np.floor(cx + 4.5 * np.cos(a) + 0.5)), int(np.floor(cz + 4.5 * np.sin(a) + 0.5))
        if not (sx + sz < -1 or (sx + sz == -1 and sx <= -1)):
            continue
        g = H(F, sx, sz)
        for y in range(g + 1, g + 4):
            w.set(sx, y, sz, B.STONE, 5 if y % 2 else 0)
    for (x, z) in ((-1, -1), (-1, 0), (0, -1), (-2, -1), (-1, -2)):
        if x + z < -1 or (x + z == -1 and x <= -1):
            g = H(F, x, z)
            w.set(x, g + 1, z, B.COBBLE); w.set(x, g + 2, z, B.COBBLE) if (x, z) == (-1, -1) else None


def watchtower(w, F, cx, cz):
    """The ruined watchtower on Kraakodde: a round stone stump, its top broken off, stones fallen round it."""
    g = H(F, cx, cz)
    claim(F, "watchtower", (cx - 4, cz - 4, cx + 4, cz + 4))
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            d = np.hypot(x - cx, z - cz)
            if 2.4 < d <= 3.6:
                top = g + 4 + int(5 * (0.5 + 0.5 * np.sin(np.arctan2(z - cz, x - cx) * 2 + 1)))
                for y in range(g + 1, top):
                    w.set(x, y, z, *((B.COBBLE, 0) if RNG.random() < 0.3 else (B.STONEBRICK, 0 if RNG.random() < 0.7 else 2)))
            elif 3.6 < d <= 4.5 and RNG.random() < 0.25:
                w.set(x, H(F, x, z) + 1, z, B.COBBLE)
    for y in (g + 1, g + 2):
        w.set(cx - 3, y, cz, B.AIR)
    for y in range(g + 1, g + 7):
        w.set(cx + 2, y, cz, B.LADDER, 4)
        if w.id(cx + 3, y, cz) == B.AIR:
            w.set(cx + 3, y, cz, B.STONEBRICK)


def paths(w, F):
    """Trodden paths: the snow walked off them, gravel and coarse dirt and podzol a third each."""
    mats = [(B.GRAVEL, 0), (B.DIRT, 1), (B.DIRT, 2)]
    for r in P.ROUTES:
        width = 3 if r["kind"] == "road" else 2
        for x, z in spline(r["pts"], 0.5):
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    X, Z = int(round(x + dx)), int(round(z + dz))
                    if np.hypot(X - x, Z - z) > width / 2.0 or not (X + Z < -1):
                        continue
                    ix, iz = X - F.x0, Z - F.z0
                    if not F.inside[ix, iz] or F.water[ix, iz] or F.lake[ix, iz]:
                        continue
                    if any(a <= X <= c and b <= Z <= d for a, b, c, d in F.footprints):
                        continue
                    g = H(F, X, Z)
                    if w.id(X, g, Z) in (B.GRASS, B.DIRT, B.GRAVEL, B.STONE, B.COBBLE):
                        w.set(X, g, Z, *mats[RNG.integers(3)])
                        if w.id(X, g + 1, Z) == B.SNOW_LAYER:
                            w.set(X, g + 1, Z, B.AIR)


def build(w, F):
    F.footprints, F.things, F.conflicts = [], [], []
    RECORDS.clear()
    # the hall: long, along x, doors at both ends
    sx, sz = P.SPAWN
    hall = longhouse(w, F, sx - 11, sz - 4, sx + 11, sz + 4, along_x=True, kind="hall", doors=("e", "w"), height=4)
    F.hall = hall
    for (fx, fz) in ((sx + 13, sz - 3), (sx + 13, sz + 3)):
        g = H(F, fx, fz)
        for y in range(g + 1, g + 8):
            w.set(fx, y, fz, B.SPRUCE_FENCE)
        for y in range(g + 5, g + 8):
            for k in (1, 2):
                w.set(fx, y, fz + k, B.WOOL, 14)
    beacon(w, F)
    holmstein(w, F)
    lx, lz = P.LAKE
    ice_hut(w, F, lx - 5, lz - 4)
    ice_hut(w, F, lx + 1, lz + 2)
    bridge(w, F)
    whaler(w, F)
    # Skarvik: longhouses round a green, the church, the smithy, boathouses on Midsund, racks and a pier
    vx, vz = dict((p["key"], p) for p in P.PLACES)["village"]["at"]
    # Skarvik: each building asks for a spot near where the village wants it and takes the nearest free one
    stave_church(w, F, *[(a + c) // 2 for a, c in [free_spot(F, vx - 16, vz - 2, 9, 9)[0::2]]],
                 *[(b + d) // 2 for b, d in [free_spot(F, vx - 16, vz - 2, 9, 9)[1::2]]]) if False else None
    x0, z0, x1, z1 = free_spot(F, vx - 16, vz - 2, 9, 9)
    stave_church(w, F, (x0 + x1) // 2, (z0 + z1) // 2)
    for (cx, cz, wx, wz, along, doors) in ((vx - 9, vz - 8, 11, 6, True, ("s",)), (vx - 2, vz - 14, 6, 10, False, ("w",)),
                                           (vx - 12, vz + 8, 7, 11, False, ("e",))):
        x0, z0, x1, z1 = free_spot(F, cx, cz, wx, wz)
        longhouse(w, F, x0, z0, x1, z1, along_x=along, doors=doors)
    x0, z0, x1, z1 = free_spot(F, vx, vz + 7, 7, 6)
    smith = longhouse(w, F, x0, z0, x1, z1, along_x=True, kind="smithy", doors=("n",), height=3)
    y = smith["floor"]
    w.set(x0 + 2, y + 1, z0 + 3, B.ANVIL); w.set(x0 + 4, y + 1, z0 + 3, B.FURNACE, 2)
    boathouse(w, F, vx + 8, vz + 1, vx + 13, vz + 7, "e")
    x0, z0, x1, z1 = free_spot(F, vx - 4, vz + 16, 10, 4, margin=1)
    racks(w, F, x0, z0, 3, True)
    pier(w, F, vx + 8, vz + 10, 9, 1, 1) if False else pier(w, F, vx + 12, vz + 9, 7, 1, 0)
    tingholm(w, F)
    watchtower(w, F, *dict((p["key"], p) for p in P.PLACES)["kraak"]["at"])
    sx2, sz2 = dict((p["key"], p) for p in P.PLACES)["sealers"]["at"]
    longhouse(w, F, sx2 - 3, sz2 - 2, sx2 + 3, sz2 + 3, along_x=True, kind="hut", doors=("e",), height=3)
    racks(w, F, sx2 - 4, sz2 + 6, 2, True)
    paths(w, F)
    F.records = RECORDS
