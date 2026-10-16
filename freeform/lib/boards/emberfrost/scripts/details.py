"""What goes on last, and each for a reason: frost where the cold lane meets weather (spruce crowns, wall heads, the transition's grass), the
Ice Fall and the Magma Fall that close the gorge's two ends, leaf litter under the orchard's crowns, embers on the ash, and the lamps on
the roads. Nothing here is scattered over the whole board."""
import math

import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.built.props import lamp
from util import AIRY, claimed, claim_cells, ground_top

FROSTABLE = {B.LEAVES, B.LEAVES2, B.COBBLE_WALL, B.STONEBRICK, B.COBBLE, B.QUARTZ, B.SLAB, B.PLANKS, B.WOOD_SLAB, B.STONE, B.LOG, B.LOG2,
             B.GRASS, B.DIRT, B.GRAVEL, B.SPRUCE_FENCE, B.STAINED_CLAY, B.BRICK}


def frost(w, ice, rng, stats):
    """Snow laid thin on whatever stands in the cold: a layer on crowns and wall heads, thicker toward the glacier; on the transition's grass,
    a dusting that thins out to nothing where the orchard begins."""
    n = 0
    for i in range(w.sx):
        for k in range(w.sz):
            z = w.z0 + k
            if z >= -1:
                continue
            cold = ice[i, k]
            if cold < 0.1 or not P.LAND[i, k] or math.hypot(w.x0 + i - land.RIME[0], z - land.RIME[1]) < 10.6:
                continue
            y = ground_top(w, w.x0 + i, z)
            blk = int(w.ids[i, y, k])
            if blk not in FROSTABLE or w.ids[i, y + 1, k] != B.AIR:
                continue
            if blk in (B.LEAVES, B.LEAVES2):
                p = 0.55 + 0.4 * cold
            elif blk in (B.GRASS, B.DIRT, B.GRAVEL):
                p = max(0.0, (cold - 0.1) * 1.5)
            else:
                p = 0.35 + 0.4 * cold
            if rng.random() < p:
                w.ids[i, y + 1, k], w.dat[i, y + 1, k] = B.SNOW_LAYER, int(rng.integers(0, 2)) if blk in (B.GRASS, B.DIRT) else 0
                n += 1
    stats["snow layers"] = n


def falls(w, rng, stats):
    """Two cascades on the gorge's walls: frozen water at the west end, cooled lava at the east, each a stripe down the north wall from
    the rim to the bank, its face broken by noise so it hangs in folds."""
    for x0, x1, kinds in ((-59, -53, [((B.ICE, 0), 3), ((B.PACKED_ICE, 0), 5), ((B.SNOW, 0), 1)]),
                          (53, 59, [((B.STAINED_CLAY, 1), 3), ((B.GLOWSTONE, 0), 1), ((B.STAINED_CLAY, 12), 2), ((B.HARDENED_CLAY, 0), 2)])):
        total = sum(s for _, s in kinds)
        for x in range(x0, x1 + 1):
            fold = math.sin(x * 0.9) * 1.5
            for z in range(-16, -3):
                if not P.LAND[x - P.X_MIN, z - P.Z_MIN]:
                    continue
                g = P.g(x, z)
                if g < 50 or g > 70:
                    continue
                depth = 2 + int(abs(fold + rng.uniform(-0.8, 0.8)))
                for d in range(depth):
                    r = rng.random() * total
                    acc = 0
                    for blk, s in kinds:
                        acc += s
                        if r <= acc:
                            break
                    w.set(x, g - d, z, *blk)
                if x0 < 0 and rng.random() < 0.35 and w.id(x, g - 2, z) == B.AIR:
                    w.set(x, g - 1, z, B.ICE)
    stats["falls"] = 2


def litter(w, placed, rng, stats):
    """Leaf litter under the orchard: orange, yellow and brown carpet on the ground round a crown's trunk."""
    n = 0
    for x, z, c in placed:
        if c < 2.0 or z >= -17 or c > 7.5:
            continue
        for dx in range(-5, 6):
            for dz in range(-5, 6):
                d = math.hypot(dx, dz)
                if d < 1.4 or d > 5.0 or rng.random() > 0.6 or claimed(x + dx, z + dz):
                    continue
                gx, gz = x + dx, z + dz
                y = ground_top(w, gx, gz)
                if w.id(gx, y, gz) in (B.GRASS, B.DIRT) and w.id(gx, y + 1, gz) == B.AIR:
                    w.set(gx, y + 1, gz, B.CARPET, int(rng.choice([1, 4, 12], p=[0.45, 0.35, 0.2])))
                    n += 1
    stats["litter"] = n


def embers(w, fire, deg, rng, stats):
    """A few fires on the ash, each on netherrack, none within six blocks of wood, a road or a building."""
    placed = []
    cells = np.argwhere((fire > 0.7) & (deg < 25) & P.LAND & (P.Z < -20))
    rng.shuffle(cells)
    for i, k in cells[:900]:
        x, z = int(P.X[i, k]), int(P.Z[i, k])
        if claimed(x, z) or math.hypot(x - land.FORGE[0], z - land.FORGE[1]) < 26 or any((x - a) ** 2 + (z - b) ** 2 < 100 for a, b in placed):
            continue
        y = int(P.H[i, k])
        if w.id(x, y, z) != B.NETHERRACK or w.id(x, y + 1, z) != B.AIR:
            continue
        near = False
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                for dy in range(0, 4):
                    if w.id(x + dx, y + dy, z + dz) in (B.LEAVES, B.LEAVES2, B.PLANKS, B.LOG, B.LOG2):
                        near = True
        if near:
            continue
        w.set(x, y + 1, z, B.FIRE)
        placed.append((x, z))
        if len(placed) >= 26:
            break
    stats["embers"] = len(placed)


def lamps_on_roads(w, stats):
    n = 0
    for pts, light, post in (([(-23, -71), (-29, -62)], (B.SEA_LANTERN, 0), (B.SPRUCE_FENCE, 0)), ([(-35, -34), (-37, -29), (-40, -22)], (B.SEA_LANTERN, 0), (B.SPRUCE_FENCE, 0)),
                             ([(24, -60), (18, -61)], (B.GLOWSTONE, 0), (B.NETHER_FENCE, 0)), ([(41, -30), (41, -20)], (B.GLOWSTONE, 0), (B.NETHER_FENCE, 0)),
                             ([(16, -45), (28, -40), (38, -37)], (B.GLOWSTONE, 0), (B.NETHER_FENCE, 0))):
        for j, (x, z) in enumerate(pts):
            sx = x + (3 if j % 2 else -3)
            y = P.g(sx, z)
            if abs(y - P.g(x, z)) <= 2 and w.id(sx, y + 1, z) in AIRY:
                lamp(w, sx, y, z, height=3, post=post, light=light, cap=(B.WOOD_SLAB, 5) if post[0] == B.SPRUCE_FENCE else (B.SLAB, 6))
                claim_cells([(sx, z)], 1)
                n += 1
    stats["lamps"] = n
