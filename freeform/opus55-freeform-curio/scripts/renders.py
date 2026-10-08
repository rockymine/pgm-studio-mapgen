"""Draw Curio Square: the studio's round-trip reads, the square from two corners, the whole valley with its town
and mountains, the middle with the fountain and the cage, and a sheet of all forty-eight plots, each drawn alone
with its name and its builder.

    python3 renders.py <build-dir> <deliverable-root> "<round-trip command>"
"""
import os
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw

import plan as P
import plotkit as K
import render_iso
import sketch
from mc import World, B

HERE = os.path.dirname(os.path.abspath(__file__))
build, root, rt = sys.argv[1], sys.argv[2], sys.argv[3]
region = os.path.join(root, "world", "region")
out = os.path.join(root, "renders")
os.makedirs(out, exist_ok=True)
COLOUR = sketch.COLOUR


def run(args):
    r = subprocess.run(rt.split() + args, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED", " ".join(args), r.stderr[-600:])


def o(name):
    return os.path.join(out, name)


def trim(path, pad=16):
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))).save(path)


def sheet(path):
    """Every plot alone, from the south-east, in the square's order, captioned with its name and builder."""
    tiles = []
    tmp = os.path.join(out, "_tile.png")
    for (i, j), (builder, row) in sorted(sketch.layout().items()):
        if not row or not os.path.exists(os.path.join(HERE, "..", "plots", builder, row["file"])):
            tiles.append((None, "missing", builder))
            continue
        m = K.load(os.path.join(HERE, "..", "plots", builder, row["file"]))
        w = World(-1, -1, 13, 13, sy=K.Y_MAX + 8)
        w.fill(-1, 0, -1, 11, 1, 11, B.STONEBRICK)
        K.draw(w, m, 0, 0, 2)
        render_iso.render(w.ids, w.dat, w.x0, w.z0, tmp, 6, "se", None, 0, K.Y_MAX + 7)
        trim(tmp, 4)
        tiles.append((Image.open(tmp).copy(), m.NAME, builder))
    os.remove(tmp)
    cw, ch = 230, 270
    cols = 8
    rows = (len(tiles) + cols - 1) // cols
    img = Image.new("RGB", (cols * cw, rows * ch + 30), (34, 36, 44))
    d = ImageDraw.Draw(img)
    for k, (im, name, builder) in enumerate(tiles):
        x, y = (k % cols) * cw, (k // cols) * ch
        if im:
            im.thumbnail((cw - 10, ch - 40))
            img.paste(im, (x + (cw - im.width) // 2, y + 6 + (ch - 40 - im.height)))
        d.rectangle([x + 6, y + ch - 30, x + 16, y + ch - 20], fill=COLOUR[builder])
        d.text((x + 20, y + ch - 32), name.replace("The ", ""), fill=(240, 240, 240))
        d.text((x + 20, y + ch - 19), builder, fill=(170, 170, 170))
    d.text((8, rows * ch + 8), "the forty-eight plots, each drawn alone from the south-east, in the square's order row by row",
           fill=(220, 220, 220))
    img.save(path)


run(["--topdown", region, o("01-topdown-material.png"), "--material", "--scale", "2"])
run(["--heightmap", region, o("02-heightmap.png"), "--scale", "2"])
x0, z0, ids, dat = render_iso.load(build)
render_iso.render(ids, dat, x0, z0, o("30-iso-the-valley.png"), 2, "sw", None, 0, 199)
render_iso.render(ids, dat, x0, z0, o("31-iso-the-square-sw.png"), 6, "sw", (-P.WALL - 1, -P.WALL - 1, P.WALL + 1, P.WALL + 1), 58, 100)
render_iso.render(ids, dat, x0, z0, o("32-iso-the-square-ne.png"), 6, "ne", (-P.WALL - 1, -P.WALL - 1, P.WALL + 1, P.WALL + 1), 58, 100)
render_iso.render(ids, dat, x0, z0, o("33-iso-the-fountain-and-cage.png"), 10, "sw", (-20, -20, 20, 20), 58, 90)
for n in ("30-iso-the-valley.png", "31-iso-the-square-sw.png", "32-iso-the-square-ne.png", "33-iso-the-fountain-and-cage.png"):
    trim(o(n))
sheet(o("40-the-forty-eight-plots.png"))
print("renders written to", out)
