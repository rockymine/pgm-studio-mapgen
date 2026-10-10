"""Abbeymoor's renders: the island from two corners, red's half, the abbey hill with the nave cut away and its crypt, the village and the
green, Hall Farm, the bog and the Standing Stones; cuts across the crypt and along the passage; an x-ray of what is underground; two
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


def iso(name, scale, corner, box=None, ymin=0, ymax=None, xray=False):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax, xray=xray)
    render.trim(p)


iso("30-iso-island-se.png", 2, "se", ymin=50)
iso("31-iso-island-sw.png", 2, "sw", ymin=50)
iso("32-iso-red-half-se.png", 3, "se", (-100, -132, 99, -1), 56)
iso("33-iso-abbey-hill-se.png", 6, "se", (-62, -84, -20, -58), 66, 96)
iso("34-iso-abbey-from-the-east.png", 6, "sw", (-62, -84, -20, -58), 66, 96)
iso("35-iso-village-and-green.png", 5, "se", (0, -96, 62, -42), 62, 90)
iso("36-iso-hall-farm.png", 6, "se", (-40, -131, 40, -96), 62, 90)
iso("37-iso-bog-and-stones.png", 4, "se", (-60, -34, 60, 0), 54, 80)
iso("38-iso-peat-cuttings-and-gatehouse.png", 6, "se", (-50, -60, -10, -26), 58, 86)
iso("40-xray-crypt-and-passage.png", 4, "se", (-60, -90, 30, -40), 50, 100, xray=True)
render.cutaway(w, os.path.join(out, "10-section-abbey-z-72.png"), [(-70, -72.5), (-20, -72.5)], 54, 100, 8,
               title="along x at z -72: the moor, the hill, the nave with Monument A over its dais, the crypt under it, the Night Stair")
render.cutaway(w, os.path.join(out, "11-section-passage-z-61.png"), [(-56, -60.5), (28, -60.5)], 52, 80, 5,
               title="along x at z -61: the crypt's corner, the passage's three flights down, the valley, the cellar stair into the Tithe Barn")
render.cutaway(w, os.path.join(out, "12-section-axis-x-42.png"), [(-42.5, -131), (-42.5, 0)], 50, 100, 4,
               title="along z at x -42: the ridge, Hall Farm, the abbey hill with its crypt, the moor down into the bog")
render.cutaway(w, os.path.join(out, "13-section-green-z-70.png"), [(0, -70.5), (62, -70.5)], 56, 90, 8,
               title="along x at z -70: the moor, the village green with Monument B, the orchard, the beck")
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "50-elev-abbey-from-the-moor.png"),
                 (-62, -82, -22, -60), 62, 100, look="north", scale=8)
render.elevation(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "51-elev-green-and-monument-b.png"),
                 (10, -86, 52, -56), 60, 84, look="north", scale=8)

R = P.build()
S = Sheet("Abbeymoor - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=4, title="FROM ABOVE",
          legend="the built world's top blocks over the kill height, the plan's names and objectives over them", symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=9)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))
