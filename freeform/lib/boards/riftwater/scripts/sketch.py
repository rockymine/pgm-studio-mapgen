"""Draw the plan from above, before any terrain exists: places, routes, objectives and spawns, both halves.

    python3 sketch.py <out.png>
"""
import sys

from PIL import Image, ImageDraw

import plan as P

S = 4  # pixels per block
W, H = (P.X_MAX - P.X_MIN + 1) * S, (P.Z_MAX - P.Z_MIN + 1) * S


def px(x, z):
    return ((x - P.X_MIN) * S, (z - P.Z_MIN) * S)


COL = {"ridge": (120, 110, 90), "north_wood": (60, 110, 60), "town": (190, 120, 100), "village": (170, 140, 90),
       "fields": (215, 200, 110)}
ROUTE = {"street": (90, 90, 90), "lane": (140, 100, 60), "path": (100, 70, 40)}


def both(pts):
    return [pts, [(P.mirror_x(x), z) for x, z in pts]]


def main(out):
    img = Image.new("RGB", (W, H), (150, 185, 120))
    d = ImageDraw.Draw(img)
    # the rift
    d.rectangle([px(-P.RIFT_HALF, P.Z_MIN), px(P.RIFT_HALF, P.Z_MAX + 1)], fill=(20, 20, 30))
    for p in P.PLACES:
        c = COL.get(p["key"])
        if "poly" in p and c:
            for pts in both(p["poly"]):
                d.polygon([px(*q) for q in pts], fill=c, outline=(40, 40, 40))
    for p in P.PLACES:
        if p["key"] == "pond":
            for pts in both([p["at"]]):
                (x, z), r = pts[0], p["r"]
                d.ellipse([px(x - r, z - r * 0.8), px(x + r, z + r * 0.8)], fill=(60, 110, 200))
        if p["key"] in ("river", "cave", "mine"):
            col = {"river": (60, 110, 200), "cave": (40, 40, 40), "mine": (110, 80, 50)}[p["key"]]
            wid = {"river": 6, "cave": 3, "mine": 2}[p["key"]] * S
            for pts in both(p["line"]):
                d.line([px(*q) for q in pts], fill=col, width=wid)
    for r in P.ROUTES:
        for pts in both(r["pts"]):
            d.line([px(*q) for q in pts], fill=ROUTE[r["kind"]], width=3 * S if r["kind"] == "street" else 2 * S)
    for p in P.PLACES:
        if "at" in p and p["key"] not in ("pond",):
            for pts in both([p["at"]]):
                x, z = pts[0]
                r = p["r"]
                d.ellipse([px(x - r, z - r), px(x + r, z + r)], outline=(0, 0, 0), width=2)
    for team, sx, colr in (("red", 1, (220, 40, 40)), ("blue", -1, (40, 80, 230))):
        for key, (x, z) in P.MONUMENTS.items():
            x = x if sx == 1 else P.mirror_x(x)
            d.rectangle([px(x - 1, z - 1), px(x + 1, z + 1)], fill=(0, 0, 0), outline=colr, width=3)
        x, z = P.SPAWN
        x = x if sx == 1 else P.mirror_x(x)
        d.ellipse([px(x - 4, z - 4), px(x + 4, z + 4)], fill=colr)
    for p in P.PLACES:
        if "at" in p:
            x, z = p["at"]
        elif "poly" in p:
            x = sum(q[0] for q in p["poly"]) / len(p["poly"]); z = sum(q[1] for q in p["poly"]) / len(p["poly"])
        else:
            x, z = p["line"][len(p["line"]) // 2]
        d.text(px(x - 6, z + 2), p["name"], fill=(0, 0, 0))
    img.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
