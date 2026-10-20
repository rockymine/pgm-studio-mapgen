"""Seamworks' renders: the whole board, green's back corner and crust close, and two cutaways through the plan's
sections, A-A' down the slot and B-B' across green's side.

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
shots = [("30-iso-the-board.png", 2, "se", None, 0, None),
         ("31-iso-green-back.png", 6, "se", (0, 0, 70, 130), P.YS - 22, P.YS + 6),
         ("32-iso-green-crust-and-middle.png", 6, "se", (50, 0, 190, 100), P.YS - 22, P.YS + 6),
         ("33-iso-green-forecourt-market.png", 10, "sw", (26, 60, 70, 115), P.YS - 14, P.YS + 22),
         ("34-iso-green-hall.png", 10, "se", (0, 14, 48, 70), P.YS - 10, P.YS + 22),
         ("35-iso-the-plated-slot.png", 10, "sw", (128, 22, 166, 56), P.YS - 22, P.YS + 22)]
for name, scale, corner, box, ymin, ymax in shots:
    render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, name), scale, corner, box, ymin, ymax)
    render.trim(os.path.join(out, name))
render.cutaway(w, os.path.join(out, "10-cutaway-a.png"), [(142, 0), (142, 114)], P.YS - 24, P.YS + 6, 6,
               title="A-A' down the slot, x 142")
render.cutaway(w, os.path.join(out, "11-cutaway-b.png"), [(0, 56), (174, 56)], P.YS - 24, P.YS + 6, 6,
               title="B-B' across green's side, z 56")

# with the 1.8.9 client jar in MINECRAFT_JAR, the same places in the game's own textures
if os.environ.get("MINECRAFT_JAR"):
    shots = [("40-green-back-corner.png", (0, P.YS - 12, 10, 64, P.YS + 22, 128), 225, 30),
             ("41-green-crust-and-quarry.png", (52, P.YS - 12, 22, 132, P.YS + 6, 100), 200, 34),
             ("42-the-middle-and-slots.png", (118, P.YS - 15, 24, 182, P.YS + 20, 116), 215, 36),
             ("43-twin-cut-and-spoil-heap.png", (100, P.YS - 12, 0, 212, P.YS + 18, 34), 160, 32),
             ("full-from-south-east.png", (0, P.YS - 24, 0, P.W, P.YS + 40, P.H), 210, 38),
             ("full-from-north-west.png", (0, P.YS - 24, 0, P.W, P.YS + 40, P.H), 30, 38),
             ("full-from-above.png", (0, P.YS - 24, 0, P.W, P.YS + 40, P.H), 180, 80)]
    print(render.textured(build, [dict(out=os.path.join(out, n), box=b, yaw=yaw, pitch=pitch, fov=55, w=1200, h=800)
                                  for n, b, yaw, pitch in shots]))
