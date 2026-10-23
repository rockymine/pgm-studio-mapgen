"""Chantry Gill drawn with the game's own textures: the board, the blue half, the town, the gill, the Scar and the
spawn, one picture each.

    python3 textured.py <build-dir> <out-dir> [jar]
"""
import os
import sys

from pgmvox.read import render  # noqa: E402

build, out = sys.argv[1], sys.argv[2]
jar = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser("~/.cache/minecraft/1.8.9-textures.jar")
SHOTS = {
    "50-board": ([-90, 0, -130, 89, 60, 129], 215, 38),
    "51-blue": ([-90, 0, 0, 89, 60, 129], 180, 30),
    "52-town": ([-60, 12, 20, 30, 44, 110], 160, 34),
    "53-gill": ([20, 4, 20, 70, 44, 110], 120, 28),
    "54-scar": ([36, 8, 40, 89, 58, 129], 220, 26),
    "55-spawn": ([-20, 12, 80, 40, 48, 129], 0, 30),
    "56-front-cliff": ([-60, 0, 8, 30, 30, 40], 0, 12),
    "57-tarn-wall": ([44, 6, 20, 86, 52, 62], 0, 18),
    "58-scar-tower": ([56, 30, 38, 86, 62, 70], 30, 24),
    "59-side-cliff": ([60, 0, 20, 92, 44, 64], 90, 14),
}
os.makedirs(out, exist_ok=True)
print(render.textured(build, [{"out": os.path.join(out, f"{k}.png"), "box": b, "yaw": y, "pitch": p, "fov": 34,
                               "w": 1600, "h": 1000} for k, (b, y, p) in SHOTS.items()], jar=jar))
