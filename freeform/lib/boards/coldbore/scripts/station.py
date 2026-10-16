"""Red's station on the plateau: the yard levelled over the reactor hall, the spiral stair up to it from level 0
and its head house, the great dish tilted at the sky over the fissure and the small satellite it talks to, two
signal towers either side of it, the operations block and the reactor's vent stacks; every wall of it in the
station's dark style, and boulders of the cliff's own beds lying in the snow.
"""
import numpy as np

import plan as P
from pgmvox import B
from pgmvox.core import orient
from pgmvox.scenery.forms import placed_box

import surface

TEAM = (B.STAINED_CLAY, 14)
BOULDERS = [(-62, 90, (6, 4, 5), 20), (-57, 85, (3, 3, 4), -30), (-30, 93, (5, 3, 4), 50), (-48, 95, (4, 3, 3), 10),
            (42, 92, (5, 4, 6), -15), (47, 87, (3, 2, 3), 35), (64, 62, (4, 3, 5), 60), (60, 67, (3, 3, 3), -45),
            (-70, 70, (4, 3, 4), 5), (34, 96, (3, 3, 4), 25)]                     # x, z, size, yaw
PAVING = [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)]


def cell(x, z, blocks, size=3):
    h = ((x // size) * 73856093 ^ (z // size) * 19349663) & 0xFFFF
    return blocks[h % len(blocks)]


def level(w, x, z, top_y, fill=(B.STONE, 0)):
    """A column made to stand exactly at top_y: rock filled down from it to whatever it stands on, everything over
    it cleared."""
    y = top_y
    while y > 1 and w.id(x, y, z) in (B.AIR, B.SNOW_LAYER):
        w.set(x, y, z, *fill)
        y -= 1
    for y in range(top_y + 1, w.ids.shape[1]):
        w.set(x, y, z, B.AIR)


def yard(w):
    """The yard the dish stands on, levelled and paved, held in by walls in the station's dark style wherever the
    plateau falls away from it or rises over it, a nether-brick kerb where it meets the plateau level."""
    Y = P.YARD
    top = Y["top"]
    for x in range(Y["x0"], Y["x1"] + 1):
        for z in range(Y["z0"], Y["z1"] + 1):
            level(w, x, z, top)
            w.set(x, top, z, *cell(x, z, PAVING))
    for x in range(Y["x0"], Y["x1"] + 1):
        for z in range(Y["z0"], Y["z1"] + 1):
            out = [(x + a, z + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if not (Y["x0"] <= x + a <= Y["x1"] and Y["z0"] <= z + b <= Y["z1"])]
            if not out:
                continue
            w.set(x, top, z, B.NETHER_BRICK)
            rib = (x + z) % 4 == 0
            low = min(column_top(w, ox, oz) for ox, oz in out)
            if low < top - 1:                                     # the plateau falls away: a wall under the edge
                for y in range(low + 1, top + 2):
                    w.set(x, y, z, *surface.dark(x, y, z, top + 1, rib))
            for ox, oz in out:                                    # the plateau rises over it: a retaining wall
                high = column_top(w, ox, oz)
                if high > top + 1:
                    for y in range(top + 1, high + 1):
                        w.set(ox, y, oz, *surface.dark(ox, y, oz, high, (ox + oz) % 4 == 0))


def dish(w):
    """The great dish: a paraboloid of quartz ribbed in iron, tilted at the southern sky, on a yoke over a
    pedestal, its feed horn held at the focus on three struts."""
    d = P.DISH
    t = np.radians(d["tilt"])
    axis = np.array([0.0, np.cos(t), -np.sin(t)])
    e1, e2 = np.array([1.0, 0.0, 0.0]), np.array([0.0, np.sin(t), np.cos(t)])
    centre = np.array([d["x"], d["y"], d["z"]], float)
    focal = 7.0
    r = d["r"]
    for u in np.arange(-r, r + 0.01, 0.35):
        for v in np.arange(-r, r + 0.01, 0.35):
            rr = np.hypot(u, v)
            if rr > r:
                continue
            rib = abs(u) < 0.4 or abs(v) < 0.4 or rr > r - 0.6
            for lift in (0.0, -0.5):
                p = centre + u * e1 + v * e2 + (rr * rr / (4 * focal) + lift) * axis
                x, y, z = (int(round(c)) for c in p)
                w.set(x, y, z, *((B.IRON_BLOCK, 0) if rib and lift == 0 else (B.QUARTZ, 0)))
    base = centre - 1.5 * axis
    bx, by, bz = (int(round(c)) for c in base)
    for y in range(P.YARD["top"] + 1, by):                         # the pedestal, in the station's dark style
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                corner = abs(dx) + abs(dz) == 2
                band = y == P.YARD["top"] + 3
                w.set(bx + dx, y, bz + dz, *(TEAM if band else (B.STONEBRICK, 0) if corner else (B.NETHER_BRICK, 0)))
    for dx in (-2, -1, 0, 1, 2):
        w.set(bx + dx, by, bz, B.IRON_BLOCK)
    for dx in (-2, 2):
        w.set(bx + dx, by + 1, bz, B.IRON_BLOCK)
    focus = centre + focal * axis
    fx, fy, fz = (int(round(c)) for c in focus)
    w.set(fx, fy, fz, B.IRON_BLOCK)
    w.set(fx, fy + 1, fz, B.NETHER_FENCE)                         # the feed's tip and its light
    w.set(fx, fy + 2, fz, B.REDSTONE_TORCH, 5)
    for ang in (90, 210, 330):
        a = np.radians(ang)
        rim = centre + r * 0.95 * (np.cos(a) * e1 + np.sin(a) * e2) + (r * r / (4 * focal)) * axis
        for x, y, z in surface.face_line(rim, focus):
            if w.id(x, y, z) == B.AIR:
                w.set(x, y, z, B.NETHER_FENCE)


def operations(w, x0, z0, x1, z1, height=6):
    """The operations block beside the dish: a low bunker in the station's dark style, slits of bars for windows,
    a door on its west side, consoles under the north wall, a roof of nether-brick slabs under snow."""
    y0 = P.YARD["top"] + 1
    top = y0 + height
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            if not edge:
                for y in range(y0, top - 1):
                    w.set(x, y, z, B.AIR)
                w.set(x, y0 - 1, z, B.STONE, 6)
                w.set(x, top - 1, z, B.SLAB, 6)
                w.set(x, top, z, B.SNOW_LAYER, 1)
                continue
            for y in range(y0, top + 1):
                slit = y == y0 + 2 and not corner and (x + z) % 3 == 0
                w.set(x, y, z, *((B.IRON_BARS, 0) if slit else surface.dark(x, y, z, top, corner or (x + z) % 4 == 0)))
    mz = (z0 + z1) // 2
    for y in (y0, y0 + 1, y0 + 2):
        w.set(x0, y, mz, B.AIR)
    for x in range(x0 + 2, x1 - 1, 2):
        w.set(x, y0, z1 - 1, B.IRON_BLOCK)
        w.set(x, y0 + 1, z1 - 1, B.REDSTONE_LAMP)


def satellite(w):
    """The satellite the dish is talking to, hung over the yard along the dish's axis: a body of iron, a wing of
    blue panels either side on a boom of bars, and a whip of fence."""
    d = P.DISH
    t = np.radians(d["tilt"])
    x, y, z = (int(round(c)) for c in (d["x"], d["y"] + 16 * np.cos(t), d["z"] - 16 * np.sin(t)))
    y = min(y, 125)
    w.set(x, y, z, B.IRON_BLOCK)
    w.set(x, y, z + 1, B.DISPENSER, 3)
    for side in (-1, 1):
        w.set(x + side, y, z, B.IRON_BARS)
        for k in range(2, 5):
            for dz in (0, 1):
                w.set(x + side * k, y, z + dz, B.STAINED_GLASS, 11)
    w.set(x, y + 1, z, B.NETHER_FENCE)


def stack(w, x, z, height):
    """A vent stack over the reactor hall: nether brick banded in stone brick every six, open at the top under a
    ring of nether fence."""
    y0 = P.YARD["top"] + 1
    for y in range(y0, y0 + height):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                hollow = dx == 0 and dz == 0
                w.set(x + dx, y, z + dz, *((B.AIR, 0) if hollow else (B.STONEBRICK, 0) if (y - y0) % 6 == 5
                                           else (B.NETHER_BRICK, 0)))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                w.set(x + dx, y0 + height, z + dz, B.NETHER_FENCE)


def column_top(w, x, z):
    col = w.ids[x - w.x0, :, z - w.z0]
    solid = np.nonzero((col != 0) & (col != B.SNOW_LAYER))[0]
    return int(solid.max()) if len(solid) else 0


def helix(w):
    """The spiral stair from the annex corridor up to the yard: a shaft lined in stone brick, its solid core lit
    every six blocks, stairs round the ring a block up a step with the lap above built down to four blocks over
    each, and a head house on the yard with its door over the stair's last step."""
    h = P.HELIX
    top = P.YARD["top"]
    for x in range(h["x0"] - 1, h["x1"] + 2):
        for z in range(h["z0"] - 1, h["z1"] + 2):
            ring = h["x0"] <= x <= h["x1"] and h["z0"] <= z <= h["z1"]
            core = h["x0"] < x < h["x1"] and h["z0"] < z < h["z1"]
            for y in range(P.L0, top + 5):
                if core:
                    lit = (y - P.L0) % 6 == 3 and y < top
                    w.set(x, y, z, *((B.SEA_LANTERN, 0) if lit else (B.STONE, 6)))
                elif ring:
                    w.set(x, y, z, B.AIR)
                else:
                    w.set(x, y, z, B.STONEBRICK, 0 if (x + y + z) % 5 else 2)
            if ring or core:
                w.set(x, top + 5, z, B.SLAB, 6)
                w.set(x, top + 6, z, B.SNOW_LAYER, 1)
            else:                                                 # the head house's walls, in the dark style
                corner = x in (h["x0"] - 1, h["x1"] + 1) and z in (h["z0"] - 1, h["z1"] + 1)
                for y in range(top + 1, top + 6):
                    w.set(x, y, z, *surface.dark(x, y, z, top + 5, corner))
    steps = P.helix()
    lap = len(steps) // 2
    for k, (x, z, feet) in enumerate(steps):
        for y in range(max(P.L0, feet - lap + 4), feet - 1):
            w.set(x, y, z, B.STONEBRICK)
        if k + 1 < len(steps):
            nx, nz, _ = steps[k + 1]
            way = {(1, 0): "e", (-1, 0): "w", (0, 1): "s", (0, -1): "n"}[(nx - x, nz - z)]
            w.set(x, feet - 1, z, *((B.STONEBRICK, 0) if k == 0 else (B.STONEBRICK_STAIRS, orient.stair(way))))
        else:
            w.set(x, feet - 1, z, B.STONEBRICK)
    x, z, feet = steps[-1]
    for y in range(feet, feet + 3):                              # the head house's door onto the yard
        w.set(x, y, z + 1, B.AIR)
    x, z, feet = steps[0]
    for y in range(feet, feet + 4):                              # the shaft's door from the annex corridor
        w.set(x, y, z + 1, B.AIR)


def boulders(w):
    """Boulders lying in the plateau's snow, cut from the cliff's own beds and capped with snow."""
    top = np.zeros((w.sx, w.sz), int)
    for i in range(w.sx):
        for k in range(w.sz):
            col = w.ids[i, :, k]
            solid = np.nonzero((col != 0) & (col != B.SNOW_LAYER))[0]
            top[i, k] = int(solid.max()) if len(solid) else 0
    rng = np.random.default_rng(83)
    for x, z, size, yaw in BOULDERS:
        placed_box(w, x, z, size, top, yaw=yaw, tilt=10, sink=0.35, paint=surface.bedded(rng))


def build(w):
    yard(w)
    helix(w)
    dish(w)
    operations(w, 14, 84, 23, 90)
    stack(w, -9, 72, 9)
    stack(w, 10, 66, 12)
    surface.signal_tower(w, -8, 76, 4)
    surface.signal_tower(w, 19, 78, 3)
    boulders(w)
    satellite(w)
