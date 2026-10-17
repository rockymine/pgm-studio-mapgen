"""Sixes and Sevens' pictures, drawn by the studio's textured renderer from a saved build.

    MINECRAFT_JAR=... python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pgmvox.read import render  # noqa: E402

SHOTS = [
    ("01-board", [-150, 20, -110, 149, 159, 109], 200, 38, 40, 2400, 1500),
    ("02-red-front", [-80, 38, -40, 0, 100, 70], 105, 16, 36, 2200, 1500),
    ("03-red-door", [-60, 38, -20, -20, 90, 40], 75, 10, 34, 2000, 1400),
    ("04-yard", [-72, 38, 26, -20, 75, 70], 60, 22, 34, 2000, 1400),
    ("05-field", [-50, 20, -100, 50, 70, 100], 180, 30, 38, 2400, 1500),
    ("06-above-red", [-150, 60, -110, -40, 159, 109], 70, 30, 38, 2400, 1500),
    ("12-shelf", [-50, 38, 50, 2, 75, 90], 20, 24, 36, 2000, 1300),
    ("07-seam", [-25, 10, -10, 25, 55, 60], 200, 35, 34, 2000, 1400),
    ("08-north-spur", [-60, 38, -80, -10, 80, -10], 120, 16, 36, 2000, 1300),
    ("09-tall-hall", [-72, 40, -8, -47, 64, 25], 115, 48, 34, 2000, 1500),
    ("10-spawn-hall", [-105, 40, 14, -82, 56, 39], 160, 50, 34, 1800, 1400),
    ("11-dark-room", [-110, 40, -16, -89, 64, 6], 140, 45, 34, 1700, 1400),
]


def main(build, board):
    out = os.path.join(board, "renders")
    os.makedirs(out, exist_ok=True)
    jobs = [{"out": os.path.join(out, f"{n}.png"), "box": box, "yaw": yaw, "pitch": pitch, "fov": fov, "w": w, "h": h}
            for n, box, yaw, pitch, fov, w, h in SHOTS]
    print(render.textured(build, jobs))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
