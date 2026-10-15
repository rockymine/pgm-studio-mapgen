"""Red's station on the plateau: the yard levelled over the reactor hall, the great dish tilted at the sky over the
fissure, the control house, the radome, the shed the winter brought down, the reactor's vent stacks, the mast,
the fuel tanks, the cutting that climbs from the east hill to the plateau, and the spruces that outlived the ash.
"""
import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.scenery import trees

TEAM = (B.STAINED_CLAY, 14)
CLUMPS = [(-62, 90, 8, 5), (-30, 93, 6, 3), (42, 92, 7, 4), (64, 62, 6, 3)]   # x, z, reach, trees: what survived
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
    w.set(*(int(round(c)) for c in focus), B.IRON_BLOCK)
    for ang in (90, 210, 330):
        a = np.radians(ang)
        rim = centre + r * 0.95 * (np.cos(a) * e1 + np.sin(a) * e2) + (r * r / (4 * focal)) * axis
        for s in np.linspace(0, 1, 24):
            p = rim + (focus - rim) * s
            x, y, z = (int(round(c)) for c in p)
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


def radome(w, cx, cz, r=4):
    """A radome: a sphere of white clay on a ring wall, its panels traced in a grid of quartz."""
    y0 = P.YARD["top"] + 1
    cy = y0 + 2 + r
    for x in range(cx - r - 1, cx + r + 2):
        for z in range(cz - r - 1, cz + r + 2):
            for y in range(y0, cy + r + 1):
                d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
                if r - 0.6 <= d <= r + 0.4:
                    w.set(x, y, z, *((B.QUARTZ, 0) if (x + y + z) % 4 == 0 else (B.STAINED_CLAY, 0)))
                elif y < cy - r + 2 and np.hypot(x - cx, z - cz) <= r - 1 and np.hypot(x - cx, z - cz) > r - 2:
                    w.set(x, y, z, B.STONEBRICK)


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
    for x in range(x0 + 1, x1 + 1):
        for z in range(z0 + 1, z1 + 2):
            sag = 1 if x - x0 > (x1 - x0) // 2 else 0
            w.set(x, y0 + 2 - sag - (z > z1 - 2), z, B.WOOD_SLAB, 1)
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


def mast(w, x, z, height):
    base = column_top(w, x, z) + 1
    for y in range(base, base + height):
        w.set(x, y, z, B.IRON_BARS)
        if y % 5 == 0:
            for a in (-1, 1):
                w.set(x + a, y, z, B.NETHER_FENCE)
                w.set(x, y, z + a, B.NETHER_FENCE)
    w.set(x, base + height, z, B.REDSTONE_LAMP)


def tank(w, cx, cz, r, height):
    base = min(column_top(w, cx + dx, cz + dz) for dx in (-r, r) for dz in (-r, r))
    for x in range(cx - r - 1, cx + r + 2):
        for z in range(cz - r - 1, cz + r + 2):
            if np.hypot(x - cx, z - cz) <= r:
                for y in range(base, base + height):
                    w.set(x, y, z, B.QUARTZ, 0 if (y - base) % 4 else 1)
                w.set(x, base + height, z, B.SLAB, 7)
                w.set(x, base + height + 1, z, B.SNOW_LAYER, 1)


def column_top(w, x, z):
    col = w.ids[x - w.x0, :, z - w.z0]
    solid = np.nonzero((col != 0) & (col != B.SNOW_LAYER))[0]
    return int(solid.max()) if len(solid) else 0


def cutting(w):
    """The cutting from the east hill to the plateau: a flight of stone-brick stairs cut down into the rock and
    built up where the hill falls away, open to the sky, walled either side."""
    c = P.CUTTING
    n = c["z1"] - c["z0"]
    feet = {z: int(round(c["feet0"] + (c["feet1"] - c["feet0"]) * (z - c["z0"]) / n)) for z in range(c["z0"], c["z1"] + 1)}
    for z in range(c["z0"], c["z1"] + 1):
        rises = z < c["z1"] and feet[z + 1] > feet[z]
        for x in range(c["x0"], c["x1"] + 1):
            for y in range(feet[z] - 6, feet[z] - 1):
                if w.id(x, y, z) in (B.AIR, B.SNOW_LAYER):
                    w.set(x, y, z, B.STONE)
            w.set(x, feet[z] - 1, z, *((B.STONEBRICK_STAIRS, 3) if rises else (B.STONEBRICK, 0)))
            for y in range(feet[z], w.ids.shape[1]):
                w.set(x, y, z, B.AIR)
        for x in (c["x0"] - 1, c["x1"] + 1):
            hi = max(feet[z] + 1, column_top(w, x, z))
            for y in range(feet[z] - 1, hi + 1):
                w.set(x, y, z, B.STONEBRICK, 0 if y % 4 else 2)
            w.set(x, hi + 1, z, B.NETHER_FENCE)


def survivors(w):
    """Spruces in the plateau's sheltered hollows and on the hill, crowns apart and snow on every crown, with
    the dead ones standing among them."""
    lib = trees.kinds(trees.library())
    kinds = lib["tiny-spruce"] + lib["tall-spruce"][:3]
    through = trees.PLANTS | {B.SNOW_LAYER}
    rng = np.random.default_rng(81)
    for cx, cz, reach, count in CLUMPS:
        planted = []
        for _ in range(60):
            if len(planted) >= count:
                break
            x = int(cx + rng.uniform(-reach, reach))
            z = int(cz + rng.uniform(-reach, reach))
            if not (land.Z0 + 4 <= z <= land.Z1 - 4 and land.X0 + 4 <= x <= land.X1 - 4):
                continue
            t = kinds[int(rng.integers(len(kinds)))]
            if any(np.hypot(x - px, z - pz) < (t.crown + pc) * 0.45 for px, pz, pc in planted):
                continue
            if trees.plant(w, x, z, t, int(rng.integers(4)), through=through):
                planted.append((x, z, t.crown))
        for _ in range(2):
            x, z = int(cx + rng.uniform(-reach, reach)), int(cz + rng.uniform(-reach, reach))
            trees.dead_tree(w, x, column_top(w, x, z), z, rng, int(rng.integers(5, 9)), log=B.LOG, kind=1)
        for x in range(cx - reach - 8, cx + reach + 9):
            for z in range(cz - reach - 8, cz + reach + 9):
                if not (land.X0 <= x <= land.X1 and land.Z0 <= z <= land.Z1):
                    continue
                y = column_top(w, x, z)
                if w.id(x, y, z) == B.LEAVES and w.id(x, y + 1, z) == B.AIR:
                    w.set(x, y + 1, z, B.SNOW_LAYER, 0)


def build(w):
    yard(w)
    cutting(w)
    dish(w)
    control_house(w)
    radome(w, -5, 87, 3)
    fallen_shed(w, 0, 66, 6, 71)
    stack(w, -9, 72, 9)
    stack(w, 10, 66, 12)
    mast(w, 22, 68, 22)
    mast(w, -40, 82, 16)
    tank(w, 34, 80, 3, 6)
    tank(w, 40, 73, 2, 5)
    survivors(w)
