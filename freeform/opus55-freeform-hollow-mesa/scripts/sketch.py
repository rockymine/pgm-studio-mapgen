"""Draw Hollow Mesa's plan from above before any terrain exists: the canyon's bands, the places, the routes,
the core and the spawn, both halves (blue's as red's half-turn).

    python3 sketch.py <out.png>
"""
import sys

from PIL import Image, ImageDraw

import plan as P

S = 4
W, H = (P.X_MAX - P.X_MIN + 1) * S, (P.Z_MAX - P.Z_MIN + 1) * S


def px(x, z):
    return ((x - P.X_MIN) * S, (z - P.Z_MIN) * S)


def both(pts):
    return [pts, [P.rot(x, z) for x, z in pts]]


def main(out):
    img = Image.new("RGB", (W, H), (205, 120, 70))      # mesa top
    d = ImageDraw.Draw(img)
    # the canyon's bands, row by row, both sides
    for z in range(P.Z_MIN, P.Z_MAX + 1):
        c = P.canyon_x(z)
        for x0, x1, col in ((c - 22, c + 22, (225, 175, 120)),
                            (c - 37, c - 27, (180, 110, 75)), (c + 27, c + 37, (180, 110, 75))):
            d.line([px(x0, z), px(x1, z)], fill=col, width=S)
        d.line([px(c - 1.5, z), px(c + 1.5, z)], fill=(60, 110, 200), width=S)
    COL = {"needles": (150, 70, 50), "adobe": (235, 215, 160)}
    for p in P.PLACES:
        if "poly" in p and p["key"] in COL:
            for pts in both(p["poly"]):
                d.polygon([px(*q) for q in pts], fill=COL[p["key"]], outline=(40, 40, 40))
        if "line" in p and p["key"] in ("wash", "bench", "mule"):
            col = {"wash": (230, 190, 130), "bench": (120, 70, 40), "mule": (90, 60, 40)}[p["key"]]
            for pts in both(p["line"]):
                d.line([px(*q) for q in pts], fill=col, width=(10 if p["key"] == "wash" else 3) * S // 2)
    # the arch, rim to rim
    d.rectangle([px(-44, -3), px(43, 2)], outline=(60, 30, 20), width=3)
    for r in P.ROUTES:
        col = {"street": (90, 90, 90), "road": (150, 100, 60), "track": (120, 80, 50)}[r["kind"]]
        for pts in both(r["pts"]):
            d.line([px(*q) for q in pts], fill=col, width=2 * S)
    for p in P.PLACES:
        if "at" in p:
            for (x, z) in (p["at"], P.rot(*p["at"])):
                rr = p["r"]
                d.ellipse([px(x - rr, z - rr), px(x + rr, z + rr)], outline=(0, 0, 0), width=2)
    for team, f, col in (("red", lambda x, z: (x, z), (220, 40, 40)), ("blue", P.rot, (40, 80, 230))):
        x, z = f(P.SPAWN[0], P.SPAWN[2])
        d.ellipse([px(x - 4, z - 4), px(x + 4, z + 4)], fill=col)
        cx, cz = f((P.CORE["x0"] + P.CORE["x1"]) / 2, (P.CORE["z0"] + P.CORE["z1"]) / 2)
        d.rectangle([px(cx - 2, cz - 2), px(cx + 2, cz + 2)], fill=(20, 20, 20), outline=col, width=3)
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
