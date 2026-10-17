"""The bunker study's sheets, each a small world drawn by the studio's textured renderer.

    swatch    the six segments side by side, two tiers, on a straight wall two blocks thick
    corners   one footprint with outward and inward corners, so the corner rule shows, a gable crown on its front
    floors    the three floors, a four-block grid
    stagger   segments set out of line: on a diagonal, leaning back, and both at once
    interior  a hall, a room three segments tall and tunnels 6, 12 and 18 wide, walled in segments and floored
    facade    the bunker front: a flat wall with the door and its crown, two blast walls, slanted panels to the
              west, one lofted retaining wall along the front and one beside a blast wall

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
         "w": 2200, "h": 900},
        {"out": "light", "box": [0, BASE, 0, 23, BASE + 7, 3], "yaw": 200, "pitch": 10, "fov": 30,
         "w": 2000, "h": 1000},
        {"out": "dark", "box": [24, BASE, 0, 35, BASE + 15, 3], "yaw": 200, "pitch": 10, "fov": 30,
         "w": 1400, "h": 1400},
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
        {"out": "crown", "box": [8, BASE + 18, 18, 28, BASE + 40, 30], "yaw": 240, "pitch": 8, "fov": 30,
         "w": 1600, "h": 1100},
        {"out": "inner", "box": [22, BASE, 12, 40, BASE + 26, 28], "yaw": 140, "pitch": 12, "fov": 32,
         "w": 1600, "h": 1300},
    ])


# ---- floors -----------------------------------------------------------------------------------------------
def floors():
    n = len(T.FLOORS)
    w = World(-4, -4, n * 24 + 6, 26, 12)
    ground(w)
    for k, seg in enumerate(T.FLOORS):
        x0 = k * 24
        S.floor(w, (x0, 0, x0 + 15, 15), BASE - 1, seg, module=T.FLOOR_MODULE)
    shoot(w, "floors", [
        {"out": f"{seg.name}", "box": [k * 24, BASE - 1, 0, k * 24 + 15, BASE - 1, 15], "yaw": 200, "pitch": 45,
         "fov": 30, "w": 1200, "h": 900} for k, seg in enumerate(T.FLOORS)])


# ---- stagger ----------------------------------------------------------------------------------------------
def stagger():
    w = World(-6, -14, 112, 30, 36)
    ground(w)
    kinds = [("diagonal", 1, 0), ("lean", 0, -1), ("both", 1, -1)]
    for k, (_, bay, tier) in enumerate(kinds):
        S.staggered(w, k * 36, 0, T.ANDESITE_SEG, 4, 3, shift_bay=bay, shift_tier=tier, base=BASE)
    shoot(w, "stagger", [
        {"out": name, "box": [k * 36, BASE, -8, k * 36 + 23, BASE + 23, 6], "yaw": 150, "pitch": 14, "fov": 32,
         "w": 1500, "h": 1300} for k, (name, _, _) in enumerate(kinds)])


# ---- interior ---------------------------------------------------------------------------------------------
SPACES = {                 # x0, z0, x1, z1, height
    "hall": (0, 0, 23, 23, 16),
    "east": (26, 6, 49, 17, 8),
    "room": (52, -6, 75, 29, 24),
    "south": (6, 26, 11, 49, 8),
    "dark": (0, 52, 17, 69, 24),
    "north": (52, -32, 69, -9, 8),
}
# where a tunnel goes through a wall: the carved box, and the openings on the face each side of it
MOUTHS = [
    ((24, 6, 25, 17), [S.Opening("w", 6, 17, BASE, BASE + 7, line=24), S.Opening("e", 6, 17, BASE, BASE + 7, line=25)]),
    ((50, 6, 51, 17), [S.Opening("e", 6, 17, BASE, BASE + 7, line=51), S.Opening("w", 6, 17, BASE, BASE + 7, line=50)]),
    ((6, 24, 11, 25), [S.Opening("n", 6, 11, BASE, BASE + 7, line=24), S.Opening("s", 6, 11, BASE, BASE + 7, line=25)]),
    ((6, 50, 11, 51), [S.Opening("n", 6, 11, BASE, BASE + 7, line=50), S.Opening("s", 6, 11, BASE, BASE + 7, line=51)]),
    ((52, -8, 69, -7), [S.Opening("s", 52, 69, BASE, BASE + 7, line=-7),
                        S.Opening("n", 52, 69, BASE, BASE + 7, line=-8)]),
]
# the tiers of each space's walls, foot first: the author's segment mostly, gray wool at the foot of a tall room, one
# stripe at most and only at the top; the dark segment in its own room, at the foot
STACKS = {
    "hall": [T.ANDESITE_SEG, T.STRIPE_GRAY_SEG],
    "room": [T.GRAY_CYAN_SEG, T.ANDESITE_SEG, T.STRIPE_OBSIDIAN_SEG],
    "dark": [T.DARK_SEG, T.GRAY_CYAN_SEG, T.ANDESITE_SEG],
}
FLOOR_OF = {"dark": T.FLOOR_DARK}


def interior():
    w = World(-8, -40, 92, 116, 40)
    w.fill(w.x0, 0, w.z0, w.x0 + w.sx - 1, BASE - 1, w.z0 + w.sz - 1, B.STONE)
    air = {}
    for name, (x0, z0, x1, z1, h) in SPACES.items():
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                air[(x, z)] = name
    near = lambda x, z, r: [air[(x + i, z + j)] for i in range(-r, r + 1) for j in range(-r, r + 1)
                            if (x + i, z + j) in air]
    height = lambda name: SPACES[name][4]
    for x in range(w.x0, w.x0 + w.sx):                      # the rock, as high as the spaces beside it
        for z in range(w.z0, w.z0 + w.sz):
            names = near(x, z, 4)
            if names and (x, z) not in air:
                w.column(x, z, BASE, BASE + max(map(height, names)) - 1, B.STONE)
    cells = {(x, z) for x in range(w.x0, w.x0 + w.sx) for z in range(w.z0, w.z0 + w.sz)
             if (x, z) not in air and near(x, z, 2)}
    owner = {}
    for x, z in cells:                                      # a wall belongs to the space it faces
        for r in (1, 2):
            names = near(x, z, r)
            if names:
                owner[(x, z)] = (min if r == 1 else max)(names, key=height)
                break
    heights = {c: height(n) for c, n in owner.items()}

    def choose(side, i, j, run):
        stack = STACKS.get(owner[run[0]])
        if stack is None or j == "over":
            return T.ANDESITE_SEG
        return stack[j]

    S.wall(w, cells, BASE, heights, T.ANDESITE_SEG, lambda x, z: (x, z) in air, segment_of=choose,
           openings=[o for _, ops in MOUTHS for o in ops])
    for (x0, z0, x1, z1), _ in MOUTHS:
        w.fill(x0, BASE, z0, x1, BASE + 7, z1, B.AIR)
    for name, (x0, z0, x1, z1, h) in SPACES.items():
        S.floor(w, (x0, z0, x1, z1), BASE - 1, FLOOR_OF.get(name, T.FLOOR_L), module=T.FLOOR_MODULE, align=(x0, z0))
    for (x0, z0, x1, z1), _ in MOUTHS:
        S.floor(w, (x0, z0, x1, z1), BASE - 1, T.FLOOR_L, module=T.FLOOR_MODULE, align=(x0, z0))
    shoot(w, "interior", [
        {"out": "above", "box": [-4, BASE - 1, -36, 79, BASE + 24, 73], "yaw": 200, "pitch": 68, "fov": 36,
         "w": 2000, "h": 1900},
        {"out": "room", "box": [52, BASE - 1, -12, 77, BASE + 24, 29], "yaw": 215, "pitch": 26, "fov": 34,
         "w": 1700, "h": 1500},
        {"out": "hall", "box": [0, BASE - 1, -2, 30, BASE + 16, 23], "yaw": 205, "pitch": 24, "fov": 34,
         "w": 1800, "h": 1300},
        {"out": "dark", "box": [0, BASE - 1, 48, 19, BASE + 24, 69], "yaw": 200, "pitch": 26, "fov": 34,
         "w": 1600, "h": 1500},
    ])


# ---- facade -----------------------------------------------------------------------------------------------
FACE = (0, 41)             # the front's columns
DOOR = (18, 35)            # eighteen wide
DOOR_H = 16
FRONT_H = 24


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
            w.set(lx + 2 * ix, y, lz + 2 * iz, *S.COBBLE)


def blast_wall(w, x0, z0, length, h_hi, h_lo, width=4, band=BASE + 10):
    """A blast wall `width` thick from the face outward, painted like the lofted walls: cobble at the foot fading
    through polished andesite and andesite to stone, a gray-wool line at `band`. Its top falls from h_hi at the
    face to h_lo at its end in whole blocks."""
    for z in range(z0, z0 + length):
        top = round(h_hi - (h_hi - h_lo) * (z - z0) / max(1, length - 1))
        for x in range(x0, x0 + width):
            rim = x in (x0, x0 + width - 1) or z == z0 + length - 1
            for y in range(BASE, BASE + top):
                v = (y - BASE) / (top - 1)
                block, _ = T.LOFT.at(v, v, v, (x, y, z))
                w.set(x, y, z, *(S.GRAY_WOOL if rim and y == band else block))


def mountain(w, line, floor=BASE):
    """Ground behind a polyline [(x, z, top), ...] (behind is to the right of its direction), a block under each
    point's top for the three blocks behind it, so the wall's crest stands clear, then rising with the distance
    behind it; laid only where the air is still empty."""
    for x in range(w.x0, w.x0 + w.sx):
        for z in range(w.z0, w.z0 + w.sz):
            best = None
            for k, (p, q) in enumerate(zip(line, line[1:])):
                dx, dz = q[0] - p[0], q[1] - p[1]
                L = math.hypot(dx, dz)
                tt = min(1.0, max(0.0, ((x + 0.5 - p[0]) * dx + (z + 0.5 - p[1]) * dz) / (L * L)))
                cx, cz = p[0] + tt * dx, p[1] + tt * dz
                d = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
                sd = ((x + 0.5 - cx) * -dz + (z + 0.5 - cz) * dx) / L
                if best is None or d < best[0]:
                    best = (d, sd, p[2] + (q[2] - p[2]) * tt)
            d, sd, top = best
            if sd >= 0:
                continue
            rise = 0.5 * max(0.0, d - 3) + (noise(x, z, 12) - 0.5) * 8 * min(1.0, d / 14)
            h = min(w.sy - 2, int(top - 1 + max(0.0, rise)))
            for y in range(floor, h + 1):
                if w.id(x, y, z) == 0:
                    w.set(x, y, z, *(S.STONE if y < h - 1 else (B.DIRT, 0) if y < h else (B.GRASS, 0)))


WING = (-24, -1)           # the slanted panels west of the front


def facade():
    w = World(-84, -36, 156, 96, 72)
    ground(w)
    cells = {(x, z) for x in range(FACE[0], FACE[1] + 1) for z in (-1, 0)}
    gable = S.crown(rise=3, shape="gable", rows=3)

    def choose(side, i, j, run):
        if j == "over":
            return T.STRIPE_OBSIDIAN_SEG
        return T.STRIPE_GRAY_SEG if j == 2 else T.ANDESITE_SEG

    S.wall(w, cells, BASE, FRONT_H, T.ANDESITE_SEG, lambda x, z: FACE[0] <= x <= FACE[1] and z > 0,
           segment_of=choose, openings=[S.Opening("s", DOOR[0], DOOR[1], BASE, BASE + DOOR_H - 1, door)],
           top=lambda w, side, run, y: gable(w, side, [c for c in run if DOOR[0] <= c[0] <= DOOR[1]], y)
           if side == "s" else None)
    blast_wall(w, DOOR[0] - 5, 1, 14, 19, 16)
    blast_wall(w, DOOR[1] + 2, 1, 14, 19, 16)

    # west of the front, four bays of panels, each a block further back toward the end and each tier a block back
    S.staggered(w, WING[0], -3, T.ANDESITE_SEG, 4, 3, shift_bay=1, shift_tier=-1, base=BASE)

    # the lofted walls: one along the front past the panels to the west, one beside the east blast wall running out
    # to the south, each three edges, leaning back five, falling toward its end
    west = [((-72, BASE, 13), (-72, BASE + 8, 8)),
            ((-48, BASE, 3), (-48, BASE + 15, -2)),
            ((-24, BASE, -2), (-24, BASE + 20, -7))]
    east = [((41, BASE, 1), (46, BASE + 21, 1)),
            ((46, BASE, 25), (51, BASE + 15, 25)),
            ((56, BASE, 49), (61, BASE + 7, 49))]
    band = ("#" * 90,)
    number = lambda a, b: [p + "." + q for p, q in zip(LETTERS[a], LETTERS[b])]
    S.loft(w, west, T.LOFT, thick=3, marks=[(30, 2, number("0", "6"), 2, S.OBSIDIAN), (0, 12, band, 1, S.GRAY_WOOL)])
    S.loft(w, east, T.LOFT, thick=3, marks=[(8, 2, number("0", "7"), 2, S.OBSIDIAN), (0, 12, band, 1, S.GRAY_WOOL)])

    crest = lambda edges: [(e[1][0], e[1][2] - 3, e[1][1]) for e in edges]
    line = crest(west) + [(WING[0], -7.5, BASE + FRONT_H - 1), (WING[1], -4.5, BASE + FRONT_H - 1),
                          (FACE[0], -2.5, BASE + FRONT_H - 1), (FACE[1] + 1, -2.5, BASE + FRONT_H - 1)] + \
        [(x + 3, z + 0, y) for x, z, y in [(e[1][0], e[1][2], e[1][1]) for e in east]]
    mountain(w, line)
    shoot(w, "facade", [
        {"out": "wide", "box": [-76, BASE - 1, -30, 70, BASE + 44, 54], "yaw": 200, "pitch": 22, "fov": 40,
         "w": 2400, "h": 1400},
        {"out": "front", "box": [-28, BASE - 1, -6, 48, BASE + 34, 26], "yaw": 195, "pitch": 12, "fov": 34,
         "w": 2000, "h": 1300},
        {"out": "door", "box": [8, BASE - 1, -4, 46, BASE + 24, 20], "yaw": 215, "pitch": 14, "fov": 34,
         "w": 1800, "h": 1300},
        {"out": "east", "box": [30, BASE - 1, -8, 70, BASE + 26, 54], "yaw": 250, "pitch": 18, "fov": 36,
         "w": 2000, "h": 1300},
        {"out": "west", "box": [-76, BASE - 1, -16, 2, BASE + 26, 22], "yaw": 160, "pitch": 16, "fov": 36,
         "w": 2200, "h": 1200},
    ])


SHEETS = {"swatch": swatch, "corners": corners, "floors": floors, "stagger": stagger, "interior": interior,
          "facade": facade}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in sys.argv[1:] or SHEETS:
        SHEETS[name]()
