"""What is grown or weathered rather than built, on red's half of Hollowcrown.

- Oaks in the vale and in the town's gardens; spruce on the mountain, tiny spruce on its steep ledges; none on
  a road, a field, a claim, in water, or with a crown within five blocks of a monument.
- Where water meets land: reeds on the shallow, sandy edges (the inside of a bend, the tarn's beach), lily
  pads on still water near the low shore, tall grass and ferns on the banks, mossy boulders half in the water
  on the outside of bends and in the pools under the falls.
- Vines down the retaining walls and the cliffs, flowers on the gentle grass.
- Underground: mushrooms by Deepmere, moss on the cavern's wet walls.
- Clouds of glass high over everything: white stained glass, light grey on their undersides, plain glass at
  their ragged edges.
"""
import json
import math
import os

import numpy as np

import plan as P
from mc import B
from noise import fbm

HERE = os.path.dirname(os.path.abspath(__file__))
TREES = json.load(open(os.path.join(HERE, "trees.json")))
SOFT = (B.AIR, B.TALLGRASS, B.FLOWER, B.DANDELION, B.DOUBLE_PLANT, B.VINE)
RNG = np.random.default_rng(77)


def H(F, x, z):
    return int(F.H[x - F.x0, z - F.z0])


def plant(w, F, x, z, tree, turn):
    g = H(F, x, z)
    if w.id(x, g, z) not in (B.GRASS, B.DIRT) or w.id(x, g + 1, z) not in SOFT:
        return False
    cells = []
    for dx, dy, dz, i, d in tree["blocks"]:
        for _ in range(turn):
            dx, dz = -dz, dx
        X, Y, Z = x + dx, g + 1 + dy, z + dz
        if X >= 0 or not w.inside(X, Y, Z):
            return False
        cur = w.id(X, Y, Z)
        if cur in (B.GRASS, B.DIRT, B.STONE):
            continue
        if cur not in SOFT and cur not in (B.LEAVES, B.LEAVES2):
            return False
        cells.append((X, Y, Z, i, d))
    for X, Y, Z, i, d in cells:
        if i in (17, 162) and turn % 2 == 1 and (d & 12) in (4, 8):
            d = (d & 3) | (12 - (d & 12))
        if w.id(X, Y, Z) in (B.LEAVES, B.LEAVES2) and i in (18, 161):
            continue
        w.set(X, Y, Z, i, d)
    return True


def blocked(F):
    """Where no tree may stand: water and three blocks of open shore round it, the roads and five blocks
    either side (so no crown roofs a road), the bridge and its approaches, every claim and two round it."""
    from scipy.ndimage import binary_dilation
    shore = binary_dilation(F.water_any, iterations=3)
    m = ~F.red | shore | F.market | (F.wend < 5.5) | (F.corr < 4.0)
    for (x, z) in F.bridge:
        ix, iz = x - F.x0, z - F.z0
        m[max(0, ix - 6):ix + 7, max(0, iz - 6):iz + 7] = True
    for layer in ("surface",):
        for (x, z) in F.occ[layer]:
            ix, iz = x - F.x0, z - F.z0
            m[max(0, ix - 2):ix + 3, max(0, iz - 2):iz + 3] = True
    return m


def trees(w, F):
    F.trees = []
    bl = blocked(F)
    rng = np.random.default_rng(5)
    wood = fbm(F.shape, 12, 2, seed=60)
    pts = np.argwhere(~bl & (F.angle < 48))
    rng.shuffle(pts)
    n = 0
    for ix, iz in pts:
        x, z = F.x0 + ix, F.z0 + iz
        g = H(F, x, z)
        mount = F.mount[ix, iz] and g > 50
        dense = wood[ix, iz] > (0.15 if mount else 0.25)
        if not dense and rng.random() > 0.06:
            continue
        if F.town[ix, iz] and rng.random() > 0.35:
            continue
        if mount:
            kind = "tiny-spruce" if (F.angle[ix, iz] > 30 or g > 84 or rng.random() < 0.3) else "spruce"
        else:
            kind = "tiny-oak" if (F.town[ix, iz] or rng.random() < 0.35) else "oak"
        t = TREES[kind][rng.integers(len(TREES[kind]))]
        c = t["crown"] * 0.5
        if any(math.hypot(x - mx, z - mz) < t["crown"] + 5 for (mx, my, mz) in (F.mon_a,)):
            continue
        if any(math.hypot(x - a, z - b) < (c + pc) for a, b, pc in F.trees):
            continue
        if plant(w, F, x, z, t, int(rng.integers(4))):
            F.trees.append((x, z, c))
            n += 1
    return n


def water_edges(w, F):
    """Reeds, lilies, grasses and boulders where the water meets the land."""
    water = F.water_any
    near = np.zeros(F.shape, bool)
    for ax in (0, 1):
        for s in (1, -1):
            near |= np.roll(water, s, ax)
    shore = near & ~water & F.red
    r = RNG.random(F.shape)
    n_reed = n_lily = 0
    for ix, iz in zip(*np.nonzero(shore)):
        x, z = F.x0 + ix, F.z0 + iz
        g = H(F, x, z)
        if (x, z) in F.occ["surface"] or F.wend[ix, iz] < 3 or F.corr[ix, iz] < 1:
            continue
        top = w.id(x, g, z)
        if w.id(x, g + 1, z) != B.AIR:
            continue
        lvl = P.WATER_Y if F.river[min(ix + 1, F.nx - 1), iz] or F.river[max(ix - 1, 0), iz] or F.river[ix, min(iz + 1, F.nz - 1)] or F.river[ix, max(iz - 1, 0)] else None
        low = lvl is None or g <= lvl + 1
        inner = not F.outer[ix, iz]
        if top in (B.SAND, B.GRASS, B.DIRT) and low and (inner or not F.river[ix, iz]) and r[ix, iz] < 0.38:
            for k in range(1, 2 + int(r[ix, iz] * 6) % 3):
                w.set(x, g + k, z, B.REEDS)
            n_reed += 1
        elif top == B.GRASS and r[ix, iz] < 0.6:
            w.set(x, g + 1, z, *((B.TALLGRASS, 1) if r[ix, iz] < 0.5 else (B.TALLGRASS, 2)))
    # lilies on still, shallow water near low shores; boulders on the outside of bends
    for ix, iz in zip(*np.nonzero(water & F.red)):
        x, z = F.x0 + ix, F.z0 + iz
        if (x, z) in F.occ["surface"] or (x, z) in F.bridge:
            continue
        lvl = P.WATER_Y if F.river[ix, iz] else (P.TARN_Y if F.tarn[ix, iz] else int(F.blev[ix, iz]))
        depth = lvl - H(F, x, z)
        if w.id(x, lvl + 1, z) != B.AIR or w.id(x, lvl, z) != B.WATER:
            continue
        q = r[ix, iz]
        edge = near[ix, iz] and not np.all([water[min(ix + a, F.nx - 1), min(iz + b, F.nz - 1)] for a, b in ((1, 0), (0, 1))])
        if (F.tarn[ix, iz] or (F.river[ix, iz] and not F.outer[ix, iz])) and depth <= 2 and q < 0.09:
            w.set(x, lvl + 1, z, B.LILY)
            n_lily += 1
        elif (F.pools[ix, iz] or (F.river[ix, iz] and F.outer[ix, iz] and F.across[ix, iz] > P.RIVER_HALF - 1.5)) and q > 0.96:
            for dy in range(-1, 2):
                w.set(x, lvl + dy, z, *((B.MOSSY, 0) if dy <= 0 else (B.STONE, 0)))
    return n_reed, n_lily


def vines(w, F):
    """Vines down retaining walls and cliff faces: on air beside a face, trailing a few blocks."""
    up = np.maximum.reduce([np.roll(F.H, s, a) for a in (0, 1) for s in (1, -1)]) - F.H
    rng = np.random.default_rng(9)
    sides = ((1, 0, 8), (-1, 0, 2), (0, 1, 1), (0, -1, 4))
    for ix, iz in zip(*np.nonzero((up >= 4) & F.red)):
        if rng.random() > 0.25:
            continue
        x, z = F.x0 + ix, F.z0 + iz
        g = H(F, x, z)
        for dx, dz, bit in sides:
            hn = H(F, x + dx, z + dz) if -120 <= x + dx < 0 and -96 <= z + dz <= 95 else -1
            if hn >= g + 4 and (x, z) not in F.occ["surface"]:
                top = hn - 1
                for k in range(int(rng.integers(2, 6))):
                    yy = top - k
                    if yy <= g or w.id(x, yy, z) != B.AIR:
                        break
                    w.set(x, yy, z, B.VINE, bit)
                break


def flowers(w, F):
    r = RNG.random(F.shape)
    meadow = fbm(F.shape, 8, 2, seed=70)
    for ix, iz in zip(*np.nonzero(F.red & (F.angle < 25) & (meadow > 0.3))):
        x, z = F.x0 + ix, F.z0 + iz
        g = H(F, x, z)
        if w.id(x, g, z) != B.GRASS or w.id(x, g + 1, z) != B.AIR or (x, z) in F.occ["surface"]:
            continue
        if r[ix, iz] < 0.08:
            w.set(x, g + 1, z, *((B.FLOWER, int(RNG.choice([0, 3, 8, 6]))) if r[ix, iz] < 0.05 else (B.DANDELION, 0)))
        elif r[ix, iz] < 0.3:
            w.set(x, g + 1, z, B.TALLGRASS, 1)


def underground(w, F):
    rng = np.random.default_rng(13)
    for (x, z), f in F.cave_floor.items():
        if (x, z) in F.occ["under"]:
            continue
        m = F.mere[x - F.x0, z - F.z0]
        q = rng.random()
        if w.id(x, f + 1, z) != B.AIR:
            continue
        if 0 <= m < 6 and q < 0.06:
            w.set(x, f + 1, z, B.BROWN_MUSHROOM if q < 0.03 else B.RED_MUSHROOM)
        elif q < 0.004:
            # a stalagmite
            for k in range(1, 2 + int(rng.integers(1, 4))):
                w.set(x, f + k, z, B.COBBLE_WALL if k > 1 else B.STONE)
    # moss on the walls by the lake
    for (x, z), f in F.cave_floor.items():
        m = F.mere[x - F.x0, z - F.z0]
        if m > 8:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            X, Z = x + dx, z + dz
            if (X, Z) in F.cave_floor:
                continue
            for yy in range(f + 1, f + 6):
                if w.id(X, yy, Z) == B.STONE and rng.random() < 0.5:
                    w.set(X, yy, Z, B.MOSSY)


def clouds(w, F):
    """Each cloud a string of flattened blobs along its heading, white stained glass at heart, light grey
    stained glass on its underside, plain glass at its ragged rim."""
    rng = np.random.default_rng(21)
    n = 0
    for (x, z, y, L, Wd, a) in P.CLOUDS:
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        blobs = []
        k = int(L / 4) + 2
        for i in range(k):
            t = (i / (k - 1) - 0.5) * L
            r = Wd / 2 * (0.6 + 0.4 * math.sin(math.pi * (i + 0.5) / k)) * (0.8 + 0.4 * rng.random())
            off = (rng.random() - 0.5) * Wd * 0.4
            blobs.append((x + t * c - off * s, z + t * s + off * c, y + rng.integers(-1, 2), r))
        for bx, bz, by, r in blobs:
            for X in range(int(bx - r) - 1, int(bx + r) + 2):
                if X >= 0:
                    continue
                for Z in range(int(bz - r) - 1, int(bz + r) + 2):
                    for Y in range(int(by - r * 0.45) - 1, int(by + r * 0.55) + 2):
                        q = ((X - bx) / r) ** 2 + ((Z - bz) / r) ** 2 + ((Y - by) / (r * 0.5)) ** 2
                        if q > 1.0 or Y >= w.sy or w.id(X, Y, Z) not in (B.AIR, 95, B.GLASS):
                            continue
                        rim = q > 0.72
                        if rim and rng.random() < 0.35:
                            continue
                        if rim:
                            w.set(X, Y, Z, B.GLASS)
                        elif Y < by - r * 0.15:
                            w.set(X, Y, Z, 95, 8)
                        else:
                            w.set(X, Y, Z, 95, 0)
                        n += 1
    return n


def build(w, F):
    n = trees(w, F)
    reeds, lilies = water_edges(w, F)
    vines(w, F)
    flowers(w, F)
    underground(w, F)
    c = clouds(w, F)
    print(f"  planted {n} trees, {reeds} reeds, {lilies} lilies; {c} blocks of cloud")
