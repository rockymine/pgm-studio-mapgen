"""Seamworks' renders: the whole board, green's back corner and crust close, and two cutaways through the plan's
sections, A-A' down the slot and B-B' across green's side.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World
from pgmvox.read import render

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)
shots = [("30-iso-the-board.png", 2, "se", None, 0, None),
         ("31-iso-green-back.png", 6, "se", (0, 0, 70, 130), P.YS - 22, P.YS + 6),
         ("32-iso-green-crust-and-middle.png", 6, "se", (50, 0, 190, 100), P.YS - 22, P.YS + 6)]
for name, scale, corner, box, ymin, ymax in shots:
    render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, name), scale, corner, box, ymin, ymax)
    render.trim(os.path.join(out, name))
render.cutaway(w, os.path.join(out, "10-cutaway-a.png"), [(142, 0), (142, 114)], P.YS - 24, P.YS + 6, 6,
               title="A-A' down the slot, x 142")
render.cutaway(w, os.path.join(out, "11-cutaway-b.png"), [(0, 56), (174, 56)], P.YS - 24, P.YS + 6, 6,
               title="B-B' across green's side, z 56")
