"""Tidewell Canals' renders: the quarter from two corners, the Campo and its gallery, a fish market under its
loggia, red's customs house and district, cuts spawn to spawn and flank to flank, and the plan's names over the
built top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World, render
from pgmvox.sketch import Sheet

build_dir, root = sys.argv[1], sys.argv[2]
w = World.load(build_dir)
out = os.path.join(root, "renders")


def iso(name, scale, corner, box=None, ymin=0, ymax=None):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax)
    render.trim(p)


iso("30-iso-board-se.png", 2, "se", ymin=30)
iso("31-iso-board-nw.png", 2, "nw", ymin=30)
iso("32-iso-campo-se.png", 5, "se", (-24, -30, 23, 29), 34)
iso("33-iso-north-market-sw.png", 5, "sw", (-24, -64, 23, -24), 34)
iso("34-iso-customs-and-sestiere-se.png", 4, "se", (-80, -40, -14, 39), 34)
render.cutaway(w, os.path.join(out, "10-section-spawn-to-spawn-z-1.png"), [(-80, -0.5), (79, -0.5)], 32, 60, 4,
               title="along x at z -1: the customs houses, the columns, the Grand Canals' bridges, the Campo and its pad")
render.cutaway(w, os.path.join(out, "11-section-flank-to-flank-x-8.png"), [(-7.5, -64), (-7.5, 63)], 32, 60, 4,
               title="along z at x -8: the north loggia and its pad, the Rio's bridge, the gallery over the arcade, the Campo")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-campo-from-the-west.png"),
                 (-14, -27, 13, 26), 38, 60, look="east", scale=6)

R = P.build()
S = Sheet("Tidewell Canals - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks; the plan's names, hills and spawns over them", symmetry=R.symmetry)
m.built(w, ymin=30)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
