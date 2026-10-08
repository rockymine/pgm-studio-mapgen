"""A plot: a bounded canvas handed to a contributor, and the check a plot passes alone before it goes on a board.

A plot is a Python module with NAME, KIND and build(c). It draws into its own box through a Canvas, in local
coordinates (x and z from 0 to size - 1, y from y_min to y_max, a player on the surrounding ground standing at
y 0), and the canvas refuses anything outside the box or on the forbidden list. Curio Square's 48 plots, by three
builders, were drawn this way.

    m = load("plots/opus/watermill.py")
    c = draw(w, m, x0, z0, y0)                     # into a world at an origin; c.errors says what went wrong
    r = check_alone(m)                             # places to stand, the highest, out of sight, footing
    verdict(r, need_top=6, need_hidden=12)         # [] when it passes
"""
import importlib.util
import os

import numpy as np

from . import audit, blocks as K, sight, walk
from .blocks import B
from .world import World

FORBIDDEN = K.FORBIDDEN_IN_PLAY | K.DOORS


class OutOfPlot(Exception):
    pass


class Canvas:
    def __init__(self, world, x0, z0, y0, size=11, y_range=(-1, 23), forbidden=FORBIDDEN, ground_layer=True):
        self.w, self.x0, self.z0, self.y0 = world, x0, z0, y0
        self.size, (self.y_min, self.y_max) = size, y_range
        self.forbidden, self.ground_layer = forbidden, ground_layer
        self.errors = []

    def _at(self, x, y, z):
        if not (0 <= x < self.size and 0 <= z < self.size and self.y_min <= y <= self.y_max):
            self.errors.append(f"outside the plot: {x}, {y}, {z}")
            raise OutOfPlot((x, y, z))
        return self.x0 + x, self.y0 + y, self.z0 + z

    def set(self, x, y, z, bid, d=0):
        if bid in self.forbidden:
            self.errors.append(f"forbidden block {bid} at {x}, {y}, {z}")
        if self.ground_layer and y == self.y_min and bid in (B.AIR, B.WATER, B.WATER_FLOW):
            self.errors.append(f"the ground dug through at {x}, {z}")
        self.w.set(*self._at(x, y, z), bid, d)

    def fill(self, xa, ya, za, xb, yb, zb, bid, d=0):
        for x in range(min(xa, xb), max(xa, xb) + 1):
            for y in range(min(ya, yb), max(ya, yb) + 1):
                for z in range(min(za, zb), max(za, zb) + 1):
                    self.set(x, y, z, bid, d)

    def get(self, x, y, z):
        return self.w.get(*self._at(x, y, z))


def load(path):
    """Load a plot module. Plots written against a board's own mc.py (`from mc import B`) load too: the library's
    B has the same ids and more."""
    import sys
    sys.modules.setdefault("mc", K)
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for k in ("NAME", "KIND", "build"):
        if not hasattr(m, k):
            raise ValueError(f"{path}: no {k}")
    return m


def draw(world, module, x0, z0, y0, ground=(B.GRASS, 0), **canvas):
    """Hand the plot its ground layer and run its build; returns the canvas, whose errors say what went wrong."""
    c = Canvas(world, x0, z0, y0, **canvas)
    if c.ground_layer:
        world.fill(x0, y0 + c.y_min, z0, x0 + c.size - 1, y0 + c.y_min, z0 + c.size - 1, *ground)
    try:
        module.build(c)
    except OutOfPlot:
        pass
    except Exception as e:                                       # a plot that crashes is reported, not fatal
        c.errors.append(f"build failed: {type(e).__name__}: {e}")
    return c


def check_alone(module, size=11, y_range=(-1, 23), margin=4, y0=4, **canvas):
    """Build a plot alone with `margin` blocks of street round it and walk it from the street: the places a player
    can stand on the plot, the highest over the street, how many no eye on the street sees, and its footing."""
    span = size + 2 * margin
    w = World(-margin, -margin, span, span, sy=y0 + y_range[1] + 6)
    w.fill(-margin, 0, -margin, size + margin - 1, y0 - 1, size + margin - 1, B.STONE)
    c = draw(w, module, 0, 0, y0, size=size, y_range=y_range, **canvas)
    street = [(x, y0, z) for x in range(-margin, size + margin) for z in range(-margin, size + margin)
              if not (0 <= x < size and 0 <= z < size)]
    dist = walk.walk(w.ids, street, w.x0, w.z0)
    on = np.zeros(dist.shape, bool)
    on[margin:margin + size, :, margin:margin + size] = True
    spots = [(int(i + w.x0), int(y), int(k + w.z0)) for i, y, k in np.argwhere((dist >= 0) & on)]
    top = max((y for _, y, _ in spots), default=y0) - y0
    eyes = [sight.eye(x, y0, z) for x, _, z in street if (x + z) % 2 == 0]
    opaque = sight.voxel_opaque(w)
    hid = sight.hidden([sight.target(x, y, z) for x, y, z in spots], eyes, opaque)
    feet = audit.footing(w, (0, y0 + y_range[0], 0, size - 1, y0 + y_range[1], size - 1))
    return dict(name=module.NAME, kind=module.KIND, spots=len(spots), top=top, hidden=len(hid), errors=c.errors,
                footing=feet, world=w)


def verdict(r, need_top=6, need_hidden=12):
    out = list(r["errors"]) + [f"{x}, {y}, {z}: {why}" for x, y, z, why in r["footing"]]
    if r["top"] < need_top:
        out.append(f"the highest place to stand is {r['top']} over the street, under {need_top}")
    if r["hidden"] < need_hidden:
        out.append(f"{r['hidden']} places to stand are out of sight from the street, under {need_hidden}")
    return out
