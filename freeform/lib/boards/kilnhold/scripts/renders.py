"""Kilnhold's renders: pgmvox's flat ones (the board from two corners, sections, an x-ray, the annotated top-down) and, when
MINECRAFT_JAR names the 1.8.9 client, the studio's textured ones: the board, each base's front, the Crown, the
gate hall, the objective rooms, cut through so the inside shows.

    python3 renders.py <build-dir> <board-dir>
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


iso("30-iso-board-se.png", 3, "se", ymin=40)
iso("31-iso-board-sw.png", 3, "sw", ymin=40)
iso("40-xray-red-bunker.png", 4, "se", (-66, -97, 62, -40), 50, 80, xray=True)
render.cutaway(w, os.path.join(out, "10-section-z-62-across-the-bunker.png"), [(-66, -62.5), (65, -62.5)], 40, 90, 5,
               title="along x at z -62: pump hall, west descent, gate hall, east descent, turbine hall, the Crown")
render.cutaway(w, os.path.join(out, "11-section-axis-x-1.png"), [(-0.5, -99), (-0.5, 0)], 40, 100, 6,
               title="along z at x 0: muster hall, spine, gate hall, the gate, the apron, the field, the crater")

S = Sheet("Kilnhold - as built")
m = S.map(P.X_MIN, P.Z_MIN, P.X_MAX, P.Z_MAX, scale=5, title="FROM ABOVE", symmetry=P.SYM,
          legend="the built world's top blocks; the plan's names and objectives over them")
m.built(w, ymin=40)
for name, (x, z) in P.PLACES:
    m.place(x, z, name, size=9)
m.objectives(P.objectives().markers())
S.save(os.path.join(out, "05-topdown-annotated.png"))

jar = os.environ.get("MINECRAFT_JAR")
if jar and os.path.isfile(jar):
    SH = [
        ("50-tex-board-from-south-east.png", (-70, 30, -100, 69, 112, 99), 150, 42),
        ("51-tex-board-from-north-west.png", (-70, 30, -100, 69, 112, 99), -30, 42),
        ("52-tex-red-front.png", (-70, 40, -100, 69, 100, -2), 180, 34),
        ("53-tex-blue-front.png", (-70, 40, 1, 69, 100, 99), 0, 34),
        ("54-tex-facade.png", (-34, 62, -56, 34, 90, -28), 200, 18),
        ("55-tex-crown.png", (-60, 70, -96, 60, 100, -54), 180, 40),
        ("56-tex-gate-hall.png", (-18, 62, -78, 18, 76, -54), 160, 30),
        ("57-tex-muster-and-wings.png", (-34, 62, -96, 34, 72, -79), 180, 38),
        ("58-tex-turbine-hall.png", (30, 54, -80, 60, 66, -58), 180, 40),
        ("59-tex-pump-hall.png", (-56, 54, -80, -30, 66, -58), 180, 40),
        ("60-tex-cooling-tower.png", (-62, 50, -52, -30, 95, -20), 180, 28),
        ("61-tex-quarry-pit.png", (30, 50, -60, 66, 85, -20), 180, 28),
        ("62-tex-crater.png", (-30, 50, -24, 30, 76, 0), 180, 28),
        ("63-tex-west-lane.png", (-66, 50, -56, -8, 92, -4), 200, 28),
    ]
    render.textured(build, [dict(out=os.path.join(out, n), box=b, yaw=y, pitch=p, fov=40, w=1800, h=1300)
                            for n, b, y, p in SH], jar=jar)
