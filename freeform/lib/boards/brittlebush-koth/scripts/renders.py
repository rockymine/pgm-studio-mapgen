"""Brittlebush KotH's renders: the board from two corners, red's quadrant, the keep and its house, the middle, an
edge close up, a section along red's diagonal, and the plan's names over the built top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World, render
from pgmvox.sketch import TEAM, Sheet

w = World.load(sys.argv[1])
out = os.path.join(sys.argv[2], "renders")


def iso(name, scale, corner, box=None, ymin=0):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin)
    render.trim(p)


iso("30-iso-board-se.png", 4, "se")
iso("31-iso-board-nw.png", 4, "nw")
iso("32-iso-red-quadrant-se.png", 7, "se", (P.X_MIN, P.Z_MIN, -1, -1))
iso("33-iso-keep-and-house-se.png", 12, "se", (-65, -65, -45, -45), 12)
iso("34-iso-the-dais-se.png", 9, "se", (-22, -22, 21, 21), 2)
iso("35-iso-an-edge-nw.png", 12, "nw", (-46, -65, -24, -50))
for corner in ("se", "sw", "nw", "ne"):                     # the whole board, close enough to read
    iso(f"40-iso-full-{corner}.png", 6, corner)
render.cutaway(w, os.path.join(out, "10-section-red-diagonal.png"), [(-65, -65), (0, 0)], 0, 50, 6,
               title="along red's diagonal, from the keep to the Dais")

S = Sheet("Brittlebush KotH - as built")
m = S.map(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks; white squares the five hills, S the spawns, G golden apples, A arrows")
m.built(w, ymin=0)
for hid, name, (x0, z0, x1, z1), points, hy in P.HILLS:
    m.rect(x0, z0, x1, z1, outline=(250, 250, 250), width=3)
    m.label((x0 + x1) / 2, (z0 + z1) / 2 - 7, name, size=11)
for i, colour in enumerate(("red", "blue", "green", "yellow")):
    m.marker(*P.spawn_cell(i), "S", TEAM[colour])
for x, z in P.APPLES:
    m.marker(x, z, "G", (230, 190, 40))
for x, z in P.ARROWS:
    m.marker(x, z, "A", (150, 150, 160))
S.save(os.path.join(out, "05-topdown-annotated.png"))
