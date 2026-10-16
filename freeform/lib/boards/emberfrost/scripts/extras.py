"""The last places and the signs that find them: the gorge's hanging ice and glowing seams, the Aerie on the glacier's plateau above the Rime
Core, the Organ (a field of basalt columns by the Brimstone Way) and a burnt cottage beside it, and the signposts in the Hearth yard."""
import math

import numpy as np

import land
import plan as P
from pgmvox import B
from util import claim_cells, claim_disc, disc, pick, stairs


def wall_pendants(w, rng, stats):
    """Along the gorge's north rim, ice hangs on the west half and glowstone-tipped chains of orange clay on the east, each from a rim column
    whose neighbour toward the gorge falls away by three or more."""
    n = 0
    for x in range(-52, 52):
        if abs(x) < 6:
            continue
        for z in range(-15, -7):
            g, gz = P.g(x, z), P.g(x, z + 1)
            if g - gz < 3 or P.g(x, z + 1) == 0 or rng.random() > 0.3:
                continue
            length = min(int(rng.integers(2, 6)), g - gz - 1)
            for j in range(length):
                if w.id(x, g - 1 - j, z + 1) != B.AIR:
                    break
                if x < 0:
                    w.set(x, g - 1 - j, z + 1, *((B.ICE, 0) if j % 2 == 0 else (B.PACKED_ICE, 0)))
                else:
                    w.set(x, g - 1 - j, z + 1, *((B.STAINED_CLAY, 1) if j < length - 1 else (B.GLOWSTONE, 0)))
            n += 1
    stats["pendants"] = n


def aerie(w, rng):
    """An open pavilion on the plateau at 85, northwest of the keep and above it: eight quartz columns and a low wall, so a team that
    climbs to it sees the whole terrace below and has a way to bridge down."""
    cx, cz, y = -46, -66, 85
    claim_disc(cx, cz, 8)
    for x, z, d in disc(cx, cz, 5.4):
        for yy in range(min(P.g(x, z), y) - 2, y):
            w.set(x, yy, z, B.STONE, 6)
        w.set(x, y, z, *pick(rng, [((B.STONEBRICK, 0), 4), ((B.STONE, 6), 3), ((B.QUARTZ, 0), 2)]))
        for yy in range(y + 1, y + 9):
            w.set(x, yy, z, B.AIR)
        if 4.4 < d <= 5.4:
            w.set(x, y + 1, z, B.COBBLE_WALL)
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        px, pz = cx + round(4.4 * math.cos(a)), cz + round(4.4 * math.sin(a))
        for yy in range(y + 1, y + 6):
            w.set(px, yy, pz, B.QUARTZ, 2)
        w.set(px, y + 6, pz, B.QUARTZ, 1)
    w.set(cx, y, cz, B.PRISMARINE, 1)
    for yy in range(y + 1, y + 3):
        w.set(cx, yy, cz, B.COBBLE_WALL)
    w.set(cx, y + 3, cz, B.SEA_LANTERN)


def organ(w, rng):
    """Basalt columns on the ash by the Brimstone Way: polished andesite and black clay, heights stepping toward the middle of the stand."""
    cx, cz = 58, -30
    cols = 0
    for x, z, d in disc(cx, cz, 8):
        if (x + 2 * z) % 3 or d < 0.5 and False:
            continue
        g = P.g(x, z)
        if not P.LAND[x - P.X_MIN, z - P.Z_MIN] or g < 60 or g > 70 or rng.random() < 0.3:
            continue
        h = max(1, int(round(8 - d + rng.uniform(-1.5, 1.5))))
        for yy in range(g + 1, g + 1 + h):
            w.set(x, yy, z, *((B.STONE, 6) if yy % 3 else (B.STAINED_CLAY, 15)))
        cols += 1
    claim_disc(cx, cz, 9)
    return cols


def burnt_cottage(w, rng):
    """A cottage that burnt: the ground-storey walls in nether brick and charred planks, gaps where the doors and windows were, no roof."""
    x0, z0, x1, z1 = 51, -26, 58, -21
    hs = [P.g(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
    y = max(hs)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for yy in range(P.g(x, z), y):
                w.set(x, yy, z, B.NETHER_BRICK)
            edge = x in (x0, x1) or z in (z0, z1)
            w.set(x, y, z, *((B.STAINED_CLAY, 15) if (x + z) % 2 else (B.NETHER_BRICK, 0)))
            for yy in range(y + 1, y + 5):
                w.set(x, yy, z, B.AIR)
            if edge and rng.random() < 0.8:
                for yy in range(y + 1, y + 1 + int(rng.integers(1, 4))):
                    w.set(x, yy, z, *pick(rng, [((B.NETHER_BRICK, 0), 3), ((B.STAINED_CLAY, 15), 2), ((B.PLANKS, 5), 2), ((B.COBBLE, 0), 1)]))
        # gap for the door
    for yy in range(y + 1, y + 4):
        w.set((x0 + x1) // 2, yy, z1, B.AIR)
    w.set(x0 + 1, y + 1, z0 + 1, B.NETHERRACK)
    w.set(x0 + 1, y + 2, z0 + 1, B.FIRE)
    claim_cells([(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)], 2)


def signs(w):
    """Signposts where the yard's roads begin: each names the road, where it goes and how far the first place is."""
    spots = [((-14, -75), 12, ["FROST ROAD", "Pinewatch", "Rime Keep", "the Mirror"]),
             ((4, -72), 8, ["DROVE ROAD", "Amberford", "Beacon Hill", "the Cinder Span"]),
             ((14, -75), 4, ["EMBER ROAD", "the Armoury", "the Forge", "Foundry"])]
    for (x, z), rot, lines in spots:
        y = P.g(x, z)
        w.set(x, y + 1, z, B.FENCE)
        w.sign(x, y + 2, z, lines, rot=rot)
    for (x, z), rot, lines in (((-38, -17), 8, ["FROSTSPAN", "to the south bank", "water below", ""]), ((3, -16), 8, ["CINDER SPAN", "the bar runs under", "the pier", ""]),
                              ((43, -17), 8, ["BRIMSTONE BRIDGE", "lava below", "mind the edge", ""])):
        y = P.g(x, z)
        w.set(x, y + 1, z, B.FENCE)
        w.sign(x, y + 2, z, lines, rot=rot)


def floes(w, rng, stats):
    """Pressure ridges on the Mirror: heaps of packed ice and snow where the ice has buckled, each on the lake's own ice and clear of the shore."""
    from pgmvox.geom.shapes import distance_in
    lake = land.lake_distance(P.X, P.Z) < 0.7
    n = 0
    cells = np.argwhere(lake & (P.Z < -17))
    rng.shuffle(cells)
    taken = []
    for i, k in cells[:400]:
        x, z = int(P.X[i, k]), int(P.Z[i, k])
        if any((x - a) ** 2 + (z - b) ** 2 < 30 for a, b in taken) or w.id(x, land.LAKE_ICE, z) != B.ICE:
            continue
        taken.append((x, z))
        r = int(rng.integers(1, 3))
        for dx in range(-r - 1, r + 2):
            for dz in range(-r - 1, r + 2):
                d = math.hypot(dx, dz)
                if d <= r + 0.5 and w.id(x + dx, land.LAKE_ICE, z + dz) == B.ICE:
                    for yy in range(1, max(1, int(round(2.2 - d))) + 1):
                        w.set(x + dx, land.LAKE_ICE + yy, z + dz, *((B.PACKED_ICE, 0) if yy == 1 else (B.SNOW, 0)))
        n += 1
        if n >= 7:
            break
    stats["ice heaps"] = n


def build(w, rng, stats):
    floes(w, rng, stats)
    wall_pendants(w, rng, stats)
    aerie(w, rng)
    stats["organ"] = organ(w, rng)
    burnt_cottage(w, rng)
    signs(w)
