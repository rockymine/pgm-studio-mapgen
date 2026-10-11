"""The plan drawn before any terrain: islands as discs shaded by height (the higher, the paler), bridges as
lines, balloons as rings, the two airships as hulls. Red's half is named; blue's is its half-turn.

    python3 sketch.py <out.png>
"""
import sys

from PIL import Image, ImageDraw

import plan as P

S = 4


def main(out):
    W, H = (P.X_MAX - P.X_MIN + 1) * S, (P.Z_MAX - P.Z_MIN + 1) * S
    im = Image.new("RGB", (W, H), (150, 190, 230))
    d = ImageDraw.Draw(im)

    def px(x, z):
        return ((x - P.X_MIN + 0.5) * S, (z - P.Z_MIN + 0.5) * S)

    isl = {i["key"]: i for i in P.ISLANDS}
    for f, team in ((lambda x, z: (x, z), (200, 40, 40)), (P.rot, (40, 70, 200))):
        for a, b in P.BRIDGES:
            d.line([px(*f(*isl[a]["at"])), px(*f(*isl[b]["at"]))], fill=(110, 70, 30), width=5)
        for i in P.ISLANDS:
            x, z = f(*i["at"])
            r = i["r"]
            g = int(60 + 2.2 * (i["top"] - 56))
            d.ellipse([px(x - r, z - r), px(x + r, z + r)], fill=(40, g, 40), outline=(30, 30, 30), width=2)
        for x, z, y, r in P.DEBRIS:
            x, z = f(x, z)
            d.ellipse([px(x - r, z - r), px(x + r, z + r)], fill=(120, 120, 110))
        for x, z, y, kind in P.BALLOONS:
            x, z = f(x, z)
            d.ellipse([px(x - 5, z - 5), px(x + 5, z + 5)], outline=(230, 120, 30), width=3)
        a = P.ALBATROSS
        p0, p1 = px(*f(a["x"] - 3, a["z0"])), px(*f(a["x"] + 3, a["z1"]))
        d.rectangle([min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])], fill=(90, 60, 30))
        for key in ("highmoor", "lantern", "gardens"):
            x, z = f(*isl[key]["at"])
            d.ellipse([px(x - 2, z - 2), px(x + 2, z + 2)], fill=team)
    c = P.CONCORD
    d.rectangle([px(c["x0"], -5), px(c["x1"], 4)], fill=(120, 80, 40), outline=(40, 20, 10), width=2)
    for i in P.PLACES:
        x, z = i["at"]
        d.text(px(x - 8, z + 2), i["name"], fill=(0, 0, 0))
        if "top" in isl.get(i["key"], {}):
            d.text(px(x - 3, z - 6), str(isl[i["key"]]["top"]), fill=(255, 255, 255))
    d.text((8, 8), "Cloudhaven - the plan. Discs: islands (paler = higher, number = grass height). Brown lines: bridges.",
           fill=(0, 0, 0))
    d.text((8, 20), "Orange rings: balloons. Brown hulls: the Albatross (moored) and the Concord (centre). Dots: spawn and monuments.",
           fill=(0, 0, 0))
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
