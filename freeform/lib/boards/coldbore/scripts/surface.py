"""What stands on red's snowfield: the forecourt paved in front of the gate, the roads from it to the fissure and
the flanks, the boulders that give the approaches cover, the old road bridge broken off over the fissure, the
power line's pylons coming down from the station, lamps on the forecourt, the vent hatch's frame, and the bore's
wrecked derrick on its stump in the middle.
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
BOULDERS = [(-9, 25, (4, 3, 3), 20), (13, 21, (3, 3, 4), -15), (-31, 19, (5, 3, 4), 40), (31, 28, (4, 4, 3), 10),
            (-56, 41, (5, 4, 4), -30), (59, 46, (4, 3, 5), 25), (-23, 43, (3, 3, 3), 5), (25, 47, (3, 2, 4), -40)]
PYLONS = [(46, 70, False), (44, 42, False), (40, 20, True)]       # x, z, toppled


def at(top, x, z):
    return int(top[x - land.X0, z - land.Z0])


def column_top(w, x, z):
    col = w.ids[x - w.x0, :, z - w.z0]
    solid = np.nonzero((col != 0) & (col != B.SNOW_LAYER))[0]
    return int(solid.max()) if len(solid) else 0


def cell3(x, z, blocks, size=1):
    h = ((x // size) * 2654435761 ^ (z // size) * 40503) & 0xFFFF
    return blocks[h % len(blocks)]


def forecourt(w):
    f = land.FORECOURT
    for x in range(f["x0"], f["x1"] + 1):
        for z in range(f["z0"], f["z1"] + 1):
            if P.FACADE["x0"] <= x <= P.FACADE["x1"] and z >= P.FACADE["z0"]:
                continue
            if w.id(x, land.GROUND, z) == B.AIR:
                continue
            blk = cell3(x, z, [(B.STONEBRICK, 0), (B.STONE, 6), (B.STONE, 5), (B.STONE, 0)], 3)
            if -7 <= x <= 6 and 39 <= z <= 43:                     # hazard bands before the gate
                blk = [(B.STAINED_CLAY, 4), (B.STAINED_CLAY, 15)][((x + z) // 2) % 2]
            w.set(x, land.GROUND, z, *blk)
            w.set(x, land.GROUND + 1, z, B.AIR)
    for x in (f["x0"], f["x1"]):                                   # blast walls on the forecourt's front corners
        for z in range(f["z0"], f["z0"] + 5):
            for y in (land.GROUND + 1, land.GROUND + 2):
                w.set(x, y, z, B.STONEBRICK if y == land.GROUND + 1 else B.COBBLE_WALL)
    for x in (f["x0"] + 2, f["x1"] - 2):                           # lamps, one of them dark
        for y in range(land.GROUND + 1, land.GROUND + 5):
            w.set(x, y, f["z0"] + 8, B.NETHER_FENCE)
        w.set(x, land.GROUND + 5, f["z0"] + 8, B.GLOWSTONE if x > 0 else B.COAL_BLOCK)


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


def boulders(w, top):
    rng = np.random.default_rng(31)

    def paint(u, ly, lz, size):
        r = rng.random()
        if ly > size[1] / 2 - 1.0 and r < 0.6:
            return (B.SNOW, 0)
        return (B.STONE, 5) if r < 0.35 else (B.COBBLE, 0) if r < 0.5 else (B.STONE, 0)
    for x, z, size, yaw in BOULDERS:
        placed_box(w, x, z, size, top, yaw=yaw, tilt=8, sink=0.35, paint=paint)


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


def pylon(w, x, z, base, height=15, toppled=False):
    """A lattice pylon of iron bars and nether fence; toppled, it lies along the snow toward the fissure."""
    for t in range(height):
        half = max(0, 2 - t // 6)
        for dx in (-half, half):
            for dz in (-half, half):
                if toppled:
                    w.set(x + dx, base + 1 + (dz > 0), z - t, B.NETHER_FENCE)
                else:
                    w.set(x + dx, base + 1 + t, z + dz, B.NETHER_FENCE)
        if t % 4 == 3:
            for a in range(-half, half + 1):
                if toppled:
                    w.set(x + a, base + 1, z - t, B.IRON_BARS)
                else:
                    w.set(x + a, base + 1 + t, z - half, B.IRON_BARS)
                    w.set(x + a, base + 1 + t, z + half, B.IRON_BARS)
    if not toppled:
        for a in range(-4, 5):
            w.set(x + a, base + height, z, B.NETHER_FENCE)


def pylons(w):
    for x, z, toppled in PYLONS:
        pylon(w, x, z, column_top(w, x, z), toppled=toppled)


def vent_hatch(w):
    lad = P.LADDER
    for x in range(lad["x"] - 1, lad["x"] + 3):
        for z in range(lad["z0"] - 1, lad["z1"] + 2):
            inside = lad["x"] <= x <= lad["x"] + 1 and lad["z0"] <= z <= lad["z1"]
            if not inside:
                w.set(x, land.GROUND, z, B.STAINED_CLAY, 4 if (x + z) % 2 else 15)
                if z == lad["z1"] + 1 or x == lad["x"] + 2:
                    w.set(x, land.GROUND + 1, z, B.IRON_BARS)


def derrick(w):
    """The bore's derrick, wrecked on its stump in the lava: a lattice leaning off the pillar's top."""
    y0 = land.PILLAR + 1
    for t in range(16):
        lean = t // 3
        for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            w.set(-1 + dx + lean, y0 + t, -1 + dz, B.NETHER_FENCE)
        if t % 4 == 2:
            for a in (-1, 0, 1):
                w.set(-1 + a + lean, y0 + t, -2, B.IRON_BARS)
                w.set(-1 + a + lean, y0 + t, 0, B.IRON_BARS)
    for x in range(-3, 3):
        for z in range(-3, 3):
            if np.hypot(x + 0.5, z + 0.5) < 3.2:
                w.set(x, land.PILLAR, z, B.OBSIDIAN if (x + z) % 3 else B.COAL_BLOCK)


LAVAFALLS = [-48, -9, 37]                                    # columns x where a lavafall runs down red's wall


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
    forecourt(w)
    roads(w, top)
    boulders(w, top)
    bridge_stub(w, top)
    vent_hatch(w)
    derrick(w)
    pylons(w)
