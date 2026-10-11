"""Lantern Drop's plan, drawn before anything is built, the course laid on its side (the bell court at the left):

1. THE FALL — the course from the side, true scale: every piece at its height, the left way in front, and from each
   piece's far edge the jump the checker found to the next, drawn as the fall model flies it; lethal drops red.
2. THE COURSE — from above: the pieces by theme, the left way above the middle line and the right below, cisterns and
   paddies blue, hills ringed red, the harbour and its slipway.
3. THE CHECK — the checker's numbers.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import math
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C

THEME = {"court": (200, 195, 180), "torii": (190, 50, 40), "roof": (50, 45, 50), "pagoda": (60, 40, 45),
         "beam": (150, 110, 60), "bamboo": (90, 160, 70), "rope": (190, 150, 90), "pillar": (150, 150, 150),
         "gallery": (170, 60, 50), "terrace": (120, 170, 80), "awning": (220, 120, 60), "arcade": (110, 80, 50),
         "nest": (140, 100, 60), "boathouse": (130, 60, 50), "barge": (100, 70, 45)}
S = 3
Z0, Z1 = -6, 320
Y0, Y1 = 10, 250
X0, X1 = -26, 26


def side(d, oy):
    pz = lambda z: 10 + (z - Z0) * S
    py = lambda y: oy + (Y1 - y) * S
    d.rectangle([0, oy, (Z1 - Z0) * S + 20, oy + (Y1 - Y0) * S], fill=(215, 228, 240))
    h = P.HARBOUR
    d.rectangle([pz(h["z"][0]), py(h["y"]), pz(h["z"][1]), py(Y0)], fill=(60, 110, 190))
    ps = [p for p in P.pieces() if p[9] in ("left", "middle")]
    for p in ps:
        d.rectangle([pz(p[5]), py(p[7]), pz(p[6] + 1), py(p[7] - 3)], fill=THEME[p[2]])
        if p[8].get("hill"):
            d.rectangle([pz(p[5]), py(p[7] + 5), pz(p[5] + P.HILL), py(p[7])], outline=(230, 40, 40), width=2)
        d.text((pz(p[5]), py(p[7]) - 26 if p[0] % 2 else py(p[7] - 4) + 2), p[1].replace("the ", ""), fill=(0, 0, 0))
    for a, b in zip(ps, ps[1:]):
        dy = a[7] - b[7]
        along, across = P.gap(a, b)
        how = C.gentlest(dy, math.hypot(max(along, 0), across))
        vx, vy, acc = P.LEAVES[how]
        x = y = 0.0
        pts = [(pz(a[6] + 1), py(a[7] + 1))]
        while y > -dy:
            x += vx
            y += vy
            vy = (vy - 0.08) * 0.98
            vx = (vx + acc) * 0.91
            pts.append((pz(a[6] + 1 + x), py(a[7] + 1 + y)))
        d.line(pts, fill=(220, 40, 40) if P.damage(dy) >= P.HEALTH else (255, 255, 255), width=2)
    for y in range(20, 250, 20):
        d.text((2, py(y) - 6), str(y), fill=(90, 90, 90))


def plan_view(d, oy):
    pz = lambda z: 10 + (z - Z0) * S
    px = lambda x: oy + (X1 - x) * S
    d.rectangle([0, oy, (Z1 - Z0) * S + 20, oy + (X1 - X0) * S], fill=(25, 25, 32))
    h = P.HARBOUR
    d.rectangle([pz(h["z"][0]), px(h["x"][1]), pz(h["z"][1] + 1), px(h["x"][0] - 1)], fill=(60, 110, 190))
    s = P.SLIPWAY
    d.rectangle([pz(s["z"][0]), px(s["x"][1]), pz(s["z"][1] + 1), px(s["x"][0] - 1)], fill=(250, 250, 250))
    for p in P.pieces():
        d.rectangle([pz(p[5]), px(p[4]), pz(p[6] + 1) - 1, px(p[3] - 1) - 1], fill=THEME[p[2]])
        if "water" in p[8]:
            a0, a1, b0, b1 = p[8]["water"]
            d.rectangle([pz(b0), px(a1), pz(b1 + 1) - 1, px(a0 - 1) - 1], fill=(60, 120, 210))
        if p[8].get("hill"):
            d.rectangle([pz(p[5]) - 2, px(p[4]) - 2, pz(p[6] + 1) + 1, px(p[3] - 1) + 1], outline=(230, 40, 40), width=2)
    d.text((10, oy + 2), "left", fill=(255, 255, 255))
    d.text((10, oy + (X1 - X0) * S - 14), "right", fill=(255, 255, 255))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    W = (Z1 - Z0) * S + 20
    H1 = (Y1 - Y0) * S
    H2 = (X1 - X0) * S
    import textwrap
    lines = [w for ln in lines for w in (textwrap.wrap(ln, 160, subsequent_indent="    ") or [""])]
    T = 14 * len(lines) + 30
    im = Image.new("RGB", (W, 20 + H1 + 24 + H2 + 20 + T), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((10, 4), "1. THE FALL from the side, true scale: the left way and the middle; each jump as the fall model flies it, "
           "red where it kills without water; hills ringed red", fill=(255, 255, 255))
    side(d, 20)
    d.text((10, 20 + H1 + 6), "2. THE COURSE from above: pieces by theme, water blue, hills ringed red; the harbour and its "
           "slipway (white) at the right", fill=(255, 255, 255))
    plan_view(d, 20 + H1 + 24)
    y = 20 + H1 + 24 + H2 + 10
    for ln in lines:
        d.text((10, y), ln, fill=(230, 230, 230))
        y += 14
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
