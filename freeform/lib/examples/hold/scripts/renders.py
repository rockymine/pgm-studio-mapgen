"""Knuckle Hold from two corners, and cut through each of its floors: the Shelf over the meadow, the arch over the
river, the cave from its mouth to the cavern and the hold from the cistern past the well to the crypt; then
everything under a roof, x-rayed; and the arch from the south, through the gap between the ridges."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pgmvox import World  # noqa: E402
from pgmvox.read import render  # noqa: E402

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-se.png"), 3, "se")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-ne.png"), 3, "ne")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "32-iso-arch.png"), 6, "sw", (50, 108, 112, 140), 30)
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "44-side-arch.png"), (50, 116, 112, 128), 30, 64,
                 look="north", scale=8)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "33-iso-shelf.png"), 5, "se", (10, 24, 90, 92), 34)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "34-xray.png"), 4, "se", (20, 30, 145, 105), 14, 48,
           xray=True)
render.cutaway(w, os.path.join(out, "40-cut-shelf.png"), [(8, 52), (100, 52)], ymin=14, ymax=84, scale=6,
               title="z 52 west to east: the Shelf on the Knuckle, out over the meadow, its stream falling")
render.cutaway(w, os.path.join(out, "41-cut-arch.png"), [(50, 122), (112, 122)], ymin=24, ymax=64, scale=8,
               title="z 122 west to east: the arch over the river")
render.cutaway(w, os.path.join(out, "42-cut-cave.png"), [(66, 73.5), (53, 71.5), (46, 67.5), (36, 60.5), (24, 60.5)],
               ymin=20, ymax=84, scale=8, title="the cave from its mouth under the Shelf down to the cavern")
render.cutaway(w, os.path.join(out, "43-cut-hold.png"), [(118.5, 34), (118.5, 91.5), (94, 91.5)], ymin=14, ymax=50,
               scale=8, title="x 118: the cistern, the undercroft under the well, then west into the crypt")
for n in os.listdir(out):
    if n.startswith("3"):
        render.trim(os.path.join(out, n))
