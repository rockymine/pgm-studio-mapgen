"""Scratch: three houses on flat ground at 0, 12 and 45 degrees, one delved house, to look at the rasterizer."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from mc import World, B
import house, render_iso
w = World(-40, -20, 80, 40, sy=40)
w.fill(-40, 1, -20, 39, 5, 19, B.GRASS)
w.fill(-40, 1, -20, 39, 4, 19, B.DIRT)
specs = [dict(cx=-26, cz=0, heading=0, L=11, W=7, floor=5, storeys=2, jetty=True, style="town"),
         dict(cx=-6, cz=0, heading=12, L=11, W=7, floor=5, storeys=2, jetty=True, style="plaster"),
         dict(cx=15, cz=0, heading=45, L=11, W=7, floor=5, storeys=2, style="brick"),
         dict(cx=31, cz=8, heading=30, L=8, W=6, floor=5, storeys=1, style="delved")]
for s in specs:
    house.build(w, s)
w.save("/tmp/house-test", "t", (0, 10, 0))
x0, z0, ids, dat = render_iso.load("/tmp/house-test")
render_iso.render(ids, dat, x0, z0, sys.argv[1], 7, "se")
render_iso.render(ids, dat, x0, z0, sys.argv[2], 7, "nw")
