"""The asset sheet drawn with the game's own textures, one picture a plot.

    python3 textured.py <build-dir> <out-dir> [jar]
"""
import os
import sys

from pgmvox.read import render  # noqa: E402

build, out = sys.argv[1], sys.argv[2]
jar = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser("~/.cache/minecraft/1.8.9-textures.jar")
SHOTS = {
    "t10-houses": ([4, 38, 8, 110, 62, 28], 180, 22),
    "t11-slopes": ([118, 36, 5, 199, 66, 45], 200, 30),
    "t12-gill-arch": ([30, 26, 44, 100, 50, 80], 140, 30),
    "t13-tarn-adit": ([8, 26, 82, 90, 52, 118], 250, 28),
    "t14-shelf": ([128, 34, 78, 199, 72, 125], 110, 22),
    "t15-chapel": ([94, 38, 86, 128, 56, 108], 200, 34),
}
os.makedirs(out, exist_ok=True)
print(render.textured(build, [{"out": os.path.join(out, f"{k}.png"), "box": b, "yaw": y, "pitch": p, "fov": 34,
                               "w": 1600, "h": 1000} for k, (b, y, p) in SHOTS.items()], jar=jar))
