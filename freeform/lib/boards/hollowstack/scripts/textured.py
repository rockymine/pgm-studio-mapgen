"""Hollowstack drawn with the game's own textures: the board, each wall's face seen across the chasm, the board cut
open along its middle, the Underwood, the Tops and the keep.

    python3 textured.py <build-dir> <out-dir> [jar]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.read import render  # noqa: E402

build, out = sys.argv[1], sys.argv[2]
jar = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser("~/.cache/minecraft/1.8.9-textures.jar")
SHOTS = {
    "50-board": ([-96, 0, -28, 95, 112, 27], 210, 22),
    "51-section": ([-96, 0, -28, 95, 112, 0], 180, 0),
    "52-face-blue": ([-12, 0, -28, 40, 112, 27], 270, 5),
    "53-face-red": ([-41, 0, -28, 11, 112, 27], 90, 5),
    "54-underwood": ([10, 50, -20, 70, 80, 0], 180, 15),
    "55-underwood-mouth": ([-4, 50, -16, 40, 80, 16], 270, 10),
    "56-tops": ([-30, 90, -28, 95, 120, 27], 230, 35),
    "57-keep": ([70, 98, -16, 95, 116, 15], 250, 40),
    "58-deep": ([10, 8, -18, 92, 34, 0], 180, 10),
}
os.makedirs(out, exist_ok=True)
print(render.textured(build, [{"out": os.path.join(out, f"{k}.png"), "box": b, "yaw": y, "pitch": p, "fov": 40,
                               "w": 1600, "h": 1100} for k, (b, y, p) in SHOTS.items()], jar=jar))
