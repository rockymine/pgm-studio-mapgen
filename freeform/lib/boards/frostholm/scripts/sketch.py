"""Draw Frostholm's plan from above before any terrain: the crescent, the islands, the lead along the
diagonal, the places and the objectives, both halves (blue's as red's half-turn).

    python3 sketch.py <out.png>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

import plan as P
from noise import polyline_distance

S = 4


def main(out):
    xs = np.arange(P.X_MIN, P.X_MAX + 1); zs = np.arange(P.Z_MIN, P.Z_MAX + 1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    land = np.zeros(X.shape, bool)
    spine = [(a, b) for a, b, _ in P.SPINE]
    widths = [w for _, _, w in P.SPINE]
    for (ax, az, aw), (bx, bz, bw) in zip(P.SPINE[:-1], P.SPINE[1:]):
        d, t = polyline_distance(X, Z, [(ax, az), (bx, bz)])
        L = np.hypot(bx - ax, bz - az)
        land |= d < aw + (bw - aw) * (t / L)
    for isl in P.ISLANDS:
        (cx, cz), (rx, rz) = isl["at"], isl["r"]
        land |= np.hypot((X - cx) / rx, (Z - cz) / rz) < 1
    red = (X + Z < -1) | ((X + Z == -1) & (X <= -1))
    land = np.where(red, land, land[::-1, ::-1])
    img = np.zeros(X.shape + (3,), np.uint8)
    img[:] = (200, 225, 240)                                       # sea ice
    img[np.abs(X + Z + 1) < 6] = (60, 100, 170)                    # the lead
    img[land] = (235, 238, 240)                                    # snow-covered land
    im = Image.fromarray(np.transpose(img, (1, 0, 2))).resize((X.shape[0] * S, X.shape[1] * S), Image.NEAREST)
    d = ImageDraw.Draw(im)

    def px(x, z):
        return ((x - P.X_MIN) * S, (z - P.Z_MIN) * S)
    for r in P.ROUTES:
        for pts in (r["pts"], [P.rot(*q) for q in r["pts"]]):
            d.line([px(*q) for q in pts], fill=(120, 90, 60), width=2 * S)
    for p in P.PLACES:
        for (x, z) in (p["at"], P.rot(*p["at"])):
            d.ellipse([px(x - p["r"], z - p["r"]), px(x + p["r"], z + p["r"])], outline=(0, 0, 0), width=2)
        x, z = p["at"]
        d.text(px(x - 8, z + 2), p["name"], fill=(0, 0, 0))
    for f, col in ((lambda x, z: (x, z), (220, 40, 40)), (P.rot, (40, 80, 230))):
        x, z = f(P.SPAWN[0], P.SPAWN[2]); d.ellipse([px(x - 4, z - 4), px(x + 4, z + 4)], fill=col)
        x, z = f(*P.CORE); d.rectangle([px(x - 2, z - 2), px(x + 2, z + 2)], fill=(20, 20, 20), outline=col, width=3)
        x, z = f(*P.MONUMENT); d.rectangle([px(x - 1, z - 1), px(x + 1, z + 1)], fill=(20, 20, 20), outline=col, width=3)
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
