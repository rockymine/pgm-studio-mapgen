"""Brittlebush III's renders: the board from two corners, red's part, its spawn, its wool's tower, the three
under-sections, and the built top-down with the plan's objectives over it.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World, render
from pgmvox.sketch import TEAM, Sheet

w = World.load(sys.argv[1])
out = os.path.join(sys.argv[2], "renders")
lo, hi = w.x0, w.x0 + w.sx - 1


def iso(name, scale, corner, box=None, ymin=0):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin)
    render.trim(p)


iso("30-iso-board-se.png", 3, "se")
iso("31-iso-board-nw.png", 3, "nw")
iso("32-iso-red-part-se.png", 6, "se", (-20, lo, 42, -10))
iso("33-iso-red-spawn-se.png", 12, "se", (18, -62, 42, -28), 8)
iso("34-iso-red-wool-sw.png", 10, "sw", (-14, lo, 22, -70), 8)
iso("35-iso-the-middle-se.png", 8, "se", (-25, -25, 24, 24), 4)
iso("36-iso-middle-island-under-se.png", 14, "se", (-16, -24, 4, -6), 4)
iso("37-iso-tunnel-se.png", 14, "se", (-18, -44, 2, -26), 4)
iso("38-iso-approach-under-se.png", 14, "se", (-18, -64, 2, -46), 4)

S = Sheet("Brittlebush III - as built")
m = S.map(lo, lo, hi, hi, scale=3, title="FROM ABOVE",
          legend="the built world's top blocks; S the spawns, W the monuments, w the wools in their rooms")
m.built(w, ymin=0)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
