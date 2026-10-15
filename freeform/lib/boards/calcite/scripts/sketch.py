"""Calcite's plan, drawn from the raster before anything is built, in three panels:

1. THE BOWL — every column by floor height (lava, Ledge, Bench, wall), the stairs with the way they
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
    if k == P.KINDS["lava"]:
        return (225, 95, 20)
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
    labels = [(-38, 30, "Bench 17"), (-28, 20, "Ledge 13"), (-17, 10, "lava 11"),
              (-8, 10, "apron 14"), (-2, -1, "17"), (-2, -38, "20"), (-2, 37, "20"), (-48, 0, "SPAWN 21")]
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
    # tunnels (dashed): the spawn's, and the Spring's under the lava
    for t in P.TUNNELS:
        for twin in (False, True):
            pts = t["pts"] if not twin else [(*P.rot(x, z), y) for x, z, y in t["pts"]]
            q = [px(x, z, oy) for x, z, _ in pts]
            col = (150, 60, 160) if t["key"] == "spawn-tunnel" else (230, 150, 30)
            for k in range(len(q) - 1):
                (a, b), (c, e) = q[k], q[k + 1]
                n = max(2, int(max(abs(c - a), abs(e - b)) // 8))
                for s_ in range(0, n, 2):
                    d.line([(a + (c - a) * s_ / n, b + (e - b) * s_ / n), (a + (c - a) * (s_ + 1) / n, b + (e - b) * (s_ + 1) / n)],
                           fill=col, width=3)
    # the arrow spawners in two diagonal corners
    for x, y, z in P.ARROWS_AT:
        a, b = px(x - 0.5, z - 0.5, oy)
        d.polygon([(a, b - 6), (a + 6, b), (a, b + 6), (a - 6, b)], fill=(120, 200, 255), outline=(0, 60, 120))
    # the gapple spring
    a, b = px(-0.5, -0.5, oy)
    d.ellipse([a - 5, b - 5, a + 5, b + 5], outline=(220, 170, 0), width=2)
    d.text((6, oy + 4), "1. THE BOWL — floor height (lava 11, Ledge 13, Bench 17, side hills 20, spawn 21), stairs (ticks), lava (orange), hills (pale yellow),"
           " pads (green, simulated flights),\n   the spawn tunnels (purple dashes), the Spring's tunnels under the lava (orange dashes),"
           " the golden apples (gold ring), arrows (blue diamonds), walls (dark)",
           fill=(255, 255, 255))


def routes(d, oy, lines):
    for i in range(P.NX):
        for j in range(P.NZ):
            x, z = i + P.X_MIN, j + P.Z_MIN
            a, b = px(x - 0.5, z - 0.5, oy)
            c = colour(R.H[i, j], R.K[i, j])
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=tuple(int(v * 0.55) for v in c))
    R_ = [
        ("main lane: spawn stair, Bench, axis stair, causeway, apron", [(-46, 0), (-37, 0), (-30, 0), (-10, 0), (-4, 0)], (240, 80, 70), 4),
        ("forecourt stair onto a side hill", [(-40, -2), (-36, -20), (-20, -33), (-1, -33), (-1, -36)], (250, 220, 90), 3),
        ("side passage and door, either wall", [(-20, -33), (-11, -36), (-11, -38), (-6, -38)], (250, 160, 60), 2),
        ("spawn tunnel to the Ledge's corner", [(-46, -6), (-46, -22), (-30, -22)], (190, 90, 210), 3),
        ("the Spring: down from the apron, the apples, under the lava, up a trench", [(-8, 8), (-1, 0), (-1, -12), (6, -12), (6, -22), (13, -22)], (240, 150, 30), 3),
        ("parkour: the Ledge to the apron", [(-1, -21), (-1, -16), (-1, -12), (-1, -8)], (120, 220, 255), 3),
        ("pads: the apron to either side passage", [(-5, -8), (-10.5, -30.5)], (60, 200, 60), 3),
        ("diagonal steps: the arrows' corner to the apron", [(23, -20), (19.5, -16.5), (15.5, -13.5), (11.5, -10.5), (8, -9)], (120, 220, 255), 3),
        ("pad: the Ledge's corner onto the apron", [(-28, -24), (-8, -7)], (60, 200, 60), 2),
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
    """Two sections at true scale (6 px a block both ways), so a stair reads as a stair."""
    d.rectangle([0, oy, W, oy + hgt], fill=(215, 228, 240))
    band = hgt // 2

    def one(axis, fixed, top, title):
        lo, hi = (P.X_MIN, P.X_MAX) if axis == "x" else (P.Z_MIN, P.Z_MAX)
        y_lo = 4
        py = lambda y: top + band - 8 - (y - y_lo) * S
        sx = lambda u: (u - P.X_MIN if axis == "x" else u - P.Z_MIN) * S + (0 if axis == "x" else (W - P.NZ * S) // 2)
        for u in range(lo, hi + 1):
            i, j = (P.ix(u), P.iz(fixed)) if axis == "x" else (P.ix(fixed), P.iz(u))
            h, k = R.H[i, j], R.K[i, j]
            col = colour(h, k)
            if k == P.KINDS["lava"]:
                d.rectangle([sx(u), py(P.LAVA_Y + 1), sx(u + 1) - 1, py(7)], fill=col)
                d.rectangle([sx(u), py(7), sx(u + 1) - 1, py(y_lo)], fill=(150, 145, 135))
            else:
                d.rectangle([sx(u), py(min(h, P.WALL_Y) + 1), sx(u + 1) - 1, py(y_lo)],
                            fill=col if k != P.KINDS["wall"] else (120, 115, 108))
        # the Spring under the Middle, and the tunnels it opens, in outline
        x0, x1, z0, z1 = P.SPRING["box"]
        a0, a1 = (x0, x1) if axis == "x" else (z0, z1)
        d.rectangle([sx(a0), py(P.SPRING["ceil"]), sx(a1 + 1), py(P.SPRING["floor"] + 1)], fill=(250, 230, 160), outline=(150, 100, 0))
        d.text((sx(a0) + 2, py(P.SPRING["ceil"]) + 2), "apples", fill=(120, 80, 0))
        if axis == "z":
            for twin in (1, -1):
                pts = [(0, -4 * twin, 9), (0, -11 * twin, 7), (0, -22 * twin, 7)]
                q = [(sx(z), py(y + 1.5)) for _, z, y in pts]
                d.line(q, fill=(230, 150, 30), width=3)
        d.text((6, top + 4), title, fill=(0, 0, 0))
    one("x", -1, oy, "3a. WEST TO EAST through the Middle, true scale: spawn terrace, Bench, axis stair, Ledge, causeway, the stepped hill, the Spring under it")
    one("z", -1, oy + band, "3b. NORTH TO SOUTH through all three hills, true scale: alcove, forecourt stair, Bench, Ledge, parkour, the Middle; the Spring's tunnels under the lava (orange)")
    d.line([(0, oy + band), (W, oy + band)], fill=(0, 0, 0))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    lines = [ln for ln in lines if not ln.startswith("   (") and not ln.startswith("route ")]
    hs = 2 * ((P.WALL_Y - 4) * S + 40)
    im = Image.new("RGB", (W, 2 * H + hs + 8), (0, 0, 0))
    d = ImageDraw.Draw(im)
    bowl(d, 0)
    routes(d, H + 4, lines)
    sections(d, 2 * H + 8, hs)
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
