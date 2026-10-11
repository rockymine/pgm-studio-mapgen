"""Loomfall's plan, drawn before anything is built:

1. THE CARPETS — each from above, woven in its pattern, its moth holes black.
2. THE FALLS — each from above again, every cell by what a player falling from it lands on: the next carpet (green),
   one further down (blue), or nothing (red).
3. THE STACK — from the south and from the east, true scale: the carpets at their heights, the kill height under
   them.
4. THE CHECK — the checker's numbers.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C

WOOL = [(230, 230, 230), (230, 125, 55), (180, 70, 190), (100, 140, 210), (205, 185, 40), (65, 175, 55),
        (210, 130, 155), (65, 65, 65), (155, 160, 160), (45, 115, 140), (125, 55, 180), (45, 55, 150),
        (80, 50, 30), (55, 75, 30), (160, 45, 40), (25, 25, 25)]
S = 4
R = 27                                                           # every carpet within x, z of -27 .. 27


def top(d, ox, oy, k, mode):
    cs = P.cells(P.CARPETS[k])
    name, x0, x1, z0, z1, y, holes = P.CARPETS[k]
    d.rectangle([ox, oy, ox + (2 * R + 1) * S, oy + (2 * R + 1) * S], fill=(16, 18, 34))
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            a, b = ox + (x + R) * S, oy + (z + R) * S
            if (x, z) not in cs:
                c = (0, 0, 0)
            elif mode == "pattern":
                c = WOOL[P.pattern(k, x, z)]
            else:
                j = P.below(k, x, z)
                c = (200, 50, 50) if j is None else (80, 180, 80) if j == k + 1 else (70, 110, 210)
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=c)
    d.text((ox, oy - 13), f"{k + 1}. {name}, {y}", fill=(255, 255, 255))


def stack(d, ox, oy, along):
    """From the south (x across) or the east (z across), true scale."""
    H = (P.CARPETS[0][5] - P.KILL_Y + 12) * S
    d.rectangle([ox, oy, ox + (2 * R + 1) * S, oy + H], fill=(16, 18, 34))
    py = lambda y: oy + (P.CARPETS[0][5] + 6 - y) * S
    for k, (name, x0, x1, z0, z1, y, holes) in enumerate(P.CARPETS):
        a0, a1 = (x0, x1) if along == "x" else (z0, z1)
        mid = [P.pattern(k, (x0 + x1) // 2 if along == "z" else a, (z0 + z1) // 2 if along == "x" else a) for a in range(a0, a1 + 1)]
        for n, a in enumerate(range(a0, a1 + 1)):
            d.rectangle([ox + (a + R) * S, py(y), ox + (a + R + 1) * S - 1, py(y) + S - 1], fill=WOOL[mid[n]])
    d.line([(ox, py(P.KILL_Y)), (ox + (2 * R + 1) * S, py(P.KILL_Y))], fill=(220, 60, 60), width=2)
    d.text((ox + 4, py(P.KILL_Y) + 4), "the kill height", fill=(220, 60, 60))
    d.text((ox, oy - 13), "from the south" if along == "x" else "from the east", fill=(255, 255, 255))
    return H


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    cell = (2 * R + 1) * S
    n = len(P.CARPETS)
    W = n * (cell + 14) + 20
    Hs = (P.CARPETS[0][5] - P.KILL_Y + 12) * S
    T = 14 * len(lines) + 30
    im = Image.new("RGB", (W, 40 + cell + 40 + cell + 40 + Hs + 30 + T), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((10, 4), "1. THE CARPETS from above, north up, in their patterns; moth holes black", fill=(255, 255, 255))
    for k in range(n):
        top(d, 10 + k * (cell + 14), 34, k, "pattern")
    y2 = 34 + cell + 40
    d.text((10, y2 - 30), "2. THE FALLS: what a player falling from each cell lands on - the next carpet green, one further "
           "down blue, nothing red", fill=(255, 255, 255))
    for k in range(n):
        top(d, 10 + k * (cell + 14), y2, k, "falls")
    y3 = y2 + cell + 40
    d.text((10, y3 - 30), "3. THE STACK, true scale", fill=(255, 255, 255))
    stack(d, 10, y3, "x")
    stack(d, 10 + cell + 14, y3, "z")
    y = y3 + Hs + 20
    for ln in lines:
        d.text((10, y), ln, fill=(230, 230, 230))
        y += 14
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
