"""Red's station on the plateau: the yard levelled at the cliff's edge, the spawn's shelter, the head house over
the stair, the drop's railed mouth, two vent stacks, the antenna mast, the fuel tank, and the cutting that climbs
the cliff from the snowfield to the yard.
"""
import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.core import orient

TEAM = (B.STAINED_CLAY, 14)


def cell(x, z, blocks, size=3):
    h = ((x // size) * 73856093 ^ (z // size) * 19349663) & 0xFFFF
    return blocks[h % len(blocks)]


def level(w, x, z, top_y, fill=(B.STONE, 0)):
    """A column made to stand exactly at top_y: rock filled up to it, everything over it cleared."""
    for y in range(1, top_y):
        if w.id(x, y, z) == B.AIR and y > top_y - 12:
            w.set(x, y, z, *fill)
    for y in range(top_y + 1, w.ids.shape[1]):
        w.set(x, y, z, B.AIR)


def yard(w):
    Y = P.YARD
    holes = [(P.SHAFT["x0"], P.SHAFT["x1"], P.SHAFT["z0"], P.SHAFT["z1"]),
             (P.DROP["x0"], P.DROP["x1"], P.DROP["z0"], P.DROP["z1"])]
    for x in range(Y["x0"] - 1, Y["x1"] + 8):
        for z in range(Y["z0"] - 1, Y["z1"] + 3):
            if any(a <= x <= b and c <= z <= d for a, b, c, d in holes):
                continue
            inner = Y["x0"] <= x <= Y["x1"] and Y["z0"] <= z <= Y["z1"] or 30 <= x <= 37 and 80 <= z <= 86
            if not inner:
                continue
            level(w, x, z, Y["top"])
            w.set(x, Y["top"], z, *cell(x, z, [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]))
    for x in range(Y["x0"], Y["x1"] + 1):                          # a rail along the cliff's edge
        z = Y["z0"]
        if w.id(x, Y["top"], z) != B.AIR and not P.SHAFT["x0"] <= x <= P.SHAFT["x1"]:
            w.set(x, Y["top"] + 1, z, B.NETHER_FENCE)


def shelter(w):
    """The spawn's shelter: four nether-brick piers under a slab roof banded in the team's colour, open toward the
    fissure."""
    a = P.SPAWN_AREA
    roof = P.TOP + 5
    for x in range(a.x0, a.x1 + 1):
        for z in range(a.z0, a.z1 + 1):
            edge = x in (a.x0, a.x1) or z in (a.z0, a.z1)
            w.set(x, roof, z, *(TEAM if edge and (x + z) % 2 else (B.DSLAB, 0)))
    for x in (a.x0, a.x1):
        for z in (a.z0, a.z1, (a.z0 + a.z1) // 2):
            for y in range(P.TOP, roof):
                w.set(x, y, z, B.NETHER_BRICK)
    for x in range(a.x0 + 1, a.x1):                                 # its back wall
        for y in range(P.TOP, roof):
            w.set(x, y, a.z1, B.NETHER_BRICK if (x + y) % 5 else B.STONEBRICK)


def head_house(w):
    """The head house over the stair: walls of nether brick round the shaft's top, a door to the yard at the stair's
    last step, a slab roof."""
    sh = P.SHAFT
    roof = P.TOP + 6
    dx, dz, _ = P.DOORS[0]
    for x in range(sh["x0"], sh["x1"] + 1):
        for z in range(sh["z0"], sh["z1"] + 1):
            wall = x in (sh["x0"], sh["x1"]) or z in (sh["z0"], sh["z1"])
            if wall:
                for y in range(P.TOP, roof):
                    door = (x, z) == (dx, dz) and y < P.TOP + 3
                    w.set(x, y, z, B.AIR if door else B.NETHER_BRICK)
            w.set(x, roof, z, B.DSLAB)


def drop_mouth(w):
    d = P.DROP
    for x in range(d["x0"] - 1, d["x1"] + 2):
        for z in range(d["z0"] - 1, d["z1"] + 2):
            if not (d["x0"] <= x <= d["x1"] and d["z0"] <= z <= d["z1"]):
                w.set(x, P.TOP - 1, z, B.STAINED_CLAY, 4 if (x + z) % 2 else 15)
                if x == d["x1"] + 1 or z == d["z1"] + 1:
                    w.set(x, P.TOP, z, B.IRON_BARS)


def stack(w, x, z, height):
    for y in range(P.TOP, P.TOP + height):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                hollow = dx == 0 and dz == 0
                w.set(x + dx, y, z + dz, *((B.AIR, 0) if hollow else (B.STONEBRICK, 0) if y % 6 else (B.NETHER_BRICK, 0)))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                w.set(x + dx, P.TOP + height, z + dz, B.COBBLE_WALL)


def mast(w, x, z, height):
    for y in range(P.TOP, P.TOP + height):
        w.set(x, y, z, B.IRON_BARS)
        if y % 5 == 0:
            for a in (-1, 1):
                w.set(x + a, y, z, B.NETHER_FENCE)
                w.set(x, y, z + a, B.NETHER_FENCE)
    w.set(x, P.TOP + height, z, B.REDSTONE_LAMP)


def tank(w, cx, cz, r, height):
    for x in range(cx - r - 1, cx + r + 2):
        for z in range(cz - r - 1, cz + r + 2):
            d = np.hypot(x - cx, z - cz)
            if d <= r:
                for y in range(P.TOP - 1, P.TOP + height):
                    w.set(x, y, z, B.QUARTZ, 0 if (y - P.TOP) % 4 else 1)
                w.set(x, P.TOP + height, z, B.SLAB, 7)


def cutting(w):
    """The cutting up the cliff: the flight opened to the sky, retaining walls of stone brick either side."""
    f = next(fl for fl in P.FLIGHTS if fl.name == "the cutting")
    for x, z, feet in f.cells():
        for y in range(feet + 3, w.ids.shape[1]):
            w.set(x, y, z, B.AIR)
    for z in range(min(f.z0, f.z1), max(f.z0, f.z1) + 1):
        feet = f.feet_at(z)
        for x in (f.x0 - 1, f.x1 + 1):
            top = w.ids[x - w.x0, :, z - w.z0]
            solid = np.nonzero(top)[0]
            hi = int(solid.max()) if len(solid) else feet
            for y in range(feet - 1, max(feet + 1, hi + 1)):
                w.set(x, y, z, B.STONEBRICK, 0 if y % 4 else 2)
            w.set(x, max(feet + 1, hi + 1), z, B.NETHER_FENCE)


def build(w):
    yard(w)
    cutting(w)
    shelter(w)
    head_house(w)
    drop_mouth(w)
    stack(w, 5, 82, 10)
    stack(w, 29, 64, 13)
    mast(w, 27, 83, 20)
    tank(w, 41, 74, 3, 6)
