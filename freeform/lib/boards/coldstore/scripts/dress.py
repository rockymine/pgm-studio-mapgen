"""Coldstore's dressing, all of it in the faces of the rock or over the roof, so none of it is a ledge to stand on.

    alcoves(w)      the great door's alcove in the south wall at the islands' height, and the balcony at the vents'
    vault_door(w)   a round blast door in the west wall's face, its hinge on the north
    faces(w, k)     on every face of rock: pipes, valves, vent grates, screens, graffiti and fire extinguishers
    ceiling(w)      the roof's underside coffered in obsidian and grey wool, lamps, icicles, and its fans
    drifts(w, k)    snow and ice blown in through the fans, lying on the islands
    surface(w)      the block's rock rim and the snowfield over the roof, the fans' shafts, the hatch and the mast

**The story is that the cold got in.** The bunker's fans drew the air of the ice field above it, and the snow came
with it: it lies in drifts on the islands, thickest under the fans, and the islands' drifts are the one ground a
player can dig away.
"""
import math

import numpy as np

import layout as L
import shell as S
from pgmvox import B
from pgmvox.geom import noise

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
SPRAY = ((1, 4), (2, 6), (3, 11), (5, 13), (14, 1))     # a blot's rim and its middle, in stained clay


def alcoves(w):
    """The great door: an alcove eight wide in the south wall at the islands' height, its back a door that does not
    open. The balcony: an alcove at the vents' height where the south wall meets its image across the teams."""
    a0, a1 = -24, -17
    for u in range(a0, a1 + 1):
        for v in range(45, 52):
            w.column(u, v, L.FLOOR, L.TOP - 1, B.BEDROCK)
            w.set(u, L.TOP, v, *S.DECK)
            for y in range(L.TOP + 1, L.TOP + 11):
                w.set(u, y, v, B.AIR)
        for y in range(L.TOP + 1, L.TOP + 11):
            w.set(u, y, 52, B.IRON_BLOCK)
    for v in range(45, 52):
        for y in range(L.TOP + 1, L.TOP + 11):
            for u in (a0 - 1, a1 + 1):
                w.set(u, y, v, *S.SKIN)
    for u in range(a0 + 1, a1):                           # the door's leaves, hazard-striped where they meet
        w.set(u, L.TOP + 11, 45, *S.SKIN)
        for y in range(L.TOP + 2, L.TOP + 10):
            if u in (-21, -20):
                w.set(u, y, 52, B.STAINED_CLAY, 4 if (u + y) % 4 < 2 else 15)
            else:
                w.set(u, y, 52, B.STAINED_CLAY, 8)
    y0, y1 = L.TUNNEL
    for u in range(-4, 0):
        for v in range(45, 53):
            w.set(u, y0, v, *S.TUNNEL_FLOOR)
            for y in range(y0 + 1, y1 + 1):
                w.set(u, y, v, B.AIR)
        for y in range(y0 + 1, y1 + 1):
            w.set(u, y, 53, B.STAINED_CLAY, 15)
        w.set(u, y0 + 1, 45, B.COBBLE_WALL)
    for v in range(45, 53):
        for y in range(y0 + 1, y1 + 1):
            w.set(-5, y, v, *S.SKIN)
    for u in range(-4, 0):                                # a screen on its back wall
        for y in range(y0 + 2, y1):
            if (u * 3 + y * 5) % 7 == 0:
                w.set(u, y, 53, B.STAINED_CLAY, 5)


def vault_door(w):
    """A round blast door nine across in the west wall's face between the hub and the wool block, its hinge north."""
    cu, cv, cy, r = -91, 20, 28, 4.6
    for v in range(cv - 6, cv + 7):
        for y in range(cy - 6, cy + 7):
            d = math.hypot(v - cv, y - cy)
            if d <= r - 1.2:
                spoke = abs(v - cv) <= 0 or abs(y - cy) <= 0
                w.set(cu, y, v, *((B.IRON_BLOCK, 0) if spoke else (B.STONE, 6)))
            elif d <= r:
                w.set(cu, y, v, B.IRON_BLOCK)
            elif d <= r + 1 and v < cv:
                w.set(cu, y, v, B.QUARTZ, 2)
    for y in (cy - 3, cy + 3):                            # the hinge's two knuckles
        w.set(cu, y, cv - 6, B.IRON_BLOCK)


def faces(w, k, seed=5):
    """Every face of rock looking onto the void: its pipes, valves, vents, screens, graffiti and extinguishers."""
    rng = np.random.default_rng(seed)
    U0, V0 = S.U0, S.V0
    blots = noise.fbm((400, 12), 3, 2, seed=seed)       # over a face's run and the height above the islands
    paint = noise.fbm((400, 12), 9, 1, seed=seed + 1)
    for u in range(U0, 0):
        for v in range(V0, S.V1 + 1):
            if k[u - U0, v - V0] != S.ROCK:
                continue
            out = [d for d in DIRS if S.at(k, u + d[0], v + d[1]) == S.VOID]
            if not out or w.id(u, 30, v) != B.STONEBRICK:
                continue
            along = v if out[0][0] else u
            if w.id(u, 29, v) == B.STONEBRICK:            # the pipes, two of them, round every face at y 29 and 30
                run = 3 if out[0][0] == 0 else 4             # a quartz pillar laid along the face reads as a pipe
                w.set(u, 29, v, B.QUARTZ, run)
                w.set(u, 30, v, B.QUARTZ, run)
                if along % 11 == 0:
                    w.set(u, 29, v, B.WOOL, 14)                   # a valve
                if along % 11 == 1:
                    w.set(u, 30, v, B.IRON_BLOCK)                 # a joint
            g, c = blots[(u - v) % 400], paint[(u - v) % 400]
            for y in range(L.TOP + 2, L.TOP + 9):         # graffiti low on the faces, where a hand reaches
                if g[y - L.TOP] > 0.25 and w.id(u, y, v) == B.STONEBRICK:
                    tones = SPRAY[int((c[y - L.TOP] + 1) * 2.5) % len(SPRAY)]
                    w.set(u, y, v, B.STAINED_CLAY, tones[1] if g[y - L.TOP] > 0.5 else tones[0])
            if along % 17 == 3:                           # a vent grate, three wide and two high
                for y in (32, 33):
                    w.set(u, y, v, B.IRON_BARS)
            if along % 23 == 9 and w.id(u, 22, v) == B.STONEBRICK:      # a screen
                for y in range(21, 25):
                    w.set(u, y, v, B.STAINED_CLAY, 15)
                w.set(u, 22, v, B.STAINED_CLAY, int(rng.choice([5, 9, 13])))
                w.set(u, 23, v, B.STAINED_CLAY, int(rng.choice([5, 9, 3])))
            if along % 29 == 14:                          # a fire extinguisher
                w.set(u, L.TOP + 2, v, B.WOOL, 14)
                w.set(u, L.TOP + 3, v, B.WOOL, 14)
                w.set(u, L.TOP + 4, v, B.COAL_BLOCK)
    for u in range(U0, 0):                                # the vents behind their grates: dark, a block deep
        for v in range(V0, S.V1 + 1):
            for y in (32, 33):
                if w.id(u, y, v) == B.IRON_BARS:
                    for du, dv in DIRS:
                        if S.at(k, u - du, v - dv) == S.ROCK and S.at(k, u + du, v + dv) == S.VOID:
                            w.set(u - du, y, v - dv, B.COAL_BLOCK)


def ceiling(w, seed=31):
    """The roof's underside coffered: ribs of obsidian every eight blocks, panels of grey wool between them with a lamp
    in each middle; icicles of packed ice hanging from it, thickest along the walls; and the fans. Packed ice, since
    a broken icicle of ice would leave water running from the roof."""
    rng = np.random.default_rng(seed)
    for u in range(S.U0, 0):
        for v in range(0, S.V1 + 1):
            if w.id(u, L.CEIL, v) != B.AIR:
                continue
            if u % 8 == 4 and v % 8 == 4:
                w.set(u, L.ROOF[0], v, B.SEA_LANTERN)
            elif u % 8 == 0 or v % 8 == 0 or (u % 8 + v % 8 == 8 and u % 8 in (2, 6)):
                w.set(u, L.ROOF[0], v, B.OBSIDIAN)       # the ribs, and a short diagonal at each lamp's corners
            else:
                w.set(u, L.ROOF[0], v, B.WOOL, 7)
    for u in range(S.U0, 0):
        for v in range(0, S.V1 + 1):
            if w.id(u, L.CEIL, v) != B.AIR or w.id(u, L.ROOF[0], v) == B.SEA_LANTERN:
                continue
            wall = any(w.id(u + du, L.CEIL, v + dv) != B.AIR for du, dv in DIRS)      # beside the cornice
            if rng.random() < (0.10 if wall else 0.025):
                n = int(rng.choice([1, 2, 2, 3, 3, 4, 5]))
                for y in range(L.CEIL, L.CEIL - n, -1):
                    if w.id(u, y, v) != B.AIR:
                        break
                    w.set(u, y, v, B.PACKED_ICE)
    for cu, cv, r in L.FANS:
        for u in range(cu - r - 1, cu + r + 2):
            for v in range(cv - r - 1, cv + r + 2):
                d = math.hypot(u - cu, v - cv)
                if d <= r:
                    for y in range(L.ROOF[0], L.ROOF[1]):
                        w.set(u, y, v, B.AIR)
                    if d > L.SHAFT:                                           # the funnel up into the shaft
                        w.set(u, L.ROOF[1] - 1, v, B.IRON_BLOCK)
                    else:
                        w.set(u, L.ROOF[1], v, B.AIR)
                    a = math.atan2(v - cv, u - cu)
                    if d < 1.5 or (abs(math.sin(2 * a)) < 0.35 and d < r - 0.5):
                        w.set(u, L.ROOF[1] - 2, v, B.IRON_BLOCK)              # the blades, four of them
                elif d <= r + 1:
                    w.set(u, L.ROOF[0], v, B.IRON_BARS)                       # the rim
                    w.set(u, L.ROOF[0] + 1, v, B.IRON_BLOCK)


def drifts(w, k, seed=11):
    """Snow on the islands: a scatter of layers everywhere, mounds by the walls and thickest under the fans, packed
    ice where a drift has lain long. Never on the spawn's way out or on a monument's slot."""
    rng = np.random.default_rng(seed)
    U0, V0 = S.U0, S.V0
    n = noise.fbm(k.shape, 6, 3, seed=seed)
    for u in range(U0, 0):
        for v in range(V0, S.V1 + 1):
            if k[u - U0, v - V0] != S.ISLAND or w.id(u, L.TOP + 1, v) != B.AIR:
                continue
            if abs(u - L.SLOT[0]) <= 2 and abs(v - L.SLOT[2]) <= 2 or u <= L.SPAWN_EXIT[1] + 3:
                continue
            fan = max(0.0, 1 - min(math.hypot(u - cu, v - cv) / (r * 2.2) for cu, cv, r in L.FANS))
            wall = any(S.at(k, u + du * s, v + dv * s) == S.ROCK for du, dv in DIRS for s in (1, 2))
            depth = n[u - U0, v - V0] * 1.8 + fan * 3.0 + (0.8 if wall else 0.0)
            if depth > 1.6:
                w.set(u, L.TOP + 1, v, B.PACKED_ICE if rng.random() < 0.25 else B.SNOW)
                if depth > 2.6:
                    w.set(u, L.TOP + 2, v, B.SNOW)
                    w.set(u, L.TOP + 3, v, B.SNOW_LAYER, int(rng.integers(0, 3)))
                else:
                    w.set(u, L.TOP + 2, v, B.SNOW_LAYER, int(rng.integers(0, 4)))
            elif depth > 0.7:
                w.set(u, L.TOP + 1, v, B.SNOW_LAYER, int(rng.integers(0, 2)))


def _strata(y, u, v):
    """The block's sides: beds of stone, andesite, diorite and cobble, gently waved, packed ice in the top beds."""
    k = (y + int(2.5 * math.sin(u / 9.0) + 2.0 * math.sin(v / 7.0))) % 11
    if y > L.SURFACE + 1 and k in (3, 4):
        return (B.PACKED_ICE, 0)
    return ((B.STONE, 0), (B.STONE, 0), (B.STONE, 5), (B.STONE, 5), (B.STONE, 0), (B.COBBLE, 0),
            (B.STONE, 0), (B.STONE, 3), (B.STONE, 0), (B.STONE, 5), (B.STONE, 0))[k]


def surface(w, seed=21):
    """The ice field over the roof, the drawn quarter's share of it. The map stays one block: past the bunker's walls
    a rim of rock RIM blocks thick stands from the world's floor, its sides beds of stone, and on top lies a snowfield
    as the winter study drew it: outcrops of tilted rock breaking through snow that flows round them, drift ridges
    across a wind from the west, and gorges cracked down through the ice, some of them out through the block's sides.
    A shaft rises from each fan to the sky, and the spawn's hatch and a mast stand on the snow."""
    from scipy import ndimage
    from pgmvox.geom.noise import smoothstep
    from pgmvox.geom.shapes import polyline, shatter
    ru, rv = L.OUTER_U - L.RIM, L.OUTER_V + L.RIM
    U, V = np.meshgrid(np.arange(ru, 0), np.arange(0, rv + 1), indexing="ij")
    U, V = U.astype(float), V.astype(float)
    base = L.SURFACE + 6 + 2.5 * noise.fbm(U.shape, 40, 3, seed=seed)
    p = shatter(U, V, 10, seed=seed + 2, warp=(5, 2, 60, 12))
    rng = np.random.default_rng(seed + 3)
    n = len(p.centres)
    plane = rng.uniform(2, 8, n)[p.id] + rng.uniform(-0.5, 0.5, n)[p.id] * (U - p.centres[p.id, 0]) \
        + rng.uniform(-0.5, 0.5, n)[p.id] * (V - p.centres[p.id, 1])
    crag = np.clip(noise.fbm(U.shape, 30, 3, seed=seed + 4) + 0.4 * noise.fbm(U.shape, 9, 2, seed=seed + 5) + 0.05,
                   0, None) / 0.45
    rock = base - 3 + np.clip(plane * crag, 0, None) - 2 * smoothstep(0.8, 0, p.edge) * crag \
        + 2 * noise.ridged(U.shape, 14, 3, seed=seed + 6) * crag
    smooth = ndimage.gaussian_filter(rock, 5)
    tail = ndimage.gaussian_filter(np.roll(np.clip(rock - smooth, 0, None), 5, axis=0), (8, 2))   # downwind, east
    Uw, Vw = noise.warp(U, V, seed=seed + 7, big=10, small=2, big_cell=50, small_cell=12)
    drift = 1.4 * np.sin(Uw / 7 + 0.3 * Vw / 7) + 0.7 * np.abs(np.sin(Uw / 2.6 + Vw / 11))
    snow = smooth + 2.2 + drift + 1.2 * tail - 0.6 * np.clip(rock - smooth, 0, None)
    deep = np.zeros(U.shape)
    for c in range(L.GORGES):                           # zigzag gorges down through the ice, a few bridged by snow
        x0, z0 = rng.uniform(ru, -10), rng.uniform(5, rv)
        ang = rng.uniform(0, np.pi)
        pts = [(x0, z0)]
        for _ in range(6):
            ang += rng.uniform(-0.7, 0.7)
            step = rng.uniform(8, 16)
            pts.append((pts[-1][0] + step * np.cos(ang), pts[-1][1] + step * np.sin(ang)))
        dd, al = polyline(U, V, pts)[:2]
        width = (1.2 + 1.8 * (0.5 + 0.5 * np.sin(al / 7 + c))) * smoothstep(0, 8, al) * smoothstep(al.max(), al.max() - 8, al)
        bridged = noise.fbm(U.shape, 8, 1, seed=seed + 60 + c) > 0.5
        depth = 10 + 4 * np.sin(al / 11 + 2 * c)
        deep = np.where((dd < width) & ~bridged, np.maximum(deep, depth * smoothstep(width, width * 0.3, dd)), deep)
    exposed = rock >= snow - 0.5
    top = np.where(exposed, rock, snow) - deep
    floor = L.SURFACE + 1                                # a gorge stops on the ice over the roof
    top = np.maximum(top, floor)
    for i in range(U.shape[0]):
        for j in range(U.shape[1]):
            u, v = int(U[i, j]), int(V[i, j])
            inside = u >= L.OUTER_U and v <= L.OUTER_V
            lo = L.SURFACE if inside else 0
            t = int(round(top[i, j]))
            r = int(round(min(rock[i, j], top[i, j])))
            side = u == ru or v == rv
            for y in range(lo, t + 1):
                if y <= r or (not inside and y < L.SURFACE):
                    blk = _strata(y, u, v) if side or y < L.SURFACE else \
                        ((B.STONE, 5) if p.id[i, j] % 3 == 0 else (B.COBBLE, 0) if p.id[i, j] % 7 == 0 else (B.STONE, 0))
                elif deep[i, j] > 0.5:
                    blk = (B.ICE, 0) if y == t else (B.PACKED_ICE, 0)
                else:
                    blk = (B.SNOW, 0) if y > t - 2 else (B.PACKED_ICE, 0)
                w.set(u, y, v, *blk)
            if not exposed[i, j] and deep[i, j] <= 0.5:
                layer = int(np.clip((snow[i, j] - t + 0.5) * 7, 0, 6))
                if layer:
                    w.set(u, t + 1, v, B.SNOW_LAYER, layer - 1)

    def ground(u, v):
        return int(round(top[u - ru, v]))
    for cu, cv, r in L.FANS:                              # the shaft from the fan to the sky, its crown louvred
        crown = max(ground(u, v) for u in range(cu - 4, cu + 5) for v in range(cv - 4, cv + 5)) + 5
        for u in range(cu - 4, cu + 5):
            for v in range(cv - 4, cv + 5):
                d = math.hypot(u - cu, v - cv)
                for y in range(L.ROOF[1] + 1, crown + 1):
                    if d <= L.SHAFT - 0.9:
                        w.set(u, y, v, B.AIR)
                    elif d <= L.SHAFT:
                        louvre = y > crown - 4 and (y + int(math.degrees(math.atan2(v - cv, u - cu)) // 30)) % 2
                        w.set(u, y, v, B.IRON_BARS if louvre else B.IRON_BLOCK)
                if d <= L.SHAFT:
                    for y in range(crown + 1, L.SY):
                        w.set(u, y, v, B.AIR)
    hu = (L.SPAWN_ROOM[0] + L.SPAWN_ROOM[1]) // 2         # the hatch over the spawn: a hut of iron and clay
    hy = max(ground(u, v) for u in range(hu - 3, hu + 4) for v in range(0, 4))
    for u in range(hu - 3, hu + 4):
        for v in range(0, 4):
            for y in range(L.SURFACE + 1, hy + 1):
                w.set(u, y, v, B.PACKED_ICE)
            for y in range(hy + 1, hy + 7):
                edge = abs(u - hu) == 3 or v == 3
                w.set(u, y, v, *((B.STAINED_CLAY, 9) if edge else (B.AIR, 0)))
            w.set(u, hy + 7, v, B.IRON_BLOCK)
            w.set(u, hy, v, B.DSLAB, 8)
            for y in range(hy + 8, hy + 10):
                w.set(u, y, v, B.AIR)
    for y in range(hy + 1, hy + 5):
        w.set(hu, y, 3, B.IRON_BLOCK)                     # its shut door
    mu, mv = -40, 30                                      # the mast, with its stays
    my = ground(mu, mv)
    for y in range(my + 1, my + 22):
        w.set(mu, y, mv, B.IRON_BARS)
    for y in (my + 10, my + 16, my + 21):
        for d in (-1, 1):
            w.set(mu + d, y, mv, B.IRON_BARS)
            w.set(mu, y, mv + d, B.IRON_BARS)
    w.set(mu, my + 22, mv, B.REDSTONE_BLOCK)
