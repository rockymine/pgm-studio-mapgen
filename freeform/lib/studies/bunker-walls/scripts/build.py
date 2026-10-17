"""The bunker study's sheets, each a small world drawn by the studio's textured renderer.

    swatch    the six segments side by side, two tiers, on a straight wall two blocks thick
    corners   one footprint with outward and inward corners, so the corner rule shows, a gable crown on its front
    floors    the four floor segments, eighteen blocks a side each
    facade    the bunker front: a projecting keep with the door and its crown, two blast walls, two lofted retaining
              walls holding the mountain, the forecourt paved on the facade's module

    MINECRAFT_JAR=/path/to/1.8.9.jar python3 build.py [name ...]      # renders into ../renders
"""
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
from pgmvox import B, World                                                   # noqa: E402
from pgmvox.built.facade import LETTERS                                       # noqa: E402
from pgmvox.read import render                                                # noqa: E402

import segments as S                                                          # noqa: E402
import styles as T                                                            # noqa: E402

OUT = os.path.join(HERE, "..", "renders")
BUILD = os.path.join(tempfile.gettempdir(), "pgmvox-bunker-walls")
BASE = 4


def ground(w, y=BASE - 1, block=(B.GRASS, 0)):
    w.fill(w.x0, 0, w.z0, w.x0 + w.sx - 1, y - 1, w.z0 + w.sz - 1, B.STONE)
    w.fill(w.x0, y, w.z0, w.x0 + w.sx - 1, y, w.z0 + w.sz - 1, *block)


def shoot(w, name, shots):
    d = os.path.join(BUILD, name)
    w.save(d, name, (0, BASE, 0))
    jobs = [{**s, "out": os.path.join(OUT, f"{name}-{s['out']}.png")} for s in shots]
    print(render.textured(d, jobs))


def noise(x, z, cell=8.0, seed=0):
    """Smooth value noise in [0, 1)."""
    gx, gz = math.floor(x / cell), math.floor(z / cell)
    fx, fz = x / cell - gx, z / cell - gz
    fx, fz = fx * fx * (3 - 2 * fx), fz * fz * (3 - 2 * fz)
    a, b = S.h01(gx, gz, seed), S.h01(gx + 1, gz, seed)
    c, d = S.h01(gx, gz + 1, seed), S.h01(gx + 1, gz + 1, seed)
    return (a * (1 - fx) + b * fx) * (1 - fz) + (c * (1 - fx) + d * fx) * fz


# ---- swatch -----------------------------------------------------------------------------------------------
def swatch():
    n = len(T.SEGMENTS)
    w = World(-4, -8, n * 6 + 8, 20, 32)
    ground(w)
    cells = {(x, z) for x in range(0, n * 6) for z in (0, 1)}
    S.wall(w, cells, BASE, 16, T.ANDESITE_SEG, lambda x, z: z > 1,
           segment_of=lambda side, i, j, run: T.SEGMENTS[i] if side == "s" else T.ANDESITE_SEG)
    shoot(w, "swatch", [
        {"out": "front", "box": [0, BASE, 0, n * 6 - 1, BASE + 15, 3], "yaw": 180, "pitch": 6, "fov": 30,
         "w": 2000, "h": 900},
        {"out": "angle", "box": [0, BASE, 0, 17, BASE + 15, 3], "yaw": 215, "pitch": 14, "fov": 30,
         "w": 1600, "h": 1100},
        {"out": "close", "box": [0, BASE, 0, 5, BASE + 7, 3], "yaw": 200, "pitch": 10, "fov": 30,
         "w": 1200, "h": 1200},
    ])


# ---- corners ----------------------------------------------------------------------------------------------
def ring(inside, thick=2):
    return {c for c in inside if any((c[0] + dx, c[1] + dz) not in inside
                                     for dx in range(-thick, thick + 1) for dz in range(-thick, thick + 1))}


def corners():
    w = World(-6, -6, 50, 50, 56)
    ground(w)
    inside = {(x, z) for x in range(0, 37) for z in range(0, 19)} | \
             {(x, z) for x in range(12, 25) for z in range(19, 26)}
    cells = ring(inside)
    for x, z in inside - cells:
        w.column(x, z, BASE, BASE + 23, *S.COBBLE)
    gable = S.crown(rise=2, shape="gable")
    S.wall(w, cells, BASE, 24, T.ANDESITE_SEG, lambda x, z: (x, z) not in inside,
           top=lambda w, side, run, y: gable(w, side, run, y) if side == "s" and run[0][1] == 25 else None)
    shoot(w, "corners", [
        {"out": "se", "box": [-2, BASE, -2, 40, BASE + 40, 30], "yaw": 220, "pitch": 18, "fov": 34,
         "w": 1800, "h": 1300},
        {"out": "inner", "box": [22, BASE, 12, 40, BASE + 26, 28], "yaw": 140, "pitch": 12, "fov": 32,
         "w": 1600, "h": 1300},
    ])


# ---- floors -----------------------------------------------------------------------------------------------
def floors():
    n = len(T.FLOORS)
    w = World(-4, -4, n * 22 + 6, 28, 12)
    ground(w)
    for k, seg in enumerate(T.FLOORS):
        x0 = k * 22
        S.floor(w, (x0, 0, x0 + 17, 17), BASE - 1, seg)
    shoot(w, "floors", [
        {"out": f"{seg.name}", "box": [k * 22, BASE - 1, 0, k * 22 + 17, BASE - 1, 17], "yaw": 200, "pitch": 40,
         "fov": 30, "w": 1200, "h": 900} for k, seg in enumerate(T.FLOORS)])


# ---- facade -----------------------------------------------------------------------------------------------
ZF = 0                     # the main wall's face row
PROJ = (12, 36)            # the keep's columns, sides included
PROJ_D = 7                 # how far the keep stands forward of the main wall
DOOR = (18, 29)
MAIN_H, KEEP_H = 24, 32


def door(w, columns, side, y0, y1):
    """A blast door in a slot of the face: a bedrock frame in the face, an obsidian frame a block back, the leaf two
    blocks back, gray wool ribbed every four rows with a nether-brick slab over a nook, an obsidian seam down
    its middle."""
    ix, iz = S.DIRS[S.OPP[side]]
    n = len(columns)
    for s, (x, z) in enumerate(columns):
        for y in range(y0, y1 + 1):
            t = y - y0
            edge = s in (0, n - 1) or y == y1
            w.set(x, y, z, *(S.BEDROCK if edge else S.AIR))
            inner = s in (1, n - 2) or y == y1 - 1
            if edge:
                w.set(x + ix, y, z + iz, *S.BEDROCK)
            else:
                w.set(x + ix, y, z + iz, *(S.OBSIDIAN if inner else S.AIR))
            if edge or inner:
                continue
            lx, lz = x + 2 * ix, z + 2 * iz
            if s in (n // 2 - 1, n // 2):
                w.set(lx, y, lz, *S.OBSIDIAN)
            elif t % 4 == 3:
                w.set(lx, y, lz, *S.TOP_SLAB["nether"])
                w.set(lx + ix, y, lz + iz, *S.NETHER_BRICK)
            else:
                w.set(lx, y, lz, *S.GRAY_WOOL)


def blast_wall(w, x0, z0, length, h_hi, h_lo, blocked):
    """A blast wall four thick from the face outward, faced in the author's segment, its top falling from h_hi at
    the face to h_lo at its end in whole blocks under a polished-andesite coping that follows the fall."""
    cells = {(x, z) for x in range(x0, x0 + 4) for z in range(z0, z0 + length)}
    S.wall(w, cells, BASE, h_hi, T.ANDESITE_SEG, lambda x, z: (x, z) not in cells and (x, z) not in blocked)
    for z in range(z0, z0 + length):
        top = round(h_hi - (h_hi - h_lo) * (z - z0) / max(1, length - 1))
        for x in range(x0, x0 + 4):
            for y in range(BASE + top, BASE + h_hi + 1):
                w.set(x, y, z, B.AIR)
            w.set(x, BASE + top - 1, z, *S.POL_ANDESITE)
    return cells


def facade():
    w = World(-60, -40, 168, 100, 80)
    ground(w)
    zp = ZF + PROJ_D
    front = lambda x: zp if PROJ[0] <= x <= PROJ[1] else ZF
    main = {(x, z) for x in range(0, 49) for z in (ZF - 1, ZF)}
    keep_in = {(x, z) for x in range(PROJ[0], PROJ[1] + 1) for z in range(ZF - 1, zp + 1)}
    keep = ring(keep_in) - {(x, ZF - 1) for x in range(PROJ[0] + 2, PROJ[1] - 1)}
    for x, z in keep_in - keep:
        w.column(x, z, BASE, BASE + KEEP_H - 1, *S.COBBLE)
    cells = (main - keep_in) | keep
    heights = {c: (KEEP_H if c in keep_in else MAIN_H) for c in cells}
    outside = lambda x, z: 0 <= x <= 48 and z > front(x)
    gable = S.crown(rise=3, shape="gable", rows=3)
    S.wall(w, cells, BASE, heights, T.ANDESITE_SEG, outside,
           segment_of=lambda side, i, j, run: T.OBSIDIAN_SEG if j == "over" else T.ANDESITE_SEG,
           openings=[S.Opening("s", DOOR[0], DOOR[1], BASE, BASE + 15, door)],
           top=lambda w, side, run, y: gable(w, side, run, y) if side == "s" and run[0][1] == zp else None)

    # the forecourt, paved on the keep's module
    S.floor(w, (2, zp + 1, 46, zp + 30), BASE - 1, T.FLOOR_L, align=(PROJ[0], zp + 1))
    blocked = cells | keep_in
    b1 = blast_wall(w, DOOR[0] - 5, zp + 1, 14, 19, 16, blocked)
    blast_wall(w, DOOR[1] + 2, zp + 1, 14, 19, 16, blocked | b1)

    # the lofted retaining walls, each two planes, leaning back five over sixteen
    top = BASE + 16
    right = [((49, BASE, ZF + 1), (49, top, ZF + 1 - 5)),
             ((73, BASE, ZF + 1 + 5), (73, top, ZF + 1)),
             ((97, BASE, ZF + 1 + 15), (97, top, ZF + 1 + 10))]
    left = [((48 - p[0], p[1], p[2]), (48 - q[0], q[1], q[2])) for p, q in reversed(right)]
    behind = lambda x, y, z: S.STONE if w.id(x, y, z) == 0 else None
    band = ("#" * 90,)
    marks_r = [(10, 3, [a + "." + b for a, b in zip(LETTERS["0"], LETTERS["7"])], 2, S.OBSIDIAN),
               (0, 12, band, 1, S.GRAY_WOOL)]
    marks_l = [(30, 3, [a + "." + b for a, b in zip(LETTERS["0"], LETTERS["6"])], 2, S.OBSIDIAN),
               (0, 12, band, 1, S.GRAY_WOOL)]
    S.loft(w, right, T.LOFT, thick=3, behind=behind, reach=14, marks=marks_r)
    S.loft(w, left, T.LOFT, thick=3, behind=behind, reach=14, marks=marks_l)

    # the mountain behind, rising from the walls' tops
    for x in range(w.x0, w.x0 + w.sx):
        if 0 <= x <= 48:
            zline, h0 = ZF - 2, BASE + MAIN_H
        else:
            k = x - 49 if x > 48 else -1 - x
            zline = (ZF - 4 + k * 5 / 24) if k <= 24 else (ZF + 1 + (k - 24) * 10 / 24)
            zline = int(math.floor(zline)) - 2
            h0 = BASE + 16
        for z in range(w.z0, zline + 1):
            dist = zline - z
            h = int(h0 + 1 + dist * 0.7 + noise(x, z, 12) * 8 - 3)
            h = min(w.sy - 2, h)
            col_top = w.top(x, z)
            for y in range(BASE, h + 1):
                if w.id(x, y, z) == 0:
                    w.set(x, y, z, *(S.STONE if y < h - 1 else (B.DIRT, 0) if y < h else (B.GRASS, 0)))
    shoot(w, "facade", [
        {"out": "wide", "box": [-50, BASE - 1, -30, 98, BASE + 50, zp + 32], "yaw": 195, "pitch": 18, "fov": 40,
         "w": 2200, "h": 1300},
        {"out": "keep", "box": [4, BASE - 1, -2, 44, BASE + 44, zp + 18], "yaw": 200, "pitch": 10, "fov": 34,
         "w": 1800, "h": 1500},
        {"out": "door", "box": [10, BASE - 1, zp - 4, 38, BASE + 20, zp + 16], "yaw": 215, "pitch": 12, "fov": 34,
         "w": 1800, "h": 1300},
        {"out": "loft", "box": [44, BASE - 1, -16, 100, BASE + 20, 20], "yaw": 210, "pitch": 16, "fov": 36,
         "w": 2000, "h": 1200},
    ])


SHEETS = {"swatch": swatch, "corners": corners, "floors": floors, "facade": facade}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in sys.argv[1:] or SHEETS:
        SHEETS[name]()
