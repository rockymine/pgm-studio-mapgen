"""Sunwell's plan, drawn before anything is built:

1. THE SECTION — the shaft cut north to south down its middle, true scale: the shelves stepping down from side to
   side, their pools, the shafts through them, the lake; from the first edge, the three ways of leaving it drawn
   as the fall model flies them.
2. THE SHELVES — each shelf from above: its rock, the overhang of the shelf above it (hatched), its pools (blue),
   its shaft (black), the falls' basin (pale blue), and the rim along its own edge with its gaps (yellow).
3. THE CHECK — the checker's numbers.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import sys

from PIL import Image, ImageDraw

import plan_v1 as P
import plan_check_v1 as C

ROCK, SHELF, POOL, FALLS, SHAFT, RIM, GAP = (90, 85, 80), (150, 140, 110), (50, 110, 200), (150, 200, 240), (10, 10, 10), \
    (120, 70, 50), (250, 210, 60)


def section(d, ox, oy, scale):
    """North (z -21) at the left, south at the right; y up."""
    R = P.R_SHAFT
    W = (2 * R + 1) * scale
    top, bot = P.TOP + 12, P.LAKE_Y - 12
    py = lambda y: oy + (top - y) * scale
    px = lambda z: ox + (z + R) * scale
    d.rectangle([ox - 8 * scale, py(top), ox, py(bot)], fill=ROCK)
    d.rectangle([px(R + 1), py(top), px(R + 1) + 8 * scale, py(bot)], fill=ROCK)
    d.rectangle([px(-R), py(P.LAKE_Y), px(R + 1), py(bot)], fill=POOL)
    for k in range(P.N_SHELVES):
        y = P.shelf_y(k)
        z0, z1 = (-R, P.EDGE) if P.side(k) == "N" else (-P.EDGE, R)
        d.rectangle([px(z0), py(y), px(z1 + 1), py(y - P.THICK)], fill=SHELF)
        d.text((px(z0) + 3 if P.side(k) == "N" else px(z1) - 30, py(y) - 13), str(y), fill=(0, 0, 0))
    for k, dr in enumerate(P.DROPS):
        if dr.get("lake"):
            continue
        y = P.shelf_y(k + 1)
        for name, x0, x1, s0, s1 in P.pools(k):
            if x0 <= 0 <= x1:
                za, zb = sorted((P.z_of(k, s0), P.z_of(k, s1)))
                d.rectangle([px(za), py(y), px(zb + 1), py(y - 3)], fill=POOL)
        if "shaft" in dr:
            x0, x1, s0, s1 = dr["shaft"]
            za, zb = sorted((P.z_of(k, s0), P.z_of(k, s1)))
            d.rectangle([px(za), py(y + 1), px(zb + 1), py(y - P.THICK - 1)], fill=(215, 228, 240))
            d.text((px(za), py(y) + 6), "shaft", fill=(0, 0, 0))
    k = 0
    for how, col in (("step off", (255, 255, 255)), ("run off", (250, 210, 60)), ("sprint jump", (230, 60, 60))):
        vx, vy, acc = P.LEAVES[how]
        x = y = 0.0
        pts = [(px(P.EDGE + 1), py(P.shelf_y(0) + 1.6))]
        while y > -P.DROP:
            x += vx
            y += vy
            vy = (vy - 0.08) * 0.98
            vx = (vx + acc) * 0.91
            pts.append((px(P.EDGE + 1 + x), py(P.shelf_y(0) + 1.6 + y)))
        d.line(pts, fill=col, width=2)
    d.text((px(-R), py(P.LAKE_Y) + 4), "the lake", fill=(255, 255, 255))


def shelf_plan(d, ox, oy, k, scale):
    R = P.R_SHAFT
    px = lambda x: ox + (x + R) * scale
    pz = lambda z: oy + (z + R) * scale
    above = k - 1
    for x in range(-R, R + 1):
        for z in range(-R, R + 1):
            if not P.in_shaft(x, z):
                continue
            if k == P.N_SHELVES:
                c = POOL
            elif P.on_shelf(k, x, z):
                c = SHELF
            else:
                c = (30, 30, 36)
            d.rectangle([px(x), pz(z), px(x) + scale - 1, pz(z) + scale - 1], fill=c)
            if above >= 0 and P.on_shelf(above, x, z) and (P.on_shelf(k, x, z) or k == P.N_SHELVES):
                d.line([(px(x), pz(z) + scale - 1), (px(x) + scale - 1, pz(z))], fill=(90, 85, 70))
    if above >= 0 and not P.DROPS[above].get("lake"):
        for name, x0, x1, s0, s1 in P.pools(above):
            za, zb = sorted((P.z_of(above, s0), P.z_of(above, s1)))
            d.rectangle([px(x0), pz(za), px(x1 + 1) - 1, pz(zb + 1) - 1], fill=POOL)
        dr = P.DROPS[above]
        if "shaft" in dr:
            x0, x1, s0, s1 = dr["shaft"]
            za, zb = sorted((P.z_of(above, s0), P.z_of(above, s1)))
            d.rectangle([px(x0), pz(za), px(x1 + 1) - 1, pz(zb + 1) - 1], fill=SHAFT)
        if dr.get("falls") is not None:
            fx = dr["falls"]
            xa, xb = sorted((fx, fx - 3 * (fx // abs(fx))))
            za, zb = sorted((P.z_of(above, 1), P.z_of(above, 4)))
            d.rectangle([px(xa), pz(za), px(xb + 1) - 1, pz(zb + 1) - 1], fill=FALLS)
    if k < P.N_SHELVES:
        ze = P.EDGE if P.side(k) == "N" else -P.EDGE
        for x in range(-R, R + 1):
            if P.in_shaft(x, ze):
                gap = any(g[1] <= x <= g[2] for g in P.gaps(k))
                d.rectangle([px(x), pz(ze), px(x) + scale - 1, pz(ze) + scale - 1], fill=GAP if gap else RIM)
    label = f"shelf {k + 1}, {P.shelf_y(k)}" if k < P.N_SHELVES else f"the lake, {P.LAKE_Y}"
    d.text((ox, oy - 12), label, fill=(255, 255, 255))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    sc = 3
    SW = (2 * P.R_SHAFT + 1 + 16) * sc + 40
    SH = (P.TOP - P.LAKE_Y + 24) * sc
    ps = 5
    cell = (2 * P.R_SHAFT + 1) * ps
    cols = 5
    PW = cols * (cell + 18) + 20
    W = SW + PW
    T = 14 * len(lines) + 40
    H = max(SH + 70, 2 * (cell + 30) + 40) + T
    im = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 20, SW, SH + 30], fill=(215, 228, 240))
    d.text((10, 4), "1. THE SECTION at x 0", fill=(255, 255, 255))
    d.text((10, SH + 34), "north left; off the top edge: step off white,", fill=(255, 255, 255))
    d.text((10, SH + 48), "run off yellow, sprint jump red", fill=(255, 255, 255))
    section(d, 30 + 8 * sc, 30, sc)
    d.text((SW + 20, 4), "2. THE SHELVES from above, north up: rock, the shelf above overhead (hatched), pools blue, "
           "shafts black, the falls' basin pale; the rim on the edge brown, its gaps yellow", fill=(255, 255, 255))
    for k in range(P.N_SHELVES + 1):
        r, c = divmod(k, cols)
        shelf_plan(d, SW + 20 + c * (cell + 18), 40 + r * (cell + 30), k, ps)
    y = max(SH + 70, 2 * (cell + 30) + 40) + 10
    d.text((10, y), "3. THE CHECK", fill=(255, 255, 255))
    y += 18
    for ln in lines:
        d.text((10, y), ln, fill=(230, 230, 230))
        y += 14
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
