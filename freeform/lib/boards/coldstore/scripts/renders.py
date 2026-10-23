"""Coldstore's pictures, drawn by the studio's renderer: the bunker with its roof lifted off, from over it and into
each part, and the ice field over the roof.

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
w = World.load(build)
w.ids[:, L.ROOF[0]:, :] = 0
w.dat[:, L.ROOF[0]:, :] = 0
lifted = tempfile.mkdtemp(prefix="coldstore-lifted-")
w.save(lifted, "Coldstore", L.SPAWN)
R = lambda name: os.path.join(out, name)                                               # noqa: E731
B = (L.OUTER_U, L.FLOOR, -L.OUTER_V, -1 - L.OUTER_U, L.CEIL, L.OUTER_V - 1)
render.textured(lifted, [
    dict(out=R("50-board.png"), box=B, yaw=0, pitch=89, fov=40, w=2000, h=1150),
    dict(out=R("51-board-se.png"), box=B, yaw=150, pitch=42, fov=45, w=2000, h=1300),
    dict(out=R("52-quarter.png"), box=(-104, 7, 0, 0, 41, 55), yaw=150, pitch=35, fov=45, w=1800, h=1200),
    dict(out=R("53-hub.png"), box=(-92, 16, -12, -40, 40, 40), yaw=110, pitch=30, fov=55, w=1800, h=1100),
    dict(out=R("54-wool-block.png"), box=(-92, 16, 14, -60, 38, 36), yaw=60, pitch=20, fov=55, w=1600, h=1000),
    dict(out=R("55-middle.png"), box=(-40, 16, -30, 39, 40, 30), yaw=180, pitch=30, fov=55, w=1800, h=1100),
    dict(out=R("56-great-door.png"), box=(-32, 16, 24, -10, 30, 53), yaw=0, pitch=25, fov=55, w=1400, h=1000),
], jar=jar)
render.textured(build, [dict(out=R("57-ice.png"), box=(L.X0, 0, L.Z0, -1 - L.X0, 90, -1 - L.Z0), yaw=150, pitch=30,
                             fov=45, w=1800, h=1100)], jar=jar)
print(f"renders in {out}")
