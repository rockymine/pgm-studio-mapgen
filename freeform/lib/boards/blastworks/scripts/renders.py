"""Blastworks' pictures, drawn by the studio's renderer: the whole board, blue's works, the box and the bridge from
below, the spawn's hall cut open, and the middle.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import layout as L                                                                     # noqa: E402
from pgmvox.read import render                                                         # noqa: E402

build, board = sys.argv[1], sys.argv[2]
out = os.path.join(board, "renders")
os.makedirs(out, exist_ok=True)
jar = os.environ.get("MINECRAFT_JAR") or os.path.expanduser("~/.cache/minecraft/1.8.9-textures.jar")
R = lambda name: os.path.join(out, name)                                               # noqa: E731
x0, z0, x1, z1 = L.HALL
render.textured(build, [
    dict(out=R("50-board.png"), box=(-115, 0, -25, 114, 32, 24), yaw=0, pitch=89, fov=40, w=2200, h=600),
    dict(out=R("51-board-se.png"), box=(-115, 0, -25, 114, 32, 24), yaw=150, pitch=40, fov=45, w=2000, h=1200),
    dict(out=R("52-blue-works.png"), box=(-112, 0, -24, -24, 30, 22), yaw=160, pitch=40, fov=50, w=1800, h=1100),
    dict(out=R("53-box-and-bridge.png"), box=(-98, 0, -23, -40, 28, -6), yaw=330, pitch=25, fov=50, w=1600, h=1000),
    dict(out=R("54-under-bridge.png"), box=(-98, 0, -23, -40, 28, -6), yaw=160, pitch=10, fov=50, w=1600, h=1000),
    dict(out=R("55-hall.png"), box=(x0 - 1, L.SPAWN_H - 1, z0 + 1, x1 + 4, L.HALL_H, z1 + 1), yaw=-20, pitch=25,
         fov=55, w=1300, h=900),
    dict(out=R("56-middle.png"), box=(-42, 0, -24, 41, 26, 23), yaw=150, pitch=35, fov=50, w=1800, h=1100),
], jar=jar)
print(f"renders in {out}")
