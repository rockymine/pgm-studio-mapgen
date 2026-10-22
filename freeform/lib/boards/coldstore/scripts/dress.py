"""Coldstore's dressing, all of it in the faces of the rock or over the roof, so none of it is a ledge to stand on.

    alcoves(w)      the great door's alcove in the south wall at the islands' height, and the balcony at the vents'
    vault_door(w)   a round blast door in the west wall's face, its hinge on the north
    faces(w, k)     on every face of rock: pipes, valves, vent grates, screens, graffiti and fire extinguishers
    ceiling(w)      lamps in the roof and its fans: a round hole over the void with a blade fan and a cap
    drifts(w, k)    snow and ice blown in through the fans, lying on the islands; it grows back in a match
    surface(w)      the ice over the roof, the stacks over the fans, the hatch over the spawn and the mast

**The story is that the cold got in.** The bunker's fans drew the air of the ice field above it, and the snow came
with it: it lies in drifts on the islands, thickest under the fans, and the islands' drifts are the one ground a
blast can take away and the match gives back.
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


def ceiling(w):
    """Lamps in the roof's underside every eight blocks, and the fans."""
    for u in range(S.U0, 0):
        for v in range(0, S.V1 + 1):
            if u % 8 == 4 and v % 8 == 4 and w.id(u, L.CEIL, v) == B.AIR:
                w.set(u, L.ROOF[0], v, B.SEA_LANTERN)
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


def surface(w, seed=21):
    """The ice field over the roof and round the bunker, the drawn quarter's share of it: packed ice and snow rolling
    eight to twenty blocks deep over the roof, rock showing through, and past the walls the field falling away in
    cliffs of rock and ice to the world's floor, so the bunker's bedrock is nowhere seen; a shaft up from each fan to
    the sky, the spawn's hatch and a mast."""
    u0, v1 = L.X0, L.Z0 + L.SZ - 1
    nu, nv = -u0, v1 + 1
    big = noise.fbm((nu, nv), 30, 3, seed=seed)
    small = noise.fbm((nu, nv), 7, 2, seed=seed + 1)
    rock = noise.fbm((nu, nv), 9, 2, seed=seed + 2)        # rock showing through: knolls, not ridges
    edge = noise.fbm((nu, nv), 12, 2, seed=seed + 3)
    for i in range(nu):
        for j in range(nv):
            u, v = u0 + i, j
            t = L.SURFACE + 9 + int(round(7 * big[i, j] + 2 * small[i, j]))
            out = max(L.OUTER_U - u, v - L.OUTER_V, 0)       # how far past the bunker's walls
            if out:
                f = min(1.0, (out + 4 * edge[i, j]) / L.MARGIN)
                t = int(round(t - (t - 3) * f * f * (3 - 2 * f)))
                base = 0
            else:
                base = L.SURFACE
            for y in range(base, t + 1):
                w.set(u, y, v, B.STONE if y < t - 3 and out else B.PACKED_ICE)
            if rock[i, j] > 0.55:
                for y in range(max(base, t - 3), t + int((rock[i, j] - 0.55) * 18) + 1):
                    w.set(u, y, v, B.STONE, 5 if (u + v) % 3 else 0)
            elif big[i, j] + 0.6 * small[i, j] > -0.35:
                w.set(u, t, v, B.SNOW)
                if small[i, j] > -0.2:
                    w.set(u, t + 1, v, B.SNOW_LAYER, int(np.clip((small[i, j] + 0.2) * 7, 0, 6)))
    for cu, cv, r in L.FANS:                              # the shaft from the fan to the sky, its crown louvred
        top = L.SURFACE + 26
        for u in range(cu - 4, cu + 5):
            for v in range(cv - 4, cv + 5):
                d = math.hypot(u - cu, v - cv)
                for y in range(L.ROOF[1] + 1, top + 1):
                    if d <= L.SHAFT - 0.9:
                        w.set(u, y, v, B.AIR)
                    elif d <= L.SHAFT:
                        louvre = y > top - 4 and (y + int(math.degrees(math.atan2(v - cv, u - cu)) // 30)) % 2
                        w.set(u, y, v, B.IRON_BARS if louvre else B.IRON_BLOCK)
                if d <= L.SHAFT:
                    for y in range(top + 1, L.SY):
                        w.set(u, y, v, B.AIR)
    hu, hv = (L.SPAWN_ROOM[0] + L.SPAWN_ROOM[1]) // 2, 0  # the hatch over the spawn: a hut of iron and clay
    for u in range(hu - 3, hu + 4):
        for v in range(0, 4):
            for y in range(L.SURFACE + 5, L.SURFACE + 11):
                edge = abs(u - hu) == 3 or v == 3
                w.set(u, y, v, *((B.STAINED_CLAY, 9) if edge else (B.AIR, 0)))
            w.set(u, L.SURFACE + 11, v, B.IRON_BLOCK)
            w.set(u, L.SURFACE + 4, v, B.DSLAB, 8)
    for y in range(L.SURFACE + 5, L.SURFACE + 9):
        w.set(hu, y, 3, B.IRON_BLOCK)                     # its shut door
    mu, mv = -40, 30                                      # the mast, with its stays
    for y in range(L.SURFACE + 4, L.SURFACE + 26):
        w.set(mu, y, mv, B.IRON_BARS)
    for y in (L.SURFACE + 14, L.SURFACE + 20, L.SURFACE + 25):
        for d in (-1, 1):
            w.set(mu + d, y, mv, B.IRON_BARS)
            w.set(mu, y, mv + d, B.IRON_BARS)
    w.set(mu, L.SURFACE + 26, mv, B.REDSTONE_BLOCK)
