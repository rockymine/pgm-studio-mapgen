"""Pithead's renders: the whole board, red's hub with its plated strips and headframe, red's two wool approaches, the
middle's two islands, and two cutaways.

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
         ("31-iso-red-hub.png", 6, "se", (30, 140, 100, 236), 0, YS + 30),
         ("32-iso-red-wool-works.png", 5, "sw", (6, 154, 122, 210), 0, YS + 24),
         ("33-iso-the-middle.png", 6, "se", (36, 100, 112, 150), 0, YS + 6)]
for name, scale, corner, box, ymin, ymax in shots:
    render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, name), scale, corner, box, ymin, ymax)
    render.trim(os.path.join(out, name))
render.cutaway(w, os.path.join(out, "10-cutaway-a.png"), [(60, 120), (60, P.H)], 0, YS + 26, 4,
               title="A-A' down red's half, x 60")
render.cutaway(w, os.path.join(out, "11-cutaway-b.png"), [(0, 192), (P.W, 192)], 0, YS + 20, 4,
               title="B-B' across red's hub and both wool corridors, z 192")

# with the 1.8.9 client jar in MINECRAFT_JAR, the same places in the game's own textures
if os.environ.get("MINECRAFT_JAR"):
    shots = [("40-red-hub.png", (36, YS - 6, 164, 92, YS + 32, 220), 200, 40),
             ("41-red-wool-works-west.png", (8, YS - 10, 150, 50, YS + 14, 196), 140, 32),
             ("42-red-wool-works-east.png", (78, YS - 10, 150, 118, YS + 14, 196), 220, 32),
             ("43-the-middle.png", (36, 10, 100, 112, YS + 16, 150), 200, 38),
             ("45-red-ledge-from-the-hub.png", (14, YS - 4, 176, 46, YS + 16, 204), 90, 30),
             ("44-red-spawn-yard.png", (44, YS - 2, 196, 76, YS + 20, 236), 180, 26),
             ("full-from-south-east.png", (0, 0, 0, P.W, YS + 44, P.H), 210, 40),
             ("full-from-above.png", (0, 0, 0, P.W, YS + 44, P.H), 180, 80)]
    print(render.textured(build, [dict(out=os.path.join(out, n), box=b, yaw=yaw, pitch=pitch, fov=55, w=1200, h=800)
                                  for n, b, yaw, pitch in shots]))
