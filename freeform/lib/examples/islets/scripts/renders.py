"""Islets' renders: the board among its mountains, and the islands close."""
import os
import sys

from pgmvox import World, render

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-the-board.png"), 2, "sw")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-the-islands.png"), 6, "sw", (-30, -16, 29, 15), 15, 45)
render.cutaway(w, os.path.join(out, "10-cutaway-x.png"), [(-32, 0), (32, 0)], 0, 45, 6, title="along x at z 0")
for n in ("30-iso-the-board.png", "31-iso-the-islands.png"):
    render.trim(os.path.join(out, n))
