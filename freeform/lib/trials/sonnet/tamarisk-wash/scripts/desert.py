"""The desert's own small built things: palms, tamarisk, cacti, tents, an arcade with round arches, a well house, a
broken pillar. Written here; the library has no plants beyond the studio's tree cut and no arcade.
"""
import math

import plan  # noqa: F401  (puts the library on the path)
from pgmvox import B
from pgmvox.orient import door as door_data, ladder as ladder_data


def palm(w, x, y, z, rng, h=None):
    """A date palm: a jungle trunk leaning a little, a crown of fronds that droop, a bunch of dates. y is the
    ground's top block; the trunk starts over it."""
    h = h or int(rng.integers(6, 10))
    lean = (int(rng.integers(-1, 2)), int(rng.integers(-1, 2)))
    cx, cz = x, z
    for k in range(1, h + 1):
        if k > 2 and lean != (0, 0) and k % 3 == 0:
            cx, cz = cx + lean[0], cz + lean[1]
        w.set(cx, y + k, cz, B.LOG, 3)
    top = y + h
    leaf = (B.LEAVES, 3 | 4)
    w.set(cx, top + 1, cz, *leaf)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for s in (1, 2, 3):
            yy = top + 1 if s == 1 else top if s == 2 else top - 1
            if w.id(cx + dx * s, yy, cz + dz * s) in (B.AIR, B.TALLGRASS):
                w.set(cx + dx * s, yy, cz + dz * s, *leaf)
    for dx, dz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        for s, yy in ((1, top), (2, top - 1)):
            if w.id(cx + dx * s, yy, cz + dz * s) in (B.AIR, B.TALLGRASS):
                w.set(cx + dx * s, yy, cz + dz * s, *leaf)
    return cx, cz


def tamarisk(w, x, y, z, rng):
    """A tamarisk: a thin acacia trunk, a feathery crown of acacia leaves in two layers."""
    h = int(rng.integers(3, 6))
    for k in range(1, h + 1):
        w.set(x, y + k, z, B.LOG2, 0)
    leaf = (B.LEAVES2, 0 | 4)
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) + abs(dz) <= 3 and rng.random() < 0.85 and w.id(x + dx, y + h, z + dz) in (B.AIR, B.TALLGRASS):
                w.set(x + dx, y + h, z + dz, *leaf)
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            if abs(dx) + abs(dz) <= 1 and w.id(x + dx, y + h + 1, z + dz) in (B.AIR, B.TALLGRASS):
                w.set(x + dx, y + h + 1, z + dz, *leaf)


def cactus(w, x, y, z, rng):
    """A cactus one to three high on sand, with nothing solid beside it."""
    if any(w.id(x + dx, y + 1, z + dz) != B.AIR for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        return False
    for k in range(1, int(rng.integers(2, 4)) + 1):
        w.set(x, y + k, z, B.CACTUS, 0)
    return True


def tent(w, x, y, z, along="x", length=5, colour=0, stripe=3):
    """A pitched tent of wool, three wide: a ridge course, two sloping courses, open ends."""
    for s in range(length):
        for off in (-1, 0, 1):
            xx, zz = (x + s, z + off) if along == "x" else (x + off, z + s)
            if off == 0:
                w.set(xx, y + 3, zz, B.WOOL, colour)
            else:
                w.set(xx, y + 2, zz, B.WOOL, stripe if s % 2 == 0 else colour)
        for off in (-2, 2):
            xx, zz = (x + s, z + off) if along == "x" else (x + off, z + s)
            w.set(xx, y + 1, zz, B.WOOL, stripe if s % 2 == 0 else colour)


def arcade(w, x0, x1, z0, z1, deck, ground_at, rng, piers, block=(B.SANDSTONE, 2), pier=(B.SANDSTONE, 0),
           ragged_end=None):
    """A Roman arcade carrying a deck at y `deck` from x0 to x1, z0..z1 wide: piers (x ranges) down to the ground, a
    round arch between each pair, a two-course deck. Past ragged_end the arcade is broken, half its blocks gone."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if ragged_end is not None and (x > ragged_end or (x == ragged_end and rng.random() < 0.5)):
                continue
            g = ground_at(x, z)
            on_pier = any(a <= x <= b for a, b in piers)
            w.set(x, deck, z, *block)
            w.set(x, deck - 1, z, *block)
            if on_pier:
                for y in range(g, deck - 1):
                    w.set(x, y, z, *pier)
                continue
            lo = max([b for a, b in piers if b < x], default=None)
            hi = min([a for a, b in piers if a > x], default=None)
            if lo is None or hi is None:
                for y in range(max(g, deck - 3), deck - 1):
                    w.set(x, y, z, *block)
                continue
            c, r = (lo + hi) / 2.0, (hi - lo) / 2.0
            spring = deck - 2 - r
            for y in range(int(spring) - 1, deck - 1):
                dy = y - spring
                inside = (abs(x - c) < r) if dy < 0 else ((x - c) ** 2 + dy ** 2 < (r - 0.4) ** 2)
                if not inside and y >= g:
                    w.set(x, y, z, *block)


def well_house(w, x, z, top_y, bottom_y, rng, door_side="e"):
    """A sandstone well: a five-by-five ring (smooth sandstone, three courses over the ground at top_y) with a
    doorway two high on one side, a three-by-three shaft from top_y down to bottom_y, a ladder on the wall opposite
    the door, and a lining of smooth sandstone down the shaft."""
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            edge = max(abs(dx), abs(dz)) == 2
            for y in range(bottom_y, top_y + 4):
                if edge:
                    w.set(x + dx, y, z + dz, *((B.SANDSTONE, 2) if y < top_y + 2 else (B.SANDSTONE, 1) if y == top_y + 2
                                               else (B.AIR, 0)))
                else:
                    w.set(x + dx, y, z + dz, B.AIR)
    ddx, ddz = {"e": (2, 0), "w": (-2, 0), "n": (0, -2), "s": (0, 2)}[door_side]
    for y in (top_y + 1, top_y + 2):
        w.set(x + ddx, y, z + ddz, B.AIR)
    w.set(x + ddx, top_y, z + ddz, B.SANDSTONE, 2)
    lx, lz = -ddx // 2, -ddz // 2
    face = {(1, 0): "e", (-1, 0): "w", (0, 1): "s", (0, -1): "n"}[(lx, lz)]
    for y in range(bottom_y, top_y + 2):
        w.set(x + lx, y, z + lz, B.LADDER, ladder_data(face))


def broken_pillar(w, x, y, z, rng, h=None):
    """A fluted pillar of smooth sandstone, snapped at a random height, rubble at its foot."""
    h = h or int(rng.integers(3, 7))
    for k in range(1, h + 1):
        w.set(x, y + k, z, B.QUARTZ, 2 if k < h else 0)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if rng.random() < 0.4 and w.id(x + dx, y + 1, z + dz) == B.AIR:
            w.set(x + dx, y + 1, z + dz, B.SANDSTONE, 2)
