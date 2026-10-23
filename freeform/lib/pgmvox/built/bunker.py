"""A bunker plan (`plan.bunker`) laid in blocks: rock and pillars of bedrock under a skin of stone brick, islands
standing in the void, a roof over all of it, each wool room sealed behind an end stone capsule on the void, each
spawn a hall cut into the rock, and the plan's defence walls from the floor to the roof.

    got = bunker.lay(w, b)                        # b from plan.bunker.draw
    got.spawns, got.rooms, got.islands, got.blocks

**Nothing a player sees is a ledge.** The skin is one block laid on bedrock, so a wall has nothing to hide in; the
pipes, screens, vents and graffiti of `dress` are in the skin's own plane. The plinth at an island's foot and the
cornice under the roof stand a block proud, as the concept's do.

**A wool room is sealed from its face inward.** From the face on the void: a glass case, a capsule of end stone up
to ten deep with rounded ends, a gap, a screen of panes, and the room, three deep and six across. The capsule is the
seal; its glass case runs back along both its sides, so it can be seen from either flank.
"""
import math
from dataclasses import dataclass, field

import numpy as np

from pgmvox.core.blocks import B
from pgmvox.plan.bunker import ISLAND, PILLAR, ROCK, VOID
from pgmvox.play.objectives import Box

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclass
class Heights:
    floor: int = 7                   # an island's underside and the rock's foot; below, the void to the world's floor
    top: int = 17                    # an island's top block: players stand at y 18
    plinth: tuple = (9, 10)
    ceil: int = 41                   # the last air under the roof
    roof: tuple = (42, 48)
    room: int = 27                   # a wool room's floor; its air y 28 to 31


SKIN = (B.STONEBRICK, 0)
STRIPES = {12: (B.STAINED_CLAY, 9), 13: (B.SANDSTONE, 2), 37: (B.SANDSTONE, 2), 38: (B.STAINED_CLAY, 9)}
DECK = (B.DSLAB, 8)
SCREEN = (B.STAINED_PANE, 3)
CASE = (B.STAINED_GLASS, 3)


@dataclass
class Laid:
    blocks: np.ndarray               # the plan's kind at every block column, indexed from (x0, z0)
    x0: int
    z0: int
    spawns: list = field(default_factory=list)     # [dict(k, at, yaw, area, slots)]
    rooms: list = field(default_factory=list)      # [dict(k, wool, room, found, seal, case, door, face)]
    islands: list = field(default_factory=list)    # [Box] of each island's deck and the air over it


def raster(b):
    """The plan at block scale: a kind a block column, and its corner's block coordinates."""
    n = b.cell
    return np.repeat(np.repeat(b.kind, n, 0), n, 1), b.x0 * n, b.z0 * n


def _spread(mask, r):
    """The mask grown by r blocks, square."""
    out = mask.copy()
    for _ in range(r):
        g = out.copy()
        g[1:, :] |= out[:-1, :]
        g[:-1, :] |= out[1:, :]
        g[:, 1:] |= out[:, :-1]
        g[:, :-1] |= out[:, 1:]
        out = g
    return out


def lay(w, b, h=None, seal_depth=10, wall_depth=24):
    h = h or Heights()
    blk, x0, z0 = raster(b)
    got = Laid(blk, x0, z0)

    def kind(x, z):
        i, j = x - x0, z - z0
        if 0 <= i < blk.shape[0] and 0 <= j < blk.shape[1]:
            return int(blk[i, j])
        return ROCK
    hall = blk != ROCK
    deep = _spread(hall, wall_depth)              # rock farther than this from the hall is left out: nobody sees it
    for i, j in np.ndindex(*blk.shape):
        x, z = i + x0, j + z0
        k = blk[i, j]
        if k == ROCK and not deep[i, j]:
            continue
        if k in (ROCK, PILLAR):
            w.column(x, z, h.floor, h.roof[1], B.BEDROCK)
            if any(kind(x + dx, z + dz) not in (ROCK, PILLAR) for dx, dz in DIRS):
                for y in range(h.plinth[1] + 1, h.roof[0]):
                    w.set(x, y, z, *STRIPES.get(y, SKIN))
        else:
            if k == ISLAND:
                w.column(x, z, h.floor, h.floor + 1, B.BEDROCK)
                w.column(x, z, h.floor + 2, h.top - 1, B.STONE)
                w.set(x, h.top, z, *DECK)
                if any(kind(x + dx, z + dz) == VOID for dx, dz in DIRS):
                    for y in range(h.plinth[1] + 1, h.top):
                        w.set(x, y, z, *STRIPES.get(y, SKIN))
            else:
                near = [kind(x + dx, z + dz) for dx, dz in DIRS]
                if any(n != VOID for n in near):
                    w.column(x, z, h.floor, h.floor + 1, B.BEDROCK)
                    w.column(x, z, *h.plinth, B.STONE)
                if any(n in (ROCK, PILLAR) for n in near):
                    w.column(x, z, h.ceil - 1, h.ceil, B.STONE)
            w.column(x, z, h.roof[0], h.roof[1], B.BEDROCK)
    for p, q in b.walls:
        wall(w, b, p, q, h)
    for s in b.spawns:
        got.spawns.append(spawn(w, b, s, h))
    for r in b.rooms:
        got.rooms.append(room(w, b, r, h, seal_depth))
    for comp in b.islands:
        xs = [c[0] for c in comp]
        zs = [c[1] for c in comp]
        got.islands.append(Box(min(xs) * b.cell, h.top + 1, min(zs) * b.cell, (max(xs) + 1) * b.cell - 1, h.top + 4,
                               (max(zs) + 1) * b.cell - 1))
    return got


def _cells_box(cells, n):
    xs = [c[0] for c in cells]
    zs = [c[1] for c in cells]
    return min(xs) * n, min(zs) * n, (max(xs) + 1) * n - 1, (max(zs) + 1) * n - 1


def _frame(box, face):
    """A rectangle of blocks seen from its face: the depth axis inward from the face, the lateral axis across it.
    Returns (depth, width, at(a, l) -> (x, z))."""
    bx0, bz0, bx1, bz1 = box
    dx, dz = face
    if dx:
        depth, width = bx1 - bx0 + 1, bz1 - bz0 + 1
        edge = bx1 if dx > 0 else bx0
        return depth, width, lambda a, l: (edge - dx * a, bz0 + l)
    depth, width = bz1 - bz0 + 1, bx1 - bx0 + 1
    edge = bz1 if dz > 0 else bz0
    return depth, width, lambda a, l: (bx0 + l, edge - dz * a)


def wall(w, b, p, q, h):
    """A defence wall on the seam between cells p and q: one block of bedrock on p's edge, floor to roof, skinned."""
    n = b.cell
    d = (q[0] - p[0], q[1] - p[1])
    _, width, at = _frame((p[0] * n, p[1] * n, (p[0] + 1) * n - 1, (p[1] + 1) * n - 1), d)
    for l in range(width):
        x, z = at(0, l)
        w.column(x, z, h.floor, h.roof[1], B.BEDROCK)
        for y in range(h.plinth[1] + 1, h.roof[0]):
            w.set(x, y, z, *STRIPES.get(y, SKIN))


def spawn(w, b, s, h):
    """A spawn hall cut in the rock: its walls a block thick, its floor the islands' height, an opening six wide on
    its face."""
    bx0, bz0, bx1, bz1 = _cells_box(s["cells"], b.cell)
    depth, width, at = _frame((bx0, bz0, bx1, bz1), s["face"])
    for a in range(depth):
        for l in range(width):
            x, z = at(a, l)
            inside = 0 < l < width - 1 and a < depth - 1
            w.set(x, h.top, z, *DECK)
            for y in range(h.top + 1, h.top + 8):
                w.set(x, y, z, *(((B.AIR, 0) if y < h.top + 7 else (B.SEA_LANTERN, 0)) if inside else SKIN))
    mid = width // 2
    for l in range(mid - 3, mid + 3):
        x, z = at(0, l)
        for y in range(h.top + 1, h.top + 5):
            w.set(x, y, z, B.AIR)
    cx, cz = at(depth // 2, mid)
    yaw = {(1, 0): -90, (-1, 0): 90, (0, 1): 0, (0, -1): 180}[s["face"]]
    a0, l0 = at(depth - 2, 1), at(1, width - 2)
    area = Box(min(a0[0], l0[0]), h.top + 1, min(a0[1], l0[1]), max(a0[0], l0[0]), h.top + 6, max(a0[1], l0[1]))
    slots = []
    for l in (mid - 4, mid + 3):                  # two wool monuments on the island just outside the door
        x, z = at(-4, l)
        slots.append((x, h.top + 1, z))
    return dict(k=s["k"], at=(cx, h.top + 1, cz), yaw=yaw, area=area, slots=slots)


def room(w, b, r, h, seal_depth):
    """A wool room and its seal, laid inward from the room block's face. The block reaches back into the rock
    behind the room's cells as far as the seal needs."""
    n = b.cell
    bx0, bz0, bx1, bz1 = _cells_box(r["cells"], n)
    dx, dz = r["face"]
    back = 2 * n                                  # the rock behind the room's cells it may cut into
    if dx > 0:
        bx0 -= back
    elif dx < 0:
        bx1 += back
    elif dz > 0:
        bz0 -= back
    else:
        bz1 += back
    depth, width, at = _frame((bx0, bz0, bx1, bz1), r["face"])
    cap = max(4, min(seal_depth, depth - 7))
    mid = width // 2
    lat = range(mid - 3, mid + 3)                 # the room's and the capsule's six across
    f = h.room
    y0, y1 = f - 2, f + 8                         # the capsule's height: eleven, rounded at its ends
    seal, case, door = [], [], []
    for a in range(1, cap + 7):                   # behind the face, the block is bedrock round all of it
        for l in range(mid - 6, mid + 6):
            x, z = at(a, l)
            for y in range(y0 - 1, y1 + 2):
                w.set(x, y, z, B.BEDROCK)
    for a in range(1, cap + 1):                   # the capsule, deepest at its middle height
        for y in range(y0, y1 + 1):
            t = abs(y - (y0 + y1) / 2) / ((y1 - y0) / 2 + 0.5)
            if a > round(cap * math.sqrt(max(0.0, 1 - t ** 4))):
                continue
            for l in lat:
                x, z = at(a, l)
                w.set(x, y, z, B.END_STONE)
                seal.append((x, y, z))
    for y in range(y0 - 1, y1 + 2):               # the case: its face on the void and two layers down each side
        for l in range(mid - 5, mid + 5):
            x, z = at(0, l)
            w.set(x, y, z, *CASE)
            case.append((x, y, z))
        for a in range(1, cap + 1):
            for l in (mid - 5, mid - 4, mid + 3, mid + 4):
                x, z = at(a, l)
                w.set(x, y, z, *CASE)
                case.append((x, y, z))
    for l in lat:                                 # the gap, the screen, the room
        for y in range(f + 1, f + 5):
            x, z = at(cap + 1, l)
            w.set(x, y, z, B.AIR)
            x, z = at(cap + 2, l)
            w.set(x, y, z, *SCREEN)
            if l in (mid - 1, mid):
                door.append((x, y, z))
        for a in range(cap + 3, cap + 6):
            x, z = at(a, l)
            w.set(x, f, z, *DECK)
            for y in range(f + 1, f + 5):
                w.set(x, y, z, B.AIR)
    fx, fz = at(cap + 4, mid)
    ra, rb = at(cap + 3, mid - 3), at(cap + 5, mid + 2)
    room_box = Box(min(ra[0], rb[0]), f + 1, min(ra[1], rb[1]), max(ra[0], rb[0]), f + 4, max(ra[1], rb[1]))
    xs, ys, zs = zip(*seal)
    return dict(k=r["k"], wool=r["wool"], room=room_box, found=(fx, f + 1, fz), seal=seal, case=case, door=door,
                seal_box=Box(min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)), face=r["face"],
                face_at=at(-1, mid))


SPRAY = ((1, 4), (2, 6), (3, 11), (5, 13), (14, 1))     # a graffiti blot's rim and its middle, in stained clay


def dress(w, got, h=None, seed=5, clear=()):
    """The bunker's dressing, all of it in the skin's plane or the roof: two pipes round every face of rock at y 29
    and 30 with valves and joints, graffiti low on the faces, vent grates, screens and fire extinguishers, lamps in
    the roof every eight blocks, and snow on the islands, never within three blocks of a point in `clear`."""
    from pgmvox.geom import noise
    h = h or Heights()
    rng = np.random.default_rng(seed)
    blk, x0, z0 = got.blocks, got.x0, got.z0
    solid = (blk == ROCK) | (blk == PILLAR)
    blots = noise.fbm((400, 12), 3, 2, seed=seed)
    paint = noise.fbm((400, 12), 9, 1, seed=seed + 1)
    for i, j in np.argwhere(solid):
        x, z = int(i) + x0, int(j) + z0
        out = [(dx, dz) for dx, dz in DIRS if 0 <= i + dx < blk.shape[0] and 0 <= j + dz < blk.shape[1]
               and not solid[i + dx, j + dz]]
        if not out or w.id(x, 30, z) != B.STONEBRICK:
            continue
        along = z if out[0][0] else x
        if w.id(x, 29, z) == B.STONEBRICK:
            run = 3 if out[0][0] == 0 else 4
            w.set(x, 29, z, B.QUARTZ, run)
            w.set(x, 30, z, B.QUARTZ, run)
            if along % 11 == 0:
                w.set(x, 29, z, B.WOOL, 14)
            if along % 11 == 1:
                w.set(x, 30, z, B.IRON_BLOCK)
        g, c = blots[(x - z) % 400], paint[(x - z) % 400]
        for y in range(h.top + 2, h.top + 9):
            if g[y - h.top] > 0.25 and w.id(x, y, z) == B.STONEBRICK:
                tones = SPRAY[int((c[y - h.top] + 1) * 2.5) % len(SPRAY)]
                w.set(x, y, z, B.STAINED_CLAY, tones[1] if g[y - h.top] > 0.5 else tones[0])
        if along % 17 == 3:
            for y in (32, 33):
                w.set(x, y, z, B.IRON_BARS)
                dx, dz = out[0]
                if w.id(x - dx, y, z - dz) == B.BEDROCK:
                    w.set(x - dx, y, z - dz, B.COAL_BLOCK)
        if along % 23 == 9 and w.id(x, 22, z) == B.STONEBRICK:
            for y in range(21, 25):
                w.set(x, y, z, B.STAINED_CLAY, 15)
            w.set(x, 22, z, B.STAINED_CLAY, int(rng.choice([5, 9, 13])))
            w.set(x, 23, z, B.STAINED_CLAY, int(rng.choice([5, 9, 3])))
        if along % 29 == 14 and w.id(x, h.top + 2, z) in (B.STONEBRICK, B.STAINED_CLAY):
            w.set(x, h.top + 2, z, B.WOOL, 14)
            w.set(x, h.top + 3, z, B.WOOL, 14)
            w.set(x, h.top + 4, z, B.COAL_BLOCK)
    for i, j in np.argwhere(~solid):
        x, z = int(i) + x0, int(j) + z0
        if x % 8 == 4 and z % 8 == 4 and w.id(x, h.ceil, z) == 0:
            w.set(x, h.roof[0], z, B.SEA_LANTERN)
    n = noise.fbm(blk.shape, 6, 3, seed=seed + 2)
    for i, j in np.argwhere(blk == ISLAND):
        x, z = int(i) + x0, int(j) + z0
        if w.id(x, h.top + 1, z) != 0 or any(abs(x - p[0]) <= 3 and abs(z - p[2]) <= 3 for p in clear):
            continue
        wall = any(solid[min(max(i + dx * s, 0), blk.shape[0] - 1), min(max(j + dz * s, 0), blk.shape[1] - 1)]
                   for dx, dz in DIRS for s in (1, 2))
        depth = n[i, j] * 1.8 + (0.8 if wall else 0.0)
        if depth > 1.3:
            w.set(x, h.top + 1, z, B.PACKED_ICE if rng.random() < 0.25 else B.SNOW)
            w.set(x, h.top + 2, z, B.SNOW_LAYER, int(rng.integers(0, 4)))
        elif depth > 0.5:
            w.set(x, h.top + 1, z, B.SNOW_LAYER, int(rng.integers(0, 2)))
