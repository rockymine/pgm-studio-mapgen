"""Brassmoor Works' renders: the board from two corners, red's half, the Gatehouse and the Yard, each wool room
with its lane, the band and the crane, cuts across a room and from spawn to band, an elevation of the Boiler House,
and the plan's names over the built top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
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
iso("32-iso-red-half-sw.png", 3, "sw", (-88, -112, 87, -1), 20)
iso("33-iso-gatehouse-and-yard-se.png", 5, "se", (-30, -102, 30, -56), 55)
iso("34-iso-boiler-house-and-gantry-se.png", 5, "se", (-82, -94, -26, -36), 50)
iso("35-iso-water-tower-and-spur-sw.png", 5, "sw", (24, -94, 80, -36), 50)
iso("36-iso-band-and-crane-se.png", 4, "se", (-44, -26, 44, 26), 50)
render.cutaway(w, os.path.join(out, "10-section-boiler-to-tower-z-78.png"), [(-88, -77.5), (87, -77.5)], 20, 100, 4,
               title="along x at z -78: the Boiler House, the bedrock line, the Gantry, the Yard, the Spur, the Water Tower")
render.cutaway(w, os.path.join(out, "11-section-spawn-to-band-x-34.png"), [(-33.5, -112), (-33.5, 111)], 20, 100, 4,
               title="along z at x -34: the Gantry, the Yard, the West Quay, the band, blue's Quay and Yard")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-boiler-house-from-the-gantry.png"),
                 (-80, -92, -40, -72), 60, 100, look="west", scale=6)

R = P.build()
S = Sheet("Brassmoor Works - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=3, title="FROM ABOVE",
          legend="the built world's top blocks over the kill height, the plan's names and objectives over them",
          symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
