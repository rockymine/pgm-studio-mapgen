"""Build Sixes and Sevens: Red's half (the ground, the needles, the bunker, the lofted walls), turned onto Blue's,
then Blue's lofted walls marked 07, the objectives, and the world saved.

    python3 gen.py <build-dir>
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import bunker  # noqa: E402
import land
import plan as P
from pgmvox import B, World
from pgmvox.built import segments as S
from pgmvox.built.facade import LETTERS
from pgmvox.core.orient import turn_world
from pgmvox.grammar import bunker as T
from pgmvox.scenery.forms import spike

SY = 160
BAND = ("#" * 120,)


def number(a, b):
    return [p + "." + q for p, q in zip(LETTERS[a], LETTERS[b])]


def lofts(w, digits, image=None):
    """Every lofted wall of one bunker, the bunker's number on the spurs and the gray-wool line on all of them."""
    for name, edges in P.LOFTS.items():
        if image:
            edges = [tuple((*image(p[0], p[2])[:1], p[1], image(p[0], p[2])[1]) for p in e) for e in edges]
            edges = [((b[0], b[1], b[2]), (t[0], t[1], t[2])) for b, t in edges]
        marks = [(0, 10, BAND, 1, S.GRAY_WOOL)]
        if name == "tier":
            marks = []
        if name == "north spur":
            marks.append((14, 2, number(*digits), 2, S.OBSIDIAN))
        S.loft(w, edges, T.LOFT, thick=3, marks=marks)


def needles(w, top):
    """A tall needle of rock over the bunker, and a lesser one, in strata of stone and andesite."""
    for k, ((x, z), rise) in enumerate(land.NEEDLES):
        y0 = int(top[x - w.x0, z - w.z0]) - 6
        axis = [(x, y0, z), (x + 2, y0 + rise * 0.5, z - 1), (x + 4, y0 + rise, z + 1)]
        m = spike(w, axis, (9 if k == 0 else 6, 0.5, 1.3), sides=7, flutes=(5, 0.6), ledges=(9, 1.0), rough=0.15,
                  seed=80 + k)
        ys = np.arange(w.sy)[None, :, None]
        strata = np.array([B.STONE, B.STONE, B.STONE, B.COBBLE], np.uint16)[(ys // 3) % 4] * np.ones_like(m)
        dat = np.where((ys // 3) % 4 == 1, 5, 0) * np.ones_like(m)
        w.ids[m] = strata[m]
        w.dat[m] = dat[m]


def boulders(w):
    """A few boulders on the field, each a lumpy ball of andesite and cobblestone sunk a third into the snow."""
    r = np.random.default_rng(90)
    for x, z, rad in P.BOULDERS:
        y0 = w.top(x, z)
        for dx in range(-rad - 1, rad + 2):
            for dz in range(-rad - 1, rad + 2):
                for dy in range(-rad, rad + 1):
                    k = (dx / (rad + 0.5)) ** 2 + (dz / (rad + 0.3)) ** 2 + (dy / (rad * 0.8 + 0.4)) ** 2
                    if k <= 1 + 0.25 * r.uniform(-1, 1):
                        block = (B.STONE, 5) if r.random() < 0.6 else (B.COBBLE, 0)
                        w.set(x + dx, y0 + dy + rad // 2, z + dz, *block)


def build(out):
    x0, z0, sx, sz = P.WORLD
    w = World(x0, z0, sx, sz, sy=SY)
    w.biome[:] = 12                                      # ice plains
    X, Z = w.grid()
    X, Z = X.astype(float), Z.astype(float)
    rock, snow, teeth = land.heights(X, Z)
    half = X < 0
    top = land.lay(w, rock, snow, teeth, X, Z, half)
    needles(w, top)
    boulders(w)
    bunker.build(w)
    lofts(w, ("0", "6"))
    turn_world(w, "half", half)
    lofts(w, ("0", "7"), image=P.SYM.point)
    w.fill(x0, 0, z0, x0 + sx - 1, 0, z0 + sz - 1, B.BEDROCK)
    O = P.objectives()
    O.stamp(w)
    w.save(out, "Sixes and Sevens", (0, 90, 0))
    problems = O.check(w)
    print("\n".join(problems) or "objectives read back clean")
    return w


if __name__ == "__main__":
    build(sys.argv[1])
