"""Hollow Mesa from above with the plan written on it: each place's name where it stands, the spawns, the
cores, and the ways under the rock (the adit, the Chimney, the Old Workings) drawn over it.

    python3 annotate.py <build-dir> <out.png>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

import plan as P
import render_iso
import underground as U

S = 4


def main(build, out):
    x0, z0, ids, dat = render_iso.load(build)
    sx, sy, sz = ids.shape
    table = render_iso.colour_table()
    # the top block of each column, shaded by height so the relief reads
    nonair = ids > 0
    ytop = sy - 1 - np.argmax(nonair[:, ::-1, :], axis=1)
    has = nonair.any(axis=1)
    X, Z = np.meshgrid(np.arange(sx), np.arange(sz), indexing="ij")
    tid = ids[X, ytop, Z]
    tdt = dat[X, ytop, Z]
    col = table[tid, tdt & 15]
    shade = 0.8 + 0.3 * (ytop - 41) / 40.0
    hs = np.roll(ytop, 1, 0) - ytop + np.roll(ytop, 1, 1) - ytop
    shade = shade - 0.05 * np.clip(hs, -3, 3)
    col = col * np.clip(shade, 0.5, 1.2)[..., None]
    col[~has] = (18, 18, 26)
    img = np.transpose(np.clip(col, 0, 255).astype(np.uint8), (1, 0, 2))
    im = Image.fromarray(img).resize((sx * S, sz * S), Image.NEAREST)
    d = ImageDraw.Draw(im)

    def px(x, z):
        return ((x - x0 + 0.5) * S, (z - z0 + 0.5) * S)

    def both(pts):
        return [pts, [P.rot(x, z) for x, z in pts]]

    # the ways under the rock: the Chimney in black, the drifts in brown
    for line in both([(p[0], p[2]) for p in U.CHIMNEY]):
        d.line([px(*q) for q in line], fill=(10, 10, 10), width=3)
    for pts in (U.ADIT, U.WORKINGS):
        for line in both([(p[0], p[2]) for p in pts]):
            d.line([px(*q) for q in line], fill=(150, 90, 30), width=3)
    for team, f, colr in (("red", lambda x, z: (x, z), (230, 40, 40)), ("blue", P.rot, (50, 90, 240))):
        c = P.CORE
        cx, cz = f((c["x0"] + c["x1"]) / 2, (c["z0"] + c["z1"]) / 2)
        d.rectangle([px(cx - 2, cz - 2), px(cx + 2, cz + 2)], fill=(0, 0, 0), outline=colr, width=3)
        tx, tz = f(P.THROAT[0], P.THROAT[1])
        d.ellipse([px(tx - 3, tz - 3), px(tx + 3, tz + 3)], outline=colr, width=2)
        x, z = f(P.SPAWN[0], P.SPAWN[2])
        d.ellipse([px(x - 3, z - 3), px(x + 3, z + 3)], fill=colr, outline=(255, 255, 255), width=2)
    for p in P.PLACES:
        if "at" in p:
            x, z = p["at"]
        elif "poly" in p:
            x = sum(q[0] for q in p["poly"]) / len(p["poly"]); z = sum(q[1] for q in p["poly"]) / len(p["poly"])
        else:
            x, z = p["line"][len(p["line"]) // 2]
        if p["key"] in ("needles", "adobe"):
            z += 6
        tx, tz = px(x - 8, z + 3)
        d.text((tx + 1, tz + 1), p["name"], fill=(0, 0, 0))
        d.text((tx, tz), p["name"], fill=(255, 255, 255))
    d.text((8, 8), "Hollow Mesa - red (west) is named; blue (east) is its half-turn. Black: the Chimney. Brown: the Bench Adit and the Old Workings. Circle: the Throat's hole.",
           fill=(255, 255, 255))
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
