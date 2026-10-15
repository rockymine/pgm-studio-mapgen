"""Coldbore's renders: the board from two corners, red's station close, the station x-rayed, and sections down
the gate's axis and across the reactor.

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
os.makedirs(out, exist_ok=True)


def iso(name, **kw):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, **kw)
    render.trim(p)


iso("10-iso-board-se.png", scale=2, corner="se", ymin=10)
iso("11-iso-board-nw.png", scale=2, corner="nw", ymin=10)
iso("20-iso-red-front.png", scale=3, corner="nw", box=(-75, 0, 74, 99), ymin=40)
iso("21-iso-red-gate.png", scale=6, corner="nw", box=(-30, 28, 30, 70), ymin=64)
iso("22-xray-red-station.png", scale=4, corner="nw", box=(-40, 0, 45, 99), ymin=24, ymax=112, xray=True)
iso("23-xray-red-cave.png", scale=6, corner="nw", box=(-68, 0, -10, 40), ymin=16, ymax=50, xray=True)
iso("24-iso-fissure.png", scale=4, corner="ne", box=(-45, -22, 45, 22), ymin=14)
iso("25-iso-red-plateau.png", scale=6, corner="nw", box=(0, 55, 50, 99), ymin=88)
render.cutaway(w, os.path.join(out, "30-section-gate-axis.png"), [(0, -40), (0, 99)], ymin=12, ymax=112, scale=4,
               title="down the gate's axis, x 0: the fissure, the gallery, the stair, the vault under the reactor, "
                     "the vestibule, the ramp, the turn hall")
render.cutaway(w, os.path.join(out, "31-section-reactor.png"), [(-36, 55), (30, 55)], ymin=24, ymax=112, scale=4,
               title="across the reactor, z 55: the barracks, the vent bay, the core over its well and the vault "
                     "under it, the stair core")
render.cutaway(w, os.path.join(out, "32-section-cave.png"), [(-66, 20), (-12, 20)], ymin=14, ymax=80, scale=4,
               title="along the cave, z 20, from the west flank to the gallery")
