"""Hollowcrown from above with the plan written on it: each place's polygon and name, the spawns, the
monuments and the tunnels drawn over the ground.

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
    shade = 0.65 + 0.5 * (ytop - 40) / 60.0
    hs = np.roll(ytop, 1, 0) - ytop + np.roll(ytop, 1, 1) - ytop
    shade = shade - 0.05 * np.clip(hs, -3, 3)
    col = col * np.clip(shade, 0.5, 1.2)[..., None]
    col[~has] = (18, 18, 26)
    im = Image.fromarray(np.transpose(np.clip(col, 0, 255).astype(np.uint8), (1, 0, 2))).resize((sx * S, sz * S), Image.NEAREST)
    d = ImageDraw.Draw(im)

    def px(x, z):
        return ((x - x0 + 0.5) * S, (z - z0 + 0.5) * S)

    def both(pts):
        return [pts, [P.rot(x, z) for x, z in pts]]
    for poly in [p["poly"] for p in P.PLACES]:
        for q in both(poly):
            d.line([px(*c) for c in q + q[:1]], fill=(255, 255, 255), width=1)
    for t in P.TUNNELS:
        for q in both([(x, z) for x, z, y in t["pts"]]):
            d.line([px(*c) for c in q], fill=(230, 160, 60), width=2)
    for f, colr in ((lambda x, z: (x, z), (230, 40, 40)), (P.rot, (50, 90, 240))):
        for m in (P.MON_A, P.MON_B):
            x, z = f(*m)
            d.polygon([px(x, z - 3), px(x + 3, z), px(x, z + 3), px(x - 3, z)], fill=(20, 0, 30), outline=colr)
        for sp in (P.SPAWN_TOP, P.SPAWN_LOW):
            x, z = f(*sp)
            d.ellipse([px(x - 3, z - 3), px(x + 3, z + 3)], fill=colr, outline=(255, 255, 255), width=2)
    for p in P.PLACES:
        x = sum(q[0] for q in p["poly"]) / len(p["poly"]); z = sum(q[1] for q in p["poly"]) / len(p["poly"])
        tx, tz = px(x - 8, z + 4)
        d.text((tx + 1, tz + 1), p["name"], fill=(0, 0, 0))
        d.text((tx, tz), p["name"], fill=(255, 255, 255))
    for p in P.POINTS:
        x, z = p["at"]
        tx, tz = px(x - 6, z + 3)
        d.text((tx + 1, tz + 1), p["name"], fill=(0, 0, 0))
        d.text((tx, tz), p["name"], fill=(255, 230, 160))
    d.rectangle([0, 0, 470, 32], fill=(18, 18, 26))
    d.text((8, 8), "Hollowcrown - red (west) is named; blue (east) is its half-turn. White: the plan's polygons.", fill=(255, 255, 255))
    d.text((8, 20), "Diamond: monuments A (Eyrie) and B (Hall of Echoes). Discs: top and lower spawns. Orange: tunnels.", fill=(255, 255, 255))
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
