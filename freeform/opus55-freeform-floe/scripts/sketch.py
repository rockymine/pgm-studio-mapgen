"""Floe's plan, drawn before anything is built:

1. THE FLOES — from above: snow shaded by the floe's height, bare ice blue, the holes and the void black, the crates
   brown, each floe's spawn marked.
2. WHERE A HIT KILLS — from above again, every cell by the share of the directions a plain knockback-one hit could
   push a player in that ends off the ice: white for none, red for all.
3. THE SAME AT KNOCKBACK THREE, from two minutes on.
4. THE CHECK — the checker's numbers, read from renders/plan-check.txt.

    python3 sketch.py <out.png>
"""
import math
import os
import sys

from PIL import Image, ImageDraw

import plan as P

S = 6
R = 42
SNOW = {64: (205, 212, 222), 65: (226, 232, 240), 66: (246, 249, 252)}
ICE = (120, 165, 225)
CRATE = (150, 105, 60)
VOID = (14, 18, 30)
DIRS = [(math.cos(a), math.sin(a)) for a in [i * math.pi / 16 for i in range(32)]]


def share(x, z, level):
    r = P.knock(level, P.surface(x, z), sprint=False)
    n = 0
    for dx, dz in DIRS:
        t = 0.5
        while t <= r:
            px, pz = int(round(x + dx * t)), int(round(z + dz * t))
            if P.crate_at(px, pz):
                break
            if not P.is_floor(px, pz):
                n += 1
                break
            t += 0.5
    return n / len(DIRS)


def panel(d, ox, oy, title, colour):
    d.rectangle([ox, oy, ox + (2 * R + 1) * S, oy + (2 * R + 1) * S], fill=VOID)
    for x in range(-R, R + 1):
        for z in range(-R, R + 1):
            if not P.is_floor(x, z):
                continue
            a, b = ox + (x + R) * S, oy + (z + R) * S
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=colour(x, z))
            for dx, dz in ((1, 0), (0, 1)):                       # the step where one floe lies over the next
                t2 = P.top(x + dx, z + dz)
                if t2 is not None and t2 != P.top(x, z) and P.is_floor(x + dx, z + dz):
                    if dx:
                        d.line([(a + S - 1, b), (a + S - 1, b + S - 1)], fill=(90, 100, 120))
                    else:
                        d.line([(a, b + S - 1), (a + S - 1, b + S - 1)], fill=(90, 100, 120))
    d.text((ox, oy - 14), title, fill=(255, 255, 255))


def floor_colour(x, z):
    if P.crate_at(x, z):
        return CRATE if P.crate_at(x, z) == 1 else (115, 75, 40)
    return ICE if P.surface(x, z) == "ice" else SNOW[P.top(x, z)]


def heat(level):
    cache = {}

    def colour(x, z):
        if P.crate_at(x, z):
            return CRATE
        s = cache.setdefault((x, z), share(x, z, level))
        return (255, int(255 * (1 - s)), int(255 * (1 - s)))
    return colour


def main(out):
    W = (2 * R + 1) * S
    img = Image.new("RGB", (3 * W + 80, W + 260), (30, 32, 40))
    d = ImageDraw.Draw(img)
    panel(d, 20, 30, "1. the floes: snow by height (darker lower), blue ice, brown crates (dark: two high)", floor_colour)
    for f in P.FLOES:
        a, b = 20 + (f[0] + R) * S + S // 2, 30 + (f[1] + R) * S + S // 2
        d.ellipse([a - 4, b - 4, a + 4, b + 4], outline=(40, 160, 60), width=2)
        d.text((a + 6, b - 6), f"y {f[3]}", fill=(30, 60, 30))
    panel(d, 40 + W, 30, "2. where a plain hit kills, knockback one: the share of directions", heat(1))
    panel(d, 60 + 2 * W, 30, "3. the same at knockback three, from two minutes", heat(3))
    path = os.path.join(os.path.dirname(out), "plan-check.txt")
    text = open(path).read() if os.path.exists(path) else "(run plan_check.py > renders/plan-check.txt)"
    d.multiline_text((20, W + 50), "4. the check\n" + text, fill=(230, 230, 230), spacing=5)
    img.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
