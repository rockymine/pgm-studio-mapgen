"""Floe's plan, drawn before anything is built:

1. THE SPARK — from above: the terracotta floor, its rim a shade darker, the eye and the void black, the blocks to
   brace against cream, the ring the players spawn on.
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

S = 5
R = P.REACH
CLAY = (217, 119, 87)                                            # the Claude terracotta
RIM = (175, 88, 58)
CRATE = (240, 238, 230)
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
    d.text((ox, oy - 14), title, fill=(255, 255, 255))


def floor_colour(x, z):
    if P.crate_at(x, z):
        return CRATE if P.crate_at(x, z) == 1 else (205, 200, 185)
    rim = any(not P.is_floor(x + dx, z + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return RIM if rim else CLAY


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
    panel(d, 20, 30, "1. the spark: terracotta, its rim darker; cream blocks (greyer: two high); the spawn ring", floor_colour)
    c = 20 + R * S + S // 2, 30 + R * S + S // 2
    r = P.SPAWN_R * S
    d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=(40, 160, 60), width=2)
    panel(d, 40 + W, 30, "2. where a plain hit kills, knockback one: the share of directions", heat(1))
    panel(d, 60 + 2 * W, 30, "3. the same at knockback three, from two minutes", heat(3))
    path = os.path.join(os.path.dirname(out), "plan-check.txt")
    text = open(path).read() if os.path.exists(path) else "(run plan_check.py > renders/plan-check.txt)"
    d.multiline_text((20, W + 50), "4. the check\n" + text, fill=(230, 230, 230), spacing=5)
    img.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
