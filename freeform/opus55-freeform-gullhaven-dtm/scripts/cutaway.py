"""A cutaway section along any line across the board, at true scale: every block the line's vertical plane cuts,
in its colour, the sky and the void left empty. The studio's round-trip cuts along x or z only; this cuts along
the line from one team's back through its town, the Skerry, and the other town to the other back.

    python3 cutaway.py <build-dir> <out.png> [x0 z0 x1 z1 ...]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "opus55-freeform-gullhaven", "scripts"))
import render_iso  # noqa: E402


def cut(build, out, pts, ymin=4, ymax=60, scale=4, step=0.5, title=""):
    x0, z0, ids, dat = render_iso.load(build)
    table = render_iso.colour_table()
    L = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(L)
    n = int(total / step) + 1
    W, H = n * scale // 2 + 20, (ymax - ymin) * scale + 40
    im = Image.new("RGB", (W, H), (205, 222, 236))
    d = ImageDraw.Draw(im)
    for k in range(n):
        s = k * step
        seg, acc = 0, 0.0
        while seg < len(L) - 1 and acc + L[seg] < s:
            acc += L[seg]
            seg += 1
        t = (s - acc) / L[seg]
        (ax, az), (bx, bz) = pts[seg], pts[seg + 1]
        x, z = ax + (bx - ax) * t, az + (bz - az) * t
        i, j = int(math.floor(x)) - x0, int(math.floor(z)) - z0
        px = 10 + k * scale // 2
        if not (0 <= i < ids.shape[0] and 0 <= j < ids.shape[2]):
            d.rectangle([px, 20, px + scale // 2, H - 20], fill=(25, 25, 30))
            continue
        for y in range(ymin, min(ymax, ids.shape[1])):
            b = int(ids[i, y, j])
            if b == 0:
                continue
            c = tuple(int(v) for v in table[b, int(dat[i, y, j])])
            py = H - 20 - (y - ymin + 1) * scale
            d.rectangle([px, py, px + scale // 2, py + scale - 1], fill=c)
    for y in range(ymin, ymax, 4):
        py = H - 20 - (y - ymin) * scale
        d.line([(0, py), (6, py)], fill=(0, 0, 0))
        d.text((W - 18, py - 6), str(y), fill=(80, 80, 80))
    d.text((10, 4), title, fill=(0, 0, 0))
    im.save(out)


if __name__ == "__main__":
    build, out = sys.argv[1], sys.argv[2]
    nums = [float(v) for v in sys.argv[3:]]
    pts = list(zip(nums[0::2], nums[1::2]))
    cut(build, out, pts)
