"""The Rime Rotunda: the ice core on its terrace at 72 over a ring of broken columns, and the Blue Cave under it, a passage up from the
Mirror's shore to a hall and an undercroft whose roof is the plaza's floor. The core stands exposed in the open with nothing within
seven blocks of it; the approaches differ: over the glacier's ledge from above, up the cave from below, across the open terrace from
the Frost Gate, and over the Mirror's ice.
"""
import math

import numpy as np

import land
import plan as P
from pgmvox import B
from pgmvox.volume import under
from pgmvox.geom import noise
from util import disc, line_cells, pick, stairs

CX, CZ = land.RIME
Y = land.RIME_LEVEL

FLAG = [((B.STONEBRICK, 0), 6), ((B.STONE, 6), 4), ((B.STONEBRICK, 2), 2)]


def plaza(w, rng):
    """The plaza's floor in rings of one cool tone, the core's footprint kept as stone under it."""
    for x, z, d in disc(CX, CZ, 12.5):
        if d > 10.4 + rng.uniform(-0.2, 1.4):
            continue
        h = P.g(x, z)
        for yy in range(min(h, Y) - 1, Y):
            w.set(x, yy, z, B.STONE, 0)
        for yy in range(Y + 1, max(h, Y) + 3):
            w.set(x, yy, z, B.AIR)
        m = max(abs(x - CX), abs(z - CZ))
        if m <= 2:
            blk = (B.PRISMARINE, 2) if (x + z) % 2 else (B.PRISMARINE, 1)       # the foot of the core: dark prismarine in a checker
        elif m == 3:
            blk = (B.QUARTZ, 1)
        elif d < 6.2:
            blk = pick(rng, FLAG)
        elif d < 7.0:
            blk = (B.QUARTZ, 0)
        elif d < 9.6:
            blk = pick(rng, [((B.STONEBRICK, 0), 5), ((B.STONE, 5), 3), ((B.STONEBRICK, 2), 2), ((B.STONE, 6), 2)])
        else:
            blk = pick(rng, [((B.STONEBRICK, 2), 3), ((B.COBBLE, 0), 2), ((B.STONE, 5), 3), ((B.GRAVEL, 0), 1)])
        w.set(x, Y, z, *blk)


def colonnade(w, rng):
    """Eight columns of quartz round the plaza at radius 9.4, some whole, some broken, lintels between the standing pairs."""
    tops = {}
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        x, z = CX + round(9.4 * math.cos(a)), CZ + round(9.4 * math.sin(a))
        h = [8, 8, 8, 5, 8, 3, 8, 7][k]
        base = P.g(x, z)
        for yy in range(min(base, Y), Y + 1):
            w.set(x, yy, z, B.STONEBRICK, 3)
        w.set(x, Y + 1, z, B.STONEBRICK, 3)
        for yy in range(Y + 2, Y + h):
            w.set(x, yy, z, B.QUARTZ, 2)
        if h >= 8:
            w.set(x, Y + h, z, B.QUARTZ, 1)
            w.set(x, Y + h + 1, z, B.SLAB, 7)
            tops[k] = (x, z, Y + h + 1)
        else:
            w.set(x, Y + h, z, B.QUARTZ, 2)
            if h == 5:
                for dx, dz in ((1, 0), (0, 1), (-1, 0)):
                    if rng.random() < 0.6:
                        w.set(x + dx, Y + 1, z + dz, B.QUARTZ, 0)         # a fallen drum beside the stump
    for k in range(8):
        a, b = tops.get(k), tops.get((k + 1) % 8)
        if not a or not b or rng.random() < 0.28:
            continue
        cells = line_cells((a[0], a[1]), (b[0], b[1]))
        for j, (x, z) in enumerate(cells[1:-1]):
            y = a[2] + (1 if 0.2 < (j + 1) / len(cells) < 0.8 else 0)
            w.set(x, y - 1, z, B.STONEBRICK, 0)
            if j % 3 == 1 and rng.random() < 0.8:
                for k2 in range(1, 1 + int(rng.integers(1, 4))):
                    w.set(x, y - 1 - k2, z, B.ICE if k2 == 1 else B.PACKED_ICE)


def frost_gate(w):
    """A standing gate on the road a dozen blocks south of the plaza: two piers, a lintel, a lantern hung under it."""
    gz = CZ + 14
    for gx in (CX - 4, CX + 4):
        base = P.g(gx, gz)
        for yy in range(base, base + 9):
            w.set(gx, yy, gz, B.STONEBRICK, 3 if yy == base + 1 else 0)
            w.set(gx, yy, gz + 1, B.STONEBRICK, 0)
            w.set(gx, yy, gz - 1, B.STONEBRICK, 0)
        w.set(gx, base + 9, gz, B.QUARTZ, 1)
    top = P.g(CX, gz) + 9
    for gx in range(CX - 4, CX + 5):
        for dz in (-1, 0, 1):
            w.set(gx, top, gz + dz, B.STONEBRICK, 0)
        w.set(gx, top + 1, gz, B.SLAB, 5)
    w.set(CX, top - 1, gz, B.SEA_LANTERN)
    for gx in (CX - 3, CX + 3):
        w.set(gx, top - 1, gz, B.STONEBRICK_STAIRS, 3 | 4)


def cave_skin(w, before, rng):
    """After a carve: every wall, floor and roof the cave touches becomes ice-tone rock, with lanterns in the roof, hanging ice and standing."""
    carved = (before != 0) & (w.ids == 0)
    pts = np.argwhere(carved)
    solid = lambda a, y, c: 0 <= a < w.sx and 0 <= y < w.sy and 0 <= c < w.sz and w.ids[a, y, c] != 0 and not carved[a, y, c] \
        and w.ids[a, y, c] not in (B.WATER, B.LAVA, B.ICE)
    for a, y, c in pts:
        for da, dy, dc in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0)):
            na, ny, nc = a + da, y + dy, c + dc
            if solid(na, ny, nc):
                if dy == 1 and rng.random() < 0.06:
                    w.ids[na, ny, nc], w.dat[na, ny, nc] = B.SEA_LANTERN, 0
                elif dy == -1:
                    w.ids[na, ny, nc], w.dat[na, ny, nc] = pick(rng, [((B.STONE, 6), 3), ((B.PACKED_ICE, 0), 4), ((B.STONE, 5), 3), ((B.SNOW, 0), 2)])
                else:
                    w.ids[na, ny, nc], w.dat[na, ny, nc] = pick(rng, [((B.PACKED_ICE, 0), 6), ((B.STONE, 5), 2), ((B.ICE, 0), 2), ((B.SNOW, 0), 1)])
    for a, y, c in pts:
        if w.ids[a, y + 1, c] != 0 and w.ids[a, y, c] == 0 and rng.random() < 0.09 and not carved[a, y + 1, c]:
            for j in range(int(rng.integers(1, 4))):
                if w.ids[a, y - j, c] == 0:
                    w.ids[a, y - j, c], w.dat[a, y - j, c] = (B.ICE if j == 0 else B.PACKED_ICE), 0


def cave(w, rng, stats):
    """The Blue Cave: a mouth in the Mirror's north shore, a passage to a hall, a passage on to the undercroft under the plaza."""
    lo = (min(CX, -52) - 12, 52, min(CZ, -58) - 8)
    snap = w.ids.copy()
    n1, _ = under.tunnel(w, [(-44, 64, -36, 2.9), (-45, 63, -42, 2.8), (-46, 63, -49, 3.0), (-47, 62, -54, 3.3)], ground=None)
    n2 = under.chamber(w, -48, 62, -55, 8, 4.4, rz=7.5, ground=None)
    n3, _ = under.tunnel(w, [(-48, 62, -54, 3.2), (-42, 63, -52, 2.8), (-37, 64, -51, 2.8)], ground=None)
    n4 = under.chamber(w, CX, 64, CZ, 5.6, 3.1, rz=5.6, ground=None)
    cave_skin(w, snap, rng)
    stats["blue cave"] = n1 + n2 + n3 + n4


def build(w, rng, stats):
    cave(w, rng, stats)
    plaza(w, rng)
    colonnade(w, rng)
    frost_gate(w)
