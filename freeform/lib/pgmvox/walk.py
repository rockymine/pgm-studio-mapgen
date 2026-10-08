"""The walk over built blocks, and the checks a board reads back from them.

From a set of starting places, how far is every place a player can stand, on foot, placing no blocks? The rules
are a MoveRules: a step climbs one block (with headroom over the player, the check generation 1 lost); a player
drops off any edge to whatever is below, up to `max_drop` (None for any, as with fall damage off); running jumps
clear gaps of one to `max_gap` blocks landing at most one higher; ladders, vines and water lift a player up.

    st, grid = standing(ids)                      # where a player can stand
    dist = walk(ids, starts, x0, z0, rules)       # moves to every standing place, -1 where unreached

The checks:

    no_stand_above(w, y, inside, allowed)   columns inside a region with anything standable above y but what is allowed
    catchers(w, course, margin, y_top, y_kill)  blocks beside a course a falling player could land on
    unreached(dist, cells)                  the cells of a list nobody reaches
    nearest(dist, x0, z0, x, y, z, r)       moves to the nearest reached place by a point

This is a stopgap the repository's rule allows for a world that is not a stored map: the studio's own walk reads
a stored map; when it can read an uploaded region folder, these reads belong there.
"""
from collections import deque
from dataclasses import dataclass

import numpy as np

from . import blocks as K
from .move import jump_reach


@dataclass
class MoveRules:
    max_drop: int | None = None          # None: any drop (fall damage off); else the most a walk drops
    jumps: bool = True                   # running jumps over gaps
    max_gap: int = 3                     # the widest gap a running jump clears
    climb: bool = True                   # ladders, vines and water lift a player


def classes(ids):
    """passable, water, climbable and solid masks over an id volume."""
    passable = K.mask(ids, K.PASSABLE)
    water = K.mask(ids, {K.B.WATER, K.B.WATER_FLOW})
    climb = K.mask(ids, K.CLIMBABLE)
    return passable, water, climb, ~passable


def standing(ids):
    """A cell a player can occupy: two passable cells high, with solid ground or water under or in it."""
    passable, water, climb, solid = classes(ids)
    st = np.zeros_like(passable)
    st[:, 1:-1, :] = passable[:, 1:-1, :] & passable[:, 2:, :] & (solid[:, :-2, :] | water[:, 1:-1, :] | water[:, :-2, :])
    return st, (passable, water, climb, solid)


def _jump_offsets(max_gap):
    return [(dx, dz) for dx in range(-max_gap - 1, max_gap + 2) for dz in range(-max_gap - 1, max_gap + 2)
            if 1 <= ((max(abs(dx) - 1, 0)) ** 2 + (max(abs(dz) - 1, 0)) ** 2) ** 0.5 <= max_gap]


def walk(ids, starts, x0, z0, rules=None):
    """Moves to every standing place from the starts (world (x, y, z) of the feet), -1 where unreached."""
    rules = rules or MoveRules()
    st, (passable, water, climb, solid) = standing(ids)
    sx, sy, sz = st.shape
    dist = np.full(st.shape, -1, np.int32)
    q = deque()
    for (x, y, z) in starts:
        i = (x - x0, y, z - z0)
        if 0 <= i[0] < sx and 0 <= i[2] < sz and st[i]:
            dist[i] = 0
            q.append(i)
    jumps = _jump_offsets(rules.max_gap) if rules.jumps else []

    def push(i, d):
        if dist[i] < 0:
            dist[i] = d
            q.append(i)
    while q:
        x, y, z = q.popleft()
        d = dist[x, y, z] + 1
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if not (0 <= nx < sx and 0 <= nz < sz):
                continue
            if y + 2 < sy and st[nx, y + 1, nz] and passable[x, y + 2, z]:
                push((nx, y + 1, nz), d)                         # a step up, with headroom to jump it
            if st[nx, y, nz]:
                push((nx, y, nz), d)
                continue
            if not (passable[nx, y, nz] and passable[nx, y + 1, nz]):
                continue
            for ny in range(y - 1, 0, -1):                       # off the edge: fall to whatever is below
                if rules.max_drop is not None and y - ny > rules.max_drop:
                    break
                if not passable[nx, ny, nz]:
                    break
                if st[nx, ny, nz]:
                    push((nx, ny, nz), d)
                    break
        for dx, dz in jumps:                                     # a running jump over a gap, at most one up
            nx, nz = x + dx, z + dz
            if not (0 <= nx < sx and 0 <= nz < sz) or y + 3 >= sy:
                continue
            n = max(abs(dx), abs(dz)) * 3
            line = {(x + round(dx * s / n), z + round(dz * s / n)) for s in range(1, n)} - {(x, z), (nx, nz)}
            if not line or any(st[a, y, b] or st[a, y + 1, b] for a, b in line):
                continue                                         # not a gap: the ground runs on
            if not all(passable[a, y + 1, b] and passable[a, y + 2, b] for a, b in line):
                continue
            for ny in (y + 1, y):
                if st[nx, ny, nz]:
                    push((nx, ny, nz), d + max(abs(dx), abs(dz)))
                    break
        if rules.climb:
            for dy in (1, -1):                                   # ladders, vines and water lift a player
                ny = y + dy
                if 1 <= ny < sy - 1 and (climb[x, ny, z] or climb[x, y, z] or water[x, ny, z]) and \
                        (st[x, ny, z] or climb[x, ny, z]):
                    push((x, ny, z), d)
    return dist


def nearest(dist, x0, z0, x, y, z, r=1):
    """Moves to the nearest reached place within r blocks (and one up or down) of (x, y, z), or None."""
    best = None
    for dx in range(-r, r + 1):
        for dz in range(-r, r + 1):
            for dy in range(-1, 2):
                i = (x + dx - x0, y + dy, z + dz - z0)
                if 0 <= i[0] < dist.shape[0] and 0 <= i[2] < dist.shape[2] and 0 <= i[1] < dist.shape[1] and dist[i] >= 0:
                    if best is None or dist[i] < best:
                        best = int(dist[i])
    return best


def unreached(dist, x0, z0, cells):
    """The (x, y, z) feet positions of a list nobody reaches."""
    return [c for c in cells if nearest(dist, x0, z0, *c, r=0) is None]


def no_stand_above(w, y, inside, allowed=None):
    """Columns inside a region (a boolean (sx, sz) mask, or a function (X, Z) -> mask) with anything a player
    could stand on above height y, other than where `allowed` (same shape) is True: the places a knocked or
    falling player could land and wait out the match."""
    X, Z = w.grid()
    region = inside(X, Z) if callable(inside) else inside
    st, _ = standing(w.ids)
    high = st[:, y + 1:, :].any(axis=1)
    bad = high & region
    if allowed is not None:
        bad &= ~(allowed(X, Z) if callable(allowed) else allowed)
    return [(int(X[i, k]), int(Z[i, k])) for i, k in np.argwhere(bad)]


def catchers(w, course, margin, y_top, y_kill):
    """Blocks beside a course that a player falling off its edges could land on: anything solid in the columns
    within `margin` of the course (but not under it), between the kill height and the course's top. course is a
    boolean (sx, sz) mask of the columns the course covers; returns [(x, y, z)]."""
    from scipy import ndimage
    near = ndimage.binary_dilation(course, iterations=margin) & ~course
    _, (passable, *_rest) = standing(w.ids)
    solid = ~passable[:, y_kill + 1:y_top + 1, :]
    hits = np.argwhere(solid & near[:, None, :])
    return [(int(i + w.x0), int(y + y_kill + 1), int(k + w.z0)) for i, y, k in hits]


def gap_cleared(gap, rise=0):
    """Whether a running sprint jump clears a gap of `gap` blocks landing `rise` higher (the player's 0.6 width
    counted): the same rule the plan walk uses, so the plan and the built world agree."""
    return gap <= jump_reach(rise) - 0.6
