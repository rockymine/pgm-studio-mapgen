"""Hoarfrost Reach's renders: the board from two corners, red's half, the skald, the strand, the lighthouse, the glacier
stair and the Ice Hall, the breakwater and the band; four cuts; two elevations; and the plan's names over the built
top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World, render
from pgmvox.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")


def iso(name, scale, corner, box=None, ymin=0, ymax=None):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax)
    render.trim(p)


iso("30-iso-board-se.png", 2, "se", ymin=36)
iso("31-iso-board-sw.png", 2, "sw", ymin=36)
iso("32-iso-red-half-se.png", 3, "se", (-88, -100, 87, -1), 44)
iso("33-iso-skald.png", 6, "se", (-40, -100, 40, -62), 66)
iso("34-iso-strand-and-breakwater.png", 5, "se", (-46, -66, 46, -14), 56)
iso("35-iso-lighthouse.png", 6, "se", (-90, -70, -52, -40), 52)
iso("36-iso-glacier-stair-and-hall.png", 5, "sw", (44, -94, 80, -42), 60)
iso("37-iso-band-and-floes.png", 4, "se", (-54, -26, 54, 26), 50)
render.cutaway(w, os.path.join(out, "10-section-causeways-z-55.png"), [(-88, -54.5), (87, -54.5)], 36, 112, 4,
               title="along x at z -55: the Lighthouse, the gap, the strand, the causeway, the shelf")
render.cutaway(w, os.path.join(out, "11-section-axis-x0.png"), [(0.5, -100), (0.5, 99)], 36, 112, 3,
               title="along z at x 0: skald to skald, through the strand, the breakwater and the band")
render.cutaway(w, os.path.join(out, "12-section-glacier-stair-x62.png"), [(62.5, -92), (62.5, -42)], 60, 112, 8,
               title="along z at x 62: the Ice Hall, the landing and the Glacier Stair down to the shelf")
render.cutaway(w, os.path.join(out, "13-section-lighthouse-x-78.png"), [(-78.5, -70), (-78.5, -42)], 60, 112, 10,
               title="along z at x -78: the lighthouse with its floors, ladder and glazed room")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-lighthouse-from-the-causeway.png"),
                 (-90, -64, -66, -46), 60, 112, look="west", scale=8)
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "52-elev-glacier-stair-from-the-shelf.png"),
                 (50, -96, 76, -44), 60, 112, look="east", scale=6)

R = P.build()
S = Sheet("Hoarfrost Reach - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks over the kill height, the plan's names and objectives over them, "
                 "the build zones outlined", symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=10)
m.objectives(P.objectives().markers())
for _, _, (x0, z0, x1, z1) in P.ZONES:
    m.ghost([(x0 - 0.5, z0 - 0.5), (x1 + 0.5, z0 - 0.5), (x1 + 0.5, z1 + 0.5), (x0 - 0.5, z1 + 0.5)], (230, 200, 60))
    m.ghost([(x0 - 0.5, -1 - z1 - 0.5), (x1 + 0.5, -1 - z1 - 0.5), (x1 + 0.5, -1 - z0 + 0.5), (x0 - 0.5, -1 - z0 + 0.5)],
            (230, 200, 60))
S.save(os.path.join(out, "05-topdown-annotated.png"))
