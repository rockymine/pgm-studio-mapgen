"""Hoarfire's renders: the library's flat-colour iso and section, the plan's names over the built world, and the
studio's textured views (MINECRAFT_JAR set) of the board, each half, each objective, the lodge, the Rift and the
Ice Cave.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import land
import plan as P
from pgmvox import World
from pgmvox.read import render
from pgmvox.read.sketch import Sheet

build, root = sys.argv[1], sys.argv[2]
w = World.load(build)
out = os.path.join(root, "renders")
render.iso(w.ids, w.dat, w.x0, w.z0, os.path.join(out, "30-iso-the-board.png"), 2, "se")
render.trim(os.path.join(out, "30-iso-the-board.png"))
render.cutaway(w, os.path.join(out, "31-cutaway-z-50.png"), [(-72, -50), (71, -50)], 20, 80, 4,
               title="along x at z -50: monument shelf, the Thaw, the Ember Pit, Kiln Hill")

R = P.build()
S = Sheet("Hoarfire - as built")
m = S.map(R.x_min, R.z_min, R.x_max, R.z_max, scale=6, title="FROM ABOVE",
          legend="the built world's top blocks, the plan's names and objectives over them", symmetry=R.symmetry)
m.built(w, ymin=P.KILL_Y)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=11)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))

if os.environ.get("MINECRAFT_JAR"):
    def shot(name, box, yaw, pitch, fov=40, wd=1800, ht=1300):
        return dict(out=os.path.join(out, name), box=box, yaw=yaw, pitch=pitch, fov=fov, w=wd, h=ht)
    shots = [
        shot("t01-overview.png", (-72, 0, -98, 71, 99, 97), 35, 42),
        shot("t02-rowan-from-the-rift.png", (-72, 0, -98, 71, 99, -8), 180, 30),
        shot("t03-rime-monument.png", (-50, 44, -64, -22, 70, -38), 30, 20),
        shot("t04-ember-core.png", (24, 38, -70, 70, 75, -30), 200, 20),
        shot("t05-hearth-lodge.png", (-18, 40, -98, 18, 90, -66), 165, 14),
        shot("t06-the-rift.png", (-72, 0, -26, 71, 90, 25), 90, 12),
        shot("t07-the-seam.png", (-26, 40, -72, 26, 90, -18), 180, 22),
        shot("t08-ice-cave-cut.png", (-64, 30, -36, -54, 60, -8), 90, 8),
        shot("t09-sloe-half.png", (-72, 0, -1, 71, 99, 97), 0, 30),
        shot("t10-fire-falls-and-cinder.png", (18, 0, -30, 71, 80, 4), 120, 12),
        shot("t11-across-the-rift.png", (-44, 30, -70, 44, 85, 12), 175, 9),
        shot("t12-lodge-hall-inside.png", (-12, 54, -96, 12, 59, -80), 160, 55),
        shot("t13-hollow-way-into-the-pit.png", (16, 36, -56, 48, 70, -8), 160, 26),
    ]
    print(render.textured(build, shots))
