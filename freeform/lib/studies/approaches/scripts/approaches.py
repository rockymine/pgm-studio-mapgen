"""The studio's eight goal approaches turned on their side: each form a chain of chambers cut into one block of rock,
stepping down from its host to its room, the voids it leaves cut to the void, its defence walls in bedrock. Each is
read back from its cells, counted for its ways in, and walked to its room in a long match's four phases under two
sets of rules: CTW's usual, where every block breaks and building reaches over the rock, and held, where only
the kit's blocks break and the build height is the rock's own top.

    python3 approaches.py <build-dir>          # renders into ../renders, the readings into ../renders/readings.txt
"""
import os
import sys

import numpy as np

from pgmvox import B, World                                                   # noqa: E402
from pgmvox.built import chambers as CH                                       # noqa: E402
from pgmvox.plan import approach as AP                                        # noqa: E402
from pgmvox.read import late, render                                          # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders")
CELL, DROP, TOP, ROCK_TOP = 7, 6, 60, 72
LANE = 64                                         # each form in a square of rock this wide, four to a row
SIZES = {"I": (3, 1), "L": (3, 3), "Z": (2, 2), "scythe": (3, 1), "clamp": (3, 1), "U": (3, 1), "H": (3, 1),
         "donut": (3, 2)}


def build():
    w = World(0, 0, 4 * LANE, 2 * LANE, 112)
    w.ids[:, 1:ROCK_TOP + 1, :] = B.STONE
    w.ids[:, 0, :] = B.BEDROCK
    w.ids[:, ROCK_TOP, :] = B.GRASS
    laid = {}
    for n, form in enumerate(AP.FORMS):
        a = AP.emit(form, *SIZES[form])
        cells = a.cells() | a.host()
        i0, j0 = min(c[0] for c in cells), min(c[1] for c in cells)
        i1, j1 = max(c[0] for c in cells), max(c[1] for c in cells)
        ox = (n % 4) * LANE + (LANE - (i1 - i0 + 1) * CELL) // 2 - i0 * CELL
        oz = (n // 4) * LANE + (LANE - (j1 - j0 + 1) * CELL) // 2 - j0 * CELL
        got = CH.lay(w, a, (ox, oz), TOP, CELL, DROP, np.random.default_rng(n))
        hx, hy, hz = CH.centre(got, got["host"][0])
        for y in range(hy, ROCK_TOP + 1):                         # a well from the host up to the open top
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    w.set(hx + dx, y, hz + dz, B.AIR)
        for y in range(hy - 1, ROCK_TOP + 1):
            w.set(hx + 2, y, hz, B.LADDER, 4)
        laid[form] = (a, got)
    return w, laid


def door(a, got):
    """The openings into the room: every block of air on the edges the room shares with its neighbours."""
    cells = a.cells()
    out = []
    x0, z0 = got["at"]
    n = got["cell"]
    for c in a.room:
        f = got["floors"][c]
        for d in AP.DIRS:
            m = (c[0] + d[0], c[1] + d[1])
            if m not in cells:
                continue
            for k in range(n):
                u = (n - 1 if d == (1, 0) else 0) if d[0] else k
                v = (n - 1 if d == (0, 1) else 0) if d[1] else k
                for y in range(f + 1, f + 9):
                    out.append((x0 + c[0] * n + u, y, z0 + c[1] * n + v))
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    w, laid = build()
    w.save(sys.argv[1], "approaches", (LANE // 2, ROCK_TOP + 2, LANE // 2))
    lines = ["form     reads    doors  walls  shafts", ""]
    for form, (a, got) in laid.items():
        lines.append(f"{form:8} {AP.classify(a.cells(), a.room):8} {AP.doors(a):5}  {len(got['walls']):5}  "
                     f"{len(got['shafts']):6}")
    lines.append("")
    zone = np.zeros((w.sx, w.sz), bool)
    rows = []
    for form, (a, got) in laid.items():
        start = CH.centre(got, got["host"][0])
        room = CH.centre(got, sorted(a.room)[0])
        cells = door(a, got)
        rows.append((f"{form} - usual rules", late.phases(w, start, room, zone, ROCK_TOP + 8, door=cells)))
        rows.append((f"{form} - held rules", late.phases(w, start, room, zone, ROCK_TOP, door=cells,
                                                         breakable=set())))
    lines.append(late.table(rows))
    text = "\n".join(lines)
    print(text)
    open(os.path.join(OUT, "readings.txt"), "w").write(text + "\n")
    with open(os.path.join(OUT, "plans.txt"), "w") as f:
        for form, (a, _) in laid.items():
            f.write(f"{AP.describe(a)}\n{AP.ascii(a)}\n\n")
