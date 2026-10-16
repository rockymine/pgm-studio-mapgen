"""The trees. Two species and a burnt one: the studio's oak, its crown turned autumn by laying orange, yellow and brown clay among the leaves
(the biome tints the rest); its spruce on the ice lane; dead oaks in the ash. A wood stands where a noise says a wood does, never on a road,
a building, a plaza, a bridge's approach, a steep face or the ground round a core."""
import dataclasses
import math

import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.geom import noise
from pgmvox.scenery import trees as TR
from util import claimed, claim_cells, disc

TONES = {"russet": [(1, 0.5), (12, 0.5)], "orange": [(1, 0.8), (4, 0.2)], "gold": [(4, 0.6), (1, 0.4)], "amber": [(1, 0.4), (4, 0.3), (12, 0.3)]}
THROUGH = TR.PLANTS | {B.STAINED_CLAY, B.SNOW_LAYER}
GROUND = TR.GIVES_WAY | {B.COAL_ORE, B.NETHERRACK, B.RED_SANDSTONE, B.PACKED_ICE, B.HARDENED_CLAY, B.SNOW, B.SOUL_SAND}


def scatter(w, zone, by_kind, weights, rng, spacing, tries, planted, ok, radius=0.8):
    """TR.scatter with ground that gives way to a crown: the strata's own rock, snow, clay and netherrack."""
    X, Z = w.grid()
    names = list(weights)
    p = np.array([weights[k] for k in names], float)
    p /= p.sum()
    cells = np.argwhere(zone)
    rng.shuffle(cells)
    n = 0
    for i, k in cells[:tries]:
        x, z = int(X[i, k]), int(Z[i, k])
        group = by_kind[names[int(rng.choice(len(names), p=p))]]
        t = group[int(rng.integers(len(group)))]
        c = t.crown * radius
        if any((x - px) ** 2 + (z - pz) ** 2 < ((c + pc) * spacing) ** 2 for px, pz, pc in planted):
            continue
        if not ok(x, z, t):
            continue
        if TR.plant(w, x, z, t, int(rng.integers(4)), through=THROUGH, gives_way=GROUND):
            planted.append((x, z, c))
            n += 1
    return n


def autumn(tree, tone, share, seed):
    """The tree with `share` of its leaves replaced by clay in the tone's colours, drawn once per tree."""
    rng = np.random.default_rng(seed)
    blocks = []
    palette, weights = zip(*TONES[tone])
    for dx, dy, dz, i, d in tree.blocks:
        if i in TR.LEAVES and rng.random() < share:
            blocks.append((dx, dy, dz, B.STAINED_CLAY, int(rng.choice(palette, p=weights))))
        else:
            blocks.append((dx, dy, dz, i, d))
    return dataclasses.replace(tree, blocks=tuple(blocks), name=f"{tree.name}-{tone}-{seed}")


def library():
    lib = TR.library()
    by = TR.kinds(lib)
    out = {"oak": [], "spruce": [], "tiny-spruce": [], "tall-spruce": []}
    k = 0
    for kind, take in (("tiny-oak", 9), ("dense-oak", 5)):
        for t in by[kind][:take]:
            for tone in TONES:
                k += 1
                out.setdefault("autumn", []).append(autumn(t, tone, 0.5, 1000 + k))
    k = 0
    for t in by["oak"][:6]:
        for tone in ("orange", "gold", "amber"):
            k += 1
            out.setdefault("great", []).append(autumn(t, tone, 0.62, 2000 + k))
    out["tall"] = by["tall-spruce"]
    out["tiny"] = by["tiny-spruce"]
    return out


def stands_clear(x, z, deg, ice, fire, minimum_deg=44):
    i, k = x - P.X_MIN, z - P.Z_MIN
    return P.LAND[i, k] and deg[i, k] < minimum_deg and not claimed(x, z) and z < -17


def plant_woods(w, deg, ice, fire, rng, stats):
    lib = library()
    X, Z = P.X, P.Z
    red = Z < -17
    forest = 0.5 * land.SYM.field(noise.fbm(X.shape, 23, 3, seed=201))
    grove = land.SYM.field(noise.fbm(X.shape, 15, 2, seed=202))
    placed = []
    n_autumn = n_spruce = n_edge = 0
    # the autumn orchard and its woods: the middle and the edges of the other two lanes, in groves
    zone = red & (ice < 0.55) & (fire < 0.6) & (forest + 0.2 * grove > -0.6)
    by = {"autumn": lib["autumn"]}
    ok = lambda x, z, t: stands_clear(x, z, deg, ice, fire) and (math.hypot(x - land.BEACON[0], z - land.BEACON[1]) > 7)
    great = 0
    for gx, gz in ((-20, -34), (22, -52), (-22, -52), (26, -28), (-4, -66), (14, -66), (-20, -24), (28, -64), (8, -20)):
        for ox, oz in ((0, 0), (3, 0), (-3, 0), (0, 3), (0, -3), (4, 4), (-4, -4)):
            x, z = gx + ox, gz + oz
            t = lib["great"][int(rng.integers(len(lib["great"])))]
            if ok(x, z, t) and TR.plant(w, x, z, t, int(rng.integers(4)), through=THROUGH, gives_way=GROUND):
                placed.append((x, z, t.crown * 0.9))
                claim_cells([(x, z)], 2)
                great += 1
                break
    stats["great maples"] = great
    avenue(w, lib, rng, placed, stats)
    n_rows = 0
    for gx in range(6, 30, 7):
        for gz in range(-36, -19, 6):
            x, z = gx + int(rng.integers(-1, 2)), gz + int(rng.integers(-1, 2))
            t = lib["autumn"][int(rng.integers(len(lib["autumn"])))]
            if ok(x, z, t) and TR.plant(w, x, z, t, int(rng.integers(4)), through=THROUGH, gives_way=GROUND):
                placed.append((x, z, t.crown * 0.8))
                n_rows += 1
    n_great = scatter(w, zone & (ice < 0.5), {"great": lib["great"]}, {"great": 1.0}, rng, 0.9, 5000, placed, ok, radius=0.9)
    n_autumn = n_rows + n_great + scatter(w, zone & (ice < 0.5), by, {"autumn": 1.0}, rng, 1.0, 12000, placed, ok)
    # the ice lane: spruce in stands, tall among tiny
    sp = red & (ice > 0.42) & (forest + 0.25 * grove > -0.12)
    by2 = {"tall": lib["tall"], "tiny": lib["tiny"]}
    ok2 = lambda x, z, t: stands_clear(x, z, deg, ice, fire, 40) and math.hypot(x - land.RIME[0], z - land.RIME[1]) > 16 \
        and land.lake_distance(np.array([[x]]), np.array([[z]]))[0, 0] > 1.1
    n_spruce = scatter(w, sp, by2, {"tall": 0.55, "tiny": 0.45}, rng, 0.7, 7000, placed, ok2)
    stats["autumn trees"], stats["spruce"] = n_autumn, n_spruce
    return placed


def avenue(w, lib, rng, placed, stats):
    """The Drove Road lined with maples every nine blocks, one side and then the other, so the main way through Amberford reads as somebody's."""
    from pgmvox.geom.shapes import length, point_at
    pts = [(2, -68), (-1, -58), (2, -49), (-4, -44), (-7, -37), (-5, -28), (-1, -20)]
    total = length(pts)
    s, n, put = 4.0, 0, 0
    while s < total:
        (px, pz), (hx, hz) = point_at(pts, s)
        sign = 1 if n % 2 == 0 else -1
        s += 9
        n += 1
        for reach in (4.8, 5.8, 6.8, 8.0):
            x, z = int(round(px - hz * sign * reach)), int(round(pz + hx * sign * reach))
            t = lib["autumn"][int(rng.integers(len(lib["autumn"])))]
            if any((x - a) ** 2 + (z - b) ** 2 < 16 for a, b, _ in placed):
                break
            if TR.plant(w, x, z, t, int(rng.integers(4)), through=THROUGH, gives_way=GROUND):
                placed.append((x, z, t.crown * 0.8))
                claim_cells([(x, z)], 1)
                put += 1
                break
    stats["avenue"] = put


def dead_trees(w, deg, fire, rng, stats):
    """Burnt oaks in the ash: a bare trunk and arms, none near a road, a building, the moat or the objectives."""
    X, Z = P.X, P.Z
    zone = (Z < -17) & (fire > 0.5) & P.LAND & (deg < 30)
    cells = np.argwhere(zone)
    rng.shuffle(cells)
    n = 0
    taken = []
    for i, k in cells[:1400]:
        x, z = int(X[i, k]), int(Z[i, k])
        if claimed(x, z) or math.hypot(x - land.FORGE[0], z - land.FORGE[1]) < 20 or any((x - a) ** 2 + (z - b) ** 2 < 49 for a, b in taken):
            continue
        if rng.random() < 0.28:
            TR.dead_tree(w, x, int(P.H[i, k]), z, rng, int(rng.integers(5, 9)))
            taken.append((x, z))
            n += 1
    stats["dead trees"] = n
