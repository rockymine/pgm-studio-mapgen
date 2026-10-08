"""Lantern Karst's renders, named as the original's are so the two can be set side by side: the board from two
corners, red's half, the spawn, the Pillar, the Store, the hub, the middle; four cuts; two elevations; and the
plan's names over the built top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan  # noqa: F401  (puts the library on the path)
from plan import KILL_Y, PLACES, ZONES, build, objectives
from pgmvox import World, render
from pgmvox.sketch import Sheet

build_dir, root = sys.argv[1], sys.argv[2]
w = World.load(build_dir)
out = os.path.join(root, "renders")


def iso(name, scale, corner, box=None, ymin=0, ymax=None):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax)
    render.trim(p)


iso("30-iso-board-se.png", 2, "se", ymin=20)
iso("31-iso-board-nw.png", 2, "nw", ymin=20)
iso("32-iso-red-half-sw.png", 3, "sw", (-112, -128, 111, -1), 20)
iso("33-iso-spawn.png", 6, "se", (-26, -124, 26, -74), 55)
iso("34-iso-pillar-and-arms.png", 5, "se", (-98, -104, -28, -54), 20)
iso("35-iso-store-and-road.png", 5, "sw", (26, -116, 76, -34), 40)
iso("36-iso-hub-and-gate.png", 5, "se", (-40, -84, 40, -10), 45)
iso("37-iso-middle-and-steps.png", 4, "se", (-76, -52, 76, 14), 40)

render.cutaway(w, os.path.join(out, "10-section-spawn-to-spawn-x0.png"), [(0.5, -127), (0.5, 127)], 20, 96, 4,
               title="spawn to spawn, along z at x 0")
render.cutaway(w, os.path.join(out, "11-section-pillar-z-94.png"), [(-100, -93.5), (-25, -93.5)], 20, 96, 6,
               title="the Pillar between its Arms, along x at z -94")
render.cutaway(w, os.path.join(out, "12-section-ledges-z-79.png"), [(-100, -78.5), (-25, -78.5)], 20, 96, 6,
               title="the Ledges under the Long Terrace, along x at z -79")
render.cutaway(w, os.path.join(out, "13-section-store-road-x56.png"), [(56.5, -116), (56.5, -20)], 20, 96, 6,
               title="the Store Road, along z at x 56")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-store-from-the-road.png"),
                 (42, -114, 71, -90), 64, 92, look="north", scale=8)
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "52-elev-pillar-from-the-terrace.png"),
                 (-96, -100, -28, -74), 40, 92, look="north", scale=6)

R, _, _ = build()
S = Sheet("Lantern Karst - as built (port)")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=3, title="FROM ABOVE",
          legend="the built world's top blocks over the kill height, the plan's names and objectives over them, "
                 "the build zones outlined", symmetry=R.symmetry)
m.built(w, ymin=KILL_Y)
for name, (x, z) in PLACES:
    m.place(x, z, name, size=11)
m.objectives(objectives().markers())
for _, _, (x0, z0, x1, z1) in ZONES:
    m.ghost([(x0 - 0.5, z0 - 0.5), (x1 + 0.5, z0 - 0.5), (x1 + 0.5, z1 + 0.5), (x0 - 0.5, z1 + 0.5)],
            (230, 200, 60))
    m.ghost([(-1 - x1 - 0.5, -1 - z1 - 0.5), (-1 - x0 + 0.5, -1 - z1 - 0.5), (-1 - x0 + 0.5, -1 - z0 + 0.5),
             (-1 - x1 - 0.5, -1 - z0 + 0.5)], (230, 200, 60))
S.save(os.path.join(out, "05-topdown-annotated.png"))
