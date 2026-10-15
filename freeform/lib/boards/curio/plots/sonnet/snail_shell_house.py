"""A snail whose shell is a spiral ziggurat with a ramp winding up it, alcoves in the whorls and a tower-head."""
import math
from mc import B

NAME = "The Snail House"
KIND = "house"

CX, CZ = 5, 4
A = 4 * math.pi          # two turns
H = 12.0                 # height gained over the whole ramp
R0, R1, HW = 3.8, 0.9, 0.85


def rho(a):
    return R0 + (R1 - R0) * a / A


def top_at(a):
    return round((0.5 + (H - 0.5) * a / A) * 2) / 2


def shell_height(x, z):
    dx, dz = x - CX, z - CZ
    r = math.hypot(dx, dz)
    phi = math.atan2(dz, dx) % (2 * math.pi)
    best = 0
    for n in range(2):
        a = phi + 2 * math.pi * n
        if a > A:
            continue
        if r <= rho(a) + HW:
            best = max(best, top_at(a))
    if r <= R1 + HW - 0.2:
        best = max(best, top_at(A))
    return best


def build(c):
    hts = {}
    for x in range(0, 11):
        for z in range(0, 9):
            h = shell_height(x, z)
            if h > 0:
                hts[(x, z)] = h
    for (x, z), h in hts.items():
        full = int(h) if abs(h - int(h)) < 1e-9 else None
        top_y = (full - 1) if full is not None else int(h)         # last full-block layer
        solid_to = (full - 1) if full is not None else int(h) - 1
        for y in range(0, solid_to + 1):
            c.set(x, y, z, B.STAINED_CLAY, [12, 12, 1, 1][y % 4])
        if full is not None:
            c.set(x, top_y, z, B.SANDSTONE, 2 if (x + z) % 5 == 0 else 0)
        else:
            c.set(x, int(h), z, B.SLAB, 1)
    # rooms inside the shell: a lower den and an upper chamber, joined by a ladder shaft
    c.fill(4, 1, 3, 6, 3, 5, B.AIR)
    c.fill(3, 1, 3, 3, 3, 5, B.AIR)
    c.fill(4, 1, 6, 6, 3, 6, B.AIR)
    c.fill(4, 3, 6, 6, 3, 6, B.AIR)
    c.fill(7, 1, 4, 7, 2, 4, B.AIR)             # the den's mouth, off the foot of the ramp
    c.fill(4, 6, 3, 5, 9, 5, B.AIR)
    c.fill(6, 6, 4, 6, 7, 4, B.AIR)             # the chamber's mouth, off the first whorl
    c.fill(5, 4, 3, 5, 5, 3, B.AIR)
    for y in range(1, 11):
        c.set(5, y, 3, B.LADDER, 3)
    c.set(4, 11, 3, B.AIR)
    c.set(5, 4, 4, B.GLOWSTONE)
    c.set(4, 9, 4, B.GLOWSTONE)
    c.set(4, 6, 5, B.CHEST, 3)
    c.set(6, 1, 3, B.CRAFTING)
    c.set(4, 1, 5, B.BOOKSHELF)
    # crown of the shell
    ty = int(top_at(A))
    c.set(CX, ty, CZ + 1, B.GOLD_BLOCK)
    c.set(CX, ty + 1, CZ + 1, B.FENCE)
    c.set(CX, ty + 2, CZ + 1, B.WOOL, 14)
    # the slug body
    for x in range(2, 11):
        hh = 3 if x <= 7 else (2 if x <= 9 else 1)
        if x == 2:
            hh = 4
        c.fill(x, 0, 8, x, hh - 1, 10, B.STAINED_CLAY, 8 if x >= 3 else 0)
        c.fill(x, hh - 1, 8, x, hh - 1, 10, B.STAINED_CLAY, 4) if x >= 3 else None
    # stripes along the back
    for x in range(3, 8):
        c.set(x, 2, 9, B.STAINED_CLAY, 12) if x % 2 == 0 else None
    # tower head (hollow, with a ladder), x0..2
    c.fill(0, 0, 8, 2, 6, 10, B.STAINED_CLAY, 8)
    c.fill(1, 0, 9, 1, 6, 9, B.AIR)
    c.fill(0, 7, 8, 2, 7, 10, B.STAINED_CLAY, 4)
    c.set(1, 7, 9, B.AIR)
    for y in range(0, 8):
        c.set(1, y, 9, B.LADDER, 3)
    c.fill(1, 0, 10, 1, 1, 10, B.AIR)         # the doorway (south)
    c.fill(2, 3, 9, 2, 4, 9, B.AIR)           # a window onto the body
    c.fill(0, 3, 9, 0, 4, 9, B.PANE)
    c.fill(0, 0, 9, 0, 1, 9, B.AIR)           # the mouth (west)
    c.fill(1, 3, 8, 1, 4, 8, B.PANE)
    # eye stalks and eyeballs
    for z in (8, 10):
        c.fill(0, 8, z, 0, 10, z, B.FENCE)
        c.set(0, 11, z, B.WOOL, 0)
    # the smile: black eyes on the face
    c.set(0, 5, 8, B.COAL_BLOCK)
    c.set(0, 5, 10, B.COAL_BLOCK)
    c.set(0, 2, 9, B.STAINED_CLAY, 6)
    # tail flag
    c.set(10, 1, 9, B.STAINED_CLAY, 6)
