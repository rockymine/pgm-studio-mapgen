"""Thawline's ground in the world: rock in beds, soil by slope, the top by season, the waters, the rift.

    rock(w)        both halves at once: beds of stone and andesite, soil by slope, bedrock at y 1 under the land;
                   the island's underside tapers to the void at the coast and drops sheer into the rift
    paint(w, ...)  the top of every column by its half, its depth from the rift, its slope and the way it faces:
                   snow over Frost's back, autumn under a first snow at its front, autumn at Ember's front with a
                   frost in the shade, leaf litter and burnt ground at Ember's back; rock wherever it is steep
    waters(w)      the tarn and the beck; ice on Frost's margins, lily pads on Ember's
    rift(w)        the Thawline's floor: lava between baked walls, icicles hung down Frost's wall, lava falling
                   down Ember's, the beck's fall into the rift where it meets the lava
"""
import numpy as np
from scipy import ndimage

import plan as P
from pgmvox import B
from pgmvox.geom import noise
from pgmvox.geom.noise import smoothstep as ss
from pgmvox.geom.shapes import distance_in, polyline
from pgmvox.surface import terrain as T
from season import ICE_PLAINS, MESA, SAVANNA

SNOWY = (B.SNOW_LAYER, B.SNOW)


def strata():
    return T.Strata([((B.STONE, 0), 3, 4), ((B.STONE, 5), 2.5, 3), ((B.COBBLE, 0), 0.6, 1), ((B.STONE, 0), 1, 2),
                     ((B.STONE, 6), 0.8, 2), ((B.STONE, 1), 0.35, 1)], seed=17, start=1)


REF = 42                    # the underside is measured down from this height, whatever the ground over it


def bottom():
    """Where the rock ends under each column of the land and the rift together, one floating island: four or five
    under the coast, deeper inland as a cone with flutes and spires hanging from it, never below y 1. The rift is
    part of the island's body, so the Thawline is a gorge with a floor and not a gap between two plates."""
    body = P.LAND | P.RIFT
    hang = T.root_depth(body, cone=0.9, power=0.85, rough=0.5, flutes=5.0, flute_cell=4, spires=14.0, spire_cell=9,
                        seed=61)
    from scipy.ndimage import gaussian_filter
    top = np.where(P.LAND, P.H, P.RIFT_FLOOR + 20).astype(float)
    base = np.minimum(REF, gaussian_filter(top, 3, mode="nearest") - 2)
    return np.where(body, np.clip(base - 4 - hang, 1, None), 0).astype(int)


def bed_fill():
    """The rock at a column's height y, as the beds lay it: (i, k, y) -> block."""
    beds = strata()
    offset = T.bed_offset(P.H.shape, dip=(0.03, 0.0), fold=2.5, cell=20, seed=5, drape=(P.H, 0.35, 10))
    return lambda i, k, y: beds(y - int(offset[i, k]))


def rock(w):
    beds = strata()
    offset = T.bed_offset(P.H.shape, dip=(0.03, 0.0), fold=2.5, cell=20, seed=5,
                          drape=(P.H, 0.35, 10))
    fill = T.beds(beds, offset, flecks=[((B.STONE, 0), (B.COBBLE, 0), 0.04), ((B.STONE, 5), (B.STONE, 0), 0.05)],
                  seed=6)
    deg = T.lay(w, P.H, mask=P.LAND, top=lambda d, h: (B.GRASS, 0), under=(B.DIRT, 0), bands=fill, from_y=1,
                bottom=bottom())
    return deg


def season_fields():
    """The noise fields the paint reads, each made once so every pass agrees."""
    shape = P.H.shape
    return dict(
        litter=noise.fbm(shape, 3, 3, seed=101),        # the autumn floor's patches, five to seven across
        snow=noise.fbm(shape, 11, 2, seed=102),         # where the first snow lies on Frost's front
        drift=noise.fbm(shape, 11, 2, seed=103),        # where it drifts deeper at the back
        rockset=noise.fbm(shape, 2, 2, seed=104),       # which stone a rocky top takes
        bend=noise.fbm(shape, 18, 2, seed=105),         # the season's edges, bent
    )


def depth_of(F):
    """0 at the rift, 1 at the board's back, the same on both halves (Frost's z < 0 and Ember's image)."""
    d = (np.abs(P.Z + 0.5) - 6) / 90
    return np.clip(d + 0.06 * F["bend"], 0, 1)


def facing_north(H):
    """Where the ground falls toward the north (rising to the south): the shade side of a hill on Frost's field and
    on Ember's alike, since both look across the rift at the other."""
    gz = np.gradient(H.astype(float), axis=1)
    return gz > 0.35


def snow_cover(F, depth):
    """Frost's chance of lying snow: 0.35 at the rift's lip, every column past a depth of 0.55."""
    return 0.38 + 0.62 * ss(0.12, 0.55, depth)


def paint(w, deg, F, trees_litter):
    """The top block of every land column, and what lies on it (snow layers), by half, depth, slope and facing.
    `trees_litter` is a mask of the ground under the crowns, laid with leaf litter rather than grass."""
    H, LAND, made, wet = P.H, P.LAND, P.MADE, P.WET
    depth = depth_of(F)
    frost = P.Z < 0
    north = facing_north(H)
    cover = snow_cover(F, depth)
    snowy = F["snow"] * 0.5 + 0.5 < cover
    stats = {"snow": 0, "litter": 0, "rock": 0, "grass": 0}
    rs = F["rockset"]
    lt = F["litter"]
    beds_at = bed_fill()
    for i, k in np.argwhere(LAND & ~wet & ~made):
        h = int(H[i, k])
        a = deg[i, k]
        f = frost[i, k]
        dp = depth[i, k]
        top = None
        layer = None
        # the autumn floor: grass, with podzol and coarse dirt in patches at the two ends of the field's range
        v = lt[i, k]
        if trees_litter[i, k]:
            floor = (B.DIRT, 2) if v > -0.25 else (B.DIRT, 1)
        elif v < -0.42:
            floor = (B.DIRT, 2)
        elif v > 0.48:
            floor = (B.DIRT, 1)
        else:
            floor = (B.GRASS, 0)
        if a > 52:                                          # a face: the beds' own rock, to its top
            w.ids[i, h, k], w.dat[i, h, k] = beds_at(i, k, h)
            continue
        if a > 34:                                          # rock coming through where it steepens
            top = (B.STONE, 5) if rs[i, k] > 0.15 else (B.STONE, 0) if rs[i, k] > -0.35 else (B.GRAVEL, 0)
            stats["rock"] += 1
            if f and dp > 0.3 and a < 44:
                layer = 0
        elif f:
            if snowy[i, k]:
                top = (B.SNOW, 0) if dp > 0.45 else floor
                drift = F["drift"][i, k]
                layer = int(np.clip(round(0.6 + 1.6 * drift), 0, 2)) if dp > 0.5 else 0
                stats["snow"] += 1
            else:
                top = floor
        else:
            top = floor
            pass
        if top is None:
            continue
        w.ids[i, h, k], w.dat[i, h, k] = top
        stats["litter" if top[0] == B.DIRT else "grass" if top[0] == B.GRASS else "snow" if top[0] == B.SNOW
              else "rock"] += 0
        if layer is not None and w.ids[i, h + 1, k] == 0:
            w.ids[i, h + 1, k], w.dat[i, h + 1, k] = B.SNOW_LAYER, layer
    # the biome: Ice plains over Frost's back, Mesa over the autumn, Savanna under Ember's larch crowns
    bio = np.where(frost & (depth > 0.40), ICE_PLAINS, MESA)
    w.biome[:, :] = bio.astype(np.uint8)
    return stats


def icefall(X, Z):
    """Frost's icefalls: where the Glacier's ice comes down between its spurs, a band either side of two lines."""
    m = np.zeros(X.shape, bool)
    for pts in ([(-13, -100), (-11, -92), (-9, -89)], [(12, -100), (11, -93), (9, -90)],
                ([(-40, -97), (-36, -90)]), ([(38, -97), (35, -90)])):
        d = polyline(X, Z, pts)[0]
        m |= d < 3.2 + 1.2 * noise.fbm(X.shape, 4, 2, seed=int(abs(pts[0][0])))
    return m & (Z < -84)


CASCADES = [-22, 5, 27]      # x of the three falls down the board's back, Frost's; Ember's are their images


def glacier(w, deg, under):
    """The Glacier on Frost's back and its twin on Ember's. Frost: the ridge's steep ground and its crest capped with
    packed ice, snow on what is gentle, the icefalls laid three deep between the spurs, the back cliff glazed ten
    deep where it falls to the void, and three frozen falls hanging down it. Ember: the same ground a cinder ridge,
    coal and black clay with obsidian, lava running in the icefalls' gutters, and three lava falls pouring off the
    back into the void."""
    X, Z, H = P.X, P.Z, P.H
    fall = icefall(X, Z)
    rng = np.random.default_rng(71)
    edge = distance_in(P.LAND, "euclid")
    cap = P.LAND & (Z < -88) & ((H > 58) | fall) & ~P.MADE
    back = P.LAND & (Z < -80) & (edge <= 1.5) & ~P.MADE
    laid = 0
    for i, k in np.argwhere(cap | back):
        x, z, h = int(X[i, k]), int(Z[i, k]), int(H[i, k])
        steep = deg[i, k] > 34 or fall[i, k]
        lo = h - 2 if cap[i, k] else h - 1
        if back[i, k]:
            lo = max(int(under[i, k]) + 2, h - 10 - int(rng.integers(0, 4)))
        for y in range(lo, h + 1):
            w.set(x, y, z, *((B.PACKED_ICE, 0) if steep or y < h or back[i, k] else (B.SNOW, 0)))
        if steep and w.id(x, h + 1, z) == B.SNOW_LAYER:
            w.set(x, h + 1, z, B.AIR)
        ex, ez = -1 - x, -1 - z
        for y in range(lo, h + 1):
            r = rng.random()
            w.set(ex, y, ez, *((B.COAL_BLOCK, 0) if r < 0.4 else (B.STAINED_CLAY, 15) if r < 0.8 else
                               (B.OBSIDIAN, 0) if r < 0.93 else (B.NETHERRACK, 0)))
        if w.id(ex, h + 1, ez) == B.SNOW_LAYER:
            w.set(ex, h + 1, ez, B.AIR)
        laid += 1
    # the gutters: lava down the middle of each cinder flow, sunk a block, on its steep ground
    for pts in ([(-13, -100), (-11, -92), (-9, -89)], [(12, -100), (11, -93), (9, -90)]):
        d = polyline(X, Z, pts)[0]
        for i, k in np.argwhere((d < 0.8) & P.LAND & (deg > 25) & (Z < -88)):
            x, z = -1 - int(X[i, k]), -1 - int(Z[i, k])
            h = int(H[x - P.X_MIN, z - P.Z_MIN])
            w.set(x, h, z, B.LAVA)
            w.set(x, h - 1, z, B.OBSIDIAN)
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if w.id(x + dx, h, z + dz) in (B.AIR, B.SNOW_LAYER):
                    w.set(x + dx, h, z + dz, B.STAINED_CLAY, 15)
    # the falls off the back: for each, the coast column nearest its x at the back, and the void column beyond it
    for cx in CASCADES:
        i = cx - P.X_MIN
        ks = [k for k in range(P.H.shape[1]) if P.LAND[i, k]]
        k = min(ks)
        x, z, h = cx, int(Z[i, k]), int(H[i, k])
        low = int(under[i, k]) - 6
        for dx in (0, 1):
            # Frost: a frozen fall, packed ice and ice hanging two wide down the outside of the cliff
            for y in range(low, h + 1):
                v = rng.random()
                w.set(x + dx, y, z - 1, *((B.ICE, 0) if v < 0.35 else (B.PACKED_ICE, 0)))
                if v < 0.15 and y < h - 2:
                    w.set(x + dx, y, z - 2, B.ICE)
            w.set(x + dx, h, z, B.PACKED_ICE)
            # Ember: lava welling from a pool in the crest and pouring off the back
            ex, ez = -1 - (x + dx), -1 - z
            w.set(ex, h, ez, B.LAVA)
            w.set(ex, h - 1, ez, B.OBSIDIAN)
            for y in range(low, h + 1):
                w.set(ex, y, ez + 1, B.LAVA_FLOW, 8)
            w.set(ex, h, ez + 1, B.LAVA)
    return laid


def waters(w, F):
    """The tarn and the beck filled to their surfaces, beds of gravel and clay; Frost's margins iced over and its
    beck shelved with ice in its quiet reaches; Ember's tarn carrying lily pads."""
    level = np.zeros(P.H.shape)
    for wat in P.WATERS:
        level = np.maximum(level, np.where(wat.mask, wat.surface, 0))
    level = np.where(P.LAND, level, 0)
    bed = [T.Paint((B.GRAVEL, 0), values=((F["litter"], 0.2, None),)), T.Paint((B.CLAY, 0))]
    T.fill_water(w, P.H, level, bed, mask=P.LAND)
    wet = level > 0
    shore = distance_in(~wet, "euclid")
    rng = np.random.default_rng(81)
    depth = depth_of(F)
    for i, k in np.argwhere(wet):
        x, z = int(P.X[i, k]), int(P.Z[i, k])
        y = int(level[i, k])
        if z < 0:
            if shore[i, k] <= 2.2 + 1.5 * F["snow"][i, k] or depth[i, k] > 0.5:
                w.set(x, y, z, B.ICE)
        elif shore[i, k] > 1.5 and rng.random() < 0.05:
            w.set(x, y + 1, z, B.LILY)
    return int(wet.sum())


def beck_fall(w):
    """The Rime Beck falls off Frost's lip into the rift and the Rust Beck off Ember's, each onto a mound of
    obsidian and cobble standing out of the lava where the water meets it."""
    out = 0
    for side in (1, -1):
        x0, z0 = P.land.BECK[-1]
        if side < 0:
            x0, z0 = -1 - x0, -1 - z0
        # the lip: the wet column of the beck nearest the rift
        best = None
        for dx in range(-3, 4):
            for dz in range(-6, 7):
                x, z = x0 + dx, z0 + dz
                i, k = x - P.X_MIN, z - P.Z_MIN
                if 0 <= i < P.H.shape[0] and 0 <= k < P.H.shape[1] and P.WET[i, k]:
                    key = -z if side > 0 else z
                    if best is None or key < best[0]:
                        best = (key, x, z)
        if best is None:
            continue
        _, x, z = best
        top = int(P.H[x - P.X_MIN, z - P.Z_MIN]) + 1
        step = 1 if side > 0 else -1
        zz = z + step
        while w.id(x, top - 1, zz) != 0 and abs(zz - z) < 6:
            zz += step
        for dx in (-1, 0, 1):
            if not P.WET[x + dx - P.X_MIN, z - P.Z_MIN]:
                continue
            for y in range(P.LAVA_Y + 1, top + 1):
                if w.id(x + dx, y, zz) == 0:
                    w.set(x + dx, y, zz, B.WATER_FLOW, 8)
                    out += 1
        rng = np.random.default_rng(91 + side)
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                r = np.hypot(dx, dz)
                if r <= 3.2:
                    hgt = P.LAVA_Y + int(2.5 - r * 0.7) + int(rng.integers(0, 2))
                    for y in range(P.RIFT_FLOOR, hgt + 1):
                        w.set(x + dx, y, zz + step * 2 + dz, *((B.OBSIDIAN, 0) if rng.random() < 0.6 else (B.COBBLE, 0)))
    return out


def rift(w):
    """The Thawline's bottom: the island's rock up to RIFT_FLOOR under the rift, netherrack on it and lava three deep
    over that, dammed with rock at both ends where the gorge opens to the void; the walls baked to netherrack and
    black clay within three of the lava."""
    RIFT = P.RIFT
    X, Z = P.X, P.Z
    rng = np.random.default_rng(101)
    under = bottom()
    fl = P.RIFT_FLOOR
    rim_d = distance_in(P.LAND | P.RIFT, "euclid")
    for i, k in np.argwhere(RIFT):
        x, z = int(X[i, k]), int(Z[i, k])
        end = rim_d[i, k] <= 4
        beds = strata()
        for y in range(int(under[i, k]), fl):
            w.set(x, y, z, *beds(y))
        w.set(x, fl, z, *((B.NETHERRACK, 0) if rng.random() < 0.7 else (B.OBSIDIAN, 0)))
        if end:
            for y in range(fl + 1, P.KILL_Y - 5 - int(2 * rim_d[i, k]) + int(rng.integers(0, 2))):
                w.set(x, y, z, *beds(y))
        else:
            w.column(x, z, fl + 1, P.LAVA_Y, B.LAVA)
    near = distance_in(~RIFT, "euclid")
    hot = P.LAND & (near <= 3)
    for i, k in np.argwhere(hot):
        x, z = int(X[i, k]), int(Z[i, k])
        for y in range(fl - 2, P.LAVA_Y + 7 - int(2 * near[i, k])):
            if w.id(x, y, z) not in (0, B.LAVA, B.LAVA_FLOW):
                r = rng.random()
                w.set(x, y, z, *((B.NETHERRACK, 0) if r < 0.55 else (B.STAINED_CLAY, 15) if r < 0.8 else (B.OBSIDIAN, 0)))
    return int(RIFT.sum())


def rift_walls(w):
    """Frost's wall of the rift hung with icicles; Ember's with lava running out of its seams. Each is laid on a
    rift column beside a wall, every so often along the wall, hanging from the land's underside rim of the lip."""
    RIFT = P.RIFT & ~P.STACK
    X, Z = P.X, P.Z
    rng = np.random.default_rng(111)
    hung, falls = 0, 0
    for i, k in np.argwhere(RIFT):
        x, z = int(X[i, k]), int(Z[i, k])
        for dz, frost in ((-1, True), (1, False)):
            # a rift column whose neighbour toward a lip is land
            if not P.LAND[i, k + dz] if 0 <= k + dz < RIFT.shape[1] else True:
                continue
            if frost != (z < 0):
                continue
            lip = int(P.H[i, k + dz])
            if frost:
                if rng.random() < 0.22:
                    start = lip - int(rng.integers(1, 4))
                    n = int(rng.integers(3, 11))
                    for y in range(start, start - n, -1):
                        if w.id(x, y, z) == 0 and w.id(x, y + 1, z) in (B.PACKED_ICE, B.ICE) or y == start:
                            w.set(x, y, z, B.PACKED_ICE if y > start - n + 2 else B.ICE)
                    hung += 1
            else:
                if rng.random() < 0.05:
                    start = lip - int(rng.integers(4, 9))
                    w.set(x, start, z + dz, B.LAVA)
                    for y in range(P.LAVA_Y + 1, start + 1):
                        if w.id(x, y, z) == 0:
                            w.set(x, y, z, B.LAVA_FLOW, 8)
                    falls += 1
                elif rng.random() < 0.08:
                    y = lip - int(rng.integers(3, 18))
                    if y > 8 and w.id(x, y, z + dz) != 0:
                        w.set(x, y, z + dz, B.GLOWSTONE)
    return hung, falls


def litter(w, mask):
    """The ground under the crowns laid with leaf litter: podzol, a little coarse dirt, where the top is grass or the
    autumn floor; Frost's snow left lying on it."""
    rng = np.random.default_rng(131)
    n = 0
    for i, k in np.argwhere(mask & P.LAND & ~P.WET & ~P.MADE):
        x, z = int(P.X[i, k]), int(P.Z[i, k])
        h = int(P.H[i, k])
        if w.id(x, h, z) == B.GRASS:
            w.set(x, h, z, *((B.DIRT, 2) if rng.random() < 0.75 else (B.DIRT, 1)))
            n += 1
    return n
