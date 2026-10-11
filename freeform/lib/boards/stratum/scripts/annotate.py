"""Stratum from above with the plan written on it: each place's footprint and name, the spawns, the
monuments and cores, the skyways.

    python3 annotate.py <build-dir> <out.png>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

import plan as P
import render_iso

S = 4


def main(build, out):
    x0, z0, ids, dat = render_iso.load(build)
    sx, sy, sz = ids.shape
    table = render_iso.colour_table()
    nonair = ids > 0
    ytop = sy - 1 - np.argmax(nonair[:, ::-1, :], axis=1)
    has = nonair.any(axis=1)
    X, Z = np.meshgrid(np.arange(sx), np.arange(sz), indexing="ij")
    col = table[ids[X, ytop, Z], dat[X, ytop, Z] & 15]
    shade = 0.6 + 0.5 * (ytop - 20) / 100.0
    hs = np.roll(ytop, 1, 0) - ytop + np.roll(ytop, 1, 1) - ytop
    shade = shade - 0.05 * np.clip(hs, -3, 3)
    col = col * np.clip(shade, 0.5, 1.2)[..., None]
    col[~has] = (18, 18, 26)
    im = Image.fromarray(np.transpose(np.clip(col, 0, 255).astype(np.uint8), (1, 0, 2))).resize((sx * S, sz * S), Image.NEAREST)
    d = ImageDraw.Draw(im)

    def px(x, z):
        return ((x - x0 + 0.5) * S, (z - z0 + 0.5) * S)

    def both(pts):
        return [pts, [P.mir(x, z) for x, z in pts]]
    for p in P.PLACES:
        for q in both(p["poly"]):
            d.line([px(*c) for c in q + q[:1]], fill=(255, 255, 255) if p["layer"] == "city" else (120, 200, 255), width=1)
    for s_ in P.SKYWAYS:
        for q in both(s_["pts"]):
            d.line([px(*c) for c in q], fill=(230, 120, 40), width=2)
    for f, colr in ((lambda x, z: (x, z), (230, 40, 40)), (P.mir, (50, 90, 240))):
        for (x, z), mark in ((P.SPAWN, "S"), ((-54, -50), "M"), ((-56, 48), "C")):
            x, z = f(x, z)
            d.ellipse([px(x - 3, z - 3), px(x + 3, z + 3)], fill=colr, outline=(255, 255, 255), width=2)
            d.text(px(x - 1, z - 2), mark, fill=(255, 255, 255))
    for p in P.PLACES:
        xs = [q[0] for q in p["poly"]]; zs = [q[1] for q in p["poly"]]
        tx, tz = px(min(xs), max(zs) + 1)
        d.text((tx + 1, tz + 1), p["name"], fill=(0, 0, 0))
        d.text((tx, tz), p["name"], fill=(255, 255, 255))
    d.rectangle([0, 0, 470, 32], fill=(18, 18, 26))
    d.text((8, 8), "Stratum - red (west) is named; blue (east) is its mirror. White: the city's footprints; pale blue: the lake.", fill=(255, 255, 255))
    d.text((8, 20), "S spawn, M monument, C core. Orange: skyways. Every other gap between masses is bridged.", fill=(255, 255, 255))
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
