"""Red's station on the plateau: the yard levelled over the reactor hall, the spiral stair up to it from level 0
and its head house, the great dish tilted at the sky over the fissure and the small satellite it talks to, the
control house, the round observatory, the shed the winter brought down, the reactor's vent stacks, the signal
towers and the fuel tanks, every one standing on flat ground or on footings, and boulders of the cliff's own beds
lying in the snow.
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
    """A column made to stand exactly at top_y: rock filled up to it, everything over it cleared."""
    for y in range(top_y - 12, top_y):
        if w.id(x, y, z) == B.AIR:
            w.set(x, y, z, *fill)
    for y in range(top_y + 1, w.ids.shape[1]):
        w.set(x, y, z, B.AIR)


def yard(w):
    """The yard, paved and levelled, its edges eased into the plateau and railed along the cliff."""
    Y = P.YARD
    for x in range(Y["x0"], Y["x1"] + 1):
        for z in range(Y["z0"], Y["z1"] + 1):
            level(w, x, z, Y["top"])
            w.set(x, Y["top"], z, *cell(x, z, PAVING))
    for x in range(Y["x0"], Y["x1"] + 1):
        if w.id(x, Y["top"], Y["z0"] - 1) == B.AIR:
            w.set(x, Y["top"] + 1, Y["z0"], B.NETHER_FENCE)


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
    for y in range(P.YARD["top"] + 1, by):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(bx + dx, y, bz + dz, *((B.STONEBRICK, 0) if abs(dx) + abs(dz) < 2 else (B.STONEBRICK, 2)))
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


def house(w, x0, z0, x1, z1, height, door, wall=(B.STONEBRICK, 0), roof=(B.SLAB, 5)):
    """A flat-roofed house on the yard: walls with corner piers of nether brick, a window band of panes, a door
    in the wall named by `door` ("n" or "s" or "e" or "w"), a slab roof under snow."""
    y0 = P.YARD["top"] + 1
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            corner = x in (x0, x1) and z in (z0, z1)
            for y in range(y0, y0 + height):
                if not edge:
                    w.set(x, y, z, B.AIR)
                    continue
                window = y in (y0 + 2, y0 + 3) and not corner and (x + z) % 3
                w.set(x, y, z, *((B.NETHER_BRICK, 0) if corner else (B.PANE, 0) if window else wall))
            w.set(x, y0 + height, z, *roof)
            w.set(x, y0 + height + 1, z, B.SNOW_LAYER, 1)
            if not edge:
                w.set(x, y0 - 1, z, B.PLANKS, 1)
    mx, mz = (x0 + x1) // 2, (z0 + z1) // 2
    dx, dz = {"n": (mx, z0), "s": (mx, z1), "w": (x0, mz), "e": (x1, mz)}[door]
    for y in (y0, y0 + 1, y0 + 2):
        w.set(dx, y, dz, B.AIR)
    for x in range(x0, x1 + 1):
        w.set(x, y0 + height - 1, z0, *TEAM)


def control_house(w):
    house(w, 14, 84, 23, 90, 6, "w")
    y0 = P.YARD["top"] + 1
    for x in range(16, 22, 2):                                   # consoles under the north window
        w.set(x, y0, 89, B.IRON_BLOCK)
        w.set(x, y0 + 1, 89, B.REDSTONE_LAMP)


def observatory(w, cx, cz, r=3):
    """A round observatory: a drum of chiseled quartz with cyan panels and a ring of windows, a roof ring of nether
    brick standing out past it, a dome of cyan clay with a slit down its southern side, and the telescope's barrel
    reaching out of the slit."""
    y0 = P.YARD["top"] + 1
    eave = y0 + 4
    for x in range(cx - r - 1, cx + r + 2):
        for z in range(cz - r - 1, cz + r + 2):
            d = np.hypot(x - cx, z - cz)
            if r - 0.5 <= d <= r + 0.5:
                for y in range(y0, eave):
                    door = z == cz + r and x == cx and y < y0 + 2
                    window = y == y0 + 2 and (x + z) % 2
                    w.set(x, y, z, *((B.AIR, 0) if door else (B.PANE, 0) if window else
                                     (B.QUARTZ, 1) if (x + z) % 2 else (B.STAINED_CLAY, 9)))
            if d <= r + 1.2:
                w.set(x, eave, z, *((B.NETHER_BRICK, 0) if d > r - 0.5 else (B.STAINED_CLAY, 9)))
    for x in range(cx - r, cx + r + 1):
        for z in range(cz - r, cz + r + 1):
            for y in range(eave + 1, eave + r + 1):
                d = np.sqrt((x - cx) ** 2 + (y - eave) ** 2 + (z - cz) ** 2)
                if r - 0.6 <= d <= r + 0.4 and not (x == cx and z <= cz):
                    w.set(x, y, z, B.STAINED_CLAY, 9)
    for x, y, z in surface.face_line((cx, eave + 1, cz), (cx, eave + 4, cz - 3)):
        w.set(x, y, z, B.COBBLE_WALL)
    w.set(cx, eave + 5, cz - 3, B.IRON_BARS)


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


def fallen_shed(w, x0, z0, x1, z1):
    """A shed the winter brought down: two walls standing, the roof slid off them onto the yard, its frame
    showing."""
    y0 = P.YARD["top"] + 1
    for z in range(z0, z1 + 1):
        for y in range(y0, y0 + (4 if z < z1 - 1 else 2)):
            w.set(x0, y, z, B.PLANKS, 1)
    for x in range(x0, x1 + 1):
        for y in range(y0, y0 + (3 if x < x1 - 2 else 1)):
            w.set(x, y, z0, B.PLANKS, 1)
    for x in range(x0 + 1, x1 + 1):                               # the roof: on the west wall, slid to the yard
        for z in range(z0 + 1, z1 + 2):
            w.set(x, y0 + 3 if x - x0 <= 2 else y0, z, B.WOOD_SLAB, 1)
    for z in range(z0, z1 + 1, 2):
        w.set(x1 + 1, y0, z, B.LOG, 1 | 8)


def stack(w, x, z, height):
    y0 = P.YARD["top"] + 1
    for y in range(y0, y0 + height):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                hollow = dx == 0 and dz == 0
                w.set(x + dx, y, z + dz, *((B.AIR, 0) if hollow else (B.STONEBRICK, 0) if y % 6 else (B.NETHER_BRICK, 0)))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                w.set(x + dx, y0 + height, z + dz, B.COBBLE_WALL)


def tank(w, cx, cz, r, height):
    """A fuel tank of quartz in hoops, on the flattest ground near (cx, cz), a stone-brick plinth under it where the
    ground falls away."""
    cx, cz, base = surface.seat(w, cx, cz, r)
    cells = [(x, z) for x in range(cx - r, cx + r + 1) for z in range(cz - r, cz + r + 1) if np.hypot(x - cx, z - cz) <= r]
    surface.footings(w, cells, base)
    for x, z in cells:
        for y in range(base + 1, base + 1 + height):
            w.set(x, y, z, B.QUARTZ, 0 if (y - base) % 4 else 1)
        w.set(x, base + 1 + height, z, B.SLAB, 7)
        w.set(x, base + 2 + height, z, B.SNOW_LAYER, 1)


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
            if ring or not core:
                w.set(x, top + 5, z, B.DSLAB)
                w.set(x, top + 6, z, B.SNOW_LAYER, 1)
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
    for xx in range(h["x0"] - 1, h["x1"] + 2):                    # the team's band over the door
        w.set(xx, top + 4, h["z1"] + 1, *TEAM)


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
    control_house(w)
    observatory(w, -5, 87, 3)
    fallen_shed(w, 0, 66, 6, 71)
    stack(w, -9, 72, 9)
    stack(w, 10, 66, 12)
    surface.signal_tower(w, 10, 92, 4)
    surface.signal_tower(w, -40, 82, 3)
    tank(w, 34, 80, 3, 6)
    tank(w, 40, 73, 2, 5)
    boulders(w)
    satellite(w)
