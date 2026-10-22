"""Chantry Gill from two corners and from above, and cut through each of its floors: the gill under the brig, the
shelter climbing the chimney onto the bench, the adit from the gill floor west into the crypt and up the ladder into
the nave, and the timber bridge from the spawn hall onto the bench; then the blue half under its roofs, x-rayed.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox import World  # noqa: E402
from pgmvox.read import render  # noqa: E402

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-se.png"), 2, "se")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-nw.png"), 2, "nw")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "32-iso-blue.png"), 3, "se", (-90, 0, 89, 129))
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "33-xray-blue.png"), 3, "se", (-40, 0, 60, 110), 20, 70,
           xray=True)
render.cutaway(w, os.path.join(out, "40-cut-brig.png"), [(16, 38), (56, 38)], ymin=24, ymax=60, scale=8,
               title="z 38 west to east: the gill floor and the brig over it, the tarn beyond")
render.cutaway(w, os.path.join(out, "41-cut-shelter.png"), [(30, 72.5), (39, 73), (43, 74), (47, 76), (47, 90)],
               ymin=26, ymax=70, scale=8, title="the shelter from the gill floor, up the chimney onto the bench")
render.cutaway(w, os.path.join(out, "42-cut-adit.png"),
               [(44, 75), (37, 75), (33, 76), (24, 75), (14, 74), (6, 74), (-5, 74), (-20, 74)],
               ymin=20, ymax=64, scale=6, title="the adit from the gill floor west into the crypt, the ladder up into "
               "the nave")
render.cutaway(w, os.path.join(out, "43-cut-bridge.png"), [(-6, 92.5), (60, 92.5)], ymin=26, ymax=70, scale=6,
               title="z 92 west to east: the spawn hall, the timber bridge over the gill onto the bench")
render.cutaway(w, os.path.join(out, "44-cut-scar.png"), [(54, 30), (54, 120)], ymin=20, ymax=80, scale=6,
               title="x 54 north to south: the tarn, the brow, the bench and the plateau")
for n in os.listdir(out):
    if n.startswith("3"):
        render.trim(os.path.join(out, n))
