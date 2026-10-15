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
iso("21-iso-red-gate.png", scale=6, corner="nw", box=(-64, 28, -18, 66), ymin=64)
iso("26-iso-red-generator-house.png", scale=6, corner="nw", box=(10, 28, 56, 66), ymin=64)
iso("22-xray-red-station.png", scale=4, corner="nw", box=(-66, 0, 48, 99), ymin=36, ymax=104, xray=True)
iso("23-xray-red-cave.png", scale=6, corner="nw", box=(-68, 0, -10, 40), ymin=16, ymax=50, xray=True)
iso("24-iso-fissure.png", scale=4, corner="ne", box=(-75, -22, 74, 22), ymin=14)
iso("25-iso-red-plateau.png", scale=5, corner="nw", box=(-24, 56, 56, 99), ymin=92)
iso("27-iso-red-plateau-west.png", scale=5, corner="nw", box=(-75, 56, -20, 99), ymin=92)
render.cutaway(w, os.path.join(out, "30-section-hall-axis.png"), [(0, -20), (0, 99)], ymin=12, ymax=120, scale=4,
               title="down the reactor hall's axis, x 0: the fissure, the gallery, the ramp's corridor, the hall's ramp, "
                     "the core over its pit, the balcony, the dish on the yard")
render.cutaway(w, os.path.join(out, "31-section-across-station.png"), [(-66, 81), (48, 81)], ymin=36, ymax=120,
               scale=4, title="across the station, z 81: the armoury, the entrance hall, the west corridor, the reactor "
                              "hall and its balcony, the spawn and iron rooms over the vault")
render.cutaway(w, os.path.join(out, "32-section-cave.png"), [(-66, 20), (-12, 20)], ymin=14, ymax=80, scale=4,
               title="along the cave, z 20, from the west flank to the gallery's ramp")
render.cutaway(w, os.path.join(out, "33-section-store.png"), [(28, 20), (28, 70)], ymin=40, ymax=110, scale=5,
               title="through the fallen ceiling, x 28: the snowfield, the hole, the rubble under it, the generator "
                     "house's link")
