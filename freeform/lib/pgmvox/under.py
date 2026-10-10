"""Under the ground: caves, mines and shafts, carved into a built world.

    tunnel(w, [(x, floor_y, z, r), ...], ground=H)      # a cave passage with a level floor, under the surface
    chamber(w, cx, floor_y, cz, rx, h, ground=H)         # a hall in it
    dress_cave(w, box, ground=H, rng=r)                  # gravel and clay floors, stalactites, stalagmites, ore
    line = gallery_line([(x, y, z), ...])                # a mine's cells, its floor changing a block a step at most
    gallery(w, line, rng=r)                              # three wide and three high, timbered, railed, stepped
    shaft(w, x, z, bottom, top)                          # a ladder in a timber-lined well

**A cave passage is a tube held to a level floor.** The tube (`solid.tube`) gives it width and a rounded roof, and
everything below the floor interpolated along the passage is left solid, so a player walks a cave rather than
climbing the inside of a pipe. A carve never comes nearer the surface than `cover` blocks and never cuts into
water, so a tunnel under a river stays under it.

**A mine gallery is carved along a line whose floor changes a block at a time**, so every rise is one stair. Its
timber sets stand only where the floor is level, because a cap over a stair takes the headroom a player needs to
climb it; a rebuild found that only from its walk.

`ground` is the heights a carve keeps under: an array over the world's columns (H[x - x0, z - z0]), a function
(x, z) -> y, or None for no surface guard.
"""
import math

import numpy as np

from . import solid as S
from .blocks import B, PASSABLE
from .orient import ladder as ladder_data, stair as stair_data, torch as torch_data, vec
from .shapes import nearest_on

WATERS = (B.WATER, B.WATER_FLOW)


def _ground(w, ground):
    if ground is None:
        return lambda x, z: None
    if callable(ground):
        return ground

    def at(x, z):
        i, k = x - w.x0, z - w.z0
        if 0 <= i < ground.shape[0] and 0 <= k < ground.shape[1]:
            return int(ground[i, k])
        return None
    return at


def carve(w, cells, floor=None, ground=None, cover=3, keep=None):
    """Air in every (x, y, z) of `cells` at or over floor(x, z), never within `cover` blocks of the ground, never
    into water, never where keep(x, y, z) says. Returns how many were carved."""
    g = _ground(w, ground)
    n = 0
    for x, y, z in cells:
        if not w.inside(x, y, z) or (floor is not None and y < floor(x, z)):
            continue
        top = g(x, z)
        if top is not None and y > top - cover:
            continue
        if w.id(x, y, z) in WATERS or (keep is not None and keep(x, y, z)):
            continue
        w.set(x, y, z, B.AIR)
        n += 1
    return n


def tunnel(w, pts, ground=None, cover=3, keep=None, lift=0.45):
    """A cave passage through waypoints (x, floor_y, z, radius): a tube whose axis runs `lift` of the radius over
    the floor, carved only at or over the floor interpolated along the passage. Returns the blocks carved and the
    floor function, for whatever is laid on it next."""
    arc = np.concatenate([[0], np.cumsum([math.hypot(b[0] - a[0], b[2] - a[2]) for a, b in zip(pts, pts[1:])])])
    tube = S.tube([(x + 0.5, fy + lift * r, z + 0.5) for x, fy, z, r in pts], [p[3] for p in pts])
    plan = [(p[0], p[2]) for p in pts]

    def floor(x, z):
        return int(round(np.interp(nearest_on(plan, x, z)[1], arc, [p[1] for p in pts])))
    return carve(w, tube.cells(), floor, ground, cover, keep), floor


def chamber(w, cx, floor_y, cz, rx, h, rz=None, ground=None, cover=3, keep=None):
    """A hall: an ellipsoid rx across (rz the other way), h high, its floor level at floor_y."""
    e = S.ellipsoid(cx + 0.5, floor_y + 0.6 * h, cz + 0.5, rx, h, rz if rz is not None else rx * 0.9)
    return carve(w, e.cells(), lambda x, z: floor_y, ground, cover, keep)


def dress_cave(w, box, rng, ground=None, cover=2, keep=None, floors=((B.GRAVEL, 0), (B.STONE, 5), (B.CLAY, 0), (B.COBBLE, 0)),
               weights=(0.45, 0.25, 0.1, 0.2), mushrooms=0.015, stalactites=0.05, ores=300, stalagmites=900,
               ore_blocks=((B.COAL_ORE, 0.6), (B.IRON_ORE, 0.4))):
    """Finish every cave inside box (x0, x1, z0, z1, y0, y1): floors of gravel, andesite, clay and cobble, a
    mushroom here and there, stalactites hanging from the roof, `ores` tries at ore in the faces and `stalagmites`
    tries at a stalagmite against a wall. Only air at least `cover` under the ground is touched; a column with no
    ground is not under anything and is left alone, and keep(x, y, z) holds a block back."""
    x0, x1, z0, z1, y0, y1 = box
    g = _ground(w, ground)
    p = np.array(weights, float) / sum(weights)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            top = g(x, z)
            if top is None and ground is not None:
                continue
            hi = min(y1, top - cover) if top is not None else y1
            for y in range(max(2, y0), hi):
                if w.id(x, y, z) != B.AIR or (keep is not None and keep(x, y, z)):
                    continue
                below, above = w.id(x, y - 1, z), w.id(x, y + 1, z)
                if below in (B.STONE, B.COBBLE, B.DIRT):
                    w.set(x, y - 1, z, *floors[int(rng.choice(len(floors), p=p))])
                    if rng.random() < mushrooms:
                        w.set(x, y, z, B.BROWN_MUSHROOM if rng.random() < 0.6 else B.RED_MUSHROOM)
                if above == B.STONE and below == B.AIR and rng.random() < stalactites:
                    n = 1 + int(rng.random() * 2.5)
                    for k in range(n):
                        if w.id(x, y - k, z) == B.AIR and w.id(x, y - k - 1, z) == B.AIR:
                            w.set(x, y - k, z, B.STONE if k < n - 1 else B.COBBLE_WALL)
    for _ in range(ores):
        x, z, y = int(rng.integers(x0, x1 + 1)), int(rng.integers(z0, z1 + 1)), int(rng.integers(y0, y1))
        if (keep is None or not keep(x, y, z)) and w.id(x, y, z) == B.STONE and any(w.id(x + a, y + b, z + c) == B.AIR for a, b, c in
                                            ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0))):
            r, acc = rng.random(), 0.0
            for blk, share in ore_blocks:
                acc += share
                if r < acc:
                    w.set(x, y, z, blk)
                    break
    for _ in range(stalagmites):
        x, z, y = int(rng.integers(x0, x1 + 1)), int(rng.integers(z0, z1 + 1)), int(rng.integers(y0, y1))
        top = g(x, z)
        if (top is None and ground is not None) or (top is not None and y > top - cover - 1) \
                or w.id(x, y, z) != B.AIR or (keep is not None and keep(x, y, z)):
            continue
        if w.id(x, y - 1, z) not in (B.GRAVEL, B.STONE, B.CLAY, B.COBBLE):
            continue
        walls = sum(w.id(x + a, y, z + c) not in (B.AIR,) + WATERS for a, c in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if walls >= 1 and w.id(x, y + 1, z) == B.AIR and w.id(x, y + 2, z) == B.AIR:
            w.set(x, y, z, B.STONE, 5)
            if rng.random() < 0.5:
                w.set(x, y + 1, z, B.COBBLE_WALL)


def gallery_line(waypoints):
    """A mine's cells through waypoints (x, y, z): one a block in plan, the floor (y, the lowest air) changing at
    most one a step, so every rise is a stair."""
    path = []
    for (ax, ay, az), (bx, by, bz) in zip(waypoints, waypoints[1:]):
        n = int(max(abs(bx - ax), abs(bz - az))) or 1
        for i in range(n):
            t = i / n
            path.append((round(ax + (bx - ax) * t), ay + (by - ay) * t, round(az + (bz - az) * t)))
    path.append(waypoints[-1])
    clean = [(int(path[0][0]), int(path[0][1]), int(path[0][2]))]
    for x, y, z in path[1:]:
        if (x, z) == (clean[-1][0], clean[-1][2]):
            continue
        clean.append((int(x), clean[-1][1] + int(np.clip(round(y) - clean[-1][1], -1, 1)), int(z)))
    return clean


def gallery(w, line, rng, timber=(B.LOG, 1), fence=(B.SPRUCE_FENCE, 0), stair=B.COBBLE_STAIRS, every=4,
            rails=True, torches=12, floor=((B.GRAVEL, 0), (B.STONE, 0), (B.STONE, 5)), ore=(B.IRON_ORE, 0)):
    """A mine gallery along a gallery_line: three wide and three high, a rough floor, a timber set (posts, braces
    and a cap) every `every` cells where the floor is level, rails on the level runs, a stair at every rise,
    a torch every `torches` cells, and ore in the walls. Returns the cells carved along."""
    room = set()
    for x, y, z in line:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dy in (0, 1, 2):
                    w.set(x + dx, y + dy, z + dz, B.AIR)
                    room.add((x + dx, y + dy, z + dz))
    for x, y, z in line:                                        # floors after the carve: a floor laid cell by cell
        for dx in (-1, 0, 1):                                   # filled the last cell's feet before every rise
            for dz in (-1, 0, 1):                               # and left no place for its stair
                if (x + dx, y - 1, z + dz) not in room:
                    w.set(x + dx, y - 1, z + dz, *floor[int(rng.integers(len(floor)))])
    for i, (x, y, z) in enumerate(line):
        nxt, prv = line[min(i + 1, len(line) - 1)], line[max(i - 1, 0)]
        along_x = abs(nxt[0] - prv[0]) >= abs(nxt[2] - prv[2])
        step = None
        if nxt[1] > y and i + 1 < len(line):
            step = (nxt[0] - x, nxt[2] - z)
        elif prv[1] > y and i > 0:
            step = (prv[0] - x, prv[2] - z)
        level = nxt[1] == y and prv[1] == y
        if step is not None and step != (0, 0):
            for k in (-1, 0, 1):
                ox, oz = (0, k) if along_x else (k, 0)
                if w.id(x + ox, y, z + oz) == B.AIR:
                    w.set(x + ox, y, z + oz, stair, stair_data(vec(step)))
        elif level and rails and w.id(x, y, z) == B.AIR:
            w.set(x, y, z, B.RAIL, 1 if along_x else 0)
        if i % every == every // 2 and level:                  # a set only on the level: over a stair, its cap
            for k in (-1, 1):                                   # would take the climb's headroom
                ox, oz = (0, k * 2) if along_x else (k * 2, 0)
                for dy in (0, 1, 2):
                    if w.id(x + ox, y + dy, z + oz) != B.AIR:
                        w.set(x + ox, y + dy, z + oz, *timber)
                for dy in (0, 1):
                    if w.id(x + ox // 2, y + dy, z + oz // 2) in (B.AIR, B.RAIL):
                        w.set(x + ox // 2, y + dy, z + oz // 2, *fence)
            for k in (-1, 0, 1):
                ox, oz = (0, k) if along_x else (k, 0)
                w.set(x + ox, y + 2, z + oz, timber[0], (timber[1] & 3) | (4 if along_x else 8))
            if torches and i % torches == every // 2:
                tx, tz = (x, z + 1) if along_x else (x + 1, z)
                if w.id(tx, y + 1, tz) == B.AIR:
                    w.set(tx, y + 1, tz, B.TORCH, torch_data("s" if along_x else "e"))
    if ore:
        for x, y, z in line[::2]:
            for _ in range(3):
                ox, oy, oz = int(rng.integers(-2, 3)), int(rng.integers(0, 3)), int(rng.integers(-2, 3))
                if w.id(x + ox, y + oy, z + oz) == B.STONE:
                    w.set(x + ox, y + oy, z + oz, *ore)
    return line


def shaft(w, x, z, bottom, top, wall=(B.PLANKS, 1), post=(B.LOG, 1), ladder_on="s", foot=3):
    """A shaft from the floor at `bottom` up to `top`: a three-by-three well, logs at its corners, planks between,
    and a ladder on its `ladder_on` wall with a plank under its foot. In its lowest `foot` courses the lining is
    left off wherever the cell is already open (air, a rail), so a gallery carved first runs into the well instead of ending
    at a wall; a test walk found that wall."""
    dx_, dz_ = vec(ladder_on)
    for y in range(bottom, top + 1):
        def line(ox, oz, blk):
            if y < bottom + foot and w.id(x + ox, y, z + oz) in PASSABLE:
                return
            w.set(x + ox, y, z + oz, *blk)
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                w.set(x + dx, y, z + dz, B.AIR)
        for ox, oz in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
            line(ox, oz, post)
        for d in (-1, 0, 1):
            for ox, oz in ((d, -2), (d, 2), (-2, d), (2, d)):
                line(ox, oz, wall)
        w.set(x + dx_, y, z + dz_, B.LADDER, ladder_data(ladder_on))
    w.set(x + dx_, bottom - 1, z + dz_, *wall)


def bore(w, at, r, y0, y1, seed=0, r_noise=0.0, fill=(B.AIR, 0), lip=None):
    """A round hole straight through rock: every column within r of `at` (x, z), the radius jittered by `r_noise`
    blocks drawn from seed, emptied (or filled with `fill`) from y0 to y1, so lava let out above falls through it.
    `lip` (y, block) rings it at y. Returns the columns it opened."""
    rng = np.random.default_rng(seed)
    cx, cz = at
    opened = []
    for x in range(int(cx - r - 1), int(cx + r + 2)):
        for z in range(int(cz - r - 1), int(cz + r + 2)):
            d = math.hypot(x - cx, z - cz)
            if d < r + r_noise * rng.standard_normal():
                for y in range(y0, y1 + 1):
                    w.set(x, y, z, *fill)
                opened.append((x, z))
            elif lip is not None and d < r + 1.5:
                w.set(x, lip[0], z, *lip[1])
    return opened

