"""Riad's plan, drawn from the rasters before anything is built, in three panels:

1. THE BOARD — every column by what it is and how high: the void, the ground, the water, the walls and
   hedges, the arcade roofs hatched over the walks under them, the stairs with the way they rise, the ladders,
   the Cistern's water columns, the three posts, the spawn houses, and the line the carrier may not cross.
2. THE ROUTES — blue's ways from the spawn to each post and between them, with the checker's numbers.
3. TWO SECTIONS at true scale — north to south down the axis, through both spawns, the canal and the
   Cistern; and west to east through the Mirador, the court and the Minaret.

    python3 sketch.py <out.png>
"""
import contextlib
import io
import math
import sys

from PIL import Image, ImageDraw

import plan as P
import plan_check as C

S = 8
W, H = P.NX * S, P.NZ * S
R = C.R
KN = C.KN
TEAM = {"red": (200, 50, 50), "blue": (50, 90, 210)}


def px(x, z, oy=0, ox=0):
    return (ox + (x - P.X_MIN) * S, oy + (z - P.Z_MIN) * S)


def colour(i, j):
    k, h = KN[R.K[i, j]], R.H[i, j]
    if k == "void":
        return (18, 18, 24)
    if k == "water":
        return (40, 120, 200)
    if k == "canal":
        return (90, 170, 220)
    if k == "swim":
        return (120, 220, 255)
    if k == "cage":
        return (170, 230, 240)
    if k in ("wall",):
        return (150, 95, 70) if h < 30 else (110, 70, 55)
    if k == "hedge":
        return (50, 120, 50)
    if k == "column":
        return (235, 225, 200)
    if k == "post":
        return (190, 80, 200)
    if k == "ladder":
        return (150, 105, 50)
    if k == "spawn":
        z = j + P.Z_MIN
        return (230, 170, 170) if z < 0 else (170, 185, 235)
    if k == "stone":
        return (210, 200, 150)
    if k == "bridge":
        return (220, 200, 160)
    t = (h - 18) / 8.0
    base = (int(205 + 30 * t), int(190 + 30 * t), int(150 + 30 * t))
    if k == "stair":
        return tuple(int(c * 0.8) for c in base)
    return base


def board(d, oy, dim=1.0):
    for i in range(P.NX):
        for j in range(P.NZ):
            a, b = px(i + P.X_MIN, j + P.Z_MIN, oy)
            col = tuple(int(v * dim) for v in colour(i, j))
            d.rectangle([a, b, a + S - 1, b + S - 1], fill=col)
            if R.UK[i, j] == P.UKINDS["roof"] and dim == 1.0:
                d.line([(a, b + S - 1), (a + S - 1, b)], fill=(120, 100, 80))
            if R.UK[i, j] == P.UKINDS["deck"] and dim == 1.0:
                d.rectangle([a + 1, b + 1, a + S - 2, b + S - 2], outline=(80, 80, 80))


def bowl(d, oy):
    board(d, oy)
    for (x, z), r in R.stair.items():
        a, b = px(x, z, oy)
        cx, cy = a + S / 2, b + S / 2
        dx, dz = {"+x": (1, 0), "-x": (-1, 0), "+z": (0, 1), "-z": (0, -1)}[r]
        d.line([(cx - dx * 2, cy - dz * 2), (cx + dx * 2, cy + dz * 2)], fill=(40, 40, 40), width=2)
    # the carrier's line
    for zl in (-P.CARRIER_LINE, P.CARRIER_LINE):
        a, b = px(-36, zl + (0 if zl > 0 else 1), oy)
        c, e = px(37, zl + (0 if zl > 0 else 1), oy)
        for s in range(int(a), int(c), 8):
            d.line([(s, b), (s + 4, b)], fill=(240, 60, 200), width=2)
    # the posts
    for post in P.POSTS:
        x, y, z = post["at"]
        a, b = px(x, z, oy)
        d.ellipse([a - 7, b - 7, a + 7, b + 7], outline=(255, 255, 255), width=2)
        d.text((a + 9, b - 6), f"{post['name']} y{y}", fill=(255, 255, 255))
    # spawn points
    for team, (x, y, z, yaw) in P.SPAWNS.items():
        a, b = px(x, z, oy)
        d.polygon([(a, b - 5), (a + 5, b), (a, b + 5), (a - 5, b)], fill=TEAM[team], outline=(255, 255, 255))
    labels = [(-34, 10, "balcony 20"), (-29, -1, "porch 24"), (-40, -3, "bridge 24"), (19, -14, "the Minaret's garden 20"),
              (-14, -14, "the court 20"), (-34, 22, "west garden"), (16, 22, "east garden"), (-1, 30, "canal"),
              (-34, 44, "back garden"), (-6, 59, "spawn house, deck 32"), (-12, 36, "arcade, roof 24")]
    for x, z, t in labels:
        a, b = px(x, z, oy)
        d.text((a, b), t, fill=(20, 20, 20))
    d.text((6, oy + 4), "1. THE BOARD — ground (sand, by height), void (black), water (blue), canal (pale blue), walls (brown), hedges and planters (green),"
           " arcade roofs (hatched), stairs (ticks), posts (purple, circled),", fill=(255, 255, 255))
    d.text((6, oy + 16), "   the swim columns (cyan, caged), ladders (brown), parkour stones (pale), spawn patios (team colour) under their decks (boxed),"
           " the carrier's line (magenta dashes)", fill=(255, 255, 255))


ROUTES = [
    ("spawn to the Cistern down the canal", [(10, 52), (10, 43), (4, 40), (4, 8), (0, 4)], (90, 170, 255), 4),
    ("spawn to the Mirador by the west garden and blue's stair", [(-10, 52), (-15, 43), (-30, 36), (-26, 12), (-26, 6), (-30, 1), (-41, 1)], (250, 220, 90), 3),
    ("spawn to the Minaret by the east garden", [(10, 52), (15, 43), (30, 36), (32, 12), (30, 3)], (240, 120, 60), 3),
    ("the roof walk: three stones up, the arcade roof to the court", [(11, 47), (11, 40), (11, 38), (11, 18)], (200, 120, 255), 3),
    ("the Mirador's other stair: red's, from the north balcony", [(-26, -12), (-26, -6), (-26, -2)], (250, 220, 90), 2),
]


def routes(d, oy, lines):
    board(d, oy, dim=0.5)
    for k, (name, pts, col, w) in enumerate(ROUTES):
        d.line([tuple(v + S / 2 for v in px(x, z, oy)) for x, z in pts], fill=col, width=w)
        a, b = 8, oy + 24 + 13 * k
        d.rectangle([a, b + 3, a + 14, b + 8], fill=col)
        d.text((a + 20, b), name, fill=(255, 255, 255))
    y = oy + H + 6
    for ln in lines:
        d.text((10, y), ln[:125], fill=(230, 230, 230))
        y += 13
    d.text((6, oy + 4), "2. THE ROUTES — blue's (red's are the same mirrored); the checker's walks below, in blocks, water counted double",
           fill=(255, 255, 255))


def section(d, top, band, axis, fixed, title):
    """A true-scale section: the ground's columns, the roofs and decks over them, the water."""
    d.rectangle([0, top, W, top + band], fill=(215, 228, 240))
    lo, hi = (P.X_MIN, P.X_MAX) if axis == "x" else (P.Z_MIN, P.Z_MAX)
    n = hi - lo + 1
    s = min(S, (W - 20) / n)
    y0 = 8
    py = lambda y: top + band - 10 - (y - y0) * s
    sx = lambda u: 10 + (u - lo) * s
    for u in range(lo, hi + 1):
        i, j = (P.ix(u), P.iz(fixed)) if axis == "x" else (P.ix(fixed), P.iz(u))
        k, h = KN[R.K[i, j]], R.H[i, j]
        if k == "void":
            pass
        elif k == "water":
            floor = P.CISTERN["floor"] if abs(u) < 10 and abs(fixed) < 10 else h - 3
            d.rectangle([sx(u), py(h + 1), sx(u + 1) - 1, py(floor + 1)], fill=(40, 120, 200))
            d.rectangle([sx(u), py(floor + 1), sx(u + 1) - 1, py(y0)], fill=(150, 140, 120))
        elif k == "canal":
            d.rectangle([sx(u), py(h + 1), sx(u + 1) - 1, py(h)], fill=(90, 170, 220))
            d.rectangle([sx(u), py(h), sx(u + 1) - 1, py(y0)], fill=(170, 160, 130))
        elif k in ("swim",):
            d.rectangle([sx(u), py(h + 1), sx(u + 1) - 1, py(P.CISTERN["floor"] + 1)], fill=(120, 220, 255))
            d.rectangle([sx(u), py(P.CISTERN["floor"] + 1), sx(u + 1) - 1, py(y0)], fill=(150, 140, 120))
        elif k == "cage":
            d.rectangle([sx(u), py(h + 1), sx(u + 1) - 1, py(P.CISTERN["water"] + 1)], fill=(190, 235, 245))
            d.rectangle([sx(u), py(P.CISTERN["water"] + 1), sx(u + 1) - 1, py(P.CISTERN["floor"] + 1)], fill=(40, 120, 200))
            d.rectangle([sx(u), py(P.CISTERN["floor"] + 1), sx(u + 1) - 1, py(y0)], fill=(150, 140, 120))
        elif k in ("column", "bridge") or (k == "post" and abs(u) > 30 and axis == "x"):
            base = P.G if k == "column" else h - 1
            d.rectangle([sx(u), py(h + 1), sx(u + 1) - 1, py(base + 1)], fill=colour(i, j))
            if k == "column":
                d.rectangle([sx(u), py(P.G + 1), sx(u + 1) - 1, py(y0)], fill=(200, 190, 150))
        else:
            d.rectangle([sx(u), py(h + 1), sx(u + 1) - 1, py(y0)], fill=colour(i, j))
        if R.U[i, j] >= 0:
            col = (190, 160, 120) if R.UK[i, j] == P.UKINDS["roof"] else (160, 160, 170)
            d.rectangle([sx(u), py(R.U[i, j] + 1), sx(u + 1) - 1, py(R.U[i, j])], fill=col)
    for yy in range(y0, 40, 4):
        d.line([(4, py(yy)), (8, py(yy))], fill=(0, 0, 0))
        d.text((W - 26, py(yy) - 6), str(yy), fill=(90, 90, 90))
    d.text((10, top + 4), title, fill=(0, 0, 0))


def main(out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lines = C.main()
    lines = [ln for ln in lines if not ln.startswith("   ")]
    band = 40 * S
    T = 13 * len(lines) + 12
    im = Image.new("RGB", (W, 2 * H + T + 2 * band + 12), (0, 0, 0))
    d = ImageDraw.Draw(im)
    bowl(d, 0)
    routes(d, H + 4, lines)
    section(d, 2 * H + T + 8, band, "z", 0, "3a. NORTH TO SOUTH down the axis, true scale: red's spawn house, the canal under the arcades' level, the court, the Cistern and its tower, blue's")
    section(d, 2 * H + T + 10 + band, band, "x", 0, "3b. WEST TO EAST through the posts, true scale: the Mirador's pad and bridge over the void, the porch, the court, the Cistern, the Minaret's garden")
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
