"""The plan drawn before any terrain, in three panels:

1. the surface — every place as its polygon, filled by kind; every route as its polyline with the y it is
   graded to at each bend; the river and Millbrook; the glass clouds as outlines;
2. under the mountain — the cavern, the lake, the Lower Gate, the tunnels with their y, the Deep Stair, with
   the mountain's foot and the summits faint above them;
3. a section west to east along z = -18, from Crownhold through Wendholm to the river, the cavern under it.

Red's half is drawn and named; blue's is its half-turn, drawn paler.

    python3 sketch.py <out.png>
"""
import math
import sys

from PIL import Image, ImageDraw

import plan as P

S = 3
W, H = (P.X_MAX - P.X_MIN + 1) * S, (P.Z_MAX - P.Z_MIN + 1) * S
FILL = {"citadel": (170, 160, 150), "objective": (200, 150, 60), "town": (205, 170, 130), "plaza": (230, 205, 160),
        "water": (90, 140, 210), "valley": (150, 190, 110), "cavern": (90, 80, 75), "cavern-water": (60, 90, 150),
        "spawn": (200, 70, 70)}


def px(x, z, oy=0):
    return ((x - P.X_MIN + 0.5) * S, (z - P.Z_MIN + 0.5) * S + oy)


def pale(c, k=0.45):
    return tuple(int(v + (255 - v) * k) for v in c)


def both(poly):
    return [(poly, False), ([P.rot(x, z) for x, z in poly], True)]


def label(d, x, z, text, oy, fill=(0, 0, 0)):
    tx, tz = px(x, z, oy)
    d.text((tx + 1, tz + 1), text, fill=(255, 255, 255))
    d.text((tx, tz), text, fill=fill)


def surface(d, oy):
    d.rectangle([0, oy, W, oy + H], fill=(120, 150, 95))
    for poly, blue in both(P.FOOT):
        d.polygon([px(x, z, oy) for x, z in poly], fill=pale((150, 140, 120), 0.3 if blue else 0), outline=(90, 80, 70))
    for s in P.SUMMITS:
        for poly, blue in both(s["poly"]):
            d.polygon([px(x, z, oy) for x, z in poly], fill=pale((185, 175, 160), 0.3 if blue else 0), outline=(80, 70, 60))
    for p in P.PLACES:
        if p["kind"] in ("cavern", "cavern-water", "spawn"):
            continue
        for poly, blue in both(p["poly"]):
            c = FILL[p["kind"]]
            d.polygon([px(x, z, oy) for x, z in poly], fill=pale(c, 0.45 if blue else 0) if p["kind"] != "valley" else None,
                      outline=(40, 30, 20))
    for poly in P.FIELDS:
        for q, blue in both(poly):
            d.polygon([px(x, z, oy) for x, z in q], fill=pale((200, 190, 90), 0.4 if blue else 0), outline=(120, 110, 40))
    # the river
    for sgn in (-1, 1):
        d.line([px(P.river_x(z) + sgn * P.RIVER_HALF, z, oy) for z in range(P.Z_MIN, P.Z_MAX + 1)], fill=(40, 80, 170), width=2)
    pts = [px(P.river_x(z), z, oy) for z in range(P.Z_MIN, P.Z_MAX + 1)]
    d.line(pts, fill=(80, 130, 220), width=int(2 * P.RIVER_HALF * S) - 4)
    for q, blue in both(P.TARN):
        d.polygon([px(x, z, oy) for x, z in q], fill=(80, 130, 220), outline=(40, 80, 170))
    for brook in (P.BROOK, [(*P.rot(x, z), y) for x, z, y in P.BROOK]):
        d.line([px(x, z, oy) for x, z, y in brook], fill=(80, 130, 220), width=4)
    for (x, z) in P.FALLS:
        for fx, fz in ((x, z), P.rot(x, z)):
            d.ellipse([px(fx - 2, fz - 2, oy), px(fx + 2, fz + 2, oy)], fill=(255, 255, 255), outline=(40, 80, 170))
    # routes with their heights at the bends
    colours = {"road": (120, 70, 30), "path": (150, 100, 50), "stair": (90, 60, 40)}
    for r in P.ROUTES:
        for pts, blue in ((r["pts"], False), ([(*P.rot(x, z), y) for x, z, y in r["pts"]], True)):
            c = colours[r["kind"]]
            d.line([px(x, z, oy) for x, z, y in pts], fill=pale(c, 0.4) if blue else c, width=2 * r["half"] + 1)
            if not blue:
                for x, z, y in pts[::2] + [pts[-1]]:
                    label(d, x + 1, z - 2, str(y), oy, (60, 20, 0))
    # objectives, spawns, points
    for (x, z), mark in ((P.MON_A, "A"), (P.SPAWN_TOP, "S")):
        for fx, fz in ((x, z), P.rot(x, z)):
            col = (200, 30, 30) if fx < 0 else (40, 70, 200)
            d.ellipse([px(fx - 3, fz - 3, oy), px(fx + 3, fz + 3, oy)], fill=col, outline=(255, 255, 255))
            d.text(px(fx - 1, fz - 2, oy), mark, fill=(255, 255, 255))
    # the bridge and the fords
    b = P.BRIDGE
    d.rectangle([px(b["x0"], -3, oy), px(-1 - b["x0"], 2, oy)], fill=(160, 160, 160), outline=(60, 60, 60))
    for z in P.FORDS:
        d.line([px(P.river_x(z) - 7, z, oy), px(P.river_x(z) + 7, z, oy)], fill=(200, 200, 180), width=3)
    # clouds
    for (x, z, y, L, Wd, a) in P.CLOUDS:
        for fx, fz, fa in ((x, z, a), (*P.rot(x, z), a)):
            c, s_ = math.cos(math.radians(fa)), math.sin(math.radians(fa))
            ring = [(fx + L / 2 * math.cos(t) * c - Wd / 2 * math.sin(t) * s_,
                     fz + L / 2 * math.cos(t) * s_ + Wd / 2 * math.sin(t) * c) for t in [i * math.pi / 12 for i in range(24)]]
            d.line([px(qx, qz, oy) for qx, qz in ring + ring[:1]], fill=(255, 255, 255), width=1)
    for p in P.PLACES:
        if p["kind"] in ("cavern", "cavern-water", "spawn"):
            continue
        cx = sum(q[0] for q in p["poly"]) / len(p["poly"]); cz = sum(q[1] for q in p["poly"]) / len(p["poly"])
        label(d, cx - 8, cz, p["name"], oy)
    for p in P.POINTS:
        if p["key"] in ("bridge", "mill", "minedoor"):
            label(d, p["at"][0] - 6, p["at"][1] + 2, p["name"], oy)
    d.text((6, oy + 4), "1. THE SURFACE  - polygons: places filled by kind; lines: routes, numbers the y they are graded to;"
           " white outlines: glass clouds", fill=(0, 0, 0))


def underground(d, oy):
    d.rectangle([0, oy, W, oy + H], fill=(45, 42, 40))
    for poly, blue in both(P.FOOT):
        d.polygon([px(x, z, oy) for x, z in poly], outline=(90, 85, 80))
    for s in P.SUMMITS:
        for poly, blue in both(s["poly"]):
            d.polygon([px(x, z, oy) for x, z in poly], outline=(110, 105, 100))
    for key in ("underhall", "mere", "lowergate"):
        p = [q for q in P.PLACES if q["key"] == key][0]
        for poly, blue in both(p["poly"]):
            d.polygon([px(x, z, oy) for x, z in poly], fill=pale(FILL[p["kind"]], 0.25 if blue else 0), outline=(200, 190, 170))
    for t in P.TUNNELS:
        for pts, blue in ((t["pts"], False), ([(*P.rot(x, z), y) for x, z, y in t["pts"]], True)):
            d.line([px(x, z, oy) for x, z, y in pts], fill=(220, 170, 90) if not blue else (150, 120, 80), width=2 * t["half"] + 1)
            if not blue:
                for x, z, y in pts:
                    label(d, x + 1, z - 2, str(y), oy, (120, 60, 0))
    for (x, z), mark in ((P.MON_B, "B"), (P.SPAWN_LOW, "S"), (P.DEEP_STAIR, "D")):
        for fx, fz in ((x, z), P.rot(x, z)):
            col = (200, 30, 30) if fx < 0 else (40, 70, 200)
            d.ellipse([px(fx - 3, fz - 3, oy), px(fx + 3, fz + 3, oy)], fill=col, outline=(255, 255, 255))
            d.text(px(fx - 1, fz - 2, oy), mark, fill=(255, 255, 255))
    for p in P.PLACES:
        if p["kind"] in ("cavern", "cavern-water", "spawn"):
            cx = sum(q[0] for q in p["poly"]) / len(p["poly"]); cz = sum(q[1] for q in p["poly"]) / len(p["poly"])
            label(d, cx - 8, cz + 4, p["name"], oy, (255, 230, 180))
    for p in P.POINTS:
        if p["key"] in ("temple", "stair", "gallery"):
            label(d, p["at"][0] - 6, p["at"][1] + 4, p["name"], oy, (255, 230, 180))
    d.text((6, oy + 4), "2. UNDER THE MOUNTAIN  - floor 20; Deepmere at 19; tunnels with their y; B monument, S lower spawn,"
           " D the Deep Stair; faint: the surface above", fill=(255, 255, 255))


def section(d, oy, hgt):
    """West to east along z = -18, drawn from the plan's numbers."""
    d.rectangle([0, oy, W, oy + hgt], fill=(200, 220, 240))

    def py(y):
        return oy + hgt - (y - 0) * hgt / 128.0

    prof = [(-120, 78), (-104, 96), (-100, 98), (-63, 98), (-62, 90), (-60, 87), (-58, 86), (-57, 83), (-55, 82),
            (-52, 82), (-49, 74), (-45, 70), (-41, 61), (-37, 60), (-34, 56), (-31, 56), (-28, 47), (-24, 45),
            (-8, 43), (-6, 40), (5, 40), (7, 43)]
    poly = [(px(x, 0)[0], py(y)) for x, y in prof] + [(px(7, 0)[0], py(0)), (px(-120, 0)[0], py(0))]
    d.polygon(poly, fill=(140, 125, 105), outline=(60, 50, 40))
    d.rectangle([px(-6, 0)[0], py(40), px(5, 0)[0], py(35)], fill=(80, 130, 220))
    # the cavern and the Deep Stair
    d.rectangle([px(-104, 0)[0], py(40), px(-50, 0)[0], py(20)], fill=(60, 55, 50))
    d.rectangle([px(-89, 0)[0], py(98), px(-83, 0)[0], py(20)], fill=(90, 80, 70), outline=(200, 190, 170))
    d.rectangle([px(-100, 0)[0], py(19), px(-90, 0)[0], py(14)], fill=(60, 90, 150))
    for x, y, t in ((-84, 100, "Crownhold 98"), (-61, 90, "leg 4"), (-55, 85, "leg 3"), (-41, 64, "leg 2"),
                    (-34, 59, "leg 1"), (-20, 47, "the Vale 43-46"), (-4, 43, "river 40"), (-82, 30, "Underhall floor 20"),
                    (-98, 22, "Deepmere 19"), (-82, 70, "Deep Stair")):
        d.text((px(x, 0)[0], py(y)), t, fill=(0, 0, 0))
    for y in range(0, 128, 20):
        d.line([(0, py(y)), (8, py(y))], fill=(0, 0, 0))
        d.text((10, py(y) - 6), str(y), fill=(0, 0, 0))
    d.text((6, oy + 4), "3. SECTION west-east along z = -18 (red half): the citadel, the Wend's legs as shelves, the vale,"
           " the cavern 60 blocks under the court", fill=(0, 0, 0))


def main(out):
    hs = 128 * 3
    im = Image.new("RGB", (W, 2 * H + hs + 8), (255, 255, 255))
    d = ImageDraw.Draw(im)
    surface(d, 0)
    underground(d, H + 4)
    section(d, 2 * H + 8, hs)
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
