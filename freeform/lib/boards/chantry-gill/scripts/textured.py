"""Chantry Gill drawn with the game's own textures: the board, the blue half, the town, the gill, the Scar and the
spawn, one picture each.

    python3 textured.py <build-dir> <out-dir> [jar]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.read import render  # noqa: E402

build, out = sys.argv[1], sys.argv[2]
jar = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser("~/.cache/minecraft/1.8.9-textures.jar")
SHOTS = {
    "50-board": ([-90, 0, -130, 89, 80, 129], 215, 38),
    "51-blue": ([-90, 20, 0, 89, 80, 129], 180, 30),
    "52-town": ([-60, 34, 20, 30, 66, 110], 160, 34),
    "53-gill": ([20, 26, 20, 70, 66, 110], 120, 28),
    "54-scar": ([36, 30, 50, 89, 80, 129], 220, 26),
    "55-spawn": ([-20, 34, 80, 40, 70, 129], 0, 30),
}
os.makedirs(out, exist_ok=True)
print(render.textured(build, [{"out": os.path.join(out, f"{k}.png"), "box": b, "yaw": y, "pitch": p, "fov": 34,
                               "w": 1600, "h": 1000} for k, (b, y, p) in SHOTS.items()], jar=jar))
