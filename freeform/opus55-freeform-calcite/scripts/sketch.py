"""Calcite's plan, drawn from the raster before anything is built, in three panels:

1. THE BOWL — every column by floor height (pool blue, Ledge, Bench, Rim, wall), the stairs with the way they
   rise, the ladders, the pads with their simulated flights, the parkour pillars, the tunnels, the hills.
2. THE ROUTES — red's ways onto each hill, coloured by kind, with the checker's numbers.
3. TWO SECTIONS — west to east through the Middle, and north to south through the Middle and both side hills.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import math
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C
from pad import fly

S = 6
W, H = P.NX * S, P.NZ * S
R = C.R


def px(x, z, oy=0):
    return ((x - P.X_MIN + 0.5) * S, oy + (z - P.Z_MIN + 0.5) * S)


def colour(h, k):
    if k == P.KINDS["wall"]:
        return (70, 66, 62)
    if k == P.KINDS["water"]:
        return (70, 160, 175)
    if k == P.KINDS["ladder"]:
        return (150, 110, 60)
    if k == P.KINDS["hill"]:
        return (245, 235, 160)
    if k == P.KINDS["spawn"]:
        return (230, 190, 190)
    t = (h - 10) / 20.0
    base = (int(150 + 90 * t), int(150 + 90 * t), int(140 + 95 * t))
    if k == P.KINDS["stair"]:
        return tuple(int(c * 0.82) for c in base)
    return base


def bowl(d, oy):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            a, b = px(x - 0.5, z - 0.5, oy)
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=colour(R.H[i, j], R.K[i, j]))
    # stair arrows
    for (x, z), r in R.stair.items():
        if (x + z) % 2:
            continue
        cx, cy = px(x, z, oy)
        dx, dz = {"+x": (1, 0), "-x": (-1, 0), "+z": (0, 1), "-z": (0, -1)}[r]
        d.line([(cx - dx * 2, cy - dz * 2), (cx + dx * 2, cy + dz * 2)], fill=(40, 40, 40), width=1)
    # floor heights
    labels = [(-49, 20, "Rim 28"), (-34, 12, "Bench 22"), (-27, 12, "Ledge 16"), (-17, 10, "pool 10"),
              (-8, 10, "apron 19"), (-2, -1, "22"), (-2, -30, "23"), (-2, 28, "23"), (-52, 0, "SPAWN")]
    for x, z, t in labels:
        a, b = px(x, z, oy)
        d.text((a, b), t, fill=(20, 20, 20))
    # pads and their flights
    for pad in P.PADS:
        for twin in (False, True):
            x0, x1, z0, z1, y = pad["cells"]
            vx, vy, vz = pad["v"]
            cx, cz = (x0 + x1 + 1) / 2, (z0 + z1 + 1) / 2
            if twin:
                cx, cz, vx, vz = -cx, -cz, -vx, -vz
            *_, path = fly((cx, y + 1.0, cz), (vx, vy, vz), None, 40)
            L = C.land_of_pad(pad)
            pts = []
            for t, x, yy, z in path:
                pts.append(px(x - 0.5, z - 0.5, oy))
                if t >= L["t"]:
                    break
            d.line(pts, fill=(60, 200, 60), width=2)
            a, b = px(cx - 0.5, cz - 0.5, oy)
            d.rectangle([a - 6, b - 6, a + 6, b + 6], fill=(60, 200, 60), outline=(0, 90, 0))
    # tunnels
    for twin in (False, True):
        pts = P.TUNNEL if not twin else [(*P.rot(x, z), y) for x, z, y in P.TUNNEL]
        q = [px(x, z, oy) for x, z, _ in pts]
        for k in range(len(q) - 1):
            (a, b), (c, e) = q[k], q[k + 1]
            n = int(max(abs(c - a), abs(e - b)) // 8)
            for s in range(0, n, 2):
                d.line([(a + (c - a) * s / n, b + (e - b) * s / n), (a + (c - a) * (s + 1) / n, b + (e - b) * (s + 1) / n)],
                       fill=(150, 60, 160), width=3)
    # drops onto the side hills
    for x in range(-4, 4):
        for z in (-34, 33):
            a, b = px(x, z, oy)
            d.polygon([(a - 2, b - 2), (a + 2, b - 2), (a, b + (3 if z < 0 else -3))], fill=(200, 60, 40))
    # the gapple spring
    a, b = px(-0.5, -0.5, oy)
    d.ellipse([a - 5, b - 5, a + 5, b + 5], outline=(220, 170, 0), width=2)
    d.text((6, oy + 4), "1. THE BOWL — floor height (pool, Ledge 16, Bench 22, Rim 28), stairs (ticks), ladders (brown), hills (pale yellow),"
           " pads (green squares, simulated flights), tunnels (purple dashes), drops onto the side hills (red), the gapple spring (gold ring)",
           fill=(255, 255, 255))


def routes(d, oy, lines):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            a, b = px(x - 0.5, z - 0.5, oy)
            c = colour(R.H[i, j], R.K[i, j])
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=tuple(int(v * 0.55) for v in c))
    R_ = [
        ("main lane: notch, well, causeway, apron", [(-50, 0), (-44, 0), (-36, 0), (-29, 0), (-10, 0), (-4, 0)], (240, 80, 70), 4),
        ("the Rim to the North hill, dropping on it", [(-46, -4), (-41, -37), (-2, -37), (-1, -31)], (250, 160, 60), 3),
        ("the tunnel to the Ledge, up the side stair", [(-50, -7), (-50, -24), (-28, -24), (-16, -24), (-16, -27), (-10, -27), (-4, -29)], (190, 90, 210), 3),
        ("the Bench round to the South hill", [(-44, 2), (-37, 2), (-33, 4), (-33, 29), (-5, 29)], (250, 220, 90), 3),
        ("parkour from the north Ledge onto the Middle", [(-1, -21), (-1, -16), (-1, -12), (-1, -8)], (120, 220, 255), 3),
        ("pad: the Middle to the North hill's flank", [(-8, -8), (-13.5, -29.5)], (60, 200, 60), 3),
        ("pad: the Ledge's corner to the Rim", [(-28, -24), (-40.5, -37.5)], (60, 200, 60), 2),
    ]
    for k, (name, pts, col, w) in enumerate(R_):
        d.line([px(x, z, oy) for x, z in pts], fill=col, width=w)
        a, b = 8, oy + 24 + 13 * k
        d.rectangle([a, b + 3, a + 14, b + 8], fill=col)
        d.text((a + 20, b), name, fill=(255, 255, 255))
    y = oy + H - 13 * len(lines) - 8
    d.rectangle([4, y - 4, W - 4, oy + H - 4], fill=(15, 15, 20))
    for ln in lines:
        d.text((10, y), ln, fill=(230, 230, 230))
        y += 13
    d.text((6, oy + 4), "2. THE ROUTES — red's ways onto the hills (blue's are the same turned); the checker's walks below", fill=(255, 255, 255))


def sections(d, oy, hgt):
    d.rectangle([0, oy, W, oy + hgt], fill=(215, 228, 240))
    half = W // 2

    def py(y):
        return oy + hgt - 12 - (y - 4) * (hgt - 30) / 40.0
    for side, (axis, fixed, lo, hi) in enumerate((("x", -1, -60, 59), ("z", -1, -48, 47))):
        ox = side * half
        sx = lambda u: ox + 8 + (u - lo) * (half - 16) / (hi - lo + 1)
        for u in range(lo, hi + 1):
            i, j = (P.ix(u), P.iz(fixed)) if axis == "x" else (P.ix(fixed), P.iz(u))
            h, k = R.H[i, j], R.K[i, j]
            top = min(h, P.WALL_Y)
            col = colour(h, k)
            if k == P.KINDS["water"]:
                d.rectangle([sx(u), py(P.WATER_Y), sx(u + 1), py(6)], fill=col)
                d.rectangle([sx(u), py(6), sx(u + 1), py(4)], fill=(150, 145, 135))
            else:
                d.rectangle([sx(u), py(top), sx(u + 1), py(4)], fill=col if k != P.KINDS["wall"] else (120, 115, 108))
        name = "WEST-EAST through the Middle" if axis == "x" else \
            "NORTH-SOUTH through all three hills"
        d.text((ox + 6, oy + 4), ("3a. " if axis == "x" else "3b. ") + name, fill=(0, 0, 0))
    d.line([(half, oy), (half, oy + hgt)], fill=(0, 0, 0))
    # the Spring under the Middle, and the drops
    d.text((8, oy + 18), "under the Middle's top: the Spring, golden apples, two stairwells down from the apron", fill=(150, 100, 0))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    lines = [ln for ln in lines if not ln.startswith("   (") and not ln.startswith("route ")]
    hs = 280
    im = Image.new("RGB", (W, 2 * H + hs + 8), (0, 0, 0))
    d = ImageDraw.Draw(im)
    bowl(d, 0)
    routes(d, H + 4, lines)
    sections(d, 2 * H + 8, hs)
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
