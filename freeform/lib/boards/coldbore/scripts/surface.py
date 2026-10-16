"""What stands on red's snowfield: the courts paved in front of the gate and the generator house, the roads from
them to the fissure and the flanks, the boulders that give the approaches cover, the old road bridge broken off
over the fissure, signal towers on the hill and one blown over on the snow, lamps on the courts, the lavafalls down red's wall
of the fissure, and the bore's wrecked derrick on its stump in the middle.
"""
import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.geom import noise
from pgmvox.geom.noise import spline
from pgmvox.geom.shapes import polyline
from pgmvox.scenery.forms import placed_box

ROAD = [(B.GRAVEL, 0), (B.STONE, 5), (B.COBBLE, 0)]           # a third each: hard ground's path
BOULDERS = [(-9, 25, (4, 3, 3), 20), (16, 16, (3, 3, 4), -15), (-31, 19, (5, 3, 4), 40), (31, 28, (4, 4, 3), 10),
            (-67, 40, (5, 4, 4), -30), (59, 46, (4, 3, 5), 25), (-18, 40, (3, 3, 3), 5), (14, 45, (3, 2, 4), -40),
            (-12, 32, (4, 3, 4), 60)]
TOWERS = [(58, 70, False), (56, 40, False), (46, 36, True)]       # x, z, blown over


def at(top, x, z):
    return int(top[x - land.X0, z - land.Z0])


def column_top(w, x, z):
    col = w.ids[x - w.x0, :, z - w.z0]
    solid = np.nonzero((col != 0) & (col != B.SNOW_LAYER))[0]
    return int(solid.max()) if len(solid) else 0


def cell3(x, z, blocks, size=1):
    h = ((x // size) * 2654435761 ^ (z // size) * 40503) & 0xFFFF
    return blocks[h % len(blocks)]


def courts(w):
    """Both courts paved in cells of three, hazard bands across the gate's mouth and the garage's, lamps on posts
    at the courts' outer corners, one of them dark."""
    for f, door in ((P.GATE_COURT, P.GATE), (P.ANNEX_YARD, P.GARAGE)):
        for x in range(f["x0"], f["x1"] + 1):
            for z in range(f["z0"], f["z1"] + 1):
                if w.id(x, land.GROUND, z) == B.AIR or w.id(x, land.GROUND + 1, z) not in (B.AIR, B.SNOW_LAYER):
                    continue
                blk = cell3(x, z, [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)], 3)
                if door["x0"] - 1 <= x <= door["x1"] + 1 and door["z"] - 4 <= z <= door["z"] - 2:
                    blk = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)][((x + z) // 2) % 2]
                w.set(x, land.GROUND, z, *blk)
                w.set(x, land.GROUND + 1, z, B.AIR)
        for x in (f["x0"] + 2, f["x1"] - 2):
            for y in range(land.GROUND + 1, land.GROUND + 5):
                w.set(x, y, f["z0"] + 1, B.NETHER_FENCE)
            w.set(x, land.GROUND + 5, f["z0"] + 1, B.GLOWSTONE if x > f["x0"] + 2 else B.COAL_BLOCK)


def roads(w, top):
    """Each road splined, wandering a little, three blocks wide and laid flush in the snow at the ground's height
    smoothed along it, so it never steps more than a block."""
    X, Z = land.grid()
    for k, pts in enumerate(P.ROADS):
        line = spline(pts, 2.0)
        n = len(line)
        wob = 1.2 * noise.fbm((n,), 12, 2, seed=60 + k)
        bent = []
        for j, (x, z) in enumerate(line):
            if 0 < j < n - 1:
                dx, dz = line[j + 1][0] - line[j - 1][0], line[j + 1][1] - line[j - 1][1]
                L = max(np.hypot(dx, dz), 1e-6)
                ease = min(j, n - 1 - j) / 6
                bent.append((x - dz / L * wob[j] * min(1, ease), z + dx / L * wob[j] * min(1, ease)))
            else:
                bent.append((x, z))
        d, al = polyline(X, Z, bent)[:2]
        band = d < 1.6
        for i, kk in np.argwhere(band):
            x, z = int(X[i, kk]), int(Z[i, kk])
            if land.across(np.array([float(x)]), np.array([float(z)]))[0] < land.RIM_HALF + 0.5:
                continue
            h = int(top[i, kk])
            if h <= land.LAVA + 4:
                continue
            w.set(x, h, z, *cell3(x, z, ROAD))
            if w.id(x, h + 1, z) == B.SNOW_LAYER:
                w.set(x, h + 1, z, B.AIR)


def bedded(rng):
    """A boulder's paint: the cliff's own beds across it, at an offset of their own, with snow lying on its top."""
    import ground
    bounds, beds = ground.strata()
    offset = rng.uniform(20, 80)

    def paint(u, ly, lz, size):
        if ly > size[1] / 2 - 1.0 and rng.random() < 0.6:
            return (B.SNOW, 0)
        b = beds[np.searchsorted(bounds, ly + offset)]
        return int(b[0]), int(b[1])
    return paint


def boulders(w, top):
    rng = np.random.default_rng(31)
    for x, z, size, yaw in BOULDERS:
        placed_box(w, x, z, size, top, yaw=yaw, tilt=8, sink=0.35, paint=bedded(rng))


def seat(w, x, z, half, reach=6):
    """The flattest place within `reach` of (x, z) for a footprint `half` out from its centre: (x, z, base), base the
    footprint's highest ground, so whatever stands there stands on it or on footings down to it."""
    best = None
    for dx in range(-reach, reach + 1):
        for dz in range(-reach, reach + 1):
            tops = [column_top(w, x + dx + a, z + dz + b) for a in (-half, 0, half) for b in (-half, 0, half)]
            score = (max(tops) - min(tops), abs(dx) + abs(dz))
            if best is None or score < best[0]:
                best = (score, x + dx, z + dz, max(tops))
    return best[1], best[2], best[3]


def face_line(a, b):
    """The cells from a to b, each one sharing a face with the last, so a strut drawn through them holds together."""
    a, b = np.array(a, float), np.array(b, float)
    n = int(np.abs(b - a).max() * 2) + 1
    out = [tuple(int(round(c)) for c in a)]
    for t in np.linspace(0, 1, n + 1)[1:]:
        cell = [int(round(c)) for c in a + (b - a) * t]
        last = list(out[-1])
        for axis in range(3):
            if cell[axis] != last[axis]:
                last[axis] = cell[axis]
                out.append(tuple(last))
    return out


def footings(w, cells, base):
    """Stone brick under each cell from its ground up to `base`, so nothing built on `base` hangs over a hollow."""
    for x, z in cells:
        for y in range(column_top(w, x, z) + 1, base + 1):
            w.set(x, y, z, B.STONEBRICK)


def bridge_stub(w, top):
    """The road bridge broken off over the fissure: a slab deck on stone-brick beams with iron rails, its end
    ragged, a girder hanging from it."""
    c, half = land.fissure_line()
    b = P.BRIDGE_STUB
    for x in range(b["x0"], b["x1"] + 1):
        rim = int(np.ceil(c[x - land.X0] + half[x - land.X0]))
        length = b["length"] - (1 if x in (b["x0"], b["x1"]) else 0) - (x % 2)
        for z in range(rim - length, rim + 1):
            w.set(x, land.GROUND, z, B.DSLAB)
            w.set(x, land.GROUND - 1, z, B.STONEBRICK)
            if x in (b["x0"], b["x1"]):
                w.set(x, land.GROUND + 1, z, B.IRON_BARS)
        if x == b["x0"] + 1:
            for y in range(land.GROUND - 9, land.GROUND - 1):
                w.set(x, y, rim - length, B.IRON_BARS)


TEAM = (B.STAINED_CLAY, 14)                                     # red; blue's image recolours it
MODULE = ["clay", "clay", "clay", "collar", "quartz", "quartz"]   # a signal tower's six-block repeat, from its foot


def signal_tower(w, x, z, modules=4):
    """A signal tower, one block thick: banded in the team's clay and chiseled quartz, a collar of slabs round an
    iron hub every six blocks, buttons, a trapdoor and stub antennas of bars on its faces, and a crown of cobble
    walls carrying two redstone torches under a whip of bars and fence. It stands on the flattest ground near
    (x, z), on a plinth of polished andesite under a ring of slabs."""
    x, z, base = seat(w, x, z, 1)
    footings(w, [(x + a, z + b) for a in (-1, 0, 1) for b in (-1, 0, 1)], base)
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            w.set(x + a, base + 1, z + b, *((B.STONE, 6) if a == b == 0 else (B.SLAB, 5)))
    y = base + 2
    for m in range(modules):
        for row, part in enumerate(MODULE):
            if part == "clay":
                w.set(x, y, z, *TEAM)
                if row == 0:
                    w.set(x - 1, y, z, B.BUTTON_STONE, 2)
                    w.set(x + 1, y, z, B.BUTTON_STONE, 1)
                    if m % 2:
                        for t in (1, 2):
                            w.set(x, y, z + t, B.IRON_BARS)
            elif part == "collar":
                w.set(x, y, z, *((B.DISPENSER, 1) if m == modules - 1 else (B.IRON_BLOCK, 0)))
                for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    w.set(x + a, y, z + b, B.SLAB, 5 if m % 2 else 0)
            else:
                w.set(x, y, z, B.QUARTZ, 1)
                if row == 4:
                    w.set(x, y, z + 1, B.IRON_TRAPDOOR, 5)
            y += 1
    for t in range(3):
        w.set(x, y + t, z, B.COBBLE_WALL)
    w.set(x, y + 2, z + 1, B.COBBLE_WALL)
    w.set(x, y + 3, z + 1, B.REDSTONE_TORCH, 5)
    w.set(x, y + 3, z, B.QUARTZ, 1)
    for t in (4, 5):
        w.set(x, y + t, z, B.COBBLE_WALL)
    w.set(x, y + 5, z - 1, B.COBBLE_WALL)
    w.set(x, y + 6, z - 1, B.REDSTONE_TORCH, 5)
    w.set(x, y + 6, z, B.IRON_BARS)
    w.set(x, y + 7, z, B.NETHER_FENCE)


def fallen_tower(w, x, z, length=18):
    """A signal tower blown over, lying along the snow toward the fissure, each block of it on the ground under
    it, its end broken off where the ground falls away."""
    start = column_top(w, x, z)
    parts = (MODULE * 4)[:length]
    for t, part in enumerate(parts):
        zz = z - t
        g = column_top(w, x, zz)
        if g < start - 3:
            break
        if part == "clay":
            w.set(x, g + 1, zz, *TEAM)
        elif part == "collar":
            w.set(x, g + 1, zz, B.IRON_BLOCK)
            for a in (-1, 1):
                w.set(x + a, column_top(w, x + a, zz) + 1, zz, B.SLAB, 5)
        else:
            w.set(x, g + 1, zz, B.QUARTZ, 1)


def towers(w):
    for x, z, fallen in TOWERS:
        if fallen:
            fallen_tower(w, x, z)
        else:
            signal_tower(w, x, z)


def derrick(w):
    """The bore's derrick, wrecked on its stump in the lava: a lattice leaning off the pillar's top."""
    y0 = land.PILLAR + 1
    for t in range(16):
        lean = t // 3
        for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            w.set(-1 + dx + lean, y0 + t, -1 + dz, B.NETHER_FENCE)
            if t and lean > (t - 1) // 3:                       # each lean joined to the leg under it
                w.set(-1 + dx + lean, y0 + t - 1, -1 + dz, B.NETHER_FENCE)
        if t % 4 == 2:
            for a in (-1, 0, 1):
                w.set(-1 + a + lean, y0 + t, -2, B.IRON_BARS)
                w.set(-1 + a + lean, y0 + t, 0, B.IRON_BARS)
    for x in range(-3, 3):
        for z in range(-3, 3):
            if np.hypot(x + 0.5, z + 0.5) < 3.2:
                w.set(x, land.PILLAR, z, B.OBSIDIAN if (x + z) % 3 else B.COAL_BLOCK)


LAVAFALLS = [-68, -54, -42, -31, -22, 22, 30, 41, 52, 64]      # columns x where a lavafall runs down red's wall


def lavafalls(w, top):
    """Lava breaking from a notch high in red's wall of the fissure and falling into the lake: a source in the
    notch, a falling column in front of the wall, far from either core."""
    c, half = land.fissure_line()
    for x in LAVAFALLS:
        i = x - land.X0
        zs = range(int(c[i]), int(c[i] + half[i]) + 1)
        wall = [z for z in zs if top[i, z - land.Z0] > 48]
        if not wall:
            continue
        zw = wall[0]
        zf = zw - 1                                              # the air in front of the wall
        src = int(top[i, zw - land.Z0]) - 3
        w.set(x, src, zw, B.LAVA)
        w.set(x, src + 1, zw, B.STONE)
        for y in range(land.LAVA + 1, src + 1):
            if w.id(x, y, zf) == B.AIR:
                w.set(x, y, zf, B.LAVA_FLOW, 8)


def build(w, top):
    courts(w)
    roads(w, top)
    boulders(w, top)
    bridge_stub(w, top)
    derrick(w)
    lavafalls(w, top)
