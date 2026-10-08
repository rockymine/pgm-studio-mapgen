"""The parts from above the south-west corner, and close."""
import os
import sys

from pgmvox import World, render

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-the-parts.png"), 4, "sw", ymin=9)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-the-houses.png"), 8, "sw", (-4, -4, 96, 42), 9, 40)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "32-iso-the-houses-ne.png"), 8, "ne", (-4, -4, 96, 42), 9, 40)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "33-iso-mass-and-carpets.png"), 6, "sw", (-4, 44, 96, 72), 9, 40)
for n in os.listdir(out):
    if n.startswith("3"):
        render.trim(os.path.join(out, n))
