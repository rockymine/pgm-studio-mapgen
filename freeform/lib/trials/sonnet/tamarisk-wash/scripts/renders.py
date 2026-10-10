"""Tamarisk Wash's renders: the basin from two corners, red's half, the kasbah, the Souk and the Sunstone, Table Rock
and the arch, the wash and its aqueduct, the oasis, the caravanserai; the underground in x-ray; three cuts; an
elevation of the wash's wall; and the plan's names over the built top-down.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import numpy as np

import plan as P
from pgmvox import World, render
from pgmvox.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")


def iso(name, scale, corner, box=None, ymin=0, ymax=None, xray=False):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax, xray)
    render.trim(p)


iso("30-iso-board-se.png", 2, "se", ymin=40)
iso("31-iso-board-sw.png", 2, "sw", ymin=40)
iso("32-iso-red-half.png", 3, "se", (-100, -64, -1, 63), 44)
iso("33-iso-kasbah.png", 6, "se", (-100, -20, -72, 10), 60)
iso("34-iso-souk-and-sunstone.png", 6, "se", (-82, 2, -44, 40), 58)
iso("35-iso-table-rock-and-arch.png", 5, "sw", (-84, -52, -14, -10), 58)
iso("36-iso-wash-and-aqueduct.png", 4, "se", (-40, -24, 40, 26), 40)
iso("37-iso-oasis.png", 5, "se", (-84, 30, -46, 62), 55)
iso("38-iso-caravanserai.png", 6, "se", (-52, 18, -22, 46), 58)
# the underground in x-ray: clear everything over the plan's ground first
under = w.ids.copy()
for i in range(w.sx):
    for k in range(w.sz):
        under[i, int(P.land().H[i, k]) - 2:, k] = 0
p = os.path.join(out, "40-xray-qanat-and-mine.png")
render.iso(under, w.dat, w.x0, w.z0, p, 4, "se", (-80, -40, -4, 40), 40, 74, True)
render.trim(p)
render.cutaway(w, os.path.join(out, "10-section-z-28-table-rock.png"), [(-100, -27.5), (99, -27.5)], 30, 100, 3,
               title="along x at z -28: the plateau, Table Rock, the north ghats, the wash, and the mirror")
render.cutaway(w, os.path.join(out, "11-section-z24-souk-serai.png"), [(-100, 24.5), (99, 24.5)], 30, 100, 3,
               title="along x at z 24: the souk, the caravanserai, the south ghats, the wash")
render.cutaway(w, os.path.join(out, "12-section-qanat.png"), [(q[0] + 0.5, q[2] + 0.5) for q in P.QANAT[:-1]] + [(-66.5, 28.5)], 40, 66, 6,
               title="the qanat, from the wash to the cistern under the souk")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-wash-wall-from-the-floor.png"),
                 (-30, -40, -6, 40), 40, 70, look="west", scale=6)

R = P.build()
S = Sheet("Tamarisk Wash - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=5, title="FROM ABOVE",
          legend="the built world's top blocks; the plan's names, objectives and building footprints over them",
          symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for b in P.houses().values():
    xs = [c[0] for c in b["cells"]]
    zs = [c[1] for c in b["cells"]]
    m.rect(min(xs), min(zs), max(xs), max(zs), outline=(255, 255, 255), both=True)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
