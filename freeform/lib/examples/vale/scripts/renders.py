"""The Vale from the south-west and the north-east, the canyon walls close, and the board annotated from above."""
import os
import sys

from land import BUTTE, CANYON, ISLAND, RIVER, ROAD, SPIRE, TERRACES
from pgmvox import World, render
from pgmvox.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-sw.png"), 3, "sw")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "31-iso-ne.png"), 3, "ne")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "32-iso-canyon.png"), 7, "sw", (-30, -100, 20, -30), 20, 110)
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "33-iso-island.png"), 7, "sw", (-82, -40, -42, 0), 40, 110)
for n in ("30-iso-sw.png", "31-iso-ne.png", "32-iso-canyon.png", "33-iso-island.png"):
    render.trim(os.path.join(out, n))
S = Sheet("The Vale - as built")
m = S.map(-100, -100, 99, 99, scale=4, title="FROM ABOVE", legend="the landforms, by name, over what was built")
m.built(w)
m.line(ROAD, (60, 60, 60), 1, dash=True)
m.callout(*CANYON[1], "canyon, ledges every 3", dx=30, dz=-10)
m.callout(*RIVER[2], "river: reaches and falls", dx=30, dz=10)
m.callout(*ROAD[1], "road graded to 1 in 7", dx=-10, dz=40)
m.callout(*TERRACES[0], "terraces 3 apart", dx=30, dz=20)
m.callout(*BUTTE[0], "butte", dx=20, dz=20)
m.callout(*SPIRE[0], "spire", dx=-20, dz=20)
m.callout(*ISLAND[0], "floating island", dx=-20, dz=-30)
m.callout(-20, -48, "scarp", dx=-30, dz=-20)
S.save(os.path.join(out, "05-topdown-annotated.png"))
