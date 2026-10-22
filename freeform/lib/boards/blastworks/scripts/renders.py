"""Blastworks' pictures, drawn by the studio's renderer: the whole board, blue's works, the box cut open, the plain
wool room and the middle.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import layout as L                                                                     # noqa: E402
from pgmvox import World                                                               # noqa: E402
from pgmvox.read import render                                                         # noqa: E402

build, board = sys.argv[1], sys.argv[2]
out = os.path.join(board, "renders")
os.makedirs(out, exist_ok=True)
jar = os.environ.get("MINECRAFT_JAR") or os.path.expanduser("~/.cache/minecraft/1.8.9-textures.jar")
R = lambda name: os.path.join(out, name)                                               # noqa: E731
everything = (L.X0, 0, L.Z0, L.X0 + L.SX - 1, L.MAX_BUILD, L.Z0 + L.SZ - 1)
render.textured(build, [
    dict(out=R("50-board.png"), box=everything, yaw=0, pitch=89, fov=40, w=1400, h=1900),
    dict(out=R("51-board-se.png"), box=everything, yaw=150, pitch=45, fov=45, w=1800, h=1300),
    dict(out=R("52-blue-works.png"), box=(-20, 0, 50, 42, 20, 100), yaw=210, pitch=30, fov=50, w=1700, h=1100),
    dict(out=R("53-under-bridge.png"), box=(-2, 0, 50, 24, 18, 80), yaw=180, pitch=10, fov=55, w=1400, h=1000),
    dict(out=R("54-plain-room.png"), box=(-70, 8, 72, -50, 20, 100), yaw=-45, pitch=25, fov=55, w=1400, h=1000),
    dict(out=R("55-middle.png"), box=(-45, 0, -35, 44, 18, 34), yaw=180, pitch=35, fov=50, w=1800, h=1100),
], jar=jar)
w = World.load(build)                                    # the box with its roof lifted, to see in
x0, z0, x1, z1, y0, y1 = L.ROOM
w.ids[x0 - 1 - w.x0:x1 + 2 - w.x0, y1 + 1:, z0 - 1 - w.z0:z1 + 2 - w.z0] = 0
cut = tempfile.mkdtemp(prefix="blastworks-cut-")
w.save(cut, "Blastworks", L.SPAWN)
render.textured(cut, [dict(out=R("56-box-inside.png"), box=(x0 - 2, 0, z0 - 2, x1 + 6, y1, z1 + 2), yaw=200,
                           pitch=55, fov=50, w=1300, h=1000)], jar=jar)
print(f"renders in {out}")
