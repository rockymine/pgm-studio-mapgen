"""The plot kit: the canvas every plot is drawn into, and the check every plot must pass before it goes in the square.

A plot is a Python module in plots/<builder>/<name>.py with three names in it:

    NAME = "The Lighthouse"          # shown when the plot vanishes
    KIND = "structure"               # house, structure or sculpture
    def build(c): ...                # draws into the canvas c

The canvas is the plot's own box, in local coordinates: x and z from 0 to 10, y from -1 to 23. A player on the
street outside stands at y 0, on the ground layer at y -1. The
plot's ground layer, y -1, is grass when the canvas is handed over and may be repainted, never dug through. Nothing
may be set outside the box: the canvas refuses it and the check fails.

    c.set(x, y, z, B.STONE)                 # a block; data as a fourth argument
    c.fill(x0, y0, z0, x1, y1, z1, B.PLANKS, 1)
    c.get(x, y, z)                          # (id, data)

    python3 plotkit.py <plot.py>            # build one plot alone, check it, draw it
"""
import importlib.util
import os
import sys

import numpy as np

import walk_core as W
from mc import B, World

SIZE = 11
Y_MIN, Y_MAX = -1, 23
FORBIDDEN = {B.WATER_FLOW, B.LAVA, B.LAVA_FLOW, B.TNT, B.BEDROCK, B.BARRIER, B.SPAWNER, B.COBWEB, 51,     # 51 fire
             B.OAK_DOOR, B.IRON_DOOR, 193, 194, 195, 196, 197}                                     # doors
GRAVITY = {B.SAND, B.GRAVEL, B.ANVIL}
# the side an attached block hangs on, by its data: (dx, dz) to the block holding it; (0, 0) means the block below
TORCH_ON = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1), 5: (0, 0)}
LADDER_ON = {2: (0, 1), 3: (0, -1), 4: (1, 0), 5: (-1, 0)}
NEED_TOP = 6                     # a plot's highest reachable standing place, at least this far over the street
NEED_HIDES = 12                  # standing places a seeker on the street cannot see


class OutOfPlot(Exception):
    pass


class Canvas:
    def __init__(self, world, x0, z0, y0):
        self.w, self.x0, self.z0, self.y0 = world, x0, z0, y0
        self.errors = []

    def _at(self, x, y, z):
        if not (0 <= x < SIZE and 0 <= z < SIZE and Y_MIN <= y <= Y_MAX):
            self.errors.append(f"outside the plot: {x}, {y}, {z}")
            raise OutOfPlot((x, y, z))
        return self.x0 + x, self.y0 + y, self.z0 + z

    def set(self, x, y, z, bid, d=0):
        if bid in FORBIDDEN:
            self.errors.append(f"forbidden block {bid} at {x}, {y}, {z}")
        if y == Y_MIN and bid in (B.AIR, B.WATER):
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
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for k in ("NAME", "KIND", "build"):
        if not hasattr(m, k):
            raise SystemExit(f"{path}: no {k}")
    return m


def draw(world, module, x0, z0, y0):
    """Hand the plot its grass and run its build. Returns the canvas, whose errors list says what went wrong."""
    c = Canvas(world, x0, z0, y0)
    world.fill(x0, y0 - 1, z0, x0 + SIZE - 1, y0 - 1, z0 + SIZE - 1, B.GRASS)
    try:
        module.build(c)
    except OutOfPlot:
        pass
    except Exception as e:                                       # a plot that crashes is reported, not fatal
        c.errors.append(f"build failed: {type(e).__name__}: {e}")
    return c


def check(world, x0, z0, y0, margin):
    """Walk the plot from the street round it: the highest place a hider can stand, and how many standing places a
    seeker on the street cannot see. The world is the plot alone with `margin` blocks of street round it."""
    ids = world.ids
    passable, water, ladder, solid = W.grid(ids)
    st = W.standable(passable, water, solid)
    sx, sy, sz = ids.shape
    starts = [(world.x0 + i, y0, world.z0 + k) for i in range(sx) for k in range(sz)
              if not (margin <= i < margin + SIZE and margin <= k < margin + SIZE)]
    dist = W.bfs(st, ladder, water, passable, starts, world.x0, world.z0, jumps=True)
    reach = (dist >= 0)
    on_plot = np.zeros_like(reach)
    on_plot[margin:margin + SIZE, :, margin:margin + SIZE] = True
    spots = np.argwhere(reach & on_plot)
    top = int(spots[:, 1].max()) - y0 if len(spots) else 0
    eyes = [(i, y0 + 1.6, k) for i in range(sx) for k in range(sz)
            if not (margin <= i < margin + SIZE and margin <= k < margin + SIZE) and (i + k) % 2 == 0]
    hidden = 0
    for x, y, z in spots:
        if not any(_sees(passable, e, (x + 0.5, y + 0.9, z + 0.5)) for e in eyes):
            hidden += 1
    return dict(spots=len(spots), top=top, hidden=hidden)


def _sees(passable, a, b):
    ax, ay, az = a[0] + 0.5, a[1], a[2] + 0.5
    n = int(max(abs(b[0] - ax), abs(b[1] - ay), abs(b[2] - az)) * 2) + 1
    for s in range(1, n):
        t = s / n
        x, y, z = int(ax + (b[0] - ax) * t), int(ay + (b[1] - ay) * t), int(az + (b[2] - az) * t)
        if not passable[x, y, z]:
            return False
    return True


def footing(world, x0, z0, y0):
    """Blocks that would fall or pop off when the world loads: sand, gravel and anvils over air; torches, ladders and
    wall signs with nothing solid to hang on."""
    out = []
    passable = W.grid(world.ids)[0]
    for x in range(SIZE):
        for z in range(SIZE):
            for y in range(Y_MIN, Y_MAX + 1):
                bid, d = world.get(x0 + x, y0 + y, z0 + z)
                if not bid:
                    continue
                if bid in GRAVITY and world.get(x0 + x, y0 + y - 1, z0 + z)[0] == 0:
                    out.append(f"block {bid} over air at {x}, {y}, {z}: it falls")
                on = (TORCH_ON.get(d) if bid in (B.TORCH, 76) else LADDER_ON.get(d) if bid in (B.LADDER, B.WALL_SIGN)
                      else None)
                if bid in (B.TORCH, 76, B.LADDER, B.WALL_SIGN) and on is None:
                    out.append(f"block {bid} at {x}, {y}, {z} has data {d}, which faces nowhere")
                elif on is not None:
                    hx, hy, hz = (x, y - 1, z) if on == (0, 0) else (x + on[0], y, z + on[1])
                    i = (x0 + hx - world.x0, y0 + hy, z0 + hz - world.z0)
                    if passable[i]:
                        out.append(f"block {bid} at {x}, {y}, {z} hangs on nothing: it pops off")
    return out


def verdict(c, r, world=None, x0=0, z0=0, y0=0):
    out = list(c.errors)
    if world is not None:
        out += footing(world, x0, z0, y0)
    if r["top"] < NEED_TOP:
        out.append(f"the highest place to stand is {r['top']} over the street, under {NEED_TOP}: nothing to climb")
    if r["hidden"] < NEED_HIDES:
        out.append(f"{r['hidden']} places to stand are out of sight from the street, under {NEED_HIDES}")
    return out


def main(path, png=None):
    m = load(path)
    margin, y0 = 4, 4
    w = World(-margin, -margin, SIZE + 2 * margin, SIZE + 2 * margin, sy=y0 + Y_MAX + 6)
    w.fill(-margin, 0, -margin, SIZE + margin - 1, y0 - 1, SIZE + margin - 1, B.STONE)
    c = draw(w, m, 0, 0, y0)
    r = check(w, 0, 0, y0, margin)
    bad = verdict(c, r, w, 0, 0, y0)
    print(f"{m.NAME} ({m.KIND}): {r['spots']} places to stand, the highest {r['top']} over the street, "
          f"{r['hidden']} out of sight from it")
    print("\n".join("  FAIL " + b for b in bad) or "  pass")
    if png:
        import render_iso
        for corner in ("se", "nw"):
            render_iso.render(w.ids, w.dat, w.x0, w.z0, png.replace(".png", f"-{corner}.png"), scale=10, corner=corner)
    return not bad


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None) else 1)
