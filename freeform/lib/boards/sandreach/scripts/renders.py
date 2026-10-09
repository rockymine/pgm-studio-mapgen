"""Sandreach's renders: the whole board from four corners, red's half, where the made yard meets the grown meadow,
the island off the landing, the wool's house, and the built top-down with the objectives over it.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World, render
from pgmvox.sketch import Sheet

w = World.load(sys.argv[1])
out = os.path.join(sys.argv[2], "renders")


def iso(name, scale, corner, box=None, ymin=0):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin)
    render.trim(p)


for corner in ("se", "sw", "nw", "ne"):
    iso(f"30-iso-full-{corner}.png", 4, corner)
iso("32-iso-red-half-se.png", 5, "se", (P.X_MIN, P.Z_MIN, P.X_MAX, -1))
iso("33-iso-yard-meets-meadow-se.png", 9, "se", (-12, -82, 50, -30))
iso("34-iso-island-and-landing-sw.png", 9, "sw", (-60, -50, -20, -2))
iso("35-iso-wool-house-se.png", 12, "se", (-60, -80, -40, -55), 10)
S = Sheet("Sandreach - as built")
m = S.map(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=3, title="FROM ABOVE",
          legend="the built world's top blocks; S the spawns, W the monuments, w the wools in their houses")
m.built(w, ymin=0)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
