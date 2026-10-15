"""The yard from the south-east and the south-west, and each row from the side."""
import os
import sys

from pgmvox import World
from pgmvox.read import render

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-the-yard-se.png"), 3, "se", ymin=10)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-the-yard-sw.png"), 3, "sw", ymin=10)
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "40-side-back-row.png"), (-140, -60, 139, -1), 10, 100,
                 look="north", scale=3)
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "41-side-front-row.png"), (-140, 0, 139, 59), 10, 100,
                 look="north", scale=3)
for n in os.listdir(out):
    if n.startswith("3"):
        render.trim(os.path.join(out, n))
