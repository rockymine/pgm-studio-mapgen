"""Everything built on red's half of Cloudhaven: Highmoor's keep, the windmill, the gazebo over monument A,
the sunken garden round monument B, Port Aerie's dock, warehouse and crane, the Albatross moored at the pier,
the Concord's red half, the rope bridges and stairs between the islands, the balloons, and the small things
on the flank rocks. Each builder claims its footprint; a claim on ground already claimed is a conflict.
"""
import numpy as np

import plan as P
from mc import B

RNG = np.random.default_rng(777)
RECORDS = []
ISL = {i["key"]: i for i in P.ISLANDS}
QUARTZ_PILLAR = 2


def H(F, x, z):
    return int(F.H[x - F.x0, z - F.z0])


def land(F, x, z):
    ix, iz = x - F.x0, z - F.z0
    return 0 <= ix < F.nx and 0 <= iz < F.nz and bool(F.land[ix, iz])


def claim(F, name, box):
    a0, b0, a1, b1 = box
    for other, (c0, d0, c1, d1) in F.things:
        if other != name and a0 <= c1 and c0 <= a1 and b0 <= d1 and d0 <= b1:
            F.conflicts.append((name, other, box))
    F.things.append((name, box))


def level(w, F, x0, z0, x1, z1, y):
    """Make the ground in a box exactly y: cut what stands higher, fill with dirt what is lower, grass on top."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not land(F, x, z):
                continue
            g = H(F, x, z)
            for yy in range(y + 1, g + 3):
                w.set(x, yy, z, B.AIR)
            for yy in range(g, y):
                w.set(x, yy, z, B.DIRT)
            w.set(x, y, z, B.GRASS)
            F.H[x - F.x0, z - F.z0] = y


def floor_y(F, x0, z0, x1, z1):
    hs = [H(F, x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) if land(F, x, z)]
    return int(np.median(hs))


# ---------------------------------------------------------------------------------------------------------
# bridges

def line_cells(x0, z0, x1, z1):
    """A four-connected line of cells from (x0, z0) to (x1, z1): every step is one block along x or z."""
    cells = [(x0, z0)]
    x, z = x0, z0
    dx, dz = x1 - x0, z1 - z0
    n = max(abs(dx), abs(dz)) * 4 + 1
    for t in np.linspace(0, 1, n)[1:]:
        tx, tz = int(round(x0 + dx * t)), int(round(z0 + dz * t))
        while (x, z) != (tx, tz):
            if x != tx and (abs(tx - x) >= abs(tz - z) or z == tz):
                x += 1 if tx > x else -1
            else:
                z += 1 if tz > z else -1
            cells.append((x, z))
    return cells


def bridge(w, F, a, b):
    """A rope bridge from island a down to island b along the line between their centres. Where the drop is
    more than the gap allows at a block a step, the way down starts early: as a stair cut into a's grass,
    and, if that is not enough, a ramp on posts onto b. The deck is three wide with a rope rail of fence."""
    ia, ib = ISL[a], ISL[b]
    (ax, az), (bx, bz) = ia["at"], ib["at"]
    path = line_cells(int(round(ax)), int(round(az)), int(round(bx)), int(round(bz)))
    keys = [F.key[x - F.x0, z - F.z0] for x, z in path]
    last_a = max(i for i, k in enumerate(keys) if k == a)
    first_b = min(i for i, k in enumerate(keys) if k == b)
    ya = H(F, *path[last_a]) if True else 0
    ya = int(np.median([H(F, *path[i]) for i in range(max(0, last_a - 6), last_a + 1) if keys[i] == a]))
    yb = int(np.median([H(F, *path[i]) for i in range(first_b, min(len(path), first_b + 6)) if keys[i] == b]))
    drop = abs(ya - yb)
    gap = first_b - last_a
    need = drop + 2 - gap
    # spread the extra run over the high island first, then the low one
    s = last_a - max(1, (need + 1) // 2 if need > 0 else 1)
    e = first_b + max(1, need - (last_a - s - 1) if need > 0 else 1)
    s = max(0, s); e = min(len(path) - 1, e)
    ys, ye = H(F, *path[s]), H(F, *path[e])
    n = e - s
    dirn = (np.sign(bx - ax), np.sign(bz - az))
    cells = []
    for i in range(s, e + 1):
        t = (i - s) / n
        y = int(round(ys + (ye - ys) * t - (0.0 if need > 0 else 1.2 * np.sin(np.pi * t))))
        cells.append((path[i][0], path[i][1], y))
    # the deck: three wide, across whichever way this step of the path does not go
    for k, (x, z, y) in enumerate(cells):
        nx_, nz_ = cells[min(k + 1, len(cells) - 1)][:2]
        px_, pz_ = cells[max(k - 1, 0)][:2]
        along_x = abs(nx_ - px_) >= abs(nz_ - pz_)
        offs = [(0, s_) for s_ in (-1, 0, 1)] if along_x else [(s_, 0) for s_ in (-1, 0, 1)]
        rails = [(0, -2), (0, 2)] if along_x else [(-2, 0), (2, 0)]
        for ox, oz in offs:
            X, Z = x + ox, z + oz
            if X >= 0:
                continue
            g = H(F, X, Z) if land(F, X, Z) else -1
            mat = (B.PLANKS, 2 if (k // 2) % 2 else 0) if g < 0 or g < y else (B.STONEBRICK, 0)
            w.set(X, y, Z, *mat)
            for yy in range(y + 1, y + 4):
                if w.id(X, yy, Z) not in (B.AIR,) and w.id(X, yy, Z) not in (B.WOOL,):
                    w.set(X, yy, Z, B.AIR)
            if g > y:                       # the cut: stone brick walls are the trench's sides
                pass
            elif 0 <= g < y - 1 and k % 3 == 0:
                for yy in range(g + 1, y):
                    w.set(X, yy, Z, B.LOG, 0)
            F.bridge_cells.add((X, Z))
        for ox, oz in rails:
            X, Z = x + ox, z + oz
            if X >= 0:
                continue
            g = H(F, X, Z) if land(F, X, Z) else -1
            if g < y:
                w.set(X, y, Z, B.FENCE) if g < 0 else None
                w.set(X, y + 1, Z, B.FENCE)
                if k % 4 == 0:
                    w.set(X, y + 2, Z, B.FENCE)
            F.bridge_cells.add((X, Z))
    F.bridges.append(dict(a=a, b=b, cells=cells))
    return cells


# ---------------------------------------------------------------------------------------------------------
# Highmoor

def keep(w, F):
    """Red's spawn: a walled court of stone brick with quartz courses, a tower at each corner flying red,
    gates east (to Port Aerie), north (to Windmill Isle) and south (to Sentinel Rock). Open to the sky."""
    cx, cz = P.SPAWN
    x0, z0, x1, z1 = cx - 7, cz - 7, cx + 7, cz + 7
    y = floor_y(F, x0, z0, x1, z1)
    level(w, F, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y)
    claim(F, "the keep", (x0, z0, x1, z1))
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            w.set(x, y, z, B.STONEBRICK, 0 if (x + z) % 5 else 3) if not edge else None
            if edge:
                for yy in range(y, y + 6):
                    w.set(x, yy, z, *((B.QUARTZ, 0) if yy == y + 3 else (B.STONEBRICK, 0 if RNG.random() < 0.85 else 2)))
                if (x + z) % 2 == 0:
                    w.set(x, y + 6, z, B.STONEBRICK, 0)
    # walkway inside the wall's top, a block lower, on slabs
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            if x in (x0 + 1, x1 - 1) or z in (z0 + 1, z1 - 1):
                w.set(x, y + 4, z, B.SLAB, 13)
    # corner towers
    for tx, tz in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        for x in range(tx - 1, tx + 2):
            for z in range(tz - 1, tz + 2):
                for yy in range(y, y + 9):
                    w.set(x, yy, z, *((B.QUARTZ, 0) if yy in (y + 3, y + 8) else (B.STONEBRICK, 0)))
                if (x + z) % 2 == 0:
                    w.set(x, y + 9, z, B.STONEBRICK, 0)
        w.set(tx, y + 9, tz, B.FENCE)
        for yy in range(y + 10, y + 14):
            w.set(tx, yy, tz, B.FENCE)
        for k in (1, 2):
            for yy in (y + 12, y + 13):
                w.set(tx + (k if tx > cx else -k), yy, tz, B.WOOL, 14)
    # ladders up the inside of the north-west tower to the wall walk
    for yy in range(y + 1, y + 5):
        w.set(x0 + 2, yy, z0 + 1, B.LADDER, 3)
    w.set(x0 + 2, y + 4, z0 + 1, B.LADDER, 3)
    # gates: three wide and four high
    for (gx, gz, ax) in ((x1, cz, False), (cx, z0, True), (cx, z1, True)):
        for k in (-1, 0, 1):
            X, Z = (gx + k, gz) if ax else (gx, gz + k)
            for yy in range(y + 1, y + 5):
                w.set(X, yy, Z, B.AIR)
            w.set(X, y, Z, B.STONEBRICK, 0)
        X, Z = (gx, gz) if ax else (gx, gz)
        w.set(*((gx - 2, y + 5, gz) if ax else (gx, y + 5, gz - 2)), B.STONEBRICK, 3)
        w.set(*((gx + 2, y + 5, gz) if ax else (gx, y + 5, gz + 2)), B.STONEBRICK, 3)
    # the court: a well in the middle, benches, a chest of blocks for bridging
    w.set(cx - 3, y + 1, cz - 3, B.CRAFTING)
    w.chest(cx + 3, y + 1, cz - 4, [(0, "minecraft:planks", 64, 0), (1, "minecraft:planks", 64, 0)], facing=3)
    for x, z in ((cx - 4, cz + 4), (cx + 4, cz + 4)):
        w.set(x, y + 1, z, B.OAK_STAIRS, 2)
    F.spawn = (cx, y + 1, cz)
    F.keep = (x0, z0, x1, z1, y)
    RECORDS.append(dict(x0=x0, z0=z0, x1=x1, z1=z1, floor=y, kind="keep"))


def windmill(w, F):
    """A stone windmill: a tapering round tower, a timber cap, four sails of white wool on fence frames."""
    cx, cz = ISL["windmill"]["at"]
    y = floor_y(F, cx - 3, cz - 3, cx + 3, cz + 3)
    level(w, F, cx - 4, cz - 4, cx + 4, cz + 4, y)
    claim(F, "the windmill", (cx - 4, cz - 4, cx + 4, cz + 4))
    top = y + 10
    for yy in range(y, top + 1):
        r = 3.3 - 1.2 * (yy - y) / (top - y)
        for x in range(cx - 4, cx + 5):
            for z in range(cz - 4, cz + 5):
                d = np.hypot(x - cx, z - cz)
                if d <= r:
                    shell = d > r - 1
                    w.set(x, yy, z, *((B.COBBLE, 0) if shell and yy < y + 4 else (B.STONE, 4) if shell else (B.AIR, 0)))
    for yy in (y + 1, y + 2):
        w.set(cx + 3, yy, cz, B.AIR)
        w.set(cx + 2, yy, cz, B.AIR)
    w.set(cx + 3, y + 1, cz, B.OAK_DOOR, 2); w.set(cx + 3, y + 2, cz, B.OAK_DOOR, 8)
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            d = np.hypot(x - cx, z - cz)
            if d <= 2.6:
                w.set(x, top + 1, z, B.PLANKS, 5)
            if d <= 1.6:
                w.set(x, top + 2, z, B.PLANKS, 5)
    w.set(cx, top + 3, cz, B.WOOD_SLAB, 5)
    # the sails, on the east face, in a cross
    hx, hy = cx + 3, top - 1
    w.set(hx, hy, cz, B.LOG, 0 | 4)
    for k in range(1, 8):
        for (dy, dz) in ((k, 0), (-k, 0), (0, k), (0, -k)):
            if hy + dy <= y + 1:
                continue
            w.set(hx + 1, hy + dy, cz + dz, B.FENCE)
            if k >= 2:
                sy, sz = (dy, dz + (1 if dy > 0 else -1)) if dz == 0 else (dy + (1 if dz < 0 else -1), dz)
                if hy + sy > y + 1:
                    w.set(hx + 1, hy + sy, cz + sz, B.WOOL, 0)
    RECORDS.append(dict(x0=cx - 3, z0=cz - 3, x1=cx + 3, z1=cz + 3, floor=y, kind="windmill"))


def monument_on(w, F, x, y, z):
    """Two obsidian hanging three blocks of air over the floor y, nothing under them (the playtest rule)."""
    w.set(x, y + 4, z, B.OBSIDIAN)
    w.set(x, y + 5, z, B.OBSIDIAN)
    return (x, y + 4, z)


def gazebo(w, F):
    """Monument A: a round floor of stone brick and quartz, eight quartz pillars, a stepped dome; open on all
    sides, so the monument is seen and shot at from every bridge. Lanterns on posts round it."""
    cx, cz = ISL["lantern"]["at"]
    y = floor_y(F, cx - 4, cz - 4, cx + 4, cz + 4)
    level(w, F, cx - 5, cz - 5, cx + 5, cz + 5, y)
    claim(F, "the gazebo", (cx - 5, cz - 5, cx + 5, cz + 5))
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            d = np.hypot(x - cx, z - cz)
            if d <= 4.6:
                w.set(x, y, z, *((B.QUARTZ, 0) if d < 1.6 or 3.4 < d else (B.STONEBRICK, 0)))
            for k, r in enumerate((4.6, 3.6, 2.6, 1.4)):
                if d <= r and (k > 0 or d > 3.6):
                    w.set(x, y + 6 + k, z, *((B.SLAB, 7) if k == 0 else (B.QUARTZ, 0)))
    for k in range(8):
        a = 2 * np.pi * k / 8
        x, z = int(round(cx + 4 * np.cos(a))), int(round(cz + 4 * np.sin(a)))
        for yy in range(y + 1, y + 6):
            w.set(x, yy, z, B.QUARTZ, QUARTZ_PILLAR)
        w.set(x, y + 6, z, B.QUARTZ, 0)
    w.set(cx, y + 10, cz, B.GOLD_BLOCK)
    F.mon_a = monument_on(w, F, cx, y, cz)
    for k in range(4):
        a = 2 * np.pi * k / 4 + np.pi / 4
        x, z = int(round(cx + 7.5 * np.cos(a))), int(round(cz + 7.5 * np.sin(a)))
        if land(F, x, z):
            g = H(F, x, z)
            for yy in range(g + 1, g + 4):
                w.set(x, yy, z, B.FENCE)
            w.set(x, g + 4, z, B.GLOWSTONE)
    RECORDS.append(dict(x0=cx - 4, z0=cz - 4, x1=cx + 4, z1=cz + 4, floor=y, kind="gazebo"))


def sunken_garden(w, F):
    """Monument B: a garden sunk two blocks into the Gardens' grass, walled in stone brick, hedged round its
    rim with a gap and steps down on each side, flowers in its beds and the monument in the middle."""
    cx, cz = P.MON_B
    y = floor_y(F, cx - 6, cz - 6, cx + 6, cz + 6)
    level(w, F, cx - 7, cz - 7, cx + 7, cz + 7, y)
    claim(F, "the sunken garden", (cx - 7, cz - 7, cx + 7, cz + 7))
    f = y - 2
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            wall = max(abs(x - cx), abs(z - cz)) == 5
            for yy in range(f + 1, y + 1):
                w.set(x, yy, z, *((B.STONEBRICK, 1 if RNG.random() < 0.3 else 0) if wall else (B.AIR, 0)))
            if not wall:
                w.set(x, f, z, B.GRASS)
                r = RNG.random()
                if max(abs(x - cx), abs(z - cz)) == 4 and r < 0.6:
                    w.set(x, f + 1, z, B.FLOWER, int(RNG.choice([0, 1, 2, 3, 8])))
                elif max(abs(x - cx), abs(z - cz)) == 1:
                    w.set(x, f, z, B.STONEBRICK, 0)
            F.H[x - F.x0, z - F.z0] = f if not wall else y
    # the hedge on the rim, a gap and a flight of steps on each side
    for x in range(cx - 6, cx + 7):
        for z in range(cz - 6, cz + 7):
            if max(abs(x - cx), abs(z - cz)) == 6 and min(abs(x - cx), abs(z - cz)) > 1:
                w.set(x, y + 1, z, B.LEAVES, 4)
    for (dx, dz, st) in ((1, 0, 1), (-1, 0, 0), (0, 1, 3), (0, -1, 2)):
        for k in (-1, 0, 1):
            for step in range(3):
                X = cx + dx * (5 - step) + (k if dx == 0 else 0)
                Z = cz + dz * (5 - step) + (k if dz == 0 else 0)
                yy = y - step
                w.set(X, yy, Z, B.STONEBRICK_STAIRS, st)
                for a in (1, 2, 3):
                    if yy + a <= y + 1:
                        w.set(X, yy + a, Z, B.AIR)
    F.mon_b = monument_on(w, F, cx, f, cz)
    RECORDS.append(dict(x0=cx - 5, z0=cz - 5, x1=cx + 5, z1=cz + 5, floor=f, kind="garden"))


# ---------------------------------------------------------------------------------------------------------
# Port Aerie and the airships

def gable_house(w, F, x0, z0, x1, z1, kind, wall=(B.PLANKS, 2), frame=(B.LOG, 0), roof=(B.SPRUCE_STAIRS, None)):
    """A timber-framed house along x with a steep gable roof; the gable ends are stone, the overhang spruce."""
    y = floor_y(F, x0, z0, x1, z1)
    level(w, F, x0 - 1, z0 - 1, x1 + 1, z1 + 1, y)
    claim(F, kind, (x0, z0, x1, z1))
    ht = 4
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, y, z, B.PLANKS, 1)
            edge = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            for yy in range(y + 1, y + ht + 1):
                if corner:
                    w.set(x, yy, z, *frame)
                elif edge:
                    w.set(x, yy, z, *((B.LOG, 0 | 4) if yy == y + ht and z in (z0, z1) else wall))
                else:
                    w.set(x, yy, z, B.AIR)
    # windows and the door on the long south side
    for x in range(x0 + 2, x1 - 1, 3):
        w.set(x, y + 2, z0, B.PANE); w.set(x, y + 2, z1, B.PANE)
    dx = (x0 + x1) // 2
    w.set(dx, y + 1, z1, B.OAK_DOOR, 3); w.set(dx, y + 2, z1, B.OAK_DOOR, 8)
    # the roof: stairs climbing from both long sides, overhanging a block; stone gable ends
    half = (z1 - z0) // 2 + 1
    for k in range(half + 1):
        yy = y + ht + 1 + k
        for x in range(x0 - 1, x1 + 2):
            zn, zs = z0 - 1 + k, z1 + 1 - k
            if zn <= zs:
                w.set(x, yy, zn, B.SPRUCE_STAIRS, 2)
                w.set(x, yy, zs, B.SPRUCE_STAIRS, 3)
                if zn == zs or zn + 1 == zs:
                    w.set(x, yy, zn, B.WOOD_SLAB, 1); w.set(x, yy, zs, B.WOOD_SLAB, 1)
            if x in (x0, x1):
                for z in range(zn + 1, zs):
                    w.set(x, yy, z, B.COBBLE)
    RECORDS.append(dict(x0=x0, z0=z0, x1=x1, z1=z1, floor=y, kind=kind))
    return y


def port(w, F):
    """Port Aerie: a pier of planks out north from the island's rim, the warehouse, a crane over the pier
    with a crate on its rope, barrels of fuel for the balloons."""
    cx, cz = ISL["port"]["at"]
    a = P.ALBATROSS
    py = H(F, cx + 5, cz - 6)
    px0, px1 = a["x"] - 9, a["x"] - 7                  # the pier: three wide, out along z beside the ship
    pz0 = cz - 4
    pz1 = a["z0"] + 14
    claim(F, "the pier", (px0, pz1, px1, pz0 - 2))
    for z in range(pz1, pz0 + 1):
        for x in range(px0, px1 + 1):
            if land(F, x, z) and H(F, x, z) >= py:
                continue
            w.set(x, py, z, B.PLANKS, 1)
            for yy in (py + 1, py + 2, py + 3):
                if w.id(x, yy, z) != B.AIR:
                    w.set(x, yy, z, B.AIR)
            F.bridge_cells.add((x, z))
        if (z - pz1) % 4 == 0:
            for x in (px0, px1):
                for yy in range(py - 4, py):
                    if w.id(x, yy, z) == B.AIR:
                        w.set(x, yy, z, B.LOG, 0)
                w.set(x, py + 1, z, B.FENCE)
    # the gangplank across to the Albatross's side
    for x in range(px1 + 1, a["x"] - int(a["half"]) + 1):
        for z in (pz1 + 2, pz1 + 3, pz1 + 4):
            w.set(x, py, z, B.WOOD_SLAB, 8 + 0)
            F.bridge_cells.add((x, z))
    F.pier = (px0, pz1, px1, pz0, py)
    # the warehouse and the crane
    wy = gable_house(w, F, cx - 6, cz + 2, cx + 2, cz + 8, "the warehouse")
    kx, kz = px0 - 2, pz0 - 4
    g = H(F, kx, kz) if land(F, kx, kz) else py
    for yy in range(g + 1, g + 9):
        w.set(kx, yy, kz, B.LOG, 0)
    for k in range(1, 6):
        w.set(kx + k, g + 8, kz - k // 2, B.LOG, 0 | 4) if False else w.set(kx + k, g + 8, kz, B.LOG, 0 | 4)
    for yy in range(g + 4, g + 8):
        w.set(kx + 5, yy, kz, B.FENCE)
    w.set(kx + 5, g + 3, kz, B.PLANKS, 0)
    claim(F, "the crane", (kx - 1, kz - 1, kx + 1, kz + 1))
    for (bx, bz) in ((cx + 4, cz - 1), (cx + 5, cz), (cx + 4, cz + 1)):
        if land(F, bx, bz):
            w.set(bx, H(F, bx, bz) + 1, bz, B.LOG, 12)
    return wy


def envelope(w, cx, cy, cz, rx, ry, rz, colours, stripes="x", only_red=True, gores=8):
    """An airship's or a balloon's gas bag: a hollow ellipsoid of wool, striped. stripes 'x' bands along x,
    'gores' vertical segments round a balloon."""
    for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
        if only_red and x >= 0:
            continue
        for z in range(int(cz - rz) - 1, int(cz + rz) + 2):
            for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
                q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2
                if q > 1.0:
                    continue
                # hollow: only cells with a neighbour outside
                inner = all(((x + a - cx) / rx) ** 2 + ((y + b - cy) / ry) ** 2 + ((z + c - cz) / rz) ** 2 <= 1.0
                            for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
                if inner:
                    continue
                if stripes == "x":
                    c = colours[int(abs(x - cx) // 4) % len(colours)]
                else:
                    ang = (np.arctan2(z - cz, x - cx) + np.pi) / (2 * np.pi)
                    c = colours[int(ang * gores) % len(colours)]
                w.set(x, y, z, B.WOOL, c)


def hull_x(w, F, x0, x1, zc, deck, half, double=True, name="the Concord"):
    """A wooden hull lying along x: dark oak sides, a birch deck with a rail, its keel five below the deck.
    Double-ended (both ends pointed alike) when `double`."""
    L = (x1 - x0) / 2
    xm = (x0 + x1) / 2
    keel = deck - 5
    for x in range(x0 - 1, x1 + 2):
        if x >= 0:
            continue
        a = (x - xm) / (L + 0.5)
        if abs(a) >= 1:
            continue
        hw = half * np.sqrt(1 - abs(a) ** 2.2)
        for z in range(int(zc - half) - 2, int(zc + half) + 3):
            b = abs(z - zc)
            for y in range(keel, deck + 1):
                hy = hw * (0.35 + 0.65 * ((y - keel) / (deck - keel)) ** 0.6)
                if b > hy + 0.3:
                    continue
                shell = b > hy - 0.7 or y == keel or abs(a) > 0.93
                if y == deck:
                    w.set(x, y, z, *((B.PLANKS, 5) if shell else (B.PLANKS, 2)))
                    if shell:
                        w.set(x, y + 1, z, B.DARK_OAK_FENCE)
                elif shell:
                    w.set(x, y, z, *((B.GOLD_BLOCK, 0) if y == deck - 1 and abs(a) > 0.85 else (B.PLANKS, 5)))
                else:
                    w.set(x, y, z, B.AIR)
                F.ship_cells.add((x, z))


def concord(w, F):
    """The Concord, red's half: a double-ended hull along x across the centre, a deckhouse astride the seam,
    a white and gold envelope over it on struts, a propeller at each end. Gangways to Gate Rock."""
    c = P.CONCORD
    deck = c["deck"]
    claim(F, "the Concord", (c["x0"], int(c["zc"] - c["half"]) - 1, -1, int(c["zc"] + c["half"]) + 1))
    hull_x(w, F, c["x0"], c["x1"], c["zc"], deck, c["half"])
    # the deckhouse astride the seam: x -4..3, z -2..1 (red builds x <= -1), a door at the west end
    for x in range(-4, 0):
        for z in range(-2, 2):
            edge = x == -4 or z in (-2, 1)
            for yy in range(deck + 1, deck + 4):
                w.set(x, yy, z, *((B.PLANKS, 5) if edge else (B.AIR, 0)))
            w.set(x, deck + 4, z, B.WOOD_SLAB, 2)
    for yy in (deck + 1, deck + 2):
        w.set(-4, yy, -1, B.AIR); w.set(-4, yy, 0, B.AIR)
    w.set(-4, deck + 2, -2, B.PANE) if False else None
    for x in (-3, -2):
        w.set(x, deck + 2, -2, B.PANE); w.set(x, deck + 2, 1, B.PANE)
    # the envelope and its struts
    ey = deck + 13
    envelope(w, -0.5, ey, c["zc"], 19, 6, 6, [0, 0, 4])
    for x in range(c["x0"] + 4, 0, 5):
        for z in (int(c["zc"] - c["half"]) + 1, int(c["zc"] + c["half"])):
            for yy in range(deck + 2, ey - 4):
                if w.id(x, yy, z) == B.AIR:
                    w.set(x, yy, z, B.DARK_OAK_FENCE)
    # a propeller at the west end
    px = c["x0"] - 1
    for k in range(-2, 3):
        w.set(px - 1, deck + 2 + k, 0 if k else 0, B.FENCE) if False else None
    w.set(px - 1, deck + 2, -1, B.IRON_BLOCK); w.set(px - 1, deck + 2, 0, B.IRON_BLOCK)
    for k in (1, 2, 3):
        w.set(px - 2, deck + 2 + k, -1, B.FENCE); w.set(px - 2, deck + 2 - k, 0, B.FENCE)
        w.set(px - 2, deck + 2, -1 - k, B.FENCE); w.set(px - 2, deck + 2, 0 + k, B.FENCE)
    # the gangway from Gate Rock to the west end's deck
    gx = ISL["gate"]["at"][0]
    gy = deck
    for x in range(gx + 2, c["x0"] + 3):
        for z in (-2, -1, 0, 1):
            if land(F, x, z) and H(F, x, z) >= gy:
                continue
            if w.id(x, gy, z) in (B.AIR, B.DARK_OAK_FENCE):
                w.set(x, gy, z, B.PLANKS, 1)
            for yy in (gy + 1, gy + 2):
                if w.id(x, yy, z) in (B.DARK_OAK_FENCE, B.FENCE):
                    w.set(x, yy, z, B.AIR)
            F.bridge_cells.add((x, z))
        for z in (-3, 2):
            if not land(F, x, z):
                w.set(x, gy + 1, z, B.FENCE)
    F.concord = dict(deck=deck)


def hull_z(w, F, xc, z0, z1, deck, half):
    """A single-ended hull along z: the bow at z0 pointed, the stern at z1 square-ish."""
    L = z1 - z0
    keel = deck - 4
    for z in range(z0 - 1, z1 + 1):
        t = (z - z0) / L
        if t < 0:
            continue
        hw = half * (np.sqrt(np.clip(t / 0.35, 0, 1)) if t < 0.35 else 1.0 - 0.25 * max(0, (t - 0.85) / 0.15))
        for x in range(int(xc - half) - 2, int(xc + half) + 3):
            b = abs(x - xc)
            for y in range(keel, deck + 1):
                hy = hw * (0.4 + 0.6 * ((y - keel) / (deck - keel)) ** 0.6)
                if b > hy + 0.3:
                    continue
                shell = b > hy - 0.7 or y == keel or z == z1
                if y == deck:
                    w.set(x, y, z, *((B.PLANKS, 1) if shell else (B.PLANKS, 0)))
                    if shell:
                        w.set(x, y + 1, z, B.FENCE)
                elif shell:
                    w.set(x, y, z, B.PLANKS, 1)
                else:
                    w.set(x, y, z, B.AIR)
                F.ship_cells.add((x, z))


def albatross(w, F):
    """The Albatross, moored at Port Aerie's pier: a spruce hull along z, its bow north to Cloudstep, an
    orange and white envelope, a propeller astern, a gangway off the bow onto Cloudstep."""
    a = P.ALBATROSS
    xc, z0, z1, deck = a["x"], a["z0"], a["z1"], a["deck"]
    claim(F, "the Albatross", (int(xc - a["half"]) - 1, z0 - 1, int(xc + a["half"]) + 1, z1 + 1))
    hull_z(w, F, xc, z0, z1, deck, a["half"])
    # a cabin aft, the wheel on its roof
    for x in range(xc - 2, xc + 3):
        for z in range(z1 - 6, z1 - 2):
            edge = x in (xc - 2, xc + 2) or z in (z1 - 6, z1 - 3)
            for yy in range(deck + 1, deck + 4):
                w.set(x, yy, z, *((B.PLANKS, 1) if edge else (B.AIR, 0)))
            w.set(x, deck + 4, z, B.WOOD_SLAB, 1)
    for yy in (deck + 1, deck + 2):
        w.set(xc, yy, z1 - 6, B.AIR)
    w.chest(xc, deck + 1, z1 - 4, [(0, "minecraft:arrow", 32, 0), (1, "minecraft:golden_apple", 1, 0)], facing=2)
    w.set(xc, deck + 5, z1 - 4, B.FENCE)
    ey = deck + 11
    envelope(w, xc, ey, (z0 + z1) / 2, 5, 5, 12, [1, 0], stripes="x2") if False else None
    for x in range(int(xc - 6), int(xc + 7)):
        for z in range(z0 - 1, z1 + 2):
            for y in range(ey - 6, ey + 6):
                q = ((x - xc) / 5.0) ** 2 + ((y - ey) / 5.0) ** 2 + ((z - (z0 + z1) / 2) / 12.5) ** 2
                if q <= 1 and q > 0.62:
                    w.set(x, y, z, B.WOOL, 1 if (z // 3) % 2 else 0)
    for z in range(z0 + 3, z1 - 1, 5):
        for x in (int(xc - a["half"]) + 1, int(xc + a["half"])):
            for yy in range(deck + 2, ey - 4):
                if w.id(x, yy, z) == B.AIR:
                    w.set(x, yy, z, B.FENCE)
    # the propeller astern
    w.set(xc, deck - 1, z1 + 1, B.IRON_BLOCK)
    for k in (1, 2, 3):
        w.set(xc + k, deck - 1, z1 + 2, B.FENCE); w.set(xc - k, deck - 1, z1 + 2, B.FENCE)
        w.set(xc, deck - 1 + k, z1 + 2, B.FENCE); w.set(xc, deck - 1 - k, z1 + 2, B.FENCE)
    # the gangway off the bow onto Cloudstep
    cx, cz = ISL["cloudstep"]["at"]
    gx0 = xc
    for z in range(z0 - 6, z0 + 1):
        for x in (xc - 1, xc, xc + 1):
            if land(F, x, z):
                continue
            w.set(x, deck, z, B.PLANKS, 0)
            F.bridge_cells.add((x, z))
        for x in (xc - 2, xc + 2):
            if not land(F, x, z):
                w.set(x, deck + 1, z, B.FENCE)
    for z in range(z0 - 2, z0 + 1):
        for x in (xc - 1, xc, xc + 1):
            for yy in (deck + 1, deck + 2):
                if w.id(x, yy, z) in (B.FENCE,):
                    w.set(x, yy, z, B.AIR)
    F.albatross = dict(deck=deck)


# ---------------------------------------------------------------------------------------------------------
# balloons and the small rocks

COLOURWAYS = [[1, 4], [10, 0], [5, 13], [9, 0], [6, 0]]


def balloon(w, F, x, z, floor, k, kind):
    """A hot-air balloon: a 5 by 5 basket of spruce with a rope rail and gaps on two sides, four ropes up to
    a striped envelope, a burner of glowstone in its mouth. A tethered one has its rope to the nearest rock."""
    claim(F, f"balloon {k}", (x - 2, z - 2, x + 2, z + 2))
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            w.set(x + dx, floor, z + dz, B.PLANKS, 1)
            rim = max(abs(dx), abs(dz)) == 2
            gap = (dx == 0 and abs(dz) == 2) or (dz == 0 and abs(dx) == 2)
            if rim and not gap:
                w.set(x + dx, floor + 1, z + dz, B.SPRUCE_FENCE)
            F.ship_cells.add((x + dx, z + dz))
    for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        for yy in range(floor + 2, floor + 6):
            w.set(x + dx, yy, z + dz, B.FENCE)
    cy = floor + 12
    envelope(w, x, cy, z, 6.5, 7.5, 6.5, COLOURWAYS[k % len(COLOURWAYS)], stripes="gores", gores=10)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            for yy in range(cy - 8, cy - 5):
                if abs(dx) + abs(dz) < 2 and w.id(x + dx, yy, z + dz) == B.WOOL:
                    w.set(x + dx, yy, z + dz, B.AIR)
    w.set(x, floor + 5, z, B.GLOWSTONE)
    w.set(x, floor + 4, z, B.IRON_BARS)
    if kind == "tethered":
        best = None
        for ix in range(F.nx):
            pass
        pts = np.argwhere(F.land & (F.key == "highmoor"))
        d = np.hypot(pts[:, 0] + F.x0 - x, pts[:, 1] + F.z0 - z)
        tx, tz = pts[np.argmin(d)] + (F.x0, F.z0)
        ty = H(F, int(tx), int(tz))
        n = int(max(abs(tx - x), abs(tz - z), floor - ty)) * 2
        for t in np.linspace(0, 1, n):
            w.set(int(round(x + (tx - x) * t)), int(round(floor - 1 + (ty + 1 - floor + 1) * t)), int(round(z + (tz - z) * t)), B.FENCE)
    F.balloons.append((x, z, floor))


def ruined_arch(w, F):
    cx, cz = ISL["northreach"]["at"]
    y = H(F, cx, cz)
    claim(F, "the ruined arch", (cx - 4, cz - 1, cx + 4, cz + 1))
    for x in (cx - 3, cx + 3):
        for yy in range(y + 1, y + 8 - (2 if x > cx else 0)):
            w.set(x, yy, cz, B.STONEBRICK, 2 if RNG.random() < 0.3 else 1 if RNG.random() < 0.4 else 0)
    for x in range(cx - 3, cx):
        w.set(x, y + 8, cz, B.STONEBRICK, 0)
    w.set(cx, y + 8, cz, B.STONEBRICK_STAIRS, 1)
    for k in range(4):
        w.set(cx + RNG.integers(-3, 4), y + 1, cz + RNG.integers(-3, 4), B.STONEBRICK, 2)


def brazier(w, F):
    cx, cz = ISL["southreach"]["at"]
    y = H(F, cx, cz)
    claim(F, "the brazier", (cx - 1, cz - 1, cx + 1, cz + 1))
    w.set(cx, y + 1, cz, B.COBBLE_WALL)
    w.set(cx, y + 2, cz, B.COBBLE_WALL)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(cx + dx, y + 3, cz + dz, B.COBBLE if dx or dz else B.NETHERRACK)
    w.set(cx, y + 4, cz, 51)                # fire, which burns on netherrack for ever


def dovecote(w, F):
    cx, cz = ISL["fernrock"]["at"]
    y = H(F, cx, cz)
    claim(F, "the dovecote", (cx - 1, cz - 1, cx + 1, cz + 1))
    for yy in range(y + 1, y + 5):
        w.set(cx, yy, cz, B.LOG, 0)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            w.set(cx + dx, y + 5, cz + dz, B.PLANKS, 0)
            w.set(cx + dx, y + 6, cz + dz, B.PLANKS, 0 if dx or dz else 0)
            w.set(cx + dx, y + 7, cz + dz, B.WOOD_SLAB, 1)
    w.set(cx + 1, y + 6, cz, B.AIR); w.set(cx - 1, y + 6, cz, B.AIR)


def lookout(w, F):
    """Sentinel Rock's lookout: a timber platform on four posts, a ladder up."""
    cx, cz = ISL["sentinel"]["at"]
    cx, cz = cx - 4, cz + 1                  # off the line of the two bridges that cross the rock
    y = H(F, cx, cz)
    claim(F, "the lookout", (cx - 2, cz - 2, cx + 2, cz + 2))
    for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        g = H(F, cx + dx, cz + dz) if land(F, cx + dx, cz + dz) else y
        for yy in range(g + 1, y + 6):
            w.set(cx + dx, yy, cz + dz, B.LOG, 0)
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            w.set(cx + dx, y + 6, cz + dz, B.PLANKS, 0)
            if max(abs(dx), abs(dz)) == 2:
                w.set(cx + dx, y + 7, cz + dz, B.FENCE)
    w.set(cx, y + 6, cz + 1, B.AIR)
    for yy in range(y + 1, y + 7):
        w.set(cx, yy, cz + 1, B.LADDER, 2)
    w.set(cx, y + 7, cz + 2, B.AIR) if False else None


def build(w, F):
    F.things, F.conflicts, F.bridge_cells, F.ship_cells, F.bridges, F.balloons = [], [], set(), set(), [], []
    RECORDS.clear()
    keep(w, F)
    windmill(w, F)
    gazebo(w, F)
    sunken_garden(w, F)
    port(w, F)
    albatross(w, F)
    concord(w, F)
    lookout(w, F)
    ruined_arch(w, F)
    brazier(w, F)
    dovecote(w, F)
    from terrain import waterfall
    F.falls = [waterfall(w, F, P.SPAWN[0] - 4, P.SPAWN[1] - 12), waterfall(w, F, ISL["gardens"]["at"][0] - 8, ISL["gardens"]["at"][1] + 6)]
    for a, b in P.BRIDGES:
        cells = bridge(w, F, a, b)
        for x, z, y in cells:
            for n, (a0, b0, a1, b1) in F.things:
                if a0 <= x <= a1 and b0 <= z <= b1 and (f"bridge {a}-{b}", n) not in [c[:2] for c in F.conflicts]:
                    F.conflicts.append((f"bridge {a}-{b}", n, (x, z)))
    for k, (x, z, floor, kind) in enumerate(P.BALLOONS):
        balloon(w, F, x, z, floor, k, kind)
    F.records = RECORDS
