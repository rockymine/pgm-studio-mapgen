"""Frostvault's pictures, drawn by the studio's renderer with the roof lifted off, and its plan in text.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
import board                                                                           # noqa: E402
import layout as L                                                                     # noqa: E402
from pgmvox import World                                                               # noqa: E402
from pgmvox.plan import bunker as PB                                                   # noqa: E402
from pgmvox.read import render                                                         # noqa: E402

build, here = sys.argv[1], sys.argv[2]
out = os.path.join(here, "renders")
os.makedirs(out, exist_ok=True)
b = board.plan()
open(os.path.join(out, "plan.txt"), "w").write(
    "# rock, P pillar, . island, (space) void, R wool room, S spawn, | a defence wall's seam; a character a cell of "
    f"{b.cell} blocks\n" + PB.ascii(b) + "\n")
jar = os.environ.get("MINECRAFT_JAR") or os.path.expanduser("~/.cache/minecraft/1.8.9-textures.jar")
w = World.load(build)
w.ids[:, L.H.roof[0]:, :] = 0
w.dat[:, L.H.roof[0]:, :] = 0
lifted = tempfile.mkdtemp(prefix="frostvault-lifted-")
w.save(lifted, "Frostvault", (0, 30, 0))
got = board.laid(b)
x1, z1 = got.x0 + got.blocks.shape[0] - 1, got.z0 + got.blocks.shape[1] - 1
R = lambda name: os.path.join(out, name)                                               # noqa: E731
hall = (got.x0 + 20, L.H.floor, got.z0 + 20, x1 - 20, L.H.ceil, z1 - 20)
blue = [r for r in got.rooms if r["k"] == 0]
shots = [dict(out=R("50-board.png"), box=hall, yaw=90, pitch=89, fov=40, w=1800, h=1500),
         dict(out=R("51-board-se.png"), box=hall, yaw=150, pitch=42, fov=45, w=2000, h=1300),
         dict(out=R("52-blue-half.png"), box=(hall[0], L.H.floor, 0, hall[3], L.H.ceil, hall[5]), yaw=160, pitch=35,
              fov=45, w=1800, h=1200),
         dict(out=R("53-middle.png"), box=(hall[0], 16, -40, hall[3], L.H.ceil, 40), yaw=90, pitch=25, fov=55, w=1800,
              h=1100)]
for k, r in enumerate(blue):
    fx, fz = r["face_at"]
    shots.append(dict(out=R(f"5{4 + k}-seal-{k}.png"), box=(fx - 14, 16, fz - 14, fx + 14, 38, fz + 14),
                      yaw={(1, 0): 90, (-1, 0): -90, (0, 1): 180, (0, -1): 0}[r["face"]], pitch=20, fov=60, w=1400,
                      h=1000))
render.textured(lifted, shots, jar=jar)
print(f"renders in {out}")
