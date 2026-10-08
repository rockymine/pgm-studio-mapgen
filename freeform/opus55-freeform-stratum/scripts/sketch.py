"""The plan drawn before anything was built, in three panels:

1. the city — every mass as its footprint, shaded by the height of its top (paler is higher), the skyways,
   the objectives; the gaps between masses are what players bridge;
2. the land — the lake, the fragments of the city stuck into the ground drawn as their turned footprints,
   the spawn's pylons, and the city's outline faint above;
3. a section west to east along z = 0 and along z = -48: the city's masses at their heights, the cloud sea,
   the kill height, the land.

Red's half is named; blue's is its mirror image.

    python3 sketch.py <out.png>
"""
import math
import sys

from PIL import Image, ImageDraw

import plan as P

S = 3
W, H = (P.X_MAX - P.X_MIN + 1) * S, (P.Z_MAX - P.Z_MIN + 1) * S


def px(x, z, oy=0):
    return ((x - P.X_MIN + 0.5) * S, (z - P.Z_MIN + 0.5) * S + oy)


def both(poly):
    return [poly, [P.mir(x, z) for x, z in poly]]


def shade(y):
    g = int(90 + (y - 60) * 3)
    return (g, g, min(255, g + 8))


def city_masses():
    """Every footprint in the city with its top's height, for the panels."""
    out = [(m["poly"], m["y1"], m["name"]) for m in P.MASSES]
    for p in P.PYLONS:
        out.append((p, 75, ""))
    for c in P.COLUMNS:
        x, z = c["c"]
        h = P.COLUMN_HALF
        out.append((P.rect(x - h, z - h, x + h, z + h), c["top"], ""))
    g = P.GATE
    out.append((P.rect(g["x0"], g["z0"], g["x1"], g["z1"]), g["y1"], "the Gate"))
    out.append((P.LENS["outer"], P.LENS["y1"], "the Lens"))
    cx, cz = P.ZIGGURAT["c"]
    for r, y0, y1 in P.ZIGGURAT["tiers"]:
        out.append((P.rect(cx - r, cz - r, cx + r, cz + r), y1, ""))
    out.append((P.CANTILEVER["arm"], P.CANTILEVER["arm_y"][1], ""))
    return out


def label(d, x, z, text, oy, fill=(0, 0, 0)):
    tx, tz = px(x, z, oy)
    d.text((tx + 1, tz + 1), text, fill=(255, 255, 255))
    d.text((tx, tz), text, fill=fill)


def panel_city(d, oy):
    d.rectangle([0, oy, W, oy + H], fill=(180, 205, 235))
    for poly, top, name in sorted(city_masses(), key=lambda t: t[1]):
        for q in both(poly):
            d.polygon([px(x, z, oy) for x, z in q], fill=shade(top), outline=(30, 30, 40))
    for q in both(P.ATRIUM_COURT):
        d.polygon([px(x, z, oy) for x, z in q], fill=(150, 150, 150), outline=(30, 30, 40))
    for q in both(P.LENS["inner"]):
        d.polygon([px(x, z, oy) for x, z in q], fill=(180, 205, 235), outline=(30, 30, 40))
    for q in both(P.REACTOR_HOLLOW):
        d.polygon([px(x, z, oy) for x, z in q], fill=(120, 120, 125), outline=(30, 30, 40))
    for s in P.SKYWAYS:
        for q in both(s["pts"]):
            d.line([px(x, z, oy) for x, z in q], fill=(230, 120, 40), width=2 * s["half"] * S + S)
    for (x, z), mark, col in ((P.SPAWN, "S", (200, 30, 30)), ((-53, -49), "M", (200, 30, 30)), ((-56, 48), "C", (200, 30, 30))):
        for fx, fz in ((x, z), P.mir(x, z)):
            c = col if fx < 0 else (40, 70, 200)
            d.ellipse([px(fx - 3, fz - 3, oy), px(fx + 3, fz + 3, oy)], fill=c, outline=(255, 255, 255))
            d.text(px(fx - 1, fz - 2, oy), mark, fill=(255, 255, 255))
    for p in P.PLACES:
        if p["layer"] != "city":
            continue
        xs = [q[0] for q in p["poly"]]; zs = [q[1] for q in p["poly"]]
        label(d, min(xs), max(zs) + 1, p["name"], oy)
    d.text((6, oy + 4), "1. THE CITY, y 62-118: footprints shaded by the height of their tops (paler is higher); orange:"
           " skyways; S spawn, M monument, C core. Everything else is bridged.", fill=(0, 0, 0))


def turned_rect(cx, cz, w, l, yaw):
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    pts = [(-w / 2, -l / 2), (w / 2, -l / 2), (w / 2, l / 2), (-w / 2, l / 2)]
    return [(cx + u * c - v * s, cz + u * s + v * c) for u, v in pts]


def panel_land(d, oy):
    d.rectangle([0, oy, W, oy + H], fill=(120, 160, 80))
    # swathes of colour as the land will be painted: drawn as bands
    for k, col in enumerate(((190, 80, 70), (220, 200, 70), (160, 110, 190), (110, 140, 70))):
        for z in range(P.Z_MIN + 6 * k, P.Z_MAX, 26):
            pts = [px(x, z + 5 * math.sin(x / 13.0 + k), oy) for x in range(P.X_MIN, P.X_MAX + 1, 4)]
            d.line(pts, fill=col, width=5)
    d.polygon([px(x, z, oy) for x, z in P.LAKE], fill=(70, 120, 200), outline=(30, 70, 150))
    for f in P.FRAGMENTS:
        x, z = f["at"]
        w_, l_ = f["size"][0], f["size"][2]
        for q in both(turned_rect(x, z, w_, l_, f["yaw"])):
            d.polygon([px(a, b, oy) for a, b in q], fill=(170, 170, 175), outline=(40, 40, 40))
    for p in P.PYLONS:
        for q in both(p):
            d.polygon([px(x, z, oy) for x, z in q], fill=(150, 150, 155), outline=(40, 40, 40))
    for poly, top, name in city_masses():
        for q in both(poly):
            d.line([px(x, z, oy) for x, z in q + q[:1]], fill=(255, 255, 255), width=1)
    for f in P.FRAGMENTS:
        label(d, f["at"][0] - 6, f["at"][1] + 4, f["kind"], oy)
    label(d, -10, 0, "the Mirror", oy)
    d.text((6, oy + 4), "2. THE LAND, y 6-40: the lake, swathes of colour, the city's fragments stuck in the ground"
           " (grey, turned); white: the city above", fill=(0, 0, 0))


def panel_section(d, oy, hgt):
    d.rectangle([0, oy, W, oy + hgt], fill=(200, 220, 245))

    def py(y):
        return oy + hgt - y * hgt / 128.0
    # land
    prof = [(x, 22 + 10 * math.sin(x / 17.0) + 5 * math.sin(x / 7.0)) for x in range(P.X_MIN, P.X_MAX + 1, 2)]
    prof = [(x, min(y, P.LAKE_Y - 2) if abs(x + 0.5) < 27 else y) for x, y in prof]
    d.polygon([(px(x, 0)[0], py(y)) for x, y in prof] + [(W, py(0)), (0, py(0))], fill=(110, 150, 70))
    d.rectangle([px(-27, 0)[0], py(P.LAKE_Y), px(26, 0)[0], py(P.LAKE_Y - 3)], fill=(70, 120, 200))
    # cloud sea and the kill height
    d.rectangle([0, py(P.CLOUD_Y[1]), W, py(P.CLOUD_Y[0])], fill=(240, 245, 250))
    d.line([(0, py(P.KILL_Y)), (W, py(P.KILL_Y))], fill=(200, 30, 30), width=2)
    d.text((8, py(P.KILL_Y) - 12), f"below y {P.KILL_Y}: killed", fill=(200, 30, 30))
    # the city along z = 0 (and the Obelisk along z = -48, drawn lighter)
    segs = [((-93, -67), (76, 88)), ((-87, -73), (76, 80)), ((-49, -45), (62, 106)), ((-26, 25), (74, 80))]
    for p in P.PYLONS[:2]:
        segs.append(((p[0][0], p[1][0]), (18, 75)))
    for (x0, x1), (y0, y1) in segs:
        for a, b in ((x0, x1), (P.mir(x1, 0)[0], P.mir(x0, 0)[0])):
            d.rectangle([px(a, 0)[0], py(y1), px(b, 0)[0] + S, py(y0)], fill=(120, 120, 128), outline=(30, 30, 40))
    for a, b in ((-59, -54), (53, 58)):
        d.rectangle([px(a, 0)[0], py(118), px(b, 0)[0] + S, py(78)], fill=(170, 170, 178), outline=(80, 80, 90))
    for y in range(0, 128, 20):
        d.line([(0, py(y)), (8, py(y))], fill=(0, 0, 0))
        d.text((10, py(y) - 6), str(y), fill=(0, 0, 0))
    for x, y, t in ((-80, 92, "the Atrium"), (-47, 110, "a Column"), (-12, 84, "the Forum"), (-60, 121, "the Obelisk (z -48)"),
                    (-90, 60, "pylons"), (-14, 50, "cloud sea 44-54"), (-20, 12, "the land and the Mirror")):
        d.text((px(x, 0)[0], py(y)), t, fill=(0, 0, 0))
    d.text((6, oy + 4), "3. SECTION west-east along z = 0: the city between 62 and 118, the clouds, the kill height,"
           " the land", fill=(0, 0, 0))


def main(out):
    hs = 128 * 3
    im = Image.new("RGB", (W, 2 * H + hs + 8), (255, 255, 255))
    d = ImageDraw.Draw(im)
    panel_city(d, 0)
    panel_land(d, H + 4)
    panel_section(d, 2 * H + 8, hs)
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
