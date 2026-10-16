"""Thawline's renders: the studio's textured renderer for the board, each half, each objective and the rift (the
judge's pictures), and pgmvox's flat-colour cutaway across the rift.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

import plan as P
from pgmvox import World
from pgmvox.read import render

build, root = sys.argv[1], sys.argv[2]
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)
w = World.load(build)
render.cutaway(w, os.path.join(out, "10-cutaway-across-the-rift.png"), [(-20, -40), (-20, 40)], 0, 80, 6,
               title="across the Thawline at x -20")

E = lambda x, z: (-1 - x, -1 - z)                                            # noqa: E731
FULL = (P.X_MIN, 0, P.Z_MIN, P.X_MAX, 111, P.Z_MAX)
SHOTS = [
    ("01-board-from-the-southwest.png", FULL, 215, 34, 40),
    ("02-board-from-the-northeast.png", FULL, 35, 34, 40),
    ("03-frost-half.png", (P.X_MIN, 0, P.Z_MIN, P.X_MAX, 111, -1), 200, 40, 40),
    ("04-ember-half.png", (P.X_MIN, 0, 0, P.X_MAX, 111, P.Z_MAX), 20, 40, 40),
    ("11-rimehall.png", (-24, 30, -100, 24, 90, -70), 200, 24, 40),
    ("12-cinderhall.png", (-25, 30, 69, 23, 90, 99), 20, 24, 40),
    ("21-frost-heart-in-the-kettle.png", (-52, 30, -72, -20, 80, -40), 150, 32, 40),
    ("22-ember-heart.png", (19, 30, 39, 51, 80, 71), 330, 32, 40),
    ("31-frost-lantern-on-the-green.png", (18, 38, -70, 46, 70, -40), 215, 30, 40),
    ("32-ember-lantern.png", (-47, 38, 39, -19, 70, 69), 35, 30, 40),
    ("41-the-stack-and-the-rift.png", (-30, 8, -16, 30, 80, 15), 90, 18, 40),
    ("42-the-rift-looking-west.png", (-64, 8, -14, 10, 70, 13), 95, 12, 40),
    ("51-hoarstead.png", (20, 36, -70, 63, 70, -16), 230, 30, 40),
    ("52-kilnstead.png", (-64, 36, 15, -21, 70, 69), 50, 30, 40),
    ("61-the-knoll-and-the-moraine.png", (-20, 36, -52, 30, 70, -16), 180, 28, 40),
    ("62-rimewood-and-coldwater.png", (-63, 36, -50, -10, 80, -12), 200, 30, 40),
]
shots = [dict(out=os.path.join(out, n), box=b, yaw=yw, pitch=pt, fov=fv, w=1800, h=1300) for n, b, yw, pt, fv in SHOTS]
only = os.environ.get("THAW_SHOTS")
if only:
    shots = [s for s in shots if any(k in os.path.basename(s["out"]) for k in only.split(","))]
if os.environ.get("MINECRAFT_JAR"):
    print(render.textured(build, shots))
