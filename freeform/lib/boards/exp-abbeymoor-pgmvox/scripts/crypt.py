"""What is cut under Abbeymoor's ground (red's half): the crypt hall under the nave, the Night Stair up to the chancel, the
passage under the hill and the valley, and the Tithe Barn's cellar stair. Every floor is the plan's (plan.NIGHT_STAIR,
plan.PASSAGE_FLOORS); a stair cell is a stair block at the floor's y, rising toward the higher side, three of air over it.

    carve_all(w, R, r, stats)   hall, stairs, passage: before the buildings stand
    finish(w, stats)            the slots in the nave's and the barn's floors, rails round them: after
"""
import numpy as np

import plan as P
from pgmvox import B
from pgmvox.orient import stair as stair_data, torch as torch_data

BRICK_MIX = [(B.STONEBRICK, 0), (B.STONEBRICK, 0), (B.STONEBRICK, 2), (B.STONE, 6)]


def pick(r):
    return BRICK_MIX[int(r.integers(len(BRICK_MIX)))]


def air(w, x0, y0, z0, x1, y1, z1):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                w.set(x, y, z, B.AIR)


def line(w, x0, y0, z0, x1, y1, z1, r):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                w.set(x, y, z, *pick(r))


def hall(w, r):
    """The crypt: a vaulted hall, ten by nine and five high, brick lined, four pillars, three sarcophagi under the north wall."""
    x0, z0, x1, z1 = P.CRYPT[0] + 1, P.CRYPT[1] + 1, P.CRYPT[2] - 1, P.CRYPT[3] - 1
    f, top = P.CRYPT_FLOOR, P.CRYPT_FLOOR + P.CRYPT_H
    line(w, x0 - 1, f - 1, z0 - 1, x1 + 1, top + 1, z1 + 1, r)                # the shell
    air(w, x0, f, z0, x1, top, z1)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w.set(x, f - 1, z, *pick(r))
            w.set(x, f, z, B.AIR)
    for px, pz in ((-50, -74), (-46, -74), (-50, -71), (-46, -71)):
        for y in range(f, top + 1):
            w.set(px, y, pz, B.STONEBRICK, 3 if y == top else 0)
    for sx in (-51, -48, -45):                                                # sarcophagi: a quartz slab on a plinth
        w.set(sx, f, z0, B.STONEBRICK, 3)
        w.set(sx + 1, f, z0, B.STONEBRICK, 3)
        w.set(sx, f + 1, z0, B.SLAB, 7)
        w.set(sx + 1, f + 1, z0, B.SLAB, 7)
    for tx in range(x0 + 1, x1, 3):                                           # torches on the south wall, clear of the door
        if -50 <= tx <= -46:
            continue
        w.set(tx, f + 2, z1, B.TORCH, torch_data("s"))
    # the way east to the Night Stair: the hall's east wall opened three wide, four high
    air(w, P.CRYPT[2], f, P.SLOT[1], P.CRYPT[2], f + 3, P.SLOT[3])
    # the door south to the passage: three wide, three high
    air(w, -49, f, P.CRYPT[3], -47, f + 2, P.CRYPT[3])


def night_stair(w, r):
    """The Night Stair: x -41 to -31 under the chancel, three wide. Stairs rise east; a landing is a floor block; the slot is cut up to the
    nave's floor (and through it, in finish) and lined with brick on both sides."""
    z0, z1 = P.SLOT[1], P.SLOT[3]
    prev = P.CRYPT_FLOOR
    for x, y in P.NIGHT_STAIR:
        for z in range(z0, z1 + 1):
            for yy in range(y + 1, P.PLATEAU + 1):
                w.set(x, yy, z, B.AIR)
            for yy in range(y - 4, y):
                w.set(x, yy, z, *pick(r))
            if y != prev:
                w.set(x, y, z, B.STONEBRICK_STAIRS, stair_data("e"))
            else:
                w.set(x, y, z, *pick(r))
        for yy in range(y - 4, P.PLATEAU + 2):
            w.set(x, yy, z0 - 1, *pick(r))
            w.set(x, yy, z1 + 1, *pick(r))
        prev = y
    # the stair's cells are stair blocks where the floor changes; the first cell above the hall's floor is a step too


def floors_along_x():
    xs = sorted(P.PASSAGE_FLOORS)
    return xs, [P.PASSAGE_FLOORS[x] for x in xs]


def passage(w, r):
    """The passage: three wide and three high, brick floor, walls and roof, a pier every five, a torch every six; south from the crypt's
    door, then east along z -61 down three flights to 59, along the valley, and up the cellar stair."""
    z0, z1 = P.PASSAGE_Z - 1, P.PASSAGE_Z + 1
    f = P.CRYPT_FLOOR
    for x, z in P.PASSAGE_SOUTH:                                              # south from the door: x -49..-47, z -66..-62
        for dx in (-1, 0, 1):
            line(w, x + dx, f - 1, z, x + dx, f - 1, z, r)
            air(w, x + dx, f, z, x + dx, f + 2, z)
            line(w, x + dx, f + 3, z, x + dx, f + 3, z, r)
        line(w, x - 2, f, z, x - 2, f + 3, z, r)
        line(w, x + 2, f, z, x + 2, f + 3, z, r)
    xs, ys = floors_along_x()
    prev = ys[0]
    for x, fy in zip(xs, ys):
        for z in range(z0, z1 + 1):
            line(w, x, fy - 3, z, x, fy - 1, z, r)
            air(w, x, fy + 1, z, x, fy + 3, z) if x < 11 else air(w, x, fy + 1, z, x, min(fy + 3, 65), z)
            if fy != prev:
                rises = "w" if fy < prev else "e"
                w.set(x, fy, z, B.STONEBRICK_STAIRS, stair_data(rises))
            else:
                w.set(x, fy, z, *pick(r))
            if x < 11:
                w.set(x, fy + 4, z, *pick(r))
        for y in range(fy - 3, fy + 4 if x < 11 else min(fy + 4, 66)):
            w.set(x, y, z0 - 1, *pick(r))
            w.set(x, y, z1 + 1, *pick(r))
        if x % 6 == 0 and x < 11:
            w.set(x, fy + 2, z0, B.TORCH, torch_data("n"))
        if x % 5 == 0 and x < 11 and prev == fy:
            for z in (z0, z1):
                w.set(x, fy + 1, z, B.STONEBRICK, 3)
                w.set(x, fy + 2, z, B.STONEBRICK, 3)
        prev = fy
    # the corner where the south stretch meets the east: the room between z -62 and -60 at x -49..-47 is air
    for x in range(-49, -46):
        for z in range(z0, z1 + 1):
            air(w, x, f + 1, z, x, f + 3, z)
            w.set(x, f, z, *pick(r))


def carve_all(w, R, r, stats):
    hall(w, r)
    night_stair(w, r)
    passage(w, r)
    stats["crypt"] = "hall, Night Stair, passage cut"


def finish(w, stats):
    """After the nave and the barn stand: the slot in the barn's floor open over the cellar stair, the Night Stair's slot open through the nave's
    floor, rails along their sides."""
    z0, z1 = P.PASSAGE_Z - 1, P.PASSAGE_Z + 1
    floor = P.houses()["tithe"]["floor"]
    for x in range(P.CELLAR[0], P.CELLAR[2] + 1):
        for z in range(z0, z1 + 1):
            for y in range(P.PASSAGE_FLOORS[x] + 1, floor + 1):
                w.set(x, y, z, B.AIR)
    for x in range(P.CELLAR[0], P.CELLAR[2] + 1):
        for z in (z0 - 1, z1 + 1):
            w.set(x, floor + 1, z, B.SPRUCE_FENCE, 0)
    for x in range(P.SLOT[0], P.SLOT[2] + 1):
        for z in range(P.SLOT[1], P.SLOT[3] + 1):
            for y in range(max(P.NIGHT_STAIR[0][1], 71), P.PLATEAU + 3):
                if y > dict(P.NIGHT_STAIR).get(x, 99):
                    w.set(x, y, z, B.AIR)
        for z in (P.SLOT[1] - 1, P.SLOT[3] + 1):
            w.set(x, P.PLATEAU + 1, z, B.COBBLE_WALL, 0)
    stats["slots"] = "open"
