"""Slatefold's renders: the board from two corners, red's half, the quarry office, the row and the chapel, the cart yard and
the gantry, the quarry and the Kiln, the winding path and the bench, the dressing floor and the band; four cuts; two
elevations; and the plan's names over the built top-down.

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
iso("32-iso-red-half-se.png", 3, "se", (-88, -108, 79, -1), 44)
iso("33-iso-red-half-sw.png", 3, "sw", (-88, -108, 79, -1), 44)
iso("34-iso-spawn-terrace.png", 6, "se", (-40, -108, 34, -78), 66)
iso("35-iso-row-and-chapel.png", 6, "se", (-50, -82, 20, -62), 62)
iso("36-iso-yard-and-gantry.png", 6, "se", (-52, -64, 44, -44), 58)
iso("37-iso-quarry-and-kiln.png", 6, "sw", (28, -80, 72, -52), 52)
iso("38-iso-winding-path-and-bench.png", 6, "se", (-88, -102, -44, -58), 62)
iso("39-iso-dressing-floor.png", 5, "se", (-56, -50, 46, -10), 54)
iso("40-iso-band-and-fronts.png", 4, "se", (-60, -30, 60, 30), 46)
render.cutaway(w, os.path.join(out, "10-section-yard-gantry-z-58.png"), [(-52, -57.5), (70, -57.5)], 36, 108, 4,
               title="along x at z -58: the cart yard, the Cart Gantry's flights and wall, the Quarry Floor")
render.cutaway(w, os.path.join(out, "11-section-axis-x0.png"), [(0.5, -108), (0.5, 107)], 36, 108, 3,
               title="along z at x 0: spawn to spawn, down the four terraces and across the band")
render.cutaway(w, os.path.join(out, "12-section-winding-path-z-81.png"), [(-88, -81.5), (-40, -81.5)], 56, 108, 8,
               title="along x at z -82: the High Bench, the flight, the second landing with its wall")
render.cutaway(w, os.path.join(out, "13-section-kiln-z-68.png"), [(30, -67.5), (70, -67.5)], 40, 90, 8,
               title="along x at z -68: the Quarry Floor, the Pit, the Kiln room with its door")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-kiln-from-the-pit.png"),
                 (46, -80, 72, -56), 50, 96, look="east", scale=8)
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "51-elev-winding-house-from-the-path.png"),
                 (-88, -100, -56, -76), 74, 110, look="west", scale=8)

R = P.build()
S = Sheet("Slatefold - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks over the kill height, the plan's names and objectives over them, the build zones outlined",
          symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=9)
m.objectives(P.objectives().markers())
for _, _, (x0, z0, x1, z1) in P.ZONES:
    m.ghost([(x0 - 0.5, z0 - 0.5), (x1 + 0.5, z0 - 0.5), (x1 + 0.5, z1 + 0.5), (x0 - 0.5, z1 + 0.5)], (230, 200, 60))
    m.ghost([(x0 - 0.5, -1 - z1 - 0.5), (x1 + 0.5, -1 - z1 - 0.5), (x1 + 0.5, -1 - z0 + 0.5), (x0 - 0.5, -1 - z0 + 0.5)], (230, 200, 60))
S.save(os.path.join(out, "05-topdown-annotated.png"))
