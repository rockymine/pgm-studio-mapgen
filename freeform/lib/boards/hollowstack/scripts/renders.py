"""Hollowstack from two corners, and cut through its storeys: the whole board along its middle, the light well and
the pond, the keep well from the yard to the Undercroft, the Vault and the gallery, the chasm with every mouth.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

from pgmvox import World  # noqa: E402
from pgmvox.read import render  # noqa: E402

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-se.png"), 2, "se")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-nw.png"), 2, "nw")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "32-xray-blue.png"), 3, "se", (0, -28, 95, 27), 0, 108,
           xray=True)
render.cutaway(w, os.path.join(out, "40-cut-middle.png"), [(-96, 0.5), (95, 0.5)], ymin=0, ymax=112, scale=4,
               title="z 0 west to east: red's wall, the chasm, blue's wall; the Tops, the Workings, the Underwood, the "
               "Undercroft, the Deep")
render.cutaway(w, os.path.join(out, "41-cut-wells.png"), [(0, -8.5), (95, -8.5)], ymin=0, ymax=112, scale=5,
               title="z -9: the light well and the plunge from the Tops into the Underwood's waters")
render.cutaway(w, os.path.join(out, "42-cut-keep-well.png"), [(85.5, -26), (85.5, 26)], ymin=30, ymax=112, scale=5,
               title="x 85: the keep well from the yard down through the Workings and the postern to the Undercroft")
render.cutaway(w, os.path.join(out, "43-cut-vault.png"), [(0, 12.5), (95, 12.5)], ymin=10, ymax=60, scale=6,
               title="z 12: the Undercroft from its balcony on the chasm back to the Vault; the grotto under it")
render.cutaway(w, os.path.join(out, "44-cut-chasm.png"), [(-30, 0.5), (30, 0.5)], ymin=0, ymax=112, scale=6,
               title="the chasm at z 0: the stubs at the brink, the Underwood's mouths and the gallery fronts")
for n in os.listdir(out):
    if n.startswith("3"):
        render.trim(os.path.join(out, n))
