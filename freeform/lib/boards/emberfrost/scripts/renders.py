"""Emberfrost's renders: flat-colour pictures from pgmvox (the island from two corners, red's half, sections across the gorge and through the two
cores, the plan's names over the built top-down) and the studio's textured pictures, which draw the real block textures.

    python3 renders.py <build-dir> <board-dir>        (MINECRAFT_JAR set for the textured ones)
"""
import os
import sys

import plan as P
from pgmvox import World
from pgmvox.read import render
from pgmvox.read.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)


def iso(name, scale, corner, box=None, ymin=0, ymax=None, xray=False):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin, ymax, xray=xray)
    render.trim(p)


iso("30-flat-island-se.png", 3, "se", ymin=8)
iso("31-flat-island-nw.png", 3, "nw", ymin=8)
iso("32-flat-red-half.png", 4, "se", (-72, -96, 71, -1), 36)
iso("33-flat-gorge.png", 5, "se", (-60, -24, 60, 24), 36, 80)
render.cutaway(w, os.path.join(out, "10-section-across-the-gorge.png"), [(0.5, -40), (0.5, 40)], 36, 100, 5,
               title="along z at x 0: the red half's ground down to the Cinder Span, the stone bar under its pier, the blue half's")
render.cutaway(w, os.path.join(out, "11-section-both-cores.png"), [(-70, -49.5), (70, -49.5)], 30, 100, 4,
               title="along x at z -50: the glacier, the Rime plaza, Amberford, the Slag Run, the Forge plinth and its moat")
render.cutaway(w, os.path.join(out, "12-section-the-thaw.png"), [(-62, -0.5), (62, -0.5)], 36, 90, 5,
               title="along x down the gorge: water and ice, the bar, lava and cooled lava; the three spans stand across it")

S = Sheet("Emberfrost - as built")
m = S.map(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=5, title="FROM ABOVE",
          legend="the built world's top blocks over the kill height, the plan's names and objectives over them (S spawn, C core)", symmetry=P.SYM)
m.built(w, ymin=P.KILL_Y)
for name, x, z in P.PLACES:
    m.place(x, z, name, size=9)
    m.place(x, -1 - z, name, size=9)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))

jar = os.environ.get("MINECRAFT_JAR")
if jar and os.path.isfile(jar):
    def shot(name, box, yaw, pitch, fov=40, w_=1800, h_=1300):
        return dict(out=os.path.join(out, name), box=box, yaw=yaw, pitch=pitch, fov=fov, w=w_, h=h_)
    shots = [
        shot("t01-outside-from-the-south-east.png", (-72, 0, -96, 72, 115, 96), 25, 22, 42),
        shot("t02-outside-from-the-north-west.png", (-72, 0, -96, 72, 115, 96), 205, 24, 42),
        shot("t03-underside.png", (-72, 0, -96, 72, 115, 96), 200, -28, 42),
        shot("t04-red-half-from-above.png", (-72, 40, -96, 72, 110, -1), 170, 40, 42),
        shot("t05-blue-half-from-above.png", (-72, 40, 0, 72, 110, 95), 350, 40, 42),
        shot("t06-the-thaw-along-the-gorge.png", (-62, 36, -22, 62, 82, 22), 270, 20, 42, 1800, 1000),
        shot("t07-the-thaw-from-the-lava-end.png", (-62, 36, -22, 62, 82, 22), 90, 22, 42, 1800, 1000),
        shot("t08-spawn-hearth-yard.png", (-28, 58, -96, 28, 100, -60), 180, 28, 38, 1700, 1100),
        shot("t09-amberford.png", (-30, 50, -90, 36, 95, -12), 175, 32, 40, 1800, 1200),
        shot("t10-rime-core.png", (-48, 60, -62, -22, 94, -36), 160, 32, 36, 1500, 1100),
        shot("t11-rime-core-from-the-glacier.png", (-64, 60, -76, -10, 110, -30), 20, 30, 38, 1700, 1100),
        shot("t12-forge-core.png", (28, 56, -74, 54, 84, -46), 200, 38, 36, 1500, 1100),
        shot("t13-the-caldera.png", (6, 50, -92, 72, 100, -28), 200, 35, 40, 1700, 1100),
        shot("t14-the-mirror-and-the-blue-cave.png", (-64, 52, -62, -28, 80, -16), 150, 30, 40, 1700, 1100),
        shot("t15-inside-the-blue-cave.png", (-58, 50, -62, -30, 67, -33), 160, 48, 40, 1700, 1100),
        shot("t16-inside-the-slag-run.png", (22, 45, -66, 50, 60, -30), 150, 45, 40, 1700, 1100),
        shot("t17-the-aerie.png", (-62, 74, -80, -30, 100, -52), 160, 30, 36, 1500, 1100),
        shot("t18-both-lanes-from-the-gorge.png", (-72, 40, -70, 72, 100, -20), 180, 24, 42, 1900, 1000),
    ]
    render.textured(build, shots)
