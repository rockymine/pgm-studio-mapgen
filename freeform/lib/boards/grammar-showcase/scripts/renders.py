"""The showcase's renders: every specimen from the south-east and the north-west and from above, the gallery and its
wall, and the whole board, drawn by the studio's own renderer where the 1.8.9 client jar is in MINECRAFT_JAR and kept
to a palette of 128 colours, else in the library's flat colours from the same corners.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import gen
from pgmvox import World
from pgmvox.read import render

build, out = sys.argv[1], os.path.join(sys.argv[2], "renders")
w = World.load(build)
STEP = gen.WIDTH + gen.GAP
span = len(gen.STYLES) * gen.WIDTH + (len(gen.STYLES) - 1) * gen.GAP
gx = (span - 8 * 14) // 2
shots = []
for k, (name, _, _) in enumerate(gen.STYLES):
    box = (k * STEP - 2, 0, -2, k * STEP + gen.WIDTH + 1, 45, gen.DEPTH + 1)
    shots += [dict(out=f"{10 + k}-{name}-se.png", box=box, yaw=150, pitch=30, w=1100, h=800, breathing=0.85),
              dict(out=f"{10 + k}-{name}-nw.png", box=box, yaw=-35, pitch=24, w=1100, h=800, breathing=0.85),
              dict(out=f"{10 + k}-{name}-above.png", box=box, yaw=180, pitch=80, w=900, h=900, breathing=0.7)]
shots += [dict(out="20-gallery.png", box=(gx - 2, 10, gen.DEPTH + 22, gx + 8 * 14 + 1, 40, gen.DEPTH + 68),
               yaw=160, pitch=55, w=1400, h=860, breathing=0.75),
          dict(out="21-gallery-wall.png", box=(gx - 2, 10, gen.DEPTH + 22, gx + 8 * 14 + 1, 40, gen.DEPTH + 29),
               yaw=180, pitch=12, w=1400, h=540, breathing=0.8),
          dict(out="01-board.png", box=(w.x0, 0, w.z0, w.x0 + w.sx - 1, 45, w.z0 + w.sz - 1), yaw=150, pitch=38,
               w=1600, h=960, breathing=0.7)]
for s in shots:
    s["out"] = os.path.join(out, s["out"])
if os.environ.get("MINECRAFT_JAR"):
    from PIL import Image
    render.textured(build, shots)
    for s in shots:                                     # a palette of 128 keeps a picture a few hundred kilobytes
        Image.open(s["out"]).convert("RGB").quantize(128, dither=Image.Dither.NONE).save(s["out"], optimize=True)
else:
    for s in shots:
        x0, y0, z0, x1, y1, z1 = s["box"]
        render.iso(w.ids, w.dat, w.x0, w.z0, s["out"], 4, "nw" if s["out"].endswith("nw.png") else "se",
                   (x0, z0, x1, z1), y0)
        render.trim(s["out"])
