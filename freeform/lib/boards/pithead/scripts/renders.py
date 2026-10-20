"""Pithead's renders: the whole board, red's hub with its shaft and banks, red's two wool works, the middle, and a
cutaway down the board's long axis.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World
from pgmvox.read import render

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)
YS = P.YS
shots = [("30-iso-the-board.png", 3, "se", None, 0, None),
         ("31-iso-red-hub.png", 6, "se", (34, 140, 94, 236), YS - 24, YS + 24),
         ("32-iso-red-wool-works.png", 6, "sw", (10, 154, 116, 196), YS - 24, YS + 14),
         ("33-iso-the-middle.png", 8, "se", (40, 96, 80, 144), YS - 26, YS + 6)]
for name, scale, corner, box, ymin, ymax in shots:
    render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, name), scale, corner, box, ymin, ymax)
    render.trim(os.path.join(out, name))
render.cutaway(w, os.path.join(out, "10-cutaway-a.png"), [(60, 0), (60, P.H)], YS - 26, YS + 26, 4,
               title="A-A' down the long axis, x 60")
render.cutaway(w, os.path.join(out, "11-cutaway-b.png"), [(0, 184), (P.W, 184)], YS - 26, YS + 14, 5,
               title="B-B' across red's hub and both approaches, z 184")

# with the 1.8.9 client jar in MINECRAFT_JAR, the same places in the game's own textures
if os.environ.get("MINECRAFT_JAR"):
    shots = [("40-red-hub-and-shaft.png", (34, YS - 4, 140, 94, YS + 30, 236), 200, 34),
             ("41-red-wool-works-west.png", (8, YS - 10, 150, 50, YS + 14, 196), 140, 32),
             ("42-red-wool-works-east.png", (78, YS - 10, 150, 118, YS + 14, 196), 220, 32),
             ("43-the-middle.png", (40, YS - 14, 96, 80, YS + 8, 144), 215, 36),
             ("44-red-spawn-yard.png", (44, YS - 2, 196, 76, YS + 20, 236), 180, 26),
             ("full-from-south-east.png", (0, 0, 0, P.W, YS + 44, P.H), 210, 40),
             ("full-from-above.png", (0, 0, 0, P.W, YS + 44, P.H), 180, 80)]
    print(render.textured(build, [dict(out=os.path.join(out, n), box=b, yaw=yaw, pitch=pitch, fov=55, w=1200, h=800)
                                  for n, b, yaw, pitch in shots]))
