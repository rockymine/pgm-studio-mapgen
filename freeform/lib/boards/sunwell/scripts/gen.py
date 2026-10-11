"""Generate Sunwell from the plan: the cenote's wall, the nine shelves with their rims, pools, shafts and hills, the
falls down both side walls, the lake with its islet and the spring, the jungle on the rim; and the dressing that
makes it a cenote: vines and roots down the walls, moss and ferns on the shelves, broken ruins at their backs,
stalactites under them.

    python3 gen.py <build-dir>

The shaft is a circle on the middle of block (0, 0), so the left side is the right's mirror block for block; only
the dressing is drawn from noise and differs side to side, and never where a player drops or lands.
"""
import math
import random
import sys
import time

import numpy as np

import noise
import plan as P
from mc import World, B

R = P.R_SHAFT
X0, X1, Z0, Z1 = -32, 31, -32, 31
SY = 256
RIM_Y = 246
LAKE_FLOOR = 30
rng = random.Random(17)

STONE, ANDESITE, MOSSY, COBBLE, GRAVEL = (B.STONE, 0), (B.STONE, 5), (B.MOSSY, 0), (B.COBBLE, 0), (B.GRAVEL, 0)
SBRICK, SB_MOSSY, SB_CRACKED, SB_CHISEL = (B.STONEBRICK, 0), (B.STONEBRICK, 1), (B.STONEBRICK, 2), (B.STONEBRICK, 3)
GRASS, DIRT, PODZOL, CLAY = (B.GRASS, 0), (B.DIRT, 0), (B.DIRT, 2), (B.CLAY, 0)
JUNGLE_LOG, JUNGLE_LEAVES, DARK_LOG = (B.LOG, 3), (B.LEAVES, 3 | 4), (B.LOG2, 1)
MOSSY_WALL = (B.COBBLE_WALL, 1)
WHITE_CLAY = (B.STAINED_CLAY, 0)
WN = noise.fbm((X1 - X0 + 1, Z1 - Z0 + 1), 7, 3, seed=21)          # the wall's face
YN = noise.fbm((64, SY // 4), 6, 3, seed=22)                        # how it varies with height


def wall_r(x, z, y):
    """The wall's radius at a column and a height: never inside the shaft's circle, recessed by up to three."""
    a = (math.atan2(z, x) + math.pi) / (2 * math.pi)
    v = YN[int(a * 63) % 64, min(y // 4, SY // 4 - 1)]
    return R + max(0.0, 1.6 + 2.2 * v + 1.2 * WN[x - X0, z - Z0])


def rock(y):
    band = (y // 5) % 7
    return ANDESITE if band == 2 else (B.STONE, 1) if band == 5 and rng.random() < 0.4 else STONE


def shelf_band(y):
    """The shelf k whose rock occupies height y, or None."""
    for k in range(P.N_SHELVES):
        if P.shelf_y(k) - P.THICK + 1 <= y <= P.shelf_y(k) + 2:
            return k
    return None


# ---- the wall, the shelves, the lake -------------------------------------------------------------------------
def wall_and_shelves(w):
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            d = math.hypot(x, z)
            inside = x * x + z * z <= R * R
            for y in range(0, RIM_Y + 1):
                if y <= LAKE_FLOOR:
                    w.set(x, y, z, *rock(y))
                    continue
                k = shelf_band(y)
                if k is not None and P.shelf_y(k) - P.THICK < y <= P.shelf_y(k) and (P.on_shelf(k, x, z) or (
                        not inside and on_side(k, z))):
                    w.set(x, y, z, *rock(y))                     # a shelf runs into the wall, no gap behind it
                    continue
                if not inside and d >= wall_r(x, z, y):
                    w.set(x, y, z, *rock(y))
            if not inside:
                top = RIM_Y + int(2 + 2 * WN[x - X0, z - Z0])
                for y in range(RIM_Y, top + 1):
                    w.set(x, y, z, *DIRT)
                w.set(x, top, z, *GRASS)
    # the shelves' tops: grass and moss where a player walks
    for k in range(P.N_SHELVES):
        y = P.shelf_y(k)
        for x in range(-R, R + 1):
            for z in range(-R, R + 1):
                if P.on_shelf(k, x, z):
                    r = rng.random()
                    w.set(x, y, z, *(GRASS if r < 0.55 else MOSSY if r < 0.75 else PODZOL if r < 0.9 else COBBLE))
                    w.set(x, y - 1, z, *DIRT)
    # the lake and its islet
    for x in range(-R - 3, R + 4):
        for z in range(-R - 3, R + 4):
            if x * x + z * z <= R * R:
                w.set(x, LAKE_FLOOR, z, *(CLAY if rng.random() < 0.4 else GRAVEL))
                for y in range(LAKE_FLOOR + 1, P.LAKE_Y + 1):
                    w.set(x, y, z, B.WATER)
    i = P.ISLET
    k = len(P.DROPS) - 1
    for x in range(i["x"][0], i["x"][1] + 1):
        for s in range(i["s"][0], i["s"][1] + 1):
            z = P.z_of(k, s)
            corner = x in i["x"] and s in i["s"]
            if corner:
                continue
            for y in range(LAKE_FLOOR + 1, i["y"] + 1):
                w.set(x, y, z, *rock(y))
            w.set(x, i["y"], z, *(GRASS if rng.random() < 0.7 else MOSSY))


def on_side(k, z):
    return z <= P.EDGE if P.side(k) == "N" else z >= -P.EDGE


# ---- what is set into the shelves ---------------------------------------------------------------------------
def frame_cells(k, x0, x1, s0, s1):
    for x in range(x0, x1 + 1):
        for s in range(s0, s1 + 1):
            yield x, P.z_of(k, s)


def pools_and_shafts(w):
    for k in range(len(P.DROPS)):
        if P.DROPS[k].get("lake"):
            continue
        y = P.shelf_y(k + 1)
        for name, x0, x1, s0, s1, sd in P.pools(k):
            for x, z in frame_cells(k, x0, x1, s0, s1):
                for yy in range(y - 2, y + 1):
                    w.set(x, yy, z, B.WATER)
                w.set(x, y - 3, z, *(CLAY if (x + z) % 2 else GRAVEL))
            for x in range(x0 - 1, x1 + 2):                     # a lip of mossy stone brick round the pool
                for z in (P.z_of(k, s0 - 1), P.z_of(k, s1 + 1)):
                    if w.id(x, y, z) != B.WATER and P.on_shelf(k + 1, x, z):
                        w.set(x, y, z, *(SB_MOSSY if rng.random() < 0.5 else SBRICK))
            for s in range(s0 - 1, s1 + 2):
                for x in (x0 - 1, x1 + 1):
                    z = P.z_of(k, s)
                    if w.id(x, y, z) != B.WATER and P.on_shelf(k + 1, x, z):
                        w.set(x, y, z, *(SB_MOSSY if rng.random() < 0.5 else SBRICK))
        for name, x0, x1, s0, s1, sd in P.shafts(k):
            for x, z in frame_cells(k, x0, x1, s0, s1):
                for yy in range(y - P.THICK - 1, y + 3):
                    w.set(x, yy, z, B.AIR)
            for x in range(x0 - 1, x1 + 2):                     # the shaft's mouth ringed with chiselled stone
                for s in (s0 - 1, s1 + 1):
                    z = P.z_of(k, s)
                    if w.id(x, y, z) not in (B.WATER, 0):
                        w.set(x, y, z, *SB_CHISEL)
            for s in range(s0, s1 + 1):
                for x in (x0 - 1, x1 + 1):
                    z = P.z_of(k, s)
                    if w.id(x, y, z) not in (B.WATER, 0):
                        w.set(x, y, z, *SB_CHISEL)


def falls(w):
    """Water off both side walls at every shelf's edge: a stream across the shelf from the wall, a curtain of
    falling water two thick just past the edge, and a basin two deep on the shelf below."""
    for k in range(len(P.DROPS)):
        if P.DROPS[k].get("lake"):
            continue
        ya, yb = P.shelf_y(k), P.shelf_y(k + 1)
        for name, x0, x1, s0, s1, sd in P.falls(k):
            for x in range(x0, x1 + 1):
                for s in (1, 2):
                    z = P.z_of(k, s)
                    for y in range(yb + 1, ya + 1):
                        if x * x + z * z <= R * R:
                            w.set(x, y, z, B.WATER_FLOW, 8)
                for s in range(s0, s1 + 1):                      # the basin
                    z = P.z_of(k, s)
                    if P.on_shelf(k + 1, x, z):
                        w.set(x, yb, z, B.WATER)
                        w.set(x, yb - 1, z, B.WATER)
                # the stream on the shelf above: from the shelf's back to its edge
                ze = P.EDGE if P.side(k) == "N" else -P.EDGE
                step = -1 if P.side(k) == "N" else 1
                for zz in range(ze, ze + step * 6, step):
                    if P.on_shelf(k, x, zz):
                        w.set(x, ya, zz, B.WATER)
                        w.set(x, ya - 1, zz, *MOSSY)


def rims(w):
    """The low wall along every shelf's edge, open over its targets; mossy cobble walls, too tall to step over."""
    for k in range(len(P.DROPS)):
        if P.DROPS[k].get("lake"):
            continue
        y = P.shelf_y(k)
        ze = P.EDGE if P.side(k) == "N" else -P.EDGE
        gaps = P.gaps(k)
        for x in range(-R, R + 1):
            if not P.on_shelf(k, x, ze):
                continue
            if any(g[1] <= x <= g[2] for g in gaps):
                continue
            w.set(x, y + 1, ze, *MOSSY_WALL)


def hills(w):
    """Each hill's border marked in white clay, which PGM recolours to its holder: the shelf's top round the hill,
    where it is not water."""
    for k in range(len(P.DROPS)):
        y = P.shelf_y(k + 1) if not P.DROPS[k].get("lake") else P.ISLET["y"]
        for name, x0, x1, s0, s1, sd in P.hills(k):
            for x, z in frame_cells(k, x0, x1, s0, s1):
                border = x in (x0, x1) or z in (P.z_of(k, s0), P.z_of(k, s1))
                if border and w.id(x, y, z) not in (B.WATER, 0):
                    w.set(x, y, z, *WHITE_CLAY)
            for x, z in ((x0, P.z_of(k, s0)), (x1, P.z_of(k, s0)), (x0, P.z_of(k, s1)), (x1, P.z_of(k, s1))):
                if w.id(x, y, z) not in (B.WATER, 0) and w.id(x, y + 1, z) == 0:
                    w.set(x, y + 1, z, B.WOOL, 0)                   # a white post at each corner


def spring(w):
    """The spring: a lit grotto in the lake's far wall, at the water, that sends a player back to the top."""
    x0, x1 = P.SPRING["x"]
    z0, z1 = P.SPRING["z"]
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 5):
            for y in range(P.LAKE_Y - 2, P.LAKE_Y + 4):
                if y <= P.LAKE_Y:
                    w.set(x, y, z, B.WATER)
                else:
                    w.set(x, y, z, B.AIR)
            w.set(x, P.LAKE_Y + 4, z, *(B.GLOWSTONE, 0) if (x + z) % 3 == 0 else SB_MOSSY)
    for x in (x0 - 1, x1 + 1):
        for y in range(P.LAKE_Y + 1, P.LAKE_Y + 5):
            w.set(x, y, z0, *SB_CHISEL)
    for x in range(x0 - 1, x1 + 2):
        w.set(x, P.LAKE_Y + 5, z0, *SB_CHISEL)


# ---- dressing, never where a player drops or lands -----------------------------------------------------------
def keep_clear():
    """The cells over which a player drops or lands: every target and its drop column, every gap's approach."""
    keep = set()
    for k in range(len(P.DROPS)):
        for name, x0, x1, s0, s1, sd in P.pools(k) + P.shafts(k) + P.falls(k) + P.hills(k):
            for x, z in frame_cells(k, x0 - 2, x1 + 2, s0 - 2, s1 + 2):
                keep.add((k + 1, x, z))
        for g in P.gaps(k):
            for x in range(g[1] - 1, g[2] + 2):
                for dz in range(-4, 5):
                    keep.add((k, x, (P.EDGE if P.side(k) == "N" else -P.EDGE) + dz))
    return keep


def dressing(w):
    keep = keep_clear()
    # vines down the wall's face, roots hanging from the rim and under each shelf
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            if x * x + z * z > (R + 4) ** 2:
                continue
            for y in range(LAKE_FLOOR + 9, RIM_Y):
                if w.id(x, y, z) != 0:
                    continue
                for dx, dz, data in ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1)):
                    nb = w.id(x + dx, y, z + dz)
                    if nb in (B.STONE,) and (x + dx) ** 2 + (z + dz) ** 2 > R * R and rng.random() < 0.08:
                        for yy in range(y, y - rng.randint(3, 14), -1):
                            if w.id(x, yy, z) != 0 or w.id(x + dx, yy, z + dz) == 0:
                                break
                            w.set(x, yy, z, B.VINE, data)
                        break
    # stalactites and roots under the shelves' overhangs, and on the shelves ferns, grass and broken ruins
    for k in range(P.N_SHELVES):
        y = P.shelf_y(k)
        for x in range(-R, R + 1):
            for z in range(-R, R + 1):
                if not P.on_shelf(k, x, z):
                    continue
                if rng.random() < 0.05:
                    n = rng.randint(1, 5)
                    for yy in range(y - P.THICK, y - P.THICK - n, -1):
                        w.set(x, yy, z, *(STONE if yy > y - P.THICK - n + 1 else COBBLE))
                elif rng.random() < 0.03:
                    for yy in range(y - P.THICK, y - P.THICK - rng.randint(2, 6), -1):
                        w.set(x, yy, z, *DARK_LOG)
                if (k, x, z) in keep or w.id(x, y, z) in (B.WATER, B.WATER_FLOW) or w.id(x, y + 1, z) != 0:
                    continue
                if w.id(x, y, z) in (B.GRASS,) and rng.random() < 0.3:
                    w.set(x, y + 1, z, B.TALLGRASS, 2 if rng.random() < 0.6 else 1)
        # a ruin at the shelf's back: broken pillars and a fallen lintel, against the wall
        ang = rng.uniform(0.2, 0.8) * math.pi * (-1 if P.side(k) == "N" else 1)
        cx, cz = int(round(15 * math.cos(ang))), int(round(15 * math.sin(ang)))
        if P.side(k) == "N":
            cz = -abs(cz)
        else:
            cz = abs(cz)
        for dx in (-2, 2):
            x, z = cx + dx, cz
            if P.on_shelf(k, x, z) and (k, x, z) not in keep:
                for yy in range(y + 1, y + 1 + rng.randint(2, 5)):
                    w.set(x, yy, z, *rng.choice([SBRICK, SB_MOSSY, SB_CRACKED]))
        for dx in range(-1, 2):
            if P.on_shelf(k, cx + dx, cz + 1) and (k, cx + dx, cz + 1) not in keep:
                w.set(cx + dx, y + 1, cz + 1, *SB_MOSSY)
    # the jungle on the rim
    for _ in range(60):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(R + 4, 31)
        x, z = int(rr * math.cos(a)), int(rr * math.sin(a))
        if not (X0 + 2 <= x <= X1 - 2 and Z0 + 2 <= z <= Z1 - 2):
            continue
        g = w.top(x, z)
        if g < RIM_Y:
            continue
        tree(w, x, g, z, rng.randint(6, 13))


def tree(w, x, g, z, h):
    for y in range(g + 1, g + h + 1):
        w.set(x, y, z, *JUNGLE_LOG)
    for dy, r in ((h - 1, 3), (h, 3), (h + 1, 2), (h + 2, 1)):
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if dx * dx + dz * dz <= r * r + 1 and w.id(x + dx, g + dy, z + dz) == 0:
                    w.set(x + dx, g + dy, z + dz, *JUNGLE_LEAVES)
    for dx, dz, data in ((1, 0, 2), (-1, 0, 8), (0, 1, 4), (0, -1, 1)):    # vines down the trunk
        for y in range(g + h - 2, g + h - 2 - rng.randint(0, 4), -1):
            if w.id(x + dx, y, z + dz) == 0:
                w.set(x + dx, y, z + dz, B.VINE, data)


def make():
    w = World(X0, Z0, X1 - X0 + 1, Z1 - Z0 + 1, sy=SY)
    wall_and_shelves(w)
    pools_and_shafts(w)
    falls(w)
    rims(w)
    spring(w)
    dressing(w)
    hills(w)
    w.biome[:, :] = 21                                                  # jungle
    return w


def main(build):
    t0 = time.time()
    w = make()
    w.save(build, "Sunwell", (0, P.TOP + 2, -14))
    print(f"generated and saved {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
