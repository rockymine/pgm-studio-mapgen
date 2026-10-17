"""Build Sixes and Sevens: Red's half (the ground, the boulders, the bunker, the lofted walls), turned onto Blue's,
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

SY = 160
BAND = ("#" * 120,)


def number(a, b):
    return [p + "." + q for p, q in zip(LETTERS[a], LETTERS[b])]


def lofts(w):
    """Red's lofted walls with the gray-wool line, drawn before the half turn so Blue's are their exact copies:
    {name: (face, lowest foot)}, for the numbers stamped after the turn."""
    faces = {}
    for name, edges in P.LOFTS.items():
        faces[name] = (S.loft(w, edges, T.LOFT, thick=3, marks=[(0, 10, BAND, 1, S.GRAY_WOOL)]),
                       min(p[1] for e in edges for p in e))
    return faces


def numbers(w, faces):
    """Each bunker's number on its north spur: 06 on Red's face, 07 on the image of it."""
    face, ylo = faces["north spur"]
    mark = lambda digits: [(14, 2, number(*digits), 2, S.OBSIDIAN)]
    S.inlay(w, face, mark(("0", "6")), ylo)
    image = {(int(a), y, int(b)): u for (x, y, z), u in face.items() for a, b in [P.SYM.point(x, z)]}
    S.inlay(w, image, mark(("0", "7")), ylo)


def boulders(w):
    """A few boulders on the field, each a lumpy ball of gray and light-gray wool sunk a third into the snow."""
    r = np.random.default_rng(90)
    for x, z, rad in P.BOULDERS:
        y0 = w.top(x, z)
        for dx in range(-rad - 1, rad + 2):
            for dz in range(-rad - 1, rad + 2):
                for dy in range(-rad, rad + 1):
                    k = (dx / (rad + 0.5)) ** 2 + (dz / (rad + 0.3)) ** 2 + (dy / (rad * 0.8 + 0.4)) ** 2
                    if k <= 1 + 0.25 * r.uniform(-1, 1):
                        block = (B.WOOL, 7) if r.random() < 0.6 else (B.WOOL, 8)
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
    boulders(w)
    bunker.build(w)
    faces = lofts(w)
    turn_world(w, "half", half)
    numbers(w, faces)
    w.fill(x0, 0, z0, x0 + sx - 1, 0, z0 + sz - 1, B.BEDROCK)
    O = P.objectives()
    O.stamp(w)
    w.save(out, "Sixes and Sevens", (0, 90, 0))
    problems = O.check(w)
    print("\n".join(problems) or "objectives read back clean")
    return w


if __name__ == "__main__":
    build(sys.argv[1])
