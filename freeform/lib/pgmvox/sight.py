"""Sight lines: who can see whom, on a plan or in a built world.

One eye height for every board: move.EYE (1.62 over the feet); a target is aimed at its chest, `AIM` over its
feet. A line is clear when every cell it passes through is clear, sampled at a quarter block.

    line_clear(a, b, opaque)          a and b are (x, y, z) points; opaque(x, y, z) says a cell blocks
    plan_opaque(R, roofs=None)        an opaque() for a raster: solid up to each column's floor, and roofs
    voxel_opaque(w)                   an opaque() for a built world: anything not in blocks.SIGHT_CLEAR
    visibility(targets, eyes, opaque) for every target, the share of eyes that see it
    hidden(targets, eyes, opaque)     the targets no eye sees
"""
import math

import numpy as np

from . import blocks as K
from .move import EYE

AIM = 0.9


def line_clear(a, b, opaque, step=0.25):
    ax, ay, az = a
    bx, by, bz = b
    n = int(max(abs(bx - ax), abs(by - ay), abs(bz - az)) / step) + 1
    last = None
    for s in range(1, n):
        t = s / n
        c = (math.floor(ax + (bx - ax) * t), math.floor(ay + (by - ay) * t), math.floor(az + (bz - az) * t))
        if c == last:
            continue
        last = c
        if opaque(*c):
            return False
    return True


def plan_opaque(R, roofs=None):
    """A raster is solid up to each column's floor block; roofs (x, z) -> (y0, y1) adds a solid band above."""
    def opaque(x, y, z):
        if not R.inside(x, z):
            return False
        if y <= R.h(x, z):
            return True
        if roofs:
            band = roofs.get((x, z))
            if band and band[0] <= y <= band[1]:
                return True
        return False
    return opaque


def voxel_opaque(w):
    clear = K.mask(w.ids, K.SIGHT_CLEAR)

    def opaque(x, y, z):
        i, k = x - w.x0, z - w.z0
        if not (0 <= i < w.sx and 0 <= y < w.sy and 0 <= k < w.sz):
            return False
        return not clear[i, y, k]
    return opaque


def eye(x, y_feet, z):
    """The eye of a player standing in cell (x, z) with feet at y_feet."""
    return (x + 0.5, y_feet + EYE, z + 0.5)


def target(x, y_feet, z):
    return (x + 0.5, y_feet + AIM, z + 0.5)


def visibility(targets, eyes, opaque):
    """For every target point, the share of eye points that see it."""
    out = np.zeros(len(targets))
    for k, t in enumerate(targets):
        seen = sum(1 for e in eyes if line_clear(e, t, opaque))
        out[k] = seen / max(1, len(eyes))
    return out


def hidden(targets, eyes, opaque):
    """The targets no eye sees (stops at the first eye that does)."""
    return [t for t in targets if not any(line_clear(e, t, opaque) for e in eyes)]
